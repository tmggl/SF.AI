"""Phase 12 tokenizer v1 artifact checks."""

from __future__ import annotations

import json
from pathlib import Path

from sf_ai.models.tokenizer import BPETokenizer


ROOT = Path(__file__).resolve().parent.parent
TOKENIZER_DIR = ROOT / "artifacts/tokenizers/sf_bpe/v1"


def test_phase12_tokenizer_v1_artifacts_exist_and_are_sovereign() -> None:
    required = {
        "vocab.json",
        "merges.txt",
        "meta.json",
        "tokenizer_config.json",
        "provenance.json",
        "audit_report.json",
    }
    assert required.issubset({path.name for path in TOKENIZER_DIR.iterdir()})

    meta = json.loads((TOKENIZER_DIR / "meta.json").read_text(encoding="utf-8"))
    assert meta["sf_origin"] is True
    assert meta["tokenizer_type"] == "bpe"
    assert meta["vocab_size"] == 261
    assert meta["merges"] == 218
    assert meta["training_meta"]["extra_texts_count"] == 0

    provenance = json.loads((TOKENIZER_DIR / "provenance.json").read_text(encoding="utf-8"))
    assert provenance["training_permission"]["granted"] is True
    assert provenance["data_boundaries"]["pretrained_tokenizer_used"] is False
    assert provenance["data_boundaries"]["synthetic_llm_corpus_used"] is False


def test_phase12_tokenizer_v1_loads_and_round_trips_known_text() -> None:
    tok = BPETokenizer.load(TOKENIZER_DIR)
    text = "وش معنى سعودي"
    ids = tok.encode(text)
    assert ids
    assert tok.decode(ids) == text


def test_phase12_audit_report_records_msa_gap() -> None:
    report = json.loads((TOKENIZER_DIR / "audit_report.json").read_text(encoding="utf-8"))
    assert report["status"] == "COMPLETED_WITH_LIMITS"
    assert report["decision"]["phase12_training_started"] is True
    assert report["decision"]["suitable_for_phase13_smoke"] is True
    assert report["language_balance"]["missing_required_dialects"] == ["msa"]
