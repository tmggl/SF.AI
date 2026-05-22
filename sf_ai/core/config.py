"""Core configuration helpers — separate from the FastAPI app settings.

Holds constants used across the core brain (router thresholds, paths, etc.).
Kept tiny on purpose; expand only when a value is reused in multiple modules.
"""

from __future__ import annotations

from pathlib import Path

CORE_DIR: Path = Path(__file__).resolve().parent
PACKAGE_DIR: Path = CORE_DIR.parent
PROJECT_DIR: Path = PACKAGE_DIR.parent
RESOURCES_DIR: Path = PROJECT_DIR / "resources"
DEFAULT_REGISTRY_PATH: Path = CORE_DIR / "index" / "default_registry.yaml"

# Routing thresholds. Tunable later from settings.
MIN_DOMAIN_SCORE: float = 0.5
FUZZY_MATCH_THRESHOLD: float = 0.85
HASHING_VECTOR_BUCKETS: int = 2048

# Confidence shaping: confidence = score / (score + CONFIDENCE_SOFTENING).
# Score 0 → 0.0, score 3 → 0.6, score 5 → 0.71, score 13 → 0.87. Bounded < 1.0.
CONFIDENCE_SOFTENING: float = 2.0
