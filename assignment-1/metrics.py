import sys
import cv2
import time
import functools
from image_processing_utils import *

def mse(original, transformed):
    ''' Computes the Mean Squared Error (MSE) between the original and transformed images '''
    return ((original - transformed)**2).mean()

def rmse(original, transformed):
    ''' Computes the Root Mean Squared Error (RMSE) between the original and transformed images '''
    return np.sqrt(mse(original, transformed))

def nrmse(original, transformed):
    ''' Computes the Normalized Root Mean Squared Error (NRMSE) between the original and transformed images '''
    return rmse(original, transformed) / (original.max() - original.min())

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
    
    y, x = 242, 242
    size = 48, 64
    cv2.imwrite(os.path.join(folder, "detail", f"detail_gray_{name}.png"), gray_original[y:y+size[0], x:x+size[1]])
    for img_title, img in images.items():
        crop_img = img[y:y+size[0], x:x+size[1]]
        cv2.imwrite(os.path.join(folder, "detail", f"detail_{img_title}.png"), crop_img)
    cv2.imwrite(os.path.join(folder, "detail", f"detail_{name}.png"), original[y:y+size[0], x:x+size[1]])
    for gray_img_title, gray_img in gray_images.items():
        crop_img = gray_img[y:y+size[0], x:x+size[1]]
        cv2.imwrite(os.path.join(folder, "detail", f"detail_{gray_img_title}.png"), crop_img)
        # cv2.imshow(f"cropped {gray_img_title}", crop_img)
        # cv2.waitKey(0)

    exit()
    results = []
    gray_results = []
    print("RMSE, image, mode")
    for img_title, img in images.items():
        _rmse = rmse(original, img)
        results.append((_rmse, img_title))
        # print(f"{_rmse:.2f}, {img_title}, color")
    for gray_img_title, gray_img in gray_images.items():
        _rmse = rmse(gray_original, gray_img)
        gray_results.append((_rmse, gray_img_title))
        # print(f"{_rmse:.2f}, {gray_img_title}, gray")
    
    # print('\n')

    # print(f"\nresults: \n{sorted(results, key=lambda tup: tup[0])}")
    for _rmse, img_title in sorted(results, key=lambda tup: tup[0]):
        if not img_title.__contains__("serpentine"):
            print(f"{_rmse:.3f}, {img_title}, color")
    # print(f"\ngray_results: \n{sorted(gray_results, key=lambda tup: tup[0])}")
    for _rmse, gray_img_title in sorted(gray_results, key=lambda tup: tup[0]):
        if not gray_img_title.__contains__("serpentine"):
            print(f"{_rmse:.3f}, {gray_img_title}, gray")