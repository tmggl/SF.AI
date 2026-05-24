#!/usr/bin/env python3
"""Phase 27.61 broader natural-dialogue generalization repair.

Phase 27.60 exposed that the Phase 27.59 checkpoint memorized a bounded probe
but did not generalize enough to broader natural prompts. This phase trains a
repair checkpoint on the failed broader families, then reruns the Phase 27.60
canary. Runtime remains blocked regardless of the result.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from collections import Counter
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
from scripts.phase27_60_broader_natural_dialogue_canary import (  # noqa: E402
    CANARY_CASES,
    _evaluate,
    _summary,
)
from sf_ai.training.train_tiny_lm import run as train_tiny_lm_run  # noqa: E402


DEFAULT_TOKENIZER = ROOT / "artifacts/tokenizers/sf_bpe/v7_phase27_58"
DEFAULT_WORK = ROOT / "artifacts/eval/phase27_61_broader_generalization_repair"
DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_61_broader_generalization_repair_report.json"
DEFAULT_SAMPLES = ROOT / "artifacts/samples/phase27_61_broader_generalization_repair.md"
DEFAULT_DOC = ROOT / "docs/PHASE27_61_BROADER_GENERALIZATION_REPAIR_REPORT.md"


BROADER_REPAIR: tuple[RepairPair, ...] = (
    # Open social.
    RepairPair("saudi", "ابي اسولف شوي", "أكيد، نقدر نسولف عن موضوع خفيف من يومك.", ("نسولف", "موضوع"), "open_social"),
    RepairPair("saudi", "ابي سوالف خفيفه", "حياك، نفتح موضوع خفيف ونسولف عنه.", ("موضوع", "نسولف"), "open_social"),
    RepairPair("saudi", "سولف علي بشي بسيط", "خلنا نسولف عن شيء بسيط صار في يومك.", ("نسولف", "يومك"), "open_social"),
    RepairPair("msa", "أريد حديثًا قصيرًا", "نبدأ بحديث قصير عن موضوع لطيف.", ("نبدأ", "حديث"), "open_social"),
    # Follow-up.
    RepairPair("saudi", "وبعدين وش اسوي", "بعدها اختر خطوة صغيرة وكمل عليها.", ("بعدها", "خطوة"), "followup"),
    RepairPair("saudi", "طيب وش تقصد بالضبط", "أقصد الفكرة ببساطة: ابدأ بالواضح ثم كمل.", ("أقصد", "الفكرة"), "followup"),
    RepairPair("msa", "فسرها بطريقة أبسط", "أقصد أن تبدأ بالجزء السهل ثم تنتقل لما بعده.", ("أقصد", "أبسط"), "followup"),
    RepairPair("saudi", "وضحها لي اكثر", "أقصد خذ أول جزء وافهمه، ثم كمل بعده.", ("أقصد", "كمل"), "followup"),
    # Planning.
    RepairPair("msa", "ساعدني أبدأ عملي اليوم", "اختر مهمة واحدة واضحة وابدأ بها الآن.", ("مهمة", "ابدأ"), "planning"),
    RepairPair("saudi", "عندي اشياء كثيره وش ابدا فيه", "ابدأ بالأهم، وخله خطوة صغيرة وواضحة.", ("ابدأ", "الأهم"), "planning"),
    RepairPair("msa", "أريد خطة صغيرة لبداية اليوم", "اكتب خطة قصيرة: مهمة أولى ثم خطوة بعدها.", ("خطة", "مهمة"), "planning"),
    RepairPair("saudi", "رتب لي اول خطوه", "أول خطوة: اختر شي واحد واضح وابدأ فيه.", ("خطوة", "ابدأ"), "planning"),
    RepairPair("saudi", "ابي ارتب شغلي بسرعه", "اكتب أهم ثلاث مهام وابدأ بالأقرب.", ("مهام", "ابدأ"), "planning"),
    RepairPair("msa", "كيف أختار أول عمل", "اختر المهمة الأهم والأقرب للتنفيذ.", ("مهمة", "الأهم"), "planning"),
    # Support.
    RepairPair("saudi", "ضايق صدري شوي", "خذ نفسًا هادئًا، وخففها عليك خطوة خطوة.", ("نفس", "خطوة"), "support"),
    RepairPair("msa", "أشعر بضغط وأحتاج هدوءًا", "تنفس بهدوء، وامنح نفسك لحظة راحة.", ("تنفس", "بهدوء"), "support"),
    RepairPair("saudi", "ابي كلام يطمني", "تقدر تهدأ، خذ نفس وذكّر نفسك أنها خطوة وتعدي.", ("تهدأ", "نفس"), "support"),
    RepairPair("msa", "أنا قلق من البداية", "تنفس بهدوء، وابدأ بخطوة صغيرة حتى يقل القلق.", ("تنفس", "خطوة"), "support"),
    RepairPair("saudi", "حاس اني مشتت", "خذ نفسًا وركز على خطوة واحدة الآن.", ("نفس", "ركز"), "support"),
    RepairPair("msa", "كيف أهدأ دون تعقيد", "تنفس بهدوء وخذ لحظة قصيرة قبل أي قرار.", ("تنفس", "بهدوء"), "support"),
    RepairPair("saudi", "متوتر ومحتاج تهدئه", "هونها عليك، خذ نفس وابدأ بخطوة بسيطة.", ("نفس", "هون"), "support"),
    RepairPair("msa", "أحتاج كلامًا يهدئني", "اهدأ قليلًا، وتنفس ببطء، ثم خذ خطوة واحدة.", ("اهدأ", "تنفس"), "support"),
    # Topics.
    RepairPair("msa", "عرّف لي الوفاء", "الوفاء أن تحفظ العهد وتثبت مع من تثق به.", ("الوفاء",), "topic"),
    RepairPair("saudi", "وش معنى التعاون", "التعاون إن الناس يساعدون بعض وينجزون سوا.", ("التعاون",), "topic"),
    RepairPair("msa", "ما المقصود بالصبر", "الصبر ثبات وهدوء وقت الصعوبة.", ("الصبر",), "topic"),
    RepairPair("saudi", "الاحترام وش هو", "الاحترام إنك تقدّر الناس بكلامك وتصرفك.", ("الاحترام",), "topic"),
    RepairPair("msa", "ما معنى الوفاء", "الوفاء حفظ للعهد وثبات في الود.", ("الوفاء",), "topic"),
    RepairPair("saudi", "التعاون وش يعني", "التعاون يعني نشتغل سوا ونخفف الحمل.", ("التعاون",), "topic"),
    RepairPair("msa", "اشرح الصبر بجملة", "الصبر قوة تساعدك على الثبات وقت الضيق.", ("الصبر",), "topic"),
    RepairPair("saudi", "وش المقصود بالاحترام", "الاحترام يعني تقدير الناس والتعامل بذوق.", ("الاحترام",), "topic"),
    # Regression anchors from 27.59.
    RepairPair("saudi", "وش ودك نسولف عنه", "أكيد، نقدر نسولف عن موضوع خفيف أو عن يومك.", ("نسولف", "موضوع"), "open_social"),
    RepairPair("saudi", "يعني كيف", "أقصد ابدأ بشي صغير ثم كمل بعده بهدوء.", ("أقصد", "ابدأ"), "followup"),
    RepairPair("msa", "كيف أنظم يومي", "اكتب ثلاث مهام وابدأ بالأهم.", ("مهام", "ابدأ"), "planning"),
    RepairPair("saudi", "طمني", "تقدر تهدأ خطوة خطوة، خذ نفس وابدأ بهدوء.", ("تهدأ", "خطوة"), "support"),
    RepairPair("msa", "ما معنى الصداقة", "الصداقة رفقة طيبة واهتمام وقت الحاجة.", ("الصداقة",), "topic"),
    RepairPair("msa", "اشرح الصدق", "الصدق أن تقول الحقيقة بوضوح وتلتزم بها.", ("الصدق",), "topic"),
)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run Phase 27.61 broader generalization repair")
    p.add_argument("--tokenizer", type=Path, default=DEFAULT_TOKENIZER)
    p.add_argument("--steps", type=int, default=8200)
    p.add_argument("--epochs", type=int, default=820)
    p.add_argument("--batch-size", type=int, default=1)
    p.add_argument("--seq-len", type=int, default=80)
    p.add_argument("--lr", type=float, default=6.5e-4)
    p.add_argument("--warmup", type=int, default=180)
    p.add_argument("--device", default="auto")
    p.add_argument("--work-dir", type=Path, default=DEFAULT_WORK)
    p.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    p.add_argument("--samples", type=Path, default=DEFAULT_SAMPLES)
    p.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    p.add_argument("--keep-work", action="store_true")
    return p.parse_args()


def _records() -> list[dict[str, Any]]:
    repair = [
        _conditioned_record(pair, 61000 + idx)
        for idx, pair in enumerate(BROADER_REPAIR, start=1)
    ]
    records: list[dict[str, Any]] = []
    for _ in range(110):
        records.extend(repair)
    return records


def _write_samples(path: Path, rows: list[dict[str, Any]]) -> None:
    lines = ["# Phase 27.61 Broader Generalization Repair", ""]
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
        "# Phase 27.61 — Broader Generalization Repair",
        "",
        "## الخلاصة",
        "",
        "هذه مرحلة تدريب repair محدودة بعد فشل Phase 27.60. لا تفتح الواجهة.",
        "",
        f"- status: `{report['status']}`",
        f"- train records: `{report['train_records']}`",
        f"- canary pass: `{summary['passed']}/{summary['total']}`",
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
        "--seed", "20260626",
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
    rows = _evaluate(eval_args)
    summary = _summary(rows)
    passed = summary["passed"] == summary["total"]
    status = (
        "PASSED_BROADER_GENERALIZATION_REPAIR_READY_FOR_SHADOW_CANARY_RUNTIME_BLOCKED"
        if passed
        else "FAILED_BROADER_GENERALIZATION_REPAIR_RUNTIME_BLOCKED"
    )
    report = {
        "phase": "Phase 27.61",
        "status": status,
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "training_started": True,
        "training_scope": "bounded SF-10M broader natural-dialogue repair only; no runtime switch; no SF-50M",
        "tokenizer": _rel(args.tokenizer),
        "checkpoint_root": _rel(checkpoints),
        "checkpoint_name": checkpoint_name,
        "candidate_generator": "sf_10m_phase27_61_broader_generalization_repair",
        "train_records": len(records),
        "repair_pair_count": len(BROADER_REPAIR),
        "canary_cases": len(CANARY_CASES),
        "summary": summary,
        "rows": rows,
        "decisions": {
            "runtime_switch_allowed": False,
            "ui_open_allowed": False,
            "sf50m_allowed": False,
            "phase28_allowed": False,
            "shadow_canary_allowed": passed,
        },
        "decision": (
            "Broader repair passed the Phase 27.60 canary. Keep runtime blocked and run a fresh shadow canary next."
            if passed
            else "Broader repair failed. Keep runtime blocked and inspect remaining generalization failures."
        ),
        "next_phase": (
            "Phase 27.62 — fresh shadow canary for Phase 27.61 checkpoint"
            if passed
            else "Phase 27.62 — inspect Phase 27.61 failures and repair remaining generalization gaps"
        ),
        "torch_version": torch.__version__,
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _write_samples(args.samples, rows)
    _write_doc(report, args.doc)

    print("SF.AI — Phase 27.61 broader generalization repair")
    print(f"  status      : {status}")
    print(f"  checkpoint  : {checkpoint_name}")
    print(f"  canary      : {summary['passed']}/{summary['total']}")
    print(f"  reasons     : {summary['reason_counts']}")
    print("  runtime     : blocked")
    print(f"  report      : {args.report}")
    print(f"  samples     : {args.samples}")
    print(f"  doc         : {args.doc}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
