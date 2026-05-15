from pathlib import Path
from typing import Any

ALLOWED_AUDIO = {".mp3", ".wav", ".m4a", ".flac"}


class STTService:
    def __init__(self, model_name: str = "small"):
        self.model_name = model_name
        self._model = None

    def _load_model(self):
        if self._model is None:
            try:
                import whisper
                self._model = whisper.load_model(self.model_name)
            except Exception:
                self._model = "mock"

    def transcribe(self, audio_path: Path) -> dict[str, Any]:
        self._load_model()
        if self._model == "mock":
            return {
                "text": f"[Mock transcript] Could not load Whisper for: {audio_path.name}",
                "language": "en",
                "confidence": 0.0,
            }

        result = self._model.transcribe(str(audio_path))
        segments = result.get("segments", [])
        confidences = [s.get("avg_logprob", -1.0) for s in segments]
        confidence = float(sum(confidences) / len(confidences)) if confidences else 0.0

        return {
            "text": result.get("text", "").strip(),
            "language": result.get("language", "unknown"),
            "confidence": confidence,
        }
