"""Phase 27.124 adapter skeleton tests with synthetic terms only."""

from __future__ import annotations

import pytest

from sf_ai.reference_layers import SinaLabSynonymsReferenceAdapter, SynonymReferenceRecord


def _adapter() -> SinaLabSynonymsReferenceAdapter:
    records = (
        SynonymReferenceRecord(
            canonical="مصطلح تجريبي",
            synonyms=("عبارة اختبارية", "لفظ فحص"),
            quality_band="high",
            source_id="synthetic_reference",
            record_id="synthetic-001",
        ),
        SynonymReferenceRecord(
            canonical="تعبير مصطنع",
            synonyms=("جملة وهمية",),
            quality_band="medium",
            source_id="synthetic_reference",
            record_id="synthetic-002",
        ),
    )
    return SinaLabSynonymsReferenceAdapter(records)


def test_adapter_indexes_synthetic_terms_without_runtime_activation() -> None:
    adapter = _adapter()

    assert adapter.record_count == 2
    assert adapter.index_key_count == 5
    assert adapter.runtime_lookup_enabled is False
    assert adapter.chat_integration_enabled is False


def test_lookup_returns_redacted_hashes_for_synthetic_match() -> None:
    adapter = _adapter()

    result = adapter.lookup("عبارة اختبارية", include_terms_in_runtime_response=True)

    assert result.matched is True
    assert result.result_count == 1
    assert result.quality_bands == ("high",)
    assert result.source_ids == ("synthetic_reference",)
    assert len(result.query_hash) == 64
    assert len(result.query_normalized_hash) == 64
    assert len(result.result_hashes) == 1
    assert len(result.result_hashes[0]) == 64
    assert result.redaction_applied is True
    assert result.terms_included is False
    assert result.term_values == ()
    assert result.runtime_lookup_enabled is False
    assert result.chat_integration_enabled is False


def test_lookup_respects_quality_threshold_and_result_cap() -> None:
    adapter = _adapter()

    high = adapter.lookup("تعبير مصطنع", min_quality_band="high")
    medium = adapter.lookup("تعبير مصطنع", min_quality_band="medium", max_results=50)

    assert high.matched is False
    assert high.result_count == 0
    assert medium.matched is True
    assert medium.result_count == 1
    assert medium.quality_bands == ("medium",)


def test_lookup_normalizes_arabic_variants_aggressively() -> None:
    adapter = _adapter()

    result = adapter.lookup("عباره إختبارية")

    assert result.matched is True
    assert result.result_count == 1


def test_adapter_validates_policy_bounds() -> None:
    with pytest.raises(ValueError, match="max_results_default"):
        SinaLabSynonymsReferenceAdapter(max_results_default=0)

    with pytest.raises(ValueError, match="max_results_cap"):
        SinaLabSynonymsReferenceAdapter(max_results_default=5, max_results_cap=4)

    with pytest.raises(ValueError, match="max_results"):
        _adapter().lookup("مصطلح تجريبي", max_results=0)
