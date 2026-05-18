# Research Notes & Findings

## Key Observations

### Batch Effects
- **Observation**: Strong batch effects detected between microscopy sessions
- **Magnitude**: Silhouette score difference ~0.3 between sessions
- **Impact**: Cross-file model performance drops ~15-20%

### Temporal Dynamics
- **Observation**: Temporal trajectories diverge between chemoresistant and sensitive cells
- **Pattern**: Chemoresistant cells show increased cluster formation over time
- **Timepoint**: Divergence becomes apparent at T2 (48h)

### Normalization Strategies
- **Best performing**: Histogram matching + z-score normalization
- **Improvement**: Cross-file validation accuracy +8-12%

### Augmentation Robustness
- **Robust to**: Small rotations (±5°), mild brightness changes (±10%)
- **Sensitive to**: Large rotations (>15°), strong contrast changes (>20%)

## TODO / In Progress

- [ ] Implement DANN domain adaptation
- [ ] Complete cell-level analysis
- [ ] Generate publication figures
- [ ] Write methods section

## Challenges & Limitations

1. **Limited sample size**: Only N samples per condition
2. **Batch effects**: Strong session-to-session variability
3. **Temporal coverage**: Limited to 5 timepoints over 5 days
4. **Class imbalance**: Unequal numbers of resistant vs. sensitive cells

## Future Directions

1. Larger multicenter dataset with harmonization
2. 3D analysis (z-stack processing)
3. Multimodal analysis (incorporate other biomarkers)
4. Real-time prediction during treatment

## References & Resources

- [Include links to papers, datasets, tools]
- Leica LSM file format: [documentation]
- PyTorch documentation: https://pytorch.org/docs/
- scikit-image docs: https://scikit-image.org/

## Collaborators & Contact

- Lead: E. Martin L.
- [Other team members]

## Data Access & Sharing

- Raw data location: [Internal storage]
- Processed data: Available upon request
- Code: Public repository (this repository)
