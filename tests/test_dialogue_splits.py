"""Phase 27.7 — deterministic dialogue train/eval split."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

torch = pytest.importorskip("torch")

from sf_ai.datasets import ChatDataset  # noqa: E402
from sf_ai.datasets.splits import assign_split, write_split_manifest  # noqa: E402
from sf_ai.models.tokenizer import CharTokenizer  # noqa: E402
from sf_ai.training.train_tiny_lm import iter_token_batches  # noqa: E402


def _record(text: str, dialect: str = "msa") -> str:
    return json.dumps(
        {
            "domain": "chat",
            "lang": "ar",
            "messages": [
                {"role": "user", "content": f"سؤال {text}"},
                {"role": "assistant", "content": f"جواب {text}"},
            ],
            "provenance": {
                "source": "sf-ai-natural-dialogue-msa",
                "license": "owner-approved-for-sf-ai-training",
                "language": "ar",
                "dialect": dialect,
                "quality": "gold",
                "training_allowed": True,
                "owner_user_id": "sami-local",
                "created_by_user_id": "sf-ai-local-author",
                "target_user_id": "sami-local",
                "user_scope": "single_user",
            },
        },
        ensure_ascii=False,
    )


def test_assign_split_is_stable() -> None:
    line = _record("واحد")
    assert assign_split(line, salt="x") == assign_split(line, salt="x")


def test_write_split_manifest_counts_records(tmp_path: Path) -> None:
    corpus = tmp_path / "corpus"
    corpus.mkdir()
    (corpus / "x.jsonl").write_text(
        "\n".join(_record(str(i), "saudi" if i % 2 else "msa") for i in range(20)) + "\n",
        encoding="utf-8",
    )
    out = tmp_path / "split.json"
    manifest = write_split_manifest(corpus, out, eval_ratio=0.25, salt="unit-test")

    assert out.exists()
    assert manifest["total_records"] == 20
    assert manifest["counts"]["train"] + manifest["counts"].get("eval", 0) == 20
    assert set(manifest["dialects"]) <= {"train", "eval"}


def test_iter_token_batches_uses_eval_split(tmp_path: Path) -> None:
    corpus = tmp_path / "corpus"
    corpus.mkdir()
    (corpus / "x.jsonl").write_text(
        "\n".join(_record(str(i)) for i in range(12)) + "\n",
        encoding="utf-8",
    )
    split = tmp_path / "split.json"
    write_split_manifest(corpus, split, eval_ratio=0.95, salt="unit-test")

    ds = ChatDataset(corpus)
    tok = CharTokenizer()
    tok.train(ds.iter_dialogue_texts())
    batches = list(
        iter_token_batches(
            tok,
            ds,
            batch_size=1,
            seq_len=10,
            device=torch.device("cpu"),
            stream_format="dialogue",
            loss_scope="assistant",
            split_manifest=split,
            split_name="eval",
        )
    )

    assert batches
