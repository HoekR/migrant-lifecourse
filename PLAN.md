# Project plan — migrant-lifecourse

## Goal

Convert an Excel workbook of migrant life events (one sheet per person) into styled,
per-person **timeline HTML pages** for the Dutch–Australian migration exhibition
(`migrant.huygens.knaw.nl`). A companion subproject scrapes item metadata from the
National Archives of Australia RecordSearch.

## Data paths

Logical names live in [`data_manifest.toml`](data_manifest.toml). Verify with
`uv run python -m data_io.check`.

| Logical name | Phase | Notes |
|--------------|-------|-------|
| `lifecourses_workbook` | explore | Source Excel workbook (input) |
| `person_names` | explore | Slug → sheet-name index (input) |
| `timeline_events` | semi | Flattened per-event JSONL + provenance sidecar |
| `timeline_pages` | semi | Rendered per-person HTML pages (output dir `personen/`) |

## Build

```bash
cp data_manifest.toml.example data_manifest.toml   # first time
uv sync
uv run python -m data_io.check
uv run make-site                                    # == uv run python scripts/make_site.py
```

## Phases

### Phase 1 — Explore

- [x] Register inputs (`lifecourses_workbook`, `person_names`) in manifest
- [x] `data_io.check` passes

### Phase 2 — Semi-structured

- [x] `timeline_events` written via `save_semi_structured` (provenance sidecar)
- [x] `timeline_pages` rendered from manifest-resolved paths

### Phase 3 — Frozen

- [ ] Promote a stable event/person table to `save_parquet` if downstream analysis needs it

## Outputs

| Artifact | Logical name | Path (via manifest) |
|----------|--------------|---------------------|
| Per-event records | `timeline_events` | `scratch/timeline_events.jsonl` |
| Timeline pages | `timeline_pages` | `personen/*.html` |

## Follow-ups / tech debt

- [ ] Remove `Series.fillna(inplace=True)` and row-wise `.apply` from
      `migrant_lifecourse/` so the pipeline runs on pandas ≥ 3 (see AGENTS.md).
- [ ] Retire the hardcoded absolute paths in `scripts.py` / `make_site.ipynb`
      (superseded by `scripts/make_site.py`).
- [ ] Optionally register the NAA scraper cache (`national_archives/cache_db.sqlite`)
      as a dataset if it becomes a canonical input.
