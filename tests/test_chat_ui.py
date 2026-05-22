"""Phase 9 — chat UI mounted at /ui/chat."""

from __future__ import annotations

from fastapi.testclient import TestClient

from apps.api.main import app

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
    assert "قالب ثابت - ليس مولدًا" in body
    assert "بوابة Phase 22" in body
    assert "/system/phase22-readiness" in body
    assert "/system/phase22-collection-plan?batch_size=25" in body
    assert "غير جاهز للتوكنزر بعد" in body
    assert "جودة التصدير" in body
    assert "quality-score" in body
    assert "ui_quality_score" in body
    assert "ui_quality_label" in body
    assert "ذاكرة:" in body
    assert "تصدير" in body
    assert "training_allowed: false" in body or "training_allowed\": false" in body
    assert "sfai_chat_review_" in body


def test_get_chat_redirects_to_ui() -> None:
    r = client.get("/chat", follow_redirects=False)
    assert r.status_code in (301, 302, 307)
    assert "/ui/chat" in r.headers.get("location", "")


def test_post_chat_message_still_works_after_ui_mount() -> None:
    r = client.post("/chat/message", json={"message": "مرحبا", "session_id": "ui-test"})
    assert r.status_code == 200
    body = r.json()
    assert body["domain"] == "chat"
    assert body["intent"] == "chat.greeting"


def test_system_status_reports_phase_22_with_chat_ui() -> None:
    r = client.get("/system/status")
    assert r.status_code == 200
    body = r.json()
    assert "Phase 22" in body["current_phase"]
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
    assert any(c["name"] == "chat_review_export" and c["status"] == "active"
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
