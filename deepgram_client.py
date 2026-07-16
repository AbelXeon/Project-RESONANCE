from deepgram import DeepgramClient
from config import DEEPGRAM_API_KEY

dg_client = DeepgramClient(api_key=DEEPGRAM_API_KEY)


def transcribe_audio(file_path: str) -> str:
    """Takes a path to a local audio file (e.g. downloaded .ogg voice note)
    and returns the transcribed text."""
    with open(file_path, "rb") as f:
        audio_data = f.read()

    response = dg_client.listen.v1.media.transcribe_file(
        request=audio_data,
        model="nova-3",
        smart_format=True,
    )

    transcript = response.results.channels[0].alternatives[0].transcript
    return transcript