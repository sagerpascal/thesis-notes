# Thesis concept

The settled story, as of 2026-09-06. The framings that were tried and rejected,
and why, are in [04_story_framings.md](04_story_framings.md). This file is the
one to read before writing any thesis owned prose.

**Under review since 2026-09-12.** The author proposed a different arc, built
around the world model paper having become an evaluation paper, and wants it
compared against the story below before more frame prose is written. It is
section 10 of [04_story_framings.md](04_story_framings.md). Nothing here is
retired yet.

## Working title

**Sparse or Distributed Is a Choice.** Subtitle: How Training Decides the
Layout of a Neural Network's Solution, and What the Layout Costs.

Alternative kept in reserve: Few Neurons or Many: What Decides How a Network
Lays Out Its Solution. The title is not final.

## Thesis in one sentence

Among the many networks that solve a task equally well, how the solution is
spread across neurons is decided by the training procedure and not by the task,
it can be read off the update equation and chosen, and the choice trades
robustness to damage against speed of adaptation.

## The spine

A network that has learned a task could have laid its solution out in many
ways. The same function, at the same loss, margin and weight norm, can be
carried by a few neurons or spread across all of them, and a weight matrix can
concentrate a computation on a few columns or spread it evenly. The way a
computation is distributed over a network's parts, whether neurons or the rows
and columns of a weight matrix, is the solution's layout. That term is defined
once, in the introduction, definition before name.

Neuroscience has argued about sparse against distributed coding for decades.
Machine learning has mostly assumed the task decides the layout: the grokking
literature reads the sparse circuit as what the task demands, and the
universality claim says every network solving a task finds the same circuit.

## The arc

Findings, then method, then proposal.

1. Agents built from foundation models are the stake. The survey shows the
   field builds them by one recipe and lacks efficient learning and
   generalisation. Those are properties of the trained network, so the thesis
   asks what in training decides them.
2. The central study finds that a quantity nobody in the recipe varies, the
   learning rule, decides the layout of the solution, and that the layout
   decides how the network survives damage and how fast it adapts. Asked of a
   Transformer's attention weights, the same question gives the same answer
   one level up: the objective decides whether a few columns carry the
   computation.
3. Structure supplied from outside the data has to be measured against a
   predictor that learns nothing. The world model study is the cautionary
   instance. The Hounsfield and retrieval studies pass their controls.
4. If the rule decides the layout and the layout has a price, fix the layout in
   the architecture and let learning fill in its parts. CNA is the first
   implementation of that proposal, presented as a proposal, with what it
   shows and what it lacks. The world model the PIs care about is the far end
   of the same proposal.

## Research questions

1. Is the layout of a learned solution fixed by the task or by the procedure
   that trained the network? (grokking, attention)
2. Can the layout be predicted from the training rule without training it, and
   can it be chosen? (grokking, attention)
3. What does a layout cost? (grokking)
4. Given that the rule decides the layout and the layout has a price, can the
   layout be fixed by construction instead, and what would that buy? (CNA, as
   a proposal)

The survey frames why 1 to 3 matter for agents. Part IV supplies applied
instances of structure from outside the data and one cautionary measurement.
Neither tests the questions.

## Parts, chapters, files

| Part | Chapter | File | Label | Paper, role | Weight |
| --- | --- | --- | --- | --- | --- |
| I Introduction and Background | Introduction | `sections/1-1_introduction.tex` | `chap:introduction` | thesis owned | |
| | Background | `sections/2-1_related_work.tex` | `chap:background` | thesis owned, needs rewrite to the new story | |
| II Agents Built by One Recipe | ACU survey | `sections/3-1_acu_survey.tex` | `chap:acu` | shared first with Benjamin Meyer | pillar |
| | LLM benchmark and COGITAO | `sections/3-2_llm_benchmark.tex`, `sections/3-3_cogitao.tex` | `chap:llmbench` | evaluation only, one model only | short |
| III The Training Procedure Decides the Layout | Grokking | `sections/4-1_grokking.tex` | `chap:grokking` | first author | pillar, leads the part |
| | Attention | `sections/4-2_attention.tex` | `chap:attention` | shared first, Matteo Saponati led | full chapter |
| IV Structure Supplied from Outside the Data | World model | `sections/5-1_bounded.tex` | `chap:bounded` | first author, judged not strong | short, summarised unless published |
| | Hounsfield | `sections/5-2_hounsfield.tex` | `chap:hounsfield` | shared first, framing | short |
| | Retrieval | `sections/5-3_retrieval.tex` | `chap:retrieval` | first author | short |
| V A Layout Fixed by Construction | CNA | `sections/6-1_cna.tex` | `chap:cna` | first author | pillar, the proposal |
| VI Synthesis | Discussion, Conclusion | `sections/7-1_discussion.tex`, `sections/7-2_conclusion.tex` | `chap:discussion`, `chap:conclusion` | thesis owned | short |

