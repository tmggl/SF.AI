#!/usr/bin/env python3
"""Phase 27.11 — objective/decoding overfit probe.

This is not a production training phase. It builds a tiny gold-only corpus from
the owner-authored Phase 27.10 repair batch, trains SF-10M briefly, then checks
whether the checkpoint can reproduce simple MSA/Saudi replies from that same
micro-corpus.

If this fails, scaling to SF-50M is still blocked: the next fix belongs in the
training objective, packing, or decoding path rather than model size.
"""

from __future__ import annotations

import argparse
import json
import shutil
from collections import Counter
from pathlib import Path
from typing import Any

from sf_ai.modules.chat.generation_guard import GenerationGuard
from sf_ai.modules.chat.native_generator import NativeGenerator, NativeGeneratorConfig
from sf_ai.training.train_tiny_lm import run as train_tiny_lm_run


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_WORK = ROOT / "artifacts/eval/phase27_11_objective_probe"
DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_11_objective_probe_report.json"
DEFAULT_SAMPLES = ROOT / "artifacts/samples/phase27_11_objective_probe_generations.md"
V8_MSA = ROOT / "data/corpus/chat/jsonl/dialogue_batch_v8_short_repair_msa_008.jsonl"
V8_SAUDI = ROOT / "data/corpus/chat/jsonl/dialogue_batch_v8_short_repair_saudi_008.jsonl"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run Phase 27.11 objective/decoding probe")
    p.add_argument("--records-per-dialect", type=int, default=8)
    p.add_argument("--steps", type=int, default=1000)
    p.add_argument("--epochs", type=int, default=200)
    p.add_argument("--batch-size", type=int, default=1)
    p.add_argument("--seq-len", type=int, default=64)
    p.add_argument("--lr", type=float, default=8e-4)
    p.add_argument("--warmup", type=int, default=50)
    p.add_argument("--device", default="auto")
    p.add_argument("--work-dir", type=Path, default=DEFAULT_WORK)
    p.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    p.add_argument("--samples", type=Path, default=DEFAULT_SAMPLES)
    p.add_argument("--keep-work", action="store_true")
    return p.parse_args()


def _load_records(path: Path, limit: int) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        raw = json.loads(line)
        prov = raw.get("provenance", {})
        if prov.get("training_allowed") is not True:
            continue
        if prov.get("quality") != "gold":
            continue
        records.append(raw)
        if len(records) >= limit:
            break
    return records


def _write_probe_corpus(corpus_dir: Path, records: list[dict[str, Any]]) -> Path:
    corpus_dir.mkdir(parents=True, exist_ok=True)
    out = corpus_dir / "phase27_11_gold_probe.jsonl"
    out.write_text(
        "\n".join(json.dumps(record, ensure_ascii=False) for record in records) + "\n",
        encoding="utf-8",
    )
    return out


def _messages(record: dict[str, Any]) -> tuple[str, str]:
    user = ""
    assistant = ""
    for msg in record.get("messages", ()):
        if msg.get("role") == "user" and not user:
            user = str(msg.get("content", "")).strip()
        if msg.get("role") == "assistant" and not assistant:
            assistant = str(msg.get("content", "")).strip()
    return user, assistant


def _expected_terms(answer: str) -> tuple[str, ...]:
    tokens = [
        token.strip("،.؟!؛: ")
        for token in answer.split()
        if len(token.strip("،.؟!؛: ")) >= 3
    ]
    return tuple(tokens[:3])


def _surface(text: str) -> str:
    return " ".join((text or "").replace("ـ", "").split()).strip(" .،؟!؛:")


def _exact_or_clean_stop(generated: str, expected: str) -> bool:
    """Probe criterion: memorizing the start is not enough; it must stop cleanly."""
    g = _surface(generated)
    e = _surface(expected)
    if not g or not e:
        return False
    if g == e:
        return True
    if g.startswith(e):
        extra = g[len(e):].strip(" .،؟!؛:")
        return len(extra) <= 6
    return False


