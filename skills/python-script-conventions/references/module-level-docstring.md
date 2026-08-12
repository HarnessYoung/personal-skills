# Module-Level Docstring — Real-World Example

This reference shows the exact docstring format from
`src/01_format_and_update_ids.py` in this workspace. When writing a new
script, replace the content fields but keep the section structure intact.

---

## Standalone Script Example

```python
"""
Format Hayles 2013 Phenotype Data and Update Gene Systematic IDs
=================================================================

Two-phase pipeline that (1) cleans and normalises the raw Hayles 2013
supplementary table, and (2) maps all gene systematic IDs against a
current PomBase annotation to correct identifiers changed by genome
annotation updates since 2013.

Phase 1 — Data Formatting
  - Strips whitespace from Systematic ID, phenotype description,
    classification, and dispensability columns
  - Normalises temperature notation: coerces variants such as
    "25, 32", "25 32", "32, 25" to the canonical "25,32"
  - Drops spurious zero‑width characters from text fields
  - Ensures consistent CSV encoding (UTF-8 with BOM, CRLF line endings)

Phase 2 — Systematic ID Update
  - Reads the current PomBase gene_IDs_names_products.tsv annotation
  - For every gene in Hayles 2013:
      1. Check if the systematic ID still exists
      2. If not, lookup via gene name
      3. If that fails, lookup via synonyms column
  - Flags any IDs that could not be resolved (≤1% failure rate expected)

The script does **not** update the underlying data — it writes two
separate files (formatted + updated), leaving the original intact. Manual
QA of the updated file is required before committing to the workspace.

Input
-----
- `data/raw/Hayles2013_Suppl_Table3.csv`
  (Original 4,938‑row phenotype table, downloaded from PMC supplementary)

- `data/annotation/gene_IDs_names_products.tsv.gz`
  (PomBase 2026‑06 release, ~12.7k genes)

Output
------
- `data/formatted/Hayles2013_formatted.csv`
  (4,938 rows × 5 columns: Systematic ID, Phenotype_description,
   Phenotype_classification, Dispensability, Temperature)

- `data/formatted/Hayles2013_updated.csv`
  (Same structure, systematic IDs remapped to current annotations)

- `logs/update_summary.log`
  (Remap audit trail: fallback strategies, unresolved IDs)

Usage
-----
    mamba run -n bioinformatics python src/01_format_and_update_ids.py

Author: Yusheng Yang (guidance) + Agent (implementation)
Date:   2026‑04‑02
Version: 1.1.0
"""
```

---

## Library Module Example

When the module is a **library** — imported by other scripts but
never executed directly — the Input/Output/Usage sections are optional.
Keep only the title, description, and author/date/version:

```python
"""
Phenotype Text Classification Engine
=====================================

Core classification functions for growth / morphology / viability phenotypes.
Supports signal‑based classification with priority resolution.

Author: Yusheng Yang (guidance) + Agent (implementation)
Date:   2026‑04‑02
Version: 1.0.0
"""
```

---

## What's Mandatory vs. Optional

| Section | Purpose | When to include |
| --- | --- | --- |
| **Title + Underline** | One‑line script summary, emphasised | Always |
| **Description** | The actual business logic, broken into phases if the script has multiple steps. Bullet lists OK for multi-step pipelines | Always |
| **Input** | What files/data the script reads, format expectations | Always for standalone scripts; optional for library modules |
| **Output** | What files the script writes, their column/row structure | Always for standalone scripts; optional for library modules |
| **Usage** | Copy-pasteable CLI commands (prefixed with `mamba run -n` or equivalent) | Standalone scripts only |
| **Author / Date / Version** | `Author: Name (guidance) + Agent (implementation)`, `Date: YYYY-MM-DD`, `Version: X.Y.Z` | Always |

## Language

When a project repository will be made public alongside a publication,
write all documentation — module docstrings, ``docs/*.md``, the project
``README.md`` — in **English**.
