"""Phase 3.5 — Mo3jam Saudi-dialect importer.

These tests never hit the network. They use synthetic HTML fixtures in
tests/fixtures/ that mirror the structure observed on the source.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from unittest.mock import patch

import pytest

from sf_ai.core.nlp.dialect_mapper import DialectMapper
from sf_ai.datasets.dialects import (
    DialectLexiconMeta,
    build_dialect_yaml,
    load_dialect_yaml,
)
from sf_ai.tools.web.mo3jam_importer import (
    EXPECTED_TERMS,
    Mo3jamImportConfig,
    Mo3jamImporter,
    SOURCE_NAME,
    SOURCE_ROOT,
    normalize_arabic_term,
    parse_listing_html,
    parse_term_html,
)

FIXTURES = Path(__file__).resolve().parent / "fixtures"


# ---------- helpers ----------

def _cfg(tmp_path: Path, **overrides) -> Mo3jamImportConfig:  # type: ignore[no-untyped-def]
    base = dict(
        output_jsonl=tmp_path / "out.jsonl",
        raw_dir=tmp_path / "raw",
        report_path=tmp_path / "report.md",
        failed_urls_path=tmp_path / "failed.txt",
        rate_limit_seconds=0.0,
        dry_run=True,
        user_permission_confirmed=False,
    )
    base.update(overrides)
    return Mo3jamImportConfig(**base)


# ---------- parsing ----------

def test_parse_listing_extracts_only_saudi_term_anchors() -> None:
    html = (FIXTURES / "mo3jam_listing_sample.html").read_text(encoding="utf-8")
    paths = parse_listing_html(html)
    assert "/term/اشلونك" in paths
    assert "/term/ابتل" in paths
    assert "/term/ابخص" in paths
    assert "/term/احلت" in paths
    # Egyptian and /about distractors must be filtered out.
    assert all("Egyptian" not in p for p in paths)
    assert "/about" not in paths


def test_parse_term_extracts_saudi_block() -> None:
    html = (FIXTURES / "mo3jam_term_sample.html").read_text(encoding="utf-8")
    rec = parse_term_html(
        html,
        term_hint="اشلونك",
        source_url="https://ar.mo3jam.com/term/اشلونك",
        letter="ا",
        raw_html_path="/tmp/x.html",
    )
    assert rec.term == "اشلونك"
    assert rec.normalized_term == normalize_arabic_term("اشلونك")
    assert "كيف حالك" in rec.definition
    assert "نجد" in rec.definition or "الشمال" in rec.definition
    # Definition must NOT carry the Egyptian dialect's text.
    assert "عامل ايه" not in rec.definition
    assert rec.usage_example
    assert "اخوي" in rec.usage_example
    assert rec.subdialect == "najdi"
    assert "شلونك" in rec.spelling_variants
    assert rec.source_name == SOURCE_NAME
    assert rec.source_url == "https://ar.mo3jam.com/term/اشلونك"
    assert rec.source_root == SOURCE_ROOT
    assert rec.credit_required is True
    assert rec.permission_status == "allowed_with_user_confirmed_permission"
    assert rec.parser_version
    assert rec.dialect == "saudi"


def test_parse_term_marks_warnings_when_no_saudi_block() -> None:
    html = "<html><body><h1>foo</h1></body></html>"
    rec = parse_term_html(
        html,
        term_hint="foo",
        source_url="https://ar.mo3jam.com/term/foo",
        letter="ف",
        raw_html_path="/tmp/x.html",
    )
    assert "saudi_block_not_found" in rec.parser_warnings


# ---------- importer config & sovereignty ----------

def test_live_mode_requires_confirmed_permission(tmp_path: Path) -> None:
    with pytest.raises(ValueError):
        Mo3jamImportConfig(
            output_jsonl=tmp_path / "x.jsonl",
            raw_dir=tmp_path,
            report_path=tmp_path / "r.md",
            failed_urls_path=tmp_path / "f.txt",
            dry_run=False,
            user_permission_confirmed=False,
        )


def test_dry_run_listing_does_no_network(tmp_path: Path) -> None:
    cfg = _cfg(tmp_path, dry_run=True)
    importer = Mo3jamImporter(cfg)
    pairs = importer.crawl_listing()
    assert pairs == []
    assert importer.report.letters_seen == len(cfg.letters)


# ---------- importer with stubbed fetcher (no network) ----------

class _StubFetcher:
    def __init__(self, pages: dict[str, str]) -> None:
        self.pages = pages
        self.calls: list[str] = []

    def get(self, url: str) -> str:
        self.calls.append(url)
        if url in self.pages:
            return self.pages[url]
        raise RuntimeError(f"unexpected url in test: {url}")


def test_live_crawl_with_stub_writes_jsonl_and_report(tmp_path: Path) -> None:
    listing_html = (FIXTURES / "mo3jam_listing_sample.html").read_text(encoding="utf-8")
    term_html = (FIXTURES / "mo3jam_term_sample.html").read_text(encoding="utf-8")

    # We only feed one letter and one term URL so the test runs fast.
    cfg = Mo3jamImportConfig(
        output_jsonl=tmp_path / "out.jsonl",
        raw_dir=tmp_path / "raw",
        report_path=tmp_path / "report.md",
        failed_urls_path=tmp_path / "failed.txt",
        rate_limit_seconds=0.0,
        dry_run=False,
        user_permission_confirmed=True,
        letters=("ا",),
        limit=1,
    )

    stub = _StubFetcher(
        pages={
            "https://ar.mo3jam.com/dialect/Saudi/all/%D8%A7": listing_html,
            "https://ar.mo3jam.com/term/اشلونك": term_html,
        }
    )
    importer = Mo3jamImporter(cfg, fetcher=stub)
    pairs = importer.crawl_listing()
    assert len(pairs) >= 1
    n = importer.crawl_terms(pairs[:1])
    assert n == 1

    # JSONL has one line, with required attribution.
    lines = cfg.output_jsonl.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1
    record = json.loads(lines[0])
    assert record["source_name"] == SOURCE_NAME
    assert record["source_url"].endswith("اشلونك")
    assert record["credit_required"] is True
    assert record["permission_status"] == "allowed_with_user_confirmed_permission"
    assert record["dialect"] == "saudi"

    importer.write_report()
    assert cfg.report_path.exists()
    report_md = cfg.report_path.read_text(encoding="utf-8")
    assert SOURCE_NAME in report_md
    assert SOURCE_ROOT in report_md
    assert "credit_required" not in report_md or "true" in report_md.lower()


def test_resume_skips_already_imported(tmp_path: Path) -> None:
    listing_html = (FIXTURES / "mo3jam_listing_sample.html").read_text(encoding="utf-8")
    term_html = (FIXTURES / "mo3jam_term_sample.html").read_text(encoding="utf-8")

    # Pre-populate JSONL with the term URL we're about to "crawl".
    out_path = tmp_path / "out.jsonl"
    out_path.write_text(
        json.dumps({
            "term": "اشلونك",
            "normalized_term": normalize_arabic_term("اشلونك"),
            "source_url": "https://ar.mo3jam.com/term/اشلونك",
        }, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    cfg = Mo3jamImportConfig(
        output_jsonl=out_path,
        raw_dir=tmp_path / "raw",
        report_path=tmp_path / "report.md",
        failed_urls_path=tmp_path / "failed.txt",
        rate_limit_seconds=0.0,
        dry_run=False,
        user_permission_confirmed=True,
        letters=("ا",),
        resume=True,
    )
    stub = _StubFetcher(
        pages={
            "https://ar.mo3jam.com/dialect/Saudi/all/%D8%A7": listing_html,
            "https://ar.mo3jam.com/term/اشلونك": term_html,
        }
    )
    importer = Mo3jamImporter(cfg, fetcher=stub)
    pairs = importer.crawl_listing()
    importer.crawl_terms(pairs)
    assert importer.report.duplicates_skipped >= 1


def test_expected_term_count_constant() -> None:
    assert EXPECTED_TERMS == 3139


# ---------- YAML builder ----------

def test_build_dialect_yaml_preserves_attribution(tmp_path: Path) -> None:
    jsonl = tmp_path / "in.jsonl"
    jsonl.write_text(
        json.dumps({
            "term": "اشلونك",
            "normalized_term": normalize_arabic_term("اشلونك"),
            "definition": "كيف حالك",
            "usage_example": "اشلونك يا اخوي",
            "spelling_variants": ["شلونك"],
            "dialect": "saudi",
            "subdialect": "najdi",
            "letter": "ا",
            "source_url": "https://ar.mo3jam.com/term/اشلونك",
        }, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    out_yaml = tmp_path / "lex.yaml"
    meta = DialectLexiconMeta(
        source_name=SOURCE_NAME,
        source_url=SOURCE_ROOT,
        permission_status="allowed_with_user_confirmed_permission",
        credit_required=True,
        expected_terms=EXPECTED_TERMS,
    )
    n = build_dialect_yaml(jsonl, out_yaml, meta=meta)
    assert n == 1
    meta_loaded, terms = load_dialect_yaml(out_yaml)
    assert meta_loaded.credit_required is True
    assert meta_loaded.source_name == SOURCE_NAME
    assert len(terms) == 1
    term = terms[0]
    assert term["training_allowed"] is False
    assert term["confidence"] == 1.0
    assert term["requires_credit"] is True
    assert "dialect_understanding" in term["use_for"]
    assert "user_text_normalization" in term["use_for"]


def test_yaml_loader_refuses_missing_credit(tmp_path: Path) -> None:
    bad = tmp_path / "bad.yaml"
    bad.write_text(
        "metadata: {source_name: x, source_url: y, credit_required: false}\nterms: []\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError):
        load_dialect_yaml(bad)


# ---------- DialectMapper integration ----------

def test_dialect_mapper_ignores_mo3jam_by_default(tmp_path: Path) -> None:
    # No env flag → mapper must not load the Mo3jam YAML even if it exists.
    mo3jam_yaml = tmp_path / "saudi.yaml"
    mo3jam_yaml.write_text(
        "metadata:\n  source_name: x\n  source_url: y\n"
        "  permission_status: allowed_with_user_confirmed_permission\n"
        "  credit_required: true\n  expected_terms: 1\n"
        "terms:\n  - term: 'مصطلح_تجريبي'\n    definition: 'تعريف'\n    confidence: 1.0\n",
        encoding="utf-8",
    )
    with patch.dict(os.environ, {}, clear=False):
        os.environ.pop("ENABLE_MO3JAM_SAUDI_LEXICON", None)
        mapper = DialectMapper(mo3jam_saudi_path=mo3jam_yaml)
    out, signals = mapper.map_text("مصطلح_تجريبي")
    # No Saudi-dialect signal expected because the lexicon is gated off.
    assert all(s.dialect != "saudi" for s in signals)


def test_dialect_mapper_loads_mo3jam_when_flag_set(tmp_path: Path) -> None:
    mo3jam_yaml = tmp_path / "saudi.yaml"
    mo3jam_yaml.write_text(
        "metadata:\n  source_name: مصدر\n  source_url: https://example\n"
        "  permission_status: allowed_with_user_confirmed_permission\n"
        "  credit_required: true\n  expected_terms: 1\n"
        "terms:\n  - term: 'مصطلح_تجريبي'\n    definition: 'تعريف'\n    confidence: 1.0\n",
        encoding="utf-8",
    )
    with patch.dict(os.environ, {"ENABLE_MO3JAM_SAUDI_LEXICON": "true"}, clear=False):
        mapper = DialectMapper(mo3jam_saudi_path=mo3jam_yaml)
    _, signals = mapper.map_text("مصطلح_تجريبي")
    assert any(s.dialect == "saudi" for s in signals)


def test_dialect_mapper_survives_missing_mo3jam_file(tmp_path: Path) -> None:
    # Flag on but file missing: must not raise.
    missing = tmp_path / "no_such_file.yaml"
    with patch.dict(os.environ, {"ENABLE_MO3JAM_SAUDI_LEXICON": "true"}, clear=False):
        mapper = DialectMapper(mo3jam_saudi_path=missing)
    # Mapper still works with the baseline lexicons.
    out, signals = mapper.map_text("شلونك")
    assert "كيف حالك" in out or signals  # gulf rewrite still happens
