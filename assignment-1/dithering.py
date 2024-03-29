import numpy as np
from utils import clamp

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
    ],
}

###############################################################################

def threshold(img, threshold=128):
    ''' Returns a new halftone image based on the given threshold '''
    __img = img.copy()
    __img = np.where(__img < threshold, 0, 255)
    return __img

def dither(img, technique, threshold=128):
    ''' Returns a new halftone image by applying the error diffusion dithering technique to img\n
        The image is traversed top-to-bottom in a raster pattern (left-to-right) '''
    assert(technique in Technique.list_all), f"The dithering technique must be one of: {Technique.list_all}"
    __img = img.copy()
    height, width, *_ = __img.shape
    for y in range(height):
        for x in range(width):
            new_color = np.where(__img[y, x] < threshold, 0, 255)
            quantization_error = __img[y, x] - new_color
            __img[y, x] = new_color
            # error diffusion
            for dx, dy, weight in DIFFUSION_MAP[technique]:
                if (0 <= y + dy < height) and (0 <= x + dx < width):
                    __img[y + dy, x + dx] = clamp(__img[y + dy, x + dx] + weight * quantization_error)
    return __img

def serpentine_dither(img, technique, threshold=128):
    ''' Returns a new halftone image by applying the error diffusion dithering technique to img\n
        The image is traversed top-to-bottom in a serpentine pattern (alternating left-to-right and right-to-left) '''
    assert(technique in Technique.list_all), f"The dithering technique must be one of: {Technique.list_all}"
    __img = img.copy()
    height, width, *_ = __img.shape
    for y in range(height):
        left_to_right = (y % 2 == 0) # go right-to-left on odd lines
        for x in (range(width) if left_to_right else range(width - 1, -1, -1)):
            new_color = np.where(__img[y, x] < threshold, 0, 255)
            quantization_error = __img[y, x] - new_color
            __img[y, x] = new_color
            # error diffusion
            for dx, dy, weight in DIFFUSION_MAP[technique]:
                if not left_to_right:
                    dx = -dx # alternate horizontal direction
                if (0 <= y + dy < height) and (0 <= x + dx < width):
                    __img[y + dy, x + dx] = clamp(__img[y + dy, x + dx] + weight * quantization_error)
    return __img

###############################################################################

if __name__ == "__main__":
    # check that the sum of weights is equal to 1 for all dithering techniques
    print(f"Diffusion map weight sum:")
    for technique in Technique.list_all:
        weight_sum = 0
        for _, _, weight in DIFFUSION_MAP[technique]:
            weight_sum += weight
        print(f"- {technique}: {weight_sum}")