"""Phase 5.5 — CharTokenizer + BPETokenizer + sovereign training."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from sf_ai.models.tokenizer import (
    BPETokenizer,
    CharTokenizer,
    TokenizerConfig,
    train_bpe_from_corpus,
)


# ---------- TokenizerConfig ----------

def test_config_rejects_undersized_vocab() -> None:
    with pytest.raises(ValueError):
        TokenizerConfig(vocab_size=2)  # less than special tokens


def test_config_rejects_zero_min_freq() -> None:
    with pytest.raises(ValueError):
        TokenizerConfig(min_frequency=0)


# ---------- CharTokenizer ----------

def test_char_tokenizer_trains_and_encodes() -> None:
    tok = CharTokenizer(config=TokenizerConfig(vocab_size=64, min_frequency=1))
    tok.train(["hello", "world", "مرحبا"])
    # Special tokens registered.
    assert "<pad>" in tok.vocab
    assert "<unk>" in tok.vocab
    # Round-trip.
    ids = tok.encode("hello")
    assert tok.decode(ids) == "hello"


def test_char_tokenizer_handles_unknown_chars() -> None:
    tok = CharTokenizer(config=TokenizerConfig(vocab_size=32, min_frequency=1))
    tok.train(["abc"])
    ids = tok.encode("abz")
    # 'z' is unknown → maps to unk.
    assert ids[-1] == tok.unk_id()


def test_char_tokenizer_save_load_roundtrip(tmp_path: Path) -> None:
    tok = CharTokenizer(config=TokenizerConfig(vocab_size=64, min_frequency=1))
    tok.train(["مرحبا كيف الحال", "hello world"])
    out = tmp_path / "char"
    tok.save(out)
    loaded = CharTokenizer.load(out)
    assert loaded.vocab == tok.vocab


def test_char_tokenizer_refuses_non_sovereign(tmp_path: Path) -> None:
    out = tmp_path / "char_bad"
    out.mkdir()
    (out / "vocab.json").write_text('{"a":0}', encoding="utf-8")
    (out / "meta.json").write_text('{"sf_origin": false}', encoding="utf-8")
    with pytest.raises(ValueError):
        CharTokenizer.load(out)


# ---------- BPETokenizer ----------

def test_bpe_trains_and_learns_merges() -> None:
    cfg = TokenizerConfig(vocab_size=128, min_frequency=1)
    tok = BPETokenizer(config=cfg)
    # "ab" should be merged because it co-occurs frequently.
    stats = tok.train(["abab abab abab", "ab ab ab"])
    assert stats.merges_learned > 0
    assert tok.stats is not None
    # Vocab includes specials + base alphabet + merges.
    assert "<unk>" in tok.vocab
    assert "</w>" in tok.vocab


def test_bpe_encode_decode_roundtrip_arabic() -> None:
    cfg = TokenizerConfig(vocab_size=300, min_frequency=1)
    tok = BPETokenizer(config=cfg)
    tok.train(
        [
            "مرحبا كيف الحال",
            "مرحبا كيف الحال",
            "اهلا اهلا",
            "كيف حالك اليوم",
        ]
    )
    text = "مرحبا كيف"
    ids = tok.encode(text)
    decoded = tok.decode(ids)
    assert decoded.replace(" ", "") == text.replace(" ", "")


def test_bpe_protected_phrase_roundtrip_single_piece() -> None:
    cfg = TokenizerConfig(
        vocab_size=300,
        min_frequency=1,
        protected_terms=("وعليكم السلام", "نشتغل سوا"),
    )
    tok = BPETokenizer(config=cfg)
    tok.train(
        [
            "وعليكم السلام أهلًا بك",
            "نشتغل سوا ونخفف الحمل",
        ]
    )

    ids = tok.encode("وعليكم السلام")
    assert len(ids) == 1
    assert tok.decode(ids) == "وعليكم السلام"

    text = "نشتغل سوا"
    assert tok.decode(tok.encode(text)) == text


def test_bpe_decode_keeps_boundary_after_protected_phrase() -> None:
    tok = BPETokenizer(
        config=TokenizerConfig(
            vocab_size=300,
            min_frequency=1,
            protected_terms=("نشتغل سوا",),
        )
    )
    tok.train(["نشتغل سوا ونخفف الحمل"])

    ids = tok.encode("نشتغل سوا") + tok.encode("ونخفف الحمل")
    assert tok.decode(ids) == "نشتغل سوا ونخفف الحمل"


def test_bpe_save_load_roundtrip(tmp_path: Path) -> None:
    cfg = TokenizerConfig(vocab_size=200, min_frequency=1)
    tok = BPETokenizer(config=cfg)
    tok.train(["the quick brown fox", "the lazy dog", "fox and dog"])
    out = tmp_path / "bpe"
    tok.save(out)
    # Files exist.
    assert (out / "vocab.json").exists()
    assert (out / "merges.txt").exists()
    meta = json.loads((out / "meta.json").read_text(encoding="utf-8"))
    assert meta["sf_origin"] is True
    assert meta["tokenizer_type"] == "bpe"
    # Reload and verify identity on a known string.
    loaded = BPETokenizer.load(out)
    a = tok.encode("the fox")
    b = loaded.encode("the fox")
    assert a == b


def test_bpe_save_load_preserves_protected_phrases(tmp_path: Path) -> None:
    tok = BPETokenizer(
        config=TokenizerConfig(
            vocab_size=300,
            min_frequency=1,
            protected_terms=("القراءة تفيد",),
        )
    )
    tok.train(["القراءة تفيد وتزيد المفردات"])
    out = tmp_path / "bpe_protected"
    tok.save(out)

    meta = json.loads((out / "meta.json").read_text(encoding="utf-8"))
    assert meta["protected_terms"] == ["القراءة تفيد"]

    loaded = BPETokenizer.load(out)
    ids = loaded.encode("القراءة تفيد")
    assert len(ids) == 1
    assert loaded.decode(ids) == "القراءة تفيد"



def test_bpe_refuses_non_sovereign_load(tmp_path: Path) -> None:
    out = tmp_path / "bpe_bad"
    out.mkdir()
    (out / "vocab.json").write_text("{}", encoding="utf-8")
    (out / "merges.txt").write_text("", encoding="utf-8")
    (out / "meta.json").write_text('{"sf_origin": false}', encoding="utf-8")
    with pytest.raises(ValueError):
        BPETokenizer.load(out)


def test_bpe_refuses_load_without_meta(tmp_path: Path) -> None:
    out = tmp_path / "bpe_no_meta"
    out.mkdir()
    (out / "vocab.json").write_text("{}", encoding="utf-8")
    with pytest.raises(ValueError):
        BPETokenizer.load(out)


# ---------- train_bpe_from_corpus ----------

def test_train_from_empty_corpus_refuses(tmp_path: Path) -> None:
    corpus = tmp_path / "corpus"
    corpus.mkdir()
    with pytest.raises(ValueError):
        train_bpe_from_corpus(
            corpus_root=corpus,
            output_dir=tmp_path / "out",
            config=TokenizerConfig(vocab_size=128, min_frequency=1),
        )


def test_train_from_corpus_writes_artifacts(tmp_path: Path) -> None:
    corpus = tmp_path / "corpus"
    corpus.mkdir()
    sample = corpus / "a.jsonl"
    sample.write_text(
        '{"messages":[{"role":"user","content":"مرحبا كيف الحال"},'
        '{"role":"assistant","content":"اهلا"}]}\n'
        '{"text":"المستخدم: السلام عليكم\\nالمساعد: وعليكم السلام"}\n',
        encoding="utf-8",
    )

    out = tmp_path / "out"
    tok = train_bpe_from_corpus(
        corpus_root=corpus,
        output_dir=out,
        config=TokenizerConfig(vocab_size=256, min_frequency=1),
    )
    assert len(tok) > 0
    assert (out / "meta.json").exists()
    meta = json.loads((out / "meta.json").read_text(encoding="utf-8"))
    assert meta["sf_origin"] is True
    # Provenance: source files hashed.
    sources = meta.get("training_meta", {}).get("source_files", [])
    assert len(sources) == 1
    assert sources[0]["blake2b_16"]
