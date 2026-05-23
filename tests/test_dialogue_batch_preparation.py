"""Phase 18 — data expansion loop for reviewed chat exports."""

from __future__ import annotations

import json
from pathlib import Path

from sf_ai.datasets.corpus_governance import audit_jsonl_file_for_training
from sf_ai.datasets.dialogue_batch import prepare_dialogue_batch


def _review_export(path: Path, *, user: str = "وش تقدر تسوي؟") -> None:
    record = {
        "domain": "chat",
        "lang": "ar",
        "messages": [
            {"role": "user", "content": user},
            {"role": "assistant", "content": "أساعدك في الفصحى والسعودية ضمن حدود النظام."},
        ],
        "provenance": {
            "source": "sf-ai-chat-ui-review-export",
            "license": "user-review-required",
            "language": "ar",
            "dialect": "saudi",
            "quality": "needs_review",
            "training_allowed": False,
            "owner_user_id": "sami-local",
            "created_by_user_id": "sami-local",
            "target_user_id": "sami-local",
            "user_scope": "single_user",
        },
    }
    path.write_text(json.dumps(record, ensure_ascii=False) + "\n", encoding="utf-8")


def test_prepare_dialogue_batch_report_only_without_training_allowed(tmp_path: Path) -> None:
    src = tmp_path / "review.jsonl"
    out = tmp_path / "batch.jsonl"
    report_path = tmp_path / "report.json"
    _review_export(src)

    report = prepare_dialogue_batch(
        input_path=src,
        output_path=out,
        report_path=report_path,
        source="sf-ai-user-reviewed-dialogue",
        license_name="user-provided",
        dialect="saudi",
        quality="silver",
        training_allowed=False,
    )

    assert report.total_records == 1
    assert report.written_records == 0
    assert out.exists() is False
    saved = json.loads(report_path.read_text(encoding="utf-8"))
    assert saved["skipped_reasons"]["training_allowed_flag_missing"] == 1


def test_prepare_dialogue_batch_writes_governed_training_jsonl(tmp_path: Path) -> None:
    src = tmp_path / "review.jsonl"
    out = tmp_path / "batch.jsonl"
    report_path = tmp_path / "report.json"
    _review_export(src)

    report = prepare_dialogue_batch(
        input_path=src,
        output_path=out,
        report_path=report_path,
        source="sf-ai-user-reviewed-dialogue",
        license_name="user-provided",
        dialect="saudi",
        quality="gold",
        training_allowed=True,
    )

    assert report.written_records == 1
    audit = audit_jsonl_file_for_training(out)
    assert audit.error_count == 0
    assert audit.training_ready == 1
    row = json.loads(out.read_text(encoding="utf-8"))
    assert row["provenance"]["training_allowed"] is True
    assert row["provenance"]["quality"] == "gold"
    assert row["provenance"]["owner_user_id"] == "sami-local"
    assert row["provenance"]["target_user_id"] == "sami-local"
    assert row["provenance"]["user_scope"] == "single_user"


def test_prepare_dialogue_batch_skips_safety_flagged_by_default(tmp_path: Path) -> None:
    src = tmp_path / "review.jsonl"
    out = tmp_path / "batch.jsonl"
    report_path = tmp_path / "report.json"
    _review_export(src, user="عندي ألم وش الدواء؟")

    report = prepare_dialogue_batch(
        input_path=src,
        output_path=out,
        report_path=report_path,
        source="sf-ai-user-reviewed-dialogue",
        license_name="user-provided",
        dialect="saudi",
        quality="silver",
        training_allowed=True,
    )

    assert report.written_records == 0
    assert report.skipped_reasons["safety_flagged"] == 1


def test_prepare_dialogue_batch_skips_operational_internal_dialogue(tmp_path: Path) -> None:
    src = tmp_path / "review.jsonl"
    out = tmp_path / "batch.jsonl"
    report_path = tmp_path / "report.json"
    _review_export(src, user="التالي شغل pytest ثم ارفع commit")

    report = prepare_dialogue_batch(
        input_path=src,
        output_path=out,
        report_path=report_path,
        source="sf-ai-user-reviewed-dialogue",
        license_name="user-provided",
        dialect="saudi",
        quality="silver",
        training_allowed=True,
    )

    assert report.written_records == 0
    assert report.skipped_reasons["training_forbidden_operational_internal_dialogue"] == 1
