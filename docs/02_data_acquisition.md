# Data acquisition plan (provenance-tracked)

> Every raw artifact lands in its own directory under `data/raw/<source>/` with a
> `SOURCE.md` recording: URL, access date, version/commit, license, and a checksum.
> Raw data is untrusted input — we never run code *from inside* a downloaded directory,
> and raw dirs are git-ignored (only the provenance notes and processed outputs are
> committed).

## Sources

### 1. Arnold Lab `channels` (Baseline A + ChR electrophysiology)
- Public repo accompanying the 2019 Nature Methods paper.
- Target files: `Ephys_data_formatted.csv` (sequences, generation, photocurrent,
  steady-state, green response, off-kinetics), the encoding code, the GP notebook.
- Capture the exact commit hash — the reported metrics are tied to a pinned environment.
- **Risk:** 2019-era dependency pins (GPy / old sklearn). Baseline reproduction is its
  own milestone, not an afternoon.

### 2. VPOD v1.3 (spectral phenotype, cross-family)
- Public opsin genotype→λmax database.
- Record the exact version (v1.3) and release.
- Normalize λmax units on ingest; retain raw.

### 3. Ehrlich et al. 2026 (temporal OOD test set)
- 17 ChrimsonR variants from the paper's supplement — **manual transcription**, small n.
- Capture: variant id, mutation(s), measured property, value, wavelength, intensity, n,
  assay. These become the held-out temporal test set (`source=ehrlich2026`).

### 4. Translation roadmap (2025 Perspective)
- Not a dataset — the source of the translational *objective*. Extract the enumerated
  bottlenecks (light penetration by wavelength, device geometry, targeting, scale from
  mouse→human) into `00_research_framework.md`'s objective layer.

## Network note

Outbound HTTPS in this environment goes through the agent proxy. If a download fails
TLS / returns 403/407, consult `/root/.ccr/README.md` — do **not** disable TLS or unset
the proxy. If a source host is blocked by the environment's network policy, that's an
environment-config issue (see `read_documentation`), not a code problem.

## Order of operations

1. Pull source 1, pin the commit, land provenance.
2. Pull source 2, pin the version.
3. Transcribe source 3 by hand into the measurement schema.
4. Build the unified dataset view (`src/optobench/schema.py` records → processed parquet/csv).
5. Only then: baseline reproduction (Milestone 1).
