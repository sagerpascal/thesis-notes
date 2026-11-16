#!/usr/bin/env python3
"""Merge the bibliographies of the imported papers into one thesis bibliography.

Six published papers bring six bibliographies with heavy overlap, inconsistent
keys, inconsistent formatting, and the same work appearing as a preprint in one
file and as a published paper in another. This script folds them into a single
`references/merged.bib` that `main.tex` can load on its own.

The one rule that shapes everything: imported .tex files are never edited, so
the old citation keys have to keep working. Every merged entry therefore carries
biblatex's `ids` field listing every old key that resolved to it, and biber
treats those as aliases.

Run from the repository root:

    uv run --no-project python scripts/merge_bib.py            # merge and write
    uv run --no-project python scripts/merge_bib.py --check    # report only
    uv run --no-project python scripts/merge_bib.py --apply-keys

Hand corrections go in `references/overrides.toml`, never into an imported bib
file. The merge report lists every decision the script could not make on its own
and prints a ready to paste override block for each.
"""

from __future__ import annotations

import argparse
import csv
import difflib
import re
import sys
import tomllib
import unicodedata
from collections import defaultdict
from dataclasses import dataclass, field as dc_field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


# ============================================================================
# CONFIGURATION
# ============================================================================


def cited_keys() -> set[str]:
    """The citation keys the last build asked for, from main.bcf.

    A merged entry missing a year is only a problem if something cites it.
    Most of the bibliographies read here belong to papers the thesis
    summarises rather than reproduces, so they carry hundreds of references
    no included text can reach. Reporting those as errors to fix buries the
    ones that matter.

    Returns an empty set when there is no build to consult, and the caller
    then treats every entry as cited, which is the safe direction.
    """
    import re as _re
    bcf = Path(__file__).resolve().parent.parent / "main.bcf"
    if not bcf.exists():
        return set()
    text = bcf.read_text(errors="replace")
    return set(_re.findall(r"<bcf:citekey[^>]*>([^<]+)</bcf:citekey>", text))

# Every bibliography that feeds the thesis, in a fixed order. The order is a
# tie breaker during merging, so put the most trustworthy source first.
# Paths are relative to the repository root.
INPUT_FILES = [
    "references/manual.bib",
    # Thesis owned, for the background chapter. It cites a literature no
    # imported paper carries, see CLAUDE.md section 5.2.
    "references/background.bib",
    "imported_papers/ACU_JAIR/cleaned_references.bib",
    "imported_papers/CLEF_Checkthat_4b/sources_cleaned.bib",
    "imported_papers/Llama2_benchmark_sds/references.bib",
    "imported_papers/sds_hounsfield_features/references_clean.bib",
    # The self attention project ships three variants. ICML2025 is the import
    # source for the chapter, so its bib is the one that counts. The rebuttal
    # bib is a superset used only for the response letter and is not built.
    "imported_papers/self_attention_geometry_project_ICML/ICML2025/bib.bib",
    "imported_papers/grokking/iclr2027_conference.bib",
    "imported_papers/probe-norm/main.bib",
    # COGITAO also ships the ICLR template's sample bibliography, which the
    # paper does not cite. Only the one it cites is read.
    "imported_papers/COGITAO_ICML_2026/references.bib",
    # The CNA paper carries its bibliography inline as \bibitem entries.
    # scripts/split_paper.py converts them so its citations resolve.
    "generated/imported/cna/_thebibliography.bib",
]

OVERRIDES_FILE = "references/overrides.toml"

OUTPUT_BIB = "references/merged.bib"
OUTPUT_KEYMAP = "references/keymap.csv"
OUTPUT_REPORT = "references/merge_report.md"

# Files whose citation keys `--apply-keys` may rewrite. Never list anything
# under imported_papers/.
THESIS_TEX = ["main.tex", "preface.tex", "sections/*.tex"]

# Fuzzy title similarity above which two entries are reported as possibly the
# same work. Fuzzy matches are never merged automatically.
FUZZY_TITLE_THRESHOLD = 0.93

# Fields thrown away on the way in. Reference manager cruft and anything that
# only bloats the file.
DROP_FIELDS = {
    "abstract", "annote", "file", "keywords", "urldate", "shorttitle",
    "timestamp", "biburl", "bibsource", "owner", "groups", "copyright",
    "pmid", "pmcid", "readstatus", "rating", "priority", "citeulike-article-id",
}

# Drop `url` when the entry already has a DOI, so the printed reference carries
# one pointer rather than two.
DROP_URL_WHEN_DOI = True

# How to resolve a field two sources disagree on. Every real disagreement is
# reported whatever the policy says.
#   canonical  take the value from the canonical record
#   longest    take the longest value, which beats truncations and abbreviations
#   range      prefer a page range over a single page, then canonical
#   first      first non-empty value in record order
CONFLICT_POLICY = {
    "author": "longest",     # beats "and others" truncation
    "editor": "longest",
    "journal": "longest",    # beats "Proc. of NIPS'16"
    "booktitle": "longest",
    "publisher": "longest",
    "pages": "range",
    "title": "canonical",
    "year": "canonical",
    "doi": "first",
    "eprint": "first",
    "url": "first",
    "isbn": "first",
    "issn": "first",
}
DEFAULT_CONFLICT_POLICY = "canonical"

# Entry types ranked by how much we trust them to be the published form. Lower
# is better. Used to pick the canonical record of a merged group.
TYPE_RANK = {
    "article": 0, "inproceedings": 0, "incollection": 1, "inbook": 1,
    "book": 1, "proceedings": 2, "phdthesis": 2, "mastersthesis": 2,
    "techreport": 3, "manual": 3, "online": 4, "electronic": 4,
    "unpublished": 5, "misc": 6,
}
DEFAULT_TYPE_RANK = 7

# Field order in the output file.
FIELD_ORDER = [
    "ids", "author", "editor", "title", "booktitle", "journal", "series",
    "volume", "number", "pages", "publisher", "address", "institution",
    "school", "organization", "howpublished", "edition", "month", "year",
    "doi", "eprint", "eprinttype", "eprintclass", "url", "isbn", "issn",
    "language", "note",
]

# Words never used as the title word of a generated key. Articles, prepositions
# and conjunctions, plus the generic adjectives that open a third of all machine
# learning titles and say nothing about which paper this is.
TITLE_SKIP_WORDS = {
    "a", "an", "the", "on", "of", "in", "for", "to", "and", "or", "with",
    "from", "by", "at", "as", "is", "are", "we", "our", "its", "it", "this",
    "that", "these", "those", "into", "via", "using", "toward", "towards",
    "revisiting", "rethinking", "beyond", "when", "what", "why", "how",
    "comprehensive", "novel", "new", "simple", "general", "unified",
    "scalable", "efficient", "effective", "improved", "better", "fast",
    "practical", "empirical", "systematic", "large", "small",
}

