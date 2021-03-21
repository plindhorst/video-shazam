import glob

import cv2
import numpy as np

from code.util.video import get_frame_rate


def normalize(data):
    """
    normalizes data in array
    :param data: array with values
    :return: normalized array
    """
    if np.max == 0:
        return data
    else:
        return data / np.max(data)


def get_video_list(videos_path):
    """
    get all videos in a folder
    :param videos_path: path to videos
    :return: array of videos
    """
    video_types = ('*.mp4', '*.avi')
    videos = []
    for type_ in video_types:
        files = videos_path + '/' + type_
        videos.extend(glob.glob(files))
    return videos


def get_features(video):
    """
    get video and audio features
    :param video: path to video
    :return: features
    """
    frame_rate = get_frame_rate(video)

    features = {'colorhists': []}
    cap = cv2.VideoCapture(video)
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            features["colorhists"].append(colorhist(frame))
        else:
            cap.release()
            break
    return features


def temporal_diff(frame1, frame2, threshold=50):
    """
    compute temporal difference between two consecutive frames
    :param frame1: first frame
    :param frame2: second frame
    :param threshold: difference threshold
    :return: sum of pixel differences
    """
    if frame1 is None or frame2 is None:
        return None
    diff = np.abs(frame1.astype('int16') - frame2.astype('int16'))
    diff_t = diff > threshold
    return np.sum(diff_t)


def colorhist_diff(hist1, hist2):
    """
    compute histogram difference between two consecutive frames
    :param hist1: first histogram
    :param hist2: second histogram
    :return: sum of histogram differences
    """
    if hist1 is None or hist2 is None:
        return None
    diff = np.abs(hist1 - hist2)
    return np.sum(diff)


def colorhist(im):
    """
    compute the color histogram from an image
    :param im: image
    :return: color histogram
    """
    chans = cv2.split(im)
    color_hist = np.zeros((256, len(chans)))
    for i in range(len(chans)):
        color_hist[:, i] = np.histogram(chans[i], bins=np.arange(256 + 1))[0] / float(
            (chans[i].shape[0] * chans[i].shape[1]))
    return color_hist


def audio_powers(audio_frame):
    """
    compute audio intensities from audio
    :param audio_frame: audio frame
    :return: average audio power
    """
    return np.mean(audio_frame ** 2)
