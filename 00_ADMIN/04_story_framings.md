# Thesis story: candidate framings and a recommendation

Written 2026-09-06, after two changes to the paper set. The Koopman-JEPA world
model paper became "Bounded Is Not Better", a controlled study showing that the
spectral constraint's five order of magnitude win is a measurement artefact. A
new first author paper, "Grokking Beyond Backpropagation", shows that the
learning rule decides whether a network groks and how many units carry the
solution. The old arc (diagnose, constrain, change paradigm) no longer holds,
because its middle part now argues against itself.

## 1. What the papers actually show

The table strips each paper to the one claim the thesis may rest on.

| Paper | Role | What varies | What is held fixed | What is decided |
| --- | --- | --- | --- | --- |
| Attention (ICML) | shared first | training objective, bidirectional against autoregressive | architecture, data | geometry of the query key product: symmetry against directionality and column dominance |
| Grokking (ICLR submission) | first | learning rule, twelve published plus a credit knob | task, data, architecture, optimizer, weight decay | whether the network groks (transverse component at the minima) and how many units carry the circuit (grain) |
| CNA (Neural Computation) | first | learning principle, Hebbian and recurrent instead of gradient and feedforward | input statistics | representation type (nets from fragments) and its robustness, completion and OOD behaviour |
| Bounded (in preparation) | first | spectral constraint on the latent transition operator | encoder, objective, data, seeds | latent norm growth, and through it the probe curve, not predictive quality; trivial predictors beat every learned model |
| ACU survey (JAIR) | shared first | the field | | one dominant recipe (foundation model, prompting or behaviour cloning) and six gaps, three of them about evaluation |
| Hounsfield (IEEE) | shared first, framing | input representation, HU masks | model, data | data efficiency and accuracy against the same model without masks |
| Retrieval (CLEF) | first | pipeline design | task, no external data | rank on a leaderboard of 31 teams |
| LLM benchmark | minor, evaluation | compression method | model | GPU memory, and a quality loss that raters see and the advertised metrics do not |
| COGITAO | minor, one model | composition depth | architecture family | in distribution success with failure on unseen rule combinations |

Two things stand out. The four strong first author or shared first author
papers (attention, grokking, CNA, bounded) share one method: hold everything
fixed, vary one part of the training procedure, and read the resulting
structure off the update equation before verifying it. And in three of them the
result is that a property the literature attributed to the task or to the model
belongs to the procedure instead. The minor papers are about evaluation and
about deliberately imposed knowledge.

## 2. Ten framings, judged

### F1. Keep the old arc: diagnose, constrain, change paradigm

Claim. Failures of deployed systems are structural. Hard constraints mitigate
them. Neuro inspired architectures replace the substrate.

Placement. Unchanged. Bounded replaces Koopman as "constraints have limits".
Grokking joins CNA in the paradigm part.

Judgement. The middle part now says the opposite of what the part title
promises: the flagship constraint chapter shows the constraint's win was an
artefact, leaving one modest positive (Hounsfield) and a competition entry. The
title promises agents and no chapter builds one. "Paradigm shift" is rhetoric
the style guide bans. The attention chapter is asked to carry a causal claim
(objective decides geometry, so models fail to generalise) that the paper does
not make. Verdict: drop.

### F2. The procedure decides the solution

Claim. The task fixes the set of networks that fit. The training procedure
picks the member, and which member can be read off the update equation. The
objective picks the geometry of attention (attention paper). The learning rule
picks whether the network groks and how many units carry the circuit (grokking
paper). A Hebbian, local principle picks a structured representation with
properties gradient training does not produce (CNA). And because the procedure
decides so much, a measurement that the procedure alone can satisfy is not
evidence about the task (bounded paper).

Placement. ACU as motivation: the field builds agents by one recipe and the
gaps it reports (generalisation, planning, evaluation) are the properties the
rest of the thesis shows to be decided by the procedure or mismeasured.
Attention, grokking, CNA as the three pillars of "what the procedure decides".
Bounded as the pillar of "what the procedure decides about the measurement".
Hounsfield and retrieval as deliberately chosen procedures whose gains survive
the controls the bounded chapter asks for.

Strengths. Unifies the four strong papers on content (what is decided) and on
method (read the update, predict the structure, verify). Extends the implicit
bias literature, which studies optimizers, to the objective, the credit
assignment rule and the readout. Every chapter has a constructive consequence:
symmetric initialisation, the credit knob and its trade off, HU masks, the
rollout evaluation protocol. No claim exceeds its paper.

Weaknesses. ACU becomes motivation rather than a pillar. "Procedure" needs one
definition site and a careful scope (objective, rule, constraint, readout). The
attention result is about weight geometry, and the frame must not restate it as
"models do not learn world structure".

Verdict. Strongest. Recommended.

### F3. Confounds and controls: what the measurement shows

Claim. Several headline results are properties of the pipeline rather than of
the model, and a controlled variation exposes each one.

Placement. Bounded central. Grokking as "universality of the sparse circuit
rested on one learning rule". Attention as "individual attention matrices were
the wrong object, the bilinear form is the right one". ACU's three evaluation
gaps, the LLM benchmark (advertised lossless against what raters see) and
COGITAO (in distribution success hides compositional failure) as further cases.

Strengths. Honest and distinctive. The minor papers fit naturally and the
survey's evaluation gaps become load bearing.

Weaknesses. CNA and Hounsfield have no home. A thesis that is mostly "the
evidence was confounded" reads as negative, and the grokking paper's
constructive findings (grain law, robustness against adaptation) get demoted
to "a confound was removed". The committee will ask what was built.

Verdict. Good as the second half of F2, not as the spine.

### F4. Beyond backpropagation

Claim. Backpropagation is one rule among many. Other rules produce different
solutions, some more robust. CNA shows a rule plus substrate alternative.

Placement. Grokking and CNA as pillars. Attention as "what backpropagation
under a given objective produces". Bounded, Hounsfield, retrieval and ACU as
motivation or appendix.

Strengths. Fits the institute and the committee. "DFC groks" is a headline.

Weaknesses. The grokking paper's finding is not that non gradient rules are
better. It is that the rule decides the layout, and that per unit grain does
so whatever the rule (Nero is a plain optimizer). Four of eight papers become
preface. The attention paper is about backpropagation. Bounded has nothing to
do with learning rules. Forces a value judgement the data do not make.

Verdict. Use as the ordering principle inside the "solution" part (distance
from backpropagation: objective varied, rule varied, no gradient at all). Not
the thesis.

### F5. Where inductive bias enters: a taxonomy of the pipeline

Claim. Bias enters at the input (Hounsfield), the objective (attention), the
rule (grokking), the constraint (bounded), the substrate (CNA), inference time
(retrieval) and the readout (bounded).

Strengths. Every paper has a slot. The part structure writes itself.

Weaknesses. A taxonomy is not an argument. Each chapter becomes an example
rather than a step, and the thesis has no verdict at the end. "Inductive bias"
already has a narrower meaning in the literature.

Verdict. Useful as the map in the introduction of F2. Weak as the spine.

### F6. The origins of structure in neural representations

Claim. Where does structure in trained networks come from.

