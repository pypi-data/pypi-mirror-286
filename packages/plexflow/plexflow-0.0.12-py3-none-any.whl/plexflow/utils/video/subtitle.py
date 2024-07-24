import subprocess
import json
from pydantic import BaseModel
from typing import List, Optional

class SubtitleStream(BaseModel):
    index: int
    lang: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "index": 0,
                "lang": "en"
            }
        }

def get_subtitles(video_path: str) -> List[SubtitleStream]:
    """
    Function to get subtitle streams from a video file.

    Args:
        video_path (str): The path to the video file.

    Returns:
        List[SubtitleStream]: A list of SubtitleStream objects, each representing a subtitle stream.

    Raises:
        FileNotFoundError: If the video file does not exist.
        ValueError: If the output from the command could not be parsed.

    Examples:
        >>> video_path = "/path/to/your/video.mp4"
        >>> try:
        ...     subtitles = get_subtitles(video_path)
        ...     for subtitle in subtitles:
        ...         print(f"Subtitle stream index: {subtitle.index}, language: {subtitle.lang}")
        ... except FileNotFoundError:
        ...     print(f"The video file {video_path} does not exist.")
        ... except ValueError:
        ...     print("There was a problem parsing the command output.")
        ...
        Subtitle stream index: 0, language: en
        Subtitle stream index: 1, language: es
    """
    if not os.path.isfile(video_path):
        raise FileNotFoundError(f"No such file: '{video_path}'")

    command = [
        'ffprobe',
        '-v', 'quiet',
        '-print_format', 'json',
        '-show_streams',
        '-select_streams', 's',
        video_path
    ]

    output = subprocess.run(command, capture_output=True, text=True)

    try:
        probe = json.loads(output.stdout)
    except json.JSONDecodeError as e:
        raise ValueError("Could not parse command output") from e

    subtitle_streams = []
    for stream in probe['streams']:
        subtitle_info = SubtitleStream(
            index=stream['index'],
            lang=stream['tags']['language'] if 'tags' in stream and 'language' in stream['tags'] else None
        )
        subtitle_streams.append(subtitle_info)

    return subtitle_streams
