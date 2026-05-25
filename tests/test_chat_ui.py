"""Phase 9 — chat UI mounted at /ui/chat."""

from __future__ import annotations

import json
from pathlib import Path

from fastapi.testclient import TestClient

from apps.api.main import app
from apps.api.routers import chat as chat_router

client = TestClient(app)


def test_ui_chat_serves_html() -> None:
    r = client.get("/ui/chat")
    assert r.status_code == 200
    body = r.text
    assert "<html" in body
    assert "SF.AI" in body
    assert "/chat/message" in body  # the JS posts there
    # RTL Arabic surface is present.
    assert 'dir="rtl"' in body
    assert "محادثة" in body
    assert "--bg: #f6f8fb" in body
    assert "اكتب رسالتك هنا" in body
    assert "المحادثة جاهزة" in body
    assert "قالب ثابت - ليس مولدًا" not in body
    assert "مولّد تجريبي" not in body
    assert "المولّد مباشر" in body
    assert "generator_trial" not in body
    assert "Canary SF-10M v0.2" in body
    assert "مولّد SF-10M Phase 27.47" in body
    assert "ذاكرة:" in body
    assert "تصدير" not in body
    assert "حفظ للمراجعة" not in body
    assert "/chat/review-export" not in body
    assert "جودة التصدير" not in body
    assert "بوابة Phase 22" not in body
    assert "user-badge" in body


def test_get_chat_redirects_to_ui() -> None:
    r = client.get("/chat", follow_redirects=False)
    assert r.status_code in (301, 302, 307)
    assert "/ui/chat" in r.headers.get("location", "")


def test_post_chat_message_still_works_after_ui_mount() -> None:
    r = client.post("/chat/message", json={"message": "علومك", "session_id": "ui-test"})
    assert r.status_code == 200
    body = r.json()
    assert body["domain"] == "chat"
    assert body["intent"] == "chat.smalltalk"
    assert body["generator"] == "sf_10m_phase27_81"


def test_save_review_export_writes_review_only_jsonl(
    tmp_path: Path, monkeypatch
) -> None:
    monkeypatch.setattr(chat_router, "REVIEW_EXPORT_DIR", tmp_path)
    record = {
        "domain": "chat",
        "lang": "ar",
        "messages": [
            {"role": "user", "content": "أريد حوارًا فصيحًا للمراجعة."},
            {
                "role": "assistant",
                "content": "هذا رد مراجعة فقط.",
                "generator": "generator_blocked",
                "intent": "chat.general",
                "domain": "chat",
            },
        ],
        "review_metadata": {
            "exported_from": "ui",
            "session_id": "sf-test",
            "owner_user_id": "sami-local",
            "exported_by_user_id": "sami-local",
            "target_user_id": "sami-local",
            "user_scope": "single_user",
            "phase22_next_batch": {"batch_id": "msa_001"},
            "ui_quality_score": 70,
            "ui_quality_label": "مرشح متوسط بعد مراجعة",
            "ui_quality_blockers": [],
            "contains_raw_generator_output": False,
        },
        "provenance": {
            "source": "sf-ai-chat-ui-review-export",
            "license": "user-review-required",
            "language": "ar",
            "dialect": "msa",
            "quality": "needs_review",
            "training_allowed": False,
            "owner_user_id": "sami-local",
            "created_by_user_id": "sami-local",
            "target_user_id": "sami-local",
            "user_scope": "single_user",
            "notes": "Review only.",
        },
    }

    r = client.post(
        "/chat/review-export",
        json={"session_id": "sf-test", "user_id": "sami-local", "record": record},
    )

    assert r.status_code == 201
    body = r.json()
    assert body["saved"] is True
    assert body["training_allowed"] is False
    assert body["status"] == "saved_for_manual_review_only"
    saved_path = tmp_path / body["filename"]
    assert saved_path.exists()
    saved = json.loads(saved_path.read_text(encoding="utf-8"))
    assert saved["provenance"]["training_allowed"] is False
    assert saved["provenance"]["quality"] == "needs_review"
    assert saved["provenance"]["owner_user_id"] == "sami-local"
    assert saved["review_metadata"]["target_user_id"] == "sami-local"


