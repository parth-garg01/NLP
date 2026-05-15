# Training Pipeline

This folder contains dataset download/prep and fine-tuning entrypoints for both STT and TTS.

## Files
- `scripts/download_stt_dataset.py`: Downloads Common Voice split and normalizes columns.
- `scripts/download_tts_dataset.py`: Downloads or validates LJSpeech/VCTK style TTS data.
- `scripts/finetune_whisper.py`: Fine-tunes Whisper with Hugging Face Trainer.
- `scripts/finetune_coqui.py`: Fine-tunes Coqui TTS using dataset config.
- `configs/training_config.json`: Central training configuration.

## Quick Run
```bash
cd backend
python -m training.scripts.download_stt_dataset --config training/configs/training_config.json
python -m training.scripts.download_tts_dataset --config training/configs/training_config.json
python -m training.scripts.finetune_whisper --config training/configs/training_config.json
python -m training.scripts.finetune_coqui --config training/configs/training_config.json
```
