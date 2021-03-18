import numpy as np
import cv2
import matplotlib.pyplot as plt


def colorHist(path):
    cap = cv2.VideoCapture(path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    codec = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('./input/SuperCoilsEN/SuperCoilsEN11.mp4', codec, 30, (width, height))
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            hist, bins = np.histogram(frame.flatten(), 256, [0, 256])

            cdf = hist.cumsum()
            cdf_normalized = cdf * hist.max() / cdf.max()

            cdf_m = np.ma.masked_equal(cdf, 0)
            cdf_m = (cdf_m - cdf_m.min()) * 255 / (cdf_m.max() - cdf_m.min())
            cdf = np.ma.filled(cdf_m, 0).astype('uint8')
            im = cdf[frame]

            f, axarr = plt.subplots(1, 2, figsize=(9, 3))

            axarr[0].hist(frame.flatten(), 256, [0, 256], color='r')
            axarr[0].set_xlim([0, 256])
            axarr[0].legend(('histogram'), loc='upper left')

            axarr[1].hist(im.flatten(), 256, [0, 256], color='r')
            axarr[1].set_xlim([0, 256])
            axarr[1].legend(('histogram'), loc='upper left')
            plt.show()
            out.write(im)
        else:
            out.release()
            cap.release()
            break

colorHist('./input/TheWinterGames_highBrightness.mp4')