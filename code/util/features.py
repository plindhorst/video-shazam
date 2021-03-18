import glob

import cv2
import numpy as np


def get_video_list(videos_path):
    video_types = ('*.mp4', '*.avi')
    audio_types = ('*.wav')
    videos = []
    for type_ in video_types:
        files = videos_path + '/' + type_
        videos.extend(glob.glob(files))
    return videos


def get_features(video):
    features = {'colorhists': [], 'tempdiffs': [], 'audiopowers': [], 'mfccs': [], 'colorhistdiffs': []}
    cap = cv2.VideoCapture(video)
    prev_frame = None
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            features["colorhists"].append(colorhist(frame))

            if prev_frame is not None:
                features["colorhistdiffs"].append(colorhist_diff(colorhist(prev_frame), colorhist(frame)))
                features["tempdiffs"].append(temporal_diff(prev_frame, frame, 10))

            prev_frame = frame
        else:
            cap.release()
            break
    return features


def temporal_diff(frame1, frame2, threshold=50):
    if frame1 is None or frame2 is None:
        return None
    diff = np.abs(frame1.astype('int16') - frame2.astype('int16'))
    diff_t = diff > threshold
    return np.sum(diff_t)


def colorhist_diff(hist1, hist2):
    if hist1 is None or hist2 is None:
        return None
    diff = np.abs(hist1 - hist2)
    return np.sum(diff)


def colorhist(im):
    chans = cv2.split(im)
    color_hist = np.zeros((256, len(chans)))
    for i in range(len(chans)):
        color_hist[:, i] = np.histogram(chans[i], bins=np.arange(256 + 1))[0] / float(
            (chans[i].shape[0] * chans[i].shape[1]))
    return color_hist


def audio_powers(audio_frame):
    return np.mean(audio_frame ** 2)
