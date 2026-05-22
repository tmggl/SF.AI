"""Phase 6 — TinyTransformer + RoPE + RMSNorm + SwiGLU + generation + losses.

Skips automatically if torch is not installed (Phase 5.5 already established
that torch is an optional extra).
"""

from __future__ import annotations

from pathlib import Path

import pytest

torch = pytest.importorskip("torch")

from sf_ai.models.transformer import (  # noqa: E402
    GenerationConfig,
    RMSNorm,
    SF_MODEL_SIZES,
    SwiGLU,
    TinyTransformer,
    TransformerConfig,
    build_rope_cache,
    config_for_size,
    cross_entropy_lm,
    greedy_generate,
    perplexity,
    sample_generate,
)
from sf_ai.models.transformer.attention import CausalSelfAttention, apply_rope


# ---------- TransformerConfig ----------

def test_config_validates_d_model_divisible_by_heads() -> None:
    with pytest.raises(ValueError):
        TransformerConfig(d_model=10, n_heads=3, vocab_size=64, max_seq_len=16, n_layers=1)


def test_config_rejects_non_sovereign() -> None:
    with pytest.raises(ValueError):
        TransformerConfig(sovereign=False)


def test_config_for_size_known() -> None:
    cfg = config_for_size("sf-10m", vocab_size=512, max_seq_len=64)
    assert cfg.name == "sf-10m"
    assert cfg.d_model == 256
    assert cfg.n_heads == 4


def test_config_for_size_unknown() -> None:
    with pytest.raises(ValueError):
        config_for_size("sf-1t", vocab_size=512)


def test_size_ladder_has_five_entries() -> None:
    assert set(SF_MODEL_SIZES) == {"sf-10m", "sf-50m", "sf-120m", "sf-350m", "sf-700m"}


# ---------- RoPE ----------

def test_rope_cache_shape() -> None:
    cos, sin = build_rope_cache(seq_len=8, head_dim=16)
    assert cos.shape == (8, 8)
    assert sin.shape == (8, 8)


def test_rope_application_preserves_shape() -> None:
    head_dim = 16
    seq_len = 5
    cos, sin = build_rope_cache(seq_len=seq_len, head_dim=head_dim)
    x = torch.randn(1, 2, seq_len, head_dim)
    out = apply_rope(x, cos, sin)
    assert out.shape == x.shape


# ---------- Attention ----------

def test_attention_forward_shape_and_causal_independence() -> None:
    torch.manual_seed(0)
    d, h, T = 32, 4, 6
    attn = CausalSelfAttention(d_model=d, n_heads=h)
    cos, sin = build_rope_cache(seq_len=T, head_dim=d // h)
    x = torch.randn(2, T, d)
    out = attn(x, cos, sin)
    assert out.shape == (2, T, d)

    # Causal: changing the last token of x must not change the first output token.
    x2 = x.clone()
    x2[:, -1, :] = torch.randn_like(x2[:, -1, :])
    out2 = attn(x2, cos, sin)
    assert torch.allclose(out[:, 0, :], out2[:, 0, :], atol=1e-5)


# ---------- RMSNorm + SwiGLU ----------

def test_rmsnorm_keeps_shape_and_finite() -> None:
    n = RMSNorm(16)
    x = torch.randn(4, 16)
    y = n(x)
    assert y.shape == x.shape
    assert torch.isfinite(y).all()


def test_swiglu_keeps_dim() -> None:
    s = SwiGLU(d_model=16, ff_dim=32)
    x = torch.randn(2, 16)
    y = s(x)
    assert y.shape == (2, 16)


# ---------- TinyTransformer ----------

def _small_cfg(vocab_size: int = 128, max_seq_len: int = 32) -> TransformerConfig:
    return TransformerConfig(
        vocab_size=vocab_size,
        max_seq_len=max_seq_len,
        d_model=64,
        n_heads=4,
        n_layers=2,
        ff_mult=2,
    )


def test_tiny_transformer_forward_shape() -> None:
    torch.manual_seed(0)
    cfg = _small_cfg()
    model = TinyTransformer(cfg)
    ids = torch.randint(0, cfg.vocab_size, (2, 16))
    logits = model(ids)
    assert logits.shape == (2, 16, cfg.vocab_size)


def test_tiny_transformer_weight_tying_default() -> None:
    cfg = _small_cfg()
    model = TinyTransformer(cfg)
    # When tied, lm_head.weight is the same tensor as tok_embed.weight.
    assert model.lm_head.weight.data_ptr() == model.tok_embed.weight.data_ptr()


def test_tiny_transformer_no_weight_tying_option() -> None:
    cfg = TransformerConfig(
        vocab_size=128, max_seq_len=32, d_model=64, n_heads=4, n_layers=2,
        ff_mult=2, tie_weights=False,
    )
    model = TinyTransformer(cfg)
    assert model.lm_head.weight.data_ptr() != model.tok_embed.weight.data_ptr()


def test_tiny_transformer_param_count_in_range() -> None:
    cfg = _small_cfg()
    model = TinyTransformer(cfg)
    n = model.num_parameters()
    # Tiny model: should be small but > 0.
    assert 1_000 < n < 1_000_000


def test_tiny_transformer_random_init_changes_with_seed() -> None:
    cfg = _small_cfg()
    torch.manual_seed(0)
    a = TinyTransformer(cfg)
    torch.manual_seed(1)
    b = TinyTransformer(cfg)
    # Models with different seeds must differ — proves random init, not load.
    assert not torch.allclose(a.tok_embed.weight, b.tok_embed.weight)


def test_tiny_transformer_marks_sf_origin() -> None:
    model = TinyTransformer(_small_cfg())
    assert model.sf_origin is True


def test_tiny_transformer_rejects_overlong_input() -> None:
    cfg = _small_cfg(max_seq_len=8)
    model = TinyTransformer(cfg)
    ids = torch.randint(0, cfg.vocab_size, (1, 9))
    with pytest.raises(ValueError):
        model(ids)


def test_tiny_transformer_save_and_load_roundtrip(tmp_path: Path) -> None:
    torch.manual_seed(7)
    cfg = _small_cfg()
    a = TinyTransformer(cfg)
    path = tmp_path / "state.pt"
    a.save_state(path)

    # Build a fresh model and load. After loading, outputs match exactly.
    torch.manual_seed(99)
    b = TinyTransformer(cfg)
    b.load_state(path)
    ids = torch.randint(0, cfg.vocab_size, (1, 8))
    a.eval(); b.eval()
    with torch.no_grad():
        assert torch.allclose(a(ids), b(ids), atol=1e-6)


def test_tiny_transformer_refuses_suspicious_load_path(tmp_path: Path) -> None:
    cfg = _small_cfg()
    model = TinyTransformer(cfg)
    path = tmp_path / "huggingface_cache" / "pytorch_model.bin"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"junk")
    with pytest.raises(ValueError):
        model.load_state(path)


