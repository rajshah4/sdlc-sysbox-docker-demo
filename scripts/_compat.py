"""Compatibility helpers for legacy script entry points."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType
from typing import Any


def export_target(namespace: dict[str, Any], caller_file: str, *target_parts: str) -> ModuleType:
    target = Path(caller_file).resolve().parent.joinpath(*target_parts)
    module_name = f"_sdlc_script_{'_'.join(target.with_suffix('').parts[-3:])}"
    spec = importlib.util.spec_from_file_location(module_name, target)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load script target: {target}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    for name, value in vars(module).items():
        if not name.startswith("__"):
            namespace[name] = value
    return module
