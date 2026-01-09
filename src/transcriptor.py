#!/usr/bin/env python3
"""
Transcriptor de Audio usando OpenAI Whisper
Procesa archivos M4A y genera transcripciones en texto
"""

import sys
from pathlib import Path
from audio_processor import AudioProcessor
from openai_service import OpenAITranscriptionService
from config import Config

def main():
    """Función principal del transcriptor"""
    print("🎤 Transcriptor de Audio - OpenAI")
    print("=" * 50)
    
    # Seleccionar modelo
    print("Modelos disponibles:")
    for key, model_info in Config.AVAILABLE_MODELS.items():
        print(f"   {key}. {model_info['display_name']}")
    
    while True:
        choice = input("\nSelecciona modelo (1-3): ").strip()
        if choice in Config.AVAILABLE_MODELS:
            selected_model = Config.AVAILABLE_MODELS[choice]["name"]
            model_display = Config.AVAILABLE_MODELS[choice]["display_name"]
            break
        print("❌ Opción inválida. Selecciona 1, 2 o 3.")
    
    print(f"✅ Usando: {model_display}")
    
    try:
        # Inicializar componentes
        audio_processor = AudioProcessor()
        transcription_service = OpenAITranscriptionService()
        
        # Buscar archivos de audio
        audio_files = audio_processor.get_audio_files()
        
        if not audio_files:
            print("❌ No se encontraron archivos de audio en el directorio 'mp3'")
            return
        
        print(f"📁 Encontrados {len(audio_files)} archivo(s) de audio:")
        for file in audio_files:
            print(f"   • {file.name}")
        
        # Procesar cada archivo
        for i, audio_file in enumerate(audio_files, 1):
            print(f"\n🔄 Procesando ({i}/{len(audio_files)}): {audio_file.name}")
            
            try:
                # Preparar archivo para transcripción
                prepared_file, info = audio_processor.prepare_for_transcription(audio_file)
                print(f"   📄 Archivo: {info}")
                
                # Verificar si ya existe transcripción (con sufijo del modelo)
                if "mini" in selected_model:
                    model_suffix = "_mini"
                elif "diarize" in selected_model:
                    model_suffix = "_diarization"
                else:
                    model_suffix = "_standard"
                output_path = audio_processor.get_output_path(audio_file).with_name(
                    audio_processor.get_output_path(audio_file).stem + model_suffix + ".txt"
                )
                if output_path.exists():
                    print(f"   ⚠️  Ya existe transcripción: {output_path.name}")
                    continue
                
                # Dividir archivo si es necesario
                chunk_paths = audio_processor.split_large_audio(prepared_file)
                
                if len(chunk_paths) == 1:
                    # Archivo pequeño, transcripción directa
                    print(f"   🤖 Enviando a {model_display}...")
                    transcription = transcription_service.transcribe_audio(chunk_paths[0], model=selected_model)
                else:
                    # Archivo grande, transcribir por chunks
                    print(f"   🤖 Transcribiendo {len(chunk_paths)} chunks con {model_display}...")
                    transcriptions = []
                    
                    for i, chunk_path in enumerate(chunk_paths, 1):
                        print(f"      🔄 Chunk {i}/{len(chunk_paths)}")
                        chunk_transcription = transcription_service.transcribe_audio(chunk_path, model=selected_model)
                        transcriptions.append(chunk_transcription)
                    
                    # Combinar transcripciones
                    transcription = "\n\n".join(transcriptions)
                    
                    # Limpiar archivos temporales
                    audio_processor.cleanup_temp_files(chunk_paths)
                
                # Guardar resultado
                transcription_service.save_transcription(transcription, output_path)
                print(f"   ✅ Transcripción guardada: {output_path.name}")
                
            except Exception as e:
                print(f"   ❌ Error procesando {audio_file.name}: {str(e)}")
                continue
        
        print(f"\n🎉 Proceso completado!")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Proceso interrumpido por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error fatal: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()