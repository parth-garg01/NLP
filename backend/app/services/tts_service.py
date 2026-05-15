from pathlib import Path


class TTSService:
    def __init__(self):
        self._tts = None

    def _load(self, voice: str):
        if self._tts is None:
            try:
                from TTS.api import TTS
                self._tts = TTS(model_name=voice, progress_bar=False, gpu=False)
            except Exception:
                self._tts = "mock"

    def synthesize(self, text: str, output_path: Path, voice: str, rate: float, pitch: float) -> Path:
        self._load(voice)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if self._tts == "mock":
            output_path.write_bytes(b"Mock audio generated. Install Coqui TTS for real synthesis.")
            return output_path

        # Coqui does not expose direct pitch/rate controls uniformly across all models;
        # these are accepted in API for future extension.
        self._tts.tts_to_file(text=text, file_path=str(output_path))
        return output_path