Weaknesses. "Structure" means something different in every chapter: weight
symmetry, circuit layout, nets, a spectral bound, HU masks. The old subtitle
already used the word and it gave no thread. There is no actor, which invites
vague passive sentences.

Verdict. F2 with a weaker noun. Drop.

### F7. Universality and its limits

Claim. What is the same across trained networks, and what is contingent on how
they were trained. Attention: the geometry is universal across models and
modalities once the objective is fixed. Grokking: the computation is universal,
the layout is not. CNA: change the substrate and the representation changes.
Bounded: an apparent universal win is an artefact.

Strengths. Sharp, and it enters a live debate (Chughtai et al., Olah).

Weaknesses. Narrow. ACU, Hounsfield, retrieval and the LLM benchmark have no
place. "Universality" is a mechanistic interpretability term that CNA readers
will not recognise.

Verdict. A section of the discussion in F2.

### F8. Robustness and its price

Claim. Robustness can be bought (distributed circuits, nets, HU masks,
retrieval) and the price is adaptation speed, scale or data.

Weaknesses. The attention paper does not fit. Bounded fits only as "stability
is not accuracy". Trade off theses are generic, and the trade off is measured
in one paper.

Verdict. Drop. Keep the grokking trade off as a finding.

### F9. Applied reliability (the engineering thesis)

Claim. Reliable learned systems need constraints, retrieval and honest
evaluation.

Weaknesses. Puts the minor papers at the centre and the two strongest first
author papers at the edge. Wrong centre of gravity for an INI doctorate.

Verdict. Drop.

### F10. No thread, chronological

Verdict. Permitted for a cumulative thesis and the weakest defensible option.
Fall back only if F2 fails with the committee.

## 3. Recommendation: F2 with F3 as its second half and F4 as the ordering

### Thesis in one sentence

Among the networks that fit the data, the training procedure picks the one you
get. Its structure can be read off the update equation. And a result that can
be read off the procedure is not evidence about the task.

### Title candidates

Plain statement titles, per the style guide.

1. What the Training Procedure Decides: Objective, Learning Rule and Constraint
   as Choices Among Solutions in Deep Learning
2. Chosen, Not Found: How Objective, Learning Rule and Constraint Decide What a
   Neural Network Becomes
3. Implicit Bias Beyond the Optimizer: Objective, Learning Rule and Readout in
   Deep Learning

The first is the safest. The second is the most memorable. The third places the
work in a named literature at the cost of sounding like a paper title.

### Research questions

1. When a trained network shows a structure, which part of the procedure
   decided it: the task, the objective, the learning rule, or a constraint?
2. Can that structure be predicted from the form of the update alone, without
   running the rule?
3. When a procedure decides a structure, does it also decide what a standard
   measurement reports, and how are the two told apart?
4. What does choosing the procedure deliberately buy, and at what price?

### Parts and chapters

Part I. The question and why it matters.
- Ch 1 Introduction. The one sentence thesis, the four questions, the map of
  where the procedure acts (objective, rule, constraint, readout).
- Ch 2 Background. Implicit bias of optimizers, grokking and its circuits,
  self attention as a bilinear form, latent world models and rollout
  evaluation, credit assignment rules, Hebbian assemblies.
- Ch 3 ACU survey (full chapter). The field builds agents by one recipe. The
  six gaps name the properties the thesis then studies: generalisation and
  robustness (Part II), planning and its evaluation (Part III).
- Ch 4 Short chapter, LLM benchmark and COGITAO. Two further settings where
  the benchmark number and the capability diverge. Sets up the measurement
  thread. The thesis author's limited role is stated at the top.

Part II. The procedure decides the solution.
- Ch 5 Attention. The objective decides the geometry of the attention weights.
  Read off the update, verified across models and modalities. Design
  consequence: symmetric initialisation.
- Ch 6 Grokking. The learning rule decides whether the network groks
  (direction) and how many units carry the circuit (grain). Read off the
  update. Design consequence: the credit knob, and the robustness against
  adaptation trade off. First grokking under a control driven rule.
- Ch 7 CNA. With no gradient at all, a Hebbian local principle picks a
  structured representation with completion, denoising and OOD behaviour. The
  far end of the spectrum of procedures.

Part III. The procedure decides the measurement.
- Ch 8 Bounded. The constraint decides latent norm growth, the scale invariant
  loss leaves scale free, the scale sensitive probe reads exactly that. The
  theory is right and the inference from bounded to better fails. Trivial
  predictors, the constant predictor curve, and the protocol.
- Ch 9 Short chapter, Hounsfield and retrieval. Two deliberate impositions
  whose gains survive the controls Chapter 8 asks for: the same model without
  masks on the same data, and a leaderboard of 31 teams. Roles stated.

Part IV. Synthesis.
- Ch 10 Discussion. What the task fixes, what the procedure chooses, what the
  readout shows. Universality at the level of computation, not layout. Design
  consequences collected. Limitations, specific and plain.
- Ch 11 Conclusion.

Alternative for Chapter 4: fold the two minor papers into Part III as the
opening of the measurement part. Chapter 4 in Part I is preferred because Part
I should carry both threads before the reader meets either pillar.

### Honesty guardrails for the frame

- Attention. Claim only what is proven: the objective decides symmetry against
  directionality of the query key product. Never "models do not learn world
  structure".
- ACU. The six gaps are observations. The frame may say the field varies the
  model and rarely the procedure, which the survey's trend findings support.
  It may not say the gaps are consequences of anything the thesis shows.
- Bounded. The constraint does what theory says. What fails is the inference
  from bounded to better. Never "constraints do not work".
- Grokking. The rule decides the layout, the task decides the computation.
  Never "non gradient rules are better".
- Minor papers. Short, with the author's role in the first sentence.

### What changes in the repository

- `main.tex`: title, subtitle, part names. Parts II to V become the four parts
  above. `sections/5-1_koopman_jepa.tex` is renamed for the bounded paper.
- `sections/1-1_introduction.tex`, both abstracts, `2-1_related_work.tex`,
  `7-1_discussion.tex`, `7-2_conclusion.tex`: rewritten to the new frame.
- `CLAUDE.md` 3.4: the "paradigm" carve out no longer applies and is removed.
  3.9 and the glossary get the thesis wide terms: procedure, solution set,
  layout, circuit, readout, grain, transverse component.
- `CLAUDE.md` 4.6: two new rows once the grokking and bounded papers are
  vendored, with manifests in `imports/`.
- The related work chapter loses the Koopman and world model sections as
  written and gains implicit bias, grokking and learning rules.

### Open decisions for the author

1. Does the ACU survey stay a full chapter in Part I, or become the closing
   half of the introduction? A full chapter is recommended: it is a JAIR paper
   with shared first authorship.
2. Where do Hounsfield and retrieval sit: Part III as "impositions that pass
   the controls" (recommended) or Part II as further instances of "the
   procedure decides"?
3. Title 1, 2 or 3.

## 4. Revision after author feedback (2026-09-06)

The author weighted the papers by ownership. ACU, CNA and grokking are the ones
the author drove and are the pillars. Attention is strong but Matteo drove it,
which the supervisors know, so it is a supporting chapter. Everything else,
including the bounded paper, is side work.

This narrows F2 from "the training procedure" to "the learning rule". The
narrowing is what makes the message followable, and the ownership weights are
what justify it. It also promotes ACU from motivation to pillar: the survey is
the chapter that shows the field has one recipe and names what it lacks.

