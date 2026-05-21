# PhD Thesis Outline
**Institution:** University of Zurich — Institute of Neuroinformatics  
**Start Date:** 01 October 2023  
**Status:** Draft Outline — v0.1

---

## Proposed Title

**"From Statistical Correlations to Structured Intelligence: Diagnosing Limitations of Deep Learning and Paths Toward Neuro-Inspired Solutions"**

*(Working title — alternative framings possible once all papers are finalised)*

---

## Publications and Contributions

The following table summarises all publications forming the basis of this thesis. Per UZH cumulative thesis conventions, chapters are structured to reflect the candidate's primary contributions.

| Paper | Role | Thesis Status |
|---|---|---|
| ACU Survey | Shared First Author | Main chapter |
| Self-Attention Structures | Shared First Author | Main chapter |
| Koopman-JEPA | First Author | Main chapter |
| CNA | First Author | Main chapter |
| Deep Retrieval / CheckThat! 2025 | First Author | Supporting section |
| HU Ranges for CT Segmentation | Shared First Author | Supporting section |
| Private LLM Survey | Evaluator | Contextual reference |
| COGITAO | Tester | Contextual reference |
| DFC Paper (planned) | First Author | Placeholder chapter |

---

## Part 0: Preamble

### Chapter 1: Introduction

**1.1 Motivation and Research Context**  
The recent decade has seen deep learning achieve remarkable performance across vision, language, and sequential decision-making. Yet as these systems are deployed in increasingly demanding settings, recurring failure modes emerge: brittleness under distribution shift, inability to compose learned concepts, exponentially compounding errors in multi-step prediction, and opaque representational structures that resist theoretical understanding. This thesis argues that these failures share a common root: current architectures learn structured statistical correlations rather than grounded, invariant representations of the world — and that meeting this challenge requires both careful constraint design and, ultimately, a paradigm shift toward neuro-inspired learning principles.

**1.2 Research Questions**
1. What are the concrete failure modes of state-of-the-art deep learning systems when deployed in real-world settings?
2. What structural properties of learned representations underlie these failures?
3. Can hard inductive constraints — imposed architecturally or via domain knowledge — meaningfully mitigate these failures?
4. Can alternative, neuro-inspired learning paradigms address the limitations that constraint engineering alone cannot?

**1.3 Thesis Contributions** *(brief enumeration — to be expanded into full abstract after outline is confirmed)*

**1.4 Thesis Structure and Reading Guide**

---

### Chapter 2: Background

**2.1 Deep Learning Foundations Relevant to This Thesis**  
- Backpropagation and gradient-based optimisation
- Transformer architectures and self-attention
- World models and predictive learning

**2.2 Relevant Neuro-Inspired Concepts**  
- Predictive coding and feedback control
- Compositional and structured representations in biological vision
- Koopman operator theory as a bridge between dynamical systems and learning

**2.3 Scope and Positioning of This Thesis**

---

## Part I: The State of Current AI — Identifying Limitations

*Narrative: Before proposing solutions, we must clearly characterise the problem space. This part surveys the landscape of a highly promising and actively deployed class of AI systems — agents for computer use — to establish, concretely and comprehensively, where current deep learning falls short. Two contextual papers corroborate the argument from independent angles.*

---

### Chapter 3: Agents for Computer Use — A Systematic Survey of Capabilities and Gaps *(Main Paper)*

**Role:** Shared First Author  
**Contribution:** Full chapter treatment

**3.1 Introduction and Motivation**  
Agents for computer use (ACUs) represent one of the most ambitious deployments of modern AI: systems that must perceive dynamic interfaces, plan multi-step sequences, and execute precise low-level actions. As such, they are an ideal diagnostic lens — their failure modes are symptomatic of the field's deepest open problems.

**3.2 A Multifaceted Taxonomy of ACUs**  
- Domain perspective: operating contexts
- Interaction perspective: observation and action modalities
- Agent perspective: perception, reasoning, and learning

**3.3 Survey of 87 Research Papers and 33 Benchmarks**  
- Trajectory from specialised to foundation-model-based agents
- Shift from text-based to vision-based observation spaces
- Rise of behaviour cloning methodologies

**3.4 Six Identified Research Gaps**  
- Insufficient generalisation
- Inefficient learning
- Limited planning
- Benchmark complexity mismatch
- Non-standardised evaluation
- Disconnection from real-world deployment constraints

