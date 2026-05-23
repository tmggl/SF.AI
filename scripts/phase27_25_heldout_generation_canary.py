#!/usr/bin/env python3
"""Phase 27.25 held-out generation-quality canary.

Phase 27.24 proved the stack can reach 32/32 on the trained micro-probe.
This script asks nearby but unseen prompts to check whether the model
generalizes enough for runtime. It does not train and never enables runtime.
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

from scripts.phase27_17_prompt_answer_micro_probe import _semantic_match, _surface  # noqa: E402
from sf_ai.modules.chat.generation_guard import GenerationGuard  # noqa: E402
from sf_ai.modules.chat.native_generator import NativeGenerator, NativeGeneratorConfig  # noqa: E402


DEFAULT_TOKENIZER = ROOT / "artifacts/tokenizers/sf_bpe/v4_min_lexical"
DEFAULT_CHECKPOINTS = ROOT / "artifacts/eval/phase27_24_minimal_lexical_stabilization/checkpoints"
DEFAULT_CHECKPOINT = "sf-10m-step5600"
DEFAULT_PREVIOUS_REPORT = ROOT / "artifacts/reports/phase27_24_minimal_lexical_stabilization_report.json"
DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_25_heldout_generation_canary_report.json"
DEFAULT_SAMPLES = ROOT / "artifacts/samples/phase27_25_heldout_generation_canary_generations.md"


@dataclass(frozen=True)
class HeldoutPrompt:
    id: str
    dialect: str
    prompt: str
    expected_terms: tuple[str, ...]
    category: str


HELDOUT_PROMPTS: tuple[HeldoutPrompt, ...] = (
    HeldoutPrompt("phase27_25_msa_001", "msa", "حيّني بتحية قصيرة", ("أهلًا",), "greeting"),
    HeldoutPrompt("phase27_25_msa_002", "msa", "كيف حالك الآن", ("بخير",), "smalltalk"),
    HeldoutPrompt("phase27_25_msa_003", "msa", "اشرح التعاون بجملة", ("التعاون", "معًا"), "definition"),
    HeldoutPrompt("phase27_25_msa_004", "msa", "عرّف الاحترام باختصار", ("الاحترام", "تقدير"), "definition"),
    HeldoutPrompt("phase27_25_msa_005", "msa", "ما فائدة القراءة باختصار", ("الفهم", "المفردات"), "definition"),
    HeldoutPrompt("phase27_25_msa_006", "msa", "أحتاج نصيحة بسيطة", ("ابدأ", "خطوة"), "advice"),
    HeldoutPrompt("phase27_25_msa_007", "msa", "كيف أرتب يومي", ("ثلاث", "مهام"), "planning"),
    HeldoutPrompt("phase27_25_msa_008", "msa", "أشعر بالقلق", ("نفس", "اهدأ"), "support"),
    HeldoutPrompt("phase27_25_saudi_001", "saudi", "هلا كيف الحال", ("هلا", "تحتاج"), "greeting"),
    HeldoutPrompt("phase27_25_saudi_002", "saudi", "وش معنى التعاون", ("سوا", "الحمل"), "definition"),
    HeldoutPrompt("phase27_25_saudi_003", "saudi", "اشرح الاحترام", ("تقدّر", "تصرفك"), "definition"),
    HeldoutPrompt("phase27_25_saudi_004", "saudi", "وش فايدة القراءة", ("فهمك", "كلماتك"), "definition"),
    HeldoutPrompt("phase27_25_saudi_005", "saudi", "ابي نصيحة سريعة", ("ابدأ", "بسيط"), "advice"),
    HeldoutPrompt("phase27_25_saudi_006", "saudi", "ودي ارتب يومي", ("ثلاث", "الأول"), "planning"),
    HeldoutPrompt("phase27_25_saudi_007", "saudi", "متوتر شوي", ("يهونها", "اهدأ"), "support"),
    HeldoutPrompt("phase27_25_saudi_008", "saudi", "مشكور يا بعدي", ("العفو", "حاضر"), "thanks"),
)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run Phase 27.25 held-out canary")
    p.add_argument("--tokenizer", type=Path, default=DEFAULT_TOKENIZER)
    p.add_argument("--checkpoints", type=Path, default=DEFAULT_CHECKPOINTS)
    p.add_argument("--checkpoint-name", default=DEFAULT_CHECKPOINT)
    p.add_argument("--previous-report", type=Path, default=DEFAULT_PREVIOUS_REPORT)
    p.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    p.add_argument("--samples", type=Path, default=DEFAULT_SAMPLES)
    p.add_argument("--device", default="auto")
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


def _evaluate(args: argparse.Namespace) -> tuple[list[dict[str, Any]], Counter[str]]:
    generator = NativeGenerator(
        NativeGeneratorConfig(
            tokenizer_path=args.tokenizer,
            checkpoints_root=args.checkpoints,
            checkpoint_name=args.checkpoint_name,
            generator_name="sf_10m_phase27_24_min_lexical",
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
    results: list[dict[str, Any]] = []
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
        results.append(
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
    return results, reasons


def _write_samples(path: Path, results: list[dict[str, Any]]) -> None:
    lines = ["# Phase 27.25 Held-out Generation Canary", ""]
    for item in results:
        lines.extend(
            [
                f"## {item['id']} — {item['dialect']} — {item['category']} — {'PASS' if item['passed'] else 'FAIL'}",
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
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    args = parse_args()
    if not (args.tokenizer / "meta.json").exists():
        print(f"error: missing tokenizer at {args.tokenizer}", file=sys.stderr)
        return 1
    ckpt_dir = args.checkpoints / args.checkpoint_name
    if not (ckpt_dir / "state.pt").exists():
        print(f"error: missing checkpoint at {ckpt_dir}", file=sys.stderr)
        return 1

    previous = _load_previous(args.previous_report).get("current", {})
    results, reasons = _evaluate(args)
    total = len(results)
    passed = sum(1 for row in results if row["passed"])
    guard_passed = sum(1 for row in results if row["guard_reason"] == "passed")
    semantic = sum(1 for row in results if row["semantic_match"])
    categories: dict[str, dict[str, int]] = {}
    for row in results:
        bucket = categories.setdefault(row["category"], {"passed": 0, "total": 0})
        bucket["total"] += 1
        bucket["passed"] += int(bool(row["passed"]))

    status = (
        "PASSED_HELDOUT_GENERATION_CANARY_READY_FOR_LIMITED_RUNTIME_TRIAL"
        if passed == total
        else "FAILED_HELDOUT_GENERATION_CANARY_BLOCK_RUNTIME"
    )
    report = {
        "phase": "Phase 27.25",
        "status": status,
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "tokenizer": _rel(args.tokenizer),
        "checkpoint_root": _rel(args.checkpoints),
        "checkpoint_name": args.checkpoint_name,
        "previous_phase27_24": {
            "passed": int(previous.get("passed", 0) or 0),
            "exact_clean": int(previous.get("exact_clean", 0) or 0),
            "semantic_match": int(previous.get("semantic_match", 0) or 0),
            "guard_passed": int(previous.get("guard_passed", 0) or 0),
        },
        "current": {
            "passed": passed,
            "failed": total - passed,
            "eval_records": total,
            "pass_rate": round(passed / total, 4) if total else 0.0,
            "semantic_match": semantic,
            "guard_passed": guard_passed,
            "reason_counts": dict(Counter(reasons)),
            "category_breakdown": categories,
        },
        "runtime_allowed": False,
        "limited_runtime_trial_allowed": passed == total,
        "sf50m_allowed": False,
        "decision": (
            "Held-out canary passed. Runtime still needs a separate limited-trial switch and monitoring."
            if passed == total
            else "Held-out prompts expose memorization and weak generalization. Keep templates as runtime brain."
        ),
        "next_phase": (
            "Phase 27.26 — limited runtime trial design"
            if passed == total
            else "Phase 27.26 — held-out objective repair and generalization training"
        ),
        "failures": [row for row in results if not row["passed"]],
        "results": results,
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _write_samples(args.samples, results)

    print("SF.AI — Phase 27.25 held-out generation canary")
    print(f"  status       : {status}")
    print(f"  checkpoint   : {args.checkpoint_name}")
    print(f"  passed       : {passed}/{total}")
    print(f"  semantic     : {semantic}/{total}")
    print(f"  guard_passed : {guard_passed}/{total}")
    print(f"  reasons      : {dict(reasons)}")
    print("  runtime      : blocked")
    print(f"  report       : {args.report}")
    print(f"  samples      : {args.samples}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
