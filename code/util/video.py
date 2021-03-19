import cv2
import moviepy.editor as mp


def get_median_frame(video):
    cap = cv2.VideoCapture(video)
    i = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) / 2)
    cap.set(1, i)
    ret, frame = cap.read()
    return frame


def save_audio(video, output):
    my_clip = mp.VideoFileClip(r"" + video)
    my_clip.audio.write_audiofile(r"" + output, verbose=False, logger=None)


def frame_to_audio(frame_nbr, frame_rate, fs, audio):
    start_index = int(frame_nbr / frame_rate * fs)
    end_index = int((frame_nbr + 1) / frame_rate * fs)
    return audio[start_index:end_index]


def get_duration(video):
    cap = cv2.VideoCapture(video)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_rate = cap.get(cv2.CAP_PROP_FPS)
    return int(frame_count / frame_rate)


def get_frame_rate(video):
    cap = cv2.VideoCapture(video)
    return cap.get(cv2.CAP_PROP_FPS)


def get_frame_count(video):
    cap = cv2.VideoCapture(video)
    return int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
