import numpy as np

WHITE = 0
BLACK = 255

''' Implemented thresholding methods '''
class Method:
    GLOBAL = "global"
    BERNSEN = "bernsen"
    NIBLACK = "niblack"
    SAUVOLA_PIETAKSINEN = "sauvola_pietaksinen"
    PHANSALSKAR_MORE_SABALE = "phansalskar_more_sabale"
    CONTRAST = "contrast"
    MEAN = "mean"
    MEDIAN = "median"
    list_local = [BERNSEN, NIBLACK, SAUVOLA_PIETAKSINEN, PHANSALSKAR_MORE_SABALE, CONTRAST, MEAN, MEDIAN]
    list_all = [GLOBAL] + list_local

###############################################################################

def global_threshold(img, threshold=128):
    ''' Returns a new binary image based on the given threshold '''
    __img = img.copy()
    __img = np.where(__img < threshold, BLACK, WHITE)
    return __img

def local_threshold(img, method, window_size=3):
    ''' Returns a new binary image by applying the given method to each pixel, with a neighborhood of window_size x window_size '''
    assert(window_size % 2 == 1)
    assert(method in Method.list_local), f"The local method must be one of: {Method.list_local}"
    __img = img.copy()
    height, width, *_ = __img.shape

    delta = (window_size - 1) // 2
    for y in range(height):
        for x in range(width):
            neighborhood = img[max(0, y-delta) : min(y+delta+1, height), 
                               max(0, x-delta) : min(x+delta+1, width)]
            __img[y, x] = __apply_local[method](**{ "pixel_value": img[y, x], 
                                                    "kernel": neighborhood})

    return __img

###############################################################################

def __bernsen(pixel_value, kernel):
    threshold = (np.max(kernel).astype('float') + np.min(kernel).astype('float')) / 2
    return BLACK if pixel_value < threshold else WHITE

def __niblack(pixel_value, kernel, k=0.25):
    threshold = np.mean(kernel, dtype='float') + k * np.std(kernel, dtype='float')
    return BLACK if pixel_value < threshold else WHITE

def __sauvola_pietaksinen(pixel_value, kernel, k=0.25, R=128):
    threshold = np.mean(kernel, dtype='float') * (1 + k * (-1 + np.std(kernel, dtype='float') / R))
    return BLACK if pixel_value < threshold else WHITE

def __phansalskar_more_sabale(pixel_value, kernel, k=0.25, R=0.5, p=2, q=10):
    # assert(k != 0)
    mean = np.mean(kernel, dtype='float')
    threshold = mean * (1 + p * np.exp(-q * mean) + k * (-1 + np.std(kernel, dtype='float') / R))
    return BLACK if pixel_value < threshold else WHITE

def __contrast(pixel_value, kernel):
    # obs.: since min <= pixel_value <= max we don't need to use abs
    return BLACK if np.max(kernel) - pixel_value < pixel_value - np.min(kernel) else WHITE

def __mean(pixel_value, kernel):
    return BLACK if pixel_value < np.mean(kernel, dtype='float') else WHITE

def __median(pixel_value, kernel):
    return BLACK if pixel_value < np.median(kernel) else WHITE

__apply_local = {
    Method.BERNSEN: lambda **kwargs: __bernsen(**kwargs),
    Method.NIBLACK: lambda **kwargs: __niblack(**kwargs),
    Method.SAUVOLA_PIETAKSINEN: lambda **kwargs: __sauvola_pietaksinen(**kwargs),
    Method.PHANSALSKAR_MORE_SABALE: lambda **kwargs: __phansalskar_more_sabale(**kwargs),
    Method.CONTRAST: lambda **kwargs: __contrast(**kwargs),
    Method.MEAN: lambda **kwargs: __mean(**kwargs),
    Method.MEDIAN: lambda **kwargs: __median(**kwargs)
}

###############################################################################

if __name__ == "__main__":
    print(f"Method.list_all: {Method.list_all}")
    print(f"Method.list_local: {Method.list_local}")

    applicable_local_methods = __apply_local.keys()
    for method in Method.list_local:
        if method not in applicable_local_methods:
            print(f"__apply_local is missing method '{method}'")