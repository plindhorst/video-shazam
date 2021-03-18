import numpy as np
import cv2
import matplotlib.pyplot as plt

def histNormalization(path):
    cap = cv2.VideoCapture(path)

    out = cv2.VideoWriter('..input/SuperCoilsEN/SuperCoilsEN11.mp4',0x7634706d, 20.0, (640,480))
    while cap.isOpened():
        print("here")
        ret, frame=cap.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        # res = np.hstack((frame, gray))  # stacking images side-by-side
        out.write(gray)



    cap.release()
    cv2.destroyAllWindows()
    return out


histNormalization('..input/SuperCoilsEN/SuperCoilsEN1.mp4')