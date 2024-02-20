from coodles.utils import load_json_file, save_json_file, yt_channel_id
from typing import List, Set
import periodictable


def find_elements_in_sentence(elements: list, sentence: str) -> Set[str]:
    element_set = set(elements)

    words = sentence.lower().split()

    # Find and return the set of matched elements
    return {word.lower() for word in words if word.lower() in element_set}


def get_chemical_elements() -> List[str]:
    """
    Returns the list of periodic elements
    """
    chemical_elements = [
        element.name for element in periodictable.elements if element.number > 0
    ]
    return chemical_elements


def get_elements_videos() -> None:
    channel_json_file_path = f"data/channel_metadata_processed_{yt_channel_id}.json"
    videos_with_elements = []
    elements = get_chemical_elements()
    channel_processed_data = load_json_file(channel_json_file_path)
    for entry in channel_processed_data:
        matches = find_elements_in_sentence(elements, entry["title"])
        if matches:
            video_with_element = {
                "id": entry.get("id"),
                "title": entry.get("title"),
                "elements": list(matches),
                "url": entry.get("url"),
                "view_count": entry.get("view_count"),
                "thumbnail_url": entry.get("thumbnail_url"),
            }
            videos_with_elements.append(video_with_element)

    video_elements_file_path = f"data/channel_videos_elements_{yt_channel_id}.json"
    save_json_file(video_elements_file_path, videos_with_elements)


get_elements_videos()
