#!/usr/bin/env python3
"""Phase 27.97 — Topic Variable Binding Objective Design.

No training. No tokenizer work. No runtime release.

This phase turns the Phase 27.96 diagnosis into an implementation-ready
objective spec. The current failure is not "topic family missing"; it is that
the generated answer often uses a neighboring memorized topic instead of the
requested topic variable.
"""
# ruff: noqa: E402

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.phase27_26_heldout_objective_repair import _rel

DEFAULT_SOURCE = ROOT / "artifacts/reports/phase27_96_topic_objective_result_diagnosis_report.json"
DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_97_topic_variable_binding_objective_design_report.json"
DEFAULT_DECISION = ROOT / "artifacts/reports/PHASE27_97_TOPIC_VARIABLE_BINDING_OBJECTIVE_DESIGN_DECISION.json"
DEFAULT_SPEC = ROOT / "artifacts/reports/phase27_97_topic_variable_binding_objective_spec.json"
DEFAULT_DOC = ROOT / "docs/PHASE27_97_TOPIC_VARIABLE_BINDING_OBJECTIVE_DESIGN_REPORT.md"

TOPIC_TERMS: tuple[str, ...] = (
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
    p = argparse.ArgumentParser(description="Build Phase 27.97 topic binding objective design")
    p.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    p.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    p.add_argument("--decision", type=Path, default=DEFAULT_DECISION)
    p.add_argument("--spec", type=Path, default=DEFAULT_SPEC)
    p.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    return p.parse_args(argv)


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(path)
    return json.loads(path.read_text(encoding="utf-8"))


def _contrastive_pairs() -> list[dict[str, Any]]:
    pairs: list[dict[str, Any]] = []
    for term in TOPIC_TERMS:
        forbidden = [item for item in TOPIC_TERMS if item != term]
        pairs.append(
            {
                "requested_topic": term,
                "must_include": [term],
                "must_not_include": forbidden,
                "target_prefixes": [
                    f"معنى {term}:",
                    f"{term} يعني",
                    f"{term} هو",
                ],
            }
        )
    return pairs


def build_spec() -> dict[str, Any]:
    return {
        "spec_id": "PHASE27_97_TOPIC_VARIABLE_BINDING_OBJECTIVE_SPEC",
        "version": "v1",
        "language_track": ["msa", "saudi"],
        "target_family": "topic",
        "target_terms": list(TOPIC_TERMS),
        "problem_statement": (
            "Phase 27.95 generated topic-shaped answers, but substituted the requested "
            "topic variable with neighboring topic prototypes such as الصداقة or الشجاعة."
        ),
        "objective_name": "topic_copy_contrastive_binding_objective_v1",
        "conditioning_lines": [
            "النطاق: <فصحى|سعودي>",
            "عائلة الحوار: موضوع",
            "الموضوع المطلوب: <topic_term>",
        ],
        "assistant_target_contract": {
            "copy_anchor": (
                "The assistant answer must copy the exact requested topic term inside the "
                "first 12 visible Arabic characters after the assistant role marker."
            ),
            "prefix_templates": [
                "معنى <topic_term>: <short explanation>",
                "<topic_term> يعني <short explanation>",
                "<topic_term> هو <short explanation>",
            ],
            "single_topic_rule": (
                "For one-sentence topic answers, no other protected topic term may appear "
                "unless the requested topic also appears first."
            ),
            "short_answer_rule": "One compact sentence, 8-18 Arabic words, then EOS.",
            "assistant_loss_rule": (
                "Conditioning/user lines stay masked. The supervised assistant target begins "
                "at the prefix containing <topic_term>, so the model learns copy binding."
            ),
        },
        "contrastive_controls": _contrastive_pairs(),
        "metadata_rule": (
            "Every topic-family training sample must have explicit provenance.topic_term. "
            "Inference from user text is allowed only in audits, not in training gates."
        ),
        "curriculum_rule": {
            "sampler": "topic_term_round_robin_within_family_round_robin",
            "window_size": 800,
            "min_per_topic_per_window": 20,
            "dialect_balance": "each topic alternates msa/saudi when both are available",
            "no_adjacent_same_topic": True,
        },
        "canary_design": {
            "known_topic_min": "16/16",
            "fresh_topic_min": "8/10",
            "contrastive_wrong_topic_max": 0,
            "copy_anchor_min": "26/26",
            "all_family_regression_min": "45/50",
            "topic_family_min": "8/10",
            "malformed_max": 0,
            "repeated_phrase_max": 0,
        },
        "phase27_98_required_gates": [
            "topic metadata audit proves explicit topic_term for every topic sample",
            "renderer can emit copy-anchor targets without unmasking condition lines",
            "contrastive canary covers all topic terms and wrong-topic substitutions",
            "sampler dry-run proves per-topic round-robin exposure",
            "no training is started in the gate-encoding phase",
        ],
        "blocked": [
            "LM training before Phase 27.98 gates",
            "runtime release",
            "UI generator release",
            "SF-50M transition",
            "tokenizer retrain",
            "pretrained/open-weight usage",
            "keyword/template masking",
        ],
    }


def build_report(args: argparse.Namespace) -> tuple[dict[str, Any], dict[str, Any]]:
    source = _load_json(args.source)
    spec = build_spec()
    decision_in = source["decision"]
    signals = source["diagnosis_signals"]
    weights = source["root_cause_weights"]
    design_ready = (
        decision_in["engineering_decision"]
        == "DESIGN_TOPIC_COPY_CONTRASTIVE_OBJECTIVE_BEFORE_ANY_TRAINING"
        and signals["topic_variable_binding_failure"] is True
        and int(signals["wrong_topic_substitution_count"]) >= 10
        and int(weights["topic_variable_binding_failure"]) >= 30
        and int(weights["model_capacity"]) <= 5
        and len(spec["contrastive_controls"]) == len(TOPIC_TERMS)
    )
    decision = {
        "decision_id": "PHASE27_97_TOPIC_VARIABLE_BINDING_OBJECTIVE_DESIGN_DECISION",
        "engineering_decision": (
            "ALLOW_PHASE27_98_TOPIC_BINDING_GATE_ENCODING_NO_TRAINING"
            if design_ready
            else "BLOCK_PHASE27_98_FIX_TOPIC_BINDING_DESIGN"
        ),
        "new_training_allowed": False,
        "topic_binding_gate_encoding_allowed": design_ready,
        "runtime_release_allowed": False,
        "ui_release_allowed": False,
        "heldout_runtime_gate_allowed": False,
        "sf50m_justified_transition": False,
        "tokenizer_retrain_allowed": False,
        "why": (
            "The next step must encode a copy-anchored, contrastive topic objective and "
            "metadata/sampler gates. Capacity and tokenizer remain minor causes."
        ),
        "next_phase": "Phase 27.98 — Topic Binding Gate Encoding and Metadata Audit",
    }
    report = {
        "phase": "Phase 27.97",
        "strategy": "Sovereign Practical Acceleration Strategy v2",
        "sovereignty_mode": "SF-native only",
        "status": (
            "PHASE27_97_TOPIC_BINDING_OBJECTIVE_DESIGN_READY_NO_TRAINING"
            if design_ready
            else "PHASE27_97_TOPIC_BINDING_OBJECTIVE_DESIGN_BLOCKED"
        ),
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "training_started": False,
        "runtime_changed": False,
        "source_report": _rel(args.source),
        "source_diagnosis_signals": signals,
        "source_root_cause_weights": weights,
        "design_ready": design_ready,
        "objective_spec": spec,
        "decision": decision,
    }
    return report, spec


def _write_doc(path: Path, report: dict[str, Any]) -> None:
    decision = report["decision"]
    spec = report["objective_spec"]
    contract = spec["assistant_target_contract"]
    lines = [
        "# Phase 27.97 — Topic Variable Binding Objective Design",
        "",
        "## الخلاصة",
        "",
        "هذه مرحلة تصميم فقط. لا تدريب ولا runtime.",
        "",
        f"- status: `{report['status']}`",
        f"- decision: `{decision['engineering_decision']}`",
        f"- gate encoding allowed: `{decision['topic_binding_gate_encoding_allowed']}`",
        f"- training allowed: `{decision['new_training_allowed']}`",
        f"- runtime release: `{decision['runtime_release_allowed']}`",
        f"- next: `{decision['next_phase']}`",
        "",
        "## Objective",
        "",
        f"- name: `{spec['objective_name']}`",
        f"- target family: `{spec['target_family']}`",
        f"- target terms: `{spec['target_terms']}`",
        "",
        "## Assistant Target Contract",
        "",
        f"- copy anchor: {contract['copy_anchor']}",
        f"- single topic rule: {contract['single_topic_rule']}",
        f"- short answer rule: {contract['short_answer_rule']}",
        "",
        "## Prefix Templates",
        "",
    ]
    for template in contract["prefix_templates"]:
        lines.append(f"- `{template}`")
    lines.extend(["", "## Canary Design", ""])
    for key, value in spec["canary_design"].items():
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(["", "## Phase 27.98 Required Gates", ""])
    for item in spec["phase27_98_required_gates"]:
        lines.append(f"- {item}")
    lines.extend(["", "## Blocked", ""])
    for item in spec["blocked"]:
        lines.append(f"- {item}")
    lines.append("")
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
    args.decision.parent.mkdir(parents=True, exist_ok=True)
    args.spec.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    args.decision.write_text(
        json.dumps(report["decision"], ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    args.spec.write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _write_doc(args.doc, report)
    print(report["status"])
    print(report["decision"]["engineering_decision"])
    print(f"objective={spec['objective_name']}")
    print(f"contrastive_controls={len(spec['contrastive_controls'])}")
    print(f"report={_rel(args.report)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
