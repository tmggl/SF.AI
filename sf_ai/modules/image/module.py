"""Image domain skeleton — no image generation or analysis yet."""

from __future__ import annotations

from sf_ai.modules._skeleton import SkeletonDomainModule


class ImageModule(SkeletonDomainModule):
    domain = "image"
    limitations = (
        "does not generate, edit, classify, or inspect images yet",
        "no vision model, diffusion model, or external AI API",
        "text-only chat remains the active interface",
    )
