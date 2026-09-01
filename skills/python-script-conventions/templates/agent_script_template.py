#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# =============================================================================
# CHECKLIST BEFORE FINALIZING (delete this block when done):
# - [ ] Replace the module docstring: title, description, Input, Output, Usage
# - [ ] Resolve every `REPLACE THIS` marker below
# - [ ] Update REQUIRED_COLUMNS to match the real input
# - [ ] Implement the real logic in filter_dataframe(), or rename it
# - [ ] Update parse_args() with the actual CLI parameters
# - [ ] Verify every import is used, and that none sit inside a function body
# - [ ] Walk the full checklist in the skill's SKILL.md section 7
# =============================================================================

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
Script Template for Data Processing                    # REPLACE THIS: One-line title
===================================================

A template script that demonstrates the standard layout for AI-generated
Python scripts in this workspace. Replace this description with the
script's actual business logic, core algorithm, and context.
                                                        # REPLACE THIS: Full description

Input
-----
- Input file path (CSV, TSV, or XLSX) with required columns.
- See ``--input`` / ``--help`` for exact format.      # REPLACE THIS: Actual input spec

Output
------
- Filtered results saved to the configured output directory.
- File format depends on the script's core logic.     # REPLACE THIS: Actual output spec

Usage
-----
    mamba run -n bioinformatics python script_template.py \
        --input data/raw/file.csv \
        --output-dir outputs/ \
        --keywords growth morphology \
        --verbose                                      # REPLACE THIS: Real usage examples

Author: Yusheng Yang (guidance) + Agent (implementation)  # REPLACE THIS: Actual author
Date:   YYYY-MM-DD                                     # REPLACE THIS: Today's date
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
REQUIRED_COLUMNS = ["gene_id", "description", "category"]  # REPLACE THIS: Your actual required columns

# ==================== §4 CONFIG ====================

@dataclass(kw_only=True, slots=True, frozen=True)
class Config:
    """Immutable configuration container for script execution."""
    input_path: Path
    output_dir: Path
    keywords: list[str]
    verbose: bool = False
    # kw_only=True → forces keyword arguments (prevents positional confusion)
    # slots=True → reduces memory footprint (no __dict__ per instance)
    # frozen=True → makes instances immutable (config shouldn't change after creation)

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
    
    # REPLACE THIS: Main filtering logic - implement your actual business logic here
    if not config.keywords:
        logger.info("No keywords provided; returning all rows.")
        return df
    
    # Filter rows where 'description' contains any of the keywords (case-insensitive)
    mask = df["description"].str.lower().str.contains("|".join(config.keywords), na=False, case=False)
    result = df[mask].copy()
    
    logger.info(f"Filtered {len(df):,} rows down to {len(result):,} matching keywords: {config.keywords}")
    return result

# ==================== §7 MAIN EXECUTION ====================

def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Process data and filter by keywords.",  # REPLACE THIS: Your actual description
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
        help="Keywords to filter descriptions (e.g., 'growth', 'morphology')"  # REPLACE THIS: Your params
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
