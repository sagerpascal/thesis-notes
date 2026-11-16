# CLAUDE.md

Working rules for this repository. Read before writing prose, before touching
`imported_papers/`, and before changing anything about the bibliography.

## 1. What this repository is

A cumulative PhD thesis (kaobook class, pdflatex + biber) by Pascal Sager,
University of Zurich. Each results chapter is built around one published paper.
The published papers are vendored under `imported_papers/` and are reused
verbatim. The thesis frame around them (title, abstracts, introduction,
per chapter framing, discussion, conclusion) is written fresh.

The story, the part structure and the role of each paper are in
`00_ADMIN/05_thesis_concept.md`. Read it before writing frame prose. The
framings that were tried and rejected are in `00_ADMIN/04_story_framings.md`.

Two kinds of file live here, and the difference governs almost every rule below.

**Thesis owned.** `main.tex`, `preface.tex`, `thesis_style.tex`,
`thesis_import.sty`, `sections/**`, `references/manual.bib`,
`references/background.bib`, `references/overrides.toml`, `imports/**`,
`scripts/**`, this file. We write
these, we restyle these, the style guide in Section 3 applies to these.

**Imported.** Everything under `imported_papers/**`. Upstream copies of
published papers. We never edit them. They are exempt from the style guide,
because the text is already published and because any edit is lost on the next
import. See Section 4.

**Generated.** Everything under `generated/**`. Produced by a script from
imported sources, committed to git so that Overleaf can build without Python.
Never edited by hand.

Overleaf note. This repository syncs with Overleaf, which has no Python. Every
generated artefact must therefore be committed, and the build must never depend
on a script running first.

## 2. Build and verify

```bash
./build.sh errors
```

`./build.sh` runs pdflatex, biber, pdflatex, pdflatex and writes
`build-pass-*.log` and `build-biber.log`. `quick` does a single pass, `clean`
removes artefacts, `errors` builds and then prints a summary with the first
errors and the first missing bibliography keys. Use `errors` by default.

Gates before every commit that touches the text:

- The build reaches the end, and the last pass reports zero LaTeX errors.
- Zero LaTeX errors. Read `./build.sh errors`, which counts them, rather than
  filtering the log by hand: pdflatex reports some as `file:line: LaTeX Error`
  and not as a line starting with `!`, and `Float(s) lost` went unnoticed for
  a while behind a hand written `grep '^!'`.
- Zero undefined references and zero duplicate labels. Count them in the PDF,
  not in the log: the log reports each label once, the PDF prints one `??` per
  use, and `scripts/check_layout.py --pdf` gives every hole with its page.
  `build.sh`'s own `undefined` count is higher than the number of `??`,
  because it also counts hyperref's `bhfn:N` back reference anchors. Those
  come from kaobiblio's `backref` option, print nothing, and are not worth
  chasing.
- Zero missing bibliography keys in `build-biber.log`.
- Zero entries in the bibliography that nothing cites. After content is
  removed from the thesis an incremental build keeps printing the references
  that content used to cite, because the citation keys survive in `main.bcf`
  and three passes never converge back. The cut of 2026-11-14 left $143$ of
  them and every other check passed.

  ```bash
  uv run --no-project python scripts/check_layout.py --bibliography
  ```

  The fix is `./build.sh clean` followed by a full build, and any measurement
  taken after content is removed should be taken on one.
- Zero banned words and zero em dashes in thesis owned files (Section 3.10).
- After any trim, no number, citation key or label was lost. Compare the sets of
  numeric tokens, `\cite` keys and `\label` names between `HEAD` and the working
  file, and check every `\ref` still resolves.
- The commit message says what changed and what was verified.

Duplicate labels are the failure mode this repository is most exposed to,
because six papers each carry a `sec:introduction` and a `fig:overview`:

```bash
grep -c 'multiply defined' build-pass-3.log
```

## 3. Writing style guide

Applies to thesis owned prose only. Adapted from the style guide written for the
DFC-TTT paper. The goal in one line: text a careful reader can follow at reading
speed, with every term defined before it is used, every claim no larger than its
evidence, and nothing in the wording that sounds machine written.

### 3.1 How to use this section

- Read it before writing. Run the checks in 3.10 before committing.
- When one sentence is flagged, fix that sentence, then search the whole
  document for the same pattern and fix every sibling. A flagged sentence is a
  sample of a habit, not the whole problem.
- Change only what is flagged or what the sweep finds. Approved text is the
  reference for the style, so do not restyle passages that were already
  approved.
- When two readings of a comment lead to different edits, pick the plainer one.

### 3.2 Sentences

- One idea per sentence, about twenty words, with a verb. Start a new sentence
  instead of chaining clauses with "and", "while" or "which".
- Subject, verb, object. Every sentence has a clear subject. "It is not breaking
  the network" fails because the reader has to guess what "it" is.
- Plain words. "use" not "utilise", "show" not "demonstrate", "start" not
  "commence", "end" not "terminate", "about" not "approximately", "so" not
  "hence" or "therefore" where it reads well, "because" not "owing to the fact
  that".
- Active voice by default. Passive only when the actor is unknown or does not
  matter.
- Result first, then the reason. Say what happened, then why. Say a conclusion
  right after the evidence it follows from, not a paragraph later.
- Say what a number is. What it measures, in what units, at what point in
  training. A comparison names both sides: relative to what, measured how.
- Short does not mean clipped. A full sentence beats a label with a colon.
- No metaphors standing in for explanations. Write what actually happens.

### 3.3 Punctuation, typography and spelling

- British spelling throughout the thesis frame: "generalisation", "behaviour",
  "organisation", "analyse". The document already sets
  `\usepackage[english=british]{csquotes}`. Imported chapters keep whatever
  spelling they were published with, and no attempt is made to reconcile them.
- No em dashes and no en dashes anywhere in prose. Not for asides, not for
  ranges (write "from 640 to 1540", or "$0.2$ to $0.3$"), not as a colon
  substitute.
- No hyphens as connectors. Reword compounds where a plain phrase reads as well:
  "minimum norm solution" not "minimum-norm solution", "one hot" not "one-hot",
  "per unit" not "per-unit" as an adverb. A hyphen inside an established name is
  fine (sign-SGD, K-FAC, vision-language model).
- No semicolons in prose. Math and BibTeX are exempt.
- Parentheses sparingly: citations, cross references, and the name that follows
  a definition. Not for asides that carry content, and not for
  "(e.g. behaviour cloning)". If an example is needed, write "for example
  behaviour cloning" or make it a sentence.
