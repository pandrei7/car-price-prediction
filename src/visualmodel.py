"""
This module implements a model which handles visual and other types of inputs.
"""

from typing import List

import torch
import torch.nn as nn


class VisualModel(nn.Module):
    """
    A multi-modal model for predicting car prices.

    This model is based on `SimpleModel` and adapted to ingest images.
    """

    def __init__(self, input_size: int, vocab_lens: List[int], embedding_dim: int, hidden_sizes: List[int]):
        super().__init__()

        INTERIM = 28800 # This parameter depends on the image size.
        VISUAL_FEATURES = 10
        self.conv = nn.Sequential(
            self.conv_block(3, 16),
            self.conv_block(16, 32),
            nn.Flatten(),
            nn.Linear(INTERIM, VISUAL_FEATURES),
            nn.BatchNorm1d(VISUAL_FEATURES),
            nn.Dropout1d(0.5),
        )

        self.embeddings = nn.ModuleList([
            nn.Embedding(vocab_len, embedding_dim, max_norm=1)
            for vocab_len in vocab_lens
        ])
        embeddings_features = len(vocab_lens) * embedding_dim

        # The hidden layers will process all features (numeric, embeddings,
        # visual features) concatenated.
        prev_outputs = input_size + embeddings_features + VISUAL_FEATURES
        hidden = []
        for size in hidden_sizes:
            hidden.append(nn.Linear(prev_outputs, size, dtype=torch.float64))
            hidden.append(nn.BatchNorm1d(size, dtype=torch.float64))
            hidden.append(nn.ReLU())
            prev_outputs = size
        hidden.append(nn.Linear(prev_outputs, 1, dtype=torch.float64))
        self.hidden_layers = nn.Sequential(*hidden)

    def conv_block(self, input_size: int, output_size: int) -> nn.Sequential:
        return nn.Sequential(
            nn.Conv2d(input_size, output_size, (3, 3)),
            nn.ReLU(),
            nn.BatchNorm2d(output_size),
            nn.MaxPool2d((2, 2)),
        )

    def forward(self, inputs, indices, images):
        all_inputs = inputs

        # Convert the indices into embeddings and add them to the other inputs.
        for i, emb_layer in enumerate(self.embeddings):
            col_indices = emb_layer(indices[:, i])
            all_inputs = torch.hstack((all_inputs, col_indices))

        # Process the images and add their features to the other inputs.
        visual_features = self.conv(images)
        all_inputs = torch.hstack((all_inputs, visual_features))

        out = self.hidden_layers(all_inputs)
        return out
