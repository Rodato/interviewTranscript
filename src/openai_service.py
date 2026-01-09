from openai import OpenAI
from pathlib import Path
from config import Config

class OpenAITranscriptionService:
    def __init__(self):
        if not Config.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY no encontrada en las variables de entorno")
        
        self.client = OpenAI()
        
    def transcribe_audio(self, audio_file_path, model=None):
        """Transcribe un archivo de audio usando OpenAI"""
        try:
            # Usar modelo específico o el por defecto
            selected_model = model if model else Config.WHISPER_MODEL
            
            # Verificar tamaño del archivo
            file_size_mb = Path(audio_file_path).stat().st_size / (1024 * 1024)
            if file_size_mb > Config.MAX_FILE_SIZE_MB:
                raise Exception(f"Archivo muy grande ({file_size_mb:.1f}MB). Máximo permitido: {Config.MAX_FILE_SIZE_MB}MB")
            
            with open(audio_file_path, "rb") as audio_file:
                # Configurar parámetros según el modelo
                params = {
                    "model": selected_model,
                    "file": audio_file,
                    "response_format": Config.WHISPER_RESPONSE_FORMAT
                }
                
                # Para modelos de diarización, añadir chunking_strategy y response_format
                if "diarize" in selected_model:
                    params["chunking_strategy"] = "auto"
                    params["response_format"] = "diarized_json"
                
                transcript = self.client.audio.transcriptions.create(**params)
            
            # Manejar diferentes formatos de respuesta
            if "diarize" in selected_model:
                # Para diarización, formatear los segmentos
                if hasattr(transcript, 'segments'):
                    formatted_text = []
                    for segment in transcript.segments:
                        speaker = getattr(segment, 'speaker', 'Unknown')
                        text = getattr(segment, 'text', '')
                        start = getattr(segment, 'start', 0)
                        end = getattr(segment, 'end', 0)
                        formatted_text.append(f"[{speaker}] ({start:.1f}s-{end:.1f}s): {text}")
                    return '\n'.join(formatted_text)
                else:
                    return str(transcript)
            else:
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