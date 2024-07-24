# AILungMeasure/__init__.py
import os
import torch
import gdown

from .model_functions import pspnet
from .segment_functions import segment
from .cv_functions import plot_measurments
from .main_function import *

version = 2.0


def download_model_from_google_drive(destination, quiet=False):
    file_id = "18xgjQeengKmlsFcOARqckLGGdARSG5cp"
    download_url = f"https://drive.google.com/uc?id={file_id}"

    # Download the file
    gdown.download(download_url, destination, quiet=quiet)


def load_model(quiet=False):
    model_dir = os.path.join(os.path.dirname(__file__), "models")
    model_path = os.path.join(model_dir, "pspnet_orig_noAUX_darwin_clahe_10-26-2023.pt")

    # Ensure the model directory exists
    os.makedirs(model_dir, exist_ok=True)

    if not os.path.exists(model_path):
        download_model_from_google_drive(model_path, quiet=quiet)

    model = pspnet(n_classes=1, input_size=(256, 256))
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    checkpoint = torch.load(model_path, map_location=device)
    model.load_state_dict(checkpoint["model_state_dict"])
    model.eval()
    if not quiet:
        print("Model loaded!")
    return model


__all__ = ["load_model", "segment", "plot_measurments", "main_functions"]

model = load_model(quiet=True)
