import json

import numpy as np

from code.util.features import get_features, normalize
from code.util.log import log
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
    score_colorhists = sliding_window(features_video["colorhists"], features_input["colorhists"], euclidean_norm_mean)[
        1]
    score_tempdiffs = sliding_window(features_video["tempdiffs"], features_input["tempdiffs"], euclidean_norm)[1]
    score_colorhistdiffs = \
        sliding_window(features_video["colorhistdiffs"], features_input["colorhistdiffs"], euclidean_norm)[1]
    score_audiopowers = sliding_window(features_video["audiopowers"], features_input["audiopowers"], euclidean_norm)[1]
    return score_colorhists, score_tempdiffs, score_colorhistdiffs, score_audiopowers


def euclidean_norm_mean(x, y):
    x = np.mean(x, axis=0)
    y = np.mean(y, axis=0)
    return np.linalg.norm(x - y)


def euclidean_norm(x, y):
    return np.linalg.norm(np.array(x) - np.array(y))


def matching(video_path, audio_path, database, verbose=False):
    features_input = get_features(video_path, audio_path)
    duration_input = get_duration(video_path)

    videos = database.get_video_names()

    scores_features = {"colorhists": [], "tempdiffs": [], "colorhistdiffs": [], "audiopowers": []}
    for video in videos:
        features_video = database.get_features(video)

        duration = features_video[1]
        if duration < duration_input:
            log("Error: query is longer than database video \"" + video + "\"", verbose)
            continue

        log("Matching with \"" + video + "\"", verbose)
        features_video = {'colorhists': json.loads(features_video[2]),
                          'tempdiffs': json.loads(features_video[3]),
                          'colorhistdiffs': json.loads(features_video[4]), 'audiopowers': json.loads(features_video[5]),
                          'mfccs': []}

        match = score(features_video, features_input)
        scores_features["colorhists"].append(match[0])
        scores_features["tempdiffs"].append(match[1])
        scores_features["colorhistdiffs"].append(match[2])
        scores_features["audiopowers"].append(match[3])

    scores_features["colorhists"] = normalize(scores_features["colorhists"])
    scores_features["tempdiffs"] = normalize(scores_features["tempdiffs"])
    scores_features["colorhistdiffs"] = normalize(scores_features["colorhistdiffs"])
    scores_features["audiopowers"] = normalize(scores_features["audiopowers"])

    scores = []
    for i, video in enumerate(videos):
        scores.append(np.mean(
            [scores_features["colorhists"][i], scores_features["tempdiffs"][i], scores_features["colorhistdiffs"][i],
             scores_features["audiopowers"][i]]))

    matches = []
    idx = np.argsort(scores)
    for i in idx:
        matches.append((videos[i], round(scores[i], 2)))
    return matches
