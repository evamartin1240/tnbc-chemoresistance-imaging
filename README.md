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
| `08_normalisation_strategies1.ipynb` | Comparison of normalization approaches - baseline |
| `08_normalisation_strategies2_ben.ipynb` | Batch effect normalization approach |
| `08_normalisation_strategies3_dann.ipynb` | DANN-based normalization approach |
| `09_augmentation_robustness.ipynb` | Data augmentation impact assessment |
| `10_temporal_analysis.ipynb` | File-level temporal pattern analysis |

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
