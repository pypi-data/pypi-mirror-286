# smiles-autoencoder

[![GitHub version](https://badge.fury.io/gh/tjkessler%2Fsmiles-autoencoder.svg)](https://badge.fury.io/gh/tjkessler%2Fsmiles-autoencoder)
[![PyPI version](https://badge.fury.io/py/smiles-autoencoder.svg)](https://badge.fury.io/py/smiles-autoencoder)
![GitHub License](https://img.shields.io/github/license/tjkessler/smiles-autoencoder)

LSTM-based autoencoders for SMILES strings

# Installation

```
$ pip install smiles-autoencoder
```

or

```
$ git clone https://gitlab.com/tjkessler/smiles-autoencoder
$ cd smiles-autoencoder
$ pip install .
```

# Usage

### One-hot encoding

```python
from smiles_autoencoder.encoding import SmilesEncoder


smiles: List[str] = [...]

encoder = SmilesEncoder()
encoder.fit(smiles)

encoded_smiles: numpy.ndarray = encoder.encode_many(smiles)
# encoded_smiles.shape == (n_smiles_strings, sequence_length, n_unique_characters)
```

### Autoencoding

```python
import torch
import torch.nn as nn

from smiles_autoencoder.model import LSTMAutoencoder


encoded_smiles = torch.tensor(encoded_smiles, dtype=torch.float32)

autoencoder = LSTMAutoencoder(
    input_size=encoded_smiles.shape[2],
    hidden_size=64,
    latent_size=12,
    num_lstm_layers=1
)

opt = torch.optim.Adam(autoencoder.parameters(), lr=0.001)
loss_crit = nn.L1Loss(reduction="sum")

for epoch in range(8):

    for enc_smiles in encoded_smiles:

        opt.zero_grad()
        pred = autoencoder(enc_smiles)
        loss = loss_crit(pred, enc_smiles)
        loss.backward()
        opt.step()
```

### Decoding predictions

```python
pred_smiles: torch.Tensor = autoencoder(encoded_smiles[0])
pred_smiles: str = encoder.decode(torch.round(pred_smiles).detach().numpy().astype(int))
```

# Contributing, Reporting Issues and Other Support:

To contribute to smiles-autoencoder, make a pull request. Contributions should include tests for new features added, as well as extensive documentation.

To report problems with the software or feature requests, file an issue. When reporting problems, include information such as error messages, your OS/environment and Python version.

For additional support/questions, contact Travis Kessler (travis.j.kessler@gmail.com).
