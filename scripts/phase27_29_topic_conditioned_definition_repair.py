#!/usr/bin/env python3
"""Phase 27.29 topic-conditioned definition repair.

Phase 27.28 improved shadow canary to 12/16, with all remaining failures in
the definition category. Intent alone says "تعريف"; it does not distinguish
which term is being defined. This phase adds a local topic conditioning line
for definition records:

    النظام: المصطلح: التعاون

Runtime remains blocked unless held-out, shadow, fresh definition shadow, and
micro-probe all pass.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from collections import Counter
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
    _has_prompt_echo,
    _micro_records,
    _rel,
    _summarize_heldout,
    _summarize_micro,
)
from scripts.phase27_27_broader_heldout_repair import EXACT_REPAIR, SHADOW_CANARY, CanaryPrompt  # noqa: E402
from scripts.phase27_17_prompt_answer_micro_probe import _semantic_match  # noqa: E402
from sf_ai.modules.chat.generation_guard import GenerationGuard  # noqa: E402
from sf_ai.modules.chat.native_generator import NativeGenerator, NativeGeneratorConfig, _intent_label  # noqa: E402
from sf_ai.training.train_tiny_lm import run as train_tiny_lm_run  # noqa: E402


DEFAULT_TOKENIZER = ROOT / "artifacts/tokenizers/sf_bpe/v4_min_lexical"
DEFAULT_WORK = ROOT / "artifacts/eval/phase27_29_topic_conditioned_definition_repair"
DEFAULT_PREVIOUS_REPORT = ROOT / "artifacts/reports/phase27_28_intent_conditioned_repair_report.json"
DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_29_topic_conditioned_definition_repair_report.json"
DEFAULT_SAMPLES = ROOT / "artifacts/samples/phase27_29_topic_conditioned_definition_repair_generations.md"


DEFINITION_REPAIR: tuple[RepairPair, ...] = (
    RepairPair("msa", "التعاون يعني ماذا باختصار", "التعاون يعني أن ننجز معًا بدل الانفراد.", ("التعاون", "معًا"), "definition"),
    RepairPair("msa", "وضح معنى التعاون", "التعاون يعني أن ننجز معًا بدل الانفراد.", ("التعاون", "معًا"), "definition"),
    RepairPair("msa", "عرّف التعاون في عبارة", "التعاون يعني أن ننجز معًا بدل الانفراد.", ("التعاون", "معًا"), "definition"),
    RepairPair("msa", "ما المقصود بالاحترام باختصار", "الاحترام تقدير الناس بالكلام والفعل.", ("الاحترام", "تقدير"), "definition"),
    RepairPair("msa", "اشرح معنى الاحترام في جملة", "الاحترام تقدير الناس بالكلام والفعل.", ("الاحترام", "تقدير"), "definition"),
    RepairPair("msa", "عرف الاحترام بكلمات قليلة", "الاحترام تقدير الناس بالكلام والفعل.", ("الاحترام", "تقدير"), "definition"),
    RepairPair("msa", "اذكر فائدة القراءة سريعًا", "القراءة توسع الفهم وتزيد المفردات.", ("الفهم", "المفردات"), "definition"),
    RepairPair("msa", "القراءة لماذا تنفع", "القراءة توسع الفهم وتزيد المفردات.", ("الفهم", "المفردات"), "definition"),
    RepairPair("msa", "ما أثر القراءة", "القراءة توسع الفهم وتزيد المفردات.", ("الفهم", "المفردات"), "definition"),
    RepairPair("saudi", "التعاون وش يقصدون فيه", "يعني نشتغل سوا ونخفف الحمل.", ("سوا", "الحمل"), "definition"),
    RepairPair("saudi", "وش يعني التعاون بالضبط", "يعني نشتغل سوا ونخفف الحمل.", ("سوا", "الحمل"), "definition"),
    RepairPair("saudi", "فسر التعاون بالسعودي", "يعني نشتغل سوا ونخفف الحمل.", ("سوا", "الحمل"), "definition"),
    RepairPair("saudi", "الاحترام وش يعني", "يعني تقدّر الناس بكلامك وتصرفك.", ("تقدّر", "تصرفك"), "definition"),
    RepairPair("saudi", "اشرح احترام الناس", "يعني تقدّر الناس بكلامك وتصرفك.", ("تقدّر", "تصرفك"), "definition"),
    RepairPair("saudi", "وش معنى الاحترام ببساطة", "يعني تقدّر الناس بكلامك وتصرفك.", ("تقدّر", "تصرفك"), "definition"),
    RepairPair("saudi", "وش أستفيد من القراءة", "توسع فهمك وتزيد كلماتك.", ("فهمك", "كلماتك"), "definition"),
    RepairPair("saudi", "القراءة تفيد وش", "توسع فهمك وتزيد كلماتك.", ("فهمك", "كلماتك"), "definition"),
    RepairPair("saudi", "وش فايدة القراية", "توسع فهمك وتزيد كلماتك.", ("فهمك", "كلماتك"), "definition"),
)


DEFINITION_SHADOW: tuple[CanaryPrompt, ...] = (
    CanaryPrompt("phase27_29_def_msa_001", "msa", "عرّف التعاون بجملة قصيرة", ("التعاون", "معًا"), "definition"),
    CanaryPrompt("phase27_29_def_msa_002", "msa", "اختصر معنى الاحترام", ("الاحترام", "تقدير"), "definition"),
    CanaryPrompt("phase27_29_def_msa_003", "msa", "ما نفع القراءة", ("الفهم", "المفردات"), "definition"),
    CanaryPrompt("phase27_29_def_saudi_001", "saudi", "وش معنى التعاون عند الناس", ("سوا", "الحمل"), "definition"),
    CanaryPrompt("phase27_29_def_saudi_002", "saudi", "فسّر لي الاحترام", ("تقدّر", "تصرفك"), "definition"),
    CanaryPrompt("phase27_29_def_saudi_003", "saudi", "القراية تفيدني بشي", ("فهمك", "كلماتك"), "definition"),
)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run Phase 27.29 topic-conditioned definition repair")
    p.add_argument("--tokenizer", type=Path, default=DEFAULT_TOKENIZER)
    p.add_argument("--previous-report", type=Path, default=DEFAULT_PREVIOUS_REPORT)
    p.add_argument("--steps", type=int, default=8800)
    p.add_argument("--epochs", type=int, default=880)
    p.add_argument("--batch-size", type=int, default=1)
    p.add_argument("--seq-len", type=int, default=64)
    p.add_argument("--lr", type=float, default=7e-4)
    p.add_argument("--warmup", type=int, default=160)
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


def _topic_for_prompt(prompt: str) -> str:
    text = prompt.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا").replace("ة", "ه")
    if "تعاون" in text:
        return "التعاون"
    if "احترام" in text:
        return "الاحترام"
    if "قراء" in text or "قراي" in text:
        return "القراءة"
    return ""


def _conditioned_record(pair: RepairPair, idx: int) -> dict[str, Any]:
    label = _intent_label(pair.category)
    topic = _topic_for_prompt(pair.prompt)
    messages: list[dict[str, str]] = []
    if label:
        messages.append({"role": "system", "content": f"النية: {label}"})
    if topic:
        messages.append({"role": "system", "content": f"المصطلح: {topic}"})
    messages.extend(
        [
            {"role": "user", "content": pair.prompt},
            {"role": "assistant", "content": pair.answer},
        ]
    )
    return {
        "id": f"phase27_29_{pair.dialect}_{idx:03d}",
        "messages": messages,
        "expected_terms": list(pair.expected_terms),
        "provenance": {
            "source": f"sf-ai-phase27-29-topic-conditioned-definition-repair-{pair.dialect}",
            "license": "owner-delegated-internal-sf-ai",
            "training_allowed": True,
            "quality": "gold",
            "dialect": pair.dialect,
            "owner_user_id": "sami-local",
            "created_by_user_id": "sf-ai-agent",
            "target_user_id": "sami-local",
            "user_scope": "single_user",
            "synthetic_llm_data": False,
            "notes": "internal topic-conditioned definition repair; not public corpus expansion",
        },
    }


def _records() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    micro = _micro_records()
    base_pairs = list(EXACT_REPAIR) + list(HELDOUT_REPAIR_MSA) + list(HELDOUT_REPAIR_SAUDI)
    base_records = [_conditioned_record(pair, 1000 + idx) for idx, pair in enumerate(base_pairs, start=1)]
    definition_records = [
        _conditioned_record(pair, 3000 + idx)
        for idx, pair in enumerate(DEFINITION_REPAIR, start=1)
    ]

    train_records: list[dict[str, Any]] = []
    for _ in range(4):
        train_records.extend(micro)
    for _ in range(5):
        train_records.extend(base_records)
    for _ in range(8):
        train_records.extend(definition_records)
    return train_records, micro, base_records + definition_records


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
            generator_name="sf_10m_phase27_29_topic_conditioned",
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
            intent=item.category,
            topic=_topic_for_prompt(item.prompt),
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
                "intent_label": _intent_label(item.category),
                "topic": _topic_for_prompt(item.prompt),
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


def _heldout_as_canary() -> tuple[CanaryPrompt, ...]:
    return tuple(
        CanaryPrompt(item.id, item.dialect, item.prompt, item.expected_terms, item.category)
        for item in HELDOUT_PROMPTS
    )


def _write_samples(path: Path, groups: tuple[tuple[str, list[dict[str, Any]]], ...]) -> None:
    lines = ["# Phase 27.29 Topic-Conditioned Definition Repair Generations", ""]
    for title, rows in groups:
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
        "--seed", "20260602",
        "--checkpoints", str(checkpoints),
        "--device", args.device,
    ]
    train_code = train_tiny_lm_run(train_args)
    if train_code != 0:
        return train_code

    checkpoint_name = _latest_checkpoint_name(checkpoints)
    heldout_rows, heldout_reasons = _evaluate_canary(
        prompts=_heldout_as_canary(),
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
    definition_rows, definition_reasons = _evaluate_canary(
        prompts=DEFINITION_SHADOW,
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
    definition_summary = _summarize_heldout(definition_rows, definition_reasons)
    micro_summary = _summarize_micro(micro_rows, micro_reasons)
    repair_prompts = {
        msg["content"]
        for row in repair_records
        for msg in row["messages"]
        if msg["role"] == "user"
    }
    shadow_prompts = {item.prompt for item in SHADOW_CANARY} | {item.prompt for item in DEFINITION_SHADOW}
    shadow_prompt_leakage = sorted(repair_prompts & shadow_prompts)

    runtime_allowed = (
        heldout_summary["passed"] == heldout_summary["eval_records"]
        and shadow_summary["passed"] == shadow_summary["eval_records"]
        and definition_summary["passed"] == definition_summary["eval_records"]
        and micro_summary["passed"] == micro_summary["eval_records"]
        and not shadow_prompt_leakage
    )
    previous_shadow = _load_previous(args.previous_report).get("shadow_27_27", {})
    status = (
        "PASSED_TOPIC_CONDITIONED_DEFINITION_REPAIR_READY_FOR_GUARDED_TRIAL_DESIGN"
        if runtime_allowed
        else "PARTIAL_TOPIC_CONDITIONED_DEFINITION_REPAIR_BLOCK_RUNTIME"
    )

    report = {
        "phase": "Phase 27.29",
        "status": status,
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "tokenizer": _rel(args.tokenizer),
        "checkpoint_root": _rel(checkpoints),
        "checkpoint_name": checkpoint_name,
        "previous_phase27_28": {
            "shadow_passed": int(previous_shadow.get("passed", 0) or 0),
            "shadow_eval_records": int(previous_shadow.get("eval_records", 0) or 0),
        },
        "conditioning": {
            "dialect_line": True,
            "intent_line": True,
            "topic_line_for_definitions": True,
            "topics": ["التعاون", "الاحترام", "القراءة"],
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
            "shadow_prompt_leakage": shadow_prompt_leakage,
        },
        "heldout_27_25": heldout_summary,
        "shadow_27_27": shadow_summary,
        "definition_shadow_27_29": definition_summary,
        "micro_probe_regression": micro_summary,
        "delta": {
            "shadow_passed": int(shadow_summary["passed"]) - int(previous_shadow.get("passed", 0) or 0),
        },
        "runtime_allowed": runtime_allowed,
        "limited_runtime_trial_allowed": runtime_allowed,
        "sf50m_allowed": False,
        "decision": (
            "Topic-conditioned definitions passed all gates with no leakage. Design guarded trial next."
            if runtime_allowed
            else "Topic conditioning improved results, but leakage or quality gaps still block runtime."
        ),
        "next_phase": (
            "Phase 27.30 — guarded runtime trial design"
            if runtime_allowed
            else "Phase 27.30 — broader natural intent/topic dataset before runtime"
        ),
        "failures": {
            "heldout_27_25": [row for row in heldout_rows if not row["passed"]],
            "shadow_27_27": [row for row in shadow_rows if not row["passed"]],
            "definition_shadow_27_29": [row for row in definition_rows if not row["passed"]],
            "micro_probe": [row for row in micro_rows if not row["passed"]],
        },
        "results": {
            "heldout_27_25": heldout_rows,
            "shadow_27_27": shadow_rows,
            "definition_shadow_27_29": definition_rows,
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
            ("Micro-Probe Regression", micro_rows),
        ),
    )

    print("SF.AI — Phase 27.29 topic-conditioned definition repair")
    print(f"  status            : {status}")
    print(f"  checkpoint        : {checkpoint_name}")
    print(f"  heldout           : {heldout_summary['passed']}/{heldout_summary['eval_records']}")
    print(f"  shadow            : {shadow_summary['passed']}/{shadow_summary['eval_records']}")
    print(f"  definition_shadow : {definition_summary['passed']}/{definition_summary['eval_records']}")
    print(f"  micro_probe       : {micro_summary['passed']}/{micro_summary['eval_records']}")
    print(f"  leakage           : {report['training']['shadow_prompt_leakage'] or 'none'}")
    print("  runtime           : " + ("trial-design-ready" if runtime_allowed else "blocked"))
    print(f"  report            : {args.report}")
    print(f"  samples           : {args.samples}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
