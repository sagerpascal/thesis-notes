# Hand-off

Branch `rewrite`, cut from `main`. `diff_vs_approved.pdf` marks every change
against the version you approved.

## What the paper claims now

We built a controlled test of whether constraining a latent operator's spectrum
fixes long-horizon prediction. Measured with the probe, it works by five orders
of magnitude. It does not survive two controls that cost one line each: copying
the current latent forward and returning the dataset mean beat every learned
model in 168 of 168 cells at ten steps and beyond. A readout that ignores latent
scale shrinks the five orders of magnitude to a factor of 1.4 without changing
the ordering. The cause is that the probe penalizes a rollout whose latent norm
drifts and the bound behind the constraint limits exactly that drift, so the two
agree by construction: a bounded error curve under a norm-sensitive readout is a
property of the constraint, not evidence of a learned model. We measure the
drift on the operators, move it by rescaling a trained one, and remove it by
changing the prediction loss, which closes the gap and still leaves every model
behind the trivial predictors.

The theory is intact throughout and the paper says so. What fails is the
inference from the guarantee to better prediction.

## How much is your text

**15% of the body is verbatim from your version**, not the 40% the plan
estimated before anything was written. Most of the compression rewrote
sentences rather than keeping them. Your prose survives densest in the bound
(Section 2.2), the protocol (4.2), the architecture (4.1), the opening two
paragraphs of the introduction, and Appendices A, C and D. Everything else is
new and you have not read it.

Your sample-efficiency and robustness results are **not** contradicted. They
hold among the learned models and are reported as holding, in Appendix E. What
the control rows add is that the ordering is between models that all lose.

## Three things for you to decide

1. **The paper says the original claim does not hold.** No framing avoids that.
   The framing chosen makes Koopman-JEPA the instrument rather than the subject,
   which is what makes this a finding rather than a retraction.
2. **The control result is one paragraph plus Appendix D**, down from a full
   section. It is real and it is off the argument. Restoring it to the main text
   costs about half a page.
3. **The body is 12.3 pages against a target of 10**, total 23. `BUILD_STEPS.md`
   lists what the next 1.3 pages would cost, cheapest first. My recommendation
   is to leave it.

## One phrase worth your eye

Appendix A says the selection protocol was "fixed in advance of the final runs".
That is true of the hyperparameter protocol and is not a claim that any result
was predicted in advance, but it is the one sentence in the paper a hostile
reader could take the second way.
