# AILungMeasure/__init__.py
import os
import torch
import gdown

from .model import pspnet
from .segment_functions import segment
from .cv_functions import plot_measurments

def download_model_from_google_drive(file_id, destination):
    url = f"https://drive.google.com/uc?export=download&id={file_id}"
    gdown.download(url, destination, quiet=False)

def load_model():
    model_dir = os.path.join(os.path.dirname(__file__), 'models')
    model_path = os.path.join(model_dir, 'pspnet_orig_noAUX_darwin_clahe_10-26-2023.pt')
    
    # Ensure the model directory exists
    os.makedirs(model_dir, exist_ok=True)
    
    if not os.path.exists(model_path):
        file_id = '1cKN9KZFJsOFWZGaAmsrhib0tSr1lTOpA'  # Replace with your Google Drive file ID
        download_model_from_google_drive(file_id, model_path)
    
    model = pspnet(n_classes=1, input_size=(256, 256))
    print(f"Loading model from {model_path}")
    checkpoint = torch.load(model_path)
    model.load_state_dict(checkpoint['model_state_dict'])
    model.eval()
    print('Model loaded!')
    return model

__all__ = ['load_model', 'segment', 'plot_measurments']