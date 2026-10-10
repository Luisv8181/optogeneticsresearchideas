"""Loaders that turn each raw source into schema records and assemble a unified Dataset.

Faithful to the measurement-centric schema: one Measurement per (protein × property ×
condition), created only where a value actually exists (no imputation). See
docs/01_data_schema.md and docs/02_data_acquisition.md.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from .schema import Dataset, Family, Measurement, Property, Protein, Source

CIT_ARNOLD = "Bedbrook et al. 2019, Nat. Methods 16:1176 (repo fhalab/channels)"
CIT_VPOD = "Frazer et al., VPOD v1.3 (Mol. Biol. Evol. 2026 / GigaScience 2024)"
CIT_EHRLICH = "Ehrlich et al. 2026, bioRxiv 10.64898/2026.05.13.725064 (preprint)"


def _mk(mid, pid, prop, value, *, source, citation, **kw) -> Measurement:
    return Measurement(
        measurement_id=mid, protein_id=pid, property=prop, value=value,
        citation=citation, source=source, **kw,
    )


def load_channels(csv_path: str | Path, ds: Dataset) -> None:
    """Arnold `channels` ChR electrophysiology → ChR proteins + 4 phenotype measurements.

    Columns: chimera, kinetics_off, block_k, gen, seq, green_norm, max_peak, max_ss.
    `seq` is the 341-position alignment; ungapped sequence is derived from it.
    Measurements are emitted only where the cell is non-null (green_norm/kinetics_off
    are missing for 26 of 154 records).
    """
    df = pd.read_csv(csv_path)
    prop_map = {
        "max_peak": (Property.PEAK_PHOTOCURRENT, "pA"),
        "max_ss": (Property.STEADY_STATE_PHOTOCURRENT, "pA"),
        "green_norm": (Property.GREEN_RESPONSE, None),
        "kinetics_off": (Property.OFF_KINETICS_TAU, "ms"),
    }
    for _, r in df.iterrows():
        pid = f"arnold:{r['chimera']}"
        aligned = str(r["seq"])
        ds.add_protein(Protein(
            protein_id=pid, sequence=aligned.replace("-", ""), family=Family.CHR,
            source=Source.ARNOLD2019, aligned_sequence=aligned,
            generation=int(r["gen"]) if pd.notna(r["gen"]) else None,
            meta={"chimera": r["chimera"]},
        ))
        for col, (prop, unit) in prop_map.items():
            v = r[col]
            if pd.notna(v):
                ds.add_measurement(_mk(
                    f"{pid}:{col}", pid, prop, float(v),
                    source=Source.ARNOLD2019, citation=CIT_ARNOLD, unit=unit,
                    assay_system="patch_clamp",
                ))


# Family is derived from Phylum, which is clean and authoritative. Seq_Id is NOT a safe
# join key across the subset files (IDs collide between subsets), so subset membership is
# not used. Chordata = vertebrate; animal invertebrate phyla = invertebrate; non-animal
# opsins (e.g. plant Streptophyta) = other.
_NONANIMAL_PHYLA = {"Streptophyta", "Chlorophyta", "Bacteria", "Cyanobacteria"}


def _vpod_family(phylum) -> Family:
    p = str(phylum)
    if p == "Chordata":
        return Family.VERTEBRATE_OPSIN
    if p in _NONANIMAL_PHYLA:
        return Family.OTHER
    return Family.INVERTEBRATE_OPSIN


def load_vpod(meta_tsv: str | Path, ds: Dataset) -> None:
    """VPOD v1.3 whole dataset → opsin proteins + one λmax measurement each.

    Family is derived from Phylum (see `_vpod_family`). Phylum/Class/Opsin_Family/Species
    kept in meta for the phylogenetic split.
    """
    from .schema import Source

    df = pd.read_csv(meta_tsv, sep="\t")
    for _, r in df.iterrows():
        sid = str(r["Seq_Id"])
        pid = f"vpod:{sid}"
        fam = _vpod_family(r.get("Phylum"))
        muts = str(r["Mutations"]).strip()
        ds.add_protein(Protein(
            protein_id=pid, sequence=str(r["Protein"]).replace("-", ""), family=fam,
            source=Source.VPOD_V1_3,
            mutations=tuple(muts.split(";")) if muts and muts.lower() != "nan" else (),
            meta={"phylum": r.get("Phylum"), "class": r.get("Class"),
                  "opsin_family": r.get("Opsin_Family"), "species": r.get("Species"),
                  "accession": r.get("Accession"), "seq_id": sid},
        ))
        if pd.notna(r["Lambda_Max"]):
            ds.add_measurement(_mk(
                f"{pid}:lmax", pid, Property.LAMBDA_MAX, float(r["Lambda_Max"]),
                source=Source.VPOD_V1_3, citation=CIT_VPOD, unit="nm",
                assay_system="heterologous_expression",
            ))


def load_ehrlich(csv_path: str | Path, ds: Dataset) -> None:
    """Curated ChrimsonR variants (temporal OOD test set).

    Sequences are NOT available here (only mutation strings relative to ChrimsonR WT),
    so proteins are carried with an empty sequence and excluded from sequence-model views
    until the ChrimsonR WT sequence is added and mutations applied. See data/curated/.
    """
    from .schema import Source

    df = pd.read_csv(csv_path)
    for _, r in df.iterrows():
        pid = f"ehrlich:{r['variant']}"
        mut = str(r["mutation"])
        ds.add_protein(Protein(
            protein_id=pid, sequence="", family=Family.CHR, source=Source.EHRLICH2026,
            mutations=() if mut.lower() == "none" else (mut,),
            reference_protein="ChrimsonR_WT",
            meta={"completeness": r.get("completeness")},
        ))
        if pd.notna(r.get("value")):
            ds.add_measurement(_mk(
                f"{pid}:ss", pid, Property.STEADY_STATE_PHOTOCURRENT, float(r["value"]),
                source=Source.EHRLICH2026, citation=CIT_EHRLICH, unit="pA",
                wavelength_nm=635, assay_system="whole_cell_patch_clamp",
                n=int(r["n"]) if pd.notna(r.get("n")) else None,
            ))
        if pd.notna(r.get("ec50_mW_575nm")):
            ds.add_measurement(_mk(
                f"{pid}:ec50", pid, Property.EC50, float(r["ec50_mW_575nm"]),
                source=Source.EHRLICH2026, citation=CIT_EHRLICH, unit="mW",
                wavelength_nm=575, assay_system="whole_cell_patch_clamp",
            ))
        if pd.notna(r.get("tau_off_s")):
            ds.add_measurement(_mk(
                f"{pid}:tauoff", pid, Property.OFF_KINETICS_TAU, float(r["tau_off_s"]),
                source=Source.EHRLICH2026, citation=CIT_EHRLICH, unit="s",
                assay_system="whole_cell_patch_clamp",
            ))


def read_ids(tsv_path: str | Path) -> set[str]:
    """Seq_Id set from a VPOD subset meta.tsv (first column)."""
    return set(pd.read_csv(tsv_path, sep="\t")["Seq_Id"].astype(str))
