#!/usr/bin/env python3
"""Convert an imported paper's EPS figures to PDF, for pdflatex.

pdflatex cannot place an EPS. graphicx knows this and asks epstopdf to convert
on the fly, which needs shell escape and a ghostscript on the path. Overleaf
may have neither, and the thesis build is supposed to work there with nothing
but LaTeX, so the conversion happens here instead and the result is committed.

The converted file keeps the name the paper asks for, which matters: the CNA
paper ships PDF versions of its figures already, but under a different
basename, so \\includegraphics{NECO-...-Figure.1} finds neither the .eps it can
read nor the .pdf it cannot name.

Output goes to generated/imported/<slug>/figures/, which
thesis_import.sty puts first on \\graphicspath, so the converted file wins over
the .eps beside it. The paper itself is never touched.

    uv run --no-project python scripts/convert_eps.py
    uv run --no-project python scripts/convert_eps.py --check
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_ROOT = ROOT / "generated" / "imported"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_imports import load_manifests, matches_any  # noqa: E402


def ghostscript() -> str | None:
    for name in ("gs", "gswin64c"):
        found = shutil.which(name)
        if found:
            return found
    return None


def convert(src: Path, dst: Path, gs: str) -> bool:
    dst.parent.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run(
        [gs, "-q", "-dNOPAUSE", "-dBATCH", "-dSAFER", "-dEPSCrop",
         "-sDEVICE=pdfwrite", f"-sOutputFile={dst}", str(src)],
        capture_output=True, text=True, errors="replace")
    return proc.returncode == 0 and dst.is_file()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--paper", help="convert only this slug")
    parser.add_argument("--check", action="store_true",
                        help="do not convert, fail if anything is missing")
    args = parser.parse_args()

    gs = ghostscript()
    todo: list[tuple[Path, Path, str]] = []
    for m in load_manifests(args.paper):
        if not m.dir.is_dir():
            continue
        for src in sorted(m.dir.rglob("*.eps")):
            rel = str(src.relative_to(m.dir))
            if matches_any(rel, m.exclude):
                continue
            dst = OUTPUT_ROOT / m.slug / "figures" / (src.stem + ".pdf")
            if dst.is_file() and dst.stat().st_mtime >= src.stat().st_mtime:
                continue
            todo.append((src, dst, m.slug))

    if not todo:
        print("  every EPS figure already has a converted PDF")
        return 0

    if args.check:
        for src, _, slug in todo:
            print(f"  MISSING  {slug}: {src.relative_to(ROOT)}")
        print(f"\n  {len(todo)} figures need converting, run without --check")
        return 1

    if gs is None:
        print("  ghostscript not found, cannot convert. Install it, or commit "
              "the converted PDFs from a machine that has it.", file=sys.stderr)
        return 1

    failed = 0
    for src, dst, slug in todo:
        if convert(src, dst, gs):
            print(f"  {slug}: {src.name} -> {dst.relative_to(ROOT)}")
        else:
            print(f"  ERROR {slug}: could not convert {src.relative_to(ROOT)}")
            failed += 1

    print(f"\n  {len(todo) - failed} converted, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