- Colons only to introduce a list or a restatement, and rarely. No label
  sentences such as "Key finding: the agents fail to generalise."
- No rhetorical questions in prose. Section titles are statements.
- `\emph{}` only when naming a defined term at its one definition site. Bold
  only for panel labels in captions and for highlighted cells in tables.
- Numbers in math mode, with thousands grouped as `$200{,}000$`. Standard
  deviations in parentheses after the mean.

### 3.4 Banned words and patterns

Filler and emphasis words that mark text as machine written. Grep for them
before every commit.

> delve, leverage, harness, unlock, crucially, notably, importantly,
> interestingly, remarkably, strikingly, elegantly, moreover, furthermore,
> additionally, it is worth noting, note that, landscape, paradigm shift (as
> filler), nuanced, underscore, highlight (as a verb for emphasis), showcase,
> pivotal, seamless, shed light, pave the way, realm, at its core,
> a testament to, serves as, plays a role, navigate (as a metaphor), foster,
> bolster, cutting edge, comprehensive (as praise), holistic, multifaceted,
> intricate, interplay, dive into, stands in stark contrast,
> a growing body of work, has garnered attention, "In this work, we".

One word needs a carve out in this thesis. "Comprehensive" appears in the
title of the published ACU survey and stays there, but is not used as praise
elsewhere. "Paradigm" has no load bearing use in the current story and is
treated as filler.

Patterns to avoid:

- "not only X but also Y", and "X is not just Y, it is Z". Write two sentences.
- Three parallel items for rhythm rather than content.
- Sentences that open with "To answer this question", "Recall that", "In this
  section we", "Having established".
- Stacked hedges: "may potentially suggest". One hedge at most, and only if the
  evidence is really uncertain.
- "We believe", "we argue". Say what the evidence shows.
- Vague intensifiers: "significantly" without a test, "dramatically", "vastly".
- Code identifiers in prose. Write "controller step size", never `target_lr`.

### 3.5 Terms and definitions

- Definition first, then the name. Write "the group of parameters that shares
  one normaliser, which we call the rule's `\emph{grain}`". Never "the rule's
  `\emph{grain}`, the group of parameters that shares one normaliser".
- One definition site per term, thesis wide. Every later use is plain text with
  no `\emph`. A cumulative thesis makes this harder than a paper does, because
  six papers each define their own vocabulary. See Section 3.9.
- Never use a coined term before its definition, including inside abstracts,
  captions and the appendix in appendix order.
- The abstract contains no coined vocabulary at all. The reader has nowhere to
  look anything up.
- Gloss technical words inline at first use, with "meaning": "the circuit found
  there is sparse, meaning a few neurons carry the computation".
- Do not coin what you do not need.
- A new name must not collide with an existing one, in this thesis or in any of
  the six imported chapters.
- When something is excluded from scope, say why in the same sentence.

### 3.6 Who may act

- Agents, models, learning rules, optimizers and credit assignment algorithms
  may act: decide, choose, prefer, equalise, rescale, build, spread.
- Tasks, benchmarks, datasets, architectures as abstractions, measures, "the
  field" and "the literature" may not decide or choose. They exist, emerge, are
  found, or are set by something. Not "the benchmark decides what counts as
  success". Write "the benchmark's success criterion counts a trajectory as
  successful when", and "the task offers a sparse solution" rather than "the
  task demands it".
- A network may generalise, memorise and compute, but the sentence should make
  clear which training procedure produced it.
- Do not personify the thesis. "The thesis carries" is acceptable once, "the
  thesis argues" is not.

### 3.7 Claims and honesty

- Never say a prediction was made before the runs or before training. Say what
  an equation or proposition implies and that the measurement agrees. Banned:
  "predicted in advance", "before training", "before the runs", "registered",
  "pre-specified".
- Verbs no larger than the evidence. "shows", "gives", "lands at", not
  "demonstrates", "proves", "establishes", unless it is a theorem.
- Failed predictions and negative results stay in the thesis and are called
  failures.
- Limitations are specific and plain, not apologetic and not padded with
  defences.
- State the verdict when there is one.
- Do not put two nearly equal numbers side by side in prose and ask the reader
  to see a difference (0.60 against 0.64). Put them in a table or give the
  interval.
- Make comparisons complete: same seeds, same budget, same measure, and say so.
- Describe what a method does before what it does not.
- Name the thing. Say "Adam" when Adam is meant, not "the shared optimizer".
- Contribution statements are the one place where the thesis speaks about who
  did what. They are factual, they name co-authors, and they do not inflate the
  thesis author's share. When attribution is genuinely unclear, say that it is
  unclear rather than claiming or disclaiming.

### 3.8 Structure

- Section titles are statements of the finding. "Whether a rule groks is decided
  at the minima of the loss", not "Does the rule decide grokking?".
- One exemption, taken deliberately on 2026-11-16. A section whose content is
  structural rather than a finding keeps a noun label: "Research questions",
  "Contributions", "Introduction and Background", "Synthesis", "Further
  Contributions". Statement forms for these come out worse than the labels.
  The exemption covers part titles of the same kind and nothing else, and a
  section that states a finding does not get it.
- Every results section opens with the finding, then the setup that produced it,
  then the evidence, then the controls. Setup does not come first.
- The first sentence of a section connects to the result of the previous one.
- No roadmap paragraphs, no "In this section we", no repeating the contributions
  list later. A finding is stated once in full. Later sections refer to it in
  one clause. In a cumulative thesis this rule is easy to break, because the
  same result appears in the introduction, in its chapter, and in the
  discussion. State it in full in its chapter. The introduction gives the
  one sentence version. The discussion refers to it and does something new with
  it.
- Say how a measurement is made where it is first used, at the depth the reader
  needs there. Exact protocol lives in the appendix and the main text points to
  it.
- The thesis frame speaks generically: "a hidden layer", "a unit's outgoing
  weight norm". Layer numbers, epoch counts and seed lists belong in the
  imported chapter or the appendix.
- Related work reads as one argument, holds no results of ours, cites each
  method at its first mention, and ends by naming the gap the thesis fills. It
  is titled by what it covers.
- Captions: the first sentence states the claim the figure supports. Then the
  panels in order. Long caption sentences are split like any other sentence.
- Appendix sections open with one sentence saying which reading of the results
  they close off or which claim they check.

