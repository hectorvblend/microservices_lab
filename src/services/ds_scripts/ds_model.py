import os
from time import sleep
import dill
import pathlib

BASE_DIR = pathlib.Path(os.path.dirname(os.path.abspath(__file__)))
model_file_path = os.path.join(BASE_DIR, "model.pkl")

# 📌 Codigo para generar el fake model:
def model(number):
    return number ** 2
with open(model_file_path, "wb") as f:
    dill.dump(model, f)


async def load_model():
    """
    Asynchronously loads a pre-trained model from a file.

    The model is serialized using dill and stored in the file
    specified by `model_file_path`. This function reads the file
    and deserializes the model for use.

    Returns:
        callable: The deserialized model loaded from the file.
    """
    sleep(10)
    with open(model_file_path, "rb") as f:
        loaded_model = dill.load(f)
    return loaded_model