# Name particles that belong to the surname.
NAME_PARTICLES = {
    "von", "van", "de", "der", "den", "del", "della", "di", "du", "da",
    "dos", "das", "la", "le", "ten", "ter", "af", "av", "zu", "bin", "ibn",
}

MONTHS = {
    "jan": "jan", "january": "jan", "1": "jan", "01": "jan",
    "feb": "feb", "february": "feb", "2": "feb", "02": "feb",
    "mar": "mar", "march": "mar", "3": "mar", "03": "mar",
    "apr": "apr", "april": "apr", "4": "apr", "04": "apr",
    "may": "may", "5": "may", "05": "may",
    "jun": "jun", "june": "jun", "6": "jun", "06": "jun",
    "jul": "jul", "july": "jul", "7": "jul", "07": "jul",
    "aug": "aug", "august": "aug", "8": "aug", "08": "aug",
    "sep": "sep", "september": "sep", "sept": "sep", "9": "sep", "09": "sep",
    "oct": "oct", "october": "oct", "10": "oct",
    "nov": "nov", "november": "nov", "11": "nov",
    "dec": "dec", "december": "dec", "12": "dec",
}

# Citation commands `--apply-keys` rewrites. Order matters: longer names first
# so the regex alternation does not match a prefix.
CITE_COMMANDS = [
    "citepeg", "citeauthor", "citeyearpar", "citeyear", "citealp", "citealt",
    "citenum", "citetitle", "fullcite", "footcite", "autocite", "parencite",
    "textcite", "smartcite", "supercite", "nocite", "citep", "citet", "cite",
]


# ============================================================================
# BIBTEX PARSER
# ============================================================================

@dataclass
class Record:
    """One entry as it appeared in one source file."""
    key: str
    etype: str
    fields: dict[str, str]
    source: str
    source_index: int
    order: int

    @property
    def type_rank(self) -> int:
        return TYPE_RANK.get(self.etype, DEFAULT_TYPE_RANK)


def split_top_level(text: str, sep: str) -> list[str]:
    """Split on `sep`, ignoring separators inside braces or quotes."""
    parts: list[str] = []
    buf: list[str] = []
    depth = 0
    in_quote = False
    i = 0
    while i < len(text):
        c = text[i]
        if c == "\\" and i + 1 < len(text):
            buf.append(c)
            buf.append(text[i + 1])
            i += 2
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
        elif c == '"' and depth == 0:
            in_quote = not in_quote
        if c == sep and depth == 0 and not in_quote:
            parts.append("".join(buf))
            buf = []
        else:
            buf.append(c)
        i += 1
    parts.append("".join(buf))
    return parts


def find_entry_end(text: str, start: int, open_char: str) -> int:
    """Index of the delimiter that closes the entry opened at `start`."""
    close = "}" if open_char == "{" else ")"
    depth = 1 if open_char == "{" else 0
    i = start
    while i < len(text):
        c = text[i]
        if c == "\\":
            i += 2
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if open_char == "{" and depth == 0:
                return i
        elif c == close and open_char == "(" and depth == 0:
            return i
        i += 1
    return -1


def unwrap_value(raw: str, strings: dict[str, str]) -> str:
    """Resolve a field value: braces, quotes, bare numbers, macros, `#` joins."""
    out: list[str] = []
    for part in split_top_level(raw, "#"):
        p = part.strip()
        if not p:
            continue
        if p.startswith("{") and p.endswith("}") and len(p) >= 2:
            out.append(p[1:-1])
        elif p.startswith('"') and p.endswith('"') and len(p) >= 2:
            out.append(p[1:-1])
        elif p.lower() in strings:
            out.append(strings[p.lower()])
        else:
            out.append(p)
    return "".join(out).strip()


ENTRY_HEAD = re.compile(r"\s*([A-Za-z]+)\s*([{(])")


def parse_bib(text: str, source: str, source_index: int,
              problems: list[str]) -> list[Record]:
    """Parse one .bib file into records. Tolerant, but complains in `problems`."""
    records: list[Record] = []
    strings: dict[str, str] = {}
    order = 0
    i = 0
    while True:
        at = text.find("@", i)
        if at < 0:
            break
        head = ENTRY_HEAD.match(text, at + 1)
        if not head:
            i = at + 1
            continue
        etype = head.group(1).lower()
        open_char = head.group(2)
        body_start = head.end()
        body_end = find_entry_end(text, body_start, open_char)
        if body_end < 0:
            problems.append(f"{source}: unterminated `@{etype}` near offset {at}")
            break
        body = text[body_start:body_end]
        i = body_end + 1

        if etype in {"comment", "preamble"}:
            continue

        if etype == "string":
            for assignment in split_top_level(body, ","):
                if "=" not in assignment:
                    continue
                name, _, raw = assignment.partition("=")
                strings[name.strip().lower()] = unwrap_value(raw, strings)
            continue

        chunks = split_top_level(body, ",")
        key = chunks[0].strip()
        if not key:
            problems.append(f"{source}: `@{etype}` with no citation key near offset {at}")
            continue

        fields: dict[str, str] = {}
        for chunk in chunks[1:]:
            if "=" not in chunk:
                if chunk.strip():
                    problems.append(f"{source}:{key}: ignored fragment `{chunk.strip()[:40]}`")
                continue
            name, _, raw = chunk.partition("=")
            name = name.strip().lower()
            if not name:
                continue
            value = unwrap_value(raw, strings)
            if name in fields and fields[name] != value:
                problems.append(f"{source}:{key}: field `{name}` given twice")
            fields[name] = value

        records.append(Record(key=key, etype=etype, fields=fields,
                              source=source, source_index=source_index,
                              order=order))
        order += 1
    return records


# ============================================================================
# NORMALISATION
# ============================================================================

ACCENT_CMD = re.compile(r"""\\(['`"^~=.]|[cvuHkrbdt])\s*\{?([A-Za-z])\}?""")
LATEX_CMD = re.compile(r"\\[A-Za-z]+\s*")
SMART_PUNCT = {
    "\u2013": "--", "\u2014": "---", "\u2012": "--", "\u2212": "-",
    "\u2018": "`", "\u2019": "'", "\u201c": "``", "\u201d": "''",
    "\u2026": "...", "\u00a0": " ", "\u200b": "", "\ufeff": "",
}


def tidy_value(value: str) -> str:
    """Collapse whitespace and turn typographic punctuation into LaTeX."""
    for bad, good in SMART_PUNCT.items():
        value = value.replace(bad, good)
    value = re.sub(r"\s+", " ", value)
    return value.strip().strip(",").strip()