### The message in three sentences

Almost everything in deep learning is trained one way, backpropagation plus an
optimizer on a fixed architecture, and the field has stopped treating that as a
choice. It is a choice, and it decides things people attribute to the task or
to scale: whether a network generalises at all, how many neurons carry its
solution, how robust it is, and how fast it adapts. So the learning rule should
be chosen deliberately, and its consequences measured with controls that the
choice alone cannot pass.

### Title candidates

1. What the Learning Rule Decides
2. The Learning Rule as a Choice: Generalisation, Robustness and Adaptation
   Beyond Backpropagation
3. One Recipe, Many Solutions: The Learning Rule as a Design Choice in Deep
   Learning

### Parts and chapters, revised

Part I. Introduction and background.

Part II. What the field builds and what it lacks.
- ACU survey (pillar). One recipe, six gaps. Two of the gaps, generalisation
  and inefficient learning, are the properties Parts III and IV show to depend
  on the rule.
- Short chapter: LLM benchmark and COGITAO. Two further places where the
  benchmark number and the capability diverge.

Part III. The learning rule decides the solution.
- Grokking (pillar). Same task, data, architecture and optimizer, only the rule
  varies. Four rules never generalise. Among those that do, the rule decides
  the layout, the layout decides robustness against adaptation, and both are
  readable from the update equation. First grokking under a control driven
  rule.
- Attention (supporting). With backpropagation fixed, the objective imprints a
  geometry on the attention weights. Contribution statement states Matteo's
  lead.

Part IV. A learning rule that builds structure.
- CNA (pillar). Hebbian plasticity, recurrent assemblies, robustness and
  completion by construction. Does not yet scale, and says so.

Part V. Imposing a property instead of learning it.
- Bounded (supporting). A constraint satisfies the standard readout without
  anything being learned. Trivial predictors, scale invariant readouts, the
  protocol. This is the control logic the grokking chapter applies.
- Short chapter: Hounsfield and retrieval. Two impositions whose gains survive
  such controls.

Part VI. Discussion and conclusion. When to choose the rule and when to impose
a constraint. What the task fixes and what the rule chooses. Limitations.

### Draft abstract

Almost every neural network in use today is trained the same way. An error is
computed at the output, backpropagation assigns each weight its share of that
error, and an optimizer turns the shares into updates. This thesis asks what
that single choice decides. The answer is that the learning rule decides which
of the many solutions that fit the data the network ends up with, and that this
choice, rather than the task, sets how robust the solution is, how fast it
adapts, and whether it generalises at all.

The thesis starts with the field in which the consequences are most visible. A
survey of 87 papers and 33 datasets on agents for computer use, systems that
operate software from natural language instructions, finds that the field has
converged on one recipe, a pretrained foundation model adapted by prompting or
behaviour cloning, and that agents built this way share six gaps, among them
insufficient generalisation and inefficient learning. The survey names the
properties. The rest of the thesis asks what decides them.

The central study uses grokking, a setting in which a network fits its
training data long before it generalises, because there the solution a rule
reaches can be read at the level of single neurons. It holds task, data,
architecture and optimizer fixed and varies only the learning rule, across
twelve published rules and a controlled family built for the purpose. Four
rules never generalise, because their update does not vanish at the minima of
the loss. Among the rules that do, the number of neurons carrying the solution
runs from about 150 to 250 of 256 at matched accuracy, loss and weight norm. A
rescaling of each neuron's share of the error that provably leaves the
objective and every update direction unchanged moves that number across its
whole range, so the layout of the solution is set by how credit is assigned and
not by the task. Which rules spread the solution is readable from their update
equation: only rules that normalise one neuron at a time do. The layout has a
price. Spread solutions survive neuron deletion far better, and concentrated
ones adapt to a new task about twice as fast. A control driven rule is shown to
grok, to our knowledge for the first time.

A supporting study shows that the same holds one level up. With
backpropagation fixed, the training objective alone imprints a geometry on the
attention weights of Transformers, symmetric under bidirectional and
directional under autoregressive training, across models and modalities.

The thesis then leaves gradient based learning altogether. The Cooperative
Network Architecture represents sensory input by structured, recurrently
connected groups of neurons that are assembled from fragments learned by
Hebbian plasticity. Composition by construction gives it noise resilience,
figure completion and generalisation to unseen patterns without supervision,
properties the standard recipe does not deliver, at the cost of a model that
does not yet scale.

A property can also be imposed instead of learned. A controlled study of latent
world models shows the risk. A spectral constraint on the transition operator
wins by five orders of magnitude under the standard readout, and the win is an
artefact of that readout, since predictors that learn no dynamics beat every
learned model. Two further studies, on CT segmentation with input masks derived
from medical knowledge and on scientific source retrieval, show impositions
whose gains survive such controls.

The conclusion is that the learning rule is a design choice with measurable
consequences, that the field currently makes by default, and that its
consequences must be measured with controls the choice alone cannot satisfy.

## 5. Second revision: representations an agent can act on (2026-09-06)

Further constraints from the author. The original PhD topic was actionable
representations and world models, the PIs would like the thesis to connect to
it, and a world model built on principles from neuroscience is their dream. The
attention paper can carry more weight than section 4 gave it.

This wraps the "recipe decides" argument of sections 3 and 4 in the purpose
that made the author study it. The four properties an agent needs from its
representation become the criteria, and every chapter reports which choice in
the recipe decides which property. It gives attention a full role (the
objective component, and autoregressive training is the objective behind every
foundation model in the survey), and it gives the bounded paper the hinge role:
the direct route to a world model was tried, its evidence was confounded, and
that is what justifies taking the recipe apart.

### The message in four sentences

An agent needs a representation it can act on: one that generalises beyond its
training data, predicts the consequences of actions over several steps,
survives damage, and adapts when the task changes. Deep learning produces
representations by one recipe, an objective, backpropagation of its error
through a fixed architecture, and an optimizer. This thesis takes the recipe
apart, one component at a time, and asks what each decides about those four
properties. The objective, the learning rule and the substrate each decide
properties the field treats as given by the task, and the standard evaluation
of world models can be passed by the recipe alone with none of them present.

### Which chapter measures which property

| Property an agent needs | Measured in | What decides it |
| --- | --- | --- |
| Generalisation beyond the training data | grokking (four rules never generalise), CNA (unseen patterns), COGITAO, ACU gap 1 | the learning rule, the substrate |
| Multi step prediction | bounded, ACU gap 3 | not the spectral constraint; the evaluation must be designed so trivial predictors cannot pass |
| Robustness to damage and noise | grokking (deletion tolerance), CNA (noise, completion) | the layout the rule chooses, the substrate |
| Adaptation and learning efficiency | grokking (adaptation speed), Hounsfield (data efficiency), ACU gap 2, LLM benchmark | the layout the rule chooses, structure supplied from outside |
| Geometry of the representation itself | attention | the objective, not the domain |

### Title candidates

1. Representations an Agent Can Act On: What the Objective, the Learning Rule
   and the Substrate Decide
2. Toward World Models Built on Principles from Neuroscience: What Decides a
   Representation an Agent Can Act On
