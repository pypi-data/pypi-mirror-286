# AILungMeasure/example.py

import tempfile
import os
from matplotlib import pyplot as plt
import pydicom

from .segment_functions import segment
from .cv_functions import CV_target_points_plot, get_lung_measurments


temp_dir = tempfile.gettempdir()

def get_mask(image_path): return segment(image_path)

def show_mask(image_path): 
    mask = segment(image_path)
    plt.imshow(mask)
    
def show_measurments(image_path, dpi=200):
    ext = '.dcm'
    try:
        pydicom.dcmread(image_path)
    except:
        ext = '.jpg'
    temp_dir = tempfile.gettempdir()
    temp_mask = os.path.join(temp_dir, 'tmp_mask'+ext)
    mask = segment(image_path, temp_mask)
    CV_target_points_plot(temp_mask , imname= image_path,  plot=1, alpha=0.5, cmap='jet', radius=40, mode=1, dpi=dpi)
    # os.remove(temp_mask)
    
    
def get_measurments(image_path, pixel_spacing=1):
    ext = '.dcm'
    try:
        pydicom.dcmread(image_path)
    except:
        ext = '.jpg'
    temp_dir = tempfile.gettempdir()
    temp_mask = os.path.join(temp_dir, 'tmp_mask'+ext)
    mask = segment(image_path, temp_mask)
    r = get_lung_measurments(temp_mask, pixel_spacing)
    # os.remove(temp_mask)
    ret = {"R-ACPA": r[3], "R-AMD": r[4], 
           "L-ACPA": r[8], "L-AMD": r[9],
           "width-at-hilum": r[0] , "width-at-base": r[13]}
           # "height" : r[1],
           # "R-ACPA-old": r[2], , , "R-width": r[5], "R-height": r[6],
           # "L-ACPA-old": r[7],  "L-width": r[10], "L-height": r[11], 
           # "width-at-base": r[12], "width-at-base-modified": r[13], "ratio": r[14]}
    return ret


    