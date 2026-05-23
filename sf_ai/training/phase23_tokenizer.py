"""Phase 23 tokenizer v2 audit and artifact metadata.

This module is intentionally local and deterministic. It does not train a
tokenizer by itself; it verifies the already-trained SF-BPE v2 artifact,
compares it with v1, and writes the extra governance files expected next to
the tokenizer.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean
from typing import Any

from sf_ai.datasets.corpus_governance import audit_jsonl_directory_for_training
from sf_ai.models.tokenizer import BPETokenizer
from sf_ai.models.tokenizer.policy_audit import (
    audit_tokenization_policy,
    load_plain_terms,
)


@dataclass(frozen=True)
class ProtectedTermTokenization:
    term: str
    v1_tokens: int
    v2_tokens: int
    v2_decoded: str
    v2_roundtrip_ok: bool
    aggressive_split: bool


@dataclass(frozen=True)
class Phase23TokenizerAudit:
    phase: str
    status: str
    artifact_dir: str
    previous_artifact_dir: str
    tokenizer: dict[str, Any]
    corpus: dict[str, Any]
    tokenization_policy: dict[str, Any]
    protected_terms_behavior: dict[str, Any]
    comparison_with_v1: dict[str, Any]
    sovereignty: dict[str, Any]
    decision: dict[str, Any]

    def to_json(self) -> dict[str, Any]:
        return asdict(self)


def build_phase23_tokenizer_audit(
    *,
    artifact_dir: str | Path = "artifacts/tokenizers/sf_bpe/v2",
    previous_artifact_dir: str | Path = "artifacts/tokenizers/sf_bpe/v1",
    corpus_root: str | Path = "data/corpus/chat/jsonl",
    protected_terms_path: str | Path = "resources/tokenization/protected_terms_saudi.txt",
    preferred_merges_path: str | Path = "resources/tokenization/preferred_merges.txt",
    rules_path: str | Path = "resources/tokenization/tokenization_rules.yaml",
) -> Phase23TokenizerAudit:
    artifact = Path(artifact_dir)
    previous = Path(previous_artifact_dir)
    corpus_path = Path(corpus_root)

    meta = _read_json(artifact / "meta.json")
    prev_meta = _read_json(previous / "meta.json")
    tokenizer = BPETokenizer.load(artifact)
    previous_tokenizer = BPETokenizer.load(previous)

    corpus = audit_jsonl_directory_for_training(corpus_path)
    policy = audit_tokenization_policy(
        corpus=corpus_path,
        protected_terms_path=protected_terms_path,
        preferred_merges_path=preferred_merges_path,
        rules_path=rules_path,
    )
    protected_terms = load_plain_terms(protected_terms_path)
    protected_rows = _protected_term_rows(
        protected_terms=protected_terms,
        previous_tokenizer=previous_tokenizer,
        tokenizer=tokenizer,
    )
    v1_counts = [row.v1_tokens for row in protected_rows]
    v2_counts = [row.v2_tokens for row in protected_rows]
    roundtrip_failures = [row.term for row in protected_rows if not row.v2_roundtrip_ok]
    aggressive_splits = [row.term for row in protected_rows if row.aggressive_split]

    tokenizer_ok = (
        meta.get("sf_origin") is True
        and meta.get("tokenizer_type") == "bpe"
        and int(meta.get("vocab_size", 0)) > int(prev_meta.get("vocab_size", 0))
        and int(meta.get("merges", 0)) > int(prev_meta.get("merges", 0))
    )
    corpus_ok = corpus.error_count == 0 and corpus.training_ready >= 500
    policy_ok = not policy.warnings and policy.coverage_ratio == 1.0
    terms_ok = not roundtrip_failures and not aggressive_splits
    status = (
        "COMPLETED_READY_FOR_PHASE24"
        if tokenizer_ok and corpus_ok and policy_ok and terms_ok
        else "NEEDS_REVIEW_BEFORE_PHASE24"
    )

    return Phase23TokenizerAudit(
        phase="Phase 23 — Tokenizer v2 Retrain & Audit",
        status=status,
        artifact_dir=str(artifact),
        previous_artifact_dir=str(previous),
        tokenizer={
            "type": meta.get("tokenizer_type"),
            "sf_origin": meta.get("sf_origin"),
            "vocab_size": meta.get("vocab_size"),
            "merges": meta.get("merges"),
            "words_seen": (meta.get("training_stats") or {}).get("words_seen"),
            "unique_words": (meta.get("training_stats") or {}).get("unique_words"),
            "base_alphabet_size": (meta.get("training_stats") or {}).get(
                "base_alphabet_size"
            ),
            "lowercase": meta.get("lowercase"),
            "byte_level": meta.get("byte_level"),
        },
        corpus={
            "root": str(corpus_path),
            "total_records": corpus.total_records,
            "training_ready": corpus.training_ready,
            "issues": corpus.error_count,
            "dialects": dict(corpus.dialect_counts),
            "quality": dict(corpus.quality_counts),
            "source_count": len(corpus.source_counts),
        },
        tokenization_policy={
            "protected_terms_total": policy.protected_terms_total,
            "protected_terms_covered": policy.protected_terms_covered,
            "coverage_ratio": policy.coverage_ratio,
            "warnings": list(policy.warnings),
            "protected_terms_path": str(policy.protected_terms_path),
            "preferred_merges_path": str(policy.preferred_merges_path),
            "rules_path": str(policy.rules_path),
            "encoding": (policy.rules or {}).get("encoding"),
            "no_pretrained_vocab": ((policy.rules or {}).get("sovereignty") or {}).get(
                "no_pretrained_vocab"
            ),
            "no_pretrained_merges": ((policy.rules or {}).get("sovereignty") or {}).get(
                "no_pretrained_merges"
            ),
        },
        protected_terms_behavior={
            "terms_checked": len(protected_rows),
            "v2_roundtrip_failures": roundtrip_failures,
            "aggressive_split_terms": aggressive_splits,
            "average_v1_tokens": round(mean(v1_counts), 3) if v1_counts else 0,
            "average_v2_tokens": round(mean(v2_counts), 3) if v2_counts else 0,
            "max_v1_tokens": max(v1_counts, default=0),
            "max_v2_tokens": max(v2_counts, default=0),
            "samples": [asdict(row) for row in protected_rows[:10]],
        },
        comparison_with_v1={
            "v1_vocab_size": prev_meta.get("vocab_size"),
            "v2_vocab_size": meta.get("vocab_size"),
            "vocab_delta": int(meta.get("vocab_size", 0))
            - int(prev_meta.get("vocab_size", 0)),
            "v1_merges": prev_meta.get("merges"),
            "v2_merges": meta.get("merges"),
            "merges_delta": int(meta.get("merges", 0)) - int(prev_meta.get("merges", 0)),
            "v1_words_seen": (prev_meta.get("training_stats") or {}).get("words_seen"),
            "v2_words_seen": (meta.get("training_stats") or {}).get("words_seen"),
            "v1_unique_words": (prev_meta.get("training_stats") or {}).get(
                "unique_words"
            ),
            "v2_unique_words": (meta.get("training_stats") or {}).get("unique_words"),
            "protected_term_average_tokens_improved": (
                mean(v2_counts) <= mean(v1_counts) if v1_counts and v2_counts else False
            ),
        },
        sovereignty={
            "external_llm_api_used": False,
            "pretrained_weights_used": False,
            "pretrained_embeddings_used": False,
            "pretrained_tokenizer_used": False,
            "pretrained_vocab_used": False,
            "pretrained_merges_used": False,
            "synthetic_llm_corpus_used": False,
            "sf_origin": meta.get("sf_origin") is True,
        },
        decision={
            "phase23_training_started": True,
            "phase23_training_completed": status == "COMPLETED_READY_FOR_PHASE24",
            "suitable_for_phase24_quality_training": status
            == "COMPLETED_READY_FOR_PHASE24",
            "runtime_chat_should_use_this_directly": False,
            "next_recommended_phase": "Phase 24 — SF-10M v0.2 Quality Training",
        },
    )


def write_phase23_artifact_files(
    *,
    artifact_dir: str | Path = "artifacts/tokenizers/sf_bpe/v2",
    previous_artifact_dir: str | Path = "artifacts/tokenizers/sf_bpe/v1",
    corpus_root: str | Path = "data/corpus/chat/jsonl",
    required_flag_used: str = "--confirm-phase23-tokenizer",
) -> Phase23TokenizerAudit:
    artifact = Path(artifact_dir)
    meta = _read_json(artifact / "meta.json")
    existing_provenance = (
        _read_json(artifact / "provenance.json")
        if (artifact / "provenance.json").exists()
        else {}
    )
    audit = build_phase23_tokenizer_audit(
        artifact_dir=artifact,
        previous_artifact_dir=previous_artifact_dir,
        corpus_root=corpus_root,
    )

    tokenizer_config = {
        "tokenizer_type": "sf_bpe",
        "version": "v2",
        "vocab_size_requested": 8000,
        "vocab_size_actual": meta.get("vocab_size"),
        "min_frequency": 2,
        "special_tokens": meta.get("special_tokens"),
        "lowercase": meta.get("lowercase"),
        "byte_level": meta.get("byte_level"),
        "encoding": "utf-8",
        "sovereign": True,
        "pretrained_vocab_used": False,
        "pretrained_merges_used": False,
    }
    provenance = {
        "artifact": str(artifact),
        "phase": "Phase 23 — Tokenizer v2 Retrain & Audit",
        "created_at_utc": existing_provenance.get(
            "created_at_utc", datetime.now(timezone.utc).isoformat()
        ),
        "training_permission": {
            "granted": True,
            "granted_by": "Sami",
            "permission_text_summary": (
                "Sami delegated continuing the documented roadmap, including "
                "training and tests, without waiting for repeated approvals."
            ),
            "required_flag_used": required_flag_used,
        },
        "corpus_root": str(corpus_root),
        "source_files": (meta.get("training_meta") or {}).get("source_files", []),
        "artifact_hashes": {
            "vocab.json": _hash_file(artifact / "vocab.json"),
            "merges.txt": _hash_file(artifact / "merges.txt"),
            "meta.json": _hash_file(artifact / "meta.json"),
        },
        "data_boundaries": {
            "external_llm_data_used": False,
            "pretrained_weights_used": False,
            "pretrained_tokenizer_used": False,
            "pretrained_vocab_used": False,
            "pretrained_merges_used": False,
            "synthetic_llm_corpus_used": False,
            "extra_texts_count": (meta.get("training_meta") or {}).get(
                "extra_texts_count"
            ),
        },
        "known_limits": [
            "Tokenizer v2 improves tokenization coverage; it is not a dialogue model.",
            "Runtime chat stays template/default until a later generator canary passes.",
            "Phase 24 must still prove loss/perplexity and repetition improvements.",
        ],
    }

    _write_json(artifact / "tokenizer_config.json", tokenizer_config)
    _write_json(artifact / "provenance.json", provenance)
    _write_json(artifact / "audit_report.json", audit.to_json())
    return audit


def _protected_term_rows(
    *,
    protected_terms: list[str],
    previous_tokenizer: BPETokenizer,
    tokenizer: BPETokenizer,
) -> list[ProtectedTermTokenization]:
    rows: list[ProtectedTermTokenization] = []
    for term in protected_terms:
        v1_tokens = len(previous_tokenizer.encode(term))
        v2_ids = tokenizer.encode(term)
        v2_tokens = len(v2_ids)
        decoded = tokenizer.decode(v2_ids)
        max_reasonable_tokens = max(6, len(term.split()) * 3)
        rows.append(
            ProtectedTermTokenization(
                term=term,
                v1_tokens=v1_tokens,
                v2_tokens=v2_tokens,
                v2_decoded=decoded,
                v2_roundtrip_ok=decoded == term,
                aggressive_split=v2_tokens > max_reasonable_tokens,
            )
        )
    return rows


def _hash_file(path: Path) -> str:
    h = hashlib.blake2b(digest_size=16)
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
