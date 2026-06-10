"""Streaming TTS por frase: o LLM produz, o Piper consome em paralelo."""
import queue
import re
import threading

_FIM_FRASE = re.compile(r"(?<=[.!?…])\s+")
_SENTINELA = None  # marca o fim do stream


class SentenceStreamer:
    def __init__(self, tts):
        """tts: instância de LunaTTS — usa o método .say(texto), bloqueante."""
        self.tts = tts
        self.fila = queue.Queue()
        self.thread = None
        self.frases_enviadas = 0

    def _consumidor(self):
        while True:
            frase = self.fila.get()
            if frase is _SENTINELA:
                break
            try:
                self.tts.say(frase)
            except Exception as e:
                print(f"[TTS] falha numa frase: {e}")

    def start(self):
        """Arranca a thread consumidora. Chamar uma vez por resposta."""
        self.thread = threading.Thread(target=self._consumidor, daemon=True)
        self.thread.start()

    def feed(self, buffer: str) -> str:
        """Recebe o buffer acumulado; envia frases completas para a fila;
        devolve o resto (frase ainda incompleta)."""
        partes = _FIM_FRASE.split(buffer)
        for frase in partes[:-1]:
            frase = frase.strip()
            if frase:
                self.fila.put(frase)
                self.frases_enviadas += 1
        return partes[-1]

    def finish(self, resto: str = ""):
        """Envia o que restar, fecha a fila e espera a fala terminar."""
        resto = resto.strip()
        if resto:
            self.fila.put(resto)
            self.frases_enviadas += 1
        self.fila.put(_SENTINELA)
        if self.thread:
            self.thread.join()
