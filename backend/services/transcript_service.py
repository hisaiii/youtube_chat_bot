"""Everything related to pulling a transcript off YouTube."""
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled


def extract_video_transcript(video_id: str) -> str | None:
    """Fetch and flatten a video's English transcript into one string.
    Returns None if transcripts are disabled or fetching fails.
    """
    print(f"🔍 Fetching transcript for: {video_id}")
    try:
        ytt_api = YouTubeTranscriptApi()
        fetched_transcript = ytt_api.fetch(video_id, languages=["en"])

        transcript_segments = []
        for chunk in fetched_transcript:
            # Handles both object (new API) and dict (old API) shapes
            if hasattr(chunk, "text"):
                transcript_segments.append(chunk.text)
            else:
                transcript_segments.append(chunk["text"])

        return " ".join(transcript_segments)

    except TranscriptsDisabled:
        print(f"FAIL: Transcripts are disabled for video {video_id}")
        return None
    except Exception as e:
        print(f"Unexpected error fetching transcript: {e}")
        return None