**3.5 Implications: What ACU Gaps Reveal About Deep Learning Broadly**  
This section serves as the bridge from the survey to the thesis argument: the identified gaps are not engineering shortcomings of ACU systems specifically — they are expressions of structural properties of the underlying learning paradigm.

---

### Chapter 4: Contextual Evidence — Efficiency and Generalization Limitations

*This chapter synthesises two supporting publications in which the candidate's contribution was targeted rather than leading. Each receives a focused 1–2 page discussion; together, they triangulate the thesis argument from two independent directions: computational cost and compositional failure.*

**4.1 The Computational Cost of Current AI (≈1 page)**  
Drawing on the private LLM survey (candidate contribution: benchmark evaluation), this section examines why state-of-the-art models are computationally intractable for private deployment, and what this reveals about the scaling-centric assumptions underpinning current paradigms. Key finding: quantisation methods, despite their appeal, introduce non-trivial quality degradation — demonstrating that efficiency and capability are in tension without architectural innovation.

**4.2 Compositional Generalization Remains Unsolved (≈1 page)**  
Drawing on COGITAO (candidate contribution: evaluation of MLDM on the benchmark), this section examines the persistent failure of state-of-the-art models — including architectures with strong inductive biases for compositionality — to generalize to novel rule combinations. This corroborates the ACU survey's generalization gap from a controlled, formal evaluation perspective.

**4.3 Synthesis: A Consistent Pattern of Failure**  
The failures catalogued in Chapters 3 and 4 are not isolated — they reflect a consistent limitation across scales, modalities, and deployment contexts.

---

## Part II: Root Causes — What Backpropagation Actually Learns

*Narrative: Having established the empirical failure landscape, we turn to theory. This part presents a mathematical analysis of the representational structures that backpropagation-trained Transformers actually produce — and argues that these structures are a direct consequence of the training objective, not a bug to be patched.*

---

### Chapter 5: The Mathematical Structure of Self-Attention — Symmetry, Directionality, and Statistical Correlation *(Main Paper)*

**Role:** Shared First Author  
**Contribution:** Led experiments across all model families and modalities; theoretical framework developed jointly

**5.1 Introduction: The Black Box of Representation Learning**

**5.2 A Mathematical Framework for Self-Attention Matrices**  
Derivation of the structures governing weight updates; analysis of how objective functions shape the geometry of learned representations.

**5.3 Bidirectional Training Induces Symmetry**  
Formal result: bidirectional objectives produce symmetric weight matrices. Validated empirically on ModernBERT across text, vision, and audio.

**5.4 Autoregressive Training Induces Directionality and Column Dominance**  
Formal result and empirical validation on GPT, LLaMA3, and Mistral. Column dominance as a structural footprint of causal masking.

**5.5 Symmetric Initialization Improves Encoder Performance**  
Applied result: exploiting the theoretical insight yields measurable gains on language tasks.

**5.6 Interpretive Discussion: Representations as Statistical Artifacts**  
The core thesis claim, established formally: the geometry of learned representations is determined by the statistical structure of the training objective. This explains the generalisation and compositionality failures identified in Part I — models are not learning causal, invariant structure, but optimally encoding statistical co-occurrence patterns as shaped by the loss. This sets the motivation for Part III (constraint-based mitigation) and Part IV (paradigm change).

---

## Part III: Mitigating the Limitations — Hard Constraints and Inductive Biases

*Narrative: Given the structural diagnosis of Part II, this part explores whether imposing hard mathematical or domain constraints on deep learning systems can correct for the failure modes — and where such approaches reach their limits.*

---

### Chapter 6: Koopman-JEPA — Enforcing Linear Dynamics for Stable World Models *(Main Paper)*

**Role:** First Author (manuscript in preparation)  
**Contribution:** Full chapter treatment

**6.1 The Problem: Exponential Error Accumulation in World Models**  
Multi-step prediction in learned world models compounds approximation errors exponentially: chaining a nonlinear function amplifies each step's error by its Lipschitz constant, causing long-horizon rollouts to diverge. We show this failure is structural — a mathematical property of nonlinear function composition, not a training deficiency.

**6.2 The Koopman Operator Approach**  
By lifting visual observations into a latent space where dynamics are globally linear, temporal rollouts reduce to matrix multiplications. Error accumulation is bounded linearly rather than exponentially.

