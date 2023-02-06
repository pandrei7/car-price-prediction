"""
This module implements a web application for making car price predictions.
"""

from typing import Optional

from PIL import Image
from flask import Flask, Request, render_template, request

from . import visualmodel_wrapper
from .model_input import ModelInput

app = Flask(__name__)


def load_the_model() -> None:
    """Load into memory *globally* the model used to make predictions."""
    global model

    model = visualmodel_wrapper.Wrapper(
        model_name="visualmodel",
        helper_filename="visualmodel-helper.pkl",
        dir="models",
    )

    print("Done loading the model.")


def make_prediction(model_input: ModelInput) -> float:
    global model
    return model.predict(model_input)


def parse_request(request: Request) -> ModelInput:
    """Convert the user-submitted form into usable input."""

    return ModelInput(
        # It's possible the user did not provide an image.
        image=Image.open(file) if (file := request.files["photo"]) else None,

        # Numeric inputs.
        year=float(request.form["year"]),
        km=float(request.form["km"]),
        power=float(request.form["power"]),
        cylinder_cap=float(request.form["cylinder_cap"]),
        doors=float(request.form["doors"]),
        consumption=float(request.form["consumption"]),

        # Boolean inputs.
        no_accident="no_accident" in request.form,
        service_book="service_book" in request.form,
        particle_filter="particle_filter" in request.form,
        matriculated="matriculated" in request.form,
        first_owner="first_owner" in request.form,

        # Categorical inputs.
        brand=request.form["brand"],
        model=request.form["model"],
        fuel=request.form["fuel"],
        gearbox=request.form["gearbox"],
        body=request.form["body"],
        color=request.form["color"],
        drivetrain=request.form["drivetrain"],
    )


@app.route("/")
def index(form=None, prediction: Optional[float] = None):
    return render_template("index.html", form=form, prediction=prediction)


@app.route("/predict", methods=["POST"])
def predict():
    model_input = parse_request(request)
    prediction = make_prediction(model_input)

    return index(form=request.form, prediction=prediction)


if __name__ == "__main__":
    load_the_model()
    app.run(host="0.0.0.0", debug=True)
