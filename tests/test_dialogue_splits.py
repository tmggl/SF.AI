"""Phase 27.7 — deterministic dialogue train/eval split."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

torch = pytest.importorskip("torch")

from sf_ai.datasets import ChatDataset  # noqa: E402
from sf_ai.datasets.splits import (  # noqa: E402
    assign_split,
    iter_split_samples_round_robin_by_family,
    write_split_manifest,
)
from sf_ai.models.tokenizer import CharTokenizer  # noqa: E402
from sf_ai.training.train_tiny_lm import iter_token_batches  # noqa: E402


def _record(text: str, dialect: str = "msa", family: str | None = None) -> str:
    provenance = {
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
    }
    if family:
        provenance["dialogue_family"] = family
        provenance["prompt_family"] = family
        provenance["answer_family"] = family
    return json.dumps(
        {
            "domain": "chat",
            "lang": "ar",
            "messages": [
                {"role": "user", "content": f"سؤال {text}"},
                {"role": "assistant", "content": f"جواب {text}"},
            ],
            "provenance": provenance,
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


def test_round_robin_split_order_interleaves_dialogue_families(tmp_path: Path) -> None:
    corpus = tmp_path / "corpus"
    corpus.mkdir()
    families = ["open_social", "followup", "planning", "support", "topic"]
    rows: list[str] = []
    records: list[dict[str, object]] = []
    line_no = 1
    for family in families:
        for idx in range(2):
            rows.append(_record(f"{family}-{idx}", family=family))
            records.append({"file": "x.jsonl", "line": line_no, "split": "train", "sha256": str(line_no)})
            line_no += 1
    rows.append(_record("unknown"))
    records.append({"file": "x.jsonl", "line": line_no, "split": "train", "sha256": str(line_no)})
    (corpus / "x.jsonl").write_text("\n".join(rows) + "\n", encoding="utf-8")
    split = tmp_path / "split.json"
    split.write_text(json.dumps({"records": records}, ensure_ascii=False), encoding="utf-8")

    samples = list(
        iter_split_samples_round_robin_by_family(
            corpus,
            split,
            split_name="train",
        )
    )
    actual = [
        getattr(sample.provenance, "dialogue_family", None)
        for sample in samples
    ]

    assert actual[:5] == families
    assert actual[5:10] == families
    assert actual[-1] is None
