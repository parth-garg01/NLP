# API Guide

## Health
`GET /api/health`

## Models
`GET /api/models`

## STT
`POST /api/stt`
- Form fields:
  - `file` (audio: mp3/wav/m4a/flac)
  - `export_format` (`txt`, `json`, `docx`)

## TTS
`POST /api/tts`
- Form fields:
  - `text` or `text_file`
  - `voice`
  - `rate`
  - `pitch`

## History
`GET /api/history`

## Download
`GET /api/download?path=<absolute_or_relative_path>`
