from coodles.utils import load_json_file, save_json_file, yt_channel_id
import yt_dlp
import json


def get_channel_metadata() -> None:
    """
    Fetch the metadata of a YouTube channel and save it to a JSON file.
    """
    channel_url = f"https://www.youtube.com/channel/{yt_channel_id}"

    # Configure options for youtube-dl
    ydl_opts = {
        "quiet": True,
        "extract_flat": True,
        "dump_single_json": True,
    }

    # Use yt_dlp to extract channel information
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(channel_url, download=False)

    channel_metadata = info_dict["entries"]

    # Save the channel metadata to a JSON file
    channel_metadata_file_path = f"data/channel_metadata_{yt_channel_id}.json"
    with open(channel_metadata_file_path, "w") as outfile:
        json.dump(channel_metadata, outfile, indent=4)


def get_thumbnail_url(thumbnails: list) -> str:
    """Retrieve thumbnail URL for a video entry."""

    for thumbnail in thumbnails:
        if thumbnail["height"] > 138:
            return thumbnail["url"]
    return None


def process_channel_data() -> None:
    """
    Process channel data from a JSON file and save the processed
    data to another JSON file.
    """

    channel_json_file_path = f"data/channel_metadata_{yt_channel_id}.json"
    channel_data = load_json_file(channel_json_file_path)

    processed_channel_data = []
    for category_entry in channel_data:
        for video_entry in category_entry["entries"]:
            video_data = {
                "id": video_entry["id"],
                "url": video_entry["url"],
                "title": video_entry["title"],
                "duration": video_entry["duration"],
                "view_count": video_entry["view_count"],
                "thumbnail_url": get_thumbnail_url(video_entry["thumbnails"]),
            }
            processed_channel_data.append(video_data)

    processed_json_file_path = f"data/channel_metadata_processed_{yt_channel_id}.json"
    save_json_file(processed_json_file_path, processed_channel_data)


def download_channel_metadata() -> None:
    """
    Download metadata of a youtube channel and process it, saves the data as
    two JSON files.
    """
    get_channel_metadata()
    process_channel_data()
