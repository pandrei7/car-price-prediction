"""
This module implements a dummy model wrapper.

This wrapper allows you to test the rest of the implementation without loading
a real model.
"""

from .model_input import ModelInput


class DummyWrapper:
    """
    The dummy wrapper implements the model interface expected by the
    application without using a real model.
    """

    def predict(self, inputs: ModelInput):
        """Make a random price prediction."""
        price = inputs.consumption
        if inputs.no_accident:
            price *= 2
        return price
