"""Phase 23 — tokenizer v2 artifact and audit checks."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from sf_ai.models.tokenizer import BPETokenizer
from sf_ai.models.tokenizer.policy_audit import load_plain_terms
from sf_ai.training.phase23_tokenizer import build_phase23_tokenizer_audit


ROOT = Path(__file__).resolve().parents[1]
TOKENIZER_DIR = ROOT / "artifacts/tokenizers/sf_bpe/v2"


def test_phase23_tokenizer_v2_artifacts_exist_and_are_sovereign() -> None:
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
    assert meta["vocab_size"] == 4493
    assert meta["merges"] == 4386
    assert meta["training_stats"]["words_seen"] == 23190
    assert meta["training_stats"]["unique_words"] == 2492
    assert meta["training_meta"]["extra_texts_count"] == 0
    assert len(meta["training_meta"]["source_files"]) == 22


def test_phase23_provenance_records_no_pretrained_or_external_data() -> None:
    provenance = json.loads((TOKENIZER_DIR / "provenance.json").read_text(encoding="utf-8"))
    assert provenance["phase"].startswith("Phase 23")
    assert provenance["training_permission"]["granted"] is True
    assert provenance["training_permission"]["required_flag_used"] == "--confirm-phase23-tokenizer"
    assert provenance["data_boundaries"]["external_llm_data_used"] is False
    assert provenance["data_boundaries"]["pretrained_tokenizer_used"] is False
    assert provenance["data_boundaries"]["pretrained_vocab_used"] is False
    assert provenance["data_boundaries"]["pretrained_merges_used"] is False
    assert provenance["data_boundaries"]["synthetic_llm_corpus_used"] is False
    assert provenance["data_boundaries"]["extra_texts_count"] == 0


def test_phase23_audit_marks_v2_ready_for_phase24() -> None:
    report = json.loads((TOKENIZER_DIR / "audit_report.json").read_text(encoding="utf-8"))
    assert report["status"] == "COMPLETED_READY_FOR_PHASE24"
    assert report["corpus"]["training_ready"] == 1550
    assert report["corpus"]["dialects"] == {"msa": 775, "saudi": 775}
    assert report["tokenization_policy"]["protected_terms_covered"] == 30
    assert report["tokenization_policy"]["coverage_ratio"] == 1.0
    assert report["protected_terms_behavior"]["v2_roundtrip_failures"] == []
    assert report["protected_terms_behavior"]["aggressive_split_terms"] == []
    assert report["protected_terms_behavior"]["average_v2_tokens"] < report[
        "protected_terms_behavior"
    ]["average_v1_tokens"]
    assert report["comparison_with_v1"]["vocab_delta"] > 0
    assert report["comparison_with_v1"]["merges_delta"] > 0
    assert report["decision"]["suitable_for_phase24_quality_training"] is True
    assert report["decision"]["runtime_chat_should_use_this_directly"] is False


def test_phase23_tokenizer_round_trips_active_protected_terms() -> None:
    tok = BPETokenizer.load(TOKENIZER_DIR)
    terms = load_plain_terms(ROOT / "resources/tokenization/protected_terms_saudi.txt")
    assert terms
    for term in terms:
        assert tok.decode(tok.encode(term)) == term


def test_phase23_audit_builder_matches_written_report() -> None:
    built = build_phase23_tokenizer_audit()
    written = json.loads((TOKENIZER_DIR / "audit_report.json").read_text(encoding="utf-8"))
    assert built.status == written["status"]
    assert built.tokenizer["vocab_size"] == written["tokenizer"]["vocab_size"]
    assert built.protected_terms_behavior["average_v2_tokens"] == written[
        "protected_terms_behavior"
    ]["average_v2_tokens"]


def test_phase23_audit_cli_is_successful() -> None:
    proc = subprocess.run(
        [sys.executable, "scripts/phase23_tokenizer_audit.py"],
        check=True,
        capture_output=True,
        text=True,
    )
    assert "Phase 23 tokenizer v2 audit" in proc.stdout
    assert "status                        : COMPLETED_READY_FOR_PHASE24" in proc.stdout
    assert "vocab_size                    : 4493" in proc.stdout
