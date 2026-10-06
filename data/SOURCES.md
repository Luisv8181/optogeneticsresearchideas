# Data provenance ledger

Raw data under `data/raw/` is git-ignored; this committed ledger is the record of what
was pulled, from where, and when. Regenerate raw data from here.

## arnold2019_channels — ✅ acquired 2026-10-06
- **Repo:** https://github.com/fhalab/channels (Frances H. Arnold Lab)
- **Commit:** `da2f6651a760be6b8daec06467272b0ac2d8aeeb` (dated 2019-05-06), branch `master`
- **Clone:** `git clone --depth 1` → `data/raw/arnold2019_channels/` (~107 MB)
- **Key file:** `regression/inputs/Ephys_data_formatted.csv` — 154 rows × 9 cols
  - columns: `chimera, kinetics_off, block_k, gen, seq, green_norm, max_peak, max_ss`
  - phenotypes: `max_peak` (peak photocurrent), `max_ss` (steady-state),
    `green_norm` (green-light response), `kinetics_off` (off-kinetics)
  - `seq`: 341-char aligned sequences (constant length — the project MSA width)
  - `gen` distribution: gen1=76, gen2=5, gen4=12, gen5=5, gen7=4, gen9=22, **gen10=30**
    (gen10 = held-out final generation, confirming the repo-internal numbers)
- **Note:** repo uses git-LFS; `regression/inputs/alignment_and_contacts_C1C2.pkl` came
  down as a non-pointer during clone — verify it (and other `.pkl` contact inputs) before
  relying on structural-contact features in M2.
- **License:** confirm from repo before any redistribution.

## vpod — ✅ acquired 2026-10-06 (trimmed to v1.3)
- **Repo:** https://github.com/VisualPhysiologyDB/visual-physiology-opsin-db
- **Commit:** `c2912f843b0dc520f7f8631d025d00c8c601fd6b` (see `vpod/CLONE_COMMIT.txt`)
- **Disk note:** full checkout is **~20 GB / 30k files** (bloated history; `--filter=blob:none`
  does not help once the working tree is written). We extracted only `vpod_data/VPOD_1.3/`
  (30 MB) plus README/AUTHORS/LICENSE and **deleted the full clone** to reclaim disk. To
  re-acquire, clone and keep only `vpod_data/VPOD_1.3/`.
- **v1.3 whole dataset: 1,211 unique genotypes** (NOT 1,714 — see VERIFICATION.md §3).
  - whole-dataset files: `.../vpod_1.3_data_splits_2025-10-06_16-50-06/wds_meta.tsv`
    (+ `wds_aligned_VPOD_1.3_het.fasta`), 1,211 rows/seqs.
  - columns: `Seq_Id, Lambda_Max, Species, Opsin_Family, Phylum, Class, Accession,
    Mutations, Protein, RefId`.
  - subsets: vert 1,057 / inv 155; wt 364 / mut 848 — ready-made phylogenetic &
    wild-type-vs-mutant splits.
- **License:** LICENSE.txt retained in `data/raw/vpod/`.

## ehrlich2026 — ☐ not yet acquired
- **bioRxiv preprint**, DOI 10.64898/2026.05.13.725064 (unrefereed).
- 17 ChrimsonR variants to be transcribed by hand from the preprint's supplement into
  the measurement schema (`source=ehrlich2026`). Small n; one careful transcription pass.
