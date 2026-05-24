#!/usr/bin/env python3
"""Phase 27.83 — consolidate bounded repair training results.

This phase trains once (done by `make train-lm` from the Phase 27.82 plan)
and then records whether the produced checkpoints may move toward runtime.

The script does not train and does not release runtime. It reads the fresh
shadow canary reports produced for the Phase 27.83 checkpoints and emits the
engineering decision.
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


DEFAULT_EVAL_DIR = ROOT / "artifacts/reports/phase27_83_family_conditioned_repair_training"
DEFAULT_SAMPLES_DIR = ROOT / "artifacts/samples/phase27_83_family_conditioned_repair_training"
DEFAULT_CHECKPOINTS = ROOT / "artifacts/eval/phase27_83_family_conditioned_repair/checkpoints"
DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_83_family_conditioned_repair_training_report.json"
DEFAULT_DECISION = ROOT / "artifacts/reports/PHASE27_83_FAMILY_CONDITIONED_REPAIR_TRAINING_DECISION.json"
DEFAULT_DOC = ROOT / "docs/PHASE27_83_FAMILY_CONDITIONED_REPAIR_TRAINING_REPORT.md"
DEFAULT_SAMPLES = ROOT / "artifacts/samples/phase27_83_family_conditioned_repair_training.md"

EVAL_LOSS = {
    "sf-10m-step600": {"loss": 3.7397, "perplexity": 42.08},
    "sf-10m-step1200": {"loss": 5.9248, "perplexity": 374.19},
    "sf-10m-step1800": {"loss": 5.9722, "perplexity": 392.39},
}

GENERATION_NOTES = {
    "sf-10m-step600": "عندما تريد الهدوءخفيف عن يومك.",
    "sf-10m-step1200": "اكتب ثلاث وابدأ بالأهم وقت لاحقم، وابدأ بالأهم لمعشدقيقة.",
    "sf-10m-step1800": "بعد ه. ه. ه. شيء أأأن تجيرة، وابدأ بشي بشي بشي عل عل عل إذا تجلوقت ثتجلس فيه واضح.",
}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Build Phase 27.83 repair training report")
    p.add_argument("--eval-dir", type=Path, default=DEFAULT_EVAL_DIR)
    p.add_argument("--samples-dir", type=Path, default=DEFAULT_SAMPLES_DIR)
    p.add_argument("--checkpoints", type=Path, default=DEFAULT_CHECKPOINTS)
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


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(path)
    return json.loads(path.read_text(encoding="utf-8"))


def _checkpoint_meta(root: Path, checkpoint: str) -> dict[str, Any]:
    meta_path = root / checkpoint / "meta.json"
    meta = _load_json(meta_path)
    state_path = root / checkpoint / "state.pt"
    return {
        "checkpoint": checkpoint,
        "path": _rel(root / checkpoint),
        "state_exists": state_path.exists(),
        "sf_origin": meta.get("sf_origin") is True,
        "step": meta.get("step"),
        "model_name": meta.get("model_name"),
        "notes": meta.get("notes", ""),
    }


def _checkpoint_report(args: argparse.Namespace, checkpoint: str) -> dict[str, Any]:
    step = checkpoint.rsplit("step", 1)[-1]
    canary_path = args.eval_dir / f"fresh_shadow_step{step}.json"
    canary = _load_json(canary_path)
    summary = canary["summary"]
    return {
        "checkpoint": checkpoint,
        "meta": _checkpoint_meta(args.checkpoints, checkpoint),
        "fresh_shadow_report": _rel(canary_path),
        "fresh_shadow": summary,
        "eval_loss": EVAL_LOSS.get(checkpoint),
        "sample_generation": GENERATION_NOTES.get(checkpoint, ""),
    }


def build_report(args: argparse.Namespace) -> dict[str, Any]:
    checkpoints = ("sf-10m-step600", "sf-10m-step1200", "sf-10m-step1800")
    rows = [_checkpoint_report(args, checkpoint) for checkpoint in checkpoints]
    best_by_canary = max(rows, key=lambda row: row["fresh_shadow"]["passed"])
    best_by_loss = min(rows, key=lambda row: row["eval_loss"]["loss"])

    all_state_ok = all(row["meta"]["state_exists"] and row["meta"]["sf_origin"] for row in rows)
    fresh_threshold = 60
    runtime_release_allowed = (
        all_state_ok and best_by_canary["fresh_shadow"]["passed"] >= fresh_threshold
    )
    next_phase = (
        "Phase 27.84 — Objective/Curriculum Failure Diagnosis"
        if not runtime_release_allowed
        else "Phase 27.84 — Held-out Runtime Release Gate"
    )
    decision = {
        "decision_id": "PHASE27_83_FAMILY_CONDITIONED_REPAIR_TRAINING_DECISION",
        "engineering_decision": (
            "BLOCK_RUNTIME_DIAGNOSE_OBJECTIVE_CURRICULUM_FAILURE"
            if not runtime_release_allowed
            else "ALLOW_HELDOUT_RUNTIME_RELEASE_GATE"
        ),
        "training_completed": True,
        "runtime_release_allowed": runtime_release_allowed,
        "ui_release_allowed": False,
        "sf50m_justified_transition": False,
        "tokenizer_retrain_allowed": False,
        "best_checkpoint_by_canary": best_by_canary["checkpoint"],
        "best_checkpoint_by_eval_loss": best_by_loss["checkpoint"],
        "why": (
            "The best fresh-shadow checkpoint reached only "
            f"{best_by_canary['fresh_shadow']['passed']}/{best_by_canary['fresh_shadow']['total']}; "
            "training over-collapsed into one family and produced malformed/repetitive samples."
        ),
        "next_phase": next_phase,
    }

    return {
        "phase": "Phase 27.83",
        "strategy": "Sovereign Practical Acceleration Strategy v2",
        "sovereignty_mode": "SF-native only",
        "status": "PHASE27_83_TRAINED_RUNTIME_BLOCKED_DIAGNOSIS_REQUIRED",
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "training_started": True,
        "training_completed": True,
        "runtime_changed": False,
        "training_scope": "bounded SF-10M repair training from Phase 27.82 plan",
        "tokenizer": "artifacts/tokenizers/sf_bpe/v9_phase27_76",
        "init_checkpoint": "artifacts/eval/phase27_77_v9_bounded_open_social_lm_repair/checkpoints/sf-10m-step6200",
        "checkpoint_root": _rel(args.checkpoints),
        "checkpoints": rows,
        "observations": [
            "step600 has the lowest eval loss but weak fresh-shadow pass rate.",
            "step1200 has the best fresh-shadow count but is concentrated in planning.",
            "step1800 regresses further and produces malformed repetition.",
            "Loss alone is not reliable; runtime remains blocked by held-out behavior.",
        ],
        "decision": decision,
    }


def _write_doc(path: Path, report: dict[str, Any]) -> None:
    decision = report["decision"]
    lines = [
        "# Phase 27.83 — Family-conditioned SF-10M Bounded Repair Training",
        "",
        "## الخلاصة",
        "",
        "اكتمل تدريب الإصلاح المحدود، لكنه فشل في بوابة الحوار غير المرئي.",
        "",
        f"- status: `{report['status']}`",
        f"- decision: `{decision['engineering_decision']}`",
        f"- runtime release: `{decision['runtime_release_allowed']}`",
        f"- best by canary: `{decision['best_checkpoint_by_canary']}`",
        f"- best by eval loss: `{decision['best_checkpoint_by_eval_loss']}`",
        f"- next: `{decision['next_phase']}`",
        "",
        "## Checkpoints",
        "",
    ]
    for row in report["checkpoints"]:
        summary = row["fresh_shadow"]
        loss = row["eval_loss"]
        lines.extend(
            [
                f"### {row['checkpoint']}",
                "",
                f"- fresh shadow: `{summary['passed']}/{summary['total']}`",
                f"- eval loss: `{loss['loss']}`",
                f"- perplexity: `{loss['perplexity']}`",
                f"- family summary: `{summary['family_summary']}`",
                f"- sample: `{row['sample_generation']}`",
                "",
            ]
        )
    lines.extend(
        [
            "## القرار",
            "",
            "- لا تفعيل للواجهة.",
            "- لا runtime release.",
            "- لا SF-50M.",
            "- لا tokenizer retrain الآن.",
            "- المرحلة التالية تشخيص objective/curriculum failure بدل تدريب أعمى جديد.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_samples(path: Path, report: dict[str, Any]) -> None:
    lines = ["# Phase 27.83 Samples", ""]
    for row in report["checkpoints"]:
        lines.extend([f"## {row['checkpoint']}", ""])
        source = ROOT / row["fresh_shadow_report"]
        canary = _load_json(source)
        failed = [item for item in canary["rows"] if not item["passed"]][:8]
        for item in failed:
            lines.extend(
                [
                    f"### {item['id']} — FAIL",
                    "",
                    f"- family: {item['family']}",
                    f"- prompt: {item['prompt']}",
                    f"- response: {item['response']}",
                    f"- reason: {item['reason']}",
                    "",
                ]
            )
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
    _write_samples(args.samples, report)

    decision = report["decision"]
    print("SF.AI — Phase 27.83 repair training report")
    print(f"status: {report['status']}")
    print(f"decision: {decision['engineering_decision']}")
    print(f"best_by_canary: {decision['best_checkpoint_by_canary']}")
    print(f"runtime_release_allowed: {decision['runtime_release_allowed']}")
    print(f"report: {_rel(args.report)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
