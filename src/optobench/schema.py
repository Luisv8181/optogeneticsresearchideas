"""Measurement-centric data schema for the optogenetic-protein benchmark.

The unit of record is a *measurement* (one property observed under one set of assay
conditions), not a protein. A photocurrent value is meaningless without the wavelength,
intensity, and cell system it was measured in, so those conditions stay attached to the
value. A model's training matrix is a *view* built by joining measurements to a chosen
protein set and filtering to a chosen assay regime — an explicit, auditable step.

See docs/01_data_schema.md for the rationale and the known merge hazards.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class Family(str, Enum):
    CHR = "ChR"
    VERTEBRATE_OPSIN = "vertebrate_opsin"
    INVERTEBRATE_OPSIN = "invertebrate_opsin"
    OTHER = "other"


class Source(str, Enum):
    ARNOLD2019 = "arnold2019"
    VPOD_V1_3 = "vpod_v1_3"
    EHRLICH2026 = "ehrlich2026"
    OTHER = "other"


class Property(str, Enum):
    PEAK_PHOTOCURRENT = "peak_photocurrent"
    STEADY_STATE_PHOTOCURRENT = "steady_state_photocurrent"
    GREEN_RESPONSE = "green_response"
    OFF_KINETICS_TAU = "off_kinetics_tau"
    ON_KINETICS_TAU = "on_kinetics_tau"
    LAMBDA_MAX = "lambda_max"
    EC50 = "ec50"
    EXPRESSION = "expression"
    MEMBRANE_LOCALIZATION = "membrane_localization"
    FUNCTIONAL = "functional"


@dataclass
class Protein:
    """Identity of a protein. One row per distinct genotype.

    `sequence` may be empty when only a mutation string is known relative to a reference
    whose sequence we do not yet hold (e.g. the Ehrlich ChrimsonR variants) — such a
    protein is carried but excluded from sequence-model views until reconstructed.
    `meta` holds source-specific fields that do not belong in the core schema
    (species, opsin family, phylum, class, accession) and that drive splits.
    """

    protein_id: str
    sequence: str
    family: Family
    source: Source
    aligned_sequence: str | None = None
    parents: tuple[str, ...] = ()
    mutations: tuple[str, ...] = ()
    reference_protein: str | None = None
    generation: int | None = None
    structure_ref: str | None = None
    meta: dict = field(default_factory=dict)


@dataclass(frozen=True)
class Measurement:
    """One property observed under one assay condition. Foreign-keyed to a Protein.

    `citation` is required: provenance is non-negotiable. `value` carries a bool for
    categorical properties (functional / membrane_localization) and a float otherwise.
    """

    measurement_id: str
    protein_id: str
    property: Property
    value: float | bool
    citation: str
    source: Source
    unit: str | None = None
    wavelength_nm: float | None = None
    light_intensity: float | None = None
    light_intensity_unit: str | None = None
    assay_system: str | None = None
    cell_type: str | None = None
    n: int | None = None

    def __post_init__(self) -> None:
        if not self.citation:
            raise ValueError(
                f"measurement {self.measurement_id!r} has no citation; "
                "provenance is required for every measurement"
            )


@dataclass
class Dataset:
    """A unified collection. Not a flat table — a protein set plus a measurement set.

    Build model-ready matrices with `view()` (to be implemented in M1), which joins and
    filters to an explicit assay regime rather than silently averaging across conditions.
    """

    proteins: dict[str, Protein] = field(default_factory=dict)
    measurements: list[Measurement] = field(default_factory=list)

    def add_protein(self, p: Protein) -> None:
        if p.protein_id in self.proteins:
            raise ValueError(f"duplicate protein_id {p.protein_id!r}")
        self.proteins[p.protein_id] = p

    def add_measurement(self, m: Measurement) -> None:
        if m.protein_id not in self.proteins:
            raise ValueError(
                f"measurement {m.measurement_id!r} references unknown "
                f"protein {m.protein_id!r}"
            )
        self.measurements.append(m)

    def to_frame(self):
        """Tidy long DataFrame: one row per measurement, joined to its protein fields."""
        import pandas as pd

        rows = []
        for m in self.measurements:
            p = self.proteins[m.protein_id]
            rows.append(
                {
                    "protein_id": p.protein_id,
                    "family": p.family.value,
                    "generation": p.generation,
                    "has_sequence": bool(p.sequence),
                    "sequence": p.sequence,
                    "aligned_sequence": p.aligned_sequence,
                    "mutations": ";".join(p.mutations),
                    "property": m.property.value,
                    "value": m.value,
                    "unit": m.unit,
                    "wavelength_nm": m.wavelength_nm,
                    "assay_system": m.assay_system,
                    "n": m.n,
                    "source": m.source.value,
                    "phylum": p.meta.get("phylum"),
                    "taxon_class": p.meta.get("class"),
                    "opsin_family": p.meta.get("opsin_family"),
                    "species": p.meta.get("species"),
                    "citation": m.citation,
                }
            )
        return pd.DataFrame(rows)

    def view(self, property=None, source=None, require_sequence=True):
        """Model-ready view: filter the tidy frame to one property/source regime.

        An explicit, auditable step — never a silent average across conditions.
        `require_sequence=True` drops proteins carried without a sequence (the Ehrlich
        variants until their ChrimsonR sequence is reconstructed).
        """
        df = self.to_frame()
        if df.empty:
            return df
        if property is not None:
            prop = property.value if isinstance(property, Property) else property
            df = df[df["property"] == prop]
        if source is not None:
            src = source.value if isinstance(source, Source) else source
            df = df[df["source"] == src]
        if require_sequence:
            df = df[df["has_sequence"]]
        return df.reset_index(drop=True)
