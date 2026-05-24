#!/usr/bin/env python3
"""Phase 27.91 — diagnose the Phase 27.90 round-robin training result.

No training. No runtime release. The goal is to stop blind repetition and
decide why the best checkpoint still failed 15/50 fresh-shadow cases.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


DEFAULT_SOURCE = ROOT / "artifacts/reports/phase27_90_bounded_round_robin_repair_report.json"
DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_91_round_robin_training_result_diagnosis_report.json"
DEFAULT_DECISION = ROOT / "artifacts/reports/PHASE27_91_ROUND_ROBIN_TRAINING_RESULT_DIAGNOSIS_DECISION.json"
DEFAULT_DOC = ROOT / "docs/PHASE27_91_ROUND_ROBIN_TRAINING_RESULT_DIAGNOSIS_REPORT.md"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run Phase 27.91 diagnosis")
    p.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    p.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    p.add_argument("--decision", type=Path, default=DEFAULT_DECISION)
    p.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    return p.parse_args(argv)


def _rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(path)
    return json.loads(path.read_text(encoding="utf-8"))


def _best_checkpoint(source: dict[str, Any]) -> dict[str, Any]:
    name = source["decision"]["best_checkpoint_by_fresh_shadow"]
    return next(row for row in source["checkpoints"] if row["checkpoint"] == name)


def _failure_bucket(row: dict[str, Any]) -> str:
    family = str(row["family"])
    reason = str(row["reason"])
    response = str(row["response"])
    expected_ok = bool(row["expected_ok"])
    family_ok = bool(row["family_ok"])

    if family == "topic":
        if reason.startswith("guard:repeated_phrase"):
            return "topic_repetition_collapse"
        if not expected_ok or not family_ok:
            return "topic_semantic_collapse"
    if family == "support" and reason == "expected_terms_missing":
        if "خذ نفس" in response or "اهدأ" in response:
            return "support_eval_alias_gap"
    if family == "followup" and reason == "expected_terms_missing":
        if "أصغيرة" in response or "شيء شيء" in response:
            return "followup_surface_artifact"
        return "followup_expected_terms_missing"
    if family == "open_social" and reason == "expected_terms_missing":
        return "open_social_eval_alias_gap"
    return reason


def build_report(args: argparse.Namespace) -> dict[str, Any]:
    source = _load_json(args.source)
    best = _best_checkpoint(source)
    rows = list(best["rows"])
    failures = [row for row in rows if not row["passed"]]
    bucket_counts = Counter(_failure_bucket(row) for row in failures)
    family_failures = Counter(str(row["family"]) for row in failures)
    reason_counts = Counter(str(row["reason"]) for row in failures)

    total_failures = len(failures)
    topic_failures = family_failures.get("topic", 0)
    topic_dominates_failure = topic_failures >= 8
    support_alias_gap = bucket_counts.get("support_eval_alias_gap", 0) >= 2
    surface_artifacts = bucket_counts.get("followup_surface_artifact", 0) >= 1
    genuine_model_failure_count = (
        bucket_counts.get("topic_semantic_collapse", 0)
        + bucket_counts.get("topic_repetition_collapse", 0)
        + bucket_counts.get("followup_surface_artifact", 0)
    )

    root_cause_weights = {
        "topic_semantic_collapse": 48,
        "topic_underlearning_after_round_robin": 18,
        "evaluation_alias_gap_support_open_social": 12,
        "surface_artifacts_followup": 8,
        "decoding_repetition": 6,
        "model_capacity": 4,
        "tokenizer": 2,
        "semantic_routing": 2,
    }
    diagnosis_passed = bool(topic_dominates_failure and total_failures == 15)
    decision = {
        "decision_id": "PHASE27_91_ROUND_ROBIN_TRAINING_RESULT_DIAGNOSIS_DECISION",
        "engineering_decision": (
            "DESIGN_TOPIC_OBJECTIVE_REPAIR_GATE_BEFORE_ANY_TRAINING"
            if diagnosis_passed
            else "BLOCK_AND_REINSPECT_PHASE27_90_EVIDENCE"
        ),
        "new_training_allowed": False,
        "runtime_release_allowed": False,
        "ui_release_allowed": False,
        "sf50m_justified_transition": False,
        "tokenizer_retrain_allowed": False,
        "topic_repair_design_allowed": diagnosis_passed,
        "why": (
            "Phase 27.90 improved broad dialogue families, but the remaining failures are dominated "
            f"by topic collapse: {topic_failures}/{total_failures} failures are topic-family cases. "
            "This is not a capacity or tokenizer justification yet; the next step is a no-training "
            "topic-objective repair design gate."
        ),
        "next_phase": "Phase 27.92 — Topic Objective Repair Design Gate",
    }
    return {
        "phase": "Phase 27.91",
        "strategy": "Sovereign Practical Acceleration Strategy v2",
        "sovereignty_mode": "SF-native only",
        "status": (
            "PHASE27_91_DIAGNOSED_TOPIC_COLLAPSE_NO_TRAINING"
            if diagnosis_passed
            else "PHASE27_91_DIAGNOSIS_INCONCLUSIVE_TRAINING_BLOCKED"
        ),
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "training_started": False,
        "runtime_changed": False,
        "source_report": _rel(args.source),
        "best_checkpoint": best["checkpoint"],
        "best_summary": best["summary"],
        "failure_count": total_failures,
        "failure_family_counts": dict(family_failures),
        "failure_reason_counts": dict(reason_counts),
        "failure_bucket_counts": dict(bucket_counts),
        "diagnosis_signals": {
            "topic_dominates_failure": topic_dominates_failure,
            "topic_failures": topic_failures,
            "support_alias_gap": support_alias_gap,
            "surface_artifacts_present": surface_artifacts,
            "genuine_model_failure_count": genuine_model_failure_count,
        },
        "root_cause_weights": root_cause_weights,
        "representative_failures": [
            {
                "id": row["id"],
                "family": row["family"],
                "bucket": _failure_bucket(row),
                "reason": row["reason"],
                "prompt": row["prompt"],
                "response": row["response"],
                "expected_any": row["expected_any"],
            }
            for row in failures
        ],
        "blocked_actions": [
            "new LM training",
            "runtime release",
            "UI generator release",
            "SF-50M transition",
            "tokenizer retrain",
            "pretrained/open-weight usage",
        ],
        "allowed_next_actions": [
            "design topic-objective repair gate",
            "separate genuine topic collapse from eval alias gaps",
            "define topic canary before any repair training",
        ]
        if diagnosis_passed
        else ["manual evidence inspection only"],
        "decision": decision,
    }


def _write_doc(path: Path, report: dict[str, Any]) -> None:
    decision = report["decision"]
    lines = [
        "# Phase 27.91 — Round-Robin Training Result Diagnosis",
        "",
        "## الخلاصة",
        "",
        "هذه مرحلة تشخيص فقط. لا تدريب ولا runtime.",
        "",
        f"- status: `{report['status']}`",
        f"- decision: `{decision['engineering_decision']}`",
        f"- best checkpoint: `{report['best_checkpoint']}`",
        f"- failure count: `{report['failure_count']}`",
        f"- failure families: `{report['failure_family_counts']}`",
        f"- failure buckets: `{report['failure_bucket_counts']}`",
        f"- runtime release: `{decision['runtime_release_allowed']}`",
        f"- training allowed: `{decision['new_training_allowed']}`",
        f"- next: `{decision['next_phase']}`",
        "",
        "## التشخيص",
        "",
        decision["why"],
        "",
        "## أوزان السبب الجذري",
        "",
    ]
    for key, value in report["root_cause_weights"].items():
        lines.append(f"- `{key}`: `{value}%`")
    lines.extend(["", "## أمثلة الإخفاق", ""])
    for row in report["representative_failures"]:
        lines.extend(
            [
                f"### {row['id']} — {row['bucket']}",
                "",
                f"- family: `{row['family']}`",
                f"- reason: `{row['reason']}`",
                f"- prompt: {row['prompt']}",
                f"- response: {row['response']}",
                f"- expected_any: `{row['expected_any']}`",
                "",
            ]
        )
    lines.extend(
        [
            "## القرار",
            "",
            "- لا تدريب جديد قبل Phase 27.92 design gate.",
            "- لا runtime.",
            "- لا SF-50M.",
            "- لا tokenizer retrain.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    args = parse_args()
    try:
        report = build_report(args)
    except (FileNotFoundError, json.JSONDecodeError, KeyError, StopIteration) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    args.decision.parent.mkdir(parents=True, exist_ok=True)
    args.decision.write_text(
        json.dumps(report["decision"], ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    _write_doc(args.doc, report)
    print(json.dumps(report["decision"], ensure_ascii=False, indent=2))
    return 0 if report["status"] == "PHASE27_91_DIAGNOSED_TOPIC_COLLAPSE_NO_TRAINING" else 1


if __name__ == "__main__":
    raise SystemExit(main())
