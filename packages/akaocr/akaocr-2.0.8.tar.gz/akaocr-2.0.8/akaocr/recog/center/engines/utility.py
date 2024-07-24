# WRITER: LauNT # DATE: 05/2024
# FROM: akaOCR Team - QAI

import cv2, math
import numpy as np

    
def resize_image(image, image_shape, max_ratio):
    """Resize image without distortion
    Args:
        image (array): color image, read by opencv
        image_shape (list): desired image shape
        max_ratio (float)): max ratio in a batch of images
    Returns:
        array: resized image
    """
    h, w = image.shape[0], image.shape[1]
    img_c, img_h, img_w = image_shape
    current_ratio = w * 1.0 / h

    # get resized width
    img_w = int(img_h * max_ratio)
    if math.ceil(img_h * current_ratio) > img_w: resized_w = img_w
    else: resized_w = int(math.ceil(img_h * current_ratio))
    
    # resize image
    resized_image = cv2.resize(image, (resized_w, img_h))
    resized_image = resized_image.astype('float32')

    # normalize image
    resized_image = resized_image.transpose((2, 0, 1))/255
    resized_image -= 0.5
    resized_image /= 0.5
    padding_im = np.zeros((img_c, img_h, img_w), dtype=np.float32)
    padding_im[:, :, :resized_w] = resized_image

    return padding_im