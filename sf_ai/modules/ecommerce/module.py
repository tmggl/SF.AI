"""Ecommerce domain skeleton — no store integration yet."""

from __future__ import annotations

from sf_ai.modules._skeleton import SkeletonDomainModule


class EcommerceModule(SkeletonDomainModule):
    domain = "ecommerce"
    limitations = (
        "does not manage products, orders, payments, or stores yet",
        "no external marketplace or payment integration",
        "only skeleton metadata is available",
    )
