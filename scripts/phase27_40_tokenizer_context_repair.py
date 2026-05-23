#!/usr/bin/env python3
"""Phase 27.40 tokenizer/context repair for topic isolation.

Phase 27.39 improved topic collapse but exposed lexical fractures in the new
definition topics. This phase trains a new sovereign tokenizer artifact with
the failed topic surfaces protected, then reruns a less topic-heavy context
probe so social/advice lanes are not crushed by definition examples.
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
from scripts.phase27_26_heldout_objective_repair import _rel  # noqa: E402
from scripts.phase27_33_advice_micro_stabilization import _records as phase27_33_records  # noqa: E402
from scripts.phase27_39_topic_isolation_repair import (  # noqa: E402
    BALANCED_TOPIC_REPAIR,
    PROBE_CASES,
    TOPIC_STEMS,
    _conditioned_record,
    _semantic_match,
    _topic_isolated,
)
from sf_ai.models.tokenizer import BPETokenizer, TokenizerConfig, train_bpe_from_corpus  # noqa: E402
from sf_ai.models.tokenizer.policy_audit import load_plain_terms  # noqa: E402
from sf_ai.modules.chat.generation_guard import GenerationGuard  # noqa: E402
from sf_ai.modules.chat.native_generator import NativeGenerator, NativeGeneratorConfig  # noqa: E402
from sf_ai.training.train_tiny_lm import run as train_tiny_lm_run  # noqa: E402


DEFAULT_TOKENIZER_OUT = ROOT / "artifacts/tokenizers/sf_bpe/v5_topic_terms"
DEFAULT_PROTECTED = ROOT / "resources/tokenization/protected_phrases_phase27_40.txt"
DEFAULT_WORK = ROOT / "artifacts/eval/phase27_40_tokenizer_context_repair"
DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_40_tokenizer_context_repair_report.json"
DEFAULT_SAMPLES = ROOT / "artifacts/samples/phase27_40_tokenizer_context_repair.md"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run Phase 27.40 tokenizer/context repair")
    p.add_argument("--corpus", type=Path, default=ROOT / "data/corpus/chat/jsonl")
    p.add_argument("--tokenizer-out", type=Path, default=DEFAULT_TOKENIZER_OUT)
    p.add_argument("--protected-phrases", type=Path, default=DEFAULT_PROTECTED)
    p.add_argument("--vocab-size", type=int, default=8000)
    p.add_argument("--min-frequency", type=int, default=2)
    p.add_argument("--steps", type=int, default=6400)
    p.add_argument("--epochs", type=int, default=640)
    p.add_argument("--batch-size", type=int, default=1)
    p.add_argument("--seq-len", type=int, default=64)
    p.add_argument("--lr", type=float, default=6e-4)
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
        name="sf_bpe_v5_topic_terms_phase27_40",
    )


def _tokenizer_rows(tokenizer: BPETokenizer, phrases: list[str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for phrase in phrases:
        ids = tokenizer.encode(phrase)
        decoded = tokenizer.decode(ids)
        rows.append(
            {
                "phrase": phrase,
                "piece_count": len(ids),
                "decoded": decoded,
                "roundtrip_ok": decoded == phrase,
            }
        )
    return rows


def _records() -> list[dict[str, Any]]:
    phase27_33_train, micro_records, _repair_records = phase27_33_records()
    topic_records = [
        _conditioned_record(pair, idx)
        for idx, pair in enumerate(BALANCED_TOPIC_REPAIR, start=1)
    ]
    train_records = list(phase27_33_train)
    for _ in range(2):
        train_records.extend(micro_records)
    for _ in range(42):
        train_records.extend(topic_records)
    return train_records


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
            generator_name="sf_10m_phase27_40",
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
        verdict = (
            guard.inspect(out.text)
            if item.intent == "definition"
            else guard.inspect_for_prompt(item.prompt, out.text)
        )
        semantic = _semantic_match(out.text, item.expected_terms)
        isolated, forbidden_topics = _topic_isolated(out.text, item.topic)
        passed = bool(out.used and verdict.allowed and semantic and isolated)
        if passed:
            reason = "passed"
        elif not out.used:
            reason = f"generator:{out.reason}"
        elif not verdict.allowed:
            reason = f"guard:{verdict.reason}"
        elif not semantic:
            reason = "semantic_mismatch"
        else:
            reason = "topic_leakage"
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
                "topic_isolated": isolated,
                "forbidden_topics": forbidden_topics,
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
    lines = ["# Phase 27.40 Tokenizer/Context Repair", ""]
    for row in rows:
        lines.extend(
            [
                f"## {row['id']} — {'PASS' if row['passed'] else 'FAIL'}",
                "",
                f"- bucket: {row['bucket']}",
                f"- prompt: {row['prompt']}",
                f"- topic: {row['topic'] or '-'}",
                f"- response: {row['response']}",
                f"- semantic_match: {row['semantic_match']}",
                f"- topic_isolated: {row['topic_isolated']}",
                f"- forbidden_topics: {', '.join(row['forbidden_topics']) if row['forbidden_topics'] else '-'}",
                f"- reason: {row['reason']}",
                "",
            ]
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


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
    train_records = _records()
    _write_probe_corpus(corpus_dir, train_records)

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
        "--seed", "20260610",
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
        "PASSED_TOKENIZER_CONTEXT_REPAIR_READY_FOR_GUARDED_RUNTIME_CANDIDATE"
        if all_passed
        else "PARTIAL_TOKENIZER_CONTEXT_REPAIR_KEEP_CURRENT_RUNTIME"
    )
    report = {
        "phase": "Phase 27.40",
        "status": status,
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "training_started": True,
        "training_scope": "SF-10M tokenizer/context repair only; no scaling",
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
        "candidate_generator": "sf_10m_phase27_40",
        "train_records": len(train_records),
        "balanced_topics": sorted(TOPIC_STEMS),
        "summary": summary,
        "runtime_switch_allowed": all_passed,
        "sf50m_allowed": False,
        "phase28_allowed": False,
        "next_phase": (
            "Phase 27.41 — guarded runtime switch design for phase27_40 candidate"
            if all_passed
            else "Phase 27.41 — objective balance repair after tokenizer v5"
        ),
        "torch_version": torch.__version__,
        "rows": rows,
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _write_samples(args.samples, rows)

    print("SF.AI — Phase 27.40 tokenizer/context repair")
    print(f"  status      : {status}")
    print(f"  tokenizer   : {_rel(args.tokenizer_out)}")
    print(f"  max_pieces  : {max(piece_counts, default=0)}")
    print(f"  checkpoint  : {checkpoint_name}")
    print(f"  cases       : {summary['passed']}/{summary['total']}")
    for bucket, item in summary["bucket_summary"].items():
        print(f"  {bucket:<10}: {item['passed']}/{item['total']}")
    print(f"  reasons     : {summary['reason_counts']}")
    print(f"  report      : {args.report}")
    print(f"  samples     : {args.samples}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
