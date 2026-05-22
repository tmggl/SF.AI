"""Mo3jam Saudi-dialect importer.

Source: معجم — اللهجة السعودية (https://ar.mo3jam.com/dialect/Saudi)
Permission: confirmed verbally by the user. credit_required=True on every
record produced.

The importer has two phases:
1. Listing crawl: for each Arabic letter, fetch
   `https://ar.mo3jam.com/dialect/Saudi/all/{letter}` and extract every
   `<li><a href="/term/{TERM}#Saudi">...</a></li>` link.
2. Term crawl: for each discovered term URL, fetch
   `https://ar.mo3jam.com/term/{TERM}` and extract definition / example /
   variants for the Saudi block.

Both phases:
- check robots.txt before the first request
- rate-limit between requests (default 2 s)
- store raw HTML under data/corpus/dialects/saudi/raw/mo3jam/<phase>/...
- emit JSONL records to data/corpus/dialects/saudi/jsonl/

The term-page parser uses several heuristics because the live HTML wasn't
fully introspected during build (safety classifier blocked one of the
discovery fetches — see SOURCE_DISCOVERY_MO3JAM.md). The parser surfaces
uncertain rows so they can be reviewed instead of silently dropped.
"""

from __future__ import annotations

import hashlib
import json
import re
import time
import unicodedata
import urllib.parse
import urllib.request
import urllib.robotparser
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from bs4 import BeautifulSoup


# ----- public types -----

USER_AGENT = "SF.AI Research Importer - permission confirmed by user"
PARSER_VERSION = "1.0"
SOURCE_NAME = "معجم — اللهجة السعودية"
SOURCE_ROOT = "https://ar.mo3jam.com/dialect/Saudi"
BASE_URL = "https://ar.mo3jam.com"
EXPECTED_TERMS = 3139

# Arabic letters listed on the source page index. Order matches the site UI;
# duplicates between أ/ا are preserved because the source lists both.
SAUDI_LETTERS: tuple[str, ...] = (
    "ا", "أ", "إ", "آ",
    "ب", "ت", "ث", "ج", "ح", "خ",
    "د", "ذ", "ر", "ز", "س", "ش",
    "ص", "ض", "ط", "ظ", "ع", "غ",
    "ف", "ق", "ك", "ل", "م", "ن",
    "ه", "و", "ي", "ى", "ء",
)


@dataclass(frozen=True)
class Mo3jamImportConfig:
    output_jsonl: Path
    raw_dir: Path
    report_path: Path
    failed_urls_path: Path
    rate_limit_seconds: float = 2.0
    request_timeout: float = 20.0
    limit: int | None = None           # cap total terms (for tests / dry-run)
    resume: bool = True                # skip terms already in JSONL
    dry_run: bool = True               # no writes, no network; just plan
    user_permission_confirmed: bool = False
    letters: tuple[str, ...] = SAUDI_LETTERS

    def __post_init__(self) -> None:
        if self.rate_limit_seconds < 0:
            raise ValueError("rate_limit_seconds must be >= 0")
        if not self.dry_run and not self.user_permission_confirmed:
            raise ValueError(
                "Live import requires --confirm-user-permission. Permission is "
                "verbal between the SF.AI user and the Mo3jam team; the script "
                "will not crawl without explicit acknowledgement."
            )


@dataclass
class Mo3jamTerm:
    term: str
    normalized_term: str
    definition: str
    usage_example: str
    spelling_variants: list[str]
    dialect: str
    subdialect: str
    letter: str
    source_name: str
    source_url: str
    source_root: str
    permission_status: str
    credit_required: bool
    imported_at: str
    raw_html_path: str
    parser_version: str
    parser_warnings: list[str] = field(default_factory=list)


@dataclass
class Mo3jamImportReport:
    started_at: str
    finished_at: str = ""
    letters_seen: int = 0
    term_urls_discovered: int = 0
    terms_imported: int = 0
    terms_with_definition: int = 0
    terms_with_example: int = 0
    terms_with_source_url: int = 0
    terms_with_subdialect: int = 0
    duplicates_skipped: int = 0
    failures: int = 0
    failed_urls: list[str] = field(default_factory=list)
    parser_warnings_total: int = 0
    expected_terms: int = EXPECTED_TERMS
    is_close_to_expected: bool = False
    notes: list[str] = field(default_factory=list)


