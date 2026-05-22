"""Phase 3 — DialectMapper + ArabiziMapper."""

from __future__ import annotations

from sf_ai.core.nlp import ArabiziMapper, DialectMapper


def test_dialect_maps_saudi_to_canonical() -> None:
    dm = DialectMapper()
    out, signals = dm.map_text("شلونك اخوي")
    assert "كيف حالك" in out
    assert any(s.dialect == "saudi" and s.surface == "شلونك" for s in signals)


def test_wider_dialects_are_disabled_by_default() -> None:
    dm = DialectMapper()
    out, signals = dm.map_text("ازيك يا صاحبي")
    assert out == "ازيك يا صاحبي"
    assert signals == ()


def test_dialect_no_match_returns_original() -> None:
    dm = DialectMapper()
    out, signals = dm.map_text("نص عادي تماما")
    assert out == "نص عادي تماما"
    assert signals == ()


def test_dialect_detect_picks_strongest_signal() -> None:
    dm = DialectMapper()
    _, signals = dm.map_text("شلونك")
    label = dm.detect_dialect(signals)
    assert label == "saudi"


def test_arabizi_rewrites_known_tokens() -> None:
    am = ArabiziMapper()
    out, signals = am.transform("shlon halak")
    assert "شلون" in out
    assert any(s.surface.lower() == "shlon" for s in signals)


def test_arabizi_protects_programming_terms() -> None:
    am = ArabiziMapper()
    out, signals = am.transform("ابي python و docker")
    assert "python" in out
    assert "docker" in out
    assert all(s.surface.lower() not in {"python", "docker"} for s in signals)


def test_arabizi_does_not_touch_arabic_text() -> None:
    am = ArabiziMapper()
    out, signals = am.transform("مرحبا كيف الحال")
    assert out == "مرحبا كيف الحال"
    assert signals == ()
