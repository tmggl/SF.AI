"""Pytest configuration for SF.AI."""

from __future__ import annotations

import sys
from pathlib import Path

# Make project root importable when tests run from repo root.
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
