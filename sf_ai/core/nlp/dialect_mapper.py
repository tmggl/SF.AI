"""DialectMapper — maps dialect surface forms → canonical MSA-ish hints.

Operates on the post-normalized Arabic text. Multi-word phrases are tried
first (longest-match-first) before single tokens. The mapper emits
DialectSignal records describing what was rewritten and which dialect we
detected. The Router uses these as `dialect_alias` signals.

Does NOT rewrite the user's visible message. The canonical form lives only
on the canonical_text lens of NLPAnalysis; the original is preserved for the
chat module to echo back faithfully.
"""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Iterable

import yaml

from sf_ai.core.nlp._lexicons import load_lexicon
from sf_ai.core.nlp.types import DialectSignal


# Default path to the Mo3jam-derived Saudi lexicon (Phase 3.5). The mapper
# refuses to load it unless `ENABLE_MO3JAM_SAUDI_LEXICON=true` is set, so the
# default behavior of SF.AI is unchanged.
_MO3JAM_SAUDI_YAML = (
    Path(__file__).resolve().parents[3]
    / "resources" / "lexicons" / "imported" / "mo3jam" / "saudi_dialect_terms.yaml"
)


def _env_flag(name: str) -> bool:
    val = os.environ.get(name, "").strip().lower()
    return val in {"1", "true", "yes", "on"}


def _wider_dialects_enabled() -> bool:
    """Keep runtime focused on MSA + Saudi unless explicitly widened."""
    return _env_flag("ENABLE_WIDER_ARABIC_DIALECTS")


def _load_mo3jam_saudi_entries(path: Path) -> list[tuple[str, str, str, float]]:
    """Read Mo3jam YAML and return (surface, canonical, dialect, conf) tuples.

    Source attribution is required: the file must declare credit_required=true
    in its metadata. Each entry contributes a `saudi` dialect signal whose
    canonical form is the term's definition (so downstream matchers see the
    full meaning). The router uses the dialect tag for voting; the canonical
    string is what gets substituted into the canonical_text lens.
    """
    if not path.exists():
        return []
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    meta = data.get("metadata") or {}
    if not meta.get("credit_required", False):
        # Refuse silently rather than raising — the rest of the system stays
        # functional, and the operator can re-import to fix the metadata.
        return []
    entries: list[tuple[str, str, str, float]] = []
    for entry in data.get("terms") or ():
        if not isinstance(entry, dict):
            continue
        term = str(entry.get("term") or "").strip()
        if not term:
            continue
        # Use the definition as the canonical form when present, otherwise the
        # normalized term — that way matching still helps even if a definition
        # is missing for that record.
        canonical = (
            str(entry.get("definition") or "").strip()
            or str(entry.get("normalized_term") or "").strip()
            or term
        )
        conf = float(entry.get("confidence", 1.0))
        entries.append((term, canonical, "saudi", conf))
    return entries


def _load_saudi_seed_entries(
    path: Path | None,
) -> list[tuple[str, str, str, float]]:
    """Load Saudi seed v1 entries as DialectMapper tuples.

    Each entry contributes a `saudi` signal. The canonical form is the MSA
    meaning where present, else the normalized term. Confidence is mapped:
    high → 0.95, medium → 0.7, low → 0.5 (we still filter to high by default
    via `is_safe_for_runtime` in the loader).
    """
    try:
        from sf_ai.datasets.saudi_seed import load_saudi_seed
    except Exception:
        return []
    try:
        entries = load_saudi_seed(path=path, safe_only=True)
    except Exception:
        return []
    out: list[tuple[str, str, str, float]] = []
    for e in entries:
        surface = e.term.strip()
        if not surface:
            continue
        canonical = (e.meaning_msa.strip() or e.normalized_term.strip() or surface)
        conf = 0.95 if e.confidence == "high" else 0.7 if e.confidence == "medium" else 0.5
        out.append((surface, canonical, "saudi", conf))
        # Also surface variants as additional entry points pointing to the
        # same canonical form.
        for v in e.variants:
            v = v.strip()
            if v and v != surface:
                out.append((v, canonical, "saudi", conf * 0.95))
    return out


