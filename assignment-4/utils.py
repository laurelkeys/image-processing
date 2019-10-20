import os
import warnings

import cv2
import numpy as np
import matplotlib.pyplot as plt

INPUT_FOLDER  = "i"
OUTPUT_FOLDER = "o"

DEFAULT_EXT = ".png"

BLACK = 0
WHITE = 255

RGB_BLACK = BGR_BLACK = np.array([ 0 ,  0 ,  0 ])
RGB_WHITE = BGR_WHITE = np.array([255, 255, 255])
RGB_RED   = BGR_BLUE  = np.array([255,  0 ,  0 ])
RGB_GREEN = BGR_GREEN = np.array([ 0 , 255,  0 ])
RGB_BLUE  = BGR_RED   = np.array([ 0 ,  0 , 255])

###############################################################################

def is_gray(img):
    ''' Verifies if img is a 2D array '''
    return img.ndim == 2

def normalize(img, min_v, max_v):
    ''' Returns a normalized array representation of img with min=min_v and max=max_v '''
    norm_img = np.zeros(np.shape(img)) # output dst array
    norm_img = cv2.normalize(img, norm_img, min_v, max_v, cv2.NORM_MINMAX)
    return norm_img

def clamp(v, min_v=0, max_v=255):
    ''' Constrains v to lie between min_v and max_v\n
        If v is an array, returns a copy of it with all values between min_v and max_v '''
    if (np.isscalar(v)):
        return min_v if (v < min_v) else max_v if (v > max_v) else v
    else:
        __v = v.copy()
        __v[__v < min_v] = min_v
        __v[__v > max_v] = max_v
        return __v

###############################################################################

def show(img, img_title=""):
    ''' Shows img without changing its pixel values for display '''
    plt.axis("off")
    plt.title(img_title)
    if is_gray(img):
        plt.imshow(img, vmin=0, vmax=255, cmap="gray")
    else:
        # FIXME
        rgb_img = cv2.cvtColor(img.astype('uint8'), cv2.COLOR_BGR2RGB)
        plt.imshow(rgb_img, vmin=0, vmax=255)
    plt.show()

def load(fname, folder=INPUT_FOLDER):
    ''' Returns the BGR array representation of the image stored in os.path.join(folder, fname) '''
    bgr_img = cv2.imread(os.path.join(folder, fname), cv2.IMREAD_COLOR)
    return bgr_img

def save(img, fname, folder=OUTPUT_FOLDER, ext=DEFAULT_EXT):
    ''' Saves img to os.path.join(folder, fname)\n
        Uses ext as the file extension if not specified in fname '''
    if not fname.__contains__('.'):
        fname += ext
    cv2.imwrite(os.path.join(folder, fname), img)

def split_name_ext(fname):
    ''' Returns a tuple (name, ext) such that name + ext == os.path.basename(fname)'''
    return os.path.splitext(os.path.basename(fname))

def image_fnames(folder=INPUT_FOLDER, ext=DEFAULT_EXT):
    ''' Iterator for the files in folder with ext extension '''
    for fname in os.listdir(folder):
        if fname.endswith(ext):
            yield fname

def create_folder(path):
    ''' Creates the directories specified in path if they don't already exist '''
    fname = os.path.basename(path)
    if fname.__contains__('.'):
        path = os.path.dirname(path) # if path contains a file name we remove it
    if not os.path.exists(path):
        os.makedirs(path)

###############################################################################

if __name__ == "__main__":
    print(f"cv2 version: {cv2.__version__}")  # https://docs.opencv.org/4.1.0/
    print(f"numpy version: {np.__version__}")