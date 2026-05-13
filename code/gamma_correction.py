# Code for Debugging, stress test and just trying things. Not serious code.
# Ivan Acedo Aguilar

from datetime import datetime, timedelta
import numpy as np
from skimage import io, exposure
from tifffile import tifffile
from glob import glob
import os

def best_gamma_corr(img):
    img_float = img.astype(np.float32)
    img_float /= img_float.max()

    gamma_list = np.linspace(0.5, 2, 15)

    best_score = -np.inf
    best_img = img_float

    for g in gamma_list:
        corrected = exposure.adjust_gamma(img_float, g)
        score = corrected.std()

        if score > best_score:
            best_score = score
            best_img = corrected

    return best_img

def apply_gamma_and_save(image_paths):
    for path in image_paths:
        img = tifffile.imread(path)
        
        print(f"{path} --->  {img.shape}")

        base, ext = os.path.splitext(path)

        for i, page in enumerate(img):
            processed = best_gamma_corr(page)

            if img.dtype == np.uint16:
                img_out = (processed * 65535).astype(np.uint16)
            else:
                img_out = (processed * 255).astype(np.uint8)

            new_path = f"{base}_z{i}_edited{ext}"
            tifffile.imwrite(new_path, img_out, resolution=(300, 300),resolutionunit="inch")

            print(f"Saved: {new_path}")




image_list = glob("/Volumes/Extreme SSD/Ivan/Images/2/*.tiff")  # or .tiff, .png, etc.

apply_gamma_and_save(image_list)