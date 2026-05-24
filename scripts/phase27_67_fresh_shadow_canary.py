#!/usr/bin/env python3
"""Phase 27.67 fresh shadow canary for the Phase 27.66 candidate.

This phase does not train. It evaluates the Phase 27.66 checkpoint against
fresh, author-written MSA/Saudi prompts that are not exact matches for the
Phase 27.60 canary or the Phase 27.66 repair curriculum.

Runtime remains blocked regardless of the result. A pass only permits a later
guarded runtime-review phase.
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
from sf_ai.modules.chat.generation_guard import GenerationGuard  # noqa: E402
from sf_ai.modules.chat.native_generator import NativeGenerator, NativeGeneratorConfig  # noqa: E402


DEFAULT_TOKENIZER = ROOT / "artifacts/tokenizers/sf_bpe/v8_phase27_65"
DEFAULT_CHECKPOINTS = ROOT / "artifacts/eval/phase27_66_v8_bounded_topic_repair/checkpoints"
DEFAULT_CHECKPOINT_NAME = "sf-10m-step6200"
DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_67_fresh_shadow_canary_report.json"
DEFAULT_SAMPLES = ROOT / "artifacts/samples/phase27_67_fresh_shadow_canary.md"
DEFAULT_DOC = ROOT / "docs/PHASE27_67_FRESH_SHADOW_CANARY_REPORT.md"


@dataclass(frozen=True)
class ShadowCase:
    id: str
    dialect: str
    prompt: str
    intent: str
    topic: str
    family: str
    expected_any: tuple[str, ...]


FRESH_SHADOW_CASES: tuple[ShadowCase, ...] = (
    ShadowCase("open_social_01", "saudi", "ودي اسمع منك سوالف خفيفة", "open_social", "", "open_social", ("نسولف", "سولف", "موضوع", "خفيف")),
    ShadowCase("open_social_02", "msa", "ابدأ معي كلامًا لطيفًا", "open_social", "", "open_social", ("حديث", "موضوع", "نبدأ", "خفيف")),
    ShadowCase("open_social_03", "saudi", "افتح لي سالفة بسيطة", "open_social", "", "open_social", ("سولف", "موضوع", "يومك", "نبدأ")),
    ShadowCase("open_social_04", "msa", "لنبدأ حديثًا عاديًا", "open_social", "", "open_social", ("حديث", "موضوع", "نبدأ")),
    ShadowCase("open_social_05", "saudi", "ابي كلام عادي بدون موضوع كبير", "open_social", "", "open_social", ("نسولف", "موضوع", "خفيف")),
    ShadowCase("open_social_06", "msa", "اختر لي شيئًا نتحدث عنه", "open_social", "", "open_social", ("موضوع", "حديث", "نبدأ")),
    ShadowCase("open_social_07", "saudi", "وش سالفتك اليوم", "open_social", "", "open_social", ("سولف", "يومك", "موضوع")),
    ShadowCase("open_social_08", "msa", "أريد حوارًا بسيطًا لا أكثر", "open_social", "", "open_social", ("حوار", "موضوع", "نبدأ")),
    ShadowCase("open_social_09", "saudi", "خل الجو خفيف وسولف", "open_social", "", "open_social", ("خفيف", "سولف", "موضوع")),
    ShadowCase("open_social_10", "msa", "هات فكرة لطيفة للكلام", "open_social", "", "open_social", ("موضوع", "حديث", "نبدأ", "فكرة", "نتحدث")),
    ShadowCase("followup_01", "saudi", "ما وضحت لي زين", "followup", "", "followup", ("أقصد", "اقصد", "وضح", "أبسط", "خطوة")),
    ShadowCase("followup_02", "msa", "أعد المعنى بطريقة أوضح", "followup", "", "followup", ("أقصد", "الفكرة", "أبسط", "وضح")),
    ShadowCase("followup_03", "saudi", "طيب بعد كلامك وش الخطوة", "followup", "", "followup", ("بعدها", "خطوة", "ابدأ")),
    ShadowCase("followup_04", "msa", "ما الفكرة التي تريدها بالضبط", "followup", "", "followup", ("أقصد", "الفكرة", "يعني")),
    ShadowCase("followup_05", "saudi", "يعني وش المطلوب مني", "followup", "", "followup", ("يعني", "خطوة", "ابدأ")),
    ShadowCase("followup_06", "msa", "بسّطها لي أكثر", "followup", "", "followup", ("أبسط", "ابدأ", "خطوة")),
    ShadowCase("followup_07", "saudi", "ما دخلت مخي اشرحها", "followup", "", "followup", ("أقصد", "الفكرة", "وضح")),
    ShadowCase("followup_08", "msa", "تابع الشرح من النقطة الأخيرة", "followup", "", "followup", ("نكمل", "بعدها", "الفكرة")),
    ShadowCase("followup_09", "saudi", "وش تقصد بهالكلام", "followup", "", "followup", ("أقصد", "اقصد", "يعني")),
    ShadowCase("followup_10", "msa", "أريد صياغة أبسط للفكرة", "followup", "", "followup", ("أبسط", "الفكرة", "خطوة")),
    ShadowCase("planning_01", "saudi", "ابي ابدأ يومي صح", "planning", "", "planning", ("ابدأ", "مهمة", "مهام", "خطوة")),
    ShadowCase("planning_02", "msa", "رتب لي بداية عملية", "planning", "", "planning", ("رتب", "ابدأ", "مهمة", "خطوة")),
    ShadowCase("planning_03", "saudi", "عندي لخبطة بالمهام", "planning", "", "planning", ("مهام", "الأهم", "خطوة")),
    ShadowCase("planning_04", "msa", "كيف أضع أولوية لعملي", "planning", "", "planning", ("أولويات", "مهمة", "ابدأ")),
    ShadowCase("planning_05", "saudi", "وش اول شي اسويه اليوم", "planning", "", "planning", ("ابدأ", "الأهم", "خطوة")),
    ShadowCase("planning_06", "msa", "ساعدني أختار مهمة واحدة", "planning", "", "planning", ("مهمة", "ابدأ", "الأهم")),
    ShadowCase("planning_07", "saudi", "ابي طريقة سهلة للترتيب", "planning", "", "planning", ("رتب", "مهام", "خطوة")),
    ShadowCase("planning_08", "msa", "دلني على خطة قصيرة", "planning", "", "planning", ("خطة", "مهمة", "ابدأ")),
    ShadowCase("planning_09", "saudi", "مهامي كثيره ومادري من وين", "planning", "", "planning", ("مهام", "ابدأ", "الأهم")),
    ShadowCase("planning_10", "msa", "كيف أبدأ بلا تشتت", "planning", "", "planning", ("ابدأ", "مهمة", "خطوة")),
    ShadowCase("support_01", "saudi", "احس بضيق بسيط", "support", "", "support", ("نفس", "تهدأ", "هون", "خفف")),
    ShadowCase("support_02", "msa", "أحتاج جملة تهدئني", "support", "", "support", ("تنفس", "بهدوء", "راحة")),
    ShadowCase("support_03", "saudi", "مضغوط شوي وش اسوي", "support", "", "support", ("نفس", "اهدأ", "خطوة")),
    ShadowCase("support_04", "msa", "أنا مرتبك وأريد هدوءًا", "support", "", "support", ("تنفس", "هدوء", "راحة")),
    ShadowCase("support_05", "saudi", "ابي اروق بدون كلام كثير", "support", "", "support", ("نفس", "خفف", "تهدأ")),
    ShadowCase("support_06", "msa", "كيف أستعيد تركيزي بهدوء", "support", "", "support", ("تنفس", "خطوة", "راحة")),
    ShadowCase("support_07", "saudi", "توترت من البداية", "support", "", "support", ("نفس", "اهدأ", "خطوة")),
    ShadowCase("support_08", "msa", "طمئني بكلام قصير", "support", "", "support", ("تستطيع", "تنفس", "راحة", "نفس", "هون")),
    ShadowCase("support_09", "saudi", "احس اني مشتت ومتوتر", "support", "", "support", ("نفس", "ركز", "خطوة")),
    ShadowCase("support_10", "msa", "أريد أن أهدأ قليلًا", "support", "", "support", ("اهدأ", "تنفس", "بهدوء")),
    ShadowCase("topic_01", "msa", "فسر الوفاء بجملة قصيرة", "topic", "الوفاء", "topic", ("الوفاء",)),
    ShadowCase("topic_02", "saudi", "وش هو التعاون بين الناس", "topic", "التعاون", "topic", ("التعاون",)),
    ShadowCase("topic_03", "msa", "عرّف الصبر تعريفًا بسيطًا", "topic", "الصبر", "topic", ("الصبر",)),
    ShadowCase("topic_04", "saudi", "الاحترام كيف تفهمه", "topic", "الاحترام", "topic", ("الاحترام",)),
    ShadowCase("topic_05", "msa", "ما معنى الهدوء في الحياة", "topic", "الهدوء", "topic", ("الهدوء",)),
    ShadowCase("topic_06", "saudi", "الصدق وش فايدته", "topic", "الصدق", "topic", ("الصدق",)),
    ShadowCase("topic_07", "msa", "اشرح الصداقة دون إطالة", "topic", "الصداقة", "topic", ("الصداقة",)),
    ShadowCase("topic_08", "saudi", "الشجاعة متى تظهر", "topic", "الشجاعة", "topic", ("الشجاعة",)),
    ShadowCase("topic_09", "msa", "أعطني معنى التعاون ببساطة", "topic", "التعاون", "topic", ("التعاون",)),
    ShadowCase("topic_10", "saudi", "وش معنى الوفاء باختصار", "topic", "الوفاء", "topic", ("الوفاء",)),
)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run Phase 27.67 fresh shadow canary")
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
    for pair in (*FAMILY_BALANCE_REPAIR, *TOPIC_EMPHASIS_REPAIR):
        previous[_surface(pair.prompt)] = "phase27_66_repair_curriculum"

    rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    for case in FRESH_SHADOW_CASES:
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
            generator_name="sf_10m_phase27_66_v8_bounded_topic_repair",
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
    for case in FRESH_SHADOW_CASES:
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
    lines = ["# Phase 27.67 Fresh Shadow Canary", ""]
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
        "# Phase 27.67 — Fresh Shadow Canary",
        "",
        "## الخلاصة",
        "",
        "هذه مرحلة تقييم فقط على checkpoint Phase 27.66 بأسئلة غير مرئية. لا تدريب ولا فتح واجهة.",
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
    strong = summary["passed"] >= 45 and novelty_pass
    status = (
        "PASSED_FRESH_SHADOW_CANARY_READY_FOR_GUARDED_RUNTIME_REVIEW"
        if passed
        else (
            "STRONG_FRESH_SHADOW_CANARY_RUNTIME_BLOCKED"
            if strong
            else "FAILED_FRESH_SHADOW_CANARY_RUNTIME_BLOCKED"
        )
    )
    novelty_summary = {
        "novel": sum(1 for row in novelty_rows if row["novel"]),
        "total": len(novelty_rows),
        "duplicates": [row for row in novelty_rows if not row["novel"]],
    }
    report = {
        "phase": "Phase 27.67",
        "status": status,
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "training_started": False,
        "training_scope": "no training; fresh shadow canary evaluation only",
        "tokenizer": _rel(args.tokenizer),
        "checkpoint_root": _rel(args.checkpoints),
        "checkpoint_name": args.checkpoint_name,
        "candidate_generator": "sf_10m_phase27_66_v8_bounded_topic_repair",
        "canary_cases": len(FRESH_SHADOW_CASES),
        "novelty_summary": novelty_summary,
        "summary": summary,
        "rows": rows,
        "decisions": {
            "runtime_switch_allowed": False,
            "ui_open_allowed": False,
            "sf50m_allowed": False,
            "phase28_allowed": False,
            "guarded_runtime_review_allowed": passed,
            "repair_required_before_runtime": not passed,
        },
        "decision": (
            "Fresh shadow canary passed. Runtime remains blocked; next phase may run a guarded runtime-review gate."
            if passed
            else "Fresh shadow canary did not fully pass. Runtime remains blocked; inspect failures before any UI/runtime change."
        ),
        "next_phase": (
            "Phase 27.68 — guarded runtime-review gate for Phase 27.66 candidate"
            if passed
            else "Phase 27.68 — inspect Phase 27.67 failures and repair before runtime"
        ),
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _write_samples(args.samples, rows)
    _write_doc(report, args.doc)

    print("SF.AI — Phase 27.67 fresh shadow canary")
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
