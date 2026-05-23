"""Phase 11 — governance checks for Saudi/MSA training corpus."""

from __future__ import annotations

from pathlib import Path

from sf_ai.datasets import (
    audit_jsonl_directory_for_training,
    audit_jsonl_file_for_training,
    audit_record_for_training,
)


def _ready_record(dialect: str = "saudi", quality: str = "gold") -> dict:
    return {
        "domain": "chat",
        "lang": "ar",
        "messages": [
            {"role": "user", "content": "وشلونك؟"},
            {"role": "assistant", "content": "بخير، شكرًا لك."},
        ],
        "provenance": {
            "source": "sami-authored",
            "license": "user-provided",
            "language": "ar",
            "dialect": dialect,
            "quality": quality,
            "training_allowed": True,
            "owner_user_id": "sami-local",
            "created_by_user_id": "sami-local",
            "target_user_id": "sami-local",
            "user_scope": "single_user",
        },
    }


def test_training_ready_record_has_no_governance_issues() -> None:
    issues = audit_record_for_training(_ready_record(), line_number=1)
    assert issues == []


def test_missing_provenance_is_rejected() -> None:
    raw = {
        "domain": "chat",
        "lang": "ar",
        "messages": [
            {"role": "user", "content": "مرحبا"},
            {"role": "assistant", "content": "أهلًا"},
        ],
    }
    issues = audit_record_for_training(raw, line_number=1)
    assert any(i.message == "missing provenance" for i in issues)


def test_only_msa_and_saudi_are_training_ready() -> None:
    issues = audit_record_for_training(_ready_record(dialect="egyptian"), line_number=1)
    assert any("dialect must be" in i.message for i in issues)


def test_quality_is_required_for_training_pack() -> None:
    raw = _ready_record()
    raw["provenance"].pop("quality")
    issues = audit_record_for_training(raw, line_number=1)
    assert any("quality must be" in i.message for i in issues)


def test_training_allowed_must_be_true_for_training_pack() -> None:
    raw = _ready_record()
    raw["provenance"]["training_allowed"] = False
    issues = audit_record_for_training(raw, line_number=1)
    assert any("training_allowed must be true" in i.message for i in issues)


def test_operational_project_dialogue_is_training_forbidden() -> None:
    raw = _ready_record(dialect="msa", quality="silver")
    raw["messages"] = [
        {"role": "user", "content": "التالي: شغل pytest ثم ارفع commit"},
        {"role": "assistant", "content": "سأراجع readiness وأحدث corpus."},
    ]
    issues = audit_record_for_training(raw, line_number=1)
    assert any("training_forbidden operational/internal" in i.message for i in issues)


def test_natural_daily_dialogue_is_not_operationally_blocked() -> None:
    raw = _ready_record(dialect="saudi", quality="silver")
    raw["messages"] = [
        {"role": "user", "content": "هلا، وش رايك نطلع بدري؟"},
        {"role": "assistant", "content": "فكرة طيبة، إذا خلصنا شغلنا نطلع قبل الزحمة."},
        {"role": "user", "content": "تمام، خلها بعد العصر."},
        {"role": "assistant", "content": "تم، بعد العصر مناسب."},
    ]
    issues = audit_record_for_training(raw, line_number=1)
    assert issues == []


def test_user_ownership_fields_are_required_for_training_pack() -> None:
    raw = _ready_record()
    raw["provenance"].pop("target_user_id")
    issues = audit_record_for_training(raw, line_number=1)
    assert any("target_user_id" in i.message for i in issues)


def test_dialogue_must_include_user_and_assistant() -> None:
    raw = _ready_record()
    raw["messages"] = [{"role": "user", "content": "مرحبا"}]
    issues = audit_record_for_training(raw, line_number=1)
    assert any("user and one assistant" in i.message for i in issues)


def test_audit_jsonl_file_counts_ready_records(tmp_path: Path) -> None:
    f = tmp_path / "pack.jsonl"
    f.write_text(
        (
            '{"domain":"chat","lang":"ar","messages":[{"role":"user","content":"مرحبا"},'
            '{"role":"assistant","content":"أهلًا"}],"provenance":{"source":"sami",'
            '"license":"user-provided","language":"ar","dialect":"msa","quality":"gold",'
            '"training_allowed":true,"owner_user_id":"sami-local","created_by_user_id":"sami-local","target_user_id":"sami-local","user_scope":"single_user"}}\n'
        )
        + (
            '{"domain":"chat","lang":"ar","messages":[{"role":"user","content":"ازيك"},'
            '{"role":"assistant","content":"تمام"}],"provenance":{"source":"x",'
            '"license":"user-provided","language":"ar","dialect":"egyptian","quality":"gold",'
            '"training_allowed":true,"owner_user_id":"sami-local","created_by_user_id":"sami-local","target_user_id":"sami-local","user_scope":"single_user"}}\n'
        ),
        encoding="utf-8",
    )
    report = audit_jsonl_file_for_training(f)
    assert report.total_records == 2
    assert report.training_ready == 1
    assert report.dialect_counts == {"msa": 1}
    assert report.error_count == 1


def test_audit_jsonl_directory_rejects_empty_corpus(tmp_path: Path) -> None:
    report = audit_jsonl_directory_for_training(tmp_path)
    assert report.total_records == 0
    assert report.training_ready == 0
    assert report.error_count == 1
    assert "no JSONL files found" in report.issues[0].message


def test_audit_jsonl_directory_aggregates_ready_records(tmp_path: Path) -> None:
    first = tmp_path / "msa.jsonl"
    second = tmp_path / "saudi.jsonl"
    first.write_text(
        (
            '{"domain":"chat","lang":"ar","messages":[{"role":"user","content":"مرحبا"},'
            '{"role":"assistant","content":"أهلًا"}],"provenance":{"source":"sami",'
            '"license":"user-provided","language":"ar","dialect":"msa","quality":"gold",'
            '"training_allowed":true,"owner_user_id":"sami-local","created_by_user_id":"sami-local","target_user_id":"sami-local","user_scope":"single_user"}}\n'
        ),
        encoding="utf-8",
    )
    second.write_text(
        (
            '{"domain":"chat","lang":"ar","messages":[{"role":"user","content":"وشلونك"},'
            '{"role":"assistant","content":"بخير"}],"provenance":{"source":"sami",'
            '"license":"user-provided","language":"ar","dialect":"saudi","quality":"silver",'
            '"training_allowed":true,"owner_user_id":"sami-local","created_by_user_id":"sami-local","target_user_id":"sami-local","user_scope":"single_user"}}\n'
        ),
        encoding="utf-8",
    )

    report = audit_jsonl_directory_for_training(tmp_path)
    assert report.total_records == 2
    assert report.training_ready == 2
    assert report.error_count == 0
    assert report.dialect_counts == {"msa": 1, "saudi": 1}
    assert report.quality_counts == {"gold": 1, "silver": 1}
