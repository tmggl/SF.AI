"""Phase 27.15 — social/lexical curriculum and strict quality gate."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_phase27_15_report_blocks_runtime_despite_eval_improvement() -> None:
    report = json.loads(
        (ROOT / "artifacts/reports/sf_10m_v0_10_social_lexical_curriculum_report.json")
        .read_text(encoding="utf-8")
    )

    assert report["phase"] == "Phase 27.15"
    assert report["status"] == "completed_eval_improved_strict_generation_blocked"
    assert report["language_track"] == ["msa", "saudi"]
    assert report["lexicon_track"] == "Saudi Seed v1"
    assert report["curriculum"]["records_added"] == 400
    assert report["corpus"]["total_records"] == 5943
    assert report["corpus"]["issues"] == 0
    assert report["eval"]["best_checkpoint_by_eval"] == "sf-10m-step6000"
    assert report["eval"]["checkpoints"][-1]["loss"] == 3.0452
    assert report["generation_quality"]["passed"] == 0
    assert report["generation_quality"]["runtime_allowed"] is False
    assert report["decision"]["activate_in_chat_ui"] is False
    assert report["decision"]["start_sf50m"] is False


def test_phase27_15_curriculum_files_are_training_ready() -> None:
    for name, dialect in (
        ("dialogue_batch_v9_social_lexical_msa_009.jsonl", "msa"),
        ("dialogue_batch_v9_social_lexical_saudi_009.jsonl", "saudi"),
    ):
        path = ROOT / "data/corpus/chat/jsonl" / name
        rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
        assert len(rows) == 200
        assert {row["provenance"]["dialect"] for row in rows} == {dialect}
        assert all(row["provenance"]["quality"] == "gold" for row in rows)
        assert all(row["provenance"]["training_allowed"] is True for row in rows)