def ascii_fold(text: str) -> str:
    """Strip LaTeX accents and diacritics down to plain ASCII letters."""
    text = ACCENT_CMD.sub(r"\2", text)
    text = text.replace("\\ss", "ss").replace("\\o", "o").replace("\\l", "l")
    text = text.replace("\\aa", "aa").replace("\\ae", "ae").replace("\\oe", "oe")
    text = LATEX_CMD.sub("", text)
    text = text.replace("{", "").replace("}", "")
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    for bad, good in {"ø": "o", "Ø": "O", "ł": "l", "Ł": "L", "đ": "d",
                      "ß": "ss", "æ": "ae", "œ": "oe", "Æ": "AE",
                      "Œ": "OE", "ı": "i"}.items():
        text = text.replace(bad, good)
    return text


def norm_title(title: str) -> str:
    """Comparison form of a title: folded, lowercase, alphanumeric only."""
    t = ascii_fold(title).lower()
    t = re.sub(r"[^a-z0-9]+", " ", t)
    return " ".join(t.split())


DOUBLE_AND = re.compile(r"\s+and(?:\s+and)+\s+", re.I)
DOI_PREFIX = re.compile(r"^\s*(?:https?://(?:dx\.)?doi\.org/|doi:\s*)", re.I)


def norm_doi(value: str) -> str:
    v = DOI_PREFIX.sub("", value or "").strip()
    v = v.replace("\\_", "_").replace("{", "").replace("}", "")
    v = v.rstrip(" .,;")
    if not v.lower().startswith("10."):
        return ""
    return v.lower()


ARXIV_PATTERNS = [
    re.compile(r"arxiv[.:/ ]*((?:\d{4}\.\d{4,5})|(?:[a-z-]+(?:\.[A-Z]{2})?/\d{7}))", re.I),
    re.compile(r"arxiv\.org/(?:abs|pdf)/((?:\d{4}\.\d{4,5})|(?:[a-z-]+/\d{7}))", re.I),
]
ARXIV_CLASS = re.compile(r"\[([a-z-]+\.[A-Z]{2})\]")


def find_arxiv(fields: dict[str, str]) -> tuple[str, str]:
    """Return (arxiv id without version, subject class) from anywhere it hides."""
    haystacks = [
        fields.get("eprint", ""), fields.get("doi", ""), fields.get("note", ""),
        fields.get("journal", ""), fields.get("url", ""),
        fields.get("howpublished", ""), fields.get("archiveprefix", ""),
    ]
    ident = ""
    for hay in haystacks:
        if not hay:
            continue
        # A bare eprint field is often just the identifier.
        bare = hay.strip()
        if re.fullmatch(r"\d{4}\.\d{4,5}(v\d+)?", bare):
            ident = bare
            break
        for pattern in ARXIV_PATTERNS:
            m = pattern.search(hay)
            if m:
                ident = m.group(1)
                break
        if ident:
            break
    ident = re.sub(r"v\d+$", "", ident)
    klass = ""
    for hay in haystacks:
        m = ARXIV_CLASS.search(hay or "")
        if m:
            klass = m.group(1)
            break
    if not klass:
        klass = fields.get("primaryclass", "") or fields.get("eprintclass", "")
    return ident, klass.strip()


def norm_pages(value: str) -> str:
    v = value.replace("--", "-").replace("\u2013", "-").replace("\u2014", "-")
    v = re.sub(r"\s*-\s*", "-", v.strip())
    if re.fullmatch(r"[A-Za-z]?\d+[A-Za-z]?-[A-Za-z]?\d+[A-Za-z]?", v):
        return v.replace("-", "--")
    return value.strip()


def split_authors(value: str) -> list[str]:
    if not value:
        return []
    parts = re.split(r"\s+and\s+", value, flags=re.I)
    return [p.strip() for p in parts if p.strip()]


def surname_of(author: str) -> str:
    """Surname of one author name, folded to lowercase letters."""
    name = author.strip()
    if not name or name.lower() in {"others", "et al.", "et al"}:
        return ""
    if name.startswith("{") and name.endswith("}"):
        return re.sub(r"[^a-z]", "", ascii_fold(name).lower())
    if "," in name:
        surname = name.split(",", 1)[0]
    else:
        tokens = ascii_fold(name).split()
        if not tokens:
            return ""
        start = len(tokens) - 1
        for idx, tok in enumerate(tokens[:-1]):
            if tok.lower().strip(".") in NAME_PARTICLES:
                start = idx
                break
        surname = " ".join(tokens[start:])
    return re.sub(r"[^a-z]", "", ascii_fold(surname).lower())


def first_surname(fields: dict[str, str]) -> str:
    authors = split_authors(fields.get("author", "")) or split_authors(fields.get("editor", ""))
    for a in authors:
        s = surname_of(a)
        if s:
            return s
    return ""


def year_of(fields: dict[str, str]) -> str:
    for name in ("year", "date"):
        m = re.search(r"(1[89]\d{2}|20\d{2})", fields.get(name, ""))
        if m:
            return m.group(1)
    return ""


KEY_YEAR = re.compile(r"((?:19|20)\d{2})$")


def normalise_record(rec: Record, replacements: dict[str, dict[str, str]],
                     report_lines: dict[str, list[str]]) -> None:
    """Bring one record to the shape everything downstream assumes."""
    fields = {k: tidy_value(v) for k, v in rec.fields.items() if v.strip()}

    for name in list(fields):
        if name in DROP_FIELDS or name.startswith("mendeley"):
            del fields[name]

    if rec.etype in {"inproceedings", "incollection", "inbook"} and "journal" in fields:
        # Some sources put the proceedings title in `journal`.
        fields.setdefault("booktitle", fields.pop("journal"))

    arxiv_id, arxiv_class = find_arxiv(fields)
    if arxiv_id:
        fields["eprint"] = arxiv_id
        fields["eprinttype"] = "arxiv"
        if arxiv_class:
            fields["eprintclass"] = arxiv_class
        for name in ("archiveprefix", "primaryclass"):
            fields.pop(name, None)
        # `note = {arXiv:2303.18223}` and `publisher = {arXiv}` are now redundant.
        if re.fullmatch(r"arxiv\s*:?\s*\S+", fields.get("note", ""), re.I):
            del fields["note"]
        if fields.get("publisher", "").strip().lower() == "arxiv":
            del fields["publisher"]
        if re.fullmatch(r"(arxiv|arxiv preprint.*)", fields.get("journal", ""), re.I):
            del fields["journal"]

    doi = norm_doi(fields.get("doi", ""))
    if doi:
        fields["doi"] = doi
    else:
        fields.pop("doi", None)

    # A doubled `and` leaves an empty name in the list. Biber then builds no
    # entry for the record, and if anything cites it through an alias biber
    # dereferences the missing entry and aborts with "Can't call method
    # get_field on an undefined value", writing no bibliography at all.
    for name in ("author", "editor"):
        if name in fields:
            fixed = DOUBLE_AND.sub(" and ", fields[name])
            parts = [p for p in split_authors(fixed) if p.lower() != "and"]
            if parts:
                fields[name] = " and ".join(parts)

    if "pages" in fields:
        fields["pages"] = norm_pages(fields["pages"])

    if "month" in fields:
        key = fields["month"].strip().lower().strip(".")
        fields["month"] = MONTHS.get(key, fields["month"])

    y = year_of(fields)
    if not y:
        # Reference managers end their keys with the year, so recover it from
        # there rather than shipping an entry with no date at all.
        m = KEY_YEAR.search(rec.key)
        if m:
            y = m.group(1)
            report_lines["recovered_year"].append(
                f"`{rec.key}` ({rec.source}) has no year field, took {y} from "
                f"its citation key")
    if y:
        fields["year"] = y
        if "date" in fields and re.fullmatch(r"\d{4}", fields["date"]):
            del fields["date"]

    for fname, table in replacements.items():
        if fname in fields:
            probe = norm_title(fields[fname])
            if probe in table:
                fields[fname] = table[probe]

    if DROP_URL_WHEN_DOI and fields.get("doi") and "url" in fields:
        del fields["url"]

    rec.fields = fields


