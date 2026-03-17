import json
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import openai

from schemas import (
    TranscriptRequest, TranscriptResponse,
    SummarizeRequest, SummarizeResponse,
    AskRequest, AskResponse,
)
from services import transcript as transcript_service
from services import summarize as summarize_service
from services import qa as qa_service

_config = json.loads((Path(__file__).parent.parent / "config.json").read_text())
openai.api_key = _config["OPENAI_API_KEY"]

app = FastAPI(title="YT Summarizer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/transcript", response_model=TranscriptResponse)
def get_transcript(req: TranscriptRequest):
    text, video_id = transcript_service.get_transcript(req.url)
    return TranscriptResponse(transcript=text, video_id=video_id)


@app.post("/api/summarize", response_model=SummarizeResponse)
def summarize(req: SummarizeRequest):
    summary = summarize_service.summarize(req.transcript, req.format)
    return SummarizeResponse(summary=summary)


@app.post("/api/ask", response_model=AskResponse)
def ask(req: AskRequest):
    answer = qa_service.answer_question(req.transcript, req.question)
    return AskResponse(answer=answer)


@app.get("/")
def root():
    return {"message": "API is running"}