# ---------- Losses ----------

def test_cross_entropy_lm_shape() -> None:
    torch.manual_seed(0)
    cfg = _small_cfg()
    model = TinyTransformer(cfg)
    ids = torch.randint(0, cfg.vocab_size, (2, 10))
    logits = model(ids)
    targets = torch.randint(0, cfg.vocab_size, (2, 10))
    loss = cross_entropy_lm(logits, targets)
    assert loss.dim() == 0
    assert torch.isfinite(loss)


def test_cross_entropy_validates_shapes() -> None:
    bad_logits = torch.zeros(2, 5)
    targets = torch.zeros(2, 5, dtype=torch.long)
    with pytest.raises(ValueError):
        cross_entropy_lm(bad_logits, targets)


def test_perplexity_from_loss() -> None:
    assert abs(perplexity(0.0) - 1.0) < 1e-6
    assert perplexity(1.0) > 1.0


# ---------- Generation ----------

def test_greedy_generate_extends_sequence() -> None:
    torch.manual_seed(0)
    cfg = _small_cfg()
    model = TinyTransformer(cfg)
    prompt = torch.randint(0, cfg.vocab_size, (1, 4))
    cfg_gen = GenerationConfig(max_new_tokens=6)
    out = greedy_generate(model, prompt, cfg_gen)
    assert out.shape == (1, prompt.shape[1] + cfg_gen.max_new_tokens)


def test_sample_generate_extends_sequence_with_topk() -> None:
    torch.manual_seed(0)
    cfg = _small_cfg()
    model = TinyTransformer(cfg)
    prompt = torch.randint(0, cfg.vocab_size, (1, 3))
    cfg_gen = GenerationConfig(max_new_tokens=5, temperature=1.0, top_k=4)
    out = sample_generate(model, prompt, cfg_gen)
    assert out.shape == (1, prompt.shape[1] + cfg_gen.max_new_tokens)


def test_generation_config_rejects_bad_values() -> None:
    with pytest.raises(ValueError):
        GenerationConfig(max_new_tokens=0)
    with pytest.raises(ValueError):
        GenerationConfig(temperature=0)
    with pytest.raises(ValueError):
        GenerationConfig(top_k=-1)


# ---------- Training step ----------

def test_train_one_step_reduces_loss_on_overfit() -> None:
    """Overfit a single batch repeatedly — loss must drop fast."""
    from sf_ai.training.optimizers import OptimizerSpec, build_optimizer
    from sf_ai.training.train_tiny_lm import train_one_step

    torch.manual_seed(0)
    cfg = _small_cfg(vocab_size=64, max_seq_len=16)
    model = TinyTransformer(cfg)
    optim = build_optimizer(model.parameters(), OptimizerSpec(lr=3e-3))
    ids = torch.randint(0, cfg.vocab_size, (2, 8))
    targets = torch.randint(0, cfg.vocab_size, (2, 8))
    first = train_one_step(model, ids, targets, optim)
    for _ in range(20):
        last = train_one_step(model, ids, targets, optim)
    assert last < first
