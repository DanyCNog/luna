"""Contexto temporal injectado no system prompt a cada interacção."""
import json
import locale
import time
from datetime import datetime
from pathlib import Path

ESTADO = Path(__file__).resolve().parents[2] / "data" / "estado_luna.json"

try:
    locale.setlocale(locale.LC_TIME, "pt_PT.UTF-8")
except locale.Error:
    pass  # sem locale PT, os nomes saem em inglês — não é fatal


def _carregar() -> dict:
    if ESTADO.exists():
        try:
            return json.loads(ESTADO.read_text())
        except json.JSONDecodeError:
            return {}
    return {}


def _guardar(d: dict) -> None:
    ESTADO.parent.mkdir(exist_ok=True)
    ESTADO.write_text(json.dumps(d))


def contexto_temporal() -> str:
    """Devolve linhas de contexto para anexar ao system prompt.

    Actualiza o timestamp da última interacção como efeito secundário.
    """
    agora = datetime.now()
    estado = _carregar()
    ultima = estado.get("ultima_interaccao")

    linhas = [
        f"Agora são {agora.strftime('%H:%M')} de "
        f"{agora.strftime('%A, %d de %B')}."
    ]

    if ultima is None:
        linhas.append("É a primeira interacção de sempre.")
    else:
        delta_h = (time.time() - ultima) / 3600
        if datetime.fromtimestamp(ultima).date() != agora.date():
            linhas.append("É a primeira conversa de hoje.")
        elif delta_h >= 1:
            linhas.append(f"Não falam há cerca de {int(delta_h)}h.")

    if 1 <= agora.hour < 6:
        linhas.append(
            "É de madrugada — podes estranhar que ainda estejam acordados."
        )

    estado["ultima_interaccao"] = time.time()
    _guardar(estado)
    return "\n".join(linhas)
