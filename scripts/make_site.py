#!/usr/bin/env python
"""Build the migrant lifecourse timeline site from the data manifest.

Run from the repository root (so data_io can locate data_manifest.toml):

    uv run python scripts/make_site.py
    # or, via the console script:
    uv run make-site
"""

from migrant_lifecourse.build_site import main

if __name__ == "__main__":
    main()
