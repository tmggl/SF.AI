"""CharTokenizer — character-level tokenizer trained from SF.AI corpus.

Smallest possible tokenizer. Useful for SF-10M smoke tests, debugging the
training loop, and detecting issues that BPE would mask. NOT used for the
real model — that uses BPETokenizer.
"""

from __future__ import annotations

import json
from collections.abc import Iterable
from pathlib import Path

from sf_ai.models.tokenizer.tokenizer_config import (
    DEFAULT_SPECIAL_TOKENS,
    TokenizerConfig,
)


class CharTokenizer:
    def __init__(
        self,
        vocab: dict[str, int] | None = None,
        config: TokenizerConfig | None = None,
    ) -> None:
        self.config = config or TokenizerConfig(vocab_size=512)
        self._token_to_id: dict[str, int] = dict(vocab) if vocab else {}
        self._id_to_token: dict[int, str] = {i: t for t, i in self._token_to_id.items()}

    # ----- properties -----

    def __len__(self) -> int:
        return len(self._token_to_id)

    @property
    def vocab(self) -> dict[str, int]:
        return dict(self._token_to_id)

    def unk_id(self) -> int:
        return self._token_to_id.get("<unk>", 0)

    # ----- training -----

    def train(self, texts: Iterable[str]) -> None:
        """Build vocab from a stream of texts. Idempotent if called multiple times."""
        # Start with special tokens (stable IDs).
        for tok in self.config.special_tokens:
            self._add_token(tok)
        # Collect character frequencies.
        freq: dict[str, int] = {}
        for text in texts:
            for ch in text:
                freq[ch] = freq.get(ch, 0) + 1
        # Sort by frequency desc, then lexicographic for determinism.
        sorted_chars = sorted(freq.items(), key=lambda kv: (-kv[1], kv[0]))
        for ch, count in sorted_chars:
            if count < self.config.min_frequency:
                continue
            if ch in self._token_to_id:
                continue
            if len(self._token_to_id) >= self.config.vocab_size:
                break
            self._add_token(ch)

    def _add_token(self, token: str) -> int:
        if token in self._token_to_id:
            return self._token_to_id[token]
        new_id = len(self._token_to_id)
        self._token_to_id[token] = new_id
        self._id_to_token[new_id] = token
        return new_id

    # ----- encode / decode -----

    def encode(self, text: str) -> list[int]:
        unk = self.unk_id()
        return [self._token_to_id.get(ch, unk) for ch in text]

    def decode(self, ids: Iterable[int]) -> str:
        out: list[str] = []
        for i in ids:
            tok = self._id_to_token.get(i, "")
            if tok in DEFAULT_SPECIAL_TOKENS:
                continue
            out.append(tok)
        return "".join(out)

    # ----- save / load -----

    def save(self, directory: str | Path) -> Path:
        d = Path(directory)
        d.mkdir(parents=True, exist_ok=True)
        (d / "vocab.json").write_text(
            json.dumps(self._token_to_id, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        (d / "meta.json").write_text(
            json.dumps(
                {
                    "tokenizer_type": "char",
                    "vocab_size": len(self._token_to_id),
                    "special_tokens": list(self.config.special_tokens),
                    "sf_origin": True,
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
        return d

    @classmethod
    def load(cls, directory: str | Path) -> "CharTokenizer":
        d = Path(directory)
        vocab = json.loads((d / "vocab.json").read_text(encoding="utf-8"))
        meta_path = d / "meta.json"
        if meta_path.exists():
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
            if not meta.get("sf_origin", False):
                raise ValueError(
                    f"refusing to load non-sovereign tokenizer at {d} "
                    "(meta.json missing sf_origin=true)"
                )
        return cls(vocab=vocab, config=TokenizerConfig(vocab_size=max(len(vocab), 64)))
