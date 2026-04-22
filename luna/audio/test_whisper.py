"""Test Whisper transcription on a 5-second recording."""

import time

import numpy as np
import sounddevice as sd
from faster_whisper import WhisperModel

SAMPLE_RATE = 16000
DURATION = 5


def main() -> None:
    print("A carregar Whisper medium... (primeira vez demora ~2-3 min a descarregar 1.5 GB)")
    t0 = time.time()
    model = WhisperModel(
        "medium",
        device="cpu",
        compute_type="int8",  # quantização que acelera no CPU
    )
    print(f"Modelo carregado em {time.time() - t0:.1f}s.\n")

    print(f"A gravar {DURATION} segundos... fala uma frase em português de Portugal!")
    audio = sd.rec(
        int(DURATION * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="float32",
    )
    sd.wait()
    print("Gravação concluída. A transcrever...")

    t0 = time.time()
    segments, info = model.transcribe(
        audio.flatten(),
        language="pt",       # forçar PT (Whisper iria detectar automaticamente)
        beam_size=5,          # maior precisão (5 = bom equilíbrio)
        vad_filter=True,      # filtra silêncio/ruído automático
    )
    text = " ".join(s.text.strip() for s in segments).strip()
    elapsed = time.time() - t0

    print(f"\n[Detectado idioma: {info.language} (prob {info.language_probability:.2f})]")
    print(f"[Transcrição em {elapsed:.1f}s]")
    print(f"\n>>> {text}\n")


if __name__ == "__main__":
    main()
