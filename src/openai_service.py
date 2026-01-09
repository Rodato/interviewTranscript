from openai import OpenAI
from pathlib import Path
from config import Config

class OpenAITranscriptionService:
    def __init__(self):
        if not Config.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY no encontrada en las variables de entorno")
        
        self.client = OpenAI()
        
    def transcribe_audio(self, audio_file_path):
        """Transcribe un archivo de audio usando OpenAI Whisper"""
        try:
            # Verificar tamaño del archivo
            file_size_mb = Path(audio_file_path).stat().st_size / (1024 * 1024)
            if file_size_mb > Config.MAX_FILE_SIZE_MB:
                raise Exception(f"Archivo muy grande ({file_size_mb:.1f}MB). Máximo permitido: {Config.MAX_FILE_SIZE_MB}MB")
            
            with open(audio_file_path, "rb") as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model=Config.WHISPER_MODEL,
                    file=audio_file,
                    response_format=Config.WHISPER_RESPONSE_FORMAT
                )
            
            return transcript.text if hasattr(transcript, 'text') else transcript
            
        except Exception as e:
            raise Exception(f"Error en transcripción: {str(e)}")
    
    def save_transcription(self, transcription, output_path):
        """Guarda la transcripción en un archivo"""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(transcription)
            return True
        except Exception as e:
            raise Exception(f"Error guardando transcripción: {str(e)}")