**6.3 Self-Supervised Learning via a JEPA Objective**  
The predictability-maximising JEPA objective makes linear lifting tractable for high-dimensional visual inputs, avoiding the computational cost of pixel-level reconstruction.

**6.4 Three Variants and the Cayley Parameterization**  
Progressive spectral constraints on the transition matrix, culminating in a Cayley parameterization that architecturally enforces strict stability.

**6.5 Empirical Results**  
- Up to 99% reduction in physical-state prediction error at 10-step horizon (action-free tasks)
- Up to 91% reduction on action-conditioned tasks
- Robust tracking where the baseline diverges catastrophically (24.4 ± 29.2 vs. 0.250 ± 0.012)
- ~16× improvement in sample efficiency at 10% training data

**6.6 Theoretical Analysis: Stabilizability and Discrete-Time LQR**  
Only the Cayley parameterization satisfies the stabilizability precondition of discrete-time LQR — confirmed empirically by a four-orders-of-magnitude difference in DARE gain norms. This connects the architectural choice to formal control theory.

**6.7 Discussion: The Power and Limits of Hard Constraints**  
Koopman-JEPA demonstrates that imposing mathematically grounded constraints can correct specific, structurally identified failure modes. But constraint design requires knowing the geometry of the failure in advance — a limitation that motivates the paradigm shift in Part IV.

---

### Chapter 7: Complementary Constraint Strategies — Domain Knowledge and Inference-Time Grounding

*Two supporting publications, each receiving focused treatment (~1–2 pages), illustrating that the constraint approach generalises across domains and mechanisms.*

**7.1 Input-Space Constraints via Domain Knowledge: Hounsfield Units for CT Segmentation (≈1.5 pages)**  
**Role:** Shared First Author (framing and conceptual contribution)

By encoding tissue-specific Hounsfield unit ranges as binary masks — hard constraints derived from medical literature — segmentation models achieve up to 5% improvement in intramuscular adipose tissue segmentation and match full-data performance using only 50% of training samples. This is a clean instance of the thesis argument: explicit domain knowledge as an inductive bias compensates for the statistical limitations of unconstrained learning.

**7.2 Inference-Time Grounding via Hybrid Retrieval (≈1.5 pages)**  
**Role:** First Author

The Deep Retrieval system (1st on development leaderboard, 3rd on test leaderboard, CLEF CheckThat! 2025) combines BM25 lexical matching, dense semantic retrieval with a fine-tuned INF-Retriever-v1, and LLM-based cross-encoder re-ranking. This represents a different axis of constraint: rather than architectural or input-space constraints, knowledge is retrieved and grounded at inference time. This addresses a distinct failure mode — the inability of parametric models to access precise factual knowledge — by outsourcing it to a structured external index.

**7.3 Synthesis: A Taxonomy of Constraint Strategies**  
Together, Chapters 6 and 7 map out three constraint regimes:
- **Architectural constraints** (Koopman-JEPA): embed mathematical structure into the model itself
- **Input-space constraints** (HU ranges): encode domain knowledge into the representation
- **Inference-time constraints** (retrieval): ground predictions in external knowledge at test time

Each addresses a different failure mode; none alone resolves the fundamental issue identified in Part II. This motivates Part IV.

---

## Part IV: A Change of Paradigm — Neuro-Inspired Architectures

*Narrative: The constraint-based approaches of Part III are powerful but reactive — they require knowing the shape of the failure in advance. This part argues that a deeper solution lies in rethinking the learning paradigm itself, drawing inspiration from how biological neural systems construct structured, invariant representations.*

---

### Chapter 8: The Cooperative Network Architecture — Structured Assemblies as an Alternative to Distributed Representations *(Main Paper)*

**Role:** First Author  
**Contribution:** Full chapter treatment

**8.1 Motivation: From Pattern Matching to Structured Representation**  
Standard deep learning encodes inputs into distributed, unstructured activation patterns. CNA instead represents sensory signals through dynamically assembled, structured networks of neurons ("nets") — a fundamentally different computational strategy.

**8.2 Architecture: Net Fragments, Assembly, and Recurrent Structure**  
- Nets as recurrently connected networks of neurons
- Net fragments learned from statistical regularities in sensory input
- Dynamic assembly via overlapping fragment matching

