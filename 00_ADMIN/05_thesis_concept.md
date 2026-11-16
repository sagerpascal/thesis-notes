# Thesis concept

**The settled story, as of 2026-11-16.** The arc was reopened on 2026-09-12,
settled once on 2026-11-14 as arc A, and revised the same evening when two
constraints came to light: the CNA code no longer runs and no attention
checkpoints survive, so the cross chapter measurements that would have
tightened the argument are not available, and the author reopened which papers
the thesis reproduces at all. Sections 12 and 13 of
[04_story_framings.md](04_story_framings.md) hold the reasoning. Everything
earlier in that file is retired.

**The spine changed on 2026-11-16.** The thesis was framed for one day as
sparse against distributed coding. A critique of the writing plan made the case
that the framing is borrowed rather than earned: the measure is structural
rather than a coding measure over a stimulus ensemble, and the three routes to
unused neurons that the thesis unifies are coupled weight decay, Adam's
epsilon and a decaying gain, none of which has a counterpart in a brain. The
author chose credit assignment instead. Sparse against distributed survives as
one declared analogy in the introduction and one paragraph in the outlook, and
the participation measure is still borrowed from that literature and is said to
be. What changed is which claim the thesis is making, not which results it
reports.

## Working title

**The Learning Rule Decides How Much of a Network Carries the Computation.**
Subtitle: Credit Assignment, and What a Task Leaves Open in a Trained Network.

Three constraints shaped it. The title page comes before every definition
site, so the title carries no coined vocabulary. The verb is scoped to the
fraction of available width, because width alone moves reference participation
from $0.937$ to $0.162$ and a bare "decides" claims sole determination the
evidence does not support. And the subject is the learning rule rather than
credit assignment, because twelve learning rules were varied while only one
credit assignment algorithm other than backpropagation survives the
comparison. Credit assignment is the subject the thesis is about and it sits
in the subtitle, where the introduction's definition can reach it.

Alternatives, if the committee wants something shorter: "What a Task Leaves
Open", with everything else in the subtitle, and "Credit Assignment Decides
How Far a Computation Spreads", which is the stronger sentence and the weaker
claim.

## Thesis in one sentence

A task fixes what a network computes and leaves open how much of the network
carries it, the rule that assigns credit during training fixes that, the
condition deciding it can be read off the update equation and intervened on,
and the choice trades tolerance of damage against how far the network prunes
and how fast it transfers.

## The spine

A task and a loss fix what a network computes. They do not fix how that
computation is laid out across the network's parts. Several structural
properties of a trained network are left open, and something settles each one
that the person who chose the task never chose. Which part of the training
setup settles which property, and what each settlement costs, is the subject
of this thesis.

One distinction has to be made in the introduction and made once, because the
whole spine rests on it. A task is what the network is asked to compute. A
training objective is a particular loss written to get it there, and in the
attention chapter the objective is what varies. So the objective is on the
near side of the line and the task on the far side, and the sentence saying so
belongs at the definition site, not in a chapter introduction four parts
later.

The property studied in depth is how far a computation spreads over the
neurons available to it, which this thesis calls the solution's circuit. The
term is defined once, in the introduction, definition before name, and in a
narrower sense than mechanistic interpretability uses it: here it is a count of
participating units derived from weight norms, not a subgraph of components.

The determinant is credit assignment. A neuron stays in use when the credit it
receives is large relative to the non gradient term of its own update, which is
a property of the rule and not of the task. That is a credit assignment claim
and so sits in the institute's own subject. The literature it answers to is the
implicit bias of training procedures and the conservation laws of gradient
flow, which varies the optimizer and asks which minimum is reached. This thesis
asks a different question about the minimum: not how large the weights are, but
over how many neurons the computation is spread.

Machine learning has mostly assumed the task decides. The grokking literature
reads a concentrated circuit as what the task offers, and the universality
claim says every network solving a task finds the same one. The algorithm is
indeed the same. The number of neurons implementing it is not, and it is the
rule that sets it.

The other chapters take other properties. The training objective, not the
learning rule, decides whether a Transformer's attention weights stay
symmetric or a few columns come to dominate, which is a second component of
the training setup fixing a second structural property. The norm of a
predicted latent is a quantity the loss never constrains at all, and the probe
the field uses to score predicted latents responds to it, so a readout can
report a free quantity in place of the one it names. The Cooperative Network
Architecture asks what happens if the structure is fixed in the architecture
instead of being left to the procedure.