# ============================================================================
# OVERRIDES
# ============================================================================

@dataclass
class Overrides:
    entry: dict[str, dict] = dc_field(default_factory=dict)
    merges: list[dict] = dc_field(default_factory=list)
    splits: list[dict] = dc_field(default_factory=list)
    replace: dict[str, dict[str, str]] = dc_field(default_factory=dict)
    used: set[str] = dc_field(default_factory=set)


def load_overrides(path: Path, problems: list[str]) -> Overrides:
    if not path.exists():
        return Overrides()
    with path.open("rb") as fh:
        raw = tomllib.load(fh)

    ov = Overrides()
    for key, patch in (raw.get("entry") or {}).items():
        if not isinstance(patch, dict):
            problems.append(f"{path.name}: [entry.{key}] must be a table")
            continue
        ov.entry[key] = patch
    for block in raw.get("merge") or []:
        # One key is enough when that key is the whole problem. A citation key
        # used by two source bibliographies for the same work resolves to two
        # records, and naming it once says to fold them. Two keys are still
        # the usual form, for the case where the same work arrived under
        # different names.
        if not block.get("keys"):
            problems.append(f"{path.name}: a [[merge]] block needs a key")
            continue
        ov.merges.append(block)
    for block in raw.get("split") or []:
        if len(block.get("keys", [])) < 2:
            problems.append(f"{path.name}: a [[split]] block needs at least two keys")
            continue
        ov.splits.append(block)
    for fname, table in (raw.get("replace") or {}).items():
        ov.replace[fname.lower()] = {norm_title(k): v for k, v in table.items()}
    return ov


# ============================================================================
# GROUPING
# ============================================================================

class DisjointSet:
    def __init__(self) -> None:
        self.parent: dict[int, int] = {}

    def find(self, x: int) -> int:
        self.parent.setdefault(x, x)
        root = x
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[x] != root:
            self.parent[x], x = root, self.parent[x]
        return root

    def union(self, a: int, b: int) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.parent[rb] = ra


@dataclass
class Group:
    records: list[Record]
    fields: dict[str, str] = dc_field(default_factory=dict)
    etype: str = "misc"
    new_key: str = ""
    aliases: list[str] = dc_field(default_factory=list)
    conflicts: list[tuple[str, list[tuple[str, str]]]] = dc_field(default_factory=list)
    notes: list[str] = dc_field(default_factory=list)
    confirmed: bool = False  # an override says these records are one work


def build_groups(records: list[Record], ov: Overrides,
                 report_lines: dict[str, list[str]]) -> list[Group]:
    """Union records that describe the same work."""
    by_index = {i: rec for i, rec in enumerate(records)}
    key_to_indices: dict[str, list[int]] = defaultdict(list)
    for i, rec in by_index.items():
        key_to_indices[rec.key].append(i)

    forbidden: set[frozenset[int]] = set()
    for block in ov.splits:
        keys = block["keys"]
        idxs = [i for k in keys for i in key_to_indices.get(k, [])]
        missing = [k for k in keys if k not in key_to_indices]
        if missing:
            report_lines["stale"].append(
                f"[[split]] names unknown key(s) {', '.join(missing)}")
        else:
            ov.used.add(f"split:{'+'.join(sorted(keys))}")
        for a in idxs:
            for b in idxs:
                if a != b:
                    forbidden.add(frozenset((a, b)))

    dsu = DisjointSet()
    for i in by_index:
        dsu.find(i)

    members: dict[int, set[int]] = {i: {i} for i in by_index}

    def try_union(a: int, b: int, why: str) -> None:
        ra, rb = dsu.find(a), dsu.find(b)
        if ra == rb:
            return
        for x in members[ra]:
            for y in members[rb]:
                if frozenset((x, y)) in forbidden:
                    report_lines["blocked"].append(
                        f"kept `{by_index[x].key}` and `{by_index[y].key}` apart "
                        f"({why} said they match, an override says otherwise)")
                    return
        dsu.union(a, b)
        root = dsu.find(a)
        merged = members[ra] | members[rb]
        members[root] = merged

    # 1. Forced merges win over everything.
    for block in ov.merges:
        keys = block["keys"]
        idxs = [i for k in keys for i in key_to_indices.get(k, [])]
        missing = [k for k in keys if k not in key_to_indices]
        if missing:
            report_lines["stale"].append(
                f"[[merge]] names unknown key(s) {', '.join(missing)}. "
                f"A directive is matched against the keys the source "
                f"bibliographies use, not against the keys this script "
                f"generates, because the generated ones do not exist yet when "
                f"the directive is applied.")
        else:
            ov.used.add(f"merge:{'+'.join(sorted(keys))}")
        if len(idxs) < 2:
            report_lines["stale"].append(
                f"[[merge]] on {', '.join(keys)} matched fewer than two "
                f"records and did nothing")
        for other in idxs[1:]:
            try_union(idxs[0], other, "an override")

    # 2. Same DOI. 3. Same arXiv identifier. 4. Same title and first author.
    for label, signal in (("DOI", "doi"), ("arXiv id", "eprint"), ("title", "title")):
        buckets: dict[str, list[int]] = defaultdict(list)
        for i, rec in by_index.items():
            if signal == "doi":
                probe = rec.fields.get("doi", "")
            elif signal == "eprint":
                probe = rec.fields.get("eprint", "") if rec.fields.get("eprinttype") == "arxiv" else ""
            else:
                t = norm_title(rec.fields.get("title", ""))
                s = first_surname(rec.fields)
                probe = f"{s}|{t}" if t and s else ""
            if probe:
                buckets[probe].append(i)
        for probe, idxs in buckets.items():
            for other in idxs[1:]:
                try_union(idxs[0], other, f"a matching {label}")

    grouped: dict[int, list[Record]] = defaultdict(list)
    for i, rec in by_index.items():
        grouped[dsu.find(i)].append(rec)

    confirmed_keys = {k for block in ov.merges for k in block.get("keys", [])}
    groups = [
        Group(records=sorted(recs, key=record_sort_key),
              confirmed=any(rec.key in confirmed_keys for rec in recs))
        for recs in grouped.values()
    ]

    report_fuzzy(groups, forbidden, key_to_indices, report_lines)
    return groups


