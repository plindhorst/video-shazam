import numpy as np
import cv2
import matplotlib.pyplot as plt

def histNormalization(path):
    cap = cv2.VideoCapture(path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    codec = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('./input/SuperCoilsEN/SuperCoilsEN11.mp4', codec, 30, (width, height))
    while cap.isOpened():
        ret, frame = cap.read()

        if ret:
            # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            img = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
            gray = cv2.equalizeHist(gray)
            plt.plot(gray)
            plt.show()
            backtorgb = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)
            res = np.hstack((frame, backtorgb))  # stacking images side-by-side
            out.write(res)
            # cv2.imshow("frame", frame)
            # cv2.waitKey(0)
        else:
            out.release()
            cap.release()
            break



# histNormalization('./input/SuperCoilsEN/SuperCoilsEN1.mp4')


from skimage.filters import threshold_yen
from skimage.exposure import rescale_intensity
def brightness(path):
    cap = cv2.VideoCapture(path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    codec = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('./input/SuperCoilsEN/SuperCoilsEN11.mp4', codec, 30, (width, height))
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            yen_threshold = threshold_yen(frame)
            bright = rescale_intensity(frame, (0, yen_threshold), (0, 255))
            out.write(bright)
            # cv2.imshow("frame", frame)
            # cv2.waitKey(0)
        else:
            out.release()
            cap.release()
            break

brightness('./input/SuperCoilsEN/SuperCoilsEN1.mp4')