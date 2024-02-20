import json


def load_json_file(file_path: str) -> None:
    """Load JSON data from a file."""

    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file: {file_path}")
        return []


def save_json_file(file_path: str, data: list) -> None:
    """Save processed data to a JSON file."""

    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)


yt_channel_id = "UCu6mSoMNzHQiBIOCkHUa2Aw"
