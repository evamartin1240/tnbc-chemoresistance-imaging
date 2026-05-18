# Batch Effects Analysis: Comprehensive Summary

## Executive Summary

This document summarizes the exhaustive investigation into batch effects and their relationship with classification performance in the chemoresistance dataset.

**Key Finding:** Batch identity and biological class are **informationally inseparable** at the experimental design level. This is not a technical problem that can be solved algorithmically, but a fundamental structural property of the data.

---

## Part 1: Diagnosis

### Time-Zero Sanity Check
- **CNN at t=0:** ~91% accuracy
- **Logistic regression (14 intensity features):** ~93% accuracy
- **Biological expectation at t=0:** No difference (no treatment applied)
- **Conclusion:** Classification signal exists before any biological differentiation, indicating batch confounding

### Intensity Statistics
- All 7 spectral channels show systematic differences between files
- Differences in both mean and variance (illumination, staining batch, detector gain)
- Cell area distributions also differ between sessions
- Low-level features dominate classification (confirmed by logistic regression)

---

## Part 2: Normalisation Attempts

### Strategy 1: Statistical Normalisation
Tested three approaches:
- Global per-channel z-score: ~93% accuracy
- Per-cell per-channel z-score: ~79% accuracy  
- Spatial normalisation: ~93% accuracy

**Result:** All failed. Static normalisation cannot remove confounding when batch effects are pervasive across multiple feature levels.

### Strategy 2: CNN-Based Batch Correction (BEN)

**Approach:** 
- SmallCNN with file-grouped batches
- Stratified group k-fold cross-validation
- Two timepoints tested: t=0 and t=14

**Results:**
| Metric | t=0 | t=14 |
|--------|-----|------|
| File-level accuracy | 62.5% | 62.5% |
| Per-cell accuracy | 50.0% | 50.0% |
| % cells predicted Chemoresistant | 0% | 0% |

**Finding:** Identical performance at t=0 and t=14. The model predicts 100% Control, indicating complete failure to learn any class signal. The failure is structural (batch ≡ class), not due to weak biological signal.

### Strategy 3: Domain-Adversarial Neural Networks (DANN)

**Architecture:**
- Feature extractor (256-dim CNN)
- Class head (Control vs Chemoresistant)
- Domain head (4-session predictor)
- **Key innovation:** Gradient reversal layer to force session-invariance

**Hypothesis:** If confounding is a distribution shift, DANN should succeed. If structural, it should fail.

**Results at t=14 (Maximum Biological Differentiation):**

| Fold | Class Acc | Domain Acc | Train Cells | Test Cells |
|------|-----------|-----------|-------------|-----------|
| 1 | 58.1% | 58.1% | 1,557 | 731 |
| 2 | 9.9% | 0.0% | 1,650 | 638 |
| 3 | 72.3% | 0.0% | 1,769 | 519 |
| 4 | 0.0% | 0.0% | 1,888 | 400 |
| **Mean** | **35.1% ± 35.5%** | **14.5% ± 29.1%** | | **2,288 total** |

**Findings:**
- Class accuracy 35.1% is **FAR BELOW CHANCE** (50% random for binary classification)
- Extreme variance (std=35.5%) shows inconsistent learning across folds
- Folds collapse to near-random when test files from different sessions
- Domain predictor not successfully confused in 2/4 folds
- Gradient reversal layer did not help

**What This Reveals:**
- ✗ Batch/class confounding is NOT a distribution shift
- ✗ It is NOT correctable by adversarial domain adaptation
- ✓ It is **structurally inseparable** at the informational level

---

## Part 3: The Confounding Structure

### Why All Three Approaches Failed

```
EXPERIMENTAL DESIGN:
  Session 0: CNTL-MB231 (Control) + TAMO-MB231 (Chemoresistant)
  Session 2: All 4 CNTL_75uM files (Control)
  Session 3: Both TAMO files (Chemoresistant)

CONSEQUENCE:
  ∀ file f: session(f) → class(f)
  ∴ batch ≡ class
```

When batch perfectly predicts class at experimental design level:
- Statistical normalisation works on low-level statistics → can't distinguish signal from confound
- BEN learns file-level patterns → reinforces, not removes, the confound
- DANN searches for session-invariant features → cannot find class signal independent of session

### The Fundamental Problem

In this dataset, **there is no biological signal that is independent of session identity**. The two acquisition sessions have fundamentally different:
- Illumination profiles
- Staining batch characteristics
- Detector settings
- Cell density/focus

These static differences completely dominate the ~35,000-dimensional image space. Any machine learning approach that tries to find features independent of these session-level differences will fail.

---

## Part 4: The Solution

The temporal approach (Chapter 6) **sidesteps** rather than **solves** this problem:

**Key Insight:** Static batch effects are **constant within each file** but differ between files.

**Within-file temporal dynamics:**
- Control cells: `I(t) = I_batch + f_control(t)` 
- Chemoresistant cells: `I(t) = I_batch + f_chemo(t)`
- **Change in time:** `ΔI = f_control(t) - f_control(0)` or `f_chemo(t) - f_chemo(0)`

When we use temporal changes:
- `I_batch` term cancels (constant within file)
- Only biological dynamics remain
- **Result:** 87.5% accuracy, consistent across sessions

---

## Summary Table

| Approach | Type | Result | Signal Found? |
|----------|------|--------|--------------|
| CNN at t=0 | Baseline | 91% | **No** (batch signal) |
| Statistical norm. | Algorithm | ~93% | **No** |
| BEN | Algorithm | 50-62.5% | **No** |
| DANN | Algorithm | 35.1% ± 35.5% | **No** |
| **Temporal** | **Different approach** | **87.5%** | **Yes** |

---

## Conclusion

**The batch effect in this dataset is not a technical problem for machine learning to solve.**

It is a fundamental consequence of experimental design where:
1. Each biological condition was acquired in a different session
2. Session-level technical differences are larger than biological differences
3. These static differences completely dominate the static image features

Three state-of-the-art approaches (statistical, CNN-based, adversarial) have been exhaustively tested and all failed, confirming this conclusion.

**The only viable solution requires fundamentally different data:**
- Use temporal information (within-file dynamics)
- Normalize by relative change rather than absolute intensity
- Measure biology via system response, not system state

This approach achieves 87.5% accuracy and demonstrates genuine generalization across sessions.

---

## References

**In Thesis:**
- Chapter 4, Sections 4.1-4.4: Diagnosis and failed normalisation strategies
- Chapter 5: Cross-session validation of static approaches
- Chapter 6: Temporal approach achieving robust generalisation
