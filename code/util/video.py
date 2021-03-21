import datetime

import cv2
import moviepy.editor as mp


def format_duration(seconds):
    """
    formats seconds into H:m:s format
    :param seconds: duration of video
    :return: string
    """
    duration = str(datetime.timedelta(seconds=seconds))
    return duration[:duration.find(".")]


def get_median_frame(video):
    """
    get frame in middle of video
    :param video: path of video
    :return: image
    """
    cap = cv2.VideoCapture(video)
    i = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) / 2)
    cap.set(1, i)
    ret, frame = cap.read()
    return frame


def save_audio(video, output):
    """
    saves audio from a video file
    :param video: path of video
    :param output: path of audio to be saved
    """
    my_clip = mp.VideoFileClip(r"" + video)
    my_clip.audio.write_audiofile(r"" + output, verbose=False, logger=None)


def frame_to_audio(frame_nbr, frame_rate, fs, audio):
    """
    get audio from frame
    :param frame_nbr: frame number
    :param frame_rate: frames per second
    :param fs: frequencies of audio
    :param audio: audio values of audio
    :return audio part corresponding to the frame
    """
    start_index = int(frame_nbr / frame_rate * fs)
    end_index = int((frame_nbr + 1) / frame_rate * fs)
    return audio[start_index:end_index]


def get_duration(video):
    """
    get duration of video in seconds
    :param video: path of video
    :return: duration
    """
    cap = cv2.VideoCapture(video)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_rate = cap.get(cv2.CAP_PROP_FPS)
    return int(frame_count / frame_rate)


def get_frame_rate(video):
    """
    get frame rate of video
    :param video: path of video
    :return: fps
    """
    cap = cv2.VideoCapture(video)
    return cap.get(cv2.CAP_PROP_FPS)


def get_frame_count(video):
    """
    get total frame count in a video
    :param video: path of video
    :return: frame count
    """
    cap = cv2.VideoCapture(video)
    return int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
