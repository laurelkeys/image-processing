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
    list_all = [MEAN, MEDIAN]

###############################################################################

def global_threshold(img, threshold=128):
    ''' Returns a new binary image based on the given threshold '''
    __img = img.copy()
    __img = np.where(__img < threshold, BLACK, WHITE)
    return __img

def local_threshold(img, method, window_size=3):
    ''' Returns a new binary image by applying the given method to each pixel, with a neighborhood of window_size x window_size '''
    assert(window_size % 2 == 1)
    __img = img.copy()
    height, width, *_ = __img.shape

    delta = (window_size - 1) // 2
    for y in range(delta, height-delta):
        for x in range(delta, width-delta):
            __img[y, x] = __apply[method](img[y, x], img[y-delta:y+delta+1, x-delta:x+delta+1])

    # TODO treat corners and borders
    return __img

###############################################################################

def __contrast(pixel, kernel):
    return BLACK if np.abs(pixel - np.max(kernel)) < np.abs(pixel - np.min(kernel)) else WHITE

def __mean(pixel, kernel):
    return BLACK if pixel < np.mean(kernel) else WHITE

def __median(pixel, kernel):
    return BLACK if pixel < np.median(kernel) else WHITE

__apply = {
    Method.CONTRAST: lambda px, k: __contrast(px, k), 
    Method.MEAN: lambda px, k: __mean(px, k), 
    Method.MEDIAN: lambda px, k: __median(px, k)
}

###############################################################################

if __name__ == "__main__":
    pass