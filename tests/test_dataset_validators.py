"""Phase 5 — dataset schemas, validators, cleaners, loaders, ChatDataset."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from sf_ai.datasets import (
    ChatDataset,
    ChatMessage,
    SampleCleaner,
    SimpleSample,
    StructuredSample,
    iter_chat_samples,
    iter_jsonl,
    parse_record,
    validate_jsonl_file,
    validate_record,
)


# ---------- schemas ----------

def test_chat_message_roles() -> None:
    ChatMessage(role="user", content="مرحبا")
    ChatMessage(role="assistant", content="أهلا")
    ChatMessage(role="system", content="hi")
    with pytest.raises(ValidationError):
        ChatMessage(role="bot", content="x")


def test_chat_message_rejects_empty_content() -> None:
    with pytest.raises(ValidationError):
        ChatMessage(role="user", content="")


def test_structured_sample_valid() -> None:
    sample = StructuredSample(
        domain="chat",
        lang="ar",
        messages=[
            ChatMessage(role="user", content="مرحبا"),
            ChatMessage(role="assistant", content="أهلاً"),
        ],
    )
    assert sample.lang == "ar"
    assert len(sample.messages) == 2


def test_structured_sample_invalid_lang() -> None:
    with pytest.raises(ValidationError):
        StructuredSample(
            lang="zz",
            messages=[ChatMessage(role="user", content="x")],
        )


def test_structured_sample_requires_messages() -> None:
    with pytest.raises(ValidationError):
        StructuredSample(messages=[])


def test_simple_sample_parses_role_markers() -> None:
    sample = SimpleSample(text="المستخدم: مرحبا\nالمساعد: أهلاً")
    msgs = sample.to_messages()
    assert len(msgs) == 2
    assert msgs[0].role == "user"
    assert msgs[0].content == "مرحبا"
    assert msgs[1].role == "assistant"
    assert msgs[1].content == "أهلاً"


def test_simple_sample_english_markers() -> None:
    sample = SimpleSample(text="USER: hello\nASSISTANT: hi there")
    msgs = sample.to_messages()
    assert [m.role for m in msgs] == ["user", "assistant"]


def test_simple_sample_no_marker_wraps_as_user() -> None:
    sample = SimpleSample(text="just plain text")
    msgs = sample.to_messages()
    assert len(msgs) == 1
    assert msgs[0].role == "user"


def test_parse_record_picks_correct_type() -> None:
    s = parse_record({"text": "hi"})
    assert isinstance(s, SimpleSample)
    s2 = parse_record({"messages": [{"role": "user", "content": "hi"}]})
    assert isinstance(s2, StructuredSample)


def test_parse_record_rejects_garbage() -> None:
    with pytest.raises(ValueError):
        parse_record({"foo": "bar"})
    with pytest.raises(ValueError):
        parse_record([1, 2, 3])  # type: ignore[arg-type]


# ---------- validators ----------

def test_validate_record_returns_none_on_valid() -> None:
    issue = validate_record({"text": "hi"}, line_number=1)
    assert issue is None


def test_validate_record_returns_issue_on_bad_schema() -> None:
    issue = validate_record({"messages": []}, line_number=3)
    assert issue is not None
    assert issue.line_number == 3
    assert issue.kind == "schema"


def test_validate_jsonl_file_missing(tmp_path: Path) -> None:
    report = validate_jsonl_file(tmp_path / "nope.jsonl")
    assert report.error_count == 1
    assert report.issues[0].kind == "encoding"


def test_validate_jsonl_file_clean(tmp_path: Path) -> None:
    f = tmp_path / "ok.jsonl"
    f.write_text(
        '{"text":"hello"}\n'
        '{"messages":[{"role":"user","content":"x"},{"role":"assistant","content":"y"}]}\n',
        encoding="utf-8",
    )
    report = validate_jsonl_file(f)
    assert report.is_clean
    assert report.total_lines == 2
    assert report.valid_samples == 2


def test_validate_jsonl_file_mixed(tmp_path: Path) -> None:
    f = tmp_path / "mix.jsonl"
    f.write_text(
        '{"text":"hi"}\n'
        'not json at all\n'
        '\n'
        '{"messages":[]}\n'
        '{"messages":[{"role":"bot","content":"x"}]}\n',
        encoding="utf-8",
    )
    report = validate_jsonl_file(f)
    assert report.total_lines == 4   # blank line skipped
    assert report.valid_samples == 1  # only the first one is valid
    kinds = {i.kind for i in report.issues}
    assert "json" in kinds
    assert "schema" in kinds


# ---------- loaders ----------

def test_iter_jsonl_skips_blank_and_bad(tmp_path: Path) -> None:
    f = tmp_path / "x.jsonl"
    f.write_text('{"text":"a"}\n\nNOT JSON\n{"text":"b"}\n', encoding="utf-8")
    out = list(iter_jsonl(f))
    assert [r["text"] for r in out] == ["a", "b"]


def test_iter_jsonl_strict_raises(tmp_path: Path) -> None:
    f = tmp_path / "x.jsonl"
    f.write_text('not json\n', encoding="utf-8")
    with pytest.raises(ValueError):
        list(iter_jsonl(f, strict=True))


def test_iter_chat_samples_yields_models(tmp_path: Path) -> None:
    f = tmp_path / "x.jsonl"
    f.write_text(
        '{"text":"hi"}\n'
        '{"messages":[{"role":"user","content":"x"}]}\n',
        encoding="utf-8",
    )
    samples = list(iter_chat_samples(f))
    assert isinstance(samples[0], SimpleSample)
    assert isinstance(samples[1], StructuredSample)


def test_iter_chat_samples_skips_invalid(tmp_path: Path) -> None:
    f = tmp_path / "x.jsonl"
    f.write_text(
        '{"text":"ok"}\n'
        '{"foo":"bar"}\n'
        '{"messages":[{"role":"user","content":"x"}]}\n',
        encoding="utf-8",
    )
    samples = list(iter_chat_samples(f))
    assert len(samples) == 2


# ---------- cleaners ----------

def test_cleaner_preserves_code() -> None:
    c = SampleCleaner()
    msg = ChatMessage(role="user", content="def f(x): return {y: x + 1}")
    out = c.clean_message(msg)
    assert out.content == msg.content


def test_cleaner_strips_control_chars() -> None:
    c = SampleCleaner()
    msg = ChatMessage(role="user", content="ab\x00cd")
    out = c.clean_message(msg)
    assert out.content == "abcd"


def test_cleaner_normalize_option() -> None:
    c = SampleCleaner(normalize=True)
    msg = ChatMessage(role="user", content="مَرْحَبًا")
    out = c.clean_message(msg)
    assert out.content == "مرحبا"


def test_cleaner_drops_emptied_messages_in_structured() -> None:
    c = SampleCleaner()
    sample = StructuredSample(
        messages=[
            ChatMessage(role="user", content="hi"),
            ChatMessage(role="assistant", content="\x00\x00"),  # becomes empty
        ],
    )
    out = c.clean_structured(sample)
    assert len(out.messages) == 1
    assert out.messages[0].role == "user"


def test_cleaner_raises_when_all_empty() -> None:
    c = SampleCleaner()
    sample = StructuredSample(
        messages=[ChatMessage(role="user", content="\x00")],
    )
    with pytest.raises(ValueError):
        c.clean_structured(sample)


# ---------- ChatDataset ----------

def test_chat_dataset_discovers_files(tmp_path: Path) -> None:
    (tmp_path / "a.jsonl").write_text('{"text":"x"}\n', encoding="utf-8")
    (tmp_path / "sub").mkdir()
    (tmp_path / "sub" / "b.jsonl").write_text('{"text":"y"}\n', encoding="utf-8")
    ds = ChatDataset(root=tmp_path)
    files = ds.jsonl_files()
    assert len(files) == 2


def test_chat_dataset_stats(tmp_path: Path) -> None:
    f = tmp_path / "x.jsonl"
    f.write_text(
        '{"messages":[{"role":"user","content":"hi"},{"role":"assistant","content":"hello there"}]}\n'
        '{"text":"المستخدم: مرحبا\\nالمساعد: أهلا"}\n',
        encoding="utf-8",
    )
    ds = ChatDataset(root=tmp_path)
    stats = ds.stats()
    assert stats.files == 1
    assert stats.valid_samples == 2
    assert stats.user_messages == 2
    assert stats.assistant_messages == 2
    assert stats.total_chars > 0


def test_chat_dataset_iter_messages_streams(tmp_path: Path) -> None:
    f = tmp_path / "x.jsonl"
    f.write_text(
        '{"messages":[{"role":"user","content":"a"},{"role":"assistant","content":"b"}]}\n',
        encoding="utf-8",
    )
    ds = ChatDataset(root=tmp_path)
    msgs = list(ds.iter_messages())
    assert [m.role for m in msgs] == ["user", "assistant"]
    assert [m.content for m in msgs] == ["a", "b"]


def test_real_corpus_dir_contains_only_explicit_reviewed_seeds() -> None:
    # Sanity: corpus content must be explicit and reviewed, not auto-filled.
    corpus = Path(__file__).resolve().parent.parent / "data" / "corpus" / "chat"
    assert corpus.exists()
    jsonl_files = sorted((corpus / "jsonl").glob("*.jsonl"))
    raw_files = list((corpus / "raw").glob("*.jsonl"))
    assert [p.name for p in jsonl_files] == [
        "dialogue_batch_v2_msa_001.jsonl",
        "dialogue_batch_v2_msa_002.jsonl",
        "dialogue_batch_v2_msa_003.jsonl",
        "dialogue_batch_v2_msa_004.jsonl",
        "dialogue_batch_v2_msa_005.jsonl",
        "dialogue_batch_v2_msa_006.jsonl",
        "first_dialogue_seed.jsonl",
        "protected_terms_msa_seed_v1.jsonl",
        "protected_terms_seed_v1.jsonl",
    ]
    assert raw_files == []
