"""Phase 27.23 — semantic/lexical repair report."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_phase27_23_improves_pass_count_but_blocks_runtime() -> None:
    report = json.loads(
        (ROOT / "artifacts/reports/phase27_23_semantic_lexical_repair_report.json")
        .read_text(encoding="utf-8")
    )

    assert report["phase"] == "Phase 27.23"
    assert report["status"] == "PARTIAL_SEMANTIC_LEXICAL_REPAIR_BLOCK_RUNTIME"
    assert report["tokenizer"]["path"] == "artifacts/tokenizers/sf_bpe/v3"
    assert report["previous_phase27_22"]["passed"] == 29
    assert report["current"]["passed"] == 30
    assert report["current"]["exact_clean"] == 30
    assert report["current"]["semantic_match"] == 30
    assert report["runtime_allowed"] is False
    assert report["sf50m_allowed"] is False
    assert "Phase 27.24" in report["next_phase"]


def test_phase27_23_remaining_failures_are_lexical_stability() -> None:
    report = json.loads(
        (ROOT / "artifacts/reports/phase27_23_semantic_lexical_repair_report.json")
        .read_text(encoding="utf-8")
    )
    failed = [row for row in report["results"] if not row["passed"]]

    assert len(failed) == 2
    failed_prompts = {row["prompt"] for row in failed}
    assert failed_prompts == {"اشرح لي التعاون", "ما معنى الاحترام"}
    generated = "\n".join(row["generated"] for row in failed)
    assert "التعاعاون" in generated
    assert "الاحتات" in generated
