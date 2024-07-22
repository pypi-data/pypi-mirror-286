"""Molecular Featurization Pipeline"""

from rdkit import Chem
from rdkit.Chem import rdFingerprintGenerator

from .utils import InvalidSMILESError


class FingerprintCalculator:
    def __init__(self, descriptor="morgan2"):
        self.descriptor = descriptor
        self.descriptors = {
            "morgan2": rdFingerprintGenerator.GetMorganGenerator(
                radius=2, includeChirality=False
            ).GetFingerprint,
            "morgan2_chiral": rdFingerprintGenerator.GetMorganGenerator(
                radius=2, includeChirality=True
            ).GetFingerprint,
            "morgan3": rdFingerprintGenerator.GetMorganGenerator(
                radius=3, includeChirality=False
            ).GetFingerprint,
            "morgan3_chiral": rdFingerprintGenerator.GetMorganGenerator(
                radius=3, includeChirality=True
            ).GetFingerprint,
            "atom pair": rdFingerprintGenerator.GetAtomPairGenerator().GetFingerprint,
            "topological torsion": rdFingerprintGenerator.GetTopologicalTorsionGenerator().GetFingerprint,
            "rdkit": rdFingerprintGenerator.GetRDKitFPGenerator().GetFingerprint,
        }

    def calculate_fingerprint(self, smi):
        mol = Chem.MolFromSmiles(smi)
        if mol:
            fn = self.descriptors[self.descriptor]
            return fn(mol)
        raise InvalidSMILESError
