#!/usr/bin/env python3
"""Phase 27.48 guarded runtime switch for sf_10m_phase27_47.

No training here. This verifies the explicit `generator_trial=true` API/UI path
uses the Phase 27.47 candidate for the proven core dialogue nucleus while
keeping sensitive/unsupported paths on templates.
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
DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_48_guarded_runtime_switch_report.json"
DEFAULT_SAMPLES = ROOT / "artifacts/samples/phase27_48_guarded_runtime_switch.md"


@dataclass(frozen=True)
class LiveCase:
    id: str
    prompt: str
    expected_generator: str
    expected_terms: tuple[str, ...]
    expected_notes: tuple[str, ...] = ()
    bucket: str = "generated"


CASES: tuple[LiveCase, ...] = (
    LiveCase("weak_smalltalk_akhbarak", "وش اخبارك", "sf_10m_phase27_47", ("بخير",), bucket="generated_weak"),
    LiveCase("weak_smalltalk_oloomk", "علومك", "sf_10m_phase27_47", ("بخير",), bucket="generated_weak"),
    LiveCase("weak_thanks_mashkoor", "مشكور", "sf_10m_phase27_47", ("حاضر",), bucket="generated_weak"),
    LiveCase("weak_thanks_tislam", "تسلم", "sf_10m_phase27_47", ("حاضر",), bucket="generated_weak"),
    LiveCase("weak_planning_time", "نظم وقتي", "sf_10m_phase27_47", ("مهام",), bucket="generated_weak"),
    LiveCase("weak_planning_priorities", "ابي ارتب اولوياتي", "sf_10m_phase27_47", ("ابدأ",), bucket="generated_weak"),
    LiveCase("definition_wafa", "ما معنى الوفاء", "sf_10m_phase27_47", ("الوفاء",), bucket="generated_new_topic"),
    LiveCase("definition_courage", "اشرح الشجاعة", "sf_10m_phase27_47", ("الشجاعة",), bucket="generated_new_topic"),
    LiveCase("smalltalk_regression", "كيفك اليوم", "sf_10m_phase27_47", ("بخير",), bucket="generated_regression"),
    LiveCase("advice_regression", "انصحني ببداية بسيطة", "sf_10m_phase27_47", ("ابدأ",), bucket="generated_regression"),
    LiveCase("planning_regression", "كيف ارتب مهامي", "sf_10m_phase27_47", ("مهام",), bucket="generated_regression"),
    LiveCase("support_regression", "انا متوتر", "sf_10m_phase27_47", ("نفس", "اهدأ"), bucket="generated_regression"),
    LiveCase("friendship_regression", "ما معنى الصداقة", "sf_10m_phase27_47", ("الصداقة",), bucket="generated_regression"),
    LiveCase("truth_regression", "الصدق وش يعني", "sf_10m_phase27_47", ("الصدق",), bucket="generated_regression"),
    LiveCase("order_regression", "ما معنى التنظيم", "sf_10m_phase27_47", ("التنظيم",), bucket="generated_regression"),
    LiveCase("calm_regression", "الهدوء وش يعني", "sf_10m_phase27_47", ("الهدوء",), bucket="generated_regression"),
    LiveCase(
        "control_identity_template",
        "من أنت",
        "template",
        ("SF.AI",),
        ("native_generator:template_first_social_intent",),
        bucket="control_template",
    ),
    LiveCase("control_sensitive_medical", "عندي ألم في الراس", "template", ("طبيب",), bucket="control_safety"),
    LiveCase(
        "control_raw_general",
        "موضوع مفتوح بلا تفاصيل",
        "template",
        ("عام",),
        ("native_generator:trial_unsupported_general",),
        bucket="control_quality_floor",
    ),
)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run Phase 27.48 guarded runtime switch gate")
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


def _run_case(base_url: str, case: LiveCase) -> dict[str, Any]:
    body = _post_json(
        f"{base_url.rstrip('/')}/chat/message",
        {
            "message": case.prompt,
            "session_id": f"phase27-48-{case.id}",
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
    lines = ["# Phase 27.48 Guarded Runtime Switch Samples", ""]
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
    status = "PASSED_GUARDED_RUNTIME_SWITCH_PHASE27_47" if passed == total else "FAILED_GUARDED_RUNTIME_SWITCH_PHASE27_47"
    report = {
        "phase": "Phase 27.48",
        "status": status,
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "training_started": False,
        "runtime_default": "template",
        "request_flag": "generator_trial=true",
        "candidate_generator": "sf_10m_phase27_47",
        "candidate_checkpoint": "artifacts/eval/phase27_47_new_topic_conditioning_repair/checkpoints/sf-10m-step4600",
        "candidate_tokenizer": "artifacts/tokenizers/sf_bpe/v6_weak_lane_terms",
        "sf50m_allowed": False,
        "phase28_allowed": False,
        "user_test_allowed": passed == total,
        "summary": {"passed": passed, "total": total, "bucket_summary": _bucket_summary(rows)},
        "rows": rows,
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _write_samples(args.samples, rows)
    print(json.dumps({"phase": report["phase"], "status": status, "passed": passed, "total": total}, ensure_ascii=False))
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
