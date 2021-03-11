import cv2
import numpy as np

from src.util.image import grey_scale, blur, threshold, opening, rgb


def __get_heat_map(input_path):
    """
    returns heat map of temporal differences
    :param input_path: path to the input video
    :return: heat map
    """

    cap = cv2.VideoCapture(input_path)

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    heat_map = np.zeros((height, width), dtype=np.uint8)

    while cap.isOpened():
        ret1, im_current = cap.read()
        ret2, im_next = cap.read()

        if ret1 and ret2:
            # Compute absolute difference between two consecutive frames
            im = grey_scale(cv2.absdiff(im_current, im_next))
            # Remove noise
            im = blur(im, 11)
            # Convert image to binary
            im = threshold(im, 19, 5)
            # Find positions of differences
            xs, ys = np.nonzero(im)

            for i in range(len(xs)):
                x = xs[i]
                y = ys[i]
                heat_map[x, y] += 1
        else:
            cap.release()

    # Convert heat_map to binary
    heat_map = threshold(heat_map, 19, 1)
    # Perform erosion followed by dilation
    heat_map = opening(heat_map, 2)
    return heat_map


def __get_position(heat_map):
    """
    gets the rectangle around a heat map
    :param heat_map: heat map of temporal differences
    :return: center, size and angle of the screen
    """
    # Get contours
    contours, hierarchy = cv2.findContours(heat_map, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    # Get area of contours
    rectangle = None, None, None
    if len(contours) > 0:
        # Add contours together
        contours = np.concatenate(contours)
        # Get rectangle
        rectangle = center, size, angle = cv2.minAreaRect(contours)
        # Rotate rectangle if height > width
        if size[0] < size[1]:
            size = (size[1], size[0])
            angle += 90
            rectangle = center, size, angle

    return rectangle


def localization(input_path, debug=False):
    """
    finds screen position using temporal differences
    :param debug: if true show all steps
    :param input_path: path to the input video
    :return: center, size and angle of the screen
    """

    heat_map = __get_heat_map(input_path)
    center, size, angle = __get_position(heat_map)

    if debug:
        im_contours = np.zeros((len(heat_map), len(heat_map[0]), 3), dtype=np.uint8)
        im_contours += rgb(heat_map)
        box = cv2.boxPoints((center, size, angle))
        box = np.int0(box)
        cv2.drawContours(im_contours, [box], 0, (0, 0, 255), 2)
        cv2.imshow("debug", im_contours)
        cv2.waitKey(0)

    return center, size, angle
