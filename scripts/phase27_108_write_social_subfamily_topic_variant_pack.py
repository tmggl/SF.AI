#!/usr/bin/env python3
"""Write a sovereign gold data pack for social subfamilies and topic variants.

No external datasets. No project-operation dialogue. The records are authored
locally for SF.AI's Arabic/Saudi conversational repair path.
"""
# ruff: noqa: E402

from __future__ import annotations

import json
import sys
from collections.abc import Iterable
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sf_ai.datasets.corpus_governance import audit_jsonl_file_for_training

OUT_DIR = ROOT / "data/corpus/chat/jsonl"
REPORT_DIR = ROOT / "artifacts/reports"
DOC_DIR = ROOT / "docs"
LICENSE = "owner-approved-for-sf-ai-training"
OWNER_USER_ID = "sami-local"
CREATOR_USER_ID = "sf-ai-local-author"
REPORT = REPORT_DIR / "phase27_108_social_subfamily_topic_variant_data_pack_report.json"
DECISION = REPORT_DIR / "PHASE27_108_SOCIAL_SUBFAMILY_TOPIC_VARIANT_DATA_PACK_DECISION.json"
DOC = DOC_DIR / "PHASE27_108_SOCIAL_SUBFAMILY_TOPIC_VARIANT_DATA_PACK_REPORT.md"

FORBIDDEN_CONTENT = (
    "التالي",
    "اكمل",
    "أكمل",
    "ارفع",
    "commit",
    "pytest",
    "git",
    "phase",
    "Phase",
    "gates",
    "readiness",
    "corpus",
    "tokenizer",
    "تدريب",
    "التدريب",
    "الواجهة",
    "سيرفر",
    "endpoint",
    "runtime",
    "agent",
    "workflow",
    "سامي",
    "checkpoint",
    "Qwen",
    "Llama",
    "Mistral",
    "Gemma",
)

SOCIAL_LABELS = {
    "greeting": "تحية",
    "smalltalk": "سؤال حال",
    "open_chat": "فتح سالفة",
    "thanks": "شكر",
    "identity": "هوية",
    "capability": "قدرات",
}

