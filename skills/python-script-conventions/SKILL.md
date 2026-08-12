---
name: python-script-conventions
description: Use when generating, modifying, or reviewing Python scripts (3.12+). Specifies section layout, import ordering, type system, logging, dataclass patterns, and AI-agent-friendly design principles. Load this skill whenever creating or editing a .py file — especially for bioinformatics/data-science scripts.
version: 1.4.0
author: Yusheng Yang
license: MIT
metadata:
  hermes:
    tags: [python, conventions, style-guide, code-quality, ai-design]
    related_skills: [plan, writing-plans, test-driven-development, project-scaffolding, systematic-debugging]
---

# Python Script Conventions (Modern Python 3.12+)

## Overview

This skill defines the coding standards and design patterns to follow when generating or modifying Python scripts in this workspace. It codifies a consistent layout, modern Python 3.12+ idioms, and AI-agent-friendly design so that every script reads like it belongs to the same codebase.

The companion file `templates/agent_script_template.py` provides a concrete reference implementation of these principles. **Always open that template as a starting point when writing a new script from scratch.**

Apply these rules thoughtfully — if a rule would make a particular script worse, adapt accordingly.

---

## When to Use

- **Creating any new `.py` script** in this workspace — load this skill first, then open `templates/agent_script_template.py` as the starting structure.
- **Modifying an existing script** — refactor to match these conventions when the edit is substantial (layout, imports, logging, etc.).
- **Reviewing a PR or diff that includes Python files** — use the checklist below as review criteria.
- **Generating a single-file script** meant for `uv` or standalone execution.

### When NOT to Use

