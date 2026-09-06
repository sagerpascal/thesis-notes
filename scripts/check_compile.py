#!/usr/bin/env python3
"""Compile every imported paper's body and report what breaks, per paper.

A chapter wrapper carries the thesis's own framing, so it cannot be written
until the story is settled. The imported bodies, though, either compile or they
do not, and that is independent of the story. This script builds a throwaway
document from main.tex's preamble plus every paper's includable content, runs
pdflatex over it, and attributes each error to the paper it came from.

It is a development tool. It writes nothing that the thesis build depends on,
and Overleaf never runs it.

Run from the repository root:

    uv run --no-project python scripts/check_compile.py
    uv run --no-project python scripts/check_compile.py --paper grokking
    uv run --no-project python scripts/check_compile.py --keep

The commonest failures it catches are a macro the paper's preamble defined and
the splitter did not carry across, and a package the paper needs that main.tex
does not load.
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUILD_DIR = ROOT / "build" / "compilecheck"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_imports import (  # noqa: E402
    Manifest, Report, collect_reachable, load_manifests, matches_any,
    strip_comments,
)

TEXBIN = Path("/usr/local/texlive/2025/bin/universal-darwin/pdflatex")
ERROR_LINE = re.compile(r"^(?:\./)?(\S+?\.tex):(\d+): (.*)$", re.M)
BANG_LINE = re.compile(r"^! (.*)$", re.M)
UNDEFINED_CS = re.compile(r"^! Undefined control sequence\.$\n^.*$\n^(.*)$", re.M)


def pdflatex() -> str:
    return str(TEXBIN) if TEXBIN.exists() else "pdflatex"


def top_level_files(m: Manifest, report: Report) -> list[str]:
    """The files a chapter would include: those nothing else already reaches.

    A sections paper is a tree. Including every file would include the leaves
    twice, once on their own and once through the parent that inputs them, so
    only the roots of that tree belong in a chapter.
    """
    candidates = []
    for path in sorted(m.dir.rglob("*.tex")):
        rel = str(path.relative_to(m.dir))
        if rel in m.drop or matches_any(rel, m.exclude):
            continue
        candidates.append(path)

    reached: set[Path] = set()
    for path in candidates:
        for other in collect_reachable(path, m.dir, report):
            if other != path:
                reached.add(other)
    return [str(p.relative_to(m.dir)) for p in candidates if p not in reached]


def body_for(m: Manifest, report: Report) -> tuple[str, list[str]]:
    lines = [f"\\chapter{{Compile check: {m.slug}}}",
             f"\\begin{{importedpaper}}{{{m.slug}}}"]
    included: list[str] = []
    if m.layout == "monolithic":
        out = ROOT / "generated" / "imported" / m.slug
        for part in sorted(out.glob("*.tex")):
            if part.name.startswith("_"):
                continue
            lines.append(f"\\importpart{{{part.stem}}}")
            included.append(part.stem)
    else:
        for rel in top_level_files(m, report):
            lines.append(f"\\importsection{{{rel}}}")
            included.append(rel)
    lines.append("\\end{importedpaper}")
    return "\n".join(lines), included


def build_document(manifests: list[Manifest], report: Report) -> str:
    preamble = (ROOT / "main.tex").read_text(encoding="utf-8")
    preamble = preamble.split("\\begin{document}")[0]
    bodies = [body_for(m, report)[0] for m in manifests]
    return (preamble + "\\begin{document}\n\\mainmatter\n"
            + "\n\n".join(bodies) + "\n\\end{document}\n")


def attribute(log: str, manifests: list[Manifest]) -> dict[str, list[str]]:
    """Group each reported problem under the paper whose file it came from."""
    owners = {m.slug: str(Path(m.data["dir"])) for m in manifests}
    found: dict[str, list[str]] = defaultdict(list)

    for path, line, message in ERROR_LINE.findall(log):
        if "Warning" in message or "Overfull" in message or "Underfull" in message:
            continue
        slug = "thesis"
        for name, d in owners.items():
            if d in path or f"imported/{name}/" in path:
                slug = name
                break
        found[slug].append(f"{path}:{line}: {message.strip()}")

    # Undefined control sequences report the offending macro on the line after
    # the message, and often carry no file name at all.
    for tail in UNDEFINED_CS.findall(log):
        macro = re.findall(r"(\\[A-Za-z@]+)\s*$", tail)
        if macro:
            found["undefined macros"].append(macro[-1])
    return found


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--paper", help="check only this slug")
    parser.add_argument("--keep", action="store_true",
                        help="leave the generated document and log in place")
    args = parser.parse_args()

    manifests = [m for m in load_manifests(args.paper) if m.dir.is_dir()]
    if not manifests:
        print("no papers to check", file=sys.stderr)
        return 1

    report = Report()
    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    doc = build_document(manifests, report)
    # The document must live at the repository root, because every path in it,
    # and in main.tex's preamble, is relative to it.
    test_tex = ROOT / "_compilecheck.tex"
    test_tex.write_text(doc, encoding="utf-8")

    for m in manifests:
        _, included = body_for(m, report)
        print(f"  {m.slug:12s} {len(included)} files")

    # pdflatex wraps its log at 79 columns by default, which cuts long paths
    # and error messages in half and makes them impossible to attribute.
    # error_line and half_error_line have a hard ceiling around 254 in TeX and
    # setting them higher makes it refuse to start, so only the log width moves.
    env = dict(os.environ, max_print_line="10000", error_line="254",
               half_error_line="238")
    subprocess.run(
        [pdflatex(), "-interaction=nonstopmode", "-file-line-error",
         "-output-directory", str(BUILD_DIR), str(test_tex.name)],
        cwd=ROOT, capture_output=True, text=True, errors="replace", env=env)
    log = (BUILD_DIR / "_compilecheck.log").read_text(encoding="utf-8",
                                                      errors="replace")

    problems = attribute(log, manifests)
    # With -file-line-error the errors are `path:line: message`, so the
    # bare `! message` form only shows up for a few kernel errors.
    total = sum(len(v) for k, v in problems.items() if k != 'undefined macros')
    total = max(total, len(BANG_LINE.findall(log)))

    print()
    if not problems:
        print("  clean, no errors attributed to any paper")
    for slug in sorted(problems):
        items = problems[slug]
        uniq = sorted(set(items))
        print(f"  {slug}: {len(items)} problems, {len(uniq)} distinct")
        for line in uniq[:12]:
            print(f"      {line}")
        if len(uniq) > 12:
            print(f"      ... and {len(uniq) - 12} more")

    for line in report.errors:
        print(f"  ERROR  {line}")

    if not args.keep:
        test_tex.unlink(missing_ok=True)
        shutil.rmtree(BUILD_DIR, ignore_errors=True)
    else:
        print(f"\n  kept {test_tex.relative_to(ROOT)} and {BUILD_DIR}")

    print(f"\n  {total} LaTeX errors over {len(manifests)} papers")
    return 1 if total or report.errors else 0


if __name__ == "__main__":
    sys.exit(main())
