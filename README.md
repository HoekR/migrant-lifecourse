# migrant-lifecourse

Convert lifecourse spreadsheets into per-person **timeline HTML pages** for the
Dutch–Australian migration exhibition (`migrant.huygens.knaw.nl`). A companion
subproject (`national_archives/`) scrapes item metadata from the National Archives
of Australia RecordSearch.

This repository follows the [dighum_template](https://github.com/HoekR/dighum_template)
conventions: manifest-based data paths (`data_manifest.toml` + `data_io`), provenance
sidecars on pipeline writes, and a uv-managed environment.

## Quick start

```bash
cp data_manifest.toml.example data_manifest.toml   # first time (repo-relative defaults)
uv sync                                             # + --extra notebook --extra scraper as needed
uv run python -m data_io.check                      # verify tiers + dataset paths
uv run make-site                                    # build personen/*.html from the workbook
uv run pytest -q                                    # data_io tests
```

`uv run make-site` (a.k.a. `uv run python scripts/make_site.py`) resolves the input
workbook and names index from the manifest, writes a provenance-tracked
`timeline_events.jsonl` intermediate, and renders one HTML page per person into
`personen/`.

## Layout

```
├── AGENTS.md / PLAN.md          # agent + planning docs
├── data_manifest.toml.example   # copy to data_manifest.toml (gitignored)
├── data_io/                     # vendored manifest + provenance I/O (dighum_template)
├── migrant_lifecourse/          # pipeline package (Sheet2Timeline, templates, build_site)
├── scripts/make_site.py         # manifest-driven build entrypoint
├── docs/DATA.md                 # tiers, phases, datasets
├── tests/                       # data_io tests
├── data/                        # source workbook + names index
├── personen/                    # rendered timeline pages
└── national_archives/           # NAA RecordSearch scraper notebooks
```

See [docs/DATA.md](docs/DATA.md) for the data model and [PLAN.md](PLAN.md) for status.
