import sys
import os.path
import argparse
import numpy as np
from utils import *

def get_parser():
    parser = argparse.ArgumentParser(description="Steganography algorithm to hide a text message in an image.")
    parser.add_argument("--input_image", "-i", type=str, required=True, 
                        help="Input image file name (with path), in which the message will be embedded")
    parser.add_argument("--message", "-m", type=str, required=True, 
                        help="Text file name (with path), containing the message to hide")
    parser.add_argument("--output_image", "-o", type=str, 
                        help="Output image file name (with path)")
    parser.add_argument("--output_folder", "-of", type=str, default=os.path.join(OUTPUT_FOLDER, ''), 
                        help="Ignored if [output_image] is passed (default: %(default)s)")
    parser.add_argument("--bit_plane", "-b", type=int, choices=range(0, 8), default=0, 
                        help="Bit plane in which to hide the message (default: %(default)d)")
    parser.add_argument("--verbose", "-v", action="store_true", 
                        help="Increase verbosity")
    parser.add_argument("--very_verbose", "-vv", action="store_true", 
                        help="Increase verbosity even more (only recommended for small input images)")
    return parser

def validate_file_paths(args):
    if not os.path.isfile(args.input_image):
        sys.exit(f"\nERROR: Invalid image file path '{args.input_image}'")
    if not os.path.isfile(args.message):
        sys.exit(f"\nERROR: Invalid message file path '{args.message}'")
    if args.output_image is None:
        root, image_fname, ext = split_root_name_ext(args.input_image)
        _, message_fname, _ = split_root_name_ext(args.message)
        if args.output_folder is not None:
            root = args.output_folder
        args.output_image = os.path.join(root, f"{image_fname}-{message_fname}-b{args.bit_plane}{ext}")
    create_folder(args.output_image) # creates the output folder if it doesn't exist

###############################################################################

if __name__ == '__main__':
    args = get_parser().parse_args()
    if args.very_verbose: args.verbose = True
    
    validate_file_paths(args)
    print(f"Input: {args.input_image}")
    print(f"Output: {args.output_image}")
    print(f"Message: {args.message}")

    bgr_img = load(full_path=args.input_image)

    # calculate the max number of bits we can hide on the image
    height, width, depth = bgr_img.shape
    max_bytes = height * width * depth // 8
    max_bits = max_bytes * 8 # we can only store whole byte words

    # read message lines into an array
    with open(args.message, 'r') as txt_file:
        lines = [line.encode('ascii') for line in txt_file.readlines()]

    message = b''.join(lines)
    if args.verbose:
        print(" |> '" + message.decode('ascii') + "'")

    if len(message) < max_bytes:
        message += b'\0' # mark the end of the message
    message_bytes = to_byte_array(message)
    message_bits = np.unpackbits(message_bytes)
    
    if message_bits.size > max_bits:
        message_bits = message_bits[:max_bits]
        if args.verbose:
            print("\nThe message is too big to fit in the image, only its start will be hidden:")
            print(" |> '" + ''.join([chr(byte) for byte in np.packbits(message_bits)]) + "'")
    
    if args.very_verbose:
        print(" |> '" + to_bit_str(message_bits) + "'")
    if args.verbose:
        print(f"\nThis image can hide up to {max_bits} bits (i.e. {max_bytes} ASCII characters)\n")

    r_message = message_bits[0::3]
    g_message = message_bits[1::3]
    b_message = message_bits[2::3]
    r_length, g_length, b_length = r_message.size, g_message.size, b_message.size
    if args.very_verbose:
        print(f"R channel ({r_length} bits):\n", r_message)
        print(f"G channel ({g_length} bits):\n", g_message)
        print(f"B channel ({b_length} bits):\n", b_message, '\n')

    # NOTE OpenCV uses BGR order
    r = bgr_img[..., 2].ravel()
    g = bgr_img[..., 1].ravel()
    b = bgr_img[..., 0].ravel()

    if args.verbose:
        print(f"Hiding message on bit plane {args.bit_plane}..")
    # ?..?b?..? == (?..?0?..? | 0..0b0..0) == ((?..???..? & 1..101..1) | 0..0b0..0)
	#     ^- bit_plane
	# obs.: 1..101..1 == ~0..010..0 == ~(0..000..1 << bit_plane)
	#       0..0b0..0 == (0..000..b << bit_plane), where b is either 0 or 1
    #       |<--8-->|, b can be in any position (i.e.: 0 <= bit_plane < 8)
    mask = 1 << args.bit_plane
    r[:r_length] = (r[:r_length] & ~mask) | (r_message << args.bit_plane)
    g[:g_length] = (g[:g_length] & ~mask) | (g_message << args.bit_plane)
    b[:b_length] = (b[:b_length] & ~mask) | (b_message << args.bit_plane)
    
    __img = np.dstack((b.reshape((height, width)), 
                       g.reshape((height, width)), 
                       r.reshape((height, width))))

    if args.very_verbose:
        # use [..., ::-1] to display RGB instead of BGR
        print("\nOriginal image:")
        print_binary_repr(bgr_img[..., ::-1])
        print("\nImage with message embedded:")
        print_binary_repr(__img[..., ::-1])
        print()
    
    save(__img, full_path=args.output_image)
    if not args.verbose: print()
    print(f"Image saved to '{args.output_image}'")

# >>> chr(10)
# '\n'
# >>> chr(32)
# ' '
# https://www.rapidtables.com/convert/number/binary-to-ascii.html