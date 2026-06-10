"""Respostas pré-definidas para quando o LLM está indisponível."""
import random

RESPOSTAS_OFFLINE = [
    "Estou aqui, mas o meu cérebro está com problemas. Aguenta um momento.",
    "Ouço-te, mas não consigo pensar agora. Tenta outra vez daqui a pouco.",
    "Estou com uma dor de cabeça digital. Dá-me um minuto.",
]


def resposta_offline() -> str:
    return random.choice(RESPOSTAS_OFFLINE)
