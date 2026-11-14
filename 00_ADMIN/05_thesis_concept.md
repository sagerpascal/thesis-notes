# Thesis concept

**The settled story, as of 2026-11-14 (evening revision).** The arc was
reopened on 2026-09-12, settled once on 2026-11-14 as arc A, and revised the
same evening when two constraints came to light: the CNA code no longer runs
and no attention checkpoints survive, so the cross chapter measurements that
would have tightened the argument are not available, and the author reopened
which papers the thesis reproduces at all. Sections 12 and 13 of
[04_story_framings.md](04_story_framings.md) hold the reasoning. Everything
earlier in that file is retired.

## Working title

**Sparse or Distributed Is a Choice.** Subtitle: How the Learning Rule Decides
the Circuit a Network Learns, and What the Circuit Costs.

## Thesis in one sentence

Whether a computation is carried by a few neurons or spread across many is not
decided by the task but by how the learning rule assigns credit across
neurons, it can be read off the update equation and chosen, and the choice
trades robustness to damage against compressibility and speed of transfer.

## The spine

Neuroscience has asked for a century whether a representation is sparse,
carried by few cells, or distributed across many. A trained network poses the
same question, and the object that answers it is the set of neurons that carry
a computation, which this thesis calls the solution's circuit. The term is
defined once, in the introduction, definition before name.

Machine learning has mostly assumed the task decides. The grokking literature
reads the sparse circuit as what the task offers, and the universality claim
says every network solving a task finds the same one. This thesis shows the
task does not decide. The learning rule does, through how it assigns and
normalises credit across neurons, which is a credit assignment claim and so
sits in the institute's own subject.

The thesis is written for a committee at the Institute of Neuroinformatics.
That is why the question is posed as sparse against distributed coding rather
than as underdetermination of a loss, although the two are the same claim. The
machine learning literature it sits in is implicit bias and the conservation
laws of gradient flow, which varies the optimizer and asks which minimum is
reached. This thesis varies the credit assignment rule and asks how the
solution is laid out across neurons at the same minimum.

## The arc

Stake, finding, measurement, construction.

1. The stake. A survey of 87 papers and 33 datasets on agents for computer use
   finds one recipe and six gaps. Generalisation and sample efficiency are
   properties of the trained network, so the thesis asks what in training
   produces them. This is motivation and is called that. It is not evidence
   for the thesis claim.
2. The finding. With task, data, architecture and width fixed, every learning
   rule that groks modular addition recovers the same Fourier algorithm with
   circuits of different size. A neuron stays in use when its credit is large
   relative to the non gradient term of its own update. Equalising credit
   expands the effective circuit from 60% to 99% of the layer at width 256,
   including when switched on after grokking. Margin and parameter norm stay
   within a few percent, and mean test accuracy falls from 0.998 to 0.976, so
   this is not free and the thesis says the number wherever it says the
   headline. What an optimizer normalises together decides which neurons stay
   in use, which separates Nero from Adam, RMSProp, Muon, Shampoo and the
   others tested. The circuit
   has a price: distributed circuits tolerate neuron deletion, concentrated
   ones prune further and transfer about twice as fast. The same question
   asked of a Transformer's attention weights gives the same answer one level
   up, where the objective's index set decides whether a few columns dominate.
3. The measurement. A claim about a trained network is only as good as the
   readout behind it. The probe the field uses to score predicted latents is
   mostly reporting a quantity the loss never fixed, and re projection
   corrects it. This chapter states the standard the circuit claims are made
   to: matched loss, margin and weight norm, and imposed and permuted controls
   that the free quantity alone cannot satisfy.
4. The construction. If the rule decides the circuit and the circuit has a
   price, fix the circuit in the architecture and let learning fill in its
   parts. CNA represents a pattern by a net in which every active neuron is
   supported by several others, which is a distributed code by construction.
   Presented as a proposal, with what it shows and what it lacks.

## Research questions

1. Is the circuit of a learned solution fixed by the task or by the rule that
   assigned credit during training? (grokking, attention)
2. Can the circuit be predicted from the rule without training it, and can it
   be chosen? (grokking, attention)
3. What does a circuit cost? (grokking)
4. Does the readout used to make such a claim report the quantity it names?
   (world model)
5. Given that the rule decides the circuit and the circuit has a price, can
   the circuit be fixed by construction instead, and what would that buy?
   (CNA, as a proposal)

## Paper selection

Decided on 2026-11-14. Five papers are reproduced as full imported chapters.
Four are cut to one or two pages each in a single chapter, with the author's
role stated, which is the policy
[03_phd_thesis_outline.md](03_phd_thesis_outline.md) already set and which the
repository had drifted away from. The page figures are body plus appendix,
measured from the 367 page build of 2026-11-14.

