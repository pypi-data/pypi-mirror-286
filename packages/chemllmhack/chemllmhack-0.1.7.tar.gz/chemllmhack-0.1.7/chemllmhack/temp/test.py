from Bio.PDB import PDBParser, Superimposer, Select
import os
import numpy as np


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


def calculate_rmsd(structure_path1, structure_path2, align_atoms='all', alignment_strategy='default'):
    parser = PDBParser(QUIET=True)

    try:
        structure1 = parser.get_structure('Structure1', structure_path1)
        structure2 = parser.get_structure('Structure2', structure_path2)
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
        #TODO Implement flexible alignment
        pass
    else:
        raise ValueError(f"Unknown alignment strategy: {alignment_strategy}")

    return sup.rms


def calculate_per_residue_rmsd(structure_path1, structure_path2, align_atoms='all'):
    parser = PDBParser(QUIET=True)

    try:
        structure1 = parser.get_structure('Structure1', structure_path1)
        structure2 = parser.get_structure('Structure2', structure_path2)
    except Exception as e:
        raise ValueError(f"Error parsing PDB files: {e}")

    per_residue_rmsd = {}

    for (model1, model2) in zip(structure1, structure2):
        for (chain1, chain2) in zip(model1, model2):
            for (res1, res2) in zip(chain1, chain2):
                res_atoms1 = list(res1.get_atoms())
                res_atoms2 = list(res2.get_atoms())

                atom_selector = AtomSelect(align_atoms)
                res_atoms1 = [atom for atom in res_atoms1 if atom_selector.accept_atom(atom)]
                res_atoms2 = [atom for atom in res_atoms2 if atom_selector.accept_atom(atom)]

                if len(res_atoms1) != len(res_atoms2):
                    continue

                sup = Superimposer()
                sup.set_atoms(res_atoms1, res_atoms2)

                rmsd = sup.rms
                per_residue_rmsd[res1.get_id()] = rmsd

    return per_residue_rmsd


try:
    #print current path
    print(os.getcwd())


    rmsd_value = calculate_rmsd("./temp/8ejb.pdb", "./temp/8ejb.pdb", align_atoms=['CA', 'CB'],
                                alignment_strategy='default')
    print(f"Calculated RMSD: {rmsd_value} Angstroms")

    per_residue_rmsd = calculate_per_residue_rmsd("./temp/8ejb.pdb", "./temp/8ejb.pdb",
                                                  align_atoms='backbone')
    print("Per-residue RMSD:")
    for res_id, rmsd in per_residue_rmsd.items():
        print(f"Residue {res_id}: {rmsd} Angstroms")
except Exception as e:
    print(f"An error occurred: {e}")