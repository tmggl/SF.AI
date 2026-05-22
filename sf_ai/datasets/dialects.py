"""Dialect-lexicon helpers — Phase 3.5.

Builds the SF-friendly YAML lexicon from a JSONL produced by an importer
(e.g. Mo3jam Saudi). Source attribution is preserved on every entry.

Output schema:

    metadata:
      source_name: ...
      source_url: ...
      permission_status: allowed_with_user_confirmed_permission
      credit_required: true
      expected_terms: 3139

    terms:
      - term: "..."
        normalized_term: "..."
        definition: "..."
        usage_example: "..."
        dialect: "saudi"
        subdialect: "unknown"
        source_url: "..."
        use_for: [...]
        training_allowed: false
        confidence: 1.0
        requires_credit: true
"""

from __future__ import annotations

import json
from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


DEFAULT_USE_FOR: tuple[str, ...] = (
    "dialect_understanding",
    "lexical_matching",
    "response_context",
    "slang_explanation",
    "user_text_normalization",
)


USE_RULES: tuple[str, ...] = (
    "لا تستخدم التعريف كحقيقة عامة خارج سياق اللهجة.",
    "استخدم المصطلح لفهم كلام المستخدم السعودي.",
    "إذا سأل المستخدم عن معنى كلمة، يمكن استخدام التعريف مع ذكر المصدر.",
    "لا تستخدم المصطلحات لتوليد محتوى منسوب للمصدر بدون ذكر المصدر.",
    "لا تدخل هذه البيانات في التدريب إلا لاحقًا بعد قرار صريح.",
)


@dataclass(frozen=True)
class DialectLexiconMeta:
    source_name: str
    source_url: str
    permission_status: str
    credit_required: bool
    expected_terms: int


def iter_jsonl_records(path: str | Path) -> Iterator[dict[str, Any]]:
    p = Path(path)
    with p.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue


def build_dialect_yaml(
    jsonl_path: str | Path,
    output_yaml: str | Path,
    *,
    meta: DialectLexiconMeta,
    use_for: Iterable[str] = DEFAULT_USE_FOR,
    training_allowed: bool = False,
    confidence: float = 1.0,
) -> int:
    """Convert a Mo3jam-style JSONL into a SF-AI lexicon YAML.

    Returns the number of terms written. The output YAML always carries the
    full attribution metadata at the top, even if the JSONL records contain
    their own (they do — but a corpus-level overview helps quick scans).
    """
    terms: list[dict[str, Any]] = []
    for rec in iter_jsonl_records(jsonl_path):
        if not rec.get("term"):
            continue
        entry: dict[str, Any] = {
            "term": rec["term"],
            "normalized_term": rec.get("normalized_term", ""),
            "definition": rec.get("definition", ""),
            "usage_example": rec.get("usage_example", ""),
            "spelling_variants": list(rec.get("spelling_variants") or []),
            "dialect": rec.get("dialect", "saudi"),
            "subdialect": rec.get("subdialect", "unknown"),
            "letter": rec.get("letter", ""),
            "source_url": rec.get("source_url", ""),
            "use_for": list(use_for),
            "use_rules": list(USE_RULES),
            "training_allowed": training_allowed,
            "confidence": confidence,
            "requires_credit": True,
        }
        terms.append(entry)

    payload: dict[str, Any] = {
        "metadata": {
            "source_name": meta.source_name,
            "source_url": meta.source_url,
            "permission_status": meta.permission_status,
            "credit_required": meta.credit_required,
            "expected_terms": meta.expected_terms,
            "attribution": (
                "مصدر اللهجات السعودية:\n"
                f"{meta.source_name}\n"
                f"{meta.source_url}"
            ),
        },
        "terms": terms,
    }

    out = Path(output_yaml)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as f:
        yaml.safe_dump(payload, f, allow_unicode=True, sort_keys=False)
    return len(terms)


def load_dialect_yaml(path: str | Path) -> tuple[DialectLexiconMeta, list[dict[str, Any]]]:
    """Load a dialect YAML built by `build_dialect_yaml`.

    Refuses to return contents if `credit_required` is missing/false — the
    file must always carry attribution.
    """
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    meta_raw = data.get("metadata") or {}
    if not meta_raw.get("credit_required", False):
        raise ValueError(
            f"refusing to load dialect lexicon {path}: credit_required missing/false"
        )
    meta = DialectLexiconMeta(
        source_name=str(meta_raw.get("source_name", "")),
        source_url=str(meta_raw.get("source_url", "")),
        permission_status=str(meta_raw.get("permission_status", "unknown")),
        credit_required=bool(meta_raw.get("credit_required", False)),
        expected_terms=int(meta_raw.get("expected_terms", 0)),
    )
    terms = list(data.get("terms") or [])
    return meta, terms
