import cv2 # https://docs.opencv.org/4.1.0/
import numpy as np
import matplotlib.pyplot as plt

from glob import iglob
from os.path import basename, splitext, join

class Technique:
    FLOYD_STEINBERG = "floyd_steinberg"
    STEVENSON_ARCE = "stevenson_arce"
    BURKES = "burkes"
    SIERRA = "sierra"
    STUCKI = "stucki"
    JARVIS_JUDICE_NINKE = "jarvis_judice_ninke"
    list_all = [FLOYD_STEINBERG, STEVENSON_ARCE, BURKES, SIERRA, STUCKI, JARVIS_JUDICE_NINKE]

ERROR_DISTRIBUTION = {
    Technique.FLOYD_STEINBERG: [
        ( 1, 0, 7/16), 
        (-1, 1, 3/16), 
        ( 0, 1, 5/16), 
        ( 1, 1, 1/16)
    ],
    Technique.STEVENSON_ARCE: [
        ( 2, 0, 32/200), 
        (-3, 1, 12/200), 
        (-1, 1, 26/200), 
        ( 1, 1, 30/200), 
        ( 3, 1, 16/200), 
        (-2, 2, 12/200), 
        ( 0, 2, 26/200), 
        ( 2, 2, 12/200), 
        (-3, 3,  5/200), 
        (-1, 3, 12/200), 
        ( 1, 3, 12/200), 
        ( 3, 3,  5/200)
    ],
    Technique.BURKES: [
        ( 1, 0, 8/32), 
        ( 2, 0, 4/32), 
        (-2, 1, 2/32), 
        (-1, 1, 4/32), 
        ( 0, 1, 8/32), 
        ( 1, 1, 4/32), 
        ( 2, 1, 2/32)
    ],
    Technique.SIERRA: [
        ( 1, 0, 5/32), 
        ( 2, 0, 3/32), 
        (-2, 1, 2/32), 
        (-1, 1, 4/32), 
        ( 0, 1, 5/32), 
        ( 1, 1, 4/32), 
        ( 2, 1, 2/32), 
        (-1, 2, 2/32), 
        (-1, 2, 3/32), 
        ( 1, 2, 2/32)
    ],
    Technique.STUCKI: [
        ( 1, 0, 8/42), 
        ( 2, 0, 4/42), 
        (-2, 1, 2/42), 
        (-1, 1, 4/42), 
        ( 0, 1, 8/42), 
        ( 1, 1, 4/42), 
        ( 2, 1, 2/42), 
        (-2, 2, 1/42), 
        (-1, 2, 2/42), 
        ( 0, 2, 4/42), 
        ( 1, 2, 2/42), 
        ( 2, 2, 1/42)
    ],
    Technique.JARVIS_JUDICE_NINKE: [
        ( 1, 0, 7/48), 
        ( 2, 0, 5/48), 
        (-2, 1, 3/48), 
        (-1, 1, 5/48), 
        ( 0, 1, 7/48), 
        ( 1, 1, 5/48), 
        ( 2, 1, 3/48), 
        (-2, 2, 1/48), 
        (-1, 2, 3/48), 
        ( 0, 2, 5/48), 
        ( 1, 2, 3/48), 
        ( 2, 2, 1/48)
    ],
}