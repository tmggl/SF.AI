#!/usr/bin/env python3
"""Phase 27.30 fresh mixed shadow canary.

No training. This evaluates the Phase 27.29 topic-conditioned checkpoint on a
fresh, non-leaked mixed canary. If this fails, the next step is broader natural
intent/topic data, not runtime activation.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.phase27_17_prompt_answer_micro_probe import _semantic_match  # noqa: E402
from scripts.phase27_26_heldout_objective_repair import _has_prompt_echo, _rel, _summarize_heldout  # noqa: E402
from scripts.phase27_29_topic_conditioned_definition_repair import _topic_for_prompt  # noqa: E402
from sf_ai.modules.chat.generation_guard import GenerationGuard  # noqa: E402
from sf_ai.modules.chat.native_generator import NativeGenerator, NativeGeneratorConfig, _intent_label  # noqa: E402


DEFAULT_TOKENIZER = ROOT / "artifacts/tokenizers/sf_bpe/v4_min_lexical"
DEFAULT_CHECKPOINTS = ROOT / "artifacts/eval/phase27_29_topic_conditioned_definition_repair/checkpoints"
DEFAULT_CHECKPOINT = "sf-10m-step8800"
DEFAULT_PREVIOUS_REPORT = ROOT / "artifacts/reports/phase27_29_topic_conditioned_definition_repair_report.json"
DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_30_fresh_mixed_shadow_canary_report.json"
DEFAULT_SAMPLES = ROOT / "artifacts/samples/phase27_30_fresh_mixed_shadow_canary_generations.md"


@dataclass(frozen=True)
class FreshPrompt:
    id: str
    dialect: str
    prompt: str
    expected_terms: tuple[str, ...]
    category: str


FRESH_MIXED_CANARY: tuple[FreshPrompt, ...] = (
    FreshPrompt("phase27_30_msa_001", "msa", "قل أهلًا بطريقة قصيرة", ("أهلًا",), "greeting"),
    FreshPrompt("phase27_30_msa_002", "msa", "كيف حالك باختصار", ("بخير",), "smalltalk"),
    FreshPrompt("phase27_30_msa_003", "msa", "ما معنى التعاون باختصار شديد", ("التعاون", "معًا"), "definition"),
    FreshPrompt("phase27_30_msa_004", "msa", "اكتب تعريفًا للاحترام", ("الاحترام", "تقدير"), "definition"),
    FreshPrompt("phase27_30_msa_005", "msa", "لماذا القراءة مفيدة", ("الفهم", "المفردات"), "definition"),
    FreshPrompt("phase27_30_msa_006", "msa", "وجهني بخطوة بسيطة", ("ابدأ", "خطوة"), "advice"),
    FreshPrompt("phase27_30_msa_007", "msa", "رتب لي أولويات اليوم", ("ثلاث", "مهام"), "planning"),
    FreshPrompt("phase27_30_msa_008", "msa", "أشعر بتوتر الآن", ("نفس", "اهدأ"), "support"),
    FreshPrompt("phase27_30_msa_009", "msa", "شكرًا لمساعدتك", ("العفو", "أساعدك"), "thanks"),
    FreshPrompt("phase27_30_saudi_001", "saudi", "هلا عطنا بداية", ("هلا", "تحتاج"), "greeting"),
    FreshPrompt("phase27_30_saudi_002", "saudi", "كيفك اليوم", ("بخير", "كيفك"), "smalltalk"),
    FreshPrompt("phase27_30_saudi_003", "saudi", "فسر التعاون لي", ("سوا", "الحمل"), "definition"),
    FreshPrompt("phase27_30_saudi_004", "saudi", "وش المقصود بالاحترام", ("تقدّر", "تصرفك"), "definition"),
    FreshPrompt("phase27_30_saudi_005", "saudi", "القراية وش تعطيني", ("فهمك", "كلماتك"), "definition"),
    FreshPrompt("phase27_30_saudi_006", "saudi", "دلني على نصيحة خفيفة", ("ابدأ", "بسيط"), "advice"),
    FreshPrompt("phase27_30_saudi_007", "saudi", "رتب لي يومي بسرعة", ("ثلاث", "الأول"), "planning"),
    FreshPrompt("phase27_30_saudi_008", "saudi", "توترت شوي وش اسوي", ("يهونها", "اهدأ"), "support"),
    FreshPrompt("phase27_30_saudi_009", "saudi", "ممتن لك", ("العفو", "حاضر"), "thanks"),
)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run Phase 27.30 fresh mixed shadow canary")
    p.add_argument("--tokenizer", type=Path, default=DEFAULT_TOKENIZER)
    p.add_argument("--checkpoints", type=Path, default=DEFAULT_CHECKPOINTS)
    p.add_argument("--checkpoint-name", default=DEFAULT_CHECKPOINT)
    p.add_argument("--previous-report", type=Path, default=DEFAULT_PREVIOUS_REPORT)
    p.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    p.add_argument("--samples", type=Path, default=DEFAULT_SAMPLES)
    p.add_argument("--device", default="auto")
    return p.parse_args()


def _load_previous(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _evaluate(args: argparse.Namespace) -> tuple[list[dict[str, Any]], Counter[str]]:
    generator = NativeGenerator(
        NativeGeneratorConfig(
            tokenizer_path=args.tokenizer,
            checkpoints_root=args.checkpoints,
            checkpoint_name=args.checkpoint_name,
            generator_name="sf_10m_phase27_30_fresh_mixed_shadow",
            model_size="sf-10m",
            seq_len=64,
            max_new_tokens=24,
            temperature=1.0,
            top_k=0,
            no_repeat_ngram_size=3,
            repetition_penalty=1.08,
            device=args.device,
            dialogue_prompt=True,
        )
    )
    guard = GenerationGuard(min_chars=4)
    rows: list[dict[str, Any]] = []
    reasons: Counter[str] = Counter()
    for item in FRESH_MIXED_CANARY:
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


def _write_samples(path: Path, rows: list[dict[str, Any]]) -> None:
    lines = ["# Phase 27.30 Fresh Mixed Shadow Canary", ""]
    for item in rows:
        lines.extend(
            [
                f"## {item['id']} — {item['dialect']} — {item['category']} — {'PASS' if item['passed'] else 'FAIL'}",
                "",
                f"- prompt: {item['prompt']}",
                f"- intent_label: {item['intent_label']}",
                f"- topic: {item['topic'] or '-'}",
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
    ckpt = args.checkpoints / args.checkpoint_name
    if not (ckpt / "state.pt").exists():
        print(f"error: missing checkpoint at {ckpt}", file=sys.stderr)
        return 1

    rows, reasons = _evaluate(args)
    summary = _summarize_heldout(rows, reasons)
    previous = _load_previous(args.previous_report)
    total = int(summary["eval_records"])
    runtime_allowed = summary["passed"] == total
    status = (
        "PASSED_FRESH_MIXED_SHADOW_READY_FOR_GUARDED_TRIAL_DESIGN"
        if runtime_allowed
        else "FAILED_FRESH_MIXED_SHADOW_BLOCK_RUNTIME"
    )
    report = {
        "phase": "Phase 27.30",
        "status": status,
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "tokenizer": _rel(args.tokenizer),
        "checkpoint_root": _rel(args.checkpoints),
        "checkpoint_name": args.checkpoint_name,
        "previous_phase27_29": {
            "status": previous.get("status", ""),
            "runtime_allowed": bool(previous.get("runtime_allowed", False)),
        },
        "conditioning": {
            "dialect_line": True,
            "intent_line": True,
            "topic_line_for_definitions": True,
        },
        "fresh_mixed_shadow": summary,
        "runtime_allowed": runtime_allowed,
        "limited_runtime_trial_allowed": runtime_allowed,
        "sf50m_allowed": False,
        "decision": (
            "Fresh mixed shadow passed. Design a guarded runtime trial next."
            if runtime_allowed
            else "Fresh mixed shadow failed. Keep templates as runtime brain and expand natural intent/topic data."
        ),
        "next_phase": (
            "Phase 27.31 — guarded runtime trial design"
            if runtime_allowed
            else "Phase 27.31 — broader natural intent/topic dataset before runtime"
        ),
        "failures": [row for row in rows if not row["passed"]],
        "results": rows,
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _write_samples(args.samples, rows)

    print("SF.AI — Phase 27.30 fresh mixed shadow canary")
    print(f"  status    : {status}")
    print(f"  checkpoint: {args.checkpoint_name}")
    print(f"  passed    : {summary['passed']}/{summary['eval_records']}")
    print("  runtime   : " + ("trial-design-ready" if runtime_allowed else "blocked"))
    print(f"  report    : {args.report}")
    print(f"  samples   : {args.samples}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
