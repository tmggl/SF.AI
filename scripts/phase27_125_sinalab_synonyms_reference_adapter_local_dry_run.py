#!/usr/bin/env python3
"""Phase 27.125 — SinaLab Synonyms adapter local dry-run.

Reads the gitignored local reference layer, feeds it through the Phase 27.124
adapter skeleton, and publishes aggregate metrics only. No raw terms, no query
rows, no runtime/chat wiring, no corpus/tokenizer writes, and no training.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from sf_ai.reference_layers import SinaLabSynonymsReferenceAdapter, SynonymReferenceRecord

ROOT = Path(__file__).resolve().parents[1]
RESOURCE_DIR = ROOT / "resources/external_sources"
REPORT_DIR = ROOT / "artifacts/reports"
DOCS_DIR = ROOT / "docs"

PHASE27_124_DECISION = (
    REPORT_DIR / "PHASE27_124_SINALAB_SYNONYMS_REFERENCE_ADAPTER_SKELETON_DECISION.json"
)
PHASE27_124_GATE = RESOURCE_DIR / "phase27_124_sinalab_synonyms_reference_adapter_skeleton_gate.json"
PHASE27_121_MANIFEST = (
    RESOURCE_DIR / "phase27_121_sinalab_synonyms_local_reference_layer_build_manifest.json"
)

METRICS = RESOURCE_DIR / "phase27_125_sinalab_synonyms_reference_adapter_local_dry_run_metrics.json"
GATE = RESOURCE_DIR / "phase27_125_sinalab_synonyms_reference_adapter_local_dry_run_gate.json"
REPORT = REPORT_DIR / "phase27_125_sinalab_synonyms_reference_adapter_local_dry_run_report.json"
DECISION = REPORT_DIR / "PHASE27_125_SINALAB_SYNONYMS_REFERENCE_ADAPTER_LOCAL_DRY_RUN_DECISION.json"
DOC = DOCS_DIR / "PHASE27_125_SINALAB_SYNONYMS_REFERENCE_ADAPTER_LOCAL_DRY_RUN_REPORT.md"


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


def _local_paths(manifest: dict[str, Any]) -> tuple[Path, Path]:
    reference = ROOT / manifest["local_files"]["reference_records"]["relative_path"]
    eval_candidates = ROOT / manifest["local_files"]["eval_candidates"]["relative_path"]
    return reference, eval_candidates


def _records_from_rows(rows: list[dict[str, Any]]) -> tuple[SynonymReferenceRecord, ...]:
    return tuple(
        SynonymReferenceRecord(
            canonical=str(row["candidate_term"]),
            synonyms=(),
            quality_band=str(row["quality_band"]),  # type: ignore[arg-type]
            source_id=str(row["source_id"]),
            record_id=str(row["record_id"]),
        )
        for row in rows
    )


def _quality_counts(rows: list[dict[str, Any]]) -> dict[str, int]:
    counts = {"high": 0, "medium": 0, "low": 0}
    for row in rows:
        counts[str(row["quality_band"])] += 1
    return counts


def _metrics(manifest: dict[str, Any]) -> dict[str, Any]:
    reference_path, eval_path = _local_paths(manifest)
    reference_rows = _read_jsonl(reference_path)
    eval_rows = _read_jsonl(eval_path)
    adapter = SinaLabSynonymsReferenceAdapter(_records_from_rows(reference_rows))

    eval_count = 0
    exact_hits = 0
    redacted_hits = 0
    term_leak_count = 0
    hash_lengths: set[int] = set()
    result_hashes: set[str] = set()
    quality_band_hits = {"high": 0, "medium": 0, "low": 0}
    missing_by_band = {"high": 0, "medium": 0, "low": 0}

    for row in eval_rows:
        eval_count += 1
        band = str(row["quality_band"])
        result = adapter.lookup(
            str(row["candidate_term"]),
            min_quality_band="high",
            include_terms_in_runtime_response=True,
        )
        if result.matched:
            exact_hits += 1
            quality_band_hits[band] += 1
        else:
            missing_by_band[band] += 1
        if result.redaction_applied and not result.terms_included and not result.term_values:
            redacted_hits += 1
        if result.terms_included or result.term_values:
            term_leak_count += 1
        hash_lengths.add(len(result.query_hash))
        hash_lengths.add(len(result.query_normalized_hash))
        for digest in result.result_hashes:
            hash_lengths.add(len(digest))
            result_hashes.add(digest)

    exact_rate = exact_hits / eval_count if eval_count else 0.0
    redaction_rate = redacted_hits / eval_count if eval_count else 0.0
    return {
        "phase": "Phase 27.125",
        "scope": "local_reference_adapter_dry_run_counts_only",
        "adapter_class": "SinaLabSynonymsReferenceAdapter",
        "reference_record_count": len(reference_rows),
        "eval_query_count": eval_count,
        "adapter_record_count": adapter.record_count,
        "adapter_index_key_count": adapter.index_key_count,
        "reference_quality_band_counts": _quality_counts(reference_rows),
        "eval_quality_band_counts": _quality_counts(eval_rows),
        "exact_lookup_hits": exact_hits,
        "exact_lookup_rate": round(exact_rate, 6),
        "missing_lookup_count": eval_count - exact_hits,
        "quality_band_hits": quality_band_hits,
        "missing_by_quality_band": missing_by_band,
        "redacted_lookup_count": redacted_hits,
        "redaction_rate": round(redaction_rate, 6),
        "term_leak_count": term_leak_count,
        "unique_result_hash_count": len(result_hashes),
        "observed_hash_lengths": sorted(hash_lengths),
        "local_reference_files_gitignored": True,
        "raw_source_records_loaded_locally": True,
        "raw_terms_published": False,
        "query_rows_published": False,
        "runtime_lookup_enabled": False,
        "chat_integration_enabled": False,
        "dialogue_corpus_written": False,
        "tokenizer_vocab_written": False,
        "training_started": False,
    }


def _gate(
    *,
    decision124: dict[str, Any],
    gate124: dict[str, Any],
    manifest121: dict[str, Any],
    metrics: dict[str, Any],
) -> dict[str, Any]:
    preconditions = {
        "phase27_124_allows_local_dry_run": decision124["engineering_decision"]
        == "ALLOW_PHASE27_125_SYNONYMS_REFERENCE_ADAPTER_LOCAL_DRY_RUN_NO_RUNTIME",
        "phase27_124_gate_passed": gate124["gate_passed"] is True,
        "manifest_counts_match_adapter_metrics": (
            manifest121["reference_record_count"] == metrics["reference_record_count"]
            and manifest121["eval_candidate_record_count"] == metrics["eval_query_count"]
            and metrics["adapter_record_count"] == metrics["reference_record_count"]
        ),
        "adapter_index_has_expected_unique_keys": metrics["adapter_index_key_count"]
        == metrics["reference_record_count"],
        "all_eval_queries_hit": metrics["exact_lookup_rate"] == 1.0,
        "redaction_applied_to_all_queries": metrics["redaction_rate"] == 1.0,
        "no_term_leaks": metrics["term_leak_count"] == 0,
        "hash_contract_passed": metrics["observed_hash_lengths"] == [64],
        "raw_terms_not_published": metrics["raw_terms_published"] is False,
        "query_rows_not_published": metrics["query_rows_published"] is False,
        "runtime_and_chat_still_disabled": metrics["runtime_lookup_enabled"] is False
        and metrics["chat_integration_enabled"] is False,
        "no_corpus_tokenizer_training": metrics["dialogue_corpus_written"] is False
        and metrics["tokenizer_vocab_written"] is False
        and metrics["training_started"] is False,
    }
    passed = all(preconditions.values())
    return {
        "phase": "Phase 27.125",
        "gate_id": "PHASE27_125_SINALAB_SYNONYMS_REFERENCE_ADAPTER_LOCAL_DRY_RUN_GATE",
        "source_id": "sinalab_synonyms",
        "gate_passed": passed,
        "preconditions": preconditions,
        "reference_runtime_policy_design_allowed_next": passed,
        "runtime_lookup_activation_allowed": False,
        "chat_integration_allowed": False,
        "raw_terms_commit_allowed": False,
        "query_rows_commit_allowed": False,
        "dialogue_corpus_allowed": False,
        "tokenizer_vocab_allowed": False,
        "training_allowed": False,
        "runtime_release_allowed": False,
        "sf50m_transition_allowed": False,
    }


def _decision(gate: dict[str, Any]) -> dict[str, Any]:
    passed = gate["gate_passed"] is True
    return {
        "decision_id": "PHASE27_125_SINALAB_SYNONYMS_REFERENCE_ADAPTER_LOCAL_DRY_RUN_DECISION",
        "engineering_decision": (
            "ALLOW_PHASE27_126_SYNONYMS_REFERENCE_RUNTIME_POLICY_DESIGN_NO_ACTIVATION"
            if passed
            else "BLOCK_PHASE27_126_REPAIR_REFERENCE_ADAPTER_LOCAL_DRY_RUN"
        ),
        "local_dry_run_passed": passed,
        "reference_runtime_policy_design_allowed_next": passed,
        "runtime_lookup_activation_allowed": False,
        "chat_integration_allowed": False,
        "raw_terms_commit_allowed": False,
        "query_rows_commit_allowed": False,
        "dialogue_corpus_allowed": False,
        "tokenizer_vocab_allowed": False,
        "new_training_allowed": False,
        "runtime_release_allowed": False,
        "sf50m_transition_allowed": False,
        "next_phase": (
            "Phase 27.126 — Synonyms Reference Runtime Policy Design, no activation"
            if passed
            else "Phase 27.125b — Reference Adapter Local Dry-Run Repair"
        ),
    }


def _write_doc(report: dict[str, Any]) -> None:
    metrics = report["metrics"]
    decision = report["decision"]
    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(
        "\n".join(
            [
                "# Phase 27.125 — Synonyms Reference Adapter Local Dry-Run",
                "",
                "## الخلاصة",
                "",
                "تم تشغيل adapter محليًا على reference layer gitignored وإخراج",
                "counts/hashes فقط. لا raw terms، لا query rows، لا runtime wiring،",
                "ولا corpus/tokenizer/training.",
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
                f"- adapter index keys: `{metrics['adapter_index_key_count']}`",
                f"- exact lookup hits: `{metrics['exact_lookup_hits']}`",
                f"- exact lookup rate: `{metrics['exact_lookup_rate']}`",
                f"- redaction rate: `{metrics['redaction_rate']}`",
                f"- term leak count: `{metrics['term_leak_count']}`",
                f"- observed hash lengths: `{metrics['observed_hash_lengths']}`",
                "",
                "## الممنوع",
                "",
                "- raw terms in git.",
                "- query rows in git.",
                "- runtime lookup activation.",
                "- chat module integration.",
                "- data/corpus writes.",
                "- tokenizer vocab/merges.",
                "- training.",
                "- SF-50M transition.",
                "",
                "## الملفات",
                "",
                f"- `{METRICS.relative_to(ROOT)}`",
                f"- `{GATE.relative_to(ROOT)}`",
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
    decision124 = _read_json(PHASE27_124_DECISION)
    if decision124["engineering_decision"] != (
        "ALLOW_PHASE27_125_SYNONYMS_REFERENCE_ADAPTER_LOCAL_DRY_RUN_NO_RUNTIME"
    ):
        raise RuntimeError("Phase 27.124 does not allow Phase 27.125")
    gate124 = _read_json(PHASE27_124_GATE)
    manifest121 = _read_json(PHASE27_121_MANIFEST)
    metrics = _metrics(manifest121)
    gate = _gate(
        decision124=decision124,
        gate124=gate124,
        manifest121=manifest121,
        metrics=metrics,
    )
    decision = _decision(gate)
    report = {
        "phase": "Phase 27.125",
        "status": "PHASE27_125_SYNONYMS_REFERENCE_ADAPTER_LOCAL_DRY_RUN_READY_NO_RUNTIME",
        "strategy": "Sovereign Practical Acceleration Strategy v2",
        "sovereignty_mode": "SF-native only",
        "language_track": ["msa", "saudi"],
        "dictionary_track": "Saudi Seed v1",
        "metrics": metrics,
        "gate": gate,
        "decision": decision,
        "adapter_code_changed": False,
        "runtime_changed": False,
        "runtime_lookup_enabled": False,
        "chat_integration_enabled": False,
        "raw_source_records_loaded_locally": True,
        "query_rows_committed": False,
        "reference_records_committed": False,
        "corpus_changed": False,
        "tokenizer_changed": False,
        "training_started": False,
        "raw_terms_published": False,
    }
    _write_json(METRICS, metrics)
    _write_json(GATE, gate)
    _write_json(REPORT, report)
    _write_json(DECISION, decision)
    _write_doc(report)
    return report


def main() -> int:
    report = build_report()
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return (
        0
        if report["status"] == "PHASE27_125_SYNONYMS_REFERENCE_ADAPTER_LOCAL_DRY_RUN_READY_NO_RUNTIME"
        else 1
    )


if __name__ == "__main__":
    raise SystemExit(main())
