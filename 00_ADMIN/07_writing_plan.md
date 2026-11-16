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
about each. Two questions came out of that critique that were the author's to
answer. The first was answered on 2026-11-16: the spine is credit assignment,
not sparse against distributed coding. Level 0 and Level 1 below are written
to that answer. The second is still open and is in its own section.

---

## Level 0: what the thesis claims

### The shape of the argument

A task and a loss fix what a network computes and leave the layout of that
computation open. Each chapter takes one property left open that way. Credit
assignment decides how far a computation spreads over the neurons available,
and that pair is studied in depth. The training objective decides whether a
Transformer's attention weights stay symmetric. The norm of a predicted latent
is left free entirely, and a state probe reports it in place of the state. CNA
fixes the structure in the architecture rather than leaving it to training.
What each settlement costs is asked in every case.

`05_thesis_concept.md` carries this in full and is the file to read. It is not
restated there and here.

One objection the frame has to survive. The objective is not something other
than the objective, so the attention chapter is not an instance of a task
leaving a property open. What it shows is that a second component of the
training setup leaves its own structure in the weights. Part III's title
covers both chapters only if the introduction says, in one sentence at the
definition site, what a task is in this thesis and what a procedure is. Write
that sentence before the part title has to be defended.

### The claim

With the task, the data, the architecture and the width held fixed, the rule
that assigns credit during training decides how far the computation spreads
over the available neurons. The task does not decide it. The condition that
keeps a neuron in use follows from the update equation, and intervening on
credit moves the spread from the reference to full distribution. The move is not free. It costs two points of test
accuracy on modular addition, and it buys tolerance of neuron deletion while
giving up how far the network prunes and how fast it transfers.

Note what this does not say. It does not say the circuit can be predicted
before a network is trained. The grain law is calibrated: the paper assumes
lognormal initial contributions and fixes the log standard deviation from one
measured value, $0.602$, after which it reproduces $0.674$, $0.737$ and
$0.834$ against measured $0.623$, $0.695$ and $0.753$. That reproduces a
shape. It is not a prediction of a circuit from a rule alone, and CLAUDE.md
3.7 bans the claim in any case.

It does not say the condition orders the rules. Table `tab:zoo` refuses that.
Lion and credit equalisation both have credit participation $1.000$ and land
at circuit participation $0.535$ and $0.992$, and across the eight optimizers
credit participation ranges from $0.478$ to $1.000$ while circuit
participation stays between $0.470$ and $0.613$. What follows from the
condition is a binary. Does the rule change each neuron's ratio of credit to
the non gradient term of its own update? Nero and credit equalisation do, per
neuron. The other seven normalise over groups larger than a neuron and cannot.

It also does not say the rule is the only thing that decides. Width matters
more for the untouched network: holding the rule fixed and growing the hidden
layer from $32$ to $2048$ takes reference participation from $0.937$ to
$0.162$. The rule decides how much of the available width gets used, and the
effect grows with width. At width $32$ the reference already uses $30$ of $32$
neurons and equalisation reaches $31$, so there is nothing to redistribute. At
width $2048$ the reference uses $332$ and the equalised network $2046$. The
claim holds where there is width to spend and says nothing at width $32$.

Normalised participation and effective count move in opposite directions here,
and the frame carries both or neither. From width $128$ to $512$ the
reference's participation falls from $0.791$ to $0.400$ while its effective
count grows from $101$ to $205$. A reader can propose from this that the task
selects a circuit of roughly fixed functional size and that the rule only
decides how much idle width sits around it. Nothing in the manuscript refutes
that reading. Prepare an answer rather than a sentence.

Two settings where the intervention has nothing to do are in the manuscript's
own scope table and belong in the frame. On MNIST the reference is at $0.99$
and equalisation leaves it at $0.99$. On the canonical transformer both are at
$0.96$. The mechanism needs a concentrated reference before it has anything to
redistribute.

### The grokking study: where the claim comes from

First author. This is the chapter that establishes the claim, and the thesis
says so.

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

The strongest evidence is causal. A credit profile is imposed on the network,
and a random permutation drawn once per run decides which neuron receives
which magnitude, so the assignment has nothing to do with what any neuron is
doing. Circuit participation follows the imposed value from $0.637$ to
$0.990$, deletion tolerance rises with it, and test accuracy stays above
$0.96$.

Whether this is a toy. The condition itself reaches scale: it governs the MLP
units of a $30$M parameter language model trained with Adam and L2
regularisation, where balancing each unit's decay leaves $1.3\%$ of units
nearly unused instead of $24\%$, at lower validation loss. The redistribution
holds on modular subtraction and multiplication, on permutation composition in
$S_5$, on sparse parity and on a transformer with a wide MLP. What does not
reach scale is the rest of the claim. At the scale of the language model there
is no deletion comparison beyond one column, no transfer experiment and no
pruning, so circuit size is not shown there to be a steerable quantity with a
measured price. Claim the condition at scale and the price in the small
setting, separately. Modular addition is where the circuit can be read neuron
by neuron, which is why the detailed work is there.

### The attention study: a second determinant, not a second data point

Shared first author, led by Matteo Saponati.

The update to a Transformer's attention weights sums over whichever token
pairs the objective allows. Bidirectional training enters each pair twice,
once in each order, so the update stays symmetric. Autoregressive training
uses a token as context many times and as a target once, and a few columns end
up dominating. The controlled evidence is twelve layer transformers trained in
both encoder and decoder modes on Jigsaw, Wikipedia and Red Pajama, with
median symmetry and directionality measured across epochs. Cite those first.
The cross family comparison in ModernBERT, GPT, LLaMA3 and Mistral, across
text, vision and audio, is observational and comes second. Symmetric
initialisation follows from the derivation and speeds up bidirectional
training.

Backpropagation is held fixed here and the objective is varied, so the
determinant is the objective. The measured object differs too: columns of a
query key bilinear form, against the participation ratio of outgoing weight
norms over hidden units. This chapter is not a second measurement of the
grokking claim. What it establishes is that a second component of the training
setup leaves its own structure in the trained weights, at a scale the grokking
setting cannot reach. The frame says that and stops there.

Two cautions. The mechanism is the index set the update sums over, and in a
decoder that set is realised by a causal mask, which is architecture. "The
objective decides" is the paper's framing and the thesis may adopt it, but it
is a framing, and a thesis whose spine rests on the boundary between task,
architecture and procedure cannot be casual about which side this falls on.
Second, a reader will ask what separates a task from an objective in this
thesis, having read that the task does not decide in one chapter and that the
objective decides in the next. One sentence, at the definition site.

### The world model study: the standard the measure is held to

First author, not yet submitted.

A probe is fitted on encoded observations and then applied to predicted
latents. During rollout the norm of a predicted latent drifts while its
direction stays accurate, and the probe responds to the norm. For TCRL on
pendulum, rescaling predictions to the norm of the encodings removes $97\%$ of
the probe's error at the end of the training horizon. A worse model that
drifts less can rank above a better one. Re projection rescales each
prediction to a reference norm taken from the encodings, and four checks test
what is left.

