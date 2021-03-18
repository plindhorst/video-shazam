import argparse
import os
import shutil

from code.cropping import cropping
from code.database import Database
from code.localization import localization
import time

from code.matching import matching
from code.util.video import save_audio

VIDEOS_PATH = "./videos/"
DATABASE_PATH = VIDEOS_PATH + "database.db"

TEMP_DIR = "./temp/"
CROPPED_PATH = TEMP_DIR + "cropped.mp4"
AUDIO_PATH = TEMP_DIR + "audio.wav"


def video_shazam(input_path):
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)
    os.makedirs(TEMP_DIR)

    save_audio(input_path, AUDIO_PATH)
    start_time = time.time()

    database = Database(DATABASE_PATH)
    database.create()
    database.build(VIDEOS_PATH)

    screen = localization(input_path)
    cropping(screen, input_path, CROPPED_PATH)
    matches = matching(CROPPED_PATH, AUDIO_PATH, database)
    for i, match in enumerate(matches):
        print("Match " + str(i) + ": " + match[0] + " (" + str(match[1]) + ")")

    database.close()

    print("\n--- finished in %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Video Shazam")
    parser.add_argument("--input_path", help="path to input video",
                        default="./input/BlackKnight/BlackKnight_fixed_short1.mp4")
    args = parser.parse_args()

    video_shazam(args.input_path)
