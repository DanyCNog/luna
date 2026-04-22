"""
Luna · Voice Chat (STT → LLM)
=============================
Carrega Enter para começar a gravar, fala durante 5s (ou até ficares calado),
a Luna transcreve e o LLM responde em texto.

Na próxima sub-fase (1v.4) acrescentamos TTS — a Luna passa a responder por voz.

Uso:
    python luna/brain/luna_voice_chat.py

Variáveis de ambiente (ver luna_chat.py):
    LUNA_MODEL, OLLAMA_KEEP_ALIVE, LUNA_FAMILY_CONFIG, LUNA_WHISPER_MODEL
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

os.environ.setdefault("OLLAMA_KEEP_ALIVE", "2h")

# Permitir importar módulos irmãos (luna.audio.stt) quando corrido directamente
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from ollama import chat  # noqa: E402
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

from luna.audio.stt import LunaSTT  # noqa: E402
from luna.brain.luna_chat import (  # noqa: E402
    GENERATION_OPTIONS,
    MODEL,
    build_system_prompt,
    load_family,
)

console = Console()

DEFAULT_RECORD_SECONDS = 5.0


def build_panel(model: str, owner_name: str, whisper_model: str) -> Panel:
    return Panel.fit(
        f"[bold cyan]Luna · Voice Chat[/bold cyan]\n"
        f"[dim]LLM: {model}  ·  STT: whisper-{whisper_model}  ·  "
        f"Keep-alive: {os.environ['OLLAMA_KEEP_ALIVE']}[/dim]\n"
        f"[dim]Olá, {owner_name}. Carrega Enter para falar, escreve 'sair' para terminar.[/dim]",
        border_style="cyan",
    )


def main() -> None:
    family = load_family()
    owner_name = family["owner"]["name"]
    system_prompt = build_system_prompt(family)

    whisper_model = os.environ.get("LUNA_WHISPER_MODEL", "medium")
    console.print(build_panel(MODEL, owner_name, whisper_model))

    stt = LunaSTT()
    history = [{"role": "system", "content": system_prompt}]

    while True:
        try:
            action = Prompt.ask(
                f"\n[bold green]{owner_name}[/bold green] "
                "[dim](Enter para falar · 'sair' para terminar)[/dim]",
                default="",
                show_default=False,
            )

            if action.strip().lower() in {"sair", "exit", "quit"}:
                console.print(f"[dim]Até logo, {owner_name}.[/dim]")
                break

            # Gravar e transcrever
            user_input = stt.record_and_transcribe(duration=DEFAULT_RECORD_SECONDS)

            if not user_input:
                console.print("[dim](só silêncio detectado — tenta novamente)[/dim]")
                continue

            console.print(f"[dim italic]> {user_input}[/dim italic]")
            history.append({"role": "user", "content": user_input})

            console.print("\n[bold magenta]Luna[/bold magenta] ", end="")
            response_text = ""

            stream = chat(
                model=MODEL,
                messages=history,
                stream=True,
                think=False,
                options=GENERATION_OPTIONS,
            )
            for chunk in stream:
                piece = chunk["message"]["content"]
                response_text += piece
                console.print(piece, end="", style="white")

            console.print()
            history.append({"role": "assistant", "content": response_text})

        except KeyboardInterrupt:
            console.print(f"\n[dim]Interrompido. Até logo, {owner_name}.[/dim]")
            break
        except Exception as exc:  # noqa: BLE001
            console.print(f"\n[bold red]Erro:[/bold red] {exc}")


if __name__ == "__main__":
    main()
