import cv2
import numpy as np
import matplotlib.pyplot as plt
from image_processing_utils import clamp

''' Supported error diffusion techniques '''
class Technique:
    FLOYD_STEINBERG = "floyd_steinberg"
    STEVENSON_ARCE = "stevenson_arce"
    BURKES = "burkes"
    SIERRA = "sierra"
    STUCKI = "stucki"
    JARVIS_JUDICE_NINKE = "jarvis_judice_ninke"    
    list_all = [FLOYD_STEINBERG, STEVENSON_ARCE, BURKES, SIERRA, STUCKI, JARVIS_JUDICE_NINKE]

''' Lists of tuples specifying the (dx, dy, weight) values for each error diffusion technique '''
DIFFUSION_MAP = {
    Technique.FLOYD_STEINBERG: [
                                       (1, 0, 7/16), 
        (-1, 1, 3/16),  (0, 1, 5/16),  (1, 1, 1/16)
    ],
    Technique.STEVENSON_ARCE: [
                                                 (2, 0, 32/200), 
        (-3, 1, 12/200), (-1, 1, 26/200), (1, 1, 30/200), (3, 1, 16/200), 
                (-2, 2, 12/200), (0, 2, 26/200), (2, 2, 12/200),  
        (-3, 3,  5/200), (-1, 3, 12/200), (1, 3, 12/200), (3, 3,  5/200)
    ],
    Technique.BURKES: [
                                                    (1, 0, 8/32), (2, 0, 4/32), 
        (-2, 1, 2/32), (-1, 1, 4/32), (0, 1, 8/32), (1, 1, 4/32), (2, 1, 2/32)
    ],
    Technique.SIERRA: [
                                                    (1, 0, 5/32), (2, 0, 3/32), 
        (-2, 1, 2/32), (-1, 1, 4/32), (0, 1, 5/32), (1, 1, 4/32), (2, 1, 2/32), 
                       (-1, 2, 2/32), (0, 2, 3/32), (1, 2, 2/32)
    ],
    Technique.STUCKI: [
                                                    (1, 0, 8/42), (2, 0, 4/42), 
        (-2, 1, 2/42), (-1, 1, 4/42), (0, 1, 8/42), (1, 1, 4/42), (2, 1, 2/42), 
        (-2, 2, 1/42), (-1, 2, 2/42), (0, 2, 4/42), (1, 2, 2/42), (2, 2, 1/42)
    ],
    Technique.JARVIS_JUDICE_NINKE: [
                                                    (1, 0, 7/48), (2, 0, 5/48), 
        (-2, 1, 3/48), (-1, 1, 5/48), (0, 1, 7/48), (1, 1, 5/48), (2, 1, 3/48), 
        (-2, 2, 1/48), (-1, 2, 3/48), (0, 2, 5/48), (1, 2, 3/48), (2, 2, 1/48)
    ]
}

###############################################################################

def dither_gray(img, technique, threshold=128):
    ''' Applies a dithering technique to the given grayscale image, returning a new halftone (black and white) image.'''
    assert(technique in Technique.list_all), f"The dithering technique must be one of: {Technique.list_all}"
    assert(img.ndim == 2)
    dithered_img = img.copy()
    height, width = dithered_img.shape
    for x in range(width):
        for y in range(height):
            new_color = 0 if dithered_img[y, x] < threshold else 255
            quant_error = dithered_img[y, x] - new_color
            dithered_img[y, x] = new_color
            # error diffusion
            for dx, dy, weight in DIFFUSION_MAP[technique]:
                if 0 <= y+dy < height and 0 <= x+dx < width:
                    dithered_img[y+dy, x+dx] = clamp(dithered_img[y+dy, x+dx] + weight * quant_error)    
    return dithered_img

def dither_rgb(img, technique, threshold=128):
    ''' Applies a dithering technique to the given colored image, returning a new halftone (RGB) image.'''
    assert(technique in Technique.list_all), f"The dithering technique must be one of: {Technique.list_all}"
    assert(img.ndim == 3)
    dithered_img = img.copy()
    height, width, _ = dithered_img.shape
    for x in range(width):
        for y in range(height):
            new_color = np.where(dithered_img[y, x] < threshold, 0, 255)
            quant_error = dithered_img[y, x] - new_color
            dithered_img[y, x] = new_color
            # error diffusion
            for dx, dy, weight in DIFFUSION_MAP[technique]:
                if 0 <= y+dy < height and 0 <= x+dx < width:
                    dithered_img[y+dy, x+dx] = clamp(dithered_img[y+dy, x+dx] + weight * quant_error)
    return dithered_img

###############################################################################

if __name__ == "__main__":
    # check that the sum of weights of all techniques are equal to 1
    print(f"Diffusion map weight sum:")
    for technique in Technique.list_all:
        weight_sum = 0
        for _, _, weight in DIFFUSION_MAP[technique]:
            weight_sum += weight
        print(f"- {technique}: {weight_sum}")