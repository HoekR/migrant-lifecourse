"""Manifest-driven site builder for the migrant lifecourse timelines.

Compliant entrypoint (replaces the hardcoded absolute paths in the exploratory
``make_site.ipynb``): input and output locations come from ``data_manifest.toml``
via ``data_io.resolve`` / ``data_io.load``, and the structured event intermediate
is written with provenance sidecars through ``data_io.save_semi_structured``.

Datasets (see data_manifest.toml):
    lifecourses_workbook  input  Excel workbook, one sheet per person
    person_names          input  {key: sheet name} JSON index
    timeline_events       semi   flattened per-event JSONL (+ .meta.toml provenance)
    timeline_pages        semi   rendered per-person HTML timeline pages
"""

from __future__ import annotations

import warnings
from pathlib import Path

import pandas as pd

from data_io import load, resolve, save_semi_structured
from migrant_lifecourse.names import readnames
from migrant_lifecourse.sheet2timeline import Sheet2Timeline
from migrant_lifecourse.settings import schemes
from migrant_lifecourse.templates import (
    container,
    linktemplate,
    mcard,
    mcardtmplt,
    naa_templ,
    toptmpt,
    tmplt,
    youtubetempl,
)
from migrant_lifecourse.patterns import pat1, pat2

warnings.filterwarnings("ignore")


def build_frames(excelfile: pd.ExcelFile, names: dict[str, str]) -> dict[str, dict]:
    """Build per-person lifeline / profile / family fragments."""
    frames: dict[str, dict] = {}
    for key, sheet_name in names.items():
        ob = Sheet2Timeline(
            sheet_name,
            excelfile,
            schemes,
            mcard=mcard,
            mcardtmplt=mcardtmplt,
            naa_templt=naa_templ,
            pat1=pat1,
            pat2=pat2,
        )
        if len(ob.df) > 0:
            frames[key] = {
                "lifeline": ob.render(),
                "profile": ob.make_personcard(),
                "family": ob.make_family(),
            }
    return frames


def flatten_events(frames: dict[str, dict]) -> list[dict]:
    """Flatten per-person lifelines into provenance-friendly event records."""
    records: list[dict] = []
    for key, frame in frames.items():
        lifeline = frame.get("lifeline")
        if lifeline is None or len(lifeline) == 0:
            continue
        for row in lifeline.to_dict(orient="records"):
            records.append(
                {
                    "person_key": key,
                    "name": row.get("nm"),
                    "date": row.get("date"),
                    "event": row.get("event"),
                    "event_html": row.get("eventtext"),
                    "side": row.get("lr"),
                }
            )
    return records


def render_pages(frames: dict[str, dict], out_dir: Path) -> list[Path]:
    """Render each person's timeline HTML page into ``out_dir``."""
    out_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for key, frame in frames.items():
        lifeline = frame.get("lifeline")
        if lifeline is None or len(lifeline) == 0:
            continue
        pieces = [
            tmplt.substitute(
                l_or_r=row.get("lr"),
                date=row.get("date"),
                item=row.get("eventtext"),
            )
            for row in lifeline.to_dict(orient="records")
        ]
        body = toptmpt.substitute(
            events="\n".join(pieces),
            personinfo=frame["profile"],
            family=frame["family"],
        )
        out_path = out_dir / f"{key}.html"
        out_path.write_text(container.substitute(body=body), encoding="utf-8")
        written.append(out_path)
    return written


def build_site() -> dict[str, object]:
    """Resolve inputs from the manifest, write provenance JSONL, render HTML."""
    excelfile = pd.ExcelFile(resolve("lifecourses_workbook"))
    names = readnames(resolve("person_names"))

    frames = build_frames(excelfile, names)

    events = flatten_events(frames)
    events_path = save_semi_structured(
        events,
        logical_name="timeline_events",
        parent_sources=["lifecourses_workbook"],
        description="Flattened per-event lifecourse records rendered into timeline pages.",
        script=__file__,
    )

    out_dir = resolve("timeline_pages")
    pages = render_pages(frames, out_dir)

    return {
        "people": len(frames),
        "events": len(events),
        "events_jsonl": events_path,
        "pages": pages,
        "pages_dir": out_dir,
    }


def main() -> None:
    result = build_site()
    print(f"People processed : {result['people']}")
    print(f"Event records     : {result['events']}")
    print(f"Events JSONL      : {result['events_jsonl']}")
    print(f"Pages directory   : {result['pages_dir']}")
    print(f"Pages written     : {len(result['pages'])}")


if __name__ == "__main__":
    main()
