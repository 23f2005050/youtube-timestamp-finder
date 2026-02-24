import yt_dlp
import uuid
import whisper
import os

# Load Whisper model once (IMPORTANT for speed)
whisper_model = whisper.load_model("tiny")


def download_audio(url):
    filename = f"{uuid.uuid4()}.mp3"

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': filename,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }],
        'quiet': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return filename


def transcribe_audio(filepath):
    result = whisper_model.transcribe(filepath)

    transcript = result["text"]
    segments = result["segments"]

    return transcript, segments


def find_timestamp_from_segments(topic, segments):
    topic = topic.lower()

    for segment in segments:
        if topic in segment["text"].lower():
            return int(segment["start"])

    return None


def format_time(seconds):
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60

    return f"{h:02}:{m:02}:{s:02}"


def cleanup(filepath):
    if os.path.exists(filepath):
        os.remove(filepath)