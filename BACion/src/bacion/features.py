"""
BACion feature extraction.

This module provides utilities for reading bacterial protein FASTA files
and calculating proteome-level features required by the BACion model.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Union

import numpy as np
import pandas as pd
from Bio import SeqIO
from Bio.SeqUtils.ProtParam import ProteinAnalysis


AMINO_ACIDS = tuple("ACDEFGHIKLMNPQRSTVWY")


def clean_sequence(sequence: str) -> str:
    """
    Clean a protein sequence.

    Parameters
    ----------
    sequence : str
        Raw protein sequence.

    Returns
    -------
    str
        Uppercase cleaned amino-acid sequence.
    """

    sequence = str(sequence).upper()

    # Remove whitespace
    sequence = "".join(sequence.split())

    return sequence


def read_proteome(
    fasta_path: Union[str, Path],
) -> List[str]:
    """
    Read protein sequences from a FASTA file.

    Parameters
    ----------
    fasta_path : str or Path
        Path to protein FASTA file.

    Returns
    -------
    list of str
        Protein sequences.
    """

    fasta_path = Path(fasta_path)

    if not fasta_path.exists():
        raise FileNotFoundError(
            f"FASTA file not found: {fasta_path}"
        )

    records = list(SeqIO.parse(str(fasta_path), "fasta"))

    if not records:
        raise ValueError(
            f"No FASTA sequences were found in: {fasta_path}"
        )

    sequences = []

    for record in records:
        sequence = clean_sequence(str(record.seq))

        if sequence:
            sequences.append(sequence)

    if not sequences:
        raise ValueError(
            "The FASTA file contains no usable protein sequences."
        )

    return sequences


def amino_acid_composition(sequence: str) -> Dict[str, float]:
    """
    Calculate amino-acid composition for one protein.

    Frequencies are calculated for the 20 standard amino acids.

    Parameters
    ----------
    sequence : str
        Protein sequence.

    Returns
    -------
    dict
        Amino-acid frequencies.
    """

    sequence = clean_sequence(sequence)

    if not sequence:
        return {aa: 0.0 for aa in AMINO_ACIDS}

    length = len(sequence)

    return {
        aa: sequence.count(aa) / length
        for aa in AMINO_ACIDS
    }


def proteome_amino_acid_composition(
    sequences: Sequence[str],
) -> Dict[str, float]:
    """
    Calculate amino-acid composition across the complete proteome.

    Parameters
    ----------
    sequences : sequence of str
        Protein sequences.

    Returns
    -------
    dict
        Proteome amino-acid frequencies.
    """

    counts = {aa: 0 for aa in AMINO_ACIDS}
    total = 0

    for sequence in sequences:

        sequence = clean_sequence(sequence)

        for aa in sequence:

            if aa in counts:
                counts[aa] += 1
                total += 1

    if total == 0:
        return {
            aa: 0.0
            for aa in AMINO_ACIDS
        }

    return {
        aa: counts[aa] / total
        for aa in AMINO_ACIDS
    }


def sequence_statistics(
    sequences: Sequence[str],
) -> Dict[str, float]:
    """
    Calculate basic proteome sequence statistics.

    Parameters
    ----------
    sequences : sequence of str
        Protein sequences.

    Returns
    -------
    dict
        Proteome statistics.
    """

    lengths = np.array(
        [len(clean_sequence(s)) for s in sequences],
        dtype=float,
    )

    lengths = lengths[lengths > 0]

    if len(lengths) == 0:
        raise ValueError(
            "No non-empty protein sequences were supplied."
        )

    return {
        "protein_count": float(len(lengths)),
        "total_residues": float(np.sum(lengths)),
        "mean_protein_length": float(np.mean(lengths)),
        "median_protein_length": float(np.median(lengths)),
        "min_protein_length": float(np.min(lengths)),
        "max_protein_length": float(np.max(lengths)),
        "std_protein_length": float(np.std(lengths)),
    }


def proteome_features(
    sequences: Sequence[str],
) -> Dict[str, float]:
    """
    Generate the default BACion proteome feature set.

    Parameters
    ----------
    sequences : sequence of str
        Protein sequences.

    Returns
    -------
    dict
        Feature dictionary.
    """

    sequences = [
        clean_sequence(s)
        for s in sequences
        if clean_sequence(s)
    ]

    if not sequences:
        raise ValueError(
            "No valid protein sequences were supplied."
        )

    features = {}

  
    # Amino-acid composition

    aa_features = proteome_amino_acid_composition(
        sequences
    )

    for aa, value in aa_features.items():
        features[f"AA_{aa}"] = value


    # Basic proteome statistics

    features.update(
        sequence_statistics(sequences)
    )

    return features


def extract_features(
    fasta_path: Union[str, Path],
) -> pd.DataFrame:
    """
    Extract BACion features from a protein FASTA file.

    Parameters
    ----------
    fasta_path : str or Path
        Protein FASTA file.

    Returns
    -------
    pandas.DataFrame
        One-row feature matrix.
    """

    sequences = read_proteome(fasta_path)

    features = proteome_features(sequences)

    return pd.DataFrame([features])


def align_features(
    features: pd.DataFrame,
    feature_names: Sequence[str],
) -> pd.DataFrame:
    """
    Align calculated features to the exact model feature order.

    Missing features are filled with zero.

    Extra calculated features are discarded.

    Parameters
    ----------
    features : pandas.DataFrame
        Calculated feature matrix.

    feature_names : sequence of str
        Exact feature names expected by the model.

    Returns
    -------
    pandas.DataFrame
        Feature matrix in model order.
    """

    aligned = pd.DataFrame(
        0.0,
        index=features.index,
        columns=list(feature_names),
    )

    for name in feature_names:

        if name in features.columns:
            aligned[name] = features[name]

    return aligned
