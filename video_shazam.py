import argparse
import os
import shutil

from src.cropping import cropping
from src.localization import localization

TEMP_DIR = "./temp/"
CROPPED_PATH = TEMP_DIR + "cropped.mp4"


def video_shazam(input_path):
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)
    os.makedirs(TEMP_DIR)

    screen = localization(input_path)
    cropping(screen, input_path, CROPPED_PATH)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Video Shazam")
    parser.add_argument("--input_path", help="path to input video",
                        default="./input/BlackKnight/BlackKnight_fixed_short1.mp4")
    args = parser.parse_args()

    video_shazam(args.input_path)
