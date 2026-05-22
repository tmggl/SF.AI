"""Loader for the user-authored Saudi seed lexicon (Phase 3.6).

The lexicon lives at:
    resources/lexicons/imported/saudi_seed_v1/saudi_dialect_lexicon_full_seed_v1.jsonl

516 entries, each with fields:
    id, term, normalized_term, variants[], kind, category, dialect_labels[],
    dialect_names_ar[], used_in_places[], meaning_msa, example_saudi, register,
    dialectality, confidence, requires_native_review,
    safety: { sensitive_or_profane, allow_for_generation, recommended_use[] },
    source_basis

Safety policy (enforced here, not in the YAML):
- Default filter for runtime use (e.g. DialectMapper):
    confidence in {"high"}  AND  safety.sensitive_or_profane is False
- Medium/low or "requires_native_review=true" entries are loadable for
  inspection but excluded from generation/use-for surfaces by default.
- "allow_for_generation=false" → never used for any generation surface.

This loader is intentionally **read-only** — the source JSONL is not
mutated. The user remains the editor of record.
"""

from __future__ import annotations

import json
from collections.abc import Iterator
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from sf_ai.core.config import PROJECT_DIR


# ----- paths -----

SAUDI_SEED_DIR: Path = (
    PROJECT_DIR / "resources" / "lexicons" / "imported" / "saudi_seed_v1"
)
SAUDI_SEED_JSONL: Path = SAUDI_SEED_DIR / "saudi_dialect_lexicon_full_seed_v1.jsonl"
SAUDI_SEED_SUMMARY: Path = SAUDI_SEED_DIR / "validation_summary.json"

SOURCE_NAME = "SF.AI Saudi dialect seed v1 (user-authored)"
SOURCE_BASIS_OK = "original_compilation_not_copied_from_mo3jam"


# ----- types -----

@dataclass(frozen=True)
class SaudiSeedSafety:
    sensitive_or_profane: bool = False
    allow_for_generation: bool = True
    recommended_use: tuple[str, ...] = ()


@dataclass(frozen=True)
class SaudiSeedEntry:
    id: str
    term: str
    normalized_term: str
    variants: tuple[str, ...]
    kind: str
    category: str
    dialect_labels: tuple[str, ...]
    dialect_names_ar: tuple[str, ...]
    used_in_places: tuple[str, ...]
    meaning_msa: str
    example_saudi: str
    register: str
    dialectality: str
    confidence: str
    requires_native_review: bool
    safety: SaudiSeedSafety
    source_basis: str
    english_gloss: str = ""
    part_of_speech: str | None = None
    usage_note: str = ""

    @property
    def primary_dialect(self) -> str:
        """Best-guess single dialect label — first in the list, else 'saudi_general'."""
        return self.dialect_labels[0] if self.dialect_labels else "saudi_general"

    def is_safe_for_runtime(self) -> bool:
        return (
            self.confidence == "high"
            and not self.safety.sensitive_or_profane
            and self.safety.allow_for_generation
            and not self.requires_native_review
        )


@dataclass(frozen=True)
class SaudiSeedStats:
    entries_total: int
    entries_safe_runtime: int
    by_confidence: dict[str, int] = field(default_factory=dict)
    by_dialect: dict[str, int] = field(default_factory=dict)
    sensitive_count: int = 0
    requires_review_count: int = 0


# ----- parsing -----

def _parse_safety(raw: Any) -> SaudiSeedSafety:
    raw = raw or {}
    if not isinstance(raw, dict):
        return SaudiSeedSafety()
    return SaudiSeedSafety(
        sensitive_or_profane=bool(raw.get("sensitive_or_profane", False)),
        allow_for_generation=bool(raw.get("allow_for_generation", True)),
        recommended_use=tuple(raw.get("recommended_use") or ()),
    )


def _parse_entry(raw: dict[str, Any]) -> SaudiSeedEntry:
    return SaudiSeedEntry(
        id=str(raw.get("id", "")),
        term=str(raw.get("term", "")),
        normalized_term=str(raw.get("normalized_term", "")),
        variants=tuple(raw.get("variants") or ()),
        kind=str(raw.get("kind", "")),
        category=str(raw.get("category", "")),
        dialect_labels=tuple(raw.get("dialect_labels") or ()),
        dialect_names_ar=tuple(raw.get("dialect_names_ar") or ()),
        used_in_places=tuple(raw.get("used_in_places") or ()),
        meaning_msa=str(raw.get("meaning_msa", "")),
        example_saudi=str(raw.get("example_saudi", "")),
        register=str(raw.get("register", "neutral")),
        dialectality=str(raw.get("dialectality", "high")),
        confidence=str(raw.get("confidence", "low")),
        requires_native_review=bool(raw.get("requires_native_review", False)),
        safety=_parse_safety(raw.get("safety")),
        source_basis=str(raw.get("source_basis", "")),
        english_gloss=str(raw.get("english_gloss") or ""),
        part_of_speech=raw.get("part_of_speech"),
        usage_note=str(raw.get("usage_note") or ""),
    )


def iter_saudi_seed_entries(
    path: str | Path | None = None,
) -> Iterator[SaudiSeedEntry]:
    """Stream entries one at a time. Skips malformed lines (best effort)."""
    p = Path(path) if path is not None else SAUDI_SEED_JSONL
    if not p.exists():
        return
    with p.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                raw = json.loads(line)
            except json.JSONDecodeError:
                continue
            if not isinstance(raw, dict) or not raw.get("term"):
                continue
            yield _parse_entry(raw)


def load_saudi_seed(
    path: str | Path | None = None,
    *,
    safe_only: bool = True,
) -> list[SaudiSeedEntry]:
    """Return entries; by default only the runtime-safe subset."""
    out: list[SaudiSeedEntry] = []
    for entry in iter_saudi_seed_entries(path):
        if safe_only and not entry.is_safe_for_runtime():
            continue
        out.append(entry)
    return out


def saudi_seed_stats(path: str | Path | None = None) -> SaudiSeedStats:
    total = 0
    safe = 0
    by_conf: dict[str, int] = {}
    by_dialect: dict[str, int] = {}
    sensitive = 0
    review = 0
    for entry in iter_saudi_seed_entries(path):
        total += 1
        if entry.is_safe_for_runtime():
            safe += 1
        by_conf[entry.confidence] = by_conf.get(entry.confidence, 0) + 1
        for d in entry.dialect_labels:
            by_dialect[d] = by_dialect.get(d, 0) + 1
        if entry.safety.sensitive_or_profane:
            sensitive += 1
        if entry.requires_native_review:
            review += 1
    return SaudiSeedStats(
        entries_total=total,
        entries_safe_runtime=safe,
        by_confidence=by_conf,
        by_dialect=by_dialect,
        sensitive_count=sensitive,
        requires_review_count=review,
    )


def attribution_block() -> str:
    """Attribution string. Use in any artifact derived from this lexicon."""
    return (
        "مصدر قاموس اللهجات السعودية:\n"
        "saudi_dialect_lexicon_full_seed_v1 — تأليف مستخدم SF.AI.\n"
        "غير منسوخ من Mo3jam. إن أضيفت لاحقًا مدخلات من Mo3jam بإذن، يجب "
        "وضع إسناد منفصل: معجم — اللهجة السعودية (https://ar.mo3jam.com/dialect/Saudi)."
    )
