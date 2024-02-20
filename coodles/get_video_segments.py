import os
import ffmpeg
import yt_dlp
from coodles.utils import load_json_file


def download_video_segments(coodles_file_path: str) -> None:
    """
    Download video segments defined in the coodles JSON file.
    """
    coodles = load_json_file(coodles_file_path)
    for index, coodle in enumerate(coodles):
        download_video_segment(
            coodle["id"], coodle["start_time"], coodle["duration"], index
        )


def download_video_segment(
    video_id: str, start_time: str, duration: str, counter: int
) -> None:
    """
    Download a specific video segment given the video ID, start time, and duration.
    """
    with yt_dlp.YoutubeDL({"ignoreerrors": True}) as ydl:
        playd = ydl.extract_info(video_id, download=False)
        video_url, audio_url = None, None
        for format in playd.get("formats", []):
            if format["format_id"] in ["136", "135"]:
                video_url = format["url"]
            elif format["format_id"] == "140":
                audio_url = format["url"]

        if not (video_url and audio_url):
            print(f"Unable to download video segment for video ID {video_id}")
            return

        output_path = f"videos/{counter}_{sanitize_filename(playd['title'])}.mp4"

        # Check if video exists
        if file_exists(output_path):
            print(f" Coodles - {output_path} - File has been already downloaded!")
        else:
            try:
                download_and_merge_media(
                    video_url, audio_url, start_time, duration, output_path
                )
            except Exception as e:
                print(f"An error occurred: {e}")


def file_exists(relative_path: str) -> bool:
    """
    Check if the file exists
    """
    absolute_path = os.path.abspath(relative_path)
    if os.path.exists(absolute_path):
        return True
    else:
        return False


def sanitize_filename(title: str) -> str:
    """
    Sanitize the filename to remove forbidden characters.
    """
    return title.replace("/", "_").replace("\\", "_").replace(" ", "_")


def download_and_merge_media(
    video_url: str, audio_url: str, start_time: str, duration: str, output_path: str
) -> None:
    """
    Download and merge the video and audio media into a single MP4 file.
    """
    print("entering ffmpeg")
    mp4_vid = ffmpeg.input(video_url, ss=start_time, t=duration)
    mp4_aud = ffmpeg.input(audio_url, ss=start_time, t=duration)
    ffmpeg.concat(mp4_vid["v"], mp4_aud["a"], v=1, a=1).output(output_path).run()
