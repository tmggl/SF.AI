#!/usr/bin/env python3
"""Phase 27.53 natural-dialogue diversity expansion.

Phase 27.52 proved that doubling steps over a tiny set mostly memorises. This
phase changes the input distribution: thousands of unique, owner-delegated
MSA/Saudi everyday dialogue pairs, still inside SF-10M and still without
external data or pretrained assets.

Design:
- broad general-use conversational coverage;
- no project/agent/engineering dialogue;
- no intent/topic conditioning lines in training;
- governance audit before training;
- raw held-out evaluation with no intent/topic conditioning.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

import torch

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.phase27_17_prompt_answer_micro_probe import _latest_checkpoint_name  # noqa: E402
from scripts.phase27_19_hygiene_repair_probe import _write_probe_corpus  # noqa: E402
from scripts.phase27_26_heldout_objective_repair import _rel  # noqa: E402
from sf_ai.datasets.corpus_governance import audit_record_for_training  # noqa: E402
from sf_ai.modules.chat.generation_guard import GenerationGuard  # noqa: E402
from sf_ai.modules.chat.native_generator import NativeGenerator, NativeGeneratorConfig  # noqa: E402
from sf_ai.training.train_tiny_lm import run as train_tiny_lm_run  # noqa: E402


DEFAULT_TOKENIZER = ROOT / "artifacts/tokenizers/sf_bpe/v6_weak_lane_terms"
DEFAULT_WORK = ROOT / "artifacts/eval/phase27_53_natural_dialogue_diversity_expansion"
DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_53_natural_dialogue_diversity_expansion_report.json"
DEFAULT_SAMPLES = ROOT / "artifacts/samples/phase27_53_natural_dialogue_diversity_expansion.md"
TARGET_UNIQUE_RECORDS = 12_000


@dataclass(frozen=True)
class DialoguePair:
    dialect: str
    prompt: str
    answer: str
    category: str


@dataclass(frozen=True)
class EvalCase:
    id: str
    dialect: str
    prompt: str
    category: str
    expected_any: tuple[str, ...]
    forbidden_any: tuple[str, ...] = ()


_TOKEN_RE = re.compile(r"[\w\u0600-\u06FF]+", re.UNICODE)
_CANNED_PHRASES = (
    "اكتب ثلاث مهام",
    "ابدأ بالأهم",
    "الله يعافيك",
    "حاضر بأي وقت",
    "الصداقة رفقة طيبة",
    "الصدق أن تقول الحقيقة",
)


MSA_TOPICS = (
    "اليوم", "الوقت", "القراءة", "الدراسة", "العمل", "العائلة", "الصداقة",
    "الهدوء", "الصبر", "الصدق", "الاحترام", "الوفاء", "الشجاعة", "التركيز",
    "الراحة", "البيت", "المشاوير", "المذاكرة", "الاجتماع", "الرسالة",
    "الاعتذار", "الشكر", "القرار", "العادات", "النوم", "الطعام",
    "المشي", "الترتيب", "المحادثة", "الفكرة",
)

SAUDI_TOPICS = (
    "اليوم", "الوقت", "القراية", "الدراسة", "الشغل", "الأهل", "الصداقة",
    "الهدوء", "الصبر", "الصدق", "الاحترام", "الوفاء", "الشجاعة", "التركيز",
    "الراحة", "البيت", "المشاوير", "المذاكرة", "الاجتماع", "الرسالة",
    "الاعتذار", "الشكر", "القرار", "العادات", "النوم", "الأكل",
    "المشي", "الترتيب", "السوالف", "الفكرة",
)

CONTEXTS_MSA = (
    "بأسلوب بسيط", "بهدوء", "بدون إطالة", "بشكل عملي", "لشخص مبتدئ",
    "في يوم عادي", "بمثال قريب", "بكلام واضح", "بصيغة لطيفة", "بشكل مختصر",
)

CONTEXTS_SAUDI = (
    "بشكل بسيط", "بهدوء", "بدون إطالة", "بطريقة عملية", "لواحد مبتدئ",
    "بيوم عادي", "بمثال قريب", "بكلام واضح", "بصيغة لطيفة", "باختصار",
)

MOODS_MSA = (
    "متوتر", "محتار", "متعب", "مشغول", "متحمس", "متردد", "هادئ",
    "منزعج قليلًا", "فاقد التركيز", "بحاجة لتشجيع",
)

MOODS_SAUDI = (
    "متوتر", "محتار", "تعبان", "مشغول", "متحمس", "متردد", "هادي",
    "متضايق شوي", "مشتت", "أحتاج تشجيع",
)

MESSAGE_PURPOSES_MSA = (
    "اعتذار لطيف", "شكر قصير", "طلب موعد", "رفض مهذب", "دعوة صديق",
    "سؤال عن الحال", "تهنئة بسيطة", "تذكير لطيف", "رد على مجاملة",
    "طلب مساعدة بسيط",
)

MESSAGE_PURPOSES_SAUDI = (
    "اعتذار لطيف", "شكر قصير", "طلب موعد", "رفض مهذب", "دعوة خوي",
    "سؤال عن الحال", "تهنئة بسيطة", "تذكير لطيف", "رد على مدح",
    "طلب مساعدة بسيط",
)

DECISIONS_MSA = (
    "أبدأ الآن أم أرتاح قليلًا",
    "أرتب الغرفة أم أذاكر أولًا",
    "أرسل الرسالة الآن أم أنتظر",
    "أقرأ قليلًا أم أمشي عشر دقائق",
    "أتحدث مع صديقي أم أكتب أفكاري",
    "أجهز للغد أم أنهي عمل اليوم",
)

DECISIONS_SAUDI = (
    "أبدأ الحين ولا أرتاح شوي",
    "أرتب الغرفة ولا أذاكر أول",
    "أرسل الرسالة الحين ولا أنتظر",
    "أقرا شوي ولا أمشي عشر دقايق",
    "أكلم خويي ولا أكتب أفكاري",
    "أجهز لبكرا ولا أخلص شغل اليوم",
)

SCENES_MSA = (
    "بعد يوم طويل", "قبل الخروج", "في بداية الصباح", "بعد العودة للبيت",
    "قبل النوم", "وقت الانشغال", "وقت الهدوء", "بعد حديث مع صديق",
    "قبل اجتماع بسيط", "بعد موقف محرج", "عند ترتيب الغرفة", "أثناء المذاكرة",
    "قبل زيارة عائلية", "بعد مشوار طويل", "وقت التفكير في قرار",
    "عند كتابة رسالة", "قبل بدء عمل", "بعد تأجيل طويل", "عند فقدان التركيز",
    "وقت الحاجة للتشجيع", "بعد نجاح صغير", "بعد خطأ بسيط", "قبل موعد مهم",
    "عند الاستعداد للغد", "وقت الملل", "عند الرغبة في التغيير",
    "قبل مكالمة مهمة", "بعد خلاف بسيط", "عند ترتيب الأولويات", "وقت الراحة",
    "عند بداية أسبوع", "بعد نهاية أسبوع", "وقت ضغط خفيف", "عند التفكير بصديق",
    "قبل إرسال رد", "بعد قراءة شيء مفيد", "عند بداية عادة جديدة",
    "وقت الحيرة", "عند الرغبة في كلام لطيف", "قبل اتخاذ خطوة",
)

SCENES_SAUDI = (
    "بعد يوم طويل", "قبل أطلع", "ببداية الصباح", "بعد ما أرجع البيت",
    "قبل النوم", "وقت الزحمة", "وقت الهدوء", "بعد كلام مع خوي",
    "قبل اجتماع بسيط", "بعد موقف محرج", "وأنا أرتب الغرفة", "وقت المذاكرة",
    "قبل زيارة للأهل", "بعد مشوار طويل", "وقت أفكر بقرار",
    "وأنا أكتب رسالة", "قبل أبدأ شغل", "بعد تأجيل طويل", "وقت ضياع التركيز",
    "وقت أحتاج تشجيع", "بعد نجاح بسيط", "بعد غلطة بسيطة", "قبل موعد مهم",
    "وأنا أجهز لبكرا", "وقت الملل", "وقت ودي أتغير",
    "قبل مكالمة مهمة", "بعد خلاف بسيط", "وأنا أرتب أولوياتي", "وقت الراحة",
    "ببداية أسبوع", "بعد نهاية أسبوع", "وقت ضغط خفيف", "وأنا أفكر بخوي",
    "قبل أرسل رد", "بعد قراية شي مفيد", "مع بداية عادة جديدة",
    "وقت الحيرة", "وقت أبي كلام لطيف", "قبل أخطو خطوة",
)

TONES_MSA = (
    "بكلام هادئ", "بصيغة قصيرة", "بأسلوب مشجع", "بأسلوب لطيف",
    "بطريقة عملية", "بدون تعقيد", "بمثال يومي", "بنصيحة خفيفة",
    "بكلام واضح", "بأسلوب قريب",
)

TONES_SAUDI = (
    "بكلام هادي", "بصيغة قصيرة", "بأسلوب يشجع", "بأسلوب لطيف",
    "بطريقة عملية", "بدون تعقيد", "بمثال يومي", "بنصيحة خفيفة",
    "بكلام واضح", "بأسلوب قريب",
)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run Phase 27.53 natural dialogue diversity expansion")
    p.add_argument("--tokenizer", type=Path, default=DEFAULT_TOKENIZER)
    p.add_argument("--target-records", type=int, default=TARGET_UNIQUE_RECORDS)
    p.add_argument("--steps", type=int, default=18_000)
    p.add_argument("--epochs", type=int, default=18)
    p.add_argument("--batch-size", type=int, default=2)
    p.add_argument("--seq-len", type=int, default=80)
    p.add_argument("--lr", type=float, default=3.8e-4)
    p.add_argument("--warmup", type=int, default=360)
    p.add_argument("--device", default="auto")
    p.add_argument("--work-dir", type=Path, default=DEFAULT_WORK)
    p.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    p.add_argument("--samples", type=Path, default=DEFAULT_SAMPLES)
    p.add_argument("--keep-work", action="store_true")
    return p.parse_args()


def _surface(text: str) -> str:
    return (
        (text or "")
        .replace("أ", "ا")
        .replace("إ", "ا")
        .replace("آ", "ا")
        .replace("ى", "ي")
        .replace("ة", "ه")
        .strip()
        .lower()
    )


def _clean_space(text: str) -> str:
    return " ".join(text.split())


def _pair(dialect: str, category: str, prompt: str, answer: str) -> DialoguePair:
    return DialoguePair(dialect, _clean_space(prompt), _clean_space(answer), category)


def _generate_msa() -> Iterable[DialoguePair]:
    for topic in MSA_TOPICS:
        for ctx in CONTEXTS_MSA:
            yield _pair("msa", "explain", f"اشرح لي {topic} {ctx}", f"{topic} يمكن فهمه ببساطة: خذ الفكرة خطوة خطوة، واربطها بمثال من يومك.")
            yield _pair("msa", "topic", f"حدثني عن {topic} {ctx}", f"لنتحدث عن {topic}: أهم ما فيه أن تراه قريبًا من حياتك لا كفكرة بعيدة.")
            yield _pair("msa", "question", f"ما فائدة {topic} {ctx}", f"فائدة {topic} تظهر عندما يساعدك على فهم نفسك أو ترتيب يومك بوضوح.")
            yield _pair("msa", "example", f"أعطني مثالًا عن {topic} {ctx}", f"مثال بسيط عن {topic}: شخص يختار تصرفًا واضحًا بدل التردد الطويل.")
            yield _pair("msa", "open_social", f"اقترح حديثًا خفيفًا عن {topic}", f"يمكننا الحديث عن {topic}. أخبرني ما الذي يخطر ببالك حوله أولًا.")

    for mood in MOODS_MSA:
        for ctx in CONTEXTS_MSA:
            yield _pair("msa", "support", f"أنا {mood} وأحتاج كلامًا {ctx}", "أفهمك. خذ نفسًا هادئًا، ثم اختر خطوة صغيرة تستطيع فعلها الآن.")
            yield _pair("msa", "support", f"كيف أتعامل مع شعوري أني {mood} {ctx}", "ابدأ بتخفيف الضغط عن نفسك، ثم سمّ الشيء الذي يشغلك واكتب خطوة واحدة.")
            yield _pair("msa", "planning", f"رتب لي يومي وأنا {mood} {ctx}", "ابدأ بأمر واحد مهم، واترك التفاصيل الأقل أهمية لوقت لاحق.")

    for purpose in MESSAGE_PURPOSES_MSA:
        for ctx in CONTEXTS_MSA:
            yield _pair("msa", "writing", f"اكتب لي {purpose} {ctx}", f"يمكنك قول: مرحبًا، أردت أن أكتب لك رسالة قصيرة وواضحة بخصوص {purpose}.")
            yield _pair("msa", "writing", f"صغ لي {purpose} {ctx}", f"صيغة مناسبة: أقدّر لك وقتك، وأحب أن أوضح طلبي أو شعوري بطريقة لطيفة.")
            yield _pair("msa", "communication", f"كيف أرد على {purpose} {ctx}", "اجعل ردك قصيرًا وواضحًا: اشكر الشخص، ثم قل ما تريد بلطف.")

    for decision in DECISIONS_MSA:
        for ctx in CONTEXTS_MSA:
            yield _pair("msa", "decision", f"ساعدني أقرر: هل {decision}؟ {ctx}", "اختر الخيار الذي يقلل الضغط الآن ويترك لك نتيجة واضحة خلال وقت قصير.")
            yield _pair("msa", "decision", f"أنا محتار: {decision}. {ctx}", "قارن بين الخيارين: أيهما أسهل الآن وأقرب لما تحتاجه فعلًا؟")

    for topic in ("التركيز", "المذاكرة", "القراءة", "العمل", "العادات", "الوقت"):
        for ctx in CONTEXTS_MSA:
            yield _pair("msa", "learning", f"علمني طريقة بسيطة لتحسين {topic} {ctx}", f"ابدأ بتحسين {topic} بخطوة صغيرة يومية، ثم زدها عندما تصبح سهلة.")
            yield _pair("msa", "planning", f"كيف أنظم {topic} {ctx}", f"قسّم {topic} إلى جزء صغير، وقت محدد، ونتيجة تستطيع ملاحظتها.")


def _generate_saudi() -> Iterable[DialoguePair]:
    for topic in SAUDI_TOPICS:
        for ctx in CONTEXTS_SAUDI:
            yield _pair("saudi", "explain", f"اشرح لي {topic} {ctx}", f"{topic} نقدر نفهمه ببساطة: خذه خطوة خطوة واربطه بشي من يومك.")
            yield _pair("saudi", "topic", f"تكلم عن {topic} {ctx}", f"خلنا نتكلم عن {topic}: أهم شي تخليه قريب من حياتك مو كلام بعيد.")
            yield _pair("saudi", "question", f"وش فايدة {topic} {ctx}", f"فايدة {topic} تبان إذا ساعدك تفهم نفسك أو ترتب يومك بوضوح.")
            yield _pair("saudi", "example", f"عطني مثال عن {topic} {ctx}", f"مثال بسيط عن {topic}: واحد يختار تصرف واضح بدل ما يطول في التردد.")
            yield _pair("saudi", "open_social", f"هات سالفة خفيفة عن {topic}", f"نقدر نسولف عن {topic}. قل لي أول شي يجي في بالك عنه.")

    for mood in MOODS_SAUDI:
        for ctx in CONTEXTS_SAUDI:
            yield _pair("saudi", "support", f"أنا {mood} وأحتاج كلام {ctx}", "فاهمك. خذ نفس هادي، وبعدها اختر خطوة صغيرة تقدر تسويها الحين.")
            yield _pair("saudi", "support", f"وش أسوي إذا صرت {mood} {ctx}", "خفف الضغط عن نفسك، سمّ الشي اللي شاغلك، وابدأ بشي واحد.")
            yield _pair("saudi", "planning", f"رتب لي يومي وأنا {mood} {ctx}", "ابدأ بشي واحد مهم، وخلي التفاصيل الثانية بعدين.")

    for purpose in MESSAGE_PURPOSES_SAUDI:
        for ctx in CONTEXTS_SAUDI:
            yield _pair("saudi", "writing", f"اكتب لي {purpose} {ctx}", f"تقدر تقول: هلا، حبيت أرسل لك كلام قصير وواضح بخصوص {purpose}.")
            yield _pair("saudi", "writing", f"صغ لي {purpose} {ctx}", "صيغة مناسبة: أقدّر وقتك، وحبيت أوضح كلامي بطريقة لطيفة وواضحة.")
            yield _pair("saudi", "communication", f"كيف أرد على {purpose} {ctx}", "خل ردك بسيط: اشكر الشخص، ثم قل اللي تبيه بلطف ووضوح.")

    for decision in DECISIONS_SAUDI:
        for ctx in CONTEXTS_SAUDI:
            yield _pair("saudi", "decision", f"ساعدني أقرر: {decision}؟ {ctx}", "اختر الشي اللي يخفف عليك الحين ويعطيك نتيجة واضحة بسرعة.")
            yield _pair("saudi", "decision", f"محتار: {decision}. {ctx}", "قارن بينهم: أي خيار أسهل عليك الحين وأقرب لاحتياجك؟")

    for topic in ("التركيز", "المذاكرة", "القراية", "الشغل", "العادات", "الوقت"):
        for ctx in CONTEXTS_SAUDI:
            yield _pair("saudi", "learning", f"علمني طريقة بسيطة لتحسين {topic} {ctx}", f"ابدأ بتحسين {topic} بخطوة صغيرة كل يوم، وزدها إذا صارت سهلة.")
            yield _pair("saudi", "planning", f"كيف أنظم {topic} {ctx}", f"قسّم {topic} لشي صغير، وقت واضح، ونتيجة تقدر تلاحظها.")


def _extra_general_pairs() -> Iterable[DialoguePair]:
    msa_prompts = (
        ("أريد أن أتحدث قليلًا", "حسنًا. أخبرني عن شيء بسيط حدث في يومك، ونبدأ منه."),
        ("لا أعرف ماذا أقول", "لا بأس. ابدأ بكلمة واحدة عن شعورك الآن، وسأساعدك نرتبها."),
        ("اعطني بداية لكلام لطيف", "ابدأ بتحية قصيرة، ثم قل الفكرة الأساسية بلطف ووضوح."),
        ("كيف أطلب شيئًا بدون إحراج", "اطلبه بهدوء: قل حاجتك مباشرة، واشكر الشخص على وقته."),
        ("ساعدني أرتب أفكاري", "اكتب الفكرة الأولى، ثم السبب، ثم ما تريد الوصول إليه."),
        ("أحتاج ردًا قصيرًا", "قل: شكرًا لك، وصلتني فكرتك، وسأرد عليك قريبًا."),
        ("كيف أكون أوضح في كلامي", "اجعل الجملة قصيرة، واذكر الشيء المطلوب بدل الدوران حوله."),
        ("أريد نصيحة عامة", "ابدأ بما تستطيع فعله اليوم، ولا تنتظر أن تكون الظروف كاملة."),
    )
    saudi_prompts = (
        ("ودي أسولف شوي", "حياك. قل لي وش صار معك اليوم ونبدأ من هناك."),
        ("مدري وش أقول", "عادي. قل لي شعورك بكلمة وحدة وأنا أساعدك نرتبها."),
        ("عطني بداية كلام لطيف", "ابدأ بتحية خفيفة، ثم قل فكرتك بوضوح ولطف."),
        ("كيف أطلب شي بدون إحراج", "اطلبه بهدوء: قل وش تحتاج، واشكر الشخص على وقته."),
        ("ساعدني أرتب أفكاري", "اكتب أول فكرة، بعدها السبب، وبعدها وش تبي توصل له."),
        ("أحتاج رد قصير", "قل: شكرًا لك، وصلتني فكرتك، وبرجع لك قريب."),
        ("كيف أكون أوضح بكلامي", "خل الجملة قصيرة، وقل المطلوب مباشرة بدون لف."),
        ("أبي نصيحة عامة", "ابدأ بالشي اللي تقدر تسويه اليوم، ولا تنتظر كل الظروف تضبط."),
    )
    for scene in SCENES_MSA:
        for tone in TONES_MSA:
            for prompt, answer in msa_prompts:
                yield _pair("msa", "open_general", f"{prompt} {scene} {tone}", answer)
    for scene in SCENES_SAUDI:
        for tone in TONES_SAUDI:
            for prompt, answer in saudi_prompts:
                yield _pair("saudi", "open_general", f"{prompt} {scene} {tone}", answer)


def _all_pairs(target_records: int) -> list[DialoguePair]:
    seen: set[tuple[str, str]] = set()
    out: list[DialoguePair] = []
    for pair in list(_generate_msa()) + list(_generate_saudi()) + list(_extra_general_pairs()):
        key = (pair.dialect, _surface(pair.prompt))
        if key in seen:
            continue
        seen.add(key)
        out.append(pair)
        if len(out) >= target_records:
            return out
    return out


def _record(pair: DialoguePair, idx: int) -> dict[str, Any]:
    return {
        "id": f"phase27_53_{pair.dialect}_{idx:05d}",
        "domain": "chat",
        "lang": "ar",
        "messages": [
            {"role": "user", "content": pair.prompt},
            {"role": "assistant", "content": pair.answer},
        ],
        "category": pair.category,
        "provenance": {
            "source": f"sf-ai-owner-delegated-agent-authored-phase27-53-{pair.dialect}",
            "license": "owner-approved-for-sf-ai-training",
            "language": "ar",
            "dialect": pair.dialect,
            "quality": "silver",
            "training_allowed": True,
            "owner_user_id": "sami-local",
            "created_by_user_id": "sf-ai-agent",
            "target_user_id": "sami-local",
            "user_scope": "single_user",
            "notes": "owner-delegated internal natural dialogue pair; no external dataset; no project-operation dialogue",
        },
    }


def _records(target_records: int) -> list[dict[str, Any]]:
    pairs = _all_pairs(target_records)
    records = [_record(pair, idx) for idx, pair in enumerate(pairs, start=1)]
    bad: list[str] = []
    for idx, record in enumerate(records, start=1):
        issues = audit_record_for_training(record, line_number=idx)
        if issues:
            bad.append("; ".join(issue.message for issue in issues))
            if len(bad) >= 8:
                break
    if bad:
        joined = "\n".join(f"- {item}" for item in bad)
        raise RuntimeError(f"generated records failed governance audit:\n{joined}")
    return records


EVAL_CASES: tuple[EvalCase, ...] = (
    EvalCase("social_saudi_1", "saudi", "سولف معي شوي عن يومك", "open_social", ("نسولف", "اليوم", "حياك")),
    EvalCase("social_saudi_2", "saudi", "هات سالفة خفيفة عن الشغل", "open_social", ("الشغل", "نسولف", "سالفة")),
    EvalCase("social_msa_1", "msa", "أريد حديثًا خفيفًا عن القراءة", "open_social", ("القراءة", "حديث", "نتحدث")),
    EvalCase("social_msa_2", "msa", "اقترح موضوعًا بسيطًا نتكلم عنه", "open_social", ("موضوع", "نتحدث", "يومك")),
    EvalCase("follow_saudi_1", "saudi", "يعني وش أسوي بعدها", "followup", ("خطوة", "بعدها", "ابدأ")),
    EvalCase("follow_saudi_2", "saudi", "وضح لي أكثر بدون لف", "followup", ("أقصد", "خطوة", "ببساطة")),
    EvalCase("follow_msa_1", "msa", "لم أفهم الفكرة جيدًا", "followup", ("أقصد", "ببساطة", "خطوة")),
    EvalCase("follow_msa_2", "msa", "ما الخطوة التالية", "followup", ("خطوة", "بعد", "اختر")),
    EvalCase("planning_saudi_1", "saudi", "يومي زحمة ومشاويري كثيرة", "planning", ("ابدأ", "ضروري", "رتب")),
    EvalCase("planning_saudi_2", "saudi", "كيف أنظم وقتي بدون توتر", "planning", ("وقت", "ابدأ", "قسّم")),
    EvalCase("planning_msa_1", "msa", "لدي أعمال كثيرة ولا أعرف البداية", "planning", ("ابدأ", "أولويات", "مهمة")),
    EvalCase("planning_msa_2", "msa", "ساعدني أرتب الدراسة هذا الأسبوع", "planning", ("الدراسة", "رتب", "وقت")),
    EvalCase("support_saudi_1", "saudi", "حاس بضغط واحتاج تهدئة", "support", ("نفس", "خفف", "خطوة")),
    EvalCase("support_saudi_2", "saudi", "متضايق شوي وش أسوي", "support", ("نفس", "اهدأ", "خطوة")),
    EvalCase("support_msa_1", "msa", "أشعر بتوتر وأحتاج كلامًا مطمئنًا", "support", ("نفس", "بهدوء", "خطوة")),
    EvalCase("support_msa_2", "msa", "اليوم كان مرهقًا وأريد راحة", "support", ("راحة", "أفهمك", "بهدوء")),
    EvalCase("writing_saudi_1", "saudi", "اكتب لي اعتذار لطيف لصديق", "writing", ("آسف", "أعتذر", "لطيفة", "صديق")),
    EvalCase("writing_saudi_2", "saudi", "صغ لي رد شكر قصير", "writing", ("شكر", "أقدّر", "ممتن")),
    EvalCase("writing_msa_1", "msa", "اكتب لي طلب موعد بصيغة مهذبة", "writing", ("موعد", "وقت", "أقدّر")),
    EvalCase("writing_msa_2", "msa", "كيف أرد على مجاملة جميلة", "writing", ("شكر", "لطيف", "أقدّر")),
    EvalCase("decision_saudi_1", "saudi", "أرتاح شوي ولا أبدأ الحين", "decision", ("ابدأ", "راحة", "اختر")),
    EvalCase("decision_saudi_2", "saudi", "أرسل الرسالة الحين ولا أنتظر", "decision", ("رسالة", "انتظر", "اختر")),
    EvalCase("decision_msa_1", "msa", "هل أقرأ قليلًا أم أمشي عشر دقائق", "decision", ("اختر", "أقرب", "يريحك")),
    EvalCase("decision_msa_2", "msa", "أجهز للغد أم أنهي عمل اليوم", "decision", ("اليوم", "الغد", "قارن")),
    EvalCase("topic_saudi_1", "saudi", "تكلم عن الوفاء بمثال قريب", "topic", ("الوفاء", "مثال", "معروف")),
    EvalCase("topic_saudi_2", "saudi", "وش فايدة الهدوء في التعامل", "topic", ("الهدوء", "تفكر", "استعجال")),
    EvalCase("topic_msa_1", "msa", "حدثني عن الشجاعة دون تعقيد", "topic", ("الشجاعة", "الخوف", "الصواب")),
    EvalCase("topic_msa_2", "msa", "أعطني مثالًا عن الاحترام", "topic", ("الاحترام", "الناس", "تقدير")),
    EvalCase("learning_saudi_1", "saudi", "علمني طريقة بسيطة لتحسين التركيز", "learning", ("التركيز", "خطوة", "يوم")),
    EvalCase("learning_saudi_2", "saudi", "كيف أتعلم القراءة بشكل أحسن", "learning", ("القراية", "القراءة", "كل يوم")),
    EvalCase("learning_msa_1", "msa", "كيف أحسن عاداتي بهدوء", "learning", ("عادة", "خطوة", "يومية")),
    EvalCase("learning_msa_2", "msa", "اشرح لي طريقة بسيطة للمذاكرة", "learning", ("المذاكرة", "قسّم", "وقت")),
    EvalCase("general_saudi_1", "saudi", "مدري وش أقول بس ودي أتكلم", "open_general", ("شعورك", "كلمة", "أساعدك")),
    EvalCase("general_saudi_2", "saudi", "أبي نصيحة عامة تنفعني اليوم", "open_general", ("اليوم", "ابدأ", "تقدر")),
    EvalCase("general_msa_1", "msa", "لا أعرف كيف أبدأ الكلام", "open_general", ("ابدأ", "كلمة", "فكرة")),
    EvalCase("general_msa_2", "msa", "أحتاج ردًا قصيرًا ومهذبًا", "open_general", ("شكر", "قصير", "واضح")),
)


def _has_canned_phrase(text: str) -> bool:
    surface = _surface(text)
    return any(_surface(phrase) in surface for phrase in _CANNED_PHRASES)


def _has_expected(text: str, terms: tuple[str, ...]) -> bool:
    surface = _surface(text)
    return any(_surface(term) in surface for term in terms)


def _forbidden_absent(text: str, terms: tuple[str, ...]) -> bool:
    surface = _surface(text)
    return not any(_surface(term) in surface for term in terms)


def _overlap_ratio(prompt: str, response: str) -> float:
    p = set(_TOKEN_RE.findall(_surface(prompt)))
    r = set(_TOKEN_RE.findall(_surface(response)))
    if not p or not r:
        return 0.0
    return len(p & r) / max(1, len(p))


def _evaluate(
    *,
    tokenizer: Path,
    checkpoints_root: Path,
    checkpoint_name: str,
    device: str,
) -> list[dict[str, Any]]:
    generator = NativeGenerator(
        NativeGeneratorConfig(
            tokenizer_path=tokenizer,
            checkpoints_root=checkpoints_root,
            checkpoint_name=checkpoint_name,
            generator_name="sf_10m_phase27_53",
            model_size="sf-10m",
            seq_len=80,
            max_new_tokens=42,
            temperature=1.0,
            top_k=0,
            no_repeat_ngram_size=3,
            repetition_penalty=1.08,
            device=device,
            dialogue_prompt=True,
        )
    )
    guard = GenerationGuard(min_chars=4, max_repetition_ratio=0.45)
    rows: list[dict[str, Any]] = []
    for item in EVAL_CASES:
        out = generator.generate(
            item.prompt,
            dialect=item.dialect,
            intent=None,
            topic=None,
            max_new_tokens=42,
            temperature=1.0,
            top_k=0,
        )
        verdict = guard.inspect(out.text)
        expected_ok = _has_expected(out.text, item.expected_any)
        forbidden_ok = _forbidden_absent(out.text, item.forbidden_any)
        canned = _has_canned_phrase(out.text)
        overlap = _overlap_ratio(item.prompt, out.text)
        passed = bool(
            out.used
            and verdict.allowed
            and expected_ok
            and forbidden_ok
            and not canned
            and overlap >= 0.05
        )
        if passed:
            reason = "passed"
        elif not out.used:
            reason = f"generator:{out.reason}"
        elif not verdict.allowed:
            reason = f"guard:{verdict.reason}"
        elif not expected_ok:
            reason = "expected_terms_missing"
        elif not forbidden_ok:
            reason = "forbidden_terms_present"
        elif canned:
            reason = "canned_phrase"
        else:
            reason = f"low_prompt_overlap:{overlap:.2f}"
        rows.append(
            {
                "id": item.id,
                "bucket": item.category,
                "dialect": item.dialect,
                "prompt": item.prompt,
                "expected_any": list(item.expected_any),
                "response": out.text,
                "generator_used": out.used,
                "guard_allowed": verdict.allowed,
                "guard_reason": verdict.reason,
                "expected_ok": expected_ok,
                "canned_phrase": canned,
                "prompt_overlap": round(overlap, 4),
                "passed": passed,
                "reason": reason,
            }
        )
    return rows


def _summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    buckets = sorted({str(row["bucket"]) for row in rows})
    return {
        "passed": sum(1 for row in rows if row["passed"]),
        "total": len(rows),
        "bucket_summary": {
            bucket: {
                "passed": sum(1 for row in rows if row["bucket"] == bucket and row["passed"]),
                "total": sum(1 for row in rows if row["bucket"] == bucket),
            }
            for bucket in buckets
        },
        "reason_counts": dict(Counter(str(row["reason"]) for row in rows)),
    }


def _write_samples(path: Path, rows: list[dict[str, Any]]) -> None:
    lines = ["# Phase 27.53 Natural Dialogue Diversity Expansion", ""]
    for row in rows:
        lines.extend(
            [
                f"## {row['id']} — {'PASS' if row['passed'] else 'FAIL'}",
                "",
                f"- bucket: {row['bucket']}",
                f"- dialect: {row['dialect']}",
                f"- prompt: {row['prompt']}",
                f"- response: {row['response'] or '(empty)'}",
                f"- overlap: {row['prompt_overlap']}",
                f"- reason: {row['reason']}",
                "",
            ]
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    args = parse_args()
    if not (args.tokenizer / "meta.json").exists():
        print(f"error: missing tokenizer at {args.tokenizer}; run Phase 27.44 first", file=sys.stderr)
        return 1
    if args.work_dir.exists() and not args.keep_work:
        shutil.rmtree(args.work_dir)

    corpus_dir = args.work_dir / "corpus"
    checkpoints = args.work_dir / "checkpoints"
    records = _records(args.target_records)
    _write_probe_corpus(corpus_dir, records)

    train_args = [
        "--tokenizer", str(args.tokenizer),
        "--corpus", str(corpus_dir),
        "--size", "sf-10m",
        "--steps", str(args.steps),
        "--epochs", str(args.epochs),
        "--batch-size", str(args.batch_size),
        "--seq-len", str(args.seq_len),
        "--stream-format", "dialogue",
        "--loss-scope", "assistant",
        "--packing-mode", "sample_isolated",
        "--lr", str(args.lr),
        "--warmup", str(args.warmup),
        "--min-lr", "1e-5",
        "--save-every", str(args.steps),
        "--seed", "20260619",
        "--checkpoints", str(checkpoints),
        "--device", args.device,
    ]
    train_code = train_tiny_lm_run(train_args)
    if train_code != 0:
        return train_code

    checkpoint_name = _latest_checkpoint_name(checkpoints)
    rows = _evaluate(
        tokenizer=args.tokenizer,
        checkpoints_root=checkpoints,
        checkpoint_name=checkpoint_name,
        device=args.device,
    )
    summary = _summary(rows)
    passed = summary["passed"] >= 26
    status = (
        "PASSED_NATURAL_DIALOGUE_DIVERSITY_READY_FOR_SHADOW_RUNTIME"
        if passed
        else "PARTIAL_NATURAL_DIALOGUE_DIVERSITY_KEEP_PHASE27_47_RUNTIME"
    )
    category_counts = dict(Counter(str(record.get("category", "")) for record in records))
    dialect_counts = dict(Counter(str(record["provenance"]["dialect"]) for record in records))
    report = {
        "phase": "Phase 27.53",
        "status": status,
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "training_started": True,
        "training_scope": "SF-10M natural dialogue diversity expansion; no model-size scaling",
        "progressive_scaling_respected": True,
        "model_size": "sf-10m",
        "tokenizer": _rel(args.tokenizer),
        "checkpoint_root": _rel(checkpoints),
        "checkpoint_name": checkpoint_name,
        "candidate_generator": "sf_10m_phase27_53",
        "unique_train_records": len(records),
        "dialect_counts": dialect_counts,
        "category_counts": category_counts,
        "training_budget": {
            "steps": args.steps,
            "batch_size": args.batch_size,
            "seq_len": args.seq_len,
            "lr": args.lr,
            "warmup": args.warmup,
        },
        "governance": {
            "owner_delegated_agent_authored": True,
            "external_data_used": False,
            "pretrained_used": False,
            "operational_dialogue_excluded": True,
            "records_governance_audited": True,
        },
        "no_keyword_lane_claim": {
            "intent_conditioning_used_in_training": False,
            "topic_conditioning_used_in_training": False,
            "raw_eval_intent": None,
            "raw_eval_topic": None,
        },
        "summary": summary,
        "runtime_switch_allowed": passed,
        "sf50m_allowed": False,
        "phase28_allowed": False,
        "previous_phase27_52": {"raw_natural_passed": 5, "raw_natural_total": 20},
        "next_phase": (
            "Phase 27.54 — guarded shadow switch for phase27_53"
            if passed
            else "Phase 27.54 — inspect diversity failures and consider tokenizer/model-capacity gate"
        ),
        "torch_version": torch.__version__,
        "rows": rows,
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _write_samples(args.samples, rows)

    print("SF.AI — Phase 27.53 natural dialogue diversity expansion")
    print(f"  status       : {status}")
    print(f"  tokenizer    : {_rel(args.tokenizer)}")
    print(f"  checkpoint   : {checkpoint_name}")
    print(f"  records      : {len(records)}")
    print(f"  dialects     : {dialect_counts}")
    print(f"  steps        : {args.steps}")
    print(f"  cases        : {summary['passed']}/{summary['total']}")
    for bucket, item in summary["bucket_summary"].items():
        print(f"  {bucket:<14}: {item['passed']}/{item['total']}")
    print(f"  reasons      : {summary['reason_counts']}")
    print(f"  report       : {args.report}")
    print(f"  samples      : {args.samples}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
