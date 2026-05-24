#!/usr/bin/env python3
"""Phase 27.103 — Topic Prototype Contrastive Curriculum Pack.

No training. No tokenizer work. No runtime release.

This phase authors a sovereign, local-only curriculum pack that targets the
Phase 27.101/27.102 failure mode: answers drifting to prototype topics such as
الصداقة and الامتنان instead of binding to the requested topic.
"""
# ruff: noqa: E402

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.phase27_26_heldout_objective_repair import _rel
from scripts.phase27_58_tokenizer_bounded_alignment_probe import _surface
from sf_ai.datasets.corpus_governance import audit_jsonl_file_for_training
from sf_ai.datasets.splits import write_split_manifest

DEFAULT_SOURCE = ROOT / "artifacts/reports/phase27_102_topic_prototype_contrastive_gate_report.json"
DEFAULT_OUT = ROOT / "data/corpus/chat/jsonl/dialogue_batch_v12_topic_prototype_contrastive_012.jsonl"
DEFAULT_SPLIT = ROOT / "data/corpus/chat/splits/dialogue_split_v1.json"
DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_103_topic_prototype_contrastive_curriculum_pack_report.json"
DEFAULT_DECISION = ROOT / "artifacts/reports/PHASE27_103_TOPIC_PROTOTYPE_CONTRASTIVE_CURRICULUM_PACK_DECISION.json"
DEFAULT_MANIFEST = ROOT / "artifacts/reports/phase27_103_topic_prototype_contrastive_curriculum_manifest.json"
DEFAULT_SCHEDULE = ROOT / "artifacts/reports/phase27_103_topic_prototype_contrastive_curriculum_schedule.json"
DEFAULT_DOC = ROOT / "docs/PHASE27_103_TOPIC_PROTOTYPE_CONTRASTIVE_CURRICULUM_PACK_REPORT.md"

TARGET_DIALECTS: tuple[str, ...] = ("msa", "saudi")
TARGET_TERMS: tuple[str, ...] = (
    "الوفاء",
    "التعاون",
    "الصبر",
    "الاحترام",
    "الهدوء",
    "الصدق",
    "الصداقة",
    "الشجاعة",
)
PROTOTYPE_DECOYS: tuple[str, ...] = ("الصداقة", "الامتنان")

