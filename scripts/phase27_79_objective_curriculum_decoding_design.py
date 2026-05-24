#!/usr/bin/env python3
"""Phase 27.79 — Objective/Curriculum/Decoding Repair Design.

This phase is intentionally no-training. It turns Phase 27.78's root-cause
decision into an executable engineering design for the next implementation
phase. The output is a decision report, not a checkpoint.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


DEFAULT_SOURCE = ROOT / "artifacts/reports/phase27_78_engineering_root_cause_gate_report.json"
DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_79_objective_curriculum_decoding_design_report.json"
DEFAULT_DECISION = ROOT / "artifacts/reports/PHASE27_79_REPAIR_DESIGN_DECISION.json"
DEFAULT_DOC = ROOT / "docs/PHASE27_79_OBJECTIVE_CURRICULUM_DECODING_REPAIR_DESIGN.md"


FAMILY_WEIGHTS = {
    "open_social": 1.0,
    "followup": 1.0,
    "planning": 1.0,
    "support": 1.0,
    "topic": 1.0,
}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run Phase 27.79 repair design gate")
    p.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
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
        raise FileNotFoundError(f"missing Phase 27.78 source report: {path}")
    source = json.loads(path.read_text(encoding="utf-8"))
    if source.get("phase") != "Phase 27.78":
        raise ValueError("Phase 27.79 expects Phase 27.78 source report")
    decision = source.get("decision", {})
    if decision.get("decision_id") != "PHASE27_78_ENGINEERING_DECISION":
        raise ValueError("missing PHASE27_78_ENGINEERING_DECISION")
    if decision.get("new_training_allowed") is not False:
        raise ValueError("Phase 27.79 requires training to be blocked by Phase 27.78")
    return source


def _objective_design() -> dict[str, Any]:
    return {
        "name": "family_conditioned_prompt_to_answer_objective_v1",
        "goal": "تعليم النموذج اختيار عائلة الرد الصحيحة قبل صياغة الرد، لا حفظ نصوص منفردة.",
        "format": [
            "<|dialogue_family:{family}|>",
            "<|dialect:{msa|saudi}|>",
            "<|intent:{intent}|>",
            "<|topic:{topic_or_none}|>",
            "<|user|>{prompt}<|assistant|>{answer}<eos>",
        ],
        "loss_scope": "assistant_answer_only_with_eos",
        "required_controls": [
            "single_answer_boundary",
            "explicit_family_condition",
            "explicit_dialect_condition",
            "topic_or_none_condition",
            "assistant_eos_required",
            "no_cross_sample_packing",
        ],
        "rejected_patterns": [
            "multi-answer continuation",
            "topic-definition answer for open_social prompt",
            "support answer for planning prompt",
            "project/operator wording",
            "template fallback in generator path",
        ],
    }


def _curriculum_design() -> dict[str, Any]:
    return {
        "name": "interleaved_family_curriculum_v2",
        "goal": "منع انجذاب النموذج لعائلة واحدة، خصوصًا topic/open_social.",
        "family_weights": FAMILY_WEIGHTS,
        "ordering": "round_robin_interleaved_by_family_then_dialect",
        "dialect_balance": {"msa": 0.5, "saudi": 0.5},
        "batch_rules": [
            "لا دفعات كتلية من family واحدة.",
            "كل نافذة تدريب صغيرة يجب أن تحتوي open_social/followup/planning/support/topic.",
            "كل عائلة يجب أن تحتوي صيغًا مباشرة وغير مباشرة.",
            "held-out prompts لا تدخل التدريب.",
        ],
        "minimum_pre_training_diagnostics": [
            "family distribution report",
            "dialect distribution report",
            "prompt novelty report",
            "operator-contamination scan",
            "family confusion dry-run matrix",
        ],
    }


def _decoding_design() -> dict[str, Any]:
    return {
        "name": "semantic_guarded_decoding_v1",
        "goal": "تقليل الخلط والتكرار دون تغطية ضعف المولد بقوالب.",
        "controls": [
            "stop_at_eos",
            "max_answer_tokens_by_family",
            "no_repeat_ngram",
            "repetition_penalty",
            "family_allowed_terms_floor",
            "family_blocked_terms_soft_guard",
            "malformed_fragment_guard",
        ],
        "not_allowed": [
            "template replacement",
            "keyword-triggered canned answer",
            "rewriting bad generation into good answer",
        ],
        "runtime_rule": (
            "إذا حُجب المولد في generator-only lab mode فالرد يبقى فارغًا مع metadata، "
            "ولا نضع قالبًا يخدع المستخدم."
        ),
    }


def _gate_design() -> dict[str, Any]:
    return {
        "name": "PHASE27_80_GATE_ENCODING_PLAN",
        "next_phase": "Phase 27.80 — Repair Gate Encoding and Dry-Run Validation",
        "training_allowed_in_next_phase": False,
        "runtime_release_allowed_in_next_phase": False,
        "sf50m_allowed_in_next_phase": False,
        "must_implement": [
            "objective spec validator",
            "curriculum family-balance dry-run",
            "decoding policy config validator",
            "held-out/shadow canary manifest validator",
            "family confusion matrix builder",
            "operator-contamination regression scan",
        ],
        "must_pass_before_any_training_after_next_phase": [
            "objective_format_valid",
            "family_balance_valid",
            "dialect_balance_valid",
            "heldout_separation_valid",
            "operator_contamination_zero",
            "decoding_policy_valid",
            "runtime_template_masking_absent",
        ],
    }


def _decision(source: dict[str, Any]) -> dict[str, Any]:
    phase27_78_decision = source["decision"]
    return {
        "decision_id": "PHASE27_79_REPAIR_DESIGN_DECISION",
        "engineering_decision": "DESIGN_READY_ENCODE_GATES_NEXT_NO_TRAINING",
        "source_decision": phase27_78_decision["decision_id"],
        "continue_sf10m": True,
        "new_training_allowed": False,
        "tokenizer_retrain_allowed": False,
        "runtime_release_allowed": False,
        "sf50m_justified_transition": False,
        "next_phase": "Phase 27.80 — Repair Gate Encoding and Dry-Run Validation",
        "why_no_training_yet": (
            "Phase 27.79 is a design gate. It defines the objective, curriculum, "
            "decoding, and evaluation gates that must be encoded before any new LM training."
        ),
        "why_sf50m_still_blocked": (
            "Capacity remains only 1% in Phase 27.78 root-cause weights; the next fix targets "
            "family mixing, objective, curriculum, weak generalization, semantic routing, and decoding."
        ),
        "root_cause_weights_percent": phase27_78_decision["root_cause_weights_percent"],
    }


def _write_doc(path: Path, report: dict[str, Any]) -> None:
    decision = report["decision"]
    lines = [
        "# Phase 27.79 — Objective/Curriculum/Decoding Repair Design",
        "",
        "## الخلاصة",
        "",
        "هذه مرحلة تصميم هندسي فقط. لم يبدأ تدريب جديد، ولم يتغير runtime،",
        "ولم يُفتح `SF-50M`.",
        "",
        f"- status: `{report['status']}`",
        f"- decision id: `{decision['decision_id']}`",
        f"- source decision: `{decision['source_decision']}`",
        f"- language track: `{', '.join(report['language_track'])}`",
        f"- lexicon: `{report['lexicon_track']}`",
        f"- next phase: `{decision['next_phase']}`",
        "",
        "## القرار",
        "",
        f"- continue SF-10M: `{decision['continue_sf10m']}`",
        f"- new training allowed: `{decision['new_training_allowed']}`",
        f"- tokenizer retrain allowed: `{decision['tokenizer_retrain_allowed']}`",
        f"- runtime release allowed: `{decision['runtime_release_allowed']}`",
        f"- SF-50M justified transition: `{decision['sf50m_justified_transition']}`",
        "",
        "## Objective Design",
        "",
        f"- name: `{report['objective_design']['name']}`",
        f"- loss scope: `{report['objective_design']['loss_scope']}`",
        "",
    ]
    for item in report["objective_design"]["required_controls"]:
        lines.append(f"- {item}")
    lines.extend(["", "## Curriculum Design", ""])
    for item in report["curriculum_design"]["batch_rules"]:
        lines.append(f"- {item}")
    lines.extend(["", "## Decoding Design", ""])
    for item in report["decoding_design"]["controls"]:
        lines.append(f"- {item}")
    lines.extend(["", "## Phase 27.80 Gate Encoding Plan", ""])
    for item in report["gate_design"]["must_implement"]:
        lines.append(f"- {item}")
    lines.extend(["", "## Blocked Actions", ""])
    for item in report["blocked_actions"]:
        lines.append(f"- {item}")
    lines.extend(
        [
            "",
            "## Regression Summary",
            "",
            "- Phase 27.78 أثبتت أن capacity ليست السبب الأكبر.",
            "- Phase 27.79 لا تحاول تحسين benchmark؛ هي تصمم الإصلاح قبل التنفيذ.",
            "- أي تدريب لاحق يحتاج Phase 27.80 gates مكتوبة وناجحة.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    try:
        source = _load_source(args.source)
    except (FileNotFoundError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    decision = _decision(source)
    report = {
        "phase": "Phase 27.79",
        "strategy": "Sovereign Practical Acceleration Strategy v2",
        "gate": "OBJECTIVE_CURRICULUM_DECODING_REPAIR_DESIGN",
        "status": "PHASE27_79_REPAIR_DESIGN_READY_NEXT_GATE_ENCODING_NO_TRAINING",
        "source_report": _rel(args.source),
        "training_started": False,
        "tokenizer_training_started": False,
        "runtime_changed": False,
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "objective_design": _objective_design(),
        "curriculum_design": _curriculum_design(),
        "decoding_design": _decoding_design(),
        "gate_design": _gate_design(),
        "allowed_actions": [
            "encode gates and validators",
            "dry-run curriculum diagnostics",
            "dry-run objective format validation",
            "dry-run decoding policy validation",
            "build canary manifests",
            "build family confusion diagnostics",
        ],
        "blocked_actions": [
            "new LM training",
            "tokenizer retraining",
            "SF-50M full training",
            "runtime release",
            "template masking",
            "external/pretrained data or weights",
        ],
        "decision": decision,
        "artifacts": {
            "report": _rel(args.report),
            "decision": _rel(args.decision),
            "doc": _rel(args.doc),
        },
    }

    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    args.decision.parent.mkdir(parents=True, exist_ok=True)
    args.decision.write_text(json.dumps(decision, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _write_doc(args.doc, report)

    print("SF.AI — Phase 27.79 objective/curriculum/decoding repair design")
    print(f"status: {report['status']}")
    print(f"decision: {decision['decision_id']}")
    print(f"new training allowed: {decision['new_training_allowed']}")
    print(f"next phase: {decision['next_phase']}")
    print(f"report: {_rel(args.report)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
