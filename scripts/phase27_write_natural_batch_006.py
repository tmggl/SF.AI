#!/usr/bin/env python3
"""Write Phase 27 natural dialogue batch 006."""

from __future__ import annotations

from phase27_write_natural_batch_004 import (  # type: ignore
    MSA_SCENARIOS,
    OUT_DIR,
    SAUDI_SCENARIOS,
    _build_records,
    _write_card,
    _write_jsonl,
)


OPENINGS_MSA_006 = (
    "أريد صياغة إنسانية لموقف:",
    "في حديث عادي،",
    "ما الجواب الأقرب للطبيعي إذا",
    "أحتاج ردًا مختصرًا حول:",
    "كيف أتكلم بلطف عندما",
    "ما العبارة الهادئة إذا",
    "أريد ترتيب كلامي في موقف:",
    "لو احتجت أن أقول هذا:",
    "ما الأسلوب المناسب مع شخص حين",
    "أريد مساعدة في موقف بسيط:",
    "كيف أقولها بطريقة مريحة:",
    "ما الرد المتزن على:",
    "أريد نصيحة قصيرة عندما",
    "كيف أتعامل مع شخص إذا",
    "ما الصيغة اليومية المناسبة إذا",
)

OPENINGS_SAUDI_006 = (
    "أبي صياغة طبيعية لموقف:",
    "في سوالف عادية،",
    "وش الجواب الأقرب للطبيعي إذا",
    "أحتاج رد مختصر عن:",
    "كيف أتكلم بلطف يوم",
    "وش العبارة الهادية إذا",
    "أبي أرتب كلامي في موقف:",
    "لو احتجت أقول كذا:",
    "وش الأسلوب المناسب مع شخص يوم",
    "أبي مساعدة في موقف بسيط:",
    "كيف أقولها بطريقة مريحة:",
    "وش الرد المتزن على:",
    "أبي نصيحة قصيرة إذا",
    "كيف أتعامل مع شخص لو",
    "وش الصيغة اليومية المناسبة إذا",
)


def main() -> int:
    msa_records = _build_records(
        dialect="msa",
        openings=OPENINGS_MSA_006,
        scenarios=MSA_SCENARIOS,
    )
    saudi_records = _build_records(
        dialect="saudi",
        openings=OPENINGS_SAUDI_006,
        scenarios=SAUDI_SCENARIOS,
    )
    if len(msa_records) != 750 or len(saudi_records) != 750:
        raise RuntimeError(
            f"unexpected batch size: msa={len(msa_records)} saudi={len(saudi_records)}"
        )

    msa_path = OUT_DIR / "dialogue_batch_v6_msa_006.jsonl"
    saudi_path = OUT_DIR / "dialogue_batch_v6_saudi_006.jsonl"
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
