#!/usr/bin/env python3
"""Split a monolithic imported paper into one file per section.

Three of the six papers arrived as a single .tex file. A chapter cannot include
half a file, so the parts a chapter wants have to exist as files. This script
cuts the paper at its top level \\section boundaries and writes the pieces to
generated/imported/<slug>/, which is committed so that Overleaf, which has no
Python, can still build.

The paper itself is never touched. Everything here reads from
imported_papers/ and writes to generated/.

Run from the repository root:

    uv run --no-project python scripts/split_paper.py
    uv run --no-project python scripts/split_paper.py --paper cna
    uv run --no-project python scripts/split_paper.py --check

`--check` regenerates into memory and fails if the committed files differ,
which is what catches a re import that nobody re-split.
"""

from __future__ import annotations

import argparse
import fnmatch
import re
import sys
import tomllib
from dataclasses import dataclass, field as dc_field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST_DIR = ROOT / "imports"
OUTPUT_ROOT = ROOT / "generated" / "imported"

# The chunk before the first \section: title, authors, abstract. Named so that
# it can be dropped in the manifest like any other part, with a reason.
FRONT_MATTER = "(front matter)"

SECTION_START = re.compile(r"^[ \t]*\\section(\*?)\s*\{", re.M)
BEGIN_DOC = re.compile(r"\\begin\{document\}")
END_DOC = re.compile(r"\\end\{document\}")
APPENDIX_RE = re.compile(r"^[ \t]*\\appendix[ \t]*$", re.M)


def find_sections(text: str) -> list[tuple[int, str]]:
    """Every top level \\section as (offset of the command, title).

    The title is read by matching braces rather than by a regular expression,
    because a section line often carries a \\label after the title and a title
    may itself contain braces. `\\section{Introduction}\\label{sec:intro}` has
    the title `Introduction`, not `Introduction}\\label{sec:intro`.

    scripts/check_imports.py imports this, so that the checker and the splitter
    can never disagree about what a paper's sections are.
    """
    out: list[tuple[int, str]] = []
    for m in SECTION_START.finditer(text):
        depth = 1
        i = m.end()
        while i < len(text) and depth:
            c = text[i]
            if c == "\\":
                i += 2
                continue
            if c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    break
            i += 1
        if depth == 0:
            out.append((m.start(), text[m.end():i].strip()))
    return out

# Constructs that would inject a second bibliography or renumber the thesis
# appendix. Each removal is reported.
STRIP_LINES = [
    (re.compile(r"^[ \t]*\\bibliographystyle\{[^}]*\}[ \t]*$", re.M),
     "bibliography style, the thesis sets its own"),
    (re.compile(r"^[ \t]*\\bibliography\{[^}]*\}[ \t]*$", re.M),
     "bibliography, the thesis loads references/merged.bib"),
    (re.compile(r"^[ \t]*\\printbibliography(\[[^\]]*\])?[ \t]*$", re.M),
     "bibliography, the thesis loads references/merged.bib"),
]
# \appendix is removed at render time rather than here, because where it sits
# is what tells us which parts are appendix material.
THEBIB_RE = re.compile(
    r"\\begin\{thebibliography\}.*?\\end\{thebibliography\}", re.S)

# The paper's body uses macros its own preamble defines. We drop the preamble,
# so those definitions have to be carried across or the chapter will not build.
MACRO_START = re.compile(
    r"^[ \t]*\\(?:new|renew|provide)command\*?\s*[\\{]"
    r"|^[ \t]*\\def\s*\\"
    r"|^[ \t]*\\DeclareMathOperator\*?\s*\{"
    r"|^[ \t]*\\newcolumntype\s*\{"
    r"|^[ \t]*\\newcounter\s*\{"
    # Named definitions whose name is not a macro. They cannot be matched
    # against usage, so ALWAYS_CARRY keeps them unconditionally.
    r"|^[ \t]*\\lstdefinestyle\s*\{"
    r"|^[ \t]*\\lstnewenvironment\s*\{"
    r"|^[ \t]*\\(?:new|renew)environment\*?\s*\{"
    r"|^[ \t]*\\newtcolorbox\s*\{"
    r"|^[ \t]*\\DeclareRobustCommand\*?\s*[\\{]", re.M)