def test_save_review_export_rejects_training_allowed_true(
    tmp_path: Path, monkeypatch
) -> None:
    monkeypatch.setattr(chat_router, "REVIEW_EXPORT_DIR", tmp_path)
    record = {
        "domain": "chat",
        "messages": [
            {"role": "user", "content": "اختبار"},
            {"role": "assistant", "content": "رد"},
        ],
        "review_metadata": {
            "exported_from": "ui",
            "owner_user_id": "sami-local",
            "exported_by_user_id": "sami-local",
            "target_user_id": "sami-local",
            "user_scope": "single_user",
        },
        "provenance": {
            "quality": "needs_review",
            "training_allowed": True,
            "owner_user_id": "sami-local",
            "created_by_user_id": "sami-local",
            "target_user_id": "sami-local",
            "user_scope": "single_user",
        },
    }

    r = client.post(
        "/chat/review-export",
        json={"session_id": "sf-test", "record": record},
    )

    assert r.status_code == 400
    assert "training_allowed=false" in r.json()["detail"]
    assert not list(tmp_path.glob("*.jsonl"))


def test_save_review_export_rejects_operational_internal_dialogue(
    tmp_path: Path, monkeypatch
) -> None:
    monkeypatch.setattr(chat_router, "REVIEW_EXPORT_DIR", tmp_path)
    record = {
        "domain": "chat",
        "messages": [
            {"role": "user", "content": "التالي شغل pytest ثم ارفع commit"},
            {"role": "assistant", "content": "سأفحص readiness وأحدث corpus."},
        ],
        "review_metadata": {
            "exported_from": "ui",
            "owner_user_id": "sami-local",
            "exported_by_user_id": "sami-local",
            "target_user_id": "sami-local",
            "user_scope": "single_user",
        },
        "provenance": {
            "quality": "needs_review",
            "training_allowed": False,
            "owner_user_id": "sami-local",
            "created_by_user_id": "sami-local",
            "target_user_id": "sami-local",
            "user_scope": "single_user",
        },
    }

    r = client.post(
        "/chat/review-export",
        json={"session_id": "sf-test", "record": record},
    )

    assert r.status_code == 400
    assert "training_forbidden_operational_internal_dialogue" in r.json()["detail"]
    assert not list(tmp_path.glob("*.jsonl"))


def test_save_review_export_rejects_missing_user_ownership(
    tmp_path: Path, monkeypatch
) -> None:
    monkeypatch.setattr(chat_router, "REVIEW_EXPORT_DIR", tmp_path)
    record = {
        "domain": "chat",
        "messages": [
            {"role": "user", "content": "اختبار"},
            {"role": "assistant", "content": "رد"},
        ],
        "review_metadata": {"exported_from": "ui"},
        "provenance": {
            "quality": "needs_review",
            "training_allowed": False,
        },
    }

    r = client.post(
        "/chat/review-export",
        json={"session_id": "sf-test", "user_id": "sami-local", "record": record},
    )

    assert r.status_code == 400
    assert "ownership" in r.json()["detail"]
    assert not list(tmp_path.glob("*.jsonl"))


def test_system_status_reports_current_phase_with_chat_ui() -> None:
    r = client.get("/system/status")
    assert r.status_code == 200
    body = r.json()
    assert "Phase 27.115" in body["current_phase"]
    assert any(c["name"] == "chat_ui" and c["status"] == "active"
               for c in body["components"])
    assert any(c["name"] == "native_generator" and c["status"] == "ready_offline"
               for c in body["components"])
    assert any(c["name"] == "evaluation_harness" and c["status"] == "active"
               for c in body["components"])
    assert any(c["name"] == "chat_rag_bridge" and c["status"] == "ready_offline"
               for c in body["components"])
    assert any(c["name"] == "dialogue_batch_preparation" and c["status"] == "active"
               for c in body["components"])
    assert any(c["name"] == "chat_review_export" and c["status"] == "internal_only"
               for c in body["components"])
    assert any(c["name"] == "chat_review_local_save" and c["status"] == "internal_only"
               for c in body["components"])
    assert any(c["name"] == "phase19_readiness" and c["status"] == "active"
               for c in body["components"])
    assert any(c["name"] == "domain_activation_gates" and c["status"] == "active"
               for c in body["components"])
    assert any(c["name"] == "generative_roadmap" and c["status"] == "active"
               for c in body["components"])
    assert any(c["name"] == "phase22_readiness" and c["status"] == "active"
               for c in body["components"])
    assert any(c["name"] == "coding_module" and c["status"] == "skeleton_only"
               for c in body["components"])
    assert any(c["name"] == "corpus_governance" and c["status"] == "active"
               for c in body["components"])
