import cv2
import numpy as np

from utils import BGR_RED, WHITE

###############################################################################

def color_to_black(img):
    ''' Converts every non-white pixel of a colored image to black, returning a binary image '''
    __img = img.astype('float') / 255
    __img = np.sum(__img, axis=-1) / 3 # sum RGB channels into one
    __img = np.where(np.isclose(__img, 1), 1, 0) # turn what isn't white (1) into black (0)
    return 255 * __img

def y_linear(img, bgr=True):
    __img = img.astype('float') / 255
    R = 2 if bgr else 0
    G = 1
    B = 2 - R
    return 255 * (0.2126 * __img[:, :, R] + 0.7152 * __img[:, :, G] + 0.0722 * __img[:, :, B])

def y_srgb(img, bgr=True):
    __img = y_linear(img, bgr) / 255
    return 255 * np.where(__img <= 0.0031308, 12.92 * __img, 1.055 * np.power(__img, 1/2.4) - 0.055)

###############################################################################

def contours(img, objects_are_black=True, draw_bbox=False):
    ''' Returns an image displaying the contours (edges) of objects present in img '''
    __img = color_to_black(img).astype('uint8')
    contours, _ = cv2.findContours(__img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return cv2.drawContours(np.full(img.shape, WHITE), contours if draw_bbox else contours[1:], -1, BGR_RED)

###############################################################################

def number_regions(img, disconsider_bbox=True):
    ''' Returns an image with each object (region) in img numbered at its centroid\n
        and a dictionary with the area, perimeter, eccentricity and solidity for each object '''
    __img = color_to_black(img).astype('uint8')
    contours, _ = cv2.findContours(__img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if disconsider_bbox:
        contours = contours[1:]
    
    text_layer = np.full(img.shape, WHITE, dtype='uint8')
    properties = { region: dict() for region in range(len(contours)) }
    for region, contour in enumerate(reversed(contours)):
        M = cv2.moments(contour)
        cx, cy = __centroid(M)
        org = (cx - (4 if region < 10 else 8), cy + 4)
        cv2.putText(text_layer, str(region), org, color=(0, 0, 0), thickness=1, 
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.4, lineType=cv2.LINE_AA)
        properties[region]['centroid']     = (cx, cy)
        properties[region]['area']         = M['m00']
        properties[region]['perimeter']    = cv2.arcLength(contour, True)
        properties[region]['eccentricity'] = __eccentricity(M)
        properties[region]['solidity']     = __solidity(contour, M['m00'])
    
    return cv2.addWeighted(img, 0.5, text_layer, 0.5, 0), properties

def print_region_properties(properties):
    ''' Pretty prints a region properties dictionary '''
    n_of_regions = len(properties)
    region_padding = len(str(n_of_regions))
    print(f"número de regiões: {n_of_regions}")
    for region in properties.keys():
        print("região {0:{1}d}:  área: {2:4.0f}  perímetro: {3:10.6f}  "
              "excentricidade: {4:8.6f}  solidez: {5:8.6f}".format(
                  region, region_padding, 
                  properties[region]['area'], properties[region]['perimeter'], 
                  properties[region]['eccentricity'], properties[region]['solidity']
              )
        )

###############################################################################

def area_hist(properties, print_regions_per_area=True, limits=[1500, 3000]):
    ''' Returns an image with a histogram of region areas grouped into 'small', 'medium' and 'large'\n
        The classification criteria is the following:
            'small':  area  < limits[0]
            'medium': area >= limits[0] and area < limits[1]
            'large':  area >= limits[1]
        
        If print_regions_per_area is True then the amount of regions per area group is printed '''
    small = medium = large = 0
    areas = []
    for region in properties.keys():
        area = properties[region]['area']
        areas.append(area)
        if   area < limits[0]: small  += 1
        elif area < limits[1]: medium += 1
        else:                  large  += 1
    if print_regions_per_area:
        padding = len(str(max(small, medium, large)))
        print(f"número de regiões pequenas: {small:{padding}d}")
        print(f"número de regiões médias: {medium:{2+padding}d}")
        print(f"número de regiões grandes: {large:{1+padding}d}")
    # FIXME TODO return the histogram

###############################################################################

def __centroid(M):
    return int(M['m10'] / M['m00']), int(M['m01'] / M['m00']) # cx, cy

def __eccentricity(M):
    # FIXME
    lhs = M['mu20'] + M['mu02']
    rhs = np.sqrt(4 * M['mu11']**2 + (M['mu20'] - M['mu02'])**2)
    lambda1 = lhs - rhs # minor axis
    lambda2 = lhs + rhs # major axis
    return np.sqrt(1 - (lambda1 / lambda2))

def __solidity(contour, area=None):
    if area is None:
        area = cv2.contourArea(contour)
    hull = cv2.convexHull(contour)
    hull_area = cv2.contourArea(hull)
    return area / hull_area
