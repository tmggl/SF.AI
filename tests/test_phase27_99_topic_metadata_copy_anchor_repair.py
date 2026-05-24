"""Phase 27.99 — topic metadata/copy-anchor repair coverage."""

from __future__ import annotations

import json
from pathlib import Path

from scripts.phase27_99_topic_metadata_copy_anchor_repair import (
    DEFAULT_FILES,
    DEFAULT_REPORT,
)

ROOT = Path(__file__).resolve().parents[1]
DECISION = ROOT / "artifacts/reports/PHASE27_99_TOPIC_METADATA_COPY_ANCHOR_REPAIR_DECISION.json"


def _copy_anchor_ok(answer: str, term: str) -> bool:
    compact = "".join(ch for ch in answer if not ch.isspace())
    return bool(term and compact.find(term) != -1 and compact.find(term) <= 12)


def test_phase27_99_topic_files_have_explicit_topic_terms_and_copy_anchor() -> None:
    for path in DEFAULT_FILES:
        rows = [
            json.loads(line)
            for line in Path(path).read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        assert rows
        for row in rows:
            provenance = row["provenance"]
            topic = provenance["topic_term"]
            assert provenance["dialogue_family"] == "topic"
            assert provenance["topic_metadata_repair_phase"] == "Phase 27.99"
            assert topic
            assistant = next(
                message["content"]
                for message in row["messages"]
                if message["role"] == "assistant"
            )
            assert _copy_anchor_ok(assistant, topic)


def test_phase27_99_report_allows_only_bounded_training_next() -> None:
    report = json.loads(Path(DEFAULT_REPORT).read_text(encoding="utf-8"))
    decision = json.loads(DECISION.read_text(encoding="utf-8"))
    gate = report["post_repair_phase27_98_gate"]

    assert report["decision"] == decision
    assert report["training_started"] is False
    assert report["runtime_changed"] is False
    assert gate["metadata_ready"] is True
    assert gate["copy_anchor_ready"] is True
    assert gate["missing_topic_term_records"] == 0
    assert decision["engineering_decision"] == (
        "ALLOW_PHASE27_100_BOUNDED_TOPIC_BINDING_REPAIR_TRAINING"
    )
    assert decision["new_training_allowed"] is True
    assert decision["runtime_release_allowed"] is False
    assert decision["sf50m_justified_transition"] is False
    assert "Phase 27.100" in decision["next_phase"]
