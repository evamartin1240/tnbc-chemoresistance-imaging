# Dataset Description

## Overview

This dataset contains confocal microscopy images of triple-negative breast cancer (TNBC) cells, specifically MDA-MB-231 cells, acquired under different experimental conditions and timepoints.

## Data Organization

### Directory Structure

```
data/raw/
├── sample_1/
│   ├── metadata.txt
│   ├── channel_1.lsm
│   ├── channel_2.lsm
│   └── channel_3.lsm
├── sample_2/
└── ...
```

## Image Specifications

- **Microscope**: Leica SP8 (or similar confocal system)
- **Format**: LSM (Leica Scan Module) files
- **Channels**: 3-4 fluorescence channels (wavelengths: 405nm, 488nm, 555nm, 640nm)
- **Spatial Resolution**: 
  - X/Y: 0.123 µm/pixel (63x oil objective, 1.4 NA)
  - Z: 0.5-1.0 µm/slice
- **Bit Depth**: 12 or 16-bit
- **Image Size**: ~512x512 or 1024x1024 pixels

## Experimental Conditions

### Timepoints
- T0: Baseline (day 0)
- T1: 24 hours
- T2: 48 hours
- T3: 72 hours
- T4: 96 hours (5 days)

### Treatment Conditions
- **Control**: No chemotherapy
- **Chemoresistant**: Previously exposed to chemotherapy agents
- **Chemosensitive**: Sensitive to chemotherapy

### Cell Types
- MDA-MB-231 (human TNBC)
- [Other cell lines if applicable]

## Sample Information

Each sample is associated with:
- **Sample ID**: Unique identifier (e.g., CTRL_001, CHEM_001)
- **Condition**: Control / Chemoresistant / Chemosensitive
- **Timepoint**: T0-T4
- **Replicate**: Replicate number (1-3)
- **Acquisition Date**: Date of microscopy acquisition
- **Acquisition Parameters**: Laser power, gain, pinhole diameter, dwell time, line averaging

## Preprocessing

Raw LSM files are typically preprocessed:

1. **Channel Registration**: Align multiple channels to correct for spectral bleed-through
2. **Background Subtraction**: Remove noise and instrument background
3. **Normalization**: Equalize intensity across samples and timepoints
4. **Segmentation**: Identify cell regions
5. **Cropping**: Extract individual cell crops (~64x64 pixels)

## Data Availability

Raw microscopy files are not included in this repository due to:
- Large file sizes (LSM files: 50-500 MB each)
- Access restrictions and institutional data policies

Processed crops, features, and analysis results are available in the `results/` directory.

## Citation

If using this dataset, please cite:
[Your citation information]