The link to the grokking chapter is the only cross chapter argument the thesis
has, and it has to be stated as a standard rather than as a parallel. Not that
both chapters are about a readout responding to a free degree of freedom: that
is a metaphor doing an argument's work, and it is also false in one direction,
because the ReLU rescaling gauge is a symmetry of the loss and coupled decay
pins it, whereas the latent norm really is loose and drifts. What is true is
that this chapter sets a standard for readouts, and the discussion holds the
participation measure to it. Running the four checks honestly:

- The support check has no analogue. Drop it or invent one and say so.
- The radius check does transfer, and it costs something. The measures tied to
  the computation put the reference at $0.343$ and $0.422$ where the
  structural measure puts it at $0.602$. The direction survives and the level
  does not. Budget for the concession rather than presenting the exercise as
  an answer.
- Probe agreement transfers. Three measures, same direction, different levels.
- Null controls transfer, and they are strong: permuted credit profiles,
  the outgoing norm constraint, and from scratch training as the transfer
  baseline.

Nero belongs in this paragraph. Because it holds each neuron's incoming weight
norm fixed, its participation cannot come from scale moving between a neuron's
incoming and outgoing weights.

One further observation worth taking seriously. The world model paper is
explicit that the objective decides whether the norm is free at all: TCRL uses
a cosine loss that ignores the norm, while squared error and SimNorm keep it
in check. Read that way, this chapter is a second instance of the attention
chapter's claim rather than a third category, and Parts III and IV would share
a claim instead of an umbrella. That reading is available and has not been
taken. Decide before the discussion is written.

### The Cooperative Network Architecture: a convergence, not a consequence

First author. Published in Neural Computation, from a manuscript submitted in
2024. The grokking work is from 2026, and the publication boxes print both
dates on the same page, so no claim running from the rule to the architecture
is available.

CNA represents a sensory pattern by a net in which every active neuron is
supported by several others, assembled from fragments learned by Hebbian
plasticity. The network filters noise, which nothing supports, even when more
than half the input is corrupted. It completes occluded figures. Fragments
learned separately recombine into patterns the network was never trained on.

The link is one mechanism. CNA builds redundancy of support into its
architecture, and credit equalisation produces redundancy of support by
training. The chapter is presented as a proposal that reached the same
mechanism by another route. CNA does not measure participation, does not run
the deletion protocol, and the code no longer runs, so nothing will be added
to it.

### The survey: motivation

Shared first author. One recipe, six gaps: insufficient generalisation,
inefficient learning, limited planning, low task complexity in benchmarks, non
standardised evaluation, and a disconnect between research and practical
conditions. Two of the six are properties of the trained network, the first
two. Limited planning is a property of the scaffold around the model rather
than of the trained network, and the last three concern how the field measures
and deploys what it builds. An earlier version of this file said three and
three, which the survey refuses and which contradicted the concept file. It
does not predict the grokking result and the frame should never imply that it
does.

### What has to be admitted, in the frame

Nine, and a reader will find every one of them in the manuscript.

1. The headline intervention costs test accuracy, $0.998$ to $0.976$.
2. The central measure has a gauge freedom. Outgoing weight norms move under
   ReLU rescaling with the function unchanged. Two answers exist and the frame
   carries both. The measures tied to the computation put the reference lower
   than the structural one does, at $0.343$ activation weighted and $0.422$ by
   ablation against $0.602$, rising to $0.813$ and $0.801$ under equalisation.
   So the direction survives and the level does not, and $60\%$ to $99\%$ is
   the gauge sensitive pair of numbers. The second answer is Nero, which holds
   each neuron's incoming weight norm fixed, so its participation of $0.986$
   at test accuracy $0.985$ cannot come from scale moving between a neuron's
   incoming and outgoing weights. That is one distributed circuit which
   provably is not a gauge artefact, and it was produced by an optimizer
   rather than by the intervention. It is the cleanest answer to the gauge
   objection in the manuscript and the frame should use it.
3. The rule is one determinant among several. Width alone moves reference
   participation from $0.937$ to $0.162$, and at width $32$ there is nothing
   for the intervention to do. On MNIST and on the canonical transformer the
   reference is already distributed and the intervention changes nothing.
4. Two of the three prices follow from the measure rather than being
   discovered. A computation spread over more neurons survives random deletion
   better, and a circuit with more nearly unused neurons has more to prune.
   Faster transfer is the surprising one, and its scope is narrow enough that
   the frame states the scope with the number. The advantage appears for
   targets that need new hidden combinations of the operand frequencies and
   not for targets that change only the readout. On multiplication every
   pretrained network is slower than training from scratch, $1800$ to $2020$
   epochs against $1200$. The distributed circuit at $1540$ epochs is itself
   slower than from scratch at $1410$.
5. The concentration is produced by a coupling, and the field's default
   already avoids it. The reference adds L2 to the gradient before Adam.
   Loshchilov and Hutter described that coupling and the paper cites them for
   it. Under AdamW the paper's own numbers read the other way: the reference
   is distributed in both kinds of measure on modular addition, $0.96$ against
   $0.91$ at the end of training; the wide transformer with decay on weight
   matrices only, "as in most current training code", sits at $0.82$; the
   canonical transformer at $0.96$; MNIST at $0.99$; and the language model
   has fewer than $1\%$ nearly unused units. The manuscript says plainly that
   "Adam with L2 serves here to test the condition at scale and not as a
   recommended setting", and its limitations say the residual AdamW effect is
   "not explained by the condition". An earlier version of this list said the
   opposite, that every model in the field is concentrated. That is false and
   would not have survived ten minutes of a viva. The claim that does survive:
   the condition is general, it bites wherever a non gradient term dominates a
   neuron's update, and coupled L2 is one such term among three. The other two
   are live under AdamW. Adam's $\epsilon$ dominates in a wide transformer
   whose normalisation parameters are decayed, and the decay of a trainable
   per neuron gain does the same in a layer normalised net.
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
9. One credit assignment algorithm other than backpropagation survives the
   comparison, which is DFC. Feedback alignment, direct feedback alignment and
   sign-SGD do not generalise and are excluded. Everything else varied is an
   optimizer. The thesis therefore has $n = 1$ on the axis its title names
   unless the introduction defines credit assignment to cover how an optimizer
   distributes credit across neurons, which is what the condition is about and
   what the measure measures. Write that definition or change the title.

### Questions to prepare for the viva

1. Your reference adds L2 to the gradient before Adam. Your own appendix shows
   that with decoupled decay the reference is already distributed, $0.91$ on
   modular addition, $0.82$ in the wide transformer with decay on weight
   matrices only, $0.96$ on the canonical transformer, $0.99$ on MNIST, and
   under $1\%$ dead units in your language model. Your limitations say the
   residual AdamW effect is not explained by the condition. Loshchilov and
   Hutter described this coupling and you cite them for it. Is the thesis
   about how credit assignment decides circuit size, or about what happens
   when you keep using an optimizer configuration the field replaced?
