#!/usr/bin/env python3
"""Phase 27.92 — Topic Objective Repair Design Gate.

No training. No runtime release. This phase turns the Phase 27.91 diagnosis
into an implementation-ready design for a topic-specific objective repair.
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


DEFAULT_SOURCE = ROOT / "artifacts/reports/phase27_91_round_robin_training_result_diagnosis_report.json"
DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_92_topic_objective_repair_design_gate_report.json"
DEFAULT_DECISION = ROOT / "artifacts/reports/PHASE27_92_TOPIC_OBJECTIVE_REPAIR_DESIGN_DECISION.json"
DEFAULT_SPEC = ROOT / "artifacts/reports/phase27_92_topic_objective_repair_spec.json"
DEFAULT_DOC = ROOT / "docs/PHASE27_92_TOPIC_OBJECTIVE_REPAIR_DESIGN_GATE_REPORT.md"


TOPIC_TERMS = (
    "الوفاء",
    "التعاون",
    "الصبر",
    "الاحترام",
    "الهدوء",
    "الصدق",
    "الصداقة",
    "الشجاعة",
)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run Phase 27.92 topic objective repair design gate")
    p.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    p.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    p.add_argument("--decision", type=Path, default=DEFAULT_DECISION)
    p.add_argument("--spec", type=Path, default=DEFAULT_SPEC)
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


def _topic_objective_spec() -> dict[str, Any]:
    return {
        "spec_id": "PHASE27_92_TOPIC_OBJECTIVE_REPAIR_SPEC",
        "version": "v1",
        "language_track": ["msa", "saudi"],
        "target_family": "topic",
        "target_terms": list(TOPIC_TERMS),
        "problem_statement": (
            "After Phase 27.90, general families improved, but topic prompts collapsed "
            "into unrelated definitions such as الهدوء or malformed fragments."
        ),
        "objective_name": "topic_anchor_prompt_to_answer_objective_v1",
        "conditioning_lines": [
            "النطاق: <فصحى|سعودي>",
            "عائلة الحوار: موضوع",
            "الموضوع المطلوب: <topic_term>",
        ],
        "topic_anchor_rule": (
            "For topic-family samples, the assistant answer must include the requested "
            "topic term exactly once within the first sentence."
        ),
        "assistant_loss_rule": (
            "Conditioning lines and user text remain masked under loss_scope=assistant; "
            "assistant content plus EOS remain supervised."
        ),
        "answer_contract": [
            "one short explanatory sentence",
            "include the requested topic term",
            "do not substitute another known topic term",
            "avoid malformed fragments",
            "avoid repeated words/phrases",
            "no project/operator language",
        ],
        "negative_controls": [
            "Prompt asks about الوفاء but answer starts with معنى الهدوء",
            "Prompt asks about التعاون but answer answers الصداقة",
            "Prompt asks about الشجاعة but answer repeats شي شي شي",
            "Prompt asks about الصدق but answer omits الصدق",
        ],
        "data_design_for_next_phase": {
            "no_external_data": True,
            "authoring_mode": "owner-delegated SF.AI authored only",
            "records_per_topic_min": 20,
            "dialect_balance_per_topic": {"msa": 10, "saudi": 10},
            "prompt_variants_per_topic": [
                "definition",
                "benefit",
                "when_it_appears",
                "daily_example",
                "short_explanation",
            ],
            "anti_collapse_pairs": (
                "Each topic appears beside contrastive prompts for other topic terms so the "
                "model learns the requested anchor, not a dominant memorized topic."
            ),
        },
        "decoding_design": {
            "max_new_tokens": 22,
            "no_repeat_ngram_size": 3,
            "repetition_penalty_min": 1.12,
            "stop_at_eos": True,
            "topic_term_required_in_guard": True,
            "blocked_if_other_topic_term_without_requested_term": True,
        },
        "canary_design": {
            "known_topic_canary_min": "18/20",
            "fresh_topic_shadow_min": "16/20",
            "all_family_regression_min": "45/50",
            "topic_family_min": "8/10",
            "malformed_max": 0,
            "repeated_phrase_max": 0,
        },
        "non_topic_cleanup": {
            "support_eval_alias_gap": (
                "Update evaluation aliases for valid Saudi support wording like خذ نفس واهدأ; "
                "do not train just to satisfy one wording."
            ),
            "open_social_eval_alias_gap": "Update aliases if the response is natural but misses exact expected terms.",
            "followup_surface_artifacts": "Track as guard/artifact issue in next diagnosis; do not mix with topic repair.",
        },
        "blocked": [
            "training before Phase 27.93 gate encoding",
            "runtime release",
            "SF-50M transition",
            "tokenizer retrain",
            "pretrained/open-weight usage",
        ],
    }


def build_report(args: argparse.Namespace) -> tuple[dict[str, Any], dict[str, Any]]:
    source = _load_json(args.source)
    spec = _topic_objective_spec()
    source_decision = source["decision"]["engineering_decision"]
    topic_dominates = source["diagnosis_signals"]["topic_dominates_failure"] is True
    topic_collapse_weight = int(source["root_cause_weights"]["topic_semantic_collapse"])
    capacity_weight = int(source["root_cause_weights"]["model_capacity"])
    design_ready = (
        source_decision == "DESIGN_TOPIC_OBJECTIVE_REPAIR_GATE_BEFORE_ANY_TRAINING"
        and topic_dominates
        and topic_collapse_weight >= 40
        and capacity_weight <= 5
        and len(spec["target_terms"]) >= 8
    )
    decision = {
        "decision_id": "PHASE27_92_TOPIC_OBJECTIVE_REPAIR_DESIGN_DECISION",
        "engineering_decision": (
            "ALLOW_PHASE27_93_TOPIC_OBJECTIVE_GATE_ENCODING_NO_TRAINING"
            if design_ready
            else "BLOCK_PHASE27_93_FIX_TOPIC_DESIGN"
        ),
        "new_training_allowed": False,
        "topic_gate_encoding_allowed": design_ready,
        "runtime_release_allowed": False,
        "ui_release_allowed": False,
        "sf50m_justified_transition": False,
        "tokenizer_retrain_allowed": False,
        "why": (
            "The next fix should target topic anchoring and anti-collapse objective design. "
            "Capacity remains a minor factor, so SF-50M is still blocked."
        ),
        "next_phase": "Phase 27.93 — Topic Objective Gate Encoding and Dry-Run Validation",
    }
    report = {
        "phase": "Phase 27.92",
        "strategy": "Sovereign Practical Acceleration Strategy v2",
        "sovereignty_mode": "SF-native only",
        "status": (
            "PHASE27_92_TOPIC_OBJECTIVE_REPAIR_DESIGN_READY_NO_TRAINING"
            if design_ready
            else "PHASE27_92_TOPIC_OBJECTIVE_REPAIR_DESIGN_BLOCKED"
        ),
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "training_started": False,
        "runtime_changed": False,
        "source_report": _rel(args.source),
        "source_failure_bucket_counts": source["failure_bucket_counts"],
        "source_root_cause_weights": source["root_cause_weights"],
        "design_ready": design_ready,
        "objective_spec": spec,
        "phase27_93_required_gates": [
            "renderer emits الموضوع المطلوب for topic-family samples",
            "assistant loss masks the topic anchor line",
            "topic canary manifest covers all target terms",
            "anti-collapse pairs are present",
            "non-topic alias updates are separated from training data",
            "no runtime release is possible from gate encoding alone",
        ],
        "decision": decision,
    }
    return report, spec


def _write_doc(path: Path, report: dict[str, Any]) -> None:
    decision = report["decision"]
    spec = report["objective_spec"]
    lines = [
        "# Phase 27.92 — Topic Objective Repair Design Gate",
        "",
        "## الخلاصة",
        "",
        "هذه مرحلة تصميم فقط. لا تدريب ولا runtime.",
        "",
        f"- status: `{report['status']}`",
        f"- decision: `{decision['engineering_decision']}`",
        f"- topic gate encoding allowed: `{decision['topic_gate_encoding_allowed']}`",
        f"- training allowed: `{decision['new_training_allowed']}`",
        f"- runtime release: `{decision['runtime_release_allowed']}`",
        f"- next: `{decision['next_phase']}`",
        "",
        "## التصميم",
        "",
        f"- objective: `{spec['objective_name']}`",
        f"- target family: `{spec['target_family']}`",
        f"- target terms: `{spec['target_terms']}`",
        "",
        "### Conditioning Lines",
        "",
    ]
    for line in spec["conditioning_lines"]:
        lines.append(f"- `{line}`")
    lines.extend(
        [
            "",
            "### Answer Contract",
            "",
            *[f"- {item}" for item in spec["answer_contract"]],
            "",
            "### Canary Design",
            "",
        ]
    )
    for key, value in spec["canary_design"].items():
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(
        [
            "",
            "## القرار",
            "",
            decision["why"],
            "",
            "## محظور الآن",
            "",
            *[f"- {item}" for item in spec["blocked"]],
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    args = parse_args()
    try:
        report, spec = build_report(args)
    except (FileNotFoundError, json.JSONDecodeError, KeyError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    args.decision.parent.mkdir(parents=True, exist_ok=True)
    args.decision.write_text(
        json.dumps(report["decision"], ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    args.spec.parent.mkdir(parents=True, exist_ok=True)
    args.spec.write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _write_doc(args.doc, report)
    print(json.dumps(report["decision"], ensure_ascii=False, indent=2))
    return 0 if report["status"] == "PHASE27_92_TOPIC_OBJECTIVE_REPAIR_DESIGN_READY_NO_TRAINING" else 1


if __name__ == "__main__":
    raise SystemExit(main())
