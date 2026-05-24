"""Phase 27.80 remediation — family-balance plan coverage."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_phase27_80_family_balance_remediation_blocks_training_and_sets_quotas() -> None:
    report = json.loads(
        (
            ROOT / "artifacts/reports/phase27_80_family_balance_remediation_report.json"
        ).read_text(encoding="utf-8")
    )

    assert report["phase"] == "Phase 27.80 remediation"
    assert report["sovereignty_mode"] == "SF-native only"
    assert report["training_started"] is False
    assert report["tokenizer_training_started"] is False
    assert report["runtime_changed"] is False
    assert report["decision"]["new_training_allowed"] is False
    assert report["decision"]["runtime_release_allowed"] is False
    assert report["decision"]["sf50m_justified_transition"] is False

    quotas = report["quota_plan"]["needed_records"]
    assert report["quota_plan"]["total_needed"] == 0
    assert quotas["planning"] == {"total": 0, "msa": 0, "saudi": 0}
    assert quotas["support"] == {"total": 0, "msa": 0, "saudi": 0}
    assert quotas["topic"] == {"total": 0, "msa": 0, "saudi": 0}
    assert quotas["open_social"]["total"] == 0
    assert quotas["followup"]["total"] == 0


def test_phase27_80_family_balance_artifacts_exist_and_are_nontraining() -> None:
    report = json.loads(
        (
            ROOT / "artifacts/reports/phase27_80_family_balance_remediation_report.json"
        ).read_text(encoding="utf-8")
    )
    artifacts = report["artifacts"]

    manifest = ROOT / artifacts["family_manifest"]
    config = json.loads((ROOT / artifacts["balanced_curriculum_config"]).read_text(encoding="utf-8"))
    authoring_plan = json.loads((ROOT / artifacts["authoring_quota_plan"]).read_text(encoding="utf-8"))

    assert manifest.exists()
    assert len(manifest.read_text(encoding="utf-8").splitlines()) == 8443
    assert config["training_allowed_now"] is False
    assert config["underrepresented_family_policy"].startswith("author_more_gold_records")
    assert authoring_plan["topic"]["total"] == 0
