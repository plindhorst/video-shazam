import json

import numpy as np

from code.util.features import get_features
from code.util.video import get_duration


def sliding_window(x, w, compare_func):
    wl = len(w)
    diffs = []
    for i in range(len(x) - wl):
        diff = compare_func(w, x[i:(i + wl)])
        diffs.append(diff)
    return np.sum(diffs) / len(diffs)


def score(features_video, features_input):
    score_colorhists = sliding_window(features_video["colorhists"], features_input["colorhists"], euclidean_norm_mean)
    # score_tempdiffs = sliding_window(features_video["tempdiffs"], features_input["tempdiffs"], euclidean_norm)
    # score_colorhistdiffs = sliding_window(features_video["colorhistdiffs"], features_input["colorhistdiffs"], euclidean_norm)
    return score_colorhists


def euclidean_norm_mean(x, y):
    x = np.mean(x, axis=0)
    y = np.mean(y, axis=0)
    return np.linalg.norm(x - y)


def euclidean_norm(x, y):
    return np.linalg.norm(np.array(x) - np.array(y))


def matching(input_path, database):
    features_input = get_features(input_path)

    videos = database.get_video_names()

    scores = []
    for video in videos:
        features_video = database.get_features(video)

        duration = features_video[1]
        if duration < get_duration(input_path):
            print("Error: query is longer than database video \"" + video + "\"")
            continue

        features_video = {'colorhists': json.loads(features_video[2]),
                          'tempdiffs': json.loads(features_video[3]),
                          'colorhistdiffs': json.loads(features_video[4]), 'audiopowers': [], 'mfccs': []}

        scores.append(score(features_video, features_input))

    matches = []
    idx = np.argsort(scores)
    for i in idx:
        matches.append((videos[i], scores[i]))
    return matches
