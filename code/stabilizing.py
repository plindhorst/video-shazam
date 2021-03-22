import cv2
import numpy as np

from vidstab.VidStab import VidStab

from code.util.image import threshold, grey_scale


def __get_transformation_matrix(dx, dy, da):
    """
    Compute transformation array
    :param dx: x coordinate
    :param dy: y coordinate
    :param da: angle in radians
    :return: 2D array
    """
    m = np.zeros((2, 3), np.float32)
    m[0, 0] = m[1, 1] = np.cos(da)
    m[0, 1] = -np.sin(da)
    m[1, 0] = np.sin(da)
    m[0, 2] = dx
    m[1, 2] = dy
    return m


def __remove_black_borders(input_path, transforms):
    """
    finds smallest rectangle where no black borders are present
    :param input_path: path of input video
    :param transforms: array of transformations
    :return: position and size of rectangle
    """
    cap = cv2.VideoCapture(input_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    i = 0

    x_max = 0
    y_max = 0
    h_min = height - 1
    w_min = width - 1
    while cap.isOpened():
        ret, frame = cap.read()

        if ret and i < len(transforms):
            m = __get_transformation_matrix(transforms[i, 0], transforms[i, 1], transforms[i, 2])
            i += 1

            # rotate image
            frame = cv2.warpAffine(frame, m, (width, height), flags=cv2.INTER_LINEAR)

            #  convert to binary
            frame = grey_scale(frame)
            frame = threshold(frame, 3, 0)

            # get contours
            contours = cv2.findContours(frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
            if len(contours) != 0:
                # get largest rectangle
                c = max(contours, key=cv2.contourArea)
                center, size, angle = cv2.minAreaRect(c)
                w = int(size[0])
                h = int(size[1])
                if h > w:
                    w, h = h, w
                y = int(center[0] - w / 2)
                x = int(center[1] - h / 2)

                x_max = np.maximum(y, x_max)
                y_max = np.maximum(x, y_max)
                h_min = np.minimum(h, h_min)
                w_min = np.minimum(w, w_min)
        else:
            cap.release()
            break
    return y_max, x_max, h_min, w_min


def stabilizing(input_path, output_path):
    """
    stabilizes video
    :param input_path: path of input video
    :param output_path: path of output video
    """
    stabilizer = VidStab()
    stabilizer.gen_transforms(input_path)
    transforms = stabilizer.transforms

    y_max, x_max, h_min, w_min = __remove_black_borders(input_path, transforms)

    cap = cv2.VideoCapture(input_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    codec = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(output_path, codec, 30.0, (w_min, h_min))

    i = 0
    while cap.isOpened():
        ret, frame = cap.read()

        if ret and i < len(transforms):
            m = __get_transformation_matrix(transforms[i, 0], transforms[i, 1], transforms[i, 2])
            i += 1

            # rotate image
            frame = cv2.warpAffine(frame, m, (width, height), flags=cv2.INTER_LINEAR)

            writer.write(frame[y_max:y_max + h_min, x_max:x_max + w_min])
        else:
            cap.release()
            break