2. Your circuit measure is a participation ratio of outgoing weight norms,
   weight decay acts on norms, and your intervention equalises per neuron
   magnitudes before you measure per neuron magnitudes. Apply your own four
   checks to your own measure. What survives?
3. You are examined at an institute whose own work on credit assignment is
   deep feedback control, and your comparison contains one credit assignment
   algorithm other than backpropagation. Everything else you vary is an
   optimizer, and your abstract says Nero wins because it normalises per
   neuron. On this evidence, why is the title not about the optimizer?
4. Your appendix says the AdamW reference has nearly equal outgoing norms and
   prunes to about as few neurons as the Adam reference. One network your
   measure calls distributed and one it calls concentrated reduce to the same
   minimal circuit. In what sense is the computation spread over more neurons
   in one of them, and which number is the finding, $0.60$ or $0.343$?
5. Holding the rule fixed and varying width moves participation further than
   holding width fixed and varying the rule, and the effective count grows
   from $101$ at width $128$ to $332$ at $2048$, sublinearly. Why is this not
   a task selecting a circuit of roughly fixed functional size, with the rule
   deciding only how much idle width sits around it?
6. Take away the grokking paper. What is left of the claim?

Questions 1, 3 and 4 are the three hardest and none of them was on the list
before 2026-11-16. Question 1 is answerable and the answer is admission 5.
Question 3 is answerable only by the definition demanded in admission 9.
Question 4 is answerable in numbers, by the activation weighted and ablation
measures together with Nero, and not by a sentence saying the paper checks it.

Question 6 decides whether the committee reads this as a thesis or as one
paper with a long preamble. The answer has to be honest: the grokking study is
where the claim is established, and the other chapters are an independent
structural result in a different substrate, a methodological correction about
readouts, a survey that sets the stake, and an earlier architecture whose
mechanism converges with the finding.

## Decision record and one open question

### 1. The spine is credit assignment. Decided 2026-11-16.

The thesis was framed for one day as sparse against distributed coding, on the
grounds that the committee sits at an institute of neuroinformatics. The
examiner's case against it was specific. Sparse against distributed coding is
a claim about how a population represents stimuli, measured over a stimulus
ensemble. The thesis measures the participation ratio of outgoing weight norms
in a hidden layer, which the source paper itself calls a structural measure.
The three routes to unused neurons that the chapter unifies are coupled weight
decay, Adam's $\epsilon$ and a decaying per neuron gain, none of which has a
counterpart in a brain. Classical sparse coding derives sparsity from an
explicit prior in an efficient coding objective, where here it is an
unintended effect of a regulariser. The concept file had also written down
that the framing was chosen for the audience and that the two framings are the
same claim, which is an awkward sentence to leave where a committee might read
it.

Credit assignment needs no analogy to carry it. The condition the grokking
chapter derives compares a neuron's credit against the non gradient term of
its own update, so credit assignment is what the result is about and what the
participation measure measures. The three disanalogies above do not apply to
it, because nothing has been borrowed.

What follows from the decision:

- The title and subtitle change, and so do two part titles. Part III is now
  the training procedure rather than the learning rule, because its second
  chapter varies the objective.
- The introduction opens on underdetermination rather than on coding.
- The background leads with underdetermination. Sparse and distributed coding
  shrinks to a subsection, placed where the participation measure is
  introduced, because that is what the thesis actually takes from it.
- Sparse against distributed keeps one paragraph in the introduction, which
  names the three disanalogies above, and one in the outlook. Nothing in
  between leans on it.
- No result changes, and no chapter changes role.

### 2. Does the survey keep 56 pages? Still open.

The cut of 2026-11-14 reduced COGITAO to two pages because the author's
contribution was testing one model, and reduced the retrieval paper to two
pages although the author is its first author. The survey is shared first
author, carries no evidential weight by the plan's own account, and keeps 56
pages, which is about a fifth of the body. No criterion written down anywhere
selects that outcome, and the one that fits is length. A reader who notices
that a first author paper was cut to two pages while a shared first paper with
no evidential role kept 56 will ask what the rule was.

Either give it a second role that is real, or cut it to the four to six pages
the others got. Nothing below depends on the answer, so the writing continues
either way.

## Level 1: titles

Revised after the title audit, then again on 2026-11-16 when the spine
changed. The replacements fix agency, unsupported scope, back references that
name nothing, metaphors standing in for explanations, and the introduction
stating its findings three times.

### Abstract

No coined vocabulary at all, per CLAUDE.md 3.5, so the word circuit cannot
appear. The abstract puts it in plain words: how many of a network's neurons
end up carrying the computation. "Credit assignment" is not coined by this
thesis and is glossed inline at first use, which the title page makes
necessary anyway.

### Introduction

Restructured on 2026-11-16, for two reasons. The spine changed, and the title
audit had found a problem the first revision did not fix: six sections each
stated a finding, a seventh restated them as questions and an eighth restated
them as contributions, which is the same finding three times inside one
chapter. CLAUDE.md 3.8 says a finding is stated once in full, in its chapter,
and that the introduction gives the one sentence version. So the introduction
now sets up, asks, and answers in one line each, and states nothing in full.

1. The task and the loss leave open how far a computation spreads over a
   network's neurons
2. A survey of agents for computer use finds six gaps, and two of them are
   properties of the trained network
3. Credit assignment fixes how far a computation spreads, and the training
   objective fixes a structure of its own
4. Research questions
5. Contributions

Section 1 is the definition site and carries four things that the rest of the
thesis assumes and that nothing later can repair. The word circuit, definition
before name, with the note that it is narrower here than in mechanistic
interpretability. What credit assignment means in this thesis, which has to
cover how an optimizer distributes credit across neurons, or admission 9
stands unanswered. What separates a task from a training objective, or Part
III's title covers neither of its chapters. And the declared analogy to sparse
and distributed coding, one paragraph, naming the three disanalogies rather
than asserting the parallel.

Section 2 was a finding title built on the same contrast as section 1, and it
referred back to a survey the reader of page 3 has not met. It is now a
statement about what a survey found. It may yet be folded into the end of
section 1: the ordering runs question, aside, answer, and 3.8 asks that each
section connect to the result of the one before. Decide when the prose is
written, not now.

Section 3 names the determinant. "Different parts of the training procedure
fix different structural properties" announced plurality where 3.7 asks the
thing to be named.

Sections 4 and 5 stay as noun labels, under the exemption now written into
CLAUDE.md 3.8. The former section 9, "Structure of the thesis", is cut: 3.8
bans roadmaps without exception, and the six part titles already do that work.