SOCIAL_PROMPTS: dict[str, dict[str, list[str]]] = {
    "msa": {
        "greeting": [
            "السلام عليكم",
            "مرحبًا",
            "أهلًا بك",
            "صباح الخير",
            "مساء الخير",
            "حيّاك الله",
            "أهلًا، هل أنت موجود؟",
            "السلام عليكم ورحمة الله",
            "تحية طيبة",
            "أهلًا من جديد",
            "مرحبا، أريد أن أبدأ حديثًا",
            "السلام عليكم، كيف حالك؟",
            "أهلًا، هل يمكن أن نتحدث؟",
            "مساء النور عليك",
            "صباحك طيب",
            "أهلًا وسهلًا",
            "مرحبًا، عندي سؤال بسيط",
            "السلام عليكم، أحتاج مساعدة",
            "أهلًا، أود الحديث قليلًا",
            "مرحبًا بك",
            "السلام عليكم، هل تسمعني؟",
            "أهلًا، أرجو أن تكون بخير",
            "مرحبًا، لنبدأ",
            "تحياتي لك",
            "أهلًا، أريد رأيك",
            "مساء الخير، هل أنت متاح؟",
            "صباح الخير، عندي فكرة",
            "السلام عليكم، نبدأ؟",
            "مرحبًا، أحتاج توجيهًا",
            "أهلًا، كيف أبدأ؟",
        ],
        "smalltalk": [
            "كيف الحال؟",
            "كيف حالك اليوم؟",
            "ما أخبارك؟",
            "هل أنت بخير؟",
            "كيف يومك؟",
            "أرجو أن تكون بخير",
            "هل كل شيء جيد؟",
            "طمئني عنك",
            "كيف تسير الأمور؟",
            "ما الجديد عندك؟",
            "كيف المزاج اليوم؟",
            "هل يومك هادئ؟",
            "هل أنت مستعد للحديث؟",
            "كيف تشعر الآن؟",
            "هل الأمور طيبة؟",
            "كيف كانت بدايتك اليوم؟",
            "هل لديك طاقة للحديث؟",
            "ما حالك هذه اللحظة؟",
            "هل يومك مزدحم؟",
            "كيف هو الجو عندك؟",
            "كيف تسير يومياتك؟",
            "أحببت أن أسأل عن حالك",
            "هل أنت مرتاح الآن؟",
            "كيف أمورك؟",
            "هل عندك شيء لطيف اليوم؟",
            "كيف كانت آخر ساعة عندك؟",
            "هل تشعر بالهدوء؟",
            "كيف حالك باختصار؟",
            "ما شعورك الآن؟",
            "هل نبدأ بسؤال خفيف؟",
        ],
        "open_chat": [
            "دعنا نتحدث قليلًا",
            "افتح لي موضوعًا خفيفًا",
            "أريد حديثًا عاديًا",
            "ما رأيك أن نتكلم؟",
            "ابدأ بسؤال لطيف",
            "اختر موضوعًا بسيطًا",
            "أريد أن أسولف قليلًا",
            "لنفتح حديثًا مريحًا",
            "اقترح عليّ سالفة قصيرة",
            "ليس لدي موضوع محدد",
            "حدثني عن شيء لطيف",
            "اسألني سؤالًا خفيفًا",
            "أريد بداية سهلة للكلام",
            "لنبدأ بشيء يومي",
            "افتح باب الحديث",
            "أريد كلامًا لا يكون رسميًا",
            "هل يمكن أن نسولف؟",
            "أريد حديثًا بسيطًا جدًا",
            "اختر سؤالًا من الحياة اليومية",
            "لنتكلم عن عادة مفيدة",
            "أريد أن أرتاح بالحديث",
            "افتح سالفة تناسب مزاج هادئ",
            "حدثني كأننا في حديث عادي",
            "أريد شيئًا خفيفًا قبل العمل",
            "ابدأ بسؤال واحد فقط",
            "خلّ الحديث بسيطًا",
            "أريد سؤالًا يفتح الكلام",
            "ما الموضوع الذي تقترحه؟",
            "دعنا نبدأ من يومي",
            "خفف عني ثقل الصمت بسؤال بسيط",
        ],
        "thanks": [
            "شكرًا",
            "شكرًا لك",
            "أشكرك على المساعدة",
            "هذا لطف منك",
            "جزاك الله خيرًا",
            "أقدر مساعدتك",
            "ممتن لك",
            "شكرًا على التوضيح",
            "شكرًا، هذا يكفي",
            "أحسنت",
            "كلامك مفيد",
            "شكرًا على صبرك",
            "أقدر وقتك",
            "هذا ساعدني",
            "شكرًا من القلب",
            "أنت أفدتني",
            "شكرًا، فهمت الآن",
            "ممتاز، شكرًا",
            "لطيف جدًا",
            "أقدر ردك",
            "شكرًا على الاختصار",
            "شكرًا على هدوء الرد",
            "جزيل الشكر",
            "أشكرك، نتابع لاحقًا",
            "هذا واضح، شكرًا",
            "شكرًا على السؤال",
            "شكرًا لأنك انتبهت",
            "ممتن لهذه الصياغة",
            "الله يعطيك العافية",
            "شكرًا، هذا ما أحتاجه",
        ],
        "identity": [
            "من أنت؟",
            "عرّفني عليك",
            "ما طبيعتك؟",
            "هل أنت مساعد؟",
            "ما دورك هنا؟",
            "كيف أتعامل معك؟",
            "هل أنت شخص؟",
            "أخبرني عن نفسك",
            "ما الذي تمثله؟",
            "ما هويتك؟",
            "هل تفهم العربية؟",
            "هل أنت هنا للمساعدة؟",
            "هل يمكنني الحديث معك؟",
            "ما علاقتك بالمحادثة؟",
            "هل أنت برنامج محادثة؟",
            "هل تتذكر ما أكتبه؟",
            "هل يمكن أن توجهني؟",
            "هل أنت مناسب للسؤال العام؟",
            "ماذا ينبغي أن أعرف عنك؟",
            "من يخاطبني الآن؟",
            "هل أنت مساعد عربي؟",
            "هل تفهم الأسئلة القصيرة؟",
            "هل ترد بالعربية؟",
            "هل يمكن أن تسألني؟",
            "هل تستطيع المتابعة معي؟",
            "هل تتعلم من الحديث؟",
            "هل أنت خاص بهذه المحادثة؟",
            "هل أنت موجود للرد فقط؟",
            "ما حدودك؟",
            "كيف تصف نفسك بجملة؟",
        ],
        "capability": [
            "ماذا تستطيع أن تفعل؟",
            "كيف تساعدني؟",
            "ما الذي تجيده؟",
            "وش تقدر تسوي؟",
            "ما فائدتك في الحوار؟",
            "هل تستطيع تنظيم أفكاري؟",
            "هل تساعدني في صياغة الكلام؟",
            "هل تستطيع أن تسألني أسئلة؟",
            "هل تفيدني في يومي؟",
            "هل تساعدني إذا كنت متوترًا؟",
            "هل تستطيع تلخيص كلامي؟",
            "هل تفهم السؤال القصير؟",
            "هل تستطيع فتح موضوع؟",
            "هل تساعدني في ترتيب مهامي؟",
            "هل تجيب على التعريفات؟",
            "هل تستطيع أن تشرح ببساطة؟",
            "هل ترد باللهجة السعودية؟",
            "هل ترد بالفصحى؟",
            "متى تكون مفيدًا؟",
            "ما أفضل طريقة لاستخدامك؟",
            "هل تساعدني في رد مهذب؟",
            "هل تفهم متابعة الحديث؟",
            "هل تستطيع سؤالًا بعد سؤال؟",
            "هل تساعدني على بداية سهلة؟",
            "هل تفهم كلمة واحدة؟",
            "هل تميز الموضوع من السؤال؟",
            "ما حدود المساعدة عندك؟",
            "هل تستطيع أن تكون مختصرًا؟",
            "هل تجيب بنقاط؟",
            "هل يمكن أن تقترح خطوة؟",
        ],
    },
    "saudi": {
        "greeting": [
            "السلام عليكم",
            "هلا",
            "يا هلا",
            "مرحبا",
            "صباح الخير",
            "مساء الخير",
            "هلا والله",
            "حياك الله",
            "السلام عليكم ورحمة الله",
            "أهلين",
            "هلا كيفك",
            "مرحبا نبدأ؟",
            "السلام عليكم، عندي سؤال",
            "يا هلا، أنت موجود؟",
            "صباحك خير",
            "مساك الله بالخير",
            "هلا بك",
            "يا مرحبا",
            "السلام عليكم، أبي أتكلم شوي",
            "هلا، ممكن أسأل؟",
            "مرحبتين",
            "هلا وغلا",
            "حياك، نبدأ؟",
            "السلام عليكم، كيف الأمور؟",
            "صباح النور",
            "مساء النور",
            "هلا، أبي رأيك",
            "السلام عليكم، أبي مساعدة",
            "مرحبا، علمني",
            "هلا، وش عندك؟",
        ],
        "smalltalk": [
            "كيف الحال؟",
            "كيفك؟",
            "علومك؟",
            "وش الأخبار؟",
            "وش جديدك؟",
            "طمني عنك",
            "أمورك طيبة؟",
            "كيف يومك؟",
            "وش وضعك؟",
            "كل شي تمام؟",
            "كيف المزاج؟",
            "بخير أنت؟",
            "وش مسوي؟",
            "كيف أمورك اليوم؟",
            "عساك طيب",
            "وش صار معك اليوم؟",
            "كيف الجو عندك؟",
            "مرتاح؟",
            "وش عندك اليوم؟",
            "كيف بداية يومك؟",
            "وش أخبارك الحين؟",
            "كل الأمور زينة؟",
            "كيفك باختصار؟",
            "وش علومك؟",
            "طمنا عليك",
            "وش أكثر شي شاغلك؟",
            "كيف حالك هاللحظة؟",
            "الأمور ماشية؟",
            "كيف طاقتك اليوم؟",
            "نبدأ بسؤال خفيف؟",
        ],
        "open_chat": [
            "خلنا نسولف",
            "افتح لي سالفة",
            "سولف معي",
            "هات سالفة خفيفة",
            "وش عندك من موضوع؟",
            "أبي كلام عادي",
            "خلنا نتكلم شوي",
            "ابدأ أنت بسؤال",
            "ما عندي موضوع محدد",
            "اقترح سالفة",
            "أبي أسولف عن شي بسيط",
            "خلنا نفتح موضوع",
            "وش تحب نسولف عنه؟",
            "أبي بداية خفيفة",
            "اسألني سؤال سهل",
            "خل الكلام بسيط",
            "أبي سالفة تروق",
            "هات موضوع من الحياة",
            "خلنا نتكلم عن اليوم",
            "سولف عن عادة مفيدة",
            "أبي كلام يخفف الجو",
            "افتح موضوع يناسب الهدوء",
            "خلنا نبدأ من شي لطيف",
            "وش أول سؤال عندك؟",
            "اسألني عن يومي",
            "خلها سوالف عادية",
            "ما أبي كلام رسمي",
            "نبي سالفة قصيرة",
            "ابدأ بشي بسيط",
            "خلنا نكسر الصمت",
        ],
        "thanks": [
            "شكرا",
            "يعطيك العافية",
            "تسلم",
            "ما قصرت",
            "بيض الله وجهك",
            "الله يعافيك",
            "كلامك واضح",
            "فهمت، يعطيك العافية",
            "مشكور",
            "حلو، شكرا",
            "الله يقويك",
            "أفدتني",
            "كفو",
            "هذا اللي أبيه",
            "تمام، تسلم",
            "ردك ساعدني",
            "شكرًا من القلب",
            "ما عليك زود",
            "الله يجزاك خير",
            "واضح ومفيد",
            "حياك الله",
            "ممتن لك",
            "تعبتك معي",
            "سلمت",
            "رائع، يعطيك العافية",
            "رد جميل",
            "أبشر، فهمت",
            "الله يرفع قدرك",
            "وصلت الفكرة",
            "أشكرك",
        ],
        "identity": [
            "من أنت؟",
            "عرفني عليك",
            "وش أنت؟",
            "أنت مساعد؟",
            "وش دورك؟",
            "كيف أتعامل معك؟",
            "أنت شخص؟",
            "تكلم عن نفسك",
            "وش هويتك؟",
            "تفهم عربي؟",
            "تفهم سعودي؟",
            "أقدر أسولف معك؟",
            "أنت هنا تساعدني؟",
            "وش المفروض أعرفه عنك؟",
            "أنت برنامج محادثة؟",
            "تتذكر كلامي؟",
            "تقدر توجهني؟",
            "ينفع أسألك أي شي عام؟",
            "من اللي يرد علي؟",
            "أنت مساعد عربي؟",
            "تفهم الجمل القصيرة؟",
            "ترد بالسعودي؟",
            "تقدر تسألني؟",
            "تقدر تتابع معي؟",
            "تتعلم من كلامي؟",
            "أنت خاص بالمحادثة؟",
            "وش حدودك؟",
            "صف نفسك بجملة",
            "هل تفهم قصدي؟",
            "أقدر أعتمد عليك في سوالف بسيطة؟",
        ],
        "capability": [
            "وش تقدر تسوي؟",
            "كيف تساعدني؟",
            "وش تعرف تسوي؟",
            "وش فايدتك؟",
            "تقدر ترتب أفكاري؟",
            "تساعدني أصيغ كلام؟",
            "تقدر تسألني أسئلة؟",
            "تفيدني في يومي؟",
            "تساعدني إذا توترت؟",
            "تلخص كلامي؟",
            "تفهم السؤال القصير؟",
            "تقدر تفتح موضوع؟",
            "تساعدني أرتب مهامي؟",
            "تجاوب على معنى كلمة؟",
            "تشرح ببساطة؟",
            "ترد باللهجة السعودية؟",
            "ترد بالفصحى؟",
            "متى تفيدني؟",
            "وش أفضل طريقة أستخدمك فيها؟",
            "تساعدني برد مهذب؟",
            "تفهم متابعة الكلام؟",
            "تقدر تمشي سؤال ورا سؤال؟",
            "تدلني على بداية سهلة؟",
            "تفهم كلمة وحدة؟",
            "تميز الموضوع من السؤال؟",
            "وش حدود المساعدة عندك؟",
            "تقدر تختصر؟",
            "تجاوب بنقاط؟",
            "تقترح خطوة؟",
            "تقدر تسولف وتوجه؟",
        ],
    },
}

