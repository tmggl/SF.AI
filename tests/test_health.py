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
    assert body["phase"] == "Phase 27.37"


def test_system_status_sovereign_flags() -> None:
    r = client.get("/system/status")
    assert r.status_code == 200
    body = r.json()
    assert body["project"] == "SF.AI"
    assert body["current_phase"].startswith("Phase 27.37")
    assert body["current_phase_status"] == "completed_supported_topic_expansion_quality_gated"
    assert "Phase 27.38" in body["next_phase"]
    assert body["sovereign"] is True
    assert body["uses_external_llm"] is False
    assert body["uses_pretrained_weights"] is False
    assert body["uses_pretrained_embeddings"] is False
    assert body["uses_pretrained_tokenizer"] is False
    assert any(c["name"] == "api" and c["status"] == "active" for c in body["components"])
    assert any(c["name"] == "orchestrator" and c["status"] == "active" for c in body["components"])
    assert any(c["name"] == "phase23_tokenizer_v2" and c["status"] == "active" for c in body["components"])
    assert any(
        c["name"] == "phase24_sf10m_v0_2"
        and c["status"] == "completed_runtime_blocked"
        for c in body["components"]
    )
    assert any(
        c["name"] == "phase25_generation_canary"
        and c["status"] == "active_runtime_guard"
        for c in body["components"]
    )
    assert any(
        c["name"] == "phase26_readiness"
        and c["status"] == "completed_training_blocked"
        for c in body["components"]
    )
    assert any(
        c["name"] == "phase27_dialogue_eval_v2"
        and c["status"] == "completed_with_blockers"
        for c in body["components"]
    )
    assert any(
        c["name"] == "phase27_7_fixed_dialogue_split"
        and c["status"] == "active_quality_gate"
        for c in body["components"]
    )
    assert any(
        c["name"] == "phase27_8_sf10m_v0_6"
        and c["status"] == "completed_runtime_blocked"
        for c in body["components"]
    )
    assert any(
        c["name"] == "phase27_9_generation_quality_harness"
        and c["status"] == "active_runtime_gate"
        for c in body["components"]
    )
    assert any(
        c["name"] == "phase27_10_short_response_repair"
        and c["status"] == "completed_runtime_blocked"
        for c in body["components"]
    )
    assert any(
        c["name"] == "phase27_11_objective_probe"
        and c["status"] == "completed_stop_boundary_blocked"
        for c in body["components"]
    )
    assert any(
        c["name"] == "phase27_12_assistant_eos_repair"
        and c["status"] == "completed_partial_runtime_blocked"
        for c in body["components"]
    )
    assert any(
        c["name"] == "phase27_13_sf10m_v0_8_boundary_eos_training"
        and c["status"] == "completed_eval_improved_runtime_blocked"
        for c in body["components"]
    )
    assert any(
        c["name"] == "phase27_14_sovereign_quality_tooling"
        and c["status"] == "completed_no_training"
        for c in body["components"]
    )
    assert any(
        c["name"] == "phase27_15_social_lexical_curriculum"
        and c["status"] == "completed_eval_improved_runtime_blocked"
        for c in body["components"]
    )
    assert any(
        c["name"] == "phase27_16_prompt_to_answer_objective"
        and c["status"] == "completed_objective_repair_runtime_blocked"
        for c in body["components"]
    )
    assert any(
        c["name"] == "phase27_17_prompt_answer_micro_probe"
        and c["status"] == "completed_breakthrough_runtime_blocked"
        for c in body["components"]
    )
    assert any(
        c["name"] == "phase27_18_tokenization_decoding_hygiene"
        and c["status"] == "completed_hygiene_audit_runtime_blocked"
        for c in body["components"]
    )
    assert any(
        c["name"] == "phase27_19_hygiene_repair_probe"
        and c["status"] == "completed_repair_probe_runtime_blocked"
        for c in body["components"]
    )
    assert any(
        c["name"] == "phase27_20_tokenizer_protected_phrase_strategy"
        and c["status"] == "completed_ready_for_tokenizer_v3_runtime_blocked"
        for c in body["components"]
    )
    assert any(
        c["name"] == "phase27_21_tokenizer_v3_micro_probe"
        and c["status"] == "completed_micro_probe_failed_runtime_blocked"
        for c in body["components"]
    )
    assert any(
        c["name"] == "phase27_22_spacing_boundary_repair"
        and c["status"] == "completed_partial_repair_runtime_blocked"
        for c in body["components"]
    )
    assert any(
        c["name"] == "phase27_23_semantic_lexical_repair"
        and c["status"] == "completed_partial_repair_runtime_blocked"
        for c in body["components"]
    )
    assert any(
        c["name"] == "phase27_24_minimal_lexical_stabilization"
        and c["status"] == "completed_micro_probe_passed_runtime_blocked"
        for c in body["components"]
    )
    assert any(
        c["name"] == "phase27_25_heldout_generation_canary"
        and c["status"] == "completed_failed_runtime_blocked"
        for c in body["components"]
    )
    assert any(
        c["name"] == "phase27_30_fresh_mixed_shadow_canary"
        and c["status"] == "completed_16_of_18_runtime_blocked"
        for c in body["components"]
    )


def test_system_corpus_audit_reports_reviewed_seeds_ready() -> None:
    r = client.get("/system/corpus-audit")
    assert r.status_code == 200
    body = r.json()
    assert body["corpus"] == "data/corpus/chat/jsonl"
    assert body["status"] == "READY_FOR_PHASE_12_TOKENIZER_TRAINING"
    assert body["total_records"] == 5943
    assert body["training_ready"] == 5943
    assert body["issue_count"] == 0
    assert body["dialect_counts"] == {"msa": 2949, "saudi": 2994}
    assert body["quality_counts"] == {"gold": 831, "silver": 5112}


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
    assert body["corpus_training_ready"] == 5943
    assert body["corpus_issue_count"] == 0
    assert body["corpus_dialect_counts"] == {"msa": 2949, "saudi": 2994}
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
    assert body["status"] == "READY_FOR_SF50M_TRAINING"
    assert body["can_start_training"] is True
    assert body["lab_experiment_allowed"] is True
    assert body["training_records"] == 5943
    assert body["min_training_records"] == 5000
    assert body["target_model"] == "sf-50m"
    assert "corpus_too_small_for_sf50m" not in body["blockers"]


def test_system_phase23_tokenizer_audit_reports_v2_ready() -> None:
    r = client.get("/system/phase23-tokenizer-audit")
    assert r.status_code == 200
    body = r.json()
    assert body["phase"].startswith("Phase 23")
    assert body["status"] == "COMPLETED_READY_FOR_PHASE24"
    assert body["tokenizer"]["sf_origin"] is True
    assert body["tokenizer"]["vocab_size"] == 4493
    assert body["corpus"]["training_ready"] == 5943
    assert body["corpus"]["dialects"] == {"msa": 2949, "saudi": 2994}
    assert body["decision"]["runtime_chat_should_use_this_directly"] is False


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
