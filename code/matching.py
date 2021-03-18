import json

import numpy as np

from code.util.features import get_features
from code.util.video import get_duration, get_frame_rate


def sliding_window(x, w, compare_func):
    wl = len(w)
    diffs = []
    for i in range(len(x) - wl):
        diff = compare_func(w, x[i:(i + wl)])
        diffs.append(diff)

    idxs = np.argsort(diffs)

    return (idxs[0], diffs[idxs[0]])


def score(features_video, features_input):
    score_colorhists = sliding_window(features_video["colorhists"], features_input["colorhists"], euclidean_norm_mean)
    # score_tempdiffs = sliding_window(features_video["tempdiffs"], features_input["tempdiffs"], euclidean_norm_mean)
    # score_colorhistdiffs = sliding_window(features_video["colorhistdiffs"], features_input["colorhistdiffs"], euclidean_norm)
    # score_audiopowers = sliding_window(features_video["audiopowers"], features_input["audiopowers"], euclidean_norm)
    return score_colorhists


def euclidean_norm_mean(x, y):
    x = np.mean(x, axis=0)
    y = np.mean(y, axis=0)
    return np.linalg.norm(x - y)


def euclidean_norm(x, y):
    return np.linalg.norm(np.array(x) - np.array(y))


def matching(video_path, audio_path, database):
    features_input = get_features(video_path, audio_path)
    frame_rate_input = get_frame_rate(video_path)
    duration_input = get_duration(video_path)

    videos = database.get_video_names()

    scores = []
    for video in videos:
        features_video = database.get_features(video)

        duration = features_video[1]
        if duration < duration_input:
            print("Error: query is longer than database video \"" + video + "\"")
            continue

        features_video = {'colorhists': json.loads(features_video[2]),
                          'tempdiffs': json.loads(features_video[3]),
                          'colorhistdiffs': json.loads(features_video[4]), 'audiopowers': json.loads(features_video[5]),
                          'mfccs': []}

        match = score(features_video, features_input)
        scores.append(match[1])

    matches = []
    idx = np.argsort(scores)
    for i in idx:
        matches.append((videos[i], round(scores[i], 2)))
    return matches