def record_sort_key(rec: Record) -> tuple:
    """Canonical record first: published form, most fields, earliest source."""
    return (rec.type_rank, -len(rec.fields), rec.source_index, rec.order, rec.key)


def report_fuzzy(groups: list[Group], forbidden: set[frozenset[int]],
                 key_to_indices: dict[str, list[int]],
                 report_lines: dict[str, list[str]]) -> None:
    """Flag near duplicate titles that survived grouping. Never merge them."""
    probes = []
    for g in groups:
        rec = g.records[0]
        t = norm_title(rec.fields.get("title", ""))
        if t:
            probes.append((t, first_surname(rec.fields), year_of(rec.fields), g))

    for i in range(len(probes)):
        ti, si, yi, gi = probes[i]
        for j in range(i + 1, len(probes)):
            tj, sj, yj, gj = probes[j]
            if abs(len(ti) - len(tj)) > 12:
                continue
            if si != sj and yi != yj:
                continue
            ratio = difflib.SequenceMatcher(None, ti, tj).ratio()
            if ratio < FUZZY_TITLE_THRESHOLD:
                continue
            ka, kb = gi.records[0].key, gj.records[0].key
            idxa = key_to_indices.get(ka, [None])[0]
            idxb = key_to_indices.get(kb, [None])[0]
            if idxa is not None and idxb is not None and frozenset((idxa, idxb)) in forbidden:
                continue
            report_lines["fuzzy"].append(
                f"- `{ka}` and `{kb}` (similarity {ratio:.2f})\n"
                f"  - {gi.records[0].fields.get('title', '')} "
                f"[{gi.records[0].source}]\n"
                f"  - {gj.records[0].fields.get('title', '')} "
                f"[{gj.records[0].source}]\n"
                f"\n```toml\n[[merge]]  # or [[split]]\n"
                f'keys = ["{ka}", "{kb}"]\nreason = ""\n```\n')


# ============================================================================
# FIELD MERGING
# ============================================================================

def comparable(fname: str, value: str) -> str:
    """The form used to decide whether two values really disagree."""
    if fname == "author" or fname == "editor":
        names = [surname_of(a) for a in split_authors(value)]
        return "|".join(n for n in names if n)
    if fname == "pages":
        return norm_pages(value).replace("--", "-")
    if fname == "doi":
        return norm_doi(value)
    if fname in {"year", "volume", "number"}:
        return re.sub(r"[^0-9]", "", value)
    return norm_title(value)


def pick_value(fname: str, candidates: list[tuple[str, Record]]) -> str:
    policy = CONFLICT_POLICY.get(fname, DEFAULT_CONFLICT_POLICY)
    values = [v for v, _ in candidates]
    if policy == "longest":
        if fname in {"author", "editor"}:
            best = max(candidates, key=lambda c: (len(split_authors(c[0])),
                                                  "others" not in c[0].lower(),
                                                  len(c[0])))
            return best[0]
        return max(values, key=len)
    if policy == "range":
        for v in values:
            if "--" in v:
                return v
        return values[0]
    if policy == "first":
        return values[0]
    return values[0]  # canonical, which is first by construction


# Below this title similarity, two records that matched on a DOI or an arXiv
# identifier are almost certainly two different works sharing a wrong pointer.
SUSPICIOUS_MERGE_THRESHOLD = 0.60


def merge_group(group: Group, report_lines: dict[str, list[str]]) -> None:
    """Fold the records of one group into one entry, recording disagreements."""
    canonical = group.records[0]
    group.etype = canonical.etype

    names: list[str] = []
    for rec in group.records:
        for fname in rec.fields:
            if fname not in names:
                names.append(fname)

    for fname in names:
        candidates = [(rec.fields[fname], rec) for rec in group.records
                      if rec.fields.get(fname)]
        if not candidates:
            continue
        distinct: dict[str, tuple[str, Record]] = {}
        for value, rec in candidates:
            distinct.setdefault(comparable(fname, value), (value, rec))
        group.fields[fname] = pick_value(fname, candidates)
        if len(distinct) > 1:
            group.conflicts.append(
                (fname, [(rec.source, value) for value, rec in distinct.values()]))

    # A group holding both a preprint and a published version keeps the
    # published type, and the arXiv identifier rides along as `eprint`.
    if group.fields.get("eprinttype") == "arxiv" and not group.fields.get("eprint"):
        del group.fields["eprinttype"]

    years = {year_of(rec.fields) for rec in group.records if year_of(rec.fields)}
    if len(years) > 1:
        span = max(int(y) for y in years) - min(int(y) for y in years)
        if span > 1:
            group.notes.append(
                f"years disagree by {span} ({', '.join(sorted(years))})")

    # A DOI or arXiv identifier shared by two unrelated titles means one of the
    # two source entries carries the wrong pointer. Merging them silently would
    # make one chapter cite the wrong paper, so say so loudly.
    if len(group.records) > 1 and not group.confirmed:
        titles = [norm_title(rec.fields.get("title", "")) for rec in group.records]
        titles = [t for t in titles if t]
        worst = min(
            (difflib.SequenceMatcher(None, a, b).ratio()
             for i, a in enumerate(titles) for b in titles[i + 1:]),
            default=1.0)
        if worst < SUSPICIOUS_MERGE_THRESHOLD:
            listing = "; ".join(
                f"`{rec.key}` ({Path(rec.source).parent.name}) "
                f"\"{rec.fields.get('title', '')}\""
                for rec in group.records)
            shared = group.fields.get("doi") or group.fields.get("eprint") or "?"
            report_lines["errors"].append(
                f"merged on `{shared}`, but the titles do not match, so one of "
                f"these entries has the wrong DOI or arXiv id: {listing}. "
                f"Fix the wrong one with an `[entry.<key>] doi = ...` override "
                f"and keep them apart with a `[[split]]` block.")


# ============================================================================
# KEY GENERATION
# ============================================================================

def title_word(title: str) -> str:
    t = ascii_fold(title).lower()
    t = re.sub(r"[^a-z0-9 ]+", " ", t)
    for word in t.split():
        if word in TITLE_SKIP_WORDS or len(word) < 3 or word.isdigit():
            continue
        return word
    for word in t.split():
        if len(word) >= 3:
            return word
    return "untitled"


def base_key(group: Group) -> str:
    surname = first_surname(group.fields) or "anon"
    word = title_word(group.fields.get("title", ""))
    year = year_of(group.fields) or "nodate"
    return f"{surname}_{word}_{year}"


