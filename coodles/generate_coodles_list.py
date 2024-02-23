from coodles.utils import save_json_file
import os


def generate_coodles_json() -> None:
    coodles = {}
    # Path to the directory you want to list the files from
    directory_path = "./videos/"
    # The output JSON file where the list of files will be stored
    output_json_file = "./data/coodles_videos.json"

    # List all files in the directory
    files_list = os.listdir(directory_path)
    coodles["coodles"] = files_list

    # Store the list in a JSON file
    save_json_file(output_json_file, coodles)
