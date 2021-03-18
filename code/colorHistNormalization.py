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
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.equalizeHist(gray)
            out.write(gray)
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
            # yen_threshold = threshold_yen(frame)
            # bright = rescale_intensity(frame, (0, yen_threshold), (0, 255))
            # out.write(bright)
            # cv2.imshow("frame", frame)
            # cv2.waitKey(0)
            hist, bins = np.histogram(frame.flatten(), 256, [0, 256])

            cdf = hist.cumsum()
            cdf_normalized = cdf * hist.max() / cdf.max()
            cdf_m = np.ma.masked_equal(cdf, 0)
            cdf_m = (cdf_m - cdf_m.min()) * 255 / (cdf_m.max() - cdf_m.min())
            cdf = np.ma.filled(cdf_m, 0).astype('uint8')
            im = cdf[frame]
            out.write(im)
        else:
            out.release()
            cap.release()
            break

brightness('./temp/cropped.mp4')