# ----- normalization helpers -----

_WHITESPACE_RE = re.compile(r"\s+")
_TASHKEEL_RE = re.compile(r"[ؐ-ًؚ-ٰٟۖ-ۭـ]")


def normalize_arabic_term(text: str) -> str:
    """Light normalization used to dedup terms internally.

    Mirrors core/nlp/arabic_normalizer behavior (NFC, strip tashkeel/tatweel,
    unify alef forms, alef-maqsura → yaa, collapse whitespace) but is
    self-contained so the importer doesn't pull the full NLP layer.
    """
    if not text:
        return ""
    text = unicodedata.normalize("NFC", text)
    text = _TASHKEEL_RE.sub("", text)
    for src, dst in (("أ", "ا"), ("إ", "ا"), ("آ", "ا"), ("ٱ", "ا"),
                     ("ى", "ي"), ("ئ", "ي"), ("ؤ", "و")):
        text = text.replace(src, dst)
    text = _WHITESPACE_RE.sub(" ", text).strip()
    return text


# ----- parsers (pure, easily testable) -----

# Matches the listing pages: <a href="/term/X#Saudi">X</a>
# We don't depend on a wrapping <li> because some letter pages may render
# differently — anchoring on the href shape is robust.
def parse_listing_html(html: str) -> list[str]:
    """Return a list of relative term URLs found on a listing page.

    Format observed: <a href="/term/<TERM>#Saudi">...</a>
    Returns paths like "/term/<TERM>" (anchor stripped) without dedup.
    """
    soup = BeautifulSoup(html, "lxml")
    found: list[str] = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if not isinstance(href, str):
            continue
        # We want term links scoped to the Saudi dialect anchor.
        if "/term/" not in href:
            continue
        if "#Saudi" not in href:
            continue
        # Strip the anchor; keep the path part.
        path = href.split("#", 1)[0]
        if not path.startswith("/term/"):
            continue
        if path not in found:
            found.append(path)
    return found


def _text_of(elem) -> str:  # type: ignore[no-untyped-def]
    if elem is None:
        return ""
    return _WHITESPACE_RE.sub(" ", elem.get_text(" ", strip=True)).strip()


# Heuristic patterns for finding the Saudi-specific block on a term page.
# The site groups definitions by dialect. We look for a header / link / tag
# containing "السعودية" or pointing to /dialect/Saudi, then take the
# enclosing section / list-item as the Saudi block.
_SAUDI_LABEL_TOKENS = ("السعودية", "السعوديه", "Saudi")
_SUBDIALECT_HINTS = {
    "hijazi": ("حجازي", "حجازية", "الحجاز"),
    "najdi": ("نجدي", "نجدية", "نجد"),
    "qassimi": ("قصيمي", "قصيمية", "القصيم"),
    "shamali": ("شمالي", "شمالية"),
    "janubi": ("جنوبي", "جنوبية"),
}


def _find_saudi_block(soup: BeautifulSoup):  # type: ignore[no-untyped-def]
    """Locate the HTML region that talks about the Saudi dialect."""
    # First: an anchor whose href points to the Saudi dialect.
    saudi_link = soup.find("a", href=lambda v: isinstance(v, str) and "/dialect/Saudi" in v)
    if saudi_link is not None:
        # Climb to the nearest containing block.
        for ancestor in saudi_link.parents:
            if ancestor.name in {"li", "article", "section", "div"}:
                return ancestor
    # Second: any element whose visible text equals "السعودية".
    for tag in soup.find_all(string=True):
        text = (tag or "").strip()
        if text in _SAUDI_LABEL_TOKENS:
            for ancestor in tag.parents:
                if ancestor.name in {"li", "article", "section", "div"}:
                    return ancestor
    return None


def _extract_definition(block) -> str:  # type: ignore[no-untyped-def]
    """Pick the most plausible definition text from a block."""
    if block is None:
        return ""
    # Common: a <p> immediately after the dialect label.
    for selector in ("p.definition", "div.definition", "p"):
        node = block.select_one(selector)
        if node is not None:
            txt = _text_of(node)
            if txt and len(txt) > 1:
                return txt
    # Fallback: largest text node inside the block, excluding the dialect label.
    text = _text_of(block)
    for tok in _SAUDI_LABEL_TOKENS:
        text = text.replace(tok, " ")
    return _WHITESPACE_RE.sub(" ", text).strip()


