class ModelManager:
    @staticmethod
    def available_stt_models() -> list[str]:
        return ["tiny", "base", "small", "medium", "large-v3"]

    @staticmethod
    def available_tts_models() -> list[str]:
        return [
            "tts_models/en/ljspeech/tacotron2-DDC",
            "tts_models/en/vctk/vits",
        ]
