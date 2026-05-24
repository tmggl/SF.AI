#!/usr/bin/env python3
"""Phase 27.80 remediation — family-balance repair plan.

This is still a no-training step. It turns the failed Phase 27.80 gates into
concrete SF-native remediation artifacts: a family manifest, target quotas, and
a curriculum config that can be validated before any future LM training.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.phase27_80_repair_gate_validation import record_family  # noqa: E402


DEFAULT_SOURCE = ROOT / "artifacts/reports/phase27_80_repair_gate_validation_report.json"
DEFAULT_CORPUS = ROOT / "data/corpus/chat/jsonl"
DEFAULT_OUT_DIR = ROOT / "artifacts/reports/phase27_80_family_balance_remediation"
DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_80_family_balance_remediation_report.json"
DEFAULT_DECISION = ROOT / "artifacts/reports/PHASE27_80_FAMILY_BALANCE_REMEDIATION_DECISION.json"
DEFAULT_DOC = ROOT / "docs/PHASE27_80_FAMILY_BALANCE_REMEDIATION.md"

FAMILIES = ("open_social", "followup", "planning", "support", "topic")
OFFICIAL_MIN_PER_FAMILY = 500


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Build Phase 27.80 family-balance remediation plan")
    p.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    p.add_argument("--corpus", type=Path, default=DEFAULT_CORPUS)
    p.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    p.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    p.add_argument("--decision", type=Path, default=DEFAULT_DECISION)
    p.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    return p.parse_args()


def _rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


def _load_source(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"missing Phase 27.80 gate report: {path}")
    source = json.loads(path.read_text(encoding="utf-8"))
    if source.get("phase") != "Phase 27.80":
        raise ValueError("expected Phase 27.80 gate report")
    decision = source.get("decision", {})
    if decision.get("decision_id") != "PHASE27_80_REPAIR_GATE_VALIDATION_DECISION":
        raise ValueError("missing PHASE27_80_REPAIR_GATE_VALIDATION_DECISION")
    return source


def _messages_text(item: dict[str, Any], role: str | None = None) -> str:
    parts = []
    for message in item.get("messages", []):
        if role is None or message.get("role") == role:
            parts.append(str(message.get("content", "")))
    return " ".join(parts)


def _read_records(corpus: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for path in sorted(corpus.glob("*.jsonl")):
        for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            if not line.strip():
                continue
            item = json.loads(line)
            provenance = item.get("provenance", {})
            prompt_family = record_family(item, role="user")
            answer_family = record_family(item, role="assistant")
            records.append(
                {
                    "file": path.name,
                    "line": line_no,
                    "dialect": provenance.get("dialect", "unknown"),
                    "quality": provenance.get("quality", "unknown"),
                    "training_allowed": bool(provenance.get("training_allowed")),
                    "prompt_family": prompt_family,
                    "answer_family": answer_family,
                    "family_aligned": prompt_family == answer_family,
                }
            )
    return records


def _quota_plan(records: list[dict[str, Any]]) -> dict[str, Any]:
    by_family = Counter(r["prompt_family"] for r in records)
    by_family_dialect: dict[str, Counter[str]] = defaultdict(Counter)
    for record in records:
        by_family_dialect[record["prompt_family"]][record["dialect"]] += 1

    needed: dict[str, dict[str, int]] = {}
    for family in FAMILIES:
        current = by_family[family]
        msa_current = by_family_dialect[family]["msa"]
        saudi_current = by_family_dialect[family]["saudi"]
        target_each = OFFICIAL_MIN_PER_FAMILY // 2
        msa_needed = max(0, target_each - msa_current)
        saudi_needed = max(0, target_each - saudi_current)
        total_needed = max(0, OFFICIAL_MIN_PER_FAMILY - current, msa_needed + saudi_needed)
        needed[family] = {
            "total": total_needed,
            "msa": msa_needed,
            "saudi": saudi_needed,
        }

    train_view = {
        "mode": "balanced_family_curriculum_view",
        "families": list(FAMILIES),
        "min_records_per_family_before_training": OFFICIAL_MIN_PER_FAMILY,
        "dialect_target_per_family": {"msa": 250, "saudi": 250},
        "overrepresented_family_policy": "cap_per_epoch_then_rotate_remaining",
        "underrepresented_family_policy": "author_more_gold_records_before_training; no blind oversampling",
        "epoch_family_units_after_remediation": OFFICIAL_MIN_PER_FAMILY,
        "packing": "no_cross_sample_packing",
        "loss_scope": "assistant_answer_only_with_eos",
        "training_allowed_now": False,
    }
    return {
        "family_counts": {family: by_family[family] for family in FAMILIES},
        "family_dialect_counts": {
            family: dict(by_family_dialect[family]) for family in FAMILIES
        },
        "official_min_per_family": OFFICIAL_MIN_PER_FAMILY,
        "needed_records": needed,
        "total_needed": sum(item["total"] for item in needed.values()),
        "curriculum_config": train_view,
    }


def _confusion_summary(records: list[dict[str, Any]]) -> dict[str, Any]:
    matrix: dict[str, dict[str, int]] = {f: {g: 0 for g in FAMILIES} for f in FAMILIES}
    for record in records:
        matrix[record["prompt_family"]][record["answer_family"]] += 1
    total = len(records)
    diagonal = sum(matrix[f][f] for f in FAMILIES)
    return {
        "matrix": matrix,
        "diagonal_rate": round(diagonal / max(1, total), 4),
        "repair_rule": (
            "new records must carry explicit intended_family metadata in the future "
            "authoring plan before training conversion"
        ),
    }


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows),
        encoding="utf-8",
    )


def _write_doc(path: Path, report: dict[str, Any]) -> None:
    decision = report["decision"]
    quotas = report["quota_plan"]["needed_records"]
    lines = [
        "# Phase 27.80 — Family Balance Remediation",
        "",
        "## الخلاصة",
        "",
        "هذه ليست مرحلة تدريب. هذه مرحلة تحويل فشل gates إلى خطة إصلاح",
        "قابلة للتنفيذ داخل مسار SF-native فقط.",
        "",
        f"- decision: `{decision['engineering_decision']}`",
        f"- training allowed: `{decision['new_training_allowed']}`",
        f"- runtime allowed: `{decision['runtime_release_allowed']}`",
        f"- total records needed: `{report['quota_plan']['total_needed']}`",
        "",
        "## Current Family Counts",
        "",
    ]
    for family, count in report["quota_plan"]["family_counts"].items():
        lines.append(f"- `{family}`: `{count}`")
    lines.extend(["", "## Authoring Quotas Before Training", ""])
    for family, item in quotas.items():
        lines.append(
            f"- `{family}`: total=`{item['total']}`, msa=`{item['msa']}`, saudi=`{item['saudi']}`"
        )
    lines.extend(
        [
            "",
            "## قرار المرحلة",
            "",
            "لا تدريب حتى تُنشأ دفعة متوازنة، وتُعاد Phase 27.80 gates، وتنجح",
            "`curriculum_family_balance_dry_run` و`family_confusion_matrix_builder`.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_report(source: dict[str, Any], records: list[dict[str, Any]], out_dir: Path) -> dict[str, Any]:
    quota_plan = _quota_plan(records)
    confusion = _confusion_summary(records)
    manifest_path = out_dir / "family_manifest.jsonl"
    config_path = out_dir / "balanced_curriculum_config.json"
    authoring_plan_path = out_dir / "authoring_quota_plan.json"

    _write_jsonl(manifest_path, records)
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(
        json.dumps(quota_plan["curriculum_config"], ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    authoring_plan_path.write_text(
        json.dumps(quota_plan["needed_records"], ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    remediation_ready = quota_plan["total_needed"] > 0
    decision = {
        "decision_id": "PHASE27_80_FAMILY_BALANCE_REMEDIATION_DECISION",
        "engineering_decision": (
            "REMEDIATION_PLAN_READY_AUTHOR_BALANCED_FAMILY_PACK_NO_TRAINING"
            if remediation_ready
            else "NO_REMEDIATION_NEEDED_RERUN_GATES"
        ),
        "new_training_allowed": False,
        "tokenizer_retrain_allowed": False,
        "runtime_release_allowed": False,
        "sf50m_justified_transition": False,
        "next_phase": "Phase 27.81 — Balanced Family Pack Authoring, no training",
        "required_before_training": [
            "author missing family records",
            "rebuild dialogue split",
            "rerun phase27-repair-gate-validation",
            "pass family balance and family confusion gates",
        ],
    }
    return {
        "phase": "Phase 27.80 remediation",
        "strategy": "Sovereign Practical Acceleration Strategy v2",
        "sovereignty_mode": "SF-native only",
        "source_report": _rel(DEFAULT_SOURCE),
        "training_started": False,
        "tokenizer_training_started": False,
        "runtime_changed": False,
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "status": "PHASE27_80_FAMILY_BALANCE_REMEDIATION_READY_NO_TRAINING",
        "failed_gate_context": {
            "all_gates_passed": source.get("decision", {}).get("all_gates_passed"),
            "blocked_training": source.get("decision", {}).get("new_training_allowed") is False,
        },
        "quota_plan": quota_plan,
        "confusion_summary": confusion,
        "artifacts": {
            "family_manifest": _rel(manifest_path),
            "balanced_curriculum_config": _rel(config_path),
            "authoring_quota_plan": _rel(authoring_plan_path),
        },
        "decision": decision,
    }


def main() -> int:
    args = parse_args()
    try:
        source = _load_source(args.source)
        records = _read_records(args.corpus)
        if not records:
            raise ValueError("empty corpus")
        report = build_report(source, records, args.out_dir)
    except (FileNotFoundError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.decision.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    args.decision.write_text(
        json.dumps(report["decision"], ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    _write_doc(args.doc, report)

    print("SF.AI — Phase 27.80 family-balance remediation")
    print(f"status: {report['status']}")
    print(f"total_needed: {report['quota_plan']['total_needed']}")
    print(f"report: {_rel(args.report)}")
    print(f"decision: {_rel(args.decision)}")
    print(f"doc: {_rel(args.doc)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
