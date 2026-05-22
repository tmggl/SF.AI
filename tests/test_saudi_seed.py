"""Phase 3.6 — Saudi seed v1 lexicon loader + DialectMapper integration."""

from __future__ import annotations

import json
import os
from pathlib import Path
from unittest.mock import patch

import pytest

from sf_ai.core.nlp.dialect_mapper import DialectMapper
from sf_ai.datasets.saudi_seed import (
    SAUDI_SEED_JSONL,
    SaudiSeedEntry,
    SaudiSeedSafety,
    attribution_block,
    iter_saudi_seed_entries,
    load_saudi_seed,
    saudi_seed_stats,
)


# ---------- real file: structure + counts ----------

def _skip_without_real_seed() -> None:
    if not SAUDI_SEED_JSONL.exists():
        pytest.skip("private Saudi seed payload is not committed to public repo")


def test_real_file_exists_at_expected_path() -> None:
    _skip_without_real_seed()
    assert SAUDI_SEED_JSONL.exists(), "Saudi seed JSONL not placed at expected path"


def test_real_file_loads_516_entries() -> None:
    _skip_without_real_seed()
    all_entries = list(iter_saudi_seed_entries())
    assert len(all_entries) == 516


def test_real_file_stats_match_validation_summary() -> None:
    _skip_without_real_seed()
    stats = saudi_seed_stats()
    assert stats.entries_total == 516
    # validation_summary.json reports high=441 — runtime-safe is a subset of that.
    assert stats.by_confidence.get("high") == 441
    assert stats.by_confidence.get("medium") == 69
    assert stats.by_confidence.get("low") == 6
    assert stats.sensitive_count == 3


def test_safe_runtime_subset_excludes_sensitive_and_lowconf() -> None:
    _skip_without_real_seed()
    safe = load_saudi_seed(safe_only=True)
    assert all(e.confidence == "high" for e in safe)
    assert all(not e.safety.sensitive_or_profane for e in safe)
    assert all(not e.requires_native_review for e in safe)
    assert all(e.safety.allow_for_generation for e in safe)


def test_full_load_returns_all_entries() -> None:
    _skip_without_real_seed()
    full = load_saudi_seed(safe_only=False)
    assert len(full) == 516


# ---------- entry shape ----------

def test_entry_has_expected_fields() -> None:
    _skip_without_real_seed()
    e = next(iter_saudi_seed_entries())
    assert isinstance(e, SaudiSeedEntry)
    assert e.term
    assert e.normalized_term
    assert isinstance(e.variants, tuple)
    assert isinstance(e.dialect_labels, tuple)
    assert isinstance(e.safety, SaudiSeedSafety)
    assert e.source_basis  # source_basis must be present


def test_entry_primary_dialect_falls_back_to_general() -> None:
    e = SaudiSeedEntry(
        id="x", term="t", normalized_term="t", variants=(), kind="", category="",
        dialect_labels=(), dialect_names_ar=(), used_in_places=(),
        meaning_msa="", example_saudi="", register="", dialectality="",
        confidence="low", requires_native_review=False,
        safety=SaudiSeedSafety(), source_basis="x",
    )
    assert e.primary_dialect == "saudi_general"


def test_is_safe_for_runtime_logic() -> None:
    base_kwargs = dict(
        id="x", term="t", normalized_term="t", variants=(), kind="", category="",
        dialect_labels=(), dialect_names_ar=(), used_in_places=(),
        meaning_msa="", example_saudi="", register="", dialectality="",
        requires_native_review=False, source_basis="x",
    )
    safe = SaudiSeedEntry(
        confidence="high", safety=SaudiSeedSafety(), **base_kwargs
    )
    assert safe.is_safe_for_runtime() is True

    low = SaudiSeedEntry(
        confidence="low", safety=SaudiSeedSafety(), **base_kwargs
    )
    assert low.is_safe_for_runtime() is False

    sensitive = SaudiSeedEntry(
        confidence="high",
        safety=SaudiSeedSafety(sensitive_or_profane=True), **base_kwargs
    )
    assert sensitive.is_safe_for_runtime() is False

    needs_review = SaudiSeedEntry(
        confidence="high", safety=SaudiSeedSafety(),
        **{**base_kwargs, "requires_native_review": True},
    )
    assert needs_review.is_safe_for_runtime() is False


# ---------- loader robustness ----------

