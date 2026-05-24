#!/usr/bin/env python3
"""Phase 27.68 targeted repair for Phase 27.67 shadow failures.

Phase 27.67 proved that the Phase 27.66 candidate overfit the known canary:
fresh unseen prompts passed only 30/50. This phase trains a bounded SF-10M
repair on tokenizer v8 with targeted family-disambiguation examples for the
failed lanes. It then evaluates:

1. Phase 27.67 fresh shadow canary (known failure set after this repair).
2. Phase 27.60 broader canary as a regression check.

Runtime remains blocked regardless of the result. A pass only allows a later
new fresh-shadow canary; it does not allow UI/runtime activation.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from collections import defaultdict
from itertools import cycle
from pathlib import Path
from typing import Any

import torch

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.phase27_17_prompt_answer_micro_probe import _latest_checkpoint_name  # noqa: E402
from scripts.phase27_19_hygiene_repair_probe import _write_probe_corpus  # noqa: E402
from scripts.phase27_26_heldout_objective_repair import RepairPair, _rel  # noqa: E402
from scripts.phase27_39_topic_isolation_repair import _conditioned_record  # noqa: E402
from scripts.phase27_60_broader_natural_dialogue_canary import _evaluate as evaluate_phase27_60, _summary as summary_phase27_60  # noqa: E402
from scripts.phase27_62_family_balance_repair import FAMILY_BALANCE_REPAIR  # noqa: E402
from scripts.phase27_66_v8_bounded_topic_repair import TOPIC_EMPHASIS_REPAIR  # noqa: E402
from scripts.phase27_67_fresh_shadow_canary import _evaluate as evaluate_phase27_67, _summary as summary_phase27_67  # noqa: E402
from sf_ai.training.train_tiny_lm import run as train_tiny_lm_run  # noqa: E402


DEFAULT_TOKENIZER = ROOT / "artifacts/tokenizers/sf_bpe/v8_phase27_65"
DEFAULT_WORK = ROOT / "artifacts/eval/phase27_68_shadow_failure_repair"
DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_68_shadow_failure_repair_report.json"
DEFAULT_SAMPLES = ROOT / "artifacts/samples/phase27_68_shadow_failure_repair.md"
DEFAULT_DOC = ROOT / "docs/PHASE27_68_SHADOW_FAILURE_REPAIR_REPORT.md"


SHADOW_FAILURE_REPAIR: tuple[RepairPair, ...] = (
    # Open social: keep casual conversation away from topic definitions/planning.
    RepairPair("saudi", "افتح لي سالفة بسيطة", "نبدأ بموضوع بسيط وخفيف عن يومك.", ("موضوع", "يومك"), "open_social"),
    RepairPair("msa", "لنبدأ حديثًا عاديًا", "نبدأ حديثًا عاديًا عن موضوع خفيف.", ("حديث", "موضوع"), "open_social"),
    RepairPair("saudi", "ابي كلام عادي بدون موضوع كبير", "نسولف بكلام عادي وخفيف بدون موضوع كبير.", ("نسولف", "موضوع"), "open_social"),
    RepairPair("saudi", "وش سالفتك اليوم", "سالفتنا اليوم خفيفة: نسولف عن يومك.", ("سالفة", "يومك"), "open_social"),
    RepairPair("msa", "أريد حوارًا بسيطًا لا أكثر", "نفتح موضوعًا بسيطًا وخفيفًا.", ("موضوع", "بسيط"), "open_social"),
    RepairPair("msa", "افتح معي حوارًا قصيرًا", "نفتح موضوعًا قصيرًا وخفيفًا.", ("موضوع", "قصير"), "open_social"),
    RepairPair("msa", "هات فكرة لطيفة للكلام", "فكرة لطيفة: نتحدث عن موضوع بسيط من يومك.", ("فكرة", "موضوع"), "open_social"),
    RepairPair("saudi", "سولف لي عن شيء عادي", "أكيد، نسولف عن موضوع عادي وخفيف.", ("نسولف", "موضوع"), "open_social"),
    RepairPair("msa", "دعنا نتكلم بلا تعقيد", "نتكلم ببساطة عن موضوع خفيف.", ("نتكلم", "موضوع"), "open_social"),
    RepairPair("saudi", "خل الجو خفيف وسولف", "أبشر، نسولف بسالفة خفيفة عن يومك.", ("نسولف", "خفيفة"), "open_social"),
    # Follow-up: interpret clarification requests as clarification, not social chat/support.
    RepairPair("saudi", "ما وضحت لي زين", "أقصد الفكرة ببساطة: خذ خطوة واضحة ثم كمل.", ("أقصد", "خطوة"), "followup"),
    RepairPair("msa", "أعد المعنى بطريقة أوضح", "أقصد أن نوضح الفكرة بخطوة أبسط.", ("أقصد", "الفكرة"), "followup"),
    RepairPair("msa", "ما الفكرة التي تريدها بالضبط", "أقصد الفكرة الأساسية: ابدأ من الجزء الواضح.", ("أقصد", "الفكرة"), "followup"),
    RepairPair("saudi", "يعني وش المطلوب مني", "يعني المطلوب خطوة صغيرة وواضحة الآن.", ("يعني", "خطوة"), "followup"),
    RepairPair("saudi", "ما دخلت مخي اشرحها", "أقصدها ببساطة: نوضح الفكرة خطوة خطوة.", ("أقصد", "الفكرة"), "followup"),
    RepairPair("msa", "تابع الشرح من النقطة الأخيرة", "نكمل من النقطة الأخيرة بخطوة أوضح.", ("نكمل", "خطوة"), "followup"),
    RepairPair("saudi", "وضح لي مقصدك", "أقصد المعنى ببساطة وبخطوة واضحة.", ("أقصد", "وضح"), "followup"),
    RepairPair("msa", "أريد شرحًا أقرب", "أبسطها لك: الفكرة خطوة واضحة ثم متابعة.", ("أبسط", "الفكرة"), "followup"),
    # Planning: keep task organization away from definitions/open social.
    RepairPair("msa", "رتب لي بداية عملية", "رتب البداية هكذا: اختر مهمة واحدة وابدأ بها.", ("رتب", "مهمة"), "planning"),
    RepairPair("saudi", "عندي لخبطة بالمهام", "اكتب المهام، واختر الأهم ثم ابدأ بخطوة.", ("مهام", "الأهم"), "planning"),
    RepairPair("msa", "دلني على خطة قصيرة", "خطة قصيرة: مهمة واحدة الآن، ثم خطوة بعدها.", ("خطة", "مهمة"), "planning"),
    RepairPair("saudi", "ابي ارتب شغلي اليوم", "رتب شغلك بثلاث مهام وابدأ بالأهم.", ("رتب", "مهام"), "planning"),
    RepairPair("msa", "كيف أجعل عملي أوضح", "اجعل العمل أوضح بمهمة واحدة وخطوة محددة.", ("مهمة", "خطوة"), "planning"),
    # Support: keep emotional support away from planning-only answers.
    RepairPair("saudi", "مضغوط شوي وش اسوي", "خذ نفسًا هادئًا وخفف الضغط خطوة خطوة.", ("نفس", "خفف"), "support"),
    RepairPair("msa", "أنا مرتبك وأريد هدوءًا", "تنفس بهدوء وامنح نفسك لحظة راحة.", ("تنفس", "راحة"), "support"),
    RepairPair("saudi", "ابي اروق بدون كلام كثير", "خذ نفسًا بسيطًا وخلها تهدأ شوي.", ("نفس", "تهدأ"), "support"),
    RepairPair("saudi", "احس اني مشتت ومتوتر", "خذ نفسًا وركز على شيء واحد الآن.", ("نفس", "ركز"), "support"),
    RepairPair("msa", "أريد تهدئة سريعة", "تنفس بهدوء وخذ لحظة راحة قصيرة.", ("تنفس", "راحة"), "support"),
    RepairPair("saudi", "ضغطي زاد شوي", "هونها على نفسك وخذ نفس هادئ.", ("هون", "نفس"), "support"),
    # Topic: repair the one remaining fresh topic collapse.
    RepairPair("msa", "الشجاعة متى تظهر", "الشجاعة تظهر حين تفعل الصواب مع وجود الخوف.", ("الشجاعة",), "topic"),
    RepairPair("msa", "فسر الوفاء بجملة قصيرة", "الوفاء حفظ للعهد وثبات في الود.", ("الوفاء",), "topic"),
    RepairPair("msa", "عرّف الصبر تعريفًا بسيطًا", "الصبر ثبات وهدوء وقت الصعوبة.", ("الصبر",), "topic"),
    RepairPair("saudi", "الصبر كيف تفهمه", "الصبر إنك تتحمل وتكمل بدون استعجال.", ("الصبر",), "topic"),
)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run Phase 27.68 targeted shadow-failure repair")
    p.add_argument("--tokenizer", type=Path, default=DEFAULT_TOKENIZER)
    p.add_argument("--steps", type=int, default=5600)
    p.add_argument("--epochs", type=int, default=560)
    p.add_argument("--batch-size", type=int, default=1)
    p.add_argument("--seq-len", type=int, default=80)
    p.add_argument("--lr", type=float, default=3.5e-4)
    p.add_argument("--warmup", type=int, default=200)
    p.add_argument("--target-per-family", type=int, default=1250)
    p.add_argument("--device", default="auto")
    p.add_argument("--work-dir", type=Path, default=DEFAULT_WORK)
    p.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    p.add_argument("--samples", type=Path, default=DEFAULT_SAMPLES)
    p.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    p.add_argument("--keep-work", action="store_true")
    return p.parse_args()


def _repair_pairs() -> tuple[RepairPair, ...]:
    return (*FAMILY_BALANCE_REPAIR, *TOPIC_EMPHASIS_REPAIR, *SHADOW_FAILURE_REPAIR)


def _family_groups() -> dict[str, list[RepairPair]]:
    grouped: dict[str, list[RepairPair]] = defaultdict(list)
    for pair in _repair_pairs():
        grouped[pair.category].append(pair)
    return dict(sorted(grouped.items()))


def _records(target_per_family: int) -> list[dict[str, Any]]:
    grouped = _family_groups()
    iterators = {family: cycle(pairs) for family, pairs in grouped.items()}
    counts = {family: 0 for family in grouped}
    records: list[dict[str, Any]] = []
    idx = 68000
    while any(count < target_per_family for count in counts.values()):
        for family in grouped:
            if counts[family] >= target_per_family:
                continue
            idx += 1
            counts[family] += 1
            records.append(_conditioned_record(next(iterators[family]), idx))
    return records


def _write_samples(path: Path, shadow_rows: list[dict[str, Any]], regression_rows: list[dict[str, Any]]) -> None:
    lines = ["# Phase 27.68 Shadow Failure Repair", "", "## Phase 27.67 shadow canary", ""]
    for row in shadow_rows:
        lines.extend(
            [
                f"### {row['id']} — {'PASS' if row['passed'] else 'FAIL'}",
                "",
                f"- family: {row['family']}",
                f"- prompt: {row['prompt']}",
                f"- response: {row['response']}",
                f"- reason: {row['reason']}",
                "",
            ]
        )
    lines.extend(["", "## Phase 27.60 regression canary", ""])
    for row in regression_rows:
        lines.extend(
            [
                f"### {row['id']} — {'PASS' if row['passed'] else 'FAIL'}",
                "",
                f"- family: {row['family']}",
                f"- prompt: {row['prompt']}",
                f"- response: {row['response']}",
                f"- reason: {row['reason']}",
                "",
            ]
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_doc(report: dict[str, Any], path: Path) -> None:
    shadow = report["shadow_summary"]
    regression = report["regression_summary"]
    lines = [
        "# Phase 27.68 — Shadow Failure Repair",
        "",
        "## الخلاصة",
        "",
        "هذه مرحلة تدريب إصلاح محدودة على فشل Phase 27.67. لا تفتح الواجهة ولا تغيّر runtime.",
        "",
        f"- status: `{report['status']}`",
        f"- tokenizer: `{report['tokenizer']}`",
        f"- checkpoint: `{report['checkpoint_root']}/{report['checkpoint_name']}`",
        f"- Phase 27.67 shadow: `{shadow['passed']}/{shadow['total']}`",
        f"- Phase 27.60 regression: `{regression['passed']}/{regression['total']}`",
        f"- runtime switch allowed: `{report['decisions']['runtime_switch_allowed']}`",
        "",
        "## shadow family summary",
        "",
    ]
    for family, item in shadow["family_summary"].items():
        lines.append(f"- `{family}`: `{item['passed']}/{item['total']}`")
    lines.extend(["", "## القرار", "", report["decision"], "", "## التالي", "", report["next_phase"]])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    if not (args.tokenizer / "meta.json").exists():
        print(f"error: missing tokenizer at {args.tokenizer}", file=sys.stderr)
        return 1

    if args.work_dir.exists() and not args.keep_work:
        shutil.rmtree(args.work_dir)
    corpus_dir = args.work_dir / "corpus"
    checkpoints = args.work_dir / "checkpoints"
    records = _records(args.target_per_family)
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
        "--seed", "20260701",
        "--checkpoints", str(checkpoints),
        "--device", args.device,
    ]
    train_code = train_tiny_lm_run(train_args)
    if train_code != 0:
        return train_code

    checkpoint_name = _latest_checkpoint_name(checkpoints)
    eval_args = argparse.Namespace(
        tokenizer=args.tokenizer,
        checkpoints=checkpoints,
        checkpoint_name=checkpoint_name,
        device=args.device,
    )
    shadow_rows = evaluate_phase27_67(eval_args)
    regression_rows = evaluate_phase27_60(eval_args)
    shadow_summary = summary_phase27_67(shadow_rows)
    regression_summary = summary_phase27_60(regression_rows)
    shadow_passed = shadow_summary["passed"] == shadow_summary["total"]
    regression_passed = regression_summary["passed"] == regression_summary["total"]
    passed = shadow_passed and regression_passed
    improved = shadow_summary["passed"] > 30 and regression_summary["passed"] >= 28
    status = (
        "PASSED_SHADOW_FAILURE_REPAIR_READY_FOR_NEW_FRESH_SHADOW_RUNTIME_BLOCKED"
        if passed
        else (
            "IMPROVED_SHADOW_FAILURE_REPAIR_RUNTIME_BLOCKED"
            if improved
            else "FAILED_SHADOW_FAILURE_REPAIR_RUNTIME_BLOCKED"
        )
    )
    report = {
        "phase": "Phase 27.68",
        "status": status,
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "training_started": True,
        "training_scope": "bounded SF-10M targeted repair for Phase 27.67 failures; no runtime switch; no SF-50M",
        "tokenizer": _rel(args.tokenizer),
        "checkpoint_root": _rel(checkpoints),
        "checkpoint_name": checkpoint_name,
        "candidate_generator": "sf_10m_phase27_68_shadow_failure_repair",
        "train_records": len(records),
        "repair_pair_count": len(_repair_pairs()),
        "shadow_failure_pair_count": len(SHADOW_FAILURE_REPAIR),
        "target_per_family": args.target_per_family,
        "shadow_summary": shadow_summary,
        "regression_summary": regression_summary,
        "shadow_rows": shadow_rows,
        "regression_rows": regression_rows,
        "decisions": {
            "runtime_switch_allowed": False,
            "ui_open_allowed": False,
            "sf50m_allowed": False,
            "phase28_allowed": False,
            "new_fresh_shadow_allowed": passed,
            "repair_required_before_runtime": not passed,
        },
        "decision": (
            "Targeted repair passed the known shadow and regression canaries. Runtime remains blocked; run a new fresh shadow canary next."
            if passed
            else "Targeted repair did not fully pass both canaries. Runtime remains blocked; inspect remaining failures before any UI/runtime change."
        ),
        "next_phase": (
            "Phase 27.69 — new fresh shadow canary with unseen prompts after repair"
            if passed
            else "Phase 27.69 — inspect Phase 27.68 failures and revise repair"
        ),
        "torch_version": torch.__version__,
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _write_samples(args.samples, shadow_rows, regression_rows)
    _write_doc(report, args.doc)

    print("SF.AI — Phase 27.68 shadow failure repair")
    print(f"  status      : {status}")
    print(f"  checkpoint  : {checkpoint_name}")
    print(f"  shadow      : {shadow_summary['passed']}/{shadow_summary['total']}")
    print(f"  regression  : {regression_summary['passed']}/{regression_summary['total']}")
    print(f"  family      : {shadow_summary['family_summary']}")
    print(f"  report      : {_rel(args.report)}")
    print(f"  samples     : {_rel(args.samples)}")
    print("  runtime     : blocked")
    return 0 if args.report.exists() else 1


if __name__ == "__main__":
    raise SystemExit(main())
