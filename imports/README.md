# Import manifests

One TOML file per published paper. Each one records what the thesis does with
that paper: which of its files the chapter includes, which it deliberately
leaves out and why, and which were deleted from the vendored copy.

The manifests live here rather than inside `imported_papers/` because that tree
is a read only vendor drop. A re import replaces a paper's directory wholesale,
and nothing written by us may be lost when it does.

Check them with:

```bash
uv run --no-project python scripts/check_imports.py
```

## Why this exists

Selection, not deletion. The published papers keep their abstract, their
introduction and their conclusion, and the thesis chapter simply does not
include those files. Deleting them from the vendored copy would have to be
redone by hand after every import, and it would quietly change the thing the
thesis claims to reproduce.

The manifest is what makes the selection auditable. A re import that adds a
section fails the check instead of silently dropping content.

## Fields

| Field | Meaning |
| --- | --- |
| `slug` | Short name for the paper. Also the label prefix, so the paper's `fig:overview` becomes `acu:fig:overview`. Must match the `\DeclareImportedPaper` call in `main.tex`. |
| `dir` | The paper's root, relative to the repository root. This is the directory its own `\input` paths are relative to, which for the self attention project is the project directory rather than the `ICML2025` subdirectory. |
| `chapter` | The thesis owned chapter file that includes this paper. |
| `title` | Human readable name, used in reports. |
| `citation_key` | The paper's own key in `references/merged.bib`, cited by the chapter's publication header box. |
| `status` | `wired` once the chapter includes the paper, `pending` before that, `summarised` when the thesis gives the paper a prose summary instead of reproducing it. Coverage is only checked for `wired` papers. |
| `summary_reason` | Required when `status` is `summarised`. Why the paper is summarised rather than reproduced, usually the author's role or the paper's distance from the argument. The checker prints it on every run. |
| `layout` | `sections` when the paper is already split into files, `monolithic` when it is one file. |
| `source` | Monolithic only. The root file of the paper. The preamble is read from here, and so are the sections unless `body` says otherwise. |
| `body` | Monolithic only, optional. The file or files the sections are in, when the root file holds only the preamble and a few `\input` lines. A list is cut as if it were one file, which is how the Frontiers supplement becomes the paper's appendix parts. |
| `split` | Monolithic only. Where to cut. `section` cuts at every top level `\section`. |
| `imported_on` | Date of the last import. |
| `upstream` | Where the paper was imported from. |
| `bib` | Bibliographies, relative to `dir`. Each must also appear in `INPUT_FILES` in `scripts/merge_bib.py`, which the checker enforces. |
| `graphics` | Figure subdirectories, relative to `dir`. The paper root is always searched, so it does not need listing. Must match the third argument of `\DeclareImportedPaper`. |

## Tables

`[drop]` names parts of the paper the chapter deliberately does not include,
each with a reason. For a `sections` paper the keys are file paths relative to
`dir`. For a `monolithic` paper they are section titles exactly as they appear
in `\section{...}`, plus the reserved key `"(front matter)"` for everything
before the first section, which is where the title, authors and abstract live.
The checker fails if a dropped file or section no longer exists, which is how a
rename during a re import gets caught.

`[exclude]` names whole trees that are not part of this import at all, as glob
patterns. The self attention project ships a rebuttal and an arXiv variant
alongside the paper, and neither is built. Excluded files are not checked for
coverage or for shadowing.

`[prune]` names files deleted from the vendored copy because the thesis never
loads them: publisher class files, bibliography styles, template PDFs and
superseded drafts. The checker warns while any of them is still present, and
`--prune` deletes them. Keeping the list means the next import can be pruned
the same way without anyone having to remember.

## Summarising a paper instead of reproducing it

A paper the thesis cites and credits but does not reproduce is marked
`status = "summarised"`, with a `summary_reason`, and its `chapter` points at
the thesis owned file that carries the summary. Several manifests may name the
same file, which is how four papers share
`sections/3-2_further_contributions.tex`.

This is selection at the level of the whole paper, and it follows the same
rule as selection within one. Nothing under `imported_papers/` changes, the
vendored copy stays complete, and the decision lives in the manifest where a
re import cannot lose it. The checker then stops asking for coverage, balance
and orphan references, since no file of that paper is included anywhere, and
instead checks two things: that the manifest says why, and that the named
chapter opens no `importedpaper` block for that slug, which would mean the
body is being imported after all.

Wiring one back in is the reverse: set `status = "wired"`, write the includes
in a chapter of its own, and run the checker until it is clean. The split
parts under `generated/imported/<slug>/` are left in place while a paper is
summarised, so `split_paper.py --check` stays green and nothing has to be
regenerated.

## Adding a paper

1. Drop the upstream copy into `imported_papers/<dir>/`, verbatim.
2. Write `imports/<slug>.toml`.
3. Add its bibliography to `INPUT_FILES` in `scripts/merge_bib.py` and re-run
   the merge.
4. Add `\DeclareImportedPaper{<slug>}{<dir>}{<graphics>}` to `main.tex`.
5. If the paper is monolithic, run `scripts/split_paper.py` and commit
   `generated/imported/<slug>/`. Read what it reports: it names the packages
   the paper's preamble loaded, and any the text needs go in `main.tex`.
6. Write the chapter following the six part anatomy in CLAUDE.md section 4.3,
   wrapping the body in `\begin{importedpaper}{<slug>}`. A `sections` paper
   uses `\importsection{...}`, a monolithic one `\importpart{...}`.
7. Set `status = "wired"` and run the checker until it is clean.

## Re importing a paper

Replace the directory contents wholesale, then:

```bash
uv run --no-project python scripts/split_paper.py     # monolithic papers only
uv run --no-project python scripts/merge_bib.py
uv run --no-project python scripts/check_imports.py
```

They will tell you what changed: files the chapter no longer covers, dropped
files or sections that have vanished, prunes to reapply, split parts that are
out of date. Commits that touch `imported_papers/` touch nothing else, so
`git log -- imported_papers/` reads as a list of imports.
