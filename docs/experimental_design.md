# Experimental Design

## Overview

This study analyzes the prediction of chemoresistance in triple-negative breast cancer cells using deep learning on confocal microscopy images.

## Research Questions

1. **Can CNN-based features predict chemoresistance?**
   - Train CNN models to classify chemoresistant vs. chemosensitive cells
   - Evaluate on held-out test data

2. **Does the signal generalize across microscopy sessions?**
   - Cross-file validation: train on one microscopy session, test on another
   - Identify and quantify batch effects
   - Implement batch correction strategies

3. **What are the temporal dynamics of chemoresistance?**
   - Analyze changes in cell features over time
   - Identify temporal biomarkers
   - Model cell trajectories

4. **How robust are models to data augmentation?**
   - Test model performance under various augmentations
   - Assess generalization to slightly different imaging conditions

## Experimental Workflow

### Phase 1: Baseline & Replication
- [ ] Explore dataset structure and basic statistics (Notebook 01)
- [ ] Validate preprocessing steps (Notebook 02)
- [ ] Replicate previous CNN results (Notebook 03)

### Phase 2: Batch Analysis
- [ ] Timepoint-specific classification (Notebook 04)
- [ ] Cross-file validation (Notebook 05)
- [ ] PCA/t-SNE batch effect analysis - hand-crafted features (Notebook 06)
- [ ] PCA/t-SNE batch effect analysis - CNN embeddings (Notebook 07)

### Phase 3: Normalization & Augmentation
- [ ] Compare normalization strategies (Notebook 08)
- [ ] Assess augmentation robustness (Notebook 09)

### Phase 4: Temporal Analysis
- [ ] File-level temporal analysis (Notebook 10)
- [ ] Cell-level temporal analysis (Notebook 11)

## Data Splits

### Cross-Validation Strategy
- **Leave-one-file-out (LOFO)**: Train on N-1 microscopy sessions, test on 1
- **Stratified k-fold**: Within-session k-fold cross-validation
- **Temporal splits**: Train on early timepoints, test on later ones

## Model Architectures

### CNN Baseline
- Input: 64x64 RGB or 4-channel images
- Layers: Conv → BatchNorm → ReLU → MaxPool (x3-4)
- Output: Classification logits
- Features: Intermediate layer activations

### DANN (Domain Adversarial NN)
- Feature extractor (CNN)
- Task classifier (chemoresistance prediction)
- Domain classifier (discriminate between microscopy sessions)
- Gradient reversal layer

## Evaluation Metrics

### Classification Metrics
- Accuracy, Precision, Recall, F1-score
- ROC-AUC, PR-AUC
- Confusion matrix

### Batch Effect Metrics
- Silhouette score
- k-BET (k-nearest batch effect test)
- Entropy of batch mixing
- LISI (Local Inverse Simpson's Index)

### Temporal Metrics
- Feature velocity (rate of change)
- Trajectory coherence
- Temporal clustering

## Statistical Analysis

- T-tests / Mann-Whitney U tests for group comparisons
- ANOVA for multi-group comparisons
- Pearson/Spearman correlations
- P-values with multiple testing correction (Bonferroni, FDR)

## Expected Outcomes

1. **Batch effects**: Significant batch effects should be detected between sessions
2. **CNN generalization**: Models should show reduced performance in cross-file validation
3. **Temporal patterns**: Distinct temporal trajectories for chemoresistant vs. sensitive cells
4. **Augmentation robustness**: Model performance degradation under augmentation

## References

- [CNN-based chemoresistance prediction previous work]
- [Domain adaptation methods]
- [Batch effect quantification literature]

## Timeline

- Phase 1-2: Data exploration and replication
- Phase 3: Normalization strategies testing
- Phase 4: Temporal analysis
- Final: Integration and figure generation
