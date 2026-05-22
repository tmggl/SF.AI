"""Type aliases for the semantic layer."""

from __future__ import annotations

from typing import TypeAlias

SparseVector: TypeAlias = dict[int, float]
TokenSet: TypeAlias = frozenset[str]
