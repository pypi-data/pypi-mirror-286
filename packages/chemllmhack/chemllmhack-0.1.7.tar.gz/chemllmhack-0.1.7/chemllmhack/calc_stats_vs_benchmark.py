# -*- coding: utf-8 -*-
"""
File name: collect_stats_result.py
Author: Bowen
Date created: 22/7/2024
Description: This Python file is for collect results and run against the benchmark.

Copyright information: © 2024 QDX
"""
import json
import os
from Bio.PDB import PDBParser, Superimposer, Select
import os
import numpy as np
import scipy


def affinity_benchmark(result_path, benchmark_name="BTK"):
    """
    This function is for benchmarking the affinity correlation results in BTK_wT_101 sheet or BTK_M_343 sheet.
    :param result_path: your result path
    :return: the pearson, kendal and spearman correlation result
    """
    if result_path is None:
        print("Please provide the path to the result file.")
    elif not os.path.exists(result_path) or not result_path.endswith(".json"):
        print("The result file does not exist or you need to provide JSON format file.")
    else:
        if benchmark_name == "BTK":
            script_dir = os.path.dirname(__file__)
            #TODO need to further handle the benchmark file, from backup folder
            benchmark_affinity_path = os.path.join(script_dir, "benchmark/benchmark_affinity/benchmark_affinity_wT.json")
            with open(benchmark_affinity_path, "r") as f:
                benchmark_affinity = json.load(f)
            with open(result_path, "r") as f:
                result = json.load(f)

            smiles_keys = benchmark_affinity.keys()
            Ki_values1 = [benchmark_affinity[smiles]["Ki (nM)"] for smiles in smiles_keys]
            Ki_values2 = [result[smiles]["Ki (nM)"] for smiles in smiles_keys]

            pearson_corr, _ = scipy.stats.pearsonr(Ki_values1, Ki_values2)
            spearman_corr, _ = scipy.stats.spearmanr(Ki_values1, Ki_values2)
            kendall_corr, _ = scipy.stats.kendalltau(Ki_values1, Ki_values2)

            print(f"Pearson correlation coefficient: {pearson_corr}")
            print(f"Spearman correlation coefficient: {spearman_corr}")
            print(f"Kendall correlation coefficient: {kendall_corr}")

            correlation_coefficients = {
                "Pearson correlation coefficient": pearson_corr,
                "Spearman correlation coefficient": spearman_corr,
                "Kendall correlation coefficient": kendall_corr
            }

            return correlation_coefficients

        elif benchmark_name == "BTK_mutant":
            script_dir = os.path.dirname(__file__)
            benchmark_affinity_path = os.path.join(script_dir, "benchmark/benchmark_affinity/benchmark_affinity_M.json")
            with open(benchmark_affinity_path, "r") as f:
                benchmark_affinity = json.load(f)
            with open(result_path, "r") as f:
                result = json.load(f)

            smiles_keys = benchmark_affinity.keys()
            ic50_values1 = [benchmark_affinity[smiles]["IC50 (nM)"] for smiles in smiles_keys]
            ic50_values2 = [result[smiles]["IC50 (nM)"] for smiles in smiles_keys]

            pearson_corr, _ = scipy.stats.pearsonr(ic50_values1, ic50_values2)
            spearman_corr, _ = scipy.stats.spearmanr(ic50_values1, ic50_values2)
            kendall_corr, _ = scipy.stats.kendalltau(ic50_values1, ic50_values2)

            print(f"Pearson correlation coefficient: {pearson_corr}")
            print(f"Spearman correlation coefficient: {spearman_corr}")
            print(f"Kendall correlation coefficient: {kendall_corr}")

            correlation_coefficients = {
                "Pearson correlation coefficient": pearson_corr,
                "Spearman correlation coefficient": spearman_corr,
                "Kendall correlation coefficient": kendall_corr
            }

            return correlation_coefficients
        else:
            print("Please provide the correct benchmark name.")


class AtomSelect(Select):
    def __init__(self, atom_types):
        self.atom_types = atom_types

    def accept_atom(self, atom):
        if self.atom_types == 'all':
            return True
        elif self.atom_types == 'backbone':
            return atom.get_name() in ['CA', 'C', 'N', 'O']
        elif isinstance(self.atom_types, list):
            return atom.get_name() in self.atom_types
        return True


def rmsd_benchmark(your_protein_path, align_atoms='all', alignment_strategy='default'):
    parser = PDBParser(QUIET=True)

    script_dir = os.path.dirname(__file__)
    benchmark_protein_path = os.path.join(script_dir, "benchmark/benchmark_RMSD/benchmark_protein.pdb")

    try:
        structure1 = parser.get_structure('Structure1', benchmark_protein_path)
        structure2 = parser.get_structure('Structure2', your_protein_path)
    except Exception as e:
        raise ValueError(f"Error parsing PDB files: {e}")

    ref_atoms = []
    sample_atoms = []

    for (model1, model2) in zip(structure1, structure2):
        for (chain1, chain2) in zip(model1, model2):
            fixed = list(chain1.get_atoms())
            moving = list(chain2.get_atoms())

            atom_selector = AtomSelect(align_atoms)
            fixed = [atom for atom in fixed if atom_selector.accept_atom(atom)]
            moving = [atom for atom in moving if atom_selector.accept_atom(atom)]

            if len(fixed) != len(moving):
                raise ValueError("Structures have different number of selected atoms")

            ref_atoms.extend(fixed)
            sample_atoms.extend(moving)

    sup = Superimposer()
    sup.set_atoms(ref_atoms, sample_atoms)

    if alignment_strategy == 'default' or alignment_strategy == 'rigid':
        sup.apply(sample_atoms)
    elif alignment_strategy == 'flexible':
        # Implement flexible alignment here
        pass
    else:
        raise ValueError(f"Unknown alignment strategy: {alignment_strategy}")

    return sup.rms


def per_residue_rmsd_benchmark(structure_path1, structure_path2, align_atoms='all'):
    parser = PDBParser(QUIET=True)

    try:
        structure1 = parser.get_structure('Structure1', structure_path1)
        structure2 = parser.get_structure('Structure2', structure_path2)
    except Exception as e:
        raise ValueError(f"Error parsing PDB files: {e}")

    per_residue_rmsd = {}

if __name__ == "__main__":
    result_path = "./results.json"
    affinity_benchmark(result_path)

