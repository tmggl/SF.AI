"""Audio domain skeleton — no speech/audio processing yet."""

from __future__ import annotations

from sf_ai.modules._skeleton import SkeletonDomainModule


class AudioModule(SkeletonDomainModule):
    domain = "audio"
    limitations = (
        "does not transcribe, synthesize, classify, or edit audio yet",
        "no speech model or external AI API",
        "text-only chat remains the active interface",
    )
