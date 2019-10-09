import ast
import sys
import os.path
import argparse
from utils import *
from transformations import *

def get_parser():
    parser = argparse.ArgumentParser(description="Some measurements and transformations of objects present in digital images.")
    parser.add_argument("--plain", action="store_true", 
                        help="Decrease verbosity")
    parser.add_argument("--image", "-img", type=str, 
                        help=f"Image file name ('{DEFAULT_EXT}' extension is optional), which must be inside the input folder")
    parser.add_argument("--input_folder", "-i", type=str, default=INPUT_FOLDER, 
                        help="Input image(s) folder path" + f" (defaults to {os.path.join(INPUT_FOLDER, '')})")
    parser.add_argument("--output_folder", "-o", type=str, default=OUTPUT_FOLDER, 
                        help="Output image(s) folder path" + f" (defaults to {os.path.join(OUTPUT_FOLDER, '')})")
    parser.add_argument("--show", "-s", action="store_true", 
                        help="Display image transformations, besides saving them")
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

def do_monochrome(images):
    v_print("Transforming color...")
    count = 1
    max_count = len(images.items())
    for img_title, img in images.items():
        v_print(f"({count}/{max_count})")
        # FIXME should we convert to binary or grayscale?
        apply_and_save(img, transformation=color_to_black, save_fname=f"{img_title}_mono")
        apply_and_save(img, transformation=y_linear, save_fname=f"{img_title}_ylinear")
        apply_and_save(img, transformation=y_srgb, save_fname=f"{img_title}_ysrgb")
        count += 1
    v_print("")

def do_contours(images):
    v_print("Drawing contours...")
    count = 1
    max_count = len(images.items())
    for img_title, img in images.items():
        v_print(f"({count}/{max_count})")
        apply_and_save(img, transformation=contours, save_fname=f"{img_title}_contours")
        count += 1
    v_print("")

def do_measurements(images):
    v_print("Taking measurements...")
    count = 1
    max_count = len(images.items())
    for img_title, img in images.items():
        v_print(f"({count}/{max_count})")
        numbered_img, region_properties = number_regions(img)
        
        print_region_properties(region_properties)
        
        save_fname = f"{img_title}_regions"
        save(numbered_img, save_fname, folder=args.output_folder)
        v_print(f"Saved '{save_fname}'")
        v_print("")
        
        count += 1
    v_print("")

###############################################################################

if __name__ == '__main__':
    parse_args()
    if args.image == None:
        run_all = prompt_yes_no(default=True, 
                                question=f"Do you want to use all images inside '{os.path.join(args.input_folder, '')}'?")
        if not run_all:
            sys.exit(f"\nExitting... please use the -img argument to use only a specific image (or -h for help)")

    # get the filenames of the test images, creating the output folder if it doesn't exist
    img_fnames = ready_image_fnames() # (kills the program if the images don't exist)

    # load input image(s)
    images = {}
    v_print("Loading images...")
    for img_fname in img_fnames:
        img_title, _ = split_name_ext(img_fname)
        images[img_title] = load(img_fname, folder=args.input_folder)
        v_print(f"'{img_fname}' loaded")
    v_print("")
    
    # transformations
    # do_monochrome(images)
    # do_contours(images)

    # measurements
    do_measurements(images)