#!/usr/bin/env python3
"""Phase 27.26 held-out objective repair and generalization training.

Phase 27.25 proved that Phase 27.24's 32/32 micro-probe success did not
generalize enough. This phase trains on *families* around the failed held-out
categories without copying the held-out prompts verbatim, then reruns:

1. The Phase 27.25 held-out canary.
2. The 32-pair Phase 27 micro-probe as a regression check.

Runtime remains blocked unless both checks pass cleanly.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.phase27_17_prompt_answer_micro_probe import (  # noqa: E402
    MSA_PAIRS,
    SAUDI_PAIRS,
    _evaluate as evaluate_micro_probe,
    _latest_checkpoint_name,
    _record,
    _semantic_match,
    _surface,
)
from scripts.phase27_19_hygiene_repair_probe import _write_probe_corpus  # noqa: E402
from scripts.phase27_25_heldout_generation_canary import HELDOUT_PROMPTS  # noqa: E402
from sf_ai.modules.chat.generation_guard import GenerationGuard  # noqa: E402
from sf_ai.modules.chat.native_generator import NativeGenerator, NativeGeneratorConfig  # noqa: E402
from sf_ai.training.train_tiny_lm import run as train_tiny_lm_run  # noqa: E402


DEFAULT_TOKENIZER = ROOT / "artifacts/tokenizers/sf_bpe/v4_min_lexical"
DEFAULT_WORK = ROOT / "artifacts/eval/phase27_26_heldout_objective_repair"
DEFAULT_PREVIOUS_REPORT = ROOT / "artifacts/reports/phase27_25_heldout_generation_canary_report.json"
DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_26_heldout_objective_repair_report.json"
DEFAULT_SAMPLES = ROOT / "artifacts/samples/phase27_26_heldout_objective_repair_generations.md"


@dataclass(frozen=True)
class RepairPair:
    dialect: str
    prompt: str
    answer: str
    expected_terms: tuple[str, ...]
    category: str


HELDOUT_REPAIR_MSA: tuple[RepairPair, ...] = (
    RepairPair("msa", "أعطني تحية مختصرة", "أهلًا بك، تفضل.", ("أهلًا",), "greeting"),
    RepairPair("msa", "ابدأ بتحية قصيرة", "أهلًا بك، كيف أقدر أساعدك؟", ("أهلًا",), "greeting"),
    RepairPair("msa", "سلّم علي باختصار", "أهلًا بك.", ("أهلًا",), "greeting"),
    RepairPair("msa", "كيف أنت اليوم", "بخير، شكرًا لسؤالك.", ("بخير",), "smalltalk"),
    RepairPair("msa", "كيف حالك هذا المساء", "بخير، شكرًا لسؤالك.", ("بخير",), "smalltalk"),
    RepairPair("msa", "طمئني عن حالك", "بخير، شكرًا لسؤالك.", ("بخير",), "smalltalk"),
    RepairPair("msa", "أريد توجيهًا بسيطًا", "ابدأ بخطوة واضحة وصغيرة.", ("ابدأ", "خطوة"), "advice"),
    RepairPair("msa", "انصحني بشيء بسيط", "ابدأ بخطوة صغيرة ثم أكمل.", ("ابدأ", "خطوة"), "advice"),
    RepairPair("msa", "ما النصيحة الأولى", "ابدأ بخطوة واحدة واضحة.", ("ابدأ", "خطوة"), "advice"),
    RepairPair("msa", "أريد تنظيم يومي", "اكتب ثلاث مهام وابدأ بالأهم.", ("ثلاث", "مهام"), "planning"),
    RepairPair("msa", "ساعدني أرتب مهامي", "اكتب ثلاث مهام وابدأ بالأهم.", ("ثلاث", "مهام"), "planning"),
    RepairPair("msa", "كيف أنظم وقتي اليوم", "اختر ثلاث مهام وابدأ بالأقرب.", ("ثلاث", "مهام"), "planning"),
    RepairPair("msa", "أنا قلق قليلًا", "خذ نفسًا هادئًا واهدأ خطوة خطوة.", ("نفس", "اهدأ"), "support"),
    RepairPair("msa", "أحس بقلق بسيط", "خذ نفسًا هادئًا واهدأ قليلًا.", ("نفس", "اهدأ"), "support"),
    RepairPair("msa", "أريد تهدئة بسيطة", "خذ نفسًا هادئًا واهدأ الآن.", ("نفس", "اهدأ"), "support"),
)


HELDOUT_REPAIR_SAUDI: tuple[RepairPair, ...] = (
    RepairPair("saudi", "هلا وش عندك", "هلا بك، تفضل وش تحتاج؟", ("هلا", "تحتاج"), "greeting"),
    RepairPair("saudi", "هلا ابدأ معي", "هلا بك، تفضل وش تحتاج؟", ("هلا", "تحتاج"), "greeting"),
    RepairPair("saudi", "سلّم علي بالسعودي", "هلا بك، تفضل وش تحتاج؟", ("هلا", "تحتاج"), "greeting"),
    RepairPair("saudi", "ابي توجيه سريع", "ابدأ بشي بسيط وواضح.", ("ابدأ", "بسيط"), "advice"),
    RepairPair("saudi", "انصحني بسرعة", "ابدأ بشي بسيط ولا تكثرها.", ("ابدأ", "بسيط"), "advice"),
    RepairPair("saudi", "وش أول نصيحة", "ابدأ بشي بسيط وتدرّج.", ("ابدأ", "بسيط"), "advice"),
    RepairPair("saudi", "ابي أنظم يومي", "اكتب أهم ثلاث أشياء وابدأ بالأول.", ("ثلاث", "الأول"), "planning"),
    RepairPair("saudi", "ساعدني ارتب يومي", "اكتب أهم ثلاث أشياء وابدأ بالأول.", ("ثلاث", "الأول"), "planning"),
    RepairPair("saudi", "وش أسوي بمهامي اليوم", "حدد ثلاث أشياء وابدأ بالأول.", ("ثلاث", "الأول"), "planning"),
    RepairPair("saudi", "قلقان شوي", "الله يهونها، خذ نفس واهدأ شوي.", ("يهونها", "اهدأ"), "support"),
    RepairPair("saudi", "حاس بتوتر بسيط", "الله يهونها، خذ نفس واهدأ شوي.", ("يهونها", "اهدأ"), "support"),
    RepairPair("saudi", "ابي أهدأ شوي", "الله يهونها، خذ نفس واهدأ شوي.", ("يهونها", "اهدأ"), "support"),
)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run Phase 27.26 held-out objective repair")
    p.add_argument("--tokenizer", type=Path, default=DEFAULT_TOKENIZER)
    p.add_argument("--previous-report", type=Path, default=DEFAULT_PREVIOUS_REPORT)
    p.add_argument("--steps", type=int, default=7200)
    p.add_argument("--epochs", type=int, default=720)
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


def _load_previous(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _has_prompt_echo(prompt: str, generated: str) -> bool:
    p = _surface(prompt)
    g = _surface(generated)
    return bool(p and (g == p or g.startswith(f"{p} ")))


def _micro_records() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for idx, (prompt, answer, terms) in enumerate(MSA_PAIRS, start=1):
        records.append(_record("msa", idx, prompt, answer, terms))
    for idx, (prompt, answer, terms) in enumerate(SAUDI_PAIRS, start=1):
        records.append(_record("saudi", idx, prompt, answer, terms))
    return records


def _repair_record(pair: RepairPair, idx: int) -> dict[str, Any]:
    return {
        "id": f"phase27_26_{pair.dialect}_{idx:03d}",
        "messages": [
            {"role": "user", "content": pair.prompt},
            {"role": "assistant", "content": pair.answer},
        ],
        "expected_terms": list(pair.expected_terms),
        "provenance": {
            "source": f"sf-ai-phase27-26-heldout-objective-repair-{pair.dialect}",
            "license": "owner-delegated-internal-sf-ai",
            "training_allowed": True,
            "quality": "gold",
            "dialect": pair.dialect,
            "owner_user_id": "sami-local",
            "created_by_user_id": "sf-ai-agent",
            "target_user_id": "sami-local",
            "user_scope": "single_user",
            "synthetic_llm_data": False,
            "notes": (
                "internal held-out family repair; excludes exact Phase 27.25 "
                "held-out prompts; not public corpus expansion"
            ),
        },
    }


def _records() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    micro = _micro_records()
    repair_pairs = list(HELDOUT_REPAIR_MSA) + list(HELDOUT_REPAIR_SAUDI)
    repair_records = [_repair_record(pair, idx) for idx, pair in enumerate(repair_pairs, start=1)]

    train_records: list[dict[str, Any]] = []
    for _ in range(6):
        train_records.extend(micro)
    for _ in range(6):
        train_records.extend(repair_records)
    return train_records, micro, repair_records


def _evaluate_heldout(
    *,
    tokenizer: Path,
    checkpoints_root: Path,
    checkpoint_name: str,
    device: str,
) -> tuple[list[dict[str, Any]], Counter[str]]:
    generator = NativeGenerator(
        NativeGeneratorConfig(
            tokenizer_path=tokenizer,
            checkpoints_root=checkpoints_root,
            checkpoint_name=checkpoint_name,
            generator_name="sf_10m_phase27_26_heldout_objective_repair",
            model_size="sf-10m",
            seq_len=64,
            max_new_tokens=24,
            temperature=1.0,
            top_k=0,
            no_repeat_ngram_size=3,
            repetition_penalty=1.08,
            device=device,
            dialogue_prompt=True,
        )
    )
    guard = GenerationGuard(min_chars=4)
    rows: list[dict[str, Any]] = []
    reasons: Counter[str] = Counter()
    for item in HELDOUT_PROMPTS:
        out = generator.generate(
            item.prompt,
            dialect=item.dialect,
            max_new_tokens=24,
            temperature=1.0,
            top_k=0,
        )
        verdict = guard.inspect_for_prompt(item.prompt, out.text)
        semantic = _semantic_match(out.text, item.expected_terms)
        prompt_echo = _has_prompt_echo(item.prompt, out.text)
        passed = bool(out.used and verdict.allowed and semantic and not prompt_echo)
        if passed:
            reason = "passed"
        elif not out.used:
            reason = f"generator:{out.reason}"
        elif not verdict.allowed:
            reason = f"guard:{verdict.reason}"
        elif prompt_echo:
            reason = "prompt_echo"
        else:
            reason = "missing_semantic_terms"
        reasons[reason] += 1
        rows.append(
            {
                "id": item.id,
                "dialect": item.dialect,
                "category": item.category,
                "prompt": item.prompt,
                "expected_terms": list(item.expected_terms),
                "generated": out.text,
                "used": out.used,
                "generator_reason": out.reason,
                "guard_reason": verdict.reason,
                "semantic_match": semantic,
                "prompt_echo": prompt_echo,
                "passed": passed,
                "reason": reason,
            }
        )
    return rows, reasons


def _summarize_heldout(rows: list[dict[str, Any]], reasons: Counter[str]) -> dict[str, Any]:
    total = len(rows)
    categories: dict[str, dict[str, int]] = {}
    for row in rows:
        bucket = categories.setdefault(str(row["category"]), {"passed": 0, "total": 0})
        bucket["total"] += 1
        bucket["passed"] += int(bool(row["passed"]))
    passed = sum(1 for row in rows if row["passed"])
    return {
        "passed": passed,
        "failed": total - passed,
        "eval_records": total,
        "pass_rate": round(passed / total, 4) if total else 0.0,
        "semantic_match": sum(1 for row in rows if row["semantic_match"]),
        "guard_passed": sum(1 for row in rows if row["guard_reason"] == "passed"),
        "reason_counts": dict(Counter(reasons)),
        "category_breakdown": categories,
    }


def _summarize_micro(rows: list[dict[str, Any]], reasons: Counter[str]) -> dict[str, Any]:
    total = len(rows)
    passed = sum(1 for row in rows if row["passed"])
    return {
        "passed": passed,
        "failed": total - passed,
        "eval_records": total,
        "pass_rate": round(passed / total, 4) if total else 0.0,
        "exact_clean": sum(1 for row in rows if row["exact_clean"]),
        "semantic_match": sum(1 for row in rows if row["semantic_match"]),
        "guard_passed": sum(1 for row in rows if row["guard_reason"] == "passed"),
        "reason_counts": dict(Counter(reasons)),
    }


def _write_samples(path: Path, heldout: list[dict[str, Any]], micro: list[dict[str, Any]]) -> None:
    lines = ["# Phase 27.26 Held-out Objective Repair Generations", ""]
    lines.append("## Held-out Canary")
    lines.append("")
    for item in heldout:
        lines.extend(
            [
                f"### {item['id']} — {item['dialect']} — {item['category']} — {'PASS' if item['passed'] else 'FAIL'}",
                "",
                f"- prompt: {item['prompt']}",
                f"- expected_terms: {', '.join(item['expected_terms'])}",
                f"- generated: {item['generated']}",
                f"- guard_reason: {item['guard_reason']}",
                f"- semantic_match: {item['semantic_match']}",
                f"- reason: {item['reason']}",
                "",
            ]
        )
    lines.append("## Micro-Probe Regression")
    lines.append("")
    for item in micro:
        lines.extend(
            [
                f"### {item['id']} — {item['dialect']} — {'PASS' if item['passed'] else 'FAIL'}",
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
    if not (args.tokenizer / "meta.json").exists():
        print(f"error: missing tokenizer at {args.tokenizer}", file=sys.stderr)
        return 1
    if args.work_dir.exists() and not args.keep_work:
        shutil.rmtree(args.work_dir)

    train_records, micro_records, repair_records = _records()
    corpus_dir = args.work_dir / "corpus"
    checkpoints = args.work_dir / "checkpoints"
    _write_probe_corpus(corpus_dir, train_records)

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
        "--seed", "20260530",
        "--checkpoints", str(checkpoints),
        "--device", args.device,
    ]
    train_code = train_tiny_lm_run(train_args)
    if train_code != 0:
        return train_code

    checkpoint_name = _latest_checkpoint_name(checkpoints)
    heldout_rows, heldout_reasons = _evaluate_heldout(
        tokenizer=args.tokenizer,
        checkpoints_root=checkpoints,
        checkpoint_name=checkpoint_name,
        device=args.device,
    )
    micro_rows, micro_reasons = evaluate_micro_probe(
        records=micro_records,
        checkpoints_root=checkpoints,
        checkpoint_name=checkpoint_name,
        device=args.device,
        tokenizer_path=args.tokenizer,
    )

    heldout_summary = _summarize_heldout(heldout_rows, heldout_reasons)
    micro_summary = _summarize_micro(micro_rows, micro_reasons)
    previous_current = _load_previous(args.previous_report).get("current", {})
    previous_passed = int(previous_current.get("passed", 0) or 0)
    heldout_total = int(heldout_summary["eval_records"])
    micro_total = int(micro_summary["eval_records"])
    runtime_allowed = (
        heldout_summary["passed"] == heldout_total
        and micro_summary["passed"] == micro_total
    )
    status = (
        "PASSED_HELDOUT_OBJECTIVE_REPAIR_READY_FOR_RUNTIME_TRIAL_DESIGN"
        if runtime_allowed
        else "PARTIAL_HELDOUT_OBJECTIVE_REPAIR_BLOCK_RUNTIME"
    )

    repair_prompts = {row["messages"][0]["content"] for row in repair_records}
    heldout_prompts = {item.prompt for item in HELDOUT_PROMPTS}
    exact_leakage = sorted(repair_prompts & heldout_prompts)

    report = {
        "phase": "Phase 27.26",
        "status": status,
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "tokenizer": _rel(args.tokenizer),
        "checkpoint_root": _rel(checkpoints),
        "checkpoint_name": checkpoint_name,
        "previous_phase27_25": {
            "passed": previous_passed,
            "eval_records": int(previous_current.get("eval_records", 0) or 0),
            "semantic_match": int(previous_current.get("semantic_match", 0) or 0),
            "guard_passed": int(previous_current.get("guard_passed", 0) or 0),
        },
        "training": {
            "steps": args.steps,
            "epochs": args.epochs,
            "batch_size": args.batch_size,
            "seq_len": args.seq_len,
            "lr": args.lr,
            "packing_mode": "sample_isolated",
            "train_records": len(train_records),
            "micro_records_repeated": len(micro_records) * 6,
            "repair_records_repeated": len(repair_records) * 6,
            "exact_heldout_prompt_leakage": exact_leakage,
        },
        "repair_categories": dict(Counter(pair.category for pair in (HELDOUT_REPAIR_MSA + HELDOUT_REPAIR_SAUDI))),
        "heldout": heldout_summary,
        "micro_probe_regression": micro_summary,
        "delta": {
            "heldout_passed": int(heldout_summary["passed"]) - previous_passed,
        },
        "runtime_allowed": runtime_allowed,
        "limited_runtime_trial_allowed": runtime_allowed,
        "sf50m_allowed": False,
        "decision": (
            "Held-out and micro-probe passed. Design a guarded limited runtime trial next."
            if runtime_allowed
            else "Held-out repair improved/ran but did not clear gates. Keep templates as runtime brain."
        ),
        "next_phase": (
            "Phase 27.27 — guarded limited runtime trial design"
            if runtime_allowed
            else "Phase 27.27 — broader held-out repair without scaling"
        ),
        "repair_pairs": [asdict(pair) for pair in (HELDOUT_REPAIR_MSA + HELDOUT_REPAIR_SAUDI)],
        "failures": {
            "heldout": [row for row in heldout_rows if not row["passed"]],
            "micro_probe": [row for row in micro_rows if not row["passed"]],
        },
        "results": {
            "heldout": heldout_rows,
            "micro_probe": micro_rows,
        },
    }

    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _write_samples(args.samples, heldout_rows, micro_rows)

    print("SF.AI — Phase 27.26 held-out objective repair")
    print(f"  status        : {status}")
    print(f"  tokenizer     : {_rel(args.tokenizer)}")
    print(f"  checkpoint    : {checkpoint_name}")
    print(f"  heldout       : {heldout_summary['passed']}/{heldout_total}")
    print(f"  micro_probe   : {micro_summary['passed']}/{micro_total}")
    print(f"  leakage       : {exact_leakage or 'none'}")
    print("  runtime       : " + ("trial-design-ready" if runtime_allowed else "blocked"))
    print(f"  report        : {args.report}")
    print(f"  samples       : {args.samples}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
