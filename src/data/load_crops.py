"""Load and manage image crop data."""

import logging
from pathlib import Path
from typing import List, Optional, Tuple
import numpy as np

logger = logging.getLogger(__name__)


def load_crops(crop_dir: Path) -> np.ndarray:
    """
    Load image crops from a directory.
    
    Args:
        crop_dir: Directory containing crop files
        
    Returns:
        Array of crops (N, C, H, W)
    """
    # TODO: Implement crop loading
    pass


def load_crops_with_metadata(crop_dir: Path) -> Tuple[np.ndarray, List[Dict]]:
    """
    Load crops with associated metadata.
    
    Args:
        crop_dir: Directory containing crops and metadata
        
    Returns:
        Tuple of (crops array, list of metadata dictionaries)
    """
    # TODO: Implement with metadata
    pass
