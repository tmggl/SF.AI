#!/usr/bin/env python3
"""Phase 27.90 — evaluate bounded SF-10M round-robin curriculum repair.

Training is run separately with the Phase 27.89 required flag:
--split-order family_round_robin. This script evaluates the resulting
checkpoints and decides whether the next step is a held-out release gate or a
fresh diagnosis. It never opens runtime by itself.
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

from scripts.phase27_87_bounded_family_conditioned_repair import (  # noqa: E402
    _evaluate_checkpoint,
    _rel,
)

DEFAULT_SOURCE = ROOT / "artifacts/reports/phase27_89_stratified_round_robin_curriculum_sampler_gate_report.json"
DEFAULT_TOKENIZER = ROOT / "artifacts/tokenizers/sf_bpe/v9_phase27_76"
DEFAULT_CHECKPOINTS = ROOT / "artifacts/eval/phase27_90_round_robin_curriculum_repair/checkpoints"
DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_90_bounded_round_robin_repair_report.json"
DEFAULT_DECISION = ROOT / "artifacts/reports/PHASE27_90_BOUNDED_ROUND_ROBIN_REPAIR_DECISION.json"
DEFAULT_DOC = ROOT / "docs/PHASE27_90_BOUNDED_ROUND_ROBIN_REPAIR_REPORT.md"
DEFAULT_SAMPLES = ROOT / "artifacts/samples/phase27_90_bounded_round_robin_repair.md"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Evaluate Phase 27.90 round-robin repair checkpoints")
    p.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    p.add_argument("--tokenizer", type=Path, default=DEFAULT_TOKENIZER)
    p.add_argument("--checkpoints", type=Path, default=DEFAULT_CHECKPOINTS)
    p.add_argument("--device", default="auto")
    p.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    p.add_argument("--decision", type=Path, default=DEFAULT_DECISION)
    p.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    p.add_argument("--samples", type=Path, default=DEFAULT_SAMPLES)
    return p.parse_args(argv)


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(path)
    return json.loads(path.read_text(encoding="utf-8"))


def build_report(args: argparse.Namespace) -> dict[str, Any]:
    source = _load_json(args.source)
    if source["decision"]["engineering_decision"] != (
        "ALLOW_PHASE27_90_BOUNDED_SF10M_TRAINING_WITH_ROUND_ROBIN_SPLIT_ORDER"
    ):
        raise ValueError("Phase 27.89 did not allow Phase 27.90 training")

    checkpoints = ("sf-10m-step600", "sf-10m-step1200", "sf-10m-step1800")
    evaluated = [_evaluate_checkpoint(args, checkpoint) for checkpoint in checkpoints]
    best = max(evaluated, key=lambda row: row["summary"]["passed"])
    all_state_ok = all(row["meta"]["state_exists"] and row["meta"]["sf_origin"] for row in evaluated)
    passed = int(best["summary"]["passed"])
    total = int(best["summary"]["total"])
    heldout_gate_threshold = max(1, int(total * 0.9))
    heldout_gate_allowed = bool(all_state_ok and passed >= heldout_gate_threshold)

    decision = {
        "decision_id": "PHASE27_90_BOUNDED_ROUND_ROBIN_REPAIR_DECISION",
        "engineering_decision": (
            "ALLOW_PHASE27_91_HELDOUT_RUNTIME_GATE_NO_DIRECT_RUNTIME"
            if heldout_gate_allowed
            else "BLOCK_RUNTIME_DIAGNOSE_ROUND_ROBIN_TRAINING_RESULT"
        ),
        "training_completed": True,
        "runtime_release_allowed": False,
        "ui_release_allowed": False,
        "heldout_runtime_gate_allowed": heldout_gate_allowed,
        "sf50m_justified_transition": False,
        "tokenizer_retrain_allowed": False,
        "best_checkpoint_by_fresh_shadow": best["checkpoint"],
        "best_fresh_shadow_passed": passed,
        "best_fresh_shadow_total": total,
        "heldout_gate_threshold": heldout_gate_threshold,
        "required_training_flag_used": "--split-order family_round_robin",
        "why": (
            f"Best checkpoint reached {passed}/{total} fresh-shadow passes after "
            "round-robin family curriculum training. Direct runtime remains blocked."
        ),
        "next_phase": (
            "Phase 27.91 — Held-out Runtime Release Gate"
            if heldout_gate_allowed
            else "Phase 27.91 — Round-Robin Training Result Diagnosis"
        ),
    }
    return {
        "phase": "Phase 27.90",
        "strategy": "Sovereign Practical Acceleration Strategy v2",
        "sovereignty_mode": "SF-native only",
        "status": (
            "PHASE27_90_TRAINED_HELDOUT_GATE_ALLOWED_RUNTIME_BLOCKED"
            if heldout_gate_allowed
            else "PHASE27_90_TRAINED_RUNTIME_BLOCKED_DIAGNOSIS_REQUIRED"
        ),
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "training_started": True,
        "training_completed": True,
        "runtime_changed": False,
        "source_phase27_89_status": source["status"],
        "training_scope": "bounded SF-10M repair with family_round_robin split order",
        "tokenizer": _rel(args.tokenizer),
        "init_checkpoint": (
            "artifacts/eval/phase27_77_v9_bounded_open_social_lm_repair/"
            "checkpoints/sf-10m-step6200"
        ),
        "checkpoint_root": _rel(args.checkpoints),
        "family_conditioning_runtime_eval": True,
        "split_order": "family_round_robin",
        "checkpoints": evaluated,
        "decision": decision,
    }


def _write_doc(path: Path, report: dict[str, Any]) -> None:
    decision = report["decision"]
    lines = [
        "# Phase 27.90 — Bounded SF-10M Round-Robin Curriculum Repair Training",
        "",
        "## الخلاصة",
        "",
        "اكتمل تقييم التدريب المقيّد بترتيب `family_round_robin`. هذه المرحلة لا تفتح runtime مباشرة.",
        "",
        f"- status: `{report['status']}`",
        f"- decision: `{decision['engineering_decision']}`",
        f"- runtime release: `{decision['runtime_release_allowed']}`",
        f"- held-out gate allowed: `{decision['heldout_runtime_gate_allowed']}`",
        f"- best checkpoint: `{decision['best_checkpoint_by_fresh_shadow']}`",
        f"- best fresh shadow: `{decision['best_fresh_shadow_passed']}/{decision['best_fresh_shadow_total']}`",
        f"- held-out threshold: `{decision['heldout_gate_threshold']}/{decision['best_fresh_shadow_total']}`",
        f"- next: `{decision['next_phase']}`",
        "",
        "## Checkpoints",
        "",
    ]
    for row in report["checkpoints"]:
        summary = row["summary"]
        lines.extend(
            [
                f"### {row['checkpoint']}",
                "",
                f"- fresh shadow: `{summary['passed']}/{summary['total']}`",
                f"- family summary: `{summary['family_summary']}`",
                f"- reason counts: `{summary['reason_counts']}`",
                "",
            ]
        )
    lines.extend(
        [
            "## القرار",
            "",
            "- لا تفعيل مباشر للواجهة من هذه المرحلة.",
            "- لا SF-50M.",
            "- لا tokenizer retrain.",
            "- إذا سمحت النتيجة ببوابة held-out، فالمرحلة التالية gate إضافية لا runtime مباشر.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_samples(path: Path, report: dict[str, Any]) -> None:
    lines = ["# Phase 27.90 Samples", ""]
    for checkpoint in report["checkpoints"]:
        lines.extend([f"## {checkpoint['checkpoint']}", ""])
        for row in checkpoint["rows"][:20]:
            lines.extend(
                [
                    f"### {row['id']} — {'PASS' if row['passed'] else 'FAIL'}",
                    "",
                    f"- family: {row['family']}",
                    f"- prompt: {row['prompt']}",
                    f"- response: {row['response']}",
                    f"- reason: {row['reason']}",
                    "",
                ]
            )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    args = parse_args()
    try:
        report = build_report(args)
    except (FileNotFoundError, json.JSONDecodeError, KeyError, ValueError) as exc:
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
    _write_samples(args.samples, report)

    decision = report["decision"]
    print("SF.AI — Phase 27.90 bounded round-robin repair")
    print(f"status: {report['status']}")
    print(f"decision: {decision['engineering_decision']}")
    print(
        "best: "
        f"{decision['best_checkpoint_by_fresh_shadow']} "
        f"({decision['best_fresh_shadow_passed']}/{decision['best_fresh_shadow_total']})"
    )
    print(f"next: {decision['next_phase']}")
    print(f"report: {_rel(args.report)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
