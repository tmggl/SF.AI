"""Constitution layer checks before Phase 12."""

from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parent.parent


def test_constitution_docs_exist() -> None:
    required = [
        "docs/PROJECT_CONSTITUTION.md",
        "docs/LANGUAGE_SEGMENTATION.md",
        "docs/TOKENIZATION_POLICY.md",
        "docs/DATASET_GOVERNANCE.md",
        "docs/AGENT_ENGINEERING_RULES.md",
    ]
    for rel in required:
        path = ROOT / rel
        assert path.exists(), rel
        assert path.read_text(encoding="utf-8").strip(), rel


def test_tokenization_resources_exist_and_include_core_saudi_terms() -> None:
    protected = ROOT / "resources/tokenization/protected_terms_saudi.txt"
    preferred = ROOT / "resources/tokenization/preferred_merges.txt"
    rules = ROOT / "resources/tokenization/tokenization_rules.yaml"

    assert protected.exists()
    assert preferred.exists()
    assert rules.exists()

    terms = {
        line.strip()
        for line in protected.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    }
    for term in ["وش", "وشلون", "تكفى", "لا هنت", "الله لا يهينك"]:
        assert term in terms


def test_msa_candidate_terms_are_large_and_not_active_training_data() -> None:
    protected = ROOT / "resources/tokenization/protected_terms_msa_candidate.txt"
    preferred = ROOT / "resources/tokenization/preferred_merges_msa_candidate.txt"

    assert protected.exists()
    assert preferred.exists()

    protected_terms = {
        line.strip()
        for line in protected.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    }
    preferred_terms = {
        line.strip()
        for line in preferred.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    }

    assert len(protected_terms) >= 120
    assert len(preferred_terms) >= 80
    for term in [
        "الذكاء الاصطناعي",
        "النموذج اللغوي",
        "السيادة المعرفية",
        "بوابة الجاهزية",
        "العربية الفصحى",
    ]:
        assert term in protected_terms
        assert term in preferred_terms

    header = protected.read_text(encoding="utf-8").splitlines()[:6]
    assert any("NOT pretrained vocabulary" in line for line in header)
    assert any("NOT active protected terms yet" in line for line in header)


def test_tokenization_rules_preserve_sovereign_constraints() -> None:
    rules_path = ROOT / "resources/tokenization/tokenization_rules.yaml"
    rules = yaml.safe_load(rules_path.read_text(encoding="utf-8"))

    assert rules["encoding"] == "utf-8"
    assert rules["scope"]["current_dialects"] == ["msa", "saudi"]
    assert rules["sovereignty"]["no_pretrained_vocab"] is True
    assert rules["sovereignty"]["no_pretrained_merges"] is True
    assert rules["sovereignty"]["learn_from_sovereign_corpus_only"] is True
    assert rules["normalization"]["arabizi_has_separate_normalization"] is True
    assert rules["normalization"]["code_is_separate_from_dialogue"] is True
    assert rules["protected_terms"]["policy"] == "avoid_aggressive_splitting"
    assert rules["protected_terms"]["active_paths"] == [
        "resources/tokenization/protected_terms_saudi.txt"
    ]
    assert rules["protected_terms"]["candidate_paths"] == [
        "resources/tokenization/protected_terms_msa_candidate.txt"
    ]
    assert rules["preferred_merges"]["candidate_paths"] == [
        "resources/tokenization/preferred_merges_msa_candidate.txt"
    ]
    assert "resources/tokenization/protected_phrases_phase27_75.txt" in (
        rules["protected_phrases"]["active_paths"]
    )
    assert rules["artifact_requirements"]["require_sf_origin"] is True
