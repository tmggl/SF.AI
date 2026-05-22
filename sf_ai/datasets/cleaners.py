"""SampleCleaner — conservative cleaning over parsed samples.

Reuses Phase 3's TextCleaner so the same rules govern code preservation, and
optionally applies the ArabicNormalizer for downstream tokenizer training
(Phase 5.5). Cleaning never changes the semantic meaning of a message.
"""

from __future__ import annotations

from sf_ai.core.nlp.arabic_normalizer import ArabicNormalizer
from sf_ai.core.nlp.text_cleaner import TextCleaner
from sf_ai.datasets.schemas import (
    ChatMessage,
    Provenance,
    SimpleSample,
    StructuredSample,
)


class SampleCleaner:
    def __init__(
        self,
        text_cleaner: TextCleaner | None = None,
        normalizer: ArabicNormalizer | None = None,
        normalize: bool = False,
    ) -> None:
        self.text_cleaner = text_cleaner or TextCleaner()
        self.normalizer = normalizer or ArabicNormalizer()
        self.normalize = normalize

    def _clean_text(self, text: str) -> str:
        cleaned = self.text_cleaner.clean(text)
        if self.normalize and cleaned:
            cleaned = self.normalizer.normalize(cleaned)
        return cleaned

    def clean_message(self, msg: ChatMessage) -> ChatMessage | None:
        """Return a cleaned ChatMessage, or None if cleaning emptied it."""
        cleaned = self._clean_text(msg.content)
        if not cleaned.strip():
            return None
        if cleaned == msg.content:
            return msg
        return ChatMessage(role=msg.role, content=cleaned)

    def clean_simple(self, sample: SimpleSample) -> SimpleSample:
        cleaned = self._clean_text(sample.text)
        if not cleaned.strip():
            raise ValueError("sample has no content after cleaning")
        if cleaned == sample.text:
            return sample
        return SimpleSample(text=cleaned, provenance=sample.provenance)

    def clean_structured(self, sample: StructuredSample) -> StructuredSample:
        new_msgs: list[ChatMessage] = []
        for m in sample.messages:
            cleaned = self.clean_message(m)
            if cleaned is not None:
                new_msgs.append(cleaned)
        if not new_msgs:
            raise ValueError("sample has no content after cleaning")
        return StructuredSample(
            domain=sample.domain,
            lang=sample.lang,
            messages=new_msgs,
            provenance=sample.provenance,
        )

    def clean(
        self, sample: SimpleSample | StructuredSample
    ) -> SimpleSample | StructuredSample:
        if isinstance(sample, SimpleSample):
            return self.clean_simple(sample)
        return self.clean_structured(sample)


__all__ = ["SampleCleaner", "Provenance"]
