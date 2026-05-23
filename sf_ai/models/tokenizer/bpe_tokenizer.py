"""BPETokenizer — Byte-Pair Encoding trained from SF.AI corpus only.

Pure-Python implementation (no external tokenizer library) so we can audit
every decision. Algorithm:

1. Pre-tokenize: split text on whitespace into "words".
2. Represent each word as a tuple of (char, char, ..., '</w>') symbols.
3. Repeat until vocab_size reached or no pairs left:
   a. Count adjacent pair frequencies across all word→tuple instances.
   b. Take the most frequent pair, merge it everywhere.
   c. Record the merge rule and append the new symbol to the vocab.

Encoding a new word:
1. Tokenize into characters + '</w>'.
2. Apply merge rules in the order they were learned, longest-first per pair.
3. Map symbols → IDs.

Storage layout (under `artifacts/tokenizers/sf_bpe/<name>/`):
- vocab.json — {token: id}
- merges.txt — "a b" pairs, one per line, in learning order
- meta.json  — {sf_origin: true, training stats, config, ...}

Loading any artifact whose `meta.json.sf_origin` is not `true` raises.
"""

from __future__ import annotations

import json
import re
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

from sf_ai.models.tokenizer.tokenizer_config import (
    DEFAULT_SPECIAL_TOKENS,
    END_OF_WORD,
    TokenizerConfig,
)


_WHITESPACE_RE = re.compile(r"\s+")


@dataclass(frozen=True)
class TrainingStats:
    words_seen: int
    unique_words: int
    merges_learned: int
    base_alphabet_size: int