### 3.9 Cumulative thesis conventions

The six papers were written for different venues, over several years, with
different notation and different names for overlapping ideas. Reconciling them
is thesis work, and it happens in the thesis frame, never by editing the papers.

- Every chapter follows the wrapper anatomy in Section 4.3. The wrapper is where
  the paper's vocabulary is connected to the thesis vocabulary.
- When a chapter's notation differs from the thesis notation, the chapter
  introduction says so in one sentence and gives the mapping. Do not silently
  let two symbols mean the same thing.
- When two papers use different names for the same idea, the thesis frame picks
  one name, defines it once in the introduction, and each affected chapter
  introduction states the local synonym once.
- A term's single definition site is in the thesis frame if the thesis frame
  uses it, even if an imported chapter also defines it. The imported definition
  is left alone and the frame definition is the one the reader is sent to.
- The six argument parts are numbered and labelled, so a chapter may refer to
  one: `part:background`, `part:agents`, `part:procedure`, `part:readout`,
  `part:construction`, `part:synthesis`. `part:readout` was `part:measurement`
  until 2026-11-16 and was renamed with its part. The appendix part is deliberately
  unnumbered, because it is not part of the argument. Rename a label with its
  part, and keep the two in step.
- Keep a ledger of thesis wide terms in `imports/glossary.toml`, one entry per
  term with its definition site and any per chapter synonyms. Add a term the day
  it is coined.

### 3.10 Checks

Fix, then sweep. After every point fix, grep the whole thesis owned tree for the
pattern. All greps are scoped to thesis owned files, because imported text is
exempt.

```bash
grep -rn '—\|–' main.tex preface.tex sections/
```

```bash
grep -rniE 'delve|leverage|harness|unlock|crucially|notably|importantly|interestingly|remarkably|strikingly|elegantly|moreover|furthermore|additionally|worth noting|showcase|pivotal|seamless|shed light|pave the way|realm|at its core|testament to|multifaceted|intricate|interplay|dive into|stark contrast|growing body of work|garnered attention|In this work, we|before training|before the runs' main.tex preface.tex sections/
```

```bash
grep -rn ';' sections/ | grep -v '\$' | grep -v '^\s*%'
```

Semicolons inside math and inside `\href` or `\url` are fine, so read the hits
rather than trusting the count.

## 4. Imported papers

### 4.1 The contract

`imported_papers/<dir>/` is a read only vendor drop. We do not edit the files,
we do not renumber their figures, we do not fix their typos, we do not restyle
their prose, and we do not prefix their labels by hand. A re import from
Overleaf or from the camera ready must be a wholesale directory replacement that
leaves the thesis building.

The user's instinct was to delete the paper's title, abstract, introduction and
conclusion from the original so that a merge file can supply replacements. Do
not do that. Deletion is a modification, so it has to be redone by hand after
every re import, and it silently changes the thing the thesis claims to
reproduce. The mechanism is **selection, not deletion**: the paper stays whole,
and the thesis chapter includes only the parts it wants. Selection is
idempotent, survives re import, and leaves an auditable record of what was left
out and why.

One exception is allowed. Publisher build cruft that the thesis never uses may
be pruned: `.cls`, `.sty`, `.bst`, `.bbx`, `.cbx`, `.dbx` from journal
templates, template PDFs, and how-to documents. Pruning is declared as glob
patterns in the paper's manifest so that a re import re-prunes deterministically
and nobody has to remember. Pruning removes only files that no `\input` and no
`\includegraphics` in the thesis resolves to.

Commits that touch `imported_papers/` touch nothing else. That way
`git log -- imported_papers/` reads as a list of imports.

### 4.2 Manifest

One manifest per paper, at `imports/<slug>.toml`, outside the untouchable tree.
Python 3.11 reads TOML with the standard library `tomllib`, so no dependency is
needed. The slug is the thesis wide short name for the paper and is decoupled
from the directory name, so the vendored directories keep whatever names they
arrived with. It doubles as the paper's label prefix.

The full schema, and the procedures for adding and re importing a paper, are in
[imports/README.md](imports/README.md). In short: `drop` names what the chapter
leaves out and why, `exclude` names whole trees that are not part of the import,
and `prune` names files deleted from the vendored copy. A manifest is never
edited to make a check pass. If the check fails, either the chapter or the
vendored copy changed, and the manifest is where that decision gets recorded.

### 4.3 Chapter wrapper anatomy

Every paper backed chapter is one thesis owned file under `sections/`, named
`<part>-<n>_<slug>.tex`, with this shape. `sections/3-1_acu_survey.tex` is the
reference implementation.

1. `\chapter{...}` and `\label{chap:<slug>}`.
2. Publication header box: full citation of the published paper, its `\cite`
   key, and its status.
3. Contribution statement, as a starred section added to the toc. Factual, names
   co-authors, follows Section 3.7.
4. Chapter introduction. Thesis owned. This replaces the paper's abstract and
   introduction. It connects the previous chapter's result to this one, gives
   the notation mapping if there is one, and states what the chapter
   contributes to the thesis argument.
5. The imported body, included section by section.
6. Chapter summary. Thesis owned. This replaces the paper's conclusion. It
   states the chapter's findings once in full and hands off to the next chapter.

The thesis owned parts obey the style guide. The imported body does not.

Dropping the paper's introduction has a cost that only shows in the PDF. The
body still says "see Figure 1", the figure went with the introduction, and the
reader gets `??`. Both survey chapters lost their overview figure that way.
The fix does not touch the paper: reproduce the float in the wrapper, inside
the `importedpaper` block, under the paper's own label. The block prefixes it
like any of the paper's own labels, so the body's reference resolves. This is
the one place thesis owned text copies published text, so `check_imports.py`
notes every reproduction on every run and a re import has to be checked
against it.

### 4.4 Including the body

`thesis_import.sty` does the scoping. Declare each paper once in the preamble
of `main.tex`, giving its slug, its root and its figure subdirectories:

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

Inside the block the package puts the paper's root on LaTeX's file search path
and its figure directories on `\graphicspath`, and restores both at the end.
That is what lets a paper's own `\input{sections/04_1_...}` resolve. Forwarding
stubs in thesis directories are not needed and none remain.

One limitation, enforced by the checker rather than by LaTeX: `\input@path` is
a fallback, not an override. LaTeX looks in the working directory first, so a
thesis file whose relative path matches one a paper asks for would shadow the
paper's file. `check_imports.py` fails when that happens.

