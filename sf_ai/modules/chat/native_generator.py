"""NativeGenerator adapter skeleton for Phase 15.

This module loads only SF.AI-origin tokenizer/checkpoint artifacts and exposes a
small generation interface. The public chat API uses guarded generation only;
unsupported prompts are blocked instead of receiving a fixed fallback reply.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import torch

from sf_ai.models.tokenizer import BPETokenizer
from sf_ai.models.transformer import (
    GenerationConfig,
    TinyTransformer,
    config_for_size,
    greedy_generate,
    sample_generate,
)
from sf_ai.training.checkpoints import CheckpointManager
from sf_ai.training.device import DeviceManager
from sf_ai.training.train_tiny_lm import ASSISTANT_EOS_TOKEN


@dataclass(frozen=True)
class NativeGeneratorConfig:
    tokenizer_path: Path = Path("artifacts/tokenizers/sf_bpe/v4_min_lexical")
    checkpoints_root: Path = Path("artifacts/eval/phase27_33_advice_micro_stabilization/checkpoints")
    checkpoint_name: str = "sf-10m-step9800"
    generator_name: str = "sf_10m_phase27_33"
    model_size: str = "sf-10m"
    seq_len: int = 64
    max_new_tokens: int = 24
    temperature: float = 1.0
    top_k: int = 0
    no_repeat_ngram_size: int = 3
    repetition_penalty: float = 1.08
    device: str = "auto"
    dialogue_prompt: bool = True
    family_conditioning: bool = False


@dataclass(frozen=True)
class NativeGenerationResult:
    used: bool
    text: str
    generator: str
    reason: str


@dataclass(frozen=True)
class NativeGeneratorStatus:
    tokenizer_exists: bool
    checkpoint_meta_exists: bool
    checkpoint_state_exists: bool
    generator: str = "sf_10m_phase27_33"


def extract_dialogue_reply(decoded: str, model_prompt: str) -> str:
    """Extract the assistant continuation from a dialogue-formatted sample."""
    text = decoded.strip()
    if not text:
        return ""

    if text.startswith(model_prompt):
        text = text[len(model_prompt):].strip()
    elif "المساعد:" in text:
        text = text.split("المساعد:", 1)[1].strip()

    if text.startswith("المساعد:"):
        text = text[len("المساعد:"):].strip()
    if "المستخدم:" in text:
        text = text.split("المستخدم:", 1)[0].strip()
    return text.strip()


class NativeGenerator:
    """Lazy-loading wrapper around the sovereign SF.AI checkpoint."""

    def __init__(self, config: NativeGeneratorConfig | None = None) -> None:
        self.config = config or NativeGeneratorConfig()
        self._tokenizer: BPETokenizer | None = None
        self._model: TinyTransformer | None = None
        self._torch_device: torch.device | None = None

    def status(self) -> NativeGeneratorStatus:
        ckpt_dir = self.config.checkpoints_root / self.config.checkpoint_name
        return NativeGeneratorStatus(
            tokenizer_exists=(self.config.tokenizer_path / "meta.json").exists(),
            checkpoint_meta_exists=(ckpt_dir / "meta.json").exists(),
            checkpoint_state_exists=(ckpt_dir / "state.pt").exists(),
            generator=self.config.generator_name,
        )

    def generate(
        self,
        prompt: str,
        *,
        dialect: str | None = None,
        intent: str | None = None,
        topic: str | None = None,
        max_new_tokens: int | None = None,
        temperature: float | None = None,
        top_k: int | None = None,
    ) -> NativeGenerationResult:
        if not prompt.strip():
            return NativeGenerationResult(False, "", self.config.generator_name, "empty_prompt")

        status = self.status()
        if not status.tokenizer_exists:
            return NativeGenerationResult(False, "", status.generator, "missing_tokenizer")
        if not status.checkpoint_meta_exists or not status.checkpoint_state_exists:
            return NativeGenerationResult(False, "", status.generator, "missing_checkpoint")

        tok, model, device = self._load()
        model_prompt = self._format_prompt(
            prompt,
            dialect=dialect,
            intent=intent,
            topic=topic,
        )
        prompt_ids = tok.encode(model_prompt)
        if not prompt_ids:
            return NativeGenerationResult(False, "", status.generator, "prompt_not_tokenized")

        input_ids = torch.tensor([prompt_ids], dtype=torch.long, device=device)
        cfg = GenerationConfig(
            max_new_tokens=max_new_tokens or self.config.max_new_tokens,
            temperature=temperature or self.config.temperature,
            top_k=self.config.top_k if top_k is None else top_k,
            eos_token_id=tok.vocab.get(ASSISTANT_EOS_TOKEN),
            no_repeat_ngram_size=self.config.no_repeat_ngram_size,
            repetition_penalty=self.config.repetition_penalty,
        )
        if cfg.top_k > 0 or cfg.temperature != 1.0:
            out = sample_generate(model, input_ids, cfg)
        else:
            out = greedy_generate(model, input_ids, cfg)
        text = tok.decode(out[0].detach().cpu().tolist()).strip()
        if self.config.dialogue_prompt:
            text = extract_dialogue_reply(text, model_prompt)
        elif text.startswith(model_prompt):
            text = text[len(model_prompt):].strip()
        if not text:
            return NativeGenerationResult(False, "", status.generator, "empty_generation")
        return NativeGenerationResult(True, text, status.generator, "generated")

    def _format_prompt(
        self,
        prompt: str,
        *,
        dialect: str | None = None,
        intent: str | None = None,
        topic: str | None = None,
    ) -> str:
        if not self.config.dialogue_prompt:
            return prompt
        condition_lines = [
            line
            for line in (
                _dialect_condition_line(dialect),
                _family_condition_line(intent) if self.config.family_conditioning else "",
                _requested_topic_condition_line(topic, intent) if self.config.family_conditioning else "",
                "" if self.config.family_conditioning else _intent_condition_line(intent),
                "" if self.config.family_conditioning else _topic_condition_line(topic),
            )
            if line
        ]
        if condition_lines:
            conditions = "\n".join(condition_lines)
            return f"{conditions}\nالمستخدم: {prompt.strip()}\nالمساعد:"
        return f"المستخدم: {prompt.strip()}\nالمساعد:"

    def _load(self) -> tuple[BPETokenizer, TinyTransformer, torch.device]:
        if self._tokenizer is not None and self._model is not None and self._torch_device is not None:
            return self._tokenizer, self._model, self._torch_device

        tokenizer = BPETokenizer.load(self.config.tokenizer_path)
        vocab_size = len(tokenizer)
        cfg = config_for_size(
            self.config.model_size,
            vocab_size=vocab_size,
            max_seq_len=self.config.seq_len,
        )
        device_info = DeviceManager(preference=self.config.device).select()
        torch_device = torch.device(device_info.name)
        model = TinyTransformer(cfg).to(torch_device)

        ckpt_mgr = CheckpointManager(self.config.checkpoints_root)
        ckpt_mgr.assert_sovereign(self.config.checkpoint_name)
        model.load_state_dict(ckpt_mgr.load_state(self.config.checkpoint_name))
        model.eval()

        self._tokenizer = tokenizer
        self._model = model
        self._torch_device = torch_device
        return tokenizer, model, torch_device


def _dialect_condition_line(dialect: str | None) -> str:
    d = (dialect or "").strip().lower()
    if d == "msa":
        return "النطاق: فصحى"
    if d in {"saudi", "gulf"}:
        return "النطاق: سعودي"
    return ""


def _intent_condition_line(intent: str | None) -> str:
    intent_label = _intent_label(intent)
    if intent_label:
        return f"النظام: النية: {intent_label}"
    return ""


def _intent_label(intent: str | None) -> str:
    i = (intent or "").strip().lower()
    mapping = {
        "greeting": "تحية",
        "chat.greeting": "تحية",
        "smalltalk": "سؤال حال",
        "chat.smalltalk": "سؤال حال",
        "definition": "تعريف",
        "chat.definition": "تعريف",
        "advice": "نصيحة",
        "chat.advice": "نصيحة",
        "planning": "تخطيط",
        "chat.planning": "تخطيط",
        "support": "دعم",
        "chat.support": "دعم",
        "thanks": "شكر",
        "chat.thanks": "شكر",
        "followup": "متابعة",
        "chat.followup": "متابعة",
        "open_social": "سوالف",
        "chat.open_social": "سوالف",
        "topic": "تعريف",
        "chat.topic": "تعريف",
    }
    return mapping.get(i, "")


def _family_condition_line(intent: str | None) -> str:
    family_label = _family_label(intent)
    if family_label:
        return f"عائلة الحوار: {family_label}"
    return ""


def _family_label(intent: str | None) -> str:
    i = (intent or "").strip().lower()
    mapping = {
        "open_social": "سوالف",
        "chat.open_social": "سوالف",
        "smalltalk": "سوالف",
        "chat.smalltalk": "سوالف",
        "greeting": "سوالف",
        "chat.greeting": "سوالف",
        "followup": "متابعة",
        "chat.followup": "متابعة",
        "planning": "تنظيم",
        "chat.planning": "تنظيم",
        "advice": "تنظيم",
        "chat.advice": "تنظيم",
        "support": "دعم",
        "chat.support": "دعم",
        "topic": "موضوع",
        "chat.topic": "موضوع",
        "definition": "موضوع",
        "chat.definition": "موضوع",
    }
    return mapping.get(i, "")


def _topic_condition_line(topic: str | None) -> str:
    t = (topic or "").strip()
    if t:
        return f"النظام: المصطلح: {t}"
    return ""


def _requested_topic_condition_line(topic: str | None, intent: str | None) -> str:
    t = (topic or "").strip()
    if t and _family_label(intent) == "موضوع":
        return f"الموضوع المطلوب: {t}"
    return ""
