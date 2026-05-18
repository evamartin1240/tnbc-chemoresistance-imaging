"""Script to compare normalization strategies."""

import logging
from pathlib import Path
from argparse import ArgumentParser

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """Compare different normalization approaches."""
    parser = ArgumentParser(description="Normalization experiments")
    parser.add_argument(
        "--data_dir",
        type=Path,
        required=True,
        help="Directory containing image data",
    )
    parser.add_argument(
        "--output_dir",
        type=Path,
        default=Path("results/normalisation"),
        help="Output directory for results",
    )
    parser.add_argument(
        "--methods",
        nargs="+",
        default=["zscore", "minmax", "histogram"],
        help="Normalization methods to compare",
    )
    
    args = parser.parse_args()
    
    # TODO: Implement normalization comparison
    logger.info(f"Comparing normalization methods: {args.methods}")
    logger.info(f"Data from {args.data_dir}")
    logger.info(f"Saving results to {args.output_dir}")


if __name__ == "__main__":
    main()
