import sys
import argparse
from .get_channel_metadata import download_channel_metadata
from .get_video_segments import download_video_segments
from .get_elements_data import get_elements_videos
from .generate_coodles_list import generate_coodles_json

__version__ = "0.0.1"


def main(argv=None):
    argv = sys.argv if argv is None else argv
    cliparser = argparse.ArgumentParser()
    cliparser.add_argument(
        "-j",
        "--download-json",
        help="Download metadata of the Cody's Lab channel",
        action="store_true",
    )

    cliparser.add_argument(
        "-v",
        "--download-videos",
        help="Download channel videos with unique intro titles",
        action="store_true",
    )

    args = cliparser.parse_args()

    if args.download_json:
        print("Downloading channel metadata...")
        download_channel_metadata()
        get_elements_videos()
        generate_coodles_json()

    if args.download_videos:
        print("Downloading coodles...")
        download_video_segments("./data/coodles.json")
