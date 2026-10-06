# M0 — literature verification record

Date: 2026-10-06. Each claim we intended to build on, checked against primary sources.
Status: **verified**, **corrected**, or **unconfirmed**. Build only on verified/corrected rows.

## 1. 2019 channelrhodopsin GP (Baseline A) — ✅ VERIFIED
- **Bedbrook, Yang, Arnold (+ Gradinaru)**, "Machine learning-guided channelrhodopsin
  engineering enables minimally invasive optogenetics," *Nature Methods* 16:1176–1184 (2019).
- Gaussian-process models trained on **102 functionally characterized ChR variants**;
  produced ChRger1/2/3. ✓
- **Repo-internal numbers — ✅ CONFIRMED (M1, 2026-10-06)** by inspecting
  `fhalab/channels` directly: `Ephys_data_formatted.csv` has **154 rows**, `seq` is a
  **341-char** aligned sequence, and **gen10 = 30** held-out variants (gen1=76, gen2=5,
  gen4=12, gen5=5, gen7=4, gen9=22). Phenotype columns: `max_peak`, `max_ss`,
  `green_norm`, `kinetics_off`. See `data/SOURCES.md`.
- **Still deferred to M2:** the reported R values (0.927/0.964/0.959) — those require
  *running* the model, not reading the repo, and are the trust check for M2.

## 2. ChrimsonR E300 / PLM study — ⚠️ CORRECTED (preprint, not journal)
- **Samuel Ehrlich et al.** (incl. Edward S. Boyden, Craig R. Forest), "Mutation E300
  recommended by protein language models gives ChrimsonR amplified photocurrent response."
- **CORRECTION:** this is a **bioRxiv preprint (2026-05, DOI 10.64898/2026.05.13.725064)**,
  **NOT** a peer-reviewed *Scientific Reports* paper as earlier notes stated. It is
  unrefereed. First author "Ehrlich" is correct.
- Verified content: zero-shot ESM-1b/1v; **17** variants tested by whole-cell patch clamp,
  **n=6** cells/mutation; sustained photocurrent **66 pA (control) → 305 pA (E300G),
  255 pA (E300P) at 635 nm**; EC50 at 575 nm **0.19 → 0.07 mW**; τ_off **0.06 s → up to
  0.40 s**. ✓
- **Consequence for the project:** fine as the temporal OOD test set, but label it a
  preprint everywhere and weight it accordingly; re-check for a peer-reviewed version
  before any publication.

## 3. VPOD — ⚠️ CORRECTED (two papers, not one; one figure unconfirmed)
- **Original database paper:** **Frazer et al.**, "Discovering genotype–phenotype
  relationships with machine learning and the Visual Physiology Opsin Database (VPOD),"
  *GigaScience* (2024). Describes **VPOD v1.0 = 864 unique opsin genotypes from 73
  publications**; best λmax model R²=0.968, MAE 6.56 nm. ✓
- **The v1.3 / physicochemical-vs-PLM claim is a SEPARATE, later paper:** **Seth A.
  Frazer et al.**, "Accessible and robust machine learning approaches to improve the
  opsin genotype–phenotype map," ***Molecular Biology and Evolution* (2026)** — **NOT**
  *Scientific Reports*. It uses **VPOD v1.3** and concludes ESM-2 embeddings were
  "similar to, but in all cases slightly worse than" optimized physicochemical-property
  encoding, which it keeps for interpretability. ✓ (This *strengthens* our "PLMs are not
  automatically superior" framing.)
- **CORRECTED (M1, 2026-10-06):** the "**1,714 genotypes**" figure is **wrong**. The
  actual VPOD v1.3 whole dataset is **1,211 unique genotypes** — confirmed two ways from
  the release (`wds_meta.tsv` = 1,211 rows; `wds_aligned_VPOD_1.3_het.fasta` = 1,211
  sequences; commit c2912f8). Subsets partition consistently: vertebrate 1,057 +
  invertebrate 155; wild-type 364 + mutant 848. Columns: `Seq_Id, Lambda_Max, Species,
  Opsin_Family, Phylum, Class, Accession, Mutations, Protein, RefId` — `Phylum`/`Class`
  give the phylogenetic split directly. (The "120+ publications" count was not checked;
  the genotype figure is the one that mattered and it was off by ~500.)

## 4. 2025 translation roadmap — ⚠️ CORRECTED (author list) + ❌ one claim rejected
- "Roadmap for direct and indirect translation of optogenetics into discoveries and
  therapies for humans," *Nature Neuroscience* Perspective, **18 Nov 2025**. ✓
- **Author list (corrected — it is a large consortium, not Deisseroth-led):** Christian
  Lüscher, Valentina Emiliani, Nita Farahany, Aryn Gittis, Viviana Gradinaru,
  Katherine A. High, Botond Roska, José-Alain Sahel, Ofer Yizhar, Hongkui Zeng,
  Karl Deisseroth.
- Direct/indirect translation framing and the retinal proof-of-principle: consistent
  with the Perspective. ✓
- **❌ REJECTED:** a search summary asserted "two Phase 2 trials in 2026 → Phase 3 for
  schizophrenia/autism." Not corroborated by the paper; treated as a search-engine
  fabrication and **excluded**.

## 5. 2017 ML membrane-localization — ✅ VERIFIED
- Bedbrook et al., "Machine learning to design integral membrane channelrhodopsins for
  efficient eukaryotic expression and plasma membrane localization," *PLOS Comput. Biol.*
  (2017, PMC5695628). GP classification/regression on **218 ChR chimeras** chosen from a
  **118,098-variant** SCHEMA-recombination library of **3 parent ChRs**, for expression +
  membrane localization. Confirms the "~218 chimeras / 3 parents" narrative figure.

## 6. 2019 paper author list — note
- Full bioRxiv author list: Bedbrook, C. N.; Yang, K. K.; **Robinson, J. E.**; Gradinaru,
  V.; Arnold, F. H. (earlier notes omitted Robinson). Published *Nat. Methods* 2019,
  DOI 10.1038/s41592-019-0583-8.

## Net effect on the project
- Journal attributions were wrong in two places (ChrimsonR = preprint; VPOD-v1.3 claim =
  *MBE* 2026, not *Scientific Reports*). Fixed in `00_research_framework.md`.
- The physicochemical-vs-PLM finding is real and *supports* the design (Baseline B is not
  a strawman; it may win).
- Nothing found that undermines the project; the gap stands.
