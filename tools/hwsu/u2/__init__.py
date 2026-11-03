"""HWSU phase-2 package (API_U2.md section 0; R-0223-3).

Importing it appends this directory to sys.path so that the phase-2 modules import one another
by their flat names (hwsu_model, hwsu_known, ...), the convention of the phase-1 modules.
"""

from __future__ import annotations

import sys
from pathlib import Path

_HERE = str(Path(__file__).resolve().parent)
if _HERE not in sys.path:
    sys.path.append(_HERE)
