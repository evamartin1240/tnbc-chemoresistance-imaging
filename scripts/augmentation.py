import os
import random
import numpy as np
import pandas as pd

from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import torchvision.transforms.functional as TF


# -------------------------
# Config
# -------------------------

DATA_DIR = "data/preprocessed"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

FILES = [
    "CNTL-MB231",
    "TAMO-MB231",
    "CNTL_75uM_p1",
    "CNTL_75uM_p2",
    "CNTL_75uM_p3",
    "CNTL_75uM_p4",
    "TAMO_p1",
    "TAMO_p2",
]

LABELS = {
    "CNTL-MB231": 0,
    "CNTL_75uM_p1": 0,
    "CNTL_75uM_p2": 0,
    "CNTL_75uM_p3": 0,
    "CNTL_75uM_p4": 0,
    "TAMO-MB231": 1,
    "TAMO_p1": 1,
    "TAMO_p2": 1,
}

FOLDS = [
    {
        "test": ["CNTL-MB231", "TAMO-MB231"]
    },
    {
        "test": ["CNTL_75uM_p1", "CNTL_75uM_p2", "TAMO_p1"]
    },
    {
        "test": ["CNTL_75uM_p3", "CNTL_75uM_p4", "TAMO_p2"]
    },
]


# -------------------------
# Utils
# -------------------------

def set_seed(seed=42):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


def load_file_data(file_name):
    x_path = os.path.join(DATA_DIR, f"{file_name}.npy")
    meta_path = os.path.join(DATA_DIR, f"{file_name}.csv")

    x = np.load(x_path)
    meta = pd.read_csv(meta_path)

    y = np.full(len(meta), LABELS[file_name], dtype=np.int64)
    file_ids = np.full(len(meta), file_name)

    return x, meta, y, file_ids


def load_timepoint_dataset(timepoint):
    xs, ys, file_ids = [], [], []

    for file_name in FILES:
        x, meta, y, fids = load_file_data(file_name)

        idx = meta["time"].values == timepoint

        xs.append(x[idx])
        ys.append(y[idx])
        file_ids.append(fids[idx])

    x_all = np.concatenate(xs, axis=0)
    y_all = np.concatenate(ys, axis=0)
    file_all = np.concatenate(file_ids, axis=0)

    return x_all, y_all, file_all


# -------------------------
# Dataset
# -------------------------

class CellDataset(Dataset):
    def __init__(self, x, y, augmentation="none"):
        self.x = x.astype(np.float32)
        self.y = y.astype(np.int64)
        self.augmentation = augmentation

    def __len__(self):
        return len(self.y)

    def augment(self, img):
        # img shape: C x H x W
        if self.augmentation == "none":
            return img

        if random.random() < 0.5:
            img = torch.flip(img, dims=[2])  # horizontal flip

        if random.random() < 0.5:
            img = torch.flip(img, dims=[1])  # vertical flip

        if self.augmentation in ["weak", "strong"]:
            noise_std = 0.02 if self.augmentation == "weak" else 0.06
            img = img + torch.randn_like(img) * noise_std

        if self.augmentation == "strong":
            scale = 0.85 + 0.30 * random.random()
            img = img * scale

        return img

    def __getitem__(self, idx):
        img = torch.tensor(self.x[idx])
        img = self.augment(img)
        label = torch.tensor(self.y[idx])
        return img, label


# -------------------------
# Model
# -------------------------

class CompactCNN(nn.Module):
    def __init__(self, in_channels=7):
        super().__init__()

        self.features = nn.Sequential(
            nn.Conv2d(in_channels, 16, kernel_size=3, padding=1),
            nn.BatchNorm2d(16),
            nn.ReLU(),

            nn.Conv2d(16, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),

            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),

            nn.AdaptiveAvgPool2d((1, 1))
        )

        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(32, 2)
        )

    def forward(self, x):
        x = self.features(x)
        x = self.classifier(x)
        return x


# -------------------------
# Training
# -------------------------

def train_model(x_train, y_train, x_test, y_test, augmentation, epochs=10):
    train_ds = CellDataset(x_train, y_train, augmentation=augmentation)
    test_ds = CellDataset(x_test, y_test, augmentation="none")

    train_loader = DataLoader(train_ds, batch_size=64, shuffle=True)
    test_loader = DataLoader(test_ds, batch_size=128, shuffle=False)

    model = CompactCNN().to(DEVICE)
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)
    criterion = nn.CrossEntropyLoss()

    model.train()
    for _ in range(epochs):
        for xb, yb in train_loader:
            xb = xb.to(DEVICE)
            yb = yb.to(DEVICE)

            optimizer.zero_grad()
            preds = model(xb)
            loss = criterion(preds, yb)
            loss.backward()
            optimizer.step()

    model.eval()
    all_preds = []
    all_true = []

    with torch.no_grad():
        for xb, yb in test_loader:
            xb = xb.to(DEVICE)
            preds = model(xb)
            pred_labels = preds.argmax(dim=1).cpu().numpy()

            all_preds.extend(pred_labels)
            all_true.extend(yb.numpy())

    acc = accuracy_score(all_true, all_preds)
    return acc


# -------------------------
# Cross-file experiment
# -------------------------

def run_cross_file(timepoint, augmentation):
    x, y, file_ids = load_timepoint_dataset(timepoint)

    fold_accs = []

    for i, fold in enumerate(FOLDS, start=1):
        test_files = fold["test"]
        train_files = [f for f in FILES if f not in test_files]

        train_idx = np.isin(file_ids, train_files)
        test_idx = np.isin(file_ids, test_files)

        x_train, y_train = x[train_idx], y[train_idx]
        x_test, y_test = x[test_idx], y[test_idx]

        acc = train_model(
            x_train,
            y_train,
            x_test,
            y_test,
            augmentation=augmentation
        )

        fold_accs.append(acc)

        print(
            f"t={timepoint} | {augmentation} | fold {i} | "
            f"acc={acc:.3f} | test={test_files}"
        )

    mean_acc = np.mean(fold_accs)
    std_acc = np.std(fold_accs, ddof=1)

    return fold_accs, mean_acc, std_acc


# -------------------------
# Run
# -------------------------

set_seed(42)

results = []

for timepoint in [0, 14]:
    for aug in ["weak", "strong"]:
        fold_accs, mean_acc, std_acc = run_cross_file(timepoint, aug)

        results.append({
            "timepoint": timepoint,
            "augmentation": aug,
            "fold_1": fold_accs[0],
            "fold_2": fold_accs[1],
            "fold_3": fold_accs[2],
            "mean": mean_acc,
            "std": std_acc
        })

results_df = pd.DataFrame(results)
results_df.to_csv("augmentation_cross_file_results.csv", index=False)

print("\nFinal results:")
print(results_df)