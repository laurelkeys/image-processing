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

def threshold(img, threshold=128):
    ''' Returns a new halftone image based on the given threshold '''
    __img = img.copy()
    __img = np.where(__img < 128, 0, 255)
    return __img

###############################################################################

if __name__ == "__main__":
    pass