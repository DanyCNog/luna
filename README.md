# 🤖 Luna

Assistente robótica pessoal 100% local, privada, em PT-PT.

## Estrutura

- `docs/` — arquitectura, progresso, manuais
- `luna/` — código-fonte da Luna (Python)
  - `core/` — loop principal, orquestração
  - `audio/` — STT (Whisper), TTS (Piper), wake word
  - `vision/` — câmara, reconhecimento facial, YOLO
  - `memory/` — ChromaDB, RAG, persistência
  - `brain/` — LLM, routing de modelos
  - `personality/` — prompts, respostas, tom
  - `web/` — PWA, API FastAPI
  - `utils/` — helpers diversos
- `models/` — modelos IA descarregados (não vai para Git)
- `data/` — base de dados, memórias, faces (não vai para Git)
- `logs/` — logs de execução
- `config/` — ficheiros de configuração
- `scripts/` — scripts utilitários
- `tests/` — testes automáticos

## Fase actual

Fase 1-virtual — Sub-fase 1v.1 (ambiente base)

## Como começar

```bash
cd ~/luna
source .venv/bin/activate
# próximos passos no manual da sub-fase
```
