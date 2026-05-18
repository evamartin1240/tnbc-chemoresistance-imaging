"""Evaluation metrics and statistical tests."""

import logging
from typing import Dict, Optional, Tuple
import numpy as np
from scipy import stats

logger = logging.getLogger(__name__)


def compute_classification_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
) -> Dict[str, float]:
    """
    Compute classification metrics.
    
    Args:
        y_true: Ground truth labels
        y_pred: Predicted labels
        
    Returns:
        Dictionary with accuracy, precision, recall, F1, etc.
    """
    # TODO: Implement metrics computation
    pass


def compute_roc_auc(
    y_true: np.ndarray,
    y_score: np.ndarray,
) -> Tuple[float, np.ndarray, np.ndarray]:
    """
    Compute ROC-AUC.
    
    Args:
        y_true: Ground truth binary labels
        y_score: Predicted probabilities
        
    Returns:
        Tuple of (auc_score, fpr, tpr)
    """
    # TODO: Implement ROC-AUC computation
    pass


def statistical_test(
    group1: np.ndarray,
    group2: np.ndarray,
    test_type: str = "ttest",
) -> Tuple[float, float]:
    """
    Perform statistical test between groups.
    
    Args:
        group1: First group values
        group2: Second group values
        test_type: Type of test (ttest, mannwhitneyu, wilcoxon)
        
    Returns:
        Tuple of (statistic, p_value)
    """
    # TODO: Implement statistical tests
    pass
