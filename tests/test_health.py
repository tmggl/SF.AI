"""Phase 1+2 — API smoke tests (health, system status, chat wiring)."""

from __future__ import annotations

from fastapi.testclient import TestClient

from apps.api.main import app

client = TestClient(app)


def test_root() -> None:
    r = client.get("/")
    assert r.status_code == 200
    body = r.json()
    assert body["project"] == "SF.AI"
    assert "Phase" in body["phase"]


def test_health_ok() -> None:
    r = client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert body["project"] == "SF.AI"


def test_system_status_sovereign_flags() -> None:
    r = client.get("/system/status")
    assert r.status_code == 200
    body = r.json()
    assert body["project"] == "SF.AI"
    assert body["sovereign"] is True
    assert body["uses_external_llm"] is False
    assert body["uses_pretrained_weights"] is False
    assert body["uses_pretrained_embeddings"] is False
    assert body["uses_pretrained_tokenizer"] is False
    assert any(c["name"] == "api" and c["status"] == "active" for c in body["components"])
    assert any(c["name"] == "orchestrator" and c["status"] == "active" for c in body["components"])


def test_system_corpus_audit_reports_not_ready_without_jsonl() -> None:
    r = client.get("/system/corpus-audit")
    assert r.status_code == 200
    body = r.json()
    assert body["corpus"] == "data/corpus/chat/jsonl"
    assert body["status"] == "NOT_READY_FOR_TRAINING"
    assert body["total_records"] == 0
    assert body["training_ready"] == 0
    assert body["issue_count"] >= 1
    assert any("no JSONL files found" in issue["message"] for issue in body["issues"])


def test_chat_greeting_routes_through_module() -> None:
    r = client.post("/chat/message", json={"message": "مرحبا", "session_id": "api-test-1"})
    assert r.status_code == 200
    body = r.json()
    assert body["domain"] == "chat"
    assert body["intent"] == "chat.greeting"
    assert body["confidence"] > 0.0
    assert body["status"] == "active"
    assert body["requires_safety"] is False
    assert body["fallback_used"] is False
    assert body["dispatch"] == "module:chat"
    assert body["echo"] == "مرحبا"
    assert "SF.AI" in body["response"]


def test_chat_unknown_falls_back_to_general() -> None:
    r = client.post("/chat/message", json={"message": "zzz qqq xyz"})
    assert r.status_code == 200
    body = r.json()
    assert body["domain"] == "chat"
    assert body["intent"] == "chat.general"
    assert body["fallback_used"] is True
    assert body["dispatch"] == "module:chat"


def test_chat_medical_triggers_safety_flag_and_uses_composer() -> None:
    r = client.post("/chat/message", json={"message": "عندي الم في الراس"})
    assert r.status_code == 200
    body = r.json()
    assert body["domain"] == "medical"
    assert body["requires_safety"] is True
    # Sensitive domains go through the composer's safety reply, not the module.
    assert body["dispatch"] == "composer"


def test_chat_rejects_empty_message() -> None:
    r = client.post("/chat/message", json={"message": ""})
    assert r.status_code == 422