Labels. The block prefixes every label the paper defines with its slug, so the
paper's `fig:overview` becomes `acu:fig:overview`, and six papers can each keep
a `sec:introduction`. References inside the paper are prefixed the same way, so
they still resolve. Thesis text points into a chapter with the prefix, as in
`\cref{acu:fig:overview}`, and `\thesisref{...}` reaches a thesis label from
inside a block.

The patched commands are `\label`, `\ref`, `\pageref`, `\nameref`, `\autoref`,
`\cref`, `\Cref`, `\crefrange`, `\Crefrange` and `\label@in@display`. The last
one matters: inside a display, amsmath swaps `\label` for its own stash and
re-emits the name afterwards, so patching `\label` alone would leave every
equation label unprefixed while its references were prefixed. `\eqref` is
deliberately not patched, because amsmath defines it in terms of `\ref` and it
picks up the prefix from there. Patching it too would prefix twice.

If a chapter ever needs another reference command, add it to `\ip@allcommands`
and check whether the package that defines it takes a private copy of `\label`
the way amsmath does.

Three variations on `\importsection`, each for a problem a published paper
can present and the thesis cannot fix by editing it.

An unbalanced file. `\importsection[\end{itemize}]{...}` runs the closing
`\end` inside the include's own group, which is where it has to go. Putting it
after the include instead closes the group that tracks the paper's working
directory, `\ip@cwd` is never restored, and the next include resolves against
a doubled path. `check_imports.py` works out what each file leaves open and
holds the closers to it in both directions, so a missing one is an error and a
stale one is reported the day the paper is fixed upstream. COGITAO's
`6_appendix/Experiments.tex` needed one, and the feature is kept because the
next paper that arrives unbalanced will need it too.

A summarised paper has no chapter to carry that optional argument, so the
closer goes in its manifest instead, as a `[closers]` table keyed by file.
COGITAO's went there when the paper was cut. Without it `check_compile.py`,
which builds every paper whether the thesis includes it or not, failed on
COGITAO and reported a missing file at `6_appendix/6_appendix/Metrics.tex`,
which is what a doubled `\ip@cwd` looks like from the log.

A file whose display equations will not fit. `\importpartwide{...}` and
`\importsectionwide{...}` set the file on pages that reclaim the margin
column, which is 153pt. Declared per file for the reason rotation is, and
margin citations are suppressed inside, because there is no margin there to
put them in.

A file whose tables will not fit. `\importsectionrotated{...}` sets the file
on turned pages. Section 4.5 explains why rotation is declared per file and
not per table.

A label the chapter has taken over. `\importedlabel{slug}{name}` defines one
of a paper's labels from thesis owned text, outside any block, without the
`\clearpage` that ending a block would cause. When a chapter drops the paper's
discussion and writes its own summary, the paper's body still says "as we
discuss in Section~\ref{sec:discussion}", and the section it wants is that
summary. Use it only where the thesis owned text really is the replacement.
It is a claim about content, not a way to silence a warning.

Monolithic papers. Three papers arrived as one file, so the parts a chapter
wants have to be made into files first:

```bash
uv run --no-project python scripts/split_paper.py
```

It cuts the paper at its top level `\section` boundaries and writes
`generated/imported/<slug>/NN_<title-slug>.tex`, each with a "generated, do not
edit" header, all committed so Overleaf can build. The chapter includes them
with `\importpart` rather than `\importsection`, because they live under
`generated/` rather than in the paper:

```latex
\begin{importedpaper}{llmbench}
\importpart{02_survey-of-key-technologies}
\end{importedpaper}
```

`--check` regenerates into memory and fails if the committed files differ,
which catches a re import that nobody re-split.

Two papers keep the preamble and the sections in different files, and one of
them keeps its appendix in a second document. A Frontiers manuscript is a
`main.tex` that loads a template, a preamble and three `\input` lines, with the
sections in `content/body.tex` and the appendix in `content/supplement.tex`,
which is the body of a separate supplement document. Cutting the root file
there finds no section at all. The optional `body` field names the file or
files the sections are really in, and they are cut as if they were one, so the
supplement's sections become the paper's appendix parts. `source` stays the
root file, because that is where the macros and the packages are read from.

Three things the splitter has to do because the paper's preamble is not
imported, each of them reported when it happens. It removes the paper's own
bibliography and its `\appendix` switch, which would otherwise inject a second
reference list and renumber the thesis appendix. It carries the preamble macro
definitions the kept text actually uses into
`generated/imported/<slug>/_macros.tex`, which `importedpaper` loads inside its
group so two papers may define the same name. And it rewrites
`\DeclareMathOperator`, which amsmath only allows in a preamble, into the
equivalent `\operatorname` form.

Only the definitions the kept text uses are carried. Carrying the whole
preamble would import the paper's journal formatting with it, and the CNA paper
sets `\baselinestretch` to 2 for double spaced submission.

Packages are the one thing that cannot be handled this way, because
`\usepackage` only works in a preamble. The splitter reports which packages
each paper's preamble loaded, and the ones its text needs go in `main.tex`.
That is why `siunitx` and `bm` are loaded there.

### 4.5 Making an imported paper compile

A paper written on a conference template does not drop into kaobook unchanged.
Four things reliably break, and all four are fixed from outside the paper.

**Its preamble is not imported, but its text needs it.** Every paper keeps
notation in the preamble, usually by `\input{math_commands.tex}`.
`split_paper.py` reads the root file the manifest names as `source`, follows
that input, and writes the definitions the kept text actually uses to
`generated/imported/<slug>/_macros.tex`, which `importedpaper` loads inside its
group. A sections paper needs `source` for this even though it is never split.
Only used definitions are carried, because a whole preamble brings the paper's
journal formatting with it. Each carried definition is preceded by
`\let\name\relax`, since `\newcommand` refuses a name the kernel already has,
and `\K`, `\B` and `\laplace` are all taken.

**Packages only work in a preamble.** The splitter reports which ones each
paper asked for. Add the ones its text needs to `main.tex`, which is why
`siunitx`, `bm` and `dsfont` are loaded there.

**Theorem environments belong to the thesis.** `kaotheorems` declares
`theorem`, `proposition`, `lemma` and the rest, and every chapter inherits
them, so a paper's own `\newtheorem` is skipped. The splitter fails if a paper
wants one the thesis does not have.

