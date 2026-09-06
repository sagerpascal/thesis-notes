# Response to the Editor / Reviewers

We thank the editor for the assessment. The decision raised three substantive
concerns — statistical soundness, hyperparameter setting / baseline tuning, and
positioning in the literature — together with a note on problem scale. We have
substantially revised the paper to address each. In brief:

- **Statistical soundness.** We re-ran the entire empirical study with **10
  seeds per configuration** (was 3) and now report **mean ± 95% bootstrap
  confidence intervals** (B = 10,000) rather than standard deviations, on a
  **held-out test set** that is disjoint from both training and model selection.
- **Hyperparameters / baseline tuning.** Every method — including the MLP-JEPA
  baseline — now has its hyperparameters **tuned independently** by a
  pre-registered selection protocol, and we report the selected values. This
  removes the "all methods share hypers / baseline may be untuned" concern.
- **Related work.** We added a dedicated treatment of prior responses to
  compounding rollout error: training on model rollouts, temporal
  abstraction / options and goal-space planning, decision-time vs. dyna-style
  planning, and value-equivalence models (MuZero and predecessors).

The revision is a clean, from-scratch re-run under a documented protocol; all
figures and tables are regenerated from a single results file. Below we detail
each point.

---

## 1. Statistical soundness

**Concern.** Results used three seeds and reported standard deviations rather
than measures of statistical confidence.

**Changes.**
- **Seeds: 3 → 10.** Every reported cell is now averaged over 10 seeds.
- **Confidence intervals, not std.** All tables report **mean ± 95% bootstrap
  confidence-interval half-width** (10,000 resamples); standard deviation is
  used only to flag baseline divergence (heavy-tailed cases, marked †).
- **Three-way data split with no leakage.** We introduced disjoint
  train / validation / test splits (distinct seeds). Model selection uses the
  **validation** split only; all reported numbers use the **test** split only.
- **A scale-invariant, collapse-robust primary metric.** We report probe-state
  MSE (a two-layer probe to ground-truth physical coordinates), probe $R^2$
  (with $R^2<0$ signalling collapse), and, as a secondary diagnostic, visual
  MSE. During revision we verified that a naive latent-space rollout MSE is
  confounded by representation scale (a model that shrinks its latents scores
  lower irrespective of skill); the probe metric is invariant to this and is
  what we report.
- **Horizon reported explicitly.** Because the contribution is about
  *compounding* error, we now report the full error-growth curve over
  $n\in\{1,5,10,20,30,50\}$ (Fig. "compounding") and give both $T{=}10$ and
  $T{=}20$ side by side in the main table, so the linear-vs-exponential growth
  is directly visible rather than summarized at a single horizon.

**Effect on conclusions.** The core claim strengthens and sharpens: the
eigenvalue-constrained variants keep rollout error bounded while the baseline
and the unconstrained linear variant diverge by many orders of magnitude at long
horizon, with tight confidence intervals over 10 seeds.

## 2. Hyperparameter selection and a fairly-tuned baseline

**Concern.** There was no discussion of how hyperparameters were set; it
appeared all methods used the same hyperparameters, so the baseline might be
untuned, making the comparison against JEPA hard to evaluate.

**Changes.** We added a pre-registered selection protocol (now described in
Section "Methods"/Appendix) and tuned **each method independently**:

- **Selection criterion.** 1-step probe-state MSE on the **held-out validation**
  set — a short-horizon, scale-invariant, collapse-robust, method-agnostic
  criterion. It deliberately does *not* optimize the long-horizon behavior we
  report, so the long-horizon results are out-of-criterion (they cannot be an
  artifact of selecting for the reported horizon).
- **Staged search that preserves the controlled comparison.**
  (A) We first search the **MLP-JEPA baseline** over both encoder architecture
  and optimization/loss hyperparameters (32 random-search trials per
  environment); the winning encoder defines the shared architecture.
  (B) We then **fix that encoder** and search the optimization/loss
  hyperparameters of each Koopman variant independently (32 trials each). This
  gives the baseline its own best architecture *and* keeps the "only the
  dynamics module differs" comparison intact.
