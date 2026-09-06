# PhD Thesis

**Author:** Pascal Sager, University of Zurich

A cumulative PhD thesis built with the `kaobook` class, pdflatex and biber.
Each results chapter is built around one published paper. The papers are
vendored under `imported_papers/` and reused verbatim, and the frame around
them is written fresh.

This file is the operating guide: how to build, how the bibliography is made,
how a paper is imported, and where the styling lives. The writing rules and
the conventions that govern the text are in [CLAUDE.md](CLAUDE.md).

## Quick start

```bash
./build.sh errors
```

That runs pdflatex, biber, pdflatex, pdflatex and then prints a summary with
the first errors and the first missing bibliography keys. `./build.sh quick`
does a single pass, `./build.sh clean` removes the artefacts.

The other two commands you will need:

```bash
uv run --no-project python scripts/merge_bib.py
```

```bash
uv run --no-project python scripts/check_imports.py
```

```bash
uv run --no-project python scripts/split_paper.py
```

```bash
uv run --no-project python scripts/check_compile.py
```

None of them needs a virtualenv or any third party package. Python 3.11 reads
TOML with the standard library.

What is still open is tracked in one place, [CLAUDE.md](CLAUDE.md) section 7.

## Three kinds of file

Almost every rule in this repository follows from this distinction.

**Thesis owned.** `main.tex`, `preface.tex`, `thesis_style.tex`,
`thesis_import.sty`, `sections/**`, `references/manual.bib`,
`references/overrides.toml`, `imports/**`, `scripts/**`. We write these.

**Imported.** Everything under `imported_papers/**`. Upstream copies of
published papers, never edited, so that a re import is a directory
replacement rather than a merge.

**Generated.** `references/merged.bib`, `references/keymap.csv`,
`references/merge_report.md`, and later `generated/**`. Produced by a script
and committed, because this repository syncs with Overleaf and Overleaf has no
Python. Never edited by hand.

## Layout

| Path | What it is |
| --- | --- |
| `main.tex` | Document root: preamble, part and chapter structure. |
| `thesis_style.tex` | Everything about how the thesis looks. |
| `thesis_import.sty` | Machinery for including a published paper. |
| `sections/` | Thesis owned prose, one file per chapter. |
| `imported_papers/` | The published papers, verbatim. Do not edit. |
| `imports/` | One manifest per paper, plus its own README. |
| `references/` | The bibliography and its inputs. |
| `scripts/` | The merge, the split, the figure conversion and the checks. |
| `generated/` | Split parts, carried macros and converted figures. Committed, never edited. |
| `figures/` | Thesis owned figures and the title page PDF. |
| `kao*.sty`, `kaobook.cls` | The kaobook class. |
| `build.sh` | The build. |

## Bibliography

Nine papers bring nine bibliographies, about 900 entries with heavy overlap, the
same work appearing as a preprint in one file and as a published paper in
another. `main.tex` loads exactly one file, `references/merged.bib`, which is
generated.

### Regenerating it

```bash
uv run --no-project python scripts/merge_bib.py
```

Inputs are listed in `INPUT_FILES` at the top of `scripts/merge_bib.py`:
`references/manual.bib` first, then each paper's bibliography. Adding a paper
means adding its bib there; `check_imports.py` fails if a manifest names a bib
that the merge does not read.

The script normalises every entry, finds duplicates by DOI, then arXiv
identifier, then title with first author, merges each group into one record,
and generates keys of the form `sager_survey_2026`. It writes three files:

- `references/merged.bib`, the only bibliography `main.tex` loads
- `references/keymap.csv`, every old key with the entry it now resolves to
- `references/merge_report.md`, everything it could not decide on its own

It is deterministic and idempotent: same inputs, byte identical output, and
running it twice changes nothing.

### Why the old citation keys still work

Imported `.tex` files cite the keys their own bibliography used, and we cannot
rewrite them. Every merged entry therefore carries biblatex's `ids` field
listing every old key that resolved to it:

```bibtex
@article{sager_survey_2026,
  ids     = {acu_survey},
  author  = {Sager, Pascal J. and Meyer, Benjamin and ...},
  ...
}
```

Biber treats those as aliases, so an imported chapter keeps compiling with no
edit. The script fails loudly if two different works ever claim the same old
key, because biber can alias it to only one of them.

### Fixing a reference

Never edit `references/merged.bib`, and never edit a bibliography under
`imported_papers/`. Both are overwritten. Corrections go in
`references/overrides.toml`, which is documented in full at the top of that
file. In short:

```toml
# Fix or add fields. Address an entry by any key it has ever had.
[entry.brown_language_2020]
doi = "10.48550/arXiv.2005.14165"

# Two entries that are the same work.
[[merge]]
keys = ["wang_user_2024", "wang_when_2023"]
reason = "same arXiv paper, retitled between versions"

# Two entries that only look like the same work. Permanent.
[[split]]
keys = ["brown_language_2020", "devlinBERTPretrainingDeep2019"]
reason = "GPT-3 and BERT, merged only because GPT-3 carried BERT's DOI"

# Venue names, applied everywhere. Left side matched loosely.
[replace.booktitle]
"Proc. of NIPS'16" = "Advances in Neural Information Processing Systems"
```

Then re-run the merge. `references/merge_report.md` prints a ready to paste
block for every conflict, so the usual workflow is to read the report and copy
from it.

### A reference the thesis needs and no paper has

Add it to `references/manual.bib` by hand. That file is listed first among the
inputs, so its values win when the same work also appears in an imported
bibliography. The thesis author's own papers live there, since a paper does not
cite itself.

## Imported papers