| Paper | Role | Now | Decision |
| --- | --- | --- | --- |
| Grokking | first author | 42 pp | full chapter, pillar |
| Attention | shared first | 42 pp | full chapter |
| CNA | first author | 26 pp | full chapter, the proposal |
| ACU survey | shared first | 56 pp | full chapter, motivation only |
| World model | first author | 34 pp | chapter kept, appendix trimmed to 19 pp |
| COGITAO | tester | 54 pp with the LLM benchmark | summarise, 1 to 2 pp |
| LLM benchmark | evaluator | see above | summarise, 1 to 2 pp |
| Retrieval | first author | 16 pp | summarise, 1 to 2 pp |
| Hounsfield | shared first, framing | 12 pp | summarise, 1 to 2 pp |

The decisive number: COGITAO's appendix is 34 pages, the largest in the
thesis, against 32 for grokking, and the author's contribution to COGITAO was
testing one model. The cut saves roughly 76 pages and takes the thesis from
367 to about 290.

The world model paper is not yet submitted to Frontiers. Its chapter is
therefore kept short, its appendix trimmed to what the body refers to, and its
publication header box says what its status actually is on the day of
submission.

## Parts, chapters, files

| Part | Chapter | File | Label | Paper, role | Weight |
| --- | --- | --- | --- | --- | --- |
| I Introduction and Background | Introduction | `sections/1-1_introduction.tex` | `chap:introduction` | thesis owned | |
| | Background | `sections/2-1_related_work.tex` | `chap:background` | thesis owned, needs rewrite to the new story | |
| II The Stake | ACU survey | `sections/3-1_acu_survey.tex` | `chap:acu` | shared first with Benjamin Meyer | full chapter, motivation |
| | Further Contributions | `sections/3-2_further_contributions.tex` | `chap:further` | four papers, roles stated | 6 pp |
| III The Learning Rule Decides the Circuit | Grokking | `sections/4-1_grokking.tex` | `chap:grokking` | first author | pillar, leads the part |
| | Attention | `sections/4-2_attention.tex` | `chap:attention` | shared first, Matteo Saponati led | full chapter |
| IV Reading a Network Out | World model | `sections/5-1_bounded.tex` | `chap:bounded` | first author, unsubmitted | short chapter |
| V A Circuit Fixed by Construction | CNA | `sections/6-1_cna.tex` | `chap:cna` | first author | the proposal |
| VI Synthesis | Discussion, Conclusion | `sections/7-1_discussion.tex`, `sections/7-2_conclusion.tex` | `chap:discussion`, `chap:conclusion` | thesis owned | short |

The part order is the September one, so the file numbering matches the part
numbers again. The morning of 2026-11-14 briefly swapped Parts III and IV to
put measurement first, on the premise that the survey's evaluation gaps handed
off to it. Demoting the survey to motivation and shortening the world model
chapter removed that premise, so the swap was reverted the same day. Do not
swap them again without a reason that outlives one session.

`part:structure` is now `part:measurement`, titled "Reading a Network Out", and
`part:procedure` is "The Learning Rule Decides the Circuit".

The cut was carried out on 2026-11-14. The four summarised papers lost their
wrapper files and their appendix chapters, their manifests carry
`status = "summarised"` with a `summary_reason`, and nothing under
`imported_papers/` was touched. The thesis went from 369 pages to 281.

The world model appendix was trimmed in the same pass. Only its Literature
Survey section could go, 3 pages of 22, because the body points at the other
four and cutting a referenced section would print `??`. The survey backs the
paper's claim about 39 published evaluations, which lives in the paper's
introduction and so is not in the thesis. Where the chapter introduction uses
that number it cites the paper.

## What each chapter says, in one line

- ACU. One recipe, six gaps. Gaps one and two, generalisation and inefficient
  learning, are properties of the trained network.
- Grokking. Re-derived from the 2026-11-14 manuscript, "Grokking Can Be
  Steered: Selecting Desirable Solutions by Choice of Learning Rule". Learning
  rule varied, everything else fixed. Every rule that groks modular addition
  recovers the same Fourier based algorithm, implemented by circuits of
  different size. A neuron stays in use when its credit is large relative to
  the non gradient term of its own update, and that one condition unifies
  three routes to unused neurons: coupled weight decay, Adam's epsilon, and
  the decay of a trainable per neuron gain. Equalising credit across neurons,
  or scaling each neuron's weight decay by its credit, expands the effective
  circuit from 60% to 99% of the layer at width 256, including when switched
  on after grokking. The paper's own wording is "similar training and test
  accuracy": margin and parameter norm stay within a few percent and mean test
  accuracy falls from 0.998 to 0.976. The headline is width specific. At width
  32 the reference already uses 30 of 32 neurons and equalisation reaches 31,
  so there is nothing to redistribute, and at width 2048 the reference uses
  332 and the equalised network 2046, so the gap widens with width. Varying how many neurons share
  one equalisation factor, the circuit stays concentrated at groups of eight
  or more and distributes fully only at one factor per neuron. What an
  optimizer normalises together therefore decides: Nero normalises per neuron
  and distributes, Adam and seven others including RMSProp, Muon and Shampoo
  do not. The grain law survives as `eq:grainlaw` and `prop:grain`.
  Distributed circuits tolerate neuron deletion better, concentrated ones
  prune further and transfer about twice as fast to a task that recombines
  the same features, largely by recruiting their unused neurons.
