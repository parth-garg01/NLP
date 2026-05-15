# Product Requirements Document (PRD)

## Offline Speech-to-Text (STT) and Text-to-Speech (TTS) Platform with API Support

---

# 1. Project Overview

### Project Name

**VoxCraft**

### Project Description

VoxCraft is a full-stack application that provides:

1. **Speech-to-Text (STT)**
   Upload an audio file (`.mp3`, `.wav`, `.m4a`, `.flac`) and receive an accurate transcript.

2. **Text-to-Speech (TTS)**
   Upload a text file or type text manually and generate natural-sounding speech.

3. **Offline Support**
   All models run locally on the user's machine without requiring internet access.

4. **API Support**
   Expose REST API endpoints so developers can integrate STT/TTS into their own applications.

5. **Model Fine-Tuning**
   Support custom training on datasets for improved accuracy.

6. **Modern Web UI**
   Drag-and-drop interface for uploads, playback, transcript display, and downloads.

---

# 2. Objectives

* Build an end-to-end STT/TTS platform.
* Work entirely offline.
* Support local inference and optional cloud deployment.
* Provide API documentation.
* Maintain production-quality Git history.
* Use open-source models.

---

# 3. Target Users

* Students
* Researchers
* Developers
* Accessibility users
* Content creators
* Businesses needing transcription or voice generation

---

# 4. Functional Requirements

## Speech-to-Text

* Upload audio file.
* Detect language automatically.
* Generate transcript.
* Show confidence scores.
* Export transcript as `.txt`, `.docx`, `.json`.

## Text-to-Speech

* Upload text file or enter text.
* Select voice.
* Adjust speaking rate and pitch.
* Generate `.wav` or `.mp3`.
* Play audio in browser.

## Offline Mode

* Download models once.
* Store locally.
* Perform inference without internet.

## API Mode

* `/api/stt`
* `/api/tts`
* `/api/health`
* `/api/models`

## History

* Save previous conversions.

## Authentication (Optional)

* API key management.

---

# 5. Non-Functional Requirements

* Response time < 5 sec for short files.
* Secure file upload.
* Cross-platform.
* GPU acceleration when available.
* Scalable architecture.

---

# 6. Technology Stack

## Frontend

* [Next.js](https://nextjs.org?utm_source=chatgpt.com)
* [TypeScript](https://www.typescriptlang.org?utm_source=chatgpt.com)
* [Tailwind CSS](https://tailwindcss.com?utm_source=chatgpt.com)
* [Shadcn UI](https://ui.shadcn.com?utm_source=chatgpt.com)

## Backend

* [FastAPI](https://fastapi.tiangolo.com?utm_source=chatgpt.com)
* [Uvicorn](https://www.uvicorn.org?utm_source=chatgpt.com)
* [Pydantic](https://docs.pydantic.dev?utm_source=chatgpt.com)

## Machine Learning

* [OpenAI Whisper](https://github.com/openai/whisper?utm_source=chatgpt.com)
* [Coqui TTS](https://github.com/coqui-ai/TTS?utm_source=chatgpt.com)
* [PyTorch](https://pytorch.org?utm_source=chatgpt.com)
* [ONNX Runtime](https://onnxruntime.ai?utm_source=chatgpt.com)

## Database

* [SQLite](https://www.sqlite.org/index.html?utm_source=chatgpt.com)

## Storage

* Local filesystem

## Containerization

* [Docker](https://www.docker.com?utm_source=chatgpt.com)

## Version Control

* [GitHub](https://github.com?utm_source=chatgpt.com)

---

# 7. Recommended Models

## Speech-to-Text Model

### Whisper

Recommended variants:

* `tiny`
* `base`
* `small`
* `medium`
* `large-v3`

For offline use:

* `small` or `medium`

## Text-to-Speech Model

### Coqui TTS

Recommended models:

* `tts_models/en/ljspeech/tacotron2-DDC`
* `tts_models/en/vctk/vits`

---

# 8. Datasets for Training

## STT Datasets

* Mozilla Common Voice
* LibriSpeech
* AISHELL

## TTS Datasets

* LJSpeech
* VCTK

## Multilingual Datasets

* Common Voice
* Indic datasets from AI4Bharat

---

# 9. Project Architecture

```text
Frontend (Next.js)
      |
      v
Backend API (FastAPI)
      |
      +---- STT Service (Whisper)
      |
      +---- TTS Service (Coqui TTS)
      |
      +---- Model Manager
      |
      +---- File Manager
      |
      +---- SQLite Database
      |
      +---- Local Storage
```
