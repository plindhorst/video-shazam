import cv2


def __crop_image(im, rectangle):
    """
    crops image from a rectangle
    :param im: image
    :param rectangle: screen rectangle
    :return: cropped image
    """
    center, size, angle = rectangle
    # rotate image
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    im_crop = cv2.warpAffine(im, rotation_matrix, im.shape[1::-1], flags=cv2.INTER_LINEAR)
    # crop image
    im_crop = cv2.getRectSubPix(im_crop, (int(size[0]), int(size[1])), center)
    im_crop = cv2.resize(im_crop, (640, 480), interpolation=cv2.INTER_AREA)

    return im_crop


def cropping(rectangle, input_path, output_path):
    """
    creates a new cropped video
    :param rectangle: screen rectangle
    :param input_path: path of input video
    :param output_path: path of output video
    :return: center, size and angle of the screen
    """

    cap = cv2.VideoCapture(input_path)

    codec = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(output_path, codec, 30.0, (640, 480))

    while cap.isOpened():
        ret, frame = cap.read()

        if ret:
            im_crop = __crop_image(frame, rectangle)
            writer.write(im_crop)
        else:
            writer.release()
            cap.release()
            break
