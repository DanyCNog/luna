"""
Luna · Continuous Listener (revisto para silero-vad v6.x + diagnóstico de timings)
==================================================================================
Escuta contínua inteligente em 2 níveis:

NÍVEL 1: Silero VAD detecta presença de voz humana (PyTorch backend, ~5% CPU).
NÍVEL 2: Quando há voz, Whisper transcreve em rajadas e procura "Luna".

Custo de CPU baixo em silêncio. Sobe apenas quando há fala.
Privacidade: áudio nunca persistido, transcrições descartadas em ms se sem menção.

Esta versão imprime timings de cada etapa para diagnóstico de latência.
"""

from __future__ import annotations

import os
import queue
import sys
import time
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

# Permitir importar módulos do pacote luna quando corrido directamente
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import numpy as np
import sounddevice as sd
import torch
from silero_vad import VADIterator, load_silero_vad

from luna.audio.mention import detect_mention
from luna.audio.stt import LunaSTT

SAMPLE_RATE = 16000
VAD_CHUNK = 512
PRE_BUFFER_SECS = 0.5
MAX_UTTERANCE_SECS = 8
SILENCE_END_MS = 700


@dataclass
class ListenerEvent:
    """O que o listener emite quando a Luna é mencionada."""

    request: str
    full_transcription: str
    confidence: float
    timestamp: float


class LunaListener:
    """Listener contínuo. Apenas chama callback se detectar 'Luna' em conversa."""

    def __init__(
        self,
        stt: LunaSTT | None = None,
        vad_threshold: float = 0.6,
    ) -> None:
        self.vad_threshold = float(
            os.environ.get("LUNA_VAD_THRESHOLD", str(vad_threshold))
        )

        print("[listener] A carregar Silero VAD (oficial v6)...")
        self.vad_model = load_silero_vad(onnx=True)
        self.vad_iterator = VADIterator(
            self.vad_model,
            threshold=self.vad_threshold,
            sampling_rate=SAMPLE_RATE,
            min_silence_duration_ms=SILENCE_END_MS,
            speech_pad_ms=30,
        )

        self.stt = stt or LunaSTT()
        print("[listener] Pronto.")

        self._audio_queue: queue.Queue[np.ndarray] = queue.Queue()
        self._stop = False

    def _audio_callback(self, indata, frames, time_info, status) -> None:  # noqa: ANN001
        if status:
            pass
        self._audio_queue.put(indata.copy().flatten().astype(np.float32))

    def listen(self, on_mention: Callable[[ListenerEvent], None]) -> None:
        """Loop principal. Chama `on_mention` cada vez que detecta 'Luna'."""
        pre_buffer_size = int(SAMPLE_RATE * PRE_BUFFER_SECS / VAD_CHUNK)
        pre_buffer: list[np.ndarray] = []

        in_speech = False
        speech_chunks: list[np.ndarray] = []
        speech_start_time = 0.0
        max_chunks = int(SAMPLE_RATE * MAX_UTTERANCE_SECS / VAD_CHUNK)

        with sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype="float32",
            blocksize=VAD_CHUNK,
            callback=self._audio_callback,
        ):
            print("[listener] A ouvir... (Ctrl+C para sair)")
            while not self._stop:
                try:
                    chunk = self._audio_queue.get(timeout=0.5)
                except queue.Empty:
                    continue

                # Normalizar se sinal demasiado alto
                peak = float(np.max(np.abs(chunk)))
                if peak > 0.3:
                    chunk = chunk * (0.3 / peak)

                # Converter para tensor PyTorch
                audio_tensor = torch.from_numpy(chunk)

                # Detectar início/fim com state interno do VADIterator
                event = self.vad_iterator(audio_tensor, return_seconds=True)

                if not in_speech:
                    pre_buffer.append(chunk)
                    if len(pre_buffer) > pre_buffer_size:
                        pre_buffer.pop(0)

                    if event and "start" in event:
                        in_speech = True
                        speech_chunks = list(pre_buffer)
                        speech_chunks.append(chunk)
                        speech_start_time = time.time()
                        pre_buffer = []
                else:
                    speech_chunks.append(chunk)

                    end_detected = event and "end" in event
                    too_long = len(speech_chunks) >= max_chunks

                    if end_detected or too_long:
                        full_audio = np.concatenate(speech_chunks)
                        self._process_utterance(
                            full_audio,
                            speech_start_time,
                            on_mention,
                        )

                        in_speech = False
                        speech_chunks = []

    def _process_utterance(
        self,
        audio: np.ndarray,
        start_time: float,
        on_mention: Callable[[ListenerEvent], None],
    ) -> None:
        """Transcreve uma utterance e dispara callback se 'Luna' presente."""
        if len(audio) < SAMPLE_RATE * 0.4:
            return

        # === Diagnóstico de timings ===
        audio_len = len(audio) / SAMPLE_RATE
        delay_capture = time.time() - start_time
        print(
            f"\n[timing] áudio={audio_len:.1f}s  "
            f"capturado_há={delay_capture:.1f}s",
            flush=True,
        )

        # STT (Whisper) — costuma ser o gargalo
        t0 = time.time()
        try:
            text = self.stt.transcribe(audio)
        except Exception as exc:  # noqa: BLE001
            print(f"[listener] Erro de transcrição: {exc}")
            return
        t_stt = time.time() - t0
        print(
            f"[timing] STT (Whisper)={t_stt:.2f}s  texto={text!r}",
            flush=True,
        )

        if not text:
            return

        # Mention detector — sempre rápido (<10ms)
        t0 = time.time()
        result = detect_mention(text)
        t_mention = (time.time() - t0) * 1000

        if result.mentioned:
            print(
                f"[timing] mention={t_mention:.0f}ms  ✓ menção detectada",
                flush=True,
            )
            event = ListenerEvent(
                request=result.request_text,
                full_transcription=text,
                confidence=1.0,
                timestamp=start_time,
            )
            on_mention(event)
        else:
            print(
                f"[timing] mention={t_mention:.0f}ms  ✗ sem menção (descarto)",
                flush=True,
            )

    def stop(self) -> None:
        self._stop = True


if __name__ == "__main__":
    listener = LunaListener()

    def on_mention(event: ListenerEvent) -> None:
        print("\n  🔔 LUNA MENCIONADA")
        print(f"     Transcrição completa: {event.full_transcription!r}")
        print(f"     Pedido: {event.request!r}\n")

    try:
        listener.listen(on_mention)
    except KeyboardInterrupt:
        print("\n[listener] Terminado.")
