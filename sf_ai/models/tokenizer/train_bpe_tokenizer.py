"""train_bpe_from_corpus — high-level training entrypoint.

Reads dialogue samples from a corpus root (Phase 5 ChatDataset), feeds the
content into BPETokenizer.train, and writes the artifacts under
`artifacts/tokenizers/sf_bpe/<name>/` along with a `meta.json` that records
training provenance.

REFUSES to start training if the corpus is empty — the user must place
dialogue data first. See PROJECT_PRINCIPLES.md and DATASET_FORMAT.md.
"""

from __future__ import annotations

import hashlib
from collections.abc import Iterable, Iterator
from datetime import datetime, timezone
from pathlib import Path

from sf_ai.datasets import ChatDataset
from sf_ai.models.tokenizer.bpe_tokenizer import BPETokenizer
from sf_ai.models.tokenizer.tokenizer_config import TokenizerConfig


def _stream_text_from_dataset(dataset: ChatDataset) -> Iterator[str]:
    for msg in dataset.iter_messages():
        if msg.content.strip():
            yield msg.content


def _hash_file(path: Path) -> str:
    h = hashlib.blake2b(digest_size=16)
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def train_bpe_from_corpus(
    corpus_root: str | Path,
    output_dir: str | Path,
    *,
    config: TokenizerConfig | None = None,
    extra_texts: Iterable[str] | None = None,
    name: str = "sf_bpe",
) -> BPETokenizer:
    """Train a sovereign BPE tokenizer on the given corpus.

    Args:
        corpus_root: Directory containing *.jsonl chat samples (Phase 5 format).
        output_dir: Where to save vocab/merges/meta. Created if missing.
        config: TokenizerConfig. Defaults to vocab_size=8000.
        extra_texts: Optional extra text stream merged into training (e.g.
            in-memory user texts). MUST NOT contain LLM-generated data.
        name: Logical name written into meta.json.

    Raises:
        ValueError: when the corpus has no usable text.
    """
    corpus_root = Path(corpus_root)
    output_dir = Path(output_dir)
    cfg = config or TokenizerConfig()

    dataset = ChatDataset(root=corpus_root)
    files = dataset.jsonl_files()
    text_iter: Iterator[str] = _stream_text_from_dataset(dataset)

    # If the user provided extra texts we chain them in deterministically.
    if extra_texts is not None:
        extra_list = list(extra_texts)
    else:
        extra_list = []

    # Realize a list for accurate stats and to avoid double-streaming.
    all_texts: list[str] = list(text_iter) + extra_list
    if not all_texts:
        raise ValueError(
            f"refusing to train — corpus at {corpus_root} is empty. "
            "Place dialogue data in data/corpus/chat/jsonl/ first."
        )

    tokenizer = BPETokenizer(config=cfg)
    stats = tokenizer.train(all_texts)

    training_meta = {
        "name": name,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "corpus_root": str(corpus_root),
        "source_files": [
            {"path": str(p), "blake2b_16": _hash_file(p)} for p in files
        ],
        "extra_texts_count": len(extra_list),
        "stats": {
            "words_seen": stats.words_seen,
            "unique_words": stats.unique_words,
            "merges_learned": stats.merges_learned,
            "base_alphabet_size": stats.base_alphabet_size,
        },
    }
    tokenizer.save(output_dir, training_meta=training_meta)
    return tokenizer
