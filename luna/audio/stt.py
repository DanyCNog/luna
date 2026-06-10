"""
Luna · Speech-to-Text
=====================
Módulo de transcrição de voz usando faster-whisper.

Uso:
    from luna.audio.stt import LunaSTT
    stt = LunaSTT()
    text = stt.record_and_transcribe(duration=5)
    print(text)
"""

from __future__ import annotations

import os
import time
from dataclasses import dataclass

import numpy as np
import sounddevice as sd
from faster_whisper import WhisperModel

# Whisper espera sempre áudio a 16 kHz, 16-bit, mono.
SAMPLE_RATE = 16000


@dataclass
class STTConfig:
    """Configuração do Speech-to-Text da Luna."""

    model_size: str = os.environ.get("LUNA_WHISPER_MODEL", "small")
    language: str = "pt"
    device: str = "cpu"          # "cuda" se houvesse GPU dedicada
    compute_type: str = "int8"    # int8 = rápido no CPU; float16 para GPU
    beam_size: int = 5
    vad_filter: bool = True       # filtra silêncio/ruído


class LunaSTT:
    """Wrapper em torno do faster-whisper para uso rápido na Luna."""

    def __init__(self, config: STTConfig | None = None) -> None:
        self.config = config or STTConfig()
        print(f"[STT] A carregar Whisper '{self.config.model_size}'...")
        t0 = time.time()
        self.model = WhisperModel(
            self.config.model_size,
            device=self.config.device,
            compute_type=self.config.compute_type,
        )
        print(f"[STT] Carregado em {time.time() - t0:.1f}s.")

    def record(self, duration: float) -> np.ndarray:
        """Grava áudio do microfone default durante N segundos."""
        audio = sd.rec(
            int(duration * SAMPLE_RATE),
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype="float32",
        )
        sd.wait()
        return audio.flatten()

    def transcribe(self, audio: np.ndarray) -> str:
        """Transcreve um array de áudio numpy. Retorna texto limpo."""
        segments, _ = self.model.transcribe(
            audio,
            language=self.config.language,
            beam_size=self.config.beam_size,
            vad_filter=self.config.vad_filter,
        )
        return " ".join(s.text.strip() for s in segments).strip()

    def record_and_transcribe(self, duration: float = 5.0) -> str:
        """Grava + transcreve num único passo. Retorna o texto."""
        print(f"[STT] A ouvir ({duration:.1f}s)...")
        audio = self.record(duration)
        rms = float(np.sqrt(np.mean(audio ** 2)))
        if rms < 0.003:
            return ""  # só silêncio, não vale a pena transcrever
        print("[STT] A transcrever...")
        return self.transcribe(audio)


if __name__ == "__main__":
    # Teste manual rápido do módulo
    stt = LunaSTT()
    text = stt.record_and_transcribe(duration=5)
    print(f"\n>>> {text!r}")
