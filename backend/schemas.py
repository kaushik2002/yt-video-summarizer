from typing import Literal
from pydantic import BaseModel


class TranscriptRequest(BaseModel):
    url: str


class TranscriptResponse(BaseModel):
    transcript: str
    video_id: str


class SummarizeRequest(BaseModel):
    transcript: str
    format: Literal["paragraph", "bullets", "chapters"]


class SummarizeResponse(BaseModel):
    summary: str


class AskRequest(BaseModel):
    transcript: str
    question: str


class AskResponse(BaseModel):
    answer: str
