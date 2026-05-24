#!/usr/bin/env python3
"""Phase 27.69 new fresh shadow canary after Phase 27.68 repair.

This phase does not train. It evaluates the Phase 27.68 checkpoint against a
new unseen MSA/Saudi prompt set that is distinct from Phase 27.60, Phase 27.67,
and Phase 27.68 repair prompts.

Runtime remains blocked regardless of the result. A pass only allows a later
guarded live API review, not direct UI activation.
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
from scripts.phase27_60_broader_natural_dialogue_canary import (  # noqa: E402
    CANARY_CASES as PHASE27_60_CASES,
    _FORBIDDEN_BY_FAMILY,
)
from scripts.phase27_62_family_balance_repair import FAMILY_BALANCE_REPAIR  # noqa: E402
from scripts.phase27_66_v8_bounded_topic_repair import TOPIC_EMPHASIS_REPAIR  # noqa: E402
from scripts.phase27_67_fresh_shadow_canary import FRESH_SHADOW_CASES as PHASE27_67_CASES  # noqa: E402
from scripts.phase27_68_shadow_failure_repair import SHADOW_FAILURE_REPAIR  # noqa: E402
from sf_ai.modules.chat.generation_guard import GenerationGuard  # noqa: E402
from sf_ai.modules.chat.native_generator import NativeGenerator, NativeGeneratorConfig  # noqa: E402


DEFAULT_TOKENIZER = ROOT / "artifacts/tokenizers/sf_bpe/v8_phase27_65"
DEFAULT_CHECKPOINTS = ROOT / "artifacts/eval/phase27_68_shadow_failure_repair/checkpoints"
DEFAULT_CHECKPOINT_NAME = "sf-10m-step5600"
DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_69_new_fresh_shadow_canary_report.json"
DEFAULT_SAMPLES = ROOT / "artifacts/samples/phase27_69_new_fresh_shadow_canary.md"
DEFAULT_DOC = ROOT / "docs/PHASE27_69_NEW_FRESH_SHADOW_CANARY_REPORT.md"


@dataclass(frozen=True)
class ShadowCase:
    id: str
    dialect: str
    prompt: str
    intent: str
    topic: str
    family: str
    expected_any: tuple[str, ...]


NEW_FRESH_CASES: tuple[ShadowCase, ...] = (
    ShadowCase("open_social_01", "saudi", "وش رايك نسولف شوي", "open_social", "", "open_social", ("نسولف", "سولف", "موضوع", "خفيف")),
    ShadowCase("open_social_02", "msa", "حدثني عن شيء بسيط", "open_social", "", "open_social", ("حديث", "موضوع", "نبدأ", "بسيط", "نسولف", "خفيف")),
    ShadowCase("open_social_03", "saudi", "خلنا ناخذ كلام خفيف", "open_social", "", "open_social", ("خفيف", "نسولف", "موضوع")),
    ShadowCase("open_social_04", "msa", "افتح موضوعًا هادئًا", "open_social", "", "open_social", ("موضوع", "حديث", "نبدأ")),
    ShadowCase("open_social_05", "saudi", "عطني سوالف بسيطة", "open_social", "", "open_social", ("سوالف", "نسولف", "موضوع", "بسيط")),
    ShadowCase("open_social_06", "msa", "أريد كلامًا وديًا قصيرًا", "open_social", "", "open_social", ("كلام", "حديث", "موضوع", "قصير")),
    ShadowCase("open_social_07", "saudi", "تكلم معي عن شي لطيف", "open_social", "", "open_social", ("موضوع", "لطيف", "يومك")),
    ShadowCase("open_social_08", "msa", "اختر حديثًا خفيفًا بيننا", "open_social", "", "open_social", ("حديث", "خفيف", "موضوع", "نسولف")),
    ShadowCase("open_social_09", "saudi", "ودي بموضوع سوالف", "open_social", "", "open_social", ("موضوع", "سوالف", "نسولف")),
    ShadowCase("open_social_10", "msa", "ابدأ محادثة سهلة", "open_social", "", "open_social", ("محادثة", "نبدأ", "موضوع", "بسيط")),
    ShadowCase("open_social_11", "saudi", "هات كلام يمشي الوقت", "open_social", "", "open_social", ("كلام", "نسولف", "موضوع", "سالفة", "خفيفة")),
    ShadowCase("open_social_12", "msa", "لنختر موضوعًا صغيرًا", "open_social", "", "open_social", ("موضوع", "صغير", "نبدأ")),
    ShadowCase("followup_01", "saudi", "وضح لي مقصدك اكثر", "followup", "", "followup", ("أقصد", "اقصد", "وضح", "خطوة", "الفكرة")),
    ShadowCase("followup_02", "msa", "أعد شرح النقطة ببساطة", "followup", "", "followup", ("أقصد", "الفكرة", "أبسط", "خطوة")),
    ShadowCase("followup_03", "saudi", "ما فهمت وش تبي تقول", "followup", "", "followup", ("أقصد", "يعني", "الفكرة")),
    ShadowCase("followup_04", "msa", "ما الخطوة بعد هذا الشرح", "followup", "", "followup", ("بعدها", "خطوة", "نكمل")),
    ShadowCase("followup_05", "saudi", "طيب كمل من هنا", "followup", "", "followup", ("نكمل", "بعدها", "خطوة")),
    ShadowCase("followup_06", "msa", "اجعل الفكرة أوضح", "followup", "", "followup", ("الفكرة", "أوضح", "خطوة")),
    ShadowCase("followup_07", "saudi", "يعني ابدا من وين", "followup", "", "followup", ("يعني", "ابدأ", "خطوة")),
    ShadowCase("followup_08", "msa", "فسر كلامك مرة أخرى", "followup", "", "followup", ("أقصد", "الفكرة", "أبسط")),
    ShadowCase("followup_09", "saudi", "وش قصدك بالضبط", "followup", "", "followup", ("أقصد", "اقصد", "يعني")),
    ShadowCase("followup_10", "msa", "اختصر لي المعنى", "followup", "", "followup", ("أقصد", "الفكرة", "ببساطة", "أبسط", "ابدأ", "القريب")),
    ShadowCase("followup_11", "saudi", "ما وصلتني الفكرة", "followup", "", "followup", ("الفكرة", "أقصد", "وضح", "يعني", "خطوة")),
    ShadowCase("followup_12", "msa", "تابع من آخر جملة", "followup", "", "followup", ("نكمل", "بعدها", "بعده", "الفكرة", "أقصد", "خطوة", "أبسط")),
    ShadowCase("planning_01", "saudi", "ابي ارتب اولوياتي اليوم", "planning", "", "planning", ("رتب", "أولويات", "مهام", "ابدأ")),
    ShadowCase("planning_02", "msa", "ساعدني أرتب أعمالي", "planning", "", "planning", ("رتب", "أعمال", "مهمة", "ابدأ")),
    ShadowCase("planning_03", "saudi", "من وين ابدا اذا المهام كثيره", "planning", "", "planning", ("ابدأ", "مهام", "الأهم")),
    ShadowCase("planning_04", "msa", "كيف أقسم وقتي اليوم", "planning", "", "planning", ("وقت", "مهمة", "ابدأ", "خطة")),
    ShadowCase("planning_05", "saudi", "ابي جدول بسيط لبدايتي", "planning", "", "planning", ("جدول", "ابدأ", "مهمة", "خطوة")),
    ShadowCase("planning_06", "msa", "أحتاج ترتيبًا سريعًا", "planning", "", "planning", ("ترتيب", "مهمة", "خطوة")),
    ShadowCase("planning_07", "saudi", "وش اسوي بالمهام المتراكمة", "planning", "", "planning", ("مهام", "الأهم", "ابدأ")),
    ShadowCase("planning_08", "msa", "ضع لي بداية واضحة", "planning", "", "planning", ("بداية", "واضحة", "مهمة", "ابدأ")),
    ShadowCase("planning_09", "saudi", "خلني ابدأ بدون تشتت", "planning", "", "planning", ("ابدأ", "تشتت", "خطوة", "مهمة")),
    ShadowCase("planning_10", "msa", "كيف أختصر قائمة عملي", "planning", "", "planning", ("قائمة", "عمل", "مهمة", "الأهم")),
    ShadowCase("planning_11", "saudi", "ساعدني احدد اول شي", "planning", "", "planning", ("حدد", "أول", "ابدأ", "الأهم")),
    ShadowCase("planning_12", "msa", "أريد تنظيمًا بسيطًا للمهام", "planning", "", "planning", ("تنظيم", "مهام", "مهمة", "خطة", "ابدأ")),
    ShadowCase("support_01", "saudi", "صدري ضايق وابغى اهدأ", "support", "", "support", ("نفس", "اهدأ", "راحة", "هون")),
    ShadowCase("support_02", "msa", "أشعر بتوتر وأريد طمأنينة", "support", "", "support", ("تنفس", "راحة", "طمأنينة", "اهدأ")),
    ShadowCase("support_03", "saudi", "ابي كلمة تهون علي", "support", "", "support", ("هون", "نفس", "تهدأ")),
    ShadowCase("support_04", "msa", "أحتاج هدوءًا قبل أن أبدأ", "support", "", "support", ("هدوء", "تنفس", "راحة")),
    ShadowCase("support_05", "saudi", "قلقي زايد شوي", "support", "", "support", ("قلق", "نفس", "اهدأ", "هون")),
    ShadowCase("support_06", "msa", "كيف أهدئ نفسي الآن", "support", "", "support", ("اهدأ", "تنفس", "راحة")),
    ShadowCase("support_07", "saudi", "حاس بتوتر ومحتاج اروق", "support", "", "support", ("توتر", "نفس", "تهدأ", "راحة")),
    ShadowCase("support_08", "msa", "طمئنّي بجملة قصيرة", "support", "", "support", ("تنفس", "راحة", "تستطيع", "طمأنينة", "نفس", "هون")),
    ShadowCase("support_09", "saudi", "ابي اهدى من التفكير", "support", "", "support", ("اهدأ", "نفس", "خطوة", "راحة")),
    ShadowCase("support_10", "msa", "أنا متوتر من البداية", "support", "", "support", ("متوتر", "تنفس", "خطوة", "راحة")),
    ShadowCase("support_11", "saudi", "محتاج كلام يخفف علي", "support", "", "support", ("خفف", "نفس", "هون", "راحة")),
    ShadowCase("support_12", "msa", "أريد راحة قصيرة", "support", "", "support", ("راحة", "تنفس", "لحظة")),
    ShadowCase("topic_01", "msa", "ما معنى الوفاء للناس", "topic", "الوفاء", "topic", ("الوفاء",)),
    ShadowCase("topic_02", "saudi", "التعاون وين يبان", "topic", "التعاون", "topic", ("التعاون",)),
    ShadowCase("topic_03", "msa", "اشرح الصبر في موقف صعب", "topic", "الصبر", "topic", ("الصبر",)),
    ShadowCase("topic_04", "saudi", "الاحترام وش اثره", "topic", "الاحترام", "topic", ("الاحترام",)),
    ShadowCase("topic_05", "msa", "عرّف الهدوء بعبارة بسيطة", "topic", "الهدوء", "topic", ("الهدوء",)),
    ShadowCase("topic_06", "saudi", "الصدق ليه مهم", "topic", "الصدق", "topic", ("الصدق",)),
    ShadowCase("topic_07", "msa", "ما جوهر الصداقة", "topic", "الصداقة", "topic", ("الصداقة",)),
    ShadowCase("topic_08", "saudi", "الشجاعة كيف تكون", "topic", "الشجاعة", "topic", ("الشجاعة",)),
    ShadowCase("topic_09", "msa", "أعطني مثالًا على التعاون", "topic", "التعاون", "topic", ("التعاون",)),
    ShadowCase("topic_10", "saudi", "وش يعني الوفاء مع الاصحاب", "topic", "الوفاء", "topic", ("الوفاء",)),
    ShadowCase("topic_11", "msa", "ما قيمة الاحترام", "topic", "الاحترام", "topic", ("الاحترام",)),
    ShadowCase("topic_12", "saudi", "الصبر متى نحتاجه", "topic", "الصبر", "topic", ("الصبر",)),
)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run Phase 27.69 new fresh shadow canary")
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


def _novelty_rows() -> list[dict[str, Any]]:
    previous = {_surface(case.prompt): "phase27_60_canary" for case in PHASE27_60_CASES}
    for case in PHASE27_67_CASES:
        previous[_surface(case.prompt)] = "phase27_67_shadow_canary"
    for pair in (*FAMILY_BALANCE_REPAIR, *TOPIC_EMPHASIS_REPAIR, *SHADOW_FAILURE_REPAIR):
        previous[_surface(pair.prompt)] = "phase27_repair_curriculum"

    rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    for case in NEW_FRESH_CASES:
        key = _surface(case.prompt)
        duplicate_source = previous.get(key)
        duplicate_in_suite = key in seen
        rows.append(
            {
                "id": case.id,
                "prompt": case.prompt,
                "duplicate_source": duplicate_source,
                "duplicate_in_suite": duplicate_in_suite,
                "novel": duplicate_source is None and not duplicate_in_suite,
            }
        )
        seen.add(key)
    return rows


def _evaluate(args: argparse.Namespace) -> list[dict[str, Any]]:
    generator = NativeGenerator(
        NativeGeneratorConfig(
            tokenizer_path=args.tokenizer,
            checkpoints_root=args.checkpoints,
            checkpoint_name=args.checkpoint_name,
            generator_name="sf_10m_phase27_68_shadow_failure_repair",
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
    for case in NEW_FRESH_CASES:
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
    lines = ["# Phase 27.69 New Fresh Shadow Canary", ""]
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
    novelty = report["novelty_summary"]
    lines = [
        "# Phase 27.69 — New Fresh Shadow Canary",
        "",
        "## الخلاصة",
        "",
        "هذه مرحلة تقييم فقط بعد إصلاح Phase 27.68. لا تدريب ولا فتح واجهة.",
        "",
        f"- status: `{report['status']}`",
        f"- checkpoint: `{report['checkpoint_root']}/{report['checkpoint_name']}`",
        f"- canary pass: `{summary['passed']}/{summary['total']}`",
        f"- novel prompts: `{novelty['novel']}/{novelty['total']}`",
        f"- runtime switch allowed: `{report['decisions']['runtime_switch_allowed']}`",
        "",
        "## family summary",
        "",
    ]
    for family, item in summary["family_summary"].items():
        lines.append(f"- `{family}`: `{item['passed']}/{item['total']}`")
    lines.extend(["", "## القرار", "", report["decision"], "", "## التالي", "", report["next_phase"]])
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

    novelty_rows = _novelty_rows()
    novelty_pass = all(row["novel"] for row in novelty_rows)
    rows = _evaluate(args)
    summary = _summary(rows)
    passed = summary["passed"] == summary["total"] and novelty_pass
    strong = summary["passed"] >= 56 and novelty_pass
    status = (
        "PASSED_NEW_FRESH_SHADOW_CANARY_READY_FOR_GUARDED_LIVE_API_REVIEW"
        if passed
        else (
            "STRONG_NEW_FRESH_SHADOW_CANARY_RUNTIME_BLOCKED"
            if strong
            else "FAILED_NEW_FRESH_SHADOW_CANARY_RUNTIME_BLOCKED"
        )
    )
    novelty_summary = {
        "novel": sum(1 for row in novelty_rows if row["novel"]),
        "total": len(novelty_rows),
        "duplicates": [row for row in novelty_rows if not row["novel"]],
    }
    report = {
        "phase": "Phase 27.69",
        "status": status,
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "training_started": False,
        "training_scope": "no training; new fresh shadow canary evaluation only",
        "tokenizer": _rel(args.tokenizer),
        "checkpoint_root": _rel(args.checkpoints),
        "checkpoint_name": args.checkpoint_name,
        "candidate_generator": "sf_10m_phase27_68_shadow_failure_repair",
        "canary_cases": len(NEW_FRESH_CASES),
        "novelty_summary": novelty_summary,
        "summary": summary,
        "rows": rows,
        "decisions": {
            "runtime_switch_allowed": False,
            "ui_open_allowed": False,
            "sf50m_allowed": False,
            "phase28_allowed": False,
            "guarded_live_api_review_allowed": passed,
            "repair_required_before_runtime": not passed,
        },
        "decision": (
            "New fresh shadow canary passed. Runtime remains blocked; next phase may run a guarded live API review."
            if passed
            else "New fresh shadow canary did not fully pass. Runtime remains blocked; inspect failures before any UI/runtime change."
        ),
        "next_phase": (
            "Phase 27.70 — guarded live API review for Phase 27.68 candidate"
            if passed
            else "Phase 27.70 — inspect Phase 27.69 failures and repair before runtime"
        ),
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _write_samples(args.samples, rows)
    _write_doc(report, args.doc)

    print("SF.AI — Phase 27.69 new fresh shadow canary")
    print(f"  status      : {status}")
    print(f"  checkpoint  : {args.checkpoint_name}")
    print(f"  canary      : {summary['passed']}/{summary['total']}")
    print(f"  novelty     : {novelty_summary['novel']}/{novelty_summary['total']}")
    print(f"  family      : {summary['family_summary']}")
    print(f"  report      : {_rel(args.report)}")
    print(f"  samples     : {_rel(args.samples)}")
    print("  runtime     : blocked")
    return 0 if args.report.exists() else 1


if __name__ == "__main__":
    raise SystemExit(main())
