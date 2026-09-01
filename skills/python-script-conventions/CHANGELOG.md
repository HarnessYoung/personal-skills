# Changelog — python-script-conventions skill

## [1.5.0] — 2026-09-01

### Added
- **Hard Rules section** — Non-negotiable conventions listed upfront (imports location, loguru usage, type hints, pathlib, dataclass flags, entry point pattern)
- **Workflow section** — Clear 4-step process (choose script type → start from template → fill sections → verify)
- **Template enhancements** — Added checklist at top, `REPLACE THIS` markers throughout, inline comments explaining dataclass flags (`kw_only`, `slots`, `frozen`)

### Changed
- **Restructured main SKILL.md** — Consistent section numbering (§1-7), improved navigation flow
- **Common Pitfalls reorganized** — Split into 3 categories: Layout & Imports (most frequent), Type System & Configuration, Control Flow & Domain Logic
- **Advanced Patterns section** — Streamlined with summaries and clear links to reference docs (signal-based classification, stem-prefix classification)
- **Domain scope clarified** — Explicitly states "developed for bioinformatics data-processing workflows, but patterns apply to any data-science script"
- **Path references standardized** — All template references now use `$SKILL_DIR/templates/agent_script_template.py`
- **Template section header** — Renamed "MAIN ENTRY POINT" to "MAIN EXECUTION" for consistency with documentation
- **Verification step (§Workflow 4)** — Now points at the §7 checklist plus `ruff check` for the mechanical rules, instead of a bundled script

### Removed
- **`scripts/verify_conventions.py`** — Added and then removed within this same release. A regex implementation was written first, and testing against six fixtures found five defects: nested imports were undetectable in files lacking section banners (the check keyed off the banner itself), a `@dataclass(kw_only=True)` config missing `slots`/`frozen` passed cleanly, `print` appearing in a docstring or string literal was reported as a violation, and a script following the three-line banner format documented in §1.2 was rejected because only the template's one-line format was matched. An AST rewrite fixed those cases, but the result still only covered the mechanically checkable rules, and it needed a `Convention-exempt` escape hatch to pass its own checks — a marker any script could add to silence the checker. `ruff` already covers unused imports, module-level import placement (E402), and `print` calls (T201) with far more rigor, and the rules that matter most here (single-line docstrings, section layout, docstring quality) are judgement calls. Shipping a bespoke checker that is weaker than `ruff` on the overlap and silent on the rest was not worth the maintenance surface.

### Improved
- Progressive disclosure — Advanced patterns summarized in main doc, details in references/
- Usability — Matches cnsplots skill structure (Hard Rules → Workflow → detailed sections)

## [1.4.0] — 2026-08-12
Migrated from Sotdo/personal_skills. Original work by Yusheng Yang.
