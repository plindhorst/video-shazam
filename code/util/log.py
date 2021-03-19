import cv2


def log(text, verbose):
    """
    print information
    :param text: message to print
    :param verbose: option to display information
    """
    if verbose:
        print(text)


def log_image(im, name, verbose):
    """
    writes an image to the temp folder
    :param im: image to save
    :param verbose: option to display information
    """
    if verbose:
        cv2.imwrite("./temp/" + name + ".png", im)
