import cv2
import numpy as np

from transformations import color_to_black

def number_regions(img, print_properties=True, disconsider_bbox=True):
    ''' Returns an image with each object (region) in img numbered at its centroid\n
        Prints the area, perimeter, eccentricity and solidity for each object if print_properties is True '''    
    __img = img.copy()
    contours, _ = cv2.findContours(color_to_black(__img).astype('uint8'), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if disconsider_bbox:
        contours = contours[1:]
    
    n_of_regions = len(contours)
    if print_properties:
        region_padding = len(str(n_of_regions))
        print(f"número de regiões: {n_of_regions}\n")    
    for region, contour in enumerate(contours):
        M = cv2.moments(contour)
        cx, cy = centroid(M)
        cv2.putText(__img, text=str(region), org=(cx, cy), color=(0, 0, 0), thickness=1, 
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5, lineType=cv2.LINE_AA)
        if print_properties:
            area = M['m00'] # cv2.contourArea(contour)
            print(
                "região {0:{1}d}:  área: {2:4.0f}  perímetro: {3:10.6f}  excentricidade: {4:8.6f}  solidez: {5:8.6f}"
                .format(region, region_padding, area, cv2.arcLength(contour, True), eccentricity(M), solidity(contour, area))
            )
    print()
    return __img

###############################################################################

def centroid(M):
    return int(M['m10'] / M['m00']), int(M['m01'] / M['m00']) # cx, cy

def eccentricity(M):
    lhs = M['mu20'] + M['mu02']
    rhs = np.sqrt(4 * M['mu11']**2 + (M['mu20'] - M['mu02'])**2)
    lambda1 = lhs - rhs # minor axis
    lambda2 = lhs + rhs # major axis
    return np.sqrt(1 - (lambda1 / lambda2))

def solidity(contour, area=None):
    if area is None:
        area = cv2.contourArea(contour)
    hull = cv2.convexHull(contour)
    hull_area = cv2.contourArea(hull)
    return area / hull_area