- Attention. Objective varied, backpropagation fixed. Autoregressive training
  uses a token as context many times and as target once, so a few columns
  dominate. Bidirectional training enters each pair in both orders, so the
  update is symmetric and the structure spreads. Symmetric initialisation
  speeds up bidirectional training.
- World model. Re-derived from the 2026-11-14 Frontiers manuscript,
  "Correcting state-probe evaluation of world models for norm drift". A latent
  world model is scored with a state probe, a regressor fitted on encoded
  observations and then applied to predicted latents. During autoregressive
  rollout the norm of a predicted latent drifts while its direction stays
  accurate, and the probe is highly sensitive to the norm, so it reports
  mostly drift. In synthetic latents that store the state in their direction,
  a norm error of 5% per step compounds within a few dozen steps until the
  probe's error is 27 times that of always predicting the mean state, and when
  the norm varies independently of the true error the probe orders only about
  61% of latent pairs correctly against a chance level of 50%. Of 39 surveyed
  evaluations of predicted latents, one reports prediction norms. For TCRL on
  pendulum, rescaling the predictions to the norm of the encodings removes 97%
  of the probe's error at the end of the training horizon. A worse model that
  drifts less can therefore rank above a better one. The paper proposes re
  projection, rescaling each prediction to a reference norm taken from the
  encodings while keeping its direction, with four checks that test whether
  the re projected error reflects what the model predicts. It needs no
  retraining. This is a constructive correction to an evaluation protocol, not
  a cautionary result.
- Hounsfield. Input masks from tissue specific Hounsfield ranges buy accuracy
  and data efficiency against the same model without masks.
- Retrieval. Lexical search, dense retrieval and a cross encoder, first on the
  development set and third of 31 on the test set with no external data.
- CNA. A net is a set of neurons each supported by several others, assembled
  from Hebbian fragments. Noise without support is filtered at more than half
  the input corrupted, occluded figures are completed, fragments recombine into
  unseen patterns. Does not scale beyond line drawings.

## Guardrails

- The survey is motivation, not evidence. It is about agents operating
  software from natural language instructions, not about agents in the
  physical world, and it does not predict the grokking result. Say what it is
  and lean no weight on it.
- The world model chapter contains no circuit in the interpretability sense.
  It is the methodological chapter and is introduced as that. It is also not
  yet submitted, so do not describe it as published.
- The world model chapter is a constructive correction to an evaluation
  protocol, not a cautionary tale and not a failed paper.
- Robustness to damage (unit deletion, weight noise) is not robustness to a
  changing environment. The survey's deployment gap is about the latter. Never
  in one sentence.
- CNA does not measure participation and does not run the deletion protocol,
  and the code no longer runs, so no new CNA measurement is coming. Its link is
  the mechanism, redundancy of support, and is called that.
- No attention checkpoints survive, so the participation ratio measurement on
  attention weights that earlier drafts listed as optional glue is not
  available. Do not promise it.
- The attention paper does not compute participation on the attention weights.
  "Circuit across columns" is the thesis's reading of column dominance and is
  introduced as that.
- Universality fails at the circuit level is a grokking result. Do not extend
  it to attention or CNA.
- Never frame the thesis as non gradient rules being better. Backpropagation
  groks, its concentrated circuit transfers faster, and CNA does not scale.
- The grokking paper no longer claims that four of twelve rules never
  generalise, and no longer reports the one over square root of the effective
  unit count law for deletion. Do not cite either.
- The neuroscience framing is the spine, not decoration, but the thesis does
  not claim to model a brain. The outlook paragraph says so.
- Chapter introductions and summaries of the ACU chapter are still written for
  the old story and must be reframed.

## Optional thesis owned glue: withdrawn

Two cross chapter measurements were listed here as the way to turn the frame's
links into evidence: participation ratio over the attention weights of the
pretrained models, sharing the grokking chapter's measure, and unit deletion on
CNA nets with supporters per neuron as the effective count. Both are
withdrawn as of 2026-11-14. No attention checkpoints survive and the CNA code
no longer runs. Neither may be promised in the abstract, in a chapter
introduction or in the discussion. The links between the grokking chapter and
the other two stay what they are, an argument about a shared mechanism, and
the discussion says so plainly.

## Repository state after 2026-09-06

Done: title and parts in `main.tex`, both abstracts, the introduction,
skeleton discussion and conclusion, `imports/glossary.toml`, bib entries for
the author's papers and the background the introduction cites,
`sections/4-1_attention.tex` renamed to `4-2_attention.tex`,
`sections/5-1_koopman_jepa.tex` renamed to `5-1_bounded.tex`, an empty
`sections/5-1_grokking.tex`.

Vendored in parallel, by another session, on the same day: the grokking paper
at `imported_papers/grokking/docs/paper/` (the whole repository was copied,
only that subtree is the paper), the Koopman rewrite for TMLR at
`imported_papers/Koopman-JEPA-TMLR-rewrite/`, and COGITAO at
`imported_papers/COGITAO_ICML_2026/`. None has a manifest yet.

Open: everything in CLAUDE.md section 7.
