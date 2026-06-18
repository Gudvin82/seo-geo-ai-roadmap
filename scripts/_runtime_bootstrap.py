#!/usr/bin/env python3
"""Bootstrap backend imports for standalone repo-level scripts."""

from __future__ import annotations

import sys
from pathlib import Path


def bootstrap_backend_imports() -> Path:
    repo_root = Path(__file__).resolve().parents[1]
    backend_root = repo_root / "app" / "backend"
    backend_app_root = backend_root / "app"

    backend_root_str = str(backend_root)
    if backend_root_str not in sys.path:
        sys.path.insert(0, backend_root_str)

    loaded_app = sys.modules.get("app")
    if loaded_app is not None and hasattr(loaded_app, "__path__"):
        current_paths = [str(item) for item in loaded_app.__path__]
        backend_app_root_str = str(backend_app_root)
        if backend_app_root_str not in current_paths:
            loaded_app.__path__.append(backend_app_root_str)

    return repo_root
