import torch
import torch.nn as nn
from torch.nn import functional as F


class LSTMEncoder(nn.Module):

    def __init__(self, input_size: int, hidden_size: int,
                 latent_size: int, num_lstm_layers: int = 1):
        """ LSTMEncoder: encodes data to latent dimension using a
        `torch.nn.LSTM` module

        Args:
            input_size (int): size of input layer (num. features)
            hidden_size (int): size of LSTM hidden layer(s)
            latent_size (int): size of latent dimension
            num_lstm_layers (int): number of hidden layers in LSTM
        """

        super().__init__()
        self.rnn = nn.LSTM(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_lstm_layers,
            batch_first=True
        )
        self.lin = nn.Linear(hidden_size, latent_size)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """ LSTMEncoder.forward: forward operation through encoder

        Args:
            x (torch.Tensor): shape (seq_len, n_features) or (n_samples,
                seq_len, n_features)

        Returns:
            torch.Tensor: shape (seq_len, latent_size) or (n_samples,
                seq_len, latent_size)
        """

        out, (h, _) = self.rnn(x)
        out = self.lin(out)
        return out, h.squeeze(0)


class LSTMDecoder(nn.Module):

    def __init__(self, output_size: int, hidden_size: int,
                 latent_size: int, num_lstm_layers: int = 1):
        """ LSTMEncoder: decodes latent data to original dimensionality using
        a `torch.nn.LSTM` module

        Args:
            output_size (int): size of output layer (num. features, equal to
                input_size in `LSTMEncoder`)
            hidden_size (int): size of LSTM hidden layer(s)
            latent_size (int): size of latent dimension
            num_lstm_layers (int): number of hidden layers in LSTM
        """

        super().__init__()
        self.rnn = nn.LSTM(
            input_size=latent_size,
            hidden_size=hidden_size,
            num_layers=num_lstm_layers,
            batch_first=True
        )
        self.lin = nn.Linear(hidden_size, output_size)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """ LSTMDecoder.forward: forward operation through decoder

        Args:
            x (torch.Tensor): shape (seq_len, latent_size) or (n_samples,
                seq_len, latent_size)

        Returns:
            torch.Tensor: shape (seq_len, n_features) or (n_samples,
                seq_len, n_features)
        """

        out, (h, _) = self.rnn(x)
        out = self.lin(out)
        return out, h.squeeze(0)


class LSTMAutoencoder(nn.Module):

    def __init__(self, input_size: int, hidden_size: int,
                 latent_size: int, num_lstm_layers: int = 1):
        """ LSTMAutoencoder: autoencodes data to and from latent dimension
        using `torch.nn.LSTM` modules

        Args:
            input_size (int): size of input/output layers (num. features)
            hidden_size (int): size of LSTM hidden layer(s)
            latent_size (int): size of latent dimension
            num_lstm_layers (int): number of hidden layers in LSTM
        """

        super().__init__()
        self.enc = LSTMEncoder(input_size, hidden_size,
                               latent_size, num_lstm_layers)
        self.dec = LSTMDecoder(input_size, hidden_size,
                               latent_size, num_lstm_layers)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """ LSTMAutoencoder.forward: forward operation through autoencoder

        Args:
            x (torch.Tensor): shape (seq_len, n_features) or (n_samples,
                seq_len, n_features)

        Returns:
            torch.Tensor: shape (seq_len, n_features) or (n_samples,
                seq_len, n_features)
        """

        x_enc, _ = self.enc(x)
        x_dec, _ = self.dec(x_enc)
        return x_dec
    
    def encode(self, x: torch.Tensor) -> torch.Tensor:
        """ LSTMAutoencoder.encode: encodes data to latent dimension

        Args:
            x (torch.Tensor): shape (seq_len, n_features) or (n_samples,
                seq_len, n_features)

        Returns:
            torch.Tensor: shape (seq_len, latent_size) or (n_samples,
                seq_len, latent_size)
        """

        x_enc, _ = self.enc(x)
        return x_enc
    
    def decode(self, x: torch.Tensor) -> torch.Tensor:
        """ LSTMAutoencoder.encode: decodes data from latent dimension

        Args:
            x (torch.Tensor): shape (seq_len, latent_size) or (n_samples,
                seq_len, latent_size)

        Returns:
            torch.Tensor: shape (seq_len, n_features) or (n_samples,
                seq_len, n_features)
        """

        x_dec, _ = self.dec(x)
        return x_dec
