"""Lock the unified-dataset merge against the real raw data.

Skips automatically if the raw sources aren't present (they're git-ignored), so the
suite still passes on a fresh checkout before data acquisition.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from optobench.ingest import load_channels, load_ehrlich, load_vpod  # noqa: E402
from optobench.schema import Dataset, Family, Property, Source  # noqa: E402

CHANNELS = ROOT / "data/raw/arnold2019_channels/regression/inputs/Ephys_data_formatted.csv"
VPOD = (ROOT / "data/raw/vpod/VPOD_1.3/formatted_database_subsets"
        / "vpod_1.3_data_splits_2025-10-06_16-50-06/wds_meta.tsv")
EHRLICH = ROOT / "data/curated/ehrlich2026_chrimsonr.csv"

pytestmark = pytest.mark.skipif(
    not (CHANNELS.exists() and VPOD.exists()),
    reason="raw data not present (git-ignored); run data acquisition first",
)


@pytest.fixture(scope="module")
def ds() -> Dataset:
    d = Dataset()
    load_channels(CHANNELS, d)
    load_vpod(VPOD, d)
    load_ehrlich(EHRLICH, d)
    return d


def test_source_counts(ds):
    df = ds.to_frame()
    by = df.groupby(["source", "property"]).size()
    assert by[("arnold2019", "peak_photocurrent")] == 154
    assert by[("arnold2019", "green_response")] == 128  # 26 missing, not imputed
    assert by[("vpod_v1_3", "lambda_max")] == 1211


def test_family_split_from_phylum(ds):
    fam = [p.family for p in ds.proteins.values()]
    assert fam.count(Family.VERTEBRATE_OPSIN) == 1057
    assert fam.count(Family.INVERTEBRATE_OPSIN) == 148
    assert fam.count(Family.OTHER) == 6  # plant (Streptophyta) opsins, not vertebrate


def test_ehrlich_variants_have_no_sequence(ds):
    """Temporal test set carries mutation strings but no sequence yet — must be
    excluded from sequence-model views until ChrimsonR WT is reconstructed."""
    v = ds.view(property=Property.PEAK_PHOTOCURRENT, source=Source.ARNOLD2019)
    assert v["has_sequence"].all()
    noseq = [p.protein_id for p in ds.proteins.values() if not p.sequence]
    assert all(pid.startswith("ehrlich:") for pid in noseq)
    assert len(noseq) == 8


def test_citation_required():
    from optobench.schema import Measurement
    with pytest.raises(ValueError):
        Measurement("m", "p", Property.LAMBDA_MAX, 500.0, citation="", source=Source.OTHER)
