"""
Detector de menção do nome "Luna" em texto transcrito.

Lida com:
- Capitalização variável: Luna, luna, LUNA
- Possível confusão com palavras parecidas (lua, lula) — usa boundaries
- Falsos positivos comuns: "lua nova", "Luna Park", "lua de mel"
- Captura o que vem após a menção (o pedido real)
"""

from __future__ import annotations

import re
from dataclasses import dataclass

# Padrão: "Luna" como palavra inteira, com fronteiras claras
# (?:^|\W) = início ou caracter não-letra antes
# luna     = a palavra
# (?:\W|$) = caracter não-letra ou fim depois
LUNA_PATTERN = re.compile(r"(?:^|\W)luna(?:\W|$)", re.IGNORECASE)

# Falsos positivos a filtrar — se o "Luna" aparece DENTRO destes contextos,
# não é uma menção genuína à Luna.
FALSE_POSITIVE_CONTEXTS = [
    r"\bluna park\b",
    r"\blua nova\b",
    r"\blua de mel\b",
    r"\blua cheia\b",
    r"\blua minguante\b",
    r"\blua crescente\b",
]
FALSE_POSITIVE_RE = re.compile(
    "|".join(FALSE_POSITIVE_CONTEXTS), re.IGNORECASE,
)


@dataclass
class MentionResult:
    """Resultado da análise de menção."""

    mentioned: bool
    request_text: str  # o que vem após "Luna" (ou texto vazio)
    raw_text: str       # texto original transcrito


def detect_mention(transcription: str) -> MentionResult:
    """Verifica se 'Luna' foi mencionada no texto.

    Devolve `MentionResult` com:
    - mentioned: True/False
    - request_text: o que vem depois de "Luna" (sem o nome)
    - raw_text: o input original
    """
    text = transcription.strip()
    if not text:
        return MentionResult(False, "", text)

    # 1. Filtrar falsos positivos óbvios
    if FALSE_POSITIVE_RE.search(text):
        # Se o ÚNICO "Luna" no texto está num contexto falso positivo,
        # rejeita. Mas se houver uma menção SEPARADA, aceita.
        cleaned = FALSE_POSITIVE_RE.sub("", text)
        if not LUNA_PATTERN.search(cleaned):
            return MentionResult(False, "", text)
        text = cleaned

    # 2. Procurar menção
    match = LUNA_PATTERN.search(text)
    if not match:
        return MentionResult(False, "", transcription)

    # 3. Extrair o que vem depois da menção
    after = text[match.end():].strip()
    # Remover pontuação inicial residual (vírgula, ponto, etc.)
    after = re.sub(r"^[,.;:!?\s]+", "", after)

    return MentionResult(True, after, transcription)


if __name__ == "__main__":
    # Bateria de testes
    cases = [
        "Olá Luna, podes ligar a luz?",
        "luna que horas são",
        "Luna, ajuda-me!",
        "A lua nova é amanhã",         # falso positivo
        "Vamos ao Luna Park no domingo",  # falso positivo
        "Não sei, talvez a Luna saiba",
        "É lua de mel ainda",          # falso positivo
        "linda diz que a luna sabe",
        "mais devagar por favor",       # sem menção
        "",                             # vazio
        "luna",                         # só o nome
    ]
    for case in cases:
        r = detect_mention(case)
        flag = "✓ MENCIONADA" if r.mentioned else "✗ ignora"
        print(f"  {flag:14s}  in={case!r:50s}  request={r.request_text!r}")
