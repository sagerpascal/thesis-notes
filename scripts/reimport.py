#!/usr/bin/env python3
"""Replace a vendored paper with a fresh copy, then rebuild what depends on it.

Three of the papers are still moving, so this will be run repeatedly. Doing it
by hand invites two mistakes: copying a whole project repository when only its
paper directory belongs here, and forgetting one of the steps that has to
follow. This does the whole thing and then tells you what changed.

    uv run --no-project python scripts/reimport.py grokking ~/code/dfc-ttt/docs/paper
    uv run --no-project python scripts/reimport.py --dry-run bounded ~/papers/koopman

The source directory is copied wholesale, the manifest's [prune] patterns are
applied to the copy, and then the splitter, the figure converter, the
bibliography merge and the checker all run. Nothing is edited inside
imported_papers/: pruning only deletes, which is the one exception the import
contract allows.

Record the source path in the manifest's `upstream` field so the next person
does not have to guess it.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_imports import load_manifests  # noqa: E402

FOLLOW_UP = [
    (["scripts/split_paper.py"], "splitting the monolithic papers"),
    (["scripts/convert_eps.py"], "converting EPS figures"),
    (["scripts/merge_bib.py"], "merging the bibliographies"),
    (["scripts/check_imports.py"], "checking the imports"),
    (["scripts/check_compile.py"], "compiling every paper's body"),
]

# Never copied in, whatever the source directory holds. These are the marks of
# a project repository rather than a paper.
NEVER_COPY = {
    ".git", ".github", ".venv", "__pycache__", ".pytest_cache", ".idea",
    "node_modules", ".DS_Store", "uv.lock", ".ruff_cache",
}


def run(cmd: list[str]) -> int:
    proc = subprocess.run([sys.executable] + cmd, cwd=ROOT)
    return proc.returncode


def ignore(_dir: str, names: list[str]) -> set[str]:
    return {n for n in names if n in NEVER_COPY}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("slug", help="the paper to replace")
    parser.add_argument("source", type=Path,
                        help="directory holding the paper, copied wholesale")
    parser.add_argument("--dry-run", action="store_true",
                        help="say what would happen and stop")
    args = parser.parse_args()

    manifests = {m.slug: m for m in load_manifests(None)}
    if args.slug not in manifests:
        print(f"no manifest for `{args.slug}`. Known: "
              f"{', '.join(sorted(manifests))}", file=sys.stderr)
        return 1
    m = manifests[args.slug]

    source = args.source.expanduser().resolve()
    if not source.is_dir():
        print(f"source {source} is not a directory", file=sys.stderr)
        return 1
    if (source / ".git").exists() or (source / "pyproject.toml").exists():
        print(f"  warning: {source} looks like a project repository, not a "
              f"paper directory. Point this at the directory holding the .tex.")

    target = m.dir
    print(f"  {args.slug}: {source}")
    print(f"        -> {target.relative_to(ROOT)}")
    if args.dry_run:
        print("\n  dry run, nothing copied")
        return 0

    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(source, target, ignore=ignore)
    print(f"  copied {sum(1 for _ in target.rglob('*') if _.is_file())} files")

    failed = []
    print()
    if run(["scripts/check_imports.py", "--prune", "--paper", args.slug]):
        pass  # prune reports through the checker below
    for cmd, what in FOLLOW_UP:
        print(f"\n  --- {what}")
        if run(cmd):
            failed.append(what)

    print()
    if failed:
        print("  needs attention: " + "; ".join(failed))
        print("  A re import that changes the paper's structure is supposed to "
              "fail here. Read what it says and update imports/"
              f"{args.slug}.toml to match.")
        return 1
    print(f"  {args.slug} re imported, everything downstream is clean")
    print(f"  Set imported_on and upstream in imports/{args.slug}.toml.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