class BPETokenizer:
    def __init__(self, config: TokenizerConfig | None = None) -> None:
        self.config = config or TokenizerConfig()
        self._vocab: dict[str, int] = {}
        self._merges: list[tuple[str, str]] = []
        self._merge_ranks: dict[tuple[str, str], int] = {}
        self._stats: TrainingStats | None = None
        self._protected_surface_to_term: dict[str, str] = self._build_protected_surface_map()

    # ----- properties -----

    def __len__(self) -> int:
        return len(self._vocab)

    @property
    def vocab(self) -> dict[str, int]:
        return dict(self._vocab)

    @property
    def merges(self) -> list[tuple[str, str]]:
        return list(self._merges)

    @property
    def stats(self) -> TrainingStats | None:
        return self._stats

    def unk_id(self) -> int:
        return self._vocab.get("<unk>", 0)

    # ----- pre-tokenization -----

    def _build_protected_surface_map(self) -> dict[str, str]:
        out: dict[str, str] = {}
        for raw in self.config.protected_terms:
            term = " ".join(str(raw).split())
            if not term:
                continue
            surface = self._term_to_surface(term)
            out[surface] = term
        return out

    def _term_to_surface(self, term: str) -> str:
        return self.config.protected_joiner.join(term.split())

    def _protect_phrases(self, text: str) -> str:
        if not self._protected_surface_to_term:
            return text
        protected_terms = sorted(
            self._protected_surface_to_term.values(),
            key=len,
            reverse=True,
        )
        out = text
        for term in protected_terms:
            surface = self._term_to_surface(term)
            pattern = re.compile(rf"(?<!\S){re.escape(term)}(?!\S)")
            out = pattern.sub(surface, out)
        return out

    def _pretokenize(self, text: str) -> list[str]:
        text = text.strip()
        if not text:
            return []
        if self.config.lowercase:
            text = text.lower()
        text = self._protect_phrases(text)
        return [w for w in _WHITESPACE_RE.split(text) if w]

    def _word_to_symbols(self, word: str) -> list[str]:
        if self.config.byte_level:
            return [bytes([b]).decode("latin1") for b in word.encode("utf-8")] + [END_OF_WORD]
        return list(word) + [END_OF_WORD]

    # ----- training -----

    def train(self, texts: Iterable[str]) -> TrainingStats:
        # Word → frequency.
        word_freq: dict[str, int] = {}
        words_seen = 0
        for text in texts:
            for w in self._pretokenize(text):
                words_seen += 1
                word_freq[w] = word_freq.get(w, 0) + 1

        # Filter words below min_frequency.
        word_freq = {
            w: c for w, c in word_freq.items() if c >= self.config.min_frequency
        }

        # Represent each word as tuple of symbols.
        word_symbols: dict[str, list[str]] = {
            w: self._word_to_symbols(w) for w in word_freq
        }

        # Initialize vocab: special tokens first, then base alphabet, then '</w>'.
        self._vocab = {}
        for tok in self.config.special_tokens:
            self._add_token(tok)
        base_alphabet: set[str] = set()
        for syms in word_symbols.values():
            base_alphabet.update(syms)
        for sym in sorted(base_alphabet):
            self._add_token(sym)
        base_alphabet_size = len(self._vocab)

        # Policy-owned protected phrases are first-class vocabulary entries.
        # They are project-authored terms, not external pretrained vocab, and
        # their presence is recorded in meta.json for auditability.
        for surface in sorted(self._protected_surface_to_term):
            if len(self._vocab) >= self.config.vocab_size:
                break
            self._add_token(surface)

        # BPE loop.
        merges_learned = 0
        while len(self._vocab) < self.config.vocab_size:
            pair_counts: dict[tuple[str, str], int] = {}
            for word, syms in word_symbols.items():
                freq = word_freq[word]
                for i in range(len(syms) - 1):
                    p = (syms[i], syms[i + 1])
                    pair_counts[p] = pair_counts.get(p, 0) + freq
            if not pair_counts:
                break

            # Most frequent pair (tie-break: lexicographic, deterministic).
            best_pair = max(pair_counts.items(), key=lambda kv: (kv[1], kv[0]))[0]
            if pair_counts[best_pair] < self.config.min_frequency:
                break

            # Apply merge across all words.
            new_token = best_pair[0] + best_pair[1]
            self._record_merge(best_pair[0], best_pair[1])
            self._add_token(new_token)
            merges_learned += 1
            for word, syms in word_symbols.items():
                if len(syms) < 2:
                    continue
                merged: list[str] = []
                i = 0
                while i < len(syms):
                    if (
                        i < len(syms) - 1
                        and syms[i] == best_pair[0]
                        and syms[i + 1] == best_pair[1]
                    ):
                        merged.append(new_token)
                        i += 2
                    else:
                        merged.append(syms[i])
                        i += 1
                word_symbols[word] = merged

        self._stats = TrainingStats(
            words_seen=words_seen,
            unique_words=len(word_freq),
            merges_learned=merges_learned,
            base_alphabet_size=base_alphabet_size,
        )
        return self._stats

    def _add_token(self, token: str) -> int:
        if token in self._vocab:
            return self._vocab[token]
        new_id = len(self._vocab)
        self._vocab[token] = new_id
        return new_id

    def _record_merge(self, a: str, b: str) -> None:
        self._merges.append((a, b))
        self._merge_ranks[(a, b)] = len(self._merges) - 1

    # ----- encoding -----

    def _encode_word(self, word: str) -> list[str]:
        if word in self._protected_surface_to_term and word in self._vocab:
            return [word]
        symbols = self._word_to_symbols(word)
        if not symbols:
            return []
        # Greedy "best pair" merging following learned ranks.
        while True:
            best_rank: int | None = None
            best_i: int = -1
            for i in range(len(symbols) - 1):
                rank = self._merge_ranks.get((symbols[i], symbols[i + 1]))
                if rank is None:
                    continue
                if best_rank is None or rank < best_rank:
                    best_rank = rank
                    best_i = i
            if best_rank is None:
                break
            merged = symbols[best_i] + symbols[best_i + 1]
            symbols = symbols[:best_i] + [merged] + symbols[best_i + 2:]
        return symbols

    def encode(self, text: str) -> list[int]:
        out: list[int] = []
        unk = self.unk_id()
        for word in self._pretokenize(text):
            for sym in self._encode_word(word):
                out.append(self._vocab.get(sym, unk))
        return out

    def decode(self, ids: Iterable[int]) -> str:
        # Reverse lookup.
        id_to_token = {i: t for t, i in self._vocab.items()}
        special = set(self.config.special_tokens)
        symbols: list[str] = []
        for i in ids:
            tok = id_to_token.get(i)
            if tok is None or tok in special:
                continue
            if tok in self._protected_surface_to_term:
                # A protected phrase token represents one or more words but
                # does not naturally carry '</w>'. Restore an explicit boundary
                # so the next generated token cannot glue to the phrase.
                symbols.append(tok + END_OF_WORD)
            else:
                symbols.append(tok)
        # Join: every '</w>' marks the end of a word → insert space afterwards.
        joined = "".join(symbols)
        joined = joined.replace(END_OF_WORD, " ")
        if self._protected_surface_to_term:
            joined = joined.replace(self.config.protected_joiner, " ")
        return joined.strip()

    # ----- save / load -----

    def save(self, directory: str | Path, *, training_meta: dict | None = None) -> Path:
        d = Path(directory)
        d.mkdir(parents=True, exist_ok=True)
        (d / "vocab.json").write_text(
            json.dumps(self._vocab, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        with (d / "merges.txt").open("w", encoding="utf-8") as f:
            f.write("# SF-BPE merges. Trained from SF.AI corpus only. sf_origin=true.\n")
            for a, b in self._merges:
                f.write(f"{a} {b}\n")
        meta: dict = {
            "tokenizer_type": "bpe",
            "sf_origin": True,
            "vocab_size": len(self._vocab),
            "merges": len(self._merges),
            "special_tokens": list(self.config.special_tokens),
            "lowercase": self.config.lowercase,
            "byte_level": self.config.byte_level,
            "protected_terms": list(self.config.protected_terms),
            "protected_joiner": self.config.protected_joiner,
        }
        if self._stats is not None:
            meta["training_stats"] = {
                "words_seen": self._stats.words_seen,
                "unique_words": self._stats.unique_words,
                "merges_learned": self._stats.merges_learned,
                "base_alphabet_size": self._stats.base_alphabet_size,
            }
        if training_meta:
            meta["training_meta"] = training_meta
        (d / "meta.json").write_text(
            json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        return d

    @classmethod
    def load(cls, directory: str | Path) -> "BPETokenizer":
        d = Path(directory)
        meta_path = d / "meta.json"
        if not meta_path.exists():
            raise ValueError(f"missing meta.json at {d} — cannot verify sovereignty")
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        if not meta.get("sf_origin", False):
            raise ValueError(
                f"refusing to load non-sovereign tokenizer at {d} "
                "(meta.json missing sf_origin=true)"
            )
        cfg = TokenizerConfig(
            vocab_size=int(meta.get("vocab_size", 8000)),
            special_tokens=tuple(meta.get("special_tokens", DEFAULT_SPECIAL_TOKENS)),
            lowercase=bool(meta.get("lowercase", False)),
            byte_level=bool(meta.get("byte_level", False)),
            protected_terms=tuple(meta.get("protected_terms") or ()),
            protected_joiner=str(meta.get("protected_joiner") or "▁"),
        )
        tok = cls(config=cfg)
        tok._vocab = json.loads((d / "vocab.json").read_text(encoding="utf-8"))
        merges_path = d / "merges.txt"
        if merges_path.exists():
            for line in merges_path.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                parts = line.split(" ")
                if len(parts) >= 2:
                    a = parts[0]
                    b = " ".join(parts[1:])
                    tok._record_merge(a, b)
        return tok
