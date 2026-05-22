"""Security domain skeleton — safety-gated, defensive-only future scope."""

from __future__ import annotations

from sf_ai.modules._skeleton import SkeletonDomainModule


class SecurityModule(SkeletonDomainModule):
    domain = "security"
    requires_safety = True
    limitations = (
        "does not provide exploit, intrusion, malware, or evasion guidance",
        "must route to safe ResponseComposer messaging while skeleton_only",
        "future activation must be defensive-only",
    )