- Libraries or packages with multiple modules (those follow their own structure; this skill targets standalone scripts).
- Jupyter notebooks (use the jupyter-live-kernel skill instead).
- Code snippets in markdown docs (unless they're illustrative of the template).

### Modifying an Existing Script

When *modifying* a script that was written before this skill was applied (or
that partially follows it), **treat the edit as a section-layout review**:

1. Re-read the entire script's section structure before editing — don't just
   jump to the line you want to change.
2. If you're adding a new import, put it in the top-level IMPORTS section,
   **not** next to where it's used in the body. The skill's import ordering
   rules apply to modifications as much as to new files.
3. If the edit is substantial (10+ lines changed, new imports, new functions),
   refactor the file to match the full section layout. This repays quickly
   — the next edit benefits from the structure.
4. Run the verification checklist after the edit, not just before it.

---

### 1.1 Standalone Scripts vs Library Modules

A file in ``src/`` is either a **standalone script** (invoked from the
command line) or a **library module** (imported by other scripts). They
have different structures:

**Standalone script** — follows the full 7-section layout (IMPORTS →
DECORATORS → CONSTANTS → CONFIG → LOGGING → CORE → MAIN). Contains
``parse_args()`` + ``if __name__ == "__main__": sys.exit(main())``.

**Library module** — omits the LOGGING, CONFIG, and MAIN sections.
Contains only IMPORTS, CONSTANTS (including enums and dataclasses), and
CORE LOGIC. No ``parse_args()``, no ``main()``, no ``setup_logger()``.
The module-level docstring omits the CLI Usage block from the §3.2
format, but keeps the title, description, I/O spec, and metadata.

Check ``src/growth_signals.py`` in this workspace for a concrete example.

### 1.2 Script Structure & Layout

Scripts should follow this section order, reflecting a natural information **dependency hierarchy** — constants → data models → core logic → CLI → main — so each section only depends on what came before it. Omit sections that a script does not need (e.g., no enums, no decorators).

Always use the `agent_script_template.py` template as the starting point:

```python
# =============================================================================
# IMPORTS
# =============================================================================
...
# =============================================================================
# DECORATORS
# =============================================================================
...
# =============================================================================
# GLOBAL CONSTANTS & ENUMS
# =============================================================================
...
# =============================================================================
# CONFIGURATION & DATACLASSES
# =============================================================================
...
# =============================================================================
# LOGGING SETUP
# =============================================================================
...
# =============================================================================
# CORE LOGIC (FUNCTIONS / CLASSES)
# =============================================================================
...
# =============================================================================
# MAIN EXECUTION
# =============================================================================
...
```

### Imports Ordering

Group imports into three blocks, sorted alphabetically within each block:

```python
# 1. Standard Library Imports
import argparse
import sys
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Any

# 2. Data Processing Imports
import pandas as pd

# 3. Third-party Imports
from loguru import logger
```

### Entry Point Pattern

All scripts must use the following pattern at the bottom:

```python
if __name__ == "__main__":
    sys.exit(main())
```

This ensures:
- The script can be imported without executing
- Exit codes are propagated correctly
- `main()` returns an integer (0 for success, non-zero for error)

### Configuration Dataclass

Use `@dataclass(kw_only=True, slots=True, frozen=True)` for configuration:

```python
@dataclass(kw_only=True, slots=True, frozen=True)
class AppConfig:
    """Configuration for the script's runtime parameters."""
    input_path: Path
    output_dir: Path
    p_value_threshold: float
    keywords: list[str]
```

- `kw_only=True` → forces keyword arguments (prevents positional confusion)
- `slots=True` → reduces memory footprint
- `frozen=True` → makes the instance immutable (most configs shouldn't change after creation)

### Logging with Loguru

Use `loguru` for all output. Never use `print()` or `logging` stdlib:

```python
from loguru import logger

def setup_logger(log_level: str = "INFO") -> None:
    """Configure the Loguru logger."""
    logger.remove()  # Remove default handler
    logger.add(
        sys.stdout,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level:<8} | {message}",
        level=log_level
    )

setup_logger()
```

Add `@logger.catch` to core logic functions for automatic exception logging.

---

## 2. Type System & Modern Python Features

### Type Hints Everywhere

Every function signature must include type hints for parameters and return values:

```python
def filter_dataframe(df: pd.DataFrame, config: AppConfig) -> pd.DataFrame:
    """Filter the Pandas DataFrame based on configured P-value thresholds."""
    ...
```

Use `-> None` for procedures that don't return a value.

### StrEnum for String Constants

When you have a fixed set of related string markers (e.g., column names, operation modes), use `StrEnum`:

```python
from enum import StrEnum

class DataCol(StrEnum):
    GENE_ID = "systematic_name"
    PHENOTYPE = "phenotype"
    PVALUE = "p_value"
```

**Do NOT use StrEnum for:**
- Single unrelated constants (just use a module-level variable)
- Dynamic values that come from user input or config files

### Pathlib Over os.path

Always use `pathlib.Path` instead of `os.path`:

```python
from pathlib import Path

config = AppConfig(
    input_path=args.input.resolve(),  # .resolve() for absolute path
    output_dir=args.outdir.resolve()
)

config.output_dir.mkdir(parents=True, exist_ok=True)
```

### F-strings Only

Use f-strings for all string interpolation. Never use `.format()` or `%`:

```python
logger.info(f"Initial raw data shape: {df.shape}")
logger.info(f"Results saved to {out_file} ({len(df_filtered):,} rows)")
```

---

## 3. Documentation Standards

### 3.1 Single-Line Docstrings for Functions

Function docstrings should be **one line** — type hints carry the type information:

```python
def filter_dataframe(df: pd.DataFrame, config: AppConfig) -> pd.DataFrame:
    """Filter the Pandas DataFrame based on configured P-value thresholds and keywords."""
    ...
```

**Do NOT write multi-line NumPy/Sphinx-style docstrings** with Parameters/Returns blocks. The type annotations already document the types.

### 3.2 Module-Level Docstring Format

Every script must have a comprehensive module-level docstring at the top, following this structure:

```python
"""
Script Title (One Line, Human-Readable)
========================================

1-3 paragraphs describing the business logic, algorithm, and context.
Use bullet lists for multi-step processes.

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
    mamba run -n bioinformatics python script_name.py
    mamba run -n bioinformatics python script_name.py --input path/to/data.csv --verbose

Author:   [Name] (guidance) + [AI Agent] (implementation)
Date:     YYYY-MM-DD
Version:  X.Y.Z
"""
```

See `references/module-level-docstring.md` for real-world examples.

### 3.3 Change Documentation Format

When documenting code changes (in commit messages, PR descriptions, or change logs), use a **three-column table** format:

```markdown
| Problem | Root Cause | Fix |
|---|---|---|
| Script fails when input CSV is empty | `filter_dataframe()` doesn't check for empty DataFrame | Added guard clause: `if df.empty: return df` |
| P-value filter returns wrong results | Used `<=` instead of `<` for threshold comparison | Changed to `df[DataCol.PVALUE] < config.p_value_threshold` |
```

This format surfaces *why* a change was needed, not just *what* changed.

---

## 4. Control Flow & Error Handling

### Guard Clauses

Use guard clauses to handle edge cases early and reduce nesting:

```python
def filter_dataframe(df: pd.DataFrame, config: AppConfig) -> pd.DataFrame:
    """Filter the Pandas DataFrame based on configured P-value thresholds."""
    # Guard clause: Return early if the dataframe is empty
    if df.empty:
        logger.warning("Received empty DataFrame. Skipping filtering.")
        return df
    
    # Main logic here
    ...
```

### Match-Case Over If-Elif Chains

For categorical logic with 3+ branches, use `match...case` instead of `if-elif-else`:

```python
match phenotype_type:
    case "growth":
        return process_growth(data)
    case "morphology":
        return process_morphology(data)
    case "viability":
        return process_viability(data)
    case _:
        logger.warning(f"Unknown phenotype type: {phenotype_type}")
        return None
```

### Exception Handling

Wrap `main()` logic in a try-except block and return non-zero on error:

```python
def main() -> int:
    """Main orchestrator function for the script execution."""
    try:
        df_raw = pd.read_csv(config.input_path)
        df_filtered = filter_dataframe(df_raw, config)
        ...
    except Exception as e:
        logger.exception(f"An unexpected error occurred: {e}")
        return 1
    
    return 0
```

---

## 5. Advanced Patterns

### 5.1 Signal-Based Classification

Replace deep `if-elif` chains with a declarative signal table + resolution engine. See `references/signal-based-classification.md` for the full pattern.

**When to use:** You have a rule-based text classifier with 8+ branches where ordering matters and rules can conflict.

**Key idea:** Define all rules as data (a list of `Signal` dataclasses), detect all matches independently, then resolve conflicts in post-processing.

### 5.2 Stem-Prefix Text Classification

For keyword-profile analysis (categorizing every word in a corpus), use exact match + stem-prefix fallback. See `references/stem-prefix-classification.md`.

**When to use:** You need to classify words into semantic categories (growth, morphology, modifiers, stop words) for quality inspection.

**Key idea:** 
1. Exact match for compound/hyphenated tokens
2. Short canonical stems (≥3 chars) for plurals and inflections
3. Multi-word phrase pre-tokenization (convert "small colonies" → "small-colonies" before splitting)

---

## 6. Common Pitfalls

1. **Using `print()` instead of `logger`.** All output must go through `loguru`. The only exception: piping structured data to stdout for shell consumption (rare).

2. **Forgetting `frozen=True` on config dataclasses.** Most configs should be immutable after creation. Only use `frozen=False` if the application genuinely needs hot-reloading.

3. **Not returning exit codes from `main()`.** Shells, CI pipelines, and scripts that check `$?` can detect errors. The template already does this — just remember to return non-zero from `main()` on failure branches.

4. **Using `os.path.join()` / `os.path.exists()` instead of `pathlib.Path`.** The template imports `Path` and uses it throughout. Keep that consistent — `pathlib` is more readable, composable, and less error-prone.

5. **Hardcoded string markers instead of `StrEnum`.** When the script uses column names, operation modes, or categorical statuses that appear in multiple places, define them as a `StrEnum`. This prevents silent breakage when a string changes in one place but not another.

6. **Creating decorators for single-use abstractions.** A decorator with only one consumer adds indirection without benefit. The rule: only create a custom decorator when it eliminates repetitive boilerplate across **3+** functions.

7. **Deep `if-elif-else` chains for categorical logic.** Two alternatives depending on the problem:

   - **Fixed enum variants** (the category set is known and closed): use
     `match...case` instead of a chain. It's more readable and the type
     checker can help ensure exhaustiveness.

   - **Rule-based classification from free-text** (keywords in a
     description drive the category): use the **signal-based
     classification** pattern instead. See `references/signal-based-classification.md`
     under this skill for the full recipe. Pay special attention to
     **contextual signal suppression** — a keyword within a compound
     phrase (e.g. "spores" in "germinated spores") may not be an
     independent signal.

   - **Keyword‑profile / vocabulary analysis** (counting and categorising
     every word across category groups): use **stem‑prefix matching** —
     short canonical stems with an exact‑match fallback, plus hyphenated
     phrase pre‑tokenisation. See `references/stem-prefix-classification.md`
     under this skill.

8. **Unused imports left after refactoring.** Imports that were added during development but became unused after the code was refactored are easy to miss — the linter only catches them if a type checker like Pyright or `ruff check` is configured. Before finalising a script, scan the import block and verify every symbol is actually referenced in the body. The checklist below catches this; the pitfall section reminds you to look for it even when no linter is active.

9. **Writing multi-line docstrings with formal Parameters/Returns blocks.** Section 3.2 mandates single-line docstrings — type hints carry the type information. When a core function has complex arguments, the natural instinct is to write NumPy-style or Sphinx-style docstrings with `Parameters\n----------\n...\nReturns\n-------\n...`. This violates the rule. The fix: keep the docstring to one concise line and let the type annotations do the rest. If the function genuinely needs narrative context, put it in a comment block inside the function body rather than in the docstring. This is the most commonly-violated rule because "important" functions feel like they deserve more documentation — resist the urge.

10. **Adding a new import inside a function body, class definition, or section header instead of the top-level IMPORTS section.** This happens most often when *patching* an existing script — the natural instinct is to add the import next to where the new code goes. Every import must live in the IMPORTS block at file scope. Imports placed elsewhere confuse the section structure, bypass the linting pass, and make the next editor hunt for where a symbol is imported. Fix: before applying a patch that needs a new import, scroll to the IMPORTS block, add it in the correct group, then reference it in the body.

11. **Forgetting to re-check `classify_phenotype_count()` logic after expanding MODIFIER_WORDS / GROWTH_KEYWORDS.** When adding words to the modifier or growth keyword lists, fewer commas will be classified as parallel (Multiple → Single shift). After any expansion, re-run the full pipeline and verify the count deltas are expected and justified. Verify with `df["Phenotype_count"].value_counts()` in the merged output.

---

## Verification Checklist

- [ ] Sections follow the ordered layout (IMPORTS → DECORATORS → CONSTANTS → CONFIG → LOGGING → CORE → MAIN)
- [ ] Imports grouped: standard library → data processing → third-party, sorted alphabetically within each group
- [ ] All imports are in the top-level IMPORTS section — none in function bodies, class definitions, or section headers
- [ ] No unused imports — every imported module/name is referenced in the script body
- [ ] No `print()` calls — all runtime output uses `loguru`
- [ ] `pathlib.Path` used everywhere (no `os.path`)
- [ ] F-strings for interpolation (no `.format()` or `%`)
- [ ] `@dataclass(kw_only=True, slots=True, frozen=True)` for configuration objects
- [ ] `StrEnum` for grouped string markers, not for singleton constants
- [ ] Guard clauses for edge cases at function top
- [ ] Library modules (imported, not run directly) omit LOGGING, CONFIG, MAIN sections — no `parse_args()`, no `main()`, no `setup_logger()`
- [ ] `parse_args()` function + `if __name__ == "__main__": sys.exit(main())` guard
- [ ] Module-level docstring follows the §3.2 format (title → description → Input → Output → Usage → metadata)
- [ ] Change documentation uses three-column table (Problem → Root Cause → Fix) when summarising code modifications
- [ ] Single-line docstrings on functions and classes
- [ ] `@logger.catch` on core logic functions
- [ ] `--verbose` CLI flag for debug-level logging
- [ ] No deep `if-elif-else` chains — use `match...case` for categorical branches