SOCIAL_ASSISTANT = {
    "msa": {
        "greeting": [
            "وعليكم السلام، أهلًا بك. كيف حالك؟",
            "مرحبًا، سعيد بحديثك. ما الذي تريد أن نبدأ به؟",
            "أهلًا وسهلًا، تفضل، أنا معك.",
            "صباح النور، أتمنى لك يومًا طيبًا.",
            "مساء النور، كيف يمكن أن أساعدك؟",
        ],
        "smalltalk": [
            "بخير، شكرًا لسؤالك. كيف حالك أنت؟",
            "الحمد لله، أنا جاهز للحديث. ما أخبارك؟",
            "أنا بخير. هل تريد أن نبدأ بشيء خفيف؟",
            "الأمور طيبة، وأتمنى أن تكون بخير أيضًا.",
            "بخير، ويسعدني أن أسمع منك.",
        ],
        "open_chat": [
            "نبدأ بسؤال خفيف: ما الشيء اللطيف الذي حدث لك اليوم؟",
            "يمكن أن نتحدث عن يومك أو عادة تحبها.",
            "خلّنا نبدأ بموضوع بسيط: ما أكثر شيء يشغلك الآن؟",
            "أقترح حديثًا خفيفًا عن شيء تحب فعله في وقت الراحة.",
            "اسألني أو احكِ لي عن يومك، وسأتابع معك.",
        ],
        "thanks": [
            "العفو، يسعدني أن أساعدك.",
            "على الرحب والسعة، أنا هنا متى احتجت.",
            "لا شكر على واجب، هل تريد شيئًا آخر؟",
            "سعيد أن الرد أفادك.",
            "حياك الله، نتابع متى أحببت.",
        ],
        "identity": [
            "أنا مساعد عربي محلي للمحادثة والتوجيه البسيط.",
            "أنا هنا لأفهم سؤالك وأساعدك برد واضح ومختصر.",
            "دوري أن أتحاور معك، أسأل عند الحاجة، وأساعدك خطوة خطوة.",
            "أنا مساعد نصي يركز على العربية والفهم اليومي.",
            "يمكنك اعتباري رفيقًا للحوار وترتيب الأفكار.",
        ],
        "capability": [
            "أقدر أساعدك في الحوار، الترتيب، الصياغة، والأسئلة اليومية.",
            "أستطيع أن أرتب الفكرة، أقترح بداية، وأسأل سؤال متابعة.",
            "أفيدك في ردود قصيرة، شرح بسيط، وتهدئة الكلام المتوتر.",
            "أساعدك في تنظيم المهام وفهم السؤال العام خطوة خطوة.",
            "أقدر أفتح موضوعًا خفيفًا أو أختصر لك فكرة واضحة.",
        ],
    },
    "saudi": {
        "greeting": [
            "وعليكم السلام، حياك الله. وش أخبارك؟",
            "هلا بك، تفضل وش تحتاج؟",
            "يا هلا، نبدأ من وين؟",
            "صباح النور، عسى يومك طيب.",
            "مساء النور، أنا معك.",
        ],
        "smalltalk": [
            "بخير ولله الحمد، أنت كيفك؟",
            "تمام الحمد لله، وش أخبارك أنت؟",
            "طيّب، ويسعدني نسولف. وش عندك؟",
            "الأمور زينة، عساك بخير.",
            "بخير، وش ودك نبدأ فيه؟",
        ],
        "open_chat": [
            "خلنا نبدأ بسؤال خفيف: وش ألطف شي صار في يومك؟",
            "نقدر نسولف عن يومك أو عادة تحبها.",
            "هات اللي في بالك، وأنا أتابع معك.",
            "أقترح سالفة بسيطة: وش الشي اللي يروقك عادة؟",
            "خلنا نفتح موضوع خفيف ونمشي فيه شوي شوي.",
        ],
        "thanks": [
            "العفو، حياك الله.",
            "تسلم، أنا موجود متى احتجت.",
            "ما سوينا إلا الواجب.",
            "الله يعافيك، نتابع إذا تبي.",
            "حياك، سعيد إني أفدتك.",
        ],
        "identity": [
            "أنا مساعد عربي محلي أركز على الحوار والتوجيه البسيط.",
            "أنا هنا أفهم كلامك وأرد عليك بوضوح.",
            "دوري أساعدك تسولف، ترتب أفكارك، وتلقى بداية مناسبة.",
            "أنا مساعد نصي يفهم الفصحى والسعودي قدر الإمكان.",
            "اعتبرني مرافق حوار يساعدك خطوة خطوة.",
        ],
        "capability": [
            "أقدر أساعدك في السوالف، ترتيب الأفكار، والردود اليومية.",
            "أقدر أرتب مهامك، أقترح بداية، وأسألك سؤال متابعة.",
            "أفيدك في شرح بسيط، صياغة رد، أو تهدئة توتر.",
            "أقدر أجاوب باختصار أو أفتح موضوع خفيف.",
            "أساعدك تمشي خطوة خطوة بدون تعقيد.",
        ],
    },
}

