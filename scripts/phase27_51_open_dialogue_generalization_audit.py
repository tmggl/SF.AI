#!/usr/bin/env python3
"""Phase 27.51 open-dialogue generalization audit.

This is intentionally stricter than the guarded UI gate.

Phase 27.50 proved that `/chat/message` no longer exposes templates. It did
not prove that the checkpoint can hold natural conversation. This audit checks
that distinction directly:

1. Live API must never leak templates.
2. Raw checkpoint is tested without intent/topic conditioning so keyword lanes
   cannot make the result look better than it is.
3. Natural prompts are scored for obvious canned/misaligned answer patterns.

No training happens here. A failure is a useful result: it blocks pretending
that SF-10M is already an open conversational model.
"""

from __future__ import annotations

import argparse
import json
import re
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from sf_ai.modules.chat.native_generator import NativeGenerator, NativeGeneratorConfig

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_51_open_dialogue_generalization_audit.json"
DEFAULT_SAMPLES = ROOT / "artifacts/samples/phase27_51_open_dialogue_generalization_audit.md"


@dataclass(frozen=True)
class NaturalCase:
    id: str
    prompt: str
    bucket: str
    expected_terms: tuple[str, ...] = ()
    forbidden_terms: tuple[str, ...] = ()


CASES: tuple[NaturalCase, ...] = (
    # Follow-up / social flow: should not require exact memorised wording.
    NaturalCase("followup_free_choice", "الي تحب", "followup", forbidden_terms=("مهام", "الأهم")),
    NaturalCase("followup_continue", "كمل كلامك", "followup", forbidden_terms=("مهام", "الأهم")),
    NaturalCase("followup_why", "طيب ليه؟", "followup"),
    NaturalCase("followup_meaning", "يعني كيف؟", "followup"),
    # Open social prompts.
    NaturalCase("social_chat", "سولف معي شوي", "open_social"),
    NaturalCase("social_topic_choice", "وش ودك نسولف عنه؟", "open_social"),
    NaturalCase("social_new_topic", "هات موضوع خفيف", "open_social"),
    NaturalCase("social_today", "يومي كان طويل", "open_social"),
    # Topic discussion beyond exact definition lanes.
    NaturalCase("topic_courage_simple", "اخبرني عن الشجاعة بأسلوب بسيط", "topic", expected_terms=("شجاع",)),
    NaturalCase("topic_friendship_talk", "وش رأيك نتكلم عن الصداقة", "topic", expected_terms=("صداق",)),
    NaturalCase("topic_honesty_example", "اعطني مثال بسيط عن الصدق", "topic", expected_terms=("صدق",)),
    NaturalCase("topic_calm_life", "الهدوء في اليوم وش يفيدني؟", "topic", expected_terms=("هدوء",)),
    # Practical requests phrased naturally.
    NaturalCase("planning_day_start", "اشرح لي كيف ابدأ يومي", "planning", expected_terms=("ابدأ",)),
    NaturalCase("planning_confused", "أنا محتار من وين أبدأ", "planning"),
    NaturalCase("planning_many_tasks", "عندي أشياء كثيرة ومتشتت", "planning"),
    NaturalCase("planning_light", "رتب لي بداية بسيطة بدون تعقيد", "planning"),
    # Emotional/support phrasing.
    NaturalCase("support_tired", "تعبان شوي واحتاج كلام يهديني", "support"),
    NaturalCase("support_anxious", "كيف أهدأ إذا توترت؟", "support", expected_terms=("اهد", "نفس", "هدوء")),
    NaturalCase("support_pressure", "حاس بضغط اليوم", "support"),
    NaturalCase("support_short", "طمني بكلام بسيط", "support"),
    # Model identity and capability must remain blocked until learned safely.
    NaturalCase("identity_general", "من أنت؟", "control_blocked"),
    NaturalCase("capability_general", "وش تقدر تسوي؟", "control_blocked"),
)

