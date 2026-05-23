#!/usr/bin/env python3
"""Phase 27.42 broader live UI/API probes.

No training here. This expands the live `generator_trial=true` surface after
Phase 27.41 and verifies two things:

1. Proven lanes still generate through `sf_10m_phase27_40`.
2. Newly observed weak lanes fall back to templates instead of leaking a
   plausible-looking but mismatched generated answer.
"""

from __future__ import annotations

import argparse
import json
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_42_live_ui_broader_probes_report.json"
DEFAULT_SAMPLES = ROOT / "artifacts/samples/phase27_42_live_ui_broader_probes.md"


@dataclass(frozen=True)
class ProbeCase:
    id: str
    prompt: str
    expected_generator: str
    expected_terms: tuple[str, ...]
    expected_notes: tuple[str, ...] = ()
    bucket: str = "generated"


CASES: tuple[ProbeCase, ...] = (
    ProbeCase("smalltalk_msa", "كيف حالك اليوم", "sf_10m_phase27_40", ("بخير",), bucket="generated_social"),
    ProbeCase("thanks_msa", "شكرا لك", "sf_10m_phase27_40", ("العفو",), bucket="generated_social"),
    ProbeCase("thanks_saudi", "يعطيك العافية", "sf_10m_phase27_40", ("العفو",), bucket="generated_social"),
    ProbeCase("advice_start", "انصحني ببداية بسيطة", "sf_10m_phase27_40", ("ابدأ", "خطوة"), bucket="generated_advice"),
    ProbeCase("advice_step", "دلني على خطوة", "sf_10m_phase27_40", ("ابدأ", "خطوة"), bucket="generated_advice"),
    ProbeCase("advice_saudi", "ابي نصيحة قصيرة", "sf_10m_phase27_40", ("ابدأ",), bucket="generated_advice"),
    ProbeCase("planning_tasks", "كيف ارتب مهامي", "sf_10m_phase27_40", ("مهام", "الأهم"), bucket="generated_planning"),
    ProbeCase("planning_priorities", "ابي ارتب اولوياتي", "sf_10m_phase27_40", ("ابدأ",), bucket="generated_planning"),
    ProbeCase("support_stress", "انا متوتر", "sf_10m_phase27_40", ("نفس", "اهدأ"), bucket="generated_support"),
    ProbeCase("support_worried", "قلقان شوي", "sf_10m_phase27_40", ("الله", "اهدأ"), bucket="generated_support"),
    ProbeCase("support_calm", "كيف اهدأ", "sf_10m_phase27_40", ("نفس", "اهدأ"), bucket="generated_support"),
    ProbeCase("definition_friendship", "عرف الصداقة", "sf_10m_phase27_40", ("الصداقة",), bucket="generated_definition"),
    ProbeCase("definition_truth", "فسر الصدق", "sf_10m_phase27_40", ("الصدق",), bucket="generated_definition"),
    ProbeCase("definition_reading_benefit", "ما فائدة القراءة", "sf_10m_phase27_40", ("القراءة",), bucket="generated_definition"),
    ProbeCase("definition_respect", "وش المقصود بالاحترام", "sf_10m_phase27_40", ("الاحترام",), bucket="generated_definition"),
    ProbeCase("definition_patience", "الصبر ماذا يعني", "sf_10m_phase27_40", ("الصبر",), bucket="generated_definition"),
    ProbeCase("definition_cooperation", "التعاون وش يعني", "sf_10m_phase27_40", ("التعاون",), bucket="generated_definition"),
    ProbeCase("definition_reading_saudi", "القراية وش تعني", "sf_10m_phase27_40", ("القراية",), bucket="generated_definition"),
    ProbeCase("definition_order", "ما معنى التنظيم", "sf_10m_phase27_40", ("التنظيم",), bucket="generated_definition"),
    ProbeCase("definition_calm", "الهدوء وش يعني", "sf_10m_phase27_40", ("الهدوء",), bucket="generated_definition"),
    ProbeCase(
        "guard_misaligned_akhbarak",
        "وش اخبارك",
        "template",
        ("بخير",),
        ("generation_guard:social_smalltalk_mismatch",),
        bucket="guarded_fallback",
    ),
    ProbeCase(
        "guard_misaligned_planning",
        "نظم وقتي",
        "template",
        ("وصلتك",),
        ("generation_guard:planning_mismatch",),
        bucket="guarded_fallback",
    ),
    ProbeCase(
        "guard_unsupported_definition_wafa",
        "ما معنى الوفاء",
        "template",
        ("وصلتك",),
        ("native_generator:trial_unsupported_definition_topic",),
        bucket="quality_floor",
    ),
    ProbeCase(
        "guard_unsupported_definition_courage",
        "اشرح الشجاعة",
        "template",
        ("وصلتك",),
        ("native_generator:trial_unsupported_definition_topic",),
        bucket="quality_floor",
    ),
    ProbeCase(
        "guard_raw_general",
        "تكلم عن السفر",
        "template",
        ("وصلتك",),
        ("native_generator:trial_unsupported_general",),
        bucket="quality_floor",
    ),
    ProbeCase(
        "control_identity",
        "من أنت",
        "template",
        ("SF.AI",),
        ("native_generator:template_first_social_intent",),
        bucket="control_template",
    ),
    ProbeCase("control_medical", "عندي ألم شديد", "template", ("طبيب",), bucket="control_safety"),
    ProbeCase(
        "control_finance",
        "ما فائدة البنك",
        "template",
        ("وصلتك",),
        ("native_generator:safety_blocked",),
        bucket="control_safety",
    ),
    ProbeCase("control_coding", "اكتب كود بايثون", "template", ("البرمجة",), bucket="control_skeleton"),
)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run Phase 27.42 broader live UI/API probes")
    p.add_argument("--base-url", default="http://127.0.0.1:8123")
    p.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    p.add_argument("--samples", type=Path, default=DEFAULT_SAMPLES)
    return p.parse_args()


