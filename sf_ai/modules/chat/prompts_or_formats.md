# sf_ai/modules/chat — Prompts & Response Formats (Phase 4)

> هذا ليس prompt-engineering لنموذج خارجي.
> ChatModule لا يتحدث مع أي LLM. هذا الملف يوثّق **قوالب الردود** التي يستخدمها ChatResponseBuilder، ومتى يستخدم كل قالب.

---

## مبدأ التصميم

1. **شفافية أكثر من ذكاء مزيف.** الرد يقول بصراحة ما هو الـ phase الحالي وما هي حدود الرد.
2. **لا توليد حر.** الردود من قوالب محدودة. التنويع يأتي من فهرس القالب بناءً على عدد التكرارات.
3. **لا تقليد لهجة المستخدم.** اللهجة تُسجَّل في `notes` كتعليق تشخيصي، لكن الرد يبقى بالفصحى الواضحة.
4. **حد أقصى للسياق.** آخر 12 turn فقط في الجلسة. الذاكرة طويلة المدى مؤجَّلة (Phase 8 RAG).

---

## القوالب

ملف القوالب: [chat_patterns.py](./chat_patterns.py).

| Intent | عدد القوالب | السلوك |
|--------|--------------|--------|
| `chat.greeting` | 2 | الأول للتحية الأولى، الثاني للتحية المتكررة |
| `chat.smalltalk` | 2 | "كيف حالك" — الثاني عند التكرار |
| `chat.identity` | 1 | "من أنت" — رد واحد متماسك |
| `chat.capability` | 1 | "وش تقدر تسوي" — رد واحد صادق |
| `chat.farewell` | 2 | "وداعًا" / "في أمان الله" |
| `chat.general` | 2 | الـ fallback، يطلب تخصيص الموضوع عند التكرار |

عند ≥ 3 تكرارات لنفس الـ intent في الجلسة (باستثناء `chat.identity`)، تُضاف لاحقة [REPEATED_NOTICE](./chat_patterns.py) كنصيحة لينة بتغيير الموضوع.

---

## شكل ModuleResponse

```python
ModuleResponse(
    text: str,                # الرد النهائي للمستخدم
    intent_used: str,         # الـ intent الذي حُلّ فعلًا
    template_index: int,      # أي قالب اختير
    session_id: str,          # فارغ للجلسات المجهولة
    turn_count: int,          # عدد turns في الذاكرة الآن
    notes: tuple[str, ...],   # ["dialect:الخليجية", "language:ar", ...]
)
```

`notes` يُضاف إلى `OrchestratorResult.debug.module_notes` ويظهر في الـ developer panel.

---

## أمثلة (Phase 4)

| المدخل | Intent | الرد |
|--------|--------|------|
| مرحبا | chat.greeting | "أهلًا. أنا SF.AI..." |
| مرحبا (مرة ثانية بنفس الجلسة) | chat.greeting | "أهلًا مرة أخرى..." |
| كيف حالك | chat.smalltalk | "بخير، شكرًا..." |
| من انت | chat.identity | "أنا SF.AI..." |
| وش تقدر تسوي | chat.capability | "حاليًا (Phase 4) أستطيع..." |
| وداعًا | chat.farewell | "في أمان الله..." |
| أي شيء غير ذلك يقع على chat | chat.general | "وصلتني رسالتك..." |

---

## ما لا يفعله ChatModule (مقصود)

- لا يُكمل كود، لا يلخص نصوصًا، لا يبحث في الويب — هذه قدرات مراحل لاحقة.
- لا يدّعي أنه فهم نبرة المستخدم، لا يطلق أحكامًا، لا يفلسف.
- لا يردّ على الأسئلة الحساسة (legal/medical/finance/security/religion) — تلك يتولاها الـ ResponseComposer برد آمن.
- لا يحفظ ذاكرة بين الجلسات. لا يدّعي ذلك.

---

## مسار النموذج اللغوي الأصيل (Phase 6)

عندما يكتمل SF Native LM، سيتم استبدال محرك ChatResponseBuilder بإنترفيس يقول:

```python
class ChatGenerator(Protocol):
    def generate(self, analysis: NLPAnalysis, intent: str, state: ConversationState) -> str: ...
```

و ChatModule.handle لن يتغير. هذا هو السبب وراء فصل الـ builder عن الـ module في Phase 4 رغم بساطته.
