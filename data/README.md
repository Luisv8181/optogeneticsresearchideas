# data/

- `raw/<source>/` — untrusted downloaded artifacts, one dir per source, each with a
  `SOURCE.md` (URL, access date, version/commit, license, checksum). Git-ignored.
- `processed/` — the unified dataset view built from raw via `optobench`. Git-ignored;
  regenerate from provenance.

Never run code from inside a `raw/` directory (interpreters load modules from the
script's own dir). Pass paths as arguments to scripts that live under `src/`.

See `docs/02_data_acquisition.md`.