3. Actionable Representations: Objective, Learning Rule and Substrate as the
   Choices Behind an Agent's World Model

Title 1 promises only what the thesis delivers. Title 2 names the PIs' dream
and must be paired with the sentence "the thesis does not build that model".
"Actionable" in title 3 is a coined term and needs its definition site in the
introduction, definition first, then the name.

### Research questions

1. What does an agent need from its representation, and where does the
   standard recipe fall short? (ACU, LLM benchmark, COGITAO)
2. Can a world model's multi step prediction be repaired by constraining its
   dynamics, and how can that be told from an artefact of the measurement?
   (bounded, with Hounsfield and retrieval as impositions that pass)
3. What do the objective and the learning rule decide about the
   representation, and can it be read from the update equation? (attention,
   grokking)
4. What does a substrate built on principles from neuroscience give that the
   recipe does not, and what does it cost? (CNA)

### Parts and chapters

Part I. Introduction and background. The four properties defined and named
once. The recipe named. The four questions.

Part II. What an agent needs.
- ACU survey (pillar). One recipe, six gaps.
- Short chapter: LLM benchmark and COGITAO. The recipe's cost under
  compression, and its limit under composition.

Part III. The direct route, and how to measure it.
- Bounded. The constraint passes the standard readout without predicting. The
  protocol. The question moves from the constraint to the recipe.
- Short chapter: Hounsfield and retrieval. Structure supplied from outside
  whose gains survive the controls.

Part IV. The recipe taken apart.
- Attention. Backpropagation fixed, objective varied. Geometry follows the
  objective's direction, not the domain. Symmetric initialisation. Contribution
  statement states Matteo's lead.
- Grokking (pillar). Objective fixed, rule varied. Generalisation, layout,
  robustness against adaptation. A control driven rule groks.

Part V. The substrate replaced.
- CNA (pillar). Assemblies from Hebbian fragments. Robustness and completion by
  construction. Does not yet scale.

Part VI. Discussion and conclusion. The pieces of a world model built on
principles from neuroscience: structured substrate, a learning rule other than
backpropagation known to reach generalising solutions, a predictive objective
whose imprint is understood, an evaluation trivial predictors cannot pass. What
is missing, named. When to impose structure and when to learn it.

### Where this framing is exposed, and the guard

- "World model" in the title promises a model the thesis does not build. Guard:
  the abstract and the discussion say so in one plain sentence, and the
  contribution is stated as "which choices decide its properties".
- The attention paper's link to world models runs through "autoregressive
  training is a predictive objective". Guard: the claim stays at geometry.
  Never "therefore the model cannot plan".
- CNA is perceptual, not dynamic. Guard: its link to world models is the
  substrate only, and dynamics over assemblies is named as future work.
- Bounded placed early could read as the thesis leading with a failure. Guard:
  it is framed as the experiment that told us where to look, and the protocol
  is a contribution the grokking controls then apply.

### Draft abstract

An agent needs a representation it can act on. Such a representation
generalises beyond the data it was trained on, predicts the consequences of
actions over several steps, survives damage, and adapts when the task changes.
Deep learning produces representations by one recipe: an objective, usually
predictive, backpropagation of its error through a fixed architecture, and an
optimizer. This thesis takes that recipe apart and asks, one component at a
time, what each decides about the representation. The objective, the learning
rule and the substrate each turn out to decide properties the field treats as
given by the task, and a standard evaluation turns out to be passable by the
recipe alone with none of those properties present.

The thesis starts with agents for computer use, systems that operate software
from natural language instructions. A survey of 87 papers and 33 datasets finds
that the field has converged on one recipe, a pretrained foundation model
adapted by prompting or behaviour cloning, and that agents built this way share
six gaps, among them insufficient generalisation, inefficient learning and
limited planning.

Planning over several steps needs a model of the environment, and the most
direct way to keep such a model's errors from compounding is to constrain its
latent dynamics. A controlled study of that route, with one encoder, one
objective and four dynamics modules that differ only in their spectral
constraint, finds that the constrained model wins by five orders of magnitude
under the standard readout and that the win is an artefact. Predictors that
learn no dynamics beat every learned model, and the gap vanishes under a
readout that ignores latent scale. The constraint does what its theory says.
The inference from bounded error to a better model fails, and the study leaves
a protocol for evaluating latent rollouts that trivial predictors cannot pass.
Two shorter studies, on CT segmentation with input masks derived from medical
knowledge and on scientific source retrieval with an external index, show
structure supplied from outside whose gains do survive such controls.

Two studies then vary one component of the recipe each. The first holds
backpropagation fixed and varies the objective. The objective alone imprints a
geometry on the attention weights of Transformers, symmetric under
bidirectional and directional under autoregressive training, the objective
behind the foundation models above, and it does so across text, vision and
audio, so the geometry of a predictive model's representation is set by the
direction of its objective and not by its domain. Symmetric initialisation,
which follows from the result, improves encoder models. The second holds the
objective fixed and varies the learning rule, in the grokking setting where a
network fits its training data long before it generalises and its solution can
be read at the level of single neurons. Four of twelve rules never generalise,
because their update does not vanish at the minima of the loss. Among those
that do, the rule decides how many neurons carry the solution, from about 150
to 250 of 256 at matched accuracy, loss and weight norm, and a rescaling of
each neuron's share of the error that provably leaves the objective and every
update direction unchanged moves that number across its full range. Spread
solutions survive neuron deletion far better and concentrated ones adapt to a
new task about twice as fast, so the learning rule sets the balance between two
properties an agent needs. A rule driven by a feedback controller rather than
by backpropagation generalises here, to our knowledge for the first time.

The last study replaces the substrate. The Cooperative Network Architecture
represents sensory input by structured, recurrently connected groups of neurons
assembled from fragments learned by Hebbian plasticity. Composition by
construction gives noise resilience, figure completion and generalisation to
unseen patterns without supervision, at the cost of a model that does not yet
scale.

Together the chapters give the pieces of a world model built on principles
from neuroscience: a structured substrate, a learning rule other than
backpropagation that is known to reach generalising solutions, a predictive
objective whose imprint on the representation is understood, and an evaluation
that trivial predictors cannot pass. The thesis does not build that model. It
shows which choices decide its properties and closes with the programme for
assembling them.

## 6. Third revision: a tested core instead of a covering story (2026-09-06)

The author judged sections 3 to 5 hand wavy and not good enough for a PhD
thesis. The diagnosis: each unifying sentence there was a re-description that
fits every paper rather than a claim any chapter tests. "Four properties an
agent needs" was a list invented after the fact. A covering story for eight
diverse papers will always read that way. The alternative is a tight core
claim that three chapters test with one argument, plus two contributions whose
relation to the core is stated exactly, including where it is loose.

### The shared argument, at the level of the equations

Three papers make the same move. Write the weight update as a sum whose index
set or scaling is fixed by something other than the data. Identify the quantity
of the trained network that this structure fixes. Derive the consequence from
the update equation alone. Verify it in trained networks, and intervene.

