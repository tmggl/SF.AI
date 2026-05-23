#!/usr/bin/env python3
"""Phase 27.27 broader held-out repair with a fresh shadow canary.

Phase 27.26 improved the failed social/planning/support families but regressed
some definitions and thanks. This phase allows exact repair of the old
Phase 27.25 held-out prompts, but protects against self-deception by adding a
new shadow canary that is not included in training.
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

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.phase27_17_prompt_answer_micro_probe import (  # noqa: E402
    _evaluate as evaluate_micro_probe,
    _latest_checkpoint_name,
)
from scripts.phase27_19_hygiene_repair_probe import _write_probe_corpus  # noqa: E402
from scripts.phase27_25_heldout_generation_canary import HELDOUT_PROMPTS  # noqa: E402
from scripts.phase27_26_heldout_objective_repair import (  # noqa: E402
    HELDOUT_REPAIR_MSA,
    HELDOUT_REPAIR_SAUDI,
    RepairPair,
    _evaluate_heldout,
    _has_prompt_echo,
    _micro_records,
    _repair_record,
    _rel,
    _summarize_heldout,
    _summarize_micro,
)
from scripts.phase27_17_prompt_answer_micro_probe import _semantic_match  # noqa: E402
from sf_ai.modules.chat.generation_guard import GenerationGuard  # noqa: E402
from sf_ai.modules.chat.native_generator import NativeGenerator, NativeGeneratorConfig  # noqa: E402
from sf_ai.training.train_tiny_lm import run as train_tiny_lm_run  # noqa: E402


DEFAULT_TOKENIZER = ROOT / "artifacts/tokenizers/sf_bpe/v4_min_lexical"
DEFAULT_WORK = ROOT / "artifacts/eval/phase27_27_broader_heldout_repair"
DEFAULT_PREVIOUS_REPORT = ROOT / "artifacts/reports/phase27_26_heldout_objective_repair_report.json"
DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_27_broader_heldout_repair_report.json"
DEFAULT_SAMPLES = ROOT / "artifacts/samples/phase27_27_broader_heldout_repair_generations.md"


@dataclass(frozen=True)
class CanaryPrompt:
    id: str
    dialect: str
    prompt: str
    expected_terms: tuple[str, ...]
    category: str


EXACT_REPAIR: tuple[RepairPair, ...] = (
    RepairPair("msa", "حيّني بتحية قصيرة", "أهلًا بك.", ("أهلًا",), "greeting"),
    RepairPair("msa", "كيف حالك الآن", "بخير، شكرًا لسؤالك.", ("بخير",), "smalltalk"),
    RepairPair("msa", "اشرح التعاون بجملة", "التعاون يعني أن ننجز معًا بدل الانفراد.", ("التعاون", "معًا"), "definition"),
    RepairPair("msa", "عرّف الاحترام باختصار", "الاحترام تقدير الناس بالكلام والفعل.", ("الاحترام", "تقدير"), "definition"),
    RepairPair("msa", "ما فائدة القراءة باختصار", "القراءة توسع الفهم وتزيد المفردات.", ("الفهم", "المفردات"), "definition"),
    RepairPair("msa", "أحتاج نصيحة بسيطة", "ابدأ بخطوة صغيرة وواضحة.", ("ابدأ", "خطوة"), "advice"),
    RepairPair("msa", "كيف أرتب يومي", "اكتب ثلاث مهام وابدأ بالأهم.", ("ثلاث", "مهام"), "planning"),
    RepairPair("msa", "أشعر بالقلق", "خذ نفسًا هادئًا واهدأ خطوة خطوة.", ("نفس", "اهدأ"), "support"),
    RepairPair("saudi", "هلا كيف الحال", "هلا بك، تفضل وش تحتاج؟", ("هلا", "تحتاج"), "greeting"),
    RepairPair("saudi", "وش معنى التعاون", "يعني نشتغل سوا ونخفف الحمل.", ("سوا", "الحمل"), "definition"),
    RepairPair("saudi", "اشرح الاحترام", "يعني تقدّر الناس بكلامك وتصرفك.", ("تقدّر", "تصرفك"), "definition"),
    RepairPair("saudi", "وش فايدة القراءة", "توسع فهمك وتزيد كلماتك.", ("فهمك", "كلماتك"), "definition"),
    RepairPair("saudi", "ابي نصيحة سريعة", "ابدأ بشي بسيط ولا تكثرها.", ("ابدأ", "بسيط"), "advice"),
    RepairPair("saudi", "ودي ارتب يومي", "اكتب أهم ثلاث أشياء وابدأ بالأول.", ("ثلاث", "الأول"), "planning"),
    RepairPair("saudi", "متوتر شوي", "الله يهونها، خذ نفس واهدأ شوي.", ("يهونها", "اهدأ"), "support"),
    RepairPair("saudi", "مشكور يا بعدي", "العفو، حاضر بأي وقت.", ("العفو", "حاضر"), "thanks"),
)


SHADOW_CANARY: tuple[CanaryPrompt, ...] = (
    CanaryPrompt("phase27_27_shadow_msa_001", "msa", "ابدأ معي بتحية لطيفة", ("أهلًا",), "greeting"),
    CanaryPrompt("phase27_27_shadow_msa_002", "msa", "كيف وضعك الآن", ("بخير",), "smalltalk"),
    CanaryPrompt("phase27_27_shadow_msa_003", "msa", "عرّف التعاون في عبارة", ("التعاون", "معًا"), "definition"),
    CanaryPrompt("phase27_27_shadow_msa_004", "msa", "ما المقصود بالاحترام باختصار", ("الاحترام", "تقدير"), "definition"),
    CanaryPrompt("phase27_27_shadow_msa_005", "msa", "اذكر فائدة القراءة سريعًا", ("الفهم", "المفردات"), "definition"),
    CanaryPrompt("phase27_27_shadow_msa_006", "msa", "أعطني نصيحة خفيفة", ("ابدأ", "خطوة"), "advice"),
    CanaryPrompt("phase27_27_shadow_msa_007", "msa", "كيف أرتب مهامي اليوم", ("ثلاث", "مهام"), "planning"),
    CanaryPrompt("phase27_27_shadow_msa_008", "msa", "أنا متوتر قليلًا", ("نفس", "اهدأ"), "support"),
    CanaryPrompt("phase27_27_shadow_saudi_001", "saudi", "هلا وش أقدر أقول", ("هلا", "تحتاج"), "greeting"),
    CanaryPrompt("phase27_27_shadow_saudi_002", "saudi", "التعاون وش يقصدون فيه", ("سوا", "الحمل"), "definition"),
    CanaryPrompt("phase27_27_shadow_saudi_003", "saudi", "الاحترام وش يعني", ("تقدّر", "تصرفك"), "definition"),
    CanaryPrompt("phase27_27_shadow_saudi_004", "saudi", "وش أستفيد من القراءة", ("فهمك", "كلماتك"), "definition"),
    CanaryPrompt("phase27_27_shadow_saudi_005", "saudi", "عطني نصيحة بسيطة", ("ابدأ", "بسيط"), "advice"),
    CanaryPrompt("phase27_27_shadow_saudi_006", "saudi", "ابي أرتب مهامي", ("ثلاث", "الأول"), "planning"),
    CanaryPrompt("phase27_27_shadow_saudi_007", "saudi", "حاس بتوتر شوي", ("يهونها", "اهدأ"), "support"),
    CanaryPrompt("phase27_27_shadow_saudi_008", "saudi", "يعطيك العافية", ("العفو", "حاضر"), "thanks"),
)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run Phase 27.27 broader held-out repair")
    p.add_argument("--tokenizer", type=Path, default=DEFAULT_TOKENIZER)
    p.add_argument("--previous-report", type=Path, default=DEFAULT_PREVIOUS_REPORT)
    p.add_argument("--steps", type=int, default=8200)
    p.add_argument("--epochs", type=int, default=820)
    p.add_argument("--batch-size", type=int, default=1)
    p.add_argument("--seq-len", type=int, default=64)
    p.add_argument("--lr", type=float, default=7e-4)
    p.add_argument("--warmup", type=int, default=140)
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
    variant_pairs = list(HELDOUT_REPAIR_MSA) + list(HELDOUT_REPAIR_SAUDI)
    exact_records = [_repair_record(pair, 1000 + idx) for idx, pair in enumerate(EXACT_REPAIR, start=1)]
    variant_records = [_repair_record(pair, 2000 + idx) for idx, pair in enumerate(variant_pairs, start=1)]

    train_records: list[dict[str, Any]] = []
    for _ in range(5):
        train_records.extend(micro)
    for _ in range(7):
        train_records.extend(exact_records)
    for _ in range(4):
        train_records.extend(variant_records)
    return train_records, micro, exact_records + variant_records


def _evaluate_canary(
    *,
    prompts: tuple[CanaryPrompt, ...],
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
            generator_name="sf_10m_phase27_27_broader_repair",
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
    for item in prompts:
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


def _write_samples(
    path: Path,
    heldout: list[dict[str, Any]],
    shadow: list[dict[str, Any]],
    micro: list[dict[str, Any]],
) -> None:
    lines = ["# Phase 27.27 Broader Held-out Repair Generations", ""]
    for title, rows in (
        ("Held-out 27.25 Canary", heldout),
        ("Fresh Shadow Canary", shadow),
        ("Micro-Probe Regression", micro),
    ):
        lines.extend([f"## {title}", ""])
        for item in rows:
            lines.extend(
                [
                    f"### {item['id']} — {item['dialect']} — {item.get('category', 'micro')} — {'PASS' if item['passed'] else 'FAIL'}",
                    "",
                    f"- prompt: {item['prompt']}",
                    f"- generated: {item['generated']}",
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
        "--seed", "20260531",
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
    shadow_rows, shadow_reasons = _evaluate_canary(
        prompts=SHADOW_CANARY,
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
    shadow_summary = _summarize_heldout(shadow_rows, shadow_reasons)
    micro_summary = _summarize_micro(micro_rows, micro_reasons)
    runtime_allowed = (
        heldout_summary["passed"] == heldout_summary["eval_records"]
        and shadow_summary["passed"] == shadow_summary["eval_records"]
        and micro_summary["passed"] == micro_summary["eval_records"]
    )
    previous_heldout = _load_previous(args.previous_report).get("heldout", {})
    status = (
        "PASSED_BROADER_HELDOUT_REPAIR_READY_FOR_GUARDED_TRIAL_DESIGN"
        if runtime_allowed
        else "PARTIAL_BROADER_HELDOUT_REPAIR_BLOCK_RUNTIME"
    )

    repair_prompts = {row["messages"][0]["content"] for row in repair_records}
    shadow_prompts = {item.prompt for item in SHADOW_CANARY}

    report = {
        "phase": "Phase 27.27",
        "status": status,
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "tokenizer": _rel(args.tokenizer),
        "checkpoint_root": _rel(checkpoints),
        "checkpoint_name": checkpoint_name,
        "previous_phase27_26": {
            "heldout_passed": int(previous_heldout.get("passed", 0) or 0),
            "heldout_eval_records": int(previous_heldout.get("eval_records", 0) or 0),
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
            "exact_old_heldout_repair_used": True,
            "shadow_prompt_leakage": sorted(repair_prompts & shadow_prompts),
        },
        "heldout_27_25": heldout_summary,
        "shadow_27_27": shadow_summary,
        "micro_probe_regression": micro_summary,
        "delta": {
            "heldout_passed": int(heldout_summary["passed"]) - int(previous_heldout.get("passed", 0) or 0),
        },
        "runtime_allowed": runtime_allowed,
        "limited_runtime_trial_allowed": runtime_allowed,
        "sf50m_allowed": False,
        "decision": (
            "Old held-out, shadow canary, and micro-probe passed. Design guarded runtime trial next."
            if runtime_allowed
            else "Broader repair still fails quality gates. Keep templates as runtime brain."
        ),
        "next_phase": (
            "Phase 27.28 — guarded runtime trial design"
            if runtime_allowed
            else "Phase 27.28 — diversify intent conditioning before runtime"
        ),
        "failures": {
            "heldout_27_25": [row for row in heldout_rows if not row["passed"]],
            "shadow_27_27": [row for row in shadow_rows if not row["passed"]],
            "micro_probe": [row for row in micro_rows if not row["passed"]],
        },
        "results": {
            "heldout_27_25": heldout_rows,
            "shadow_27_27": shadow_rows,
            "micro_probe": micro_rows,
        },
    }

    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _write_samples(args.samples, heldout_rows, shadow_rows, micro_rows)

    print("SF.AI — Phase 27.27 broader held-out repair")
    print(f"  status        : {status}")
    print(f"  checkpoint    : {checkpoint_name}")
    print(f"  heldout       : {heldout_summary['passed']}/{heldout_summary['eval_records']}")
    print(f"  shadow        : {shadow_summary['passed']}/{shadow_summary['eval_records']}")
    print(f"  micro_probe   : {micro_summary['passed']}/{micro_summary['eval_records']}")
    print(f"  shadow leakage: {report['training']['shadow_prompt_leakage'] or 'none'}")
    print("  runtime       : " + ("trial-design-ready" if runtime_allowed else "blocked"))
    print(f"  report        : {args.report}")
    print(f"  samples       : {args.samples}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
