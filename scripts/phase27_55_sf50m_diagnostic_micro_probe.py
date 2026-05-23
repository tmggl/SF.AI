#!/usr/bin/env python3
"""Phase 27.55 controlled SF-50M diagnostic micro-probe.

This is not a product scaling phase. It trains two random-initialized
sovereign models on the same tiny governed corpus:

- SF-10M baseline
- SF-50M diagnostic candidate

The only intended variable is model capacity. Runtime stays on the previous
generator regardless of the result; this phase only answers: "does capacity
help enough to justify a larger controlled run?"
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import torch

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.phase27_19_hygiene_repair_probe import _write_probe_corpus  # noqa: E402
from scripts.phase27_26_heldout_objective_repair import _rel  # noqa: E402
from scripts.phase27_52_natural_dialogue_objective_repair import (  # noqa: E402
    EVAL_CASES,
    TRAIN_PAIRS,
    _records,
)
from sf_ai.models.tokenizer import BPETokenizer  # noqa: E402
from sf_ai.models.transformer import config_for_size  # noqa: E402
from sf_ai.modules.chat.generation_guard import GenerationGuard  # noqa: E402
from sf_ai.modules.chat.native_generator import NativeGenerator, NativeGeneratorConfig  # noqa: E402
from sf_ai.training.train_tiny_lm import run as train_tiny_lm_run  # noqa: E402


DEFAULT_TOKENIZER = ROOT / "artifacts/tokenizers/sf_bpe/v6_weak_lane_terms"
DEFAULT_WORK = ROOT / "artifacts/eval/phase27_55_sf50m_diagnostic_micro_probe"
DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_55_sf50m_diagnostic_micro_probe_report.json"
DEFAULT_SAMPLES = ROOT / "artifacts/samples/phase27_55_sf50m_diagnostic_micro_probe.md"

_TOKEN_RE = re.compile(r"[\w\u0600-\u06FF]+", re.UNICODE)
_CANNED_PHRASES = (
    "اكتب ثلاث مهام",
    "ابدأ بالأهم",
    "الله يعافيك",
    "حاضر بأي وقت",
    "الصداقة رفقة طيبة",
    "الصدق أن تقول الحقيقة",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Phase 27.55 SF-50M diagnostic micro-probe")
    parser.add_argument("--tokenizer", type=Path, default=DEFAULT_TOKENIZER)
    parser.add_argument("--steps", type=int, default=700)
    parser.add_argument("--epochs", type=int, default=700)
    parser.add_argument("--batch-size", type=int, default=1)
    parser.add_argument("--seq-len", type=int, default=64)
    parser.add_argument("--lr-10m", type=float, default=4.5e-4)
    parser.add_argument("--lr-50m", type=float, default=2.8e-4)
    parser.add_argument("--warmup", type=int, default=80)
    parser.add_argument("--device", default="auto")
    parser.add_argument("--work-dir", type=Path, default=DEFAULT_WORK)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--samples", type=Path, default=DEFAULT_SAMPLES)
    parser.add_argument("--keep-work", action="store_true")
    return parser.parse_args()


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


def _token_set(text: str) -> set[str]:
    return set(_TOKEN_RE.findall(_surface(text)))


def _overlap_ratio(prompt: str, response: str) -> float:
    p = _token_set(prompt)
    r = _token_set(response)
    if not p or not r:
        return 0.0
    return len(p & r) / max(1, len(p))


def _has_canned_phrase(text: str) -> bool:
    surface = _surface(text)
    return any(_surface(phrase) in surface for phrase in _CANNED_PHRASES)


def _has_any_expected(text: str, terms: tuple[str, ...]) -> bool:
    if not terms:
        return True
    surface = _surface(text)
    return any(_surface(term) in surface for term in terms)


def _forbidden_absent(text: str, terms: tuple[str, ...]) -> bool:
    surface = _surface(text)
    return not any(_surface(term) in surface for term in terms)


def _train_one(
    *,
    model_size: str,
    tokenizer: Path,
    corpus_dir: Path,
    checkpoints: Path,
    steps: int,
    epochs: int,
    batch_size: int,
    seq_len: int,
    lr: float,
    warmup: int,
    device: str,
    seed: int,
) -> str:
    train_args = [
        "--tokenizer", str(tokenizer),
        "--corpus", str(corpus_dir),
        "--size", model_size,
        "--steps", str(steps),
        "--epochs", str(epochs),
        "--batch-size", str(batch_size),
        "--seq-len", str(seq_len),
        "--stream-format", "dialogue",
        "--loss-scope", "assistant",
        "--packing-mode", "sample_isolated",
        "--lr", str(lr),
        "--warmup", str(warmup),
        "--min-lr", "1e-5",
        "--save-every", str(steps),
        "--seed", str(seed),
        "--checkpoints", str(checkpoints),
        "--device", device,
    ]
    train_code = train_tiny_lm_run(train_args)
    if train_code != 0:
        raise RuntimeError(f"{model_size} training failed with code {train_code}")
    return _latest_checkpoint_name_for_size(checkpoints, model_size)


def _latest_checkpoint_name_for_size(checkpoints_root: Path, model_size: str) -> str:
    steps: list[tuple[int, str]] = []
    for path in checkpoints_root.glob(f"{model_size}-step*"):
        try:
            step = int(path.name.rsplit("step", 1)[1])
        except (IndexError, ValueError):
            continue
        if (path / "meta.json").exists() and (path / "state.pt").exists():
            steps.append((step, path.name))
    if not steps:
        raise RuntimeError(f"no saved {model_size} checkpoints under {checkpoints_root}")
    return sorted(steps)[-1][1]


def _evaluate(
    *,
    tokenizer: Path,
    checkpoints_root: Path,
    checkpoint_name: str,
    generator_name: str,
    model_size: str,
    device: str,
    seq_len: int,
) -> list[dict[str, Any]]:
    generator = NativeGenerator(
        NativeGeneratorConfig(
            tokenizer_path=tokenizer,
            checkpoints_root=checkpoints_root,
            checkpoint_name=checkpoint_name,
            generator_name=generator_name,
            model_size=model_size,
            seq_len=seq_len,
            max_new_tokens=36,
            temperature=1.0,
            top_k=0,
            no_repeat_ngram_size=3,
            repetition_penalty=1.1,
            device=device,
            dialogue_prompt=True,
        )
    )
    guard = GenerationGuard(min_chars=4, max_repetition_ratio=0.42)
    rows: list[dict[str, Any]] = []
    for item in EVAL_CASES:
        out = generator.generate(
            item.prompt,
            dialect=item.dialect,
            intent=None,
            topic=None,
            max_new_tokens=36,
            temperature=1.0,
            top_k=0,
        )
        verdict = guard.inspect(out.text)
        expected_ok = _has_any_expected(out.text, item.expected_terms)
        forbidden_ok = _forbidden_absent(out.text, item.forbidden_terms)
        canned = _has_canned_phrase(out.text)
        overlap = _overlap_ratio(item.prompt, out.text)
        overlap_ok = overlap >= item.min_overlap
        passed = bool(
            out.used
            and verdict.allowed
            and expected_ok
            and forbidden_ok
            and not canned
            and overlap_ok
        )
        if passed:
            reason = "passed"
        elif not out.used:
            reason = f"generator:{out.reason}"
        elif not verdict.allowed:
            reason = f"guard:{verdict.reason}"
        elif not expected_ok:
            reason = "expected_terms_missing"
        elif not forbidden_ok:
            reason = "forbidden_terms_present"
        elif canned:
            reason = "canned_phrase"
        else:
            reason = f"low_prompt_overlap:{overlap:.2f}"
        rows.append(
            {
                "id": item.id,
                "bucket": item.category,
                "dialect": item.dialect,
                "prompt": item.prompt,
                "expected_terms": list(item.expected_terms),
                "forbidden_terms": list(item.forbidden_terms),
                "response": out.text,
                "generator_used": out.used,
                "guard_allowed": verdict.allowed,
                "guard_reason": verdict.reason,
                "expected_ok": expected_ok,
                "forbidden_ok": forbidden_ok,
                "canned_phrase": canned,
                "prompt_overlap": round(overlap, 4),
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


def _param_counts(tokenizer_path: Path, seq_len: int) -> dict[str, int]:
    tok = BPETokenizer.load(tokenizer_path)
    return {
        size: config_for_size(size, vocab_size=len(tok), max_seq_len=seq_len).d_model
        for size in ("sf-10m", "sf-50m")
    }


def _model_params(tokenizer_path: Path, seq_len: int) -> dict[str, int]:
    from sf_ai.models.transformer import TinyTransformer

    tok = BPETokenizer.load(tokenizer_path)
    out: dict[str, int] = {}
    for size in ("sf-10m", "sf-50m"):
        cfg = config_for_size(size, vocab_size=len(tok), max_seq_len=seq_len)
        out[size] = TinyTransformer(cfg).num_parameters()
    return out


def _write_samples(path: Path, rows_by_model: dict[str, list[dict[str, Any]]]) -> None:
    lines = ["# Phase 27.55 SF-50M Diagnostic Micro-Probe", ""]
    for model_name, rows in rows_by_model.items():
        summary = _summary(rows)
        lines.extend([f"## {model_name} — {summary['passed']}/{summary['total']}", ""])
        for row in rows:
            lines.extend(
                [
                    f"### {row['id']} — {'PASS' if row['passed'] else 'FAIL'}",
                    "",
                    f"- bucket: {row['bucket']}",
                    f"- dialect: {row['dialect']}",
                    f"- prompt: {row['prompt']}",
                    f"- response: {row['response'] or '(empty)'}",
                    f"- overlap: {row['prompt_overlap']}",
                    f"- reason: {row['reason']}",
                    "",
                ]
            )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_doc(report: dict[str, Any]) -> None:
    path = ROOT / "docs/PHASE27_55_SF50M_DIAGNOSTIC_MICRO_PROBE_REPORT.md"
    comp = report["comparison"]
    lines = [
        "# Phase 27.55 — Controlled SF-50M Diagnostic Micro-Probe",
        "",
        "## الخلاصة",
        "",
        "هذه مرحلة تشخيصية فقط. لم تفتح الواجهة ولم تغيّر runtime.",
        "",
        f"- `SF-10M`: {comp['sf-10m']['passed']}/{comp['sf-10m']['total']}",
        f"- `SF-50M`: {comp['sf-50m']['passed']}/{comp['sf-50m']['total']}",
        f"- delta: {comp['delta_passed']}",
        "",
        "## القرار",
        "",
        f"- runtime switch: `{str(report['runtime_switch_allowed']).lower()}`",
        f"- full SF-50M training: `{str(report['sf50m_full_training_allowed']).lower()}`",
        f"- diagnostic continuation: `{str(report['sf50m_diagnostic_continuation_allowed']).lower()}`",
        "",
        "## المعنى",
        "",
        report["decision_notes"],
        "",
        "## artifacts",
        "",
        f"- JSON report: `{_rel(DEFAULT_REPORT)}`",
        f"- Samples: `{_rel(DEFAULT_SAMPLES)}`",
        f"- Checkpoints are local under `{report['checkpoint_root']}` and must not be pushed.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    args = parse_args()
    if not (args.tokenizer / "meta.json").exists():
        print(f"error: missing tokenizer at {args.tokenizer}; run Phase 27.44 first", file=sys.stderr)
        return 1
    if args.work_dir.exists() and not args.keep_work:
        shutil.rmtree(args.work_dir)

    corpus_dir = args.work_dir / "corpus"
    ckpt10 = args.work_dir / "checkpoints_sf10m"
    ckpt50 = args.work_dir / "checkpoints_sf50m"
    records = _records()
    _write_probe_corpus(corpus_dir, records)

    print("SF.AI — Phase 27.55 controlled SF-50M diagnostic micro-probe")
    print(f"  train records : {len(records)} from {len(TRAIN_PAIRS)} unique pairs")
    print(f"  steps         : {args.steps} each")
    print("  runtime       : unchanged; no switch")
    print("")

    ckpt10_name = _train_one(
        model_size="sf-10m",
        tokenizer=args.tokenizer,
        corpus_dir=corpus_dir,
        checkpoints=ckpt10,
        steps=args.steps,
        epochs=args.epochs,
        batch_size=args.batch_size,
        seq_len=args.seq_len,
        lr=args.lr_10m,
        warmup=args.warmup,
        device=args.device,
        seed=20260619,
    )
    rows10 = _evaluate(
        tokenizer=args.tokenizer,
        checkpoints_root=ckpt10,
        checkpoint_name=ckpt10_name,
        generator_name="sf_10m_phase27_55_baseline",
        model_size="sf-10m",
        device=args.device,
        seq_len=args.seq_len,
    )
    summary10 = _summary(rows10)

    ckpt50_name = _train_one(
        model_size="sf-50m",
        tokenizer=args.tokenizer,
        corpus_dir=corpus_dir,
        checkpoints=ckpt50,
        steps=args.steps,
        epochs=args.epochs,
        batch_size=args.batch_size,
        seq_len=args.seq_len,
        lr=args.lr_50m,
        warmup=args.warmup,
        device=args.device,
        seed=20260619,
    )
    rows50 = _evaluate(
        tokenizer=args.tokenizer,
        checkpoints_root=ckpt50,
        checkpoint_name=ckpt50_name,
        generator_name="sf_50m_phase27_55_diagnostic",
        model_size="sf-50m",
        device=args.device,
        seq_len=args.seq_len,
    )
    summary50 = _summary(rows50)

    delta = int(summary50["passed"]) - int(summary10["passed"])
    diagnostic_helped = delta >= 4 and int(summary50["passed"]) >= 10
    strong_enough_for_full = int(summary50["passed"]) >= 16 and delta >= 6
    status = (
        "PASSED_DIAGNOSTIC_CAPACITY_SIGNAL_CONTINUE_BOUNDED_SF50M"
        if diagnostic_helped
        else "FAILED_DIAGNOSTIC_CAPACITY_SIGNAL_KEEP_SF50M_FULL_BLOCKED"
    )
    decision_notes = (
        "السعة أعطت إشارة تشخيصية مفيدة، لكنها لا تجعل النموذج جاهزًا للواجهة. "
        "يمكن للمرحلة التالية متابعة إصلاح هدف SF-50M بحدود واضحة وبوابة held-out أقسى."
        if diagnostic_helped
        else "التشخيص لم يثبت أن السعة وحدها تحل الحوار المفتوح. يجب إصلاح objective/format/tokenization أو إعادة تصميم التشخيص قبل أي تدريب SF-50M كامل."
    )

    params = _model_params(args.tokenizer, args.seq_len)
    report = {
        "phase": "Phase 27.55",
        "status": status,
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "training_started": True,
        "training_scope": "bounded diagnostic micro-probe only; not full SF-50M scaling",
        "progressive_scaling_respected": True,
        "template_answers_allowed": False,
        "tokenizer": _rel(args.tokenizer),
        "checkpoint_root": _rel(args.work_dir),
        "train_records": len(records),
        "unique_train_pairs": len(TRAIN_PAIRS),
        "eval_cases": len(EVAL_CASES),
        "training_budget": {
            "steps_each": args.steps,
            "epochs": args.epochs,
            "batch_size": args.batch_size,
            "seq_len": args.seq_len,
            "lr_10m": args.lr_10m,
            "lr_50m": args.lr_50m,
            "warmup": args.warmup,
        },
        "models": {
            "sf-10m": {
                "checkpoint_name": ckpt10_name,
                "params": params["sf-10m"],
                "summary": summary10,
            },
            "sf-50m": {
                "checkpoint_name": ckpt50_name,
                "params": params["sf-50m"],
                "summary": summary50,
            },
        },
        "comparison": {
            "sf-10m": {"passed": summary10["passed"], "total": summary10["total"]},
            "sf-50m": {"passed": summary50["passed"], "total": summary50["total"]},
            "delta_passed": delta,
            "diagnostic_capacity_signal": diagnostic_helped,
            "strong_enough_for_full_sf50m": strong_enough_for_full,
        },
        "runtime_switch_allowed": False,
        "sf50m_full_training_allowed": strong_enough_for_full,
        "sf50m_diagnostic_continuation_allowed": diagnostic_helped,
        "phase28_allowed": False,
        "decision_notes": decision_notes,
        "next_phase": (
            "Phase 27.56 — bounded SF-50M objective repair with stronger held-out suite"
            if diagnostic_helped
            else "Phase 27.56 — objective/format/tokenizer diagnosis before another capacity attempt"
        ),
        "torch_version": torch.__version__,
        "rows": {
            "sf-10m": rows10,
            "sf-50m": rows50,
        },
    }

    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _write_samples(args.samples, {"sf-10m": rows10, "sf-50m": rows50})
    _write_doc(report)

    print("SF.AI — Phase 27.55 result")
    print(f"  status       : {status}")
    print(f"  sf-10m       : {summary10['passed']}/{summary10['total']} ({ckpt10_name})")
    print(f"  sf-50m       : {summary50['passed']}/{summary50['total']} ({ckpt50_name})")
    print(f"  delta        : {delta}")
    print(f"  runtime      : blocked")
    print(f"  full sf-50m  : {'allowed' if strong_enough_for_full else 'blocked'}")
    print(f"  report       : {args.report}")
    print(f"  samples      : {args.samples}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
