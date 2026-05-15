# VoxCraft

Offline-first STT/TTS platform with REST APIs, modern web UI, and model fine-tuning pipeline.

## Stack
- Frontend: Next.js + TypeScript + Tailwind
- Backend: FastAPI + SQLite + Pydantic
- STT: Whisper (open-source)
- TTS: Coqui TTS (open-source)

## Quick Start

### 1. Backend
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 2. Frontend
```bash
cd frontend
npm install
npm run dev
```

Frontend: http://localhost:3000  
Backend: http://localhost:8000  
API docs: http://localhost:8000/docs

## API Endpoints
- `GET /api/health`
- `GET /api/models`
- `POST /api/stt`
- `POST /api/tts`
- `GET /api/history`

## Training Pipeline

### STT dataset download (Common Voice)
```bash
cd backend
python -m training.scripts.download_stt_dataset --config training/configs/training_config.json
```

### TTS dataset download/validation (LJSpeech)
```bash
cd backend
python -m training.scripts.download_tts_dataset --config training/configs/training_config.json
```

### Fine-tune Whisper
```bash
cd backend
python -m training.scripts.finetune_whisper --config training/configs/training_config.json
```

### Fine-tune Coqui TTS
```bash
cd backend
python -m training.scripts.finetune_coqui --config training/configs/training_config.json
```

## Docker
```bash
docker compose up --build
```
