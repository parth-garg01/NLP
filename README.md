# VoxCraft

Offline-first STT/TTS platform with REST APIs and modern web UI.

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

## Docker
```bash
docker compose up --build
```