Sparse against distributed coding is an analogy and is declared as one. The
participation ratio this thesis measures comes from that literature and the
introduction says so. The claim itself is not a claim about brains, the
measure here is structural rather than taken over a stimulus ensemble, and the
mechanisms unified here have no counterpart in a brain. The analogy gets one
paragraph in the introduction and one in the outlook, and carries no weight in
between.

## The arc

Stake, finding, measurement, construction.

1. The stake. A survey of 87 papers and 33 datasets on agents for computer use
   finds a field converging on one recipe, and six gaps. Four are about how
   the field measures and deploys. Two are about what training produced, and
   the thesis asks what in training produces them. Planning is the one the
   survey splits between the model and the machinery around it, and the thesis
   measures neither. This is motivation and is called that. It is not evidence
   for the thesis claim. Summarised in six thesis owned pages as of
   2026-11-16, not reproduced.
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
   ones prune further and transfer about twice as fast. A second determinant
   is then established in a different substrate and at a scale the grokking
   setting cannot reach. Holding backpropagation fixed and varying the
   objective, the index set the update sums over decides whether a
   Transformer's attention weights stay symmetric or a few columns dominate.
   That is the objective fixing a structural property, not a second
   measurement of the credit assignment claim, and the frame says so.
3. The measurement. Some quantities are left free by the loss altogether, and
   a readout can report one of those in place of the quantity it names. The
   probe the field uses to score predicted latents responds mostly to the norm
   of a predicted latent, which the loss never constrains, and re projection
   corrects it. The chapter is a constructive correction to an evaluation
   protocol. It also sets the standard this thesis's own measure is held to,
   and the discussion applies its four checks to the participation measure.
4. The construction. The last chapter asks what it would mean to fix the
   structure in the architecture instead of leaving it to the procedure. CNA
   represents a pattern by a net in which every active neuron is supported by
   several others. It was submitted in 2024 and the grokking work is from
   2026, so it is a convergence on one mechanism, redundancy of support, and
   not a consequence of the finding. Presented as a proposal, with what it
   shows and what it lacks.

## Research questions

1. How much of a trained network's width carries the computation, and what
   sets the number? (grokking)
2. Can the condition that keeps a neuron in use be read off the update
   equation? (grokking)
3. Can the circuit be chosen by intervening on credit? (grokking)
4. What is given up when a computation is spread over more neurons, in test
   accuracy, in tolerance of neuron deletion, in how far the network prunes
   and in transfer speed? (grokking)
5. Does the training objective fix a structural property of a Transformer's
   attention weights, at a scale the modular arithmetic setting cannot reach?
   (attention)
6. Does a readout used to make claims about a trained network report the
   quantity it names, or one the loss left free? (world model)
7. Does a structural measure of a trained network report the structure, or a
   quantity the training procedure left free? (world model and grokking)
8. Can redundancy of support be built into an architecture instead of produced
   by training? (CNA, as a proposal)

Question 7 is the only one two chapters bear on, and it is new as of
2026-11-16. It costs no experiments: the world model chapter's four checks are
applied to the participation measure in the discussion, and the answer is
partly uncomfortable, because the measures tied to the computation put the
reference at $0.343$ and $0.422$ where the structural measure puts it at
$0.602$. It converts the thesis's weakest point, that no measurement is shared
across chapters, into its one integrative claim. Do not drop it to tidy the
list.

Question 2 asks whether the condition can be read off the update equation. It
does not ask whether a circuit can be predicted from a rule before training.
The grain law is calibrated from one measured value and reproduces a shape
from there, CLAUDE.md 3.7 bans the stronger claim, and an earlier wording of
this question made it. Do not restore it.

Questions 1 to 4 are the grokking paper's contributions reworded, and a
committee that opens the paper will see the mapping. That is what a lead paper
in a cumulative thesis looks like, and the frame says so rather than
disguising it.

The survey has no research question, and after the cut of 2026-11-16 it does
not need one. It sets the stake in six pages and carries no evidence, which is
what the chapter now says of itself.

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
| ACU survey | shared first | 56 pp | summarise, 6 pp, the stake (cut 2026-11-16) |
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
| II Today's Agents Share One Recipe, and Two of Their Gaps Are About Training | ACU survey | `sections/3-1_acu_survey.tex` | `chap:acu` | shared first with Benjamin Meyer | summarised, 6 pp, the stake |
| | Further Contributions | `sections/3-2_further_contributions.tex` | `chap:further` | four papers, roles stated | 6 pp |
| III The Learning Rule and the Objective Each Leave Their Own Structure in the Weights | Grokking | `sections/4-1_grokking.tex` | `chap:grokking` | first author | pillar, leads the part |
| | Attention | `sections/4-2_attention.tex` | `chap:attention` | shared first, Matteo Saponati led | full chapter |
| IV What the Loss Leaves Free Can Dominate a Readout (`part:readout`) | World model | `sections/5-1_bounded.tex` | `chap:bounded` | first author, unsubmitted | short chapter |
| V Mutual Support Can Be Built into an Architecture Rather Than Left to the Learning Rule | CNA | `sections/6-1_cna.tex` | `chap:cna` | first author | the proposal |
| VI Synthesis | Discussion, Conclusion | `sections/7-1_discussion.tex`, `sections/7-2_conclusion.tex` | `chap:discussion`, `chap:conclusion` | thesis owned | short |

