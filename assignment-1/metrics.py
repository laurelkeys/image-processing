import sys
import time
import functools
from image_processing_utils import *

def mse(original, transformed):
    ''' Computes the Mean Squared Error (MSE) between the original and transformed images '''
    return ((original - transformed)**2).mean()

if __name__ == '__main__':
    name = sys.argv[1]
    original = load(f"{name}.png", "i")
    gray_original = grayscale(original)

    images = {}
    gray_images = {}

    folder = os.path.join(OUTPUT_FOLDER, name)
    for img_fname in [ifn for ifn in image_fnames(folder)]:
        img_title, _ = split_name_ext(img_fname)
        if img_title.__contains__("gray"):
            gray_images[img_title] = cv2.imread(os.path.join(folder, img_fname), cv2.IMREAD_GRAYSCALE)
        else:
            images[img_title] = load(img_fname, folder)
    
    results = []
    gray_results = []
    print("MSE, image, mode")
    for img_title, img in images.items():
        mse = mse(original, img)
        results.append((mse, img_title))
        print(f"{mse:.2f}, {img_title}, color")
    for gray_img_title, gray_img in gray_images.items():
        gray_mse = mse(gray_original, gray_img)
        gray_results.append((gray_mse, gray_img_title))
        print(f"{gray_mse:.2f}, {gray_img_title}, gray")