USEPACKAGE_RE = re.compile(r"^[ \t]*\\usepackage(\[[^\]]*\])?\{([^}]*)\}", re.M)
DECLARE_OP_RE = re.compile(
    r"\\DeclareMathOperator(\*?)\s*\{(\\[A-Za-z@]+)\}\s*\{([^}]*)\}")
MACROS_FILE = "_macros.tex"
COLOUR_RE = re.compile(r"^[ \t]*\\(?:definecolor|colorlet)\*?\{.*$", re.M)
ANY_INPUT_RE = re.compile(r"\\\\(?:input|subfile|include)\\s*\\{([^}]*)\\}")

# Theorem environments kaotheorems declares, which every chapter inherits.
THESIS_THEOREMS = {
    "theorem", "proposition", "lemma", "corollary", "definition", "remark",
    "assumption", "example", "exercise", "proof",
}

# Packages the thesis already provides, one way or another, so a paper asking
# for them is not news.
PACKAGES_THESIS_HAS = {
    "amsmath", "amssymb", "amsfonts", "graphicx", "xcolor", "hyperref",
    "cleveref", "booktabs", "tabularx", "url", "subcaption", "enumitem",
    "multirow", "float", "algorithm", "algorithmic", "algpseudocode",
    "longtable", "threeparttable", "xspace", "inputenc", "fontenc", "babel",
    "microtype", "caption", "comment", "textcomp", "cite", "natbib",
}


@dataclass
class Part:
    index: int
    title: str
    body: str
    in_appendix: bool

    @property
    def filename(self) -> str:
        return f"{self.index:02d}_{slugify(self.title)}.tex"


@dataclass
class Result:
    slug: str
    written: list[str] = dc_field(default_factory=list)
    unchanged: list[str] = dc_field(default_factory=list)
    removed: list[str] = dc_field(default_factory=list)
    dropped: list[tuple[str, str]] = dc_field(default_factory=list)
    notes: list[str] = dc_field(default_factory=list)
    errors: list[str] = dc_field(default_factory=list)


def slugify(title: str) -> str:
    t = re.sub(r"\\[a-zA-Z]+\s*", " ", title)
    t = t.replace("{", " ").replace("}", " ")
    t = re.sub(r"[^A-Za-z0-9]+", "-", t).strip("-").lower()
    return t or "untitled"


def load_manifests(only: str | None) -> list[dict]:
    out = []
    for path in sorted(MANIFEST_DIR.glob("*.toml")):
        with path.open("rb") as fh:
            data = tomllib.load(fh)
        # A sections paper has a preamble too, in the root file it names as
        # `source`, and the text the chapter keeps uses the macros defined
        # there. Those papers get a _macros.tex but no section splitting.
        if "source" not in data:
            continue
        if only and data.get("slug", path.stem) != only:
            continue
        data.setdefault("slug", path.stem)
        out.append(data)
    return out


def consume_group(text: str, i: int) -> int:
    """End offset of the balanced {...} or [...] group starting at `i`."""
    opener = text[i]
    closer = "}" if opener == "{" else "]"
    depth = 0
    while i < len(text):
        c = text[i]
        if c == "\\":
            i += 2
            continue
        if c == opener:
            depth += 1
        elif c == closer:
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    return len(text)


def balanced_block(text: str, start: int) -> int:
    """End offset of the macro definition beginning at `start`.

    A definition is the command, an optional star, an optional macro name, and
    then every argument group that follows it. All of them: \\newcommand takes
    a name and a body, and \\DeclareMathOperator takes a name and an operator,
    so stopping after the first group truncates the definition and produces a
    file that does not compile.

    Only spaces and tabs may separate the groups. A newline ends the
    definition, which is what stops one \\newcommand from swallowing the next.
    """
    i = start
    while i < len(text) and text[i] in " \t":
        i += 1
    if i < len(text) and text[i] == "\\":               # the command itself
        i += 1
        while i < len(text) and text[i].isalpha():
            i += 1
    if i < len(text) and text[i] == "*":
        i += 1
    while i < len(text) and text[i] in " \t":
        i += 1
    if i < len(text) and text[i] == "\\":               # \def\name, \newcommand\name
        i += 1
        while i < len(text) and text[i].isalpha():
            i += 1
    while i < len(text) and text[i] in " \t#0123456789":
        i += 1
    while i < len(text) and text[i] in "{[":
        i = consume_group(text, i)
        while i < len(text) and text[i] in " \t":
            i += 1
    return i


