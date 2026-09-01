# Provenance & attribution — cnsplots skill

## Upstream

This skill is a **derivative enhancement**, not an original work.

- Upstream project: [faridrashidi/cnsplots](https://github.com/faridrashidi/cnsplots)
- Upstream skill location: `src/cnsplots/_agent_skill/cnsplots/`
- Upstream license: **BSD-3-Clause** — <https://github.com/faridrashidi/cnsplots/blob/main/LICENSE.md>
- Upstream author: Farid Rashidi

The upstream project ships its own installable agent skill via
`cnsplots skill install`. **Prefer the official skill** if you want to track
upstream exactly. This version exists to add executable verification steps, the
measured rcParams/settings style contract, and layout composition guidance.

## What is upstream-derived vs. original here

| File | Origin |
| --- | --- |
| `SKILL.md` | Restructured from upstream SKILL.md; workflow and hard rules rewritten |
| `references/plot-catalog.md` | Derived from upstream plot-catalog.md, expanded |
| `references/troubleshooting.md` | Original |
| `references/rcparams.md` | Original; tables generated from the installed package |
| `references/settings-catalog.md` | Original; generated from the installed package |
| `references/composition-patterns.md` | Original; based on measurements of `_multipanels.py` behavior |
| `references/style-bridge.md` | Original |
| `references/dense-figures.md` | Original prose; techniques derived from the upstream showcase example |
| `references/color-strategy.md` | Original prose; audits the vendored showcase source and measures assigned colors |
| `references/journal-specs.md` | Original prose and conversions; the underlying figure requirements are the publishers' own, quoted with attribution and source URLs |
| `scripts/*.py` | Original |
| `templates/*.py` | Original code; `dense_figure.py` follows the structure of the upstream showcase example |
| `templates/upstream-showcase/figure1.py`, `figure2.py` | **Vendored verbatim** from the upstream showcase; copyright Farid Rashidi, BSD-3-Clause |
| `templates/upstream-showcase/README.md` | Original |

The upstream showcase example
(<https://cnsplots.farid.one/latest/examples/showcase.html>) was run and studied
while writing `references/dense-figures.md` and `templates/dense_figure.py`. That
prose and code are written from scratch, but the techniques they teach come from
that example and are credited to it under the same BSD-3-Clause terms.

`templates/upstream-showcase/` holds the example's two figure scripts copied
**unmodified**, as reference material for cases where our distilled description
drifts from what the author actually wrote. They carry the upstream copyright and
license, are not our work, and should not be edited: re-copy them from upstream
when it changes.

## License

Upstream-derived content remains under BSD-3-Clause. Original additions are
released under the repository license (see root `LICENSE`), which is also
BSD-3-Clause to stay compatible.

## Syncing with upstream

Upstream may change the package API. Re-verify after any `cnsplots` upgrade:

```bash
python3 skills/cnsplots/scripts/check_env.py
python3 skills/cnsplots/scripts/inspect_api.py --list
python3 skills/cnsplots/scripts/dump_style.py
```

Compare the `dump_style.py` output against the tables in
`references/rcparams.md` and `references/settings-catalog.md`; regenerate them
with `--markdown` if anything moved. Run all three templates and look at the
rendered output. Then bump `skill.json` →
`verification.verified_against_package_version` and add a `CHANGELOG.md` entry.