TOPIC_MEANINGS: dict[str, dict[str, tuple[str, ...]]] = {
    "الوفاء": {
        "msa": (
            "الثبات على العهد وحفظ المعروف وقت التغيّر",
            "حفظ الود والالتزام بما وعد به الإنسان",
            "ألا تنسى من أحسن إليك عند الحاجة",
            "صدق البقاء مع من وثق بك",
        ),
        "saudi": (
            "إنك تثبت على وعدك وتحفظ معروف الناس",
            "إنك ما تنسى اللي وقف معك وقت الحاجة",
            "إنك تبقى صادق مع اللي وثق فيك",
            "إنك تحفظ العهد حتى لو تغيرت الظروف",
        ),
    },
    "التعاون": {
        "msa": (
            "مشاركة الجهد حتى يخف الحمل على الجميع",
            "أن يعمل الناس معًا لإنجاز أمر نافع",
            "تبادل المساعدة بدل أن يتحمل الفرد كل شيء",
            "تقاسم المسؤولية للوصول إلى نتيجة أفضل",
        ),
        "saudi": (
            "إنك تساعد غيرك ويتعاونون معك على الشي النافع",
            "إن الكل يشيل جزء من الشغل بدل شخص واحد",
            "إنك تمد يدك للي يحتاج وتقبل المساعدة",
            "إن الناس ينجزون مع بعض بشكل أيسر",
        ),
    },
    "الصبر": {
        "msa": (
            "احتمال الصعوبة مع الثبات وحسن التصرف",
            "تهدئة النفس حتى تمر الشدة بلا تهور",
            "قوة داخلية تمنع الاستعجال وقت الضيق",
            "القدرة على الانتظار والعمل رغم التعب",
        ),
        "saudi": (
            "إنك تتحمل الضيق وتتصرف بهدوء",
            "إنك ما تستعجل وأنت تحت ضغط",
            "إنك تثبت شوي لين تعدي الصعوبة",
            "إنك تواصل رغم التعب بدون تهور",
        ),
    },
    "الاحترام": {
        "msa": (
            "تقدير الناس بالكلمة الطيبة وحفظ الحدود",
            "معاملة الآخرين بلطف وإنصاف دون تقليل",
            "إعطاء كل شخص قدره في الحديث والتعامل",
            "أن تراعي حق غيرك كما تحب أن يراعي حقك",
        ),
        "saudi": (
            "إنك تقدر الناس بكلامك وتصرفك",
            "إنك تحفظ حدودك وما تقلل من أحد",
            "إنك تعامل غيرك بلطف حتى لو اختلفت معه",
            "إنك تعطي كل شخص قدره في الكلام",
        ),
    },
    "الهدوء": {
        "msa": (
            "اتزان النفس عند المواقف المزعجة",
            "التصرف بروية بدل الانفعال السريع",
            "راحة داخلية تساعد على رؤية الأمر بوضوح",
            "إبطاء الرد حتى يستقر التفكير",
        ),
        "saudi": (
            "إنك تهدي نفسك قبل ما ترد",
            "إنك تاخذ نفس وتفكر بدل الانفعال",
            "إنك تخفف توترك وتشوف الموضوع أوضح",
            "إنك تتصرف بروية وقت الزحمة والضغط",
        ),
    },
    "الصدق": {
        "msa": (
            "مطابقة الكلام للفعل والحقيقة",
            "أن تقول ما تعلمه بلا تزيين ولا خداع",
            "وضوح النية والكلمة في التعامل",
            "الالتزام بالحقيقة ولو كان الأمر صعبًا",
        ),
        "saudi": (
            "إن كلامك يكون واضح ومطابق للواقع",
            "إنك تقول الحقيقة بدون لف ودوران",
            "إن فعلك يوافق كلامك قدام الناس",
            "إنك تكون صريح حتى لو الموقف صعب",
        ),
    },
    "الصداقة": {
        "msa": (
            "علاقة مودة ومساندة تقوم على الثقة",
            "قرب إنساني يظهر في السؤال والوقوف وقت الحاجة",
            "صحبة طيبة تحفظ الود وتعين على الخير",
            "رابطة بين شخصين تقوى بالثقة وحسن العشرة",
        ),
        "saudi": (
            "إن بينك وبين شخص مودة ووقفة وقت الحاجة",
            "إنك تلقى خوي يسأل عنك ويوقف معك",
            "إن العلاقة تكون طيبة وفيها ثقة وراحة",
            "إنك تصحب شخص يعينك على الخير",
        ),
    },
    "الشجاعة": {
        "msa": (
            "الإقدام على الصواب مع إدراك الخوف",
            "قوة تجعل الإنسان يفعل الحق دون تهور",
            "ثبات القلب عند القرار الصعب",
            "مواجهة الموقف بحكمة لا باندفاع",
        ),
        "saudi": (
            "إنك تسوي الصح حتى لو كنت خايف",
            "إنك تواجه الموقف بحكمة بدون تهور",
            "إن قلبك يثبت وقت القرار الصعب",
            "إنك تقدم على الحق وأنت فاهم العاقبة",
        ),
    },
}

MSA_PROMPTS: tuple[str, ...] = (
    "ما معنى {topic} بجملة قصيرة؟",
    "عرّف {topic} دون إطالة.",
    "اشرح {topic} بعبارة بسيطة.",
    "كيف أفهم {topic} في الحياة اليومية؟",
    "أعطني معنى {topic} بكلام واضح.",
    "ما المقصود بـ {topic}؟",
)
SAUDI_PROMPTS: tuple[str, ...] = (
    "وش يعني {topic} باختصار؟",
    "{topic} وش معناه؟",
    "علمني عن {topic} بجملة وحدة.",
    "كيف أفهم {topic} بالحياة اليومية؟",
    "ابي معنى {topic} بكلام بسيط.",
    "{topic} يعني ايش؟",
)
PREFIXES: tuple[str, ...] = (
    "{topic} يعني {body}.",
    "معنى {topic}: {body}.",
    "{topic} هو {body}.",
)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Author Phase 27.103 topic-prototype curriculum pack")
    p.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    p.add_argument("--out", type=Path, default=DEFAULT_OUT)
    p.add_argument("--split", type=Path, default=DEFAULT_SPLIT)
    p.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    p.add_argument("--decision", type=Path, default=DEFAULT_DECISION)
    p.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    p.add_argument("--schedule", type=Path, default=DEFAULT_SCHEDULE)
    p.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    return p.parse_args(argv)


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(path)
    return json.loads(path.read_text(encoding="utf-8"))