| | Grokking (pillar) | Attention | Bounded |
| --- | --- | --- | --- |
| Update structure set by | the group of parameters that shares one normaliser (the rule's grain), and whether the update vanishes at the minima of the loss | the set $C_i$ of tokens the objective lets token $i$ use as context | a spectral constraint on the transition operator, under a loss that is invariant to latent scale |
| Quantity the data do not fix | how the solution is divided across units, at equal loss, margin and weight norm | symmetric against antisymmetric part of $W_{qk}$, row against column norms | latent scale under rollout |
| What the update does to it | plain flow $\dot u_i = -r u_i$ conserves $\log(a_i/a_j)$, so the layout inherits the initialisation; per unit normalisation $\dot u_i = -r\bar u$ conserves $u_i - u_j$, so the layout spreads; a shared normaliser freezes within group shares | bidirectional: every pair enters in both orders with near equal weight, so increments are symmetric and symmetry accumulates; autoregressive: token $j$ is context for every later $i$ but target once, so columns accumulate and dominate | the spectral radius of $K$ sets $\|K^T z\|/\|z\|$, and a probe fitted at training scale reads exactly that |
| Predicted from the equation alone | the grain law, eight of eight published optimizers, the group size sweep within $0.08$ with nothing fitted | symmetry under bidirectional and column dominance under autoregressive training | the probe curve is monotone in the spectral radius |
| Verified on | twelve rules, four tasks, MLPs and a transformer | ModernBERT, GPT, LLaMA3, Mistral; text, vision, audio | two environments, four operators, ten seeds |
| Intervention | credit knob, imposed and permuted credit profiles, rule switch after grokking | symmetric initialisation | rescaling the spectrum; a scale aware loss removes the gap |
| What the literature had read it as | a property of the task (the sparse circuit) | not previously derived | evidence of a learned model |

The core claim, in one sentence: the weight update carries structure the data
do not supply, that structure comes from the objective, the learning rule or an
imposed constraint, the trained network inherits it, and it can be derived from
the update equation. Grokking adds the strongest form, at equal loss. Bounded
adds the evaluation consequence, that a readout sensitive to the inherited
structure mistakes it for learning.

The literature this sits in is implicit bias and conservation laws of gradient
flow (Du et al. 2018 on balancedness, Gunasekar et al. 2018, Woodworth et al.
2020, Kunin et al. 2021 "Neural Mechanics"). That literature varies the
optimizer. The thesis varies the objective's index set, the credit assignment
rule, and an architectural constraint, at the scale of trained Transformers and
across twelve rules, and it adds the measurement consequence.

### The two contributions outside the core, and exactly how they connect

CNA. Its main content is a representation in which every active neuron is
supported by others, assembled from fragments learned by Hebbian plasticity,
with noise tolerance and figure completion shown on line drawings. It does not
test the core claim. Two exact connections exist and both are one paragraph
each, not a spine. First, the grokking chapter proves that under random
deletion the relative fluctuation of a summed contribution falls as
$1/\sqrt{n\,\mathrm{PR}}$, and CNA is an architecture in which the number of
supporting neurons is a design principle rather than something the rule
decides. So CNA is "layout fixed by construction" where grokking is "layout
fixed by the rule". Second, CNA's Hebbian update on an averaged correlation is
symmetric in the pair, and the paper notes that near symmetric weights emerge
with no symmetry constraint once the dynamics are stationary. That is the
attention chapter's bidirectional argument in a different substrate: a pairwise
symmetric update accumulates symmetric weights, a directional update does not.
Worth one remark in the discussion, no more.

ACU. A survey does not test a claim. Its role is motivation and a standalone
contribution. Gaps one to three (generalisation, inefficient learning, limited
planning) are the properties whose dependence on the training recipe the core
measures, in the grokking chapter (generalise at all, adapt to a new task) and
the bounded chapter (multi step prediction). Gaps four to six are about
evaluation, and the bounded chapter is one instance of what an evaluation that
tests for the property looks like. The frame may say this and no more.

### Architecture

Part I. Introduction and background. The core claim stated once, with the
table above as its map. Implicit bias and conservation laws. Grokking and its
circuits. Self attention as a bilinear form. Latent world models and rollout
evaluation. Credit assignment rules. Hebbian assemblies.

Part II. The field and what it lacks. ACU (pillar, full chapter). Short
chapter: LLM benchmark and COGITAO, with the author's role stated first.

Part III. Structure the data do not supply.
- Grokking (pillar, leads the part). Rule varied, everything else fixed.
- Attention. Objective varied, backpropagation fixed.
- Bounded. Constraint imposed, and the readout that mistook it for learning.
- Short chapter: Hounsfield and retrieval, structure supplied deliberately
  whose gains survive the controls the bounded chapter asks for.

Part IV. Layout fixed by construction. CNA (pillar, full chapter).

Part V. Discussion. What the task fixes and what the procedure fixes. The two
CNA connections. When to leave layout to the rule, when to fix it by
construction, when to impose a constraint. A world model built from these
pieces as an outlook paragraph, with the sentence that the thesis does not
build one. Conclusion.

### Title candidates

1. Structure the Data Do Not Supply: Objective, Learning Rule and Constraint in
   the Making of a Trained Network
2. Fixed by the Update: How the Objective, the Learning Rule and the Constraint
   Shape What a Network Learns
3. Same Loss, Different Networks: What Fixes the Layout of a Learned Solution

The title names the core. ACU and CNA are not in it, and the introduction says
in one plain paragraph that the thesis has a tested core and two further
contributions. That is the honest shape of a cumulative thesis with this paper
set.

### Draft abstract

A trained network is shaped by its data and by the procedure that trained it,
and the two are rarely told apart. This thesis shows in three settings that the
weight update carries structure the data do not supply, that this structure
comes from the training objective, the learning rule or an imposed constraint,
that the trained network inherits it, and that it can be derived from the
update equation and then verified. Where the literature had read that
structure as a property of the task, or as evidence of learning, it is neither.

The first setting varies the learning rule. In grokking, a network fits its
training data long before it generalises, and the solution can be read at the
level of single neurons. With task, data, architecture and optimizer fixed,
four of twelve rules never generalise, because their update does not vanish at
the minima of the loss and so does not share its fixed points. Among the rules
that do, loss, margin and weight norm agree, and the number of neurons carrying
the solution runs from about 150 to 250 of 256. A tractable model shows why.
Plain gradient flow conserves the ratios of unit norms, so the layout inherits
the initialisation, while a rule that normalises each neuron separately
conserves their differences, so the layout spreads. The group of parameters
that shares one normaliser decides, and that alone places all eight published
optimizers correctly. The layout has a price. Spread solutions survive neuron
deletion far better, and concentrated ones adapt to a new task about twice as
fast.

The second setting varies the objective with backpropagation fixed. The update
to a Transformer's attention weights is a sum over the token pairs the
objective lets one token use to predict another. A bidirectional objective
includes every pair in both orders, so the update is symmetric and symmetry
accumulates in the weights. An autoregressive objective uses each token as
context for every later token but as target once, so a few columns come to
dominate. Both structures appear in ModernBERT, GPT, LLaMA3 and Mistral across
text, vision and audio, and symmetric initialisation speeds up bidirectional
training.

The third setting imposes a constraint, and what the update leaves free becomes
a measurement error. The prediction loss of a latent world model is invariant
to the scale of the latent, so training does not fix that scale, and a spectral
constraint on the transition operator fixes how it grows under rollout. The
standard readout, a probe fitted at training scale, reads that growth. The
constrained model wins by five orders of magnitude under the probe and by
nothing under a scale invariant readout, predictors that learn no dynamics beat
every learned model, and rescaling the spectrum moves the probe curve
monotonically. The constraint does what its theory says. The inference from a
bounded curve to a better model does not follow.

Two further contributions frame these results. A survey of 87 papers and 33
datasets on agents for computer use finds that the field builds its agents by
one recipe and lacks generalisation, efficient learning and planning, the
properties whose dependence on that recipe the three settings measure. The
Cooperative Network Architecture builds a representation in which every active
neuron is supported by others, from fragments learned by Hebbian plasticity. It
tolerates noise on more than half of its inputs and completes occluded figures.
Its layout is fixed by construction rather than left to the rule, at the cost
of not yet scaling beyond line drawings.

## 7. Chosen framing: the layout of a learned solution (2026-09-06)

The author chose framing C from the five in the chat: how a solution is spread
across neurons, what decides it, and what it costs. This section develops it.

### The spine

A network that has learned a task could have laid its solution out in many
ways. The same function, at the same loss, margin and weight norm, can be
carried by a few neurons or spread across all of them, and the weight matrix
that carries a computation can concentrate on a few columns or spread evenly.
We call the way a computation is distributed over a network's parts, whether
neurons or the rows and columns of a weight matrix, the solution's layout.
(Definition first, then the name. One definition site, in the introduction.)

Neuroscience has argued about sparse against distributed coding for decades:
distributed codes degrade gracefully under neuron loss, sparse codes learn new
associations with less interference. Machine learning has mostly assumed the
task decides the layout. The grokking literature reads the sparse circuit as
what the task demands, and the universality claim in interpretability says
every network solving a task finds the same circuit.

Thesis in one sentence. Among the many networks that solve a task equally
well, how the solution is spread across neurons is decided by the training
procedure and not by the task, it can be read off the update equation and
chosen, and the choice trades robustness to damage against speed of adaptation.

### The arc

Agents built from foundation models are the stake, and the survey shows the
field builds them by one recipe and lacks efficient learning and
generalisation. Those are properties of the trained network, so the thesis
asks what in training decides them, and finds that a quantity nobody in the
recipe varies, the learning rule, decides the layout of the solution, and the
layout decides how the network survives damage and how fast it adapts. The
same question asked of a Transformer's attention weights gives the same
answer one level up: the objective decides whether a few columns carry the
computation. If the rule decides the layout, an architecture can fix it
instead, and the Cooperative Network Architecture is a layout in which every
active neuron is supported by others, with the robustness and completion that
predicts. The last part turns to method: a property the loss leaves free can
also be imposed and misread, and the world model chapter shows how, which is
why every layout claim in the thesis is made at matched loss, margin and norm
and against trivial baselines.

### Research questions

1. Is the layout of a learned solution fixed by the task or by the procedure
   that trained the network? (grokking, attention)
2. Can the layout be predicted from the training rule without training the
   rule, and can it be chosen? (grokking grain law and credit knob, attention
   symmetric initialisation)
3. What does a layout cost, and can the cost be avoided by fixing the layout
   in the architecture? (grokking trade off, CNA)
4. How is a property that training fixed told from one a constraint imposed
   and a readout misread? (bounded, and the controls used throughout)

The survey frames why questions 1 to 3 matter for agents. It does not test
them.

### Exact links, chapter by chapter

| Chapter | Layout statement | Method | Status in the argument |
| --- | --- | --- | --- |
| ACU survey | none. Names inefficient learning (gap 2) and insufficient generalisation (gap 1) as what agents built by one recipe lack | survey of 87 papers, 33 datasets | motivation, standalone contribution, leads Part II |
| Grokking | the rule decides how many neurons carry the solution at equal loss, margin and norm (about 150 to 250 of 256); direction decides whether a solution forms at all; grain law predicts 8 of 8 optimizers; knob moves layout from the start or after grokking; fluctuation under deletion falls as $1/\sqrt{n\,\mathrm{PR}}$; adaptation about twice as fast at the concentrated end | controlled variation of the rule, twelve published rules, tractable model with proofs | pillar, leads Part III |
| Attention | the objective decides the layout across the columns of $W_{qk}$: autoregressive training uses a token as context many times and as target once, so a few columns dominate; bidirectional training enters each pair in both orders, so the update is symmetric and the structure spreads | derivation from the update, verification on four model families and three modalities, symmetric initialisation | second chapter of Part III |
| CNA | a layout fixed by construction: a net is a set of neurons each supported by several others, so unsupported noise is filtered at more than half the input corrupted and missing parts are completed; fragments recombine into patterns not seen in training | architecture, Hebbian learning, qualitative and quantitative demonstrations on line drawings | pillar, leads Part IV |
| Bounded | not a layout result. A second property the loss leaves free, latent scale, is fixed by a constraint and read by the probe as learning | controlled comparison, trivial baselines, two readouts, intervention on the spectrum, scale aware loss | method chapter, leads Part V |
| Hounsfield, retrieval | structure supplied from outside (input masks, external index) whose gains survive the controls Part V asks for | | short chapter in Part V |
| LLM benchmark, COGITAO | two places where the standard recipe's benchmark number and its capability diverge | | short chapter in Part II |

### Parts and chapters

Part I. Introduction and background. Layout defined once. Sparse against
distributed coding. Implicit bias and conservation laws of gradient flow.
Grokking and its circuits, the universality claim. Self attention as a
bilinear form. Assemblies and Hebbian learning. Latent world models and
rollout evaluation.

Part II. Agents built by one recipe.
- ACU survey (pillar).
- Short chapter: LLM benchmark and COGITAO.

Part III. The training procedure decides the layout.
- Grokking (pillar). Rule varied, everything else fixed.
- Attention. Objective varied, backpropagation fixed.

Part IV. A layout fixed by construction.
- CNA (pillar).

Part V. Telling what training fixed from what was imposed.
- Bounded.
- Short chapter: Hounsfield and retrieval.

Part VI. Discussion and conclusion. Universality holds at the level of the
computation and fails at the level of the layout. The trade off as a design
axis: leave the layout to the rule and choose the rule, fix it by
construction, or impose it and check with the controls of Part V. Outlook, one
paragraph: an agent's model of its environment whose state is a net and whose
transition is learned by a per unit rule, with the sentence that the thesis
does not build it.

### Guardrails

- Robustness to damage (unit deletion, weight noise) is not robustness to a
  changing environment. The survey's deployment gap is about the latter. Do
  not join them in one sentence.
- CNA does not measure participation or run the deletion protocol. The link is
  the mechanism, redundancy of support, and is stated as such.
- The attention paper does not compute participation on $W_{qk}$. "Layout
  across columns" is the thesis's reading of column dominance and must be
  introduced as that.
- Bounded is about scale, not layout. It enters as the general concept, a
  property the loss leaves free, of which layout is the thesis's main
  instance.
- Universality fails at the layout level is a grokking result. Do not extend
  it to attention or CNA.
- The neuroscience outlook is one paragraph.

### Optional thesis owned glue, each turning a conceptual link into a measured one

1. Participation ratio over the columns and rows of $W_{qk}$ for the pretrained
   models of the attention chapter. One figure, one measure shared with the
   grokking chapter. Low effort, needs the released checkpoints.
2. Unit deletion on CNA nets, and the mean number of supporters per active
   neuron as the effective unit count. Moderate effort, needs the CNA code.
Neither is promised in the abstract until it exists.

### Title candidates

1. Sparse or Distributed Is a Choice: How Training Decides the Layout of a
   Neural Network's Solution, and What the Layout Costs
2. The Layout of a Learned Solution: Decided by the Learning Rule, Paid for in
   Robustness and Adaptation
3. Few Neurons or Many: What Decides How a Network Lays Out Its Solution

### Draft abstract

A network that has learned a task could have laid its solution out in many
ways. The same function, at the same loss, can be carried by a few of its
neurons or spread across all of them, and the weights that carry a
computation can concentrate on a few directions or spread evenly. Neuroscience
has long argued about sparse against distributed coding, and machine learning
has mostly assumed that the task decides: a grokked network is said to reach a
sparse circuit whenever the task offers one. This thesis shows that the layout
of a learned solution is decided by the training procedure, that it can be
read off the update equation and chosen, and that the choice trades robustness
to damage against speed of adaptation.

The central study holds task, data, architecture and optimizer fixed and
varies only the learning rule, in the grokking setting where a network fits
its training data long before it generalises and its solution can be read
neuron by neuron. Four of twelve rules never generalise, because their update
does not vanish at the minima of the loss. Among those that do, loss, margin
and weight norm agree while the number of neurons carrying the solution runs
from about 150 to 250 of 256. A rescaling of each neuron's share of the error
that provably leaves the objective and every update direction unchanged moves
that number across its full range, whether applied from the start or switched
on after the network has generalised, so the layout is a state the rule
maintains. Which rules spread the solution can be read from their update. Only
rules that normalise one neuron at a time do, because a shared normaliser
leaves the inequality within its group untouched, and that prediction places
all eight published optimizers correctly. The layout has a price, proven and
measured. Spread solutions survive neuron deletion far better, with the
fluctuation falling as one over the square root of the effective number of
units, and concentrated ones adapt to a new task about twice as fast.

The same question is asked of the weights that carry attention in a
Transformer. Their update is a sum over the token pairs the objective lets one
token use to predict another. An autoregressive objective uses each token as
context for every later token but as target once, so a few columns come to
dominate, and a bidirectional objective enters every pair in both orders, so
the update is symmetric and the structure spreads. Both layouts appear in
ModernBERT, GPT, LLaMA3 and Mistral across text, vision and audio, and
initialising the weights symmetrically speeds up bidirectional training.

Where the learning rule leaves the layout to be decided, an architecture can
fix it. The Cooperative Network Architecture represents a sensory pattern by a
net, a set of neurons each supported by several others, assembled from
fragments learned by Hebbian plasticity. Because support is built in, noise,
which has none, is filtered even when more than half of the input is
corrupted, occluded figures are completed, and fragments recombine into
patterns never seen in training, at the cost of a model that does not yet
scale beyond line drawings.

A property the loss leaves free can also be imposed and then misread. In
latent world models the prediction loss is invariant to latent scale, a
spectral constraint on the transition operator fixes how that scale grows
under rollout, and the standard probe reads exactly that growth. The
constrained model wins by five orders of magnitude under the probe and by
nothing under a scale invariant readout, and predictors that learn no dynamics
beat every learned model. The controls that expose this are the ones every
layout claim in the thesis rests on: matched loss, margin and norm, and
trivial baselines.

The thesis opens with a survey of 87 papers and 33 datasets on agents for
computer use. It finds that the field builds its agents by one recipe and
names inefficient learning and insufficient generalisation among its gaps, two
of the properties the layout results show to depend on a choice that recipe
never varies.

## 8. Amendment: CNA as the closing proposal (2026-09-06)

The author wants CNA positioned as the outlook, a proposal for where the field
should go, rather than as a pillar in the middle. Section 7 stands except for
the following.

### Revised arc

Findings, then method, then proposal. Parts III and IV establish that the
layout is left to the rule, that it has a price, and how to tell a property
training fixed from one a constraint imposed. Part V draws the consequence: if
the rule decides the layout and the layout has a price, fix the layout in the
architecture and let learning fill in its parts. CNA is the first
implementation of that proposal, presented as a proposal, with what it shows
and what it lacks. The world model the PIs care about is the far end of the
same proposal, stated as what a net based representation would need in order
to serve as the state of an agent's model of its environment.

### Revised parts

Part I. Introduction and background.
Part II. Agents built by one recipe. ACU (pillar). Short chapter: LLM
benchmark and COGITAO.
Part III. The training procedure decides the layout. Grokking (pillar), then
attention.
Part IV. Telling what training fixed from what was imposed. Bounded. Short
chapter: Hounsfield and retrieval.
Part V. A layout fixed by construction. CNA, as the proposal. Its chapter
introduction states the proposal and derives it from Parts III and IV. Its
chapter summary states what the implementation shows, what it lacks, and the
steps to a representation an agent could plan over: learned features, several
interacting areas, mappings between nets for invariance, and dynamics over
nets learned by a per unit rule.
Part VI. Discussion and conclusion. Shorter than before, since the outlook
lives in Part V. Universality at the computation, not the layout. The trade
off as a design axis. Limitations.

### Research question 5

Added to the four of section 7: given that the rule decides the layout and the
layout has a price, can the layout be fixed by construction instead, and what
would that buy? Answered as a proposal with a first implementation, not as a
finding.

### Revised abstract

A network that has learned a task could have laid its solution out in many
ways. The same function, at the same loss, can be carried by a few of its
neurons or spread across all of them, and the weights that carry a
computation can concentrate on a few directions or spread evenly. Neuroscience
has long argued about sparse against distributed coding, and machine learning
has mostly assumed that the task decides: a grokked network is said to reach a
sparse circuit whenever the task offers one. This thesis shows that the layout
of a learned solution is decided by the training procedure, that it can be
read off the update equation and chosen, and that the choice trades robustness
to damage against speed of adaptation. It closes with a proposal for
representations in which the layout is built in rather than left to the rule.

The stake is set by a survey of 87 papers and 33 datasets on agents for
computer use. The field builds its agents by one recipe, a pretrained
foundation model adapted by prompting or behaviour cloning, and names
inefficient learning and insufficient generalisation among its gaps. Both are
properties of the trained network, so the thesis asks what in that recipe
decides them.

The central study holds task, data, architecture and optimizer fixed and
varies only the learning rule, in the grokking setting where a network fits
its training data long before it generalises and its solution can be read
neuron by neuron. Four of twelve rules never generalise, because their update
does not vanish at the minima of the loss. Among those that do, loss, margin
and weight norm agree while the number of neurons carrying the solution runs
from about 150 to 250 of 256. A rescaling of each neuron's share of the error
that provably leaves the objective and every update direction unchanged moves
that number across its full range, whether applied from the start or switched
on after the network has generalised, so the layout is a state the rule
maintains. Which rules spread the solution can be read from their update. Only
rules that normalise one neuron at a time do, because a shared normaliser
leaves the inequality within its group untouched, and that prediction places
all eight published optimizers correctly. The layout has a price, proven and
measured. Spread solutions survive neuron deletion far better, with the
fluctuation falling as one over the square root of the effective number of
units, and concentrated ones adapt to a new task about twice as fast.

The same question is asked of the weights that carry attention in a
Transformer. Their update is a sum over the token pairs the objective lets one
token use to predict another. An autoregressive objective uses each token as
context for every later token but as target once, so a few columns come to
dominate, and a bidirectional objective enters every pair in both orders, so
the update is symmetric and the structure spreads. Both layouts appear in
ModernBERT, GPT, LLaMA3 and Mistral across text, vision and audio, and
initialising the weights symmetrically speeds up bidirectional training.

A property the loss leaves free can also be imposed and then misread. In
latent world models the prediction loss is invariant to latent scale, a
spectral constraint on the transition operator fixes how that scale grows
under rollout, and the standard probe reads exactly that growth. The
constrained model wins by five orders of magnitude under the probe and by
nothing under a scale invariant readout, and predictors that learn no dynamics
beat every learned model. The controls that expose this are the ones every
layout claim in the thesis rests on: matched loss, margin and norm, and
trivial baselines.

If the learning rule decides the layout and the layout has a price, the layout
can instead be fixed in the architecture and learning left to fill in its
parts. The Cooperative Network Architecture is a first implementation of that
proposal. It represents a sensory pattern by a net, a set of neurons each
supported by several others, assembled from fragments learned by Hebbian
plasticity. Because support is built in, noise, which has none, is filtered
even when more than half of the input is corrupted, occluded figures are
completed, and fragments recombine into patterns never seen in training. The
model does not yet scale beyond line drawings, and the thesis ends by setting
out what a representation of this kind would need in order to serve as the
state of an agent's model of its environment.

## 9. Amendment: Bounded as a side chapter (2026-09-06)

The author judges the bounded paper not strong and wants it as a side chapter
with little focus. Section 8 stands except for the following.

### Revised parts

Part I. Introduction and background.
Part II. Agents built by one recipe. ACU (pillar). Short chapter: LLM
benchmark and COGITAO.
Part III. The training procedure decides the layout. Grokking (pillar), then
attention.
Part IV. Structure supplied from outside the data. Three short chapters, each
with the author's role stated first: the world model study (a spectral
constraint on latent dynamics), Hounsfield (input masks from medical
knowledge), retrieval (an external index at inference time). The part's one
lesson, stated in its opening and in the world model chapter: structure
supplied from outside must be measured against trivial baselines and with a
readout the structure alone cannot satisfy. Whether the world model paper is
imported in full or summarised depends on whether it is published by
submission. Default: summarised in a few pages.
Part V. A layout fixed by construction. CNA as the proposal.
Part VI. Discussion and conclusion.