DEFINED_NAME_RE = re.compile(
    r"^[ \t]*\\(?:new|renew|provide)command\*?\s*\{?(\\[A-Za-z@]+)"
    r"|^[ \t]*\\def\s*(\\[A-Za-z@]+)"
    r"|^[ \t]*\\DeclareMathOperator\*?\s*\{(\\[A-Za-z@]+)\}")
ALWAYS_CARRY = re.compile(
    r"^[ \t]*\\(?:newcolumntype|newcounter|lstdefinestyle|lstnewenvironment"
    r"|newenvironment|renewenvironment|newtcolorbox)")
USED_NAME_RE = re.compile(r"\\([A-Za-z@]+)")


def defined_name(block: str) -> str | None:
    m = DEFINED_NAME_RE.match(block)
    if not m:
        return None
    return next(g for g in m.groups() if g)


def needed_macros(blocks: list[str], body: str, result: Result) -> list[str]:
    """Only the definitions the kept text actually uses, plus what those use.

    Carrying a paper's whole preamble across imports its journal formatting
    too. The CNA paper sets \\baselinestretch to 2 for double spaced
    submission, and nothing in the text the chapter keeps refers to it.
    """
    by_name: dict[str, str] = {}
    ordered: list[tuple[str | None, str]] = []
    for block in blocks:
        name = defined_name(block)
        ordered.append((name, block))
        if name:
            by_name[name] = block

    wanted = {f"\\{n}" for n in USED_NAME_RE.findall(body)} & set(by_name)
    changed = True
    while changed:
        changed = False
        for name in list(wanted):
            for used in USED_NAME_RE.findall(by_name[name]):
                cand = f"\\{used}"
                if cand in by_name and cand not in wanted:
                    wanted.add(cand)
                    changed = True

    keep, skipped = [], []
    for name, block in ordered:
        if name is None:
            if ALWAYS_CARRY.match(block):
                keep.append(block)
            else:
                skipped.append("an unnamed definition")
            continue
        if name not in wanted:
            skipped.append(name)
            continue
        # \newcommand refuses a name that already exists, and several of these
        # do: \K, \B and \laplace are taken by the kernel or by a package the
        # thesis loads. The definition would then be skipped and the paper's
        # meaning lost. Clearing the name first makes the definition win, and
        # because _macros.tex is read inside the importedpaper group the
        # clearing is local and the thesis keeps its own meaning afterwards.
        #
        # Only for \newcommand and \DeclareMathOperator. \renewcommand fails on
        # a name that does *not* exist, so clearing it first would break the
        # very definitions that need no clearing, and \def and \providecommand
        # never complain either way.
        if block.lstrip().startswith((r"\newcommand", r"\DeclareMathOperator")):
            keep.append(f"\\let{name}\\relax\n{block}")
        else:
            keep.append(block)
    if skipped:
        result.notes.append(
            f"left {len(skipped)} preamble definitions behind because the text "
            f"the chapter keeps does not use them: " + ", ".join(sorted(skipped)))
    return keep


PREAMBLE_INPUT_RE = re.compile(r"^[ \t]*\\input\s*\{([^}]*)\}", re.M)
NEWTHEOREM_RE = re.compile(
    r"^[ \t]*\\newtheorem\*?\s*\{([^}]*)\}(\[[^\]]*\])?\s*\{([^}]*)\}(\[[^\]]*\])?",
    re.M)


def inline_preamble_inputs(preamble: str, manifest: dict,
                           result: Result) -> str:
    """Pull \\input files into the preamble text before macros are read.

    Every paper written on a conference template keeps its notation in a
    separate file and says \\input{math_commands.tex} in the preamble. Reading
    only the preamble's own lines would miss all of it, and the body would come
    through with \\vg, \\mW and the rest undefined.
    """
    root = ROOT / manifest["dir"]
    seen: set[Path] = set()

    def expand(chunk: str, depth: int) -> str:
        if depth > 4:
            return chunk

        def one(m: re.Match) -> str:
            name = m.group(1).strip()
            path = root / (name if name.endswith(".tex") else name + ".tex")
            if not path.is_file() or path in seen:
                return ""
            seen.add(path)
            result.notes.append(f"inlined the preamble's \\input{{{name}}}")
            return expand(path.read_text(encoding="utf-8", errors="replace"),
                          depth + 1)

        return PREAMBLE_INPUT_RE.sub(one, chunk)

    return expand(preamble, 0)


