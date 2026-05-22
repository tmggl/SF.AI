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


def test_system_status_reports_phase_17_with_chat_ui() -> None:
    r = client.get("/system/status")
    assert r.status_code == 200
    body = r.json()
    assert "Phase 17" in body["current_phase"]
    assert any(c["name"] == "chat_ui" and c["status"] == "active"
               for c in body["components"])
    assert any(c["name"] == "native_generator" and c["status"] == "ready_offline"
               for c in body["components"])
    assert any(c["name"] == "evaluation_harness" and c["status"] == "active"
               for c in body["components"])
    assert any(c["name"] == "chat_rag_bridge" and c["status"] == "ready_offline"
               for c in body["components"])
    assert any(c["name"] == "coding_module" and c["status"] == "skeleton_only"
               for c in body["components"])
    assert any(c["name"] == "corpus_governance" and c["status"] == "active"
               for c in body["components"])
