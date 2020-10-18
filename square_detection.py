from typing import List, Optional, Union, Tuple

import cv2
import numpy as np

ImageSize = Union[Tuple[int, int], int]


def select_rgb_white_yellow(image: np.ndarray) -> np.ndarray: 
    # white color mask
    lower = np.uint8([240, 240, 240])
    upper = np.uint8([255, 255, 255])
    white_mask = cv2.inRange(image, lower, upper)

    # yellow color mask
    lower = np.uint8([150, 150,   0])
    upper = np.uint8([255, 255, 255])
    yellow_mask = cv2.inRange(image, lower, upper)

    # combine the mask
    mask = cv2.bitwise_or(white_mask, yellow_mask)
    masked = cv2.bitwise_and(image, image, mask = yellow_mask)
    return masked


def draw_lines(image: np.ndarray, lines: np.ndarray) -> np.ndarray:
    heights = np.abs(lines[:, 3] - lines[:, 1])
    widths = np.abs(lines[:, 2] - lines[:, 0])

    h_lines_mask = (heights <= 1) & (widths > image.shape[1] * .05)
    v_lines_mask = (widths <= 1) & (heights > image.shape[0] * .05)
    valid_mask = h_lines_mask | v_lines_mask

    # Extend horizontal lines to fit the whole image
    lines[h_lines_mask, 0] = 0
    lines[h_lines_mask, 2] = image.shape[1]

    # Extend vertical lines to fit the whole image
    lines[v_lines_mask, 1] = 0
    lines[v_lines_mask, 3] = image.shape[0]

    for x1, y1, x2, y2 in lines[valid_mask]:
        cv2.line(image, (x1, y1), (x2, y2), [255, 255, 255], 2)

    return image


def detect_characters(
        image: Union[str, np.ndarray],
        characters_size: Optional[ImageSize] = None) -> List[np.ndarray]:

    if isinstance(characters_size, int):
        characters_size = (characters_size,) * 2

    if isinstance(image, str):
        image = cv2.imread(image)

    # Retrieve yellows and whites from the image
    res = select_rgb_white_yellow(image)

    # Convert the image to gray scale and apply a canny edge detection
    res = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
    res = cv2.Canny(res, 50, 255)

    # Based on the canny edge detection result, find straight lines in the image
    lines = cv2.HoughLinesP(res, rho=.1, theta=np.pi/ 10., 
                            threshold=200, minLineLength=5, maxLineGap=4)
    lines = lines.reshape(-1, 4)

    # Draw completely horizontal and vertical lines and expand them to fit the
    # image, this way we can build a grid spliting all the box characters
    res = draw_lines(cv2.cvtColor(res, cv2.COLOR_GRAY2BGR), lines)

    # Again convert the image to gray scale and threshold it in order to binarize it
    res = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
    res = cv2.threshold(res, 200, 255, cv2.THRESH_BINARY)[1]

    # With the binarized image, we retrieve the countours
    cnts = cv2.findContours(res, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    # Get the rectangles surrounding the countors and compute its area and aspect
    # ratio
    rects = np.array([cv2.boundingRect(o) for o in cnts], dtype='float32')
    areas = rects[:, 2] * rects[:, 3]
    ar = rects[:, 3] / rects[:, 2]

    # We filter out:
    #   - the rectangles which have a tiny area (1% image area)
    #   - The rectangles with a massive area (10% image area)
    #   - The rectangles which do not have a squared shape (aspect ratio near to 1)
    min_area = .01 * (image.shape[1] * image.shape[0])
    max_area = .1 * (image.shape[1] * image.shape[0])
    valid_rectangles = (areas > min_area) & (areas < max_area)
    valid_rectangles &= (ar > .8) & (ar < 1.2)

    characters = []
    for i, (x, y, w, h) in enumerate(rects[valid_rectangles].astype('int32')):
        ROI = image[y:y+h, x:x+h]
        characters.append(ROI)
        cv2.imwrite(f'rois/ROI_{i}.png', ROI)
        # cv2.rectangle(image, (x, y), (x + w, y + h), (36,255,12), 5)

    if characters_size is not None:
        characters = np.array([cv2.resize(o, characters_size) 
                               for o in characters])

    return characters


if __name__ == "__main__":
    characters = detect_characters('test-crop.jpg')
    print("Characters found:", len(characters))
