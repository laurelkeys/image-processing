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
    return parser

###############################################################################

if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()