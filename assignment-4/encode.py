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

    with open(args.message, 'r') as txt_file:
        lines = [line.encode('ascii') for line in txt_file.readlines()]
    print(f"Message: {args.message}")
    print(f"\n{lines}")

    # load image
    bgr_img = cv2.imread(args.input_image, cv2.IMREAD_COLOR)
    height, width, depth = bgr_img.shape
    max_bits = height * width * depth
    while max_bits % 8 != 0:
        max_bits -= 1 # we can only store whole byte words

    # create a byte array representation of the message
    message = b''.join(lines)
    print(f"\n{message}") # print(f"\n{message.decode('ascii')}")
    
    message_bytes = to_byte_array(message)
    print(f"\n{message_bytes}")

    message_bits = np.unpackbits(message_bytes)
    print(f"\n{to_bit_str(message_bits)}")
    print(f"\n{message_bits}")
    if message_bits.size > max_bits:
        print("\nThe message is too big to fit in the image, only its start will be saved:")
        message_bits = message_bits[:max_bits]
        print(f"{to_bit_str(message_bits)}")
        print(f"{message_bits}")
        print("'" + ''.join([chr(byte) for byte in np.packbits(message_bits)]) + "'")

    r_message = message_bits[0::3]
    g_message = message_bits[1::3]
    b_message = message_bits[2::3]
    print(r_message); print(g_message); print(b_message)

    r_message = np.pad(r_message, (0, height*width - r_message.size), constant_values=0)
    g_message = np.pad(g_message, (0, height*width - g_message.size), constant_values=0)
    b_message = np.pad(b_message, (0, height*width - b_message.size), constant_values=0)
    print(r_message); print(g_message); print(b_message)

    # TODO embed message_bits into the image
    
    # for plane in range(0, 8):
    #     img = (test_img[0] >> plane) & 1
    #     title = f"1.3 {test_img[1]} (plano de bit {plane})"
    #     show_grayscale(np.where(img, 255, 0), title, save_fname=title)
    #     plt.show()

# >>> chr(10)
# '\n'
# >>> chr(32)
# ' '