#!/usr/bin/env python3
"""Phase 27.77 bounded LM open_social repair on tokenizer v9.

Phase 27.76 fixed the tokenizer boundary issue that produced fragments such as
`بس الفة`. Because tokenizer v9 changes the vocabulary, this phase trains a
bounded SF-10M candidate from scratch on v9 (no incompatible v8 checkpoint
initialization), then evaluates:

1. Phase 27.69 new fresh shadow.
2. Phase 27.67 known shadow.
3. Phase 27.60 broader regression.

Runtime remains blocked unless every gate passes, and even then a later live
review phase is required.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from collections import defaultdict
from itertools import cycle
from pathlib import Path
from typing import Any

import torch

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.phase27_17_prompt_answer_micro_probe import _latest_checkpoint_name  # noqa: E402
from scripts.phase27_19_hygiene_repair_probe import _write_probe_corpus  # noqa: E402
from scripts.phase27_26_heldout_objective_repair import RepairPair, _rel  # noqa: E402
from scripts.phase27_39_topic_isolation_repair import _conditioned_record  # noqa: E402
from scripts.phase27_60_broader_natural_dialogue_canary import _evaluate as evaluate_phase27_60, _summary as summary_phase27_60  # noqa: E402
from scripts.phase27_62_family_balance_repair import FAMILY_BALANCE_REPAIR  # noqa: E402
from scripts.phase27_66_v8_bounded_topic_repair import TOPIC_EMPHASIS_REPAIR  # noqa: E402
from scripts.phase27_67_fresh_shadow_canary import _evaluate as evaluate_phase27_67, _summary as summary_phase27_67  # noqa: E402
from scripts.phase27_68_shadow_failure_repair import SHADOW_FAILURE_REPAIR  # noqa: E402
from scripts.phase27_70_open_social_repair import OPEN_SOCIAL_REPAIR, STABILITY_REPAIR  # noqa: E402
from scripts.phase27_74_open_social_semantic_collapse_repair import (  # noqa: E402
    FAMILY_SEPARATION_PRESERVE,
    OPEN_SOCIAL_SEMANTIC_REPAIR,
)
from scripts.phase27_69_new_fresh_shadow_canary import _evaluate as evaluate_phase27_69, _summary as summary_phase27_69  # noqa: E402
from sf_ai.training.train_tiny_lm import run as train_tiny_lm_run  # noqa: E402


DEFAULT_TOKENIZER = ROOT / "artifacts/tokenizers/sf_bpe/v9_phase27_76"
DEFAULT_SOURCE_REPORT = ROOT / "artifacts/reports/phase27_76_tokenizer_v9_open_social_boundary_probe_report.json"
DEFAULT_WORK = ROOT / "artifacts/eval/phase27_77_v9_bounded_open_social_lm_repair"
DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_77_v9_bounded_open_social_lm_repair_report.json"
DEFAULT_SAMPLES = ROOT / "artifacts/samples/phase27_77_v9_bounded_open_social_lm_repair.md"
DEFAULT_DOC = ROOT / "docs/PHASE27_77_V9_BOUNDED_OPEN_SOCIAL_LM_REPAIR_REPORT.md"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run Phase 27.77 bounded LM repair on tokenizer v9")
    p.add_argument("--tokenizer", type=Path, default=DEFAULT_TOKENIZER)
    p.add_argument("--source-report", type=Path, default=DEFAULT_SOURCE_REPORT)
    p.add_argument("--steps", type=int, default=6200)
    p.add_argument("--epochs", type=int, default=620)
    p.add_argument("--batch-size", type=int, default=1)
    p.add_argument("--seq-len", type=int, default=80)
    p.add_argument("--lr", type=float, default=4e-4)
    p.add_argument("--warmup", type=int, default=180)
    p.add_argument("--target-per-family", type=int, default=1100)
    p.add_argument("--device", default="auto")
    p.add_argument("--work-dir", type=Path, default=DEFAULT_WORK)
    p.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    p.add_argument("--samples", type=Path, default=DEFAULT_SAMPLES)
    p.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    p.add_argument("--keep-work", action="store_true")
    return p.parse_args()


def _repair_pairs() -> tuple[RepairPair, ...]:
    return (
        *FAMILY_BALANCE_REPAIR,
        *TOPIC_EMPHASIS_REPAIR,
        *SHADOW_FAILURE_REPAIR,
        *OPEN_SOCIAL_REPAIR,
        *STABILITY_REPAIR,
        *OPEN_SOCIAL_SEMANTIC_REPAIR,
        *FAMILY_SEPARATION_PRESERVE,
    )


def _family_groups() -> dict[str, list[RepairPair]]:
    grouped: dict[str, list[RepairPair]] = defaultdict(list)
    for pair in _repair_pairs():
        grouped[pair.category].append(pair)
    return dict(sorted(grouped.items()))


def _records(target_per_family: int) -> list[dict[str, Any]]:
    grouped = _family_groups()
    iterators = {family: cycle(pairs) for family, pairs in grouped.items()}
    counts = {family: 0 for family in grouped}
    records: list[dict[str, Any]] = []
    idx = 77000
    while any(count < target_per_family for count in counts.values()):
        for family in grouped:
            if counts[family] >= target_per_family:
                continue
            idx += 1
            counts[family] += 1
            records.append(_conditioned_record(next(iterators[family]), idx))
    return records


def _write_samples(
    path: Path,
    rows_69: list[dict[str, Any]],
    rows_67: list[dict[str, Any]],
    rows_60: list[dict[str, Any]],
) -> None:
    lines = ["# Phase 27.77 V9 Bounded Open-Social LM Repair", ""]
    for title, rows in (
        ("Phase 27.69 new fresh shadow", rows_69),
        ("Phase 27.67 known shadow", rows_67),
        ("Phase 27.60 regression", rows_60),
    ):
        lines.extend([f"## {title}", ""])
        for row in rows:
            if row["passed"]:
                continue
            lines.extend(
                [
                    f"### {row['id']} — FAIL",
                    "",
                    f"- family: {row['family']}",
                    f"- prompt: {row['prompt']}",
                    f"- response: {row['response']}",
                    f"- guard_reason: {row.get('guard_reason')}",
                    f"- reason: {row['reason']}",
                    "",
                ]
            )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_doc(path: Path, report: dict[str, Any]) -> None:
    fresh = report["phase27_69_summary"]
    known = report["phase27_67_summary"]
    regression = report["phase27_60_summary"]
    lines = [
        "# Phase 27.77 — V9 Bounded Open-Social LM Repair",
        "",
        "## الخلاصة",
        "",
        "هذه مرحلة تدريب LM محدود على tokenizer v9. لا تفتح runtime تلقائيًا.",
        "",
        f"- status: `{report['status']}`",
        f"- tokenizer: `{report['tokenizer']}`",
        f"- checkpoint: `{report['checkpoint_root']}/{report['checkpoint_name']}`",
        f"- Phase 27.69 fresh: `{fresh['passed']}/{fresh['total']}`",
        f"- Phase 27.67 known: `{known['passed']}/{known['total']}`",
        f"- Phase 27.60 regression: `{regression['passed']}/{regression['total']}`",
        f"- runtime switch allowed: `{report['decisions']['runtime_switch_allowed']}`",
        "",
        "## القرار",
        "",
        report["decision"],
        "",
        "## التالي",
        "",
        report["next_phase"],
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    if not (args.tokenizer / "meta.json").exists():
        print(f"error: missing tokenizer at {args.tokenizer}", file=sys.stderr)
        return 1
    if not args.source_report.exists():
        print(f"error: missing source report at {args.source_report}", file=sys.stderr)
        return 1
    source = json.loads(args.source_report.read_text(encoding="utf-8"))
    if source["decisions"].get("tokenizer_v9_passed") is not True:
        print("error: Phase 27.76 tokenizer gate did not pass", file=sys.stderr)
        return 2

    if args.work_dir.exists() and not args.keep_work:
        shutil.rmtree(args.work_dir)
    corpus_dir = args.work_dir / "corpus"
    checkpoints = args.work_dir / "checkpoints"
    records = _records(args.target_per_family)
    _write_probe_corpus(corpus_dir, records)

    train_args = [
        "--tokenizer", str(args.tokenizer),
        "--corpus", str(corpus_dir),
        "--size", "sf-10m",
        "--steps", str(args.steps),
        "--epochs", str(args.epochs),
        "--batch-size", str(args.batch_size),
        "--seq-len", str(args.seq_len),
        "--stream-format", "dialogue",
        "--loss-scope", "assistant",
        "--packing-mode", "sample_isolated",
        "--lr", str(args.lr),
        "--warmup", str(args.warmup),
        "--min-lr", "1e-5",
        "--save-every", str(args.steps),
        "--seed", "20260705",
        "--checkpoints", str(checkpoints),
        "--device", args.device,
    ]
    train_code = train_tiny_lm_run(train_args)
    if train_code != 0:
        return train_code

    checkpoint_name = _latest_checkpoint_name(checkpoints)
    eval_args = argparse.Namespace(
        tokenizer=args.tokenizer,
        checkpoints=checkpoints,
        checkpoint_name=checkpoint_name,
        device=args.device,
    )
    rows_69 = evaluate_phase27_69(eval_args)
    rows_67 = evaluate_phase27_67(eval_args)
    rows_60 = evaluate_phase27_60(eval_args)
    summary_69 = summary_phase27_69(rows_69)
    summary_67 = summary_phase27_67(rows_67)
    summary_60 = summary_phase27_60(rows_60)
    all_gates = (
        summary_69["passed"] == summary_69["total"]
        and summary_67["passed"] == summary_67["total"]
        and summary_60["passed"] == summary_60["total"]
    )
    improved = (
        summary_69["passed"] >= 58
        and summary_67["passed"] >= 50
        and summary_60["passed"] >= 30
    )
    status = (
        "PASSED_V9_BOUNDED_OPEN_SOCIAL_LM_REPAIR_RUNTIME_REVIEW_ALLOWED"
        if all_gates
        else (
            "IMPROVED_V9_BOUNDED_OPEN_SOCIAL_LM_REPAIR_RUNTIME_BLOCKED"
            if improved
            else "FAILED_V9_BOUNDED_OPEN_SOCIAL_LM_REPAIR_RUNTIME_BLOCKED"
        )
    )
    report = {
        "phase": "Phase 27.77",
        "status": status,
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "training_started": True,
        "training_scope": "bounded SF-10M LM repair from scratch on tokenizer v9; no runtime switch; no SF-50M",
        "source_report": _rel(args.source_report),
        "tokenizer": _rel(args.tokenizer),
        "checkpoint_root": _rel(checkpoints),
        "checkpoint_name": checkpoint_name,
        "candidate_generator": "sf_10m_phase27_77_v9_bounded_open_social_lm_repair",
        "train_records": len(records),
        "repair_pair_count": len(_repair_pairs()),
        "target_per_family": args.target_per_family,
        "phase27_69_summary": summary_69,
        "phase27_67_summary": summary_67,
        "phase27_60_summary": summary_60,
        "phase27_69_rows": rows_69,
        "phase27_67_rows": rows_67,
        "phase27_60_rows": rows_60,
        "decisions": {
            "runtime_switch_allowed": False,
            "ui_open_allowed": False,
            "sf50m_allowed": False,
            "phase28_allowed": False,
            "live_runtime_review_allowed": all_gates,
            "repair_required_before_runtime": not all_gates,
        },
        "decision": (
            "The v9 bounded LM repair passed all offline gates. Runtime still requires a separate live review phase."
            if all_gates
            else "The v9 bounded LM repair did not pass all gates. Keep runtime blocked and inspect failures before any UI/runtime change."
        ),
        "next_phase": (
            "Phase 27.78 — guarded live review for Phase 27.77 candidate"
            if all_gates
            else "Phase 27.78 — inspect Phase 27.77 failures and revise v9 LM strategy"
        ),
        "torch_version": torch.__version__,
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _write_samples(args.samples, rows_69, rows_67, rows_60)
    _write_doc(args.doc, report)

    print("SF.AI — Phase 27.77 v9 bounded open_social LM repair")
    print(f"  status      : {status}")
    print(f"  checkpoint  : {checkpoint_name}")
    print(f"  phase27.69  : {summary_69['passed']}/{summary_69['total']}")
    print(f"  phase27.67  : {summary_67['passed']}/{summary_67['total']}")
    print(f"  phase27.60  : {summary_60['passed']}/{summary_60['total']}")
    print(f"  report      : {_rel(args.report)}")
    print("  runtime     : blocked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
