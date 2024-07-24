# AILungMeasure/example.py

import tempfile
import os
from matplotlib import pyplot as plt
import pydicom

from .segment_functions import segment
from .cv_functions import CV_target_points_plot, get_lung_measurments


temp_dir = tempfile.gettempdir()
R_ACPA_slope = 0.97 ; R_ACPA_intercept = 14.5
L_ACPA_slope = 1.02 ; L_ACPA_intercept = -4.29

R_AMD_slope = 1.02 ; R_AMD_intercept = -1.34
L_AMD_slope = 1.0  ; L_AMD_intercept = 2.45

width_hilum_slope = 0.93 ; width_hilum_intercept = 14.54
width_base_slope  = 0.90 ; width_base_intercept  = 31.48

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
    ret = {"R-ACPA": r[3] * R_ACPA_slope + R_ACPA_intercept, 
           "R-AMD": r[4]  * R_AMD_slope + R_AMD_intercept, 
           "L-ACPA": r[8] * L_ACPA_slope + L_ACPA_intercept,
           "L-AMD": r[9]  * L_AMD_slope + L_AMD_intercept,
           "width-at-hilum": r[0] * width_hilum_slope + width_hilum_intercept,
           "width-at-base": r[13] * width_base_slope + width_base_intercept
          }
           # "height" : r[1],
           # "R-ACPA-old": r[2], , , "R-width": r[5], "R-height": r[6],
           # "L-ACPA-old": r[7],  "L-width": r[10], "L-height": r[11], 
           # "width-at-base": r[12], "width-at-base-modified": r[13], "ratio": r[14]}
    return ret


    