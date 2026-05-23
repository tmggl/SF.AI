#!/usr/bin/env python3
"""Phase 27.44 tokenizer/curriculum repair for weak-lane stability.

Phase 27.43 showed that adding examples alone can destabilize the generator.
This phase trains tokenizer v6 with the newly weak surfaces protected, then
uses a balanced curriculum that gives social/planning lanes enough weight
without drowning them in definition topics.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from collections import Counter
from pathlib import Path
from statistics import mean
from typing import Any

import torch

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.phase27_17_prompt_answer_micro_probe import _latest_checkpoint_name  # noqa: E402
from scripts.phase27_19_hygiene_repair_probe import _write_probe_corpus  # noqa: E402
from scripts.phase27_26_heldout_objective_repair import RepairPair, _rel  # noqa: E402
from scripts.phase27_33_advice_micro_stabilization import _records as phase27_33_records  # noqa: E402
from scripts.phase27_39_topic_isolation_repair import (  # noqa: E402
    BALANCED_TOPIC_REPAIR,
    _conditioned_record,
)
from scripts.phase27_43_guarded_data_backed_expansion import (  # noqa: E402
    PROBE_CASES,
    WEAK_LANE_REPAIR,
    _evaluate,
    _summary,
    _write_samples,
)
from sf_ai.models.tokenizer import BPETokenizer, TokenizerConfig, train_bpe_from_corpus  # noqa: E402
from sf_ai.models.tokenizer.policy_audit import load_plain_terms  # noqa: E402
from sf_ai.training.train_tiny_lm import run as train_tiny_lm_run  # noqa: E402


DEFAULT_TOKENIZER_OUT = ROOT / "artifacts/tokenizers/sf_bpe/v6_weak_lane_terms"
DEFAULT_PROTECTED = ROOT / "resources/tokenization/protected_phrases_phase27_44.txt"
DEFAULT_WORK = ROOT / "artifacts/eval/phase27_44_tokenizer_curriculum_repair"
DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_44_tokenizer_curriculum_repair_report.json"
DEFAULT_SAMPLES = ROOT / "artifacts/samples/phase27_44_tokenizer_curriculum_repair.md"


BALANCED_SOCIAL_REPAIR: tuple[RepairPair, ...] = (
    RepairPair("saudi", "وش اخبارك", "بخير ولله الحمد، وش أخبارك أنت؟", ("بخير",), "smalltalk"),
    RepairPair("saudi", "وش أخبارك اليوم", "بخير ولله الحمد، أنت كيفك؟", ("بخير",), "smalltalk"),
    RepairPair("saudi", "علومك", "بخير ولله الحمد. وش ودك نسولف عنه؟", ("بخير",), "smalltalk"),
    RepairPair("saudi", "كيفك اليوم", "بخير ولله الحمد، أنت كيفك؟", ("بخير",), "smalltalk"),
    RepairPair("msa", "كيف حالك اليوم", "بخير، شكرًا لسؤالك.", ("بخير",), "smalltalk"),
    RepairPair("msa", "مشكور", "العفو، حاضر بأي وقت.", ("العفو",), "thanks"),
    RepairPair("msa", "تسلم", "العفو، يسعدني أساعدك.", ("العفو",), "thanks"),
    RepairPair("saudi", "يعطيك العافية", "الله يعافيك، حاضر بأي وقت.", ("يعافيك",), "thanks"),
)

BALANCED_PLANNING_REPAIR: tuple[RepairPair, ...] = (
    RepairPair("msa", "نظم وقتي", "اكتب ثلاث مهام وابدأ بالأهم.", ("مهام", "الأهم"), "planning"),
    RepairPair("msa", "كيف ارتب مهامي", "اكتب ثلاث مهام وابدأ بالأهم.", ("مهام", "الأهم"), "planning"),
    RepairPair("saudi", "ابي ارتب اولوياتي", "ابدأ بالأهم ثم انتقل للي بعده.", ("ابدأ", "الأهم"), "planning"),
    RepairPair("msa", "رتب أولوياتي", "اكتب أولوياتك ثم ابدأ بالأهم.", ("أولويات", "الأهم"), "planning"),
    RepairPair("saudi", "ابي انظم يومي", "اكتب ثلاث مهام وابدأ بالأهم.", ("مهام", "الأهم"), "planning"),
)

NEW_TOPIC_REPAIR: tuple[RepairPair, ...] = (
    RepairPair("msa", "ما معنى الوفاء", "الوفاء أن تحفظ الود وتثبت مع من تثق به.", ("الوفاء",), "definition"),
    RepairPair("saudi", "الوفاء وش يعني", "الوفاء إنك تحفظ المعروف وتوقف مع اللي تثق فيه.", ("الوفاء",), "definition"),
    RepairPair("msa", "اشرح الوفاء بجملة", "الوفاء ثبات في الود وحفظ للعهد.", ("الوفاء",), "definition"),
    RepairPair("msa", "اشرح الشجاعة", "الشجاعة أن تفعل الصواب رغم الخوف.", ("الشجاعة",), "definition"),
    RepairPair("saudi", "الشجاعة وش تعني", "الشجاعة إنك تواجه الصح حتى لو كنت خايف.", ("الشجاعة",), "definition"),
    RepairPair("msa", "ما معنى الشجاعة", "الشجاعة ثبات على الصواب وقت الخوف.", ("الشجاعة",), "definition"),
)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run Phase 27.44 tokenizer/curriculum repair")
    p.add_argument("--corpus", type=Path, default=ROOT / "data/corpus/chat/jsonl")
    p.add_argument("--tokenizer-out", type=Path, default=DEFAULT_TOKENIZER_OUT)
    p.add_argument("--protected-phrases", type=Path, default=DEFAULT_PROTECTED)
    p.add_argument("--vocab-size", type=int, default=8000)
    p.add_argument("--min-frequency", type=int, default=2)
    p.add_argument("--steps", type=int, default=5600)
    p.add_argument("--epochs", type=int, default=560)
    p.add_argument("--batch-size", type=int, default=1)
    p.add_argument("--seq-len", type=int, default=64)
    p.add_argument("--lr", type=float, default=5.5e-4)
    p.add_argument("--warmup", type=int, default=160)
    p.add_argument("--device", default="auto")
    p.add_argument("--work-dir", type=Path, default=DEFAULT_WORK)
    p.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    p.add_argument("--samples", type=Path, default=DEFAULT_SAMPLES)
    p.add_argument("--keep-work", action="store_true")
    return p.parse_args()


def _train_tokenizer(args: argparse.Namespace, phrases: list[str]) -> BPETokenizer:
    if args.tokenizer_out.exists():
        shutil.rmtree(args.tokenizer_out)
    cfg = TokenizerConfig(
        vocab_size=args.vocab_size,
        min_frequency=args.min_frequency,
        protected_terms=tuple(phrases),
    )
    return train_bpe_from_corpus(
        corpus_root=args.corpus,
        output_dir=args.tokenizer_out,
        config=cfg,
        extra_texts=phrases * 4,
        name="sf_bpe_v6_weak_lane_terms_phase27_44",
    )


def _tokenizer_rows(tokenizer: BPETokenizer, phrases: list[str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for phrase in phrases:
        ids = tokenizer.encode(phrase)
        rows.append(
            {
                "phrase": phrase,
                "piece_count": len(ids),
                "decoded": tokenizer.decode(ids),
                "roundtrip_ok": tokenizer.decode(ids) == phrase,
            }
        )
    return rows


def _records() -> list[dict[str, Any]]:
    base_train, micro_records, _repair_records = phase27_33_records()
    topic_records = [
        _conditioned_record(pair, 44000 + idx)
        for idx, pair in enumerate(BALANCED_TOPIC_REPAIR, start=1)
    ]
    weak_records = [
        _conditioned_record(pair, 45000 + idx)
        for idx, pair in enumerate(WEAK_LANE_REPAIR, start=1)
    ]
    social_records = [
        _conditioned_record(pair, 46000 + idx)
        for idx, pair in enumerate(BALANCED_SOCIAL_REPAIR, start=1)
    ]
    planning_records = [
        _conditioned_record(pair, 47000 + idx)
        for idx, pair in enumerate(BALANCED_PLANNING_REPAIR, start=1)
    ]
    new_topic_records = [
        _conditioned_record(pair, 48000 + idx)
        for idx, pair in enumerate(NEW_TOPIC_REPAIR, start=1)
    ]

    records: list[dict[str, Any]] = []
    records.extend(base_train)
    for _ in range(2):
        records.extend(micro_records)
    for _ in range(10):
        records.extend(topic_records)
    for _ in range(26):
        records.extend(weak_records)
    for _ in range(30):
        records.extend(social_records)
    for _ in range(26):
        records.extend(planning_records)
    for _ in range(24):
        records.extend(new_topic_records)
    return records


def main() -> int:
    args = parse_args()
    phrases = load_plain_terms(args.protected_phrases)
    tokenizer = _train_tokenizer(args, phrases)
    tokenizer_rows = _tokenizer_rows(tokenizer, phrases)
    piece_counts = [row["piece_count"] for row in tokenizer_rows]
    tokenizer_meta = json.loads((args.tokenizer_out / "meta.json").read_text(encoding="utf-8"))

    if args.work_dir.exists() and not args.keep_work:
        shutil.rmtree(args.work_dir)
    corpus_dir = args.work_dir / "corpus"
    checkpoints = args.work_dir / "checkpoints"
    records = _records()
    _write_probe_corpus(corpus_dir, records)

    train_args = [
        "--tokenizer", str(args.tokenizer_out),
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
        "--seed", "20260614",
        "--checkpoints", str(checkpoints),
        "--device", args.device,
    ]
    train_code = train_tiny_lm_run(train_args)
    if train_code != 0:
        return train_code

    checkpoint_name = _latest_checkpoint_name(checkpoints)
    rows = _evaluate(
        tokenizer=args.tokenizer_out,
        checkpoints_root=checkpoints,
        checkpoint_name=checkpoint_name,
        device=args.device,
    )
    summary = _summary(rows)
    all_passed = summary["passed"] == summary["total"]
    status = (
        "PASSED_TOKENIZER_CURRICULUM_REPAIR_READY_FOR_GUARDED_SWITCH"
        if all_passed
        else "PARTIAL_TOKENIZER_CURRICULUM_REPAIR_KEEP_PHASE27_40_RUNTIME"
    )
    report = {
        "phase": "Phase 27.44",
        "status": status,
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "training_started": True,
        "training_scope": "SF-10M tokenizer/curriculum repair only; no scaling",
        "tokenizer": {
            "path": _rel(args.tokenizer_out),
            "sf_origin": bool(tokenizer_meta.get("sf_origin")),
            "vocab_size": tokenizer_meta.get("vocab_size"),
            "merges": tokenizer_meta.get("merges"),
            "protected_terms": tokenizer_meta.get("protected_terms", []),
            "protected_joiner": tokenizer_meta.get("protected_joiner"),
        },
        "protected_phrase_behavior": {
            "average_pieces": round(mean(piece_counts), 4) if piece_counts else 0,
            "max_pieces": max(piece_counts, default=0),
            "all_single_piece": all(count == 1 for count in piece_counts),
            "all_roundtrip_ok": all(row["roundtrip_ok"] for row in tokenizer_rows),
            "rows": tokenizer_rows,
        },
        "checkpoint_root": _rel(checkpoints),
        "checkpoint_name": checkpoint_name,
        "candidate_generator": "sf_10m_phase27_44",
        "train_records": len(records),
        "summary": summary,
        "runtime_switch_allowed": all_passed,
        "sf50m_allowed": False,
        "phase28_allowed": False,
        "next_phase": (
            "Phase 27.45 — guarded runtime switch for phase27_44"
            if all_passed
            else "Phase 27.45 — inspect remaining weak-lane blockers"
        ),
        "torch_version": torch.__version__,
        "rows": rows,
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _write_samples(args.samples, rows)

    print("SF.AI — Phase 27.44 tokenizer/curriculum repair")
    print(f"  status      : {status}")
    print(f"  tokenizer   : {_rel(args.tokenizer_out)}")
    print(f"  max_pieces  : {max(piece_counts, default=0)}")
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
