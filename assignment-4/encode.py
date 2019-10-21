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
    parser.add_argument("--output_image", "-o", type=str, required=True, 
                        help="Output image file name (with path)")
    parser.add_argument("--bit_plane", "-b", type=int, choices=range(0, 8), default=0, 
                        help="Bit plane in which to hide the message (default: %(default)d)")
    return parser

###############################################################################

def to_byte_array(string):
    array = np.zeros(len(string), dtype='uint8')
    for i, char in enumerate(string):
        array[i] = char
    return array

def to_bit_str(bit_array):
    b = 0
    bit_str = ""
    for bit in bit_array:
        bit_str += str(bit)
        b += 1
        if b == 8:
            b = 0
            bit_str += ' '
    return bit_str
    # https://www.rapidtables.com/convert/number/binary-to-ascii.html

###############################################################################

if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()

    if not os.path.isfile(args.input_image):
        sys.exit(f"\nERROR: invalid image path or extension '{args.input_image}'")
    create_folder(args.output_image)
    print(f"Input: {args.input_image}")
    print(f"Output: {args.output_image}")

    # read message lines into an array
    with open(args.message, 'r') as txt_file:
        lines = [line.encode('ascii') for line in txt_file.readlines()]
    print(f"Message: {args.message}")

    # load image
    bgr_img = cv2.imread(args.input_image, cv2.IMREAD_COLOR)
    height, width, depth = bgr_img.shape
    max_bits = height * width * depth
    while max_bits % 8 != 0:
        max_bits -= 1 # we can only store whole byte words

    # create a byte array representation of the message
    message = b''.join(lines)
    print(" |> '" + message.decode('ascii') + "'")
    message_bytes = to_byte_array(message)

    # create a bit array representation
    message_bits = np.unpackbits(message_bytes)
    if message_bits.size > max_bits:
        message_bits = message_bits[:max_bits]
        print("\nThe message is too big to fit in the image, only its start will be saved:")
        print(" |> '" + ''.join([chr(byte) for byte in np.packbits(message_bits)]) + "'")
        # print(" |> '" + to_bit_str(message_bits) + "'")
    else:
        # print(" |> '" + to_bit_str(message_bits) + "'")
        pass
    print()

    r_message = message_bits[0::3]
    g_message = message_bits[1::3]
    b_message = message_bits[2::3]
    # print("R channel:", r_message)
    # print("G channel:", g_message)
    # print("B channel:", b_message)
    # print()

    if height*width > r_message.size: r_message = np.pad(r_message, (0, height*width - r_message.size), constant_values=0)
    if height*width > g_message.size: g_message = np.pad(g_message, (0, height*width - g_message.size), constant_values=0)
    if height*width > b_message.size: b_message = np.pad(b_message, (0, height*width - b_message.size), constant_values=0)

    # FIXME OpenCV uses BGR order
    message_plane = np.zeros(bgr_img.shape, dtype='uint8')
    message_plane[..., 0] = r_message.reshape((height, width))
    message_plane[..., 1] = g_message.reshape((height, width))
    message_plane[..., 2] = b_message.reshape((height, width))
    # print(message_plane)
    # print()

    print(f"Hiding message on bit plane {args.bit_plane}..")
    #    bit_plane
    #        v
    # 0xHH..HbH..H == (0xHH..H0H..H | 0x00..0b0..0) == ((0xHH..HHH..H & 0x11..101..1) | 0x00..0b0..0)
	#        ^
	# obs.: 0x11..101..1 == ~0x00..010..0 == ~(0x00..000..1 << bit_plane)
	#       0x00..0b0..0 == (0x00..000..b << bit_plane), b in {0, 1}
    mask = 1 << args.bit_plane
    __img = np.bitwise_and(bgr_img, ~mask)
    __img = np.bitwise_or(__img, message_plane << args.bit_plane)
    
    def print_binary_repr(arr):
        print(np.array([np.binary_repr(elem).zfill(8) for elem in arr.flatten()]).reshape(arr.shape))
    # print("Original image:")
    # print_binary_repr(bgr_img)
    # print(f"\nMessage in bit plane {args.bit_plane}:")
    # print_binary_repr(message_plane << args.bit_plane)
    # print("\nImage with message embedded:")
    # print_binary_repr(__img)

    cv2.imwrite(args.output_image, __img)
    print(f"Image saved to '{args.output_image}'")

# >>> chr(10)
# '\n'
# >>> chr(32)
# ' '