Each research question is a question the chapter answers, phrased so that the
answer is not in it. Each contribution is one line and names its chapter.

### Background

Titled by what the literature covers, per CLAUDE.md 3.8, not by what the
thesis found. Reordered on 2026-11-16: underdetermination leads, and sparse
and distributed coding is now a subsection rather than the opening section.
Retitled the same day, because five of the seven were built to one mould, two
named nothing, and one stated the thesis's own setup as a finding.

This list is the Level 1 plan. The chapter as written has eight sections, not
seven, and the titles below were revised again on 2026-11-16. What follows is
what `sections/2-1_related_work.tex` prints.

1. Many parameter settings fit the same data, and the procedure picks one
2. Credit assignment algorithms and optimizers have been compared on
   convergence and accuracy
3. In modular addition the grokked solution has been read neuron by neuron
4. How far a computation spreads has been measured in neuroscience, and the
   measures disagree
5. The two pretraining objectives differ in which token pairs enter the update
6. A world model is scored through a probe, and the probe's own behaviour has
   rarely been checked
7. Mutual support between neurons has been built into architectures rather
   than trained
8. Unused neurons have been described one mechanism at a time, and never as a
   quantity a rule sets

The coding material was promoted from a subsection of section 3 to section 4
of its own, with the reason recorded in the file: the measures and the
ablation literature are not coding-framing content, and the thesis's own
price results sit against them. The neuroscience framing stays inside it as
one subsection and is declared as the analogy it is.

The gap section was retitled because its earlier title claimed no literature
had asked the question, which the grokking paper's own related work refutes.

Section 7 is the chapter's gap, which 3.8 asks for at the end. It is not the
implicit bias gap: that one already exists as a subsection in the file, at
`sec:bg_biasgap`, and promoting it would open and close the chapter on the
same literature with five sections in between.

The coding subsection sits under section 3 rather than opening the chapter,
because what the thesis takes from that literature is the measure and not the
question. Putting it where the measure is introduced makes the borrowing
visible and keeps it from reading as a claim about brains.

One thing not done. Sections 3 to 6 are ordered by chapter rather than by what
is varied, so the chapter reads as a list keyed to the thesis's own structure
where 3.8 asks related work to read as one argument. Grouping by what is
varied would use the same material and the same 121 citation keys. It is a
Level 2 decision and it is recorded here so it is taken rather than inherited.

### Part titles

Set in `main.tex` on 2026-11-16. Parts III, IV and V changed, because two of
them applied the word circuit to chapters whose papers never measure one,
which the concept file's own guardrails forbid in prose.

| | Title | Label |
| --- | --- | --- |
| I | Introduction and Background | `part:background` |
| II | The Field Is Converging on Foundation Models, and Two of Its Gaps Are About Training | `part:agents` |
| III | The Learning Rule and the Objective Each Leave Their Own Structure in the Weights | `part:procedure` |
| IV | What the Loss Leaves Free Can Dominate a Readout | `part:readout` |
| V | Mutual Support Can Be Built into an Architecture Rather Than Left to the Learning Rule | `part:construction` |
| VI | Synthesis | `part:synthesis` |

I and VI are noun labels under the exemption now written into CLAUDE.md 3.8.
Part II still sits over the survey and over the four summarised papers, only
one of which is about agents. The title now claims only what the survey
establishes, and the four short papers sit under it as further contributions,
which the introduction says.

### Chapter titles

All five set in the files on 2026-11-16.

- `chap:acu`: A Survey of Agents for Computer Use Finds Six Gaps, and Two Are
  About What Training Produced. It was "Agents for Computer Use: A
  Comprehensive Survey", which is the published title and a colon label, and
  then briefly "One Recipe Builds Agents for Computer Use", which asserts a
  recipe the survey says the field is still converging on. The published title
  stays in the publication box and in the bibliography, where it belongs.
- `chap:grokking`: The Learning Rule Decides How Many Neurons Carry a Grokked
  Solution. The plan had proposed "Every Rule That Groks Recovers the Same
  Algorithm in Circuits of Different Size", which spends its first six words
  on the part of the result nobody disputes, reaches the finding in a trailing
  phrase against 3.2's result first, and universally quantifies over rules
  where the evidence is twelve.
- `chap:attention`: The Training Objective Decides Whether Attention Weights
  Stay Symmetric. It was "...Decides the Circuit of the Attention Weights",
  and the measured object is columns of a query key bilinear form.
- `chap:bounded`: Rescaling Predicted Latents to a Reference Norm Removes Most
  of a State Probe's Error. It was the previous paper's finding entirely.
- `chap:cna`: An Architecture of Mutually Supporting Neurons Filters Noise and
  Completes Occluded Figures. It was the architecture's name.

### The abstract is the next liability, and it is worse than a rewrite

Both abstracts still argue the retired story, and the English one breaks rules
the thesis cannot break. Its header comment claims no coined vocabulary, which
is false: it uses "layout" as a term, which is the retired frame term; it
names "net" before defining it; and it uses "effective neuron count" with no
gloss, in the one place CLAUDE.md 3.5 allows no coined vocabulary at all. It
says the choice "can be read off the procedure's update equation before the
procedure is run", which is the construction 3.7 bans by name.

Two of its claims are no longer in the manuscripts. It says four of twelve
rules never generalise and that the deletion fluctuation shrinks as one over
the root of the effective neuron count. The concept file's guardrails record
both as withdrawn. Its fifth paragraph describes the bounded operator paper
that the Frontiers norm drift paper replaced. The German abstract mirrors all
of it.

So the abstract is not waiting on a style pass. It states two withdrawn
results and describes a paper that is no longer in the thesis. It is rewritten
at Level 4 with everything else, and until then nothing should be quoted from
it.

## Level 3 for `chap:acu`: the survey cut to six pages

Decided 2026-11-16, answering the second escalated question. The survey keeps
a chapter of its own and six pages. Its imported body and its appendix chapter
leave the build. The first draft of this plan was criticised the same day and
one of its two claims was refuted by the survey; what follows is the revision.

**Why a chapter of its own, rather than a fifth section of `chap:further`.**
Four reasons, and the chapter gives them rather than asserting the status.
Shared first authorship on a JAIR survey. Fifty-six pages of source against
twelve to twenty for the others. The introduction leans on this chapter and on
no other in Part II. And a survey is a different kind of object from a study:
it is where the thesis's question comes from. Six pages against the four that
the other four papers have **between them** is four to six times the per paper
allowance, so the asymmetry is argued, not smuggled in as parity.

**The cut is also a correctness fix.** Every thesis owned paragraph in the
current wrapper argues the retired story, and its six gap list is embellished
past the survey. "Relying on world models whose predictions diverge
exponentially with rollout length", "the absence of structural priors" and
"systems cannot recombine familiar components in novel configurations" are
none of them in the survey; the last is COGITAO's result. Write the six gaps
from `sections/09_conclusion.tex`, never from the current wrapper. There is
also no challenges section to work from: `sections/08_challenges.tex` is 27
bytes and reads `% MOVED THIS TO APPENDIX!!!`, and the current chapter imports
it.

