"""Dataset schemas.

Two record types are accepted in Phase 5:

1. **SimpleSample** — a flat string with optional inline role markers.
   ``{"text": "المستخدم: مرحبا\\nالمساعد: أهلاً"}``

2. **StructuredSample** — explicit messages list.
   ``{"domain": "chat", "lang": "ar", "messages": [{"role":"user","content":"مرحبا"}]}``

Provenance metadata is optional but strongly recommended on every file.
"""

from __future__ import annotations

import re
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, ValidationError, model_validator


ALLOWED_ROLES: frozenset[str] = frozenset({"system", "user", "assistant"})
ALLOWED_LANGS: frozenset[str] = frozenset({"ar", "en", "mixed", "code", "unknown"})

# Inline role tags accepted in SimpleSample.text. Phase 5 supports Arabic +
# English shorthand; case-insensitive on English.
_INLINE_ROLE_RE = re.compile(
    r"^\s*(المستخدم|المساعد|النظام|user|assistant|system)\s*:\s*",
    re.IGNORECASE,
)
_INLINE_ROLE_NORMALIZE = {
    "المستخدم": "user",
    "المساعد": "assistant",
    "النظام": "system",
    "user": "user",
    "assistant": "assistant",
    "system": "system",
}


class SampleType(str, Enum):
    SIMPLE = "simple"
    STRUCTURED = "structured"


class ChatMessage(BaseModel):
    role: str = Field(..., description="user | assistant | system")
    content: str = Field(..., min_length=1)

    @model_validator(mode="after")
    def _check_role(self) -> "ChatMessage":
        if self.role not in ALLOWED_ROLES:
            raise ValueError(f"invalid role: {self.role!r}")
        return self


class Provenance(BaseModel):
    """Optional, but encouraged on every input file."""

    source: str | None = None      # url / corpus name / author
    license: str | None = None     # SPDX id, "user-provided", etc.
    fetched_at: str | None = None  # ISO 8601 date
    language: str | None = None    # ar / en / mixed
    dialect: str | None = None     # msa / saudi / ...
    quality: str | None = None     # gold / silver / bronze (Phase 11 training gate)
    training_allowed: bool | None = None  # explicit owner permission for training
    dialogue_family: str | None = None     # open_social / followup / planning / support / topic
    prompt_family: str | None = None       # user-side dialogue family hint
    answer_family: str | None = None       # assistant-side dialogue family hint
    topic_term: str | None = None          # requested topic anchor for topic-family dialogue
    owner_user_id: str | None = None       # canonical owner of this dialogue data
    created_by_user_id: str | None = None  # author/exporter/reviewer who created it
    target_user_id: str | None = None      # user/account this data may personalize
    user_scope: str | None = None          # single_user / multi_user / public
    notes: str | None = None


class SimpleSample(BaseModel):
    text: str = Field(..., min_length=1)
    provenance: Provenance | None = None

    def to_messages(self) -> list[ChatMessage]:
        """Best-effort parse of role markers into ChatMessage list.

        Lines whose prefix matches a role tag become a new message; otherwise
        they extend the previous message. If no marker exists at all the whole
        text is treated as a single user message.
        """
        msgs: list[ChatMessage] = []
        current_role: str | None = None
        buffer: list[str] = []

        def _flush() -> None:
            if current_role is not None and buffer:
                content = "\n".join(buffer).strip()
                if content:
                    msgs.append(ChatMessage(role=current_role, content=content))

        for line in self.text.splitlines():
            m = _INLINE_ROLE_RE.match(line)
            if m:
                _flush()
                tag = m.group(1).lower() if m.group(1).isascii() else m.group(1)
                current_role = _INLINE_ROLE_NORMALIZE[tag]
                buffer = [line[m.end():]]
            else:
                if current_role is None:
                    current_role = "user"
                buffer.append(line)
        _flush()

        if not msgs:
            # Bare text without any marker — wrap as single user message.
            msgs = [ChatMessage(role="user", content=self.text.strip())]
        return msgs


class StructuredSample(BaseModel):
    domain: str = Field(default="chat")
    lang: str = Field(default="unknown")
    messages: list[ChatMessage] = Field(..., min_length=1)
    provenance: Provenance | None = None

    @model_validator(mode="after")
    def _check_lang(self) -> "StructuredSample":
        if self.lang not in ALLOWED_LANGS:
            raise ValueError(f"invalid lang: {self.lang!r}")
        return self


def parse_record(raw: dict[str, Any]) -> SimpleSample | StructuredSample:
    """Turn a raw dict (from JSONL) into the matching pydantic model.

    Raises ValidationError or ValueError on malformed input — callers should
    handle by reporting the offending line number.
    """
    if not isinstance(raw, dict):
        raise ValueError("record must be a JSON object")
    if "messages" in raw:
        return StructuredSample(**raw)
    if "text" in raw:
        return SimpleSample(**raw)
    raise ValueError("record must contain either 'messages' or 'text'")


__all_errors__ = (ValidationError, ValueError)