TOPIC_PROMPTS = {
    "msa": {
        "الصداقة": [
            "الصداقة",
            "الصداقه",
            "ما معنى الصداقة؟",
            "عرّف الصداقة بجملة",
            "تحدث عن الصداقة باختصار",
            "لماذا الصداقة مهمة؟",
            "وش يعني الصداقة؟",
            "الصداقة وش تعني",
            "أريد جملة عن الصداقة",
            "صف الصداقة ببساطة",
            "ما قيمة الصداقة؟",
            "كيف تكون الصداقة طيبة؟",
            "اكتب معنى الصداقه",
            "ما أجمل شيء في الصداقة؟",
            "الصداقة في الحياة اليومية",
            "ما الفرق بين الصداقة والمجاملة؟",
            "أريد تعريفًا قصيرًا للصداقة",
            "هل الصداقة تحتاج اهتمامًا؟",
            "ما علامة الصداقة الجيدة؟",
            "اختصر لي معنى الصداقة",
            "الصداقة باختصار",
            "حدثني عن صديق حقيقي",
            "ما معنى رفقة طيبة؟",
            "كيف نحافظ على الصداقة؟",
            "الصديق الوفي ماذا يفعل؟",
            "هل الصداقة ثقة؟",
            "أريد كلامًا لطيفًا عن الصداقة",
            "الصداقة والثقة",
            "جملة مريحة عن الصداقة",
            "كيف أعرف الصداقة الصادقة؟",
        ],
        "الأخوة": [
            "الأخوة",
            "الاخوه",
            "ما معنى الأخوة؟",
            "عرّف الأخوة بجملة",
            "تحدث عن الأخوة باختصار",
            "لماذا الأخوة مهمة؟",
            "وش يعني الاخوه؟",
            "الأخوة وش تعني",
            "أريد جملة عن الأخوة",
            "صف الأخوة ببساطة",
            "ما قيمة الأخوة؟",
            "كيف تكون الأخوة صادقة؟",
            "اكتب معنى الاخوه",
            "ما أجمل شيء في الأخوة؟",
            "الأخوة في الحياة اليومية",
            "ما الفرق بين الأخوة والمصلحة؟",
            "أريد تعريفًا قصيرًا للأخوة",
            "هل الأخوة تحتاج مساندة؟",
            "ما علامة الأخوة الجيدة؟",
            "اختصر لي معنى الأخوة",
            "الأخوة باختصار",
            "حدثني عن أخ يقف معك",
            "ما معنى وقفة الأخ؟",
            "كيف نحافظ على الأخوة؟",
            "الأخ الوفي ماذا يفعل؟",
            "هل الأخوة سند؟",
            "أريد كلامًا لطيفًا عن الأخوة",
            "الأخوة والمساندة",
            "جملة مريحة عن الأخوة",
            "كيف أعرف الأخوة الصادقة؟",
        ],
    },
    "saudi": {
        "الصداقة": [
            "الصداقة",
            "الصداقه",
            "وش معنى الصداقة؟",
            "عرف الصداقة بجملة",
            "تكلم عن الصداقة باختصار",
            "ليه الصداقة مهمة؟",
            "الصداقة وش تعني؟",
            "أبي جملة عن الصداقة",
            "صف الصداقة ببساطة",
            "وش قيمة الصداقة؟",
            "كيف تكون الصداقة طيبة؟",
            "اكتب معنى الصداقه",
            "وش أجمل شي في الصداقة؟",
            "الصداقة بالحياة اليومية",
            "الفرق بين الصداقة والمجاملة؟",
            "أبي تعريف قصير للصداقة",
            "الصداقة تحتاج اهتمام؟",
            "وش علامة الصداقة الجيدة؟",
            "اختصر معنى الصداقة",
            "الصداقة باختصار",
            "تكلم عن خوي صدوق",
            "وش معنى الرفقة الطيبة؟",
            "كيف نحافظ على الصداقة؟",
            "الصديق الوفي وش يسوي؟",
            "الصداقة ثقة؟",
            "أبي كلام لطيف عن الصداقة",
            "الصداقة والثقة",
            "جملة تريح عن الصداقة",
            "كيف أعرف الصداقة الصادقة؟",
            "وش معنى صديق حقيقي؟",
        ],
        "الأخوة": [
            "الأخوة",
            "الاخوه",
            "وش معنى الأخوة؟",
            "عرف الأخوة بجملة",
            "تكلم عن الأخوة باختصار",
            "ليه الأخوة مهمة؟",
            "الأخوة وش تعني؟",
            "أبي جملة عن الأخوة",
            "صف الأخوة ببساطة",
            "وش قيمة الأخوة؟",
            "كيف تكون الأخوة صادقة؟",
            "اكتب معنى الاخوه",
            "وش أجمل شي في الأخوة؟",
            "الأخوة بالحياة اليومية",
            "الفرق بين الأخوة والمصلحة؟",
            "أبي تعريف قصير للأخوة",
            "الأخوة تحتاج مساندة؟",
            "وش علامة الأخوة الجيدة؟",
            "اختصر معنى الأخوة",
            "الأخوة باختصار",
            "تكلم عن أخ يوقف معك",
            "وش معنى وقفة الأخ؟",
            "كيف نحافظ على الأخوة؟",
            "الأخ الوفي وش يسوي؟",
            "الأخوة سند؟",
            "أبي كلام لطيف عن الأخوة",
            "الأخوة والمساندة",
            "جملة تريح عن الأخوة",
            "كيف أعرف الأخوة الصادقة؟",
            "وش معنى أخ حقيقي؟",
        ],
    },
}