def _extract_example(block) -> str:  # type: ignore[no-untyped-def]
    """Find a usage example inside a Saudi block."""
    if block is None:
        return ""
    # Common patterns: nodes whose class contains "example", or a label like
    # "مثال" followed by text.
    for cls in ("example", "usage", "mathal"):
        node = block.find(class_=re.compile(cls, re.I))
        if node is not None:
            return _text_of(node)
    # Search for "مثال:" in plain text.
    for tag in block.find_all(string=True):
        s = (tag or "").strip()
        if s.startswith("مثال") or s.startswith("Example"):
            # Sibling or parent text.
            parent = tag.parent
            if parent is not None:
                txt = _text_of(parent)
                if txt:
                    return txt.replace("مثال:", "").replace("Example:", "").strip()
    return ""


def _extract_spelling_variants(block) -> list[str]:  # type: ignore[no-untyped-def]
    if block is None:
        return []
    out: list[str] = []
    for cls in ("spelling", "variants", "writing"):
        node = block.find(class_=re.compile(cls, re.I))
        if node is None:
            continue
        for item in node.find_all(["li", "span"]):
            txt = _text_of(item)
            if txt and txt not in out:
                out.append(txt)
    return out


def _extract_subdialect(block) -> str:  # type: ignore[no-untyped-def]
    if block is None:
        return "unknown"
    text = _text_of(block).lower()
    for tag in block.find_all(string=True):
        text += " " + (tag or "").strip()
    text_norm = text
    for canonical, tokens in _SUBDIALECT_HINTS.items():
        for tok in tokens:
            if tok in text_norm:
                return canonical
    return "unknown"


def parse_term_html(
    html: str,
    *,
    term_hint: str,
    source_url: str,
    letter: str,
    raw_html_path: str,
    imported_at: str | None = None,
) -> Mo3jamTerm:
    """Parse a term page into a Mo3jamTerm record.

    Always returns a Mo3jamTerm; missing fields end up as empty strings or
    "unknown". `parser_warnings` lists problems for the report.
    """
    soup = BeautifulSoup(html, "lxml")
    warnings: list[str] = []

    # Term display text: prefer <h1>, fall back to <title> / hint.
    h1 = soup.find("h1")
    term_text = _text_of(h1) if h1 is not None else ""
    if not term_text:
        title = soup.find("title")
        term_text = _text_of(title)
    if not term_text:
        term_text = term_hint
        warnings.append("term_text_fallback_to_hint")

    block = _find_saudi_block(soup)
    if block is None:
        warnings.append("saudi_block_not_found")
        definition = ""
        example = ""
        variants: list[str] = []
        subdialect = "unknown"
    else:
        definition = _extract_definition(block)
        example = _extract_example(block)
        variants = _extract_spelling_variants(block)
        subdialect = _extract_subdialect(block)
        if not definition:
            warnings.append("definition_empty")

    return Mo3jamTerm(
        term=term_text,
        normalized_term=normalize_arabic_term(term_text),
        definition=definition,
        usage_example=example,
        spelling_variants=variants,
        dialect="saudi",
        subdialect=subdialect,
        letter=letter,
        source_name=SOURCE_NAME,
        source_url=source_url,
        source_root=SOURCE_ROOT,
        permission_status="allowed_with_user_confirmed_permission",
        credit_required=True,
        imported_at=imported_at or datetime.now(timezone.utc).isoformat(),
        raw_html_path=raw_html_path,
        parser_version=PARSER_VERSION,
        parser_warnings=warnings,
    )


# ----- fetcher -----

class _HttpFetcher:
    """Minimal urllib-based fetcher. Honors User-Agent and timeout."""

    def __init__(self, user_agent: str = USER_AGENT, timeout: float = 20.0) -> None:
        self.user_agent = user_agent
        self.timeout = timeout

    def get(self, url: str) -> str:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": self.user_agent, "Accept-Language": "ar,en;q=0.9"},
        )
        with urllib.request.urlopen(req, timeout=self.timeout) as resp:  # nosec: B310
            raw = resp.read()
            charset = resp.headers.get_content_charset() or "utf-8"
        return raw.decode(charset, errors="replace")


