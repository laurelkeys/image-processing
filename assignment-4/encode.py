import sys
import os.path
import argparse
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

    # create a byte array representation of the message
    message = b''.join(lines)
    print(f"\n{message}") # print(f"\n{message.decode('ascii')}")
    message_bytes = to_byte_array(message)
    print(f"\n{message_bytes}")

    # for plane in range(0, 8):
    #     img = (test_img[0] >> plane) & 1
    #     title = f"1.3 {test_img[1]} (plano de bit {plane})"
    #     show_grayscale(np.where(img, 255, 0), title, save_fname=title)
    #     plt.show()

# >>> chr(10)
# '\n'
# >>> chr(32)
# ' '