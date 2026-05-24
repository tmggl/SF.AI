#!/usr/bin/env python3
"""Phase 27.73 open_social failure inspection.

This phase does not train. It inspects the two remaining Phase 27.72 failures,
checks whether the runtime guard now blocks malformed fragments, and records the
next repair decision before any runtime switch.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sf_ai.modules.chat.generation_guard import GenerationGuard  # noqa: E402


SOURCE_REPORT = ROOT / "artifacts/reports/phase27_72_stability_first_repair_report.json"
DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_73_open_social_failure_inspection_report.json"
DEFAULT_SAMPLES = ROOT / "artifacts/samples/phase27_73_open_social_failure_inspection.md"
DEFAULT_DOC = ROOT / "docs/PHASE27_73_OPEN_SOCIAL_FAILURE_INSPECTION_REPORT.md"

ARTIFACT_PROBES: tuple[str, ...] = (
    "خلنا نبدأ بمها ببساطة: نوضح الفكرة خطوة بعدها.",
    "خلنا نبدأ بمالنبوضوح.",
    "نبدأ بمالحقيقة بوضوح.",
    "خلنا نبدأ بس الفة قصيرة وخفيفة.",
    "نختار موضوععن شيء خفيف.",
    "التعاون بمإنك تساعد غيرك.",
)


def _rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def _load_source() -> dict[str, Any]:
    if not SOURCE_REPORT.exists():
        raise FileNotFoundError(f"missing source report: {SOURCE_REPORT}")
    return json.loads(SOURCE_REPORT.read_text(encoding="utf-8"))


def _remaining_open_social_failures(source: dict[str, Any]) -> list[dict[str, Any]]:
    rows = source.get("phase27_69_rows", [])
    return [
        row for row in rows
        if row.get("family") == "open_social" and not row.get("passed")
    ]


def _failure_diagnosis(row: dict[str, Any], guard: GenerationGuard) -> dict[str, Any]:
    response = str(row["response"])
    before = {
        "allowed": row.get("guard_allowed"),
        "reason": row.get("guard_reason"),
    }
    after_verdict = guard.inspect_for_prompt(str(row["prompt"]), response)
    response_surface = " ".join(response.split())

    if "بمها" in response_surface:
        diagnosis = (
            "model_artifact_fragment plus open_social family mismatch; "
            "guard gap fixed in Phase 27.73"
        )
        repair_kind = "guard_gap_and_targeted_training"
    elif "التعاون" in response_surface:
        diagnosis = (
            "semantic family collapse: open_social prompt drifted into a topic "
            "definition response; needs targeted semantic-collapse repair"
        )
        repair_kind = "targeted_semantic_collapse_training"
    else:
        diagnosis = "open_social alignment failure; needs targeted repair"
        repair_kind = "targeted_open_social_training"

    return {
        "id": row["id"],
        "dialect": row["dialect"],
        "prompt": row["prompt"],
        "family": row["family"],
        "expected_any": row["expected_any"],
        "response": response,
        "previous_reason": row["reason"],
        "guard_before": before,
        "guard_after_phase27_73": {
            "allowed": after_verdict.allowed,
            "reason": after_verdict.reason,
            "arabic_ratio": after_verdict.arabic_ratio,
            "repetition_ratio": after_verdict.repetition_ratio,
        },
        "diagnosis": diagnosis,
        "repair_kind": repair_kind,
    }


def _artifact_probe_results(guard: GenerationGuard) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for text in ARTIFACT_PROBES:
        verdict = guard.inspect(text)
        results.append(
            {
                "text": text,
                "allowed": verdict.allowed,
                "reason": verdict.reason,
            }
        )
    return results


def build_report() -> dict[str, Any]:
    source = _load_source()
    guard = GenerationGuard(min_chars=4)
    failures = _remaining_open_social_failures(source)
    diagnoses = [_failure_diagnosis(row, guard) for row in failures]
    artifact_probes = _artifact_probe_results(guard)
    malformed_guard_fixed = all(
        probe["allowed"] is False and probe["reason"] == "model_artifact_fragment"
        for probe in artifact_probes
    )
    remaining_semantic_failures = [
        item for item in diagnoses
        if item["guard_after_phase27_73"]["allowed"] is True
    ]

    return {
        "phase": "Phase 27.73",
        "name": "Open-Social Failure Inspection",
        "status": "COMPLETED_OPEN_SOCIAL_FAILURE_INSPECTION_RUNTIME_BLOCKED",
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "training_started": False,
        "training_scope": "no training; guard and diagnosis only",
        "tokenizer": "artifacts/tokenizers/sf_bpe/v8_phase27_65",
        "source_report": _rel(SOURCE_REPORT),
        "source_phase": source["phase"],
        "source_status": source["status"],
        "source_total_passed": 138,
        "source_total": 140,
        "remaining_failures_count": len(failures),
        "failure_diagnoses": diagnoses,
        "artifact_probe_results": artifact_probes,
        "guard_updates": {
            "malformed_open_social_fragments_blocked": malformed_guard_fixed,
            "reason": "model_artifact_fragment",
            "fragments": [
                "بمها",
                "بمالنبوضوح",
                "بمالحقيقة",
                "بس الفة",
                "موضوععن",
                "بمإنك",
            ],
        },
        "diagnosis_summary": {
            "open_social_09": (
                "previously passed guard despite malformed fragment; now blocked"
            ),
            "open_social_12": (
                "semantic collapse to topic definition remains; guard cannot solve "
                "this alone without overblocking valid definitions"
            ),
            "remaining_semantic_failures_count": len(remaining_semantic_failures),
        },
        "decisions": {
            "runtime_switch_allowed": False,
            "ui_open_allowed": False,
            "sf50m_allowed": False,
            "phase28_allowed": False,
            "training_allowed_next": True,
            "repair_required_before_runtime": True,
            "guard_gap_fixed": malformed_guard_fixed,
        },
        "decision": (
            "Keep runtime blocked. The guard now blocks observed malformed "
            "open_social fragments, but semantic collapse remains and requires "
            "a targeted Phase 27.74 repair."
        ),
        "next_phase": (
            "Phase 27.74 — targeted open_social semantic-collapse repair "
            "before any runtime switch"
        ),
    }


def _write_json(path: Path, report: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def _write_samples(path: Path, report: dict[str, Any]) -> None:
    lines = ["# Phase 27.73 Open-Social Failure Inspection", ""]
    for item in report["failure_diagnoses"]:
        lines.extend(
            [
                f"## {item['id']}",
                "",
                f"- dialect: `{item['dialect']}`",
                f"- prompt: {item['prompt']}",
                f"- response: {item['response']}",
                f"- previous reason: `{item['previous_reason']}`",
                f"- guard before: `{item['guard_before']}`",
                f"- guard after: `{item['guard_after_phase27_73']}`",
                f"- diagnosis: {item['diagnosis']}",
                "",
            ]
        )
    lines.extend(["## Artifact Probe Results", ""])
    for item in report["artifact_probe_results"]:
        lines.append(f"- `{item['reason']}` / allowed=`{item['allowed']}`: {item['text']}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _write_doc(path: Path, report: dict[str, Any]) -> None:
    lines = [
        "# Phase 27.73 — Open-Social Failure Inspection",
        "",
        "## الخلاصة",
        "",
        "هذه مرحلة فحص وحوكمة جودة فقط. لم يبدأ تدريب جديد ولم يُفتح runtime.",
        "",
        f"- status: `{report['status']}`",
        f"- source: `{report['source_report']}`",
        f"- source score: `{report['source_total_passed']}/{report['source_total']}`",
        f"- remaining failures: `{report['remaining_failures_count']}`",
        f"- guard gap fixed: `{report['decisions']['guard_gap_fixed']}`",
        f"- runtime switch allowed: `{report['decisions']['runtime_switch_allowed']}`",
        "",
        "## التشخيص",
        "",
    ]
    for item in report["failure_diagnoses"]:
        lines.extend(
            [
                f"### {item['id']}",
                "",
                f"- prompt: {item['prompt']}",
                f"- response: {item['response']}",
                f"- guard after Phase 27.73: `{item['guard_after_phase27_73']['reason']}`",
                f"- diagnosis: {item['diagnosis']}",
                "",
            ]
        )
    lines.extend(
        [
            "## القرار",
            "",
            report["decision"],
            "",
            "## التالي",
            "",
            report["next_phase"],
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    report = build_report()
    _write_json(DEFAULT_REPORT, report)
    _write_samples(DEFAULT_SAMPLES, report)
    _write_doc(DEFAULT_DOC, report)
    print(json.dumps(report["decisions"], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
