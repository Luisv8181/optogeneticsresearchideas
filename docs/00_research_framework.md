# Research framework: from protein prediction to translationally-informed optogenetic design

> **Status:** design doc, v0.1. This is the positioning document — it defines *what
> we are claiming is novel* and *where the genuine research gap is*, before any
> modeling.
>
> **Provenance caveat:** the literature claims below are drawn from working notes and
> a collaborator's summary of the 2025 roadmap paper. They have **not yet been
> independently verified in this project** (see Milestone 0 in `03_benchmark_plan.md`).
> Treat every cited number and author claim as *to-be-confirmed* until that milestone
> is done. Getting a citation wrong in a publishable program is expensive, so we verify
> before we build on it.

## The three sources and what each one contributes

| Source | Year | What it gives us | Role in this project |
|---|---|---|---|
| Arnold Lab `channels` (Bedbrook et al.) | 2019 | Gaussian-process model, ~102–154 characterized ChRs, sequence+structural-contact encoding, generation-based split | **Baseline A** + the historical anchor |
| VPOD opsin database | 2024/25 | ~1,700 opsin genotypes with λmax | Spectral-phenotype data for cross-family generalization |
| ESM / ChrimsonR study (Ehrlich et al.) | 2026 | zero-shot PLM mutation recommendations, 17 experimentally-tested ChrimsonR variants | **Temporal OOD test set** + evidence PLMs transfer to opsins |
| Translation roadmap (Nat. Neurosci. Perspective) | 2025 | the clinical constraints that *define what "better" means* | **The objective function**, not a dataset |

## The reframing

The naive research question — *"can a modern protein language model beat the 2019 GP
at predicting opsin phenotype?"* — is answerable but incremental. The 2025 roadmap
reframes it, because it says protein engineering is only one of three layers of the
translational problem:

```
                  OPTOGENETIC TRANSLATION
                           |
        +------------------+------------------+
        v                  v                  v
     MOLECULE           CIRCUIT             DEVICE
     (opsin)          (cell type)      (light delivery)
        |                  |                  |
  spectrum/kinetics    targeting         depth / wavelength
  /photocurrent        specificity       penetration / geometry
        |                  |                  |
        +------------------+------------------+
                           v
                        THERAPY
```

The roadmap's two translation pathways:

- **Direct:** opsin + targeting + gene delivery + light delivery + control + safety →
  human cells. (Proof-of-principle: restoration of partial vision in a blind patient.)
- **Indirect:** optogenetics is a *causal-discovery platform* — it identifies the
  circuit, and a different modality (drug, DBS) delivers the therapy.

## Where the genuine gap is

Current opsin ML — 2019 GP and 2026 PLM alike — optimizes **lab performance** (maximize
photocurrent, in a dish, usually under blue light). The roadmap makes clear that the
*translationally* best opsin is often a different molecule:

> Opsin A: very high photocurrent, blue-activated, fast, bright → wins in a dish.
> Opsin B: lower current, red/NIR-shifted, slower → wins for deep-tissue human therapy,
> because tissue transmits red/NIR far better than blue.

So **"best opsin" is not a scalar.** It is a function of the translational target. That
is the gap this project addresses:

> **Can computational opsin modeling rank/design variants against translational
> objectives (wavelength-vs-tissue-depth, kinetic regime, targeting) rather than
> against single lab metrics?**

## What is learned vs. computed vs. deferred (the honesty boundary)

This is the most important design decision in the project. We do **not** pretend a
sequence model can predict immunogenicity or in-vivo safety.

| Layer | How we get it | Phase |
|---|---|---|
| Spectrum (λmax), photocurrent, on/off kinetics | **Learned** from sequence (the ML benchmark, models A–E) | Phase 1, now |
| Tissue optical penetration for a given λmax | **Computed** from tissue-optics physics (absorption/scattering vs. wavelength) | Phase 1, now |
| Translational score = f(predicted molecular props, target depth, kinetic need) | **Composed** — a transparent scoring layer over the above | Phase 1, now |
| Targeting / cell-type specificity | needs promoter/delivery data | Phase 2, with data |
| Immunogenicity / safety | needs annotated experimental datasets | Phase 3, wet-lab collaborator |

The buildable claim for Phase 1 is therefore precise and defensible: **molecular
properties are learned; the translational objective is a physics-grounded scoring layer
on top of them.** Nothing is inferred from sequence that cannot be.

## Why this pairs with the ML benchmark

The OOD evaluation (temporal / phylogenetic / Hamming-distance splits — see
`03_benchmark_plan.md`) becomes *more* meaningful under this frame: a model that only
works near its training chimeras is useless for proposing red-shifted, deep-tissue
variants, because those live far from the blue-light ChR training distribution. The
translational objective makes OOD generalization the whole point, not a stress test.

## Expected result (pre-registered intuition)

On the in-distribution generation-10 chimera split, the 2019 GP may **win or tie** —
GPs are strong in low-data, near-neighbor regimes. The interesting, publishable finding
is the expected **rank flip** as sequence distance grows. We state this in advance so a
GP win near the training set reads as confirmation, not failure.
