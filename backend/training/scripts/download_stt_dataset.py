import argparse
import json
from pathlib import Path


def load_config(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser(description="Download and preprocess STT dataset")
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("backend/training/datasets/stt"))
    args = parser.parse_args()

    cfg = load_config(args.config)["stt"]
    args.output.mkdir(parents=True, exist_ok=True)

    try:
        from datasets import Audio, load_dataset
    except Exception as exc:
        raise SystemExit("Install training dependencies first: pip install -r requirements.txt") from exc

    dataset = load_dataset(
        cfg["dataset_name"],
        cfg["dataset_config"],
        split=cfg["split"],
    )

    text_col = cfg["text_column"]
    audio_col = cfg["audio_column"]

    dataset = dataset.remove_columns([c for c in dataset.column_names if c not in [text_col, audio_col]])
    dataset = dataset.cast_column(audio_col, Audio(sampling_rate=16_000))

    out_dir = args.output / "common_voice"
    dataset.save_to_disk(str(out_dir))

    summary = {
        "dataset": cfg["dataset_name"],
        "config": cfg["dataset_config"],
        "split": cfg["split"],
        "rows": len(dataset),
        "saved_to": str(out_dir),
    }
    (args.output / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