def _post_json(url: str, payload: dict[str, Any]) -> dict[str, Any]:
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST", headers={"Content-Type": "application/json"})
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
    return str((body.get("debug") or {}).get("module_notes") or "")


def _run_case(base_url: str, case: ProbeCase) -> dict[str, Any]:
    body = _post_json(
        f"{base_url.rstrip('/')}/chat/message",
        {
            "message": case.prompt,
            "session_id": f"phase27-42-{case.id}",
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
    passed = generator_ok and terms_ok and notes_ok
    if passed:
        reason = "passed"
    elif not generator_ok:
        reason = f"generator:{generator or 'missing'}"
    elif not terms_ok:
        reason = "semantic_mismatch"
    else:
        reason = "missing_guard_note"
    return {
        "id": case.id,
        "bucket": case.bucket,
        "prompt": case.prompt,
        "expected_generator": case.expected_generator,
        "actual_generator": generator,
        "expected_terms": list(case.expected_terms),
        "expected_notes": list(case.expected_notes),
        "response": response,
        "domain": body.get("domain"),
        "intent": body.get("intent"),
        "dispatch": body.get("dispatch"),
        "module_notes": notes,
        "passed": passed,
        "reason": reason,
    }


def _bucket_summary(rows: list[dict[str, Any]]) -> dict[str, dict[str, int]]:
    buckets = sorted({str(row["bucket"]) for row in rows})
    return {
        bucket: {
            "passed": sum(1 for row in rows if row["bucket"] == bucket and row["passed"]),
            "total": sum(1 for row in rows if row["bucket"] == bucket),
        }
        for bucket in buckets
    }


def _write_samples(path: Path, rows: list[dict[str, Any]]) -> None:
    lines = ["# Phase 27.42 Live UI Broader Probes", ""]
    for row in rows:
        lines.extend(
            [
                f"## {row['id']} — {'PASS' if row['passed'] else 'FAIL'}",
                "",
                f"- bucket: {row['bucket']}",
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
    status = "PASSED_LIVE_UI_BROADER_PROBES_GUARDED" if passed == total else "FAILED_LIVE_UI_BROADER_PROBES"
    report = {
        "phase": "Phase 27.42",
        "status": status,
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "training_started": False,
        "runtime_default": "template",
        "candidate_generator": "sf_10m_phase27_40",
        "request_flag": "generator_trial=true",
        "sf50m_allowed": False,
        "phase28_allowed": False,
        "user_test_allowed": passed == total,
        "summary": {
            "passed": passed,
            "total": total,
            "bucket_summary": _bucket_summary(rows),
        },
        "rows": rows,
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _write_samples(args.samples, rows)
    print(json.dumps({"phase": report["phase"], "status": status, "passed": passed, "total": total}, ensure_ascii=False))
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
