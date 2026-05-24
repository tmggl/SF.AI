#!/usr/bin/env python3
"""Phase 27.60 broader natural-dialogue canary.

This phase does not train. It evaluates the Phase 27.59 bounded-alignment
checkpoint against fresh, natural MSA/Saudi prompts that were not the exact
bounded probe. Runtime stays blocked regardless of the result.
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

from scripts.phase27_26_heldout_objective_repair import _rel  # noqa: E402
from scripts.phase27_58_tokenizer_bounded_alignment_probe import (  # noqa: E402
    _expected_ok,
    _family_terms,
    _surface,
)
from sf_ai.modules.chat.generation_guard import GenerationGuard  # noqa: E402
from sf_ai.modules.chat.native_generator import NativeGenerator, NativeGeneratorConfig  # noqa: E402


DEFAULT_TOKENIZER = ROOT / "artifacts/tokenizers/sf_bpe/v7_phase27_58"
DEFAULT_CHECKPOINTS = ROOT / "artifacts/eval/phase27_59_bounded_alignment_repair/checkpoints"
DEFAULT_CHECKPOINT_NAME = "sf-10m-step6400"
DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_60_broader_natural_dialogue_canary_report.json"
DEFAULT_SAMPLES = ROOT / "artifacts/samples/phase27_60_broader_natural_dialogue_canary.md"
DEFAULT_DOC = ROOT / "docs/PHASE27_60_BROADER_NATURAL_DIALOGUE_CANARY_REPORT.md"


@dataclass(frozen=True)
class CanaryCase:
    id: str
    dialect: str
    prompt: str
    intent: str
    topic: str
    family: str
    expected_any: tuple[str, ...]


CANARY_CASES: tuple[CanaryCase, ...] = (
    CanaryCase("open_social_01", "saudi", "ابي اسولف شوي", "open_social", "", "open_social", ("نسولف", "موضوع", "يومك")),
    CanaryCase("open_social_02", "saudi", "خلنا نفتح موضوع بسيط", "open_social", "", "open_social", ("موضوع", "نبدأ", "نسولف")),
    CanaryCase("open_social_03", "msa", "حدثني حديثًا لطيفًا", "open_social", "", "open_social", ("حديث", "موضوع", "نبدأ")),
    CanaryCase("open_social_04", "saudi", "وش عندك كلام خفيف", "open_social", "", "open_social", ("خفيف", "موضوع", "يومك")),
    CanaryCase("open_social_05", "msa", "افتح معي حوارًا قصيرًا", "open_social", "", "open_social", ("حوار", "موضوع", "نبدأ")),
    CanaryCase("open_social_06", "saudi", "ما عندي موضوع سولف انت", "open_social", "", "open_social", ("سولف", "موضوع", "يومك")),
    CanaryCase("followup_01", "saudi", "ما فهمت قصدك", "followup", "", "followup", ("أقصد", "اقصد", "الفكرة")),
    CanaryCase("followup_02", "msa", "هل توضح لي الفكرة", "followup", "", "followup", ("أقصد", "الفكرة", "ابدأ")),
    CanaryCase("followup_03", "saudi", "وبعدين وش اسوي", "followup", "", "followup", ("بعدها", "كمل", "خطوة")),
    CanaryCase("followup_04", "msa", "أكمل شرحك", "followup", "", "followup", ("نكمل", "الفكرة", "بعده")),
    CanaryCase("followup_05", "saudi", "طيب وش تقصد بالضبط", "followup", "", "followup", ("أقصد", "اقصد", "الفكرة")),
    CanaryCase("followup_06", "msa", "فسرها بطريقة أبسط", "followup", "", "followup", ("أقصد", "أبسط", "ابدأ")),
    CanaryCase("planning_01", "saudi", "ابي اخلي يومي مرتب", "planning", "", "planning", ("ابدأ", "مهام", "خطوة")),
    CanaryCase("planning_02", "msa", "ساعدني أبدأ عملي اليوم", "planning", "", "planning", ("مهمة", "ابدأ", "مهام")),
    CanaryCase("planning_03", "saudi", "عندي اشياء كثيره وش ابدا فيه", "planning", "", "planning", ("ابدأ", "الأهم", "اهم")),
    CanaryCase("planning_04", "msa", "أريد خطة صغيرة لبداية اليوم", "planning", "", "planning", ("خطة", "ابدأ", "مهمة")),
    CanaryCase("planning_05", "saudi", "رتب لي اول خطوه", "planning", "", "planning", ("خطوة", "ابدأ", "واضح")),
    CanaryCase("planning_06", "msa", "كيف أختار أول مهمة", "planning", "", "planning", ("مهمة", "الأهم", "ابدأ")),
    CanaryCase("support_01", "saudi", "ضايق صدري شوي", "support", "", "support", ("نفس", "تهدأ", "هون")),
    CanaryCase("support_02", "msa", "أشعر بضغط وأحتاج هدوءًا", "support", "", "support", ("تنفس", "بهدوء", "راحة")),
    CanaryCase("support_03", "saudi", "ابي كلام يطمني", "support", "", "support", ("تهدأ", "تقدر", "نفس")),
    CanaryCase("support_04", "msa", "أنا قلق من البداية", "support", "", "support", ("تنفس", "خطوة", "يقلقك")),
    CanaryCase("support_05", "saudi", "حاس اني مشتت", "support", "", "support", ("نفس", "خطوة", "ركز")),
    CanaryCase("support_06", "msa", "كيف أهدأ دون تعقيد", "support", "", "support", ("تنفس", "بهدوء", "لحظة")),
    CanaryCase("topic_01", "msa", "عرّف لي الوفاء", "topic", "الوفاء", "topic", ("الوفاء",)),
    CanaryCase("topic_02", "saudi", "وش معنى التعاون", "topic", "التعاون", "topic", ("التعاون",)),
    CanaryCase("topic_03", "msa", "ما المقصود بالصبر", "topic", "الصبر", "topic", ("الصبر",)),
    CanaryCase("topic_04", "saudi", "الاحترام وش هو", "topic", "الاحترام", "topic", ("الاحترام",)),
    CanaryCase("topic_05", "msa", "اشرح الهدوء بجملة", "topic", "الهدوء", "topic", ("الهدوء",)),
    CanaryCase("topic_06", "saudi", "وش يعني الصدق ببساطه", "topic", "الصدق", "topic", ("الصدق",)),
)


_FORBIDDEN_BY_FAMILY: dict[str, tuple[str, ...]] = {
    "open_social": ("العفو", "مهام", "الأهم", "اولوية", "اولويات", "نفس", "تنفس"),
    "followup": ("العفو", "مهام", "اولويات", "نفس", "تنفس"),
    "planning": ("العفو", "نسولف", "يومك", "نفس", "تنفس"),
    "support": ("العفو", "مهام", "الصداقة", "الشجاعة", "الصدق"),
    "topic": ("مهام", "اولويات", "نفس", "تنفس"),
}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run Phase 27.60 broader natural-dialogue canary")
    p.add_argument("--tokenizer", type=Path, default=DEFAULT_TOKENIZER)
    p.add_argument("--checkpoints", type=Path, default=DEFAULT_CHECKPOINTS)
    p.add_argument("--checkpoint-name", default=DEFAULT_CHECKPOINT_NAME)
    p.add_argument("--device", default="auto")
    p.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    p.add_argument("--samples", type=Path, default=DEFAULT_SAMPLES)
    p.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    return p.parse_args()


def _family_ok(text: str, family: str, families: dict[str, tuple[str, ...]]) -> bool:
    surface = _surface(text)
    allowed = any(_surface(term) in surface for term in families.get(family, ()))
    forbidden = any(_surface(term) in surface for term in _FORBIDDEN_BY_FAMILY.get(family, ()))
    return allowed and not forbidden


def _evaluate(args: argparse.Namespace) -> list[dict[str, Any]]:
    generator = NativeGenerator(
        NativeGeneratorConfig(
            tokenizer_path=args.tokenizer,
            checkpoints_root=args.checkpoints,
            checkpoint_name=args.checkpoint_name,
            generator_name="sf_10m_phase27_59_alignment_repair",
            model_size="sf-10m",
            seq_len=80,
            max_new_tokens=28,
            temperature=1.0,
            top_k=0,
            no_repeat_ngram_size=3,
            repetition_penalty=1.12,
            device=args.device,
            dialogue_prompt=True,
        )
    )
    guard = GenerationGuard(min_chars=4)
    families = _family_terms()
    rows: list[dict[str, Any]] = []
    for case in CANARY_CASES:
        out = generator.generate(
            case.prompt,
            dialect=case.dialect,
            intent=case.intent,
            topic=case.topic,
            max_new_tokens=28,
            temperature=1.0,
            top_k=0,
        )
        verdict = guard.inspect(out.text) if case.family == "topic" else guard.inspect_for_prompt(case.prompt, out.text)
        expected = _expected_ok(out.text, case.expected_any)
        family = _family_ok(out.text, case.family, families)
        passed = bool(out.used and verdict.allowed and expected and family)
        if passed:
            reason = "passed"
        elif not out.used:
            reason = f"generator:{out.reason}"
        elif not verdict.allowed:
            reason = f"guard:{verdict.reason}"
        elif not expected:
            reason = "expected_terms_missing"
        else:
            reason = "response_family_mismatch"
        rows.append(
            {
                "id": case.id,
                "dialect": case.dialect,
                "prompt": case.prompt,
                "intent": case.intent,
                "topic": case.topic,
                "family": case.family,
                "expected_any": list(case.expected_any),
                "response": out.text,
                "generator_used": out.used,
                "guard_allowed": verdict.allowed,
                "guard_reason": verdict.reason,
                "expected_ok": expected,
                "family_ok": family,
                "passed": passed,
                "reason": reason,
            }
        )
    return rows


def _summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    families = sorted({str(row["family"]) for row in rows})
    passed = sum(1 for row in rows if row["passed"])
    return {
        "passed": passed,
        "total": len(rows),
        "pass_rate": round(passed / len(rows), 4) if rows else 0.0,
        "family_summary": {
            family: {
                "passed": sum(1 for row in rows if row["family"] == family and row["passed"]),
                "total": sum(1 for row in rows if row["family"] == family),
            }
            for family in families
        },
        "reason_counts": dict(Counter(str(row["reason"]) for row in rows)),
    }


def _write_samples(path: Path, rows: list[dict[str, Any]]) -> None:
    lines = ["# Phase 27.60 Broader Natural-Dialogue Canary", ""]
    for row in rows:
        lines.extend(
            [
                f"## {row['id']} — {'PASS' if row['passed'] else 'FAIL'}",
                "",
                f"- family: {row['family']}",
                f"- prompt: {row['prompt']}",
                f"- response: {row['response']}",
                f"- guard_reason: {row['guard_reason']}",
                f"- expected_ok: {row['expected_ok']}",
                f"- family_ok: {row['family_ok']}",
                f"- reason: {row['reason']}",
                "",
            ]
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_doc(report: dict[str, Any], path: Path) -> None:
    summary = report["summary"]
    lines = [
        "# Phase 27.60 — Broader Natural-Dialogue Canary",
        "",
        "## الخلاصة",
        "",
        "هذه مرحلة تقييم فقط على checkpoint Phase 27.59. لا تدريب جديد ولا فتح واجهة.",
        "",
        f"- status: `{report['status']}`",
        f"- checkpoint: `{report['checkpoint_root']}/{report['checkpoint_name']}`",
        f"- canary pass: `{summary['passed']}/{summary['total']}`",
        f"- runtime switch allowed: `{report['decisions']['runtime_switch_allowed']}`",
        "",
        "## القرار",
        "",
        report["decision"],
        "",
        "## التالي",
        "",
        report["next_phase"],
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    ckpt_dir = args.checkpoints / args.checkpoint_name
    if not (args.tokenizer / "meta.json").exists():
        print(f"error: missing tokenizer at {args.tokenizer}", file=sys.stderr)
        return 1
    if not (ckpt_dir / "meta.json").exists() or not (ckpt_dir / "state.pt").exists():
        print(f"error: missing checkpoint at {ckpt_dir}", file=sys.stderr)
        return 1

    rows = _evaluate(args)
    summary = _summary(rows)
    passed = summary["passed"] == summary["total"]
    status = (
        "PASSED_BROADER_NATURAL_DIALOGUE_CANARY_READY_FOR_GUARDED_RUNTIME_REVIEW"
        if passed
        else "FAILED_BROADER_NATURAL_DIALOGUE_CANARY_RUNTIME_BLOCKED"
    )
    report = {
        "phase": "Phase 27.60",
        "status": status,
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "training_started": False,
        "evaluation_only": True,
        "tokenizer": _rel(args.tokenizer),
        "checkpoint_root": _rel(args.checkpoints),
        "checkpoint_name": args.checkpoint_name,
        "candidate_generator": "sf_10m_phase27_59_alignment_repair",
        "canary_cases": len(CANARY_CASES),
        "summary": summary,
        "rows": rows,
        "decisions": {
            "runtime_switch_allowed": False,
            "ui_open_allowed": False,
            "sf50m_allowed": False,
            "phase28_allowed": False,
            "guarded_runtime_review_allowed": passed,
        },
        "decision": (
            "Broader canary passed. Keep runtime blocked until a separate guarded runtime-review phase checks live API behavior."
            if passed
            else "Broader canary failed. Keep runtime blocked and repair natural-dialogue generalization."
        ),
        "next_phase": (
            "Phase 27.61 — guarded runtime review for Phase 27.59 checkpoint"
            if passed
            else "Phase 27.61 — inspect Phase 27.60 failures and repair broader natural dialogue"
        ),
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _write_samples(args.samples, rows)
    _write_doc(report, args.doc)

    print("SF.AI — Phase 27.60 broader natural-dialogue canary")
    print(f"  status      : {status}")
    print(f"  checkpoint  : {_rel(args.checkpoints)}/{args.checkpoint_name}")
    print(f"  canary      : {summary['passed']}/{summary['total']}")
    print(f"  reasons     : {summary['reason_counts']}")
    print("  runtime     : blocked")
    print(f"  report      : {args.report}")
    print(f"  samples     : {args.samples}")
    print(f"  doc         : {args.doc}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
