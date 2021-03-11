import argparse

from src.localization import localization


def video_shazam(input_path, debug=False):
    center, size, angle = localization(input_path, debug)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Video Shazam")
    parser.add_argument("--input_path", help="path to input video",
                        default="./input/BlackKnight/BlackKnight_fixed_short1.mp4")
    parser.add_argument("--debug", help="show every step for debugging", default=False, type=bool)
    args = parser.parse_args()

    video_shazam(args.input_path, args.debug)
