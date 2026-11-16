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
    """Every overfull hbox from the last build, with the file it came from.

    pdflatex writes `(filename` when it opens a file and `)` when it closes
    one, so the file a warning belongs to is whatever is on top of that stack
    when the warning is printed. Nothing else in the log says where a box came
    from, and without it the only way to find one is to page through the PDF.
    """
    log = ROOT / "build-pass-3.log"
    if not log.is_file():
        return []
    # pdflatex hard wraps the log at 79 columns and inserts nothing at the
    # break, so a path can arrive in two pieces. Only a line of exactly 79
    # characters is a continuation, and joining any other pair would glue the
    # next message onto the end of a filename and hide it.
    lines = log.read_text(encoding="utf-8", errors="replace").split("\n")
    joined, buf = [], ""
    for line in lines:
        buf += line
        if len(line) != 79:
            joined.append(buf)
            buf = ""
    if buf:
        joined.append(buf)

    box = re.compile(r"^(Over|Under)full \\[hv]box \(([\d.]+)pt")
    paren = re.compile(r"\(([^\s()]*)|(\))")
    stack, found, echoing, page = [], [], False, 0
    for line in joined:
        m = box.match(line)
        if m:
            # TeX echoes the offending material on the lines that follow, and
            # that text has parens of its own. Counting them unwinds the file
            # stack and loses the attribution for everything after.
            echoing = True
            if m.group(1) == "Over" and "\\hbox" in line:
                name = next((f for f in reversed(stack) if f), None)
                found.append((float(m.group(2)), name or "?", page + 1))
            continue
        if echoing:
            if line.strip():
                continue
            echoing = False
        # pdflatex prints [N] as it ships each page out. Counting the markers
        # rather than reading N gives the page index in the PDF, which is what
        # you need to open it: N is the printed number and the front matter
        # makes the two differ by thirty odd pages.
        page += len(re.findall(r"\[\d+", line))
        for opened, closed in paren.findall(line):
            if closed:
                if stack:
                    stack.pop()
            else:
                stack.append(
                    opened if re.search(r"\.(tex|sty|cls)$", opened) else None)
    return sorted(found, reverse=True)


def report_margins() -> int:
    """How full the margin column gets, and where.

    The margin carries float captions, the margin table of contents and the
    side citations, and none of those three knows about the others. The
    marginnote package overprints rather than relocating, so a column that is
    too full is silent: nothing appears in the log and the only way to see it
    is to measure the output. This reports the fullest columns so the densest
    page can be looked at, and flags any margin material that has run past the
    foot of the paper.

    The x bands are kaobook's: on a recto page the margin is to the right of
    the text block, on a verso page it is to the left, so the band alternates.
    Rotated pages are skipped, because their bounding boxes are in unrotated
    coordinates and the bands mean nothing there.
    """
    pdf = ROOT / "main.pdf"
    if not pdf.is_file():
        print("  no main.pdf, run ./build.sh first")
        return 1
    tool = shutil.which("pdftotext") or "/opt/homebrew/bin/pdftotext"
    out = ROOT / "build" / "bbox.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([tool, "-bbox", str(pdf), str(out)], capture_output=True)
    text = out.read_text(encoding="utf-8", errors="replace")
    out.unlink(missing_ok=True)

    page = re.compile(r'<page width="([\d.]+)" height="([\d.]+)">(.*?)</page>',
                      re.S)
    word = re.compile(r'<word xMin="([\d.]+)" yMin="([\d.]+)"'
                      r' xMax="([\d.]+)" yMax="([\d.]+)">')
    rows, spilt, wide = [], [], 0
    for n, (_, height, body) in enumerate(page.findall(text), 1):
        lo, hi = (392.0, 530.0) if n % 2 else (65.0, 208.0)
        words = word.findall(body)
        # The table of contents and the two float lists are set across the
        # text block and the margin together, so on those pages the band below
        # is type and not margin material. A page like that has words in the
        # gutter that separates the two on every other page, which is what
        # \marginparsep is, and no ordinary page has anything there.
        # The band is narrowed at both ends, because a word's box can overhang
        # the measure by a point or two, and three words are required, so that
        # one stray box does not condemn a page.
        gutter = (379.0, 388.0) if n % 2 else (209.0, 218.0)
        if sum(1 for x0, _a, _x1, _b in words
               if gutter[0] < float(x0) < gutter[1]) >= 3:
            wide += 1
            continue
        boxes = [(float(a), float(b)) for x0, a, _x1, b in words
                 if lo <= float(x0) <= hi]
        if not boxes:
            continue
        rows.append((len(boxes), n))
        bottom = max(b for _, b in boxes)
        if bottom > float(height) - 30:
            spilt.append((n, round(bottom)))

    rows.sort(reverse=True)
    print(f"  {len(rows)} pages carry margin material, "
          f"{wide} wide pages skipped\n")
    print("  fullest margin columns, words in the column")
    for count, n in rows[:10]:
        print(f"    p{n:<5d} {count:4d} words")
    print()
    if spilt:
        print("  margin material within 30pt of the foot of the paper")
        for n, bottom in spilt:
            print(f"    p{n:<5d} reaches {bottom}pt of 842")
    else:
        print("  no margin material within 30pt of the foot of the paper")
    print("\n  Rotated pages are skipped. Open the fullest pages and look:\n"
          "  the marginnote package overprints instead of relocating, so an\n"
          "  overfull column is not reported anywhere else.")
    return 0


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
    parser.add_argument("--margins", action="store_true",
                        help="how full the margin column gets, and where")
    args = parser.parse_args()

    if args.pdf:
        return report_pdf()

    if args.margins:
        return report_margins()

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
        if any(ROOT.glob("build-pass-*.log")):
            print("  no overfull hboxes in the last build")
        else:
            print("  no build log, run ./build.sh first")
        return 0
    widths = [w for w, _, _ in ov]
    print(f"  {len(ov)} overfull hboxes in the last build")
    print(f"    over 100pt {sum(1 for o in widths if o > 100):4d}")
    print(f"    over  30pt {sum(1 for o in widths if o > 30):4d}")

    worst: dict[str, list[tuple[float, int]]] = {}
    for width, where, page in ov:
        worst.setdefault(where, []).append((width, page))
    print("\n  worst offenders by file, with the PDF page of the worst one")
    for where, hits in sorted(
            worst.items(), key=lambda kv: max(kv[1])[0], reverse=True)[:12]:
        top, page = max(hits)
        print(f"    {round(top):4d}pt  x{len(hits):<3d} p{page:<4d} "
              f"{where.lstrip('./')}")
    print("\n  A tabular that adjustbox shrinks still reports its unscaled\n"
          "  width, so check the page before treating one of these as real.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
