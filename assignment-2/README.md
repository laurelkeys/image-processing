> pip3 install numpy matplotlib opencv-python
```
usage: main.py [-h] [--plain]
               [--image IMAGE]
               [--input_folder INPUT_FOLDER]
               [--output_folder OUTPUT_FOLDER]
               [--threshold [0..255]]
               [--neighborhood_size {1,3,5,7}]
               [--method_index {0,1,2,3,4,5,6,7}]

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
  --threshold [0..255], -t [0..255]
                        Threshold value
  --neighborhood_size {1,3,5,7}, -s {1,3,5,7}
                        Pixel neighborhood size (for the methods to which it
                        applies)
  --method_index {0,1,2,3,4,5,6,7}, -m {0,1,2,3,4,5,6,7}
                        Index of the thresholding method to be used, where:
                        0=global, 1=bernsen, 2=niblack, 3=sauvola_pietaksinen,
                        4=phansalskar_more_sabale, 5=contrast, 6=mean,
                        7=median
```