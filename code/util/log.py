import cv2


def log(text, verbose):
    if verbose:
        print(text)


def log_image(im, name, verbose):
    if verbose:
        cv2.imwrite("./temp/" + name + ".png", im)
