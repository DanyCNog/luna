"""Teste rápido de detecção de wake word (Alexa)."""

import numpy as np
import sounddevice as sd
from openwakeword.model import Model

SAMPLE_RATE = 16000
CHUNK_SAMPLES = 1280   # 80ms de áudio (recomendado pelo openwakeword)
WAKEWORD = "alexa"     # modelo pré-treinado a usar
THRESHOLD = 0.5        # 0-1. Subir = menos falsos positivos mas mais "não ouve"


def main() -> None:
    print("[wake] A carregar modelo 'alexa'...")
    oww = Model(
        wakeword_models=[WAKEWORD],
        inference_framework="onnx",
    )
    print("[wake] Pronto. Diz 'Alexa' para testar. Ctrl+C para sair.\n")

    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="int16",
        blocksize=CHUNK_SAMPLES,
    ) as stream:
        try:
            while True:
                chunk, _ = stream.read(CHUNK_SAMPLES)
                audio = chunk.flatten()
                prediction = oww.predict(audio)
                score = prediction.get(WAKEWORD, 0.0)
                if score > THRESHOLD:
                    print(f"  🔔 DETECTADO ({score:.2f})")
        except KeyboardInterrupt:
            print("\n[wake] Terminado.")


if __name__ == "__main__":
    main()
