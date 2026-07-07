# Agent instructions — migrant-lifecourse

Convert lifecourse spreadsheets into per-person timeline HTML pages for the
Dutch–Australian migration exhibition. Read **`PLAN.md`**, **`docs/DATA.md`**, and
**`data_manifest.toml`** before pipeline work.

## Data paths (strict)

- **Never** hardcode absolute paths (`/Users/...`, `/Volumes/...`) in Python. The legacy
  `scripts.py` and the exploratory `make_site.ipynb` cells contain such paths — the
  compliant entrypoint is `scripts/make_site.py` (`uv run make-site`), which resolves
  everything through the manifest.
- **Always** register datasets in `data_manifest.toml` first, then use:
  ```python
  from data_io import resolve, load, save_semi_structured, save_parquet
  ```
- **Always** run after manifest or tier changes: `uv run python -m data_io.check`
- Keep the `PLAN.md` dataset table in sync with `[datasets.*]` keys.

## Outputs (strict)

- Semi-structured intermediates: `save_semi_structured(..., logical_name=..., script=__file__)`
  (writes `.meta.toml` provenance automatically).
- Frozen tables: `save_parquet(df, logical_name=..., script=__file__)`.
- Rendered HTML pages (`timeline_pages`) are written to the manifest-resolved directory;
  they are a presentation artifact, not a provenance-tracked table.

## Project layout

| Path | Role |
|------|------|
| `migrant_lifecourse/` | Reusable pipeline package (Sheet2Timeline, templates, helpers) |
| `migrant_lifecourse/build_site.py` | Manifest-driven build (`make-site` entrypoint) |
| `scripts/make_site.py` | Thin CLI wrapper around `build_site.main` |
| `data_io/` | Vendored manifest + provenance I/O (from dighum_template) |
| `national_archives/` | NAA RecordSearch scraper notebooks (`scraper` extra) |
| `data/`, `personen/` | Committed inputs and rendered pages |

## Environment

- Managed with **uv** — use `uv sync`, `uv run`, `uv add`; no bare `pip install`.
- Extras: `notebook` (Jupyter), `scraper` (recordsearch_data_scraper). Install with
  `uv sync --extra notebook --extra scraper`.
- **pandas is pinned `<3`**: the legacy transform relies on `Series.fillna(inplace=True)`
  propagating to the parent DataFrame (broken by pandas 3.0 copy-on-write). De-`inplace`-ing
  the transform is a tracked PLAN.md follow-up.

## Code style

- Prefer vectorized pandas; avoid row loops and `inplace=True` in new code.
- Never discard archival metadata fields during transforms.

## Template

This repo follows [dighum_template](https://github.com/HoekR/dighum_template). Wisdom and
add-ons live in that repo (`wisdom/INDEX.md`, `addons/README.md`); apply later with its
`scripts/apply_addon.sh <this-repo> <name>`.
