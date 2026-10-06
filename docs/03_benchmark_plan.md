# Benchmark plan

## Milestones (sequential — "both, in order")

- **M0 — Verify the literature.** Independently confirm each cited claim (Ehrlich et al.
  variants & numbers, VPOD v1.3 size, 2019 reported metrics, the 2025 roadmap's authors
  and claims). Correct `00_research_framework.md`. *Do this before building on any number.*
- **M1 — Unified dataset.** Acquire sources, implement the schema, build the merged view,
  document merge hazards encountered. (This doc + `01`/`02`.)
- **M2 — Reproduce Baseline A.** Pinned environment; reproduce the 2019 GP's reported
  CV and generation-10 test metrics within tolerance. This is a trust check on our whole
  pipeline, not just a baseline.
- **M3 — Model slots B–E.** Implement and evaluate under identical splits.
- **M4 — OOD evaluation.** The scientific core (below).
- **M5 — Translational scoring layer.** Compose predicted molecular props + tissue-optics
  into the translational objective.

## Model slots

| slot | model | representation |
|---|---|---|
| A | 2019 Gaussian process (baseline) | one-hot sequence + structural-contact pairs, Matérn 5/2 |
| B | conventional ML (RF / XGBoost) | physicochemical sequence features |
| C | PLM + regression | ESM-2 embeddings (`650M` or smaller — CPU/VRAM bound) + ridge |
| D | PLM + structure | ESM-2 embeddings + structural contacts + MLP |
| E | multi-task | shared trunk, per-property heads (tolerates missing targets) |

Also worth a slot, per the reframing: **task-conditioned fine-tune** — ESM-2 with a
property-specific head (τ_off, λmax, photocurrent), compared against E. If multi-task
wins, that's a finding; if task-specific wins, equally publishable.

## OOD evaluation (the contribution)

Random splits are not the test. Three stratified splits, increasing in difficulty:

1. **Temporal:** train pre-2020, test on 2020–2026 (the 17 Ehrlich ChrimsonR variants).
2. **Phylogenetic:** train vertebrate opsins, test invertebrate (or vice versa).
3. **Mutation-distance:** stratify test by Hamming distance from nearest training seq;
   report metric as a function of distance.

**Pre-registered expectation:** GP (A) competitive/winning at low distance; PLM models
(C–E) expected to overtake as distance grows. The *crossover* is the headline.

## Active learning (optional strong extension)

Framed decision-theoretically: given a fixed budget (e.g. 20 patch-clamp measurements),
which mutations maximize expected information gain about the phenotype landscape? Connects
to Bayesian optimization; can stand alone.

## Metrics

- Per-property: Pearson R, Spearman ρ, RMSE.
- Report CV and each OOD split separately — never a single headline number.
- Explainability: which residues drive predictions (attribution), checked against known
  functional residues (e.g. E300 in ChrimsonR) as a sanity test.
