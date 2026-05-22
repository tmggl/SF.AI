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


def test_system_corpus_audit_reports_reviewed_seeds_ready() -> None:
    r = client.get("/system/corpus-audit")
    assert r.status_code == 200
    body = r.json()
    assert body["corpus"] == "data/corpus/chat/jsonl"
    assert body["status"] == "READY_FOR_PHASE_12_TOKENIZER_TRAINING"
    assert body["total_records"] == 105
    assert body["training_ready"] == 105
    assert body["issue_count"] == 0
    assert body["dialect_counts"] == {"msa": 75, "saudi": 30}
    assert body["quality_counts"] == {"gold": 30, "silver": 75}


def test_system_source_inventory_reports_reference_layers() -> None:
    r = client.get("/system/source-inventory")
    assert r.status_code == 200
    body = r.json()
    assert body["source_count"] >= 4
    names = {source["name"] for source in body["sources"]}
    assert "chat_training_jsonl" in names
    assert "saudi_dialect_training_tasks_seed_v1" in names
    assert "saudi_seed_v1_lexicon_reference" in names
    assert "mo3jam_saudi_import_slot" in names
    assert any(source["private_or_ignored"] for source in body["sources"])


def test_system_phase12_readiness_is_read_only_and_permission_gated() -> None:
    r = client.get("/system/phase12-readiness")
    assert r.status_code == 200
    body = r.json()
    assert body["phase"].startswith("Phase 12")
    assert body["preflight_pass"] is True
    assert body["training_permission_granted"] is True
    assert body["can_train_now"] is False
    assert body["action"] == "PHASE12_V1_COMPLETED_CONTINUE_PHASE22_CORPUS_TARGET"
    assert body["required_permission_phrase"] == "ابدأ Phase 12"
    assert body["required_confirmation_flag"] == "--confirm-phase12-permission"
    assert body["corpus_status"] == "READY_FOR_PHASE_12_TOKENIZER_TRAINING"
    assert body["corpus_training_ready"] == 105
    assert body["corpus_issue_count"] == 0
    assert body["corpus_dialect_counts"] == {"msa": 75, "saudi": 30}
    assert body["required_dialects"] == ["msa", "saudi"]
    assert body["missing_required_dialects"] == []
    assert body["language_balance_status"] == "READY_MSA_AND_SAUDI"
    assert body["protected_terms_total"] == 30
    assert body["protected_terms_covered"] == 30
    assert body["protected_terms_coverage_ratio"] == 1.0
    assert "artifacts/tokenizers/sf_bpe/v1/vocab.json" in body["artifacts_present"]
    assert "artifacts/tokenizers/sf_bpe/v1/merges.txt" in body["artifacts_present"]
    assert "--confirm-phase12-permission" in body["required_command_after_permission"]


def test_system_phase19_readiness_reports_training_gate() -> None:
    r = client.get("/system/phase19-readiness")
    assert r.status_code == 200
    body = r.json()
    assert body["phase"].startswith("Phase 19")
    assert body["status"] == "NOT_READY_EXPAND_CORPUS_FIRST"
    assert body["can_start_training"] is False
    assert body["lab_experiment_allowed"] is True
    assert body["training_records"] == 105
    assert body["min_training_records"] == 5000
    assert body["target_model"] == "sf-50m"
    assert "corpus_too_small_for_sf50m" in body["blockers"]


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
