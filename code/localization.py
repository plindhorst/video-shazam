import cv2
import numpy as np

from code.util.image import grey_scale, blur, threshold, opening, rgb
from code.util.log import log_image
from code.util.video import get_median_frame


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
            break

    # Convert heat_map to binary
    # and perform erosion followed by dilation
    if len(np.nonzero(heat_map)[0]) >= 30000:
        heat_map = threshold(heat_map, 29, 1)
        heat_map = opening(heat_map, 6)
    else:
        heat_map = threshold(heat_map, 19, 1)
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
    center, size, angle = None, None, None
    if len(contours) > 0:
        # Add contours together
        contours = np.concatenate(contours)
        # Get rectangle
        center, size, angle = cv2.minAreaRect(contours)
        # Rotate rectangle if height > width
        if size[0] < size[1]:
            size = (size[1], size[0])
            angle += 90
            angle = - (180 - angle)
    return center, size, angle


def __write_image(input_path, heat_map, rectangle, verbose=False):
    """
    write debug image to temp folder
    :param input_path: path of input video
    :param heat_map: heat map of temporal differences
    :param rectangle: screen rectangle
    :param verbose: option to display information
    """
    heat_map = rgb(heat_map)
    cv2.drawContours(heat_map, [np.int0(cv2.boxPoints(rectangle))], 0, (0, 0, 255), 1)
    log_image(heat_map, "heat_map", verbose)

    frame = get_median_frame(input_path)
    cv2.drawContours(frame, [np.int0(cv2.boxPoints(rectangle))], 0, (0, 0, 255), 1)
    log_image(frame, "screen_contour", verbose)


def localization(input_path, verbose=False):
    """
    finds screen position using temporal differences
    :param input_path: path to the input video
    :param verbose: option to display information
    :return: center, size and angle of the screen
    """

    heat_map = __get_heat_map(input_path)
    center, size, angle = __get_position(heat_map)

    __write_image(input_path, heat_map, (center, size, angle), verbose)

    return center, size, angle
