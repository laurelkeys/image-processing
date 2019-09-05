import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

INPUT_FOLDER = "i"
OUTPUT_FOLDER = "o"

RGB_BLACK = np.array([ 0 ,  0 ,  0 ])
RGB_WHITE = np.array([255, 255, 255])
RGB_RED   = np.array([ 0 ,  0 , 255])
RGB_GREEN = np.array([ 0 , 255,  0 ])
RGB_BLUE  = np.array([255,  0 ,  0 ])

###############################################################################

def show(img, img_title=""):
    ''' Shows img without changing its pixel values for display '''
    plt.axis('off')
    plt.title(img_title)
    plt.imshow(img, vmin=0, vmax=255, cmap="gray" if img.ndim == 2 else None)
    plt.show()

def load(fname, folder=INPUT_FOLDER):
    ''' Returns the RGB array representation of the image stored in os.path.join(folder, fname) '''
    bgr_img = cv2.imread(os.path.join(folder, fname), cv2.IMREAD_COLOR)
    return cv2.cvtColor(bgr_img, cv2.COLOR_BGR2RGB)

def save(img, fname, folder=OUTPUT_FOLDER):
    ''' Saves img to os.path.join(folder, fname) '''
    cv2.imwrite(os.path.join(folder, fname), img)

def images_in_folder(folder=INPUT_FOLDER, ext=".png"):
    ''' Iterator for the images in path with ext extension '''
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

def is_gray(img):
    ''' Verifies if img is a 2D array '''
    return img.ndim == 2

def grayscale(img):
    ''' Returns the grayscale array representation of the RGB image img '''
    assert(not is_gray(img))
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

def normalize(img, min_v, max_v):
    ''' Returns a normalized array representation of img with min=min_v and max=max_v '''
    norm_img = np.zeros(np.shape(img)) # dst output array
    norm_img = cv2.normalize(img, norm_img, min_v, max_v, cv2.NORM_MINMAX)
    return norm_img

def clamp(v, min_v=0, max_v=255):
    ''' Constrains v to lie between min_v and max_v '''
    return min_v if (v < min_v) else max_v if (v > max_v) else v

###############################################################################

if __name__ == "__main__":
    print(f"cv2 version: {cv2.__version__}")
    print(f"numpy version: {np.__version__}")