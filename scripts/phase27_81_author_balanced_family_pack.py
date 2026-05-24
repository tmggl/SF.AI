#!/usr/bin/env python3
"""Phase 27.81 — author a balanced family pack.

No training. This writes owner-delegated, SF-native dialogue records for the
underrepresented families discovered by Phase 27.80:

- open_social/followup/planning/support/topic: 500 records each

The pack is authored locally for SF.AI only. No external datasets, no
pretrained model outputs, and no project/operator dialogue.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/corpus/chat/jsonl"
REPORT = ROOT / "artifacts/reports/phase27_81_balanced_family_pack_report.json"
DECISION = ROOT / "artifacts/reports/PHASE27_81_BALANCED_FAMILY_PACK_DECISION.json"
DOC = ROOT / "docs/PHASE27_81_BALANCED_FAMILY_PACK.md"


@dataclass(frozen=True)
class Quota:
    family: str
    dialect: str
    count: int
    filename: str


QUOTAS = (
    Quota("open_social", "msa", 250, "dialogue_batch_v10_balanced_open_social_msa_010.jsonl"),
    Quota("open_social", "saudi", 250, "dialogue_batch_v10_balanced_open_social_saudi_010.jsonl"),
    Quota("followup", "msa", 250, "dialogue_batch_v10_balanced_followup_msa_010.jsonl"),
    Quota("followup", "saudi", 250, "dialogue_batch_v10_balanced_followup_saudi_010.jsonl"),
    Quota("planning", "msa", 250, "dialogue_batch_v10_balanced_planning_msa_010.jsonl"),
    Quota("planning", "saudi", 250, "dialogue_batch_v10_balanced_planning_saudi_010.jsonl"),
    Quota("support", "msa", 250, "dialogue_batch_v10_balanced_support_msa_010.jsonl"),
    Quota("support", "saudi", 250, "dialogue_batch_v10_balanced_support_saudi_010.jsonl"),
    Quota("topic", "msa", 250, "dialogue_batch_v10_balanced_topic_msa_010.jsonl"),
    Quota("topic", "saudi", 250, "dialogue_batch_v10_balanced_topic_saudi_010.jsonl"),
)

OPEN_SOCIAL_PROMPTS_MSA = [
    "أريد حديثًا خفيفًا اليوم.",
    "افتح معي موضوعًا بسيطًا.",
    "أشعر بالملل قليلًا.",
    "حدثني عن شيء لطيف.",
    "أريد أن نتكلم بهدوء.",
    "اقترح حديثًا قصيرًا.",
    "كيف نجعل الحديث أخف؟",
    "أحب الكلام الهادئ.",
]
OPEN_SOCIAL_REPLIES_MSA = [
    "نبدأ بحديث خفيف عن يومك، ما الشيء اللطيف الذي حدث لك؟",
    "يمكننا أن نتكلم عن عادة بسيطة تحبها في يومك.",
    "لنجعل الحديث هادئًا: ما أكثر شيء أراحك اليوم؟",
    "موضوع لطيف: ما المكان الذي تحب أن تجلس فيه عندما تريد الهدوء؟",
    "نستطيع أن نتحدث عن شيء صغير أسعدك أو خفف عنك اليوم.",
]
OPEN_SOCIAL_PROMPTS_SAUDI = [
    "سولف معي شوي.",
    "هات سالفة خفيفة.",
    "ودي نسولف بهدوء.",
    "طفشان شوي.",
    "افتح موضوع بسيط.",
    "وش عندك من سالفة؟",
    "خلنا نتكلم شوي.",
    "ابي كلام خفيف.",
]
OPEN_SOCIAL_REPLIES_SAUDI = [
    "أبشر، خلنا نسولف عن يومك: وش ألطف شي صار لك؟",
    "نقدر نفتح سالفة خفيفة عن عادة تحبها في يومك.",
    "خلها بسيطة: وش الشي اللي ريحك اليوم؟",
    "موضوع خفيف: وش المكان اللي تحب تجلس فيه إذا تبي تهدأ؟",
    "تمام، نبدأ بشي بسيط: وش أكثر شي شاغل بالك بشكل خفيف؟",
]

FOLLOWUP_PROMPTS_MSA = [
    "ماذا تقصد؟",
    "اشرحها أكثر.",
    "لم أفهم الفكرة جيدًا.",
    "وضح لي بكلام أبسط.",
    "كيف أطبق ذلك؟",
    "هل تعني أن أبدأ بشيء صغير؟",
    "أريد مثالًا قريبًا.",
    "وماذا أفعل بعد ذلك؟",
]
FOLLOWUP_REPLIES_MSA = [
    "أقصد أن تجعل الأمر أصغر وأسهل، ثم تبدأ بالجزء الواضح.",
    "الفكرة ببساطة: خذ جزءًا واحدًا من الموضوع وتعامل معه أولًا.",
    "مثال قريب: إذا كان الأمر كبيرًا، اختر منه مهمة قصيرة وابدأ بها.",
    "يعني لا تجمع كل شيء في لحظة واحدة؛ افصل الأمر إلى أجزاء صغيرة.",
    "ابدأ بالجزء الأسهل فهمًا، ثم انتقل لما بعده عندما تتضح الصورة.",
]
FOLLOWUP_PROMPTS_SAUDI = [
    "يعني كيف؟",
    "وضح لي أكثر.",
    "ما فهمت عليك.",
    "قصدك أبدأ بشي بسيط؟",
    "طيب كيف أطبقها؟",
    "عطني مثال قريب.",
    "وش تقصد بالضبط؟",
    "وبعدها وش أسوي؟",
]
FOLLOWUP_REPLIES_SAUDI = [
    "أقصد خل الموضوع أصغر، وابدأ بالجزء الواضح قدامك.",
    "يعني لا تجمع كل شيء مرة وحدة؛ خذ جزء بسيط وابدأ فيه.",
    "مثال: إذا عندك أشياء كثيرة، اختر أسهل واحد واشتغل عليه شوي.",
    "القصد إن البداية تكون بسيطة، وبعدها تبني عليها بهدوء.",
    "ابدأ بالشي الأقرب لك، وإذا اتضحت الصورة استمر على نفس الطريق.",
]

PLANNING_TASKS = [
    "دراستي", "عملي", "مهامي المنزلية", "مشاويري", "قراءة كتاب", "ترتيب المكتب",
    "التمرين", "تعلم مهارة", "مراجعة الدروس", "تنظيف الغرفة", "الرد على الرسائل",
    "شراء الاحتياجات", "الاستعداد للموعد", "كتابة ملخص", "ترتيب الملفات",
    "زيارة عائلية", "إصلاح شيء بسيط", "متابعة موعد", "تحضير وجبة", "مراجعة الميزانية",
]
PLANNING_ASKS_MSA = [
    "كيف أنظم {item} اليوم؟",
    "أريد ترتيب {item} بطريقة سهلة.",
    "ساعدني على تقسيم {item}.",
    "ما أفضل طريقة لإنجاز {item} بدون تشتت؟",
    "كيف أبدأ في {item}؟",
    "لدي وقت قليل وأريد إنجاز {item}.",
    "كيف أرتب أولوياتي في {item}؟",
]
PLANNING_REPLIES_MSA = [
    "اكتب ثلاث مهام واضحة، ثم ابدأ بالأهم وحدد له وقتًا قصيرًا.",
    "قسّم العمل إلى مهام صغيرة، وابدأ بالأهم قبل الأشياء السهلة.",
    "اختر ثلاث مهام فقط الآن، ثم ابدأ بالأهم واترك الباقي لوقت لاحق.",
    "حدد الهدف، اكتب المهام، ثم ابدأ بالأهم لمدة عشرين دقيقة.",
    "ابدأ بالأهم، ثم راجع المهام بعد أن تنتهي من الجزء الأول.",
]
PLANNING_ASKS_SAUDI = [
    "كيف أنظم {item} اليوم؟",
    "ابي أرتب {item} بطريقة سهلة.",
    "ساعدني أقسم {item}.",
    "كيف أبدأ في {item} بدون تشتت؟",
    "وش أفضل طريقة أخلص {item}؟",
]
PLANNING_REPLIES_SAUDI = [
    "اكتب ثلاث مهام واضحة، وابدأ بالأهم لمدة قصيرة.",
    "قسمها مهام صغيرة، وابدأ بالأهم قبل الأشياء الجانبية.",
    "اختر ثلاث مهام بس، وابدأ بالأهم ثم شوف اللي بعده.",
    "حدد المطلوب، اكتب المهام، وابدأ بالأهم عشرين دقيقة.",
    "ابدأ بالأهم، وبعد ما تخلص أول جزء راجع باقي المهام.",
]

SUPPORT_SITUATIONS_MSA = [
    "أشعر بتوتر قبل الموعد", "أنا قلق من نتيجة اليوم", "أحس أنني متعب ذهنيًا",
    "تضايقت من كلام أحدهم", "لا أستطيع التركيز الآن", "أشعر أن اليوم ثقيل",
    "أنا محبط قليلًا", "توترت من كثرة المطلوب", "أحتاج أن أهدأ", "أشعر بضغط بسيط",
    "عندي خوف من البداية", "مزاجي منخفض اليوم", "أشعر أنني مستعجل", "أفكر كثيرًا",
]
SUPPORT_REPLIES_MSA = [
    "خذ نفسًا هادئًا، واهدأ قليلًا قبل أن تقرر ما ستفعله.",
    "تنفس ببطء، ثم اختر أمرًا واحدًا تستطيع فعله الآن.",
    "اهدأ لحظة، واكتب ما يزعجك في جملة قصيرة حتى يتضح أمامك.",
    "خذ نفسًا عميقًا، وذكّر نفسك أن المطلوب الآن خطوة صغيرة فقط.",
    "توقف دقيقة، تنفس بهدوء، ثم عد للأمر الأبسط.",
]
SUPPORT_SITUATIONS_SAUDI = [
    "توترت قبل الموعد", "قلقان من اللي بيصير", "حاس إن اليوم ثقيل",
    "تضايقت من كلام أحد", "ماني قادر أركز", "ودي أهدأ شوي",
    "حاس بضغط", "خايف أبدأ", "مزاجي نازل", "أفكر كثير",
    "مضغوط من كثرة الأشياء", "توترت بدون سبب واضح",
]
SUPPORT_REPLIES_SAUDI = [
    "خذ نفس شوي واهدأ، بعدها ابدأ بشي واحد بسيط.",
    "اهدأ دقيقة، تنفس بهدوء، ولا تحمل نفسك كل شيء مرة وحدة.",
    "خففها على نفسك، خذ نفس وابدأ بأقرب شيء واضح.",
    "لا تستعجل، اهدأ شوي واكتب اللي مضايقك بجملة قصيرة.",
    "خذ نفس عميق، وبعدها سو خطوة صغيرة تقدر عليها.",
]

TOPICS_MSA = [
    ("الشجاعة", "أن تفعل الصواب رغم الخوف، لا أن تختفي منك المخاوف."),
    ("الصداقة", "علاقة فيها صدق واهتمام ووقفة وقت الحاجة."),
    ("الصبر", "قدرة على احتمال التأخير أو التعب دون فقدان الاتزان."),
    ("الصدق", "وضوح في القول والعمل بلا خداع."),
    ("الاحترام", "أن تراعي قيمة الشخص وحدوده حتى عند الاختلاف."),
    ("التعاون", "أن يعمل أكثر من شخص لهدف مشترك بتفاهم."),
    ("الهدوء", "حالة تساعدك على التفكير بصفاء قبل التصرف."),
    ("المسؤولية", "أن تعرف ما عليك وتقوم به بقدر استطاعتك."),
    ("الامتنان", "أن تلاحظ الخير الموجود وتشكر عليه."),
    ("الثقة", "اطمئنان مبني على تجربة ووضوح لا على كلام فقط."),
    ("الكرم", "عطاء مناسب بلا منّ ولا مبالغة."),
    ("الاعتذار", "اعتراف بالخطأ ومحاولة إصلاح أثره."),
    ("الإنصات", "أن تسمع لتفهم لا لترد بسرعة."),
    ("المرونة", "قدرة على تغيير الطريقة دون ترك الهدف."),
    ("العدل", "أن تعطي كل ذي حق حقه بإنصاف."),
    ("الحياء", "خلق يحفظ الاحترام دون أن يمنع قول الحق."),
    ("الطموح", "رغبة واعية في التحسن والعمل لما هو أفضل."),
    ("التواضع", "أن تعرف قيمتك دون أن تتكبر على غيرك."),
    ("الحكمة", "اختيار التصرف الأنسب في الوقت الأنسب."),
    ("الوفاء", "الثبات على العهد وحفظ المعروف."),
]
TOPIC_ASKS_MSA = [
    "ما معنى {topic}؟",
    "اشرح لي {topic} ببساطة.",
    "أريد فهم {topic} بكلام سهل.",
    "ما المقصود بـ {topic}؟",
    "كيف أفهم {topic} في الحياة اليومية؟",
]

TOPICS_SAUDI = [
    ("الشجاعة", "إنك تسوي الصح حتى لو كنت خايف."),
    ("الصداقة", "رفقة طيبة ووقفة صادقة وقت الحاجة."),
    ("الصبر", "إنك تتحمل شوي بدون ما تفقد هدوءك."),
    ("الصدق", "إن كلامك يكون واضح وما فيه خداع."),
    ("الاحترام", "إنك تقدر الناس وحدودهم حتى لو اختلفت معهم."),
    ("التعاون", "إنكم تمشون مع بعض لهدف واحد."),
    ("الهدوء", "إنك تهدي نفسك عشان تفكر أوضح."),
    ("المسؤولية", "إنك تعرف اللي عليك وتسويه بقدر قدرتك."),
    ("الامتنان", "إنك تنتبه للنعم وتشكر عليها."),
    ("الثقة", "اطمئنان يجي من مواقف واضحة وتجربة."),
    ("الكرم", "عطاء طيب بدون منّة."),
    ("الاعتذار", "إنك تعترف بالغلط وتحاول تصلحه."),
    ("الإنصات", "إنك تسمع عشان تفهم، مو بس ترد."),
    ("المرونة", "إنك تغير طريقتك إذا احتجت وتبقى على هدفك."),
    ("العدل", "إنك تنصف الناس وتعطي كل واحد حقه."),
    ("الطموح", "رغبة إنك تتحسن وتوصل لشي أفضل."),
]
TOPIC_ASKS_SAUDI = [
    "{topic} وش تعني؟",
    "وش معنى {topic}؟",
    "اشرح لي {topic} بكلام بسيط.",
    "ابي أفهم {topic}.",
    "{topic} كيف تكون بالحياة؟",
]


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Author Phase 27.81 balanced family pack")
    p.add_argument("--out", type=Path, default=OUT)
    p.add_argument("--report", type=Path, default=REPORT)
    p.add_argument("--decision", type=Path, default=DECISION)
    p.add_argument("--doc", type=Path, default=DOC)
    return p.parse_args()


def _provenance(family: str, dialect: str, index: int) -> dict[str, object]:
    return {
        "source": "sf-ai-balanced-family-pack-v1",
        "license": "owner-approved-for-sf-ai-training",
        "language": "ar",
        "dialect": dialect,
        "quality": "gold",
        "training_allowed": True,
        "owner_user_id": "sami-local",
        "created_by_user_id": "sf-ai-local-author",
        "target_user_id": "sami-local",
        "user_scope": "single_user",
        "dialogue_family": family,
        "prompt_family": family,
        "answer_family": family,
        "pack_id": "phase27_81_balanced_family_pack_v1",
        "pack_index": index,
        "notes": "owner-delegated natural Arabic/Saudi dialogue; no external dataset; no pretrained output",
    }


def _record(user: str, assistant: str, family: str, dialect: str, index: int) -> dict[str, object]:
    return {
        "domain": "chat",
        "lang": "ar",
        "messages": [
            {"role": "user", "content": user},
            {"role": "assistant", "content": assistant},
        ],
        "provenance": _provenance(family, dialect, index),
    }


def _planning_msa(count: int) -> list[dict[str, object]]:
    rows = []
    for i in range(count):
        item = PLANNING_TASKS[i % len(PLANNING_TASKS)]
        ask = PLANNING_ASKS_MSA[(i // len(PLANNING_TASKS)) % len(PLANNING_ASKS_MSA)]
        reply = PLANNING_REPLIES_MSA[(i + (i // 7)) % len(PLANNING_REPLIES_MSA)]
        rows.append(_record(ask.format(item=item), reply, "planning", "msa", i + 1))
    return rows


def _open_social_msa(count: int) -> list[dict[str, object]]:
    rows = []
    for i in range(count):
        user = OPEN_SOCIAL_PROMPTS_MSA[i % len(OPEN_SOCIAL_PROMPTS_MSA)]
        assistant = OPEN_SOCIAL_REPLIES_MSA[(i + (i // 8)) % len(OPEN_SOCIAL_REPLIES_MSA)]
        rows.append(_record(user, assistant, "open_social", "msa", i + 1))
    return rows


def _open_social_saudi(count: int) -> list[dict[str, object]]:
    rows = []
    for i in range(count):
        user = OPEN_SOCIAL_PROMPTS_SAUDI[i % len(OPEN_SOCIAL_PROMPTS_SAUDI)]
        assistant = OPEN_SOCIAL_REPLIES_SAUDI[(i + (i // 8)) % len(OPEN_SOCIAL_REPLIES_SAUDI)]
        rows.append(_record(user, assistant, "open_social", "saudi", i + 1))
    return rows


def _followup_msa(count: int) -> list[dict[str, object]]:
    rows = []
    for i in range(count):
        user = FOLLOWUP_PROMPTS_MSA[i % len(FOLLOWUP_PROMPTS_MSA)]
        assistant = FOLLOWUP_REPLIES_MSA[(i + (i // 8)) % len(FOLLOWUP_REPLIES_MSA)]
        rows.append(_record(user, assistant, "followup", "msa", i + 1))
    return rows


def _followup_saudi(count: int) -> list[dict[str, object]]:
    rows = []
    for i in range(count):
        user = FOLLOWUP_PROMPTS_SAUDI[i % len(FOLLOWUP_PROMPTS_SAUDI)]
        assistant = FOLLOWUP_REPLIES_SAUDI[(i + (i // 8)) % len(FOLLOWUP_REPLIES_SAUDI)]
        rows.append(_record(user, assistant, "followup", "saudi", i + 1))
    return rows


def _planning_saudi(count: int) -> list[dict[str, object]]:
    rows = []
    for i in range(count):
        item = PLANNING_TASKS[i % len(PLANNING_TASKS)]
        ask = PLANNING_ASKS_SAUDI[(i // len(PLANNING_TASKS)) % len(PLANNING_ASKS_SAUDI)]
        reply = PLANNING_REPLIES_SAUDI[(i + (i // 7)) % len(PLANNING_REPLIES_SAUDI)]
        rows.append(_record(ask.format(item=item), reply, "planning", "saudi", i + 1))
    return rows


def _support_msa(count: int) -> list[dict[str, object]]:
    rows = []
    for i in range(count):
        situation = SUPPORT_SITUATIONS_MSA[i % len(SUPPORT_SITUATIONS_MSA)]
        reply = SUPPORT_REPLIES_MSA[(i + (i // 5)) % len(SUPPORT_REPLIES_MSA)]
        rows.append(_record(f"{situation}، ماذا أفعل؟", reply, "support", "msa", i + 1))
    return rows


def _support_saudi(count: int) -> list[dict[str, object]]:
    rows = []
    for i in range(count):
        situation = SUPPORT_SITUATIONS_SAUDI[i % len(SUPPORT_SITUATIONS_SAUDI)]
        reply = SUPPORT_REPLIES_SAUDI[(i + (i // 4)) % len(SUPPORT_REPLIES_SAUDI)]
        rows.append(_record(f"{situation} وش أسوي؟", reply, "support", "saudi", i + 1))
    return rows


def _topic_msa(count: int) -> list[dict[str, object]]:
    rows = []
    for i in range(count):
        topic, meaning = TOPICS_MSA[i % len(TOPICS_MSA)]
        ask = TOPIC_ASKS_MSA[(i // len(TOPICS_MSA)) % len(TOPIC_ASKS_MSA)]
        answer = f"معنى {topic}: {meaning}"
        rows.append(_record(ask.format(topic=topic), answer, "topic", "msa", i + 1))
    return rows


def _topic_saudi(count: int) -> list[dict[str, object]]:
    rows = []
    for i in range(count):
        topic, meaning = TOPICS_SAUDI[i % len(TOPICS_SAUDI)]
        ask = TOPIC_ASKS_SAUDI[(i // len(TOPICS_SAUDI)) % len(TOPIC_ASKS_SAUDI)]
        answer = f"معنى {topic}: {meaning}"
        rows.append(_record(ask.format(topic=topic), answer, "topic", "saudi", i + 1))
    return rows


def _rows_for(quota: Quota) -> list[dict[str, object]]:
    if quota.family == "open_social" and quota.dialect == "msa":
        return _open_social_msa(quota.count)
    if quota.family == "open_social" and quota.dialect == "saudi":
        return _open_social_saudi(quota.count)
    if quota.family == "followup" and quota.dialect == "msa":
        return _followup_msa(quota.count)
    if quota.family == "followup" and quota.dialect == "saudi":
        return _followup_saudi(quota.count)
    if quota.family == "planning" and quota.dialect == "msa":
        return _planning_msa(quota.count)
    if quota.family == "planning" and quota.dialect == "saudi":
        return _planning_saudi(quota.count)
    if quota.family == "support" and quota.dialect == "msa":
        return _support_msa(quota.count)
    if quota.family == "support" and quota.dialect == "saudi":
        return _support_saudi(quota.count)
    if quota.family == "topic" and quota.dialect == "msa":
        return _topic_msa(quota.count)
    if quota.family == "topic" and quota.dialect == "saudi":
        return _topic_saudi(quota.count)
    raise ValueError(f"unsupported quota: {quota}")


def _write_jsonl(path: Path, rows: Iterable[dict[str, object]]) -> int:
    materialized = list(rows)
    path.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in materialized),
        encoding="utf-8",
    )
    return len(materialized)


def _write_card(path: Path, quota: Quota, count: int) -> None:
    text = "\n".join(
        [
            f"# {path.name}",
            "",
            "- phase: Phase 27.81",
            "- source: sf-ai-balanced-family-pack-v1",
            "- license: owner-approved-for-sf-ai-training",
            f"- dialect: {quota.dialect}",
            f"- dialogue_family: {quota.family}",
            f"- records: {count}",
            "- quality: gold",
            "- training_allowed: true",
            "- external_dataset_used: false",
            "- pretrained_output_used: false",
            "",
        ]
    )
    path.with_suffix(".CARD.md").write_text(text, encoding="utf-8")


def main() -> int:
    args = parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    generated = []
    total = 0
    for quota in QUOTAS:
        rows = _rows_for(quota)
        path = args.out / quota.filename
        count = _write_jsonl(path, rows)
        _write_card(path, quota, count)
        total += count
        generated.append(
            {
                "file": str(path.relative_to(ROOT)),
                "card": str(path.with_suffix(".CARD.md").relative_to(ROOT)),
                "family": quota.family,
                "dialect": quota.dialect,
                "records": count,
            }
        )

    decision = {
        "decision_id": "PHASE27_81_BALANCED_FAMILY_PACK_DECISION",
        "engineering_decision": "BALANCED_FAMILY_PACK_AUTHORED_RERUN_AUDITS_AND_GATES",
        "new_training_allowed": False,
        "tokenizer_retrain_allowed": False,
        "runtime_release_allowed": False,
        "sf50m_justified_transition": False,
        "next_step": "run corpus audit, rebuild split, rerun Phase 27.80 repair gate validation",
    }
    report = {
        "phase": "Phase 27.81",
        "status": "PHASE27_81_BALANCED_FAMILY_PACK_AUTHORED_NO_TRAINING",
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "training_started": False,
        "tokenizer_training_started": False,
        "runtime_changed": False,
        "source": "sf-ai-balanced-family-pack-v1",
        "license": "owner-approved-for-sf-ai-training",
        "total_records": total,
        "generated": generated,
        "decision": decision,
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    args.decision.write_text(json.dumps(decision, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    args.doc.write_text(
        "\n".join(
            [
                "# Phase 27.81 — Balanced Family Pack",
                "",
                "هذه مرحلة تأليف بيانات فقط، بلا تدريب.",
                "",
                f"- total records: `{total}`",
                "- open_social/followup/planning/support/topic: `500` لكل عائلة",
                "- dialect per family: `250 msa + 250 saudi`",
                "- training allowed by this phase: `false`",
                "",
                "## Generated Files",
                "",
                *[f"- `{item['file']}`: {item['records']} {item['dialect']} {item['family']}" for item in generated],
                "",
                "## Next",
                "",
                "Run corpus audit, rebuild dialogue split, and rerun Phase 27.80 repair gates.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print("SF.AI — Phase 27.81 balanced family pack")
    print(f"records: {total}")
    print(f"report: {args.report.relative_to(ROOT)}")
    print(f"decision: {args.decision.relative_to(ROOT)}")
    print(f"doc: {args.doc.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
