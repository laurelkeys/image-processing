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
    if args.output_image == None:
        root, ext = os.path.splitext(args.input_image)
        message_fname, _ = os.path.splitext(os.path.basename(args.message))
        args.output_image = f"{root}-{message_fname}-b{args.bit_plane}{ext}"
    create_folder(args.output_image) # creates the output folder if it doesn't exist

###############################################################################

def to_byte_array(string):
    uint8_array = np.zeros(len(string), dtype='uint8')
    for i, char in enumerate(string):
        uint8_array[i] = char
    return uint8_array

def to_bit_str(bit_array):
    bit_str = ""
    bits_added = 0
    for bit in bit_array:
        if bits_added % 8 == 0:
            bit_str += ' '
        bit_str += str(bit)
        bits_added += 1
    return bit_str[1:] # removes the first ' '

def print_binary_repr(uint8_array):
    print(np.array([np.binary_repr(elem).zfill(8) for elem in uint8_array.ravel()])
            .reshape(uint8_array.shape))

###############################################################################

if __name__ == '__main__':
    args = get_parser().parse_args()
    if args.very_verbose: args.verbose = True
    
    validate_file_paths(args)
    print(f"Input: {args.input_image}")
    print(f"Output: {args.output_image}")
    print(f"Message: {args.message}")

    # load image
    bgr_img = cv2.imread(args.input_image, cv2.IMREAD_COLOR)
    
    # calculate the max number of bits we can hide on the image
    height, width, depth = bgr_img.shape
    max_bits = height * width * depth
    while max_bits % 8 != 0:
        max_bits -= 1 # we can only store whole byte words

    # read message lines into an array
    with open(args.message, 'r') as txt_file:
        lines = [line.encode('ascii') for line in txt_file.readlines()]

    message = b''.join(lines)
    print(" |> '" + message.decode('ascii') + "'")

    message_bits = np.unpackbits(to_byte_array(message))
    if message_bits.size > max_bits:
        message_bits = message_bits[:max_bits]
        print("\nThe message is too big to fit in the image, only its start will be hidden:")
        print(" |> '" + ''.join([chr(byte) for byte in np.packbits(message_bits)]) + "'")
        if args.verbose: print(" |> '" + to_bit_str(message_bits) + "'")
    else:
        if args.verbose: print(" |> '" + to_bit_str(message_bits) + "'")
    print()

    r_message = message_bits[0::3]
    g_message = message_bits[1::3]
    b_message = message_bits[2::3]
    if args.very_verbose:
        print("R channel:", r_message)
        print("G channel:", g_message)
        print("B channel:", b_message)
        print()

    if height*width > r_message.size: r_message = np.pad(r_message, (0, height*width - r_message.size), constant_values=0)
    if height*width > g_message.size: g_message = np.pad(g_message, (0, height*width - g_message.size), constant_values=0)
    if height*width > b_message.size: b_message = np.pad(b_message, (0, height*width - b_message.size), constant_values=0)

    # NOTE OpenCV uses BGR order
    message_plane = np.zeros(bgr_img.shape, dtype='uint8')
    message_plane[..., 0] = b_message.reshape((height, width))
    message_plane[..., 1] = g_message.reshape((height, width))
    message_plane[..., 2] = r_message.reshape((height, width))
    if args.very_verbose: print("Message plane:"); print(message_plane); print()

    if args.verbose: print(f"Hiding message on bit plane {args.bit_plane}..")
    # 0xHH..HbH..HH == (0xHH..H0H..HH | 0x00..0b0..00) == ((0xHH..HHH..HH & 0x11..101..11) | 0x00..0b0..00)
	#        ^- bit_plane
	# obs.: 0x11..101..11 == ~0x00..010..00 == ~(0x00..000..01 << bit_plane)
	#       0x00..0b0..00 == (0x00..000..0b << bit_plane), where b is 0 or 1
    mask = 1 << args.bit_plane
    __img = np.bitwise_and(bgr_img, ~mask)
    __img = np.bitwise_or(__img, message_plane << args.bit_plane)
    
    if args.very_verbose:
        print("Original image:")
        print_binary_repr(bgr_img)
        print(f"Message in bit plane {args.bit_plane}:")
        print_binary_repr(message_plane << args.bit_plane)
        print("Image with message embedded:")
        print_binary_repr(__img)

    cv2.imwrite(args.output_image, __img)
    print(f"Image saved to '{args.output_image}'")

# >>> chr(10)
# '\n'
# >>> chr(32)
# ' '
# https://www.rapidtables.com/convert/number/binary-to-ascii.html