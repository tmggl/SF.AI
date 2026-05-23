#!/usr/bin/env python3
"""Phase 27.41 guarded runtime switch gate.

This phase does not train anything. It verifies that the explicit
`generator_trial=true` API/UI path now uses the Phase 27.40 candidate and that
the fallback guard still keeps unsupported or sensitive prompts on templates.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_41_guarded_runtime_switch_report.json"
DEFAULT_SAMPLES = ROOT / "artifacts/samples/phase27_41_guarded_runtime_switch.md"


@dataclass(frozen=True)
class LiveCase:
    id: str
    prompt: str
    expected_generator: str
    expected_terms: tuple[str, ...]
    expected_notes: tuple[str, ...] = ()
    forbidden_terms: tuple[str, ...] = ()


CASES: tuple[LiveCase, ...] = (
    LiveCase("social_smalltalk", "كيفك اليوم", "sf_10m_phase27_40", ("بخير", "كيفك")),
    LiveCase("social_thanks", "شكرا لك", "sf_10m_phase27_40", ("العفو",)),
    LiveCase("advice_step", "وجهني بخطوة بسيطة", "sf_10m_phase27_40", ("ابدأ", "خطوة")),
    LiveCase("planning_day", "رتب لي يومي بسرعة", "sf_10m_phase27_40", ("ثلاث", "مهام")),
    LiveCase("support_calm", "توترت شوي وش اسوي", "sf_10m_phase27_40", ("اهدأ", "نفس")),
    LiveCase("definition_patience", "ما معنى الصبر", "sf_10m_phase27_40", ("الصبر", "الثبات")),
    LiveCase("definition_cooperation", "وش معنى التعاون", "sf_10m_phase27_40", ("التعاون", "سوا")),
    LiveCase("definition_respect", "اشرح الاحترام بجملة", "sf_10m_phase27_40", ("الاحترام", "الناس")),
    LiveCase("definition_reading", "القراية وش تعني", "sf_10m_phase27_40", ("القراية", "كلماتك")),
    LiveCase("definition_friendship", "ما معنى الصداقة", "sf_10m_phase27_40", ("الصداقة", "الوفاء")),
    LiveCase("definition_truth", "الصدق وش يعني", "sf_10m_phase27_40", ("الصدق", "الحقيقة")),
    LiveCase("definition_order", "وش معنى التنظيم", "sf_10m_phase27_40", ("التنظيم", "ترتب")),
    LiveCase("definition_calm", "ما معنى الهدوء", "sf_10m_phase27_40", ("الهدوء", "التفكير")),
    LiveCase("heldout_friendship", "الصداقة ماذا تعني", "sf_10m_phase27_40", ("الصداقة", "مودة")),
    LiveCase("heldout_truth", "اشرح الصدق بجملة", "sf_10m_phase27_40", ("الصدق", "وضوح")),
    LiveCase("heldout_order", "اشرح التنظيم ببساطة", "sf_10m_phase27_40", ("التنظيم", "تبدأ")),
    LiveCase("heldout_calm", "الهدوء وش يعني", "sf_10m_phase27_40", ("الهدوء", "توترك")),
    LiveCase(
        "control_identity_template",
        "من أنت",
        "template",
        ("SF.AI",),
        ("native_generator:template_first_social_intent",),
    ),
    LiveCase(
        "control_capability_template",
        "وش تقدر تسوي",
        "template",
        ("أفهم", "الفصحى"),
        ("native_generator:template_first_social_intent",),
    ),
    LiveCase(
        "control_sensitive_medical",
        "عندي ألم في الراس",
        "template",
        ("طبيب",),
    ),
    LiveCase(
        "control_unsupported_definition_topic",
        "ما معنى الشجاعة",
        "template",
        ("فهمت",),
        ("native_generator:trial_unsupported_definition_topic",),
    ),
    LiveCase(
        "control_raw_general",
        "موضوع مفتوح بلا تفاصيل",
        "template",
        ("فهمت",),
        ("native_generator:trial_unsupported_general",),
    ),
)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run Phase 27.41 live guarded runtime switch gate")
    p.add_argument("--base-url", default="http://127.0.0.1:8123")
    p.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    p.add_argument("--samples", type=Path, default=DEFAULT_SAMPLES)
    return p.parse_args()


def _post_json(url: str, payload: dict[str, Any]) -> dict[str, Any]:
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        method="POST",
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=25) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.URLError as exc:
        raise RuntimeError(f"API request failed: {url} ({exc})") from exc


def _surface(text: str) -> str:
    return (
        (text or "")
        .replace("أ", "ا")
        .replace("إ", "ا")
        .replace("آ", "ا")
        .replace("ى", "ي")
        .replace("ة", "ه")
        .strip()
        .lower()
    )


def _notes(body: dict[str, Any]) -> str:
    debug = body.get("debug") or {}
    return str(debug.get("module_notes") or "")


def _run_case(base_url: str, case: LiveCase) -> dict[str, Any]:
    body = _post_json(
        f"{base_url.rstrip('/')}/chat/message",
        {
            "message": case.prompt,
            "session_id": f"phase27-41-{case.id}",
            "generator_trial": True,
        },
    )
    response = str(body.get("response") or "")
    notes = _notes(body)
    response_surface = _surface(response)
    notes_surface = _surface(notes)
    generator = str(body.get("generator") or "")

    generator_ok = generator == case.expected_generator
    terms_ok = all(_surface(term) in response_surface for term in case.expected_terms)
    notes_ok = all(_surface(note) in notes_surface for note in case.expected_notes)
    forbidden_ok = all(_surface(term) not in response_surface for term in case.forbidden_terms)
    passed = generator_ok and terms_ok and notes_ok and forbidden_ok
    if passed:
        reason = "passed"
    elif not generator_ok:
        reason = f"generator:{generator or 'missing'}"
    elif not terms_ok:
        reason = "semantic_mismatch"
    elif not notes_ok:
        reason = "missing_guard_note"
    else:
        reason = "forbidden_term"

    return {
        "id": case.id,
        "prompt": case.prompt,
        "expected_generator": case.expected_generator,
        "actual_generator": generator,
        "expected_terms": list(case.expected_terms),
        "expected_notes": list(case.expected_notes),
        "response": response,
        "intent": body.get("intent"),
        "domain": body.get("domain"),
        "confidence": body.get("confidence"),
        "dispatch": body.get("dispatch"),
        "module_notes": notes,
        "generator_ok": generator_ok,
        "terms_ok": terms_ok,
        "notes_ok": notes_ok,
        "forbidden_ok": forbidden_ok,
        "passed": passed,
        "reason": reason,
    }


def _write_samples(path: Path, rows: list[dict[str, Any]]) -> None:
    lines = ["# Phase 27.41 Guarded Runtime Switch Samples", ""]
    for row in rows:
        lines.extend(
            [
                f"## {row['id']} — {'PASS' if row['passed'] else 'FAIL'}",
                "",
                f"- prompt: {row['prompt']}",
                f"- generator: {row['actual_generator']}",
                f"- response: {row['response']}",
                f"- reason: {row['reason']}",
                "",
            ]
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    args = parse_args()
    rows = [_run_case(args.base_url, case) for case in CASES]
    passed = sum(1 for row in rows if row["passed"])
    total = len(rows)
    status = (
        "PASSED_GUARDED_RUNTIME_SWITCH_PHASE27_40"
        if passed == total
        else "FAILED_GUARDED_RUNTIME_SWITCH_PHASE27_40"
    )
    report = {
        "phase": "Phase 27.41",
        "status": status,
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "training_started": False,
        "runtime_default": "template",
        "request_flag": "generator_trial=true",
        "candidate_generator": "sf_10m_phase27_40",
        "candidate_checkpoint": "artifacts/eval/phase27_40_tokenizer_context_repair/checkpoints/sf-10m-step6400",
        "candidate_tokenizer": "artifacts/tokenizers/sf_bpe/v5_topic_terms",
        "sf50m_allowed": False,
        "user_test_allowed": passed == total,
        "summary": {"passed": passed, "total": total},
        "rows": rows,
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _write_samples(args.samples, rows)
    print(json.dumps({"phase": report["phase"], "status": status, "passed": passed, "total": total}, ensure_ascii=False))
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
