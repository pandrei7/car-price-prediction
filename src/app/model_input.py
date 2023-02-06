from dataclasses import dataclass

import numpy as np


@dataclass
class ModelInput:
    """
    This class represents model-agnostic inputs provided by the user and used
    to make predictions.
    """

    image: np.ndarray

    # Numeric inputs.
    year: float
    km: float
    power: float
    cylinder_cap: float
    doors: float
    consumption: float

    # Boolean inputs.
    no_accident: bool
    service_book: bool
    particle_filter: bool
    matriculated: bool
    first_owner: bool

    # Categorical inputs.
    brand: str
    model: str
    fuel: str
    gearbox: str
    body: str
    color: str
    drivetrain: str