def assign_keys(groups: list[Group], ov: Overrides, previous: dict[str, str],
                report_lines: dict[str, list[str]]) -> None:
    """Give every group a key, reusing the previous run's key where possible."""
    pinned: dict[int, str] = {}
    for gi, group in enumerate(groups):
        for rec in group.records:
            patch = ov.entry.get(rec.key)
            if patch and "_key" in patch:
                pinned[gi] = patch["_key"]
                ov.used.add(f"entry:{rec.key}")
                break

    # Reuse the key the last run gave this entry, so that citations already
    # written against it keep working. Only when the group holds exactly the
    # same records as last time. If a merge or a split changed what the entry
    # is, the old key described something else and has to go.
    previous_members: dict[str, set[str]] = defaultdict(set)
    for old, new in previous.items():
        previous_members[new].add(old)

    carried: dict[int, str] = {}
    for gi, group in enumerate(groups):
        if gi in pinned:
            continue
        seen = {previous[rec.key] for rec in group.records if rec.key in previous}
        if len(seen) != 1:
            continue
        candidate = seen.pop()
        if previous_members[candidate] == {rec.key for rec in group.records}:
            carried[gi] = candidate
        else:
            report_lines["notes"].append(
                f"`{candidate}` no longer describes the same set of source "
                f"entries, so its key was regenerated")

    taken: set[str] = set(pinned.values())
    for gi in sorted(carried, key=lambda g: carried[g]):
        if carried[gi] not in taken:
            taken.add(carried[gi])
        else:
            del carried[gi]

    buckets: dict[str, list[int]] = defaultdict(list)
    for gi, group in enumerate(groups):
        if gi in pinned or gi in carried:
            continue
        buckets[base_key(group)].append(gi)

    for base, idxs in buckets.items():
        idxs.sort(key=lambda g: (norm_title(groups[g].fields.get("title", "")),
                                 groups[g].fields.get("doi", ""),
                                 groups[g].records[0].key))
        if len(idxs) == 1 and base not in taken:
            groups[idxs[0]].new_key = base
            taken.add(base)
            continue
        for n, gi in enumerate(idxs):
            suffix = chr(ord("a") + n) if n < 26 else f"_{n}"
            candidate = f"{base}{suffix}"
            while candidate in taken:
                n += 1
                suffix = chr(ord("a") + n) if n < 26 else f"_{n}"
                candidate = f"{base}{suffix}"
            groups[gi].new_key = candidate
            taken.add(candidate)

    for gi, key in pinned.items():
        groups[gi].new_key = key
    for gi, key in carried.items():
        groups[gi].new_key = key

    # If a generated key differs from one of the group's own old keys only in
    # case, adopt the old key. Biber matches keys case-insensitively, so the
    # two cannot coexist as key and alias: the entry would alias itself and
    # biber would abort. Dropping the alias instead is worse, because the
    # imported chapter still cites the old spelling and biber then aborts on a
    # citekey it can neither find nor alias. Adopting it keeps the citation
    # working and needs no alias at all.
    taken_ci = {g.new_key.lower() for g in groups}
    for group in groups:
        if any(rec.key == group.new_key for rec in group.records):
            continue
        for rec in group.records:
            if rec.key.lower() == group.new_key.lower():
                taken_ci.discard(group.new_key.lower())
                report_lines["notes"].append(
                    f"kept `{rec.key}` as the citation key rather than "
                    f"`{group.new_key}`, which differs only in case")
                group.new_key = rec.key
                taken_ci.add(rec.key.lower())
                break


def assign_aliases(groups: list[Group], previous: dict[str, str],
                   report_lines: dict[str, list[str]]) -> None:
    """Every old key becomes an alias, so imported .tex keeps compiling."""
    # Biber matches citation keys case-insensitively. An alias that differs
    # from its own key only in case therefore makes the entry alias itself, and
    # biber does not report that: it dies with "Can't call method get_field on
    # an undefined value" and writes no bibliography, so every citation in the
    # thesis silently renders as a raw key. All the comparisons below are
    # folded to lower case for that reason.
    primary = {g.new_key.lower() for g in groups}
    owner: dict[str, Group] = {}

    # Source keys first. Losing one of these breaks a citation in an imported
    # chapter, which we cannot edit, so a clash here is an error.
    for group in groups:
        for rec in group.records:
            alias = rec.key
            if alias.lower() == group.new_key.lower() or alias in group.aliases:
                continue
            if alias.lower() in primary:
                report_lines["errors"].append(
                    f"`{alias}` is a citation key in a source bibliography and "
                    f"also the generated key of `{alias}`, a different work. "
                    f"Citations of `{alias}` in imported files would resolve to "
                    f"the wrong reference. Pin a different key with "
                    f"`[entry.{alias}] _key = \"...\"`.")
                continue
            if owner.get(alias.lower()) not in (None, group):
                report_lines["errors"].append(
                    f"citation key `{alias}` is used for two different works "
                    f"(`{owner[alias].new_key}` and `{group.new_key}`). Biber "
                    f"can alias it to only one of them, so one imported chapter "
                    f"will cite the wrong reference until this is resolved.")
                continue
            owner[alias.lower()] = group
            group.aliases.append(alias)

    # Then the key the last run generated, if it changed. This only protects
    # citations in thesis owned files, which `--apply-keys` can rewrite anyway,
    # so a clash here is not worth reporting.
    for group in groups:
        seen = {previous[rec.key] for rec in group.records if rec.key in previous}
        if len(seen) != 1:
            continue
        alias = seen.pop()
        if (alias.lower() == group.new_key.lower() or alias.lower() in primary
                or alias.lower() in owner):
            continue
        owner[alias.lower()] = group
        group.aliases.append(alias)
        report_lines["notes"].append(
            f"`{alias}` became `{group.new_key}`, kept as an alias. Run with "
            f"`--apply-keys` to update thesis owned files.")

    for group in groups:
        group.aliases.sort()


# ============================================================================
# PATCHES
# ============================================================================

def apply_patches(groups: list[Group], ov: Overrides,
                  report_lines: dict[str, list[str]]) -> list[Group]:
    """Apply per entry corrections from overrides.toml. Overrides always win."""
    kept: list[Group] = []
    for group in groups:
        addresses = [rec.key for rec in group.records] + [group.new_key]
        patches = [(addr, ov.entry[addr]) for addr in addresses if addr in ov.entry]
        dropped = False
        for addr, patch in patches:
            ov.used.add(f"entry:{addr}")
            if patch.get("_drop"):
                dropped = True
                continue
            for name in patch.get("_remove", []):
                group.fields.pop(name.lower(), None)
            if "_type" in patch:
                group.etype = str(patch["_type"]).lower()
            for name, value in patch.items():
                if name.startswith("_"):
                    continue
                group.fields[name.lower()] = tidy_value(str(value))
            # A hand set value settles any disagreement about that field.
            patched = {n.lower() for n in patch if not n.startswith("_")}
            group.conflicts = [c for c in group.conflicts if c[0] not in patched]
        if dropped:
            report_lines["notes"].append(f"dropped `{group.new_key}` on request")
            continue
        kept.append(group)
    return kept


