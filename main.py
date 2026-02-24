from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os

from utils import (
    download_audio,
    transcribe_audio,
    find_timestamp_from_segments,
    format_time,
    cleanup
)

load_dotenv()

app = FastAPI()


class AskRequest(BaseModel):
    video_url: str
    topic: str


@app.post("/ask")
def ask(request: AskRequest):

    audio_file = download_audio(request.video_url)

    try:
        transcript, segments = transcribe_audio(audio_file)

        seconds = find_timestamp_from_segments(request.topic, segments)

        if seconds is None:
            raise HTTPException(
                status_code=404,
                detail="Topic not found in video"
            )

        timestamp = format_time(seconds)

        return {
            "timestamp": timestamp,
            "video_url": request.video_url,
            "topic": request.topic
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:
        cleanup(audio_file)