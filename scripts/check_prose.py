#!/usr/bin/env python3
"""Screen thesis owned prose for the patterns that mark machine written text.

CLAUDE.md section 3.10 already gives three greps: em dashes, the banned word
list, and semicolons. They catch the easy half. This script carries those and
adds the tells that a grep cannot express, chiefly the ones about rhythm
rather than vocabulary, because a language model's prose gives itself away by
its evenness long before it reaches for "delve".

Scope is thesis owned files only. Imported papers are published text and are
exempt, per CLAUDE.md section 4.1.

    uv run --no-project python scripts/check_prose.py [paths...]

With no paths it screens main.tex, preface.tex and sections/. Exits non zero
when anything in a `hard` category is found, so it can gate a commit. The
`soft` categories are reported and do not fail, because they need a human to
look: a long paragraph of even sentences may be a list of measurements, and a
triple may be three real things.
"""
from __future__ import annotations

import re
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT = ["main.tex", "preface.tex", "sections"]

BANNED = [
    "delve", "leverage", "harness", "unlock", "crucially", "notably",
    "importantly", "interestingly", "remarkably", "strikingly", "elegantly",
    "moreover", "furthermore", "additionally", "it is worth noting",
    "note that", "paradigm shift", "nuanced", "underscore", "showcase",
    "pivotal", "seamless", "shed light", "pave the way", "realm",
    "at its core", "a testament to", "serves as", "plays a role", "foster",
    "bolster", "cutting edge", "holistic", "multifaceted", "intricate",
    "interplay", "dive into", "stands in stark contrast",
    "a growing body of work", "has garnered attention", "in this work, we",
]

# Not banned by CLAUDE.md, but characteristic of generated prose. Reported as
# soft, because each has a legitimate use and the judgement is the author's.
TELLS = [
    "robust", "key insight", "critical", "ensures", "facilitates",
    "it is important", "comprehensive", "significantly", "dramatically",
    "vastly", "we believe", "we argue", "effectively", "notably",
]

HARD = {
    "em dash": re.compile(r"[—–]"),
    "banned word": re.compile("|".join(re.escape(w) for w in BANNED), re.I),
    "not only / but also": re.compile(r"not only\b.{0,80}?\bbut also", re.I | re.S),
    "is not just X, it is Y": re.compile(r"\bis not (just|merely|only)\b.{0,60}?,\s*it is\b", re.I | re.S),
    "roadmap opener": re.compile(
        r"(?m)^\s*(To answer this question|Recall that|In this section,? we|"
        r"Having established|In what follows|We now turn)", re.I),
    "stacked hedge": re.compile(
        r"\b(may|might|could|can)\b\s+(\w+\s+){0,2}"
        r"(potentially|possibly|perhaps|arguably|conceivably|suggest)", re.I),
    "prediction claimed in advance": re.compile(
        r"\b(predicted in advance|before training|before the runs|"
        r"pre-?specified|registered in advance)\b", re.I),
    "code identifier in prose": re.compile(r"(?<![\\\w/])[a-z]+_[a-z_]+(?![\w/}])"),
}

SOFT = {
    "characteristic word": re.compile("|".join(r"\b" + re.escape(w) + r"\b" for w in TELLS), re.I),
    "semicolon": re.compile(r";"),
}


def strip_latex(text: str) -> list[tuple[int, str]]:
    """Return (line number, prose) with comments, math and markup removed."""
    out = []
    for n, raw in enumerate(text.split("\n"), 1):
        line = re.sub(r"(?<!\\)%.*$", "", raw)
        # Lines that are nothing but a path or a declaration. They carry file
        # names with underscores, which the code identifier rule would
        # otherwise read as a code identifier in prose.
        if re.search(r"\\(DeclareImportedPaper|importsection|importpart"
                     r"|importsectionrotated|importedlabel|includegraphics"
                     r"|addbibresource|graphicspath|bibliography)\b", line):
            continue
        if re.match(r"\s*\\(label|ref|cite|input|include|begin|end|usepackage"
                    r"|documentclass|newcommand|renewcommand|def)\b", line):
            # Structural lines carry no prose worth screening, but \section
            # and \caption do, so keep those.
            if not re.match(r"\s*\\(begin\{(abstract|publicationbasis)\})", line):
                if not re.search(r"\\(section|subsection|paragraph|caption|chapter)\b", line):
                    continue
        line = re.sub(r"\$[^$]*\$", " NUM ", line)
        line = re.sub(r"\\(href|url)\{[^}]*\}", " ", line)
        line = re.sub(r"\\(cite|ref|cref|Cref|label|eqref|nameref)\w*\{[^}]*\}", " ", line)
        line = re.sub(r"\\texttt\{[^}]*\}", " ", line)
        line = re.sub(r"\\[a-zA-Z]+\*?", " ", line)
        line = re.sub(r"[{}]", " ", line)
        if line.strip():
            out.append((n, line))
    return out


