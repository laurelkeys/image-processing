import sys
import os.path
import argparse
from utils import *

def get_parser():
    parser = argparse.ArgumentParser(description="Steganography algorithm to recover a text message hidden in an image.")
    parser.add_argument("--image", "-i", type=str, required=True, 
                        help="File name (with path) of the image in which the message is embedded")
    parser.add_argument("--message", "-m", type=str, required=True, 
                        help="Text file name (with path) for which to save the decoded message")
    parser.add_argument("--bit_plane", "-b", type=int, choices=range(0, 8), default=0, 
                        help="Bit plane in which the message is hidden (default: %(default)d)")
    parser.add_argument("--verbose", "-v", action="store_true", 
                        help="Increase verbosity")
    parser.add_argument("--very_verbose", "-vv", action="store_true", 
                        help="Increase verbosity even more (only recommended for small input images)")
    return parser

def validate_file_paths(args):
    if not os.path.isfile(args.image):
        sys.exit(f"\nERROR: Invalid image file path '{args.image}'")

###############################################################################

if __name__ == '__main__':
    args = get_parser().parse_args()
    if args.very_verbose: args.verbose = True
    
    validate_file_paths(args)
    print(f"Image: {args.image}")
    print(f"Message: {args.message}")

    bgr_img = load(full_path=args.image)

    # 0..000..b == (0..0b0..0 >> bit_plane) == ((?..?b?..? & 0..010..0) >> bit_plane)
	# obs.: 0..010..0 == (0..000..1 << bit_plane)
    mask = 1 << args.bit_plane
    __img = np.bitwise_and(bgr_img, mask)
    __img >>= args.bit_plane

    # NOTE OpenCV uses BGR order
    b_message = __img[..., 0].ravel()
    g_message = __img[..., 1].ravel()
    r_message = __img[..., 2].ravel()
    
    # retrieve message from bit_plane
    message_bits = np.dstack((r_message, g_message, b_message)).ravel()
    max_bits = message_bits.size
    while max_bits % 8 != 0:
        max_bits -= 1 # we can only store whole byte words
    message = ''.join([chr(byte) for byte in np.packbits(message_bits[:max_bits])])

    # FIXME
    # look for the '\0' marking the end of the message
    end = message.find('\0')
    if end != -1:
        message = message[:end]
    if args.very_verbose:
        print(" |> '" + to_bit_str(message_bits) + "'")
    if args.verbose:
        print(" |> '" + message  + "'")

    if args.very_verbose:
        print()
        print("Image:")
        print_binary_repr(bgr_img)
        print(f"Message hidden on bit plane {args.bit_plane}:")
        print(__img)
        print("R channel:", r_message)
        print("G channel:", g_message)
        print("B channel:", b_message)
    
    # write decoded message to file
    create_folder(args.message)
    with open(args.message, 'w+') as txt_file:
        txt_file.write(message)
    print(f"\nDecoded message saved to '{args.message}'")