Each pillar still leads its own part. The method lesson that section 7 gave a
whole part now takes one paragraph in the grokking chapter, where it belongs:
every layout claim is made at matched loss, margin and weight norm and against
imposed and permuted profiles as trivial controls.

### Research questions, final

1. Is the layout of a learned solution fixed by the task or by the procedure
   that trained the network? (grokking, attention)
2. Can the layout be predicted from the training rule without training it, and
   can it be chosen? (grokking, attention)
3. What does a layout cost? (grokking)
4. Given that the rule decides the layout and the layout has a price, can the
   layout be fixed by construction instead, and what would that buy? (CNA, as
   a proposal)

The survey frames why 1 to 3 matter for agents. Part IV supplies three applied
instances of structure from outside the data and one cautionary measurement.
Neither tests the questions.

### Revised abstract paragraph replacing the bounded paragraph of section 8

Three shorter studies supply structure from outside the data: a spectral
constraint on the latent dynamics of a world model, input masks derived from
medical knowledge for CT segmentation, and an external index for retrieving
scientific sources from social media posts. The last two pass their controls.
The first is the cautionary case: the constraint wins by five orders of
magnitude under the standard probe and by nothing under a readout that ignores
latent scale, and predictors that learn no dynamics beat every learned model,
so a property the loss leaves free had been imposed and read as learning.

