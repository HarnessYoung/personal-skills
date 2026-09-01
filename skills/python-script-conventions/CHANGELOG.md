# Changelog — python-script-conventions skill

## [1.5.0] — 2026-09-01

### Added
- **Hard Rules section** — Non-negotiable conventions listed upfront (imports location, loguru usage, type hints, pathlib, dataclass flags, entry point pattern)
- **Workflow section** — Clear 4-step process (choose script type → start from template → fill sections → verify)
- **Automated verification script** (`scripts/verify_conventions.py`) — AST-based checker for section headers, import location, no print() calls, entry point pattern, pathlib usage, dataclass flags, and loguru import
- **Template enhancements** — Added checklist at top, `REPLACE THIS` markers throughout, inline comments explaining dataclass flags (`kw_only`, `slots`, `frozen`)

### Changed
- **Restructured main SKILL.md** — Consistent section numbering (§1-7), improved navigation flow
- **Common Pitfalls reorganized** — Split into 3 categories: Layout & Imports (most frequent), Type System & Configuration, Control Flow & Domain Logic
- **Advanced Patterns section** — Streamlined with summaries and clear links to reference docs (signal-based classification, stem-prefix classification)
- **Domain scope clarified** — Explicitly states "developed for bioinformatics data-processing workflows, but patterns apply to any data-science script"
- **Path references standardized** — All template references now use `$SKILL_DIR/templates/agent_script_template.py`
- **Template section header** — Renamed "MAIN ENTRY POINT" to "MAIN EXECUTION" for consistency with documentation
- **Verification script rewritten** — Now uses AST parsing instead of regex, fixing all false positives and false negatives

### Fixed (in verify_conventions.py rewrite)
- **False negative #1**: Nested imports inside functions/classes now correctly detected (was missed in files without section headers)
- **False negative #2**: Dataclass flags (`kw_only`, `slots`, `frozen`) now checked individually; missing any flag is reported
- **False negative #3**: Multi-line dataclass decorators now handled correctly
- **False positive #4**: No longer reports `print` when it appears in docstrings, comments, or string literals
- **False positive #5**: Now accepts both single-line (`§N SECTION`) and three-line banner formats from SKILL.md
- **Self-consistency**: Verification script now passes its own checks (with appropriate CLI-tool exemption)

### Improved
- Progressive disclosure — Advanced patterns summarized in main doc, details in references/
- Usability — Matches cnsplots skill structure (Hard Rules → Workflow → detailed sections)
- Verification — Checklist now actionable via robust AST-based automated script

## [1.4.0] — 2026-08-12
Migrated from Sotdo/personal_skills. Original work by Yusheng Yang.
