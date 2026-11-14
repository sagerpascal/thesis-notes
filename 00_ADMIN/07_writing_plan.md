# Writing plan: think, then skeleton, then paragraphs, then prose

The rule this file exists to enforce: no prose is written until the level
above it has been criticised and has survived. The levels are

0. what the thesis must say, claim by claim, with what backs each claim
1. titles
2. subtitles
3. one line per paragraph saying what that paragraph has to do
4. prose

Each level is written, then criticised by readers who are given the material
and the standard but not the reasoning behind it, then revised. A level is
done when a critic cannot find a load bearing objection. The standard is
CLAUDE.md section 3 for style and `05_thesis_concept.md` for the argument.

Status: level 0 and level 1 drafted 2026-11-14. Critique rounds recorded at
the end of each level.

---

## Level 0: what the thesis must say

### The one claim

In a trained network, how a computation is distributed over its neurons is not
fixed by the task. It is fixed by the rule that assigned credit during
training. It can be derived from the update equation, predicted before the
network is trained, and chosen. It is not free: the choice trades tolerance of
damage against how far the network compresses and how fast it transfers.

Everything else in the thesis either supports that claim, establishes the
standard it is measured to, says why it matters, or draws the consequence.

### What backs it, and how far each piece reaches

**S1, grokking, first author, the evidence.** Task, data, architecture and
width fixed, learning rule varied. Every rule that groks modular addition
recovers the same Fourier based algorithm, implemented by circuits of
different size, so the algorithm and its implementation come apart. A neuron
stays in use when its credit is large relative to the non gradient term of its
own update, and that one condition unifies three separate routes to unused
neurons. Equalising credit expands the effective circuit from $60\%$ to $99\%$
of the layer at similar training and test accuracy, and does so even when
switched on after grokking has happened, so the circuit is a state the rule
maintains rather than a path it took. What an optimizer normalises together
decides, which places Nero apart from Adam and seven others. The price:
distributed circuits tolerate neuron deletion, concentrated ones prune further
and transfer about twice as fast by recruiting unused neurons.

Reach: this is the whole claim, demonstrated in one setting. The setting is
small and chosen because the solution can be read neuron by neuron. The thesis
must say that, not hide it.

**S2, attention, shared first, Saponati led, the second level.** The update to
a Transformer's attention weights is a sum over the token pairs the objective
allows. A bidirectional objective enters every pair in both orders, so the
update is symmetric and symmetry accumulates. An autoregressive objective uses
each token as context many times and as target once, so a few columns come to
dominate. Verified in ModernBERT, GPT, LLaMA3 and Mistral across text, vision
and audio. Symmetric initialisation speeds up bidirectional training.

Reach: the same question asked of a weight matrix rather than a layer of
neurons, with the objective as the knob rather than the rule. It is the same
argument in a different substrate and at a scale the grokking setting cannot
reach. It is not the same measurement: the paper does not compute
participation on the attention weights, and "circuit across columns" is the
thesis's reading of column dominance. Say so once, where it is first used.

**S3, world model, first author, unsubmitted, the standard.** A claim about a
trained network is only as good as the readout behind it. The probe the field
uses to score predicted latents is sensitive to a quantity the loss never
fixed, the norm, which drifts during rollout while direction stays accurate.
For one published model, rescaling to the encodings' norm removes $97\%$ of
the probe's error. A worse model that drifts less can rank above a better one.
Re-projection removes the free quantity from the score, with four checks on
what is left.

Reach: it licenses the method the circuit claims use, which is to compare at
matched loss, margin and weight norm and against imposed and permuted controls
that the free quantity alone cannot satisfy. It is not an instance of the one
claim, because the latent norm is not a circuit. The frame says this plainly
rather than stretching the word.

**S4, CNA, first author, the consequence.** If the rule decides the circuit
and the circuit has a price, the circuit can be fixed in the architecture
instead. CNA represents a sensory pattern by a net in which every active
neuron is supported by several others, assembled from fragments learned by
Hebbian plasticity. Noise, which has no support, is filtered when more than
half the input is corrupted. Occluded figures are completed. Fragments
recombine into patterns never trained on.

Reach: a proposal with a first implementation, not a finding. It does not
measure participation, does not run the deletion protocol, and does not scale
beyond line drawings. The code no longer runs, so no new measurement is
coming. The connection to S1 is the mechanism, redundancy of support, and is
named as a mechanism rather than a shared measurement.

**M, the survey, shared first, why it matters.** One recipe, six gaps. Three
are properties of the trained network, three are about how the field measures
what it claims. Motivation only. It does not predict S1 and the thesis never
implies it does.

### The three things the thesis must admit, in the frame, not in a footnote

1. No measurement is shared across the chapters. The link from S1 to S2 and
   from S1 to S4 is an argument about a mechanism. Two cross chapter
   measurements were planned and are not available.
2. The survey is about agents operating software from natural language
   instructions. The distance from there to modular addition is large, and the
   survey carries motivation only.
3. S2 was led by a co-author and S3 is not yet submitted.

### What a committee at this institute will push on

- Modular addition is a toy. Why should anything here hold at scale? The
  honest answer is S2, which is at scale and finds the same kind of structure,
  and the admission that S1's strongest form needs a setting where the circuit
  is readable.
- Is "circuit size" the right measure, or an artefact of the outgoing weight
  norm? S1 answers this in its own appendix and the chapter must point at it.
- Sparse against distributed coding is a neuroscience question about brains.
  What does a network trained by backpropagation say about one? Nothing
  directly, and the thesis says so in one sentence rather than reaching.

---

## Level 1: titles

Statements of findings, per CLAUDE.md 3.8. Abstract first because its
constraint is the tightest.

### Abstract

No coined vocabulary at all, per CLAUDE.md 3.5, so the word *circuit* cannot
appear as a defined term. The abstract says the thing in plain words: how many
neurons carry the computation, spread across many or concentrated in a few.

### Introduction, section titles

1. A task fixes what a network computes, not how many of its neurons carry it
2. The gaps that motivate the question are properties of the trained network
3. The learning rule decides how many neurons carry the computation, and the
   choice has a price
4. The training objective decides the same thing for a weight matrix
5. A readout can report a quantity the loss never fixed
6. A circuit with a price need not be left to the learning rule
7. Research questions
8. Contributions
9. Structure of the thesis

### Background, section titles

The existing skeleton is sound and mostly survives. One reordering is
proposed: the sparse against distributed question moves to the front, because
it is now the thesis's opening question rather than a measure it borrows.

1. How a computation is spread over neurons is an old question with measures
2. Many parameter settings fit the same data, and the procedure picks one
3. The training procedure has parts, and each of them can be varied
4. Grokking is where the circuit can be read off
5. The same question can be asked of a weight matrix, where the objective is
   the knob
6. A claim about a trained network is only as good as its readout
7. A circuit can also be built into the substrate
8. The gap

Section 6 replaces "Structure can be supplied instead of learned, which makes
measurement the hard part", which was written when two applied chapters sat in
that part. They are summarised now, so the section is about readouts.

### Chapter titles still to settle

- `chap:grokking` says "Units" where the noun is circuit. Proposed: *The
  Learning Rule Decides the Size of the Circuit, Not the Algorithm*.
- `chap:bounded` states the previous paper's finding. Proposed: *A State Probe
  Reports Norm Drift Rather Than Prediction Quality*.
- `chap:cna` is *The Cooperative Network Architecture*, a name rather than a
  statement. Proposed: *Support Built Into the Architecture Gives a
  Distributed Code Without the Rule*.
