"""migrant_lifecourse — convert lifecourse spreadsheets into timeline HTML pages.

Reusable pipeline modules for the "Dutch migrants to/from Australia" exhibition site.
The manifest-driven build entrypoint lives in ``scripts/make_site.py``.
"""

from migrant_lifecourse.names import readnames, writenames
from migrant_lifecourse.sheet2timeline import Sheet2Timeline

__all__ = ["Sheet2Timeline", "readnames", "writenames"]
