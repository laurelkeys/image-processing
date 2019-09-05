import os.path
import argparse
from dithering import Technique
from image_processing_utils import *

def get_parser():
    parser = argparse.ArgumentParser(description='Implementations of dithering techniques for creating halftone images.')
    parser.add_argument('--image', '-img', type=str, 
                        help='The name of the input (original) image file')
    parser.add_argument('--input_folder', '-i', type=str, default=INPUT_FOLDER, 
                        help='The folder path for the input (original) image')
    parser.add_argument('--output_folder', '-o', type=str, default=OUTPUT_FOLDER, 
                        help='The output folder path for the dithered image')
    parser.add_argument('--technique_index', '-t', type=int, choices=range(0, len(Technique.list_all)), 
                        help='The index of the dithering technique to be used, where: ' + 
                             ', '.join([f"{i}={x}" for i, x in enumerate(Technique.list_all)]))
    parser.add_argument('--verbose', '-v', action="store_true", 
                        help='Increase verbosity')
    return parser

args = None
v_print = None
def parse_args():
    parser = get_parser()
    global args
    args = parser.parse_args()

    if args.verbose:
        def __v_print(*a):
            print(*a)
    else:
        __v_print = lambda *a: None
    
    global v_print
    v_print = __v_print

###############################################################################

if __name__ == '__main__':
    parse_args()

    v_print(f"Input folder: {os.path.join(args.input_folder, '')}")
    v_print(f"Output folder: {os.path.join(args.output_folder, '')}")

    techniques = Technique.list_all if args.technique_index == None else [Technique.list_all[args.technique_index]]
    v_print(f"Techniques: {techniques}")

    if args.image == None:
        img_fnames = image_fnames(args.input_folder)
    else:
        if not args.image.endswith(".png"):
            args.image += ".png"
        img_fnames = [os.path.join(args.input_folder, args.image)]

    # load input image(s)
    images = {}
    gray_images = {}
    for img_fname in img_fnames:
        img_title, _ = split_name_ext(img_fname)
        images[img_title] = load(img_fname, args.input_folder)
        gray_images[img_title] = grayscale(images[img_title])
