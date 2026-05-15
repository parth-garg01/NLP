import argparse
import csv
import json
import shutil
import tarfile
from pathlib import Path
from urllib.request import urlretrieve


LJSPEECH_URL = "https://data.keithito.com/data/speech/LJSpeech-1.1.tar.bz2"


def load_config(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_ljspeech(root: Path) -> tuple[bool, str]:
    wavs = root / "wavs"
    metadata = root / "metadata.csv"
    if not wavs.exists() or not metadata.exists():
        return False, "Missing wavs/ or metadata.csv"

    with metadata.open("r", encoding="utf-8") as f:
        sample = next(csv.reader(f, delimiter="|"), None)
    if not sample or len(sample) < 2:
        return False, "metadata.csv is malformed"

    return True, "LJSpeech structure valid"


def main() -> None:
    parser = argparse.ArgumentParser(description="Download/validate TTS dataset")
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--dataset", choices=["ljspeech", "vctk"], default="ljspeech")
    parser.add_argument("--output", type=Path, default=Path("backend/training/datasets"))
    parser.add_argument("--skip-download", action="store_true")
    args = parser.parse_args()

    _ = load_config(args.config)
    args.output.mkdir(parents=True, exist_ok=True)

    if args.dataset == "vctk":
        target = args.output / "vctk"
        target.mkdir(parents=True, exist_ok=True)
        print(json.dumps({
            "dataset": "vctk",
            "status": "manual_step_required",
            "message": "Place VCTK data inside backend/training/datasets/vctk and create metadata/manifest.",
        }, indent=2))
        return

    dataset_root = args.output / "ljspeech" / "LJSpeech-1.1"
    archive_path = args.output / "LJSpeech-1.1.tar.bz2"

    if not args.skip_download and not dataset_root.exists():
        urlretrieve(LJSPEECH_URL, archive_path)
        with tarfile.open(archive_path, "r:bz2") as tar:
            tar.extractall(path=args.output / "ljspeech")
        if archive_path.exists():
            archive_path.unlink()

    ok, message = validate_ljspeech(dataset_root)
    summary = {
        "dataset": "ljspeech",
        "path": str(dataset_root),
        "valid": ok,
        "message": message,
    }
    (args.output / "tts_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
