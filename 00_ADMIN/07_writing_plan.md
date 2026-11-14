# Writing plan

This file exists to stop prose being written early. Nothing at one level gets
written until the level above it has been criticised and has come through.

0. what the thesis claims, and what backs each part of it
1. titles
2. subtitles
3. one line per paragraph saying what that paragraph has to do
4. prose

Levels 0 and 1 were drafted on 2026-11-14 and criticised the same day by
three readers who were given the material and the standard but not the
reasoning. Their findings are at the end of this file, with what was done
about each. Level 0 below is the revised version. Two questions came out of
the critique that are the author's to answer, and they are in their own
section because the rest of the plan depends on them.

---

## Level 0: what the thesis claims

### The claim

With the task, the data, the architecture and the width held fixed, the rule
that assigns credit during training decides how far the computation spreads
over the available neurons. The task does not decide it. The condition that
keeps a neuron in use follows from the update equation, the ordering across
rules follows from that condition, and intervening on credit moves the spread
across its whole range. The move is not free. It costs two points of test
accuracy on modular addition, and it buys tolerance of neuron deletion while
giving up how far the network prunes and how fast it transfers.

Note what this does not say. It does not say the circuit can be predicted
before a network is trained. The grain law is calibrated: the paper assumes
lognormal initial contributions and fixes the log standard deviation from one
measured value, $0.602$, after which it reproduces $0.674$, $0.737$ and
$0.834$ against measured $0.623$, $0.695$ and $0.753$. That reproduces a
shape. It is not a prediction of a circuit from a rule alone, and CLAUDE.md
3.7 bans the claim in any case.

It also does not say the rule is the only thing that decides. Width matters
more for the untouched network: holding the rule fixed and growing the hidden
layer from $32$ to $2048$ takes reference participation from $0.937$ to
$0.162$. The honest shape of the result is that the rule decides how much of
the available width gets used, and that the effect grows with width rather
than shrinking. At width $32$ the reference already uses $30$ of $32$ neurons
and equalisation reaches $31$, so there is nothing to redistribute. At width
$2048$ the reference uses $332$ and the equalised network $2046$.

### The grokking study: where the claim comes from

First author. This is the chapter that establishes the claim, and the thesis
should say plainly that it is the one that does.

A neuron stays in use when its credit is large relative to the non gradient
term of its own update. That one condition covers three routes to unused
neurons which had no common account before: coupled weight decay, Adam's
$\epsilon$, and the decay of a trainable per neuron gain. Equalising credit
expands the effective circuit from $60\%$ to $99\%$ of the layer at width
$256$, and switching it on after grokking has already happened gives the same
expansion, so the rule holds the circuit open continuously. Margin and
parameter norm stay within a few percent. Mean test accuracy falls from
$0.998$ to $0.976$, and that number belongs next to the headline every time it
appears.

The strongest evidence is causal and the first draft of this plan left it out.
A credit profile is imposed on the network, and a random permutation drawn
once per run decides which neuron receives which magnitude, so the assignment
has nothing to do with what any neuron is doing. Circuit participation follows
the imposed value from $0.637$ to $0.990$, deletion tolerance rises with it,
and test accuracy stays above $0.96$.

On whether this is a toy. The first draft conceded that it was, which was both
wrong and expensive, because the paper already answers the objection. The same
condition governs the MLP units of a $30$M parameter language model trained
with Adam and L2 regularisation, where balancing each unit's decay leaves
$1.3\%$ of units nearly unused instead of $24\%$, at lower validation loss,
and AdamW leaves $0.9\%$. The redistribution also holds on modular subtraction
and multiplication, on permutation composition in $S_5$, on sparse parity and
on a transformer with a wide MLP. Modular addition is where the circuit can be
read neuron by neuron, which is why the detailed work is there.

### The attention study: a second determinant, not a second data point

Shared first author, led by Matteo Saponati.

