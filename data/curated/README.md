# data/curated/

Hand-curated, committed data (unlike `data/raw/`, which is git-ignored). Each file is
transcribed by hand from a primary source and carries provenance.

## ehrlich2026_chrimsonr.csv — ⚠️ INCOMPLETE (7 of 17 variants)

The 17 ChrimsonR variants from the Ehrlich et al. bioRxiv preprint
(10.64898/2026.05.13.725064), the project's **temporal OOD test set**.

**Status:** only the variants named/quantified in the preprint's main text are
transcribed. The complete 17-variant list lives in a **supplementary table** not
machine-readable via web fetch. The remaining ~10 variants ("reduced photocurrent
amplitude or complete loss of function") are **not** transcribed because their exact
mutation identities are not in the fetchable text — they will **not** be invented. To
complete: open the preprint's supplement and transcribe the remaining mutation strings
and values.

**Captured:**
- WT baseline: 66 pA sustained @635 nm, EC50 0.19 mW @575 nm, τ_off 0.06 s (n=6).
- Gain of function: E300G (305 pA, EC50 0.07, τ_off 0.19), E300P (255 pA, EC50 0.07,
  τ_off 0.40), E300V (maintained, τ_off 0.22).
- Other named: H291Y (<20 pA, blue-shifted), E132A, H307L, F341E (maintained, not
  quantified in main text).

**Wavelengths tested in the study:** 395, 440, 470, 575, 635, 740 nm.
**Method:** whole-cell patch clamp, n=6 cells/mutation.

Empty value cells mean "reported but not quantified in the fetchable text," not zero.
