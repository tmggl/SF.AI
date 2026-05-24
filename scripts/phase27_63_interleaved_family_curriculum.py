#!/usr/bin/env python3
"""Phase 27.63 interleaved response-family curriculum.

Phase 27.62 proved that family balance by count is not enough when records are
written in family blocks: the final training window drifted toward open_social.
This phase keeps the same sovereign repair data but writes records in a strict
round-robin order across families, lowers the learning rate, and uses fewer
steps to reduce overfit/malformed-token collapse.

Runtime remains blocked regardless of the result.
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
from scripts.phase27_60_broader_natural_dialogue_canary import CANARY_CASES, _evaluate, _summary  # noqa: E402
from scripts.phase27_62_family_balance_repair import FAMILY_BALANCE_REPAIR  # noqa: E402
from sf_ai.training.train_tiny_lm import run as train_tiny_lm_run  # noqa: E402


DEFAULT_TOKENIZER = ROOT / "artifacts/tokenizers/sf_bpe/v7_phase27_58"
DEFAULT_WORK = ROOT / "artifacts/eval/phase27_63_interleaved_family_curriculum"
DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_63_interleaved_family_curriculum_report.json"
DEFAULT_SAMPLES = ROOT / "artifacts/samples/phase27_63_interleaved_family_curriculum.md"
DEFAULT_DOC = ROOT / "docs/PHASE27_63_INTERLEAVED_FAMILY_CURRICULUM_REPORT.md"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run Phase 27.63 interleaved family curriculum")
    p.add_argument("--tokenizer", type=Path, default=DEFAULT_TOKENIZER)
    p.add_argument("--steps", type=int, default=5600)
    p.add_argument("--epochs", type=int, default=560)
    p.add_argument("--batch-size", type=int, default=1)
    p.add_argument("--seq-len", type=int, default=80)
    p.add_argument("--lr", type=float, default=4e-4)
    p.add_argument("--warmup", type=int, default=160)
    p.add_argument("--target-per-family", type=int, default=900)
    p.add_argument("--device", default="auto")
    p.add_argument("--work-dir", type=Path, default=DEFAULT_WORK)
    p.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    p.add_argument("--samples", type=Path, default=DEFAULT_SAMPLES)
    p.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    p.add_argument("--keep-work", action="store_true")
    return p.parse_args()


def _family_groups() -> dict[str, list[RepairPair]]:
    grouped: dict[str, list[RepairPair]] = defaultdict(list)
    for pair in FAMILY_BALANCE_REPAIR:
        grouped[pair.category].append(pair)
    return dict(sorted(grouped.items()))


def _records(target_per_family: int) -> list[dict[str, Any]]:
    grouped = _family_groups()
    iterators = {family: cycle(pairs) for family, pairs in grouped.items()}
    counts = {family: 0 for family in grouped}
    records: list[dict[str, Any]] = []
    idx = 63000
    while any(count < target_per_family for count in counts.values()):
        for family in grouped:
            if counts[family] >= target_per_family:
                continue
            idx += 1
            counts[family] += 1
            records.append(_conditioned_record(next(iterators[family]), idx))
    return records


def _write_samples(path: Path, rows: list[dict[str, Any]]) -> None:
    lines = ["# Phase 27.63 Interleaved Family Curriculum", ""]
    for row in rows:
        lines.extend(
            [
                f"## {row['id']} — {'PASS' if row['passed'] else 'FAIL'}",
                "",
                f"- family: {row['family']}",
                f"- prompt: {row['prompt']}",
                f"- response: {row['response']}",
                f"- guard_reason: {row['guard_reason']}",
                f"- expected_ok: {row['expected_ok']}",
                f"- family_ok: {row['family_ok']}",
                f"- reason: {row['reason']}",
                "",
            ]
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_doc(report: dict[str, Any], path: Path) -> None:
    summary = report["summary"]
    lines = [
        "# Phase 27.63 — Interleaved Family Curriculum",
        "",
        "## الخلاصة",
        "",
        "هذه مرحلة إصلاح ترتيب curriculum بعد فشل Phase 27.62. لا تفتح الواجهة.",
        "",
        f"- status: `{report['status']}`",
        f"- canary pass: `{summary['passed']}/{summary['total']}`",
        f"- runtime switch allowed: `{report['decisions']['runtime_switch_allowed']}`",
        "",
        "## family summary",
        "",
    ]
    for family, item in summary["family_summary"].items():
        lines.append(f"- `{family}`: `{item['passed']}/{item['total']}`")
    lines.extend(["", "## القرار", "", report["decision"], "", "## التالي", "", report["next_phase"]])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    if not (args.tokenizer / "meta.json").exists():
        print(f"error: missing tokenizer at {args.tokenizer}", file=sys.stderr)
        return 1

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
        "--seed", "20260628",
        "--checkpoints", str(checkpoints),
        "--device", args.device,
    ]
    train_code = train_tiny_lm_run(train_args)
    if train_code != 0:
        return train_code

    checkpoint_name = _latest_checkpoint_name(checkpoints)
    rows = _evaluate(
        argparse.Namespace(
            tokenizer=args.tokenizer,
            checkpoints=checkpoints,
            checkpoint_name=checkpoint_name,
            device=args.device,
        )
    )
    summary = _summary(rows)
    passed = summary["passed"] == summary["total"]
    recovered = summary["passed"] > 18
    status = (
        "PASSED_INTERLEAVED_FAMILY_CURRICULUM_READY_FOR_FRESH_SHADOW_CANARY_RUNTIME_BLOCKED"
        if passed
        else (
            "IMPROVED_INTERLEAVED_FAMILY_CURRICULUM_RUNTIME_BLOCKED"
            if recovered
            else "FAILED_INTERLEAVED_FAMILY_CURRICULUM_RUNTIME_BLOCKED"
        )
    )
    report = {
        "phase": "Phase 27.63",
        "status": status,
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "training_started": True,
        "training_scope": "bounded SF-10M interleaved family curriculum only; no runtime switch; no SF-50M",
        "tokenizer": _rel(args.tokenizer),
        "checkpoint_root": _rel(checkpoints),
        "checkpoint_name": checkpoint_name,
        "candidate_generator": "sf_10m_phase27_63_interleaved_family_curriculum",
        "train_records": len(records),
        "repair_pair_count": len(FAMILY_BALANCE_REPAIR),
        "target_per_family": args.target_per_family,
        "canary_cases": len(CANARY_CASES),
        "summary": summary,
        "rows": rows,
        "decisions": {
            "runtime_switch_allowed": False,
            "ui_open_allowed": False,
            "sf50m_allowed": False,
            "phase28_allowed": False,
            "fresh_shadow_canary_allowed": passed,
        },
        "decision": (
            "Interleaved curriculum passed the existing broader canary. Keep runtime blocked and run a fresh shadow canary next."
            if passed
            else "Interleaved curriculum did not pass. Keep runtime blocked and inspect remaining family failures."
        ),
        "next_phase": (
            "Phase 27.64 — fresh shadow canary with unseen natural prompts"
            if passed
            else "Phase 27.64 — inspect Phase 27.63 failures and revise objective/curriculum"
        ),
        "torch_version": torch.__version__,
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _write_samples(args.samples, rows)
    _write_doc(report, args.doc)

    print("SF.AI — Phase 27.63 interleaved family curriculum")
    print(f"  status      : {status}")
    print(f"  checkpoint  : {checkpoint_name}")
    print(f"  canary      : {summary['passed']}/{summary['total']}")
    print(f"  family      : {summary['family_summary']}")
    print(f"  report      : {_rel(args.report)}")
    print(f"  samples     : {_rel(args.samples)}")
    print("  runtime     : blocked")
    return 0 if args.report.exists() else 1


if __name__ == "__main__":
    raise SystemExit(main())