def paragraphs(lines: list[tuple[int, str]]) -> list[tuple[int, str]]:
    """Group consecutive prose lines into paragraphs."""
    paras, cur, start, prev = [], [], None, None
    for n, line in lines:
        if prev is not None and n != prev + 1 and cur:
            paras.append((start, " ".join(cur)))
            cur, start = [], None
        if start is None:
            start = n
        cur.append(line.strip())
        prev = n
    if cur:
        paras.append((start, " ".join(cur)))
    return paras


def sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z])", text)
    return [p.strip() for p in parts if len(p.split()) > 2]


def check_rhythm(path: Path, paras: list[tuple[int, str]]) -> list[tuple[str, int, str]]:
    """Even sentence length is the tell a word list cannot catch.

    A person writing at speed produces sentences of uneven length. Generated
    prose tends to settle near one length and stay there. The threshold is
    deliberately loose: five or more sentences, and a coefficient of variation
    under 0.25, which in practice fires on passages that do read as even.
    """
    hits = []
    for start, body in paras:
        sents = sentences(body)
        if len(sents) < 5:
            continue
        lengths = [len(s.split()) for s in sents]
        mean = statistics.mean(lengths)
        if mean < 8:
            continue
        cv = statistics.pstdev(lengths) / mean
        if cv < 0.25:
            hits.append(("even sentence length", start,
                         f"{len(sents)} sentences, mean {mean:.0f} words, "
                         f"variation {cv:.2f}"))
        triples = len(re.findall(r"\w+,\s+\w+,?\s+and\s+\w+", body))
        if triples >= 3:
            hits.append(("parallel triples", start,
                         f"{triples} three item lists in one paragraph"))
    return hits


def check_file(path: Path) -> tuple[list, list]:
    text = path.read_text(encoding="utf-8")
    lines = strip_latex(text)
    hard, soft = [], []
    for n, line in lines:
        for name, pat in HARD.items():
            for m in pat.finditer(line):
                hard.append((name, n, m.group(0).strip()[:60]))
        for name, pat in SOFT.items():
            for m in pat.finditer(line):
                soft.append((name, n, m.group(0).strip()[:60]))
    soft.extend(check_rhythm(path, paragraphs(lines)))
    return hard, soft


def main() -> int:
    args = sys.argv[1:] or DEFAULT
    targets: list[Path] = []
    for a in args:
        p = ROOT / a
        if p.is_dir():
            targets.extend(sorted(p.glob("*.tex")))
        elif p.is_file():
            targets.append(p)
    n_hard = n_soft = 0
    for path in targets:
        hard, soft = check_file(path)
        if not hard and not soft:
            continue
        rel = path.relative_to(ROOT)
        print(f"\n{rel}")
        for name, n, what in sorted(hard, key=lambda h: h[1]):
            print(f"  {rel}:{n}  {name}: {what}")
        for name, n, what in sorted(soft, key=lambda h: h[1]):
            print(f"  {rel}:{n}  [soft] {name}: {what}")
        n_hard += len(hard)
        n_soft += len(soft)
    print(f"\n  {len(targets)} files, {n_hard} hard, {n_soft} soft")
    if n_hard:
        print("  Hard findings are style guide violations and block a commit.")
    print("  Soft findings need a human: each has a legitimate use.")
    return 1 if n_hard else 0


if __name__ == "__main__":
    raise SystemExit(main())