def extract_preamble(text: str, manifest: dict, result: Result,
                     kept_body: str) -> str | None:
    """Carry the paper's own macro definitions across, and report its packages.

    The paper's preamble is dropped along with everything else outside the
    document body, but its \\newcommand definitions are used by the text we do
    keep. They are written to a file the importedpaper environment loads inside
    its group, so two papers can define the same macro name without clashing.

    Packages cannot be handled this way, because \\usepackage only works in a
    preamble. Those are reported so they can be added to main.tex by hand.
    """
    # The whole source file, not just the part before \begin{document}. The
    # ACU paper defines \T after it, and since the source file is dropped in
    # its entirety a definition there is lost just as surely as one in the
    # preamble. Carrying a definition twice is harmless, because each one is
    # preceded by a \let that clears the name.
    begin = BEGIN_DOC.search(text)
    preamble = inline_preamble_inputs(text, manifest, result)

    # Theorem environments are the thesis's, not the paper's. kaotheorems
    # already declares the usual set and styles them to match the document, and
    # re-declaring one in the body would clash the moment a second paper wants
    # the same name. Report them so a missing one is caught.
    missing = sorted({m.group(1).strip() for m in NEWTHEOREM_RE.finditer(preamble)}
                     - THESIS_THEOREMS)
    if missing:
        result.errors.append(
            "the paper declares theorem environments the thesis does not have: "
            + ", ".join(missing)
            + ". Add them to thesis_style.tex, since kaotheorems owns the rest.")

    wanted = []
    for m in USEPACKAGE_RE.finditer(preamble):
        for name in m.group(2).split(","):
            name = name.strip()
            if name and name not in PACKAGES_THESIS_HAS:
                wanted.append(name)
    if wanted:
        result.notes.append(
            "the paper's preamble loads packages the thesis may not: "
            + ", ".join(sorted(set(wanted)))
            + ". \\usepackage only works in a preamble, so add the ones the "
              "text actually needs to main.tex.")

    # Colours are declared wherever the paper felt like it, often in the first
    # body file rather than the preamble, and \definecolor obeys grouping. The
    # chapter's block would define them and the appendix block for the same
    # paper would not have them, so they are gathered from the whole paper and
    # carried unconditionally. Defining a colour twice is harmless.
    root = ROOT / manifest["dir"]
    colours: list[str] = []
    seen_colour: set[str] = set()
    for f in sorted(root.rglob("*.tex")):
        rel = str(f.relative_to(root))
        if any(rel.startswith(e[:-2]) if e.endswith("/**") else fnmatch.fnmatch(rel, e)
               for e in manifest.get("exclude", {})):
            continue
        for line in COLOUR_RE.findall(
                f.read_text(encoding="utf-8", errors="replace")):
            if line not in seen_colour:
                seen_colour.add(line)
                colours.append(line)
    if colours:
        result.notes.append(f"carried {len(colours)} colour definitions")

    blocks = []
    for m in MACRO_START.finditer(preamble):
        blocks.append(preamble[m.start():balanced_block(preamble, m.start())])
    blocks = needed_macros(blocks, kept_body, result) + colours
    if not blocks:
        return None

    # \DeclareMathOperator is amsmath's, and amsmath only allows it in a
    # preamble. This file is loaded from the document body, so rewrite it to
    # the \operatorname form it is defined as, which works anywhere.
    rewritten = 0
    for i, block in enumerate(blocks):
        new, n = DECLARE_OP_RE.subn(
            lambda mm: (f"\\newcommand*{{{mm.group(2)}}}"
                        f"{{\\operatorname{mm.group(1)}{{{mm.group(3)}}}}}"),
            block)
        blocks[i] = new
        rewritten += n
    if rewritten:
        result.notes.append(
            f"rewrote {rewritten} \\DeclareMathOperator into \\operatorname, "
            f"which amsmath allows outside a preamble")

    header = [
        "% " + "=" * 74,
        "% GENERATED by scripts/split_paper.py. Do not edit this file.",
        "%",
        f"% Macro definitions lifted from the preamble of",
        f"% {manifest['dir']}/{manifest['source']}, because the text this",
        "% chapter includes uses them and the preamble itself is not imported.",
        "%",
        "% \\begin{importedpaper} loads this inside its group, so the",
        "% definitions are scoped to the chapter and two papers may define the",
        "% same name.",
        "% " + "=" * 74,
        "",
    ]
    result.notes.append(f"carried {len(blocks)} macro definitions into {MACROS_FILE}")
    return "\n".join(header) + "\n\n".join(b.strip() for b in blocks) + "\n"