**pdflatex cannot place an EPS.** `convert_eps.py` converts them to PDF under
`generated/imported/<slug>/figures/`, which goes first on `\graphicspath`, and
the result is committed because Overleaf cannot run the converter. This also
fixes the CNA paper, which ships PDF versions of its figures under a different
basename than the one it asks for.

Two smaller ones handled in `thesis_import.sty`, both scoped to the block so
thesis prose is unaffected: the old two-letter font commands (`\it`, `\sc`),
which KOMA turns into errors, and `\subfile` from the subfiles package, which
resolves relative to the including file rather than the document root.

Figures are the one thing `.gitignore` gets wrong by default. The blanket
`*.pdf` rule is aimed at build output, and exceptions keep every vendored and
converted figure tracked.

**Its tables may be too wide, and a longtable cannot be scaled.** Every
other table is wrapped in an adjustbox and shrunk to the measure. A longtable
breaks across pages, so it is never one box, and it measures against the page
rather than `\linewidth`, so kaobook's `widepar` does not reach it either. The
ACU survey's three agent tables, fifteen columns each, ran 182pt past a 304pt
measure.

Turning the page fixes it, with two corrections to `lscape`, both in
`thesis_import.sty`. It sets the rotated column to the old `\textwidth`, only
304pt here because the margin column takes another 153pt, and rotated that
margin is not a margin but unused paper, so the margin is added back to give
458pt. And the rotated block is set down from the text block's own left edge,
which on a verso page sits beyond the margin column, so it is shifted back by
the margin width there.

Rotation is declared per file, with `\importsectionrotated`, not wrapped
around each longtable. Turning the page is a `\clearpage` at each end, so
rotating three tables in one file left each of their subsection headings alone
on an otherwise empty upright page.

**Its bibliography may be inline.** A journal often wants the references pasted
into the manuscript, and the CNA paper arrived that way, as `\bibitem` entries
inside `\begin{thebibliography}`. The splitter strips that, because two
bibliographies cannot coexist, and converts it to
`generated/imported/<slug>/_thebibliography.bib`, which `merge_bib.py` reads
like any other source. A `\bibitem` is formatted text rather than data, so the
fields it yields are rough and the whole original string is kept in `note`.

**Its environments may not balance.** An unclosed `\begin` does not fail
politely: it swallows the rest of the document and the output routine then
spins on one page instead of stopping. `check_imports.py` checks every included
file for this.

Two limits found the hard way, both recorded here so they are not retried.
`\pagelayout{wide}` for imported chapters cuts the overfull boxes from 151 to
41, because the papers were typeset for wide templates, and it also exhausts
TeX's main memory in kaobook's output routine and produces no PDF. And a file
with a few hundred lines of `lstlisting` does the same on its own, which is why
COGITAO's raw prompt appendix was dropped while that paper was still
imported.

### 4.6 Checking that it compiles

```bash
uv run --no-project python scripts/check_compile.py
```

A chapter wrapper carries the thesis's framing, so it cannot be written before
the story is settled, but the imported bodies either compile or they do not.
This builds a throwaway document from `main.tex`'s preamble plus every paper's
includable content, runs pdflatex, and attributes each error to the paper it
came from. It writes nothing the thesis build depends on.

### 4.7 Re importing a paper

```bash
uv run --no-project python scripts/reimport.py <slug> <path to the paper>
```

Copies the source directory over the vendored one, applies the manifest's
prunes, then runs the splitter, the figure converter, the bibliography merge,
the checker and the compile check. A re import that changes the paper's
structure fails one of those, which is the point. Copy the directory holding
the `.tex`, not the project repository around it.

### 4.8 Drift check

The point of the manifest is that a re import cannot silently drop content.

```bash
uv run --no-project python scripts/check_imports.py
```

For every manifest it verifies:

- Every `.tex` in the paper is reached from the chapter, or listed in `drop`
  with a reason, or matched by `exclude`. Reachability is transitive, so a file
  a section file inputs counts as covered.
- Every entry in `drop` still exists in the paper, and none of them is also
  reached from the chapter.
- No thesis file shadows a file the paper inputs.
- The chapter opens `importedpaper` with the right slug and contains the six
  wrapper parts from Section 4.3.
- The bib files named in the manifest exist and appear in `INPUT_FILES` in
  `scripts/merge_bib.py`, so their references reach the bibliography.
- Labels defined by more than one paper are listed, as a reminder that the slug
  prefix is what keeps them apart.
- No kept file refers to a label that only a dropped file, or only an excluded
  variant of the paper, defines. That is the check that catches a `??` before
  anybody reads the PDF, and the message names the file the target lives in so
  the choice is between restoring it and rewording the sentence. Labels are
  counted however they are spelled, so a `label=` key in an `lstlisting` or an
  `algorithm` option counts as a definition.
- Where a wrapper reproduces a float from a dropped file, that is noted every
  run. It is the one place thesis owned text copies published text, so it is
  the one place a re import can silently go stale.

Unapplied prunes are warnings rather than errors, because nothing loads those
files. `--prune` applies them.

A re import that adds a section fails this check loudly. That is the whole
design.

### 4.9 Papers and their chapters

| Slug | Directory | Chapter | Layout |
| --- | --- | --- | --- |
| `acu` | `imported_papers/ACU_JAIR` | summarised | sections |
| `grokking` | `imported_papers/grokking` | `sections/4-1_grokking.tex` | monolithic, `iclr2027_conference_v2.tex` |
| `attention` | `imported_papers/self_attention_geometry_project_ICML` | `sections/4-2_attention.tex` | sections, under `ICML2025/` |
| `bounded` | `imported_papers/probe-norm` | `sections/5-1_bounded.tex` | monolithic, `main.tex` plus `body` |
| `cna` | `imported_papers/Neural_Computation__CNA` | `sections/6-1_cna.tex` | monolithic, `NECO-D-24-00304-Source.tex` |
| `llmbench` | `imported_papers/Llama2_benchmark_sds` | summarised | monolithic, `llm_at_home.tex` |
| `cogitao` | `imported_papers/COGITAO_ICML_2026` | summarised | sections |
| `hounsfield` | `imported_papers/sds_hounsfield_features` | summarised | monolithic, `main.tex` |
| `retrieval` | `imported_papers/CLEF_Checkthat_4b` | summarised | sections |

