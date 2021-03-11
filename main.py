import argparse

from src.localisation import localisation


def video_shazam(input_path):
    localisation(input_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Video Shazam")
    parser.add_argument("--input_path", help="path to input video", default="./input/BlackKnight/BlackKnight_fixed_long.mp4")
    args = parser.parse_args()

    video_shazam(args.input_path)
