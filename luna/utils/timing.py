"""Cronómetro simples por etapa para medir latência do pipeline."""
import time


class StageTimer:
    def __init__(self):
        self.stages = {}
        self._start = None
        self._stage = None

    def start(self, stage: str):
        """Termina a etapa anterior (se houver) e inicia uma nova."""
        now = time.monotonic()
        if self._stage is not None:
            self.stages[self._stage] = now - self._start
        self._stage = stage
        self._start = now

    def stop(self):
        """Termina a etapa actual."""
        if self._stage is not None:
            self.stages[self._stage] = time.monotonic() - self._start
            self._stage = None

    def report(self) -> str:
        """Devolve um relatório formatado com os tempos por etapa."""
        total = sum(self.stages.values())
        linhas = [f"  {k:<12} {v:6.2f}s" for k, v in self.stages.items()]
        linhas.append(f"  {'TOTAL':<12} {total:6.2f}s")
        return "\n".join(linhas)