# ============================================================================
# QUALITY CHECKS
# ============================================================================

VENUE_FIELDS = ("journal", "booktitle", "publisher", "institution", "school",
                "howpublished", "eprint")


# Fields whose value is a citation key, not text. They have to follow the key
# renaming like any citation does, and a dangling one is not cosmetic: biber
# aborts with "Can't call method get_field on an undefined value" and writes no
# bibliography at all, so every citation in the thesis silently renders as a
# raw key.
KEY_VALUED_FIELDS = ("crossref", "xref")


def fix_crossrefs(groups: list[Group], report_lines: dict[str, list[str]]) -> None:
    lookup: dict[str, str] = {}
    for group in groups:
        lookup[group.new_key] = group.new_key
        for rec in group.records:
            lookup[rec.key] = group.new_key
        for alias in group.aliases:
            lookup[alias] = group.new_key

    for group in groups:
        for field in KEY_VALUED_FIELDS:
            target = group.fields.get(field)
            if not target:
                continue
            new = lookup.get(target.strip())
            if new is None:
                del group.fields[field]
                report_lines["notes"].append(
                    f"`{group.new_key}` pointed {field} at `{target}`, which is "
                    f"in no bibliography. The field was dropped, because biber "
                    f"aborts on a dangling one.")
            elif new != target:
                group.fields[field] = new


def check_quality(groups: list[Group], report_lines: dict[str, list[str]]) -> None:
    _cited = cited_keys()
    for group in sorted(groups, key=lambda g: g.new_key):
        f = group.fields
        missing = []
        if not f.get("author"):
            missing.append("author")
        if not f.get("title"):
            missing.append("title")
        if not year_of(f):
            missing.append("year")
        if missing:
            where = "errors"
            note = ""
            reachable = {group.new_key, *group.aliases,
                         *(r.key for r in group.records)}
            if _cited and not (reachable & _cited):
                where = "uncited_incomplete"
                note = ""
            report_lines[where].append(
                f"`{group.new_key}` has no {', '.join(missing)} "
                f"(from {group.records[0].source}){note}")

        if not f.get("doi") and not f.get("eprint") and not f.get("url"):
            report_lines["no_pointer"].append(
                f"`{group.new_key}` has no DOI, no arXiv id and no URL")
        elif not f.get("doi") and group.etype in {"article", "inproceedings"}:
            report_lines["no_doi"].append(f"`{group.new_key}` has no DOI")

        if not any(f.get(name) for name in VENUE_FIELDS):
            report_lines["no_venue"].append(
                f"`{group.new_key}` names no journal, book, publisher or preprint server")

        risky = sorted({c for v in f.values() for c in v
                        if ord(c) > 0x17F and c not in "–—‘’“”…"})
        if risky:
            report_lines["encoding"].append(
                f"`{group.new_key}` contains {' '.join(risky)}, which T1 encoded "
                f"pdflatex may not be able to set")


# ============================================================================
# OUTPUT
# ============================================================================

def format_entry(group: Group) -> str:
    fields = dict(group.fields)
    if group.aliases:
        fields["ids"] = ", ".join(group.aliases)
    ordered = [n for n in FIELD_ORDER if n in fields]
    ordered += sorted(n for n in fields if n not in FIELD_ORDER)
    width = max((len(n) for n in ordered), default=0)
    lines = [f"@{group.etype}{{{group.new_key},"]
    for name in ordered:
        lines.append(f"  {name.ljust(width)} = {{{fields[name]}}},")
    if len(lines) > 1:
        lines[-1] = lines[-1].rstrip(",")
    lines.append("}")
    return "\n".join(lines)


def write_bib(path: Path, groups: list[Group]) -> None:
    header = [
        "% references/merged.bib",
        "%",
        "% GENERATED by scripts/merge_bib.py. Do not edit this file.",
        "% Corrections belong in references/overrides.toml, then re-run:",
        "%     uv run --no-project python scripts/merge_bib.py",
        "%",
        "% Every entry's `ids` field lists the citation keys it carried in the",
        "% source bibliographies. Biber treats those as aliases, which is what",
        "% lets the imported papers keep citing their original keys.",
        "%",
        "% Sources:",
    ]
    for name in INPUT_FILES:
        header.append(f"%   {name}")
    header.append(f"% {len(groups)} entries.")
    header.append("")
    body = "\n\n".join(format_entry(g) for g in sorted(groups, key=lambda g: g.new_key))
    path.write_text("\n".join(header) + "\n" + body + "\n", encoding="utf-8")


def write_keymap(path: Path, groups: list[Group]) -> None:
    rows = []
    for group in groups:
        for rec in group.records:
            rows.append((rec.key, rec.source, group.new_key))
    rows.sort()
    with path.open("w", encoding="utf-8", newline="") as fh:
        # \n explicitly: csv defaults to \r\n, which makes the file differ
        # by platform and breaks the byte identical rerun guarantee.
        writer = csv.writer(fh, lineterminator="\n")
        writer.writerow(["old_key", "source_file", "new_key"])
        writer.writerows(rows)