TOPIC_ASSISTANT = {
    "msa": {
        "الصداقة": [
            "الصداقة علاقة فيها صدق واهتمام ووقفة وقت الحاجة.",
            "الصداقة رفقة طيبة تقوم على الثقة والتقدير.",
            "الصداقة تعني أن تجد من يسمعك ويصدق معك.",
            "الصداقة الجيدة لا تحتاج كثرة كلام بقدر ما تحتاج ثباتًا.",
            "الصداقة الطيبة تحفظ الود وتقف معك عند الحاجة.",
        ],
        "الأخوة": [
            "الأخوة سند ومساندة وحرص صادق.",
            "الأخوة تعني أن تجد من يقف معك بمحبة وتقدير.",
            "الأخوة قرب في الشدة واليسر، لا مجرد اسم.",
            "الأخوة تحفظ الود وتعينك على الخير.",
            "الأخوة علاقة فيها رحمة ووقفة صادقة.",
        ],
    },
    "saudi": {
        "الصداقة": [
            "الصداقة إنك تلقى خوي صادق يوقف معك وقت الحاجة.",
            "الصداقة ثقة واهتمام، مو بس كلام كثير.",
            "الصداقة إنك تلقى شخص يسمع لك ويحفظ الود.",
            "الصداقة الطيبة تبان في المواقف، مو في المجاملات.",
            "الصداقة تخلي الخوي قريب وقت الشدة والفرح.",
        ],
        "الأخوة": [
            "الأخوة سند ووقفة، خصوصًا وقت الحاجة.",
            "الأخوة إنك تلقى من يوقف معك ويحرص عليك.",
            "الأخوة مو بس اسم، هي وفاء ومساندة.",
            "الأخوة الطيبة تبان في المواقف الصعبة.",
            "الأخوة تخفف عنك وتعينك على الخير.",
        ],
    },
}


