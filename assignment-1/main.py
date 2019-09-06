import os.path
import argparse
from dithering import *
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
        def __v_print(*a, **kwa):
            print(*a, **kwa)
    else:
        __v_print = lambda *a, **kwa: None
    
    global v_print
    v_print = __v_print

###############################################################################

def ready_image_fnames():
    v_print(f"Input folder: {os.path.join(args.input_folder, '')}")
    v_print(f"Output folder: {os.path.join(args.output_folder, '')}")
    create_folder(args.output_folder)

    if args.image == None:
        return [ifn for ifn in image_fnames(folder=args.input_folder)]
    else:
        if not args.image.endswith(".png"):
            args.image += ".png"
        return [args.image]

###############################################################################

def apply_and_save(img, transformation, save_fname):
    ''' Applies transformation to a copy of img and saves it '''
    transformed_img = transformation(img)
    save(transformed_img, save_fname, folder=args.output_folder)
    v_print(f"Saved '{save_fname}'")

def do_threshold(images):
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

def do_dither(images, techniques):
    v_print("Dithering...")
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

def do_zigzag_dither(images, techniques):
    v_print("Dithering in zigzag...")
    count = 1
    max_count = len(techniques)
    for technique in techniques:
        v_print(f"({count}/{max_count})")
        for img_title, img in images.items():
            apply_and_save(img, transformation=lambda i: zigzag_dither(i, technique), 
                           save_fname=f"{img_title}_{technique}_zigzag")
            gray_img = gray_images[img_title]
            apply_and_save(gray_img, transformation=lambda i: zigzag_dither(i, technique), 
                           save_fname=f"gray_{img_title}_{technique}_zigzag")
        count += 1
    v_print("")

###############################################################################

if __name__ == '__main__':
    parse_args()

    techniques = Technique.list_all if args.technique_index == None else [Technique.list_all[args.technique_index]]
    v_print(f"Techniques: {techniques}\n")

    # create the output folder if it doesn't exist
    # and get the filenames of the test images
    img_fnames = ready_image_fnames()

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
    do_threshold(images)

    # dithering
    do_dither(images, techniques)

    # zigzag dithering
    do_zigzag_dither(images, techniques)