The rest of the abstract in section 8 stands: opening, survey, grokking,
attention, then this paragraph, then the CNA proposal as the close.

## 10. Open proposal: the circuit arc (2026-09-12)

**Status: not decided. This is the author's proposal, written down so that the
next session starts by comparing it against section 9 and `05_thesis_concept.md`
rather than assuming the settled story still holds.**

Why it was raised. The Koopman paper turned into an evaluation paper, and the
settled story puts it in Part IV as a short cautionary chapter. The author's
reading is that an evaluation result of that kind can carry more than a side
chapter, and that the paper set may tell a different story with it in second
position.

### The arc, as the author stated it

1. ACU survey. This is where the field is going, AI interacting with the
   physical world. It closes on the open issues, and on the claim that they
   need a real understanding of the world.
2. World model paper, now an evaluation paper. Long horizon prediction is the
   problem, and it needs proper evaluation before anything else is claimed.
3. Attention. Besides evaluating properly, the right thing has to be learned.
   This chapter asks what is actually learned.
4. A critique that what is learned is just statistics.
5. Grokking. A step towards the generalisation that is needed.
6. CNA. The circuit can be fixed in advance.

### The circuit variant

The same order, with one noun running through every chapter.

| Chapter | Role in the circuit frame |
| --- | --- |
| ACU | which circuit properties would be wanted |
| World model | testing the circuit |
| Attention | what the circuit actually learns |
| Grokking | generalising the circuit |
| CNA | choosing the circuit |

