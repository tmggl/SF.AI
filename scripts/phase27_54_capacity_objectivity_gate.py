#!/usr/bin/env python3
"""Phase 27.54 capacity/objectivity gate.

This phase is deliberately read-only: it does not train, generate corpus, or
touch checkpoints. It compares the recent open-dialogue failures and records a
scaling decision before any SF-50M work can happen.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_54_capacity_objectivity_gate_report.json"
DEFAULT_DOC = ROOT / "docs/PHASE27_54_CAPACITY_OBJECTIVITY_GATE_REPORT.md"

PHASE27_51 = ROOT / "artifacts/reports/phase27_51_open_dialogue_generalization_audit.json"
PHASE27_52 = ROOT / "artifacts/reports/phase27_52_natural_dialogue_objective_repair_report.json"
PHASE27_53 = ROOT / "artifacts/reports/phase27_53_natural_dialogue_diversity_expansion_report.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the Phase 27.54 scaling gate report")
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    return parser.parse_args()


def _load(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"missing required report: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def _ratio(passed: int, total: int) -> float:
    if total <= 0:
        return 0.0
    return round(passed / total, 4)


def build_report() -> dict[str, Any]:
    p51 = _load(PHASE27_51)
    p52 = _load(PHASE27_52)
    p53 = _load(PHASE27_53)

    raw51 = p51["summary"]["raw_unconditioned"]
    obs = {
        "phase27_51": {
            "candidate_generator": p51["candidate_generator"],
            "training_started": p51["training_started"],
            "raw_natural_passed": raw51["natural_passed"],
            "raw_natural_total": raw51["natural_total"],
            "raw_natural_ratio": _ratio(raw51["natural_passed"], raw51["natural_total"]),
        },
        "phase27_52": {
            "candidate_generator": p52["candidate_generator"],
            "training_started": p52["training_started"],
            "model_size": p52["model_size"],
            "train_records": p52["train_records"],
            "unique_train_pairs": p52["unique_train_pairs"],
            "steps": p52["training_budget"]["steps"],
            "passed": p52["summary"]["passed"],
            "total": p52["summary"]["total"],
            "ratio": _ratio(p52["summary"]["passed"], p52["summary"]["total"]),
        },
        "phase27_53": {
            "candidate_generator": p53["candidate_generator"],
            "training_started": p53["training_started"],
            "model_size": p53["model_size"],
            "unique_train_records": p53["unique_train_records"],
            "steps": p53["training_budget"]["steps"],
            "passed": p53["summary"]["passed"],
            "total": p53["summary"]["total"],
            "ratio": _ratio(p53["summary"]["passed"], p53["summary"]["total"]),
            "dialect_counts": p53["dialect_counts"],
            "category_counts": p53["category_counts"],
        },
    }

    p51_passed = obs["phase27_51"]["raw_natural_passed"]
    p52_passed = obs["phase27_52"]["passed"]
    p53_passed = obs["phase27_53"]["passed"]
    p52_total = obs["phase27_52"]["total"]
    p53_total = obs["phase27_53"]["total"]

    data_volume_helped = p53_passed / p53_total > p52_passed / p52_total
    more_steps_helped = p52_passed > p51_passed
    broad_diversity_regressed = p53_passed / p53_total < p52_passed / p52_total

    return {
        "phase": "Phase 27.54",
        "status": "COMPLETED_CAPACITY_OBJECTIVITY_GATE_FULL_SCALING_BLOCKED_DIAGNOSTIC_MICRO_PROBE_ALLOWED",
        "training_started": False,
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "template_answers_allowed": False,
        "progressive_scaling_strategy_respected": True,
        "observations": obs,
        "diagnosis": {
            "more_steps_alone_helped_some": more_steps_helped,
            "data_volume_alone_helped": data_volume_helped,
            "broad_diversity_regressed_vs_phase27_52": broad_diversity_regressed,
            "sf10m_collapses_under_broad_open_dialogue": True,
            "objective_or_format_issue_still_possible": True,
            "capacity_limit_suspected_but_not_proven": True,
            "direct_full_scaling_would_be_blind": True,
        },
        "scaling_gates": {
            "corpus_readiness": {
                "passed": True,
                "notes": "Phase 27.53 produced governed MSA/Saudi dialogue with operational dialogue excluded.",
            },
            "tokenization_audit": {
                "passed": True,
                "notes": "Tokenizer v6 is sovereign and protected weak-lane terms are present.",
            },
            "evaluation_suite": {
                "passed": False,
                "notes": "Open natural dialogue remains far below the runtime bar: 2/36 in Phase 27.53.",
            },
            "safety_checks": {
                "passed": True,
                "notes": "No unsafe domain expansion was opened; generator-only runtime stays guarded.",
            },
            "runtime_quality": {
                "passed": False,
                "notes": "Newer checkpoints are not opened; live UI stays on Phase 27.47 only.",
            },
            "hallucination_checks": {
                "passed": False,
                "notes": "Open dialogue failures include prompt drift and unrelated fragments.",
            },
            "repetition_checks": {
                "passed": False,
                "notes": "Phase 27.53 still shows fragments/mixing; quality gate blocks runtime.",
            },
            "resource_readiness": {
                "passed": True,
                "notes": "Local MPS training pipeline and checkpoint policy are available.",
            },
        },
        "decisions": {
            "runtime_switch_allowed": False,
            "phase27_52_runtime_allowed": False,
            "phase27_53_runtime_allowed": False,
            "sf50m_full_training_allowed": False,
            "phase28_allowed": False,
            "sf50m_diagnostic_micro_probe_allowed": True,
            "diagnostic_micro_probe_is_not_runtime_scaling": True,
            "must_compare_against_sf10m_same_data_and_eval": True,
        },
        "next_phase": (
            "Phase 27.55 — Controlled SF-50M diagnostic micro-probe vs SF-10M baseline; "
            "bounded training only, no runtime switch unless gate passes"
        ),
        "required_next_gate": {
            "purpose": "prove whether capacity helps before any full SF-50M plan",
            "conditions": [
                "same governed MSA/Saudi micro corpus for SF-10M and SF-50M comparison",
                "same tokenizer policy unless explicitly audited",
                "same held-out natural dialogue suite",
                "no templates and no keyword-lane claims",
                "no runtime switch on partial result",
                "report must show clear improvement over Phase 27.52 and Phase 27.53",
            ],
            "minimum_to_open_runtime": (
                "natural dialogue quality must pass the gate, not merely improve numerically"
            ),
        },
    }


def write_doc(report: dict[str, Any], path: Path) -> None:
    gates = report["scaling_gates"]
    obs = report["observations"]
    lines = [
        "# Phase 27.54 — Capacity/Objectivity Gate",
        "",
        "## الخلاصة",
        "",
        "هذه المرحلة لم تبدأ تدريبًا جديدًا. قرأت نتائج Phase 27.51–27.53 وخرجت بقرار واضح:",
        "",
        "- لا يتم فتح `sf_10m_phase27_52` ولا `sf_10m_phase27_53` في الواجهة.",
        "- لا يسمح بتدريب `SF-50M` كامل الآن.",
        "- لا يسمح ببدء Phase 28 الآن.",
        "- يسمح فقط بمرحلة تشخيصية مضبوطة: `SF-50M` micro-probe مقارنة بنفس corpus/eval ضد `SF-10M`.",
        "",
        "## الدليل الرقمي",
        "",
        "| المرحلة | المرشح | التدريب | النتيجة | القرار |",
        "|---------|--------|---------|---------|--------|",
        (
            f"| Phase 27.51 | `{obs['phase27_51']['candidate_generator']}` | لا | "
            f"{obs['phase27_51']['raw_natural_passed']}/{obs['phase27_51']['raw_natural_total']} raw natural | فشل تعميم الحوار المفتوح |"
        ),
        (
            f"| Phase 27.52 | `{obs['phase27_52']['candidate_generator']}` | "
            f"{obs['phase27_52']['steps']} خطوة / {obs['phase27_52']['unique_train_pairs']} زوجًا فريدًا | "
            f"{obs['phase27_52']['passed']}/{obs['phase27_52']['total']} | تحسن جزئي لا يكفي |"
        ),
        (
            f"| Phase 27.53 | `{obs['phase27_53']['candidate_generator']}` | "
            f"{obs['phase27_53']['steps']} خطوة / {obs['phase27_53']['unique_train_records']} سجلًا فريدًا | "
            f"{obs['phase27_53']['passed']}/{obs['phase27_53']['total']} | تراجع مع تنوع واسع |"
        ),
        "",
        "## التشخيص",
        "",
        "- زيادة الخطوات وحدها ساعدت قليلًا في Phase 27.52 لكنها لم تصل لحوار مقنع.",
        "- زيادة البيانات والتنوع داخل `SF-10M` تراجعت إلى `2/36` في Phase 27.53.",
        "- إذن المشكلة ليست نقص أمثلة فقط. يوجد حد من السعة أو الهدف أو الصيغة أو التوكنة.",
        "- التكبير الكامل الآن سيكون قفزة عمياء؛ الصحيح تجربة تشخيصية صغيرة تثبت هل السعة تساعد فعلًا.",
        "",
        "## Scaling Gates",
        "",
        "| gate | النتيجة | الملاحظة |",
        "|------|---------|----------|",
    ]
    for name, gate in gates.items():
        mark = "pass" if gate["passed"] else "fail"
        lines.append(f"| `{name}` | {mark} | {gate['notes']} |")

    lines.extend(
        [
            "",
            "## القرار",
            "",
            "- `runtime_switch_allowed=false`",
            "- `sf50m_full_training_allowed=false`",
            "- `phase28_allowed=false`",
            "- `sf50m_diagnostic_micro_probe_allowed=true`",
            "",
            "الـ micro-probe التشخيصي ليس تكبيرًا رسميًا ولا يفتح runtime. هو اختبار قصير مضبوط لمعرفة هل السعة تحل جزءًا من المشكلة أم أن العائق في objective/format/tokenizer.",
            "",
            "## المرحلة التالية",
            "",
            report["next_phase"],
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = parse_args()
    report = build_report()
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    write_doc(report, args.doc)
    print(json.dumps({"phase": report["phase"], "status": report["status"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
