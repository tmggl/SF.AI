#!/usr/bin/env python3
"""Phase 27.24 minimal lexical stabilization.

Phase 27.23 reached 30/32 but left two MSA lexical failures:

- "التعاون" -> "التعاعاون"
- "الاحترام" -> "الاحتات..."

This phase avoids broad protection and broad corpus changes. It trains a new
small tokenizer artifact with only the original Phase 27.20 protected phrases
plus the two failing MSA lexical surfaces, then reruns a balanced micro-probe.
The result remains an eval artifact. Runtime stays blocked.
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

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.phase27_17_prompt_answer_micro_probe import (  # noqa: E402
    MSA_PAIRS,
    SAUDI_PAIRS,
    _evaluate,
    _latest_checkpoint_name,
    _record,
)
from scripts.phase27_19_hygiene_repair_probe import _write_probe_corpus  # noqa: E402
from scripts.phase27_23_semantic_lexical_repair import (  # noqa: E402
    SEMANTIC_REPAIR_MSA,
    SEMANTIC_REPAIR_SAUDI,
)
from sf_ai.models.tokenizer import BPETokenizer, TokenizerConfig, train_bpe_from_corpus  # noqa: E402
from sf_ai.models.tokenizer.policy_audit import load_plain_terms  # noqa: E402
from sf_ai.training.train_tiny_lm import run as train_tiny_lm_run  # noqa: E402


DEFAULT_TOKENIZER_OUT = ROOT / "artifacts/tokenizers/sf_bpe/v4_min_lexical"
DEFAULT_PROTECTED = ROOT / "resources/tokenization/protected_phrases_phase27_24.txt"
DEFAULT_WORK = ROOT / "artifacts/eval/phase27_24_minimal_lexical_stabilization"
DEFAULT_PREVIOUS_REPORT = ROOT / "artifacts/reports/phase27_23_semantic_lexical_repair_report.json"
DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_24_minimal_lexical_stabilization_report.json"
DEFAULT_SAMPLES = ROOT / "artifacts/samples/phase27_24_minimal_lexical_stabilization_generations.md"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run Phase 27.24 minimal lexical stabilization")
    p.add_argument("--corpus", type=Path, default=ROOT / "data/corpus/chat/jsonl")
    p.add_argument("--tokenizer-out", type=Path, default=DEFAULT_TOKENIZER_OUT)
    p.add_argument("--protected-phrases", type=Path, default=DEFAULT_PROTECTED)
    p.add_argument("--previous-report", type=Path, default=DEFAULT_PREVIOUS_REPORT)
    p.add_argument("--vocab-size", type=int, default=8000)
    p.add_argument("--min-frequency", type=int, default=2)
    p.add_argument("--steps", type=int, default=5600)
    p.add_argument("--epochs", type=int, default=560)
    p.add_argument("--batch-size", type=int, default=1)
    p.add_argument("--seq-len", type=int, default=64)
    p.add_argument("--lr", type=float, default=8e-4)
    p.add_argument("--warmup", type=int, default=120)
    p.add_argument("--device", default="auto")
    p.add_argument("--work-dir", type=Path, default=DEFAULT_WORK)
    p.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    p.add_argument("--samples", type=Path, default=DEFAULT_SAMPLES)
    p.add_argument("--keep-work", action="store_true")
    return p.parse_args()


def _rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def _record_many(
    dialect: str,
    offset: int,
    rows: tuple[tuple[str, str, tuple[str, ...]], ...],
) -> list[dict[str, Any]]:
    return [_record(dialect, offset + idx, p, a, t) for idx, (p, a, t) in enumerate(rows, start=1)]


def _records() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    eval_records: list[dict[str, Any]] = []
    base_records: list[dict[str, Any]] = []
    for idx, (prompt, answer, terms) in enumerate(MSA_PAIRS, start=1):
        row = _record("msa", idx, prompt, answer, terms)
        eval_records.append(row)
        base_records.append(row)
    for idx, (prompt, answer, terms) in enumerate(SAUDI_PAIRS, start=1):
        row = _record("saudi", idx, prompt, answer, terms)
        eval_records.append(row)
        base_records.append(row)

    train_records: list[dict[str, Any]] = []
    for _ in range(6):
        train_records.extend(base_records)
    for round_idx in range(2):
        base = 500 + (round_idx * 100)
        train_records.extend(_record_many("msa", base, SEMANTIC_REPAIR_MSA))
        train_records.extend(_record_many("saudi", base, SEMANTIC_REPAIR_SAUDI))
    return train_records, eval_records


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
        name="sf_bpe_v4_min_lexical_phase27_24",
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


def _load_previous(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _write_samples(path: Path, results: list[dict[str, Any]]) -> None:
    lines = ["# Phase 27.24 Minimal Lexical Stabilization Generations", ""]
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
    phrases = load_plain_terms(args.protected_phrases)
    tokenizer = _train_tokenizer(args, phrases)
    meta = json.loads((args.tokenizer_out / "meta.json").read_text(encoding="utf-8"))
    tokenizer_rows = _tokenizer_rows(tokenizer, phrases)
    piece_counts = [row["piece_count"] for row in tokenizer_rows]

    train_records, eval_records = _records()
    if args.work_dir.exists() and not args.keep_work:
        shutil.rmtree(args.work_dir)
    corpus_dir = args.work_dir / "corpus"
    checkpoints = args.work_dir / "checkpoints"
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
        "--seed", "20260529",
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
        tokenizer_path=args.tokenizer_out,
    )

    total = len(results)
    passed = sum(1 for item in results if item["passed"])
    exact = sum(1 for item in results if item["exact_clean"])
    semantic = sum(1 for item in results if item["semantic_match"])
    guard = sum(1 for item in results if item["guard_reason"] == "passed")
    previous = _load_previous(args.previous_report).get("current", {})
    previous_passed = int(previous.get("passed", 0) or 0)
    previous_exact = int(previous.get("exact_clean", 0) or 0)
    previous_semantic = int(previous.get("semantic_match", 0) or 0)
    previous_guard = int(previous.get("guard_passed", 0) or 0)
    failure_rows = [row for row in results if not row["passed"]]
    status = (
        "PASSED_MINIMAL_LEXICAL_STABILIZATION_HOLD_RUNTIME_FOR_CANARY"
        if passed == total
        else "PARTIAL_MINIMAL_LEXICAL_STABILIZATION_BLOCK_RUNTIME"
    )

    report = {
        "phase": "Phase 27.24",
        "status": status,
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "tokenizer": {
            "path": _rel(args.tokenizer_out),
            "sf_origin": bool(meta.get("sf_origin")),
            "vocab_size": meta.get("vocab_size"),
            "merges": meta.get("merges"),
            "protected_terms": meta.get("protected_terms", []),
            "protected_joiner": meta.get("protected_joiner"),
        },
        "protected_phrase_behavior": {
            "average_pieces": round(mean(piece_counts), 4) if piece_counts else 0,
            "max_pieces": max(piece_counts, default=0),
            "all_single_piece": all(count == 1 for count in piece_counts),
            "all_roundtrip_ok": all(row["roundtrip_ok"] for row in tokenizer_rows),
            "rows": tokenizer_rows,
        },
        "repair_focus": ["التعاون", "الاحترام"],
        "train_records": len(train_records),
        "eval_records": total,
        "repair_records": len(train_records) - total,
        "training": {
            "steps": args.steps,
            "epochs": args.epochs,
            "batch_size": args.batch_size,
            "seq_len": args.seq_len,
            "lr": args.lr,
            "packing_mode": "sample_isolated",
            "checkpoint_name": checkpoint_name,
            "checkpoint_root": _rel(checkpoints),
        },
        "previous_phase27_23": {
            "passed": previous_passed,
            "exact_clean": previous_exact,
            "semantic_match": previous_semantic,
            "guard_passed": previous_guard,
        },
        "current": {
            "passed": passed,
            "failed": total - passed,
            "pass_rate": round(passed / total, 4) if total else 0.0,
            "exact_clean": exact,
            "semantic_match": semantic,
            "guard_passed": guard,
            "reason_counts": dict(Counter(reasons)),
        },
        "delta": {
            "passed": passed - previous_passed,
            "exact_clean": exact - previous_exact,
            "semantic_match": semantic - previous_semantic,
            "guard_passed": guard - previous_guard,
        },
        "runtime_allowed": False,
        "sf50m_allowed": False,
        "decision": (
            "Micro-probe reached 32/32. Keep runtime blocked until a broader held-out canary passes."
            if passed == total
            else "Minimal lexical stabilization did not fully pass. Keep runtime and SF-50M blocked."
        ),
        "next_phase": (
            "Phase 27.25 — held-out generation-quality canary before any runtime"
            if passed == total
            else "Phase 27.25 — continue lexical/objective stabilization without scaling"
        ),
        "failures": failure_rows,
        "results": results,
    }

    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _write_samples(args.samples, results)

    print("SF.AI — Phase 27.24 minimal lexical stabilization")
    print(f"  status       : {status}")
    print(f"  tokenizer    : {_rel(args.tokenizer_out)}")
    print(f"  checkpoint   : {checkpoint_name}")
    print(f"  train        : {len(train_records)}")
    print(f"  eval         : {total}")
    print(f"  passed       : {passed}/{total} (delta {passed - previous_passed:+d})")
    print(f"  exact_clean  : {exact}/{total} (delta {exact - previous_exact:+d})")
    print(f"  semantic     : {semantic}/{total} (delta {semantic - previous_semantic:+d})")
    print(f"  guard_passed : {guard}/{total} (delta {guard - previous_guard:+d})")
    print(f"  reasons      : {dict(reasons)}")
    print(f"  runtime      : blocked")
    print(f"  report       : {args.report}")
    print(f"  samples      : {args.samples}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
