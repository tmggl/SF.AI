#!/usr/bin/env python3
"""Phase 27.50 generator-only UI/API gate.

No training here. This verifies that /chat/message no longer exposes template
answers in the single-user lab surface. Supported prompts must be answered by
`sf_10m_phase27_47`; unsupported/template-first prompts must return an empty
response with `generator_blocked`, not a fallback template.
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
DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_50_generator_only_ui_gate_report.json"
DEFAULT_SAMPLES = ROOT / "artifacts/samples/phase27_50_generator_only_ui_gate.md"


@dataclass(frozen=True)
class Case:
    id: str
    prompt: str
    expected_generator: str
    required_terms: tuple[str, ...] = ()
    expect_empty: bool = False


CASES: tuple[Case, ...] = (
    Case("smalltalk_news", "وش الاخبار", "sf_10m_phase27_47", ("بخير",)),
    Case("smalltalk_oloomk", "علومك", "sf_10m_phase27_47", ("بخير",)),
    Case("planning_time", "نظم وقتي", "sf_10m_phase27_47", ("مهام",)),
    Case("advice_saudi", "وش تنصحني اسوي", "sf_10m_phase27_47", ("ابدأ",)),
    Case("definition_wafa", "الوفاء وش يعني", "sf_10m_phase27_47", ("الوفاء",)),
    Case("unsupported_karam_no_template", "ما معنى الكرم", "generator_blocked", expect_empty=True),
    Case("identity_no_template", "من أنت", "generator_blocked", expect_empty=True),
)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run Phase 27.50 generator-only UI/API gate")
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


def _run_case(base_url: str, case: Case) -> dict[str, Any]:
    body = _post_json(
        f"{base_url.rstrip('/')}/chat/message",
        {"message": case.prompt, "session_id": f"phase27-50-{case.id}"},
    )
    response = str(body.get("response") or "")
    generator = str(body.get("generator") or "")
    surface = _surface(response)
    generator_ok = generator == case.expected_generator
    no_template = generator != "template" and _surface("قالب ثابت") not in surface
    terms_ok = all(_surface(term) in surface for term in case.required_terms)
    empty_ok = (response == "") if case.expect_empty else response != ""
    passed = generator_ok and no_template and terms_ok and empty_ok
    if passed:
        reason = "passed"
    elif not generator_ok:
        reason = f"generator:{generator or 'missing'}"
    elif not no_template:
        reason = "template_leak"
    elif not terms_ok:
        reason = "semantic_mismatch"
    else:
        reason = "empty_response_mismatch"
    return {
        "id": case.id,
        "prompt": case.prompt,
        "expected_generator": case.expected_generator,
        "actual_generator": generator,
        "required_terms": list(case.required_terms),
        "expect_empty": case.expect_empty,
        "response": response,
        "domain": body.get("domain"),
        "intent": body.get("intent"),
        "dispatch": body.get("dispatch"),
        "debug": body.get("debug"),
        "passed": passed,
        "reason": reason,
    }


def _write_samples(path: Path, rows: list[dict[str, Any]]) -> None:
    lines = ["# Phase 27.50 Generator-Only UI/API Gate", ""]
    for row in rows:
        lines.extend(
            [
                f"## {row['id']} — {'PASS' if row['passed'] else 'FAIL'}",
                "",
                f"- prompt: {row['prompt']}",
                f"- generator: {row['actual_generator']}",
                f"- response: {row['response'] or '(empty)'}",
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
    status = "PASSED_GENERATOR_ONLY_UI_GATE" if passed == total else "FAILED_GENERATOR_ONLY_UI_GATE"
    report = {
        "phase": "Phase 27.50",
        "status": status,
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "training_started": False,
        "runtime_default": "generator_only_lab",
        "candidate_generator": "sf_10m_phase27_47",
        "template_answers_allowed": False,
        "sf50m_allowed": False,
        "phase28_allowed": False,
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