### What the chapter claims, and what the survey will not support

The first draft sorted the six gaps four ways: two properties of the trained
network, planning a property of the scaffold around it, three about
measurement and deployment. The survey refuses the middle term.
`05_agent_perspective.tex:372` says "LLMs exhibit limited long-horizon
planning capabilities", naming the model first; `:343` has specialised agents
doing "implicit planning in their latent space"; and conclusion recommendation
(c) is "advancing policy architectures that support long-horizon reasoning and
planning", where the policy is the network. Only the second remedy, hybrid
symbolic planning, sits outside the model. A singleton category that exists so
the thesis faces two unexplained gaps instead of three is the sort working for
the thesis rather than reporting the survey, in the one chapter whose
guardrail says to lean no weight on it. Drop it. The word "scaffold" is
dropped with it: it is coined nowhere, is in no glossary entry, and collides
with the survey's own "conceptual scaffold" for the taxonomy.

The sort is two ways, which is what `sections/1-1_introduction.tex` already
says and what the concept file says. Two gaps are about what training
produced. The other four are not what this thesis is about. Planning is named
as the one the survey splits between the model and the machinery around it,
and the thesis measures neither.

Two honesty requirements that the first draft missed, both of which make the
chapter better rather than weaker.

The survey's own diagnosis for gap one is the input modality, not the network:
conclusion (1) reads "reliance on structurally inconsistent input modalities
that hinder generalization", and the remedy is to change what the agent
observes. The thesis's reading runs through the survey's own aside that agents
on such representations "may develop scenario-specific heuristics (shortcuts,
cp. Geirhos et al.) that do not generalize well beyond the training data",
which is a property of what training produced. That sentence is quoted and the
reading is declared as a reading. The survey offers the brittleness as a
hypothesis, so the chapter may not report it as a finding.

Gap two is an equivocation waiting to happen. The survey means cost: learning
strategies that are "highly resource-intensive, requiring either high-fidelity
simulation environments or curated and labeled datasets", with recommendation
(b) asking for "cost-efficient learning strategies". Sample efficiency is one
component of that cost and is the component the thesis takes. Say which
component in one sentence, or the chapter equivocates on "inefficient" in the
sentence that licenses research question 4.

One more correction. "The field builds those agents by one recipe" overstates,
and so does the current chapter title. The survey says the field is
transitioning, and its own counts refuse the present tense: 35 of 87 agents
use textual observations against 31 image and 15 bi-modal, and 30 of 87 do no
environment learning at all. The introduction already has the honest verb,
"the field is converging on one recipe", and the chapter may not assert more
than the introduction does. Likewise the image trend is growth, not
replacement: image observations go from 0 to 12 to 19 across 2022 to 2024
while textual stays flat at 3, 10, 8.

**Chapter title.** Was "One Recipe Builds Agents for Computer Use, and Six
Gaps Are Shared Across Them", which asserts the overstated recipe and a
sharing the survey never claims. Now: "A Survey of Agents for Computer Use
Finds Six Gaps, and Two Are About What Training Produced". It states the
chapter's one claim, which is the sort.

### The six pages

About $2400$ words. A page of this thesis carries $400$ to $470$ words, and
`3-2_further_contributions.tex` runs $1408$ words over four pages. The first
draft of this plan budgeted twelve paragraphs and a list, which is $1300$ to
$1650$ words and fills four pages, not six. The additions below are the
missing two.

**Publication header box.** Kept, in the APA form the reproduced chapters use,
because this chapter keeps a `publicationbasis` and a `contributionstatement`
while the four short summaries in `chap:further` carry their citation in
running prose. The difference is deliberate and the reason is the four above.
Check `references/manual.bib` first: `acu_survey` has `pages = {34}`, which is
a JAIR article number rather than a page, and the box prints "85, 34".

**Contribution statement.** Keep the first four paragraphs, which are factual
and were written against the author list. Replace the last, which claims the
thesis framing reads the gaps as symptoms of structural limits in the learning
paradigm. The replacement states what this chapter's framing does: it sorts
the six gaps by whether they are about what training produced, and declares
the reading of gap one as a reading.

**Opening.** No roadmap paragraph: CLAUDE.md 3.8 bans them by name, and the
first draft opened with one whose whole content was the chapter's length and
status. No second definition of an agent for computer use either, because
`sections/1-1_introduction.tex` already defines it and 3.5 allows one site
thesis wide. Open on the stake in a number, which the survey supplies and the
first draft did not have: agents reach "almost six time lower success rates
than humans", from failures on dynamic interfaces, on switching between
applications, and in dense interfaces such as spreadsheets.

**What the survey covers**, and what it does not.
1. Scope and the exclusions, with the reason in the same sentence per 3.5:
   no chatbots that only advise, no video game agents, no server control, no
   coding agents, no software testing, text instructions only, and fully
   disclosed systems only, which leaves out the commercial products a reader
   of 2026 will think of first.
2. How the 87 were chosen, and that this is not a systematic review: the field
   "lacks a unified terminology, making a classic systematic review
   infeasible", so the collection was iterative and semi-structured with
   snowball sampling to saturation, two reviewers and a consensus discussion.
   About a third of the cited works are preprints, which the survey says may
   lack validation.
3. The taxonomy, and why a technology agnostic one was needed: it is what lets
   reinforcement learning agents and prompting based agents be compared in one
   scheme, which the existing surveys could not do because each covered one
   technology or one platform. This is the paper's claim to novelty and gets
   a sentence of its own.
4. What the taxonomy does not do, sourced rather than asserted: no capability
   comparison across agents, because agents support different benchmarks and
   report different metrics; no analysis of how design choices affect
   performance; text instructions and static interaction patterns only.

**What the field builds.** Two paragraphs: the converging recipe, and the
three trends with the counts that qualify them.

**The six gaps.** One list from the conclusion, each two sentences, stated
once in full here and nowhere else in the thesis. Gap six is marked as the
survey's own addition rather than a literature finding, because the conclusion
says limitation (6) and recommendation (f) "concern real-world discrepancies
that are not addressed in the current literature". The deployment gap is wider
than a changing environment: non-stationarity, privacy, cost, availability and
safety under conditional autonomy.

**The six recommendations**, (a) to (f), in one short paragraph. Contribution
four of the paper is "the proposal of strategic directions to address these
challenges", and a chapter that lists the gaps and drops the directions
reports half the paper.

**The sort, and the hand off.** Three paragraphs, not five. The sort; why the
survey cannot settle the two it hands over, which is not that it never varies
the training procedure, since it classifies 87 agents by learning strategy,
but that it never varies the procedure with task, data, architecture and width
held fixed; and the hand off. The guardrails go in one sentence each at the
end of the paragraph they belong to, the way `3-2_further_contributions.tex`
does it, not in paragraphs of their own. A quarter of a chapter spent
disclaiming one's own survey reads as anxiety, and 3.7 asks for limitations
plain rather than apologetic.

