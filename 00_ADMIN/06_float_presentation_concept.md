# Float presentation: list entries and a uniform table style

Two open questions about how the imported papers' figures and tables are
presented, with the measurements behind them and a recommended mechanism for
each. Written 2026-09-07. Nothing here is implemented yet.

## 1. The list of figures and the list of tables

### What is wrong

The two lists print each float's whole caption. The papers' captions run to
several sentences, so the lists became walls of text spanning eleven pages.

The measurement that matters: the papers contain **211 captions and not one of
them carries a short form**. LaTeX's own mechanism for this is
`\caption[short entry]{full caption}`, and the optional argument is used
nowhere, because a paper written for a conference has no list of figures to
keep short.

### Why the obvious fixes are not available

Adding the optional argument means editing the papers, which the thesis does
not do. Taking the caption apart after the fact does not work either: by the
time the entry reaches the list it has been through the label prefixing in
`thesis_import.sty` and through hyperref's link, so it is no longer text that
can be matched on.

### Option 1: clip the entry to one line

Currently implemented in `thesis_style.tex`. The entry goes into a box and
whatever does not fit on one line is clipped, with an ellipsis to mark it.

Rejected by the author: a truncation is not a summary. It cuts mid-sentence,
often mid-word, and the reader learns nothing from the fragment that survives.
It also reads as a fault rather than as a decision.

Worth keeping only as the last-resort fallback for an entry that no other rule
can shorten.

### Option 2: the caption's first sentence, computed at caption time

Inside an `importedpaper` block the caption is still an ordinary token list
when `\caption` receives it, before anything has wrapped it. At that point the
first sentence can be split off with a delimited macro and passed as the
optional argument.

This works because the papers' captions are mostly written claim-first: "The
grain prediction holds for all eight published rules, 8/8 in the branch." is
the whole of what the list needs.

Failure modes, all of which need a guard:

- An abbreviation ends the "sentence" early: `e.g.`, `Fig.`, `Eq.`, `et al.`,
  `approx.`, a decimal number, an initial in a name. Guard: reject a candidate
  shorter than about 25 characters and try the next period.
- A caption whose first sentence is itself three lines long. Guard: reject a
  candidate longer than about 110 characters and fall back to Option 1.
- Panel labels. A caption that opens "(a) Left: the ..." yields a first
  sentence that means nothing on its own. These are the cases Option 3 exists
  for.

Recommended as the default, because it needs no per float bookkeeping and so
survives a re import untouched.

### Option 3: declared summaries, keyed by label

For the floats where the first sentence reads badly, a hand written one line
summary in a table the thesis owns:

```toml
# imports/floatsummaries.toml
["acu:fig:intro"]
summary = "An ACU task and the three perspectives the survey is built on"

["grokking:tab:grain-sweep"]
summary = "Grain against grokking for the twelve rules"
```

The key is the label, because a label is the only identifier of a float that is
stable across a re import. Float numbers shift when a chapter moves and
graphics filenames do not exist for tables.

**The implementation problem.** `\caption` runs before `\label`, so at caption
time the label is not known yet and the entry has already been written.

**The fix.** Inside a block, patch `\caption` so that it does not write its
list entry immediately: it computes the Option 2 default, stashes the entry,
and lets the patched `\label` that follows resolve the key. `\label` already
goes through `thesis_import.sty`, so it is the natural place to look the
summary up and write the entry with it. Flush the stash at `\end{figure}` and
`\end{table}` so a float with no label still gets its default.

Failure modes:

- A float that writes `\label` before `\caption`. The stash is empty when the
  label arrives, so the float falls back to the default. Acceptable, and the
  checker can list them.
- `subfigure`, which nests captions. The stash has to be a stack, or nested
  captions have to be excluded from the mechanism entirely. Excluding them is
  simpler and loses nothing: a subfigure caption does not belong in the list
  of figures anyway.

### Checks this needs

`check_imports.py` should report, per paper:

- Every float whose list entry still exceeds one line after Option 2, so the
  ones that need a declared summary are a list rather than a discovery.
- Every entry in `floatsummaries.toml` whose label no longer exists, which is
  how a re import that renumbered or removed a float gets caught.
- Every declared summary alongside the first characters of the caption it
  replaces, so a re import that rewrote a caption is visible.

### TODO

1. Implement Option 2 with both guards, and measure how many entries still
   overflow one line.
2. Implement Option 3 for those, and write the summaries.
3. Add the three checks above.
4. Keep Option 1 as the fallback for anything that survives both.

## 2. A uniform table and figure style

Nine papers were typeset for nine templates. What follows is every dimension
along which they disagree, measured, with whether it can be settled from
outside the papers.

| Dimension | What the papers do | Settled from outside? | Recommendation |
| --- | --- | --- | --- |
| Horizontal rules | 89 `\toprule` against 39 `\hline` | Yes. Map `\hline` to `\midrule` inside the block. | Do it. booktabs everywhere. |
| Vertical rules | 10 column specs carry `\|` | Yes, but only by rewriting the spec, which is fiddly and easy to get wrong. | Leave. Ten tables is not worth a token level rewrite of column specs. |
| Table font size | ACU `\footnotesize` 42 times, attention `\small` 15 times, CNA and Hounsfield nothing at all | Yes. Set one size at the top of every `tabular` inside a block. | Set `\footnotesize`. It is what the widest tables already use and it reduces the scaling adjustbox has to apply. |
| Caption position | 5 tables above and 0 below in ACU, 0 above and 8 below in COGITAO | Yes, through `caption`'s `position` key. | Force above for tables, below for figures, which is the convention the other eight follow. |
| Caption placement | 120 of 132 in the margin, 12 in the text block where the float is too wide | Already automatic and already right. | Leave. |
| Row height | Global `\arraystretch` 1.18 | Already uniform. | Leave. |
| Column separation | Global `\tabcolsep` | Already uniform. | Leave. |
| Table width | adjustbox clamps to the measure, longtable is rotated | Already uniform. | Leave. |
| Figure width | Clamped to `\linewidth` and 0.85 `\textheight` | Already uniform. | Leave. |
| Numeric alignment | ACU and COGITAO use `siunitx` `S` columns, the rest align by hand | No. Retrofitting `S` columns means rewriting every column spec and every cell. | Leave, and say so. |
| Cell colour | ACU colours column groups, nobody else colours anything | Yes, but the colour carries meaning there. | Leave. |

Three of these are worth doing, and all three are one line each in
`thesis_import.sty`: the rule mapping, the font size, and the caption
position. The rest are either already uniform or cost more than they return.

`scripts/check_layout.py` already reports the caption position and the float
counts per paper, so the effect is measurable before and after.

### TODO

1. Map `\hline` to `\midrule` inside imported blocks.
2. Set one table font size inside imported blocks.
3. Force table captions above and figure captions below.
4. Re run `check_layout.py` and record the before and after in CLAUDE.md.
