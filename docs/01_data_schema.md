# Unified data schema (measurement-centric)

> **Core principle:** the unit of record is a **measurement**, not a protein. A
> photocurrent value is not a property of a sequence floating in isolation — it depends
> on wavelength, intensity, expression system, and cell type. Those conditions stay
> attached to the measurement. This is what lets us merge ChR electrophysiology with
> VPOD spectral data without silently averaging across incompatible assays.

## Why not one-row-per-protein

If we stored one row per protein with a single `photocurrent` column we would be forced
to collapse measurements taken at different wavelengths/intensities into one number —
destroying exactly the signal the translational objective needs. Instead:

- **Protein** table: identity, sequence, family, parents, mutations, structure refs.
- **Measurement** table: one row per (protein × property × assay-condition) observation,
  foreign-keyed to the protein.

A model's training matrix is then a *view* built by joining + filtering measurements to
a chosen assay regime — an explicit, auditable step, not a hidden assumption.

## Protein record

| field | type | notes |
|---|---|---|
| `protein_id` | str (PK) | stable internal id |
| `sequence` | str | amino acids, ungapped |
| `aligned_sequence` | str \| null | gapped, to the project MSA (341 cols for ChR set) |
| `family` | enum | `ChR`, `vertebrate_opsin`, `invertebrate_opsin`, ... |
| `parents` | list[str] | parent proteins for chimeras |
| `mutations` | list[str] | e.g. `["E300G"]`, relative to a named reference |
| `reference_protein` | str \| null | what mutations are relative to |
| `generation` | int \| null | engineering generation (ChR set only) |
| `structure_ref` | str \| null | PDB id / model path |
| `source` | enum | `arnold2019`, `vpod_v1_3`, `ehrlich2026`, ... |

## Measurement record

| field | type | notes |
|---|---|---|
| `measurement_id` | str (PK) | |
| `protein_id` | str (FK) | |
| `property` | enum | `peak_photocurrent`, `steady_state_photocurrent`, `green_response`, `off_kinetics_tau`, `on_kinetics_tau`, `lambda_max`, `ec50`, `expression`, `membrane_localization`, `functional` |
| `value` | float \| bool | |
| `unit` | str \| null | `pA`, `ms`, `nm`, `mW`, ... |
| `wavelength_nm` | float \| null | illumination wavelength (null for λmax itself) |
| `light_intensity` | float \| null | with `light_intensity_unit` |
| `light_intensity_unit` | str \| null | `mW`, `mW/mm2`, ... |
| `assay_system` | str \| null | `HEK293`, `cultured_neuron`, `patch_clamp`, ... |
| `cell_type` | str \| null | |
| `n` | int \| null | replicate count (e.g. n=6 cells) |
| `source` | enum | matches protein source |
| `citation` | str | DOI or repo path — **required**, provenance is non-negotiable |

## Derived / translational fields (computed, not stored raw)

Not in the merged dataset — produced by the scoring layer at analysis time, so the
physics stays separate from the data:

| field | how |
|---|---|
| `tissue_penetration_depth` | tissue-optics model as a function of (predicted) λmax |
| `kinetic_regime` | bucketed from predicted off-kinetics vs. a target need |
| `translational_score` | transparent composite over predicted molecular props + target spec |

## Known merge hazards (flag, don't paper over)

1. **VPOD gives λmax; the ChR set gives electrophysiology.** The overlap in `property`
   values is small. Most cross-family rows will have λmax but no photocurrent, and vice
   versa. Multi-task models must tolerate missing targets — this is a feature of the
   problem, not a data defect.
2. **Units & conditions differ across the 120+ VPOD publications.** Normalize units on
   ingest; keep the raw value + raw unit in provenance.
3. **The 17 Ehrlich variants are hand-extracted from a supplement** — transcribe once,
   carefully, and mark `source=ehrlich2026` so they can be held out cleanly as the
   temporal test set.

### Hazards actually hit during the M1 merge (resolved)

- **VPOD `Seq_Id` is NOT a safe join key.** IDs collide across the subset files
  (`vert_meta`/`inv_meta`), so labeling family by subset membership silently mislabeled
  every invertebrate as vertebrate. **Fix:** derive family from the `Phylum` column
  (Chordata → vertebrate; Arthropoda/Mollusca/Annelida → invertebrate; Streptophyta →
  other). Verified counts: 1,057 / 148 / 6. (`ingest._vpod_family`, `tests/test_merge.py`.)
- **The Ehrlich variants have no sequence**, only mutation strings relative to ChrimsonR
  WT, which is not in any source we hold. They are carried with `sequence=""` and
  **excluded from sequence-model views** (`Dataset.view(require_sequence=True)`) until the
  ChrimsonR WT sequence is added and the mutations applied. 8 proteins affected.
- **Real missingness in the ChR set:** `green_norm` and `kinetics_off` are present for
  only 128/154 records. No imputation — a `Measurement` is emitted only where the value
  exists, so the counts are 154/154/128/128.
- **Plant opsins exist in VPOD** (6 Streptophyta). They are opsins but not animal, so
  they are `other`, not a phylogenetic-split target — don't let them leak into a
  vertebrate/invertebrate contrast.

Merged totals: **1,373 proteins, 1,786 measurements** → `data/processed/measurements.csv`
(regenerate with `python scripts/build_dataset.py`).