The guardrail about damage tolerance against environment tolerance is not in
this chapter at all. The deletion protocol first appears two chapters later,
so no reader of Part II can yet make the confusion. It belongs in the grokking
chapter or the discussion, where it is possible.

### Consequences of the cut

- `imports/acu.toml` takes `status = "summarised"` and a `summary_reason`, and
  its `[appendix]` table is emptied. `check_imports.py` skips coverage for a
  summarised paper, so no drop entries are added.
- The `app:acu` chapter leaves `sections/appendix.tex`, and with it the three
  fifteen column agent tables that `\importsectionrotated` exists for. The
  feature stays in `thesis_import.sty`: it is the only way a published table
  too wide for the measure gets set, and the next paper that needs it will.
- The reproduced overview figure goes with the block, and with it one of
  `check_imports.py`'s reproduction notes. Nothing refers to it once the body
  is gone.
- Part II is retitled to cover both of its chapters.
- `sections/3-2_further_contributions.tex` becomes false in its first
  paragraph: "Four further publications" is five, and "the five papers the
  argument rests on" is four. Both are fixed.
- `00_ADMIN/05_thesis_concept.md` contradicts the cut in three places, the
  paper selection table, the parts table and arc item 1, and its open question
  about the survey is closed by it.
- CLAUDE.md section 4.9 says five reproduced and four summarised, which is now
  four and five.
- `sections/1-1_introduction.tex` says "Four of the six can be closed by
  building harder benchmarks and agreeing on how to score them", which is
  false of gap six and was false of gap three under the retired sort. The file
  is rewritten under item 0 and the line is fixed there.
- Nothing under `imported_papers/` changes. Wiring the survey back in is
  setting `status = "wired"` and restoring the includes.

**Measured after the cut, 2026-11-16.** The thesis went from 281 pages to
229 as measured then, the overfull hboxes from 30 to 17, and the chapter from 56 pages to 5.
Zero LaTeX errors, zero duplicate labels, zero missing bibliography keys, the
one upstream `??`, `check_imports.py` at zero errors and four warnings, and
`check_prose.py` at zero hard findings across 18 files. The chapter's one soft
finding is "comprehensive" in the published title, which CLAUDE.md 3.4 carves
out by name. Nothing under `imported_papers/` was touched.

Five pages rather than six. The plan budgeted about $2400$ words and the
chapter runs about $2000$, which is where the material ran out without
padding. The additions the critique asked for are all in.

### The finished chapter was checked and rewritten once

A fourth reader checked the written chapter against the vendored survey and
found fourteen accuracy problems, one of them a real error that had also
reached the frame. $87$ is the number of agents the survey classifies, not the
number of papers it read, which is larger: "we classify \numagents as ACU
agents and \numdatasets as computer use datasets". The slip was in the
abstract in both languages and twice in the introduction, and all five are
fixed.

The other thirteen were overstatements, each corrected against a quoted line.
The chapter had said the paper's own warrant for gap six was that the first
five are "discussed throughout the field", where the paper says "throughout
the main text", meaning its own body. It had said every earlier survey covers
one technology or one platform, where the paper names one of similar scope and
claims depth against it. It had given the second location of the planning
difficulty as machinery around the model, where the survey says the
environment, whose dynamics are unknown. It had asserted a recipe the field
converges on, where the survey says the field "has yet to converge on a
unified framework" about how agents learn, so the claim is now scoped to the
model class. It had drawn the gap two distinction as if the survey stopped at
pipeline cost, where recommendation (b) already asks for adaptability. The
modality counts omitted the four agents observing indirectly. "Accessibility
tree" was the chapter's example and not the survey's, and dropped
"inconsistent", which is the adjective carrying the gap's name. Safety had
been folded into the privacy sentence. And the six times lower success rate
now says it comes from one benchmark the survey cites rather than runs, and
carries a citation.

The same reader found the prose reading as a different author from
`3-2_further_contributions.tex`: eight pseudo-clefts and three section titles
of the form "What X does", five passages narrating the chapter's own honesty,
six antitheses, four paragraphs that announce a count and then deliver it, and
a verbless fragment. All rewritten. The section titles are statements now, per
3.8. Hyphenated connectors were swept per 3.3, and three agency failures per
3.6: benchmarks pursuing, a use demanding, privacy entering.

Two things were left. The contribution statement's first four paragraphs state
the author's own attribution and are the author's to make, so only a vague
intensifier and the hyphens were touched, and the register point is marked
`TODO(author)` in the file. And `references/manual.bib` has `pages = {34}` for
`acu_survey`, which may be a JAIR article number rather than a first page; it
is marked in the bib and the publication box prints whatever is there.

## Level 3 for `chap:introduction`

Criticised once and rewritten. The first draft of this plan opened on the
retired spine, put nine paragraphs of setup before the first result, tried to
discharge two definitional obligations in a sentence each, and left out both
the strongest evidence in the thesis and the hardest objection to it. What
follows is the revision, with the reversals recorded.

### Five reversals from the critique

**The opening changes.** The first draft kept the current file's first two
paragraphs, which are sparse against distributed coding stated as the thesis's
first words. The spine was changed on 2026-11-16 precisely so that nothing
would lean on that framing, and an opening that leans on it entirely, three
paragraphs before the analogy is declared, teaches the reader to read the
whole thesis as a coding thesis. Those paragraphs also claim the clean trade
that admission 4 scopes down, and "nothing in the data chooses between them,
something does" is the unscoped sole determination claim the title was
rewritten to avoid. The chapter now opens on a measurement, which is also the
voice the one finished chapter already uses.

**The analogy paragraph goes to the background.** The first draft gave it a
paragraph in the introduction, naming three disanalogies about a framing the
reader has not met and will not meet again. It belongs where the measure is
introduced, which is `sec:bg_sparsedistributed`, and that is where the three
disanalogies now live. The introduction keeps one clause at the definition of
circuit saying the measure is borrowed and pointing there. This deviates from
the concept file's "one paragraph in the introduction and one in the outlook",
and the concept file is updated.

**Credit assignment is argued, not stipulated.** The first draft wrote one
sentence defining credit assignment to cover how an optimizer distributes
credit across neurons. Admission 9 records the motive in writing, so the
sentence is evidence for the objection it answers, and it stipulates against
the house meaning at the institute examining the thesis. The defensible
version is an argument and takes a short paragraph: the condition compares a
neuron's credit against the non gradient term of its own update, and all three
such terms the chapter unifies are supplied by the optimizer, so the quantity
the condition is about is set jointly by the backward pass and the optimizer's
normaliser, and no account that assigns credit to the backward pass alone can
state it. It ends by conceding admission 9 out loud. A concession the
candidate makes is not a finding for the committee.

