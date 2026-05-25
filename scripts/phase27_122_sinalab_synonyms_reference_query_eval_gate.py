#!/usr/bin/env python3
"""Phase 27.122 — SinaLab Synonyms reference query/eval gate.

Reads the gitignored local reference layer, builds an in-memory lookup index,
and publishes metrics only. No raw terms, no query rows, no corpus/tokenizer
writes, no training, and no runtime activation.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RESOURCE_DIR = ROOT / "resources/external_sources"
REPORT_DIR = ROOT / "artifacts/reports"
DOCS_DIR = ROOT / "docs"

PHASE27_121_DECISION = (
    REPORT_DIR / "PHASE27_121_SINALAB_SYNONYMS_LOCAL_REFERENCE_LAYER_BUILD_DECISION.json"
)
PHASE27_121_MANIFEST = (
    RESOURCE_DIR / "phase27_121_sinalab_synonyms_local_reference_layer_build_manifest.json"
)
PHASE27_121_VALIDATION = (
    RESOURCE_DIR / "phase27_121_sinalab_synonyms_local_reference_layer_validation.json"
)

QUERY_METRICS = RESOURCE_DIR / "phase27_122_sinalab_synonyms_reference_query_eval_metrics.json"
QUERY_GATE = RESOURCE_DIR / "phase27_122_sinalab_synonyms_reference_query_eval_gate.json"
REPORT = REPORT_DIR / "phase27_122_sinalab_synonyms_reference_query_eval_gate_report.json"
DECISION = REPORT_DIR / "PHASE27_122_SINALAB_SYNONYMS_REFERENCE_QUERY_EVAL_GATE_DECISION.json"
DOC = DOCS_DIR / "PHASE27_122_SINALAB_SYNONYMS_REFERENCE_QUERY_EVAL_GATE_REPORT.md"


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def _band_counts(rows: list[dict[str, Any]]) -> dict[str, int]:
    counts = {"high": 0, "medium": 0, "low": 0}
    for row in rows:
        counts[str(row["quality_band"])] += 1
    return counts


def _local_paths(manifest: dict[str, Any]) -> tuple[Path, Path]:
    reference = ROOT / manifest["local_files"]["reference_records"]["relative_path"]
    eval_candidates = ROOT / manifest["local_files"]["eval_candidates"]["relative_path"]
    return reference, eval_candidates


def _query_metrics(manifest: dict[str, Any]) -> dict[str, Any]:
    reference_path, eval_path = _local_paths(manifest)
    reference_rows = _read_jsonl(reference_path)
    eval_rows = _read_jsonl(eval_path)

    index: dict[str, list[dict[str, Any]]] = {}
    for row in reference_rows:
        index.setdefault(str(row["candidate_normalized"]), []).append(row)

    duplicate_normalized_keys = sum(1 for rows in index.values() if len(rows) > 1)
    eval_queries = 0
    exact_hits = 0
    quality_match_hits = 0
    missing_lookup = 0
    for row in eval_rows:
        eval_queries += 1
        candidates = index.get(str(row["candidate_normalized"]), [])
        if not candidates:
            missing_lookup += 1
            continue
        exact_hits += 1
        if any(candidate["quality_band"] == row["quality_band"] for candidate in candidates):
            quality_match_hits += 1

    exact_rate = exact_hits / eval_queries if eval_queries else 0.0
    quality_rate = quality_match_hits / eval_queries if eval_queries else 0.0
    return {
        "phase": "Phase 27.122",
        "source_id": "sinalab_synonyms",
        "query_scope": "local_in_memory_query_eval_terms_not_committed",
        "reference_record_count": len(reference_rows),
        "eval_query_count": eval_queries,
        "unique_normalized_index_keys": len(index),
        "duplicate_normalized_index_keys": duplicate_normalized_keys,
        "exact_lookup_hits": exact_hits,
        "missing_lookup_count": missing_lookup,
        "exact_lookup_rate": round(exact_rate, 6),
        "quality_band_match_hits": quality_match_hits,
        "quality_band_match_rate": round(quality_rate, 6),
        "reference_quality_band_counts": _band_counts(reference_rows),
        "eval_quality_band_counts": _band_counts(eval_rows),
        "local_reference_files_gitignored": True,
        "raw_terms_published": False,
        "query_rows_published": False,
        "dialogue_corpus_written": False,
        "tokenizer_vocab_written": False,
        "training_started": False,
        "runtime_lookup_enabled": False,
    }


def _gate(
    *,
    decision121: dict[str, Any],
    validation121: dict[str, Any],
    manifest121: dict[str, Any],
    metrics: dict[str, Any],
) -> dict[str, Any]:
    preconditions = {
        "phase27_121_allows_query_eval_gate": decision121["engineering_decision"]
        == "ALLOW_PHASE27_122_SYNONYMS_REFERENCE_QUERY_AND_EVAL_GATE_NO_TRAINING",
        "phase27_121_validation_passed": validation121["passed"] is True,
        "manifest_counts_match_metrics": (
            manifest121["reference_record_count"] == metrics["reference_record_count"]
            and manifest121["eval_candidate_record_count"] == metrics["eval_query_count"]
        ),
        "index_has_expected_unique_keys": (
            metrics["unique_normalized_index_keys"] == metrics["reference_record_count"]
        ),
        "no_duplicate_normalized_keys": metrics["duplicate_normalized_index_keys"] == 0,
        "all_eval_queries_hit": metrics["exact_lookup_rate"] == 1.0,
        "quality_band_matches_all_eval_queries": metrics["quality_band_match_rate"] == 1.0,
        "raw_terms_not_published": metrics["raw_terms_published"] is False,
        "query_rows_not_published": metrics["query_rows_published"] is False,
        "no_corpus_write": metrics["dialogue_corpus_written"] is False,
        "no_tokenizer_write": metrics["tokenizer_vocab_written"] is False,
        "no_training": metrics["training_started"] is False,
        "no_runtime_lookup": metrics["runtime_lookup_enabled"] is False,
    }
    passed = all(preconditions.values())
    return {
        "phase": "Phase 27.122",
        "gate_id": "PHASE27_122_SINALAB_SYNONYMS_REFERENCE_QUERY_EVAL_GATE",
        "source_id": "sinalab_synonyms",
        "gate_passed": passed,
        "preconditions": preconditions,
        "query_eval_ready_for_adapter_design": passed,
        "local_reference_records_required": True,
        "committed_outputs_allowed_next": [
            "adapter_design_spec_without_terms",
            "query_policy_manifest_without_terms",
            "eval_manifest_counts_only",
        ],
        "blocked_outputs": [
            "raw terms in git",
            "query result rows in git",
            "data/corpus writes",
            "tokenizer vocab or merges",
            "training text import",
            "checkpoint writes",
            "runtime lookup activation",
            "SF-50M transition",
        ],
        "raw_terms_commit_allowed": False,
        "query_rows_commit_allowed": False,
        "dialogue_corpus_allowed": False,
        "tokenizer_vocab_allowed": False,
        "training_allowed": False,
        "runtime_release_allowed": False,
        "runtime_lookup_activation_allowed": False,
        "sf50m_transition_allowed": False,
    }


def _decision(gate: dict[str, Any]) -> dict[str, Any]:
    passed = gate["gate_passed"] is True
    return {
        "decision_id": "PHASE27_122_SINALAB_SYNONYMS_REFERENCE_QUERY_EVAL_GATE_DECISION",
        "engineering_decision": (
            "ALLOW_PHASE27_123_SYNONYMS_REFERENCE_ADAPTER_DESIGN_NO_RUNTIME"
            if passed
            else "BLOCK_PHASE27_123_REPAIR_REFERENCE_QUERY_EVAL_GATE"
        ),
        "query_eval_gate_passed": passed,
        "reference_adapter_design_allowed_next": passed,
        "raw_terms_commit_allowed": False,
        "query_rows_commit_allowed": False,
        "external_training_text_import_allowed": False,
        "external_tokenizer_vocab_import_allowed": False,
        "dialogue_corpus_allowed": False,
        "tokenizer_vocab_allowed": False,
        "new_training_allowed": False,
        "runtime_release_allowed": False,
        "runtime_lookup_activation_allowed": False,
        "sf50m_transition_allowed": False,
        "next_phase": (
            "Phase 27.123 — Synonyms Reference Adapter Design, no runtime"
            if passed
            else "Phase 27.122b — Reference Query/Eval Gate Repair"
        ),
    }


def _write_doc(report: dict[str, Any]) -> None:
    metrics = report["metrics"]
    decision = report["decision"]
    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(
        "\n".join(
            [
                "# Phase 27.122 — Synonyms Reference Query and Eval Gate",
                "",
                "## الخلاصة",
                "",
                "تم بناء query/eval index مؤقت في الذاكرة من reference layer المحلي.",
                "المرفوع يحتوي metrics/counts فقط ولا يحتوي raw terms أو query rows.",
                "",
                "## القرار",
                "",
                "```text",
                decision["decision_id"],
                decision["engineering_decision"],
                "```",
                "",
                "## Metrics",
                "",
                f"- reference records: `{metrics['reference_record_count']}`",
                f"- eval queries: `{metrics['eval_query_count']}`",
                f"- unique index keys: `{metrics['unique_normalized_index_keys']}`",
                f"- duplicate index keys: `{metrics['duplicate_normalized_index_keys']}`",
                f"- exact lookup rate: `{metrics['exact_lookup_rate']}`",
                f"- quality match rate: `{metrics['quality_band_match_rate']}`",
                "",
                "## الممنوع",
                "",
                "- raw terms in git.",
                "- query rows in git.",
                "- data/corpus writes.",
                "- tokenizer vocab/merges.",
                "- training.",
                "- runtime lookup activation.",
                "- SF-50M transition.",
                "",
                "## الملفات",
                "",
                f"- `{QUERY_METRICS.relative_to(ROOT)}`",
                f"- `{QUERY_GATE.relative_to(ROOT)}`",
                f"- `{REPORT.relative_to(ROOT)}`",
                f"- `{DECISION.relative_to(ROOT)}`",
                "",
                "## التالي",
                "",
                "```text",
                decision["next_phase"],
                "```",
                "",
            ]
        ),
        encoding="utf-8",
    )


def build_report() -> dict[str, Any]:
    decision121 = _read_json(PHASE27_121_DECISION)
    if not decision121["engineering_decision"].startswith("ALLOW_PHASE27_122"):
        raise RuntimeError("Phase 27.121 does not allow Phase 27.122")
    manifest121 = _read_json(PHASE27_121_MANIFEST)
    validation121 = _read_json(PHASE27_121_VALIDATION)
    metrics = _query_metrics(manifest121)
    gate = _gate(
        decision121=decision121,
        validation121=validation121,
        manifest121=manifest121,
        metrics=metrics,
    )
    decision = _decision(gate)
    report = {
        "phase": "Phase 27.122",
        "status": "PHASE27_122_SYNONYMS_REFERENCE_QUERY_EVAL_GATE_READY_NO_RUNTIME",
        "strategy": "Sovereign Practical Acceleration Strategy v2",
        "sovereignty_mode": "SF-native only",
        "language_track": ["msa", "saudi"],
        "dictionary_track": "Saudi Seed v1",
        "metrics": metrics,
        "gate": gate,
        "decision": decision,
        "training_started": False,
        "runtime_changed": False,
        "runtime_lookup_enabled": False,
        "query_rows_committed": False,
        "reference_records_committed": False,
        "corpus_changed": False,
        "tokenizer_changed": False,
        "raw_terms_published": False,
    }
    _write_json(QUERY_METRICS, metrics)
    _write_json(QUERY_GATE, gate)
    _write_json(REPORT, report)
    _write_json(DECISION, decision)
    _write_doc(report)
    return report


def main() -> int:
    report = build_report()
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return (
        0
        if report["status"] == "PHASE27_122_SYNONYMS_REFERENCE_QUERY_EVAL_GATE_READY_NO_RUNTIME"
        else 1
    )


if __name__ == "__main__":
    raise SystemExit(main())
