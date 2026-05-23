#!/usr/bin/env python3
"""Phase 27.19 hygiene repair probe.

This extends the Phase 27.17 prompt-answer micro-corpus with focused repair
examples for the five phrases flagged by the Phase 27.18 hygiene audit.
It remains an internal artifacts/eval probe, not general corpus expansion.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.phase27_17_prompt_answer_micro_probe import (
    MSA_PAIRS,
    SAUDI_PAIRS,
    _evaluate,
    _latest_checkpoint_name,
    _record,
)
from sf_ai.training.train_tiny_lm import run as train_tiny_lm_run


DEFAULT_WORK = ROOT / "artifacts/eval/phase27_19_hygiene_repair_probe"
DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_19_hygiene_repair_probe_report.json"
DEFAULT_SAMPLES = ROOT / "artifacts/samples/phase27_19_hygiene_repair_probe_generations.md"


REPAIR_MSA: tuple[tuple[str, str, tuple[str, ...]], ...] = (
    ("رد السلام باختصار", "وعليكم السلام، أهلًا بك.", ("وعليكم", "أهلًا")),
    ("إذا قلت السلام عليكم فبماذا ترد", "وعليكم السلام، أهلًا بك.", ("وعليكم", "أهلًا")),
    ("اكتب تحية رد مناسبة", "وعليكم السلام، أهلًا بك.", ("وعليكم", "أهلًا")),
    ("أحتاج تهدئة قصيرة", "خذ نفسًا هادئًا وابدأ بالأهم.", ("نفسًا", "هادئًا")),
    ("كيف أهدأ الآن", "خذ نفسًا هادئًا وابدأ بالأهم.", ("نفسًا", "هادئًا")),
    ("اشرح التعاون ببساطة", "التعاون يعني أن ننجز معًا بدل الانفراد.", ("التعاون", "معًا")),
    ("ما المقصود بالتعاون", "التعاون يعني أن ننجز معًا بدل الانفراد.", ("التعاون", "معًا")),
    ("ما فائدة القراءة بجملة", "القراءة تفيد لأنها توسع الفهم.", ("القراءة", "تفيد")),
    ("القراءة تفيد في ماذا", "القراءة تفيد في توسيع الفهم.", ("القراءة", "تفيد")),
    ("كيف أحترم الناس", "تقدّر الناس بكلامك وتصرفك.", ("تقدّر", "الناس")),
)


REPAIR_SAUDI: tuple[tuple[str, str, tuple[str, ...]], ...] = (
    ("رد على السلام", "وعليكم السلام، هلا بك.", ("وعليكم", "هلا")),
    ("وش ارد على السلام عليكم", "وعليكم السلام، هلا بك.", ("وعليكم", "هلا")),
    ("ابي ارد على واحد سلم", "وعليكم السلام، هلا بك.", ("وعليكم", "هلا")),
    ("ابي اهدأ شوي", "خذ نفس هادي وابدأ بالأهم.", ("نفس", "هادي")),
    ("وش اسوي اذا توترت", "خذ نفس هادي وابدأ بالأهم.", ("نفس", "هادي")),
    ("وش يعني تعاون", "يعني نشتغل سوا ونخفف الحمل.", ("نشتغل", "سوا")),
    ("اشرح التعاون بالسعودي", "يعني نشتغل سوا ونخفف الحمل.", ("نشتغل", "سوا")),
    ("القراءة وش تفيد", "القراءة تفيد وتوسع فهمك.", ("القراءة", "تفيد")),
    ("وش فايدة القراءة", "القراءة تفيد وتزيد كلماتك.", ("القراءة", "تفيد")),
    ("كيف اقدر الناس", "تقدّر الناس بكلامك وتصرفك.", ("تقدّر", "الناس")),
)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run Phase 27.19 hygiene repair probe")
    p.add_argument("--steps", type=int, default=3200)
    p.add_argument("--epochs", type=int, default=320)
    p.add_argument("--batch-size", type=int, default=1)
    p.add_argument("--seq-len", type=int, default=64)
    p.add_argument("--lr", type=float, default=8e-4)
    p.add_argument("--warmup", type=int, default=100)
    p.add_argument("--device", default="auto")
    p.add_argument("--work-dir", type=Path, default=DEFAULT_WORK)
    p.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    p.add_argument("--samples", type=Path, default=DEFAULT_SAMPLES)
    p.add_argument("--keep-work", action="store_true")
    return p.parse_args()


def _records() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    base: list[dict[str, Any]] = []
    train: list[dict[str, Any]] = []
    for idx, (prompt, answer, terms) in enumerate(MSA_PAIRS, start=1):
        row = _record("msa", idx, prompt, answer, terms)
        base.append(row)
        train.append(row)
    for idx, (prompt, answer, terms) in enumerate(SAUDI_PAIRS, start=1):
        row = _record("saudi", idx, prompt, answer, terms)
        base.append(row)
        train.append(row)
    for idx, (prompt, answer, terms) in enumerate(REPAIR_MSA, start=1):
        train.append(_record("msa", 100 + idx, prompt, answer, terms))
    for idx, (prompt, answer, terms) in enumerate(REPAIR_SAUDI, start=1):
        train.append(_record("saudi", 100 + idx, prompt, answer, terms))
    return train, base


def _write_probe_corpus(corpus_dir: Path, records: list[dict[str, Any]]) -> Path:
    corpus_dir.mkdir(parents=True, exist_ok=True)
    out = corpus_dir / "phase27_19_hygiene_repair_probe.jsonl"
    out.write_text(
        "\n".join(json.dumps(record, ensure_ascii=False) for record in records) + "\n",
        encoding="utf-8",
    )
    return out


def _write_samples(path: Path, results: list[dict[str, Any]]) -> None:
    lines = ["# Phase 27.19 Hygiene Repair Probe Generations", ""]
    for item in results:
        lines.extend(
            [
                f"## {item['id']} — {item['dialect']} — {'PASS' if item['passed'] else 'FAIL'}",
                "",
                f"- prompt: {item['prompt']}",
                f"- expected: {item['expected']}",
                f"- generated: {item['generated']}",
                f"- exact_clean: {item['exact_clean']}",
                f"- semantic_match: {item['semantic_match']}",
                f"- reason: {item['reason']}",
                "",
            ]
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    args = parse_args()
    train_records, eval_records = _records()
    if args.work_dir.exists() and not args.keep_work:
        shutil.rmtree(args.work_dir)
    corpus_dir = args.work_dir / "corpus"
    checkpoints = args.work_dir / "checkpoints"
    _write_probe_corpus(corpus_dir, train_records)

    train_args = [
        "--tokenizer", str(ROOT / "artifacts/tokenizers/sf_bpe/v2"),
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
        "--seed", "20260526",
        "--checkpoints", str(checkpoints),
        "--device", args.device,
    ]
    train_code = train_tiny_lm_run(train_args)
    if train_code != 0:
        return train_code

    checkpoint_name = _latest_checkpoint_name(checkpoints)
    results, reasons = _evaluate(
        records=eval_records,
        checkpoints_root=checkpoints,
        checkpoint_name=checkpoint_name,
        device=args.device,
    )
    total = len(results)
    passed = sum(1 for item in results if item["passed"])
    exact = sum(1 for item in results if item["exact_clean"])
    semantic = sum(1 for item in results if item["semantic_match"])
    guard = sum(1 for item in results if item["guard_reason"] == "passed")
    status = (
        "PASSED_HYGIENE_REPAIR_PROBE"
        if passed == total
        else "FAILED_HYGIENE_REPAIR_PROBE_BLOCK_RUNTIME"
    )
    report = {
        "phase": "Phase 27.19",
        "status": status,
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "train_records": len(train_records),
        "eval_records": total,
        "repair_records": len(train_records) - total,
        "repair_focus_terms": [
            "وعليكم السلام",
            "نفسًا هادئًا",
            "نشتغل سوا",
            "القراءة تفيد",
            "تقدّر الناس",
        ],
        "training": {
            "steps": args.steps,
            "epochs": args.epochs,
            "batch_size": args.batch_size,
            "seq_len": args.seq_len,
            "lr": args.lr,
            "packing_mode": "sample_isolated",
            "checkpoint_name": checkpoint_name,
        },
        "passed": passed,
        "failed": total - passed,
        "pass_rate": round(passed / total, 4) if total else 0.0,
        "exact_clean": exact,
        "semantic_match": semantic,
        "guard_passed": guard,
        "reason_counts": dict(Counter(reasons)),
        "runtime_allowed": False,
        "sf50m_allowed": False,
        "decision": (
            "Do not enable runtime or SF-50M until repair probe and broader canary pass."
            if passed != total
            else "Repair probe passed on original 32 prompts; next run a held-out hygiene canary before runtime."
        ),
        "results": results,
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _write_samples(args.samples, results)

    print("SF.AI — Phase 27.19 hygiene repair probe")
    print(f"  status       : {status}")
    print(f"  checkpoint   : {checkpoint_name}")
    print(f"  train        : {len(train_records)}")
    print(f"  eval         : {total}")
    print(f"  passed       : {passed}/{total}")
    print(f"  exact_clean  : {exact}/{total}")
    print(f"  semantic     : {semantic}/{total}")
    print(f"  guard_passed : {guard}/{total}")
    print(f"  reasons      : {dict(reasons)}")
    print(f"  report       : {args.report}")
    print(f"  samples      : {args.samples}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