**The task against objective boundary is not drawn.** The first draft defined
it in a sentence. The boundary would be drawn by what the designer intended,
which is not a property of the training setup and is not checkable, and the
two chapters are not parallel in the way the sentence implies: the grokking
chapter holds the task literally fixed, while the attention chapter changes
the loss, the index set the update sums over, and in a decoder the causal
mask, which is architecture. The introduction instead lists the training setup
as components and says for each chapter which were held fixed and which
varied. Part III is retitled to name the two components rather than to rest on
the boundary.

**Section 3 is reweighted and gains two paragraphs.** The permutation control
is the strongest evidence in the thesis and the only answer to viva question
2, and the first draft left it out. The AdamW scope is the hardest objection
and admission 5, and the first draft left that out too. Both are in. The
paragraph that admits no measurement is shared moves earlier and leads with
the positive, because one standard does cross the chapters and that is
research question 7, which the concept file calls the thesis's one integrative
claim.

### The sections

**Section 1. A trained network uses some of its neurons and not others, and the task does not set which.** Seven paragraphs.

1. Open on the measurement. A network that has solved modular addition at
   width $2048$ carries the computation on $332$ of its $2048$ neurons.
   Changing what the update normalises takes that to $2046$ at a cost of two
   points of test accuracy. Credit assignment by sentence two, scoped by
   construction, the price beside the headline, and no coined vocabulary.
2. Why it matters, with admission 4's scope in the same paragraph. A spread
   computation survives the loss of any one neuron. A concentrated one has
   more to prune and transfers faster to a task that recombines the same
   features, and not to one that only changes the readout.
3. Why the field has assumed the task settles it. Grokking, glossed inline at
   first use, because `imports/glossary.toml` names this file as the gloss
   site. The Fourier solution read neuron by neuron, and universality. Every
   network behind that evidence was trained with backpropagation and an
   adaptive optimizer. Do not stage a refutation: universality is a claim
   about the algorithm and it holds. Admission 7.
4. The definition site for circuit, definition before name, with participation
   ratio glossed inline because the reader meets the measure here and the
   background twenty pages later. The narrower sense than mechanistic
   interpretability, admission 8, and one clause saying the measure is
   borrowed from the neuroscience literature with a pointer to
   `sec:bg_sparsedistributed`.
5. The training setup as a list of components: the target function and the
   data, the loss, the architecture and width, the credit assignment
   algorithm, the optimizer, the initialisation. Then one sentence per
   results chapter saying which were held fixed and which varied. This
   replaces the task against objective definition and makes the attention
   chapter's mask a row rather than an embarrassment.
6. What credit assignment means here, argued as above, ending on the
   concession.
7. Where the question came from, in four sentences. Agents for computer use
   defined, the survey, the six gaps and the two the thesis takes, and that
   `\cref{chap:further}` holds four further papers. One line, not the full
   version, which `sec:acu_takes` already carries in the same words.

**Section 2. The learning rule sets how much of a network carries the computation.** Five paragraphs.

8. The grokking setting and why it earns the detailed work.
9. The condition, then the intervention. Two sentences, not one: headline then
   price. The honesty rule is satisfied by adjacency, and a single sentence
   carrying four numbers breaks 3.2.
10. The permutation control. A profile imposed with a random permutation
    deciding which neuron receives which magnitude, participation following
    the imposed value from $0.637$ to $0.990$, accuracy above $0.96$.
11. The scope, in one paragraph rather than scattered in clauses. Width: $30$
    of $32$ at width $32$ and nothing to redistribute. The reference setting
    is Adam with L2 added to the gradient and the manuscript says it is not a
    recommended setting, so under AdamW the reference is already distributed
    on modular addition, on MNIST, on the canonical transformer and in the
    language model. The condition is general and two of its three non gradient
    terms are live under AdamW. Admissions 3 and 5.
12. The price, with admission 4's scope.

**Section 3. The objective, the readout and the architecture settle three further properties.** Four paragraphs.

13. Attention. Backpropagation held fixed, the objective varied, at a scale
    the grokking setting cannot reach. Not a second measurement.
14. The world model. A quantity the loss never constrains, and a probe that
    reports it in place of the state.
15. The standard that crosses the chapters, positive first. One chapter sets a
    standard for readouts and the discussion holds this thesis's own measure
    to it, which is research question 7 and the answer is partly
    uncomfortable. Then, in the same paragraph, that no measurement is shared
    and two that were planned are not available. Admissions 2 and 6, with
    Nero as the one clause that answers the gauge objection.
16. CNA, stating what it shows, not only what it is not. Noise filtering,
    completion and recombination, then the convergence and the two dates.

**Section 4. Research questions.** Seven, not eight, weighted three to the
lead paper rather than four. The first draft's question 3 was inside question
1, its question 8 contained its own answer, and its question 5 had a defence
against an objection stapled to it. Each names the chapter that answers it.

**Section 5. Contributions.** One line each, with the authorship share per
item, because `3-2_further_contributions.tex` invokes the institute's
expectation that a cumulative thesis separates the candidate's own
contribution from collaborative work and a committee reads the shares
together. Then two short paragraphs: what is left of the claim without the
grokking paper, said plainly rather than left for the discussion, and how to
read the thesis, which is not a roadmap but the facts a reader needs, that
imported bodies appear as published with their own spelling and numbering and
that the frame is written fresh.

### What this chapter does not do

It states no finding in full. The file it replaces stated six findings in six
sections, restated them as questions, and restated them again as
contributions.

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

### Round 2, 2026-11-16, the spine changed and was criticised again

The author answered the first escalated question in favour of credit
assignment. The three readers were sent again, on the revision.

**Examiner.** Checked every Level 0 number against the manuscripts; all were
right except two sentences, and both were corrected after the quoted lines
were verified here. The claim asserted that the condition orders the rules,
which `tab:zoo` refuses, because Lion and credit equalisation share credit
participation $1.000$ and land at $0.535$ and $0.992$. Admission 5 asserted
that every model the field trains is concentrated, which is the opposite of
the manuscript's AdamW results and of its own sentence that Adam with L2 is
"not a recommended setting". Both are rewritten. The report also found that
the spine's own sentence excluded the attention chapter, that "across its
whole range" was not earned, that the toy objection is half answered rather
than answered, that the grokking and world model chapters were linked by a
metaphor where a standard would do, that the survey gap split contradicted the
concept file, and that the three hardest viva questions were not on the list.
All adopted. Three recommendations are reflected rather than copied: the
spine's umbrella problem is now stated as an objection to survive, the
task against objective distinction is assigned to the definition site, and the
cross chapter argument became research question 7.