The update to a Transformer's attention weights sums over whichever token
pairs the objective allows. Bidirectional training enters each pair twice,
once in each order, so the update stays symmetric. Autoregressive training
uses a token as context many times and as a target once, and a few columns end
up dominating. The paper checks this in ModernBERT, GPT, LLaMA3 and Mistral,
on text, vision and audio, and shows that symmetric initialisation speeds up
bidirectional training.

The first draft called this "the same question one level up" and it is not.
Backpropagation is held fixed here and the objective is varied, so the
determinant is the objective, which belongs to the task specification. The
measured object differs too: columns of a query key bilinear form, against the
participation ratio of outgoing weight norms over hidden units. Treating this
chapter as a second measurement of the grokking claim will not survive a
reader who has both chapters open. What it does establish is that a second
component of the training procedure leaves its own structure in the trained
weights, at a scale the grokking setting cannot reach. The frame should say
that and stop there.

### The world model study: the same kind of readout failure

First author, not yet submitted.

A probe is fitted on encoded observations and then applied to predicted
latents. During rollout the norm of a predicted latent drifts while its
direction stays accurate, and the probe responds to the norm. For TCRL on
pendulum, rescaling predictions to the norm of the encodings removes $97\%$ of
the probe's error at the end of the training horizon. A worse model that
drifts less can rank above a better one. Re projection rescales each
prediction to a reference norm taken from the encodings, and four checks test
what is left.

The first draft said this chapter "licenses" the controls the grokking chapter
uses, and that is a non sequitur. Those controls were designed in the grokking
paper and depend on nothing here. Deleting this chapter would not change one
of them.

There is a real link and it is worth building, because it is the only genuine
cross chapter argument in the thesis. Both chapters are about a readout that
responds to a degree of freedom the loss never constrains. In the world model
it is the norm of a latent. In the grokking study it is the rescaling gauge of
a ReLU unit: multiply a neuron's incoming weights and bias by a positive
constant, divide its outgoing weights by the same constant, and the function
is unchanged while the outgoing norm moves. The grokking paper raises this
itself and answers it with two measures tied to the computation, with the
deletion and pruning experiments, and with the permuted profiles. The
discussion should apply the world model chapter's four checks to the
participation measure and say which survive. That costs no new experiments and
it answers the hardest question in the viva before it is asked.

### The Cooperative Network Architecture: a convergence, not a consequence

First author. Published in Neural Computation, from a manuscript submitted in
2024. The grokking work is from 2026.

CNA represents a sensory pattern by a net in which every active neuron is
supported by several others, assembled from fragments learned by Hebbian
plasticity. The network filters noise, which nothing supports, even when more
than half the input is corrupted. It completes occluded figures. Fragments
learned separately recombine into patterns the network was never trained on.

The first draft presented this as the consequence of the grokking result, with
an if-then that runs from the rule to the architecture. The dates make that
impossible and the publication box prints them on the same page. What is true
is more interesting: an architecture designed earlier, for its own reasons,
builds in by construction the redundancy of support that a credit assignment
rule produces by training, and the two lines of work meet at that mechanism.
CNA does not measure participation, does not run the deletion protocol, and
the code no longer runs, so nothing will be added to it.

### The survey: motivation

Shared first author. One recipe, six gaps. Three of the gaps are properties of
the trained network, three concern how the field measures what it claims. It
does not predict the grokking result and the frame should never imply that it
does.

### What has to be admitted, in the frame

The first draft listed three and two of them were cheap. These eight are the
ones a reader will find anyway.

1. The headline intervention costs test accuracy, $0.998$ to $0.976$.
2. The central measure has a gauge freedom. Outgoing weight norms move under
   ReLU rescaling with the function unchanged. The paper checks this; the
   frame has to carry the check rather than the conclusion.
3. The rule is one determinant among several. Width alone moves reference
   participation from $0.937$ to $0.162$, and at width $32$ there is nothing
   for the intervention to do.
4. Two of the three prices follow from the measure rather than being
   discovered. A computation spread over more neurons survives random deletion
   better, and a circuit with more nearly unused neurons has more to prune.
   Faster transfer is the surprising one and deserves the room.