_TOKEN_RE = re.compile(r"[\w\u0600-\u06FF]+", re.UNICODE)
_CANNED_PHRASES = (
    "اكتب ثلاث مهام",
    "ابدأ بالأهم",
    "الله يعافيك",
    "حاضر بأي وقت",
    "الصداقة رفقة طيبة",
    "الصدق أن تقول الحقيقة",
)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run Phase 27.51 open-dialogue generalization audit")
    p.add_argument("--base-url", default="http://127.0.0.1:8123")
    p.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    p.add_argument("--samples", type=Path, default=DEFAULT_SAMPLES)
    return p.parse_args()


def _post_json(url: str, payload: dict[str, Any]) -> dict[str, Any]:
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST", headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=25) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.URLError as exc:
        raise RuntimeError(f"API request failed: {url} ({exc})") from exc


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


def _token_set(text: str) -> set[str]:
    return set(_TOKEN_RE.findall(_surface(text)))


def _has_canned_phrase(text: str) -> bool:
    surface = _surface(text)
    return any(_surface(phrase) in surface for phrase in _CANNED_PHRASES)


def _terms_present(text: str, terms: tuple[str, ...]) -> bool:
    surface = _surface(text)
    return all(_surface(term) in surface for term in terms)


def _forbidden_absent(text: str, terms: tuple[str, ...]) -> bool:
    surface = _surface(text)
    return not any(_surface(term) in surface for term in terms)


def _overlap_ratio(prompt: str, response: str) -> float:
    p = _token_set(prompt)
    r = _token_set(response)
    if not p or not r:
        return 0.0
    return len(p & r) / max(1, len(p))


def _live_case(base_url: str, case: NaturalCase) -> dict[str, Any]:
    body = _post_json(
        f"{base_url.rstrip('/')}/chat/message",
        {"message": case.prompt, "session_id": f"phase27-51-live-{case.id}"},
    )
    response = str(body.get("response") or "")
    generator = str(body.get("generator") or "")
    if case.bucket == "control_blocked":
        passed = generator == "generator_blocked" and response == ""
        reason = "passed" if passed else "control_not_blocked"
    else:
        passed = (
            generator == "sf_10m_phase27_47"
            and bool(response.strip())
            and _terms_present(response, case.expected_terms)
            and _forbidden_absent(response, case.forbidden_terms)
            and not _has_canned_phrase(response)
        )
        if passed:
            reason = "passed"
        elif generator != "sf_10m_phase27_47":
            reason = f"generator:{generator or 'missing'}"
        elif not response.strip():
            reason = "empty_response"
        elif not _terms_present(response, case.expected_terms):
            reason = "expected_terms_missing"
        elif not _forbidden_absent(response, case.forbidden_terms):
            reason = "forbidden_terms_present"
        else:
            reason = "canned_phrase"
    return {
        "id": case.id,
        "bucket": case.bucket,
        "prompt": case.prompt,
        "mode": "live_api",
        "generator": generator,
        "response": response,
        "intent": body.get("intent"),
        "confidence": body.get("confidence"),
        "notes": (body.get("debug") or {}).get("module_notes"),
        "passed": passed,
        "reason": reason,
    }


def _raw_generator() -> NativeGenerator:
    return NativeGenerator(
        NativeGeneratorConfig(
            tokenizer_path=ROOT / "artifacts/tokenizers/sf_bpe/v6_weak_lane_terms",
            checkpoints_root=ROOT
            / "artifacts/eval/phase27_47_new_topic_conditioning_repair/checkpoints",
            checkpoint_name="sf-10m-step4600",
            generator_name="sf_10m_phase27_47",
            model_size="sf-10m",
            seq_len=64,
            max_new_tokens=36,
            temperature=1.0,
            top_k=0,
            no_repeat_ngram_size=3,
            repetition_penalty=1.1,
            dialogue_prompt=True,
        )
    )


