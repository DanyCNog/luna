# 📓 LUNA — Diário de Bordo

> Registo cronológico de decisões, progressos, bloqueios e aprendizagens.

## 2026-04-20 — Fase 1-virtual — 1v.1 Ambiente base ✅

**Estado:** ✅ concluído
**O quê:** Preparar portátil Kali com Python, venv, Git, dependências de sistema e estrutura de pastas.
**Porquê:** Base limpa e isolada para construir a Luna-virtual sem interferências.
**Como foi feito:** Criei ~/luna/ com venv, .gitignore, estrutura de pastas, README. Instalei portaudio19-dev, ffmpeg, libsndfile1, build-essential. Primeiro commit feito.
**Resultado:** Ambiente pronto. Microfone e altifalantes funcionam. Git versiona o projecto.
**Notas:** [adiciona aqui se houve alguma surpresa, erro que resolveste, etc.]

**Formato de cada entrada:**
```
## [DATA] — [Fase] — [Título]

**Estado:** ⏳ em curso | ✅ concluído | ⚠️ bloqueado | ❌ abandonado
**O quê:**
**Porquê:**
**Como foi feito:**
**Resultado:**
**Notas:**
```

---

## 2026-04-19 — Fase 0 — Arranque do projeto ✅

**O quê:** Levantamento de requisitos: ambição, orçamento, conhecimentos, família, casa, cães.
**Resultado:** Âmbito definido — Luna 100% local, PT-PT, privada, aprende.
**Notas:** Dany = Python académico + cibersegurança. Nunca soldou. Sem ROS. Só portátil Kali 16GB. Router Vodafone Huawei 7.

---

## 2026-04-19 — Fase 0 — Hardware base ✅

**O quê:** Pi 5 + AI HAT+ 2 + Qwen 2.5 3B
**Resultado:** Orçamento ~760€ Fases 0-9, ~890€ com Fase 10.

---

## 2026-04-19 — Fase 0 — Requisitos detalhados ✅

**Decidido:**
- Saudações personalizadas (Dany vs Linda)
- Patrol 01h-06h, evita suite, tom baixo
- Proactividade alta dia 1
- Face ID sem PIN
- Sem gravação permanente
- Auto-destruição remota
- Anti-furto ping-rede (GPS adiado)
- Dany root, Linda admin
- Luna 20 msgs, app ilimitado
- Modo Guardião Médico Fase 11

---

## 2026-04-19 — Fase 0 — Upgrade Pi 5 16GB ✅

**O quê:** Confirmação Pi 5 **16GB** (não 8GB)
**Porquê:** Ao reavaliar, os 8GB extra desbloqueiam RAG em RAM, Whisper medium, YOLOv8s, dois cérebros, full-duplex, dashboard rica.
**Resultado:** Budget ~760€ fases 0-9.

---

## 2026-04-19 — Fase 0 — Estética v1, v2, v3 ✅

**Iteração 1:** capacete + viseira. Queixo grande (mal).  
**Iteração 2:** sem queixo, paleta azul gelo. Ecrã na vertical (mal).  
**Iteração 3 ✅:** ecrã horizontal 4:3, cabeça lisa sem orelhinhas.

**Decisões estéticas finais:**
- Branco mate + preto + azul gelo (`#85B7EB`)
- Capacete liso, viseira 82% da face
- Câmara invisível atrás do acrílico, LED verde gravação
- 2 anéis LED (topo + base corpo)
- Parafusos magnéticos N52
- 2 botões na base: verde power + vermelho reset
- Inclinação corpo 10-15° + tilt 45°

---

## 2026-04-20 — Fase 0 — Descoberta benchmarks AI HAT+ 2 ⚠️✅

**O quê:** Antes de finalizar lista de compras, verifiquei benchmarks reais (Jan 2026).
**Resultado crítico:** Pi 5 CPU é **MAIS rápido** que AI HAT+ 2 para LLMs.
- Qwen 2.5 1.5B: Pi CPU 11.7 tok/s vs Hailo 6.7 tok/s
- DeepSeek 1.5B: Pi CPU 9.0 tok/s vs Hailo 6.7 tok/s
- Razão: LLMs limitados por largura de banda de memória, não TOPS. Ambos usam LPDDR4X-4267.

**Revisão de estratégia:**
- LLM corre no Pi 5 CPU (não no Hailo)
- Hailo acelera Whisper STT + YOLOv8 visão (liberta CPU ~40%)
- 16GB tornam-se obrigatórios (para o LLM caber)
- Fase 1-virtual no Kali para validar modelos antes de comprar

**Notas:** Esta descoberta poupa potencialmente 190€ se testes mostrarem que Pi 5 sozinho chega.

---

## 2026-04-20 — Fase 0 — Plano de compra faseada ✅

**Decisão Dany:** prefere comprar tudo Vaga 1 mas vai poupar algumas semanas.

**Plano:**
1. **Agora:** Fase 1-virtual no Kali (sem custos)
2. **Quando poupado:** Vaga 1 (~440€) — Pi 5 16GB + HAT+ 2 + acessórios essenciais
3. **Seguinte:** Vaga 2 (~110€) — microfones + coluna + ecrã + acrílico
4. **Fase 4:** Vaga 3 (~200€) — corpo completo
5. **Fase 10:** Vaga 4 (~130€) — LiDAR + SCD40 + dock premium

**Objectivo destas semanas:** preparar tudo exaustivamente, sem pressa.

---

## 2026-04-20 — Fase 0 — OS do Pi: Trixie ✅

**O quê:** Decidir OS final para o Pi 5 quando chegar.
**Porquê:** Dany levantou a questão Trixie vs Bookworm.
**Como foi feito:** Pesquisa em tempo real — Trixie saiu Out 2025, suporte AI HAT+ 2 adicionado Dez 2025. Docs oficiais Raspberry Pi em Abril 2026 dizem explicitamente que AI HAT+ 2 requer Trixie.
**Resultado:** Decidido Raspberry Pi OS 64-bit **Trixie** (Debian 13).
**Notas:** Atenção a Python 3.13 — algumas bibliotecas podem precisar de Docker (ex.: Open WebUI). Para Fase 1-virtual no Kali isto é irrelevante (Kali é independente).

---

## Índice de fases

| Fase | Estado | Notas |
|---|---|---|
| 0 — Arquitectura + Estética | ✅ Concluída | v0.4 |
| **1-virtual — Luna no Kali** | ⏳ **A iniciar** | Sub-fases 1v.1 a 1v.10 |
| 1 — Migração Pi | 🔒 Aguarda hardware | Vaga 1+2 |
| 2 — Personalidade TFT real | 🔒 | — |
| 3 — Visão família | 🔒 | — |
| 4 — Corpo | 🔒 Aguarda Vaga 3 | — |
| 5 — Navegação | 🔒 | — |
| 6 — Pan/tilt | 🔒 | — |
| 7 — PWA + HA? | 🔒 | — |
| 8 — Patrol | 🔒 | — |
| 9 — Hardening | 🔒 | — |
| 10 — LiDAR + SCD40 | 🔒 Aguarda Vaga 4 | — |
| 11 — Guardião Médico | 🔒 | A definir |

---

## Template

```
## AAAA-MM-DD — Fase N — Título

**Estado:**
**O quê:**
**Porquê:**
**Como foi feito:**
**Resultado:**
**Notas:**
```