The four reproduced papers are the argument. The five marked summarised carry
`status = "summarised"` in their manifests, their bodies are included nowhere,
and their appendix chapters are gone.
`sections/3-2_further_contributions.tex` gives four of them a page or two of
thesis owned prose with the author's role stated. The survey is the fifth and
keeps a chapter of its own, `sections/3-1_acu_survey.tex`, at six pages: the
authorship is shared first, the source runs to over fifty pages, and the
thesis takes its question from it. It was cut on 2026-11-16. Nothing under `imported_papers/`
changed when they were cut, which is the point: any of them is wired back in
by setting `status = "wired"` and writing the includes.
`check_imports.py` checks that a summarised manifest gives a
`summary_reason` and that its chapter opens no `importedpaper` block for that
slug. Chapters whose wrapper is still empty
get their heading and label from `main.tex` and lose both once the wrapper is
written. All nine papers have a manifest.

The self attention project ships three variants. The ICML2025 directory is the
one with split section files, so it is the import source. The arXiv and rebuttal
directories are kept for reference and are not included in the build.

## 5. Bibliography

### 5.1 The problem

Six papers bring six bibliographies, currently about 750 entries across six
files, with heavy overlap, inconsistent keys, inconsistent formatting, and the
same work appearing as a preprint in one file and as a published paper in
another. `main.tex` cannot simply load all six, because duplicate keys and
duplicate works would both break the build and corrupt the reference list.

### 5.2 Layout

```
references/
  manual.bib        # thesis owned, hand written: our own papers
  background.bib    # thesis owned, hand written: what the background cites
  merged.bib        # GENERATED, committed, the only file main.tex loads
  keymap.csv        # GENERATED, old key -> new key, with source file
  merge_report.md   # GENERATED, duplicates, conflicts and things to look at
scripts/
  merge_bib.py      # the merge
```

`main.tex` loads exactly one bibliography,
`\addbibresource{references/merged.bib}`. The root `thesis.bib` is retired and
the second `\addbibresource` for the ACU references is gone, since the merge
covers it. Corrections go in `references/overrides.toml`, never into
`merged.bib` and never into a bibliography under `imported_papers/`.

Two hand written files rather than one, because they are edited for different
reasons. `manual.bib` holds the thesis author's own papers, cited by the
publication header box of the chapter each one backs. `background.bib` holds
what `sections/2-1_related_work.tex` cites and no imported paper carries: the
implicit bias of training procedures, sparse and distributed coding in
neuroscience, unit ablation and pruning, and the evaluation of learned
predictors against trivial baselines. Before adding an entry to either, check
that no imported bibliography already has it, since six papers between them
already supply the grokking literature, the Transformer and interpretability
literature, the optimizers and credit assignment rules, retrieval, and the
assembly lineage. `merge_bib.py` folds a duplicate rather than failing on it,
so a needless entry is silent waste rather than an error.

### 5.3 How the merge works

```bash
uv run --no-project python scripts/merge_bib.py
```

Inputs are the two thesis owned files, `references/manual.bib` and
`references/background.bib`, plus every bib file named in an
`imports/<slug>.toml`. Reading the manifests rather than globbing means a stray
backup bib inside a paper directory is never picked up by accident. The thesis
owned files are listed first in `INPUT_FILES`, so where a reference also
appears in an imported bibliography, the values we wrote win.

**Normalise.** Every entry is brought to one shape before anything is compared.
Entry types unified. Zotero and Mendeley cruft dropped (`file`, `abstract`,
`keywords`, `annote`, `urldate`, `shorttitle`, `mendeley-*`). Author names to
`Last, First` with `and` separators. Title capitalisation preserved by brace
protection where it already exists, not re-cased. DOI reduced to a bare
lowercase `10.xxxx/...` with any `https://doi.org/` prefix stripped. arXiv
identifiers moved out of `journal` and `note` into `eprint`, `eprinttype` and
`eprintclass`. Page ranges to `--`. Fields sorted in a fixed order so that
output is stable. Output is UTF-8, and the script reports any entry containing
characters that T1 encoded pdflatex cannot set, because that is a build break
rather than a cosmetic issue.

**Find duplicates**, in this order, most reliable first:

1. Same normalised DOI.
2. Same arXiv identifier.
3. Same normalised title, same first author surname, and years within one of
   each other. The tolerance catches the preprint against the published version.
4. Fuzzy title similarity above a threshold. These are **reported, never merged
   automatically**. A human decides and records the decision.

**Merge a duplicate group.** Pick the canonical record: prefer the published
form over the preprint (`article` and `inproceedings` beat `misc` and
`unpublished`), then the record with the most filled fields, then the
alphabetically first source file so the result is deterministic. Fill the
canonical record's missing fields from the others. Report every field where two
records disagreed and the loser was discarded.

**Generate keys** as `lastname_word_year`, for example `sager_survey_2026`.
Surname of the first author, lowercased and ASCII folded with non letters
stripped. First significant title word after a stopword list. Four digit year.
Collisions get a suffix `a`, `b`, `c`, assigned in a deterministic order so that
re running the script does not shuffle keys.

**Keep the old keys working.** This is the part that makes the whole scheme
work with untouchable imported files. Imported `.tex` cites old keys and we
cannot rewrite it, so every merged entry carries biblatex's `ids` field listing
every old key that resolved to it:

```bibtex
@article{sager_survey_2026,
  ids = {acu_survey, sager2025comprehensive, SagerMeyer2026},
  ...
}
```

Biber treats those as aliases, so every imported citation keeps resolving with
no edit to any imported file. The script must check that no alias collides with
a real key or with another alias, and fail if one does.

**Rewrite thesis owned files**, optionally and separately:

```bash
uv run --no-project python scripts/merge_bib.py --apply-keys
```

This rewrites keys to the new scheme in `main.tex`, `preface.tex` and
`sections/**` only. It never touches `imported_papers/**`. It rewrites keys only
inside citation commands, never in free text: `\cite`, `\citep`, `\citet`,
`\citeauthor`, `\citeyear`, `\parencite`, `\textcite`, `\autocite`, `\footcite`,
`\fullcite`, `\nocite`, `\citealp`, `\citealt`, and the local `\citepeg`,
handling optional arguments and comma separated key lists.

**Properties the script must have.** Deterministic: same inputs, byte identical
output. Idempotent: running it twice changes nothing. Non destructive: it never
writes into `imported_papers/`. Loud: anything it could not decide goes into
`merge_report.md` rather than being guessed.

