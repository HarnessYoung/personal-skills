# Changelog — cnsplots skill

All notable changes to this skill. Versioning is [SemVer](https://semver.org/)
applied to the *skill*, independent of the `cnsplots` package version.

## [1.0.0] — 2026-08-12

Initial release. Derivative enhancement of the upstream skill bundled in
[faridrashidi/cnsplots](https://github.com/faridrashidi/cnsplots)
(`src/cnsplots/_agent_skill/cnsplots`, BSD-3-Clause).

### Added relative to upstream
- `scripts/check_env.py` — interpreter, package version, backend, and `mutool` probe.
- `scripts/inspect_api.py` — prints installed signatures/docstrings; `--list` dumps public API.
- `scripts/validate_output.py` — verifies artifact existence, size, magic bytes, and
  counts SVG `<text>` elements to catch text-outlined output.
- `references/troubleshooting.md` — 13 documented failure modes.

### Changed relative to upstream
- Replaced the ad-hoc heredoc introspection step with a bundled script.
- Expanded the plot catalog with a table layout, palette names, and explicit
  notes on functions that do not return a plain matplotlib `Axes`.

### Verified
Against `cnsplots` 0.6.0 on Python 3.12.13. See `skill.json` → `verification`.