def _social_record(dialect: str, subfamily: str, user: str, assistant: str) -> dict[str, object]:
    return {
        "domain": "chat",
        "lang": "ar",
        "messages": [
            {"role": "user", "content": user},
            {"role": "assistant", "content": assistant},
        ],
        "provenance": {
            "source": "sf-ai-local-social-subfamily-pack-v1",
            "license": LICENSE,
            "language": "ar",
            "dialect": dialect,
            "quality": "gold",
            "training_allowed": True,
            "dialogue_family": "open_social",
            "dialogue_subfamily": subfamily,
            "prompt_family": "open_social",
            "answer_family": "open_social",
            "owner_user_id": OWNER_USER_ID,
            "created_by_user_id": CREATOR_USER_ID,
            "target_user_id": OWNER_USER_ID,
            "user_scope": "single_user",
            "notes": "owner delegated local authoring; natural social dialogue only; no external dataset",
        },
    }


def _topic_record(dialect: str, canonical: str, user: str, assistant: str) -> dict[str, object]:
    return {
        "domain": "chat",
        "lang": "ar",
        "messages": [
            {"role": "user", "content": user},
            {"role": "assistant", "content": assistant},
        ],
        "provenance": {
            "source": "sf-ai-local-topic-variant-pack-v1",
            "license": LICENSE,
            "language": "ar",
            "dialect": dialect,
            "quality": "gold",
            "training_allowed": True,
            "dialogue_family": "topic",
            "prompt_family": "topic",
            "answer_family": "topic",
            "topic_term": canonical,
            "topic_canonical": canonical,
            "topic_variant": user,
            "owner_user_id": OWNER_USER_ID,
            "created_by_user_id": CREATOR_USER_ID,
            "target_user_id": OWNER_USER_ID,
            "user_scope": "single_user",
            "notes": "owner delegated local authoring; natural topic variant dialogue only; no external dataset",
        },
    }


