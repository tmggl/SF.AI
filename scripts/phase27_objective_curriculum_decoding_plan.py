#!/usr/bin/env python3
"""SF-native Objective/Curriculum/Decoding Acceleration Track.

This is a no-training planning gate. It re-anchors the active repair track at
Phase 27.79 and blocks training until objective, curriculum, decoding,
evaluation, logging, and hardware-smoke gates are encoded and pass.
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


DEFAULT_SOURCE = (
    ROOT
    / "artifacts/reports/phase27_104_bounded_topic_prototype_contrastive_repair_report.json"
)
DEFAULT_REPORT = ROOT / "artifacts/reports/PHASE27_OBJECTIVE_CURRICULUM_DECODING_PLAN.json"
DEFAULT_DOC = ROOT / "docs/PHASE27_OBJECTIVE_CURRICULUM_DECODING_PLAN.md"

REQUIRED_FAMILIES = ("open_social", "followup", "planning", "support", "topic")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Write the mandatory Phase 27.79 Objective/Curriculum/Decoding plan"
    )
    p.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    p.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    p.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    return p.parse_args()


def rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


def load_source(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"missing source report: {path}")
    report = json.loads(path.read_text(encoding="utf-8"))
    if report.get("phase") != "Phase 27.104":
        raise ValueError("this plan expects Phase 27.104 as the latest evidence source")
    if report.get("runtime_changed") is not False:
        raise ValueError("runtime must remain unchanged before this planning gate")
    return report


def build_report(source: dict[str, Any]) -> dict[str, Any]:
    root_cause = {
        "current_failure": (
            "Phase 27.104 fixed topic binding on the narrow prototype gate, but all-family "
            "quality regressed to 30/50. The model can follow the narrow topic objective, "
            "yet still loses stable dialogue-family behavior."
        ),
        "objective": {
            "is_problem": True,
            "weight_percent": 24,
            "evidence": "Previous objectives over-focus on topic copy/binding and do not teach family selection as a first-class behavior.",
        },
        "family_mixing": {
            "is_problem": True,
            "weight_percent": 22,
            "evidence": "All-family gate failed despite topic gates passing; family stability is not preserved.",
        },
        "curriculum_order": {
            "is_problem": True,
            "weight_percent": 18,
            "evidence": "Narrow scheduled views can improve one family while degrading broader dialogue behavior.",
        },
        "decoding": {
            "is_problem": True,
            "weight_percent": 14,
            "evidence": "Checkpoint judgment must use guarded decoding consistently before runtime decisions.",
        },
        "semantic_routing": {
            "is_problem": True,
            "weight_percent": 10,
            "evidence": "Fallback/general routing can hide family ambiguity and must be inspected in canaries.",
        },
        "capacity": {
            "is_problem": False,
            "weight_percent": 1,
            "evidence": "No evidence justifies SF-50M; errors track objective/curriculum/family behavior, not raw size.",
        },
        "other": {
            "is_problem": True,
            "weight_percent": 11,
            "evidence": "EOS, repetition, held-out separation, and runtime masking remain gate concerns.",
        },
    }
    objective = {
        "name": "family_conditioned_assistant_only_objective_v2",
        "training_format": [
            "النطاق: {msa|saudi}",
            "عائلة الحوار: {open_social|followup|planning|support|topic}",
            "المستخدم: {user_text}",
            "المساعد: {assistant_text} <eos>",
        ],
        "example": [
            "النطاق: سعودي",
            "عائلة الحوار: تنظيم",
            "المستخدم: كيف أنظم يومي؟",
            "المساعد: اكتب ثلاث مهام، وابدأ بالأهم لمدة قصيرة. <eos>",
        ],
        "context_lines_enter_model": True,
        "loss_scope": "assistant_text_and_eos_only",
        "loss_excludes": ["scope_line", "family_line", "user_line"],
        "eos_required": True,
        "no_long_family_blocks": True,
        "changes": [
            "Treat dialogue family as explicit conditioning text.",
            "Train answer boundaries with mandatory <eos>.",
            "Keep user/context visible as input while masking them out of target loss.",
            "Reject project/operator dialogue contamination.",
        ],
    }
    curriculum = {
        "name": "stratified_round_robin_family_curriculum_v2",
        "required_families": list(REQUIRED_FAMILIES),
        "ordering": "family -> dialect -> novelty round-robin",
        "window_balance_gate": {
            "window_size": 500,
            "max_family_share": 0.24,
            "min_family_share": 0.16,
            "fail_if_missing_any_family": True,
        },
        "rules": [
            "No long contiguous blocks from a single family.",
            "Every training window must cover all five required families.",
            "MSA/Saudi balance must stay close to 50/50.",
            "Held-out canaries must never enter training.",
            "Topic repair data must not drown open_social/followup/planning/support.",
        ],
    }
    decoding = {
        "name": "guarded_decoding_policy_v2",
        "must_apply_before_checkpoint_judgment": True,
        "controls": [
            "stop_at_eos",
            "no_repeat_ngram",
            "repetition_penalty",
            "known_fragment_blocklist",
            "topic_substitution_guard",
            "family_drift_guard",
            "template_masking_forbidden",
        ],
        "blocked_response_rule": "If guarded generation fails, return blocked metadata, not a fixed template.",
    }
    evaluation = {
        "name": "contrastive_checkpoint_evaluation_v2",
        "compare_against": "last_trusted_checkpoint_and_current_baseline",
        "required_suites": [
            "known_canary",
            "fresh_heldout_canary",
            "family_confusion_matrix",
            "topic_binding_canary",
            "open_social_canary",
            "followup_canary",
            "clean_stop_canary",
            "runtime_dry_run",
        ],
        "checkpoint_selector": [
            "held_out_dialogue_quality",
            "family_stability",
            "semantic_correctness",
            "clean_stop",
            "open_social_naturalness",
            "followup_continuity",
            "runtime_usability",
        ],
        "loss_only_is_never_enough": True,
    }
    acceleration = {
        "mps_amp_plan": {
            "check_mps_support": True,
            "amp_allowed_after_smoke_test_only": True,
            "disable_amp_if_unstable": True,
            "purpose": "reduce heat and speed training without changing behavioral goals",
        },
        "logging": {
            "local_only": True,
            "allowed_backends": ["csv", "tensorboard_local"],
            "required_metrics": [
                "train_loss",
                "eval_loss",
                "perplexity",
                "family_accuracy",
                "clean_stop_rate",
                "topic_binding_pass_rate",
                "canary_pass_rate",
                "blocked_reasons",
                "checkpoint_selected_or_rejected_reason",
            ],
        },
        "lora_gate": {
            "status": "deferred",
            "allowed_only_on_sf_native_models": True,
            "forbidden_on_external_models": True,
            "activate_after_base_run_success_only": True,
        },
        "preference_optimization_gate": {
            "status": "deferred",
            "methods": ["DPO", "ORPO", "SimPO"],
            "requires_local_sovereign_preference_pairs": True,
            "required_fields": [
                "chosen",
                "rejected",
                "source",
                "license",
                "training_allowed",
            ],
            "external_model_preferences_forbidden": True,
        },
    }
    gates = {
        "blocked_now": [
            "new_training",
            "tokenizer_retrain",
            "sf50m_transition",
            "runtime_release",
            "template_masking",
            "pretrained_or_open_weight_usage",
        ],
        "allow_bounded_training_only_if": [
            "objective_renderer_ready",
            "assistant_only_loss_mask_verified",
            "round_robin_sampler_ready",
            "decoding_policy_ready",
            "contrastive_eval_ready",
            "checkpoint_selector_ready",
            "heldout_canary_ready",
            "corpus_audit_passed",
            "sensitive_scan_passed",
            "all_tests_passed",
            "mps_amp_smoke_logged",
        ],
        "stop_criteria": [
            "family_balance_gate_failed",
            "heldout_leakage_detected",
            "operator_contamination_detected",
            "semantic_routing_regression",
            "clean_stop_regression",
            "topic_substitution_regression",
            "amp_instability_detected",
        ],
        "next_phase_if_plan_passes": "Phase 27.80 — Bounded SF-10M Family-Conditioned Repair Training",
        "runtime_release_requires": "RUNTIME_RELEASE_ALLOWED=true",
        "sf50m_requires": "SF-50M_JUSTIFIED_TRANSITION_GATE with capacity as the dominant proven cause",
    }
    decision = {
        "decision_id": "PHASE27_OBJECTIVE_CURRICULUM_DECODING_PLAN",
        "active_track": "SF-native Objective/Curriculum/Decoding Acceleration Track",
        "phase": "Phase 27.79 — Objective/Curriculum/Decoding Repair Plan",
        "engineering_decision": "PLAN_READY_TRAINING_BLOCKED_UNTIL_GATES_PASS",
        "new_training_allowed": False,
        "tokenizer_retrain_allowed": False,
        "sf50m_allowed": False,
        "runtime_release_allowed": False,
        "bounded_training_candidate": "Phase 27.80 — Bounded SF-10M Family-Conditioned Repair Training",
    }
    return {
        "report_id": "PHASE27_OBJECTIVE_CURRICULUM_DECODING_PLAN",
        "phase": "Phase 27.79",
        "phase_title": "Objective/Curriculum/Decoding Repair Plan",
        "active_track": "SF-native Objective/Curriculum/Decoding Acceleration Track",
        "strategy": "Sovereign Practical Acceleration Strategy v2",
        "sovereignty_mode": "SF-native only",
        "source_report": rel(DEFAULT_SOURCE),
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "training_started": False,
        "tokenizer_training_started": False,
        "runtime_changed": False,
        "root_cause": root_cause,
        "objective_plan": objective,
        "curriculum_plan": curriculum,
        "decoding_policy": decoding,
        "contrastive_evaluation": evaluation,
        "acceleration_tooling": acceleration,
        "gates": gates,
        "decision": decision,
        "artifacts": {"report": rel(DEFAULT_REPORT), "doc": rel(DEFAULT_DOC)},
    }


def write_doc(path: Path, report: dict[str, Any]) -> None:
    rc = report["root_cause"]
    lines = [
        "# PHASE27_OBJECTIVE_CURRICULUM_DECODING_PLAN",
        "",
        "## القرار",
        "",
        f"- المرحلة: `{report['phase']} — {report['phase_title']}`",
        f"- المسار: `{report['active_track']}`",
        f"- القاموس: `{report['lexicon_track']}`",
        "- تدريب جديد: `false`",
        "- tokenizer جديد: `false`",
        "- SF-50M: `false`",
        "- runtime release: `false`",
        "",
        "## المشكلة الجذرية الحالية",
        "",
        rc["current_failure"],
        "",
        "| العامل | هل هو مشكلة؟ | الوزن | الدليل |",
        "|---|---:|---:|---|",
    ]
    for key in (
        "objective",
        "family_mixing",
        "curriculum_order",
        "decoding",
        "semantic_routing",
        "capacity",
        "other",
    ):
        item = rc[key]
        lines.append(
            f"| `{key}` | `{item['is_problem']}` | `{item['weight_percent']}%` | {item['evidence']} |"
        )
    lines.extend(
        [
            "",
            "## Objective",
            "",
            f"- الاسم: `{report['objective_plan']['name']}`",
            f"- loss: `{report['objective_plan']['loss_scope']}`",
            "- الصيغة:",
            "",
            "```text",
            *report["objective_plan"]["example"],
            "```",
            "",
            "القواعد:",
        ]
    )
    for item in report["objective_plan"]["changes"]:
        lines.append(f"- {item}")
    lines.extend(["", "## Curriculum", ""])
    for item in report["curriculum_plan"]["rules"]:
        lines.append(f"- {item}")
    lines.extend(["", "## Decoding Policy", ""])
    for item in report["decoding_policy"]["controls"]:
        lines.append(f"- {item}")
    lines.extend(
        [
            f"- blocked rule: {report['decoding_policy']['blocked_response_rule']}",
            "",
            "## Contrastive Evaluation",
            "",
        ]
    )
    for item in report["contrastive_evaluation"]["required_suites"]:
        lines.append(f"- {item}")
    lines.extend(["", "## Checkpoint Selector", ""])
    for item in report["contrastive_evaluation"]["checkpoint_selector"]:
        lines.append(f"- {item}")
    lines.extend(["", "## AMP/MPS", ""])
    for key, value in report["acceleration_tooling"]["mps_amp_plan"].items():
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(["", "## Logging", ""])
    for item in report["acceleration_tooling"]["logging"]["required_metrics"]:
        lines.append(f"- {item}")
    lines.extend(["", "## Training Gate", ""])
    for item in report["gates"]["allow_bounded_training_only_if"]:
        lines.append(f"- {item}")
    lines.extend(["", "## Stop Criteria", ""])
    for item in report["gates"]["stop_criteria"]:
        lines.append(f"- {item}")
    lines.extend(
        [
            "",
            "## Deferred Tools",
            "",
            "- LoRA/QLoRA مؤجلة ومسموحة فقط على نماذج SF-native.",
            "- DPO/ORPO/SimPO مؤجلة حتى توجد preference pairs محلية وسيادية.",
            "",
            "## Next",
            "",
            f"- التالي عند نجاح البوابات: `{report['gates']['next_phase_if_plan_passes']}`",
            "- لا تفتح الواجهة إلا عند `RUNTIME_RELEASE_ALLOWED=true`.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    try:
        source = load_source(args.source)
    except (FileNotFoundError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    report = build_report(source)
    report["source_report"] = rel(args.source)
    report["artifacts"] = {"report": rel(args.report), "doc": rel(args.doc)}
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_doc(args.doc, report)
    print("SF.AI — PHASE27_OBJECTIVE_CURRICULUM_DECODING_PLAN")
    print(f"phase: {report['phase']} — {report['phase_title']}")
    print(f"training_allowed: {report['decision']['new_training_allowed']}")
    print(f"next: {report['gates']['next_phase_if_plan_passes']}")
    print(f"report: {rel(args.report)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