def read_keymap(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    previous: dict[str, str] = {}
    with path.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            previous[row["old_key"]] = row["new_key"]
    return previous


def write_report(path: Path, groups: list[Group], records: list[Record],
                 report_lines: dict[str, list[str]], ov: Overrides) -> int:
    merged = [g for g in groups if len(g.records) > 1]
    out: list[str] = []
    add = out.append

    add("# Bibliography merge report")
    add("")
    add("Generated by `scripts/merge_bib.py`. Fix things in "
        "`references/overrides.toml` and re-run.")
    add("")
    add("## Summary")
    add("")
    add(f"- {len(records)} entries read from {len(INPUT_FILES)} files")
    add(f"- {len(groups)} entries written")
    add(f"- {len(merged)} of them merged from two or more sources")
    add(f"- {sum(len(g.aliases) for g in groups)} old keys kept alive as aliases")
    add("")

    conflicts = [g for g in groups if g.conflicts]
    sections = [
        ("errors", "Errors", "These break the build or cite the wrong work. Fix them."),
        ("uncited_incomplete", "Incomplete, and cited by nothing in the build",
         "Missing an author, a title or a year, in an entry no included text "
         "cites. Most arrive in the bibliography of a paper the thesis "
         "summarises rather than reproduces, so nothing can reach them. They "
         "are listed because wiring that paper back in would promote them to "
         "errors. This section is computed from `main.bcf`, so it is empty "
         "until the thesis has been built once."),
        ("blocked", "Merges an override prevented", None),
        ("fuzzy", "Possible duplicates, not merged",
         "Titles that look alike but share no DOI, arXiv id or exact title. "
         "Decide each one and paste the block into `references/overrides.toml`."),
        ("stale", "Overrides that matched nothing",
         "These name keys that no longer exist. Delete them or fix the key."),
        ("notes", "Notes", None),
        ("recovered_year", "Years taken from the citation key",
         "The entry carried no year field. Spot check these, and pin the right "
         "one with an `[entry.<key>] year = ...` override if any is wrong."),
        ("no_pointer", "No DOI, no arXiv id and no URL",
         "Nothing here lets a reader find the work."),
        ("no_doi", "No DOI", "Journal and conference entries that should have one."),
        ("no_venue", "No venue", None),
        ("encoding", "Characters pdflatex may not set", None),
    ]

    add("## Field conflicts")
    add("")
    if not conflicts:
        add("None.")
    else:
        add(f"{len(conflicts)} entries where two sources give different values. "
            "The chosen value is listed first. To settle one, paste its block "
            "into `references/overrides.toml`.")
        add("")
        for group in sorted(conflicts, key=lambda g: g.new_key):
            add(f"### `{group.new_key}`")
            add("")
            add(f"{group.fields.get('title', '(no title)')}")
            add("")
            for fname, values in group.conflicts:
                chosen = group.fields.get(fname, "")
                add(f"- **{fname}** -> `{chosen}`")
                for source, value in values:
                    marker = "chosen" if comparable(fname, value) == comparable(fname, chosen) else "dropped"
                    add(f"  - {marker}, from `{source}`: `{value}`")
            for note in group.notes:
                add(f"- {note}")
            add("")
            add("```toml")
            add(f"[entry.{group.new_key}]")
            for fname, _ in group.conflicts:
                add(f'{fname} = "{group.fields.get(fname, "")}"')
            add("```")
            add("")
    add("")

    for name, title, blurb in sections:
        lines = report_lines.get(name) or []
        add(f"## {title}")
        add("")
        if blurb:
            add(blurb)
            add("")
        if not lines:
            add("None.")
        else:
            for line in lines:
                # Multi line blocks bring their own bullets and fences.
                add(line if line.startswith(("-", "#", "```")) else f"- {line}")
        add("")

    add("## Merged groups")
    add("")
    if not merged:
        add("None.")
    for group in sorted(merged, key=lambda g: g.new_key):
        sources = ", ".join(f"`{rec.key}` ({Path(rec.source).parent.name})"
                            for rec in group.records)
        add(f"- `{group.new_key}` <- {sources}")
    add("")

    path.write_text("\n".join(out) + "\n", encoding="utf-8")
    return len(report_lines.get("errors") or [])


# ============================================================================
# KEY REWRITING IN THESIS OWNED FILES
# ============================================================================

CITE_RE = re.compile(
    r"\\(" + "|".join(CITE_COMMANDS) + r")(\*?)((?:\[[^\]]*\])*)\{([^{}]*)\}")


def apply_keys(keymap: dict[str, str]) -> list[str]:
    """Rewrite citation keys in thesis owned .tex files. Never imported ones."""
    messages: list[str] = []
    for pattern in THESIS_TEX:
        for path in sorted(ROOT.glob(pattern)):
            if "imported_papers" in path.parts or "generated" in path.parts:
                continue
            text = path.read_text(encoding="utf-8")
            unknown: set[str] = set()
            changes = 0

            def rewrite(m: re.Match) -> str:
                nonlocal changes
                keys = [k.strip() for k in m.group(4).split(",")]
                out = []
                for k in keys:
                    if not k:
                        continue
                    if k in keymap:
                        if keymap[k] != k:
                            changes += 1
                        out.append(keymap[k])
                    else:
                        unknown.add(k)
                        out.append(k)
                return f"\\{m.group(1)}{m.group(2)}{m.group(3)}{{{', '.join(out)}}}"

            new_text = CITE_RE.sub(rewrite, text)
            if new_text != text:
                path.write_text(new_text, encoding="utf-8")
                messages.append(f"{path.relative_to(ROOT)}: rewrote {changes} keys")
            if unknown:
                messages.append(
                    f"{path.relative_to(ROOT)}: {len(unknown)} keys not in the "
                    f"bibliography: {', '.join(sorted(unknown))}")
    return messages


# ============================================================================
# MAIN
# ============================================================================

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true",
                        help="write the report only, and fail if it lists errors")
    parser.add_argument("--apply-keys", action="store_true",
                        help="also rewrite citation keys in thesis owned .tex files")
    args = parser.parse_args()

    report_lines: dict[str, list[str]] = defaultdict(list)
    problems: list[str] = []

    ov = load_overrides(ROOT / OVERRIDES_FILE, problems)

    records: list[Record] = []
    for index, name in enumerate(INPUT_FILES):
        path = ROOT / name
        if not path.exists():
            problems.append(f"input file missing: {name}")
            continue
        parsed = parse_bib(path.read_text(encoding="utf-8"), name, index, problems)
        records.extend(parsed)
        print(f"  {len(parsed):4d} entries  {name}")

    if not records:
        print("no entries read, nothing to do", file=sys.stderr)
        return 1

    for rec in records:
        normalise_record(rec, ov.replace, report_lines)

    groups = build_groups(records, ov, report_lines)
    for group in groups:
        merge_group(group, report_lines)

    previous = read_keymap(ROOT / OUTPUT_KEYMAP)
    assign_keys(groups, ov, previous, report_lines)
    groups = apply_patches(groups, ov, report_lines)
    assign_aliases(groups, previous, report_lines)
    fix_crossrefs(groups, report_lines)
    check_quality(groups, report_lines)

    for addr in ov.entry:
        if f"entry:{addr}" not in ov.used:
            report_lines["stale"].append(
                f"[entry.{addr}] matches no entry in any bibliography")
    report_lines["errors"] = problems + list(report_lines.get("errors") or [])

    out_dir = ROOT / OUTPUT_BIB
    out_dir.parent.mkdir(parents=True, exist_ok=True)
    n_errors = write_report(ROOT / OUTPUT_REPORT, groups, records, report_lines, ov)

    if not args.check:
        write_bib(ROOT / OUTPUT_BIB, groups)
        write_keymap(ROOT / OUTPUT_KEYMAP, groups)

    merged = sum(1 for g in groups if len(g.records) > 1)
    print()
    print(f"  {len(records)} entries in, {len(groups)} out, "
          f"{len(records) - len(groups)} folded into {merged} merged entries")
    print(f"  {sum(len(g.aliases) for g in groups)} old keys kept as aliases")
    print(f"  report: {OUTPUT_REPORT}")
    if n_errors:
        print(f"  {n_errors} errors, see the report")

    if args.apply_keys:
        keymap = {rec.key: g.new_key for g in groups for rec in g.records}
        print()
        for message in apply_keys(keymap):
            print(f"  {message}")

    return 1 if (args.check and n_errors) else 0


if __name__ == "__main__":
    sys.exit(main())