**8.3 Unsupervised Learning of Compositional Representations**  
Net fragments can be learned without supervision and flexibly recombined to encode novel patterns — directly addressing the compositionality failures identified in Chapter 4.

**8.4 Empirical Properties**  
- Figure completion and noise robustness
- Generalization to out-of-distribution patterns
- Resilience to deformation

**8.5 CNA as a Paradigm Shift**  
Unlike constraint-based mitigation, CNA does not patch a specific failure mode — it replaces the representational strategy. Local feature processing and global structure formation are integrated by design, rather than being forced into alignment through loss engineering. This addresses the root cause identified in Chapter 5.

**8.6 Limitations and Open Questions**  
Computational scaling; relationship to existing neuroscience models; applicability beyond vision.

---

### Chapter 9: [Placeholder] Deep Feedback Control as a Second Neuro-Inspired Paradigm *(Planned Paper)*

**Role:** First Author (in preparation)  
**Contribution:** Full chapter treatment pending completion

**9.1 Motivation: Beyond Feedforward Computation**  
*(To be completed. This chapter will present Deep Feedback Control as a complementary neuro-inspired paradigm to CNA, grounded in predictive coding principles.)*

**9.2 [Placeholder: Core DFC Contribution]**

**9.3 How DFC Complements CNA**  
CNA addresses the representational substrate; DFC addresses the learning dynamics. Together, they sketch a more complete alternative to backpropagation-trained feedforward networks.

> **Note to reader:** This chapter will be integrated upon completion of the associated manuscript. The thesis is structured such that Part IV remains coherent with or without this chapter — Chapter 8 stands independently as a complete paradigm proposal.

---

## Part V: Synthesis and Conclusion

### Chapter 10: Discussion

**10.1 Unifying the Four Parts**  
A coherent narrative: from cataloguing failures (Part I), to diagnosing their mathematical roots (Part II), to engineering mitigations (Part III), to proposing a paradigm replacement (Part IV). The progression is not merely organisational — each part motivates the next.

**10.2 What Constraint Engineering Can and Cannot Achieve**  
The Koopman, HU-range, and retrieval results demonstrate that structural knowledge, when formalised correctly, can achieve dramatic improvements. But they all require problem-specific prior knowledge. CNA and DFC demonstrate that the prior knowledge can be built into the learning paradigm itself — the neuro-inspired approach is not an engineering workaround but an architectural answer.

**10.3 The Broader Argument: Statistical Correlation vs. Structured Understanding**  
The thesis argument in full: deep learning, as currently practised, optimises for statistical fit to training distributions. The resulting representations are powerful but brittle, opaque, and compositionally impoverished. Neuro-inspired architectures — that emphasise structured, invariant, compositional representations — offer a principled path forward.

**10.4 Limitations of This Work**

**10.5 Open Problems and Future Directions**

---

### Chapter 11: Conclusion

A concise synthesis (≈2 pages) suitable for reading independently.

---

## Appendix

**A. Supplementary Material for Chapter 3** (ACU Survey: full taxonomy tables, dataset summary)  
**B. Supplementary Material for Chapter 5** (Self-attention structures: proofs, additional model validations)  
**C. Supplementary Material for Chapter 6** (Koopman-JEPA: full ablations, LQR analysis details)  
**D. Supplementary Material for Chapter 8** (CNA: additional experiments)  
**E. List of Publications**

---

## Notes on Minor Contribution Papers

The treatment of the four papers where the candidate's contribution was partial (Private LLM Survey, COGITAO, HU Ranges, Deep Retrieval) follows standard practice for cumulative theses:

- **Private LLM Survey and COGITAO** are referenced as contextual support in Chapter 4 and cited throughout. No original text from these papers is reproduced at length; instead, the candidate's specific contribution (evaluation results) is used to draw targeted argumentative points.
- **HU Ranges** receives ≈1.5 pages in Chapter 7. The framing contribution is genuine and thesis-relevant; the implementation details are attributed to co-authors.
- **Deep Retrieval** receives ≈1.5 pages in Chapter 7 and the candidate is First Author, so this receives slightly more elaborate treatment despite being a supporting work.

This approach is consistent with UZH and INI guidelines, which require that the thesis document clearly distinguishes the candidate's personal intellectual contribution from collaborative work.

---

*Next step: Based on this outline, draft the thesis abstract.*