Each of the three papers the author drove leads its own part.

## What each chapter says, in one line

- ACU. One recipe, six gaps. Gaps one and two, generalisation and inefficient
  learning, are properties of the trained network.
- Grokking. Rule varied, everything else fixed. Four of twelve rules never
  generalise. The rule decides how many neurons carry the solution at equal
  loss, margin and norm. The grain law predicts eight of eight optimizers. The
  credit knob moves the layout from the start or after grokking. Fluctuation
  under deletion falls as one over the square root of the effective unit
  count. Concentrated solutions adapt about twice as fast.
- Attention. Objective varied, backpropagation fixed. Autoregressive training
  uses a token as context many times and as target once, so a few columns
  dominate. Bidirectional training enters each pair in both orders, so the
  update is symmetric and the structure spreads. Symmetric initialisation
  speeds up bidirectional training.
- World model. A scale invariant loss leaves latent scale free, a spectral
  constraint fixes its growth, the probe reads that as learning. Trivial
  predictors beat every learned model. The controls that expose this are the
  ones every layout claim rests on.
- Hounsfield. Input masks from tissue specific Hounsfield ranges buy accuracy
  and data efficiency against the same model without masks.
- Retrieval. Lexical search, dense retrieval and a cross encoder, first on the
  development set and third of 31 on the test set with no external data.
- CNA. A net is a set of neurons each supported by several others, assembled
  from Hebbian fragments. Noise without support is filtered at more than half
  the input corrupted, occluded figures are completed, fragments recombine into
  unseen patterns. Does not scale beyond line drawings.

## Guardrails

- Robustness to damage (unit deletion, weight noise) is not robustness to a
  changing environment. The survey's deployment gap is about the latter. Never
  in one sentence.
- CNA does not measure participation or run the deletion protocol. Its link is
  the mechanism, redundancy of support, and is called that.
- The attention paper does not compute participation on the attention weights.
  "Layout across columns" is the thesis's reading of column dominance and is
  introduced as that.
- The world model chapter is about scale, not layout. It enters as the general
  concept, a property the loss leaves free, of which layout is the thesis's
  main instance.
- Universality fails at the layout level is a grokking result. Do not extend
  it to attention or CNA.
- Never frame the thesis as non gradient rules being better. Backpropagation
  groks, its concentrated solution adapts faster, and CNA does not scale.
- The neuroscience outlook is one paragraph, at the end of the CNA chapter and
  in the discussion, with the sentence that the thesis does not build it.
- Chapter introductions and summaries of the ACU chapter are still written for
  the old story and must be reframed.

## Optional thesis owned glue

1. Participation ratio over the columns and rows of the attention weights for
   the pretrained models of the attention chapter. One figure, one measure
   shared with the grokking chapter. Low effort, needs the checkpoints.
2. Unit deletion on CNA nets, with supporters per active neuron as the
   effective unit count. Moderate effort, needs the CNA code.

Neither is promised in the abstract until it exists.

## Repository state after 2026-09-06

Done: title and parts in `main.tex`, both abstracts, the introduction,
skeleton discussion and conclusion, `imports/glossary.toml`, bib entries for
the author's papers and the background the introduction cites,
`sections/4-1_attention.tex` renamed to `4-2_attention.tex`,
`sections/5-1_koopman_jepa.tex` renamed to `5-1_bounded.tex`, an empty
`sections/4-1_grokking.tex`.

Vendored in parallel, by another session, on the same day: the grokking paper
at `imported_papers/grokking/docs/paper/` (the whole repository was copied,
only that subtree is the paper), the Koopman rewrite for TMLR at
`imported_papers/Koopman-JEPA-TMLR-rewrite/`, and COGITAO at
`imported_papers/COGITAO_ICML_2026/`. None has a manifest yet.

Open: everything in CLAUDE.md section 7.
