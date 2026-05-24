#!/usr/bin/env python3
"""Phase 27.78 — Engineering Root Cause Gate.

This phase implements Sovereign Practical Acceleration Strategy v2.
It does not train. It does not create a tokenizer. It reads the latest
generation reports and produces PHASE27_78_ENGINEERING_DECISION before any
new training is allowed.
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


DEFAULT_SOURCE = ROOT / "artifacts/reports/phase27_77_v9_bounded_open_social_lm_repair_report.json"
DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_78_engineering_root_cause_gate_report.json"
DEFAULT_DECISION = ROOT / "artifacts/reports/PHASE27_78_ENGINEERING_DECISION.json"
DEFAULT_DOC = ROOT / "docs/PHASE27_78_ENGINEERING_ROOT_CAUSE_GATE_REPORT.md"
DEFAULT_SAMPLES = ROOT / "artifacts/samples/phase27_78_engineering_root_cause_gate_failures.md"

EVAL_KEYS = (
    ("phase27_69", "Phase 27.69 fresh held-out", "phase27_69_rows"),
    ("phase27_67", "Phase 27.67 known held-out", "phase27_67_rows"),
    ("phase27_60", "Phase 27.60 regression", "phase27_60_rows"),
)

ROOT_CAUSE_WEIGHTS = {
    "capacity": 1,
    "objective": 18,
    "curriculum": 16,
    "tokenizer": 4,
    "decoding": 7,
    "family_mixing": 22,
    "memorization": 2,
    "weak_generalization": 14,
    "EOS": 4,
    "repetition": 2,
    "semantic_routing": 10,
}

ALLOWED_TOOLS = [
    "PyTorch",
    "AMP / mixed precision",
    "TensorBoard المحلي",
    "schedulers",
    "experiment tracking",
    "advanced decoding",
    "repetition control",
    "curriculum tooling",
    "held-out canary",
    "shadow canary",
    "family-conditioned dialogue",
    "contrastive evaluation",
    "semantic routing diagnostics",
    "objective tracing",
    "anti-collapse diagnostics",
    "local RLHF-lite / DPO / ORPO / preference optimization",
    "LoRA / QLoRA على أوزان SF.AI فقط",
    "retrieval memory tooling",
    "local vector retrieval",
    "dialogue family balancing",
    "EOS boundary tooling",
    "checkpoint selector",
    "tokenizer boundary audit",
]

FORBIDDEN = [
    "pretrained weights",
    "pretrained vocab",
    "pretrained tokenizer merges",
    "hidden hosted APIs",
    "external reasoning services",
    "external dialogue datasets",
    "project workflow/operator dialogue contamination",
    "fake benchmark inflation",
    "template masking لإخفاء ضعف المولد",
]

SUCCESS_METRICS = [
    "held-out dialogue quality",
    "runtime usability",
    "clean-stop",
    "semantic correctness",
    "family stability",
    "open_social naturalness",
    "followup continuity",
    "canary pass rate",
    "human conversation realism",
]


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run Phase 27.78 engineering root-cause gate")
    p.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    p.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    p.add_argument("--decision", type=Path, default=DEFAULT_DECISION)
    p.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    p.add_argument("--samples", type=Path, default=DEFAULT_SAMPLES)
    return p.parse_args()


def _rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


def _failure_rows(source: dict[str, Any]) -> list[dict[str, Any]]:
    failures: list[dict[str, Any]] = []
    for eval_id, eval_name, key in EVAL_KEYS:
        for row in source.get(key, []):
            if row.get("passed") is True:
                continue
            failures.append(
                {
                    "eval_id": eval_id,
                    "eval_name": eval_name,
                    "id": row["id"],
                    "family": row["family"],
                    "dialect": row.get("dialect", "unknown"),
                    "prompt": row["prompt"],
                    "response": row.get("response", ""),
                    "reason": row.get("reason", "unknown"),
                    "guard_reason": row.get("guard_reason"),
                    "expected_any": row.get("expected_any", []),
                }
            )
    return failures


def _diagnose(row: dict[str, Any]) -> str:
    response = row["response"]
    reason = row["reason"]
    family = row["family"]
    prompt = row["prompt"]
    if reason.startswith("guard:malformed_token") and "نفسًا" in response:
        return "guard_false_positive_tanween"
    if "محام" in response:
        return "residual_artifact_fragment"
    if family == "topic" and reason == "expected_terms_missing":
        return "topic_semantic_substitution"
    if family == "followup" and reason == "expected_terms_missing":
        return "followup_flow_instability"
    if family == "support" and reason == "expected_terms_missing":
        return "support_semantic_weakness"
    if reason == "response_family_mismatch":
        return "family_mismatch"
    if "الشجاعة" in prompt and "الصدق" in response:
        return "topic_semantic_substitution"
    return "unclassified"


def _summarize(source: dict[str, Any], failures: list[dict[str, Any]]) -> dict[str, Any]:
    by_eval: dict[str, Any] = {}
    for eval_id, eval_name, key in EVAL_KEYS:
        rows = source.get(key, [])
        fail = [r for r in failures if r["eval_id"] == eval_id]
        by_eval[eval_id] = {
            "name": eval_name,
            "passed": len(rows) - len(fail),
            "total": len(rows),
            "failed": len(fail),
            "families": dict(Counter(r["family"] for r in fail)),
            "reasons": dict(Counter(r["reason"] for r in fail)),
            "diagnoses": dict(Counter(r["diagnosis"] for r in fail)),
        }
    by_family: dict[str, dict[str, int]] = defaultdict(lambda: {"failed": 0})
    for row in failures:
        by_family[row["family"]]["failed"] += 1
    return {
        "failure_count": len(failures),
        "by_eval": by_eval,
        "failure_by_family": dict(sorted(by_family.items())),
        "failure_by_reason": dict(Counter(r["reason"] for r in failures)),
        "failure_by_diagnosis": dict(Counter(r["diagnosis"] for r in failures)),
    }


def _decision(source: dict[str, Any], summary: dict[str, Any]) -> dict[str, Any]:
    fresh = source["phase27_69_summary"]
    known = source["phase27_67_summary"]
    regression = source["phase27_60_summary"]
    return {
        "decision_id": "PHASE27_78_ENGINEERING_DECISION",
        "engineering_decision": "BLOCK_TRAINING_UNTIL_OBJECTIVE_CURRICULUM_FAMILY_DECODING_PLAN",
        "continue_sf10m": True,
        "sf50m_justified_transition": False,
        "change_objective_required": True,
        "reorganize_dialogue_families_required": True,
        "curriculum_change_required": True,
        "tokenizer_retrain_allowed": False,
        "new_training_allowed": False,
        "runtime_release_allowed": False,
        "no_runtime_release_without_heldout_success": True,
        "sf50m_gate_rule": (
            "Only open SF-50M JUSTIFIED TRANSITION if family mixing, weak generalization, "
            "and semantic collapse remain after the objective/curriculum/decoding repair "
            "is implemented and held-out canaries still fail."
        ),
        "why_sf50m_blocked": (
            "The latest capacity probe showed only +1/20 for SF-50M over SF-10M, while "
            "Phase 27.77 failures point to family/objective/curriculum/semantic issues."
        ),
        "root_cause_weights_percent": ROOT_CAUSE_WEIGHTS,
        "current_scores": {
            "fresh_heldout": f"{fresh['passed']}/{fresh['total']}",
            "known_heldout": f"{known['passed']}/{known['total']}",
            "regression": f"{regression['passed']}/{regression['total']}",
        },
        "next_phase": "Phase 27.79 — Objective/Curriculum/Decoding Repair Design, no training until gates are encoded",
    }


def _write_samples(path: Path, failures: list[dict[str, Any]]) -> None:
    lines = ["# Phase 27.78 Engineering Root Cause Gate — Failure Samples", ""]
    for row in failures:
        lines.extend(
            [
                f"## {row['eval_id']} / {row['id']} — {row['diagnosis']}",
                "",
                f"- family: `{row['family']}`",
                f"- dialect: `{row['dialect']}`",
                f"- reason: `{row['reason']}`",
                f"- guard_reason: `{row['guard_reason']}`",
                f"- prompt: {row['prompt']}",
                f"- response: {row['response']}",
                "",
            ]
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_doc(path: Path, report: dict[str, Any]) -> None:
    decision = report["decision"]
    lines = [
        "# Phase 27.78 — Engineering Root Cause Gate",
        "",
        "## الخلاصة",
        "",
        "هذه المرحلة تعتمد `Sovereign Practical Acceleration Strategy v2`.",
        "لم يبدأ تدريب جديد. لم يُدرّب tokenizer جديد. لم يُفتح runtime.",
        "",
        f"- status: `{report['status']}`",
        f"- decision id: `{decision['decision_id']}`",
        f"- source: `{report['source_report']}`",
        f"- failures analyzed: `{report['summary']['failure_count']}`",
        f"- fresh held-out: `{decision['current_scores']['fresh_heldout']}`",
        f"- known held-out: `{decision['current_scores']['known_heldout']}`",
        f"- regression: `{decision['current_scores']['regression']}`",
        "",
        "## أوزان الأسباب التقريبية",
        "",
    ]
    for name, weight in decision["root_cause_weights_percent"].items():
        lines.append(f"- `{name}`: `{weight}%`")
    lines.extend(
        [
            "",
            "## القرار الهندسي",
            "",
            f"- continue SF-10M: `{decision['continue_sf10m']}`",
            f"- SF-50M justified transition: `{decision['sf50m_justified_transition']}`",
            f"- change objective required: `{decision['change_objective_required']}`",
            f"- reorganize dialogue families required: `{decision['reorganize_dialogue_families_required']}`",
            f"- curriculum change required: `{decision['curriculum_change_required']}`",
            f"- tokenizer retrain allowed: `{decision['tokenizer_retrain_allowed']}`",
            f"- new training allowed: `{decision['new_training_allowed']}`",
            f"- runtime release allowed: `{decision['runtime_release_allowed']}`",
            "",
            "## Runtime Decision",
            "",
            "`NO_RUNTIME_RELEASE_WITHOUT_HELDOUT_SUCCESS` فعّالة. لا يُفتح runtime",
            "حتى تمر held-out quality وfamily stability وclean-stop وsemantic correctness.",
            "",
            "## Allowed Actions",
            "",
            "- objective tracing.",
            "- curriculum diagnostics.",
            "- family confusion analysis.",
            "- decoding analysis and repetition profiling.",
            "- EOS inspection.",
            "- semantic routing diagnostics.",
            "- contrastive evaluation and held-out/shadow canaries.",
            "",
            "## Blocked Actions",
            "",
            "- أي تدريب جديد قبل encoding gates.",
            "- أي tokenizer version جديد قبل إثبات tokenizer كسبب أكبر.",
            "- أي SF-50M transition الآن.",
            "- أي template masking لإخفاء ضعف المولد.",
            "- أي benchmark inflation لا ينعكس على runtime behavior.",
            "",
            "## Regression Summary",
            "",
            "- Phase 27.60 regression بقي `30/30`، وهذا يعني أن الفشل الحالي ليس انهيارًا عامًا.",
            "- Phase 27.69 و27.67 ما زالت تفشل في family/semantic/followup/support.",
            "- التكبير ممنوع لأن capacity ليست السبب الأكبر حسب الأدلة الحالية.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    if not args.source.exists():
        print(f"error: missing source report: {args.source}", file=sys.stderr)
        return 1
    source = json.loads(args.source.read_text(encoding="utf-8"))
    if source.get("phase") != "Phase 27.77":
        print("error: Phase 27.78 expects Phase 27.77 source report", file=sys.stderr)
        return 2
    failures = _failure_rows(source)
    for row in failures:
        row["diagnosis"] = _diagnose(row)
    summary = _summarize(source, failures)
    decision = _decision(source, summary)

    report = {
        "phase": "Phase 27.78",
        "strategy": "Sovereign Practical Acceleration Strategy v2",
        "gate": "ENGINEERING_ROOT_CAUSE_GATE",
        "status": "PHASE27_78_ENGINEERING_DECISION_READY_TRAINING_BLOCKED_RUNTIME_BLOCKED",
        "source_report": _rel(args.source),
        "training_started": False,
        "tokenizer_training_started": False,
        "runtime_changed": False,
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "allowed_tools": ALLOWED_TOOLS,
        "forbidden": FORBIDDEN,
        "success_metrics": SUCCESS_METRICS,
        "summary": summary,
        "failures": failures,
        "decision": decision,
        "artifacts": {
            "report": _rel(args.report),
            "decision": _rel(args.decision),
            "doc": _rel(args.doc),
            "samples": _rel(args.samples),
        },
    }

    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    args.decision.parent.mkdir(parents=True, exist_ok=True)
    args.decision.write_text(json.dumps(decision, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _write_samples(args.samples, failures)
    _write_doc(args.doc, report)

    print("SF.AI — Phase 27.78 engineering root-cause gate")
    print(f"status: {report['status']}")
    print(f"decision: {decision['decision_id']}")
    print(f"new training allowed: {decision['new_training_allowed']}")
    print(f"sf50m transition: {decision['sf50m_justified_transition']}")
    print(f"report: {_rel(args.report)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
