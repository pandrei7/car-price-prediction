"""
This module implements a wrapper over the simple model.

The wrapper adapts the simple model to the interface of the web application,
allowing you to make predictions with it inside the app.
"""

import pandas as pd

from src import simplemodel
from src.utils import load_model_helper, load_model_weights

from .model_input import ModelInput


class Wrapper:
    """
    This wrapper uses the simple model to make predictions.
    """

    # These are parameters of the model.
    COLS_TO_SCALE = [
        "Anul", "Km", "Putere (CP)", "Capacitate cilindrica (cm3)",
        "Numar de portiere", "Consum (l/100km)",
    ]
    COLS_NORMAL = [
        "Fara accident in istoric", "Carte de service",
        "Filtru de particule", "Inmatriculat", "Primul proprietar",
    ]
    COLS_TO_EMBED = [
        "Marca", "Model", "Combustibil", "Cutie de viteze",
        "Tip Caroserie", "Culoare", "Tractiune",
    ]
    EMBEDDING_DIM = 4
    HIDDEN_SIZES = [113, 25]

    def __init__(self, model_name: str, helper_filename: str, dir: str):
        """Load the given model and helper from disk."""
        self.input_helper = load_model_helper(helper_filename, dir)

        self.model = simplemodel.SimpleModel(
            len(Wrapper.COLS_TO_SCALE) + len(Wrapper.COLS_NORMAL),
            [len(self.input_helper.vocabs[c]) for c in Wrapper.COLS_TO_EMBED],
            Wrapper.EMBEDDING_DIM,
            Wrapper.HIDDEN_SIZES,
        )
        load_model_weights(self.model, model_name, dir)
        self.model.eval()

    def predict(self, model_inputs: ModelInput) -> float:
        """Make a price prediction for the given inputs."""
        df = pd.DataFrame({
            "Anul": [model_inputs.year],
            "Km": [model_inputs.km],
            "Putere (CP)": [model_inputs.power],
            "Capacitate cilindrica (cm3)": [model_inputs.cylinder_cap],
            "Numar de portiere": [model_inputs.doors],
            "Consum (l/100km)": [model_inputs.consumption],
            "Fara accident in istoric": [model_inputs.no_accident],
            "Carte de service": [model_inputs.service_book],
            "Filtru de particule": [model_inputs.particle_filter],
            "Inmatriculat": [model_inputs.matriculated],
            "Primul proprietar": [model_inputs.first_owner],
            "Marca": [model_inputs.brand],
            "Model": [model_inputs.model],
            "Combustibil": [model_inputs.fuel],
            "Cutie de viteze": [model_inputs.gearbox],
            "Tip Caroserie": [model_inputs.body],
            "Culoare": [model_inputs.color],
            "Tractiune": [model_inputs.drivetrain],
        })

        inputs, indices = simplemodel.make_inputs(
            self.input_helper,
            df[Wrapper.COLS_TO_SCALE],
            df[Wrapper.COLS_NORMAL],
            df[Wrapper.COLS_TO_EMBED]
        )

        prediction = self.model(inputs, indices).item()
        prediction *= self.input_helper.maxes["Pret (EUR)"]
        return prediction
