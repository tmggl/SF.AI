#!/usr/bin/env python3
"""Phase 27.32 balanced natural calibration.

Phase 27.31 improved natural thanks/smalltalk, but it over-pulled a few Saudi
definition/planning/support prompts toward wrong categories. This phase adds a
balanced natural calibration layer for MSA+Saudi intent/topic families without
using the old canary prompts verbatim.

No runtime activation happens here. Passing only means the next phase may
design a guarded local runtime trial.
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
from sf_ai.training.train_tiny_lm import run as train_tiny_lm_run  # noqa: E402


DEFAULT_TOKENIZER = ROOT / "artifacts/tokenizers/sf_bpe/v4_min_lexical"
DEFAULT_WORK = ROOT / "artifacts/eval/phase27_32_balanced_natural_calibration"
DEFAULT_PREVIOUS_REPORT = ROOT / "artifacts/reports/phase27_31_natural_intent_topic_dataset_report.json"
DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_32_balanced_natural_calibration_report.json"
DEFAULT_SAMPLES = ROOT / "artifacts/samples/phase27_32_balanced_natural_calibration_generations.md"


BALANCED_CALIBRATION_REPAIR: tuple[RepairPair, ...] = (
    # Saudi definitions around the weak topics, excluding exact canary prompts.
    RepairPair("saudi", "وش يعني احترام الناس", "يعني تقدّر الناس بكلامك وتصرفك.", ("تقدّر", "تصرفك"), "definition"),
    RepairPair("saudi", "معنى الاحترام عند الناس", "يعني تقدّر الناس بكلامك وتصرفك.", ("تقدّر", "تصرفك"), "definition"),
    RepairPair("saudi", "اشرح لي وش يعني احترام", "يعني تقدّر الناس بكلامك وتصرفك.", ("تقدّر", "تصرفك"), "definition"),
    RepairPair("saudi", "وش معنى كلمة الاحترام", "يعني تقدّر الناس بكلامك وتصرفك.", ("تقدّر", "تصرفك"), "definition"),
    RepairPair("saudi", "القراية وش فايدتها", "توسع فهمك وتزيد كلماتك.", ("فهمك", "كلماتك"), "definition"),
    RepairPair("saudi", "هل القراية تنفعني", "توسع فهمك وتزيد كلماتك.", ("فهمك", "كلماتك"), "definition"),
    RepairPair("saudi", "وش تعطيك القراية", "توسع فهمك وتزيد كلماتك.", ("فهمك", "كلماتك"), "definition"),
    RepairPair("saudi", "فائدة القراية وش هي", "توسع فهمك وتزيد كلماتك.", ("فهمك", "كلماتك"), "definition"),
    RepairPair("saudi", "نظم لي يومي بسرعة", "اكتب أهم ثلاث أشياء وابدأ بالأول.", ("ثلاث", "الأول"), "planning"),
    RepairPair("saudi", "ساعدني أرتب اليوم", "اكتب أهم ثلاث أشياء وابدأ بالأول.", ("ثلاث", "الأول"), "planning"),
    RepairPair("saudi", "وش أبدأ فيه اليوم", "حدد ثلاث أشياء وابدأ بالأول.", ("ثلاث", "الأول"), "planning"),
    RepairPair("saudi", "رتب مهامي بسرعة", "اكتب أهم ثلاث أشياء وابدأ بالأول.", ("ثلاث", "الأول"), "planning"),
    RepairPair("saudi", "أنا متوتر وش تنصحني", "الله يهونها، خذ نفس واهدأ شوي.", ("يهونها", "اهدأ"), "support"),
    RepairPair("saudi", "حسيت بتوتر خفيف", "الله يهونها، خذ نفس واهدأ شوي.", ("يهونها", "اهدأ"), "support"),
    RepairPair("saudi", "وش أسوي إذا توترت", "الله يهونها، خذ نفس واهدأ شوي.", ("يهونها", "اهدأ"), "support"),
    RepairPair("saudi", "توتران شوي وابي أهدأ", "الله يهونها، خذ نفس واهدأ شوي.", ("يهونها", "اهدأ"), "support"),
    # MSA counterparts keep the model balanced across both active tracks.
    RepairPair("msa", "ما معنى احترام الآخرين", "الاحترام تقدير الناس بالكلام والفعل.", ("الاحترام", "تقدير"), "definition"),
    RepairPair("msa", "ما فائدة القراءة للإنسان", "القراءة توسع الفهم وتزيد المفردات.", ("الفهم", "المفردات"), "definition"),
    RepairPair("msa", "ساعدني في ترتيب يومي", "اكتب ثلاث مهام وابدأ بالأهم.", ("ثلاث", "مهام"), "planning"),
    RepairPair("msa", "أشعر بتوتر بسيط ماذا أفعل", "خذ نفسًا هادئًا واهدأ خطوة خطوة.", ("نفس", "اهدأ"), "support"),
    RepairPair("msa", "أشكرك على تعاونك", "العفو، يسعدني أن أساعدك.", ("العفو", "أساعدك"), "thanks"),
    RepairPair("msa", "كيف حالك هذا اليوم", "بخير، شكرًا لسؤالك.", ("بخير",), "smalltalk"),
)


CALIBRATION_SHADOW_CANARY: tuple[NaturalPrompt, ...] = (
    NaturalPrompt("phase27_32_saudi_001", "saudi", "فسر لي معنى الاحترام", ("تقدّر", "تصرفك"), "definition"),
    NaturalPrompt("phase27_32_saudi_002", "saudi", "الاحترام يعني ايش", ("تقدّر", "تصرفك"), "definition"),
    NaturalPrompt("phase27_32_saudi_003", "saudi", "القراية تنفعني كيف", ("فهمك", "كلماتك"), "definition"),
    NaturalPrompt("phase27_32_saudi_004", "saudi", "وش تكسبني القراءة", ("فهمك", "كلماتك"), "definition"),
    NaturalPrompt("phase27_32_saudi_005", "saudi", "نظم يومي بكلمتين", ("ثلاث", "الأول"), "planning"),
    NaturalPrompt("phase27_32_saudi_006", "saudi", "وش أول شي أسويه اليوم", ("ثلاث", "الأول"), "planning"),
    NaturalPrompt("phase27_32_saudi_007", "saudi", "متوتر وابي تهدئة", ("يهونها", "اهدأ"), "support"),
    NaturalPrompt("phase27_32_saudi_008", "saudi", "ابي أهدأ من التوتر", ("يهونها", "اهدأ"), "support"),
    NaturalPrompt("phase27_32_msa_001", "msa", "عرف احترام الناس", ("الاحترام", "تقدير"), "definition"),
    NaturalPrompt("phase27_32_msa_002", "msa", "كيف تفيدني القراءة", ("الفهم", "المفردات"), "definition"),
    NaturalPrompt("phase27_32_msa_003", "msa", "نظم أولويات هذا اليوم", ("ثلاث", "مهام"), "planning"),
    NaturalPrompt("phase27_32_msa_004", "msa", "كيف أهدأ من توتر بسيط", ("نفس", "اهدأ"), "support"),
)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run Phase 27.32 balanced natural calibration")
    p.add_argument("--tokenizer", type=Path, default=DEFAULT_TOKENIZER)
    p.add_argument("--previous-report", type=Path, default=DEFAULT_PREVIOUS_REPORT)
    p.add_argument("--steps", type=int, default=9600)
    p.add_argument("--epochs", type=int, default=960)
    p.add_argument("--batch-size", type=int, default=1)
    p.add_argument("--seq-len", type=int, default=64)
    p.add_argument("--lr", type=float, default=7e-4)
    p.add_argument("--warmup", type=int, default=170)
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
    calibration_pairs = list(BALANCED_CALIBRATION_REPAIR)

    base_records = [_conditioned_record(pair, 1000 + idx) for idx, pair in enumerate(base_pairs, start=1)]
    definition_records = [_conditioned_record(pair, 3000 + idx) for idx, pair in enumerate(definition_pairs, start=1)]
    natural_records = [_conditioned_record(pair, 5000 + idx) for idx, pair in enumerate(natural_pairs, start=1)]
    calibration_records = [_conditioned_record(pair, 7000 + idx) for idx, pair in enumerate(calibration_pairs, start=1)]

    train_records: list[dict[str, Any]] = []
    for _ in range(4):
        train_records.extend(micro)
    for _ in range(5):
        train_records.extend(base_records)
    for _ in range(8):
        train_records.extend(definition_records)
    for _ in range(5):
        train_records.extend(natural_records)
    for _ in range(13):
        train_records.extend(calibration_records)
    return train_records, micro, base_records + definition_records + natural_records + calibration_records


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
        "--seed", "20260605",
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
    heldout_rows, heldout_reasons = _evaluate_prompts(prompts=_heldout_as_canary(), **eval_kwargs)
    shadow_rows, shadow_reasons = _evaluate_prompts(prompts=SHADOW_CANARY, **eval_kwargs)
    definition_rows, definition_reasons = _evaluate_prompts(prompts=DEFINITION_SHADOW, **eval_kwargs)
    fresh_mixed_rows, fresh_mixed_reasons = _evaluate_prompts(prompts=FRESH_MIXED_CANARY, **eval_kwargs)
    natural_shadow_rows, natural_shadow_reasons = _evaluate_prompts(prompts=NATURAL_SHADOW_CANARY, **eval_kwargs)
    calibration_rows, calibration_reasons = _evaluate_prompts(prompts=CALIBRATION_SHADOW_CANARY, **eval_kwargs)
    micro_rows, micro_reasons = evaluate_micro_probe(
        records=micro_records,
        checkpoints_root=checkpoints,
        checkpoint_name=checkpoint_name,
        device=args.device,
        tokenizer_path=args.tokenizer,
    )

    summaries = {
        "heldout_27_25": _summarize_heldout(heldout_rows, heldout_reasons),
        "shadow_27_27": _summarize_heldout(shadow_rows, shadow_reasons),
        "definition_shadow_27_29": _summarize_heldout(definition_rows, definition_reasons),
        "fresh_mixed_shadow_27_30": _summarize_heldout(fresh_mixed_rows, fresh_mixed_reasons),
        "natural_shadow_27_31": _summarize_heldout(natural_shadow_rows, natural_shadow_reasons),
        "calibration_shadow_27_32": _summarize_heldout(calibration_rows, calibration_reasons),
        "micro_probe_regression": _summarize_micro(micro_rows, micro_reasons),
    }

    repair_prompts = _prompt_set(repair_records)
    leakage = {
        "fresh_mixed_prompt_leakage": sorted(repair_prompts & {item.prompt for item in FRESH_MIXED_CANARY}),
        "natural_shadow_prompt_leakage": sorted(repair_prompts & {item.prompt for item in NATURAL_SHADOW_CANARY}),
        "calibration_shadow_prompt_leakage": sorted(repair_prompts & {item.prompt for item in CALIBRATION_SHADOW_CANARY}),
    }
    runtime_allowed = all(_all_pass(summary) for summary in summaries.values()) and not any(leakage.values())
    previous = _load_previous(args.previous_report)
    status = (
        "PASSED_BALANCED_NATURAL_CALIBRATION_READY_FOR_GUARDED_TRIAL_DESIGN"
        if runtime_allowed
        else "PARTIAL_BALANCED_NATURAL_CALIBRATION_BLOCK_RUNTIME"
    )
    report = {
        "phase": "Phase 27.32",
        "status": status,
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "tokenizer": _rel(args.tokenizer),
        "checkpoint_root": _rel(checkpoints),
        "checkpoint_name": checkpoint_name,
        "previous_phase27_31": {
            "status": previous.get("status", ""),
            "fresh_mixed_passed": int(previous.get("fresh_mixed_shadow_27_30", {}).get("passed", 0) or 0),
            "natural_shadow_passed": int(previous.get("natural_shadow_27_31", {}).get("passed", 0) or 0),
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
            "balanced_calibration_pairs": len(BALANCED_CALIBRATION_REPAIR),
            **leakage,
        },
        **summaries,
        "runtime_allowed": runtime_allowed,
        "limited_runtime_trial_allowed": runtime_allowed,
        "sf50m_allowed": False,
        "decision": (
            "All Phase 27 generation gates passed without prompt leakage. Design guarded runtime trial next."
            if runtime_allowed
            else "Balanced calibration still leaves gaps; keep templates as runtime brain and continue repair."
        ),
        "next_phase": (
            "Phase 27.33 — guarded runtime trial design"
            if runtime_allowed
            else "Phase 27.33 — targeted natural repair before runtime"
        ),
        "failures": {
            "heldout_27_25": [row for row in heldout_rows if not row["passed"]],
            "shadow_27_27": [row for row in shadow_rows if not row["passed"]],
            "definition_shadow_27_29": [row for row in definition_rows if not row["passed"]],
            "fresh_mixed_shadow_27_30": [row for row in fresh_mixed_rows if not row["passed"]],
            "natural_shadow_27_31": [row for row in natural_shadow_rows if not row["passed"]],
            "calibration_shadow_27_32": [row for row in calibration_rows if not row["passed"]],
            "micro_probe": [row for row in micro_rows if not row["passed"]],
        },
        "results": {
            "heldout_27_25": heldout_rows,
            "shadow_27_27": shadow_rows,
            "definition_shadow_27_29": definition_rows,
            "fresh_mixed_shadow_27_30": fresh_mixed_rows,
            "natural_shadow_27_31": natural_shadow_rows,
            "calibration_shadow_27_32": calibration_rows,
            "micro_probe": micro_rows,
        },
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _write_samples(
        args.samples,
        (
            ("Held-out 27.25 Canary", heldout_rows),
            ("Shadow 27.27 Canary", shadow_rows),
            ("Definition Shadow 27.29", definition_rows),
            ("Fresh Mixed 27.30", fresh_mixed_rows),
            ("Natural Shadow 27.31", natural_shadow_rows),
            ("Calibration Shadow 27.32", calibration_rows),
            ("Micro-Probe Regression", micro_rows),
        ),
    )

    print("SF.AI — Phase 27.32 balanced natural calibration")
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
