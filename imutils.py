import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

DEFAULT_EXT = ".png"
INPUT_FOLDER, OUTPUT_FOLDER = "i", "o"

###############################################################################

def is_gray(img):
    ''' Verifies if `img` is a 2D array '''
    return img.ndim == 2

def grayscale(bgr_img):
    ''' Returns the grayscale array representation of the BGR image `bgr_img` '''
    assert(not is_gray(bgr_img))
    return cv2.cvtColor(bgr_img, cv2.COLOR_BGR2GRAY)

def normalize(img, min_v, max_v):
    ''' Returns a normalized array representation of `img` with min=`min_v` and max=`max_v` '''
    norm_img = np.zeros(np.shape(img))
    norm_img = cv2.normalize(alpha=min_v, beta=max_v, norm_type=cv2.NORM_MINMAX, 
                             src=img, dst=norm_img)
    return norm_img

def clamp(v, min_v=0, max_v=255):
    ''' Constrains `v` to lie between `min_v` and `max_v`\n
        If `v` is an array, returns a copy of it with all values between `min_v` and `max_v` '''
    if (np.isscalar(v)):
        return min_v if (v < min_v) else max_v if (v > max_v) else v
    else:
        __v = v.copy()
        __v[__v < min_v] = min_v
        __v[__v > max_v] = max_v
        return __v

def pixel_value_count(img, value):
    ''' Returns the amount of pixels in `img` with the given `value` '''
    return (img == value).sum()

###############################################################################

def show(img, img_title=""):
    ''' Shows `img` without changing its pixel values for display '''
    plt.axis("off")
    plt.title(img_title)
    if is_gray(img):
        plt.imshow(img, vmin=0, vmax=255, cmap="gray")
    else:
        rgb_img = cv2.cvtColor(img.astype('uint8'), cv2.COLOR_BGR2RGB)
        plt.imshow(rgb_img, vmin=0, vmax=255)
    plt.show()

def load(full_path):
    ''' Returns the BGR array representation of the image stored in `full_path` '''
    bgr_img = cv2.imread(full_path, cv2.IMREAD_COLOR)
    return bgr_img

def load_gray(full_path):
    ''' Returns the grayscale array representation of the image stored in `full_path` '''
    gray_img = cv2.imread(full_path, cv2.IMREAD_GRAYSCALE)
    return gray_img

def save(img, full_path, ext=DEFAULT_EXT):
    ''' Saves `img` to `full_path`\n
        Uses `ext` as the file extension if not specified in `full_path` '''
    if not full_path.__contains__('.'):
        full_path += ext
    cv2.imwrite(full_path, img)

###############################################################################

def split_root_fname_ext(full_path):
    ''' Returns a tuple (`root`, `fname`, `ext`) such that `fname` + `ext` == `os.path.basename(full_path)` 
        and `os.path.join(root, fname + ext)` == `full_path` '''
    root = os.path.dirname(full_path)
    fname, ext = os.path.splitext(os.path.basename(full_path))
    return root, fname, ext

def image_fnames(folder=INPUT_FOLDER, ext=DEFAULT_EXT):
    ''' Iterator for the files in `folder` with `ext` extension '''
    for fname in os.listdir(folder):
        if fname.endswith(ext):
            yield fname
    return

def create_folder(path):
    ''' Creates the directories specified in `path` if they don't already exist '''
    fname = os.path.basename(path)
    if fname.__contains__('.'):
        path = os.path.dirname(path) # if path contains a file name we remove it
    if len(path) > 0 and not os.path.exists(path):
        os.makedirs(path)

###############################################################################

if __name__ == "__main__":
    print(f"NumPy version: {np.__version__}")
    print(f"OpenCV version: {cv2.__version__}") # https://docs.opencv.org/4.1.1/