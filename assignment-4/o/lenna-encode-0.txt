import sys
import string
import os.path
import argparse
from utils import *

def get_parser():
    parser = argparse.ArgumentParser(description="Steganography algorithm to hide a text message in an image.")
    parser.add_argument("input_image", type=str, 
                        help="Input image file name (with path), in which the message will be embedded")
    parser.add_argument("message", type=str, 
                        help="Text file name (with path), containing the message to hide")
    parser.add_argument("bit_plane", type=int, choices=range(0, 8), 
                        help="Bit plane in which to hide the message")
    parser.add_argument("output_image", type=str, 
                        help="Output image file name (with path)")
    parser.add_argument("--verbose", "-v", action="store_true", 
                        help="Increase verbosity")
    parser.add_argument("--very_verbose", "-vv", action="store_true", 
                        help="Increase verbosity even more (only recommended for small messages)")
    parser.add_argument("--very_very_verbose", "-vvv", action="store_true", 
                        help="Increase verbosity even more (only recommended for small input images)")
    return parser

def validate_file_paths(args):
    if not os.path.isfile(args.input_image):
        sys.exit(f"\nERROR: Invalid image file path '{args.input_image}'")
    if not os.path.isfile(args.message):
        sys.exit(f"\nERROR: Invalid message file path '{args.message}'")
    create_folder(args.output_image) # creates the output folder if it doesn't exist

###############################################################################

def main(args):
    if args.very_very_verbose: args.very_verbose = True
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
    with open(args.message, 'r', encoding="utf-8") as txt_file:
        txt_lines = txt_file.readlines()
        try:
            lines = [line.encode('ascii') for line in txt_lines]
        except UnicodeEncodeError:
            print("WARNING: The message contains non-ASCII characters, which will be ignored")
            lines = [ascii_line.encode('ascii') 
                     for line in txt_lines
                     for ascii_line in ''.join([c for c in line if c in string.printable])]

    message = b''.join(lines)
    if args.very_verbose:
        print(" |> '" + message.decode('ascii') + "'")

    if len(message) < max_bytes:
        message += b'\0' # mark the end of the message
    message_bits = np.unpackbits(np.frombuffer(message, dtype=np.uint8))
    
    if message_bits.size > max_bits:
        message_bits = message_bits[:max_bits]
        print("\nThe message is too big to fit in the image, only its start will be hidden")
        if args.very_verbose:            
            print(" |> '" + ''.join([chr(byte) for byte in np.packbits(message_bits)]) + "'")
    
    if args.very_very_verbose:
        print(" |> '" + to_bit_str(message_bits) + "'")
    if args.verbose:
        print(f"\nThis image can hide up to {max_bits} bits (i.e. {max_bytes} ASCII characters)\n")

    r_message = message_bits[0::3]
    g_message = message_bits[1::3]
    b_message = message_bits[2::3]
    r_length, g_length, b_length = r_message.size, g_message.size, b_message.size
    if args.very_very_verbose:
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

    if args.very_very_verbose:
        # use [..., ::-1] to display RGB instead of BGR
        print("\nOriginal image:")
        print_binary_repr(bgr_img[..., ::-1])
        print("\nImage with message embedded:")
        print_binary_repr(__img[..., ::-1])
        print()
    
    save(__img, full_path=args.output_image)
    if not args.verbose: print()
    print(f"Image saved to '{args.output_image}'")


if __name__ == '__main__':
    args = get_parser().parse_args()
    main(args)

# >>> chr(10)
# '\n'
# >>> chr(32)
# ' '
# https://www.rapidtables.com/convert/number/binary-to-ascii.html