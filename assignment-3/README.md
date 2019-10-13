> pip3 install numpy matplotlib opencv-python
```
usage: main.py [-h] [--plain] 
               [--image IMAGE]
               [--input_folder INPUT_FOLDER]
               [--output_folder OUTPUT_FOLDER]
               [--display_images]
               [--save_region_properties]

Some measurements and transformations of objects present in digital images.

optional arguments:
  -h, --help            show this help message and exit
  --plain               Decrease verbosity
  --image IMAGE, -img IMAGE
                        Image file name ('.png' extension is optional), which
                        must be inside the input folder
  --input_folder INPUT_FOLDER, -i INPUT_FOLDER
                        Input image(s) folder path (defaults to i\)
  --output_folder OUTPUT_FOLDER, -o OUTPUT_FOLDER
                        Output image(s) folder path (defaults to o\)
  --display_images, -d  Display image transformations, besides saving them
  --save_region_properties, -r
                        Saves region properties to region_properties.txt
                        (appends them if the file already exists), besides
                        printing them
```