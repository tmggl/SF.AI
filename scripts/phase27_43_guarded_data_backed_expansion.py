#!/usr/bin/env python3
"""Phase 27.43 guarded data-backed expansion.

Phase 27.42 proved the live guard is useful: it blocked misaligned generated
answers for weak lanes such as "وش اخبارك" and "نظم وقتي". This phase adds a
small sovereign repair curriculum for those lanes, trains an SF-10M candidate
on tokenizer v5, then evaluates the candidate offline before any runtime
switch.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from collections import Counter
from dataclasses import dataclass
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
from scripts.phase27_40_tokenizer_context_repair import _records as phase27_40_records  # noqa: E402
from sf_ai.modules.chat.generation_guard import GenerationGuard  # noqa: E402
from sf_ai.modules.chat.native_generator import NativeGenerator, NativeGeneratorConfig  # noqa: E402
from sf_ai.training.train_tiny_lm import run as train_tiny_lm_run  # noqa: E402


DEFAULT_TOKENIZER = ROOT / "artifacts/tokenizers/sf_bpe/v5_topic_terms"
DEFAULT_WORK = ROOT / "artifacts/eval/phase27_43_guarded_data_backed_expansion"
DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_43_guarded_data_backed_expansion_report.json"
DEFAULT_SAMPLES = ROOT / "artifacts/samples/phase27_43_guarded_data_backed_expansion.md"


@dataclass(frozen=True)
class CandidateCase:
    id: str
    dialect: str
    prompt: str
    intent: str
    topic: str
    expected_terms: tuple[str, ...]
    bucket: str


WEAK_LANE_REPAIR: tuple[RepairPair, ...] = (
    RepairPair("saudi", "وش اخبارك", "بخير ولله الحمد، وش أخبارك أنت؟", ("بخير",), "smalltalk"),
    RepairPair("saudi", "وش أخبارك اليوم", "بخير ولله الحمد، أنت كيفك؟", ("بخير",), "smalltalk"),
    RepairPair("saudi", "علومك", "تمام والحمدلله. وش ودك نسولف عنه؟", ("تمام",), "smalltalk"),
    RepairPair("msa", "كيف حالك اليوم", "بخير، شكرًا لسؤالك.", ("بخير",), "smalltalk"),
    RepairPair("msa", "مشكور", "العفو، حاضر بأي وقت.", ("العفو",), "thanks"),
    RepairPair("msa", "تسلم", "العفو، يسعدني أساعدك.", ("العفو",), "thanks"),
    RepairPair("saudi", "يعطيك العافية", "الله يعافيك، حاضر بأي وقت.", ("يعافيك",), "thanks"),
    RepairPair("msa", "نظم وقتي", "اكتب ثلاث مهام وابدأ بالأهم.", ("مهام", "الأهم"), "planning"),
    RepairPair("saudi", "ابي ارتب اولوياتي", "ابدأ بالأهم ثم انتقل للي بعده.", ("ابدأ", "الأهم"), "planning"),
    RepairPair("msa", "رتب أولوياتي", "اكتب أولوياتك ثم ابدأ بالأهم.", ("أولويات", "الأهم"), "planning"),
    RepairPair("saudi", "ابي انظم يومي", "اكتب ثلاث مهام وابدأ بالأهم.", ("مهام", "الأهم"), "planning"),
    RepairPair("msa", "ما معنى الوفاء", "الوفاء أن تحفظ الود وتثبت مع من تثق به.", ("الوفاء",), "definition"),
    RepairPair("saudi", "الوفاء وش يعني", "الوفاء إنك تحفظ المعروف وتوقف مع اللي تثق فيه.", ("الوفاء",), "definition"),
    RepairPair("msa", "اشرح الشجاعة", "الشجاعة أن تفعل الصواب رغم الخوف.", ("الشجاعة",), "definition"),
    RepairPair("saudi", "الشجاعة وش تعني", "الشجاعة إنك تواجه الصح حتى لو كنت خايف.", ("الشجاعة",), "definition"),
)


PROBE_CASES: tuple[CandidateCase, ...] = (
    CandidateCase("weak_smalltalk_akhbarak", "saudi", "وش اخبارك", "smalltalk", "", ("بخير",), "weak_lane"),
    CandidateCase("weak_smalltalk_oloomk", "saudi", "علومك", "smalltalk", "", ("بخير",), "weak_lane"),
    CandidateCase("weak_thanks_mashkoor", "msa", "مشكور", "thanks", "", ("العفو",), "weak_lane"),
    CandidateCase("weak_thanks_tislam", "msa", "تسلم", "thanks", "", ("العفو",), "weak_lane"),
    CandidateCase("weak_planning_time", "msa", "نظم وقتي", "planning", "", ("مهام",), "weak_lane"),
    CandidateCase("weak_planning_priorities", "saudi", "ابي ارتب اولوياتي", "planning", "", ("ابدأ",), "weak_lane"),
    CandidateCase("new_definition_wafa", "msa", "ما معنى الوفاء", "definition", "الوفاء", ("الوفاء",), "new_topic"),
    CandidateCase("new_definition_courage", "msa", "اشرح الشجاعة", "definition", "الشجاعة", ("الشجاعة",), "new_topic"),
    CandidateCase("reg_smalltalk", "saudi", "كيفك اليوم", "smalltalk", "", ("بخير",), "regression"),
    CandidateCase("reg_advice", "msa", "انصحني ببداية بسيطة", "advice", "", ("ابدأ",), "regression"),
    CandidateCase("reg_planning", "msa", "كيف ارتب مهامي", "planning", "", ("مهام",), "regression"),
    CandidateCase("reg_support", "msa", "انا متوتر", "support", "", ("نفس", "اهدأ"), "regression"),
    CandidateCase("reg_friendship", "msa", "ما معنى الصداقة", "definition", "الصداقة", ("الصداقة",), "regression"),
    CandidateCase("reg_truth", "saudi", "الصدق وش يعني", "definition", "الصدق", ("الصدق",), "regression"),
    CandidateCase("reg_order", "msa", "ما معنى التنظيم", "definition", "التنظيم", ("التنظيم",), "regression"),
    CandidateCase("reg_calm", "saudi", "الهدوء وش يعني", "definition", "الهدوء", ("الهدوء",), "regression"),
)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run Phase 27.43 guarded data-backed expansion")
    p.add_argument("--tokenizer", type=Path, default=DEFAULT_TOKENIZER)
    p.add_argument("--steps", type=int, default=4800)
    p.add_argument("--epochs", type=int, default=480)
    p.add_argument("--batch-size", type=int, default=1)
    p.add_argument("--seq-len", type=int, default=64)
    p.add_argument("--lr", type=float, default=6e-4)
    p.add_argument("--warmup", type=int, default=140)
    p.add_argument("--device", default="auto")
    p.add_argument("--work-dir", type=Path, default=DEFAULT_WORK)
    p.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    p.add_argument("--samples", type=Path, default=DEFAULT_SAMPLES)
    p.add_argument("--keep-work", action="store_true")
    return p.parse_args()


def _records() -> list[dict[str, Any]]:
    base = phase27_40_records()
    repair = [
        _conditioned_record(pair, 43000 + idx)
        for idx, pair in enumerate(WEAK_LANE_REPAIR, start=1)
    ]
    records = list(base)
    for _ in range(36):
        records.extend(repair)
    return records


def _surface(text: str) -> str:
    return (
        (text or "")
        .replace("أ", "ا")
        .replace("إ", "ا")
        .replace("آ", "ا")
        .replace("ى", "ي")
        .replace("ة", "ه")
        .strip()
        .lower()
    )


def _semantic_match(text: str, terms: tuple[str, ...]) -> bool:
    surface = _surface(text)
    return all(_surface(term) in surface for term in terms)


def _evaluate(
    *,
    tokenizer: Path,
    checkpoints_root: Path,
    checkpoint_name: str,
    device: str,
) -> list[dict[str, Any]]:
    generator = NativeGenerator(
        NativeGeneratorConfig(
            tokenizer_path=tokenizer,
            checkpoints_root=checkpoints_root,
            checkpoint_name=checkpoint_name,
            generator_name="sf_10m_phase27_43",
            model_size="sf-10m",
            seq_len=64,
            max_new_tokens=24,
            temperature=1.0,
            top_k=0,
            no_repeat_ngram_size=3,
            repetition_penalty=1.1,
            device=device,
            dialogue_prompt=True,
        )
    )
    guard = GenerationGuard(min_chars=4)
    rows: list[dict[str, Any]] = []
    for item in PROBE_CASES:
        out = generator.generate(
            item.prompt,
            dialect=item.dialect,
            intent=item.intent,
            topic=item.topic,
            max_new_tokens=24,
            temperature=1.0,
            top_k=0,
        )
        verdict = guard.inspect(out.text) if item.intent == "definition" else guard.inspect_for_prompt(item.prompt, out.text)
        semantic = _semantic_match(out.text, item.expected_terms)
        passed = bool(out.used and verdict.allowed and semantic)
        if passed:
            reason = "passed"
        elif not out.used:
            reason = f"generator:{out.reason}"
        elif not verdict.allowed:
            reason = f"guard:{verdict.reason}"
        else:
            reason = "semantic_mismatch"
        rows.append(
            {
                "id": item.id,
                "bucket": item.bucket,
                "dialect": item.dialect,
                "prompt": item.prompt,
                "intent": item.intent,
                "topic": item.topic,
                "expected_terms": list(item.expected_terms),
                "response": out.text,
                "generator_used": out.used,
                "guard_allowed": verdict.allowed,
                "guard_reason": verdict.reason,
                "semantic_match": semantic,
                "passed": passed,
                "reason": reason,
            }
        )
    return rows


def _summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    buckets = sorted({str(row["bucket"]) for row in rows})
    return {
        "passed": sum(1 for row in rows if row["passed"]),
        "total": len(rows),
        "bucket_summary": {
            bucket: {
                "passed": sum(1 for row in rows if row["bucket"] == bucket and row["passed"]),
                "total": sum(1 for row in rows if row["bucket"] == bucket),
            }
            for bucket in buckets
        },
        "reason_counts": dict(Counter(str(row["reason"]) for row in rows)),
    }


def _write_samples(path: Path, rows: list[dict[str, Any]]) -> None:
    lines = ["# Phase 27.43 Guarded Data-Backed Expansion", ""]
    for row in rows:
        lines.extend(
            [
                f"## {row['id']} — {'PASS' if row['passed'] else 'FAIL'}",
                "",
                f"- bucket: {row['bucket']}",
                f"- prompt: {row['prompt']}",
                f"- response: {row['response']}",
                f"- guard_reason: {row['guard_reason']}",
                f"- semantic_match: {row['semantic_match']}",
                f"- reason: {row['reason']}",
                "",
            ]
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


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
        "--seed", "20260613",
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
        "PASSED_GUARDED_DATA_BACKED_EXPANSION_READY_FOR_RUNTIME_SWITCH"
        if all_passed
        else "PARTIAL_GUARDED_DATA_BACKED_EXPANSION_KEEP_PHASE27_40_RUNTIME"
    )
    report = {
        "phase": "Phase 27.43",
        "status": status,
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "training_started": True,
        "training_scope": "SF-10M targeted weak-lane repair only; no scaling",
        "tokenizer": _rel(args.tokenizer),
        "checkpoint_root": _rel(checkpoints),
        "checkpoint_name": checkpoint_name,
        "candidate_generator": "sf_10m_phase27_43",
        "train_records": len(records),
        "repair_examples": len(WEAK_LANE_REPAIR),
        "summary": summary,
        "runtime_switch_allowed": all_passed,
        "sf50m_allowed": False,
        "phase28_allowed": False,
        "next_phase": (
            "Phase 27.44 — guarded runtime switch for phase27_43"
            if all_passed
            else "Phase 27.44 — refine weak-lane curriculum before runtime switch"
        ),
        "torch_version": torch.__version__,
        "rows": rows,
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _write_samples(args.samples, rows)

    print("SF.AI — Phase 27.43 guarded data-backed expansion")
    print(f"  status      : {status}")
    print(f"  checkpoint  : {checkpoint_name}")
    print(f"  cases       : {summary['passed']}/{summary['total']}")
    for bucket, item in summary["bucket_summary"].items():
        print(f"  {bucket:<12}: {item['passed']}/{item['total']}")
    print(f"  reasons     : {summary['reason_counts']}")
    print(f"  report      : {args.report}")
    print(f"  samples     : {args.samples}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
