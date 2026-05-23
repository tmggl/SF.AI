"""NativeGenerator adapter skeleton for Phase 15.

This module loads only SF.AI-origin tokenizer/checkpoint artifacts and exposes a
small generation interface. It is not enabled by default and ChatModule keeps
using templates unless the runtime explicitly opts in and the policy allows it.
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
    tokenizer_path: Path = Path("artifacts/tokenizers/sf_bpe/v2")
    checkpoints_root: Path = Path("artifacts/checkpoints/sf_10m_v0_2")
    checkpoint_name: str = "sf-10m-step2000"
    generator_name: str = "sf_10m_v0_2"
    model_size: str = "sf-10m"
    seq_len: int = 64
    max_new_tokens: int = 48
    temperature: float = 0.20
    top_k: int = 0
    device: str = "auto"
    dialogue_prompt: bool = True


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
    generator: str = "sf_10m_v0_2"


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
        model_prompt = self._format_prompt(prompt, dialect=dialect)
        prompt_ids = tok.encode(model_prompt)
        if not prompt_ids:
            return NativeGenerationResult(False, "", status.generator, "prompt_not_tokenized")

        input_ids = torch.tensor([prompt_ids], dtype=torch.long, device=device)
        cfg = GenerationConfig(
            max_new_tokens=max_new_tokens or self.config.max_new_tokens,
            temperature=temperature or self.config.temperature,
            top_k=self.config.top_k if top_k is None else top_k,
            eos_token_id=tok.vocab.get(ASSISTANT_EOS_TOKEN),
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

    def _format_prompt(self, prompt: str, *, dialect: str | None = None) -> str:
        if not self.config.dialogue_prompt:
            return prompt
        scope = _dialect_condition_line(dialect)
        if scope:
            return f"{scope}\nالمستخدم: {prompt.strip()}\nالمساعد:"
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