**Verify after every merge.** The set of citation keys reachable before and
after must be identical, counting aliases. Then build and confirm
`build-biber.log` reports zero missing entries.

## 6. Styling

Everything visual lives in `thesis_style.tex`, which `main.tex` inputs at the
very end of the preamble so it wins over the class. Do not style inline in a
chapter, and do not add a `\definecolor` or a `\tcolorbox` in `sections/`. If a
chapter needs a new visual element, define it in `thesis_style.tex` so that
every chapter gets the same one.

The palette is five colours at the top of the file: `ThesisPrimary` (slate
teal) for headings and rules, `ThesisSecondary` for subordinate headings,
`ThesisAccent` (amber) for citations and URLs, `ThesisGrey` for anything that
should recede, and `ThesisRule` and `ThesisTint` for boxes. Nothing else refers
to a colour directly, so changing the identity is changing those five lines.

Chapter furniture. Every paper backed chapter opens with the same two elements,
defined once in `thesis_style.tex`:

```latex
\begin{publicationbasis}{Published}
Full citation of the paper, ending in its \cite key.
\end{publicationbasis}

\contributionstatement
```

`check_imports.py` checks that each chapter has both.

Citations go in the margin. `\sidecite` sets the usual numeric marker in the
text and puts the work's marker, author and year beside it, which is what
kaobook's wide margin is for. It is applied by patching `\cite`, `\parencite`
and `\textcite`, the three biblatex commands everything else routes through,
so all nine papers get it without one of them being edited. `\ts@sidecitefalse`
turns the whole thing off.

The margin holds 165 of the thesis's 588 single key citations, and every one
of the five decisions that got it from 588 to 165 was forced by a measurement.
Changing any of them means taking the measurement again.

A citation of several works at once does not go there. Five references stacked
in the margin swamp the page and the marker in the text is one bracket either
way.

A citation outside running text does not. Beside a float the margin already
carries that float's caption, a caption's citation is re-executed when the
list of figures is typeset, and a table cell has no margin of its own.

A work already introduced in this chapter does not. Of the 588 single key
citations only 276 are a work's first mention in its chapter, and at 276 five
pages had margin notes running off the paper.

The note carries no title. kaobiblio's own margin format ends with the full
title, which is four or five lines in a 136pt column, and the title is the one
part the bibliography already gives in full. `\formatmargincitation` is
redefined to stop at the year.

At most one citation per paragraph reaches the margin, through the kernel's
`para/begin` hook. A paragraph that cites three works in two sentences
otherwise stacks three notes in the same few lines.

And the note is placed by the marginnote package rather than by `\marginpar`.
kaobook reads an offset-less `\marginnote` as a request for the floating
`\marginpar`, so the shift is passed as `0pt` rather than left out. The
floating one was tried first and cannot be used here: at full density seventy
notes a run were relocated away from the paragraph they belonged to, and one
left pending at the `\clearpage` that ends an imported chapter made LaTeX
report `Float(s) lost` and discard it. An empty `importedpaper` block
reproduces that, so it is the mechanism and not the volume. What marginnote
does instead of relocating is overprint, which is why the two rules above are
not optional, and why the check is to look at the densest margin in the
document rather than to trust the log:

```bash
uv run --no-project python scripts/check_layout.py --margins
```

Float pages are top aligned. LaTeX centres them, because `\@fptop` and
`\@fpbot` are both infinitely stretchable, and a single table on such a page
then floats a third of the way down with white above and below it and reads as
an accident. `\@fptop` is 0pt, so a float page starts where the text block
starts on every other page.

Fonts are kaobook's and are not overridden. The class chooses them with its
`fontmethod` option: `tex`, the default, gives Palatino through newpxtext and
newpxmath, and `modern` gives Libertinus through fontspec but needs XeLaTeX or
LuaLaTeX. This thesis builds with pdflatex, so it gets Palatino, and kao.sty
sets `\linespread` to 1.07 for it. Loading `libertinus` or `newtx` in
`thesis_style.tex` on top of that leaves the text in Palatino while the
mathematics is split between two families. Changing the face means changing the
class option and the build engine, not adding a package.

Two things are deliberately left alone. Margin material is driven by kaobook
through `\marginfont`, which the margin table of contents and sidenotes depend
on, so it is not restyled. Theorem heads are declared by `kaotheorems` through
thmtools, and colouring them means re-declaring every theorem, which is not
worth the risk until a chapter actually needs it.

## 7. Open issues

The one todo list for this repository. It holds only what is still open. When
something is done, delete its entry rather than marking it done, so the list
stays short enough to read every session. Anything that has become permanent
knowledge belongs in the sections above, not here.

The thesis builds: 229 pages, zero LaTeX errors, zero duplicate labels, a
working bibliography, and four of the nine papers reproduced with their
appendices. The other five are summarised. `check_compile.py` reports zero
errors across all nine, and `check_imports.py` zero. Machinery that works is not listed here: `build.sh`,
`thesis_style.tex`, `thesis_import.sty`, the nine manifests, the `references/`
and `generated/` trees, and all seven scripts.

### Blocking the thesis

The thesis frame is written end to end as of 2026-11-16: both abstracts, the
introduction, the background, five chapter wrappers, the discussion and the
conclusion. What is left here needs the author, or needs a paper to be
finalised, or is cosmetic.

0. **The story is settled and the frame is written to it.** The spine is
   credit assignment, set on 2026-11-16, and
   `00_ADMIN/05_thesis_concept.md` carries it. The paragraph plans every
   chapter was written to, and four rounds of critique with what was done
   about each, are in `00_ADMIN/07_writing_plan.md`. Read both before
   changing any frame prose. The retired word "layout" is gone from thesis
   owned prose; the only remaining matches are a kaobook class option and a
   comment about visual layout.

1. **Seven things need the author and nobody else.**
   - `figures/Titelblatt_E_POV2011.pdf` is still the faculty's blank form,
     see item 7 below.
   - `sections/0-3_acknowledgements.tex` is a placeholder.
   - `sections/9-1_declarations.tex` carries the originality declaration as a
     placeholder, and the faculty may prescribe its own wording.
   - Three contribution statements are reconstructions and are marked
     `TODO(author)`: grokking, CNA and the survey. The survey's is also in a
     more bureaucratic register than the other four, which one reviewer read
     as advocacy in two places.
   - `sections/0-4_publications.tex` prints a status line per entry that
     should be checked against the published record.
   - `references/manual.bib` has `pages = {34}` for `acu_survey`, which may
     be a JAIR article number rather than a first page.
   - The working title. Alternatives are in `00_ADMIN/05_thesis_concept.md`.