5. Among the optimizers in general use there is no choice on offer. Adam,
   Adam-mini, Lion, SGD with momentum, RMSProp, Muon and Shampoo all stay
   concentrated. Only Nero and DFC distribute, and only credit equalisation
   distributes fully. For the field as it stands the finding reads: every
   model you have is concentrated.
6. No measurement is shared across the chapters. Two were planned and are not
   available, because no attention checkpoints survive and the CNA code no
   longer runs.
7. "Universality fails" is not the finding. The literature's universality
   claim is about the algorithm, and every rule that groks recovers the same
   Fourier algorithm. The finding is that one algorithm admits implementations
   of very different size. Nobody claimed otherwise, so do not stage a
   refutation.
8. The word circuit is being used in a narrower sense than mechanistic
   interpretability uses it, where a circuit is a subgraph of components. Here
   it is a count of participating units derived from weight norms. Say so at
   the definition site.

### Three questions to prepare for the viva

1. Your own chapter on readouts says a probe can report a quantity the loss
   never fixed. Your circuit measure is a participation ratio of outgoing
   weight norms, weight decay acts on norms, and your intervention equalises
   per neuron magnitudes before you measure per neuron magnitudes. Apply your
   four checks to your own measure. What survives?
2. Holding the rule fixed and varying width moves participation further than
   holding width fixed and varying the rule. On what grounds does the title
   say the rule decides?
3. Take away the grokking paper. What is left of the claim?

Question 3 is the one that decides whether the committee reads this as a
thesis or as one paper with a long preamble. The answer has to be prepared,
and it has to be honest: the grokking study is where the claim is established,
and the other chapters are an independent structural result in a different
substrate, a methodological correction about readouts, and an earlier
architecture whose mechanism converges with the finding.

---

## Two questions for the author

Both came out of the critique, both reverse a decision taken earlier today,
and neither should be decided without the author.

### 1. Is the sparse against distributed framing earned, or is it a costume?

The examiner's case against it is specific and it is not easy to dismiss.
Sparse against distributed coding in neuroscience is a claim about how a
population represents stimuli, measured over a stimulus ensemble. The thesis
measures the participation ratio of outgoing weight norms in a hidden layer,
which the paper itself calls a structural measure. The three routes to unused
neurons that the chapter unifies are coupled weight decay, Adam's $\epsilon$
and a decaying per neuron gain, none of which has a counterpart in a brain.
Classical sparse coding derives sparsity from an explicit prior on an
efficient coding objective, where here it is an unintended effect of a
regulariser.

What is earned without argument is credit assignment, which is the
institute's own subject and is what the result is actually about. The concept
file currently says the framing was chosen because of the audience and that
the two framings are the same claim, which is an awkward sentence to have
written down if a committee ever reads it.

The options are to keep the framing and give it real weight, which means
confronting the three disanalogies above in the introduction, or to open on
credit assignment and underdetermination and keep sparse against distributed
as one declared analogy in the introduction and one paragraph in the outlook.
The second is safer. The first is the one the author chose this morning.

### 2. Does the survey keep 56 pages?

The cut of 2026-11-14 reduced COGITAO to two pages because the author's
contribution was testing one model, and reduced the retrieval paper to two
pages although the author is its first author. The survey is shared first
author, carries no evidential weight by the plan's own account, and keeps 56
pages, which is about a fifth of the body. No criterion written down anywhere
selects that outcome, and the one that fits is length. A reader who notices
that a first author paper was cut to two pages while a shared first paper with
no evidential role kept 56 will ask what the rule was.

Either give it a second role that is real, or cut it to the four to six pages
the others got.

---

## Level 1: titles

Revised after the title audit. The replacements adopted below fix agency,
unsupported scope, back references that name nothing, and metaphors standing
in for explanations.

### Abstract

No coined vocabulary at all, per CLAUDE.md 3.5, so the word circuit cannot
appear. The abstract puts it in plain words: how many of a network's neurons
end up carrying the computation.

### Introduction

1. The task leaves open how many neurons carry the computation
2. Two of the survey's six gaps are properties of the trained network, not of
   the task
