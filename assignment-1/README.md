```
usage: main.py [-h] [--plain] [--image IMAGE] [--input_folder INPUT_FOLDER]
               [--output_folder OUTPUT_FOLDER]
               [--technique_index {0,1,2,3,4,5}]

Error diffusion dithering techniques for creating halftone images.

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
  --technique_index {0,1,2,3,4,5}, -t {0,1,2,3,4,5}
                        Index of the dithering technique to be used, where:
                        0=floyd_steinberg, 1=stevenson_arce, 2=burkes,
                        3=sierra, 4=stucki, 5=jarvis_judice_ninke
```