"""Imprime nível RMS do microfone em tempo real."""

import numpy as np
import sounddevice as sd

SAMPLE_RATE = 16000
CHUNK = 1024

print("[mic] A escutar... Fala para veres a barra mexer. Ctrl+C para sair.\n")

with sd.InputStream(
    samplerate=SAMPLE_RATE,
    channels=1,
    dtype="float32",
    blocksize=CHUNK,
) as stream:
    try:
        while True:
            data, _ = stream.read(CHUNK)
            rms = float(np.sqrt(np.mean(data.flatten() ** 2)))
            bar = "█" * int(rms * 200)
            print(f"\r  RMS={rms:.4f}  {bar:<60}", end="", flush=True)
    except KeyboardInterrupt:
        print("\n[mic] Terminado.")
