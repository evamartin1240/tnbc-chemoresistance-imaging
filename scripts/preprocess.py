#!/usr/bin/env python
"""
Preprocessing pipeline — ALL files.

Handles two LSM layouts:
  A) (tiles, timepoints, 2_substacks, 33ch, 1024, 1024) — original + multi-tp
  B) (tiles, 33ch, 1024, 1024) — single-timepoint files (no substack)

Skips files that already have output in OUT_DIR.
"""

import numpy as np
from pathlib import Path
import tifffile as tiff
from skimage.measure import regionprops
import torch
from cellpose import models
import pandas as pd
import sys

sys.path.insert(0, str(Path(__file__).parent))
from PhasorUnmixing import (
    load_pure_phasors,
    image_to_components_multi_harm_less_coords,
)

# =========================
# Paths and constants
# =========================

BASE = Path("/baldig/bioprojects2/dikshans/chemores/data")

FILES = [
    # --- Original files ---
    ("CNTL-MB231", "Control", BASE / "original_files" / "CNTL-MB231.lsm"),
    ("TAMO-MB231", "Chemoresistant", BASE / "original_files" / "TAMO-MB231.lsm"),

    # --- Testset: Control ---
    ("CNTL", "Control", BASE / "testset" / "CNTL.lsm"),
    ("CNTL_2", "Control", BASE / "testset" / "CNTL_2.lsm"),
    ("CNTL_75uM_p1", "Control", BASE / "testset" / "CNTL_75uM_CNTL_15uM_2025_10_09__12_22_04__p1.lsm"),
    ("CNTL_75uM_p2", "Control", BASE / "testset" / "CNTL_75uM_CNTL_15uM_2025_10_09__12_22_04__p2.lsm"),
    ("CNTL_75uM_p3", "Control", BASE / "testset" / "CNTL_75uM_CNTL_15uM_2025_10_09__12_22_04__p3.lsm"),
    ("CNTL_75uM_p4", "Control", BASE / "testset" / "CNTL_75uM_CNTL_15uM_2025_10_09__12_22_04__p4.lsm"),

    # --- New batch: Chemoresistant ---
    ("TAMO_p1", "Chemoresistant", BASE / "new_batch" / "TAMO-TAMO_CNTL_CNTL-TAMO_2025_11_16__12_46_08__p1.lsm"),
    ("TAMO_p2", "Chemoresistant", BASE / "new_batch" / "TAMO-TAMO_CNTL_CNTL-TAMO_2025_11_16__12_46_08__p2.lsm"),
]

PURE_PHASOR_PATH = Path("/home/emartinl/chemores/scripts/Lipi Modified spectra.npz")

OUT_DIR = Path("/baldig/bioprojects2/emartinl/chemores/preprocessed_phasor")
OUT_DIR.mkdir(parents=True, exist_ok=True)

CROP_SIZE = 512
HALF = CROP_SIZE // 2
N_SPECTRAL = 32
GOOD_SUBSTACK = 1
SPECTRAL_CHANNELS = list(range(32))
BRIGHTFIELD_CHANNEL = 32

DYE_LIST = [
    "LipiBlue", "342", "BODIPY", "pHrodo", "TMRM", "Lyso", "Tubulin",
]

# =========================
# Helpers
# =========================

def read_spectral_frame_substack(series, tile, time):
    """For files with 2 substacks: series[tile, time] → list of 2 pages."""
    frame_list = series[tile, time]
    frame = np.stack([p.asarray() for p in frame_list], axis=0)
    stack = frame[GOOD_SUBSTACK]
    return stack[SPECTRAL_CHANNELS]


def read_spectral_frame_single(series, tile):
    """For single-timepoint files with no substacks: series[tile] → (33, h, w)."""
    page = series[tile]
    stack = page.asarray()  # (33, 1024, 1024)
    return stack[SPECTRAL_CHANNELS]