BIBITEM_RE = re.compile(r"\\bibitem(?:\[(?P<lbl>(?:[^\[\]]|\[[^\]]*\])*)\])?\{(?P<key>[^}]*)\}")
ASTRON_RE = re.compile(r"\\astroncite\s*\{(?P<who>[^}]*)\}\{(?P<year>[^}]*)\}")
NEWBLOCK_RE = re.compile(r"\\newblock\s*")
EM_RE = re.compile(r"\{\\em\s+(?P<v>[^}]*)\}")
THEBIB_FILE = "_thebibliography.bib"


def thebibliography_to_bib(text: str, manifest: dict, result: Result) -> str | None:
    """Turn an inline \\thebibliography into a .bib the merge can read.

    Journals often want the bibliography pasted into the manuscript, and the
    CNA paper arrived that way. The splitter strips it, because two
    bibliographies cannot coexist, and every one of its citations would then
    resolve to nothing. Each \\bibitem is converted instead, so the references
    survive the import and land in references/merged.bib like any other.

    The parse is deliberately shallow. A \\bibitem is formatted text, not data,
    so what comes out is the author, the year, the title and the journal where
    the usual layout makes them recognisable, and the whole original string in
    a note otherwise. Real entries should replace these at the next import.
    """
    m = THEBIB_RE.search(text)
    if not m:
        return None
    body = m.group(0)
    items = list(BIBITEM_RE.finditer(body))
    if not items:
        return None

    out = [
        "% " + "=" * 74,
        "% GENERATED by scripts/split_paper.py. Do not edit this file.",
        "%",
        f"% {manifest['dir']}/{manifest['source']} carries its bibliography",
        "% inline as \\bibitem entries rather than as a .bib. They are converted",
        "% here so that the paper's citations still resolve, and the fields are",
        "% only as good as a formatted reference string allows. Replacing these",
        "% with the real .bib is worth doing at the next import.",
        "% " + "=" * 74,
        "",
    ]
    for i, it in enumerate(items):
        stop = items[i + 1].start() if i + 1 < len(items) else len(body)
        raw = body[it.end():stop]
        raw = raw.replace("\\end{thebibliography}", "").strip()
        blocks = [b.strip().strip(".").strip() for b in NEWBLOCK_RE.split(raw) if b.strip()]
        who, year = "", ""
        a = ASTRON_RE.search(it.group("lbl") or "")
        if a:
            who, year = a.group("who").strip(), a.group("year").strip()
        title = blocks[1] if len(blocks) > 1 else ""
        journal = ""
        e = EM_RE.search(raw)
        if e:
            journal = e.group("v").strip()
        title = EM_RE.sub(r"\g<v>", title).strip().strip("{}").strip()
        # Every value is flattened to plain text. A \bibitem is formatted for
        # printing, not for parsing, and a single stray brace in any field
        # unbalances the file and costs the bib parser every entry after it.
        def flat(s: str) -> str:
            s = EM_RE.sub(r"\g<v>", s)
            s = re.sub(r"\\[a-zA-Z@]+\s*", " ", s)
            return " ".join(s.replace("{", "").replace("}", "").split())

        fields = [("author", flat(who)), ("title", flat(title)),
                  ("journal", flat(journal)), ("year", flat(year))]
        out.append(f"@article{{{it.group('key').strip()},")
        out += [f"  {k:8s} = {{{v}}}," for k, v in fields if v]
        # The note keeps the original string for a human to check against.
        # It has to be plain text: \newblock and {\em ...} survive otherwise,
        # and truncating a string that contains braces leaves them unbalanced,
        # which silently kills the rest of the file for the bib parser.
        plain = EM_RE.sub(r"\g<v>", raw)
        plain = NEWBLOCK_RE.sub(" ", plain)
        plain = re.sub(r"\\[a-zA-Z@]+\s*", " ", plain)
        plain = plain.replace("{", "").replace("}", "").replace("\\", "")
        plain = " ".join(plain.split())[:400]
        out.append(f"  note     = {{{plain}}}")
        out.append("}")
        out.append("")
    result.notes.append(
        f"converted {len(items)} inline \\bibitem entries into {THEBIB_FILE}")
    return "\n".join(out)


