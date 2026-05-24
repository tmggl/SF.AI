#!/usr/bin/env python3
"""Phase 27.70 targeted open-social + stability repair.

Phase 27.69 was strong (56/60) but not enough for runtime: all remaining
failures were in open_social. This phase trains a bounded SF-10M repair that
adds open_social diversity while preserving the balanced repair corpus from
Phase 27.68. If repair pressure causes family drift, this phase also carries a
small stability set for followup/planning/topic, because runtime needs family
separation as much as it needs raw prompt coverage. It evaluates:

1. Phase 27.69 new fresh shadow canary.
2. Phase 27.67 known shadow canary.
3. Phase 27.60 broader canary regression.

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
from scripts.phase27_60_broader_natural_dialogue_canary import _evaluate as evaluate_phase27_60, _summary as summary_phase27_60  # noqa: E402
from scripts.phase27_62_family_balance_repair import FAMILY_BALANCE_REPAIR  # noqa: E402
from scripts.phase27_66_v8_bounded_topic_repair import TOPIC_EMPHASIS_REPAIR  # noqa: E402
from scripts.phase27_67_fresh_shadow_canary import _evaluate as evaluate_phase27_67, _summary as summary_phase27_67  # noqa: E402
from scripts.phase27_68_shadow_failure_repair import SHADOW_FAILURE_REPAIR  # noqa: E402
from scripts.phase27_69_new_fresh_shadow_canary import _evaluate as evaluate_phase27_69, _summary as summary_phase27_69  # noqa: E402
from sf_ai.training.train_tiny_lm import run as train_tiny_lm_run  # noqa: E402


DEFAULT_TOKENIZER = ROOT / "artifacts/tokenizers/sf_bpe/v8_phase27_65"
DEFAULT_INIT_CHECKPOINTS = ROOT / "artifacts/eval/phase27_68_shadow_failure_repair/checkpoints"
DEFAULT_INIT_CHECKPOINT_NAME = "sf-10m-step5600"
DEFAULT_WORK = ROOT / "artifacts/eval/phase27_70_open_social_repair"
DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_70_open_social_repair_report.json"
DEFAULT_SAMPLES = ROOT / "artifacts/samples/phase27_70_open_social_repair.md"
DEFAULT_DOC = ROOT / "docs/PHASE27_70_OPEN_SOCIAL_REPAIR_REPORT.md"


OPEN_SOCIAL_REPAIR: tuple[RepairPair, ...] = (
    RepairPair("msa", "اختر حديثًا خفيفًا بيننا", "نختار موضوعًا خفيفًا ونتحدث عنه ببساطة.", ("موضوع", "خفيف"), "open_social"),
    RepairPair("saudi", "ودي بموضوع سوالف", "نختار موضوع سوالف خفيف ونسولف عنه.", ("موضوع", "سوالف"), "open_social"),
    RepairPair("msa", "ابدأ محادثة سهلة", "نبدأ محادثة سهلة عن موضوع بسيط.", ("محادثة", "موضوع"), "open_social"),
    RepairPair("msa", "لنختر موضوعًا صغيرًا", "نختار موضوعًا صغيرًا وخفيفًا للكلام.", ("موضوع", "صغير"), "open_social"),
    RepairPair("saudi", "هات سوالف تمشي الوقت", "نسولف بسوالف خفيفة تمشي الوقت.", ("نسولف", "سوالف"), "open_social"),
    RepairPair("msa", "أعطني بداية كلام خفيفة", "نبدأ بكلام خفيف عن موضوع بسيط.", ("كلام", "موضوع"), "open_social"),
    RepairPair("saudi", "خلنا بس نسولف", "أبشر، نسولف عن موضوع بسيط من يومك.", ("نسولف", "موضوع"), "open_social"),
    RepairPair("msa", "افتح كلامًا عاديًا", "نفتح كلامًا عاديًا عن موضوع خفيف.", ("كلام", "موضوع"), "open_social"),
    RepairPair("saudi", "ابي موضوع خفيف للسوالف", "موضوع خفيف: نسولف عن شيء صار في يومك.", ("موضوع", "نسولف"), "open_social"),
    RepairPair("msa", "اختر موضوعًا للتسلية", "نختار موضوعًا خفيفًا للتسلية والكلام.", ("موضوع", "خفيف"), "open_social"),
    RepairPair("saudi", "وش نقدر نسولف عنه", "نقدر نسولف عن يومك أو عن موضوع خفيف.", ("نسولف", "موضوع"), "open_social"),
    RepairPair("msa", "ابدأ معي محادثة ودية", "نبدأ محادثة ودية عن موضوع بسيط.", ("محادثة", "موضوع"), "open_social"),
    RepairPair("msa", "اختر لي شيئًا نتحدث عنه", "نختار موضوعًا بسيطًا نتحدث عنه بهدوء.", ("موضوع", "نتحدث"), "open_social"),
    RepairPair("saudi", "اختر لي شي نسولف عنه", "نختار موضوعًا خفيفًا ونسولف عنه.", ("موضوع", "نسولف"), "open_social"),
)


STABILITY_REPAIR: tuple[RepairPair, ...] = (
    RepairPair("saudi", "ما وصلتني الفكرة", "أقصد الفكرة ببساطة، ونوضحها خطوة خطوة.", ("الفكرة", "خطوة"), "followup"),
    RepairPair("msa", "لم تصلني الفكرة", "أوضح الفكرة: نأخذها خطوة قصيرة ثم نكمل.", ("الفكرة", "خطوة"), "followup"),
    RepairPair("msa", "تابع من آخر جملة", "نكمل من آخر جملة ونوضح الفكرة خطوة بعدها.", ("نكمل", "الفكرة", "خطوة"), "followup"),
    RepairPair("saudi", "خلني ابدأ بدون تشتت", "ابدأ بخطوة واحدة واضحة حتى يقل التشتت.", ("ابدأ", "تشتت", "خطوة"), "planning"),
    RepairPair("msa", "كيف أبدأ بلا تشتت", "ابدأ بمهمة واحدة واضحة واترك الباقي لاحقًا.", ("ابدأ", "مهمة", "تشتت"), "planning"),
    RepairPair("msa", "أريد تنظيمًا بسيطًا للمهام", "تنظيم بسيط: اختر مهمة واحدة وابدأ بها.", ("تنظيم", "مهمة", "ابدأ"), "planning"),
    RepairPair("saudi", "مهامي كثيره ومادري من وين", "ابدأ بالأهم من مهامك، ثم خذ خطوة واحدة.", ("مهام", "ابدأ", "الأهم"), "planning"),
    RepairPair("msa", "مهامي كثيرة ولا أعرف من أين أبدأ", "ابدأ بمهمة واحدة هي الأهم، ثم أكمل خطوة بعدها.", ("مهمة", "ابدأ", "الأهم"), "planning"),
    RepairPair("msa", "ما معنى الوفاء للناس", "الوفاء حفظ للعهد وثبات مع الناس.", ("الوفاء",), "topic"),
    RepairPair("saudi", "وش يعني الوفاء مع الناس", "الوفاء إنك تحفظ العهد وتثبت مع الناس.", ("الوفاء",), "topic"),
    RepairPair("msa", "عرّف الهدوء بعبارة بسيطة", "الهدوء سكينة تساعد الإنسان على التفكير بوضوح.", ("الهدوء",), "topic"),
    RepairPair("saudi", "وش يعني الهدوء باختصار", "الهدوء إنك تهدأ وتفكر بروية.", ("الهدوء",), "topic"),
    RepairPair("msa", "كيف أستعيد تركيزي بهدوء", "استعد تركيزك بهدوء: تنفس لحظة ثم اختر خطوة واحدة.", ("تركيز", "هدوء", "تنفس"), "support"),
    RepairPair("saudi", "كيف ارجع تركيزي بهدوء", "ارجع لتركيزك بهدوء: خذ نفسًا ثم ابدأ بخطوة صغيرة.", ("تركيز", "هدوء", "نفس"), "support"),
    RepairPair("msa", "طمئنّي بجملة قصيرة", "هونها على نفسك وخذ نفسًا هادئًا.", ("هون", "نفس"), "support"),
    RepairPair("msa", "طمئني بكلام قصير", "خذ نفسًا هادئًا، وستستعيد راحتك خطوة خطوة.", ("نفس", "راحة"), "support"),
)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run Phase 27.70 targeted open-social repair")
    p.add_argument("--tokenizer", type=Path, default=DEFAULT_TOKENIZER)
    p.add_argument("--steps", type=int, default=1200)
    p.add_argument("--epochs", type=int, default=120)
    p.add_argument("--batch-size", type=int, default=1)
    p.add_argument("--seq-len", type=int, default=80)
    p.add_argument("--lr", type=float, default=8e-5)
    p.add_argument("--warmup", type=int, default=80)
    p.add_argument("--target-per-family", type=int, default=1250)
    p.add_argument(
        "--families",
        default="all",
        help="Comma-separated repair families to include, or 'all'",
    )
    p.add_argument("--init-checkpoints", type=Path, default=DEFAULT_INIT_CHECKPOINTS)
    p.add_argument("--init-checkpoint-name", default=DEFAULT_INIT_CHECKPOINT_NAME)
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
    )


def _family_groups() -> dict[str, list[RepairPair]]:
    grouped: dict[str, list[RepairPair]] = defaultdict(list)
    for pair in _repair_pairs():
        grouped[pair.category].append(pair)
    return dict(sorted(grouped.items()))


def _records(target_per_family: int, *, families: set[str] | None = None) -> list[dict[str, Any]]:
    grouped = _family_groups()
    if families is not None:
        grouped = {name: pairs for name, pairs in grouped.items() if name in families}
    if not grouped:
        raise ValueError("no repair families selected")
    iterators = {family: cycle(pairs) for family, pairs in grouped.items()}
    counts = {family: 0 for family in grouped}
    records: list[dict[str, Any]] = []
    idx = 70000
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
    phase27_69_rows: list[dict[str, Any]],
    phase27_67_rows: list[dict[str, Any]],
    phase27_60_rows: list[dict[str, Any]],
) -> None:
    lines = ["# Phase 27.70 Open-Social Repair", ""]
    for title, rows in (
        ("Phase 27.69 new fresh shadow", phase27_69_rows),
        ("Phase 27.67 known shadow", phase27_67_rows),
        ("Phase 27.60 regression", phase27_60_rows),
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


def _write_doc(report: dict[str, Any], path: Path) -> None:
    fresh = report["phase27_69_summary"]
    known = report["phase27_67_summary"]
    regression = report["phase27_60_summary"]
    lines = [
        "# Phase 27.70 — Open-Social Repair",
        "",
        "## الخلاصة",
        "",
        "هذه مرحلة تدريب إصلاح محدودة لـ open_social مع stability repair للعائلات التي تراجعت. لا تفتح الواجهة ولا تغيّر runtime.",
        "",
        f"- status: `{report['status']}`",
        f"- tokenizer: `{report['tokenizer']}`",
        f"- checkpoint: `{report['checkpoint_root']}/{report['checkpoint_name']}`",
        f"- Phase 27.69 fresh: `{fresh['passed']}/{fresh['total']}`",
        f"- Phase 27.67 known: `{known['passed']}/{known['total']}`",
        f"- Phase 27.60 regression: `{regression['passed']}/{regression['total']}`",
        f"- runtime switch allowed: `{report['decisions']['runtime_switch_allowed']}`",
        "",
        "## Phase 27.69 family summary",
        "",
    ]
    for family, item in fresh["family_summary"].items():
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
    selected_families = None if args.families.strip().lower() == "all" else {
        item.strip()
        for item in args.families.split(",")
        if item.strip()
    }
    records = _records(args.target_per_family, families=selected_families)
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
        "--seed", "20260702",
        "--checkpoints", str(checkpoints),
        "--device", args.device,
    ]
    if args.init_checkpoints and args.init_checkpoint_name:
        train_args.extend(
            [
                "--init-checkpoints", str(args.init_checkpoints),
                "--init-checkpoint-name", args.init_checkpoint_name,
            ]
        )
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
    improved = summary_69["passed"] > 56 and summary_67["passed"] >= 49 and summary_60["passed"] >= 29
    status = (
        "PASSED_OPEN_SOCIAL_REPAIR_READY_FOR_NEW_FRESH_SHADOW_RUNTIME_BLOCKED"
        if passed
        else (
            "IMPROVED_OPEN_SOCIAL_REPAIR_RUNTIME_BLOCKED"
            if improved
            else "FAILED_OPEN_SOCIAL_REPAIR_RUNTIME_BLOCKED"
        )
    )
    report = {
        "phase": "Phase 27.70",
        "status": status,
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "training_started": True,
        "training_scope": "bounded SF-10M open_social + stability repair; no runtime switch; no SF-50M",
        "tokenizer": _rel(args.tokenizer),
        "checkpoint_root": _rel(checkpoints),
        "checkpoint_name": checkpoint_name,
        "init_checkpoint_root": _rel(args.init_checkpoints) if args.init_checkpoints else None,
        "init_checkpoint_name": args.init_checkpoint_name,
        "candidate_generator": "sf_10m_phase27_70_open_social_repair",
        "train_records": len(records),
        "selected_repair_families": sorted(selected_families) if selected_families is not None else "all",
        "repair_pair_count": len(_repair_pairs()),
        "open_social_repair_pair_count": len(OPEN_SOCIAL_REPAIR),
        "stability_repair_pair_count": len(STABILITY_REPAIR),
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
            "new_fresh_shadow_allowed": passed,
            "repair_required_before_runtime": not passed,
        },
        "decision": (
            "Open-social repair passed current fresh and regression canaries. Runtime remains blocked; run a new fresh shadow canary next."
            if passed
            else "Open-social repair did not fully pass current canaries. Runtime remains blocked; use candidate selection and stability gates before any UI/runtime change."
        ),
        "next_phase": (
            "Phase 27.71 — new fresh shadow canary after open_social repair"
            if passed
            else "Phase 27.71 — candidate-selection and stability strategy before runtime"
        ),
        "torch_version": torch.__version__,
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _write_samples(args.samples, rows_69, rows_67, rows_60)
    _write_doc(report, args.doc)

    print("SF.AI — Phase 27.70 open-social repair")
    print(f"  status      : {status}")
    print(f"  checkpoint  : {checkpoint_name}")
    print(f"  phase27.69  : {summary_69['passed']}/{summary_69['total']}")
    print(f"  phase27.67  : {summary_67['passed']}/{summary_67['total']}")
    print(f"  phase27.60  : {summary_60['passed']}/{summary_60['total']}")
    print(f"  family      : {summary_69['family_summary']}")
    print(f"  report      : {_rel(args.report)}")
    print(f"  samples     : {_rel(args.samples)}")
    print("  runtime     : blocked")
    return 0 if args.report.exists() else 1


if __name__ == "__main__":
    raise SystemExit(main())
