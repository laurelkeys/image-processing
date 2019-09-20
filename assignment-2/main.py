import sys
import os.path
import argparse
from functools import partial
from thresholding import *
from utils import *

def get_parser():
    parser = argparse.ArgumentParser(description="Thresholding methods for binarizing grayscale images.")
    parser.add_argument("--plain", action="store_true", 
                        help="Decrease verbosity")
    parser.add_argument("--image", "-img", type=str, 
                        help=f"Image file name ('{DEFAULT_EXT}' extension is optional), which must be inside the input folder")
    parser.add_argument("--input_folder", "-i", type=str, default=INPUT_FOLDER, 
                        help="Input image(s) folder path" + f" (defaults to {os.path.join(INPUT_FOLDER, '')})")
    parser.add_argument("--output_folder", "-o", type=str, default=OUTPUT_FOLDER, 
                        help="Output image(s) folder path" + f" (defaults to {os.path.join(OUTPUT_FOLDER, '')})")
    parser.add_argument("--threshold_value", "-t", type=int, default=128, choices=range(0, 256), metavar="[0..255]", 
                        help="Threshold value")
    parser.add_argument("--window_size", "-s", type=int, default=3, choices=[1,3,5,7], 
                        help="Pixel neighborhood window size (for the methods to which it applies)")
    parser.add_argument("--method_index", "-m", type=int, choices=range(0, len(Method.list_all)), 
                        help="Index of the thresholding method to be used, where: " + 
                             ', '.join([f"{i}={x}" for i, x in enumerate(Method.list_all)]))
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

def prompt_yes_no(question, default=None):
    if default is None: prompt = " (y/n) "
    elif default:       prompt = " (Y/n) "
    else:               prompt = " (y/N) "
    reply = str(input(question + prompt)).lower().strip()
    if reply[:1] == 'y': return True
    if reply[:1] == 'n': return False
    return default if default != None else prompt_yes_no(question)

###############################################################################

def check_paths_exist_or_die(image_fnames, folder):
    for image_fname in image_fnames:
        if not os.path.isfile(os.path.join(folder, image_fname)):
            sys.exit(f"\nERROR: invalid image path or extension '{os.path.join(folder, image_fname)}'")

def ready_image_fnames():
    v_print(f"Input folder: {os.path.join(args.input_folder, '')}")
    v_print(f"Output folder: {os.path.join(args.output_folder, '')}")
    create_folder(args.output_folder)

    if args.image == None:
        img_fnames = [ifn for ifn in image_fnames(folder=args.input_folder)]
    else:
        if not args.image.endswith(DEFAULT_EXT):
            args.image += DEFAULT_EXT
        img_fnames = [args.image]
    
    check_paths_exist_or_die(img_fnames, folder=args.input_folder)
    return img_fnames

###############################################################################

def apply_and_save(img, transformation, save_fname):
    ''' Applies transformation to a copy of img and saves it '''
    transformed_img = transformation(img)
    save(transformed_img, save_fname, folder=args.output_folder)
    v_print(f"Saved '{save_fname}'")

def do_global_threshold(images):
    v_print("Applying global threshold...")
    for img_title, img in images.items():
        apply_and_save(img, transformation=partial(global_threshold, threshold=args.threshold_value), 
                       save_fname=f"{img_title}_global_{args.threshold_value}")
    v_print("")

def do_local_threshold(images, methods):
    v_print("Applying local threshold...")
    count = 1
    max_count = len(methods)
    for method in methods:
        v_print(f"({count}/{max_count}) {method}")
        for img_title, img in images.items():
            apply_and_save(img, transformation=partial(local_threshold, method=method, window_size=args.window_size), 
                           save_fname=f"{img_title}_{method}_{args.window_size}x{args.window_size}")
            count += 1
    v_print("")

###############################################################################

if __name__ == '__main__':

    parse_args()
    if args.image == None:
        run_all = prompt_yes_no(default=True, 
                                question=f"Do you want to threhsold all images inside '{os.path.join(args.input_folder, '')}'?")
        if not run_all:
            sys.exit(f"\nExitting... please use the -img argument to threshold only a specific image (or -h for help)")

    methods = Method.list_all if args.method_index == None else [Method.list_all[args.method_index]]
    v_print(f"Methods: {methods}\n")

    # get the filenames of the test images, creating the output folder if it doesn't exist
    img_fnames = ready_image_fnames() # (kills the program if the images don't exist)

    # load input image(s)
    images = {}
    v_print("Loading images...")
    for img_fname in img_fnames:
        img_title, _ = split_name_ext(img_fname)
        images[img_title] = load_gray(img_fname, folder=args.input_folder)
        v_print(f"'{img_fname}' loaded")
    v_print("")

    # global threhsolding
    # do_global_threshold(images)

    # local threhsolding
    do_local_threshold(images, methods)

    