def _evaluate(
    *,
    records: list[dict[str, Any]],
    checkpoints_root: Path,
    checkpoint_name: str,
    device: str,
) -> tuple[list[dict[str, Any]], Counter[str]]:
    generator = NativeGenerator(
        NativeGeneratorConfig(
            tokenizer_path=ROOT / "artifacts/tokenizers/sf_bpe/v2",
            checkpoints_root=checkpoints_root,
            checkpoint_name=checkpoint_name,
            generator_name="sf_10m_phase27_11_probe",
            model_size="sf-10m",
            seq_len=64,
            max_new_tokens=24,
            temperature=1.0,
            top_k=0,
            device=device,
            dialogue_prompt=True,
        )
    )
    guard = GenerationGuard(min_chars=4)
    results: list[dict[str, Any]] = []
    reasons: Counter[str] = Counter()
    for idx, record in enumerate(records):
        prompt, expected = _messages(record)
        out = generator.generate(prompt, max_new_tokens=24, temperature=1.0, top_k=0)
        verdict = guard.inspect_for_prompt(prompt, out.text)
        terms = _expected_terms(expected)
        term_hit = any(term in out.text for term in terms) if terms else False
        clean_stop = _exact_or_clean_stop(out.text, expected)
        passed = bool(out.used and verdict.allowed and clean_stop)
        if passed:
            reason = "passed"
        elif not verdict.allowed:
            reason = f"guard:{verdict.reason}"
        elif term_hit:
            reason = "overgenerates_after_expected"
        else:
            reason = "missing_expected_terms"
        reasons[reason] += 1
        results.append(
            {
                "id": idx,
                "dialect": record.get("provenance", {}).get("dialect", ""),
                "prompt": prompt,
                "expected": expected,
                "generated": out.text,
                "used": out.used,
                "generator_reason": out.reason,
                "guard_reason": verdict.reason,
                "expected_terms": list(terms),
                "clean_stop": clean_stop,
                "passed": passed,
                "reason": reason,
            }
        )
    return results, reasons


def _latest_checkpoint_name(checkpoints_root: Path) -> str:
    steps: list[tuple[int, str]] = []
    for path in checkpoints_root.glob("sf-10m-step*"):
        try:
            step = int(path.name.rsplit("step", 1)[1])
        except (IndexError, ValueError):
            continue
        if (path / "meta.json").exists() and (path / "state.pt").exists():
            steps.append((step, path.name))
    if not steps:
        raise RuntimeError(f"no saved probe checkpoints under {checkpoints_root}")
    return sorted(steps)[-1][1]


def _write_samples(path: Path, results: list[dict[str, Any]]) -> None:
    lines = ["# Phase 27.11 Objective Probe Generations", ""]
    for item in results:
        lines.extend(
            [
                f"## {item['id']} — {item['dialect']} — {'PASS' if item['passed'] else 'FAIL'}",
                "",
                f"- prompt: {item['prompt']}",
                f"- expected: {item['expected']}",
                f"- generated: {item['generated']}",
                f"- reason: {item['reason']}",
                "",
            ]
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    args = parse_args()
    records = _load_records(V8_MSA, args.records_per_dialect) + _load_records(
        V8_SAUDI,
        args.records_per_dialect,
    )
    if not records:
        raise SystemExit("no probe records found")

    if args.work_dir.exists() and not args.keep_work:
        shutil.rmtree(args.work_dir)
    corpus_dir = args.work_dir / "corpus"
    checkpoints = args.work_dir / "checkpoints"
    _write_probe_corpus(corpus_dir, records)

    train_args = [
        "--tokenizer", str(ROOT / "artifacts/tokenizers/sf_bpe/v2"),
        "--corpus", str(corpus_dir),
        "--size", "sf-10m",
        "--steps", str(args.steps),
        "--epochs", str(args.epochs),
        "--batch-size", str(args.batch_size),
        "--seq-len", str(args.seq_len),
        "--loss-scope", "assistant",
        "--lr", str(args.lr),
        "--warmup", str(args.warmup),
        "--min-lr", "1e-5",
        "--save-every", str(args.steps),
        "--seed", "20260524",
        "--checkpoints", str(checkpoints),
        "--device", args.device,
    ]
    train_code = train_tiny_lm_run(train_args)
    if train_code != 0:
        return train_code

    checkpoint_name = _latest_checkpoint_name(checkpoints)
    results, reasons = _evaluate(
        records=records,
        checkpoints_root=checkpoints,
        checkpoint_name=checkpoint_name,
        device=args.device,
    )
    passed = sum(1 for item in results if item["passed"])
    total = len(results)
    status = (
        "PASSED_GOLD_OVERFIT_PROBE"
        if passed == total
        else "FAILED_GOLD_OVERFIT_PROBE_BLOCK_SCALING"
    )
    report = {
        "phase": "Phase 27.11 — Objective/Decoding Diagnosis",
        "status": status,
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "records": total,
        "records_per_dialect": args.records_per_dialect,
        "steps": args.steps,
        "checkpoint_name": checkpoint_name,
        "passed": passed,
        "failed": total - passed,
        "pass_rate": round(passed / total, 4) if total else 0.0,
        "reason_counts": dict(reasons),
        "decision": (
            "Do not scale to SF-50M; fix objective/packing/decoding first."
            if passed != total
            else "Overfit path can work; compare broader corpus packing next."
        ),
        "results": results,
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _write_samples(args.samples, results)

    print("SF.AI — Phase 27.11 objective/decoding probe")
    print(f"  status       : {status}")
    print(f"  checkpoint   : {checkpoint_name}")
    print(f"  records      : {total}")
    print(f"  passed       : {passed}/{total}")
    print(f"  pass_rate    : {passed / total:.2%}" if total else "  pass_rate    : 0.00%")
    print(f"  reasons      : {dict(reasons)}")
    print(f"  report       : {args.report}")
    print(f"  samples      : {args.samples}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