2. **Three papers are not final.** COGITAO, grokking and the world model
   paper are still moving. Run `scripts/reimport.py <slug> <path>`, which
   replaces the directory and reruns everything downstream. The world model
   manuscript is not yet submitted and its publication box says so; when it
   is, update the box, `references/manual.bib` and the chapter introduction.

3. **The frame's numbers come from the current manuscripts and will drift.**
   Every quantitative claim in thesis owned prose was checked against the
   vendored source on 2026-11-16, and the check caught six errors. Two were
   serious: the opening sentence of both abstracts and the introduction had
   fused the width-2048 neuron counts with the width-256 accuracy cost, and
   "a few columns come to dominate" misread the attention paper's measure,
   which means columns of high norm outnumbering rows of high norm. After any
   re import, run that check again rather than trusting the prose.

### Correctness

7. **1 `??` in the PDF, upstream and unfixable from here.** One label used
   twice is two holes in the text, so count them in the output rather than in
   the log:

   ```bash
   uv run --no-project python scripts/check_layout.py --pdf
   ```

   `attention:eq:weight-update-bilinear-form-prediction` on page 95 exists
   only in the rebuttal variant, which the thesis does not import.
   `check_imports.py` reports it with the file the target lives in. The second
   hole, COGITAO's `tab:se_all_experiments`, left the build with COGITAO.

   The old story's six names in `1-1_introduction` and `2-1_related_work` are
   gone, and so are the ACU chapter's five. Where a chapter drops a paper's
   introduction, the hero figure goes with it and the body still refers to it:
   `grokking:fig:main` and `bounded:fig:intro` are reproduced in their
   wrappers, under the paper's own label, the way Section 4.3 describes.
8. **COGITAO's three upstream bugs no longer reach the thesis.** It is
    summarised rather than imported, so the `\label` without a `\caption` in
    `transformation_learnability.tex`, the `Figures` against `figures`
    mismatch that fails on a case sensitive filesystem, and the unclosed
    `itemize` in `6_appendix/Experiments.tex` are all out of the build. Kept
    here because wiring COGITAO back in brings all three back.

9. **A long `lstlisting` cannot be imported, and nothing needs to be now.**
    COGITAO's `6_appendix/LLM_Prompts.tex`, six `lstlisting` environments over
    177 lines, exhausted TeX's main memory in kaobook's output routine and the
    build produced no PDF at all. It compiles on its own in a short document,
    so testing it outside the thesis proves nothing. Remember the limit before
    importing any paper's long listing.

10. **The CNA bibliography is converted, not real.** Its 52 references came
    from `\bibitem` entries, so author and title are as good as a formatted
    string allows. Ask for the paper's original `.bib`.
11. **Overleaf should work, and nobody has run it there.** Checked on
    2026-11-16, and four of the five things that could have broken are ruled
    out. `build.sh` calls pdflatex and biber and nothing else, so no script
    runs at build time. All $56$ files under `generated/` are committed. No
    graphics file anywhere in the repository is untracked or ignored, so
    nothing the build reads is missing from a clone. And case sensitivity is
    settled rather than assumed, because this machine is Linux and the build
    passes on it; the one known problem, COGITAO's `Figures` against
    `figures`, left the build with the cut.

    What is left is the TeX distribution. This builds with TeX Live 2023 and
    biber 2.19, and Overleaf's version has to match biber to biblatex or
    biber refuses to run. Set it in the Overleaf menu, build once, and delete
    this item.

### Style

12. **No overfull hboxes.** The count was $101$ before the cut of
    2026-11-14, $30$ after it, $17$ after the survey was summarised, and $0$
    since the two math-heavy appendix files were set wide on 2026-11-16 with
    `\importpartwide` and `\importsectionwide`.

    ```bash
    uv run --no-project python scripts/check_layout.py --overfull
    ```

    `build.sh`'s `badboxes` count stays around $91$, because it counts
    underfull boxes and vboxes as well, and those are the ordinary cost of a
    narrow measure.

    The check that matters is not the log but the page: the maximum x of any
    word against the $595$pt paper width. No page of content now comes within
    $66$pt of the edge. The two float lists still report text past the edge
    and that is an artefact, because `trimclip` hides the end of a clipped
    entry and leaves it in the text layer.

13. **Three float list entries still clip.** Option 2 of
    `00_ADMIN/06_float_presentation_concept.md` is implemented in
    `thesis_import.sty`: inside a block `\caption` is patched to compute a
    short form, taking the contents of a leading `\textbf` group where the
    paper writes its claim in bold, and otherwise the first sentence, with a
    width guard so that an abbreviation such as "Fig." does not end the
    sentence early. The clipping in `thesis_style.tex` stays as the fallback
    and now fires on three entries of about $130$ rather than on all of them.

    Cross references are dropped from the short form, because a float list is
    an index and a reference there points at something the reader has not
    reached. That also keeps the attention paper's upstream-broken equation
    label from printing a second `??`, this time in the list of figures. The
    cost is a stray parenthesis in one clipped entry, where the reference sat
    inside brackets.

    The three that still clip are the cases Option 3 of that note exists for,
    which is a declared summary keyed by label. That needs the entry to be
    stashed at `\caption` and written at `\label`, and it has not been built.
    Two of the three open with a panel label rather than a claim.
14. **Table style is uniform enough, and the rest cannot be made uniform.**
    Checked on 2026-11-16. The four reproduced papers use booktabs
    throughout: not one `\hline` survives in the build, and the caption below
    the table was COGITAO's habit, which left with it. The $89$ against $39$
    count in the earlier version of this item was over all nine papers.

    What remains is the declared font size, `\footnotesize` and `\small` in
    the grokking appendix and neither in the attention one, and it cannot be
    fixed by declaring one size. `\ip@clamptables` wraps every table in an
    adjustbox with `max width=\linewidth`, which shrinks a wide table and
    leaves a narrow one alone, so the rendered size depends on the shrink
    factor and not on the declared size. Declaring a uniform size would
    change the shrink factors and not the result.
15. **Twelve captions out of 132 sit in the text block** rather than in the
    margin, because the float is too wide for a caption beside it and floatrow
    falls back. It is automatic and it looks right where it happens. Listed
    only so nobody reports it twice.
