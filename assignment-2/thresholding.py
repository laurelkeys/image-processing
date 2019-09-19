import numpy as np

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
    list_all = [GLOBAL, BERNSEN, NIBLACK, SAUVOLA_PIETAKSINEN, PHANSALSKAR_MORE_SABALE, CONTRAST, MEAN, MEDIAN]
    function = { } # TODO map method constants to their implementation once they're done

###############################################################################

def global_threshold(img, threshold=128):
    ''' Returns a new binary image based on the given threshold '''
    __img = img.copy()
    __img = np.where(__img < threshold, 0, 255)
    return __img

def local_threshold(img, method, window_size=3, threshold=128):
    ''' Returns a new binary image by applying the given method '''
    __img = img.copy()
    __img = np.where(__img < threshold, 0, 255)
    return __img

###############################################################################

if __name__ == "__main__":
    pass