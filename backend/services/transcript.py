import re
from fastapi import HTTPException
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled


def parse_video_id(url: str) -> str:
    patterns = [
        r"(?:v=)([A-Za-z0-9_-]{11})",
        r"(?:youtu\.be/)([A-Za-z0-9_-]{11})",
        r"(?:shorts/)([A-Za-z0-9_-]{11})",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    raise HTTPException(status_code=400, detail="Could not parse a valid YouTube video ID from the URL.")


def get_transcript(url: str) -> tuple[str, str]:
    video_id = parse_video_id(url)
    try:
        ytt_api = YouTubeTranscriptApi()
        segments = ytt_api.fetch(video_id)
    except (NoTranscriptFound, TranscriptsDisabled):
        raise HTTPException(status_code=400, detail="No captions available for this video.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch transcript: {str(e)}")

    transcript = " ".join(seg.text for seg in segments)
    return transcript, video_id
