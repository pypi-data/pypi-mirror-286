import cv2
import numpy as np

from ..localizers import sharpen, autoScaleABC


def image_preprocessing(source, sharpen_weight = 1, sharpen_gauss_ksize = 3, sharpen_gamma_sigmaX = 1,
                        morph_struct_element = cv2.MORPH_CROSS, morph_blur_size = 9, morph_operations = [cv2.MORPH_OPEN], morph_iterations = [1],
                        median_blur_ksize = 7):
    if len(source.shape) == 3:
        img = cv2.cvtColor(source, cv2.COLOR_BGR2GRAY).astype(np.uint8)
    elif  len(source.shape) == 2:
        img = source.copy().astype(np.uint8)
    
    # INPAINTING DATA IN IMAGE
    inp_mask = np.zeros(img.shape, dtype=np.uint8)
    inp_mask[0, :19] = 1
    
    inp = cv2.inpaint(img, inp_mask, 1, cv2.INPAINT_TELEA)
    
    # SHARPENING
    img = sharpen(inp, weight = sharpen_weight, gauss_ksize = sharpen_gauss_ksize, gauss_sigmaX = sharpen_gamma_sigmaX)
    
    # BLURING
    for operation, iterations in zip(morph_operations, morph_iterations):
        img = cv2.morphologyEx(img, operation, cv2.getStructuringElement(morph_struct_element, (morph_blur_size, morph_blur_size)), iterations=iterations)
    
    img = cv2.medianBlur(img, median_blur_ksize)

    img = autoScaleABC(img)
    return img, inp