def _cycle(items: list[str], index: int) -> str:
    return items[index % len(items)]


def build_records() -> dict[str, list[dict[str, object]]]:
    out: dict[str, list[dict[str, object]]] = {
        "social_msa": [],
        "social_saudi": [],
        "topic_msa": [],
        "topic_saudi": [],
    }
    for dialect in ("msa", "saudi"):
        for subfamily, prompts in SOCIAL_PROMPTS[dialect].items():
            answers = SOCIAL_ASSISTANT[dialect][subfamily]
            if len(prompts) != 30:
                raise RuntimeError(f"{dialect}/{subfamily} expected 30 prompts")
            for idx, prompt in enumerate(prompts):
                out[f"social_{dialect}"].append(
                    _social_record(dialect, subfamily, prompt, _cycle(answers, idx))
                )
    for dialect in ("msa", "saudi"):
        for canonical, prompts in TOPIC_PROMPTS[dialect].items():
            answers = TOPIC_ASSISTANT[dialect][canonical]
            if len(prompts) != 30:
                raise RuntimeError(f"{dialect}/{canonical} expected 30 prompts")
            for idx, prompt in enumerate(prompts):
                out[f"topic_{dialect}"].append(
                    _topic_record(dialect, canonical, prompt, _cycle(answers, idx))
                )
    return out


def _scan_forbidden(records: Iterable[dict[str, object]]) -> None:
    for record in records:
        messages = record.get("messages")
        text = json.dumps(messages, ensure_ascii=False)
        bad = [term for term in FORBIDDEN_CONTENT if term in text]
        if bad:
            raise RuntimeError(f"forbidden operational terms in message text: {bad}")


def _write_jsonl(path: Path, records: list[dict[str, object]]) -> None:
    path.write_text(
        "\n".join(json.dumps(record, ensure_ascii=False) for record in records) + "\n",
        encoding="utf-8",
    )


def _write_card(path: Path, *, title: str, records: int, description: str) -> None:
    path.write_text(
        "\n".join(
            [
                f"# {title}",
                "",
                "- source: owner-delegated local authoring",
                "- language: ar",
                "- dialects: msa + saudi",
                f"- records: {records}",
                "- quality: gold",
                "- training_allowed: true",
                "- synthetic_llm_data: false",
                "- external_dataset: false",
                f"- purpose: {description}",
                "",
            ]
        ),
        encoding="utf-8",
    )


def _summarize(records: dict[str, list[dict[str, object]]]) -> dict[str, object]:
    all_records = [record for group in records.values() for record in group]
    social_counts: dict[str, int] = {}
    topic_counts: dict[str, int] = {}
    dialect_counts: dict[str, int] = {}
    for record in all_records:
        provenance = record["provenance"]  # type: ignore[index]
        dialect = str(provenance["dialect"])  # type: ignore[index]
        dialect_counts[dialect] = dialect_counts.get(dialect, 0) + 1
        subfamily = provenance.get("dialogue_subfamily")  # type: ignore[union-attr]
        if subfamily:
            key = f"{dialect}:{subfamily}"
            social_counts[key] = social_counts.get(key, 0) + 1
        topic = provenance.get("topic_canonical")  # type: ignore[union-attr]
        if topic:
            key = f"{dialect}:{topic}"
            topic_counts[key] = topic_counts.get(key, 0) + 1
    return {
        "total_records": len(all_records),
        "dialect_counts": dialect_counts,
        "social_subfamily_counts": social_counts,
        "topic_counts": topic_counts,
        "quality": {"gold": len(all_records), "silver": 0, "bronze": 0},
    }


def _audit_summary(path: Path) -> dict[str, Any]:
    audit = audit_jsonl_file_for_training(path)
    return {
        "path": str(path.relative_to(ROOT)),
        "total_records": audit.total_records,
        "training_ready": audit.training_ready,
        "error_count": audit.error_count,
        "issues": [
            {
                "line_number": issue.line_number,
                "kind": issue.kind,
                "message": issue.message,
                "snippet": issue.snippet,
            }
            for issue in audit.issues
        ],
        "dialects": audit.dialect_counts,
        "qualities": audit.quality_counts,
        "sources": audit.source_counts,
    }