def extract_body(text: str, result: Result) -> str:
    """The document body, with anything that fights the thesis removed."""
    begin = BEGIN_DOC.search(text)
    end = END_DOC.search(text)
    if begin and end:
        body = text[begin.end():end.start()]
    else:
        body = text
        result.notes.append(
            "no \\begin{document} found, so the whole file was split")

    if THEBIB_RE.search(body):
        body = THEBIB_RE.sub("", body)
        result.removed.append(
            "the inline thebibliography, the thesis loads references/merged.bib")

    for pattern, why in STRIP_LINES:
        hits = pattern.findall(body)
        if hits:
            body = pattern.sub("", body)
            result.removed.append(f"{len(hits)} line(s): {why}")
    return body


def cut_into_parts(body: str, result: Result) -> list[Part]:
    sections = find_sections(body)
    if not sections:
        result.errors.append("no top level \\section found, nothing to split")
        return []

    # Where the appendix begins, so a part can say it is appendix material.
    hit = APPENDIX_RE.search(body)
    appendix_at = hit.start() if hit else len(body) + 1

    parts = [Part(0, FRONT_MATTER, body[:sections[0][0]], False)]
    for n, (start, title) in enumerate(sections, start=1):
        stop = sections[n][0] if n < len(sections) else len(body)
        parts.append(Part(n, title, body[start:stop], start > appendix_at))
    return parts


def render(part: Part, manifest: dict) -> str:
    header = [
        "% " + "=" * 74,
        f"% GENERATED by scripts/split_paper.py. Do not edit this file.",
        "%",
        f"% Source: {manifest['dir']}/{manifest['source']}",
        f"% Part {part.index}: {part.title}",
        "%",
        "% Edits belong upstream, in the published paper. To change what the",
        f"% chapter includes, change imports/{manifest['slug']}.toml and re-run",
        "% the splitter.",
        "% " + "=" * 74,
        "",
    ]
    # The thesis controls its own appendix, so the paper's switch goes.
    body = APPENDIX_RE.sub("", part.body)
    return "\n".join(header) + body.strip("\n") + "\n"


def usage_text(manifest: dict, keep: dict[str, str], monolithic: bool) -> str:
    """All the text a chapter would include, for deciding which macros it uses.

    A kept part often \\inputs a table, and that table uses the paper's macros
    too, so reading only the parts themselves would drop them as unused. For a
    sections paper there are no parts at all and every file the chapter could
    include has to be read instead.
    """
    root = ROOT / manifest["dir"]
    drop = manifest.get("drop", {})
    exclude = list(manifest.get("exclude", {}))
    chunks: list[str] = []
    seen: set[Path] = set()

    def follow(text: str, here: Path, depth: int) -> None:
        if depth > 4:
            return
        for name in ANY_INPUT_RE.findall(text):
            name = name.strip()
            cand = name if name.endswith(".tex") else name + ".tex"
            for base in (here, root):
                path = base / cand
                if path.is_file() and path not in seen:
                    seen.add(path)
                    body = path.read_text(encoding="utf-8", errors="replace")
                    chunks.append(body)
                    follow(body, path.parent, depth + 1)
                    break

    if monolithic:
        for body in keep.values():
            chunks.append(body)
            follow(body, root, 0)
    else:
        for path in sorted(root.rglob("*.tex")):
            rel = str(path.relative_to(root))
            if rel in drop or rel == manifest.get("source"):
                continue
            if any(rel.startswith(e[:-2]) if e.endswith("/**") else
                   fnmatch.fnmatch(rel, e) for e in exclude):
                continue
            chunks.append(path.read_text(encoding="utf-8", errors="replace"))
    return "\n".join(chunks)


