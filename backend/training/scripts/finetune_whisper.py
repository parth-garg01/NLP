import argparse
import json
from pathlib import Path


import numpy as np


def load_config(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))["stt"]


def main() -> None:
    parser = argparse.ArgumentParser(description="Fine-tune Whisper on prepared STT dataset")
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--dataset-path", type=Path, default=Path("backend/training/datasets/stt/common_voice"))
    args = parser.parse_args()

    cfg = load_config(args.config)

    try:
        from datasets import load_from_disk
        from transformers import (
            Seq2SeqTrainer,
            Seq2SeqTrainingArguments,
            WhisperFeatureExtractor,
            WhisperForConditionalGeneration,
            WhisperProcessor,
            WhisperTokenizer,
        )
    except Exception as exc:
        raise SystemExit("Install STT training deps: transformers datasets evaluate jiwer accelerate") from exc

    if not args.dataset_path.exists():
        raise SystemExit(f"Dataset not found at {args.dataset_path}. Run download_stt_dataset first.")

    ds = load_from_disk(str(args.dataset_path))

    feature_extractor = WhisperFeatureExtractor.from_pretrained(cfg["model_name"])
    tokenizer = WhisperTokenizer.from_pretrained(cfg["model_name"], language="en", task="transcribe")
    processor = WhisperProcessor(feature_extractor=feature_extractor, tokenizer=tokenizer)
    model = WhisperForConditionalGeneration.from_pretrained(cfg["model_name"])

    def prepare(batch):
        audio = batch["audio"]
        batch["input_features"] = feature_extractor(audio["array"], sampling_rate=audio["sampling_rate"]).input_features[0]
        batch["labels"] = tokenizer(batch["sentence"]).input_ids
        return batch

    ds = ds.filter(lambda x: 0 < x["audio"]["duration"] <= cfg["max_duration_seconds"])
    ds = ds.map(prepare, remove_columns=ds.column_names)

    def data_collator(features):
        input_features = [{"input_features": f["input_features"]} for f in features]
        batch = processor.feature_extractor.pad(input_features, return_tensors="pt")

        label_features = [{"input_ids": f["labels"]} for f in features]
        labels_batch = processor.tokenizer.pad(label_features, return_tensors="pt")
        labels = labels_batch["input_ids"].masked_fill(labels_batch.attention_mask.ne(1), -100)
        batch["labels"] = labels
        return batch

    training_args = Seq2SeqTrainingArguments(
        output_dir=cfg["output_dir"],
        per_device_train_batch_size=cfg["per_device_train_batch_size"],
        per_device_eval_batch_size=cfg["per_device_eval_batch_size"],
        learning_rate=cfg["learning_rate"],
        warmup_steps=cfg["warmup_steps"],
        num_train_epochs=cfg["num_train_epochs"],
        logging_steps=cfg["logging_steps"],
        save_steps=cfg["save_steps"],
        eval_steps=cfg["eval_steps"],
        evaluation_strategy="steps",
        predict_with_generate=True,
        generation_max_length=cfg["generation_max_length"],
        fp16=False,
        report_to=[],
    )

    trainer = Seq2SeqTrainer(
        args=training_args,
        model=model,
        train_dataset=ds,
        eval_dataset=ds.select(range(min(200, len(ds)))),
        data_collator=data_collator,
        tokenizer=processor.feature_extractor,
    )

    trainer.train()
    trainer.save_model(cfg["output_dir"])
    processor.save_pretrained(cfg["output_dir"])
    print(json.dumps({"status": "ok", "saved_to": cfg["output_dir"]}, indent=2))


if __name__ == "__main__":
    main()
