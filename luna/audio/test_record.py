"""Record 3 seconds from the default microphone and play it back."""

import numpy as np
import sounddevice as sd

SAMPLE_RATE = 16000  # Whisper trabalha a 16 kHz
DURATION = 3          # segundos


def main() -> None:
    print(f"A gravar {DURATION} segundos... fala algo agora!")
    audio = sd.rec(
        int(DURATION * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="float32",
    )
    sd.wait()
    print("Gravação concluída.")

    # Mostrar nível de volume (ajuda a diagnosticar microfones mudos)
    rms = float(np.sqrt(np.mean(audio ** 2)))
    print(f"Volume médio (RMS): {rms:.4f}  " + (
        "(parece silêncio — fala mais alto ou verifica o mic)" if rms < 0.005
        else "(parece bom)"
    ))

    print("A reproduzir o que gravaste...")
    sd.play(audio, samplerate=SAMPLE_RATE)
    sd.wait()
    print("Terminado.")


if __name__ == "__main__":
    main()
