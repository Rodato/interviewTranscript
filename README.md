# 🎤 Audio Transcriptor

Herramienta avanzada de transcripción automática de archivos de audio usando OpenAI. Soporta múltiples modelos incluyendo separación de hablantes (diarización) y procesamiento inteligente de archivos grandes.

## ✨ Características

- **Múltiples modelos de transcripción**:
  - GPT-4O Transcribe (modelo principal)
  - GPT-4O Mini Transcribe (modelo económico)
  - GPT-4O Transcribe Diarization (separación de hablantes)

- **Soporte multi-formato**: M4A, MP3, WAV, FLAC, AAC, OGG, MP4
- **Chunking automático**: División inteligente de archivos grandes (>20MB o >20min)
- **División por silencio**: Evita cortar palabras a la mitad
- **Procesamiento por lotes**: Transcribe múltiples archivos automáticamente
- **Gestión de duplicados**: Detecta transcripciones existentes según modelo usado

## 🚀 Instalación y Uso

### 1. Configuración del entorno

```bash
# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Configuración de API

Crea un archivo `.env` con tus claves de API:
```env
OPENAI_API_KEY=tu_clave_openai_aqui
```

### 3. Ejecución

```bash
# Activar entorno virtual y ejecutar
venv/bin/python src/transcriptor.py
```

## 📁 Estructura del Proyecto

```
transcriptor/
├── mp3/           # Archivos de audio de entrada
├── outputs/       # Transcripciones generadas
├── src/           # Código fuente
│   ├── transcriptor.py     # Script principal
│   ├── audio_processor.py  # Procesamiento de audio
│   ├── openai_service.py   # Integración con OpenAI
│   └── config.py          # Configuraciones
├── venv/          # Entorno virtual
└── .env           # Variables de entorno
```

## 🎯 Modelos Disponibles

### 1. GPT-4O Transcribe (Estándar)
- Transcripción de alta calidad
- Ideal para la mayoría de casos de uso
- Sufijo de archivo: `_standard.txt`

### 2. GPT-4O Mini Transcribe (Económico)
- Versión más económica
- Buena calidad para casos básicos
- Sufijo de archivo: `_mini.txt`

### 3. GPT-4O Transcribe Diarization (Separación de Hablantes)
- Identifica y separa diferentes hablantes
- Incluye timestamps para cada segmento
- Formato: `[Speaker] (tiempo): texto`
- Sufijo de archivo: `_diarization.txt`

## 🔧 Características Técnicas

- **Límite de tamaño**: 25MB por chunk (manejado automáticamente)
- **Límite de duración**: 20 minutos por chunk
- **Formatos soportados**: Todos los formatos de ffmpeg
- **Codificación**: UTF-8 para archivos de salida
- **Calidad de audio**: Optimización automática a 128kbps MP3

## 📋 Requisitos

- Python 3.7+
- ffmpeg (para procesamiento de audio)
- Clave de API de OpenAI
- Conexión a internet

## 🛠️ Dependencias

- `openai` - Cliente oficial de OpenAI
- `pydub` - Manipulación de archivos de audio
- `python-dotenv` - Gestión de variables de entorno

## 📈 Limitaciones Conocidas

- La API de OpenAI tiene un límite de 25MB por archivo (manejado automáticamente)
- Archivos muy grandes pueden tomar varios minutos en procesarse
- El modelo de diarización requiere archivos de más de 30 segundos
- Se requiere ffmpeg instalado en el sistema
