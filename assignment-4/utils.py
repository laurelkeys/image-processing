import os
import warnings

import cv2
import numpy as np
import matplotlib.pyplot as plt

INPUT_FOLDER  = "i"
OUTPUT_FOLDER = "o"

DEFAULT_EXT = ".png"

###############################################################################

def is_gray(img):
    ''' Verifies if `img` is a 2D array '''
    return img.ndim == 2

###############################################################################

def show(img, img_title=""):
    ''' Shows `img` without changing its pixel values for display '''
    plt.axis("off")
    plt.title(img_title)
    if is_gray(img):
        plt.imshow(img, vmin=0, vmax=255, cmap="gray")
    else:
        # FIXME
        rgb_img = cv2.cvtColor(img.astype('uint8'), cv2.COLOR_BGR2RGB)
        plt.imshow(rgb_img, vmin=0, vmax=255)
    plt.show()

def load(full_path):
    ''' Returns the BGR array representation of the image stored in `full_path` '''
    bgr_img = cv2.imread(full_path, cv2.IMREAD_COLOR)
    return bgr_img

def save(img, full_path, ext=DEFAULT_EXT):
    ''' Saves `img` to `full_path`\n
        Uses `ext` as the file extension if not specified in `full_path` '''
    if not full_path.__contains__('.'):
        full_path += ext
    cv2.imwrite(full_path, img)

def split_root_name_ext(full_path):
    ''' Returns a tuple (`root`, `name`, `ext`) such that `name` + `ext` == os.path.basename(`full_path`) 
        and os.path.join(`root`, `name` + `ext`) == `full_path` '''
    root = os.path.dirname(full_path)
    name, ext = os.path.splitext(os.path.basename(full_path))
    return root, name, ext

def create_folder(path):
    ''' Creates the directories specified in `path` if they don't already exist '''
    fname = os.path.basename(path)
    if fname.__contains__('.'):
        path = os.path.dirname(path) # if path contains a file name we remove it
    if not os.path.exists(path):
        os.makedirs(path)

###############################################################################

if __name__ == "__main__":
    print(f"cv2 version: {cv2.__version__}")  # https://docs.opencv.org/4.1.0/
    print(f"numpy version: {np.__version__}")