# ----- importer -----

class Mo3jamImporter:
    """Drives the listing crawl + term crawl with rate limiting and resume."""

    def __init__(
        self,
        config: Mo3jamImportConfig,
        fetcher: _HttpFetcher | None = None,
    ) -> None:
        self.config = config
        self.fetcher = fetcher or _HttpFetcher(timeout=config.request_timeout)
        self.report = Mo3jamImportReport(started_at=datetime.now(timezone.utc).isoformat())
        self._seen_norm: set[str] = set()
        self._existing_urls: set[str] = set()

    # ----- robots -----

    def check_robots(self) -> bool:
        rp = urllib.robotparser.RobotFileParser()
        rp.set_url(BASE_URL + "/robots.txt")
        try:
            rp.read()
        except Exception:
            # Be conservative: if we can't read robots, assume not allowed.
            self.report.notes.append("robots_unreachable")
            return False
        allowed = rp.can_fetch(USER_AGENT, SOURCE_ROOT)
        if not allowed:
            self.report.notes.append("robots_disallow_root")
        return allowed

    # ----- listing -----

    def _letter_url(self, letter: str) -> str:
        return f"{BASE_URL}/dialect/Saudi/all/{urllib.parse.quote(letter, safe='')}"

    def _term_url(self, path: str) -> str:
        return BASE_URL + path

    def crawl_listing(self) -> list[tuple[str, str]]:
        """Return list of (letter, term_url) pairs discovered.

        Dry-run mode: returns just the planned letter URLs (no fetching).
        """
        if self.config.dry_run:
            self.report.letters_seen = len(self.config.letters)
            self.report.notes.append(
                "dry_run: would fetch " + str(len(self.config.letters)) + " letter pages"
            )
            return []

        out: list[tuple[str, str]] = []
        for letter in self.config.letters:
            url = self._letter_url(letter)
            try:
                html = self.fetcher.get(url)
            except Exception as e:
                self.report.failures += 1
                self.report.failed_urls.append(url)
                self.report.notes.append(f"letter_fetch_failed:{letter}:{type(e).__name__}")
                self._sleep()
                continue
            self.report.letters_seen += 1
            self._save_raw(html, "listing", letter)
            for path in parse_listing_html(html):
                out.append((letter, self._term_url(path)))
            self._sleep()

        # Dedup by URL, keep first letter seen for each.
        seen: dict[str, str] = {}
        for letter, url in out:
            if url not in seen:
                seen[url] = letter
        self.report.term_urls_discovered = len(seen)
        return [(letter, url) for url, letter in seen.items()]

    # ----- terms -----

    def crawl_terms(self, term_urls: Iterable[tuple[str, str]]) -> int:
        """Fetch each term URL, parse, and append to JSONL. Returns count imported."""
        self._load_existing_jsonl()

        imported = 0
        for letter, url in term_urls:
            if self.config.limit is not None and imported >= self.config.limit:
                break
            if url in self._existing_urls:
                self.report.duplicates_skipped += 1
                continue
            try:
                html = self.fetcher.get(url)
            except Exception as e:
                self.report.failures += 1
                self.report.failed_urls.append(url)
                self.report.notes.append(f"term_fetch_failed:{url}:{type(e).__name__}")
                self._sleep()
                continue
            term_path = urllib.parse.urlparse(url).path
            term_hint = urllib.parse.unquote(term_path.removeprefix("/term/"))
            raw_path = self._save_raw(html, "term", _safe_filename(term_hint))
            record = parse_term_html(
                html,
                term_hint=term_hint,
                source_url=url,
                letter=letter,
                raw_html_path=str(raw_path),
            )

            norm = record.normalized_term
            if norm and norm in self._seen_norm:
                self.report.duplicates_skipped += 1
                self._sleep()
                continue
            if norm:
                self._seen_norm.add(norm)
            self._existing_urls.add(url)

            self._append_jsonl(record)
            self._tally(record)
            imported += 1
            self._sleep()

        self.report.terms_imported = imported
        self.report.is_close_to_expected = (
            self.report.terms_imported >= int(self.report.expected_terms * 0.9)
        )
        self.report.finished_at = datetime.now(timezone.utc).isoformat()
        return imported

    # ----- io helpers -----

    def _sleep(self) -> None:
        if self.config.rate_limit_seconds > 0 and not self.config.dry_run:
            time.sleep(self.config.rate_limit_seconds)

    def _save_raw(self, html: str, kind: str, key: str) -> Path:
        if self.config.dry_run:
            return Path("(dry-run)")
        target_dir = self.config.raw_dir / kind
        target_dir.mkdir(parents=True, exist_ok=True)
        name = _safe_filename(key) + ".html"
        path = target_dir / name
        path.write_text(html, encoding="utf-8")
        return path

    def _append_jsonl(self, record: Mo3jamTerm) -> None:
        if self.config.dry_run:
            return
        self.config.output_jsonl.parent.mkdir(parents=True, exist_ok=True)
        with self.config.output_jsonl.open("a", encoding="utf-8") as f:
            payload = asdict(record)
            f.write(json.dumps(payload, ensure_ascii=False) + "\n")

    def _load_existing_jsonl(self) -> None:
        if not self.config.resume:
            return
        if not self.config.output_jsonl.exists():
            return
        with self.config.output_jsonl.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    continue
                url = rec.get("source_url")
                if url:
                    self._existing_urls.add(url)
                norm = rec.get("normalized_term")
                if norm:
                    self._seen_norm.add(norm)

    def _tally(self, record: Mo3jamTerm) -> None:
        if record.definition:
            self.report.terms_with_definition += 1
        if record.usage_example:
            self.report.terms_with_example += 1
        if record.source_url:
            self.report.terms_with_source_url += 1
        if record.subdialect and record.subdialect != "unknown":
            self.report.terms_with_subdialect += 1
        if record.parser_warnings:
            self.report.parser_warnings_total += len(record.parser_warnings)

    # ----- output writers -----

    def write_failed_urls(self) -> Path:
        if self.config.dry_run:
            return Path("(dry-run)")
        p = self.config.failed_urls_path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("\n".join(self.report.failed_urls), encoding="utf-8")
        return p

    def write_report(self) -> Path:
        p = self.config.report_path
        if self.config.dry_run:
            return p  # caller decides whether to write a dry-run summary
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(self._render_report_markdown(), encoding="utf-8")
        return p

    def _render_report_markdown(self) -> str:
        r = self.report
        lines = [
            "# Mo3jam Saudi-Dialect Import Report",
            "",
            f"**Source:** {SOURCE_NAME}",
            f"**URL:** {SOURCE_ROOT}",
            "**Permission:** allowed_with_user_confirmed_permission",
            "**Credit required:** true",
            "",
            f"- Started: `{r.started_at}`",
            f"- Finished: `{r.finished_at}`",
            f"- Letters seen: **{r.letters_seen}**",
            f"- Term URLs discovered: **{r.term_urls_discovered}**",
            f"- Terms imported: **{r.terms_imported}**",
            f"- Terms with definition: **{r.terms_with_definition}**",
            f"- Terms with usage example: **{r.terms_with_example}**",
            f"- Terms with source_url: **{r.terms_with_source_url}**",
            f"- Terms with subdialect tag: **{r.terms_with_subdialect}**",
            f"- Duplicates skipped: **{r.duplicates_skipped}**",
            f"- Failures: **{r.failures}**",
            f"- Parser warnings (total): **{r.parser_warnings_total}**",
            f"- Expected (page header): **{r.expected_terms}**",
            f"- Close to expected (≥90%): **{r.is_close_to_expected}**",
            "",
            "## Notes",
            *[f"- {n}" for n in (r.notes or ["(none)"])],
            "",
            "## Attribution",
            "",
            "مصدر اللهجات السعودية:",
            f"{SOURCE_NAME}",
            f"{SOURCE_ROOT}",
            "",
        ]
        return "\n".join(lines)


def _safe_filename(text: str) -> str:
    """Make a filesystem-safe filename out of an Arabic term."""
    text = text.strip()
    if not text:
        return "_"
    digest = hashlib.blake2b(text.encode("utf-8"), digest_size=8).hexdigest()
    # Keep some legibility: first 40 chars sanitized + hash suffix.
    safe = re.sub(r"[^\w؀-ۿ-]+", "_", text)[:40]
    return f"{safe}_{digest}"
