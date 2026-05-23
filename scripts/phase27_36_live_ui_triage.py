#!/usr/bin/env python3
"""Phase 27.36 live UI triage.

This phase keeps training closed. It probes the running local server through
`/chat/message` with `generator_trial=true`, then classifies the current
single-user generator trial into:

1. proven lanes that may use `sf_10m_phase27_33`;
2. quality-floor blocks that must remain template until more data/training;
3. pinned template/safety controls.
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
DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_36_live_ui_triage_report.json"
DEFAULT_SAMPLES = ROOT / "artifacts/samples/phase27_36_live_ui_triage.md"


@dataclass(frozen=True)
class TriageCase:
    id: str
    message: str
    expected_generator: str
    expected_terms: tuple[str, ...]
    expected_note: str
    bucket: str
    note: str


TRIAGE_CASES: tuple[TriageCase, ...] = (
    # Proven generated lanes.
    TriageCase("gen_001", "كيفك اليوم", "sf_10m_phase27_33", ("بخير",), "", "generated", "smalltalk"),
    TriageCase("gen_002", "كيف حالك", "sf_10m_phase27_33", ("بخير",), "", "generated", "smalltalk msa"),
    TriageCase("gen_003", "وش أخبارك", "sf_10m_phase27_33", ("بخير",), "", "generated", "smalltalk saudi"),
    TriageCase("gen_004", "شكرًا لمساعدتك", "sf_10m_phase27_33", ("العفو",), "", "generated", "thanks"),
    TriageCase("gen_005", "يعطيك العافية", "sf_10m_phase27_33", ("العفو",), "", "generated", "thanks saudi"),
    TriageCase("gen_006", "مشكور", "sf_10m_phase27_33", ("العفو",), "", "generated", "thanks short"),
    TriageCase("gen_007", "وجهني بخطوة بسيطة", "sf_10m_phase27_33", ("ابدأ",), "", "generated", "advice"),
    TriageCase("gen_008", "أحتاج نصيحة بسيطة", "sf_10m_phase27_33", ("ابدأ",), "", "generated", "advice msa"),
    TriageCase("gen_009", "دلني على بداية سهلة", "sf_10m_phase27_33", ("ابدأ",), "", "generated", "advice saudi"),
    TriageCase("gen_010", "رتب لي يومي بسرعة", "sf_10m_phase27_33", ("ثلاث",), "", "generated", "planning"),
    TriageCase("gen_011", "كيف أنظم مهامي", "sf_10m_phase27_33", ("مهام",), "", "generated", "planning msa"),
    TriageCase("gen_012", "رتب أولوياتي", "sf_10m_phase27_33", ("الأهم",), "", "generated", "planning priorities"),
    TriageCase("gen_013", "توترت شوي وش اسوي", "sf_10m_phase27_33", ("اهدأ",), "", "generated", "support"),
    TriageCase("gen_014", "أنا قلقان شوي", "sf_10m_phase27_33", ("اهدأ",), "", "generated", "support msa"),
    TriageCase("gen_015", "وش المقصود بالاحترام", "sf_10m_phase27_33", ("تقدّر",), "", "generated", "definition respect"),
    TriageCase("gen_016", "ما معنى التعاون", "sf_10m_phase27_33", ("التعاون",), "", "generated", "definition cooperation"),
    TriageCase("gen_017", "القراية تفيدني بشي", "sf_10m_phase27_33", ("فهمك",), "", "generated", "definition reading"),
    TriageCase("gen_018", "وش المقصود بالقراءة", "sf_10m_phase27_33", ("فهمك",), "", "generated", "definition reading msa"),
    # Quality-floor blocks discovered during live observation.
    TriageCase("floor_001", "الحمدلله", "template", ("تمام",), "template_first_social_intent", "quality_floor", "ack now stays template"),
    TriageCase("floor_002", "اشرح لي الصبر ببساطة", "template", ("وصلتك",), "trial_unsupported_definition_topic", "quality_floor", "unsupported topic"),
    TriageCase("floor_003", "عرف الصبر", "template", ("وصلتك",), "trial_unsupported_definition_topic", "quality_floor", "unsupported wording"),
    TriageCase("floor_004", "وش معنى الصداقة", "template", ("وصلتك",), "trial_unsupported_definition_topic", "quality_floor", "unsupported topic"),
    TriageCase("floor_005", "اشرح الصدق", "template", ("وصلتك",), "trial_unsupported_definition_topic", "quality_floor", "unsupported topic"),
    # Pinned controls.
    TriageCase("control_001", "من أنت", "template", ("SF.AI",), "template_first_social_intent", "control", "identity pinned"),
    TriageCase("control_002", "وش تقدر تسوي", "template", ("الفصحى",), "template_first_social_intent", "control", "capability pinned"),
    TriageCase("control_003", "ما الفرق بين تدريب النموذج وتفعيل النموذج", "template", ("التدريب",), "template_first_social_intent", "control", "project explanation pinned"),
    TriageCase("control_004", "عندي ألم في الراس", "template", ("طبيب",), "", "control", "medical composer"),
)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run Phase 27.36 live UI triage")
    p.add_argument("--base-url", default=DEFAULT_BASE_URL)
    p.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    p.add_argument("--samples", type=Path, default=DEFAULT_SAMPLES)
    return p.parse_args()


def _get_text(url: str) -> tuple[int, str]:
    try:
        with urlopen(url, timeout=20) as res:  # noqa: S310 - local-only dev server
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
        with urlopen(req, timeout=40) as res:  # noqa: S310 - local-only dev server
            return int(res.status), json.loads(res.read().decode("utf-8"))
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


def _has_note(module_notes: str, expected_note: str) -> bool:
    return not expected_note or expected_note in module_notes


def _run(base_url: str) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    base = base_url.rstrip("/")
    health_status, health_body = _get_text(f"{base}/health")
    ui_status, ui_html = _get_text(f"{base}/ui/chat")
    ui_checks = {
        "status_200": ui_status == 200,
        "has_generator_toggle_label": "مولّد تجريبي" in ui_html,
        "sends_generator_trial_field": "generator_trial" in ui_html,
        "persists_generator_trial_toggle": "sf_generator_trial" in ui_html,
    }

    rows: list[dict[str, Any]] = []
    for item in TRIAGE_CASES:
        status, body = _post_json(
            f"{base}/chat/message",
            {
                "message": item.message,
                "session_id": f"phase27-36-{item.id}",
                "user_id": "sami-local",
                "generator_trial": True,
            },
        )
        generator = str(body.get("generator") or body.get("debug", {}).get("generator") or "template")
        response = str(body.get("response") or "")
        module_notes = str(body.get("debug", {}).get("module_notes") or "")
        semantic = _semantic_match(response, item.expected_terms)
        note_match = _has_note(module_notes, item.expected_note)
        passed = (
            status == 200
            and generator == item.expected_generator
            and semantic
            and note_match
        )
        rows.append(
            {
                "id": item.id,
                "bucket": item.bucket,
                "message": item.message,
                "http_status": status,
                "domain": body.get("domain", ""),
                "intent": body.get("intent", ""),
                "dispatch": body.get("dispatch", ""),
                "expected_generator": item.expected_generator,
                "generator": generator,
                "expected_terms": list(item.expected_terms),
                "semantic_match": semantic,
                "expected_note": item.expected_note,
                "note_match": note_match,
                "response": response,
                "module_notes": module_notes,
                "note": item.note,
                "passed": passed,
            }
        )

    health = json.loads(health_body) if health_status == 200 else {}
    ui_passed = all(ui_checks.values())
    buckets = sorted({row["bucket"] for row in rows})
    bucket_summary = {
        bucket: {
            "passed": sum(1 for row in rows if row["bucket"] == bucket and row["passed"]),
            "total": sum(1 for row in rows if row["bucket"] == bucket),
        }
        for bucket in buckets
    }
    summary = {
        "health_status": health_status,
        "health_phase": health.get("phase", ""),
        "ui_checks": ui_checks,
        "ui_passed": ui_passed,
        "cases_passed": sum(1 for row in rows if row["passed"]),
        "cases_total": len(rows),
        "generated_passed": sum(1 for row in rows if row["bucket"] == "generated" and row["passed"]),
        "generated_total": sum(1 for row in rows if row["bucket"] == "generated"),
        "quality_floor_passed": sum(1 for row in rows if row["bucket"] == "quality_floor" and row["passed"]),
        "quality_floor_total": sum(1 for row in rows if row["bucket"] == "quality_floor"),
        "controls_passed": sum(1 for row in rows if row["bucket"] == "control" and row["passed"]),
        "controls_total": sum(1 for row in rows if row["bucket"] == "control"),
        "bucket_summary": bucket_summary,
    }
    return summary, rows


def _write_samples(path: Path, rows: list[dict[str, Any]]) -> None:
    lines = ["# Phase 27.36 Live UI Triage", ""]
    for row in rows:
        lines.extend(
            [
                f"## {row['id']} — {'PASS' if row['passed'] else 'FAIL'}",
                "",
                f"- bucket: {row['bucket']}",
                f"- message: {row['message']}",
                f"- generator: {row['generator']}",
                f"- intent: {row['intent']}",
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
        "PASSED_LIVE_UI_TRIAGE_QUALITY_FLOOR_ACTIVE"
        if passed
        else "FAILED_LIVE_UI_TRIAGE_KEEP_REPAIRING"
    )
    report = {
        "phase": "Phase 27.36",
        "status": status,
        "base_url": args.base_url.rstrip("/"),
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "training_started": False,
        "default_runtime": "template",
        "trial_generator": "sf_10m_phase27_33",
        "summary": summary,
        "user_test_allowed": passed,
        "sf50m_allowed": False,
        "phase28_allowed": False,
        "next_phase": "Phase 27.37 — expand supported generator intents/topics before SF-50M",
        "triage_decision": {
            "keep_generator_trial": passed,
            "keep_default_template": True,
            "quality_floor": "block raw chat.general and unsupported definition topics",
            "proven_lanes": [
                "smalltalk",
                "thanks",
                "advice",
                "planning",
                "support",
                "definition:الاحترام",
                "definition:التعاون",
                "definition:القراءة",
            ],
            "blocked_lanes": [
                "raw chat.general",
                "definition topics not yet stabilized",
                "identity/capability/project explanations",
                "safety domains",
            ],
        },
        "rows": rows,
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _write_samples(args.samples, rows)

    print("SF.AI — Phase 27.36 live UI triage")
    print(f"  status        : {status}")
    print(f"  health_phase  : {summary['health_phase']}")
    print(f"  cases         : {summary['cases_passed']}/{summary['cases_total']}")
    print(f"  generated     : {summary['generated_passed']}/{summary['generated_total']}")
    print(f"  quality_floor : {summary['quality_floor_passed']}/{summary['quality_floor_total']}")
    print(f"  controls      : {summary['controls_passed']}/{summary['controls_total']}")
    print(f"  report        : {args.report}")
    print(f"  samples       : {args.samples}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