def _assistant_variants(topic: str, dialect: str) -> list[str]:
    bodies = TOPIC_MEANINGS[topic][dialect]
    out: list[str] = []
    for index, body in enumerate(bodies):
        for prefix in PREFIXES:
            out.append(prefix.format(topic=topic, body=body))
        # Four bodies * three prefixes = twelve records per topic/dialect.
        if index == len(bodies) - 1:
            break
    return out


def _prompt_for(topic: str, dialect: str, index: int) -> str:
    prompts = SAUDI_PROMPTS if dialect == "saudi" else MSA_PROMPTS
    return prompts[index % len(prompts)].format(topic=topic)


def _forbidden_terms(topic: str) -> list[str]:
    return [term for term in TARGET_TERMS if term != topic] + [
        decoy for decoy in PROTOTYPE_DECOYS if decoy != topic
    ]


def _record(topic: str, dialect: str, index: int, user: str, assistant: str) -> dict[str, Any]:
    return {
        "domain": "chat",
        "lang": "ar",
        "messages": [
            {"role": "user", "content": user},
            {"role": "assistant", "content": assistant},
        ],
        "provenance": {
            "source": "sf-ai-topic-prototype-contrastive-curriculum-v1",
            "license": "owner-approved-for-sf-ai-training",
            "language": "ar",
            "dialect": dialect,
            "quality": "gold",
            "training_allowed": True,
            "owner_user_id": "sami-local",
            "created_by_user_id": "sf-ai-local-author",
            "target_user_id": "sami-local",
            "user_scope": "single_user",
            "dialogue_family": "topic",
            "prompt_family": "topic",
            "answer_family": "topic",
            "topic_term": topic,
            "notes": (
                "owner-delegated local Arabic/Saudi topic binding curriculum; "
                "no external dataset; no pretrained output"
            ),
        },
    }


def _records() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for topic in TARGET_TERMS:
        for dialect in TARGET_DIALECTS:
            variants = _assistant_variants(topic, dialect)
            for idx, assistant in enumerate(variants):
                records.append(
                    _record(
                        topic=topic,
                        dialect=dialect,
                        index=idx + 1,
                        user=_prompt_for(topic, dialect, idx),
                        assistant=assistant,
                    )
                )
    return records


def _write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [json.dumps(record, ensure_ascii=False, sort_keys=True) for record in records]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _message_text(record: dict[str, Any], role: str) -> str:
    return " ".join(
        str(message["content"]).strip()
        for message in record["messages"]
        if message["role"] == role and str(message["content"]).strip()
    )


def _copy_anchor_ok(text: str, topic: str, max_visible_arabic_chars: int = 12) -> bool:
    compact_text = "".join(_surface(text).split())
    compact_topic = "".join(_surface(topic).split())
    if not compact_topic:
        return False
    idx = compact_text.find(compact_topic)
    return idx != -1 and idx <= max_visible_arabic_chars


def _wrong_topic_hits(text: str, topic: str) -> list[str]:
    surface = _surface(text)
    hits = []
    for term in dict.fromkeys((*TARGET_TERMS, *PROTOTYPE_DECOYS)):
        if term != topic and _surface(term) in surface:
            hits.append(term)
    return hits