- **Reported.** The selected per-method hyperparameters are now given in a
  dedicated table; training is 2000 epochs with best-validation checkpoint
  selection (early stopping applied identically to all methods, so no method is
  advantaged by the training-length choice).

**A clarifying finding this enabled.** With a properly-tuned baseline, the
**unconstrained** linear Koopman variant diverges *alongside* the MLP baseline,
whereas the constrained variants stay bounded. This isolates the eigenvalue
constraint — not linearity per se — as the source of the improvement, which we
now state explicitly.

## 3. Positioning in the literature

**Concern.** The work was not situated against temporal abstraction / options,
E. Talvitie's work, decision-time vs. dyna-style planning, goal-space planning,
or value-equivalence models (e.g., MuZero) — all of which address compounding
rollout error.

**Changes.** We added a dedicated related-work paragraph, "Alternative Responses
to Compounding Rollout Error," that discusses these threads and positions our
contribution as complementary:

- **Training on model rollouts** — Talvitie (2014, 2017): correct the error
  distribution the model actually encounters at rollout time.
- **Temporal abstraction / options and goal-space planning** — Lo et al. (2024):
  predict multi-step transitions directly so per-step error does not chain.
- **Decision-time vs. dyna-style planning and rollout horizon as a design
  choice** — Holland et al. (2019).
- **Value-equivalence models** — the Predictron, Value Prediction Networks, and
  MuZero: train the latent dynamics to predict values/rewards rather than
  reconstruct observations.

Our approach is complementary: we keep a one-step latent model and the standard
JEPA objective, and instead constrain the transition operator to be globally
linear with controlled spectrum, which bounds worst-case error growth
structurally and (for the Cayley variant) yields the algebraic preconditions for
closed-form control.

## 4. On problem scale

The decision also noted the problems are small (though image-based). We
deliberately retain pendulum- and cartpole-swingup because their analytically
known ground-truth physical state is what lets us validate the spectral claim
against known physics rather than through proxies alone; we now strengthen the
*statistical* treatment on these benchmarks (10 seeds, CIs, held-out test,
long-horizon curves) and discuss scaling to contact-rich, visually complex
environments explicitly in the Limitations and Future Work.

---

## Summary of headline results after revision

- **Long-horizon stability (clean, 10 seeds, 95% CI).** Pendulum: the
  constrained variants keep 20-step probe-state MSE essentially flat
  (Koopman-Stable ≈ 0.44) while the MLP baseline and the unconstrained variant
  diverge (≈ 1.5×10⁴ and ≈ 4.5×10⁶). At 10 steps the best constrained variant
  reduces error by 90–92%. Cartpole: Koopman-Stable reduces 20-step error by 98%.
- **Constraint, not linearity.** The unconstrained linear variant diverges with
  the baseline; only the eigenvalue-constrained variants stay bounded.
- **Sample efficiency.** At 10% of the data the constrained variants reach a
  10-step error below the baseline trained on the full dataset.
- **Closed-form control.** Regenerating the LQR analysis on the tuned models
  gives spectral radii ρ(K) = 1.00 / 1.04 / 1.43 and gain norms
  ‖L‖_F ≈ 10.3 / 55 / 5×10⁵ for Stable / Soft / Unconstrained — a
  near-five-orders-of-magnitude gap between the Cayley and unconstrained
  variants, confirming the stabilizability claim.

## Reproducibility

The full pipeline is scripted and pre-registered: a documented protocol
(`sweeps/PROTOCOL.md`), a staged hyperparameter search with a fixed selection
criterion, deterministic run manifests with contamination guards, held-out
test-set evaluation over horizons 1–50, and generators that produce every figure
and table in the paper from a single results file. This makes the revised
empirical study straightforward to reproduce end to end.
