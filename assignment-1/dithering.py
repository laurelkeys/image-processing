import cv2 # https://docs.opencv.org/4.1.0/
import numpy as np
import matplotlib.pyplot as plt

import argparse
from glob import iglob
from os.path import basename, splitext, join

INPUT_FOLDER = "i"
OUTPUT_FOLDER = "o"

class Technique:
    FLOYD_STEINBERG = "floyd_steinberg"
    STEVENSON_ARCE = "stevenson_arce"
    BURKES = "burkes"
    SIERRA = "sierra"
    STUCKI = "stucki"
    JARVIS_JUDICE_NINKE = "jarvis_judice_ninke"    
    list_all = [FLOYD_STEINBERG, STEVENSON_ARCE, BURKES, SIERRA, STUCKI, JARVIS_JUDICE_NINKE]

DIFFUSION_MAP = {
    Technique.FLOYD_STEINBERG: [
                                        ( 1, 0, 7/16), 
        (-1, 1, 3/16),  ( 0, 1, 5/16),  ( 1, 1, 1/16)
    ],
    Technique.STEVENSON_ARCE: [
                                                  ( 2, 0, 32/200), 
        (-3, 1, 12/200), (-1, 1, 26/200), ( 1, 1, 30/200), ( 3, 1, 16/200), 
                (-2, 2, 12/200), ( 0, 2, 26/200), ( 2, 2, 12/200),  
        (-3, 3,  5/200), (-1, 3, 12/200), ( 1, 3, 12/200), ( 3, 3,  5/200)
    ],
    Technique.BURKES: [
                                                     ( 1, 0, 8/32), ( 2, 0, 4/32), 
        (-2, 1, 2/32), (-1, 1, 4/32), ( 0, 1, 8/32), ( 1, 1, 4/32), ( 2, 1, 2/32)
    ],
    Technique.SIERRA: [
                                                     ( 1, 0, 5/32), ( 2, 0, 3/32), 
        (-2, 1, 2/32), (-1, 1, 4/32), ( 0, 1, 5/32), ( 1, 1, 4/32), ( 2, 1, 2/32), 
                       (-1, 2, 2/32), (-1, 2, 3/32), ( 1, 2, 2/32)
    ],
    Technique.STUCKI: [
                                                     ( 1, 0, 8/42), ( 2, 0, 4/42), 
        (-2, 1, 2/42), (-1, 1, 4/42), ( 0, 1, 8/42), ( 1, 1, 4/42), ( 2, 1, 2/42), 
        (-2, 2, 1/42), (-1, 2, 2/42), ( 0, 2, 4/42), ( 1, 2, 2/42), ( 2, 2, 1/42)
    ],
    Technique.JARVIS_JUDICE_NINKE: [
                                                     ( 1, 0, 7/48), ( 2, 0, 5/48), 
        (-2, 1, 3/48), (-1, 1, 5/48), ( 0, 1, 7/48), ( 1, 1, 5/48), ( 2, 1, 3/48), 
        (-2, 2, 1/48), (-1, 2, 3/48), ( 0, 2, 5/48), ( 1, 2, 3/48), ( 2, 2, 1/48)
    ]
}

###############################################################################

def show(img, img_title=""):
    plt.axis('off')
    plt.title(img_title)
    plt.imshow(img, vmin=0, vmax=255, cmap="gray" if img.ndim == 2 else None)
    plt.show()

def save(img, save_fname, save_path=OUTPUT_FOLDER):
    cv2.imwrite(join(save_path, save_fname + ".png"), img)

def grayscale(img):
    assert(img.ndim == 3)
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

clamp = lambda v, min_v=0, max_v=255: min_v if v < min_v else max_v if v > max_v else v

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
                    dithered_img[y+dy, x+dx] = dithered_img[y+dy, x+dx] + weight * quant_error
                    # clamp
                    dithered_img[y+dy, x+dx][dithered_img[y+dy, x+dx] < 0] = 0
                    dithered_img[y+dy, x+dx][dithered_img[y+dy, x+dx] > 255] = 255
    return dithered_img

###############################################################################

if __name__ == '__main__':
    def get_parser():
        parser = argparse.ArgumentParser(description='Implementations of dithering techniques for creating halftone images.')
        parser.add_argument('--image', '-img', type=str, 
                            help='The name of the input (original) image')
        parser.add_argument('--technique_index', '-t', type=int, choices=range(0, 6), 
                            help='The index of the dithering technique to be used, where: 0=floyd_steinberg, '
                                '1=stevenson_arce, 2=burkes, 3=sierra, 4=stucki, 5=jarvis_judice_ninke')
        parser.add_argument('--verbose', '-v', action="store_true", 
                            help='Increase verbosity')
        return parser

    parser = get_parser()
    args = parser.parse_args()
    techniques = Technique.list_all if args.technique_index == None else [Technique.list_all[args.technique_index]]
    
    # load input images into a dictionary
    images = {}
    if not args.image:
        for img_fname in iglob(join(INPUT_FOLDER, "*.png")):
            img_title = splitext(basename(img_fname))[0]
            img = cv2.imread(img_fname, cv2.IMREAD_COLOR)
            images[img_title] = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    else:
        if not args.image.endswith(".png"): args.image += ".png"
        img_title = splitext(basename(args.image))[0]
        img = cv2.imread(join(INPUT_FOLDER, args.image), cv2.IMREAD_COLOR)
        images[img_title] = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # dithering
    for technique in techniques:
        if args.verbose: print(f"\nTechnique: {technique}")
        for img_title, img in images.items():
            if args.verbose: print(f"  Dithering '{img_title}.png'...")

            # grayscale
            dithered_img = dither_gray(grayscale(img), technique) # TODO save the grayscaled image
            save_fname = f"[ordered] {img_title}_grayscale ({technique})"
            save(dithered_img, save_fname)
            if args.verbose: print(f"  ..saved grayscale image to: '{join(OUTPUT_FOLDER, save_fname)}.png'")

            # colored (RGB)
            dithered_img = dither_rgb(img, technique)
            save_fname = f"[ordered] {img_title} ({technique})"
            save(dithered_img, save_fname)
            if args.verbose: print(f"  ..saved colored image to: '{join(OUTPUT_FOLDER, save_fname)}.png'")

# TODO thresholding
# TODO alternating order
# TODO colored dithering