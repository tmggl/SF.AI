#!/usr/bin/env python3
"""Write Phase 27 natural dialogue batch 005."""

from __future__ import annotations

from phase27_write_natural_batch_004 import (  # type: ignore
    MSA_SCENARIOS,
    OUT_DIR,
    SAUDI_SCENARIOS,
    _build_records,
    _write_card,
    _write_jsonl,
)


OPENINGS_MSA_005 = (
    "في موقف يومي،",
    "أريد ردًا مناسبًا عندما",
    "ما الطريقة الألطف إذا",
    "ساعدني في التعامل مع هذا:",
    "أحتاج صياغة قصيرة عن موقف فيه",
    "كيف أتصرف بهدوء إذا",
    "ما الكلام الأفضل حين",
    "لو حدث معي هذا:",
    "أريد جوابًا بسيطًا لموقف:",
    "ما التصرف العملي عندما",
    "كيف أطلب هذا بلطف:",
    "أريد عبارة واضحة إذا",
    "ما الرد المهذب على موقف:",
    "أحتاج نصيحة يومية عن:",
    "كيف أشرح هذا بدون إطالة:",
)

OPENINGS_SAUDI_005 = (
    "في موقف عادي،",
    "أبي رد مناسب إذا",
    "وش ألطف طريقة لو",
    "ساعدني أتعامل مع هالشي:",
    "أبي صياغة قصيرة عن موقف فيه",
    "كيف أتصرف بهدوء إذا",
    "وش الكلام الأفضل يوم",
    "لو صار معي كذا:",
    "أبي جواب بسيط لموقف:",
    "وش التصرف العملي إذا",
    "كيف أطلبها بلطف:",
    "أبي عبارة واضحة لو",
    "وش الرد المهذب على موقف:",
    "أحتاج نصيحة يومية عن:",
    "كيف أوضحها بدون إطالة:",
)


def main() -> int:
    msa_records = _build_records(
        dialect="msa",
        openings=OPENINGS_MSA_005,
        scenarios=MSA_SCENARIOS,
    )
    saudi_records = _build_records(
        dialect="saudi",
        openings=OPENINGS_SAUDI_005,
        scenarios=SAUDI_SCENARIOS,
    )
    if len(msa_records) != 750 or len(saudi_records) != 750:
        raise RuntimeError(
            f"unexpected batch size: msa={len(msa_records)} saudi={len(saudi_records)}"
        )

    msa_path = OUT_DIR / "dialogue_batch_v5_msa_005.jsonl"
    saudi_path = OUT_DIR / "dialogue_batch_v5_saudi_005.jsonl"
    _write_jsonl(msa_path, msa_records)
    _write_jsonl(saudi_path, saudi_records)
    _write_card(
        msa_path.with_suffix(".CARD.md"),
        title=msa_path.name,
        dialect="msa",
        count=len(msa_records),
    )
    _write_card(
        saudi_path.with_suffix(".CARD.md"),
        title=saudi_path.name,
        dialect="saudi",
        count=len(saudi_records),
    )
    print(f"wrote {len(msa_records)} records: {msa_path}")
    print(f"wrote {len(saudi_records)} records: {saudi_path}")
    print(f"total batch records: {len(msa_records) + len(saudi_records)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