def test_loader_skips_malformed_lines(tmp_path: Path) -> None:
    p = tmp_path / "x.jsonl"
    p.write_text(
        json.dumps({
            "id": "1", "term": "كلمة", "normalized_term": "كلمة",
            "confidence": "high",
            "safety": {"sensitive_or_profane": False, "allow_for_generation": True,
                       "recommended_use": []},
        }, ensure_ascii=False) + "\n"
        + "not-json\n"
        + json.dumps({"id": "2"}, ensure_ascii=False) + "\n"  # missing term
        + json.dumps({
            "id": "3", "term": "اخرى", "normalized_term": "اخرى",
            "confidence": "low",
            "safety": {"sensitive_or_profane": False, "allow_for_generation": True,
                       "recommended_use": []},
        }, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    full = load_saudi_seed(p, safe_only=False)
    assert {e.id for e in full} == {"1", "3"}
    safe = load_saudi_seed(p, safe_only=True)
    assert {e.id for e in safe} == {"1"}


def test_loader_returns_nothing_when_file_missing(tmp_path: Path) -> None:
    assert load_saudi_seed(tmp_path / "no_such_file.jsonl") == []


def test_attribution_block_mentions_origin() -> None:
    block = attribution_block()
    assert "saudi_dialect_lexicon_full_seed_v1" in block
    assert "غير منسوخ من Mo3jam" in block


# ---------- DialectMapper integration ----------

def test_dialect_mapper_ignores_saudi_seed_by_default(tmp_path: Path) -> None:
    fake = tmp_path / "seed.jsonl"
    fake.write_text(
        json.dumps({
            "id": "1", "term": "كلمه_تجريبيه_خاصه_بالاختبار_فقط",
            "normalized_term": "كلمه_تجريبيه_خاصه_بالاختبار_فقط",
            "meaning_msa": "تجربة",
            "confidence": "high",
            "safety": {"sensitive_or_profane": False, "allow_for_generation": True,
                       "recommended_use": []},
            "source_basis": "x",
        }, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    with patch.dict(os.environ, {}, clear=False):
        os.environ.pop("ENABLE_SAUDI_SEED_V1_LEXICON", None)
        os.environ.pop("ENABLE_MO3JAM_SAUDI_LEXICON", None)
        mapper = DialectMapper(saudi_seed_path=fake)
    out, signals = mapper.map_text("كلمه_تجريبيه_خاصه_بالاختبار_فقط")
    assert all(s.dialect != "saudi" for s in signals)


def test_dialect_mapper_loads_saudi_seed_when_flag_set(tmp_path: Path) -> None:
    fake = tmp_path / "seed.jsonl"
    fake.write_text(
        json.dumps({
            "id": "1", "term": "ابغى_تجربه",
            "normalized_term": "ابغى_تجربه",
            "meaning_msa": "اريد تجربة",
            "confidence": "high",
            "safety": {"sensitive_or_profane": False, "allow_for_generation": True,
                       "recommended_use": []},
            "source_basis": "x",
        }, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    with patch.dict(os.environ, {"ENABLE_SAUDI_SEED_V1_LEXICON": "true"}, clear=False):
        os.environ.pop("ENABLE_MO3JAM_SAUDI_LEXICON", None)
        mapper = DialectMapper(saudi_seed_path=fake)
    out, signals = mapper.map_text("ابغى_تجربه")
    assert any(s.dialect == "saudi" for s in signals)
    assert "اريد تجربة" in out


def test_dialect_mapper_real_seed_when_flag_set() -> None:
    """Loads the real file and verifies a Saudi-exclusive term yields a saudi signal."""
    _skip_without_real_seed()
    with patch.dict(os.environ, {"ENABLE_SAUDI_SEED_V1_LEXICON": "true"}, clear=False):
        os.environ.pop("ENABLE_MO3JAM_SAUDI_LEXICON", None)
        mapper = DialectMapper()
    # "ترى" is exclusively in the Saudi seed (not in baseline gulf/egyptian/
    # levantine/iraqi lexicons), so the saudi signal must surface.
    out, signals = mapper.map_text("ترى يا اخوي")
    assert any(s.dialect == "saudi" for s in signals)


def test_dialect_mapper_survives_missing_saudi_seed_file(tmp_path: Path) -> None:
    with patch.dict(os.environ, {"ENABLE_SAUDI_SEED_V1_LEXICON": "true"}, clear=False):
        mapper = DialectMapper(saudi_seed_path=tmp_path / "no_such.jsonl")
    # Mapper still works with baseline lexicons.
    out, signals = mapper.map_text("شلونك")
    assert "كيف حالك" in out or signals
