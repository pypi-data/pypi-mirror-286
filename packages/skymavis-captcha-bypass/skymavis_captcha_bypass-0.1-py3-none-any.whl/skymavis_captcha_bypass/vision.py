import cv2
import numpy as np
from PIL import Image

def capture_image(element, count):
    file_path = 'temp/captcha.png'
    with open(file_path, 'wb') as file:
        file.write(element.screenshot_as_png)
    
    image = cv2.imread(file_path)
    output_image = remove_background(image)
    cv2.imwrite(file_path, output_image)
    return output_image

def check_diff(file_path, reference_image_path):
    image = cv2.imread(file_path)
    reference_image = cv2.imread(reference_image_path)
    diff = cv2.absdiff(image, reference_image)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)

    diff_sum = np.sum(binary) / 255
    print(f'diff_sum = {diff_sum}')
    if diff_sum > 1000: 
        return False

def is_correct_orientation(image, count):
    # image = cv2.imread(file_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) == 0:
        return False

    contour = max(contours, key=cv2.contourArea)
    hull = cv2.convexHull(contour)
    
    rect = cv2.minAreaRect(hull)
    angle = rect[2]

    box = cv2.boxPoints(rect)
    box = np.int32(box)
    cv2.drawContours(image, [box], 0, (0, 0, 255), 2)
    cv2.drawContours(image, [hull], -1, (0, 255, 0), 2)
    

    width, height = rect[1]

    if width > height:
        long_edge_angle = angle
    else:
        long_edge_angle = angle - 90

    if long_edge_angle < -45:
        long_edge_angle = 90 + long_edge_angle
    else:
        long_edge_angle = -long_edge_angle

    img = np.array(image)
    true_angle = abs(int(long_edge_angle))
    if true_angle < 12:
        return determine_more_colorful_half(img)
    return False


def count_unique_colors(image):
    if len(image.shape) == 2:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    elif image.shape[2] == 4:
        image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
    reshaped = image.reshape(-1, 3)
    
    unique_colors = np.unique(reshaped, axis=0)
    return len(unique_colors)

def determine_more_colorful_half(img):
    # img = Image.open(image_path)
    img = np.array(img)

    height, width, _ = img.shape
    top_half = img[:height // 2, :]
    bottom_half = img[height // 2:, :]

    top_colors = count_unique_colors(top_half)
    bottom_colors = count_unique_colors(bottom_half)
    
    print(f'Số lượng màu sắc phần trên: {top_colors}')
    print(f'Số lượng màu sắc phần dưới: {bottom_colors}')
    if top_colors > bottom_colors:
        print("Phần trên có nhiều màu sắc hơn.")
        return True
    else:
        print("Phần dưới có nhiều màu sắc hơn.")
        return False

def determine_more_colorful_left_right(img):
    # img = Image.open(image_path)
    img = np.array(img) 
    
    height, width, _ = img.shape
    left_half = img[:, :width // 2]
    right_half = img[:, width // 2:]

    left_colors = count_unique_colors(left_half)
    right_colors = count_unique_colors(right_half)
    
    print(f'Số lượng màu sắc phần trái: {left_colors}')
    print(f'Số lượng màu sắc phần phải: {right_colors}')
    
    if left_colors > right_colors:
        print("Phần trái có nhiều màu sắc hơn.")
        print("Đề xuất xoay phải.")
        return True
    else:
        print("Phần phải có nhiều màu sắc hơn.")
        print("Đề xuất xoay trái.")
        return False

def remove_background(image):
    mask = np.zeros(image.shape[:2], np.uint8)

    bgdModel = np.zeros((1, 65), np.float64)
    fgdModel = np.zeros((1, 65), np.float64)

    rect = (10, 10, image.shape[1] - 10, image.shape[0] - 10)

    cv2.grabCut(image, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)

    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')

    image = image * mask2[:, :, np.newaxis]

    bgr = cv2.split(image)
    alpha = np.ones(bgr[0].shape, dtype=bgr[0].dtype) * 255
    alpha[mask2 == 0] = 0
    rgba = cv2.merge(bgr + (alpha,))

    return rgba