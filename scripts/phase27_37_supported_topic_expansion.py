#!/usr/bin/env python3
"""Phase 27.37 supported generator topic expansion.

No training happens here. This script probes the running local server and
verifies that adding the `الصبر` definition topic expands the guarded
generator trial without weakening the quality floor.
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
DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_37_supported_topic_expansion_report.json"
DEFAULT_SAMPLES = ROOT / "artifacts/samples/phase27_37_supported_topic_expansion.md"


@dataclass(frozen=True)
class Case:
    id: str
    message: str
    expected_generator: str
    expected_terms: tuple[str, ...]
    expected_note: str
    bucket: str


CASES: tuple[Case, ...] = (
    # Existing proven lanes must remain open.
    Case("gen_001", "كيفك اليوم", "sf_10m_phase27_33", ("بخير",), "", "generated"),
    Case("gen_002", "وش أخبارك", "sf_10m_phase27_33", ("بخير",), "", "generated"),
    Case("gen_003", "شكرًا لمساعدتك", "sf_10m_phase27_33", ("العفو",), "", "generated"),
    Case("gen_004", "يعطيك العافية", "sf_10m_phase27_33", ("العفو",), "", "generated"),
    Case("gen_005", "وجهني بخطوة بسيطة", "sf_10m_phase27_33", ("ابدأ",), "", "generated"),
    Case("gen_006", "رتب لي يومي بسرعة", "sf_10m_phase27_33", ("ثلاث",), "", "generated"),
    Case("gen_007", "توترت شوي وش اسوي", "sf_10m_phase27_33", ("اهدأ",), "", "generated"),
    Case("gen_008", "وش المقصود بالاحترام", "sf_10m_phase27_33", ("تقدّر",), "", "generated"),
    Case("gen_009", "ما معنى التعاون", "sf_10m_phase27_33", ("التعاون",), "", "generated"),
    Case("gen_010", "القراية تفيدني بشي", "sf_10m_phase27_33", ("فهمك",), "", "generated"),
    # New Phase 27.37 topic: الصبر.
    Case("new_001", "ما معنى الصبر", "sf_10m_phase27_33", ("الصبر", "الصعوبة"), "", "new_topic"),
    Case("new_002", "الصبر وش يعني", "sf_10m_phase27_33", ("الصبر", "تثبت"), "", "new_topic"),
    Case("new_003", "وش المقصود بالصبر", "sf_10m_phase27_33", ("الصبر", "الصعوبة"), "", "new_topic"),
    # Quality floor: same topic, unstable wording should be blocked.
    Case("floor_001", "عرف الصبر", "template", ("محدود",), "definition_topic_mismatch", "quality_floor"),
    Case("floor_002", "اشرح لي الصبر ببساطة", "template", ("محدود",), "definition_topic_mismatch", "quality_floor"),
    Case("floor_003", "وش معنى الصداقة", "template", ("محدود",), "trial_unsupported_definition_topic", "quality_floor"),
    Case("floor_004", "اشرح الصدق", "template", ("محدود",), "trial_unsupported_definition_topic", "quality_floor"),
    Case("floor_005", "موضوع مفتوح", "template", ("محدود",), "trial_unsupported_general", "quality_floor"),
    # Pinned controls.
    Case("control_001", "من أنت", "template", ("SF.AI",), "template_first_social_intent", "control"),
    Case("control_002", "وش تقدر تسوي", "template", ("الفصحى",), "template_first_social_intent", "control"),
    Case("control_003", "عندي ألم في الراس", "template", ("طبيب",), "", "control"),
)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run Phase 27.37 supported topic expansion")
    p.add_argument("--base-url", default=DEFAULT_BASE_URL)
    p.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    p.add_argument("--samples", type=Path, default=DEFAULT_SAMPLES)
    return p.parse_args()


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


def _get_json(url: str) -> tuple[int, dict[str, Any]]:
    try:
        with urlopen(url, timeout=20) as res:  # noqa: S310 - local-only dev server
            return int(res.status), json.loads(res.read().decode("utf-8"))
    except URLError as exc:
        raise RuntimeError(f"could not reach {url}: {exc}") from exc


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


def _has_note(notes: str, expected: str) -> bool:
    return not expected or expected in notes


def _run(base_url: str) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    base = base_url.rstrip("/")
    health_status, health = _get_json(f"{base}/health")
    rows: list[dict[str, Any]] = []
    for item in CASES:
        status, body = _post_json(
            f"{base}/chat/message",
            {
                "message": item.message,
                "session_id": f"phase27-37-{item.id}",
                "user_id": "sami-local",
                "generator_trial": True,
            },
        )
        generator = str(body.get("generator") or body.get("debug", {}).get("generator") or "template")
        response = str(body.get("response") or "")
        notes = str(body.get("debug", {}).get("module_notes") or "")
        semantic = _semantic_match(response, item.expected_terms)
        note_match = _has_note(notes, item.expected_note)
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
                "module_notes": notes,
                "passed": passed,
            }
        )

    buckets = sorted({row["bucket"] for row in rows})
    summary = {
        "health_status": health_status,
        "health_phase": health.get("phase", ""),
        "cases_passed": sum(1 for row in rows if row["passed"]),
        "cases_total": len(rows),
        "generated_passed": sum(1 for row in rows if row["bucket"] == "generated" and row["passed"]),
        "generated_total": sum(1 for row in rows if row["bucket"] == "generated"),
        "new_topic_passed": sum(1 for row in rows if row["bucket"] == "new_topic" and row["passed"]),
        "new_topic_total": sum(1 for row in rows if row["bucket"] == "new_topic"),
        "quality_floor_passed": sum(1 for row in rows if row["bucket"] == "quality_floor" and row["passed"]),
        "quality_floor_total": sum(1 for row in rows if row["bucket"] == "quality_floor"),
        "controls_passed": sum(1 for row in rows if row["bucket"] == "control" and row["passed"]),
        "controls_total": sum(1 for row in rows if row["bucket"] == "control"),
        "bucket_summary": {
            bucket: {
                "passed": sum(1 for row in rows if row["bucket"] == bucket and row["passed"]),
                "total": sum(1 for row in rows if row["bucket"] == bucket),
            }
            for bucket in buckets
        },
    }
    return summary, rows


def _write_samples(path: Path, rows: list[dict[str, Any]]) -> None:
    lines = ["# Phase 27.37 Supported Topic Expansion", ""]
    for row in rows:
        lines.extend(
            [
                f"## {row['id']} — {'PASS' if row['passed'] else 'FAIL'}",
                "",
                f"- bucket: {row['bucket']}",
                f"- message: {row['message']}",
                f"- generator: {row['generator']}",
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
    passed = summary["cases_passed"] == summary["cases_total"]
    status = (
        "PASSED_SUPPORTED_TOPIC_EXPANSION_QUALITY_GATED"
        if passed
        else "FAILED_SUPPORTED_TOPIC_EXPANSION_KEEP_REPAIRING"
    )
    report = {
        "phase": "Phase 27.37",
        "status": status,
        "base_url": args.base_url.rstrip("/"),
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "training_started": False,
        "trial_generator": "sf_10m_phase27_33",
        "expanded_topics": ["الصبر"],
        "blocked_candidate_topics": ["الصداقة", "الصدق", "التنظيم", "الهدوء"],
        "semantic_topic_guard": True,
        "summary": summary,
        "user_test_allowed": passed,
        "sf50m_allowed": False,
        "phase28_allowed": False,
        "next_phase": "Phase 27.38 — targeted topic curriculum/probe for blocked definitions",
        "rows": rows,
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _write_samples(args.samples, rows)

    print("SF.AI — Phase 27.37 supported topic expansion")
    print(f"  status        : {status}")
    print(f"  health_phase  : {summary['health_phase']}")
    print(f"  cases         : {summary['cases_passed']}/{summary['cases_total']}")
    print(f"  generated     : {summary['generated_passed']}/{summary['generated_total']}")
    print(f"  new_topic     : {summary['new_topic_passed']}/{summary['new_topic_total']}")
    print(f"  quality_floor : {summary['quality_floor_passed']}/{summary['quality_floor_total']}")
    print(f"  controls      : {summary['controls_passed']}/{summary['controls_total']}")
    print(f"  report        : {args.report}")
    print(f"  samples       : {args.samples}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
