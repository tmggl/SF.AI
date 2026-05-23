"""Phase 27.24 — minimal lexical stabilization report."""

from __future__ import annotations

import json
from pathlib import Path

from sf_ai.models.tokenizer import BPETokenizer


ROOT = Path(__file__).resolve().parents[1]


def test_phase27_24_report_passes_micro_probe_but_blocks_runtime() -> None:
    report = json.loads(
        (ROOT / "artifacts/reports/phase27_24_minimal_lexical_stabilization_report.json")
        .read_text(encoding="utf-8")
    )

    assert report["phase"] == "Phase 27.24"
    assert report["status"] == "PASSED_MINIMAL_LEXICAL_STABILIZATION_HOLD_RUNTIME_FOR_CANARY"
    assert report["previous_phase27_23"]["passed"] == 30
    assert report["current"]["passed"] == 32
    assert report["current"]["exact_clean"] == 32
    assert report["current"]["semantic_match"] == 32
    assert report["current"]["guard_passed"] == 32
    assert report["runtime_allowed"] is False
    assert report["sf50m_allowed"] is False
    assert "Phase 27.25" in report["next_phase"]
    assert report["failures"] == []


def test_phase27_24_tokenizer_protects_minimal_lexical_terms() -> None:
    tokenizer = BPETokenizer.load(ROOT / "artifacts/tokenizers/sf_bpe/v4_min_lexical")
    for term in ("التعاون", "الاحترام"):
        ids = tokenizer.encode(term)
        assert len(ids) == 1
        assert tokenizer.decode(ids) == term
