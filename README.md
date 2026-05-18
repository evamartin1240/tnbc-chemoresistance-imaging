# TNBC Chemoresistance Imaging Analysis

A comprehensive computational pipeline for analyzing triple-negative breast cancer (TNBC) chemoresistance through imaging data. This project combines image preprocessing, CNN-based feature extraction, domain adaptation, and temporal analysis to identify biomarkers of chemoresistance.

## Project Overview

This repository contains analysis of confocal microscopy imaging data from TNBC cells across multiple timepoints and experimental conditions. The pipeline implements:

- **Data Preprocessing**: LSM metadata extraction, image cropping, and normalization
- **Feature Extraction**: CNN embeddings and hand-crafted feature computation
- **Batch Effect Analysis**: PCA and t-SNE visualization with batch correction
- **Temporal Analysis**: File-level and cell-level temporal pattern analysis
- **Domain Adaptation**: DANN (Domain Adversarial Neural Networks) for cross-batch harmonization
- **Augmentation Studies**: Assessment of data augmentation impact on model robustness

## Project Structure

```
├── README.md                          # This file
├── requirements.txt                   # Python dependencies (pip)
├── environment.yml                    # Conda environment definition
├── .gitignore                         # Git ignore rules
│
├── notebooks/                         # Jupyter notebooks for exploratory analysis
│   ├── 01_data_exploration.ipynb
│   ├── 02_preprocessing_checks.ipynb
│   ├── 03_replication_prev_results.ipynb
│   ├── 04_timecourse_analysis.ipynb
│   ├── 05_cross_file_validation.ipynb
│   ├── 06_pca_batch_features_analysis.ipynb
│   ├── 07_pca_cnn_embeddings_analysis.ipynb
│   ├── 08_normalisation_strategies.ipynb
│   ├── 09_augmentation_robustness.ipynb
│   ├── 10_temporal_file_level_analysis.ipynb
│   └── 11_temporal_cell_level_analysis.ipynb
│
├── src/                               # Python source code modules
│   ├── data/                          # Data loading and preprocessing
│   │   ├── __init__.py
│   │   ├── extract_lsm_raw_metadata.py
│   │   ├── load_crops.py
│   │   └── dataset.py
│   │
│   ├── preprocessing/                 # Image preprocessing utilities
│   │   ├── __init__.py
│   │   ├── segmentation.py
│   │   ├── crop_extraction.py
│   │   └── normalisation.py
│   │
│   ├── models/                        # Model architectures and training
│   │   ├── __init__.py
│   │   ├── cnn.py
│   │   ├── dann.py
│   │   └── train_utils.py
│   │
│   ├── analysis/                      # Analysis utilities
│   │   ├── __init__.py
│   │   ├── batch_effects.py
│   │   ├── pca_tsne.py
│   │   ├── temporal_features.py
│   │   └── metrics.py
│   │
│   └── visualisation/                 # Plotting and visualization
│       ├── __init__.py
│       ├── plots.py
│       └── figures.py
│
├── scripts/                           # Standalone scripts for specific analyses
│   ├── run_metadata_extraction.py
│   ├── run_replication.py
│   ├── run_cross_file_validation.py
│   ├── run_normalisation_experiments.py
│   ├── run_augmentation_experiments.py
│   └── run_temporal_analysis.py
│
├── results/                           # Analysis results and outputs
│   ├── metadata/
│   ├── replication/
│   ├── timecourse/
│   ├── cross_file_validation/
│   ├── normalisation/
│   ├── augmentation/
│   └── temporal/
│
├── figures/                           # Generated figures and visualizations
│   ├── data/
│   ├── batch_effects/
│   ├── normalisation/
│   ├── augmentation/
│   └── temporal/
│
├── docs/                              # Documentation
│   ├── dataset_description.md
│   ├── experimental_design.md
│   └── notes.md
│
└── logs/                              # Log files
```

## Installation

### Using Conda (Recommended)

```bash
# Create environment
conda env create -f environment.yml

# Activate environment
conda activate chemores
```

### Using pip

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Quick Start

### 1. Run Data Exploration
```bash
jupyter notebook notebooks/01_data_exploration.ipynb
```

### 2. Preprocessing Validation
```bash
jupyter notebook notebooks/02_preprocessing_checks.ipynb
```

### 3. Batch Effects Analysis
```bash
jupyter notebook notebooks/06_pca_batch_features_analysis.ipynb
```

### 4. Temporal Analysis
```bash
jupyter notebook notebooks/10_temporal_file_level_analysis.ipynb
jupyter notebook notebooks/11_temporal_cell_level_analysis.ipynb
```

## Main Analysis Notebooks

| Notebook | Purpose |
|----------|---------|
| `01_data_exploration.ipynb` | Initial dataset exploration and visualization |
| `02_preprocessing_checks.ipynb` | Validation of preprocessing steps |
| `03_replication_prev_results.ipynb` | Reproduction of previous findings |
| `04_timecourse_analysis.ipynb` | Timecourse data analysis |
| `05_cross_file_validation.ipynb` | Cross-file consistency validation |
| `06_pca_batch_features_analysis.ipynb` | Batch effect analysis with hand-crafted features |
| `07_pca_cnn_embeddings_analysis.ipynb` | Batch effect analysis with CNN embeddings |
| `08_normalisation_strategies.ipynb` | Comparison of normalization approaches |
| `09_augmentation_robustness.ipynb` | Data augmentation impact assessment |
| `10_temporal_file_level_analysis.ipynb` | File-level temporal pattern analysis |
| `11_temporal_cell_level_analysis.ipynb` | Cell-level temporal pattern analysis |

## Requirements

- Python 3.10+
- PyTorch 1.9+
- NumPy, SciPy, Pandas
- scikit-learn, scikit-image
- OpenCV, Matplotlib, Seaborn, Plotly
- Jupyter, JupyterLab

See `requirements.txt` or `environment.yml` for complete dependency list.

## Data

Raw microscopy files are not included in this repository due to file size and access restrictions. To use this pipeline with your own data, ensure it follows the expected format described in `docs/dataset_description.md`.
