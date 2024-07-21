from typing import List

import numpy
import numpy as np


class SmilesEncoder:

    def __init__(self):
        """ SmilesEncoder: one-hot encoding for SMILES strings """

        self._vocab = ["unk"]
        self._max_len = 0

    def fit(self, smiles: List[str]) -> None:
        """ SmilesEncoder.fit: fit encoder using supplied SMILES strings

        Args:
            smiles (List[str]): list of SMILES strings
        """

        for smi in smiles:
            for char in smi:
                if char not in self._vocab:
                    self._vocab.append(char)
            if len(smi) > self._max_len:
                self._max_len = len(smi)

    def encode(self, smiles: str) -> numpy.ndarray:
        """ SmilesEncoder.encode: one-hot encode a SMILES string

        Args:
            smiles (str): SMILES string to encode

        Returns:
            numpy.ndarray: shape (seq_len, n_features)
        """

        encoding = np.zeros((self._max_len, len(self._vocab)))
        for idx, char in enumerate(smiles):
            encoding[idx, self._vocab.index(char)] = 1.0
        return encoding

    def encode_many(self, smiles: List[str]) -> numpy.ndarray:
        """ SmilesEncoder.encode_many: one-hot encode multiple SMILES strings

        Args:
            smiles (List[str]): SMILES strings to encode

        Returns:
            numpy.ndarray: shape (n_smiles, seq_len, n_features)
        """

        return np.concatenate([
            np.expand_dims(self.encode(smi), axis=0)
            for smi in smiles
        ], axis=0)

    def decode(self, X: numpy.ndarray) -> str:
        """ SmilesEncoder.decode: decode a one-hot encoded SMILES string

        Args:
            X (numpy.ndarray): shape (seq_len, n_features)

        Returns:
            str: decoded SMILES string
        """

        smiles = ""
        for item in X:
            _loc = np.where(item == 1)[0]
            if len(_loc) > 0:
                smiles += self._vocab[int(_loc[0])]
        return smiles

    def decode_many(self, X: numpy.ndarray) -> List[str]:
        """ SmilesEncoder.decode_many: decode multiple one-hot encoded SMILES
        strings

        Args:
            X (numpy.ndarray): shape (n_smiles, seq_len, n_features)

        Returns:
            List[str]: decoded SMILES strings
        """

        return [self.decode(entry) for entry in X]
