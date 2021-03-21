import sys

import cv2
import numpy as np

from src.util.image import grey_scale, opening, blur


def findCenter(trajectory):
    """
    Find center of the x transforms, y transforms and angle curves
    :param trajectory: input trajectory
    :return: centered trajectory
    """
    centered_trajectory = np.zeros(3)
    for i in range(3):
        centered_trajectory[i] = np.sum(trajectory[:, i]) / len(trajectory[:, i])

    return centered_trajectory


def largest_rotated_rect(w, h, angle):
    """
    Given a rectangle of size w*h that has been rotated by 'angle' (in radians), computes the width and height of the
    largest possible axis-aligned rectangle within the rotated rectangle.
    :param w: width of region
    :param h: height of region
    :param angle: angle of rotation
    :return: width and height of the largest possible axis-aligned rectangle
    """

    quadrant = int(np.floor(angle / (np.pi / 2))) & 3
    sign_alpha = angle if ((quadrant & 1) == 0) else np.pi - angle
    alpha = (sign_alpha % np.pi + np.pi) % np.pi

    bb_w = w * np.cos(alpha) + h * np.sin(alpha)
    bb_h = w * np.sin(alpha) + h * np.cos(alpha)

    gamma = np.math.atan2(bb_w, bb_w) if (w < h) else np.math.atan2(bb_w, bb_w)

    delta = np.pi - alpha - gamma

    length = h if (w < h) else w

    d = length * np.cos(alpha)
    a = d * np.sin(alpha) / np.sin(delta)

    y = a * np.cos(gamma)
    x = y * np.tan(gamma)

    return bb_w - 2 * x, bb_h - 2 * y


def crop_around_center(image, width, height):
    """
    Crop image around center point
    :param image: input image
    :param width: width of cropping region
    :param height: height: of cropping region
    :return: cropped image
    """

    image_size = (image.shape[1], image.shape[0])
    image_center = (int(image_size[0] * 0.5), int(image_size[1] * 0.5))

    if width > image_size[0]:
        width = image_size[0]

    if height > image_size[1]:
        height = image_size[1]

    x1 = int(image_center[0] - width * 0.5)
    x2 = int(image_center[0] + width * 0.5)
    y1 = int(image_center[1] - height * 0.5)
    y2 = int(image_center[1] + height * 0.5)

    return image[y1:y2, x1:x2]


def stabilizing(input_path, output_path):
    """
    stabilizes video
    :param input_path: path of input video
    :param output_path: path of output video
    :return: center, size and angle of the screen
    """

    cap = cv2.VideoCapture(input_path)

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    transforms = []

    while cap.isOpened():
        ret1, prev = cap.read()
        ret2, curr = cap.read()
        if ret1 and ret2:
            prev = grey_scale(prev)
            curr = grey_scale(curr)

            prev_pts = cv2.goodFeaturesToTrack(prev, maxCorners=200, qualityLevel=0.01, minDistance=30,
                                               blockSize=3)

            curr_pts, status, err = cv2.calcOpticalFlowPyrLK(prev, curr, prev_pts, None)
            idx = np.where(status == 1)[0]
            prev_pts = prev_pts[idx]
            curr_pts = curr_pts[idx]

            # Find transformation matrix, get transformation and rotation out, save it
            m, _ = cv2.estimateAffinePartial2D(prev_pts, curr_pts)
            dx = m[0, 2]
            dy = m[1, 2]

            da = np.arctan2(m[1, 0], m[0, 0])
            transforms.append([dx, dy, da])
        else:
            cap.release()
            break

    trajectory = np.cumsum(transforms, axis=0)
    centered_trajectory = findCenter(trajectory)
    difference = centered_trajectory - trajectory
    transforms_centered = transforms + difference

    cap = cv2.VideoCapture(input_path)
    i = 0
    x_max = 0
    y_max = 0
    h_min = height - 1
    w_min = width - 1
    while cap.isOpened():
        ret, frame = cap.read()

        if ret and i < len(transforms):
            # get transformation and rotation of the centered transforms
            dx = transforms_centered[i, 0]
            dy = transforms_centered[i, 1]
            da = transforms_centered[i, 2]
            i += 1

            # Create transformation matrix
            m = np.zeros((2, 3), np.float32)
            m[0, 0] = np.cos(da)
            m[0, 1] = -np.sin(da)
            m[1, 0] = np.sin(da)
            m[1, 1] = np.cos(da)
            m[0, 2] = dx
            m[1, 2] = dy

            # im_crop = cv2.warpAffine(im, rotation_matrix, im.shape[1::-1], flags=cv2.INTER_LINEAR)

            # Apply affine wrapping to the given frame
            frame_stabilized = cv2.warpAffine(frame, m, (width, height), flags=cv2.INTER_LINEAR)
            frame_stabilized = cv2.copyMakeBorder(frame_stabilized, 50, 50, 50, 50, cv2.BORDER_CONSTANT,
                                                  value=[0, 0, 0])
            gray = cv2.cvtColor(frame_stabilized, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)

            contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if len(contours) != 0:
                c = max(contours, key=cv2.contourArea)
                rect = center, size, angle = cv2.minAreaRect(c)
                w = int(size[0])
                h = int(size[1])
                if h > w:
                    temp = w
                    w = h
                    h = temp
                y = int(center[0] - w / 2)
                x = int(center[1] - h / 2)

                box = cv2.boxPoints(rect)
                box = np.int0(box)
                # cv2.drawContours(frame_stabilized, [box], 0, (0, 255, 255), 1)
                #
                # frame_stabilized[x][y] = (0, 0, 255)

                x_max = np.maximum(y, x_max)
                y_max = np.maximum(x, y_max)
                h_min = np.minimum(h, h_min)
                w_min = np.minimum(w, w_min)
                cv2.rectangle(frame_stabilized, (x_max, y_max), (x_max + w_min, y_max + h_min), (0, 255, 0), 1)
                # cv2.rectangle(frame_stabilized, (x, y), (x + w, y + h), (0, 0, 255), 1)
        else:
            cap.release()
            break

    cap = cv2.VideoCapture(input_path)
    i = 0
    while cap.isOpened():
        ret, frame = cap.read()

        if ret and i < len(transforms):
            # get transformation and rotation of the centered transforms
            dx = transforms_centered[i, 0]
            dy = transforms_centered[i, 1]
            da = transforms_centered[i, 2]
            i += 1

            # Create transformation matrix
            m = np.zeros((2, 3), np.float32)
            m[0, 0] = np.cos(da)
            m[0, 1] = -np.sin(da)
            m[1, 0] = np.sin(da)
            m[1, 1] = np.cos(da)
            m[0, 2] = dx
            m[1, 2] = dy

            # im_crop = cv2.warpAffine(im, rotation_matrix, im.shape[1::-1], flags=cv2.INTER_LINEAR)

            # Apply affine wrapping to the given frame
            frame_stabilized = cv2.warpAffine(frame, m, (width, height), flags=cv2.INTER_LINEAR)
            frame_stabilized = cv2.copyMakeBorder(frame_stabilized, 50, 50, 50, 50, cv2.BORDER_CONSTANT,
                                                  value=[0, 0, 0])
            cv2.imshow("frame_stabilized",
                       frame_stabilized[y_max:y_max + h_min, x_max:x_max + w_min])
            cv2.waitKey(0)
        else:
            cap.release()
            break