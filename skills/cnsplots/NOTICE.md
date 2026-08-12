# Provenance & attribution — cnsplots skill

## Upstream

This skill is a **derivative enhancement**, not an original work.

- Upstream project: [faridrashidi/cnsplots](https://github.com/faridrashidi/cnsplots)
- Upstream skill location: `src/cnsplots/_agent_skill/cnsplots/`
- Upstream license: **BSD-3-Clause** — <https://github.com/faridrashidi/cnsplots/blob/main/LICENSE.md>
- Upstream author: Farid Rashidi

The upstream project ships its own installable agent skill via
`cnsplots skill install`. **Prefer the official skill** if you want to track
upstream exactly. This version exists to add executable verification steps.

## What is upstream-derived vs. original here

| File | Origin |
| --- | --- |
| `SKILL.md` | Restructured from upstream SKILL.md; workflow and hard rules rewritten |
| `references/plot-catalog.md` | Derived from upstream plot-catalog.md, expanded |
| `references/troubleshooting.md` | Original |
| `scripts/*.py` | Original |

## License

Upstream-derived content remains under BSD-3-Clause. Original additions are
released under the repository license (see root `LICENSE`), which is also
BSD-3-Clause to stay compatible.

## Syncing with upstream

Upstream may change the package API. Re-verify after any `cnsplots` upgrade:

```bash
python3 skills/cnsplots/scripts/check_env.py
python3 skills/cnsplots/scripts/inspect_api.py --list
```

Then bump `skill.json` → `verification.verified_against_package_version` and add
a `CHANGELOG.md` entry.
