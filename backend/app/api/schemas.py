from datetime import datetime
from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    app: str
    version: str


class ModelInfo(BaseModel):
    stt_models: list[str]
    tts_models: list[str]


class HistoryRecord(BaseModel):
    id: int
    kind: str
    input_path: str | None
    output_path: str | None
    transcript: str | None
    confidence: float | None
    voice: str | None
    rate: float | None
    pitch: float | None
    created_at: datetime


class TTSRequest(BaseModel):
    text: str
    voice: str = "tts_models/en/ljspeech/tacotron2-DDC"
    rate: float = 1.0
    pitch: float = 1.0
