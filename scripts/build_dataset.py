"""Assemble the unified dataset from the three raw sources and write processed outputs.

Run:  python scripts/build_dataset.py
Writes data/processed/measurements.csv (tidy long) and prints a summary + merge hazards.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from optobench.ingest import load_channels, load_ehrlich, load_vpod  # noqa: E402
from optobench.schema import Dataset, Property, Source  # noqa: E402

RAW = ROOT / "data" / "raw"
CURATED = ROOT / "data" / "curated"
OUT = ROOT / "data" / "processed"

VPOD_SPLITS = (RAW / "vpod" / "VPOD_1.3" / "formatted_database_subsets"
               / "vpod_1.3_data_splits_2025-10-06_16-50-06")


def main() -> None:
    ds = Dataset()
    load_channels(RAW / "arnold2019_channels" / "regression" / "inputs"
                  / "Ephys_data_formatted.csv", ds)
    load_vpod(VPOD_SPLITS / "wds_meta.tsv", ds)
    load_ehrlich(CURATED / "ehrlich2026_chrimsonr.csv", ds)

    df = ds.to_frame()
    OUT.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT / "measurements.csv", index=False)

    print(f"proteins: {len(ds.proteins)}   measurements: {len(ds.measurements)}")
    print("\nmeasurements by source x property:")
    print(df.groupby(["source", "property"]).size().to_string())
    print("\nproteins by family (distinct):")
    fam = {p.protein_id: p.family.value for p in ds.proteins.values()}
    import collections
    for k, v in collections.Counter(fam.values()).most_common():
        print(f"  {k}: {v}")

    print("\nproteins carried WITHOUT a sequence (excluded from sequence views):")
    noseq = [p.protein_id for p in ds.proteins.values() if not p.sequence]
    print(f"  {len(noseq)}: {noseq}")

    # Example model-ready views
    for src, prop in [(Source.ARNOLD2019, Property.PEAK_PHOTOCURRENT),
                      (Source.VPOD_V1_3, Property.LAMBDA_MAX)]:
        v = ds.view(property=prop, source=src)
        print(f"\nview[{src.value}, {prop.value}]: {len(v)} rows, "
              f"seq len range {v['sequence'].str.len().min()}-{v['sequence'].str.len().max()}")


if __name__ == "__main__":
    main()
