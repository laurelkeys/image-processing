import numpy as np

WHITE = 0
BLACK = 255

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
            __img[y, x] = method(img[y, x], img[y-delta:y+delta+1, x-delta:x+delta+1])

    # TODO treat corners and borders
    return __img

###############################################################################

def __contrast(pixel, kernel):
    return BLACK if np.abs(pixel - np.max(kernel)) < np.abs(pixel - np.min(kernel)) else WHITE

def __mean(pixel, kernel):
    return BLACK if pixel < np.mean(kernel) else WHITE

def __median(pixel, kernel):
    return BLACK if pixel < np.median(kernel) else WHITE

###############################################################################

''' Implemented thresholding methods '''
GLOBAL = "global"
BERNSEN = "bernsen"
NIBLACK = "niblack"
SAUVOLA_PIETAKSINEN = "sauvola_pietaksinen"
PHANSALSKAR_MORE_SABALE = "phansalskar_more_sabale"
CONTRAST = "contrast"
MEAN = "mean"
MEDIAN = "median"

METHOD_LIST = [CONTRAST, MEAN, MEDIAN]

function = { 
    CONTRAST: __contrast, 
    MEAN: __mean, 
    MEDIAN: __median
}

if __name__ == "__main__":
    M = np.array([[1,2,4],
                  [4,2,1],
                  [5,6,5]])
    M_min = np.min(M)
    M_max = np.max(M)
    M_mean = np.mean(M)
    M_median = np.median(M)
    print(M_min, M_max, M_mean, M_median)
    for px in [1,2,4,5,6]:
        print(px)
        for method, method_func in function.items():
            print(f"{method}: {method_func(px, M)}")
    pass