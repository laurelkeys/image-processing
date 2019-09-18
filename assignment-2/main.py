import sys
import os.path
import argparse

INPUT_FOLDER  = "i"
OUTPUT_FOLDER = "o"

def get_parser():
    parser = argparse.ArgumentParser(description="Thresholding methods for binarizing grayscale images. Converts PGM to PBM.")
    parser.add_argument("--plain", action="store_true", 
                        help="Decrease verbosity")
    parser.add_argument("--image", "-img", type=str, 
                        help="Image file name ('.pgm' extension is optional), which must be inside the input folder")
    parser.add_argument("--input_folder", "-i", type=str, default=INPUT_FOLDER, 
                        help="Input image(s) folder path" + f" (defaults to {os.path.join(INPUT_FOLDER, '')})")
    parser.add_argument("--output_folder", "-o", type=str, default=OUTPUT_FOLDER, 
                        help="Output image(s) folder path" + f" (defaults to {os.path.join(OUTPUT_FOLDER, '')})")
    parser.add_argument("--threshold", "-t", type=int, choices=range(0, 256), metavar="[0-255]", 
                        help="Threshold value")
    parser.add_argument("--neighborhood_size", "-s", type=int, choices=[1,3,5,7], 
                        help="Pixel neighborhood size (for the methods in which it applies)")
    # parser.add_argument("--method_index", "-m", type=int, choices=range(0, len(Method.list_all)), 
    #                     help="Index of the thresholding method to be used, where: " + 
    #                          ', '.join([f"{i}={x}" for i, x in enumerate(Method.list_all)]))
    return parser

args = None
v_print = None
def parse_args():
    parser = get_parser()
    global args
    args = parser.parse_args()

    if args.plain:
        __v_print = lambda *a, **kwa: None
    else:
        def __v_print(*a, **kwa):
            print(*a, **kwa)
    
    global v_print
    v_print = __v_print

###############################################################################

if __name__ == '__main__':

    parse_args()
    print(args)