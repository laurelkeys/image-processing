import sys
import os.path
import argparse
from utils import *
from metrics import *
from numpy.linalg import svd

def get_parser():
    parser = argparse.ArgumentParser(description="Image compression through Principal Component Analysis.")
    parser.add_argument("input_image", type=str, 
                        help="Input image file name (with path)")
    parser.add_argument("number_of_components", type=int, 
                        help="Number of principal components to be used")
    parser.add_argument("output_image", type=str, nargs='?', default=None, 
                        help="Output compressed image file name (with path)")
    parser.add_argument("--verbose", "-v", action="store_true", 
                        help="Increase verbosity")
    return parser

def validate_file_paths(args):
    if not os.path.isfile(args.input_image):
        sys.exit(f"\nERROR: Invalid image file path '{args.input_image}'")
    if args.output_image is None:
        _, name, ext = split_root_name_ext(args.input_image)
        args.output_image = f"{name}-{args.number_of_components}{ext}" # default output file name
    else:
        create_folder(args.output_image) # creates the output folder if it doesn't exist

###############################################################################

def main(args):    
    validate_file_paths(args)
    print(f"Input: {args.input_image}")
    print(f"Output: {args.output_image}")

    bgr_img = load(full_path=args.input_image).astype('float') # (M, N, 3)

    height, width, _ = bgr_img.shape
    K = height if height <= width else width # max k is min(M, N)
    if args.verbose:
        print(f"\nNumber of principal components: {K}")
    
    if args.number_of_components > K:
        print(f"\nWARNING: The number k of principal components to be used should be less than or equal to {K}")
        print(f"         (i.e. k <= min(M, N) == min({height}, {width}) for '{args.input_image}')")
        args.number_of_components = K
        print(f"WARNING: Using k = {K}")

    # NOTE OpenCV uses BGR order
    # obs.: vh = np.transpose(np.conj(v))
    b_u, b_s, b_vh = svd(bgr_img[:, :, 0], full_matrices=False)
    g_u, g_s, g_vh = svd(bgr_img[:, :, 1], full_matrices=False)
    r_u, r_s, r_vh = svd(bgr_img[:, :, 2], full_matrices=False)

    # for each channel i in range(0, 3):
    # bgr_img[:, :, i] == u[:, :, i] @ s[:, :, i] @ vh[:, :, i]
    u = np.dstack((b_u, g_u, r_u))                            # (M, K, 3)
    s = np.dstack((np.diag(b_s), np.diag(g_s), np.diag(r_s))) # (K, K, 3)
    vh = np.dstack((b_vh, g_vh, r_vh))                        # (K, N, 3)

    # k <= K == min(M, N)
    k = args.number_of_components
    __u = u[:, :k, :]   # (M, k, 3)
    __s = s[:k, :k, :]  # (k, k, 3)
    __vh = vh[:k, :, :] # (k, N, 3)

    __b = __u[:, :, 0] @ __s[:, :, 0] @ __vh[:, :, 0]
    __g = __u[:, :, 1] @ __s[:, :, 1] @ __vh[:, :, 1]
    __r = __u[:, :, 2] @ __s[:, :, 2] @ __vh[:, :, 2]
    __img = np.dstack((__b, __g, __r))
    
    save(__img, full_path=args.output_image)
    print(f"\nCompressed image saved to '{args.output_image}'")

    print(f"\nRMSE: {rmse(original=bgr_img, compressed=__img):.4f}")
    rho, fsize, __fsize = compression_ratio(args.input_image, args.output_image)
    print(f"Compression ratio: {100 * rho:.2f}% = {fsize} / {__fsize}")


if __name__ == '__main__':
    args = get_parser().parse_args()
    main(args)