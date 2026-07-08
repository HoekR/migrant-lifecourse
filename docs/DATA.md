# Data layout and manifest

Decouple code from disk layout using `data_manifest.toml` and `data_io`.

## Tiers (edit in `data_manifest.toml`)

| Tier | Role in this repo |
|------|-------------------|
| **hot** | Repo root (`.`) — committed inputs (`data/`) and rendered pages (`personen/`) |
| **scratch** | Ephemeral / intermediate outputs (`scratch/`, gitignored) |

Other tiers (`warm`, `cold`, `collab`) from the template are available if the project
later needs large canonical or archival storage.

## Day-zero checklist

1. `cp data_manifest.toml.example data_manifest.toml` — the defaults use repo-relative roots.
2. Optional: `cp data_manifest.local.toml.example data_manifest.local.toml` for per-machine overrides (gitignored).
3. `uv sync`
4. `uv run python -m data_io.check`
5. Add `[datasets.*]` entries before writing scripts that read/write data.

## Datasets

| Logical name | Tier | Phase | Path |
|--------------|------|-------|------|
| `lifecourses_workbook` | hot | explore | `data/Lifecourses NA tentoonstelling.xlsx` |
| `person_names` | hot | explore | `data/names.json` |
| `timeline_events` | scratch | semi | `timeline_events.jsonl` |
| `timeline_pages` | hot | semi | `personen/` |

## Three-phase pipeline

| Phase | Format | Save via |
|-------|--------|----------|
| explore | xlsx, json, ad-hoc notebooks | (read only) |
| semi | jsonl + `.meta.toml` | `save_semi_structured(...)` |
| frozen | parquet + `.meta.json` | `save_parquet(...)` |

Promote to Parquet only after schema review.

## API

```python
from data_io import resolve, load, save_semi_structured, save_parquet

workbook = resolve("lifecourses_workbook")   # -> absolute Path
names = load("person_names")                  # -> parsed JSON dict

save_semi_structured(
    records,
    logical_name="timeline_events",
    parent_sources=["lifecourses_workbook"],
    description="Flattened per-event lifecourse records.",
    script=__file__,
)
```

## Legacy / orphan files

The dighum_template `llm_archivist` tools (`archive-inventory` / `archive-scan`) are **not**
vendored here (no LLM archival need yet). If you migrate legacy exports without `data_io`
sidecars, clone [llm_archivist](https://github.com/HoekR/llm_archivist) and follow
`dighum_template/docs/NEW_REPO.md` §5. Do **not** run archivist tools on `data_io` outputs.
