# optogeneticsresearchideas

A translation-aware benchmark for **optogenetic-protein phenotype prediction** — does a
modern protein language model actually generalize better than the 2019 channelrhodopsin
Gaussian process when the target is *translational* usefulness, not lab performance?

## The idea in one paragraph

Opsin ML (2019 GP, 2026 PLMs) optimizes lab performance — maximize photocurrent, in a
dish, under blue light. The 2025 translation roadmap says the *translationally* best
opsin is often a different molecule (e.g. red/NIR-shifted for deep tissue, even at lower
current). So "best opsin" is not a scalar — it's a function of the clinical target. This
project builds (a) a rigorous out-of-distribution benchmark of classical vs. modern
models on a unified opsin dataset, and (b) a scoring layer where **learned** molecular
properties feed a **physics-grounded** translational objective. Nothing about safety or
immunogenicity is faked from sequence — that boundary is explicit.

## Docs

- `docs/00_research_framework.md` — positioning, the gap, the learned-vs-computed boundary
- `docs/01_data_schema.md` — measurement-centric schema
- `docs/02_data_acquisition.md` — provenance-tracked data plan
- `docs/03_benchmark_plan.md` — milestones M0–M5, model slots A–E, OOD splits

## Status

Phase 1 is entirely computational (no wet lab, no GPU for the schema/data work).
Next up: **M0** (verify every cited claim) then **M1** (unified dataset).

## Layout

```
docs/            design + positioning docs
src/optobench/   package; schema.py is implemented, rest stubbed per milestone
data/            provenance-tracked (raw git-ignored)
```
