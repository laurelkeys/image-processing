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
    v_print(f"Techniques: {techniques}\n")

    if args.image == None:
        img_fnames = [ifn for ifn in image_fnames(args.input_folder)]
    else:
        if not args.image.endswith(".png"):
            args.image += ".png"
        img_fnames = [args.image]

    # load input image(s)
    images = {}
    gray_images = {}
    v_print("Loading images...")
    for img_fname in img_fnames:
        img_title, _ = split_name_ext(img_fname)
        images[img_title] = load(img_fname, args.input_folder)
        gray_images[img_title] = grayscale(images[img_title])
        v_print(f"'{img_fname}' loaded")
    v_print("")

    # threshold
    for img_title, img in images.items():
        __img = threshold(img)
        save_fname = f"{img_title} (threshold)"
        save(__img, save_fname)
        v_print(f"Saved '{save_fname}'")

        gray_img = gray_images[img_title]
        __gray_img = threshold(gray_img)
        save_fname = f"{img_title}_grayscale (threshold)"
        save(__gray_img, save_fname)
        v_print(f"Saved '{save_fname}'")
    v_print("")

    # dithering
    # for technique in techniques:
    #     if args.verbose: print(f"\nTechnique: {technique}")
    #     for img_title, img in images.items():
    #         if args.verbose: print(f"  Dithering '{img_title}.png'...")

    #         # grayscale
    #         dithered_img = dither_gray(grayscale(img), technique) # TODO save the grayscaled image
    #         save_fname = f"[ordered] {img_title}_grayscale ({technique})"
    #         save(dithered_img, save_fname)
    #         if args.verbose: print(f"  ..saved grayscale image to: '{join(OUTPUT_FOLDER, save_fname)}.png'")

    #         # colored (RGB)
    #         dithered_img = dither_rgb(img, technique)
    #         save_fname = f"[ordered] {img_title} ({technique})"
    #         save(dithered_img, save_fname)
    #         if args.verbose: print(f"  ..saved colored image to: '{join(OUTPUT_FOLDER, save_fname)}.png'")

# TODO thresholding
# TODO alternating order
# TODO colored dithering