def _raw_case(generator: NativeGenerator, case: NaturalCase) -> dict[str, Any]:
    if case.bucket == "control_blocked":
        return {
            "id": case.id,
            "bucket": case.bucket,
            "prompt": case.prompt,
            "mode": "raw_unconditioned",
            "generator": "not_scored_control",
            "response": "",
            "passed": True,
            "reason": "control_not_raw_scored",
        }
    result = generator.generate(case.prompt, dialect="saudi", intent=None, topic=None)
    response = result.text
    overlap = _overlap_ratio(case.prompt, response)
    passed = (
        result.used
        and bool(response.strip())
        and _terms_present(response, case.expected_terms)
        and _forbidden_absent(response, case.forbidden_terms)
        and not _has_canned_phrase(response)
        and overlap >= 0.15
    )
    if passed:
        reason = "passed"
    elif not result.used:
        reason = result.reason
    elif not _terms_present(response, case.expected_terms):
        reason = "expected_terms_missing"
    elif not _forbidden_absent(response, case.forbidden_terms):
        reason = "forbidden_terms_present"
    elif _has_canned_phrase(response):
        reason = "canned_phrase"
    else:
        reason = f"low_prompt_overlap:{overlap:.2f}"
    return {
        "id": case.id,
        "bucket": case.bucket,
        "prompt": case.prompt,
        "mode": "raw_unconditioned",
        "generator": result.generator,
        "response": response,
        "passed": passed,
        "reason": reason,
        "prompt_overlap": round(overlap, 4),
    }


def _bucket_summary(rows: list[dict[str, Any]], *, mode: str) -> dict[str, dict[str, int]]:
    selected = [row for row in rows if row["mode"] == mode]
    buckets = sorted({str(row["bucket"]) for row in selected})
    return {
        bucket: {
            "passed": sum(1 for row in selected if row["bucket"] == bucket and row["passed"]),
            "total": sum(1 for row in selected if row["bucket"] == bucket),
        }
        for bucket in buckets
    }


def _write_samples(path: Path, rows: list[dict[str, Any]]) -> None:
    lines = ["# Phase 27.51 Open-Dialogue Generalization Audit", ""]
    for row in rows:
        lines.extend(
            [
                f"## {row['mode']} / {row['id']} — {'PASS' if row['passed'] else 'FAIL'}",
                "",
                f"- bucket: {row['bucket']}",
                f"- prompt: {row['prompt']}",
                f"- generator: {row['generator']}",
                f"- response: {row['response'] or '(empty)'}",
                f"- reason: {row['reason']}",
                "",
            ]
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    args = parse_args()
    raw = _raw_generator()
    rows: list[dict[str, Any]] = []
    for case in CASES:
        rows.append(_live_case(args.base_url, case))
        rows.append(_raw_case(raw, case))

    live_rows = [row for row in rows if row["mode"] == "live_api"]
    raw_rows = [row for row in rows if row["mode"] == "raw_unconditioned"]
    live_passed = sum(1 for row in live_rows if row["passed"])
    raw_passed = sum(1 for row in raw_rows if row["passed"])
    live_total = len(live_rows)
    raw_total = len(raw_rows)
    natural_raw_rows = [row for row in raw_rows if row["bucket"] != "control_blocked"]
    natural_raw_passed = sum(1 for row in natural_raw_rows if row["passed"])

    # This phase is expected to be hard. Passing means the current checkpoint can
    # converse without lane conditioning; failing means Phase 27.52 must train.
    passed = live_passed == live_total and natural_raw_passed >= 16
    status = (
        "PASSED_OPEN_DIALOGUE_GENERALIZATION_AUDIT"
        if passed
        else "FAILED_OPEN_DIALOGUE_GENERALIZATION_AUDIT_TRAINING_REQUIRED"
    )
    report = {
        "phase": "Phase 27.51",
        "status": status,
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "training_started": False,
        "template_answers_allowed": False,
        "keyword_lane_success_is_not_enough": True,
        "candidate_generator": "sf_10m_phase27_47",
        "next_phase": "Phase 27.52 natural dialogue objective/corpus repair before any scaling",
        "summary": {
            "live_api": {
                "passed": live_passed,
                "total": live_total,
                "bucket_summary": _bucket_summary(rows, mode="live_api"),
            },
            "raw_unconditioned": {
                "passed": raw_passed,
                "total": raw_total,
                "natural_passed": natural_raw_passed,
                "natural_total": len(natural_raw_rows),
                "bucket_summary": _bucket_summary(rows, mode="raw_unconditioned"),
            },
        },
        "rows": rows,
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _write_samples(args.samples, rows)
    print(json.dumps({"phase": report["phase"], "status": status, "summary": report["summary"]}, ensure_ascii=False))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