def _flatten(entries: dict[str, dict], dialect: str) -> list[tuple[str, str, str, float]]:
    """Flatten YAML entries into (surface, canonical, dialect, conf) tuples."""
    out: list[tuple[str, str, str, float]] = []
    for surface, body in entries.items():
        if not isinstance(body, dict):
            continue
        canonical = str(body.get("ar", surface))
        conf = float(body.get("conf", 0.7))
        out.append((surface, canonical, dialect, conf))
    return out


class DialectMapper:
    def __init__(
        self,
        mo3jam_saudi_path: Path | None = None,
        saudi_seed_path: Path | None = None,
    ) -> None:
        entries: list[tuple[str, str, str, float]] = []
        gulf = load_lexicon("dialects_gulf.yaml")
        # For now SF.AI is intentionally tuned for MSA + Saudi. The original
        # Gulf seed entries are Saudi-compatible enough for phase routing, so
        # we label them as `saudi` in runtime metadata. Broader Arabic dialects
        # stay available behind an explicit flag for later work.
        entries.extend(_flatten(gulf.get("mappings") or {}, "saudi"))
        if _wider_dialects_enabled():
            common = load_lexicon("dialects_common_arabic.yaml")
            entries.extend(_flatten(common.get("egyptian") or {}, "egyptian"))
            entries.extend(_flatten(common.get("levantine") or {}, "levantine"))
            entries.extend(_flatten(common.get("iraqi") or {}, "iraqi"))

        # Phase 3.5: optionally load Mo3jam Saudi lexicon. Off by default.
        # Enable via env var ENABLE_MO3JAM_SAUDI_LEXICON=true. The Mo3jam data
        # is kept separate from dialects_gulf.yaml so the original SF.AI
        # seed lexicons stay attribution-free and the imported data stays
        # clearly marked as "credit_required" (handled by the loader).
        if _env_flag("ENABLE_MO3JAM_SAUDI_LEXICON"):
            path = mo3jam_saudi_path or _MO3JAM_SAUDI_YAML
            entries.extend(_load_mo3jam_saudi_entries(path))

        # Phase 3.6: optionally load the user-authored Saudi seed lexicon
        # (516 hand-curated entries, not copied from Mo3jam). Off by default.
        # Enable via ENABLE_SAUDI_SEED_V1_LEXICON=true. Safety filter applied:
        # only confidence=high + not sensitive + not requiring native review.
        if _env_flag("ENABLE_SAUDI_SEED_V1_LEXICON"):
            entries.extend(_load_saudi_seed_entries(saudi_seed_path))

        # Longest surface first so multi-word phrases get a chance before tokens.
        entries.sort(key=lambda e: -len(e[0]))
        self._entries = entries

    def detect_dialect(self, signals: Iterable[DialectSignal]) -> str:
        votes: dict[str, float] = {}
        for s in signals:
            votes[s.dialect] = votes.get(s.dialect, 0.0) + s.confidence
        if not votes:
            return "msa"
        return max(votes.items(), key=lambda kv: kv[1])[0]

    def map_text(self, text: str) -> tuple[str, tuple[DialectSignal, ...]]:
        """Return (canonical_text, signals). Longest-match-first replacement."""
        if not text:
            return "", ()

        signals: list[DialectSignal] = []
        working = text

        for surface, canonical, dialect, conf in self._entries:
            # Word-boundary match for single tokens; substring match for phrases
            # with spaces (already covers boundaries naturally in Arabic chat).
            if " " in surface:
                if surface in working:
                    working = working.replace(surface, canonical)
                    signals.append(
                        DialectSignal(
                            surface=surface,
                            canonical=canonical,
                            dialect=dialect,
                            confidence=conf,
                        )
                    )
            else:
                pattern = re.compile(rf"(?<!\S){re.escape(surface)}(?!\S)")
                if pattern.search(working):
                    working = pattern.sub(canonical, working)
                    signals.append(
                        DialectSignal(
                            surface=surface,
                            canonical=canonical,
                            dialect=dialect,
                            confidence=conf,
                        )
                    )

        return working, tuple(signals)
