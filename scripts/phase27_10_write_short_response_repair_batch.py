#!/usr/bin/env python3
"""Write Phase 27.10 short-response repair batch.

Natural MSA/Saudi short replies only. No project-operation, engineering,
agent workflow, private management, or model-training language.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "data/corpus/chat/jsonl"
LICENSE = "owner-approved-for-sf-ai-training"
OWNER_USER_ID = "sami-local"
CREATOR_USER_ID = "sf-ai-local-author"

FORBIDDEN = (
    "التالي", "اكمل", "أكمل", "ارفع", "commit", "pytest", "git", "phase",
    "Phase", "gates", "readiness", "corpus", "tokenizer", "تدريب", "التدريب",
    "الواجهة", "سيرفر", "endpoint", "runtime", "agent", "workflow", "سامي",
    "SF.AI", "النموذج", "المولد", "قالب", "checkpoint", "LLM", "RAG",
)


MSA_PAIRS: tuple[tuple[str, str], ...] = (
    ("السلام عليكم", "وعليكم السلام، أهلًا بك."),
    ("مرحبًا", "مرحبًا بك، تفضل."),
    ("صباح الخير", "صباح النور، يومك سعيد."),
    ("مساء الخير", "مساء النور، كيف أساعدك؟"),
    ("كيف حالك؟", "أنا بخير، شكرًا لسؤالك."),
    ("هل تفهمني؟", "نعم، أفهمك. وضّح لي ما تريد."),
    ("أريد جوابًا قصيرًا.", "حسنًا، سأجيب باختصار."),
    ("اشرح لي ببساطة.", "ببساطة: ابدأ بخطوة صغيرة."),
    ("لم أفهم.", "لا بأس، سأعيدها بوضوح."),
    ("شكرًا لك.", "العفو، يسعدني مساعدتك."),
    ("أعتذر.", "لا مشكلة، حصل خير."),
    ("أحتاج نصيحة.", "اختر خطوة واحدة وابدأ بها."),
    ("أنا متضايق.", "أفهمك. خذ نفسًا واهدأ قليلًا."),
    ("أريد أن أهدأ.", "تنفس بهدوء، ثم ابدأ من جديد."),
    ("هل هذا مناسب؟", "نعم، مناسب كبداية."),
    ("أريد صياغة ألطف.", "قلها بهدوء وبكلمات مباشرة."),
    ("أريد رفضًا مهذبًا.", "قل: أقدر طلبك، لكن لا أستطيع الآن."),
    ("أريد اعتذارًا قصيرًا.", "قل: أعتذر، لم أقصد إزعاجك."),
    ("أريد مثالًا.", "مثال: ابدأ بالتحية ثم اذكر طلبك."),
    ("هل نتابع لاحقًا؟", "نعم، نتابع متى عدت."),
    ("أريد أن أطمئن عليه.", "قل: كيف حالك؟ أحببت الاطمئنان عليك."),
    ("أريد ردًا رسميًا.", "استخدم عبارة محترمة ومباشرة."),
    ("أريد ردًا عاديًا.", "قلها ببساطة وبدون تكلف."),
    ("هل أكرر السؤال؟", "كرره مرة واحدة بلطف."),
    ("أحتاج ترتيب الفكرة.", "اكتبها، وسأرتبها لك."),
    ("هل كلامي واضح؟", "نعم، واضح."),
    ("أريد كلامًا مطمئنًا.", "الأمر يمكن ترتيبه خطوة خطوة."),
    ("أشعر بالحيرة.", "ابدأ بالسؤال الأقرب لك."),
    ("أريد أن أختصر.", "اكتب الهدف فقط."),
    ("هل يمكن أن تساعدني؟", "نعم، اكتب طلبك بوضوح."),
    ("ما أفضل بداية؟", "ابدأ بما تعرفه الآن."),
    ("أريد تشجيعًا.", "أنت قادر، ابدأ بخطوة بسيطة."),
    ("أريد توضيحًا.", "اسأل عن النقطة غير الواضحة."),
    ("أخاف أن أزعجه.", "اسأله بلطف إن كان الوقت مناسبًا."),
    ("أريد إنهاء الحديث.", "قل: سعدت بالحديث معك."),
    ("هذا مفيد.", "يسعدني ذلك."),
    ("أنا جاهز.", "رائع، لنبدأ."),
    ("لا أريد الإطالة.", "تمام، سأختصر."),
    ("أريد جملة واحدة.", "ابدأ بهدوء ولا تستعجل."),
    ("هل يكفي هذا؟", "نعم، يكفي كبداية."),
)


SAUDI_PAIRS: tuple[tuple[str, str], ...] = (
    ("السلام عليكم", "وعليكم السلام، حياك الله."),
    ("هلا", "هلا بك، تفضل."),
    ("صباح الخير", "صباح النور، عسى يومك طيب."),
    ("مساء الخير", "مساء النور، وش تحتاج؟"),
    ("كيفك؟", "بخير الحمد لله، أنت كيفك؟"),
    ("وشلونك؟", "تمام، الله يسلمك."),
    ("تفهم علي؟", "إيه، أفهم عليك."),
    ("أبي جواب قصير.", "تم، بعطيك المختصر."),
    ("بسطها لي.", "أبشر، بقولها ببساطة."),
    ("ما فهمت.", "ولا يهمك، أوضحها لك."),
    ("شكرًا.", "العفو، حياك."),
    ("يعطيك العافية.", "الله يعافيك."),
    ("ما قصرت.", "تسلم، هذا واجب."),
    ("آسف.", "عادي، حصل خير."),
    ("أحتاج نصيحة.", "ابدأ بخطوة وحدة."),
    ("أنا متضايق.", "أفهمك، خذها بهدوء."),
    ("أبي أهدأ.", "خذ نفس، وخلها خطوة خطوة."),
    ("يناسب كذا؟", "إيه، مناسب كبداية."),
    ("أبي صياغة ألطف.", "قلها بهدوء وبدون ضغط."),
    ("أبي أرفض بأدب.", "قل: أقدر طلبك، بس ما أقدر الحين."),
    ("أبي أعتذر.", "قل: آسف، ما كان قصدي أزعلك."),
    ("أبي مثال.", "مثال: سلم، ثم قل طلبك."),
    ("نتابع بعدين؟", "أكيد، نتابع متى رجعت."),
    ("أبي أطمن عليه.", "قل: كيفك؟ حبيت أطمن عليك."),
    ("أبي كلام رسمي.", "خلها محترمة وواضحة."),
    ("أبي كلام عادي.", "قلها ببساطة."),
    ("أعيد السؤال؟", "إيه، أعده مرة بلطف."),
    ("أبي أرتب الفكرة.", "اكتبها وأنا أرتبها لك."),
    ("كلامي واضح؟", "إيه، واضح."),
    ("أبي كلام يطمن.", "الموضوع ينحل خطوة خطوة."),
    ("محتار.", "ابدأ بأقرب سؤال لك."),
    ("خلنا نختصر.", "اكتب الهدف وبس."),
    ("تقدر تساعدني؟", "أكيد، اكتب وش تحتاج."),
    ("وش أفضل بداية؟", "ابدأ باللي تعرفه الحين."),
    ("أبي تشجيع.", "تقدر عليها، ابدأ بشي بسيط."),
    ("أبي توضيح.", "حدد النقطة اللي مو واضحة."),
    ("أخاف أزعجه.", "اسأله إذا الوقت مناسب."),
    ("أبي أنهي الكلام.", "قل: سعدت بالكلام معك."),
    ("هذا أفادني.", "الحمد لله."),
    ("أنا جاهز.", "تمام، نبدأ."),
    ("لا تطول.", "أبشر، باختصر."),
    ("أبي جملة وحدة.", "ابدأ بهدوء ولا تستعجل."),
    ("يكفي كذا؟", "إيه، يكفي كبداية."),
)


def _variants(pairs: tuple[tuple[str, str], ...], target: int) -> list[tuple[str, str]]:
    prefixes = ("", "لو سمحت، ", "طيب، ", "بس ")
    suffixes = ("", " باختصار.", " من فضلك.")
    out: list[tuple[str, str]] = []
    for prefix in prefixes:
        for user, assistant in pairs:
            for suffix in suffixes:
                u = f"{prefix}{user}".strip()
                a = assistant if not suffix else f"{assistant.rstrip('.؟!')} {suffix.strip()}"
                out.append((u, a))
                if len(out) >= target:
                    return out
    return out


def _record(dialect: str, user: str, assistant: str) -> dict[str, object]:
    return {
        "domain": "chat",
        "lang": "ar",
        "messages": [
            {"role": "user", "content": user},
            {"role": "assistant", "content": assistant},
        ],
        "provenance": {
            "source": f"sf-ai-short-response-repair-{dialect}-v1",
            "license": LICENSE,
            "language": "ar",
            "dialect": dialect,
            "quality": "gold",
            "training_allowed": True,
            "owner_user_id": OWNER_USER_ID,
            "created_by_user_id": CREATOR_USER_ID,
            "target_user_id": OWNER_USER_ID,
            "user_scope": "single_user",
            "notes": "short everyday response repair; owner delegated local authoring; no external dataset",
        },
    }


def _check(records: list[dict[str, object]]) -> None:
    text = json.dumps(records, ensure_ascii=False)
    bad = [term for term in FORBIDDEN if term in text]
    if bad:
        raise RuntimeError(f"forbidden operational terms in repair batch: {bad}")


def _write_jsonl(path: Path, records: list[dict[str, object]]) -> None:
    path.write_text(
        "\n".join(json.dumps(record, ensure_ascii=False) for record in records) + "\n",
        encoding="utf-8",
    )


def _write_card(path: Path, *, title: str, dialect: str, count: int) -> None:
    path.write_text(
        "\n".join(
            [
                f"# {title}",
                "",
                "- source: owner-delegated local authoring",
                f"- dialect: {dialect}",
                f"- records: {count}",
                "- quality: gold",
                "- training_allowed: true",
                "- synthetic_llm_data: false",
                "- external_dataset: false",
                "- purpose: short everyday response repair",
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> int:
    msa_pairs = _variants(MSA_PAIRS, 150)
    saudi_pairs = _variants(SAUDI_PAIRS, 150)
    msa = [_record("msa", user, assistant) for user, assistant in msa_pairs]
    saudi = [_record("saudi", user, assistant) for user, assistant in saudi_pairs]
    _check(msa + saudi)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    msa_path = OUT_DIR / "dialogue_batch_v8_short_repair_msa_008.jsonl"
    saudi_path = OUT_DIR / "dialogue_batch_v8_short_repair_saudi_008.jsonl"
    _write_jsonl(msa_path, msa)
    _write_jsonl(saudi_path, saudi)
    _write_card(msa_path.with_suffix(".CARD.md"), title=msa_path.name, dialect="msa", count=len(msa))
    _write_card(saudi_path.with_suffix(".CARD.md"), title=saudi_path.name, dialect="saudi", count=len(saudi))
    print(f"wrote {len(msa)} records: {msa_path}")
    print(f"wrote {len(saudi)} records: {saudi_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
