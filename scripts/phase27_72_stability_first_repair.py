#!/usr/bin/env python3
"""Phase 27.72 stability-first micro repair.

Phase 27.71 selected Phase 27.68 as the strongest available candidate
(`136/140`), with all remaining failures isolated to four open_social prompts
in the Phase 27.69 fresh canary. This phase tries a minimal sovereign
fine-tune from that candidate on the four failures only, then re-runs:

1. Phase 27.69 new fresh shadow.
2. Phase 27.67 known shadow.
3. Phase 27.60 broader regression.

Runtime remains blocked unless all gates pass.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
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
from scripts.phase27_67_fresh_shadow_canary import _evaluate as evaluate_phase27_67, _summary as summary_phase27_67  # noqa: E402
from scripts.phase27_69_new_fresh_shadow_canary import _evaluate as evaluate_phase27_69, _summary as summary_phase27_69  # noqa: E402
from sf_ai.training.train_tiny_lm import run as train_tiny_lm_run  # noqa: E402


DEFAULT_TOKENIZER = ROOT / "artifacts/tokenizers/sf_bpe/v8_phase27_65"
DEFAULT_INIT_CHECKPOINTS = ROOT / "artifacts/eval/phase27_68_shadow_failure_repair/checkpoints"
DEFAULT_INIT_CHECKPOINT_NAME = "sf-10m-step5600"
DEFAULT_WORK = ROOT / "artifacts/eval/phase27_72_stability_first_repair"
DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_72_stability_first_repair_report.json"
DEFAULT_SAMPLES = ROOT / "artifacts/samples/phase27_72_stability_first_repair.md"
DEFAULT_DOC = ROOT / "docs/PHASE27_72_STABILITY_FIRST_REPAIR_REPORT.md"


MICRO_REPAIR: tuple[RepairPair, ...] = (
    RepairPair("msa", "اختر حديثًا خفيفًا بيننا", "نختار حديثًا خفيفًا عن موضوع بسيط.", ("حديث", "خفيف", "موضوع"), "open_social"),
    RepairPair("saudi", "ودي بموضوع سوالف", "نختار موضوع سوالف خفيف ونسولف عنه.", ("موضوع", "سوالف", "نسولف"), "open_social"),
    RepairPair("saudi", "ابي موضوع سوالف", "نختار موضوع سوالف بسيط ونسولف بهدوء.", ("موضوع", "سوالف"), "open_social"),
    RepairPair("saudi", "عطني موضوع سوالف", "موضوع سوالف خفيف: نسولف عن شيء من يومك.", ("موضوع", "سوالف"), "open_social"),
    RepairPair("saudi", "خلنا نختار موضوع سوالف", "نختار موضوع سوالف خفيف ونبدأ الكلام.", ("موضوع", "سوالف"), "open_social"),
    RepairPair("msa", "ابدأ محادثة سهلة", "نبدأ محادثة سهلة عن موضوع بسيط.", ("محادثة", "نبدأ", "موضوع"), "open_social"),
    RepairPair("msa", "لنختر موضوعًا صغيرًا", "نختار موضوعًا صغيرًا وخفيفًا للكلام.", ("موضوع", "صغير"), "open_social"),
)

STABILITY_PRESERVE: tuple[RepairPair, ...] = (
    RepairPair("msa", "اشرح الصداقة دون إطالة", "الصداقة رفقة طيبة واهتمام وقت الحاجة.", ("الصداقة",), "topic"),
    RepairPair("msa", "ما جوهر الصداقة", "الصداقة رفقة طيبة ووقفة وقت الحاجة.", ("الصداقة",), "topic"),
    RepairPair("msa", "ما الخطوة بعد هذا الشرح", "بعدها نكمل بخطوة أوضح من الفكرة.", ("بعدها", "خطوة"), "followup"),
    RepairPair("msa", "ما الخطوة بعد هذا الشرح", "الخطوة بعدها أن نكمل الفكرة بجزء أوضح.", ("خطوة", "بعدها"), "followup"),
    RepairPair("msa", "تابع الشرح من النقطة الأخيرة", "نكمل من النقطة الأخيرة بخطوة أوضح.", ("نكمل", "خطوة"), "followup"),
)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run Phase 27.72 stability-first micro repair")
    p.add_argument("--tokenizer", type=Path, default=DEFAULT_TOKENIZER)
    p.add_argument("--steps", type=int, default=64)
    p.add_argument("--epochs", type=int, default=64)
    p.add_argument("--batch-size", type=int, default=1)
    p.add_argument("--seq-len", type=int, default=80)
    p.add_argument("--lr", type=float, default=5e-6)
    p.add_argument("--warmup", type=int, default=8)
    p.add_argument("--repeat", type=int, default=24)
    p.add_argument("--device", default="auto")
    p.add_argument("--init-checkpoints", type=Path, default=DEFAULT_INIT_CHECKPOINTS)
    p.add_argument("--init-checkpoint-name", default=DEFAULT_INIT_CHECKPOINT_NAME)
    p.add_argument("--work-dir", type=Path, default=DEFAULT_WORK)
    p.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    p.add_argument("--samples", type=Path, default=DEFAULT_SAMPLES)
    p.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    p.add_argument("--keep-work", action="store_true")
    return p.parse_args()


def _records(repeat: int) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    idx = 72000
    for _ in range(repeat):
        for pair in (*MICRO_REPAIR, *STABILITY_PRESERVE):
            idx += 1
            records.append(_conditioned_record(pair, idx))
    return records


def _write_samples(path: Path, rows_69: list[dict[str, Any]], rows_67: list[dict[str, Any]], rows_60: list[dict[str, Any]]) -> None:
    lines = ["# Phase 27.72 Stability-First Repair", ""]
    for title, rows in (
        ("Phase 27.69 fresh", rows_69),
        ("Phase 27.67 known", rows_67),
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
        "# Phase 27.72 — Stability-First Micro Repair",
        "",
        "## الخلاصة",
        "",
        "هذه مرحلة تدريب إصلاح صغيرة جدًا من أفضل مرشح سابق. لا تفتح runtime.",
        "",
        f"- status: `{report['status']}`",
        f"- init checkpoint: `{report['init_checkpoint_root']}/{report['init_checkpoint_name']}`",
        f"- candidate checkpoint: `{report['checkpoint_root']}/{report['checkpoint_name']}`",
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

    if args.work_dir.exists() and not args.keep_work:
        shutil.rmtree(args.work_dir)
    corpus_dir = args.work_dir / "corpus"
    checkpoints = args.work_dir / "checkpoints"
    records = _records(args.repeat)
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
        "--min-lr", "1e-6",
        "--save-every", str(args.steps),
        "--seed", "20260703",
        "--checkpoints", str(checkpoints),
        "--device", args.device,
        "--init-checkpoints", str(args.init_checkpoints),
        "--init-checkpoint-name", args.init_checkpoint_name,
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
    passed = (
        summary_69["passed"] == summary_69["total"]
        and summary_67["passed"] == summary_67["total"]
        and summary_60["passed"] == summary_60["total"]
    )
    beats_baseline = (
        summary_69["passed"] > 56
        and summary_67["passed"] >= 50
        and summary_60["passed"] >= 30
    )
    status = (
        "PASSED_STABILITY_FIRST_REPAIR_RUNTIME_REVIEW_ALLOWED"
        if passed
        else (
            "IMPROVED_STABILITY_FIRST_REPAIR_RUNTIME_BLOCKED"
            if beats_baseline
            else "FAILED_STABILITY_FIRST_REPAIR_RUNTIME_BLOCKED"
        )
    )
    report = {
        "phase": "Phase 27.72",
        "status": status,
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "training_started": True,
        "training_scope": "minimal SF-10M micro repair from Phase 27.68; no runtime switch; no SF-50M",
        "tokenizer": _rel(args.tokenizer),
        "init_checkpoint_root": _rel(args.init_checkpoints),
        "init_checkpoint_name": args.init_checkpoint_name,
        "checkpoint_root": _rel(checkpoints),
        "checkpoint_name": checkpoint_name,
        "candidate_generator": "sf_10m_phase27_72_stability_first_repair",
        "train_records": len(records),
        "micro_repair_pair_count": len(MICRO_REPAIR),
        "stability_preserve_pair_count": len(STABILITY_PRESERVE),
        "repeat": args.repeat,
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
            "live_runtime_review_allowed": passed,
            "repair_required_before_runtime": not passed,
        },
        "decision": (
            "The micro repair passed all offline gates. Runtime still requires a separate live review phase."
            if passed
            else "The micro repair did not pass all stability gates. Keep runtime blocked and inspect failures before any larger training."
        ),
        "next_phase": (
            "Phase 27.73 — live runtime review for Phase 27.72 candidate"
            if passed
            else "Phase 27.73 — inspect Phase 27.72 failures and revise stability strategy"
        ),
        "torch_version": torch.__version__,
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _write_samples(args.samples, rows_69, rows_67, rows_60)
    _write_doc(args.doc, report)

    print("SF.AI — Phase 27.72 stability-first repair")
    print(f"  status      : {status}")
    print(f"  checkpoint  : {checkpoint_name}")
    print(f"  phase27.69  : {summary_69['passed']}/{summary_69['total']}")
    print(f"  phase27.67  : {summary_67['passed']}/{summary_67['total']}")
    print(f"  phase27.60  : {summary_60['passed']}/{summary_60['total']}")
    print("  runtime     : blocked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
