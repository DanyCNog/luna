"""
Luna · Text-to-Speech
=====================
Módulo de síntese de voz usando Piper TTS (piper-tts 1.4.x, API OHF-Voice).

Uso:
    from luna.audio.tts import LunaTTS
    tts = LunaTTS()
    tts.say("Olá Dany, bem-vindo.")

Configurável via variáveis de ambiente:
    LUNA_TTS_MODEL_PATH  — caminho para o .onnx
                          (default: models/tts/pt_PT-tugao-medium.onnx)
"""

from __future__ import annotations

import os
import time
import wave
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import sounddevice as sd
from piper import PiperVoice

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MODEL = PROJECT_ROOT / "models" / "tts" / "pt_PT-tugao-medium.onnx"


@dataclass
class TTSConfig:
    """Configuração do Text-to-Speech da Luna."""

    model_path: Path = Path(
        os.environ.get("LUNA_TTS_MODEL_PATH", str(DEFAULT_MODEL))
    )


class LunaTTS:
    """Wrapper em torno do Piper TTS 1.4.x para uso rápido na Luna.

    API nova (piper-tts 1.4+):
      - voice.synthesize(text) → iterador de AudioChunk com .audio_int16_bytes
      - voice.synthesize_wav(text, wave_file) → grava num wave.open(...)
    """

    def __init__(self, config: TTSConfig | None = None) -> None:
        self.config = config or TTSConfig()
        if not self.config.model_path.exists():
            raise FileNotFoundError(
                f"Modelo TTS não encontrado em {self.config.model_path}. "
                "Descarrega a voz pt_PT-tugao-medium primeiro (ver manual 1v.4)."
            )
        print(f"[TTS] A carregar voz '{self.config.model_path.stem}'...")
        t0 = time.time()
        self.voice = PiperVoice.load(str(self.config.model_path))
        self.sample_rate = self.voice.config.sample_rate
        print(f"[TTS] Carregada em {time.time() - t0:.1f}s.")

    def synthesize(self, text: str) -> np.ndarray:
        """Sintetiza texto em array numpy int16 (mono, sample_rate da voz)."""
        chunks = []
        # API 1.4+: itera AudioChunk, cada um com audio_int16_bytes
        for chunk in self.voice.synthesize(text):
            chunks.append(np.frombuffer(chunk.audio_int16_bytes, dtype=np.int16))
        if not chunks:
            return np.zeros(0, dtype=np.int16)
        return np.concatenate(chunks)

    def say(self, text: str) -> None:
        """Sintetiza e reproduz texto em tempo real."""
        if not text.strip():
            return
        audio = self.synthesize(text)
        if len(audio) == 0:
            return
        sd.play(audio, samplerate=self.sample_rate, blocking=True)

    def save_to_file(self, text: str, output_path: str | Path) -> None:
        """Sintetiza texto e guarda num ficheiro WAV."""
        with wave.open(str(output_path), "wb") as wav_file:
            self.voice.synthesize_wav(text, wav_file)


if __name__ == "__main__":
    # Teste rápido do módulo
    tts = LunaTTS()
    tts.say("Olá Dany, sou a Luna. A minha voz ainda é provisória.")
