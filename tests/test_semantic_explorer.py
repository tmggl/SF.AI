"""Phase 2 — SemanticExplorer + primitives."""

from __future__ import annotations

import math

from sf_ai.core.semantic import (
    HashingVectorizer,
    SemanticExplorer,
    cosine_sparse,
    jaccard,
    normalized_simple,
    overlap_count,
    simple_tokenize,
)


def test_normalized_simple_basic() -> None:
    assert normalized_simple("  Hello,   World!  ") == "hello world"
    assert normalized_simple("مرحبا، كيف الحال؟") == "مرحبا كيف الحال"


def test_simple_tokenize() -> None:
    assert simple_tokenize("") == []
    assert simple_tokenize("hello world") == ["hello", "world"]
    assert simple_tokenize("مرحبا كيف الحال") == ["مرحبا", "كيف", "الحال"]


def test_overlap_count() -> None:
    assert overlap_count(["a", "b", "c"], ["b", "d"]) == 1
    assert overlap_count(["a", "a", "b"], ["a", "a"]) == 2
    assert overlap_count([], ["x"]) == 0


def test_jaccard() -> None:
    assert jaccard(["a", "b"], ["a", "b"]) == 1.0
    assert jaccard(["a", "b"], ["c", "d"]) == 0.0
    # intersection {a} = 1, union {a,b,c,x} = 4 → 0.25.
    assert math.isclose(jaccard(["a", "b", "c"], ["a", "x"]), 0.25)


def test_hashing_vectorizer_deterministic() -> None:
    hv = HashingVectorizer(buckets=128)
    v1 = hv.transform("مرحبا كيف")
    v2 = hv.transform("مرحبا كيف")
    assert v1 == v2
    # Same tokens, different order → same vector.
    v3 = hv.transform("كيف مرحبا")
    assert v1 == v3


def test_cosine_sparse_identity_and_empty() -> None:
    hv = HashingVectorizer(buckets=128)
    v = hv.transform("hello world hello")
    assert math.isclose(cosine_sparse(v, v), 1.0)
    assert cosine_sparse({}, v) == 0.0


def test_semantic_explorer_phrase_match() -> None:
    explorer = SemanticExplorer()
    match = explorer.score_candidate("مرحبا كيف حالك اليوم", "كيف حالك")
    assert match is not None
    assert match.signal == "phrase"
    assert match.score == 1.0


def test_semantic_explorer_fuzzy_match() -> None:
    explorer = SemanticExplorer()
    # Drop a letter to force fuzzy rather than exact phrase.
    match = explorer.score_candidate("كيف حالكم اليوم؟", "كيف حالك")
    assert match.score > 0.0


def test_semantic_explorer_best_match_picks_top() -> None:
    explorer = SemanticExplorer()
    best = explorer.best_match("مرحبا كيف حالك", ["وداعا", "كيف حالك", "ماذا تفعل"])
    assert best is not None
    assert best.candidate == "كيف حالك"
    assert best.signal == "phrase"


def test_semantic_explorer_no_match_returns_none() -> None:
    explorer = SemanticExplorer()
    best = explorer.best_match("zzzzzz qqqqqq", ["completely-different-text-xyz"])
    assert best is None
