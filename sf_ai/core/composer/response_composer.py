"""ResponseComposer — produces the final reply string.

Cases:
1. Active domain → ChatModule (Phase 4) handles it; the Composer is bypassed.
2. Skeleton-only domain → friendly, domain-specific "not active yet" message.
3. Safety-flagged domain → safe-by-default reply pointing to a specialist.

Strings are short, warm, and honest. They explicitly say what's available
right now and stop short of promising what isn't.
"""

from __future__ import annotations

from dataclasses import dataclass

from sf_ai.core.composer.styles import ResponseStyle
from sf_ai.core.index import DomainManifest


@dataclass(frozen=True)
class ComposedReply:
    text: str
    style: ResponseStyle
    safety_flag: bool = False


# ---------------------- Fallback chat replies (Composer-side) ----------------------

_GREETING = "أهلًا. أنا SF.AI. كيف أقدر أساعدك؟"
_SMALLTALK = "بخير، شكرًا. وأنت؟"
_IDENTITY = (
    "أنا SF.AI — مساعد ذكاء اصطناعي يُبنى من الصفر بسيادة معرفية، "
    "بدون نماذج خارجية."
)
_CAPABILITY = (
    "حاليًا أفهم العربية ولهجاتها، أوجّه السؤال داخل النظام، "
    "وأرد بشكل موضوعي. اسأل «وش تقدر تسوي» لتفاصيل أكثر."
)
_CHAT_GENERAL = (
    "وصلتك. لو خصصت السؤال أقدر أوجّهه أفضل، "
    "أو اسأل «وش تقدر تسوي» لتعرف القدرات المتاحة."
)


# ---------------------- Skeleton domains — per-domain friendly notes ---------------

_SKELETON_PER_DOMAIN: dict[str, str] = {
    "coding": (
        "البرمجة من المجالات المرشّحة للتفعيل لاحقًا. "
        "حاليًا لا أقدر أكتب أو أصلح كودًا فعليًا — هذا يحتاج نموذجًا مدرّبًا "
        "ولم نصل لتلك المرحلة. لكن لو أردت أن نفكّر معًا في فكرة عامة، تفضّل."
    ),
    "data": (
        "تحليل البيانات قادم لاحقًا. الآن ما عندي أدوات تشغيل لـ pandas "
        "أو قراءة ملفات داخل المحادثة. لو شاركت وصف المشكلة بكلمات أفهمها أفضل."
    ),
    "files": (
        "التعامل مع الملفات (PDF/Word/Excel) لم يُفعَّل بعد. أقدر أتحدث "
        "عن محتوى نصي تكتبه لي مباشرة هنا."
    ),
    "web": (
        "البحث في الويب جاهز بنيويًا لكنه غير مفعَّل في هذه الجلسة. "
        "حين يُفعَّل، سيكون عبر روابط تقدّمها أنت، باحترام robots.txt، "
        "بدون أي محرك بحث خارجي."
    ),
    "research": (
        "التلخيص متاح كقاعدة (rule-based) لكنه غير مرتبط بالشات هنا. "
        "حين يُفعَّل، أعطني الروابط وألخّص لك مع ذكر المصادر."
    ),
    "writing": (
        "الكتابة الإبداعية تحتاج نموذجًا مدرّبًا — وهذا قادم لاحقًا. "
        "حاليًا أستطيع المساعدة بصياغة بسيطة ومباشرة فقط."
    ),
    "translation": (
        "الترجمة الفعلية تحتاج نموذجًا مدرّبًا. الآن أستطيع أتعامل مع "
        "كلمات لهجية وأُرجعها إلى الفصحى عبر القاموس الداخلي."
    ),
    "education": (
        "أهلًا بالتعلم. حاليًا قدراتي التعليمية محدودة بالحوار العام. "
        "خلّيني أعرف الموضوع وأحاول أفيدك بما يمكنني."
    ),
    "social": (
        "أهلًا بالحديث. تفضّل، أنا هنا."
    ),
    "productivity": (
        "تنظيم المهام مجال مؤجَّل. حاليًا أنفع كمحاور عام فقط."
    ),
    "image": (
        "الصور لم تُفعَّل بعد. حاليًا نصوص فقط."
    ),
    "audio": (
        "الصوت لم يُفعَّل بعد. حاليًا نصوص فقط."
    ),
    "business": (
        "مجال الأعمال مؤجَّل. حاليًا حوار عام فقط."
    ),
    "ecommerce": (
        "التجارة الإلكترونية مؤجَّلة. حاليًا حوار عام فقط."
    ),
}

_SKELETON_DEFAULT = (
    "هذا المجال ({description}) موجود في الخطة لكنه غير مفعَّل بعد. "
    "نقدر نواصل بحوار عام إذا أحببت."
)


# ---------------------- Safety domains — per-domain reply ------------------------

_SAFETY_PER_DOMAIN: dict[str, str] = {
    "medical": (
        "أرى أن سؤالك صحي/طبي. لن أعطي تشخيصًا أو وصفة. "
        "أنصحك تتواصل مع طبيب مختص. أقدر أكون معك لو حبيت تكتب وتفضفض."
    ),
    "legal": (
        "أرى أن سؤالك قانوني. لن أعطي رأيًا قانونيًا. "
        "الأفضل تستشير محاميًا مرخصًا في موضوعك."
    ),
    "finance": (
        "أرى أن سؤالك مالي/استثماري. لن أعطي توصية مالية. "
        "الأفضل تستشير مستشارًا ماليًا مرخصًا."
    ),
    "security": (
        "هذا مجال أمني/سيبراني حساس. أقدر أتكلم عن الجانب الدفاعي العام "
        "بحدود، لكن بدون تفاصيل قد تُستخدم بشكل ضار."
    ),
    "religion": (
        "هذا موضوع ديني حساس. لن أُفتي. "
        "الأفضل ترجع لمرجع شرعي موثوق في حالتك."
    ),
}

_SAFETY_DEFAULT = (
    "رسالتك تخص مجالًا حساسًا. لن أعطي معلومات تخصصية، "
    "والأفضل تستشير مختصًا في الموضوع."
)


_INTENT_REPLIES: dict[str, str] = {
    "chat.greeting": _GREETING,
    "chat.smalltalk": _SMALLTALK,
    "chat.identity": _IDENTITY,
    "chat.capability": _CAPABILITY,
    "chat.general": _CHAT_GENERAL,
}


class ResponseComposer:
    """Assemble the final reply from the routing decision."""

    def __init__(self, default_style: ResponseStyle = ResponseStyle.ARABIC_FORMAL) -> None:
        self.default_style = default_style

    def compose(
        self,
        domain: DomainManifest,
        intent: str,
        *,
        intent_fallback: bool,
        domain_fallback: bool,
    ) -> ComposedReply:
        if domain.requires_safety:
            text = _SAFETY_PER_DOMAIN.get(domain.name, _SAFETY_DEFAULT)
            return ComposedReply(text=text, style=self.default_style, safety_flag=True)

        if domain.status != "active":
            text = _SKELETON_PER_DOMAIN.get(domain.name)
            if text is None:
                text = _SKELETON_DEFAULT.format(
                    description=domain.description or domain.name,
                )
            return ComposedReply(text=text, style=self.default_style)

        # Active domain — fallback to generic chat reply if a module did not handle it.
        text = _INTENT_REPLIES.get(intent, _CHAT_GENERAL)
        return ComposedReply(text=text, style=self.default_style)
