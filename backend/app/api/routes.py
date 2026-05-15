import json
from pathlib import Path
from uuid import uuid4

from docx import Document
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy.orm import Session

from app.api.schemas import HealthResponse, HistoryRecord, ModelInfo
from app.core.config import APP_NAME, APP_VERSION, OUTPUT_DIR, UPLOAD_DIR
from app.db.models import ConversionHistory
from app.db.session import get_db
from app.services.model_manager import ModelManager
from app.services.stt_service import ALLOWED_AUDIO, STTService
from app.services.tts_service import TTSService

router = APIRouter(prefix="/api", tags=["api"])
stt_service = STTService(model_name="small")
tts_service = TTSService()


def _save_upload(file: UploadFile, target_dir: Path) -> Path:
    suffix = Path(file.filename or "file").suffix.lower()
    file_path = target_dir / f"{uuid4()}{suffix}"
    with file_path.open("wb") as f:
        f.write(file.file.read())
    return file_path


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", app=APP_NAME, version=APP_VERSION)


@router.get("/models", response_model=ModelInfo)
def models() -> ModelInfo:
    return ModelInfo(
        stt_models=ModelManager.available_stt_models(),
        tts_models=ModelManager.available_tts_models(),
    )


@router.get("/history", response_model=list[HistoryRecord])
def history(db: Session = Depends(get_db)):
    rows = db.query(ConversionHistory).order_by(ConversionHistory.created_at.desc()).all()
    return rows


@router.post("/stt")
def stt(
    file: UploadFile = File(...),
    export_format: str = Form("txt"),
    db: Session = Depends(get_db),
):
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in ALLOWED_AUDIO:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {suffix}")

    audio_path = _save_upload(file, UPLOAD_DIR)
    result = stt_service.transcribe(audio_path)

    transcript_text = result["text"]
    export_format = export_format.lower()
    output_base = OUTPUT_DIR / f"{uuid4()}"

    if export_format == "txt":
        output_path = output_base.with_suffix(".txt")
        output_path.write_text(transcript_text, encoding="utf-8")
    elif export_format == "json":
        output_path = output_base.with_suffix(".json")
        output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    elif export_format == "docx":
        output_path = output_base.with_suffix(".docx")
        doc = Document()
        doc.add_heading("Transcript", level=1)
        doc.add_paragraph(transcript_text)
        doc.save(str(output_path))
    else:
        raise HTTPException(status_code=400, detail="export_format must be txt, json, or docx")

    row = ConversionHistory(
        kind="stt",
        input_path=str(audio_path),
        output_path=str(output_path),
        transcript=transcript_text,
        confidence=result.get("confidence", 0.0),
    )
    db.add(row)
    db.commit()

    return JSONResponse(
        {
            "message": "STT completed",
            "language": result.get("language"),
            "confidence": result.get("confidence"),
            "transcript": transcript_text,
            "download": f"/api/download?path={output_path}",
        }
    )


@router.post("/tts")
def tts(
    text: str = Form(""),
    voice: str = Form("tts_models/en/ljspeech/tacotron2-DDC"),
    rate: float = Form(1.0),
    pitch: float = Form(1.0),
    text_file: UploadFile | None = File(None),
    db: Session = Depends(get_db),
):
    if text_file is not None:
        text = text_file.file.read().decode("utf-8", errors="ignore")

    text = (text or "").strip()
    if not text:
        raise HTTPException(status_code=400, detail="No text provided")

    output_path = OUTPUT_DIR / f"{uuid4()}.wav"
    generated = tts_service.synthesize(text=text, output_path=output_path, voice=voice, rate=rate, pitch=pitch)

    row = ConversionHistory(
        kind="tts",
        output_path=str(generated),
        voice=voice,
        rate=rate,
        pitch=pitch,
    )
    db.add(row)
    db.commit()

    return JSONResponse(
        {
            "message": "TTS completed",
            "voice": voice,
            "rate": rate,
            "pitch": pitch,
            "download": f"/api/download?path={generated}",
        }
    )


@router.get("/download")
def download(path: str):
    file_path = Path(path)
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(str(file_path), filename=file_path.name)
