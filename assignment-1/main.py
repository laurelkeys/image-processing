import sys
import os.path
import argparse
from dithering import *
from image_processing_utils import *

def get_parser():
    parser = argparse.ArgumentParser(description="Error diffusion dithering techniques for creating halftone images.")
    parser.add_argument("--plain", action="store_true", 
                        help="Decrease verbosity")
    parser.add_argument("--image", "-img", type=str, 
                        help="Image file name ('.png' extension is optional), which must be inside the input folder")
    parser.add_argument("--input_folder", "-i", type=str, default=INPUT_FOLDER, 
                        help="Input image(s) folder path" + f" (defaults to {os.path.join(INPUT_FOLDER, '')})")
    parser.add_argument("--output_folder", "-o", type=str, default=OUTPUT_FOLDER, 
                        help="Output image(s) folder path" + f" (defaults to {os.path.join(OUTPUT_FOLDER, '')})")
    parser.add_argument("--technique_index", "-t", type=int, choices=range(0, len(Technique.list_all)), 
                        help="Index of the dithering technique to be used, where: " + 
                             ', '.join([f"{i}={x}" for i, x in enumerate(Technique.list_all)]))
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
            sys.exit(f"\nERROR: invalid image path '{os.path.join(folder, image_fname)}'")

def ready_image_fnames():
    v_print(f"Input folder: {os.path.join(args.input_folder, '')}")
    v_print(f"Output folder: {os.path.join(args.output_folder, '')}")
    create_folder(args.output_folder)

    if args.image == None:
        img_fnames = [ifn for ifn in image_fnames(folder=args.input_folder)]
    else:
        if not args.image.endswith(".png"):
            args.image += ".png"
        img_fnames = [args.image]
    
    check_paths_exist_or_die(img_fnames, folder=args.input_folder)
    return img_fnames

###############################################################################

def apply_and_save(img, transformation, save_fname):
    ''' Applies transformation to a copy of img and saves it '''
    transformed_img = transformation(img)
    save(transformed_img, save_fname, folder=args.output_folder)
    v_print(f"Saved '{save_fname}'")

def do_threshold(images, gray_images):
    v_print("Thresholding...")
    count = 1
    max_count = len(images.items())
    for img_title, img in images.items():
        v_print(f"({count}/{max_count})")
        apply_and_save(img, transformation=threshold, 
                       save_fname=f"{img_title}_threshold")
        gray_img = gray_images[img_title]
        apply_and_save(gray_img, transformation=threshold, 
                       save_fname=f"gray_{img_title}_threshold")
        count += 1
    v_print("")

def do_dither(images, gray_images, techniques):
    v_print("Dithering (raster)...")
    count = 1
    max_count = len(techniques)
    for technique in techniques:
        v_print(f"({count}/{max_count})")
        for img_title, img in images.items():
            apply_and_save(img, transformation=lambda i: dither(i, technique), 
                           save_fname=f"{img_title}_{technique}")
            gray_img = gray_images[img_title]
            apply_and_save(gray_img, transformation=lambda i: dither(i, technique), 
                           save_fname=f"gray_{img_title}_{technique}")
        count += 1
    v_print("")

def do_serpentine_dither(images, gray_images, techniques):
    v_print("Dithering (serpentine)...")
    count = 1
    max_count = len(techniques)
    for technique in techniques:
        v_print(f"({count}/{max_count})")
        for img_title, img in images.items():
            apply_and_save(img, transformation=lambda i: serpentine_dither(i, technique), 
                           save_fname=f"{img_title}_{technique}_serpentine")
            gray_img = gray_images[img_title]
            apply_and_save(gray_img, transformation=lambda i: serpentine_dither(i, technique), 
                           save_fname=f"gray_{img_title}_{technique}_serpentine")
        count += 1
    v_print("")

###############################################################################

if __name__ == '__main__':

    parse_args()
    if args.image == None:
        run_all = prompt_yes_no(f"Do you want to dither all images inside '{args.input_folder}'?", default=True)
        if not run_all:
            sys.exit(f"\nExitting... please use the -img argument to dither only a specific image (or -h for help)")

    techniques = Technique.list_all if args.technique_index == None else [Technique.list_all[args.technique_index]]
    v_print(f"Techniques: {techniques}\n")

    # get the filenames of the test images, creating the output folder if it doesn't exist
    img_fnames = ready_image_fnames() # (kills the program if the images don't exist)

    # load input image(s)
    images = {}
    gray_images = {}
    v_print("Loading images...")
    for img_fname in img_fnames:
        img_title, _ = split_name_ext(img_fname)
        images[img_title] = load(img_fname, folder=args.input_folder)
        gray_images[img_title] = grayscale(images[img_title])
        v_print(f"'{img_fname}' loaded")
    v_print("")

    # thresholding
    do_threshold(images, gray_images)

    # dithering
    do_dither(images, gray_images, techniques)

    # serpentine dithering
    do_serpentine_dither(images, gray_images, techniques)