3. The learning rule decides how many neurons carry the computation
4. The training objective decides which columns of an attention matrix
   dominate
5. Rescaling a predicted latent to the encodings' norm removes most of a state
   probe's error
6. The redundancy of support that a learning rule has to produce can be built
   into the architecture instead
7. Research questions
8. Contributions

Sections 7 and 8 stay as noun labels. CLAUDE.md 3.8 asks for statements, and
statement forms for these two come out worse than the labels, so the exemption
is taken deliberately and a line is added to 3.8 naming structural sections.
The former section 9, "Structure of the thesis", is cut: 3.8 bans roadmaps
without exception, and the six part titles already do that work.

One problem is not yet fixed. Sections 1 to 6 state six findings, section 7
restates them as questions and section 8 restates them as contributions, which
is the same finding three times inside one chapter. The research questions
have to be phrased as questions the chapters answer rather than as their
answers, and each contribution has to be one line.

### Background

Titled by what the literature covers, per CLAUDE.md 3.8, not by what the
thesis found.

1. Sparse and distributed coding is an old question, and the measures for it
   already exist
2. Many parameter settings fit the same data, and the procedure picks one
3. The training procedure has parts, and each of them can be varied
4. Grokking in modular addition gives a setting where the circuit can be read
   neuron by neuron
5. The same question arises for a weight matrix, where the training objective
   takes the place of the learning rule
6. A world model is scored through a probe, and the probe's own behaviour has
   rarely been checked
7. A circuit can also be built into the architecture rather than learned
8. The implicit bias literature has asked about norms, not about how many
   neurons carry the computation

Section 1 moves to the front only if question 1 above is answered in favour of
keeping the coding framing. If it is not, section 2 leads and section 1 shrinks
to a subsection.

### Chapter titles

- `chap:grokking`: Every Rule That Groks Recovers the Same Algorithm in
  Circuits of Different Size. The earlier proposal repeated the part title
  above it and read as a universal law.
- `chap:bounded`: Rescaling Predicted Latents to a Reference Norm Removes Most
  of a State Probe's Error. The earlier proposal generalised from one
  published model to all state probes and took the cautionary reading the
  concept file rejects.
- `chap:cna`: An Architecture of Mutually Supporting Neurons Filters Noise and
  Completes Occluded Figures. The earlier proposal claimed a distributed code,
  which CNA never measured, and said "without the rule", which is false
  because its fragments are learned by Hebbian plasticity.

---

## Critique record

### Round 1, 2026-11-14, three readers on levels 0 and 1

**Examiner.** Found that the central claim asserted the circuit could be
worked out without ever training the network, which the source paper
disclaims and CLAUDE.md 3.7 bans; that the determination
claim is contradicted by the paper's own width sweep; that the role given to
the world model chapter is a non sequitur while a real link sits unused; that
CNA is presented as a consequence of work that postdates it; that the plan
conceded the toy objection while the paper's language model appendix answers
it; that two of the three prices follow from the measure; and that the
admissions listed cheap items. Every factual claim in the report was checked
against the manuscript before being accepted. All were correct. The accuracy
cost and the width dependence were also wrong in `05_thesis_concept.md`, which
said "at the same accuracy", and that file was corrected.

Two recommendations are not adopted here because they reverse decisions the
author took and are escalated above instead: demote the coding framing, and
cut the survey.

**Title audit.** Found agency failures, scope claimed beyond the evidence,
back references that name nothing, two metaphors in titles, one epigram reused
as a section title, and the finding stated three times inside the
introduction. Adopted in full, except that sections 7 and 8 keep noun labels
by a recorded exemption.

**AI smell audit.** Found the mechanical screens clean and the shapes not:
nine antitheses, four label headings, three tricolons, five paper blocks built
to one template, a padded list of three, and a promised critique record that
did not exist. The mechanisable parts are now in `scripts/check_prose.py`,
which gained checks for label sentences, antithesis density, rhetorical
questions and personified abstractions. The rest was rewritten by hand.
