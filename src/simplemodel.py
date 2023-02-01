"""
This module contains code for working with a simple car-price prediction model
and preparing input for it.

The model implemented here contains a sequence of linear layers.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F

from .training import Vocabulary


@dataclass
class InputHelper:
    """
    Stores data that helps build inputs for the model and interpret predictions.
    """
    maxes: Dict[str, float]
    vocabs: Dict[str, Vocabulary]


def make_input_helper(cols_to_scale: pd.DataFrame, cols_to_embed: pd.DataFrame) -> InputHelper:
    """
    Remember useful information about the given data, such as scaling constants.
    """
    return InputHelper(
        maxes={
            col: cols_to_scale[col].max()
            for col in cols_to_scale.columns
        },
        vocabs={
            col: Vocabulary(cols_to_embed[col])
            for col in cols_to_embed.columns
        },
    )


def make_inputs(
    helper: InputHelper,
    cols_to_scale: Optional[pd.DataFrame] = None,
    cols_normal: Optional[pd.DataFrame] = None,
    cols_to_embed: Optional[pd.DataFrame] = None,
) -> Tuple[torch.Tensor, torch.Tensor]:
    """Convert the given data into tensors which can be used as model inputs."""
    inputs = None
    if cols_to_scale is not None:
        assert type(cols_to_scale) == pd.DataFrame, "should be a DataFrame"
        scaled = torch.tensor(cols_to_scale.values)
        maxes = np.array([helper.maxes[col] for col in cols_to_scale.columns])
        scaled /= maxes
        inputs = scaled if inputs is None else torch.hstack([inputs, scaled])

    if cols_normal is not None:
        assert type(cols_normal) == pd.DataFrame, "should be a DataFrame"
        rest = torch.tensor(cols_normal.values)
        inputs = rest if inputs is None else torch.hstack([inputs, rest])

    indices = None
    if cols_to_embed is not None:
        assert type(cols_to_embed) == pd.DataFrame, "should be a DataFrame"
        translated = cols_to_embed.apply(
            lambda col: col.map(helper.vocabs[col.name].get_index))
        indices = torch.tensor(translated.values)

    return (inputs, indices)


class SimpleModel(nn.Module):
    """
    A simple model for predicting car prices.

    This model is based on linear layers and uses batch normalization.

    This model can handle both numeric inputs, as well as categorical inputs.
    Categorial inputs have to be passed as indices and will receive embeddings.
    """

    def __init__(self, input_size: int, vocab_lens: List[int], embedding_dim: int, hidden_sizes: List[int]):
        super().__init__()

        self.embeddings = nn.ModuleList([
            nn.Embedding(vocab_len, embedding_dim, max_norm=1)
            for vocab_len in vocab_lens
        ])

        # The first layer will process both numeric inputs and embeddings,
        # concatenated.
        prev_outputs = input_size + len(vocab_lens) * embedding_dim

        hidden = []
        for size in hidden_sizes:
            hidden.append(nn.Linear(prev_outputs, size, dtype=torch.float64))
            hidden.append(nn.BatchNorm1d(size, dtype=torch.float64))
            hidden.append(nn.ReLU())
            prev_outputs = size
        hidden.append(nn.Linear(prev_outputs, 1, dtype=torch.float64))

        self.hidden_layers = nn.Sequential(*hidden)

    def forward(self, inputs, indices):
        # Convert the indices into embeddings and add them to the other inputs.
        all_inputs = inputs
        for i, emb_layer in enumerate(self.embeddings):
            col_indices = emb_layer(indices[:, i])
            all_inputs = torch.hstack((all_inputs, col_indices))

        out = self.hidden_layers(all_inputs)
        return out
