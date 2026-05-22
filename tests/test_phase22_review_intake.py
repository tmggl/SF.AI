"""Phase 22 — read-only review export intake scanner."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from fastapi.testclient import TestClient

from apps.api.main import app
from sf_ai.datasets.phase22_review_intake import build_phase22_review_intake_report


client = TestClient(app)


def _write_review_record(
    path: Path,
    *,
    training_allowed: bool = False,
    assistant_generator: str = "template",
) -> None:
    record = {
        "domain": "chat",
        "lang": "ar",
        "messages": [
            {"role": "user", "content": "وش تقدر تسوي؟"},
            {
                "role": "assistant",
                "content": "أساعدك في الفصحى والسعودية ضمن حدود النظام.",
                "generator": assistant_generator,
            },
        ],
        "review_metadata": {
            "contains_raw_generator_output": assistant_generator == "sf_10m_v0_1",
            "assistant_generator_counts": {
                "template": 1 if assistant_generator == "template" else 0,
                "sf_10m_v0_1": 1 if assistant_generator == "sf_10m_v0_1" else 0,
            },
        },
        "provenance": {
            "source": "sf-ai-chat-ui-review-export",
            "license": "user-review-required",
            "language": "ar",
            "dialect": "saudi",
            "quality": "needs_review",
            "training_allowed": training_allowed,
        },
    }
    path.write_text(json.dumps(record, ensure_ascii=False) + "\n", encoding="utf-8")


def test_phase22_review_intake_reports_sample_review_export() -> None:
    report = build_phase22_review_intake_report()
    assert report.phase.startswith("Phase 22")
    assert report.synthetic_llm_data_allowed is False
    assert report.review_files >= 1
    assert report.candidate_files >= 1
    assert any(item.path.endswith("sample_review_export.jsonl") for item in report.files)
    assert report.status == "REVIEW_EXPORTS_READY_FOR_MANUAL_REVIEW"


def test_phase22_review_intake_endpoint() -> None:
    r = client.get("/system/phase22-review-intake")
    assert r.status_code == 200
    body = r.json()
    assert body["phase"].startswith("Phase 22")
    assert body["synthetic_llm_data_allowed"] is False
    assert body["review_path"] == "data/corpus/chat/review"
    assert body["candidate_files"] >= 1
    assert body["total_raw_generator_assistant_records"] == 0
    assert any(
        f["status"] == "candidate_review_export"
        for f in body["files"]
    )


def test_phase22_review_intake_cli_is_read_only() -> None:
    proc = subprocess.run(
        [".venv/bin/python", "scripts/phase22_review_intake.py"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0
    assert "SF.AI — Phase 22 review intake" in proc.stdout
    assert "synthetic_llm_data_allowed    : false" in proc.stdout
    assert "raw_generator_records" in proc.stdout
    assert "suggested_msa_command" in proc.stdout
    assert "suggested_saudi_command" in proc.stdout


def test_phase22_review_intake_warns_on_training_allowed_true(tmp_path: Path) -> None:
    review_dir = tmp_path / "review"
    review_dir.mkdir()
    _write_review_record(review_dir / "bad_review.jsonl", training_allowed=True)

    report = build_phase22_review_intake_report(
        project_dir=tmp_path,
        review_dir=review_dir,
    )

    assert report.status == "REVIEW_EXPORT_HAS_TRAINING_ALLOWED_TRUE"
    assert report.candidate_files == 0
    assert report.files[0].status == "review_payload_should_not_be_training_allowed"
    assert report.files[0].training_allowed_true == 1


def test_phase22_review_intake_marks_raw_generator_exports_as_lab_only(tmp_path: Path) -> None:
    review_dir = tmp_path / "review"
    review_dir.mkdir()
    _write_review_record(
        review_dir / "raw_generator.jsonl",
        assistant_generator="sf_10m_v0_1",
    )

    report = build_phase22_review_intake_report(
        project_dir=tmp_path,
        review_dir=review_dir,
    )

    assert report.status == "REVIEW_EXPORT_HAS_RAW_GENERATOR_OUTPUT"
    assert report.candidate_files == 0
    assert report.total_raw_generator_assistant_records == 1
    assert report.files[0].status == "raw_generator_review_export_not_training_candidate"


def test_system_status_reports_phase22_review_intake_component() -> None:
    r = client.get("/system/status")
    assert r.status_code == 200
    body = r.json()
    assert any(
        c["name"] == "phase22_review_intake" and c["status"] == "active"
        for c in body["components"]
    )
