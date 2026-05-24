#!/usr/bin/env python3
"""Phase 27.66 bounded LM topic repair on tokenizer v8.

Phase 27.65 trained tokenizer v8 and restored protected topic terms such as
`التعاون` and `الاحترام` to single-piece tokens. This phase trains a bounded
SF-10M repair probe on that tokenizer, keeps the interleaved curriculum shape
from Phase 27.63, adds a small topic emphasis pack, and reruns the broader
natural-dialogue canary.

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


DEFAULT_TOKENIZER = ROOT / "artifacts/tokenizers/sf_bpe/v8_phase27_65"
DEFAULT_WORK = ROOT / "artifacts/eval/phase27_66_v8_bounded_topic_repair"
DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_66_v8_bounded_topic_repair_report.json"
DEFAULT_SAMPLES = ROOT / "artifacts/samples/phase27_66_v8_bounded_topic_repair.md"
DEFAULT_DOC = ROOT / "docs/PHASE27_66_V8_BOUNDED_TOPIC_REPAIR_REPORT.md"


TOPIC_EMPHASIS_REPAIR: tuple[RepairPair, ...] = (
    RepairPair("msa", "ما المقصود بالتعاون", "التعاون مشاركة الجهد بين الناس.", ("التعاون",), "topic"),
    RepairPair("saudi", "التعاون وش يعني", "التعاون يعني نساعد بعض وننجز سوا.", ("التعاون",), "topic"),
    RepairPair("msa", "عرّف التعاون ببساطة", "التعاون أن يعمل الناس معًا لهدف واضح.", ("التعاون",), "topic"),
    RepairPair("saudi", "وش معنى التعاون باختصار", "التعاون إنك تساعد غيرك وتنجزون سوا.", ("التعاون",), "topic"),
    RepairPair("msa", "ما المقصود بالاحترام", "الاحترام تقدير الناس بالكلام والتصرف.", ("الاحترام",), "topic"),
    RepairPair("saudi", "الاحترام وش معناه", "الاحترام يعني تقدّر الناس بقولك وفعلك.", ("الاحترام",), "topic"),
    RepairPair("msa", "عرّف الاحترام ببساطة", "الاحترام معاملة الناس بذوق وتقدير.", ("الاحترام",), "topic"),
    RepairPair("saudi", "وش معنى الاحترام باختصار", "الاحترام إن كلامك وتصرفك يكون فيه تقدير.", ("الاحترام",), "topic"),
)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run Phase 27.66 bounded LM topic repair on tokenizer v8")
    p.add_argument("--tokenizer", type=Path, default=DEFAULT_TOKENIZER)
    p.add_argument("--steps", type=int, default=6200)
    p.add_argument("--epochs", type=int, default=620)
    p.add_argument("--batch-size", type=int, default=1)
    p.add_argument("--seq-len", type=int, default=80)
    p.add_argument("--lr", type=float, default=4e-4)
    p.add_argument("--warmup", type=int, default=180)
    p.add_argument("--target-per-family", type=int, default=950)
    p.add_argument("--device", default="auto")
    p.add_argument("--work-dir", type=Path, default=DEFAULT_WORK)
    p.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    p.add_argument("--samples", type=Path, default=DEFAULT_SAMPLES)
    p.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    p.add_argument("--keep-work", action="store_true")
    return p.parse_args()


def _repair_pairs() -> tuple[RepairPair, ...]:
    return (*FAMILY_BALANCE_REPAIR, *TOPIC_EMPHASIS_REPAIR)


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
    idx = 66000
    while any(count < target_per_family for count in counts.values()):
        for family in grouped:
            if counts[family] >= target_per_family:
                continue
            idx += 1
            counts[family] += 1
            records.append(_conditioned_record(next(iterators[family]), idx))
    return records


def _write_samples(path: Path, rows: list[dict[str, Any]]) -> None:
    lines = ["# Phase 27.66 V8 Bounded Topic Repair", ""]
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
        "# Phase 27.66 — V8 Bounded Topic Repair",
        "",
        "## الخلاصة",
        "",
        "هذه مرحلة تدريب LM محدودة على tokenizer v8. لا تفتح الواجهة ولا تغيّر runtime.",
        "",
        f"- status: `{report['status']}`",
        f"- tokenizer: `{report['tokenizer']}`",
        f"- checkpoint: `{report['checkpoint_root']}/{report['checkpoint_name']}`",
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
        "--seed", "20260630",
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
    improved = summary["passed"] > 26
    status = (
        "PASSED_V8_BOUNDED_TOPIC_REPAIR_READY_FOR_FRESH_SHADOW_CANARY_RUNTIME_BLOCKED"
        if passed
        else (
            "IMPROVED_V8_BOUNDED_TOPIC_REPAIR_RUNTIME_BLOCKED"
            if improved
            else "COMPLETED_V8_BOUNDED_TOPIC_REPAIR_RUNTIME_BLOCKED"
        )
    )
    report = {
        "phase": "Phase 27.66",
        "status": status,
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "training_started": True,
        "training_scope": "bounded SF-10M LM repair on tokenizer v8 only; no runtime switch; no SF-50M",
        "tokenizer": _rel(args.tokenizer),
        "checkpoint_root": _rel(checkpoints),
        "checkpoint_name": checkpoint_name,
        "candidate_generator": "sf_10m_phase27_66_v8_bounded_topic_repair",
        "train_records": len(records),
        "repair_pair_count": len(_repair_pairs()),
        "topic_emphasis_pair_count": len(TOPIC_EMPHASIS_REPAIR),
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
            "Tokenizer v8 bounded repair passed the broader canary. Keep runtime blocked and run a fresh shadow canary next."
            if passed
            else "Tokenizer v8 bounded repair did not pass every broader canary item. Keep runtime blocked and inspect failures."
        ),
        "next_phase": (
            "Phase 27.67 — fresh shadow canary with unseen natural prompts"
            if passed
            else "Phase 27.67 — inspect Phase 27.66 failures before any runtime change"
        ),
        "torch_version": torch.__version__,
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _write_samples(args.samples, rows)
    _write_doc(report, args.doc)

    print("SF.AI — Phase 27.66 v8 bounded topic repair")
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
