"""
Post-procesador para mejorar transcripciones diarizadas
Combina transcripción standard (alta calidad) con diarization (speakers + timestamps)
"""

from openai import OpenAI
from pathlib import Path
from config import Config


class DiarizationImprover:
    def __init__(self):
        if not Config.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY no encontrada en las variables de entorno")
        self.client = OpenAI()

    def improve_diarization(self, standard_text: str, diarization_text: str) -> str:
        """
        Combina transcripción standard con diarization para producir
        una versión mejorada con speakers y texto fluido.
        """
        prompt = f"""Tienes dos transcripciones del mismo audio:

1. TRANSCRIPCIÓN STANDARD (texto de alta calidad, sin speakers):
{standard_text}

2. TRANSCRIPCIÓN DIARIZADA (con speakers y timestamps, pero fragmentada):
{diarization_text}

Tu tarea:
- Usar el texto de la transcripción STANDARD como base (mejor calidad de redacción)
- Asignar los speakers [A], [B], etc. basándote en la diarización
- Agrupar el texto del mismo speaker en párrafos coherentes (no fragmentos pequeños)
- Incluir UN timestamp por intervención completa (inicio-fin aproximado)
- El resultado debe ser legible como una entrevista/conversación natural

Formato de salida esperado:
[A] (0s-45s): Párrafo completo de lo que dijo el speaker A...

[B] (45s-120s): Respuesta completa del speaker B...

[A] (120s-180s): Siguiente intervención de A...

IMPORTANTE:
- NO fragmentes el texto en líneas muy cortas como la diarización original
- Mantén párrafos completos por cada intervención
- Usa el texto de STANDARD, solo toma la información de speakers de DIARIZACIÓN
- Si hay dudas sobre qué speaker dijo algo, usa el contexto para inferir"""

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Eres un experto en edición de transcripciones. Tu trabajo es combinar información de múltiples fuentes para producir transcripciones de alta calidad."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=16000
        )

        return response.choices[0].message.content

    def process_files(self, base_name: str) -> str:
        """
        Procesa archivos de transcripción existentes y genera versión mejorada.

        Args:
            base_name: Nombre base del archivo (ej: "Entrevista Claudia")

        Returns:
            Ruta del archivo de salida generado
        """
        output_dir = Path(Config.OUTPUT_DIR)

        standard_file = output_dir / f"{base_name}_standard.txt"
        diarization_file = output_dir / f"{base_name}_diarization.txt"
        output_file = output_dir / f"{base_name}_diarization_improved.txt"

        # Verificar que existen ambos archivos
        if not standard_file.exists():
            raise FileNotFoundError(f"No se encontró: {standard_file}")
        if not diarization_file.exists():
            raise FileNotFoundError(f"No se encontró: {diarization_file}")

        # Verificar si ya existe el archivo mejorado
        if output_file.exists():
            raise FileExistsError(f"Ya existe: {output_file}")

        # Leer archivos
        standard_text = standard_file.read_text(encoding='utf-8')
        diarization_text = diarization_file.read_text(encoding='utf-8')

        print(f"   📄 Standard: {len(standard_text)} caracteres")
        print(f"   📄 Diarization: {len(diarization_text)} caracteres")

        # Procesar con GPT-4o
        print(f"   🤖 Procesando con GPT-4o...")
        improved_text = self.improve_diarization(standard_text, diarization_text)

        # Guardar resultado
        output_file.write_text(improved_text, encoding='utf-8')

        return str(output_file)

    def list_improvable_files(self) -> list:
        """
        Lista los archivos que tienen tanto standard como diarization disponibles.

        Returns:
            Lista de nombres base que pueden ser mejorados
        """
        output_dir = Path(Config.OUTPUT_DIR)

        # Buscar archivos _standard.txt
        standard_files = list(output_dir.glob("*_standard.txt"))

        improvable = []
        for std_file in standard_files:
            base_name = std_file.stem.replace("_standard", "")
            diar_file = output_dir / f"{base_name}_diarization.txt"
            improved_file = output_dir / f"{base_name}_diarization_improved.txt"

            if diar_file.exists() and not improved_file.exists():
                improvable.append(base_name)

        return improvable
