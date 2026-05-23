"""Phase 20 — domain activation gates.

The gate is intentionally read-only. It should reveal blockers and prevent
silent activation of skeleton domains.
"""

from __future__ import annotations

import subprocess

from fastapi.testclient import TestClient

from apps.api.main import app
from sf_ai.core.activation import build_phase20_activation_gates


client = TestClient(app)


def test_phase20_gates_keep_only_chat_active() -> None:
    decision = build_phase20_activation_gates()
    assert decision.phase.startswith("Phase 20")
    assert decision.status == "PHASE20_GATES_ACTIVE_NO_DOMAIN_AUTO_ACTIVATED"
    assert decision.language_track == ("msa", "saudi")
    assert "Saudi Seed v1" in decision.lexicon_track
    assert decision.active_domains == ("chat",)
    assert "coding" in decision.blocked_domains
    assert "medical" in decision.blocked_domains


def test_phase20_sensitive_domains_stay_blocked_without_policy() -> None:
    decision = build_phase20_activation_gates()
    gates = {gate.domain: gate for gate in decision.gates}
    for domain in ("legal", "medical", "finance", "security", "religion"):
        gate = gates[domain]
        assert gate.requires_safety is True
        assert gate.can_activate_now is False
        assert "safety_policy_missing" in gate.blockers
        assert gate.recommended_status == "keep_skeleton_only"


def test_phase20_text_domains_wait_for_activation_tests_after_corpus_gate() -> None:
    decision = build_phase20_activation_gates()
    gates = {gate.domain: gate for gate in decision.gates}
    for domain in ("coding", "data", "writing", "translation", "education"):
        gate = gates[domain]
        assert gate.current_status == "skeleton_only"
        assert gate.can_activate_now is False
        assert "data_or_model_not_ready" not in gate.blockers
        assert "domain_activation_tests_missing" in gate.blockers


def test_phase20_productivity_gap_is_closed_as_skeleton() -> None:
    decision = build_phase20_activation_gates()
    gates = {gate.domain: gate for gate in decision.gates}
    productivity = gates["productivity"]
    assert productivity.manifest_present is True
    assert productivity.registry_present is True
    assert "manifest_missing" not in productivity.blockers


def test_system_phase20_gates_endpoint() -> None:
    r = client.get("/system/phase20-gates")
    assert r.status_code == 200
    body = r.json()
    assert body["phase"].startswith("Phase 20")
    assert body["language_track"] == ["msa", "saudi"]
    assert body["active_domains"] == ["chat"]
    assert body["sensitive_domains"] == [
        "finance",
        "legal",
        "medical",
        "religion",
        "security",
    ]
    assert any(g["domain"] == "coding" for g in body["gates"])


def test_phase20_cli_is_read_only_and_reports_gates() -> None:
    proc = subprocess.run(
        [".venv/bin/python", "scripts/phase20_gates.py"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0
    assert "Phase 20" in proc.stdout
    assert "language_track                : msa, saudi" in proc.stdout
    assert "coding" in proc.stdout
    assert "medical" in proc.stdout
