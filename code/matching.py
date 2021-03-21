import time

import numpy as np

from code.util.features import get_features, normalize
from code.util.log import log
from code.util.video import get_duration, format_duration


def sliding_window(x, w):
    """
    get window with smallest difference
    :param x: features to match against
    :param w: features of our input video
    :return: center, size and angle of the screen
    """
    wl = len(w)
    min_diff = float("inf")
    # Find smallest difference
    for i in range(len(x) - wl):
        min_diff = np.minimum(min_diff, abs_diff(w, x[i:(i + wl)]))
    return min_diff


def score(features_video, features_input):
    """
    computes scores for each feature
    :param features_video: features of database video
    :param features_input: features of input video
    :return: tuple of scores
    """
    score_colorhists = sliding_window(features_video["colorhists"], features_input["colorhists"])
    return score_colorhists


def abs_diff(x, y):
    return np.sum(np.absolute(np.array(x) - np.array(y)))


def matching(video_path, database, verbose=False):
    """
    return list of matches with their scores
    :param video_path: path of input video
    :param database: database of features to match against
    :param verbose: option to display information
    :return: list of matches with their scores in ascending order
    """

    #  compute features for the input video
    features_input = get_features(video_path)
    duration_input = get_duration(video_path)

    # retrieve video names from database
    videos = database.get_video_names()

    scores_features = {"colorhists": []}

    matched_videos = []
    for i, video in enumerate(videos):
        # retrieve video features from database
        duration, features_video = database.get_features(video)

        # check that input video is longer than the video in the database
        if duration < duration_input:
            log("Error: query is longer than database video \"" + video + "\"", verbose)
            continue

        log("Matching with \"" + video + "\" (" + format_duration(duration) + ") (" + str(i + 1) + "/" + str(
            len(videos)) + ")", verbose)
        start_time = time.time()
        matched_videos.append(video)

        #  compute dissimilarity score between the feature arrays
        match = score(features_video, features_input)
        scores_features["colorhists"].append(match)

        log("Score (" + format_duration((time.time() - start_time)) + "): " + str(round(match, 2)) + " (colorhists)",
            verbose)

    # Normalize scores
    scores_features["colorhists"] = normalize(scores_features["colorhists"])

    # Combine scores
    scores = []
    for i, video in enumerate(matched_videos):
        scores.append(scores_features["colorhists"][i])

    # Sort matches by increasing dissimilarity
    matches = []
    idx = np.argsort(scores)
    for i in idx:
        matches.append((matched_videos[i], round(scores[i], 2)))
    return matches