def _pack_quality(records: list[dict[str, Any]]) -> dict[str, Any]:
    topic_counts: Counter[str] = Counter()
    dialect_counts: Counter[str] = Counter()
    topic_dialect_counts: Counter[str] = Counter()
    bad_copy_anchor: list[dict[str, str]] = []
    wrong_topic_leaks: list[dict[str, Any]] = []
    duplicate_pairs: Counter[str] = Counter()

    for record in records:
        provenance = record["provenance"]
        topic = str(provenance["topic_term"])
        dialect = str(provenance["dialect"])
        assistant = _message_text(record, "assistant")
        user = _message_text(record, "user")
        topic_counts[topic] += 1
        dialect_counts[dialect] += 1
        topic_dialect_counts[f"{topic}/{dialect}"] += 1
        duplicate_pairs[f"{user}\n{assistant}"] += 1
        if not _copy_anchor_ok(assistant, topic):
            bad_copy_anchor.append({"topic": topic, "dialect": dialect, "assistant": assistant})
        wrong = _wrong_topic_hits(assistant, topic)
        if wrong:
            wrong_topic_leaks.append(
                {"topic": topic, "dialect": dialect, "wrong_terms": wrong, "assistant": assistant}
            )

    duplicate_count = sum(count - 1 for count in duplicate_pairs.values() if count > 1)
    return {
        "records": len(records),
        "target_terms": list(TARGET_TERMS),
        "records_per_topic": dict(topic_counts),
        "records_per_dialect": dict(dialect_counts),
        "records_per_topic_dialect": dict(topic_dialect_counts),
        "min_per_topic": min(topic_counts.values()) if topic_counts else 0,
        "max_per_topic": max(topic_counts.values()) if topic_counts else 0,
        "min_per_topic_dialect": min(topic_dialect_counts.values()) if topic_dialect_counts else 0,
        "max_per_topic_dialect": max(topic_dialect_counts.values()) if topic_dialect_counts else 0,
        "copy_anchor_bad_count": len(bad_copy_anchor),
        "copy_anchor_bad_examples": bad_copy_anchor[:8],
        "wrong_topic_leak_count": len(wrong_topic_leaks),
        "wrong_topic_leak_examples": wrong_topic_leaks[:8],
        "duplicate_pair_count": duplicate_count,
        "balanced": bool(
            len(records) == 192
            and set(topic_counts) == set(TARGET_TERMS)
            and set(dialect_counts) == set(TARGET_DIALECTS)
            and min(topic_counts.values()) == max(topic_counts.values()) == 24
            and min(topic_dialect_counts.values()) == max(topic_dialect_counts.values()) == 12
        ),
    }


def _audit_json(report: Any) -> dict[str, Any]:
    return {
        "path": str(report.path) if report.path else "",
        "total_records": report.total_records,
        "training_ready": report.training_ready,
        "error_count": report.error_count,
        "dialect_counts": report.dialect_counts,
        "quality_counts": report.quality_counts,
        "source_counts": report.source_counts,
        "issues": [
            {
                "line_number": issue.line_number,
                "kind": issue.kind,
                "message": issue.message,
                "snippet": issue.snippet,
            }
            for issue in report.issues
        ],
    }


def _schedule(records: list[dict[str, Any]]) -> dict[str, Any]:
    buckets: dict[tuple[str, str], list[int]] = {
        (topic, dialect): []
        for topic in TARGET_TERMS
        for dialect in TARGET_DIALECTS
    }
    for idx, record in enumerate(records, start=1):
        provenance = record["provenance"]
        buckets[(str(provenance["topic_term"]), str(provenance["dialect"]))].append(idx)

    sequence: list[dict[str, Any]] = []
    max_len = max(len(items) for items in buckets.values())
    for round_idx in range(max_len):
        for dialect in TARGET_DIALECTS:
            for topic in TARGET_TERMS:
                items = buckets[(topic, dialect)]
                if round_idx < len(items):
                    sequence.append(
                        {
                            "record_line": items[round_idx],
                            "topic": topic,
                            "dialect": dialect,
                        }
                    )
    first_64 = sequence[:64]
    first_64_topics = Counter(item["topic"] for item in first_64)
    first_64_dialects = Counter(item["dialect"] for item in first_64)
    adjacent_same_topic = sum(
        1
        for left, right in zip(sequence, sequence[1:], strict=False)
        if left["topic"] == right["topic"]
    )
    return {
        "schedule_id": "phase27_103_topic_dialect_round_robin_schedule_v1",
        "strategy": "topic_then_dialect_round_robin",
        "total_records": len(sequence),
        "first_64_topic_counts": dict(first_64_topics),
        "first_64_dialect_counts": dict(first_64_dialects),
        "adjacent_same_topic_count": adjacent_same_topic,
        "first_32": sequence[:32],
        "training_usage_note": (
            "Next bounded training must consume this pack through a topic/dialect round-robin "
            "view, not a contiguous topic block. The schedule intentionally avoids adjacent "
            "records for the same topic."
        ),
    }


