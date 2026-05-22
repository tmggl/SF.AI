"""Tiny shared YAML loader for the NLP layer.

Centralizes path resolution and caching so each component doesn't reinvent
file IO. Caches are keyed by absolute path, so reloads happen automatically
if the path changes.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

from sf_ai.core.config import RESOURCES_DIR

LEXICONS_DIR: Path = RESOURCES_DIR / "lexicons"


@lru_cache(maxsize=64)
def load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data or {}


def lexicon_path(name: str) -> Path:
    """Return absolute path to a lexicon file inside resources/lexicons/."""
    return LEXICONS_DIR / name


def load_lexicon(name: str) -> dict[str, Any]:
    """Convenience: load a lexicon by file name (e.g. 'arabizi_map.yaml')."""
    return load_yaml(lexicon_path(name))