def split_one(manifest: dict, write: bool) -> Result:
    slug = manifest["slug"]
    result = Result(slug=slug)
    source = ROOT / manifest["dir"] / manifest["source"]
    if not source.is_file():
        result.errors.append(f"source {manifest['source']} does not exist")
        return result

    drop = manifest.get("drop", {})
    appendix = manifest.get("appendix", {})
    text = source.read_text(encoding="utf-8")
    monolithic = manifest.get("layout") == "monolithic"

    out_dir = OUTPUT_ROOT / slug
    keep: dict[str, str] = {}

    body = extract_body(text, result) if monolithic else ""
    parts = cut_into_parts(body, result) if monolithic else []
    if monolithic and not parts:
        return result

    for part in parts:
        if part.title in drop:
            result.dropped.append((part.title, drop[part.title]))
            continue
        if part.title == FRONT_MATTER and not part.body.strip():
            continue
        if part.title == FRONT_MATTER:
            result.notes.append(
                "the front matter is not dropped in the manifest, so it was "
                "written out. It usually holds the title, authors and abstract, "
                'which the chapter replaces. Add "(front matter)" to [drop].')
        keep[part.filename] = render(part, manifest)
        if part.in_appendix:
            result.notes.append(
                f"{part.filename} comes after \\appendix in the source, so it "
                f"belongs in the thesis appendix rather than the chapter body")

    # Which preamble macros to carry across depends on what the kept parts
    # use, so this has to come after the parts are chosen.
    thebib = thebibliography_to_bib(text, manifest, result)
    if thebib:
        keep[THEBIB_FILE] = thebib

    macros = extract_preamble(text, manifest, result,
                              usage_text(manifest, keep, monolithic))
    if macros:
        keep[MACROS_FILE] = macros

    # Both extensions: the parts are .tex and a converted inline bibliography
    # is .bib, and globbing only .tex made --check report the .bib as new on
    # every run.
    existing = {p.name: p.read_text(encoding="utf-8")
                for p in out_dir.iterdir()
                if p.suffix in (".tex", ".bib")} if out_dir.is_dir() else {}

    for name, text in sorted(keep.items()):
        if existing.get(name) == text:
            result.unchanged.append(name)
        else:
            result.written.append(name)
            if write:
                out_dir.mkdir(parents=True, exist_ok=True)
                (out_dir / name).write_text(text, encoding="utf-8")

    for name in sorted(set(existing) - set(keep)):
        result.removed.append(f"stale part {name}")
        if write:
            (out_dir / name).unlink()

    # Every dropped title must really be a section of the paper. Only for a
    # monolithic paper: a sections paper drops files, and check_imports.py
    # validates those against the directory instead.
    titles = {p.title for p in parts}
    for title in ({**drop, **appendix} if monolithic else {}):
        if title not in titles:
            result.errors.append(
                f'[drop] names "{title}", which is not a section of '
                f"{manifest['source']} any more")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--paper", help="split only this slug")
    parser.add_argument("--check", action="store_true",
                        help="do not write, fail if the committed files differ")
    args = parser.parse_args()

    manifests = load_manifests(args.paper)
    if not manifests:
        print("no monolithic papers found in imports/", file=sys.stderr)
        return 1

    failed = False
    for manifest in manifests:
        result = split_one(manifest, write=not args.check)
        verb = "would write" if args.check else "wrote"
        print(f"{result.slug}: {verb} {len(result.written)}, "
              f"{len(result.unchanged)} unchanged, "
              f"{len(result.dropped)} dropped")
        for name in result.written:
            print(f"    {verb:12s} {name}")
        for title, why in result.dropped:
            print(f"    dropped      {title}  ({why})")
        for line in result.removed:
            print(f"    removed      {line}")
        for line in result.notes:
            print(f"    note         {line}")
        for line in result.errors:
            print(f"    ERROR        {line}")
        if result.errors:
            failed = True
        if args.check and result.written:
            print(f"    ERROR        {result.slug} is out of date, re-run "
                  f"scripts/split_paper.py and commit the result")
            failed = True

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