def crop_cell(components, masks, label):
    h, w = masks.shape
    prop = next(p for p in regionprops(masks) if p.label == label)
    cy, cx = map(int, prop.centroid)

    y1, y2 = cy - HALF, cy + HALF
    x1, x2 = cx - HALF, cx + HALF

    crop = np.zeros((components.shape[0], CROP_SIZE, CROP_SIZE),
                    dtype=components.dtype)

    sy1, sy2 = max(0, y1), min(h, y2)
    sx1, sx2 = max(0, x1), min(w, x2)

    dy1, dy2 = sy1 - y1, sy1 - y1 + (sy2 - sy1)
    dx1, dx2 = sx1 - x1, sx1 - x1 + (sx2 - sx1)

    crop[:, dy1:dy2, dx1:dx2] = components[:, sy1:sy2, sx1:sx2]

    mask_crop = np.zeros((CROP_SIZE, CROP_SIZE), dtype=bool)
    mask_crop[dy1:dy2, dx1:dx2] = masks[sy1:sy2, sx1:sx2] == label

    crop *= mask_crop[None, :, :]
    return crop


# =========================
# Main
# =========================

def main():
    print("Using GPU:", torch.cuda.is_available(), flush=True)

    pure_phasors = load_pure_phasors(
        pure_spectra_path=str(PURE_PHASOR_PATH),
        dye_list=DYE_LIST,
        ch_vec=np.arange(N_SPECTRAL),
        use_extra_coord=False,
    )
    print("Loaded pure phasors", flush=True)

    cellpose_model = models.CellposeModel(gpu=True)

    for sample_name, sample_group, lsm_path in FILES:

        # Skip if already preprocessed
        out_path = OUT_DIR / f"{sample_name}_cells.npy"
        if out_path.exists():
            print(f"\n### SKIPPING {sample_name} — already exists: {out_path} ###", flush=True)
            continue

        print(f"\n### Processing: {sample_name} ({sample_group}) — {lsm_path} ###", flush=True)

        all_cells = []
        all_meta = []
        cell_id = 0

        with tiff.TiffFile(lsm_path) as tif:
            series = tif.series[0]
            shape = series.shape
            ndim = len(shape)

            # Detect layout
            if ndim == 4:
                # (tiles, 33, H, W) — single timepoint, no substacks
                n_tiles = shape[0]
                n_times = 1
                has_substacks = False
            elif ndim == 5:
                # (tiles, timepoints, 33, H, W) — multi-tp with substacks
                n_tiles = shape[0]
                n_times = shape[1]
                has_substacks = True
            else:
                print(f"  WARNING: unexpected ndim={ndim}, shape={shape}. Skipping.", flush=True)
                continue

            print(f"  Layout: {n_tiles} tiles × {n_times} timepoints (substacks={has_substacks})", flush=True)

            for tile in range(n_tiles):
                for t in range(n_times):

                    print(f"  tile {tile+1}/{n_tiles}, time {t+1}/{n_times} ...", end=" ", flush=True)

                    if has_substacks:
                        spectral = read_spectral_frame_substack(series, tile, t)
                    else:
                        spectral = read_spectral_frame_single(series, tile)

                    components = image_to_components_multi_harm_less_coords(
                        spectral, pure_phasors, use_extra_coord=False
                    )

                    cellpose_input = np.stack([
                        components[DYE_LIST.index("Tubulin")],
                        components[DYE_LIST.index("342")],
                    ], axis=-1)

                    masks, flows, styles = cellpose_model.eval(cellpose_input)

                    labels = np.unique(masks)
                    labels = labels[labels != 0]
                    print(f"{len(labels)} cells", flush=True)

                    for label in labels:
                        crop = crop_cell(components, masks, label)
                        all_cells.append(crop)
                        all_meta.append({
                            "cell_id": cell_id,
                            "sample": sample_name,
                            "group": sample_group,
                            "tile": tile,
                            "time": t,
                            "cell_label": int(label),
                        })
                        cell_id += 1

        if len(all_cells) == 0:
            print(f"  No cells found for {sample_name}; skipping save.", flush=True)
            continue

        all_cells = np.stack(all_cells)
        print(f"  Final shape: {all_cells.shape} ({cell_id} cells)", flush=True)

        np.save(out_path, all_cells)
        print(f"  Saved: {out_path}", flush=True)

        meta_path = OUT_DIR / f"{sample_name}_cells_meta.csv"
        pd.DataFrame(all_meta).to_csv(meta_path, index=False)
        print(f"  Saved: {meta_path}", flush=True)


if __name__ == "__main__":
    main()