`imported_papers/<dir>/` is a read only vendor drop. We do not edit the files,
fix their typos, renumber their figures or prefix their labels. The chapter
includes the parts it wants and the manifest records why the rest are left out.
This is selection, not deletion: deleting the abstract and introduction from
the original would have to be redone after every import.

The manifest schema, and the step by step procedures for adding and re
importing a paper, are in [imports/README.md](imports/README.md).

### Including a paper in a chapter

Declare it once in the preamble of `main.tex`, giving the slug, the paper root
and its figure subdirectories:

```latex
\DeclareImportedPaper{acu}{imported_papers/ACU_JAIR}{figures,figures/data}
```

Then wrap the body in the chapter file:

```latex
\begin{importedpaper}{acu}
\importsection{sections/02_field_of_agents}
\importsection{sections/03_domain_perspective}
\end{importedpaper}
```

`thesis_import.sty` does three things inside that block and undoes all three at
the end. It puts the paper's root on LaTeX's file search path, so the paper's
own `\input{sections/...}` resolves. It puts the paper's figure directories on
`\graphicspath`. And it prefixes every label the paper defines with the slug,
so six papers can each keep a `sec:introduction` and the ACU paper's
`fig:overview` becomes `acu:fig:overview`.

From thesis owned text, point into a chapter with the prefix,
`\cref{acu:fig:overview}`. Inside a block, `\thesisref{...}` reaches a thesis
label without the prefix.

### Papers that arrived as one file

Five of the nine are a single `.tex`, and a chapter cannot include half a file.
`scripts/split_paper.py` cuts them at their top level `\section` boundaries into
`generated/imported/<slug>/`, which is committed so Overleaf can build without
Python. The chapter includes those with `\importpart{...}` instead of
`\importsection{...}`.

The paper's preamble is not imported, so the splitter also carries across the
macro definitions the kept text uses, into `_macros.tex`, which the
`importedpaper` environment loads inside its group. It only carries the ones
that are actually used: the CNA paper's preamble sets `\baselinestretch` to 2
for double spaced journal submission, and importing that would double space the
chapter.

Packages are the exception, since `\usepackage` only works in a preamble. The
splitter reports which ones each paper asked for, and the ones its text needs
are loaded in `main.tex`. That is why `siunitx` and `bm` are there.

`--check` regenerates into memory and fails if the committed files differ, which
catches a re import that nobody re-split.

### Checking it

```bash
uv run --no-project python scripts/check_imports.py
```

Every `.tex` in a paper must be reached from the chapter, listed in the
manifest's `[drop]` with a reason, or matched by `[exclude]`. Reachability is
transitive, so a file that a section file inputs counts. The checker also
verifies that dropped files still exist, that the chapter has the six wrapper
parts, that each manifest bib feeds the merge, and that no thesis file shadows
one of the paper's files. That last one matters because LaTeX searches the
working directory before the paper's root, so a thesis file with a matching
relative path would silently win.

A re import that adds a section fails this check loudly. That is the point.

### Pruning

Publisher build cruft that the thesis never loads may be deleted from the
vendored copy: class files, bibliography styles, template PDFs, superseded
drafts. Each one is declared in the manifest's `[prune]` table with a reason,
so the next import can be pruned the same way. The checker warns while any of
them is still present:

```bash
uv run --no-project python scripts/check_imports.py --prune
```

This is the one exception to not touching `imported_papers/`. It only ever
removes files that no `\input` and no `\includegraphics` resolves to.

## The scripts

| Script | What it does |
| --- | --- |
| `merge_bib.py` | Folds nine bibliographies into `references/merged.bib`. |
| `split_paper.py` | Cuts monolithic papers into parts, and carries every paper's preamble macros into `generated/imported/<slug>/_macros.tex`. |
| `convert_eps.py` | Converts EPS figures to PDF, because pdflatex cannot place an EPS and Overleaf cannot run a converter. |
| `check_imports.py` | Verifies each paper is fully accounted for by its chapter and manifest. `--prune` deletes the template files a manifest lists. |
| `check_compile.py` | Builds every paper's body against the thesis preamble and reports errors per paper. |
| `reimport.py` | Replaces a vendored paper with a fresh copy and reruns all of the above. |

None needs a virtualenv. Run them from the repository root.

## Styling

Everything visual is in [thesis_style.tex](thesis_style.tex), which `main.tex`
inputs at the very end of the preamble so it wins over the class. It sets the
palette in one block of five colours, the heading and caption colours, links,
part pages, table defaults, and the furniture each paper backed chapter opens
with:

```latex
\begin{publicationbasis}{Published}
Full citation of the paper, ending in its \cite key.
\end{publicationbasis}

\contributionstatement
```

To change the colour identity, change the five `\definecolor` lines at the top
of that file and rebuild. Nothing else refers to a colour directly.

The fonts are kaobook's and are deliberately not overridden. The class picks
them through its `fontmethod` option: the default `tex` gives Palatino through
newpxtext and newpxmath, and `modern` gives Libertinus but needs XeLaTeX or
LuaLaTeX. Loading a font package in `thesis_style.tex` on top of that leaves
the text in one family and the mathematics split across two.

## Before committing

- `./build.sh errors` reaches the end with zero LaTeX errors.
- Zero duplicate labels: `grep -c 'multiply defined' build-pass-3.log`.
- `check_imports.py` and `merge_bib.py` both exit 0.
- No em dashes and no banned words in thesis owned files. The greps are in
  CLAUDE.md section 3.10.
- A commit that touches `imported_papers/` touches nothing else, so
  `git log -- imported_papers/` reads as a list of imports.
