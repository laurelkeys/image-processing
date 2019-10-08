import numpy as np

def color_to_black(img, normalized=False):
    ''' Converts every non-white pixel of a colored image to black, returning a binary image '''
    __img = img.astype('float')
    if not normalized:
        __img /= 255
    __img = np.sum(__img, axis=-1) / 3 # sum RGB channels into one
    __img = np.where(np.isclose(__img, 1), 1, 0) # turn what isn't white (1) into black (0)
    return __img if normalized else __img * 255

def y_linear(img, normalized=False, bgr=True):
    __img = img.astype('float')
    if not normalized:
        __img /= 255
    R = 2 if bgr else 0; G = 1; B = 2 - R
    __img = 0.2126 * __img[:, :, R] + 0.7152 * __img[:, :, G] + 0.0722 * __img[:, :, B]
    return __img if normalized else __img * 255

def y_srgb(img, normalized=False, bgr=True):
    __img = y_linear(img, normalized, bgr)
    if not normalized:
        __img /= 255
    __img = np.where(__img <= 0.0031308, 12.92 * __img, 1.055 * np.power(__img, 1/2.4) - 0.055)
    return __img if normalized else __img * 255
    