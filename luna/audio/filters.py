"""Filtro de transcrições inúteis: descarta lixo antes de gastar CPU."""
import re

# Fonemas/interjeições sem conteúdo
_VAZIOS = {"ah", "hm", "uhm", "uh", "eh", "hum", "mm", "hmm", "ah ah", "ya"}

_SO_PONTUACAO = re.compile(r"^[\W_]+$")


def transcricao_util(texto: str) -> bool:
    """True se a transcrição merece ser processada."""
    t = texto.strip().lower()
    if len(t) < 5:
        return False
    if _SO_PONTUACAO.match(t):
        return False
    if t.strip(".,!?…") in _VAZIOS:
        return False
    return True
