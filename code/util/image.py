import cv2
import numpy as np


def grey_scale(im):
    """
    :param im: input image
    :return: grey scaled input image
    """
    hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
    return cv2.split(hsv)[2]


def rgb(im):
    """
    :param im: input image
    :return: image in rgb format
    """
    return cv2.cvtColor(im, cv2.COLOR_GRAY2RGB)


def blur(im, n):
    """
    :param im: input image
    :param n: kernel size
    :return: blurred image
    """
    return cv2.GaussianBlur(im, (n, n), 0)


def threshold(im, block_size, c):
    """
    :param im: input image
    :param block_size: Size of a pixel neighborhood that is used to calculate a threshold value for the pixel
    :param c: Constant subtracted from the weighted mean
    :return: threshold image
    """
    # threshold is the sum of blockSize * blockSize neighborhood minus C
    return cv2.adaptiveThreshold(im, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, block_size, c)


def opening(im, n):
    """
    :param im: input image
    :param n: kernel size
    :return: opened image
    """
    kernel = np.ones((n, n), np.uint8)
    return cv2.morphologyEx(im, cv2.MORPH_OPEN, kernel)