The part order is the September one, so the file numbering matches the part
numbers again. The morning of 2026-11-14 briefly swapped Parts III and IV to
put measurement first, on the premise that the survey's evaluation gaps handed
off to it. Demoting the survey to motivation and shortening the world model
chapter removed that premise, so the swap was reverted the same day. Do not
swap them again without a reason that outlives one session.

`part:structure` became `part:measurement` and is now `part:readout`, titled
"What the Loss Leaves Free Can Dominate a Readout". CLAUDE.md 3.9 requires the
label and the part to stay in step, and "measurement" no longer named it.
`part:procedure` is "The Learning Rule and the Objective Each Leave Their Own
Structure in the Weights". Part III went through three titles on 2026-11-16.
It was named for the learning rule alone, which covered only the first of its
two chapters; then for the circuit, which the attention chapter never
measures; then for the training procedure, which rested on a boundary between
task and procedure that the introduction decided not to draw. The title it has
names the two components instead. Part V lost "circuit" for the same reason as
Part III's second title: CNA computes no participation ratio, and the
guardrails below forbid extending the term to it. It lost "instead of trained"
as well, because CNA's fragments are learned by Hebbian plasticity, and what
is not trained is how they are joined.

The survey was cut on 2026-11-16, after the question was put to the author.
It keeps a chapter of its own and six thesis owned pages, because the
authorship is shared first, the source runs to over fifty pages, and the
thesis takes its question from this work. Its imported body and its appendix
chapter left the build, and `00_ADMIN/07_writing_plan.md` holds the paragraph
plan the chapter was written to and the critique that corrected it. Five
papers are now summarised and four reproduced.

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
- The attention paper does not compute participation on the attention weights,
  and "circuit across columns" was a misreading of its measure. Column
  dominance means that columns of high norm are more common than rows of high
  norm, which is an asymmetry between the row space and the column space, not
  a concentration of the computation on a few columns. The misreading was in
  five thesis owned sentences and was removed on 2026-11-16. There is no
  spread against concentration axis in that chapter, which is the cleaner
  position: it removes the temptation to read the chapter as a second circuit
  measurement.
- Universality fails at the circuit level is a grokking result. Do not extend
  it to attention or CNA.
- Never frame the thesis as non gradient rules being better. Backpropagation
  groks, its concentrated circuit transfers faster, and CNA does not scale.
- The grokking paper no longer claims that four of twelve rules never
  generalise, and no longer reports the one over square root of the effective
  unit count law for deletion. Do not cite either.
- The reference setting is Adam with L2 added to the gradient, and the
  manuscript says plainly that this "serves here to test the condition at
  scale and not as a recommended setting". Under AdamW the reference is
  already distributed on modular addition, on MNIST, on the canonical
  transformer, in the wide transformer with decay on weight matrices only, and
  in the language model. Never write that the models the field trains are
  concentrated. The condition is general and bites wherever a non gradient
  term dominates a neuron's update, and two of the three such terms are live
  under AdamW: Adam's $\epsilon$ in a wide transformer whose normalisation
  parameters are decayed, and the decay of a trainable per neuron gain.
- Credit participation does not order circuit participation across optimizers.
  Lion and credit equalisation both sit at credit participation $1.000$ and
  land at $0.535$ and $0.992$. What follows from the condition is whether a
  rule changes each neuron's ratio of credit to its non gradient term, which
  only per neuron normalisation does.
- Sparse against distributed coding is a declared analogy, not the spine. It
  gets one paragraph in the introduction, where the three disanalogies are
  named, and one in the outlook. The participation measure is borrowed from
  that literature and the borrowing is stated. Nothing in between leans on it,
  and the thesis does not claim to model a brain.
- The attention chapter is a second determinant, not a second measurement of
  the credit assignment claim. Backpropagation is held fixed there and the
  objective is varied, and the measured object is columns of a query key
  bilinear form rather than a participation ratio over hidden units.
- CNA predates the grokking work. Call it a convergence on one mechanism, not
  a consequence of the finding. The publication boxes print both dates.
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
