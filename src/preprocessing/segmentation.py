"""Image preprocessing utilities."""

import logging
from typing import Optional, Tuple
import numpy as np

logger = logging.getLogger(__name__)


def segment_cells(image: np.ndarray) -> np.ndarray:
    """
    Segment cells in microscopy image.
    
    Args:
        image: Input microscopy image (H, W) or (H, W, C)
        
    Returns:
        Segmentation mask with labeled regions
    """
    # TODO: Implement cell segmentation
    # Consider: Otsu thresholding, watershed, etc.
    pass


def refine_segmentation(
    image: np.ndarray,
    mask: np.ndarray,
    min_size: int = 50,
) -> np.ndarray:
    """
    Refine segmentation mask by removing small objects.
    
    Args:
        image: Original image
        mask: Segmentation mask
        min_size: Minimum object size in pixels
        
    Returns:
        Refined segmentation mask
    """
    # TODO: Implement refinement
    pass
