import os
from pathlib import Path
from pydub import AudioSegment
import tempfile

class AudioProcessor:
    def __init__(self, input_dir="mp3", output_dir="outputs"):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        
    def get_audio_files(self):
        """Encuentra todos los archivos de audio soportados en el directorio de entrada"""
        audio_files = []
        supported_formats = ["*.m4a", "*.mp3", "*.wav", "*.flac", "*.aac", "*.ogg", "*.mp4"]
        
        if self.input_dir.exists():
            for pattern in supported_formats:
                audio_files.extend(self.input_dir.glob(pattern))
        
        return sorted(audio_files)
    
    def validate_audio_file(self, file_path):
        """Valida que el archivo de audio sea procesable"""
        try:
            # OpenAI Whisper puede manejar M4A directamente
            # Solo verificamos que el archivo existe y su tamaño
            file_size_mb = file_path.stat().st_size / (1024 * 1024)
            return True, f"{file_size_mb:.1f}MB"
        except Exception as e:
            return False, str(e)
    
    def prepare_for_transcription(self, file_path):
        """Prepara el archivo de audio para transcripción"""
        try:
            # OpenAI Whisper acepta M4A directamente, solo validamos
            is_valid, info = self.validate_audio_file(file_path)
            if not is_valid:
                raise Exception(f"Archivo de audio inválido: {info}")
            
            return str(file_path), info  # Retorna path e info
        except Exception as e:
            raise Exception(f"Error preparando audio {file_path}: {str(e)}")
    
    def split_large_audio(self, file_path, max_size_mb=20):
        """Divide archivos de audio grandes en chunks más pequeños"""
        try:
            file_size_mb = Path(file_path).stat().st_size / (1024 * 1024)
            
            if file_size_mb <= max_size_mb:
                return [str(file_path)]  # No necesita división
            
            print(f"   📂 Dividiendo archivo de {file_size_mb:.1f}MB en chunks de ~{max_size_mb}MB")
            
            # Cargar audio
            audio = AudioSegment.from_file(str(file_path))
            duration_ms = len(audio)
            
            # Calcular duración por chunk (basado en tamaño)
            chunk_duration_ms = int((max_size_mb / file_size_mb) * duration_ms * 0.8)  # 80% para seguridad
            
            # Crear directorio temporal para chunks
            temp_dir = tempfile.mkdtemp()
            chunk_paths = []
            
            # Dividir en chunks
            start = 0
            chunk_num = 1
            
            while start < duration_ms:
                end = min(start + chunk_duration_ms, duration_ms)
                
                # Evitar cortar a mitad de oración - buscar silencio cerca del final
                if end < duration_ms:
                    # Buscar silencio en los últimos 30 segundos del chunk
                    search_start = max(end - 30000, start + 10000)
                    silence_thresh = audio[search_start:end].dBFS - 16
                    
                    # Buscar momento de silencio
                    for i in range(end - 5000, search_start, -1000):
                        if audio[i:i+1000].dBFS < silence_thresh:
                            end = i
                            break
                
                chunk = audio[start:end]
                # Usar formato que OpenAI soporta bien
                chunk_path = f"{temp_dir}/chunk_{chunk_num:03d}.mp3"
                chunk.export(chunk_path, format="mp3", bitrate="128k")
                chunk_paths.append(chunk_path)
                
                print(f"      • Chunk {chunk_num}: {(end-start)/60000:.1f} min")
                
                start = end
                chunk_num += 1
            
            return chunk_paths
            
        except Exception as e:
            raise Exception(f"Error dividiendo audio: {str(e)}")
    
    def cleanup_temp_files(self, file_paths):
        """Limpia archivos temporales"""
        for file_path in file_paths:
            try:
                if "/tmp" in file_path or "temp" in file_path:
                    os.remove(file_path)
            except:
                pass
    
    def get_output_path(self, input_file_path, extension="txt"):
        """Genera la ruta de salida para la transcripción"""
        self.output_dir.mkdir(exist_ok=True)
        stem = Path(input_file_path).stem
        return self.output_dir / f"{stem}.{extension}"