### First pass on what this would have to survive

Listed as questions to answer next session, not as a verdict.

- "Circuit" already has a narrow meaning in the grokking and interpretability
  literature, and the grokking chapter uses it there. Running it across all
  five chapters overloads it, and the survey and the world model chapter do not
  contain one in that sense. The settled story picked "layout" for exactly this
  reason, see section 7. Either the frame defines circuit wider at one site and
  holds that definition everywhere, or it keeps layout and uses circuit only
  where a circuit is meant.
- Step 4, "what is learned is just statistics", is currently a claim with no
  chapter behind it. Which paper tests it? If none does, it is frame rhetoric
  of the kind section 6 rejected.
- Promoting the world model paper to second position reverses the author's own
  judgement in section 9 that it is not strong and belongs as a side chapter.
  That judgement was about the paper, not about its position, so it can be
  revisited, but it has to be revisited on purpose.
- The attention paper is Matteo Saponati's lead. Giving it the "what is
  actually learned" slot makes a supporting chapter carry an argument step.
- Four papers have no slot in this arc: Hounsfield, retrieval, the LLM
  benchmark and COGITAO. Section 9 parks them in two short chapters. Where do
  they go here?
- The ACU opening claims the field is moving towards AI interacting with the
  physical world. The survey is about agents operating software from natural
  language instructions, so the physical framing needs either a different
  source or a narrower sentence.
- What this arc gains over section 9 is a clean chain of needs: evaluate
  properly, then learn the right thing, then generalise, then build it in. What
  it loses is the tested core, one claim that three chapters test with one
  argument, which section 6 identified as the thing that keeps a cumulative
  thesis from reading as a covering story.

### How to decide

Write both arcs as a one page introduction skeleton, three paragraphs each, and
see which one states a claim a chapter tests. Section 6 is the standard to
judge against.
