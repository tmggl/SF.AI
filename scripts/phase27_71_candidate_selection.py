#!/usr/bin/env python3
"""Phase 27.71 candidate-selection and stability strategy.

No training happens here. Phase 27.70 showed that small repair/fine-tune
attempts can degrade a previously strong checkpoint. This phase compares the
available tokenizer-v8 SF-10M candidates across the same three gates:

1. Phase 27.69 new fresh shadow.
2. Phase 27.67 known shadow.
3. Phase 27.60 broader regression.

Runtime remains blocked unless a candidate passes all three gates exactly.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.phase27_26_heldout_objective_repair import _rel  # noqa: E402
from scripts.phase27_60_broader_natural_dialogue_canary import _evaluate as evaluate_phase27_60, _summary as summary_phase27_60  # noqa: E402
from scripts.phase27_67_fresh_shadow_canary import _evaluate as evaluate_phase27_67, _summary as summary_phase27_67  # noqa: E402
from scripts.phase27_69_new_fresh_shadow_canary import _evaluate as evaluate_phase27_69, _summary as summary_phase27_69  # noqa: E402


DEFAULT_TOKENIZER = ROOT / "artifacts/tokenizers/sf_bpe/v8_phase27_65"
DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_71_candidate_selection_report.json"
DEFAULT_SAMPLES = ROOT / "artifacts/samples/phase27_71_candidate_selection.md"
DEFAULT_DOC = ROOT / "docs/PHASE27_71_CANDIDATE_SELECTION_REPORT.md"


@dataclass(frozen=True)
class Candidate:
    name: str
    phase: str
    checkpoints: Path
    checkpoint_name: str
    notes: str


CANDIDATES: tuple[Candidate, ...] = (
    Candidate(
        name="phase27_66_v8_bounded_topic_repair",
        phase="Phase 27.66",
        checkpoints=ROOT / "artifacts/eval/phase27_66_v8_bounded_topic_repair/checkpoints",
        checkpoint_name="sf-10m-step6200",
        notes="first tokenizer-v8 LM repair; passed Phase 27.60 but failed Phase 27.67",
    ),
    Candidate(
        name="phase27_68_shadow_failure_repair",
        phase="Phase 27.68",
        checkpoints=ROOT / "artifacts/eval/phase27_68_shadow_failure_repair/checkpoints",
        checkpoint_name="sf-10m-step5600",
        notes="best known-shadow repair baseline before Phase 27.70",
    ),
    Candidate(
        name="phase27_70_open_social_repair",
        phase="Phase 27.70",
        checkpoints=ROOT / "artifacts/eval/phase27_70_open_social_repair/checkpoints",
        checkpoint_name="sf-10m-step240",
        notes="open_social repair/fine-tune candidate; failed to beat baseline",
    ),
)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run Phase 27.71 candidate selection")
    p.add_argument("--tokenizer", type=Path, default=DEFAULT_TOKENIZER)
    p.add_argument("--device", default="auto")
    p.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    p.add_argument("--samples", type=Path, default=DEFAULT_SAMPLES)
    p.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    return p.parse_args()


def _missing_candidate_artifacts(candidate: Candidate) -> list[str]:
    root = candidate.checkpoints / candidate.checkpoint_name
    missing: list[str] = []
    for filename in ("meta.json", "state.pt"):
        if not (root / filename).exists():
            missing.append(str(root / filename))
    return missing


def _evaluate_candidate(candidate: Candidate, args: argparse.Namespace) -> dict[str, Any]:
    missing = _missing_candidate_artifacts(candidate)
    base = {
        "name": candidate.name,
        "phase": candidate.phase,
        "checkpoint_root": _rel(candidate.checkpoints),
        "checkpoint_name": candidate.checkpoint_name,
        "notes": candidate.notes,
    }
    if missing:
        return {
            **base,
            "available": False,
            "missing": missing,
            "passed_all": False,
            "score": -1,
            "runtime_switch_allowed": False,
        }

    eval_args = argparse.Namespace(
        tokenizer=args.tokenizer,
        checkpoints=candidate.checkpoints,
        checkpoint_name=candidate.checkpoint_name,
        device=args.device,
    )
    rows_69 = evaluate_phase27_69(eval_args)
    rows_67 = evaluate_phase27_67(eval_args)
    rows_60 = evaluate_phase27_60(eval_args)
    summary_69 = summary_phase27_69(rows_69)
    summary_67 = summary_phase27_67(rows_67)
    summary_60 = summary_phase27_60(rows_60)
    passed_all = (
        summary_69["passed"] == summary_69["total"]
        and summary_67["passed"] == summary_67["total"]
        and summary_60["passed"] == summary_60["total"]
    )
    score = int(summary_69["passed"]) + int(summary_67["passed"]) + int(summary_60["passed"])
    total = int(summary_69["total"]) + int(summary_67["total"]) + int(summary_60["total"])
    return {
        **base,
        "available": True,
        "passed_all": passed_all,
        "score": score,
        "total": total,
        "phase27_69_summary": summary_69,
        "phase27_67_summary": summary_67,
        "phase27_60_summary": summary_60,
        "phase27_69_failures": [row for row in rows_69 if not row["passed"]],
        "phase27_67_failures": [row for row in rows_67 if not row["passed"]],
        "phase27_60_failures": [row for row in rows_60 if not row["passed"]],
        "runtime_switch_allowed": False,
    }


def _best_candidate(candidates: list[dict[str, Any]]) -> dict[str, Any] | None:
    available = [item for item in candidates if item.get("available")]
    if not available:
        return None
    return sorted(
        available,
        key=lambda item: (
            bool(item.get("passed_all")),
            int(item.get("phase27_69_summary", {}).get("passed", 0)),
            int(item.get("phase27_67_summary", {}).get("passed", 0)),
            int(item.get("phase27_60_summary", {}).get("passed", 0)),
            int(item.get("score", -1)),
        ),
        reverse=True,
    )[0]


def _write_samples(path: Path, report: dict[str, Any]) -> None:
    lines = ["# Phase 27.71 Candidate Selection", ""]
    for item in report["candidates"]:
        lines.extend(
            [
                f"## {item['name']}",
                "",
                f"- phase: {item['phase']}",
                f"- checkpoint: {item['checkpoint_root']}/{item['checkpoint_name']}",
                f"- available: `{item['available']}`",
                f"- score: `{item.get('score')}/{item.get('total', 'n/a')}`",
                f"- passed_all: `{item.get('passed_all')}`",
                "",
            ]
        )
        if not item.get("available"):
            for missing in item.get("missing", ()):
                lines.append(f"- missing: `{missing}`")
            lines.append("")
            continue
        for gate, key in (
            ("Phase 27.69 fresh", "phase27_69_summary"),
            ("Phase 27.67 known", "phase27_67_summary"),
            ("Phase 27.60 regression", "phase27_60_summary"),
        ):
            summary = item[key]
            lines.append(f"- {gate}: `{summary['passed']}/{summary['total']}`")
        lines.append("")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _write_doc(path: Path, report: dict[str, Any]) -> None:
    winner = report.get("selected_candidate")
    lines = [
        "# Phase 27.71 — Candidate Selection and Stability Strategy",
        "",
        "## الخلاصة",
        "",
        "هذه مرحلة تقييم فقط. لا تدريب جديد ولا فتح runtime.",
        "",
        f"- status: `{report['status']}`",
        f"- tokenizer: `{report['tokenizer']}`",
        f"- selected candidate: `{winner['name'] if winner else 'none'}`",
        f"- runtime switch allowed: `{report['decisions']['runtime_switch_allowed']}`",
        f"- next phase: `{report['next_phase']}`",
        "",
        "## نتائج المرشحين",
        "",
    ]
    for item in report["candidates"]:
        lines.extend(
            [
                f"### {item['name']}",
                "",
                f"- checkpoint: `{item['checkpoint_root']}/{item['checkpoint_name']}`",
                f"- score: `{item.get('score')}/{item.get('total', 'n/a')}`",
                f"- Phase 27.69 fresh: `{item.get('phase27_69_summary', {}).get('passed', 0)}/{item.get('phase27_69_summary', {}).get('total', 0)}`",
                f"- Phase 27.67 known: `{item.get('phase27_67_summary', {}).get('passed', 0)}/{item.get('phase27_67_summary', {}).get('total', 0)}`",
                f"- Phase 27.60 regression: `{item.get('phase27_60_summary', {}).get('passed', 0)}/{item.get('phase27_60_summary', {}).get('total', 0)}`",
                "",
            ]
        )
    lines.extend(["## القرار", "", report["decision"], ""])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    args = parse_args()
    if not (args.tokenizer / "meta.json").exists():
        print(f"error: missing tokenizer at {args.tokenizer}", file=sys.stderr)
        return 1

    candidates = [_evaluate_candidate(candidate, args) for candidate in CANDIDATES]
    selected = _best_candidate(candidates)
    passed_candidate = selected if selected and selected.get("passed_all") else None
    status = (
        "PASSED_CANDIDATE_SELECTION_RUNTIME_REVIEW_ALLOWED"
        if passed_candidate
        else "NO_STABLE_CANDIDATE_RUNTIME_BLOCKED"
    )
    report = {
        "phase": "Phase 27.71",
        "status": status,
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "training_started": False,
        "tokenizer": _rel(args.tokenizer),
        "candidates": candidates,
        "selected_candidate": selected,
        "decisions": {
            "runtime_switch_allowed": False,
            "ui_open_allowed": False,
            "sf50m_allowed": False,
            "phase28_allowed": False,
            "phase27_72_training_allowed": not bool(passed_candidate),
        },
        "decision": (
            "A candidate passed all current gates, but runtime remains blocked until a separate live review phase."
            if passed_candidate
            else "No candidate passed all three stability gates. Keep runtime blocked and move to a stability-first repair strategy instead of exposing the model."
        ),
        "next_phase": (
            "Phase 27.72 — live runtime review for selected candidate"
            if passed_candidate
            else "Phase 27.72 — stability-first curriculum/selection repair"
        ),
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _write_samples(args.samples, report)
    _write_doc(args.doc, report)

    print("SF.AI — Phase 27.71 candidate selection")
    print(f"  status      : {status}")
    print(f"  tokenizer   : {_rel(args.tokenizer)}")
    for item in candidates:
        print(
            f"  {item['name']:<42} "
            f"{item.get('score')}/{item.get('total', 'n/a')} "
            f"passed_all={item.get('passed_all')}"
        )
    print(f"  selected    : {selected['name'] if selected else 'none'}")
    print("  runtime     : blocked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
