"""Image crop extraction utilities."""

import logging
from typing import List, Tuple, Optional
import numpy as np

logger = logging.getLogger(__name__)


def extract_crops(
    image: np.ndarray,
    mask: np.ndarray,
    crop_size: int = 64,
    padding: int = 5,
) -> List[np.ndarray]:
    """
    Extract crops around segmented objects.
    
    Args:
        image: Input image (H, W, C)
        mask: Segmentation mask with labeled regions
        crop_size: Size of extracted crops
        padding: Padding around object
        
    Returns:
        List of extracted crops
    """
    # TODO: Implement crop extraction
    pass


def extract_crops_with_metadata(
    image: np.ndarray,
    mask: np.ndarray,
    crop_size: int = 64,
    padding: int = 5,
) -> Tuple[List[np.ndarray], List[dict]]:
    """
    Extract crops and compute metadata.
    
    Args:
        image: Input image
        mask: Segmentation mask
        crop_size: Crop size
        padding: Padding
        
    Returns:
        Tuple of (crops list, metadata list)
    """
    # TODO: Implement with metadata (location, intensity, size, etc.)
    pass


def validate_crop_size(crop: np.ndarray, min_size: int = 32) -> bool:
    """
    Check if crop is valid (minimum size, not mostly background).
    
    Args:
        crop: Crop image
        min_size: Minimum acceptable size
        
    Returns:
        True if crop is valid
    """
    # TODO: Implement validation
    pass
