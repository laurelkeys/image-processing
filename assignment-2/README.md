> pip3 install numpy matplotlib opencv-python
```
usage: main.py [-h] [--plain]
               [--image IMAGE]
               [--input_folder INPUT_FOLDER]
               [--output_folder OUTPUT_FOLDER]
               [--threshold_value [0..255]]
               [--window_size {1,3,5,7,9,11,13,15,17,19,21,23,25}]
               [--method_index {0,1,2,3,4,5,6,7}]
               [--custom_constants CUSTOM_CONSTANTS]
               [--save_to_png]
               [--shift_constant [-255..255]]

Thresholding methods for binarizing grayscale images.

optional arguments:
  -h, --help            show this help message and exit
  --plain               Decrease verbosity
  --image IMAGE, -img IMAGE
                        Image file name ('.pgm' extension is optional), which
                        must be inside the input folder
  --input_folder INPUT_FOLDER, -i INPUT_FOLDER
                        Input image(s) folder path (defaults to i\)
  --output_folder OUTPUT_FOLDER, -o OUTPUT_FOLDER
                        Output image(s) folder path (defaults to o\)
  --threshold_value [0..255], -t [0..255]
                        Threshold value for the global method
  --window_size {1,3,5,7,9,11,13,15,17,19,21,23,25}, -s {1,3,5,7,9,11,13,15,17,19,21,23,25}
                        Pixel neighborhood window size used in local
                        thresholding methods
  --method_index {0,1,2,3,4,5,6,7}, -m {0,1,2,3,4,5,6,7}
                        Index of the thresholding method to be used, where:
                        0=global, 1=bernsen, 2=niblack, 3=sauvola_pietaksinen,
                        4=phansalskar_more_sabale, 5=contrast, 6=mean,
                        7=median
  --custom_constants CUSTOM_CONSTANTS, -cc CUSTOM_CONSTANTS
                        File with a dictionary defining constants for niblack
                        (k), sauvola_pietaksinen (k, R), and
                        phansalkar_more_sabale (k, R, p, q)
  --save_to_png, -png   Stores the output images as .png instead of .pgm
  --shift_constant [-255..255], -C [-255..255]
                        Value added to the pixel intensity before comparing it
                        to the local threshold (defaults to 0)
```