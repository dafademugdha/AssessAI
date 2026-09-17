from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs


def extract_video_id(url: str) -> str:
    """
    Extract YouTube video ID from different YouTube URL formats.
    """

    parsed_url = urlparse(url)

    # https://www.youtube.com/watch?v=VIDEO_ID
    if "youtube.com" in parsed_url.netloc:
        video_id = parse_qs(parsed_url.query).get("v")

        if video_id:
            return video_id[0]

    # https://youtu.be/VIDEO_ID
    if "youtu.be" in parsed_url.netloc:
        return parsed_url.path.strip("/")

    raise ValueError("Invalid YouTube URL")


def extract_text_from_youtube(url: str) -> str:
    """
    Extract transcript text from a YouTube video.
    """

    video_id = extract_video_id(url)

    # Create API instance
    ytt_api = YouTubeTranscriptApi()

    # Fetch transcript
    transcript = ytt_api.fetch(video_id)

    # Convert transcript snippets into plain text
    text = " ".join(
        snippet.text
        for snippet in transcript
    )

    return text.strip()