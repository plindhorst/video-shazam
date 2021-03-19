import argparse
import os
import shutil
import datetime

from code.cropping import cropping
from code.database import Database
from code.localization import localization
import time

from code.matching import matching
from code.util.log import log
from code.util.video import save_audio, get_duration

MIN_DURATION = 30

VIDEOS_PATH = "./videos/"
DATABASE_PATH = VIDEOS_PATH + "database.db"

TEMP_DIR = "./temp/"
CROPPED_PATH = TEMP_DIR + "cropped.mp4"
AUDIO_PATH = TEMP_DIR + "audio.wav"


def video_shazam(input_path, verbose=False):
    if get_duration(input_path) < MIN_DURATION:
        log("\nError: input video is shorter than " + str(MIN_DURATION) + "s", verbose)
        return None
    try:
        if os.path.exists(TEMP_DIR):
            shutil.rmtree(TEMP_DIR)
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

    save_audio(input_path, AUDIO_PATH)
    screen = localization(input_path, verbose)
    cropping(screen, input_path, CROPPED_PATH)

    log("\n--- Matching started ---", verbose)

    matches = matching(CROPPED_PATH, AUDIO_PATH, database, verbose)

    log("\n--- Results ---", verbose)
    n = 3
    for i, match in enumerate(matches):
        if i == n:
            break
        log("Match " + str(i + 1) + ": " + match[0] + " (" + str(match[1]) + ")", verbose)

    database.close()

    log("\n--- Finished in " + str(datetime.timedelta(seconds=(time.time() - start_time))) + " ---", verbose)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Video Shazam")
    parser.add_argument("--input_path", help="path to input video",
                        default="./input/BlackKnight/BlackKnight_fixed_short1.mp4")
    parser.add_argument("--verbose", help="produce log output", default=False, type=bool)
    args = parser.parse_args()

    video_shazam(args.input_path, args.verbose)
