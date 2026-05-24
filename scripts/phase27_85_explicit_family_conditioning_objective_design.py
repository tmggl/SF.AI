#!/usr/bin/env python3
"""Phase 27.85 — Explicit Family Conditioning Objective Design.

No training. No runtime release. This phase converts the Phase 27.84 diagnosis
into an implementation-ready objective/curriculum spec.
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


DEFAULT_SOURCE = ROOT / "artifacts/reports/phase27_84_objective_curriculum_failure_diagnosis_report.json"
DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_85_explicit_family_conditioning_objective_design_report.json"
DEFAULT_DECISION = ROOT / "artifacts/reports/PHASE27_85_EXPLICIT_FAMILY_CONDITIONING_OBJECTIVE_DESIGN_DECISION.json"
DEFAULT_SPEC = ROOT / "artifacts/reports/phase27_85_family_conditioning_objective_spec.json"
DEFAULT_DOC = ROOT / "docs/PHASE27_85_EXPLICIT_FAMILY_CONDITIONING_OBJECTIVE_DESIGN_REPORT.md"

FAMILY_LABELS = {
    "open_social": "سوالف",
    "followup": "متابعة",
    "planning": "تنظيم",
    "support": "دعم",
    "topic": "موضوع",
}

FAMILY_DESCRIPTIONS = {
    "open_social": "حديث اجتماعي طبيعي وسوالف خفيفة.",
    "followup": "متابعة معنى سابق أو طلب توضيح.",
    "planning": "تنظيم وقت أو مهام أو بداية عملية.",
    "support": "طمأنة وتهدئة ودعم وجداني عام.",
    "topic": "شرح معنى أو قيمة أو فكرة عامة.",
}

CANARY_THRESHOLDS = {
    "per_family_min_pass": 10,
    "overall_min_pass": 55,
    "malformed_max": 0,
    "repeated_phrase_max": 0,
    "dominant_family_share_max": 0.35,
}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Build Phase 27.85 family-conditioning design")
    p.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    p.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    p.add_argument("--decision", type=Path, default=DEFAULT_DECISION)
    p.add_argument("--spec", type=Path, default=DEFAULT_SPEC)
    p.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    return p.parse_args()


def _rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(path)
    return json.loads(path.read_text(encoding="utf-8"))


def _render_preview(family: str, dialect: str = "saudi") -> str:
    dialect_label = "سعودي" if dialect == "saudi" else "فصحى"
    family_label = FAMILY_LABELS[family]
    prompt = {
        "open_social": "وش رايك نسولف شوي؟",
        "followup": "وضح لي مقصدك اكثر.",
        "planning": "كيف أنظم دراستي اليوم؟",
        "support": "صدري ضايق وابغى اهدأ.",
        "topic": "ما معنى الشجاعة؟",
    }[family]
    answer = {
        "open_social": "نسولف عن يومك بشي خفيف: وش ألطف موقف صار لك؟",
        "followup": "أقصد نبدأ من أبسط نقطة ثم نكمل عليها خطوة خطوة.",
        "planning": "اكتب ثلاث مهام، واختر أهم واحدة وابدأ بها مدة قصيرة.",
        "support": "خذ نفسًا هادئًا، وخلّك مع خطوة صغيرة الآن.",
        "topic": "الشجاعة هي فعل الصواب رغم الخوف.",
    }[family]
    return (
        f"النطاق: {dialect_label}\n"
        f"عائلة الحوار: {family_label}\n"
        f"المستخدم: {prompt}\n"
        f"المساعد: {answer}\n"
    )


def build_spec() -> dict[str, Any]:
    examples = {
        family: {
            "label": label,
            "description": FAMILY_DESCRIPTIONS[family],
            "rendered_preview": _render_preview(family),
        }
        for family, label in FAMILY_LABELS.items()
    }
    return {
        "spec_id": "PHASE27_85_FAMILY_CONDITIONING_OBJECTIVE_SPEC",
        "version": "v1",
        "language_track": ["msa", "saudi"],
        "conditioning_lines": [
            "النطاق: <msa|saudi rendered as فصحى|سعودي>",
            "عائلة الحوار: <سوالف|متابعة|تنظيم|دعم|موضوع>",
        ],
        "family_labels": FAMILY_LABELS,
        "family_descriptions": FAMILY_DESCRIPTIONS,
        "rendering_rule": (
            "The family line appears before the user turn in every dialogue training sample. "
            "It is context only, not assistant target text."
        ),
        "assistant_loss_rule": (
            "With loss_scope=assistant, both conditioning lines and user turns remain masked; "
            "only assistant content plus EOS are supervised."
        ),
        "runtime_prompt_rule": (
            "Any future generator runtime must prepend the same family line selected by the "
            "router/semantic family classifier before calling the model."
        ),
        "curriculum_rule": (
            "Training sampler must interleave families in a round-robin or stratified schedule; "
            "balanced counts alone are insufficient."
        ),
        "canary_thresholds": CANARY_THRESHOLDS,
        "examples": examples,
        "blocked": [
            "training before renderer/gate implementation",
            "runtime release",
            "SF-50M transition",
            "tokenizer retrain",
            "pretrained/open-weight usage",
        ],
    }


def build_report(args: argparse.Namespace) -> tuple[dict[str, Any], dict[str, Any]]:
    source = _load_json(args.source)
    spec = build_spec()
    source_decision = source["decision"]["engineering_decision"]
    family_missing = source["evidence"]["family_signal_missing"] is True
    design_ready = (
        source_decision == "DESIGN_EXPLICIT_FAMILY_CONDITIONING_OBJECTIVE_BEFORE_ANY_TRAINING"
        and family_missing
        and set(spec["family_labels"]) == {"open_social", "followup", "planning", "support", "topic"}
    )
    decision = {
        "decision_id": "PHASE27_85_EXPLICIT_FAMILY_CONDITIONING_OBJECTIVE_DESIGN_DECISION",
        "engineering_decision": (
            "ALLOW_PHASE27_86_RENDERER_GATE_IMPLEMENTATION_NO_TRAINING"
            if design_ready
            else "BLOCK_PHASE27_86_FIX_DESIGN"
        ),
        "new_training_allowed": False,
        "renderer_implementation_allowed": design_ready,
        "runtime_release_allowed": False,
        "ui_release_allowed": False,
        "sf50m_justified_transition": False,
        "tokenizer_retrain_allowed": False,
        "why": (
            "A visible Arabic family-conditioning line is specified as context-only input; "
            "training remains blocked until the renderer/gate proves it is actually emitted."
        ),
        "next_phase": "Phase 27.86 — Family Conditioning Renderer Gate",
    }
    report = {
        "phase": "Phase 27.85",
        "strategy": "Sovereign Practical Acceleration Strategy v2",
        "sovereignty_mode": "SF-native only",
        "status": (
            "PHASE27_85_EXPLICIT_FAMILY_CONDITIONING_DESIGN_READY_NO_TRAINING"
            if design_ready
            else "PHASE27_85_DESIGN_BLOCKED"
        ),
        "training_started": False,
        "runtime_changed": False,
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "source_report": _rel(args.source),
        "design_ready": design_ready,
        "objective_spec": spec,
        "implementation_gates_for_phase27_86": [
            "rendered training text contains the family line",
            "assistant loss masks conditioning lines",
            "split-manifest rendering path and no-split rendering path match",
            "all five families produce distinct labels",
            "no runtime release is possible from renderer gate alone",
        ],
        "decision": decision,
    }
    return report, spec


def _write_doc(path: Path, report: dict[str, Any]) -> None:
    decision = report["decision"]
    spec = report["objective_spec"]
    lines = [
        "# Phase 27.85 — Explicit Family Conditioning Objective Design",
        "",
        "## الخلاصة",
        "",
        "هذه مرحلة تصميم فقط. لم يبدأ تدريب ولم يتغير runtime.",
        "",
        f"- status: `{report['status']}`",
        f"- decision: `{decision['engineering_decision']}`",
        f"- renderer implementation allowed: `{decision['renderer_implementation_allowed']}`",
        f"- training allowed: `{decision['new_training_allowed']}`",
        f"- next: `{decision['next_phase']}`",
        "",
        "## Conditioning Lines",
        "",
    ]
    for line in spec["conditioning_lines"]:
        lines.append(f"- `{line}`")
    lines.extend(["", "## Family Labels", ""])
    for key, label in spec["family_labels"].items():
        lines.append(f"- `{key}` → `{label}`")
    lines.extend(
        [
            "",
            "## Objective Rule",
            "",
            spec["assistant_loss_rule"],
            "",
            "## Canary Thresholds",
            "",
        ]
    )
    for key, value in spec["canary_thresholds"].items():
        lines.append(f"- `{key}`: `{value}`")
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

    print("SF.AI — Phase 27.85 explicit family conditioning design")
    print(f"status: {report['status']}")
    print(f"decision: {report['decision']['engineering_decision']}")
    print(f"next: {report['decision']['next_phase']}")
    print(f"report: {_rel(args.report)}")
    return 0 if report["design_ready"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
