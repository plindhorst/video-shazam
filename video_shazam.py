import argparse
import glob
import ntpath
import os
import time

from code.cropping import cropping
from code.database import Database
from code.localization import localization
from code.matching import matching
from code.stabilizing import stabilizing
from code.util.log import log
from code.util.video import get_duration, format_duration

N_MATCHES = 3
MIN_DURATION = 30

VIDEOS_PATH = "./videos/"
DATABASE_PATH = VIDEOS_PATH + "database.db"

TEMP_DIR = "./temp/"
STABILIZED_PATH = TEMP_DIR + "stabilized.mp4"
CROPPED_PATH = TEMP_DIR + "cropped.mp4"
AUDIO_PATH = TEMP_DIR + "audio.wav"


def video_shazam(input_path, stabilize=False, verbose=False):
    """
    get top 3 matches
    :param input_path: path of input video
    :param stabilize: specifies if we should stabilize the input video
    :param verbose: option to display information
    :return: list of top 3 matches in order
    """
    if not os.path.exists(input_path):
        log("\nError: input video not found \"" + input_path + "\"", verbose)
        return None

    if get_duration(input_path) < MIN_DURATION:
        log("\nError: input video is shorter than " + str(MIN_DURATION) + "s", verbose)
        return None
    try:
        if os.path.exists(TEMP_DIR):
            files = glob.glob(TEMP_DIR + "*")
            for f in files:
                os.remove(f)
        else:
            os.makedirs(TEMP_DIR)
    except PermissionError:
        log("\nError: could not create temp folder", verbose)
        return None

    start_time = time.time()

    log("\n--- Creating database ---", verbose)

    database = Database(DATABASE_PATH)
    database.create()
    database.build(VIDEOS_PATH, verbose)

    log("\n--- Pre-processing started ---", verbose)

    if stabilize:
        log("Stabilizing...", verbose)
        stabilizing(input_path, STABILIZED_PATH)
        input_path = STABILIZED_PATH

    log("Cropping...", verbose)
    screen = localization(input_path, verbose)
    cropping(screen, input_path, CROPPED_PATH)

    log("\n--- Matching started ---", verbose)

    matches = matching(CROPPED_PATH, database, verbose)

    log("\n--- Results for \"" + ntpath.basename(input_path) + "\" ---", verbose)

    for i, match in enumerate(matches):
        if i == N_MATCHES:
            break
        log("Match " + str(i + 1) + ": " + match[0] + " (" + str(match[1]) + ")", verbose)

    database.close()

    log("\n--- Finished in " + format_duration((time.time() - start_time)) + " ---", verbose)

    return matches[:N_MATCHES - 1]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Video Shazam")
    parser.add_argument("--input_path", help="path to input video")
    parser.add_argument("--stabilize", help="stabilize video", default=False, type=bool)
    parser.add_argument("--verbose", help="produce log output", default=True, type=bool)
    args = parser.parse_args()

    video_shazam(args.input_path, args.stabilize, args.verbose)