def build_report(args: argparse.Namespace) -> dict[str, Any]:
    source = _load_json(args.source)
    source_decision = source["decision"]["engineering_decision"]
    if source_decision != (
        "ALLOW_PHASE27_103_TOPIC_PROTOTYPE_CONTRASTIVE_CURRICULUM_PACK_NO_TRAINING"
    ):
        raise ValueError("Phase 27.102 did not allow Phase 27.103 curriculum pack")

    records = _records()
    _write_jsonl(args.out, records)
    file_audit = audit_jsonl_file_for_training(args.out)
    quality = _pack_quality(records)
    schedule = _schedule(records)
    split_manifest = write_split_manifest(
        ROOT / "data/corpus/chat/jsonl",
        args.split,
        eval_ratio=0.10,
        salt="sf-ai-dialogue-v1",
    )
    manifest = {
        "manifest_id": "phase27_103_topic_prototype_contrastive_curriculum_manifest",
        "phase": "Phase 27.103",
        "pack_file": _rel(args.out),
        "records": len(records),
        "language_track": list(TARGET_DIALECTS),
        "target_terms": list(TARGET_TERMS),
        "prototype_decoys_guarded": list(PROTOTYPE_DECOYS),
        "quality_rules": {
            "assistant_copy_anchor_required": True,
            "assistant_wrong_topic_leak_max": 0,
            "records_per_topic": 24,
            "records_per_topic_dialect": 12,
            "duplicate_pair_max": 0,
        },
        "curriculum_order": schedule["strategy"],
        "next_training_flag_requirement": "topic/dialect round-robin pack view",
    }
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    args.schedule.parent.mkdir(parents=True, exist_ok=True)
    args.schedule.write_text(json.dumps(schedule, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    ready = bool(
        file_audit.error_count == 0
        and file_audit.training_ready == len(records)
        and quality["balanced"]
        and quality["copy_anchor_bad_count"] == 0
        and quality["wrong_topic_leak_count"] == 0
        and quality["duplicate_pair_count"] == 0
        and schedule["total_records"] == len(records)
        and set(schedule["first_64_topic_counts"]) == set(TARGET_TERMS)
        and schedule["first_64_dialect_counts"] == {"msa": 32, "saudi": 32}
        and schedule["adjacent_same_topic_count"] == 0
    )
    decision = {
        "decision_id": "PHASE27_103_TOPIC_PROTOTYPE_CONTRASTIVE_CURRICULUM_PACK_DECISION",
        "engineering_decision": (
            "ALLOW_PHASE27_104_BOUNDED_TOPIC_PROTOTYPE_CONTRASTIVE_REPAIR_TRAINING"
            if ready
            else "BLOCK_PHASE27_104_FIX_TOPIC_PROTOTYPE_CURRICULUM_PACK"
        ),
        "new_training_started": False,
        "phase27_104_training_allowed": ready,
        "runtime_release_allowed": False,
        "ui_release_allowed": False,
        "sf50m_justified_transition": False,
        "tokenizer_retrain_allowed": False,
        "why": (
            "The pack is balanced across 8 topics and 2 dialects, every assistant answer "
            "copy-anchors the requested topic first, and no assistant answer leaks a different "
            "topic/prototype term. One bounded SF-10M repair may be planned next; runtime remains blocked."
            if ready
            else "The curriculum pack failed one or more balance/copy-anchor/governance gates."
        ),
        "next_phase": (
            "Phase 27.104 — Bounded Topic Prototype Contrastive Repair Training"
            if ready
            else "Phase 27.103b — Topic Prototype Curriculum Pack Repair"
        ),
    }
    return {
        "phase": "Phase 27.103",
        "strategy": "Sovereign Practical Acceleration Strategy v2",
        "sovereignty_mode": "SF-native only",
        "status": (
            "PHASE27_103_TOPIC_PROTOTYPE_CURRICULUM_PACK_READY_FOR_BOUNDED_TRAINING"
            if ready
            else "PHASE27_103_TOPIC_PROTOTYPE_CURRICULUM_PACK_BLOCKED"
        ),
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "training_started": False,
        "runtime_changed": False,
        "source_report": _rel(args.source),
        "authored_file": _rel(args.out),
        "manifest": _rel(args.manifest),
        "schedule": _rel(args.schedule),
        "records_authored": len(records),
        "quality": quality,
        "file_audit": _audit_json(file_audit),
        "split_manifest": {
            "path": _rel(args.split),
            "total_records": split_manifest["total_records"],
            "counts": split_manifest["counts"],
            "dialects": split_manifest["dialects"],
            "qualities": split_manifest["qualities"],
        },
        "blocked_actions": [
            "runtime release",
            "UI generator release",
            "SF-50M transition",
            "tokenizer retrain",
            "pretrained/open-weight usage",
            "template masking",
        ],
        "allowed_next_actions": [
            "one bounded SF-10M topic-prototype contrastive repair training",
            "must evaluate Phase 27.102 canary before any runtime decision",
            "must keep observed wrong-topic at 0 and copy-anchor at 16/16",
        ]
        if ready
        else ["repair this curriculum pack only"],
        "decision": decision,
    }


def _write_doc(path: Path, report: dict[str, Any]) -> None:
    decision = report["decision"]
    quality = report["quality"]
    lines = [
        "# Phase 27.103 — Topic Prototype Contrastive Curriculum Pack",
        "",
        "## الخلاصة",
        "",
        "هذه مرحلة حزمة بيانات فقط: لا تدريب، لا runtime، لا tokenizer.",
        "",
        f"- status: `{report['status']}`",
        f"- decision: `{decision['engineering_decision']}`",
        f"- authored file: `{report['authored_file']}`",
        f"- records authored: `{report['records_authored']}`",
        f"- records per topic: `{quality['records_per_topic']}`",
        f"- records per dialect: `{quality['records_per_dialect']}`",
        f"- copy-anchor bad count: `{quality['copy_anchor_bad_count']}`",
        f"- wrong-topic leak count: `{quality['wrong_topic_leak_count']}`",
        f"- duplicate pair count: `{quality['duplicate_pair_count']}`",
        f"- training started: `{report['training_started']}`",
        f"- phase27_104 training allowed: `{decision['phase27_104_training_allowed']}`",
        f"- runtime release: `{decision['runtime_release_allowed']}`",
        f"- next: `{decision['next_phase']}`",
        "",
        "## لماذا هذه الحزمة؟",
        "",
        "Phase 27.102 أثبتت أن wrong-topic يجب أن يُحسب من نص الرد نفسه. "
        "هذه الحزمة تجعل رد المساعد يبدأ بالموضوع المطلوب، وتمنع تسرب موضوع "
        "آخر داخل رد المساعد.",
        "",
        "## القرار",
        "",
        decision["why"],
        "",
        "## المحظور",
        "",
    ]
    for item in report["blocked_actions"]:
        lines.append(f"- {item}")
    lines.extend(["", "## المسموح تاليًا", ""])
    for item in report["allowed_next_actions"]:
        lines.append(f"- {item}")
    lines.append("")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    args = parse_args()
    try:
        report = build_report(args)
    except (FileNotFoundError, json.JSONDecodeError, KeyError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    args.decision.parent.mkdir(parents=True, exist_ok=True)
    args.decision.write_text(
        json.dumps(report["decision"], ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    _write_doc(args.doc, report)
    print(json.dumps(report["decision"], ensure_ascii=False, indent=2))
    return 0 if report["decision"]["phase27_104_training_allowed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
