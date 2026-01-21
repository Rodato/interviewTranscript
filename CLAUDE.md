# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a transcriptor project that processes audio files (.m4a format) and generates transcriptions. The project uses AI services including OpenRouter and OpenAI for transcription processing.

## Project Structure

- `mp3/` - Contains input audio files (supports .m4a format)
- `src/` - Source code directory
  - `transcriptor.py` - Main entry point
  - `audio_processor.py` - Audio file handling and chunking
  - `openai_service.py` - OpenAI API integration
  - `post_processor.py` - Diarization improvement with GPT-4o
  - `config.py` - Configuration and environment variables
- `outputs/` - Generated transcription outputs
- `.env` - Environment configuration with API keys and service URLs

## Environment Setup

The project requires the following environment variables in `.env`:
- `OPENROUTER_API_KEY` - OpenRouter API access
- `OPENAI_API_KEY` - OpenAI API access

## Python Development

- Always use `python3` instead of `python` for script execution
- Use virtual environment: `venv/bin/python` for all script execution
- The project is a Python-based transcription service using OpenAI

## Setup and Running

1. **Create virtual environment**: `python3 -m venv venv`
2. **Install dependencies**: `source venv/bin/activate && pip install -r requirements.txt` (or directly `venv/bin/pip install -r requirements.txt`)
3. **Run transcriptor**: `venv/bin/python src/transcriptor.py`

## Audio Processing Features

- **Multi-format support**: M4A, MP3, WAV, FLAC, AAC, OGG, MP4
- **Automatic chunking**: Files larger than 20MB or 20 minutes are automatically split into chunks
- **Smart splitting**: Avoids cutting mid-sentence by finding silence points
- **Chunk transcription**: Each chunk is transcribed separately and combined
- **Speaker diarization**: GPT-4O Transcribe Diarization model separates speakers with timestamps

## Available Models

- **gpt-4o-transcribe**: Standard transcription model (high quality)
- **gpt-4o-mini-transcribe**: Economic transcription model (lower cost)
- **gpt-4o-transcribe-diarize**: Speaker diarization model (separates speakers with timestamps)

## Diarization Improvement (Post-processing)

The diarization model produces fragmented text with timestamps. The `--improve` feature combines:
- **Standard transcription**: High quality, fluid text (but no speakers)
- **Diarization transcription**: Speaker labels [A], [B] with timestamps (but fragmented)

Result: Coherent paragraphs per speaker with timestamps.

### Usage

```bash
# Improve specific file (requires both _standard.txt and _diarization.txt)
venv/bin/python src/transcriptor.py --improve "Entrevista Claudia"

# Interactive mode (lists available files)
venv/bin/python src/transcriptor.py --improve
```

### Output Files

- `outputs/archivo_standard.txt` - Standard transcription
- `outputs/archivo_diarization.txt` - Diarized transcription (fragmented)
- `outputs/archivo_diarization_improved.txt` - Improved version (combined)

### Example

**Before (diarization):**
```
[A] (60.8s-62.6s): Ok, ok,
[B] (62.6s-64.9s): los impactos que va a tener y todo eso.
[A] (64.9s-67.2s): si entonces te llega la idea de Cristian.
```

**After (improved):**
```
[A] (60.8s-71.0s): Ok, entonces te llega la idea de Cristian. Cristian, ¿qué te entrega?

[B] (71.6s-80.2s): Él debería entregar la cadena de valor. La cadena de valor contiene objetivos, actividades y el enfoque del proyecto.
```

## Known Limitations

- OpenAI API has a 25MB file size limit (handled automatically)
- Large files may take several minutes to process due to chunking
- Diarization model requires files longer than 30 seconds
- Requires ffmpeg for audio processing

## Security

This project includes Claude Code hooks (`.claude/claude-hooks.js`) that prevent Claude from reading or modifying `.env` files to protect API keys and sensitive configuration.

## Key Features

- Audio file transcription (M4A format support)
- Multiple LLM provider support (OpenRouter, OpenAI)

## VPS y Credenciales

Ver `PRIVATE.md` (no se sube a GitHub) para:
- Conexión SSH al VPS
- Comandos de sincronización
- Gestión de Screen
- Notificaciones Telegram
