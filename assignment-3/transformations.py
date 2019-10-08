import cv2
import numpy as np

from utils import BGR_RED, WHITE

def contours(img, objects_are_black=True, draw_bbox=False):
    ''' Returns an image displaying the contours (edges) of objects present in img '''
    __img = color_to_black(img).astype('uint8')
    contours, _ = cv2.findContours(__img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return cv2.drawContours(np.full(img.shape, WHITE), contours if draw_bbox else contours[1:], -1, BGR_RED)

def color_to_black(img):
    ''' Converts every non-white pixel of a colored image to black, returning a binary image '''
    __img = img.astype('float') / 255
    __img = np.sum(__img, axis=-1) / 3 # sum RGB channels into one
    __img = np.where(np.isclose(__img, 1), 1, 0) # turn what isn't white (1) into black (0)
    return 255 * __img

def y_linear(img, bgr=True):
    __img = img.astype('float') / 255
    R = 2 if bgr else 0
    G = 1
    B = 2 - R
    return 255 * (0.2126 * __img[:, :, R] + 0.7152 * __img[:, :, G] + 0.0722 * __img[:, :, B])

def y_srgb(img, bgr=True):
    __img = y_linear(img, bgr) / 255
    return 255 * np.where(__img <= 0.0031308, 12.92 * __img, 1.055 * np.power(__img, 1/2.4) - 0.055)
    