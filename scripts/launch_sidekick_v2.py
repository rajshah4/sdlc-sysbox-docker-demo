#!/usr/bin/env python3
"""Compatibility wrapper for scripts/sidekick/launch_sidekick_v2.py."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _compat import export_target


_MODULE = export_target(globals(), __file__, "sidekick", "launch_sidekick_v2.py")

if __name__ == "__main__":
    raise SystemExit(_MODULE.main())
