#!/usr/bin/env python3
"""Phase 27.33 advice + micro stabilization.

Phase 27.32 passed most semantic shadows, but advice prompts drifted into
thanks responses and the exact micro-probe regressed to 29/32. This phase uses
a narrower repair: more micro repetition, less thanks-heavy natural data, and
extra advice variants that do not copy the fresh mixed canary prompts.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.phase27_17_prompt_answer_micro_probe import (  # noqa: E402
    _evaluate as evaluate_micro_probe,
    _latest_checkpoint_name,
)
from scripts.phase27_19_hygiene_repair_probe import _write_probe_corpus  # noqa: E402
from scripts.phase27_26_heldout_objective_repair import (  # noqa: E402
    HELDOUT_REPAIR_MSA,
    HELDOUT_REPAIR_SAUDI,
    RepairPair,
    _micro_records,
    _rel,
    _summarize_heldout,
    _summarize_micro,
)
from scripts.phase27_27_broader_heldout_repair import EXACT_REPAIR, SHADOW_CANARY  # noqa: E402
from scripts.phase27_29_topic_conditioned_definition_repair import DEFINITION_REPAIR, DEFINITION_SHADOW  # noqa: E402
from scripts.phase27_30_fresh_mixed_shadow_canary import FRESH_MIXED_CANARY  # noqa: E402
from scripts.phase27_31_natural_intent_topic_dataset import (  # noqa: E402
    NATURAL_INTENT_REPAIR,
    NATURAL_SHADOW_CANARY,
    NaturalPrompt,
    _conditioned_record,
    _evaluate_prompts,
    _heldout_as_canary,
    _prompt_set,
    _write_samples,
)
from scripts.phase27_32_balanced_natural_calibration import (  # noqa: E402
    BALANCED_CALIBRATION_REPAIR,
    CALIBRATION_SHADOW_CANARY,
)
from sf_ai.training.train_tiny_lm import run as train_tiny_lm_run  # noqa: E402


DEFAULT_TOKENIZER = ROOT / "artifacts/tokenizers/sf_bpe/v4_min_lexical"
DEFAULT_WORK = ROOT / "artifacts/eval/phase27_33_advice_micro_stabilization"
DEFAULT_PREVIOUS_REPORT = ROOT / "artifacts/reports/phase27_32_balanced_natural_calibration_report.json"
DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_33_advice_micro_stabilization_report.json"
DEFAULT_SAMPLES = ROOT / "artifacts/samples/phase27_33_advice_micro_stabilization_generations.md"


ADVICE_STABILIZATION_REPAIR: tuple[RepairPair, ...] = (
    RepairPair("msa", "دلني على خطوة بسيطة", "ابدأ بخطوة صغيرة وواضحة.", ("ابدأ", "خطوة"), "advice"),
    RepairPair("msa", "أحتاج توجيهًا خفيفًا", "ابدأ بخطوة صغيرة وواضحة.", ("ابدأ", "خطوة"), "advice"),
    RepairPair("msa", "ما أول خطوة تنصحني بها", "ابدأ بخطوة واحدة واضحة.", ("ابدأ", "خطوة"), "advice"),
    RepairPair("msa", "أعطني بداية سهلة", "ابدأ بخطوة صغيرة ثم أكمل.", ("ابدأ", "خطوة"), "advice"),
    RepairPair("msa", "أريد نصيحة عملية قصيرة", "ابدأ بخطوة صغيرة وواضحة.", ("ابدأ", "خطوة"), "advice"),
    RepairPair("saudi", "عطني توجيه خفيف", "ابدأ بشي بسيط وتدرّج.", ("ابدأ", "بسيط"), "advice"),
    RepairPair("saudi", "وش نصيحة بسيطة", "ابدأ بشي بسيط ولا تكثرها.", ("ابدأ", "بسيط"), "advice"),
    RepairPair("saudi", "أبي خطوة بسيطة", "ابدأ بشي بسيط وواضح.", ("ابدأ", "بسيط"), "advice"),
    RepairPair("saudi", "دلني على بداية سهلة", "ابدأ بشي بسيط وتدرّج.", ("ابدأ", "بسيط"), "advice"),
    RepairPair("saudi", "وش أول خطوة أسويها", "ابدأ بشي بسيط ولا تكثرها.", ("ابدأ", "بسيط"), "advice"),
)


ADVICE_SHADOW_CANARY: tuple[NaturalPrompt, ...] = (
    NaturalPrompt("phase27_33_msa_001", "msa", "انصحني بخطوة سهلة", ("ابدأ", "خطوة"), "advice"),
    NaturalPrompt("phase27_33_msa_002", "msa", "وجهني بجملة قصيرة", ("ابدأ", "خطوة"), "advice"),
    NaturalPrompt("phase27_33_saudi_001", "saudi", "وش تنصحني أسوي", ("ابدأ", "بسيط"), "advice"),
    NaturalPrompt("phase27_33_saudi_002", "saudi", "عطني بداية خفيفة", ("ابدأ", "بسيط"), "advice"),
)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run Phase 27.33 advice + micro stabilization")
    p.add_argument("--tokenizer", type=Path, default=DEFAULT_TOKENIZER)
    p.add_argument("--previous-report", type=Path, default=DEFAULT_PREVIOUS_REPORT)
    p.add_argument("--steps", type=int, default=9800)
    p.add_argument("--epochs", type=int, default=980)
    p.add_argument("--batch-size", type=int, default=1)
    p.add_argument("--seq-len", type=int, default=64)
    p.add_argument("--lr", type=float, default=7e-4)
    p.add_argument("--warmup", type=int, default=180)
    p.add_argument("--device", default="auto")
    p.add_argument("--work-dir", type=Path, default=DEFAULT_WORK)
    p.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    p.add_argument("--samples", type=Path, default=DEFAULT_SAMPLES)
    p.add_argument("--keep-work", action="store_true")
    return p.parse_args()


def _load_previous(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _records() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    micro = _micro_records()
    base_pairs = list(EXACT_REPAIR) + list(HELDOUT_REPAIR_MSA) + list(HELDOUT_REPAIR_SAUDI)
    definition_pairs = list(DEFINITION_REPAIR)
    natural_pairs = list(NATURAL_INTENT_REPAIR)
    balanced_pairs = list(BALANCED_CALIBRATION_REPAIR)
    advice_pairs = list(ADVICE_STABILIZATION_REPAIR)

    base_records = [_conditioned_record(pair, 1000 + idx) for idx, pair in enumerate(base_pairs, start=1)]
    definition_records = [_conditioned_record(pair, 3000 + idx) for idx, pair in enumerate(definition_pairs, start=1)]
    natural_records = [_conditioned_record(pair, 5000 + idx) for idx, pair in enumerate(natural_pairs, start=1)]
    balanced_records = [_conditioned_record(pair, 7000 + idx) for idx, pair in enumerate(balanced_pairs, start=1)]
    advice_records = [_conditioned_record(pair, 9000 + idx) for idx, pair in enumerate(advice_pairs, start=1)]

    train_records: list[dict[str, Any]] = []
    for _ in range(8):
        train_records.extend(micro)
    for _ in range(5):
        train_records.extend(base_records)
    for _ in range(7):
        train_records.extend(definition_records)
    for _ in range(3):
        train_records.extend(natural_records)
    for _ in range(9):
        train_records.extend(balanced_records)
    for _ in range(18):
        train_records.extend(advice_records)
    return train_records, micro, base_records + definition_records + natural_records + balanced_records + advice_records


def _all_pass(summary: dict[str, Any]) -> bool:
    return int(summary["passed"]) == int(summary["eval_records"])


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
        "--seed", "20260606",
        "--checkpoints", str(checkpoints),
        "--device", args.device,
    ]
    train_code = train_tiny_lm_run(train_args)
    if train_code != 0:
        return train_code

    checkpoint_name = _latest_checkpoint_name(checkpoints)
    eval_kwargs = {
        "tokenizer": args.tokenizer,
        "checkpoints_root": checkpoints,
        "checkpoint_name": checkpoint_name,
        "device": args.device,
    }
    groups = {
        "heldout_27_25": _evaluate_prompts(prompts=_heldout_as_canary(), **eval_kwargs),
        "shadow_27_27": _evaluate_prompts(prompts=SHADOW_CANARY, **eval_kwargs),
        "definition_shadow_27_29": _evaluate_prompts(prompts=DEFINITION_SHADOW, **eval_kwargs),
        "fresh_mixed_shadow_27_30": _evaluate_prompts(prompts=FRESH_MIXED_CANARY, **eval_kwargs),
        "natural_shadow_27_31": _evaluate_prompts(prompts=NATURAL_SHADOW_CANARY, **eval_kwargs),
        "calibration_shadow_27_32": _evaluate_prompts(prompts=CALIBRATION_SHADOW_CANARY, **eval_kwargs),
        "advice_shadow_27_33": _evaluate_prompts(prompts=ADVICE_SHADOW_CANARY, **eval_kwargs),
    }
    micro_rows, micro_reasons = evaluate_micro_probe(
        records=micro_records,
        checkpoints_root=checkpoints,
        checkpoint_name=checkpoint_name,
        device=args.device,
        tokenizer_path=args.tokenizer,
    )
    summaries = {name: _summarize_heldout(rows, reasons) for name, (rows, reasons) in groups.items()}
    summaries["micro_probe_regression"] = _summarize_micro(micro_rows, micro_reasons)

    repair_prompts = _prompt_set(repair_records)
    leakage = {
        "fresh_mixed_prompt_leakage": sorted(repair_prompts & {item.prompt for item in FRESH_MIXED_CANARY}),
        "natural_shadow_prompt_leakage": sorted(repair_prompts & {item.prompt for item in NATURAL_SHADOW_CANARY}),
        "calibration_shadow_prompt_leakage": sorted(repair_prompts & {item.prompt for item in CALIBRATION_SHADOW_CANARY}),
        "advice_shadow_prompt_leakage": sorted(repair_prompts & {item.prompt for item in ADVICE_SHADOW_CANARY}),
    }
    runtime_allowed = all(_all_pass(summary) for summary in summaries.values()) and not any(leakage.values())
    previous = _load_previous(args.previous_report)
    status = (
        "PASSED_ADVICE_MICRO_STABILIZATION_READY_FOR_GUARDED_TRIAL_DESIGN"
        if runtime_allowed
        else "PARTIAL_ADVICE_MICRO_STABILIZATION_BLOCK_RUNTIME"
    )
    rows_by_name = {name: rows for name, (rows, _reasons) in groups.items()}
    report = {
        "phase": "Phase 27.33",
        "status": status,
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "tokenizer": _rel(args.tokenizer),
        "checkpoint_root": _rel(checkpoints),
        "checkpoint_name": checkpoint_name,
        "previous_phase27_32": {
            "status": previous.get("status", ""),
            "fresh_mixed_passed": int(previous.get("fresh_mixed_shadow_27_30", {}).get("passed", 0) or 0),
            "micro_probe_passed": int(previous.get("micro_probe_regression", {}).get("passed", 0) or 0),
        },
        "conditioning": {
            "dialect_line": True,
            "intent_line": True,
            "topic_line_for_definitions": True,
        },
        "training": {
            "steps": args.steps,
            "epochs": args.epochs,
            "batch_size": args.batch_size,
            "seq_len": args.seq_len,
            "lr": args.lr,
            "packing_mode": "sample_isolated",
            "train_records": len(train_records),
            "repair_records": len(repair_records),
            "advice_stabilization_pairs": len(ADVICE_STABILIZATION_REPAIR),
            **leakage,
        },
        **summaries,
        "runtime_allowed": runtime_allowed,
        "limited_runtime_trial_allowed": runtime_allowed,
        "sf50m_allowed": False,
        "decision": (
            "All Phase 27 generation gates passed without prompt leakage. Design guarded runtime trial next."
            if runtime_allowed
            else "Advice/micro stabilization still leaves gaps; keep templates as runtime brain and continue repair."
        ),
        "next_phase": (
            "Phase 27.34 — guarded runtime trial design"
            if runtime_allowed
            else "Phase 27.34 — targeted natural repair before runtime"
        ),
        "failures": {
            **{name: [row for row in rows if not row["passed"]] for name, rows in rows_by_name.items()},
            "micro_probe": [row for row in micro_rows if not row["passed"]],
        },
        "results": {**rows_by_name, "micro_probe": micro_rows},
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _write_samples(
        args.samples,
        tuple((name.replace("_", " ").title(), rows) for name, rows in rows_by_name.items())
        + (("Micro-Probe Regression", micro_rows),),
    )

    print("SF.AI — Phase 27.33 advice + micro stabilization")
    print(f"  status              : {status}")
    print(f"  checkpoint          : {checkpoint_name}")
    for key, summary in summaries.items():
        print(f"  {key:<27}: {summary['passed']}/{summary['eval_records']}")
    print(f"  leakage             : {leakage}")
    print("  runtime             : " + ("trial-design-ready" if runtime_allowed else "blocked"))
    print(f"  report              : {args.report}")
    print(f"  samples             : {args.samples}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
