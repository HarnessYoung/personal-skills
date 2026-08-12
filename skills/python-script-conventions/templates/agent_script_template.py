#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# (Optional) PEP 723 inline script metadata for self-contained execution with `uv`.
# Remove or adjust if managing dependencies via a traditional virtual environment.
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pandas",
#     "loguru",
# ]
# ///

"""
Script Template for S. pombe Phenotype Processing
===================================================

A template script that demonstrates the standard layout for AI-generated
Python scripts in this workspace. Replace this description with the
script's actual business logic, core algorithm, and context.

Input
-----
- Input file path (CSV, TSV, or XLSX) with required columns.
- See ``--input`` / ``--help`` for exact format.

Output
------
- Filtered results saved to the configured output directory.
- File format depends on the script's core logic.

Usage
-----
    mamba run -n bioinformatics python script_template.py \
        --input data/raw/file.csv \
        --output-dir outputs/ \
        --keywords growth morphology \
        --verbose

Author: Yusheng Yang (guidance) + Agent (implementation)
Date:   YYYY-MM-DD
Version: 1.0.0
"""

# ==================== §1 IMPORTS ====================
# Standard library
import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

# Data manipulation / numerical (alphabetical)
import pandas as pd

# Third-party (alphabetical)
from loguru import logger

# ==================== §2 TYPE HINTS & DECORATORS ====================
# (Optional) Custom type aliases and decorators used throughout the script

# ==================== §3 CONSTANTS ====================
# Module-level constants: filenames, magic numbers, defaults, etc.
DEFAULT_OUTPUT_DIR = Path("outputs")
REQUIRED_COLUMNS = ["gene_id", "description", "category"]

# ==================== §4 CONFIG ====================

@dataclass(kw_only=True, slots=True, frozen=True)
class Config:
    """Immutable configuration container for script execution."""
    input_path: Path
    output_dir: Path
    keywords: list[str]
    verbose: bool = False

# ==================== §5 LOGGING ====================

def setup_logger(verbose: bool) -> None:
    """Configure loguru for this script's needs."""
    logger.remove()  # Clear default handler
    level = "DEBUG" if verbose else "INFO"
    logger.add(sys.stderr, level=level, format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level:<8}</level> | {message}")

# ==================== §6 CORE LOGIC ====================

@logger.catch
def filter_dataframe(df: pd.DataFrame, config: Config) -> pd.DataFrame:
    """
    Core processing function: filter the input DataFrame based on keywords.
    
    This is the main business logic. Guard clauses at the top handle edge cases.
    """
    # Guard clause: empty input
    if df.empty:
        logger.warning("Input DataFrame is empty; returning empty result.")
        return df
    
    # Guard clause: missing required columns
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    
    # Main filtering logic
    if not config.keywords:
        logger.info("No keywords provided; returning all rows.")
        return df
    
    # Filter rows where 'description' contains any of the keywords (case-insensitive)
    mask = df["description"].str.lower().str.contains("|".join(config.keywords), na=False, case=False)
    result = df[mask].copy()
    
    logger.info(f"Filtered {len(df):,} rows down to {len(result):,} matching keywords: {config.keywords}")
    return result

# ==================== §7 MAIN ENTRY POINT ====================

def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Process S. pombe phenotype data and filter by keywords.",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--input",
        type=Path,
        required=True,
        help="Path to input CSV/TSV/XLSX file."
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Output directory for results (default: {DEFAULT_OUTPUT_DIR})"
    )
    parser.add_argument(
        "--keywords",
        nargs="+",
        default=[],
        help="Keywords to filter phenotype descriptions (e.g., 'growth', 'morphology')"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable debug-level logging."
    )
    return parser.parse_args()

def main() -> int:
    """Main execution flow."""
    args = parse_args()
    setup_logger(args.verbose)
    
    # Build config from CLI args
    config = Config(
      input_path=args.input,
      output_dir=args.output_dir,
      keywords=args.keywords
    )
    
    # Prepare output directory
    config.output_dir.mkdir(parents=True, exist_ok=True)
    
    # Execute core logic 
    logger.info(f"Starting processing for file: {config.input_path}")
    try:
        df_raw = pd.read_csv(config.input_path)
        df_filtered = filter_dataframe(df_raw, config)
        
        out_file = config.output_dir / "filtered_results.csv"
        df_filtered.to_csv(out_file, index=False)
        logger.info(f"Results successfully saved to {out_file} ({len(df_filtered):,} rows)")
        
    except Exception as e:
        logger.exception(f"An unexpected error occurred: {e}")
        return 1
        
    return 0

if __name__ == "__main__":
    sys.exit(main())
