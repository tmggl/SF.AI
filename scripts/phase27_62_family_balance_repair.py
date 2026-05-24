#!/usr/bin/env python3
"""Phase 27.62 response-family balance repair.

Phase 27.61 improved broader natural dialogue from 12/30 to 18/30, but the
remaining failures show family imbalance: open_social/followup/topic prompts
often drift into support or unrelated topic answers. This phase trains a fresh,
balanced SF-10M repair probe on tokenizer v7 and reruns the Phase 27.60 canary.

Runtime remains blocked regardless of the result. A pass here only allows a
fresh shadow canary in a later phase.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from collections import defaultdict
from itertools import cycle, islice
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
DEFAULT_WORK = ROOT / "artifacts/eval/phase27_62_family_balance_repair"
DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_62_family_balance_repair_report.json"
DEFAULT_SAMPLES = ROOT / "artifacts/samples/phase27_62_family_balance_repair.md"
DEFAULT_DOC = ROOT / "docs/PHASE27_62_FAMILY_BALANCE_REPAIR_REPORT.md"


FAMILY_BALANCE_REPAIR: tuple[RepairPair, ...] = (
    # Open social: invite a natural topic without drifting to planning/support.
    RepairPair("saudi", "ابي اسولف شوي", "أكيد، نسولف عن موضوع خفيف من يومك.", ("نسولف", "موضوع"), "open_social"),
    RepairPair("saudi", "خلنا نفتح موضوع بسيط", "نبدأ بموضوع بسيط وخفيف، وش ودك؟", ("موضوع", "نبدأ"), "open_social"),
    RepairPair("msa", "حدثني حديثًا لطيفًا", "نبدأ بحديث لطيف عن شيء خفيف.", ("حديث", "نبدأ"), "open_social"),
    RepairPair("saudi", "وش عندك كلام خفيف", "عندي كلام خفيف: نسولف عن يومك أو موقف بسيط.", ("خفيف", "يومك"), "open_social"),
    RepairPair("msa", "افتح معي حوارًا قصيرًا", "نفتح حوارًا قصيرًا عن موضوع بسيط.", ("حوار", "موضوع"), "open_social"),
    RepairPair("saudi", "ما عندي موضوع سولف انت", "أبشر، نسولف عن يومك أو عن شيء خفيف.", ("سولف", "يومك"), "open_social"),
    RepairPair("saudi", "هات سالفة قصيرة", "خلنا نبدأ بسالفة قصيرة وخفيفة.", ("نبدأ", "خفيفة"), "open_social"),
    RepairPair("msa", "أريد كلامًا خفيفًا", "تفضل، نبدأ بكلام خفيف عن يومك.", ("نبدأ", "يومك"), "open_social"),
    RepairPair("saudi", "وش نسولف عنه", "نقدر نسولف عن يومك أو عن موضوع تحبه.", ("نسولف", "موضوع"), "open_social"),
    RepairPair("msa", "اختر لي موضوعًا لطيفًا", "نختار موضوعًا لطيفًا ونتحدث عنه بهدوء.", ("موضوع", "نتحدث"), "open_social"),
    RepairPair("saudi", "ودي بسوالف عاديه", "حياك، نسولف سوالف عادية وخفيفة.", ("حياك", "نسولف"), "open_social"),
    RepairPair("msa", "دعنا نتحدث قليلًا", "نعم، نتحدث قليلًا في موضوع بسيط.", ("نتحدث", "موضوع"), "open_social"),

    # Follow-up: explain/continue without drifting to definitions/support.
    RepairPair("saudi", "ما فهمت قصدك", "أقصد الفكرة ببساطة: ابدأ بالواضح ثم كمل.", ("أقصد", "الفكرة"), "followup"),
    RepairPair("msa", "هل توضح لي الفكرة", "أقصد أن الفكرة تبدأ بخطوة واضحة.", ("أقصد", "الفكرة"), "followup"),
    RepairPair("saudi", "وبعدين وش اسوي", "بعدها خذ خطوة صغيرة وكمل عليها.", ("بعدها", "خطوة"), "followup"),
    RepairPair("msa", "أكمل شرحك", "نكمل: الفكرة أن تبدأ بالسهل ثم تنتقل بعده.", ("نكمل", "الفكرة"), "followup"),
    RepairPair("saudi", "طيب وش تقصد بالضبط", "أقصد باختصار: خذ أول جزء واضح وابدأ منه.", ("أقصد", "ابدأ"), "followup"),
    RepairPair("msa", "فسرها بطريقة أبسط", "أبسطها لك: ابدأ بالجزء السهل ثم أكمل.", ("أبسط", "ابدأ"), "followup"),
    RepairPair("saudi", "يعني كيف", "يعني ابدأ بشي صغير وواضح ثم كمل.", ("يعني", "ابدأ"), "followup"),
    RepairPair("msa", "ماذا تقصد", "أقصد أن تختار خطوة واضحة قبل التفاصيل.", ("أقصد", "خطوة"), "followup"),
    RepairPair("saudi", "وضحها لي اكثر", "أقصد خذ أول خطوة وافهمها ثم كمل.", ("أقصد", "كمل"), "followup"),
    RepairPair("msa", "أعد شرح الفكرة", "الفكرة ببساطة: خطوة واضحة ثم متابعة هادئة.", ("الفكرة", "خطوة"), "followup"),
    RepairPair("saudi", "طيب بعدين", "بعدها كمل على الخطوة التالية بهدوء.", ("بعدها", "كمل"), "followup"),
    RepairPair("msa", "هل تبسطها لي", "نعم، أبسطها: ابدأ بالقريب ثم انتقل لما بعده.", ("أبسط", "ابدأ"), "followup"),

    # Topic: each topic must keep its own term and not collapse into support.
    RepairPair("msa", "عرّف لي الوفاء", "الوفاء حفظ للعهد وثبات في الود.", ("الوفاء",), "topic"),
    RepairPair("saudi", "وش معنى التعاون", "التعاون يعني نساعد بعض وننجز سوا.", ("التعاون",), "topic"),
    RepairPair("msa", "ما المقصود بالصبر", "الصبر ثبات وهدوء وقت الصعوبة.", ("الصبر",), "topic"),
    RepairPair("saudi", "الاحترام وش هو", "الاحترام يعني تقدير الناس بالكلام والتصرف.", ("الاحترام",), "topic"),
    RepairPair("msa", "اشرح الهدوء بجملة", "الهدوء سكينة تساعدك على التفكير بوضوح.", ("الهدوء",), "topic"),
    RepairPair("saudi", "وش يعني الصدق ببساطه", "الصدق يعني تقول الحقيقة بوضوح.", ("الصدق",), "topic"),
    RepairPair("msa", "ما معنى الصداقة", "الصداقة رفقة طيبة واهتمام وقت الحاجة.", ("الصداقة",), "topic"),
    RepairPair("saudi", "الشجاعة وش تعني", "الشجاعة إنك تسوي الصح حتى لو كنت خايف.", ("الشجاعة",), "topic"),
    RepairPair("msa", "ما معنى التعاون", "التعاون مشاركة الجهد بين الناس.", ("التعاون",), "topic"),
    RepairPair("saudi", "وش المقصود بالصبر", "الصبر إنك تتحمل وتكمل بدون استعجال.", ("الصبر",), "topic"),
    RepairPair("msa", "ما معنى الاحترام", "الاحترام تقدير الناس قولًا وفعلًا.", ("الاحترام",), "topic"),
    RepairPair("saudi", "الهدوء وش يعني", "الهدوء يعني تخفف توترك وتفكر بروية.", ("الهدوء",), "topic"),
    RepairPair("msa", "اشرح الصدق", "الصدق أن تقول الحقيقة وتلتزم بها.", ("الصدق",), "topic"),
    RepairPair("saudi", "وش معنى الوفاء", "الوفاء إنك تحفظ العهد وتثبت مع الناس.", ("الوفاء",), "topic"),
    RepairPair("msa", "عرّف الشجاعة", "الشجاعة فعل الصواب مع وجود الخوف.", ("الشجاعة",), "topic"),
    RepairPair("saudi", "الصداقة وش تعني", "الصداقة رفقة طيبة ووقفة وقت الحاجة.", ("الصداقة",), "topic"),

    # Regression anchors: keep strong families alive with lower diversity.
    RepairPair("saudi", "ابي اخلي يومي مرتب", "ابدأ بثلاث مهام، واختر الأهم أولًا.", ("مهام", "الأهم"), "planning"),
    RepairPair("msa", "ساعدني أبدأ عملي اليوم", "اختر مهمة واحدة واضحة وابدأ بها الآن.", ("مهمة", "ابدأ"), "planning"),
    RepairPair("saudi", "عندي اشياء كثيره وش ابدا فيه", "ابدأ بالأهم، وخله خطوة صغيرة.", ("ابدأ", "الأهم"), "planning"),
    RepairPair("msa", "أريد خطة صغيرة لبداية اليوم", "اكتب خطة قصيرة: مهمة أولى ثم خطوة بعدها.", ("خطة", "مهمة"), "planning"),
    RepairPair("saudi", "رتب لي اول خطوه", "أول خطوة: اختر شي واحد واضح وابدأ فيه.", ("خطوة", "ابدأ"), "planning"),
    RepairPair("msa", "كيف أختار أول مهمة", "اختر المهمة الأهم والأقرب للتنفيذ.", ("مهمة", "الأهم"), "planning"),

    RepairPair("saudi", "ضايق صدري شوي", "خذ نفسًا هادئًا وخففها عليك خطوة خطوة.", ("نفس", "خطوة"), "support"),
    RepairPair("msa", "أشعر بضغط وأحتاج هدوءًا", "تنفس بهدوء وامنح نفسك لحظة راحة.", ("تنفس", "راحة"), "support"),
    RepairPair("saudi", "ابي كلام يطمني", "تقدر تهدأ، خذ نفس وذكّر نفسك أنها تعدي.", ("تهدأ", "نفس"), "support"),
    RepairPair("msa", "أنا قلق من البداية", "تنفس بهدوء وابدأ بخطوة صغيرة.", ("تنفس", "خطوة"), "support"),
    RepairPair("saudi", "حاس اني مشتت", "خذ نفسًا وركز على خطوة واحدة الآن.", ("نفس", "ركز"), "support"),
    RepairPair("msa", "كيف أهدأ دون تعقيد", "تنفس بهدوء وخذ لحظة قصيرة.", ("تنفس", "بهدوء"), "support"),
)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run Phase 27.62 response-family balance repair")
    p.add_argument("--tokenizer", type=Path, default=DEFAULT_TOKENIZER)
    p.add_argument("--steps", type=int, default=7800)
    p.add_argument("--epochs", type=int, default=780)
    p.add_argument("--batch-size", type=int, default=1)
    p.add_argument("--seq-len", type=int, default=80)
    p.add_argument("--lr", type=float, default=6e-4)
    p.add_argument("--warmup", type=int, default=180)
    p.add_argument("--target-per-family", type=int, default=1200)
    p.add_argument("--device", default="auto")
    p.add_argument("--work-dir", type=Path, default=DEFAULT_WORK)
    p.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    p.add_argument("--samples", type=Path, default=DEFAULT_SAMPLES)
    p.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    p.add_argument("--keep-work", action="store_true")
    return p.parse_args()


def _records(target_per_family: int) -> list[dict[str, Any]]:
    grouped: dict[str, list[RepairPair]] = defaultdict(list)
    for pair in FAMILY_BALANCE_REPAIR:
        grouped[pair.category].append(pair)

    records: list[dict[str, Any]] = []
    idx = 62000
    for family in sorted(grouped):
        for pair in islice(cycle(grouped[family]), target_per_family):
            idx += 1
            records.append(_conditioned_record(pair, idx))
    return records


def _write_samples(path: Path, rows: list[dict[str, Any]]) -> None:
    lines = ["# Phase 27.62 Family-Balance Repair", ""]
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
        "# Phase 27.62 — Response-Family Balance Repair",
        "",
        "## الخلاصة",
        "",
        "هذه مرحلة إصلاح توازن لعائلات الرد بعد Phase 27.61. لا تفتح الواجهة.",
        "",
        f"- status: `{report['status']}`",
        f"- train records: `{report['train_records']}`",
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
    family_counts = {family: args.target_per_family for family in sorted({pair.category for pair in FAMILY_BALANCE_REPAIR})}
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
        "--seed", "20260627",
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
        "PASSED_FAMILY_BALANCE_REPAIR_READY_FOR_FRESH_SHADOW_CANARY_RUNTIME_BLOCKED"
        if passed
        else "FAILED_FAMILY_BALANCE_REPAIR_RUNTIME_BLOCKED"
    )
    report = {
        "phase": "Phase 27.62",
        "status": status,
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "training_started": True,
        "training_scope": "bounded SF-10M response-family balance repair only; no runtime switch; no SF-50M",
        "tokenizer": _rel(args.tokenizer),
        "checkpoint_root": _rel(checkpoints),
        "checkpoint_name": checkpoint_name,
        "candidate_generator": "sf_10m_phase27_62_family_balance_repair",
        "train_records": len(records),
        "repair_pair_count": len(FAMILY_BALANCE_REPAIR),
        "target_per_family": args.target_per_family,
        "record_family_notes": dict(family_counts),
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
            "Family-balance repair passed the existing broader canary. Keep runtime blocked and run a fresh shadow canary next."
            if passed
            else "Family-balance repair failed. Keep runtime blocked and inspect the remaining failed families before training again."
        ),
        "next_phase": (
            "Phase 27.63 — fresh shadow canary with unseen natural prompts"
            if passed
            else "Phase 27.63 — inspect Phase 27.62 failures and repair remaining weak families"
        ),
        "torch_version": torch.__version__,
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _write_samples(args.samples, rows)
    _write_doc(report, args.doc)

    print("SF.AI — Phase 27.62 family-balance repair")
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
