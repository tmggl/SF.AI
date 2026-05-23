#!/usr/bin/env python3
"""Phase 27.46 core dialogue stabilization.

The broader Phase 27.45 curriculum over-corrected and mixed concepts. This
phase narrows the goal: prove the native SF-10M generator can reliably produce
a small, useful MSA/Saudi dialogue nucleus before any broader expansion.
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
from scripts.phase27_43_guarded_data_backed_expansion import (  # noqa: E402
    PROBE_CASES,
    _evaluate,
    _summary,
    _write_samples,
)
from sf_ai.training.train_tiny_lm import run as train_tiny_lm_run  # noqa: E402


DEFAULT_TOKENIZER = ROOT / "artifacts/tokenizers/sf_bpe/v6_weak_lane_terms"
DEFAULT_WORK = ROOT / "artifacts/eval/phase27_46_core_dialogue_stabilization"
DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_46_core_dialogue_stabilization_report.json"
DEFAULT_SAMPLES = ROOT / "artifacts/samples/phase27_46_core_dialogue_stabilization.md"


CORE_DIALOGUE_REPAIR: tuple[RepairPair, ...] = (
    RepairPair("saudi", "وش اخبارك", "بخير ولله الحمد، وش أخبارك أنت؟", ("بخير",), "smalltalk"),
    RepairPair("saudi", "علومك", "بخير ولله الحمد. وش ودك نسولف عنه؟", ("بخير",), "smalltalk"),
    RepairPair("saudi", "كيفك اليوم", "بخير ولله الحمد، أنت كيفك؟", ("بخير",), "smalltalk"),
    RepairPair("msa", "كيف حالك اليوم", "بخير، شكرًا لسؤالك.", ("بخير",), "smalltalk"),
    RepairPair("msa", "مشكور", "العفو، حاضر بأي وقت.", ("العفو",), "thanks"),
    RepairPair("msa", "تسلم", "العفو، يسعدني أساعدك.", ("العفو",), "thanks"),
    RepairPair("saudi", "يعطيك العافية", "الله يعافيك، حاضر بأي وقت.", ("يعافيك",), "thanks"),
    RepairPair("msa", "نظم وقتي", "اكتب ثلاث مهام وابدأ بالأهم.", ("مهام", "الأهم"), "planning"),
    RepairPair("msa", "كيف ارتب مهامي", "اكتب ثلاث مهام وابدأ بالأهم.", ("مهام", "الأهم"), "planning"),
    RepairPair("saudi", "ابي ارتب اولوياتي", "ابدأ بالأهم ثم انتقل للي بعده.", ("ابدأ", "الأهم"), "planning"),
    RepairPair("msa", "رتب أولوياتي", "اكتب أولوياتك ثم ابدأ بالأهم.", ("أولويات", "الأهم"), "planning"),
    RepairPair("msa", "انصحني ببداية بسيطة", "ابدأ بخطوة صغيرة وواضحة.", ("ابدأ",), "advice"),
    RepairPair("msa", "دلني على خطوة بسيطة", "ابدأ بخطوة صغيرة وواضحة.", ("ابدأ",), "advice"),
    RepairPair("saudi", "وش تنصحني اسوي", "ابدأ بشي بسيط وواضح.", ("ابدأ",), "advice"),
    RepairPair("msa", "انا متوتر", "خذ نفسًا هادئًا واهدأ خطوة خطوة.", ("نفس", "اهدأ"), "support"),
    RepairPair("saudi", "توترت شوي وش اسوي", "خذ نفسًا هادئًا واهدأ خطوة خطوة.", ("نفس", "اهدأ"), "support"),
    RepairPair("msa", "ما معنى الوفاء", "الوفاء أن تحفظ الود وتثبت مع من تثق به.", ("الوفاء",), "definition"),
    RepairPair("saudi", "الوفاء وش يعني", "الوفاء إنك تحفظ المعروف وتوقف مع اللي تثق فيه.", ("الوفاء",), "definition"),
    RepairPair("msa", "اشرح الشجاعة", "الشجاعة أن تفعل الصواب رغم الخوف.", ("الشجاعة",), "definition"),
    RepairPair("msa", "ما معنى الشجاعة", "الشجاعة ثبات على الصواب وقت الخوف.", ("الشجاعة",), "definition"),
    RepairPair("msa", "ما معنى الصداقة", "الصداقة علاقة طيبة تقوم على الوفاء.", ("الصداقة",), "definition"),
    RepairPair("saudi", "الصداقة وش تعني", "الصداقة رفقة طيبة ووقفة وقت الحاجة.", ("الصداقة",), "definition"),
    RepairPair("saudi", "الصدق وش يعني", "الصدق يعني تقول الحقيقة بوضوح.", ("الصدق",), "definition"),
    RepairPair("msa", "ما معنى الصدق", "الصدق أن تقول الحقيقة وتلتزم بما تقول.", ("الصدق",), "definition"),
    RepairPair("msa", "ما معنى التنظيم", "التنظيم ترتيب الوقت والمهام بطريقة واضحة.", ("التنظيم",), "definition"),
    RepairPair("saudi", "التنظيم وش يعني", "التنظيم يعني تخلي أمورك مرتبة.", ("التنظيم",), "definition"),
    RepairPair("saudi", "الهدوء وش يعني", "الهدوء يعني تخفف توترك وتتكلم بروية.", ("الهدوء",), "definition"),
    RepairPair("msa", "ما معنى الهدوء", "الهدوء سكينة تساعدك على التفكير بوضوح.", ("الهدوء",), "definition"),
)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run Phase 27.46 core dialogue stabilization")
    p.add_argument("--tokenizer", type=Path, default=DEFAULT_TOKENIZER)
    p.add_argument("--steps", type=int, default=4200)
    p.add_argument("--epochs", type=int, default=420)
    p.add_argument("--batch-size", type=int, default=1)
    p.add_argument("--seq-len", type=int, default=64)
    p.add_argument("--lr", type=float, default=6e-4)
    p.add_argument("--warmup", type=int, default=100)
    p.add_argument("--device", default="auto")
    p.add_argument("--work-dir", type=Path, default=DEFAULT_WORK)
    p.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    p.add_argument("--samples", type=Path, default=DEFAULT_SAMPLES)
    p.add_argument("--keep-work", action="store_true")
    return p.parse_args()


def _records() -> list[dict[str, Any]]:
    seed = [
        _conditioned_record(pair, 46000 + idx)
        for idx, pair in enumerate(CORE_DIALOGUE_REPAIR, start=1)
    ]
    records: list[dict[str, Any]] = []
    for _ in range(180):
        records.extend(seed)
    return records


def main() -> int:
    args = parse_args()
    if not (args.tokenizer / "meta.json").exists():
        print(f"error: missing tokenizer at {args.tokenizer}; run Phase 27.44 first", file=sys.stderr)
        return 1
    if args.work_dir.exists() and not args.keep_work:
        shutil.rmtree(args.work_dir)

    corpus_dir = args.work_dir / "corpus"
    checkpoints = args.work_dir / "checkpoints"
    records = _records()
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
        "--seed", "20260616",
        "--checkpoints", str(checkpoints),
        "--device", args.device,
    ]
    train_code = train_tiny_lm_run(train_args)
    if train_code != 0:
        return train_code

    checkpoint_name = _latest_checkpoint_name(checkpoints)
    rows = _evaluate(
        tokenizer=args.tokenizer,
        checkpoints_root=checkpoints,
        checkpoint_name=checkpoint_name,
        device=args.device,
    )
    summary = _summary(rows)
    all_passed = summary["passed"] == summary["total"]
    status = (
        "PASSED_CORE_DIALOGUE_STABILIZATION_READY_FOR_GUARDED_SWITCH"
        if all_passed
        else "PARTIAL_CORE_DIALOGUE_STABILIZATION_KEEP_PHASE27_40_RUNTIME"
    )
    report = {
        "phase": "Phase 27.46",
        "status": status,
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "training_started": True,
        "training_scope": "SF-10M core dialogue stabilization only; no scaling",
        "tokenizer": _rel(args.tokenizer),
        "checkpoint_root": _rel(checkpoints),
        "checkpoint_name": checkpoint_name,
        "candidate_generator": "sf_10m_phase27_46",
        "train_records": len(records),
        "probe_case_count": len(PROBE_CASES),
        "summary": summary,
        "runtime_switch_allowed": all_passed,
        "sf50m_allowed": False,
        "phase28_allowed": False,
        "previous_phase27_44": {"passed": 11, "total": 16},
        "previous_phase27_45": {"passed": 9, "total": 16},
        "next_phase": (
            "Phase 27.47 — guarded runtime switch for phase27_46"
            if all_passed
            else "Phase 27.47 — inspect remaining core blockers"
        ),
        "torch_version": torch.__version__,
        "rows": rows,
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _write_samples(args.samples, rows)

    print("SF.AI — Phase 27.46 core dialogue stabilization")
    print(f"  status      : {status}")
    print(f"  tokenizer   : {_rel(args.tokenizer)}")
    print(f"  checkpoint  : {checkpoint_name}")
    print(f"  train rows  : {len(records)}")
    print(f"  cases       : {summary['passed']}/{summary['total']}")
    for bucket, item in summary["bucket_summary"].items():
        print(f"  {bucket:<12}: {item['passed']}/{item['total']}")
    print(f"  reasons     : {summary['reason_counts']}")
    print(f"  report      : {args.report}")
    print(f"  samples     : {args.samples}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
