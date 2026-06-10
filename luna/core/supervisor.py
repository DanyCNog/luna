"""Supervisor: mantém o ciclo vivo e regista todas as falhas."""
import logging
import traceback
from pathlib import Path

LOG_DIR = Path(__file__).resolve().parents[2] / "logs"
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    filename=LOG_DIR / "luna.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
log = logging.getLogger("luna.supervisor")

FALLBACKS = {
    "stt": "Não te consegui ouvir bem. Podes repetir?",
    "llm": "Tive um problema a pensar. Podes repetir?",
    "tts": None,       # se o TTS falhou, não há como falar — fica só no log
    "listener": None,
}


def protegido(componente: str, fn, *args, **kwargs):
    """Executa fn(*args, **kwargs).

    Devolve (resultado, None) em caso de sucesso,
    ou (None, frase_fallback) em caso de erro — com o erro completo no log.
    """
    try:
        return fn(*args, **kwargs), None
    except Exception:
        log.error("Falha em %s:\n%s", componente, traceback.format_exc())
        return None, FALLBACKS.get(componente)
