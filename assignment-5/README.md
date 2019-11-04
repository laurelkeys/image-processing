> pip3 install numpy matplotlib opencv-python
```
usage: main.py [-h] [--plain]
               [--number_of_components NUMBER_OF_COMPONENTS]
               [--image IMAGE]
               [--input_folder INPUT_FOLDER]
               [--output_folder OUTPUT_FOLDER]

Image compression through PCA.

optional arguments:
  -h, --help            show this help message and exit
  --plain               Decrease verbosity
  --number_of_components NUMBER_OF_COMPONENTS, -k NUMBER_OF_COMPONENTS
                        Number of principal components to be used (defaults to 1)
  --image IMAGE, -img IMAGE
                        Image file name ('.png' extension is optional), which
                        must be inside the input folder
  --input_folder INPUT_FOLDER, -i INPUT_FOLDER
                        Input image(s) folder path (defaults to i\)
  --output_folder OUTPUT_FOLDER, -o OUTPUT_FOLDER
                        Output image(s) folder path (defaults to o\)
```