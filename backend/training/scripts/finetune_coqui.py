import argparse
import json
from pathlib import Path


def load_config(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))["tts"]


def build_formatter(ljspeech_root: Path, metadata_file: str) -> list[dict]:
    metadata_path = ljspeech_root / metadata_file
    if not metadata_path.exists():
        raise FileNotFoundError(f"Missing metadata file: {metadata_path}")

    rows = []
    for line in metadata_path.read_text(encoding="utf-8").splitlines():
        parts = line.split("|")
        if len(parts) < 2:
            continue
        item_id, text = parts[0], parts[1]
        wav_path = ljspeech_root / "wavs" / f"{item_id}.wav"
        if wav_path.exists():
            rows.append({"audio_file": str(wav_path), "text": text, "speaker_name": "ljspeech"})
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description="Fine-tune Coqui TTS on LJSpeech style dataset")
    parser.add_argument("--config", type=Path, required=True)
    args = parser.parse_args()

    cfg = load_config(args.config)
    dataset_root = Path(cfg["dataset_dir"]) / "LJSpeech-1.1"

    try:
        import torch
        from trainer import Trainer, TrainerArgs
        from TTS.config import load_config as tts_load_config
        from TTS.tts.configs.tacotron2_config import Tacotron2Config
        from TTS.tts.models.tacotron2 import Tacotron2
        from TTS.tts.utils.text.tokenizer import TTSTokenizer
        from TTS.utils.audio import AudioProcessor
    except Exception as exc:
        raise SystemExit("Install Coqui training deps: TTS trainer torch") from exc

    samples = build_formatter(dataset_root, cfg["metadata_file"])
    if not samples:
        raise SystemExit("No valid samples found for TTS training")

    out_dir = Path(cfg["output_dir"])
    out_dir.mkdir(parents=True, exist_ok=True)

    config = Tacotron2Config(
        output_path=str(out_dir),
        batch_size=cfg["batch_size"],
        eval_batch_size=cfg["eval_batch_size"],
        num_loader_workers=cfg["num_loader_workers"],
        run_name=cfg["run_name"],
        epochs=cfg["epochs"],
        text_cleaner="english_cleaners",
        use_phonemes=False,
        print_step=25,
        save_step=500,
        lr=cfg["learning_rate"],
    )

    ap = AudioProcessor.init_from_config(config)
    tokenizer, config = TTSTokenizer.init_from_config(config)
    model = Tacotron2(config, ap, tokenizer, speaker_manager=None)

    split_idx = int(len(samples) * 0.95)
    train_samples = samples[:split_idx]
    eval_samples = samples[split_idx:] if split_idx < len(samples) else samples[: min(100, len(samples))]

    trainer = Trainer(
        TrainerArgs(),
        config,
        out_path=str(out_dir),
        model=model,
        train_samples=train_samples,
        eval_samples=eval_samples,
    )
    trainer.fit()

    print(json.dumps({"status": "ok", "saved_to": str(out_dir)}, indent=2))


if __name__ == "__main__":
    main()
