#!/usr/bin/env python3
"""Phase 27.35 live UI trial observations.

This phase does not train and does not use a browser automation dependency.
It checks the *running* local server over HTTP:

1. `/ui/chat` exposes the guarded generator toggle.
2. `/chat/message` uses `sf_10m_phase27_33` when `generator_trial=true`.
3. The default path remains `template`.
4. Sensitive/pinned prompts remain on safe template/composer paths.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.error import URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


DEFAULT_BASE_URL = "http://127.0.0.1:8123"
DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_35_live_ui_trial_observations_report.json"
DEFAULT_SAMPLES = ROOT / "artifacts/samples/phase27_35_live_ui_trial_observations.md"


@dataclass(frozen=True)
class LiveCase:
    id: str
    message: str
    generator_trial: bool
    expected_generator: str
    expected_terms: tuple[str, ...]
    note: str


LIVE_CASES: tuple[LiveCase, ...] = (
    LiveCase("live_001", "كيفك اليوم", True, "sf_10m_phase27_33", ("بخير", "كيفك"), "smalltalk generator"),
    LiveCase("live_002", "شكرًا لمساعدتك", True, "sf_10m_phase27_33", ("العفو", "أساعدك"), "thanks generator"),
    LiveCase("live_003", "وجهني بخطوة بسيطة", True, "sf_10m_phase27_33", ("ابدأ", "خطوة"), "advice generator"),
    LiveCase("live_004", "رتب لي يومي بسرعة", True, "sf_10m_phase27_33", ("ثلاث",), "planning generator"),
    LiveCase("live_005", "توترت شوي وش اسوي", True, "sf_10m_phase27_33", ("يهونها", "اهدأ"), "support generator"),
    LiveCase("live_006", "وش المقصود بالاحترام", True, "sf_10m_phase27_33", ("تقدّر", "تصرفك"), "definition generator"),
    LiveCase("live_007", "القراية تفيدني بشي", True, "sf_10m_phase27_33", ("فهمك", "كلماتك"), "definition generator"),
    LiveCase("control_001", "كيفك اليوم", False, "template", ("بخير",), "default template path"),
    LiveCase("control_002", "من أنت", True, "template", ("SF.AI",), "identity remains pinned template"),
    LiveCase("control_003", "عندي ألم في الراس", True, "template", ("طبيب",), "medical remains safe composer"),
)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run Phase 27.35 live UI trial observations")
    p.add_argument("--base-url", default=DEFAULT_BASE_URL)
    p.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    p.add_argument("--samples", type=Path, default=DEFAULT_SAMPLES)
    return p.parse_args()


def _get_text(url: str) -> tuple[int, str]:
    try:
        with urlopen(url, timeout=20) as res:  # noqa: S310 - local-only dev server URL
            return int(res.status), res.read().decode("utf-8")
    except URLError as exc:
        raise RuntimeError(f"could not reach {url}: {exc}") from exc


def _post_json(url: str, payload: dict[str, Any]) -> tuple[int, dict[str, Any]]:
    req = Request(
        url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urlopen(req, timeout=40) as res:  # noqa: S310 - local-only dev server URL
            raw = res.read().decode("utf-8")
            return int(res.status), json.loads(raw)
    except URLError as exc:
        raise RuntimeError(f"could not post to {url}: {exc}") from exc


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


def _semantic_match(text: str, terms: tuple[str, ...]) -> bool:
    surface = _surface(text)
    return all(_surface(term) in surface for term in terms)


def _run(base_url: str) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    base = base_url.rstrip("/")
    health_status, health_body = _get_text(f"{base}/health")
    ui_status, ui_html = _get_text(f"{base}/ui/chat")
    ui_checks = {
        "status_200": ui_status == 200,
        "has_generator_toggle_label": "مولّد تجريبي" in ui_html,
        "sends_generator_trial_field": "generator_trial" in ui_html,
        "persists_generator_trial_toggle": "sf_generator_trial" in ui_html,
        "mentions_phase27_33_generator": "sf_10m_phase27_33" in ui_html,
    }

    rows: list[dict[str, Any]] = []
    for item in LIVE_CASES:
        status, body = _post_json(
            f"{base}/chat/message",
            {
                "message": item.message,
                "session_id": f"phase27-35-{item.id}",
                "user_id": "sami-local",
                "generator_trial": item.generator_trial,
            },
        )
        generator = str(body.get("generator") or body.get("debug", {}).get("generator") or "template")
        response = str(body.get("response") or "")
        semantic = _semantic_match(response, item.expected_terms)
        passed = status == 200 and generator == item.expected_generator and semantic
        rows.append(
            {
                "id": item.id,
                "message": item.message,
                "generator_trial": item.generator_trial,
                "http_status": status,
                "domain": body.get("domain", ""),
                "intent": body.get("intent", ""),
                "dispatch": body.get("dispatch", ""),
                "expected_generator": item.expected_generator,
                "generator": generator,
                "expected_terms": list(item.expected_terms),
                "semantic_match": semantic,
                "response": response,
                "module_notes": body.get("debug", {}).get("module_notes", ""),
                "note": item.note,
                "passed": passed,
            }
        )

    health = json.loads(health_body) if health_status == 200 else {}
    ui_passed = all(ui_checks.values())
    cases_passed = sum(1 for row in rows if row["passed"])
    total_cases = len(rows)
    summary = {
        "health_status": health_status,
        "health_phase": health.get("phase", ""),
        "ui_checks": ui_checks,
        "ui_passed": ui_passed,
        "cases_passed": cases_passed,
        "cases_total": total_cases,
        "generator_cases": sum(1 for row in rows if row["expected_generator"] != "template"),
        "generator_cases_passed": sum(
            1
            for row in rows
            if row["expected_generator"] != "template" and row["passed"]
        ),
        "template_controls": sum(1 for row in rows if row["expected_generator"] == "template"),
        "template_controls_passed": sum(
            1
            for row in rows
            if row["expected_generator"] == "template" and row["passed"]
        ),
    }
    return summary, rows


def _write_samples(path: Path, rows: list[dict[str, Any]]) -> None:
    lines = ["# Phase 27.35 Live UI Trial Observations", ""]
    for row in rows:
        lines.extend(
            [
                f"## {row['id']} — {'PASS' if row['passed'] else 'FAIL'}",
                "",
                f"- message: {row['message']}",
                f"- generator_trial: {str(row['generator_trial']).lower()}",
                f"- generator: {row['generator']}",
                f"- dispatch: {row['dispatch']}",
                f"- response: {row['response']}",
                f"- notes: {row['module_notes'] or '-'}",
                "",
            ]
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    args = parse_args()
    summary, rows = _run(args.base_url)
    passed = bool(summary["ui_passed"] and summary["cases_passed"] == summary["cases_total"])
    status = (
        "PASSED_LIVE_UI_TRIAL_READY_FOR_USER_OBSERVATION"
        if passed
        else "FAILED_LIVE_UI_TRIAL_KEEP_REPAIRING"
    )
    report = {
        "phase": "Phase 27.35",
        "status": status,
        "base_url": args.base_url.rstrip("/"),
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "default_runtime": "template",
        "trial_generator": "sf_10m_phase27_33",
        "summary": summary,
        "ui_user_test_allowed": passed,
        "sf50m_allowed": False,
        "next_phase": (
            "Phase 27.36 — collect/triage live UI observations"
            if passed
            else "Phase 27.36 — repair live UI trial gaps"
        ),
        "failures": [row for row in rows if not row["passed"]],
        "results": rows,
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _write_samples(args.samples, rows)

    print("SF.AI — Phase 27.35 live UI trial observations")
    print(f"  status       : {status}")
    print(f"  health_phase : {summary['health_phase']}")
    print(f"  ui_passed    : {str(summary['ui_passed']).lower()}")
    print(f"  cases        : {summary['cases_passed']}/{summary['cases_total']}")
    print(f"  generator    : {summary['generator_cases_passed']}/{summary['generator_cases']}")
    print(f"  controls     : {summary['template_controls_passed']}/{summary['template_controls']}")
    print(f"  user_test    : {str(passed).lower()}")
    print(f"  report       : {args.report}")
    print(f"  samples      : {args.samples}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
