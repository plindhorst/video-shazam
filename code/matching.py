import numpy as np

from code.util.features import get_features, normalize
from code.util.log import log
from code.util.video import get_duration


def sliding_window(x, w, compare_func):
    """
    get window with smallest difference
    :param x: features to match against
    :param w: features of our input video
    :param compare_func: dissimilarity function
    :return: center, size and angle of the screen
    """
    wl = len(w)
    min_diff = float("inf")
    # Find smallest difference
    for i in range(len(x) - wl):
        min_diff = np.minimum(min_diff, compare_func(w, x[i:(i + wl)]))
    return min_diff


def score(features_video, features_input):
    """
    computes scores for each feature
    :param features_video: features of database video
    :param features_input: features of input video
    :return: tuple of scores
    """
    score_colorhists = sliding_window(features_video["colorhists"], features_input["colorhists"], euclidean_norm_mean)
    score_tempdiffs = sliding_window(features_video["tempdiffs"], features_input["tempdiffs"], euclidean_norm)
    score_colorhistdiffs = \
        sliding_window(features_video["colorhistdiffs"], features_input["colorhistdiffs"], euclidean_norm)
    score_audiopowers = sliding_window(features_video["audiopowers"], features_input["audiopowers"], euclidean_norm)
    return score_colorhists, score_tempdiffs, score_colorhistdiffs, score_audiopowers


def euclidean_norm_mean(x, y):
    """
    computes euclidean distance around mean
    :param x: first array
    :param y: second array
    :return: normalized distance
    """
    x = np.mean(x, axis=0)
    y = np.mean(y, axis=0)
    return np.linalg.norm(x - y)


def euclidean_norm(x, y):
    """
    computes euclidean distance
    :param x: first array
    :param y: second array
    :return: normalized distance
    """
    return np.linalg.norm(np.array(x) - np.array(y))


def matching(video_path, audio_path, database, verbose=False):
    """
    return list of matches with their scores
    :param video_path: path of input video
    :param audio_path: path of input audio
    :param database: database of features to match against
    :param verbose: option to display information
    :return: list of matches with their scores in ascending order
    """

    #  compute features for the input video
    features_input = get_features(video_path, audio_path)
    duration_input = get_duration(video_path)

    # retrieve video names from database
    videos = database.get_video_names()

    scores_features = {"colorhists": [], "tempdiffs": [], "colorhistdiffs": [], "audiopowers": []}

    for video in videos:
        # retrieve video features from database
        duration, features_video = database.get_features(video)

        # check that input video is longer than the video in the database
        if duration < duration_input:
            log("Error: query is longer than database video \"" + video + "\"", verbose)
            continue
        log("Matching with \"" + video + "\"", verbose)

        #  compute dissimilarity score between the feature arrays
        match = score(features_video, features_input)
        scores_features["colorhists"].append(match[0])
        scores_features["tempdiffs"].append(match[1])
        scores_features["colorhistdiffs"].append(match[2])
        scores_features["audiopowers"].append(match[3])

        log("Scores: " + str(round(match[0], 2)) + " (colorhists), " + "{:,}".format(
            int(match[1])) + " (tempdiffs), " + "{:,}".format(
            int(match[2])) + " (colorhistdiffs), " + "{:,}".format(int(match[3])) + " (audiopowers)", verbose)

    # Normalize scores
    scores_features["colorhists"] = normalize(scores_features["colorhists"])
    scores_features["tempdiffs"] = normalize(scores_features["tempdiffs"])
    scores_features["colorhistdiffs"] = normalize(scores_features["colorhistdiffs"])
    scores_features["audiopowers"] = normalize(scores_features["audiopowers"])

    # Combine scores
    scores = []
    for i, video in enumerate(videos):
        scores.append(np.mean(
            [scores_features["colorhists"][i], scores_features["tempdiffs"][i], scores_features["colorhistdiffs"][i],
             scores_features["audiopowers"][i]]))

    # Sort matches by increasing dissimilarity
    matches = []
    idx = np.argsort(scores)
    for i in idx:
        matches.append((videos[i], round(scores[i], 2)))
    return matches
