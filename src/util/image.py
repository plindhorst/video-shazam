import cv2


def grey_scale(im):
    """
    :param im: input image
    :return: grey scaled input image
    """
    hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
    return cv2.split(hsv)[2]


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
