"""
Luna · Continuous (Always-On com Escuta Inteligente)
====================================================
Sem wake word. A Luna escuta sempre, mas só responde quando és tu (ou a Linda)
a chamá-la pelo nome em conversa natural.

Sub-fase: 1v.5 (Escuta Contínua Inteligente) + cronómetro de latência (A0).

Uso:
    python luna/brain/luna_continuous.py

Variáveis de ambiente:
    LUNA_MODEL, LUNA_WHISPER_MODEL, LUNA_TTS_MODEL_PATH,
    LUNA_FAMILY_CONFIG, LUNA_VAD_THRESHOLD
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

os.environ.setdefault("OLLAMA_KEEP_ALIVE", "2h")

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from ollama import chat  # noqa: E402
from rich.console import Console
from rich.panel import Panel

from luna.audio.listener import LunaListener, ListenerEvent  # noqa: E402
from luna.audio.stt import LunaSTT  # noqa: E402
from luna.audio.tts import LunaTTS  # noqa: E402
from luna.brain.luna_chat import (  # noqa: E402
    GENERATION_OPTIONS,
    MODEL,
    build_system_prompt,
    load_family,
)
from luna.utils.timing import StageTimer  # noqa: E402

console = Console()


def build_panel(model: str, owner_name: str) -> Panel:
    return Panel.fit(
        f"[bold cyan]Luna · Escuta Contínua[/bold cyan]\n"
        f"[dim]LLM: {model}[/dim]\n"
        f"[dim]Olá, {owner_name}. Diz 'Luna' em conversa para me chamares. "
        f"Ctrl+C para terminar.[/dim]",
        border_style="cyan",
    )


def main() -> None:
    family = load_family()
    owner_name = family["owner"]["name"]
    system_prompt = build_system_prompt(family)

    console.print(build_panel(MODEL, owner_name))

    # Carregar componentes (a ordem importa)
    stt = LunaSTT()  # carregada uma só vez, partilhada com listener
    tts = LunaTTS()
    listener = LunaListener(stt=stt)

    # Saudação inicial discreta
    greeting = f"Estou aqui, {owner_name}."
    console.print(f"\n[bold magenta]Luna[/bold magenta] {greeting}")
    tts.say(greeting)

    history = [{"role": "system", "content": system_prompt}]

    def on_mention(event: ListenerEvent) -> None:
        """Callback chamado pela escuta cada vez que 'Luna' é dita."""
        request = event.request.strip()
        console.print(f"\n[dim italic]> {event.full_transcription}[/dim italic]")

        if not request:
            # Foi mencionada mas não se segue pedido (ex: "Luna?", "olá Luna")
            ack = f"Sim, {owner_name}?"
            console.print(f"[bold magenta]Luna[/bold magenta] {ack}")
            tts.say(ack)
            return

        history.append({"role": "user", "content": request})

        # Cronómetro de latência (Passo A0)
        timer = StageTimer()

        # LLM
        console.print("\n[bold magenta]Luna[/bold magenta] ", end="")
        response_text = ""
        try:
            timer.start("llm")
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

            # Falar
            timer.start("tts")
            tts.say(response_text)
            timer.stop()

            console.print(f"[dim]{timer.report()}[/dim]")
        except Exception as exc:  # noqa: BLE001
            timer.stop()
            console.print(f"\n[bold red]Erro LLM:[/bold red] {exc}")

    try:
        listener.listen(on_mention)
    except KeyboardInterrupt:
        console.print(f"\n[dim]A terminar. Até logo, {owner_name}.[/dim]")
        tts.say(f"Até logo, {owner_name}.")


if __name__ == "__main__":
    main()
