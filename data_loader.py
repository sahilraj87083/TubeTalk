from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from urllib.parse import urlparse, parse_qs



def get_transcript(video_id):
    try:
        ytt_api = YouTubeTranscriptApi()
        transcript_list = ytt_api.list(video_id)
        language_code = None

        # Step 1: Try English transcript
        try:
            transcript = transcript_list.find_transcript(['en'])
            fetched_transcript = transcript.fetch()
            language_code = transcript.language_code
            
        except Exception:
            # Step 1b: Try Hindi transcript if English not found
            try :
                hinditranscript = transcript_list.find_transcript(['hi'])
                fetched_transcript = hinditranscript.fetch()
                language_code = hinditranscript.language_code


            except Exception:
                raise NoTranscriptFound("No English or Hindi transcript available.")
        
        full_transcript = " ".join([entry.text for entry in fetched_transcript])
        return full_transcript, language_code
        

    except NoTranscriptFound:
        print("❌ No captions found for this video.")
        return None

    except TranscriptsDisabled:
        print("❌ Captions are disabled for this video.")
        return None
    


def get_youtube_id(url: str) -> str:
    """
    Strictly extracts the YouTube video ID (11 characters).
    Works for watch, youtu.be, and embed formats.
    """
    parsed_url = urlparse(url)

    # Case 1: Standard YouTube URL -> ?v=VIDEO_ID
    if parsed_url.hostname in ["www.youtube.com", "youtube.com"]:
        query_params = parse_qs(parsed_url.query)
        if "v" in query_params:
            return query_params["v"][0]

        # Case 2: Embed format -> /embed/VIDEO_ID
        if parsed_url.path.startswith("/embed/"):
            return parsed_url.path.split("/")[2]

    # Case 3: Short youtu.be link -> /VIDEO_ID
    if parsed_url.hostname == "youtu.be":
        return parsed_url.path.lstrip("/")

    return None

