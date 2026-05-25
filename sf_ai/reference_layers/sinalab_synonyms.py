"""SinaLab Synonyms reference adapter skeleton.

Phase 27.124 scope:
- adapter code only;
- no ChatModule/runtime wiring;
- no corpus/tokenizer/training writes;
- redacted lookup results by default and by policy.

The adapter can be unit-tested with synthetic records. Real local reference
records remain gitignored and are not imported by this module.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from typing import Literal

from sf_ai.core.nlp.arabic_normalizer import ArabicNormalizer

QualityBand = Literal["high", "medium", "low"]

_QUALITY_RANK: dict[QualityBand, int] = {"low": 0, "medium": 1, "high": 2}


@dataclass(frozen=True)
class SynonymReferenceRecord:
    """One local synonym reference record.

    Tests may use synthetic terms. Real source terms must remain in the local
    gitignored reference layer until a later runtime gate allows otherwise.
    """

    canonical: str
    synonyms: tuple[str, ...]
    quality_band: QualityBand = "high"
    source_id: str = "synthetic_reference"
    record_id: str = ""

    def terms(self) -> tuple[str, ...]:
        return (self.canonical, *self.synonyms)


@dataclass(frozen=True)
class SynonymLookupResult:
    """Redacted aggregate lookup result.

    `term_values` is intentionally empty unless a future explicit gate enables
    term display. Phase 27.124 keeps it empty even when the caller asks.
    """

    query_hash: str
    query_normalized_hash: str
    matched: bool
    result_count: int
    result_hashes: tuple[str, ...]
    quality_bands: tuple[QualityBand, ...]
    source_ids: tuple[str, ...]
    redaction_applied: bool
    terms_included: bool
    term_values: tuple[str, ...] = field(default_factory=tuple)
    runtime_lookup_enabled: bool = False
    chat_integration_enabled: bool = False


class SinaLabSynonymsReferenceAdapter:
    """Small, local, redacted synonym-reference adapter skeleton."""

    def __init__(
        self,
        records: tuple[SynonymReferenceRecord, ...] | list[SynonymReferenceRecord] = (),
        *,
        max_results_default: int = 5,
        max_results_cap: int = 10,
        default_quality_band: QualityBand = "high",
        runtime_lookup_enabled: bool = False,
        chat_integration_enabled: bool = False,
        allow_term_display: bool = False,
        normalizer: ArabicNormalizer | None = None,
    ) -> None:
        if max_results_default < 1:
            raise ValueError("max_results_default must be positive")
        if max_results_cap < max_results_default:
            raise ValueError("max_results_cap must be >= max_results_default")
        if default_quality_band not in _QUALITY_RANK:
            raise ValueError("default_quality_band must be high, medium, or low")

        self.max_results_default = max_results_default
        self.max_results_cap = max_results_cap
        self.default_quality_band = default_quality_band
        self.runtime_lookup_enabled = runtime_lookup_enabled
        self.chat_integration_enabled = chat_integration_enabled
        self.allow_term_display = allow_term_display
        self._normalizer = normalizer or ArabicNormalizer()
        self._records = tuple(records)
        self._index = self._build_index(self._records)

    @property
    def record_count(self) -> int:
        return len(self._records)

    @property
    def index_key_count(self) -> int:
        return len(self._index)

    def lookup(
        self,
        query_text: str,
        *,
        max_results: int | None = None,
        min_quality_band: QualityBand | None = None,
        include_terms_in_runtime_response: bool = False,
    ) -> SynonymLookupResult:
        """Lookup a query and return a redacted aggregate result.

        This method does not imply runtime activation. It is a local adapter
        primitive; wiring it into chat remains blocked by phase gates.
        """

        limit = self._bounded_max_results(max_results)
        min_band = min_quality_band or self.default_quality_band
        if min_band not in _QUALITY_RANK:
            raise ValueError("min_quality_band must be high, medium, or low")

        normalized = self._normalize(query_text)
        records = [
            record
            for record in self._index.get(normalized, ())
            if _QUALITY_RANK[record.quality_band] >= _QUALITY_RANK[min_band]
        ][:limit]

        include_terms = (
            include_terms_in_runtime_response
            and self.allow_term_display
            and self.runtime_lookup_enabled
        )
        term_values = tuple(record.canonical for record in records) if include_terms else ()
        result_hashes = tuple(self._record_hash(record) for record in records)
        quality_bands = tuple(record.quality_band for record in records)
        source_ids = tuple(sorted({record.source_id for record in records}))

        return SynonymLookupResult(
            query_hash=self._hash_text(query_text),
            query_normalized_hash=self._hash_text(normalized),
            matched=bool(records),
            result_count=len(records),
            result_hashes=result_hashes,
            quality_bands=quality_bands,
            source_ids=source_ids,
            redaction_applied=not include_terms,
            terms_included=include_terms,
            term_values=term_values,
            runtime_lookup_enabled=self.runtime_lookup_enabled,
            chat_integration_enabled=self.chat_integration_enabled,
        )

    def _bounded_max_results(self, max_results: int | None) -> int:
        requested = self.max_results_default if max_results is None else max_results
        if requested < 1:
            raise ValueError("max_results must be positive")
        return min(requested, self.max_results_cap)

    def _normalize(self, text: str) -> str:
        return self._normalizer.normalize_aggressive(text).casefold()

    def _build_index(
        self, records: tuple[SynonymReferenceRecord, ...]
    ) -> dict[str, tuple[SynonymReferenceRecord, ...]]:
        buckets: dict[str, list[SynonymReferenceRecord]] = {}
        for record in records:
            if record.quality_band not in _QUALITY_RANK:
                raise ValueError("record quality_band must be high, medium, or low")
            for term in record.terms():
                key = self._normalize(term)
                if not key:
                    continue
                buckets.setdefault(key, []).append(record)
        return {key: tuple(value) for key, value in buckets.items()}

    def _record_hash(self, record: SynonymReferenceRecord) -> str:
        material = "\u241f".join(
            (
                record.source_id,
                record.record_id,
                self._normalize(record.canonical),
                record.quality_band,
            )
        )
        return self._hash_text(material)

    @staticmethod
    def _hash_text(text: str) -> str:
        return hashlib.sha256(text.encode("utf-8")).hexdigest()
