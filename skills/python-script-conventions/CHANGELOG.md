# Changelog — python-script-conventions skill

## [1.5.0] — 2026-09-01

### Added
- **Hard Rules section** — Non-negotiable conventions listed upfront (imports location, loguru usage, type hints, pathlib, dataclass flags, entry point pattern)
- **Workflow section** — Clear 4-step process (choose script type → start from template → fill sections → verify)
- **Automated verification script** (`scripts/verify_conventions.py`) — Checks section headers, import location, no print() calls, entry point pattern, pathlib usage, dataclass flags, and loguru import
- **Template enhancements** — Added checklist at top, `REPLACE THIS` markers throughout, inline comments explaining dataclass flags (`kw_only`, `slots`, `frozen`)

### Changed
- **Restructured main SKILL.md** — Consistent section numbering (§1-7), improved navigation flow
- **Common Pitfalls reorganized** — Split into 3 categories: Layout & Imports (most frequent), Type System & Configuration, Control Flow & Domain Logic
- **Advanced Patterns section** — Streamlined with summaries and clear links to reference docs (signal-based classification, stem-prefix classification)
- **Domain scope clarified** — Explicitly states "developed for bioinformatics data-processing workflows, but patterns apply to any data-science script"
- **Path references standardized** — All template references now use `$SKILL_DIR/templates/agent_script_template.py`
- **Template section header** — Renamed "MAIN ENTRY POINT" to "MAIN EXECUTION" for consistency with documentation

### Improved
- Progressive disclosure — Advanced patterns summarized in main doc, details in references/
- Usability — Matches cnsplots skill structure (Hard Rules → Workflow → detailed sections)
- Verification — Checklist now actionable via automated script

## [1.4.0] — 2026-08-12
Migrated from Sotdo/personal_skills. Original work by Yusheng Yang.
