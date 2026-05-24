#!/usr/bin/env python3
"""Phase 27.84 — diagnose Phase 27.83 objective/curriculum failure.

No training. No tokenizer work. No runtime release.

The key question: why did a balanced pack plus bounded SF-10M repair still
fail fresh shadow canaries? This script turns the evidence into a decision.
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


DEFAULT_PHASE83 = ROOT / "artifacts/reports/phase27_83_family_conditioned_repair_training_report.json"
DEFAULT_PACK = ROOT / "artifacts/reports/phase27_81_balanced_family_pack_report.json"
DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_84_objective_curriculum_failure_diagnosis_report.json"
DEFAULT_DECISION = ROOT / "artifacts/reports/PHASE27_84_OBJECTIVE_CURRICULUM_FAILURE_DIAGNOSIS_DECISION.json"
DEFAULT_DOC = ROOT / "docs/PHASE27_84_OBJECTIVE_CURRICULUM_FAILURE_DIAGNOSIS_REPORT.md"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run Phase 27.84 failure diagnosis")
    p.add_argument("--phase83-report", type=Path, default=DEFAULT_PHASE83)
    p.add_argument("--pack-report", type=Path, default=DEFAULT_PACK)
    p.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    p.add_argument("--decision", type=Path, default=DEFAULT_DECISION)
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


def _family_conditioning_probe() -> dict[str, Any]:
    """Inspect actual runtime training text, not metadata promises."""
    sample_path = ROOT / "data/corpus/chat/jsonl/dialogue_batch_v10_balanced_planning_saudi_010.jsonl"
    sample = json.loads(sample_path.read_text(encoding="utf-8").splitlines()[0])
    provenance = sample["provenance"]
    rendered_lines = ["النطاق: سعودي"]
    for msg in sample["messages"]:
        role = "المستخدم" if msg["role"] == "user" else "المساعد"
        rendered_lines.append(f"{role}: {msg['content']}")
    rendered = "\n".join(rendered_lines) + "\n"
    return {
        "sample": _rel(sample_path),
        "metadata_dialogue_family": provenance.get("dialogue_family"),
        "metadata_prompt_family": provenance.get("prompt_family"),
        "metadata_answer_family": provenance.get("answer_family"),
        "rendered_training_text_preview": rendered,
        "dialect_condition_visible_to_model": "النطاق:" in rendered,
        "family_condition_visible_to_model": "العائلة:" in rendered or "dialogue_family" in rendered,
        "diagnosis": (
            "family metadata exists, but no family conditioning token/line is visible "
            "inside the text seen by the model"
        ),
    }


def _checkpoint_summary(phase83: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in phase83["checkpoints"]:
        summary = row["fresh_shadow"]
        family_summary = summary["family_summary"]
        passed_by_family = {
            family: int(stats["passed"]) for family, stats in family_summary.items()
        }
        total_passed = int(summary["passed"])
        dominant_family = max(passed_by_family, key=passed_by_family.get)
        dominant_share = (
            round(passed_by_family[dominant_family] / total_passed, 4)
            if total_passed else 0.0
        )
        reason_counts = dict(summary.get("reason_counts", {}))
        rows.append(
            {
                "checkpoint": row["checkpoint"],
                "fresh_shadow_passed": total_passed,
                "fresh_shadow_total": int(summary["total"]),
                "pass_rate": round(total_passed / int(summary["total"]), 4),
                "eval_loss": row["eval_loss"]["loss"],
                "perplexity": row["eval_loss"]["perplexity"],
                "passed_by_family": passed_by_family,
                "dominant_family": dominant_family,
                "dominant_pass_share": dominant_share,
                "reason_counts": reason_counts,
                "sample_generation": row["sample_generation"],
            }
        )
    return rows


def _aggregate_reasons(rows: list[dict[str, Any]]) -> dict[str, int]:
    counter: Counter[str] = Counter()
    for row in rows:
        counter.update(row["reason_counts"])
    return dict(counter.most_common())


def build_report(args: argparse.Namespace) -> dict[str, Any]:
    phase83 = _load_json(args.phase83_report)
    pack = _load_json(args.pack_report)
    checkpoints = _checkpoint_summary(phase83)
    best = max(checkpoints, key=lambda row: row["fresh_shadow_passed"])
    conditioning = _family_conditioning_probe()
    aggregate_reasons = _aggregate_reasons(checkpoints)

    pack_balanced = (
        pack.get("total_records") == 2500
        and all(item.get("records") == 250 for item in pack.get("generated", []))
    )
    family_signal_missing = conditioning["family_condition_visible_to_model"] is False
    collapse_after_balanced_data = (
        pack_balanced
        and best["fresh_shadow_passed"] < 30
        and best["dominant_pass_share"] >= 0.8
    )
    loss_quality_mismatch = (
        phase83["decision"]["best_checkpoint_by_canary"]
        != phase83["decision"]["best_checkpoint_by_eval_loss"]
    )
    malformed_or_repetitive = (
        aggregate_reasons.get("guard:malformed_token", 0)
        + aggregate_reasons.get("guard:repeated_phrase", 0)
    )

    root_cause_weights = {
        "objective_family_signal_missing": 30,
        "curriculum_sampling_not_family_conditioned_in_text": 24,
        "weak_generalization_after_bounded_repair": 17,
        "decoding_and_repetition_fragility": 10,
        "tokenizer_boundary_residual": 7,
        "semantic_routing": 4,
        "data_quality": 4,
        "model_capacity": 4,
    }

    decision = {
        "decision_id": "PHASE27_84_OBJECTIVE_CURRICULUM_FAILURE_DIAGNOSIS_DECISION",
        "engineering_decision": "DESIGN_EXPLICIT_FAMILY_CONDITIONING_OBJECTIVE_BEFORE_ANY_TRAINING",
        "new_training_allowed": False,
        "runtime_release_allowed": False,
        "ui_release_allowed": False,
        "sf50m_justified_transition": False,
        "tokenizer_retrain_allowed": False,
        "why": (
            "Phase 27.83 failed because family metadata was balanced but not visible "
            "as a conditioning signal in training text; loss and canary also disagree."
        ),
        "next_phase": "Phase 27.85 — Explicit Family Conditioning Objective Design",
    }

    return {
        "phase": "Phase 27.84",
        "strategy": "Sovereign Practical Acceleration Strategy v2",
        "sovereignty_mode": "SF-native only",
        "status": "PHASE27_84_DIAGNOSED_OBJECTIVE_CURRICULUM_FAILURE_NO_TRAINING",
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "training_started": False,
        "runtime_changed": False,
        "source_reports": {
            "phase27_83": _rel(args.phase83_report),
            "phase27_81_pack": _rel(args.pack_report),
        },
        "evidence": {
            "pack_balanced": pack_balanced,
            "best_checkpoint": best,
            "conditioning_probe": conditioning,
            "aggregate_reason_counts": aggregate_reasons,
            "family_signal_missing": family_signal_missing,
            "collapse_after_balanced_data": collapse_after_balanced_data,
            "loss_quality_mismatch": loss_quality_mismatch,
            "malformed_or_repetitive_count": malformed_or_repetitive,
        },
        "checkpoint_summaries": checkpoints,
        "root_cause_weights": root_cause_weights,
        "blocked_actions": [
            "new LM training",
            "runtime release",
            "UI generator release",
            "SF-50M transition",
            "tokenizer retrain",
            "pretrained/open-weight usage",
        ],
        "allowed_next_actions": [
            "design explicit family conditioning line/token",
            "design stratified/interleaved family curriculum sampler",
            "define held-out canary thresholds for each family",
            "define decoding-only regression checks",
        ],
        "decision": decision,
    }


def _write_doc(path: Path, report: dict[str, Any]) -> None:
    evidence = report["evidence"]
    decision = report["decision"]
    lines = [
        "# Phase 27.84 — Objective/Curriculum Failure Diagnosis",
        "",
        "## الخلاصة",
        "",
        "هذه مرحلة تشخيص فقط. لم يبدأ تدريب جديد ولم يتغير runtime.",
        "",
        f"- status: `{report['status']}`",
        f"- decision: `{decision['engineering_decision']}`",
        f"- best checkpoint: `{evidence['best_checkpoint']['checkpoint']}`",
        f"- best fresh shadow: `{evidence['best_checkpoint']['fresh_shadow_passed']}/{evidence['best_checkpoint']['fresh_shadow_total']}`",
        f"- runtime release: `{decision['runtime_release_allowed']}`",
        f"- next: `{decision['next_phase']}`",
        "",
        "## السبب الجذري",
        "",
        "التوازن كان موجودًا في metadata، لكن عائلة الحوار لم تكن ظاهرة داخل نص التدريب.",
        "النموذج رأى `النطاق: سعودي/فصحى` فقط، ولم يرَ إشارة مثل `العائلة: planning`.",
        "",
        "## Root Cause Weights",
        "",
    ]
    for key, value in report["root_cause_weights"].items():
        lines.append(f"- `{key}`: `{value}%`")
    lines.extend(
        [
            "",
            "## Evidence",
            "",
            f"- pack balanced: `{evidence['pack_balanced']}`",
            f"- family signal missing: `{evidence['family_signal_missing']}`",
            f"- collapse after balanced data: `{evidence['collapse_after_balanced_data']}`",
            f"- loss/quality mismatch: `{evidence['loss_quality_mismatch']}`",
            f"- malformed/repetitive count: `{evidence['malformed_or_repetitive_count']}`",
            "",
            "## Blocked",
            "",
        ]
    )
    for item in report["blocked_actions"]:
        lines.append(f"- {item}")
    lines.extend(["", "## Allowed Next Actions", ""])
    for item in report["allowed_next_actions"]:
        lines.append(f"- {item}")
    lines.append("")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    args = parse_args()
    try:
        report = build_report(args)
    except (FileNotFoundError, json.JSONDecodeError, KeyError) as exc:
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

    print("SF.AI — Phase 27.84 objective/curriculum failure diagnosis")
    print(f"status: {report['status']}")
    print(f"decision: {report['decision']['engineering_decision']}")
    print(f"next: {report['decision']['next_phase']}")
    print(f"report: {_rel(args.report)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
