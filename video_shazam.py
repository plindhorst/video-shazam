import argparse

from src.cropping import cropping
from src.localization import localization
from src.stabilizing import stabilizing

CROPPED_PATH = "./temp/cropped.mp4"


def video_shazam(input_path):
    stabilizing(input_path, "")
    screen = localization(input_path)
    cropping(screen, input_path, CROPPED_PATH)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Video Shazam")
    parser.add_argument("--input_path", help="path to input video",
                        default="./input/BlackKnight/BlackKnight_fixed_short1.mp4")
    args = parser.parse_args()

    video_shazam(args.input_path)