**Title audit.** Found the coined noun circuit applied to the attention and
CNA chapters and to two part titles, against the concept file's own
guardrails; a part label no longer matching its part; the title's bare
"decides" claiming sole determination the width sweep refuses; a dangling
pronoun in the subtitle; two chapter titles never proposed at all; and the
3.8 exemption the plan relied on never written into CLAUDE.md. Adopted in
full. The title, the subtitle, three part titles and five chapter titles
changed, and the exemption is now in CLAUDE.md. It also found that both
abstracts still argue the retired story, which turned out to understate the
problem.

**AI smell audit.** Found the rewrite cleaner on vocabulary and worse on
shape: 43 definitions by negation, five paper blocks built to one template
with six paragraphs opening on "The first draft", a tricolon claiming it
needed no argument, honesty labels standing in for corrections, a heading
promising three items over a list of four, and one argument written twice in
two voices across the two files. The templated paragraphs are gone, the
corrections they announced live here instead, and `scripts/check_prose.py`
gained six checks: per line antithesis reporting, the self congratulation
phrases, the meta label family, draft reference density, counted headings
against list length, and the anaphoric triple.

### Round 3, 2026-11-16, the finished frame

Two readers took the frame end to end once every file was prose. Every
quantitative claim either made was checked against the vendored manuscripts
before being accepted, and six factual errors came out of it.

**Examiner.** The worst was in the thesis's first sentence, in both abstracts
and the introduction: it gave the width-2048 neuron counts and attached the
width-256 accuracy cost to them, where the manuscript says "At width $2048$
the reference and equalization both start at $0.998$". Next worst, "a few
columns come to dominate" misread the attention paper in five places; its
theorem reads "more columns with high norms than rows with high norms", so
column dominance is columns against rows. The thesis's "circuit across
columns" analogy rested entirely on that misreading and is gone, which is the
cleaner position. Also: the background claimed no literature had asked what
sets the number of neurons in use, where the grokking paper's own related
work cites seven works for the separate routes; the world model chapter
omitted its paper's own negative result, that the four checks reject every
ranking between the authors' trained modules; the transfer result was given
as its flattering half in four places; the survey gap sort contradicted
itself inside one chapter; the Hounsfield summary inverted where the
thresholds come from; and the introduction said five chapters reproduce a
paper where four do. All fixed, with the quoted source line checked in each
case.

Two of its findings were not acted on. The learning-strategy and modality
counts in the survey chapter are read off figures rather than prose and sum
to $85$ of $87$, so they need checking against the source spreadsheet before
submission. And the frame still has no answer to the manuscript's own line
that the decoupled-decay reference "has nearly equal outgoing norms but
prunes to about as few neurons as the Adam reference"; the discussion now
states the problem rather than solving it.

**AI smell audit.** Found the frame disciplined at sentence level and
repetitive across files. Six of its findings are now checks in
`scripts/check_prose.py`, the important one being cross-file shingle
duplication, which nothing looked for before. It found twenty-three copies,
including the abstract and introduction opening on the same twenty-five
words. All twenty-three are rewritten so each file says the thing in its own
words. The audit also warned against homogenising
`3-2_further_contributions.tex`, whose plainer voice reads as a second hand
and is worth keeping, so only its mechanical markers were changed.

### Round 5, 2026-11-16, the three critics again

Sent on the finished frame, each briefed on what rounds 1 to 4 had settled so
they would look for what survived. Every quantitative claim the examiner made
was checked against the vendored manuscripts before being accepted.

**Examiner.** Reported that every number in the frame is right, and that the
problems are four omissions from the grokking manuscript's own
qualifications, each of them printed in the appendix the thesis binds.

- The sentence answering the thesis's hardest objection was wrong. "Two of
  its three non gradient terms are live under decoupled decay" reads as two
  independent routes surviving current practice. Both require the decay to
  reach a network's normalisation parameters, which the manuscript says is
  not what most current code does, and where it does not the untouched
  network still moves from $0.82$ to $0.91$ under the intervention, a gap the
  paper's limitations say the condition does not explain. Corrected in all
  three places that carried it.
- The three route unification was stated without the manuscript's own
  qualifications. The control removes only about half the effect for the
  numerical floor, and for the gain the intervention has to act on the gain
  and the outgoing weights as well: equalising the incoming rows alone gives
  $0.364$ against a reference of $0.366$, which is no effect. The outgoing
  weights are what the participation ratio is computed from, so this belongs
  beside the gauge audit and not in a footnote.
- The language model result was quoted without its AdamW column. Decoupled
  decay leaves $0.9\%$ of units nearly unused at a lower loss than the
  intervention's $1.3\%$, and the manuscript says this is what the condition
  predicts. Restoring it turns the frame's most exposed omission into
  confirming evidence.
- **DFC.** The chapter reports that deep feedback control groks and produces
  a circuit of about $235$ of $256$ neurons at nearly perfect accuracy, with
  credit that is already nearly equal, no intervention and no per neuron
  normaliser. That is the title's claim demonstrated on the title's own axis
  by a rule somebody else wrote, and the frame mentioned it once, as a count.
  It is now in the introduction, the chapter and the conclusion, and the
  conclusion no longer says two rules are on the far side of the line when
  there are three. This is the round's most valuable finding.

Also corrected: an assumption-free claim in the attention chapter that its own
proofs refuse, a speed up quoted as typical where the paper says "up to" and
one run of three shows none, an invented prediction about decoders, "no
dynamics are defined over a net" where dynamics are that paper's central
mechanism, "does not scale" where the paper defers the question, the survey's
four taxonomy limits where it states six, the JAIR article number printed as
a page, and a co-author's name.

The attention contribution statement was reconstructed and marked
`TODO(author)`. The arXiv version vendored in this repository carries the
authors' own statement, so it is quoted instead and the marker is gone.

Two findings not acted on. The survey's shared first authorship is not
evidenced in the vendored copy, whose equal contribution note is commented
out, so the chapter now says it has to be checked against the published
article. And the examiner's point that the thesis opens on a bespoke pair,
Adam with coupled L2 against credit equalisation, where a published pair
exists in the same table, is a framing decision for the author.

**AI smell audit.** Found the participation ratio defined twice, in two files,
in wordings far enough apart to beat the shingle check and disagreeing about
whether the ratio is a count or a fraction. The paper's own definition settles
it and the frame now follows it. Also: a false "every" in the conclusion that
the discussion's own sentence contradicts, the central condition stated five
times with two different meanings, nine "worth saying" constructions, four
sentences whose content is where the author put the next sentence, and six
that are grammatical, correct and empty. Six of its suggestions are now checks
in `scripts/check_prose.py`, including a paragraph level pass that catches
multi-word patterns straddling a line break and a cross file numeric check
that finds a finding stated in full in three or more places.

**Title audit.** Found a `\cref` inside a section title, which hyperref cannot
put in a PDF string, so the bookmark read "The standard of , applied to the
measure of". Also the ACU chapter's Title Case headings against sentence case
everywhere else, a section title claiming the gaps recur whatever the
architecture where the survey says no such thing, and Part II stating one
claim at three nested levels.

