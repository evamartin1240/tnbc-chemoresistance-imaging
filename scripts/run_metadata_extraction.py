"""Script to extract metadata from LSM microscopy files."""

import logging
from pathlib import Path
from argparse import ArgumentParser
from src.data.extract_lsm_raw_metadata import extract_batch_metadata

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """Extract metadata from LSM files."""
    parser = ArgumentParser(description="Extract LSM metadata")
    parser.add_argument(
        "--data_dir",
        type=Path,
        required=True,
        help="Directory containing LSM files",
    )
    parser.add_argument(
        "--output_dir",
        type=Path,
        default=Path("results/metadata"),
        help="Output directory for metadata",
    )
    
    args = parser.parse_args()
    
    # TODO: Implement metadata extraction
    logger.info(f"Extracting metadata from {args.data_dir}")
    logger.info(f"Saving results to {args.output_dir}")


if __name__ == "__main__":
    main()
