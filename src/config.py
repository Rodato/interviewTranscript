import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
    
    # Directorio base del proyecto
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Directorios de trabajo
    INPUT_DIR = os.path.join(BASE_DIR, 'mp3')
    OUTPUT_DIR = os.path.join(BASE_DIR, 'outputs')
    
    # Configuración de OpenAI Transcription
    AVAILABLE_MODELS = {
        "1": {
            "name": "gpt-4o-transcribe",
            "display_name": "GPT-4O Transcribe (Modelo principal)"
        },
        "2": {
            "name": "gpt-4o-mini-transcribe", 
            "display_name": "GPT-4O Mini Transcribe (Modelo económico)"
        }
    }
    
    # Modelo por defecto
    WHISPER_MODEL = "gpt-4o-transcribe"
    WHISPER_RESPONSE_FORMAT = "text"
    
    # Tamaño máximo de archivo para Whisper (25MB)
    MAX_FILE_SIZE_MB = 25