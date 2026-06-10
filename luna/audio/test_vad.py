"""
Teste de Silero VAD em tempo real (API oficial v6).
"""

from __future__ import annotations

import numpy as np
import sounddevice as sd
import torch
from silero_vad import load_silero_vad, VADIterator

SAMPLE_RATE = 16000
CHUNK_SAMPLES = 512
THRESHOLD = 0.6
DEBUG_EVERY_N_CHUNKS = 30


def main() -> None:
    print("[VAD] A carregar Silero VAD (oficial v6)...")
    model = load_silero_vad(onnx=True)
    vad_iterator = VADIterator(
        model,
        threshold=THRESHOLD,
        sampling_rate=SAMPLE_RATE,
        min_silence_duration_ms=800,
        speech_pad_ms=30,
    )

    default_in = sd.default.device[0]
    if default_in is not None and default_in >= 0:
        device_name = sd.query_devices(default_in)["name"]
        print(f"[VAD] Microfone: {device_name}")

    print(f"[VAD] Pronto. Threshold={THRESHOLD}. "
          "Fala para testar. Ctrl+C para sair.\n")

    debug_counter = 0

    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="float32",
        blocksize=CHUNK_SAMPLES,
    ) as stream:
        try:
            while True:
                chunk, _ = stream.read(CHUNK_SAMPLES)
                audio_np = chunk.flatten().astype(np.float32)

                # Normalizar se sinal demasiado alto
                peak = np.max(np.abs(audio_np))
                if peak > 0.3:
                    audio_np = audio_np * (0.3 / peak)

                # Converter para tensor PyTorch (a API v6 exige isto)
                audio_tensor = torch.from_numpy(audio_np)

                # Probabilidade directa
                speech_prob = model(audio_tensor, SAMPLE_RATE).item()

                # Detectar início/fim
                event = vad_iterator(audio_tensor, return_seconds=True)

                # Debug periódico
                debug_counter += 1
                if debug_counter % DEBUG_EVERY_N_CHUNKS == 0:
                    rms = float(np.sqrt(np.mean(audio_np ** 2)))
                    print(f"  [debug] prob_voz={speech_prob:.3f}  "
                          f"rms_norm={rms:.4f}", flush=True)

                if event:
                    if "start" in event:
                        print(f"  🎤 VOZ DETECTADA (início @ {event['start']:.2f}s)")
                    if "end" in event:
                        print(f"  💤 silêncio (fim @ {event['end']:.2f}s)")

        except KeyboardInterrupt:
            print("\n[VAD] Terminado.")


if __name__ == "__main__":
    main()
