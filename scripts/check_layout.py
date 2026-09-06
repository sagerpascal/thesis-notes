#!/usr/bin/env python3
"""Report how uniformly the imported papers are formatted.

Nine papers written for nine templates do not agree about anything: which
citation command to use, whether a table caption goes above or below, how wide
a table may be. Most of that is settled from outside, in thesis_import.sty and
thesis_style.tex, but only if somebody looks. This is the looking.

It reports per paper and never changes anything:

  citations   which commands each paper uses, so a paper that cites unlike the
              rest is visible. Under kaobiblio's numeric style \\cite, \\citep
              and \\parencite all render the same, so a spread here is only
              worth acting on if the bibliography style changes.
  captions    whether the caption comes before or after the content of each
              float. Tables conventionally take it above and figures below.
              kaobook sets captions in the margin, so this rarely shows in the
              output, but a paper that disagrees with itself is worth knowing.
  floats      how many figures and tables each paper contributes.
  overfull    boxes from the last build, worst first. A tabular that adjustbox
              later shrinks still reports its unscaled width, so a warning here
              does not mean the output overflows. Check the page before acting.

    uv run --no-project python scripts/check_layout.py
    uv run --no-project python scripts/check_layout.py --overfull
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_imports import load_manifests, matches_any, strip_comments  # noqa: E402

CITE = re.compile(
    r"\\(citepeg|citeauthor|citeyear|citealp|citealt|parencite|textcite"
    r"|autocite|footcite|sidecite|citep|citet|cite)\b")
FLOAT = re.compile(r"\\begin\{(figure|table)\*?\}(.*?)\\end\{\1\*?\}", re.S)
CONTENT = ("\\includegraphics", "\\begin{tabular", "\\resizebox",
           "\\begin{tabularx", "\\input", "\\subfile")


def survey(m, report_rows):
    cites = Counter()
    floats = Counter()
    caption_before = Counter()
    caption_after = Counter()
    for f in sorted(m.dir.rglob("*.tex")):
        rel = str(f.relative_to(m.dir))
        if matches_any(rel, m.exclude) or rel in m.drop:
            continue
        text = strip_comments(f.read_text(encoding="utf-8", errors="replace"))
        for name in CITE.findall(text):
            cites[name] += 1
        for kind, body in FLOAT.findall(text):
            floats[kind] += 1
            cap = body.find("\\caption")
            pos = [body.find(c) for c in CONTENT]
            first = min([p for p in pos if p >= 0], default=-1)
            if cap < 0 or first < 0:
                continue
            (caption_before if cap < first else caption_after)[kind] += 1
    report_rows.append((m.slug, cites, floats, caption_before, caption_after))


def overfull_from_log():
    log = ROOT / "build-pass-3.log"
    if not log.is_file():
        return []
    text = log.read_text(encoding="utf-8", errors="replace")
    return sorted((float(x) for x in re.findall(
        r"Overfull \\hbox \(([\d.]+)pt too wide", text)), reverse=True)


def report_pdf() -> int:
    """Every ?? in the built PDF, which is the only place they are all visible.

    The build log counts each undefined reference once. The PDF prints one ??
    per use, and a label used eight times is eight holes in the text, so the
    log understates the damage. This reads the output instead.
    """
    pdf = ROOT / "main.pdf"
    if not pdf.is_file():
        print("  no main.pdf, run ./build.sh first")
        return 1
    for tool in ("/opt/homebrew/bin/pdftotext", "pdftotext"):
        if shutil.which(tool) or Path(tool).is_file():
            break
    else:
        print("  pdftotext not found, install poppler")
        return 1
    out = ROOT / "build" / "pdftext.txt"
    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([tool, "-layout", str(pdf), str(out)], capture_output=True)
    pages = out.read_text(encoding="utf-8", errors="replace").split("\f")

    hits = []
    for n, page in enumerate(pages, 1):
        for m in re.finditer(r"\?\?", page):
            lo = max(0, m.start() - 70)
            hits.append((n, " ".join(page[lo:m.end() + 30].split())))
    print(f"  {len(hits)} occurrences of ?? on "
          f"{len({h[0] for h in hits})} pages\n")
    for n, ctx in hits:
        print(f"  p{n:<5d} ...{ctx}")
    if hits:
        print("\n  Each one is a \\ref, \\Cref or \\eqref whose label does not\n"
              "  exist. Either the label is in a file the chapter drops, or the\n"
              "  sentence points at something the thesis has renamed.")
    out.unlink(missing_ok=True)
    return 1 if hits else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--overfull", action="store_true",
                        help="only the overfull box summary")
    parser.add_argument("--pdf", action="store_true",
                        help="find every ?? in the built PDF, with its page")
    args = parser.parse_args()

    if args.pdf:
        return report_pdf()

    if not args.overfull:
        rows = []
        for m in load_manifests(None):
            if m.dir.is_dir():
                survey(m, rows)

        print(f"  {'paper':11s} {'citation commands used':38s} "
              f"{'figs':>5s} {'tabs':>5s}  caption above/below")
        for slug, cites, floats, before, after in rows:
            used = ", ".join(f"{k}:{v}" for k, v in cites.most_common(4))
            print(f"  {slug:11s} {used:38s} {floats['figure']:5d} "
                  f"{floats['table']:5d}  "
                  f"tab {before['table']}/{after['table']}  "
                  f"fig {before['figure']}/{after['figure']}")

        odd = [s for s, _, fl, b, a in rows
               if fl["table"] and a["table"] > b["table"]]
        if odd:
            print("\n  captions below their table, against the convention the "
                  "other papers follow: " + ", ".join(odd))
        print()

    ov = overfull_from_log()
    if not ov:
        print("  no build log, run ./build.sh first")
        return 0
    print(f"  {len(ov)} overfull hboxes in the last build")
    print(f"    over 100pt {sum(1 for o in ov if o > 100):4d}")
    print(f"    over  30pt {sum(1 for o in ov if o > 30):4d}")
    print(f"    worst      {', '.join(str(round(o)) for o in ov[:6])}")
    print("\n  A tabular that adjustbox shrinks still reports its unscaled\n"
          "  width, so check the page before treating one of these as real.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
