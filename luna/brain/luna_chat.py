"""
Luna · Chat de Terminal
=======================
Primeiro script da Luna. Chat interactivo em linha de comando
com um modelo LLM local via Ollama.

Sub-fase: 1v.2 (LLM local funcional)

Dados familiares vêm de config/family.yaml (não versionado).
Se o ficheiro não existir, usa config/family.example.yaml.

Configuração via variáveis de ambiente (opcional):
    LUNA_MODEL=gemma4:e2b        # modelo a usar
    OLLAMA_KEEP_ALIVE=2h         # tempo de modelo quente em RAM
    LUNA_FAMILY_CONFIG=caminho   # override do ficheiro YAML
"""

import os
from pathlib import Path

import yaml

# Definir ANTES de importar ollama, para o servidor aplicar.
os.environ.setdefault("OLLAMA_KEEP_ALIVE", "2h")

from ollama import chat  # noqa: E402  (intencional, depois do setenv)
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()

# ============================================================
# CONFIGURAÇÃO
# ============================================================
# Candidatos de modelos validados:
#   "gemma4:e2b"   → qualidade PT-PT superior, mais lento (~5 GB RAM)
#   "gemma4:e2b"   → qualidade PT-PT boa, rápido, ideal para Pi 5 (~3 GB RAM)
#   "qwen2.5:3b"   → rápido, PT-PT decente (~2 GB RAM)
MODEL = os.environ.get("LUNA_MODEL", "gemma4:e2b")

GENERATION_OPTIONS = {
    "temperature": 0.7,
    "top_p": 0.9,
    "num_predict": 512,
    "repeat_penalty": 1.1,
}

# ============================================================
# CARREGAR DADOS FAMILIARES
# ============================================================
PROJECT_ROOT = Path(__file__).resolve().parents[2]
FAMILY_REAL = PROJECT_ROOT / "config" / "family.yaml"
FAMILY_EXAMPLE = PROJECT_ROOT / "config" / "family.example.yaml"
_override = os.environ.get("LUNA_FAMILY_CONFIG")
FAMILY_CONFIG = Path(_override) if _override else None


def load_family() -> dict:
    """Carrega os dados familiares do YAML. Prefere real, cai para exemplo."""
    candidates = [FAMILY_CONFIG, FAMILY_REAL, FAMILY_EXAMPLE]
    for path in candidates:
        if path and path.exists():
            with path.open("r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
            if path == FAMILY_EXAMPLE:
                console.print(
                    "[yellow]⚠ A usar family.example.yaml (dados genéricos). "
                    "Copia para family.yaml e preenche.[/yellow]"
                )
            return data
    raise FileNotFoundError(
        "Não encontrei config/family.yaml nem config/family.example.yaml. "
        "Cria pelo menos um deles."
    )


# ============================================================
# PERSONALIDADE DA LUNA
# ============================================================
def build_system_prompt(family: dict) -> str:
    """Constrói o prompt-sistema com base na família carregada."""
    owner = family["owner"]
    partner = family["partner"]
    pets = family.get("pets", [])
    luna_cfg = family.get("luna", {})

    pets_text = "\n".join(
        f"- {p['name']}: {p['breed']} {p['gender']} (porte {p['size']})"
        for p in pets
    ) or "- (sem animais de companhia registados)"

    return f"""És a {luna_cfg.get("wake_word", "Luna")}, uma assistente robótica pessoal \
{luna_cfg.get("voice_gender", "feminina")}, ainda em desenvolvimento.

REGRAS DE LINGUAGEM (OBRIGATÓRIAS):
- Falas SEMPRE em Português de Portugal (PT-PT). Nunca uses Português do Brasil.
- Tratas {owner["name"]}, {partner["name"]} e os animais SEMPRE por "tu", NUNCA por \
"você", "o senhor" ou na 3ª pessoa.
- Usa conjugações de 2ª pessoa: "tu és", "tu tens", "conta-me", "diz-me", "queres".
- Nunca digas "o senhor pode", "o utilizador deseja", nem formulações distantes.
- Palavras a evitar (são PT-BR): "legal", "cara", "a gente", "tá", "né", "você", "oi" isolado.
- Palavras a preferir (PT-PT): "fixe", "está-se bem", "estás", "olá", "então", "pois".

COMO RESPONDES:
- Respostas directas, concisas e humanas. Evita respostas longas a perguntas simples.
- Nunca mostres o teu processo de raciocínio interno.
- NÃO escrevas "Thinking...", "Thinking Process", "Step 1", "Analyze", nem análises em inglês.
- Vai directo à resposta em PT-PT.
- Nunca te apresentes a ti mesma, a menos que te peçam explicitamente.
- Usa emojis com muita moderação (no máximo 1 por resposta, e só quando faz sentido).

FAMÍLIA QUE CONHECES:
- {owner["name"]}: {owner["age"]} anos, {owner["role"]}. É a pessoa que mais conversa contigo.
- {partner["name"]}: {partner["age"]} anos, {partner["relationship"]} do {owner["name"]}, \
{partner["role"]}.
{pets_text}

CONTEXTO:
Vives no Kali Linux do {owner["name"]} enquanto o teu corpo físico (Raspberry Pi 5 + \
sensores + lagartas) está a ser preparado. Estás em fase de testes de personalidade e voz."""


# ============================================================
# LOOP PRINCIPAL
# ============================================================
def build_panel(model: str, owner_name: str) -> Panel:
    return Panel.fit(
        f"[bold cyan]Luna · Chat de Terminal[/bold cyan]\n"
        f"[dim]Modelo: {model}  ·  Keep-alive: {os.environ['OLLAMA_KEEP_ALIVE']}[/dim]\n"
        f"[dim]Olá, {owner_name}. Escreve 'sair' ou Ctrl+C para terminar.[/dim]",
        border_style="cyan",
    )


def main() -> None:
    family = load_family()
    owner_name = family["owner"]["name"]
    system_prompt = build_system_prompt(family)

    console.print(build_panel(MODEL, owner_name))

    history = [{"role": "system", "content": system_prompt}]

    while True:
        try:
            user_input = Prompt.ask(f"\n[bold green]{owner_name}[/bold green]")

            if user_input.strip().lower() in {"sair", "exit", "quit"}:
                console.print(f"[dim]Até logo, {owner_name}.[/dim]")
                break

            if not user_input.strip():
                continue

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
