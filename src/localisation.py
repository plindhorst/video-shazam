import cv2
import numpy as np

from src.util.image import grey_scale, blur, threshold


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
    return heat_map


def localisation(input_path):
    """
    finds screen position using temporal differences
    :param input_path: path to the input video
    :return: center, size and angle of the screen
    """

    heat_map = __get_heat_map(input_path)
    cv2.imshow("heat_map", heat_map)
    cv2.waitKey(0)
