"""
Luna · Voice Full (STT → LLM → TTS)
===================================
Carrega Enter para começar a gravar, fala a tua pergunta,
a Luna transcreve, pensa, e responde-te por voz.

Fechamento do ciclo audível completo.

Sub-fase: 1v.4 (Voz TTS).

Uso:
    python luna/brain/luna_voice_full.py

Variáveis de ambiente relevantes:
    LUNA_MODEL, LUNA_WHISPER_MODEL, LUNA_TTS_MODEL_PATH,
    LUNA_FAMILY_CONFIG, OLLAMA_KEEP_ALIVE
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

os.environ.setdefault("OLLAMA_KEEP_ALIVE", "2h")

# Permitir importar módulos irmãos
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from ollama import chat  # noqa: E402
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

from luna.audio.stt import LunaSTT  # noqa: E402
from luna.audio.tts import LunaTTS  # noqa: E402
from luna.brain.luna_chat import (  # noqa: E402
    GENERATION_OPTIONS,
    MODEL,
    build_system_prompt,
    load_family,
)

console = Console()

DEFAULT_RECORD_SECONDS = 5.0


def build_panel(model: str, owner_name: str, whisper_model: str, tts_name: str) -> Panel:
    return Panel.fit(
        f"[bold cyan]Luna · Voice Full[/bold cyan]\n"
        f"[dim]LLM: {model}  ·  STT: whisper-{whisper_model}  ·  TTS: {tts_name}[/dim]\n"
        f"[dim]Olá, {owner_name}. Carrega Enter para falar, 'sair' para terminar.[/dim]",
        border_style="cyan",
    )


def main() -> None:
    family = load_family()
    owner_name = family["owner"]["name"]
    system_prompt = build_system_prompt(family)

    whisper_model = os.environ.get("LUNA_WHISPER_MODEL", "medium")
    tts_path = Path(os.environ.get(
        "LUNA_TTS_MODEL_PATH",
        str(Path(__file__).resolve().parents[2] / "models" / "tts" / "pt_PT-tugao-medium.onnx"),
    ))
    tts_name = tts_path.stem

    console.print(build_panel(MODEL, owner_name, whisper_model, tts_name))

    stt = LunaSTT()
    tts = LunaTTS()

    history = [{"role": "system", "content": system_prompt}]

    # Saudação inicial
    greeting = f"Olá {owner_name}, estou a ouvir-te."
    console.print(f"\n[bold magenta]Luna[/bold magenta] {greeting}")
    tts.say(greeting)

    while True:
        try:
            action = Prompt.ask(
                f"\n[bold green]{owner_name}[/bold green] "
                "[dim](Enter para falar · 'sair' para terminar)[/dim]",
                default="",
                show_default=False,
            )

            if action.strip().lower() in {"sair", "exit", "quit"}:
                farewell = f"Até logo, {owner_name}."
                console.print(f"[bold magenta]Luna[/bold magenta] {farewell}")
                tts.say(farewell)
                break

            # Gravar e transcrever
            user_input = stt.record_and_transcribe(duration=DEFAULT_RECORD_SECONDS)

            if not user_input:
                console.print("[dim](só silêncio detectado — tenta de novo)[/dim]")
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

            # Luna fala a resposta
            tts.say(response_text)

        except KeyboardInterrupt:
            console.print(f"\n[dim]Interrompido. Até logo, {owner_name}.[/dim]")
            break
        except Exception as exc:  # noqa: BLE001
            console.print(f"\n[bold red]Erro:[/bold red] {exc}")


if __name__ == "__main__":
    main()
