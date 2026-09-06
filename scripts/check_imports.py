#!/usr/bin/env python3
"""Check that every imported paper is fully accounted for by its chapter.

The point of the manifests in imports/ is that a re import cannot silently
drop content. A published paper is vendored under imported_papers/ and never
edited, so the only record of what the thesis does with each of its files is
the chapter that includes them and the manifest that says why the rest are
left out. This script checks that record against what is actually on disk.

Run from the repository root:

    uv run --no-project python scripts/check_imports.py
    uv run --no-project python scripts/check_imports.py --paper acu

It fails when a re import adds a file nobody included, when a manifest names a
file that no longer exists, when a prune was not applied, and when a thesis
file would shadow one of the paper's own files.
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

# The six parts a paper backed chapter is made of, from CLAUDE.md section 4.3.
WRAPPER_PARTS = {
    "chapter heading": re.compile(r"\\chapter\{"),
    "chapter label": re.compile(r"\\label\{chap:"),
    "publication header box": re.compile(
        r"\\begin\{publicationbasis\}|Publication basis of this chapter"),
    "contribution statement": re.compile(
        r"\\contributionstatement\b|\\section\*?\{Contribution Statement\}"),
    "chapter introduction": re.compile(r"\\section\{Chapter Introduction\}"),
    "chapter summary": re.compile(r"\\section\{Chapter Summary\}"),
}

IMPORT_ENV = re.compile(r"\\begin\{importedpaper\}\{([^}]*)\}")
# \importsectionrotated is \importsection on a turned page, so it counts as
# an include for coverage exactly the same way.
IMPORT_SECTION = re.compile(r"\\importsection(?:rotated)?\{([^}]*)\}")
IMPORT_PART = re.compile(r"\\importpart\{([^}]*)\}")
# \subfile is the subfiles package's include. COGITAO uses it throughout, and
# its leaves carry no standalone preamble, so it behaves exactly like \input.
# thesis_import.sty aliases it to \input for the same reason.
INPUT_CMD = re.compile(r"(?<!\\)(?:\\input|\\include|\\subfile)\s*\{([^}]*)\}")
LABEL_CMD = re.compile(r"\\label\{([^}]*)\}")
# listings, algorithm2e and tcolorbox take the label as a key in the optional
# argument instead, so a file can define a label without ever writing \label.
KEYVAL_LABEL = re.compile(r"(?<![a-zA-Z\\])label\s*=\s*(?:\{([^}]*)\}|([\w:.\-]+))")


def labels_in(text: str) -> set[str]:
    """Every label a chunk of LaTeX defines, however it spells the definition."""
    found = set(LABEL_CMD.findall(text))
    for braced, bare in KEYVAL_LABEL.findall(text):
        name = (braced or bare).strip()
        if name:
            found.add(name)
    return found

# The splitter owns the definition of what a paper's sections are, so import
# it rather than writing a second regular expression that can disagree.
from split_paper import FRONT_MATTER, find_sections  # noqa: E402
GENERATED_ROOT = ROOT / "generated" / "imported"
# A paper's appendix material is included from here, not from its chapter.
APPENDIX_FILE = ROOT / "sections" / "appendix.tex"

# Thesis owned directories a paper's \input could accidentally resolve into.
# LaTeX searches the working directory before \input@path, so a thesis file
# with the same relative path as one a paper asks for would win.
THESIS_INPUT_ROOTS = ["sections", "appendices", "figures", "."]


@dataclass
class Manifest:
    path: Path
    data: dict
    slug: str
    dir: Path
    chapter: Path
    layout: str
    status: str

    drop: dict[str, str] = dc_field(default_factory=dict)
    exclude: dict[str, str] = dc_field(default_factory=dict)
    prune: dict[str, str] = dc_field(default_factory=dict)
    appendix: dict[str, str] = dc_field(default_factory=dict)


@dataclass
class Report:
    errors: list[str] = dc_field(default_factory=list)
    warnings: list[str] = dc_field(default_factory=list)
    notes: list[str] = dc_field(default_factory=list)


def load_manifests(only: str | None) -> list[Manifest]:
    manifests = []
    for path in sorted(MANIFEST_DIR.glob("*.toml")):
        with path.open("rb") as fh:
            data = tomllib.load(fh)
        if "dir" not in data:
            # Not a paper manifest. imports/glossary.toml, the ledger of thesis
            # wide terms from CLAUDE.md 3.9, lives in this directory too.
            continue
        slug = data.get("slug") or path.stem
        if only and slug != only:
            continue
        manifests.append(Manifest(
            path=path,
            data=data,
            slug=slug,
            dir=ROOT / data["dir"],
            chapter=ROOT / data["chapter"],
            layout=data.get("layout", "sections"),
            status=data.get("status", "pending"),
            drop=data.get("drop", {}),
            exclude=data.get("exclude", {}),
            prune=data.get("prune", {}),
            appendix=data.get("appendix", {}),
        ))
    return manifests


def matches_any(rel: str, patterns) -> bool:
    for pattern in patterns:
        if fnmatch.fnmatch(rel, pattern):
            return True
        # `dir/**` should also match `dir/a/b.tex`, which fnmatch does not do.
        if pattern.endswith("/**") and rel.startswith(pattern[:-2]):
            return True
    return False


def resolve_input(name: str, paper_dir: Path, here: Path | None = None) -> Path | None:
    """Resolve an \\input target the way the build will resolve it.

    `here` is the directory of the file doing the including. It is tried last,
    and it is what makes \\subfile work: the subfiles package resolves relative
    to the including file, so 3_generator/main.tex asking for motivation.tex
    means 3_generator/motivation.tex. thesis_import.sty tracks the same thing.
    """
    candidates = [name, f"{name}.tex"] if not name.endswith(".tex") else [name]
    bases = [ROOT, paper_dir] + ([here] if here else [])
    for candidate in candidates:
        # LaTeX looks in the working directory first, then in \input@path.
        for base in bases:
            probe = base / candidate
            if probe.is_file():
                return probe
    return None


def collect_reachable(start: Path, paper_dir: Path, report: Report) -> set[Path]:
    """Every file reached from `start` by following \\input, transitively."""
    seen: set[Path] = set()
    queue = [start]
    while queue:
        current = queue.pop()
        if current in seen or not current.is_file():
            continue
        seen.add(current)
        text = strip_comments(current.read_text(encoding="utf-8", errors="replace"))
        for target in INPUT_CMD.findall(text):
            target = target.strip()
            if not target:
                continue
            resolved = resolve_input(target, paper_dir, current.parent)
            if resolved is None:
                report.errors.append(
                    f"{current.relative_to(ROOT)} inputs `{target}`, which "
                    f"resolves to no file in the thesis or in the paper")
                continue
            queue.append(resolved)
    return seen


def strip_comments(text: str) -> str:
    out = []
    for line in text.splitlines():
        idx = 0
        while True:
            idx = line.find("%", idx)
            if idx == -1:
                out.append(line)
                break
            if idx > 0 and line[idx - 1] == "\\":
                idx += 1
                continue
            out.append(line[:idx])
            break
    return "\n".join(out)


def check_paths(m: Manifest, report: Report) -> None:
    if not m.dir.is_dir():
        report.errors.append(f"{m.slug}: directory {m.data['dir']} does not exist")
        return
    if not m.chapter.is_file():
        report.errors.append(f"{m.slug}: chapter {m.data['chapter']} does not exist")

    for name in m.data.get("bib", []):
        if not (m.dir / name).is_file():
            report.errors.append(f"{m.slug}: bib file {name} is missing from the paper")

    for name in m.data.get("graphics", []):
        if not (m.dir / name).is_dir():
            report.warnings.append(
                f"{m.slug}: graphics directory {name} does not exist in the paper")

    # A prune that still matches means the vendored copy was not pruned. This
    # does not break the build, since nothing loads these files, so it is a
    # warning. `--prune` applies it.
    for pattern in m.prune:
        stale = pruneable(m, pattern)
        if stale:
            report.warnings.append(
                f"{m.slug}: prune pattern `{pattern}` still matches "
                f"{', '.join(stale)}. Run with --prune to delete them.")


def pruneable(m: Manifest, pattern: str) -> list[str]:
    present = (str(p.relative_to(m.dir)) for p in m.dir.rglob("*") if p.is_file())
    return sorted(rel for rel in present if matches_any(rel, [pattern]))


def apply_prune(manifests: list[Manifest]) -> int:
    """Delete the files the manifests say should not be in the vendored copies."""
    removed = 0
    for m in manifests:
        if not m.dir.is_dir():
            continue
        for pattern in m.prune:
            for rel in pruneable(m, pattern):
                (m.dir / rel).unlink()
                print(f"  removed  {m.data['dir']}/{rel}")
                removed += 1
    return removed


def check_bib_registered(m: Manifest, report: Report) -> None:
    """Every bib named here must be an input to the bibliography merge."""
    merge = (ROOT / "scripts" / "merge_bib.py").read_text(encoding="utf-8")
    for name in m.data.get("bib", []):
        rel = f"{m.data['dir']}/{name}"
        if rel not in merge:
            report.errors.append(
                f"{m.slug}: {rel} is not in INPUT_FILES in scripts/merge_bib.py, "
                f"so its references are not in the thesis bibliography")


def check_shadowing(m: Manifest, report: Report) -> None:
    """No thesis file may sit where one of the paper's own files is expected.

    LaTeX searches the working directory before \\input@path, so if the thesis
    has sections/foo.tex and a paper asks for sections/foo, the thesis file
    wins and the paper silently loses a section.
    """
    # A monolithic paper's source is read by the splitter, not by LaTeX, so no
    # thesis file can shadow it.
    source = m.data.get("source") if m.layout == "monolithic" else None

    for path in m.dir.rglob("*.tex"):
        rel = str(path.relative_to(m.dir))
        # A dropped or excluded file is never included, so nothing can shadow it.
        if matches_any(rel, m.exclude) or rel in m.drop or rel == source:
            continue
        shadow = ROOT / rel
        if shadow.is_file() and shadow.resolve() != path.resolve():
            report.errors.append(
                f"{m.slug}: {rel} exists both in the paper and in the thesis "
                f"root, so an \\input of it inside the paper would pick up the "
                f"thesis file. Rename the thesis file.")


def check_coverage(m: Manifest, report: Report) -> None:
    """Every file in the paper is either included, dropped, or excluded."""
    chapter_text = strip_comments(m.chapter.read_text(encoding="utf-8"))

    env = IMPORT_ENV.search(chapter_text)
    if not env:
        report.notes.append(
            f"{m.slug}: the chapter has no importedpaper environment yet, so "
            f"coverage was not checked")
        return
    if env.group(1) != m.slug:
        report.errors.append(
            f"{m.slug}: the chapter opens importedpaper with slug "
            f"`{env.group(1)}`, which is not this paper's slug")

    for name, pattern in WRAPPER_PARTS.items():
        if not pattern.search(chapter_text):
            report.warnings.append(f"{m.slug}: the chapter has no {name}")

    reachable: set[Path] = set()
    # The thesis appendix is a second entry point: a paper's own appendix is
    # included from there rather than from its chapter, so a file reached only
    # from sections/appendix.tex still counts as covered.
    if APPENDIX_FILE.is_file():
        appendix_text = strip_comments(APPENDIX_FILE.read_text(encoding="utf-8"))
        for block in re.finditer(
                r"\\begin\{importedpaper\}\{" + re.escape(m.slug)
                + r"\}(.*?)\\end\{importedpaper\}", appendix_text, re.S):
            for target in IMPORT_SECTION.findall(block.group(1)):
                resolved = resolve_input(target.strip(), m.dir)
                if resolved is not None:
                    reachable |= collect_reachable(resolved, m.dir, report)

    for target in IMPORT_SECTION.findall(chapter_text):
        resolved = resolve_input(target.strip(), m.dir)
        if resolved is None:
            report.errors.append(
                f"{m.slug}: \\importsection{{{target}}} resolves to no file")
            continue
        reachable |= collect_reachable(resolved, m.dir, report)

    covered = {str(p.relative_to(m.dir)) for p in reachable
               if p.is_relative_to(m.dir)}

    for path in sorted(m.dir.rglob("*.tex")):
        rel = str(path.relative_to(m.dir))
        if rel in covered or rel in m.drop or matches_any(rel, m.exclude):
            continue
        report.errors.append(
            f"{m.slug}: {rel} is in the paper but the chapter does not include "
            f"it and the manifest does not say why. Add it to the chapter, or "
            f"add a [drop] entry with a reason.")

    for rel in m.drop:
        if not (m.dir / rel).exists():
            report.errors.append(
                f"{m.slug}: [drop] names {rel}, which is not in the paper any "
                f"more. The last import removed or renamed it.")
        elif rel in covered:
            report.errors.append(
                f"{m.slug}: {rel} is marked dropped but the chapter reaches it")


def check_monolithic(m: Manifest, report: Report) -> None:
    source = m.dir / m.data["source"]
    if not source.is_file():
        report.errors.append(f"{m.slug}: source {m.data['source']} does not exist")
        return
    titles = [t for _, t in find_sections(source.read_text(encoding="utf-8"))]
    for name in m.drop:
        if name == FRONT_MATTER:
            continue
        if name not in titles:
            report.errors.append(
                f"{m.slug}: [drop] names the section \"{name}\", which is not a "
                f"section of {m.data['source']} any more")

    # The split parts are generated and committed. They must exist, and the
    # chapter must include the ones that were not dropped.
    # Files starting with _ are not parts. _macros.tex carries the paper's own
    # preamble definitions and the importedpaper environment loads it itself.
    out_dir = GENERATED_ROOT / m.slug
    parts = sorted(p.stem for p in out_dir.glob("*.tex")
                   if not p.name.startswith("_")) if out_dir.is_dir() else []
    expected = len(titles) + 1 - len(m.drop)
    if len(parts) != expected:
        report.errors.append(
            f"{m.slug}: generated/imported/{m.slug}/ holds {len(parts)} parts "
            f"but the manifest implies {expected}. Re-run "
            f"scripts/split_paper.py and commit the result.")

    if m.status != "wired":
        report.notes.append(
            f"{m.slug}: monolithic, {len(titles)} sections, {len(m.drop)} "
            f"dropped, {len(parts)} parts generated. Status is pending, so the "
            f"chapter was not checked.")
        return

    chapter_text = strip_comments(m.chapter.read_text(encoding="utf-8"))
    included = set(IMPORT_PART.findall(chapter_text))
    for name in parts:
        if name not in included:
            report.errors.append(
                f"{m.slug}: generated part {name} is not included by the "
                f"chapter. Add \\importpart{{{name}}} or drop its section.")
    for name in sorted(included - set(parts)):
        report.errors.append(
            f"{m.slug}: the chapter includes \\importpart{{{name}}}, which is "
            f"not a generated part")


def check_balanced(m: Manifest, report: Report) -> None:
    """Every included file closes what it opens.

    An unclosed \\begin swallows everything after it and the output routine
    then spins on one page rather than failing, which is expensive to find by
    hand. COGITAO shipped one, an itemize left open in an appendix file, and it
    cost an afternoon before this check existed.
    """
    from collections import Counter
    comment = re.compile(r"(?<!\\)%.*")
    for path in sorted(m.dir.rglob("*.tex")):
        rel = str(path.relative_to(m.dir))
        if matches_any(rel, m.exclude) or rel in m.drop:
            continue
        text = comment.sub("", path.read_text(encoding="utf-8", errors="replace"))
        opened = Counter(re.findall(r"\\begin\{([^}]*)\}", text))
        closed = Counter(re.findall(r"\\end\{([^}]*)\}", text))
        for name in sorted(set(opened) | set(closed)):
            if name == "document" or opened[name] == closed[name]:
                continue
            report.errors.append(
                f"{m.slug}: {rel} opens {opened[name]} `{name}` and closes "
                f"{closed[name]}. An unbalanced environment swallows the rest "
                f"of the thesis. Fix it upstream, or drop the file.")


REF_CMD = re.compile(
    r"\\(?:c|C)?ref(?:range)?\*?\{([^}]*)\}|"
    r"\\(?:page|name|auto|eq)?ref\*?\{([^}]*)\}")


def kept_files(m: Manifest, report: Report) -> set[Path]:
    """The files a paper actually contributes, chapter and appendix together.

    A paper reaches the thesis through \\importsection, which names a file in
    the paper, and \\importpart, which names one the splitter wrote under
    generated/. Both are followed transitively, because a kept file may input
    another.
    """
    found: set[Path] = set()
    for entry in (m.chapter, APPENDIX_FILE):
        if not entry.is_file():
            continue
        text = strip_comments(entry.read_text(encoding="utf-8", errors="replace"))
        for block in re.finditer(
                r"\\begin\{importedpaper\}\{" + re.escape(m.slug)
                + r"\}(.*?)\\end\{importedpaper\}", text, re.S):
            body = block.group(1)
            for target in IMPORT_SECTION.findall(body):
                resolved = resolve_input(target.strip(), m.dir)
                if resolved is not None:
                    found |= collect_reachable(resolved, m.dir, report)
            for target in IMPORT_PART.findall(body):
                part = GENERATED_ROOT / m.slug / f"{target.strip()}.tex"
                if part.is_file():
                    found |= collect_reachable(part, m.dir, report)
    return found


def check_orphan_refs(m: Manifest, report: Report) -> None:
    """A kept file may not refer to a label only a dropped file defines.

    Dropping a paper's introduction is the normal case, because the thesis
    writes its own. The cost is invisible until the PDF is read: the body still
    says "see Figure 1", the label went with the introduction, and the reader
    gets ??. Both survey chapters lost their overview figure that way. The fix
    is to reproduce the float in the wrapper, inside the block and under the
    paper's own label, which is why the wrapper's own labels count as kept.
    """
    kept = kept_files(m, report)
    if not kept:
        return

    defined: set[str] = set()
    used: dict[str, str] = {}
    for path in sorted(kept):
        text = strip_comments(path.read_text(encoding="utf-8", errors="replace"))
        defined |= labels_in(text)
        rel = str(path.relative_to(ROOT))
        for group in REF_CMD.findall(text):
            for names in group:
                for name in names.split(","):
                    name = name.strip()
                    if name:
                        used.setdefault(name, rel)

    # Labels the wrapper defines inside the block are prefixed like the
    # paper's own, so they close exactly this gap.
    reproduced: set[str] = set()
    if m.chapter.is_file():
        chapter = strip_comments(m.chapter.read_text(encoding="utf-8"))
        for block in re.finditer(
                r"\\begin\{importedpaper\}\{" + re.escape(m.slug)
                + r"\}(.*?)\\end\{importedpaper\}", chapter, re.S):
            reproduced |= labels_in(block.group(1))
    defined |= reproduced

    # Where an orphan does live, so the message says what to restore. A file
    # the chapter drops is a candidate for restoring. An excluded tree is a
    # different variant of the same paper, so a label found only there means
    # the variant the thesis imports never had it.
    elsewhere: dict[str, str] = {}
    variant: dict[str, str] = {}
    for path in m.dir.rglob("*.tex"):
        if path in kept:
            continue
        rel = str(path.relative_to(m.dir))
        target = variant if matches_any(rel, m.exclude) else elsewhere
        for name in labels_in(
                strip_comments(path.read_text(encoding="utf-8", errors="replace"))):
            target.setdefault(name, rel)

    # A reproduced float is the one place thesis owned text copies published
    # text, so it is the one place a re import can silently go stale. Say so
    # every run rather than trusting anyone to remember.
    for name in sorted(reproduced & set(elsewhere)):
        report.notes.append(
            f"{m.slug}: the wrapper reproduces `{name}`, which the dropped "
            f"{elsewhere[name]} also defines. After a re import, check the "
            f"reproduction still matches the paper.")

    for name in sorted(set(used) - defined):
        where = used[name]
        if name in elsewhere:
            report.warnings.append(
                f"{m.slug}: {where} refers to `{name}`, which only "
                f"{elsewhere[name]} defines, and the chapter leaves that file "
                f"out. The reference prints ??. Reproduce the float or the "
                f"statement in the wrapper inside the block, under the same "
                f"label, or reword the sentence.")
        elif name in variant:
            report.warnings.append(
                f"{m.slug}: {where} refers to `{name}`, which exists only in "
                f"{variant[name]}, a variant of the paper the thesis does not "
                f"import. The reference prints ??. The imported variant lost "
                f"the target, so fix it upstream and re import.")
        else:
            report.warnings.append(
                f"{m.slug}: {where} refers to `{name}`, which no file in the "
                f"paper defines. The reference prints ??. This one is an "
                f"upstream bug, so fix it in the paper and re import.")


def check_label_collisions(manifests: list[Manifest], report: Report) -> None:
    """Two papers may share a label name only if both are label prefixed."""
    owners: dict[str, list[str]] = {}
    for m in manifests:
        if not m.dir.is_dir():
            continue
        names: set[str] = set()
        for path in m.dir.rglob("*.tex"):
            rel = str(path.relative_to(m.dir))
            if matches_any(rel, m.exclude):
                continue
            names |= labels_in(
                strip_comments(path.read_text(encoding="utf-8", errors="replace")))
        for name in names:
            owners.setdefault(name, []).append(m.slug)

    for name, slugs in sorted(owners.items()):
        if len(slugs) > 1:
            report.notes.append(
                f"label `{name}` is defined in {', '.join(sorted(slugs))}. "
                f"The importedpaper environment prefixes each with its slug, so "
                f"they do not collide.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--paper", help="check only this slug")
    parser.add_argument("--prune", action="store_true",
                        help="delete the files the manifests list under [prune]")
    args = parser.parse_args()

    manifests = load_manifests(args.paper)
    if not manifests:
        print("no manifests found in imports/", file=sys.stderr)
        return 1

    if args.prune:
        count = apply_prune(manifests)
        print(f"  removed {count} files")
        print()

    report = Report()
    for m in manifests:
        check_paths(m, report)
        if not m.dir.is_dir() or not m.chapter.is_file():
            continue
        check_bib_registered(m, report)
        check_shadowing(m, report)
        check_balanced(m, report)
        check_orphan_refs(m, report)
        if m.layout == "monolithic":
            check_monolithic(m, report)
        elif m.status == "wired":
            check_coverage(m, report)
        else:
            report.notes.append(
                f"{m.slug}: status is pending, so coverage was not checked")

    check_label_collisions(manifests, report)

    for line in report.notes:
        print(f"  note     {line}")
    for line in report.warnings:
        print(f"  warning  {line}")
    for line in report.errors:
        print(f"  ERROR    {line}")

    print()
    print(f"  {len(manifests)} papers, {len(report.errors)} errors, "
          f"{len(report.warnings)} warnings")
    return 1 if report.errors else 0


if __name__ == "__main__":
    sys.exit(main())
