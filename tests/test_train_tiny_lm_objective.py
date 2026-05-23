"""Phase 27.6 — assistant-target training objective tests."""

from __future__ import annotations

from pathlib import Path

import pytest

torch = pytest.importorskip("torch")

from sf_ai.datasets import ChatDataset  # noqa: E402
from sf_ai.models.tokenizer import CharTokenizer  # noqa: E402
from sf_ai.training.train_tiny_lm import (  # noqa: E402
    _encode_assistant_target_dialogue,
    iter_token_batches,
)


def test_assistant_target_masks_user_and_role_markers() -> None:
    text = "المستخدم: مرحبا\nالمساعد: أهلا"
    tok = CharTokenizer()
    tok.train([text, text])

    ids, labels = _encode_assistant_target_dialogue(tok, text)

    assert len(ids) == len(labels)
    learned = [token for token in labels if token != -100]
    ignored = [token for token in labels if token == -100]
    assert ignored
    assert tok.decode(learned) == "أهلا"


def test_iter_token_batches_assistant_scope_uses_ignore_index(tmp_path: Path) -> None:
    corpus_file = tmp_path / "x.jsonl"
    corpus_file.write_text(
        '{"messages":[{"role":"user","content":"مرحبا"},'
        '{"role":"assistant","content":"أهلا وسهلا بك"}]}\n'
        '{"messages":[{"role":"user","content":"كيفك"},'
        '{"role":"assistant","content":"بخير الحمد لله"}]}\n',
        encoding="utf-8",
    )
    ds = ChatDataset(root=tmp_path)
    tok = CharTokenizer()
    tok.train(ds.iter_dialogue_texts())

    batches = list(
        iter_token_batches(
            tok,
            ds,
            batch_size=1,
            seq_len=12,
            device=torch.device("cpu"),
            stream_format="dialogue",
            loss_scope="assistant",
        )
    )

    assert batches
    inputs, targets = batches[0]
    assert inputs.shape == targets.shape == (1, 12)
    assert (targets == -100).any()
    assert (targets != -100).any()