def _write_doc(report: dict[str, Any]) -> None:
    summary = report["summary"]
    decision = report["decision"]
    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(
        "\n".join(
            [
                "# Phase 27.108 — Social Subfamily + Topic Variant Data Pack",
                "",
                "## الخلاصة",
                "",
                "اكتملت حزمة بيانات gold سيادية بلا تدريب وبلا تغيير runtime.",
                "",
                "القرار:",
                "",
                "```text",
                str(decision["decision_id"]),
                "```",
                "",
                "النتيجة:",
                "",
                f"- السجلات الجديدة: `{summary['total_records']}`.",
                "- المسار اللغوي: فصحى + سعودي فقط.",
                "- المحتوى: حوار بشري طبيعي، بلا أوامر تشغيل أو إدارة مشروع.",
                "- كل السجلات تحمل source/license/quality/training_allowed.",
                "- لا pretrained، لا بيانات خارجية، لا تدريب جديد.",
                "",
                "## التوزيع",
                "",
                "```json",
                json.dumps(summary, ensure_ascii=False, indent=2),
                "```",
                "",
                "## القرار الهندسي",
                "",
                "```text",
                str(decision["engineering_decision"]),
                "```",
                "",
                "المسموح التالي:",
                "",
                "- Phase 27.109 audit/gate فقط.",
                "- فحص corpus-audit كامل.",
                "- فحص توازن social subfamilies وtopic variants.",
                "",
                "الممنوع:",
                "",
                "- training جديد.",
                "- runtime release رسمي.",
                "- SF-50M.",
                "- tokenizer retrain.",
                "- أي نموذج أو tokenizer خارجي.",
                "",
                "## التالي",
                "",
                "```text",
                str(decision["next_phase"]),
                "```",
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> int:
    records = build_records()
    all_records = [record for group in records.values() for record in group]
    _scan_forbidden(all_records)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    outputs = {
        "social_msa": OUT_DIR / "dialogue_batch_v14_social_subfamily_msa_014.jsonl",
        "social_saudi": OUT_DIR / "dialogue_batch_v14_social_subfamily_saudi_014.jsonl",
        "topic_msa": OUT_DIR / "dialogue_batch_v14_topic_variants_msa_014.jsonl",
        "topic_saudi": OUT_DIR / "dialogue_batch_v14_topic_variants_saudi_014.jsonl",
    }
    for key, path in outputs.items():
        _write_jsonl(path, records[key])
        _write_card(
            path.with_suffix(".CARD.md"),
            title=path.name,
            records=len(records[key]),
            description="Phase 27.108 social subfamily/topic variant repair data",
        )

    audits = {key: _audit_summary(path) for key, path in outputs.items()}
    summary = _summarize(records)
    ready = bool(
        summary["total_records"] == 480
        and summary["dialect_counts"] == {"msa": 240, "saudi": 240}
        and set(summary["social_subfamily_counts"].values()) == {30}
        and set(summary["topic_counts"].values()) == {30}
        and all(audit["error_count"] == 0 for audit in audits.values())
        and all(audit["training_ready"] == audit["total_records"] for audit in audits.values())
    )
    decision = {
        "decision_id": "PHASE27_108_SOCIAL_SUBFAMILY_TOPIC_VARIANT_DATA_PACK_DECISION",
        "engineering_decision": (
            "ALLOW_PHASE27_109_SOCIAL_SUBFAMILY_TOPIC_VARIANT_DATA_PACK_AUDIT_NO_TRAINING"
            if ready
            else "BLOCK_PHASE27_109_REPAIR_PHASE27_108_DATA_PACK"
        ),
        "data_pack_written": True,
        "new_training_started": False,
        "phase27_109_audit_allowed": ready,
        "bounded_training_allowed": False,
        "runtime_release_allowed": False,
        "ui_release_allowed": False,
        "sf50m_justified_transition": False,
        "tokenizer_retrain_allowed": False,
        "why": (
            "The pack adds 480 governed gold records: 30 per social subfamily per dialect "
            "and 30 per topic/canonical per dialect. Governance audit is clean for all new files."
            if ready
            else "The pack failed count, balance, or governance audit checks."
        ),
        "next_phase": (
            "Phase 27.109 — Social Subfamily + Topic Variant Data Pack Audit"
            if ready
            else "Phase 27.108b — Social Subfamily + Topic Variant Data Pack Repair"
        ),
    }
    summary = {
        "phase": "Phase 27.108",
        "strategy": "Sovereign Practical Acceleration Strategy v2",
        "sovereignty_mode": "SF-native only",
        "status": (
            "PHASE27_108_DATA_PACK_READY_FOR_AUDIT_NO_TRAINING"
            if ready
            else "PHASE27_108_DATA_PACK_BLOCKED"
        ),
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "training_started": False,
        "runtime_changed": False,
        "files": {key: str(path.relative_to(ROOT)) for key, path in outputs.items()},
        "summary": summary,
        "new_file_audits": audits,
        "decision": decision,
        "next_phase": decision["next_phase"],
    }
    REPORT.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    DECISION.write_text(json.dumps(decision, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _write_doc(summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
