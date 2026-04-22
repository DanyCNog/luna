# 🤖 LUNA — Documento de Arquitectura

> Assistente robótica pessoal 100% local, privada e fluida para a família Dany, Linda, Ivy (Samoieda) e Thor (Lulu da Pomerânia).

**Versão:** 0.4 — Fase 1-virtual adicionada
**Data:** Abril 2026
**Estado:** A iniciar Fase 1-virtual no Kali

---

## 1. Princípios do projeto

1. **100% local.** Zero cloud. Zero APIs pagas. Zero subscrições.
2. **Privacidade e segurança por defeito.** VPN cifrada sempre.
3. **Português de Portugal nativo.** Entende inglês e espanhol, responde só PT-PT.
4. **Fluida, não instantânea.** 1-2s latência em perguntas simples.
5. **Aprende sem ficar mais lenta.** RAG em RAM, escrita assíncrona.
6. **Falha com elegância.**
7. **Por fases.** Nunca avança sem a anterior funcional.
8. **Valida antes de comprar.** Tudo o que pode ser testado em software é testado antes de hardware.

---

## 2. Identidade & personalidade

- **Nome:** Luna
- **Wake word:** "Luna"
- **Voz:** Feminina, jovem, PT-PT — Piper TTS (voz exacta a decidir)
- **Proactividade:** Alta
- **Idiomas:** Fala PT-PT. Entende inglês e espanhol.

### Saudações

| Quem | Saudação |
|---|---|
| Dany | "Olá Dany!" |
| Linda | "Oi oooiii, bem-vinda de volta!" |
| Visita conhecida | "Olá [Nome]!" + contexto |
| Visita desconhecida | "Bem-vindo, pode apresentar-se?" → registo |
| Ivy / Thor | Festinha visual nos olhos |

### Pessoas conhecidas

| Pessoa | Info |
|---|---|
| Dany | 31, 22/09/1994, Cybersecurity Architect (ES), 1.87m |
| Linda | 32, 28/09/1993, Professora Doutorada |
| Ivy | Samoieda fêmea |
| Thor | Lulu Pomerânia macho |

---

## 3. Especificações físicas e estética

### Dimensões

| Atributo | Valor |
|---|---|
| Altura total | 36-38 cm |
| Cabeça | 17×18×8 cm |
| Ecrã viseira | 3.5" TFT IPS **horizontal 4:3** |
| Peso | 1.8-2.2 kg |
| Inclinação corpo | 10-15° para trás |
| Tilt cabeça | até 45° acima horizontal |

### Estética

| Elemento | Decisão |
|---|---|
| Paleta | Branco mate · preto mate · azul gelo (`#85B7EB`) |
| Cabeça | Capacete liso, sem queixo, sem orelhinhas |
| Viseira | Acrílico fumado único, 82% da face, esconde câmara |
| Câmara NoIR | Invisível atrás do acrílico · LED verde quando grava |
| Olhos | Grandes, lado a lado, azul gelo, respiração na dock |
| Pescoço | Curto, grosso, cinza claro |
| Corpo | Rover integrado, largo e baixo |
| Anéis LED | 2 paralelos: topo corpo + base |
| Grelha coluna | Pequenos furos discretos no peito |
| Lagartas | Borracha silenciosa preta |
| Carcaça | Parafusos magnéticos N52 |
| Botões | 2 na base escondidos: verde=power, vermelho=reset |

### Velocidades

| Modo | Velocidade |
|---|---|
| Normal | ~0.4 m/s |
| Patrol | ~0.15 m/s |
| Rápido | ~0.6 m/s |

### Autonomia
- 4× 18650 Samsung 30Q 3000mAh
- 5-6h uso activo, noite em Patrol com rondas intercaladas
- Volta à dock a 25%, recarrega 20min, sai para próxima ronda

---

## 4. Realidade técnica dos benchmarks (Abril 2026)

**Descoberta importante durante a Fase 0:**

| Teste | AI HAT+ 2 | Pi 5 CPU |
|---|---|---|
| Qwen 2.5 1.5B | 6.7 tok/s | 11.7 tok/s |
| DeepSeek R1 1.5B | 6.7 tok/s | 9.0 tok/s |

**Razão:** LLMs são limitados pela largura de banda de memória, não TOPS. Pi 5 e Hailo-10H usam LPDDR4X-4267 (similar). O CEO da Raspberry Pi confirmou.

**Consequência prática:**
- **LLM corre no Pi 5 CPU** (mais rápido)
- **Hailo acelera apenas Whisper + YOLOv8 visão**
- **16GB são OBRIGATÓRIOS** (não opcional) para o LLM caber no Pi
- Esta divisão de trabalho é óptima — Pi pensa, Hailo vê/ouve

### Nota sobre OS — Trixie (Abril 2026)

O AI HAT+ 2 **requer Raspberry Pi OS Trixie** (Debian 13). O suporte foi adicionado em Dezembro 2025, depois de alguns meses de incompatibilidade inicial. Bookworm está em modo legacy.

**Atenção:** Trixie usa Python 3.13, que quebra algumas bibliotecas Python mais antigas. Estratégia:
- Código principal da Luna corre em venv com Python 3.12 quando necessário
- Componentes problemáticos (ex.: Open WebUI) correm em Docker
- A maioria das bibliotecas (Whisper, Piper, ChromaDB, llama.cpp) já suportam 3.13

---

## 5. Arquitectura de hardware (BOM)

> **Compra em fases** (poupança a decorrer).
> **Primeira vaga:** Pi 5 16GB + HAT+ 2 + acessórios essenciais (~440€).

### Vaga 1 — Core essencial (~€440)

| # | Componente | Modelo | Loja | Preço est. |
|---|---|---|---|---|
| 1 | Pi 5 **16GB** | Raspberry Pi 5 16GB | PTRobotics | ~170€ |
| 2 | AI HAT+ 2 | Raspberry Pi AI HAT+ 2 (40 TOPS) | PTRobotics | ~190€ |
| 3 | Cooler activo | Raspberry Pi Active Cooler | PTRobotics | ~5€ |
| 4 | microSD | SanDisk Extreme 128GB A2 | Amazon.pt | ~20€ |
| 5 | PSU bancada | PSU oficial 27W USB-C | PTRobotics | ~15€ |
| 6 | Câmara | Pi Camera 3 NoIR | PTRobotics | ~35€ |

**Subtotal vaga 1:** ~€435

### Vaga 2 — Completa Fase 1 (~€110)

| # | Componente | Loja | Preço |
|---|---|---|---|
| 7 | ReSpeaker 4-Mic | PTRobotics | ~75€ |
| 8 | Coluna USB 3W | Aliexpress | ~10€ |
| 9 | Ecrã 3.5" TFT IPS SPI 4:3 | Aliexpress | ~15€ |
| 10 | Acrílico fumado 10×10cm | Aliexpress | ~5€ |
| 11 | Cabo CSI FFC 30cm | Aliexpress | ~3€ |
| 12 | LED IR 850nm | Aliexpress | ~5€ |

### Vaga 3 — Corpo (Fase 4, ~€200)

Chassis, motores, baterias, sensores, LEDs, botões — ver lista completa em `LUNA_BOM_COMPLETE.md` quando chegarmos à Fase 4.

### Vaga 4 — Upgrades Fase 10 (~€130)

SCD40, LiDAR LD19, dock premium.

### Ferramentas (~€30)

Ferro de soldar T12, solda, multímetro.

### Totais

| Cenário | Valor |
|---|---|
| Fases 0-9 completas | **~€780** |
| Com Fase 10 | **~€910** |

---

## 6. Arquitectura de software

### Stack

| Camada | Tecnologia | Onde |
|---|---|---|
| OS | **Raspberry Pi OS 64-bit Trixie** (Debian 13) | Pi 5 |
| Runtime LLM | **llama.cpp** (Pi CPU) + hailo-ollama (Hailo, só se útil) | Pi 5 + HAT |
| **LLM primário** | **Qwen 2.5 3B** (Q4_K_M) no CPU | Pi 5 |
| **LLM alternativo** | Gemma 3 4B / Qwen 2 1.5B (via Hailo) | a testar |
| Wake word | openWakeWord custom "Luna" | Pi 5 CPU |
| Som anómalo | YAMNet paralelo | Pi 5 CPU |
| Speech-to-text | Whisper (Hailo-acelerado) | AI HAT+ 2 |
| Text-to-speech | Piper TTS voz PT-PT | Pi 5 CPU |
| Full-duplex | Echo cancellation + VAD | Pi 5 |
| Face recognition | face_recognition + dlib | Pi CPU |
| Objects/dogs | YOLOv8s (Hailo) | AI HAT+ 2 |
| Memória | ChromaDB em RAM | Pi 5 |
| Dashboard | FastAPI + gráficos | Pi 5 |
| Orquestração | Python + asyncio | Pi 5 |
| Motor control | MicroPython | ESP32 |
| Streaming vídeo | GStreamer + WebRTC | Pi 5 |
| VPN | WireGuard | Pi 5 |

### Divisão de trabalho (crucial)

- **Pi 5 CPU:** LLM, TTS, orquestração, API, RAG, motor control via ESP32
- **AI HAT+ 2:** Whisper (STT), YOLOv8 (visão), liberta CPU ~40%

### Expressões dos olhos

| Estado | Aparência |
|---|---|
| Idle | Olhos normais, pisca ocasional |
| A ouvir | Olhos abrem mais, LED pulsa |
| A pensar | Olhos rolam |
| A falar | Acompanham entonação |
| Contente | `^ ^` |
| Atento | Ligeiramente maiores |
| Carinhoso (cães) | Coração ou `~ ~` |
| A dormir (dock) | Pálpebras baixas, respiração 3-4s |
| Preocupado | `\ /` |
| Apagado | Preto |

---

## 7. Segurança (resumo)

- **Canais:** WireGuard VPN + mTLS
- **Autenticação app:** Face ID apenas
- **Cifra em repouso:** LUKS + SQLCipher
- **Firewall:** UFW, só VPN + SSH custom + HTTPS local
- **Sem internet** por defeito
- **Anti-furto:** ping-rede 24/7
- **Auto-destruição:** botão "Wipe Luna" na app
- **Permissões:** Dany root, Linda admin

---

## 8. Memória & aprendizagem

- ChromaDB vectorial em RAM
- Top-5 memórias por similaridade antes de cada resposta
- Escrita assíncrona em idle
- Luna 20 msgs, app ilimitado

---

## 9. App PWA

- Face ID apenas
- Chat, vídeo WebRTC tempo real, dashboard, timeline, histórico
- Botão Wipe Luna
- Notificações push enriquecidas (localização, hora, contexto)

---

## 10. Modo Patrol

- 01h00 – 06h00 (ou sem humanos >2h)
- Evita suite, velocidade lenta silenciosa
- Olhos apagados · LEDs off
- YAMNet detecta anomalias
- Reagindo: tom baixo a humanos, ignora cães, alerta imediato a desconhecidos

---

## 11. Plano de fases

### 🆕 Fase 1-virtual — No Kali, **sem custos, começa já**

Enquanto o hardware não chega, construímos a Luna **inteira em software** no Kali para validar tudo.

**Objectivo:** Ter Luna a falar contigo em PT-PT, lembrar-se de factos e responder de forma natural, correndo no teu portátil Kali. Zero hardware extra.

**Sub-fases:**

1. **1v.1 — Ambiente base** (Python venv, dependências, Ollama)
2. **1v.2 — LLM local funcional** (Qwen 2.5 3B + Gemma 3 4B no Ollama, chat texto)
3. **1v.3 — Voz STT** (Whisper a transcrever PT-PT do teu microfone portátil)
4. **1v.4 — Voz TTS** (Piper a falar PT-PT pelos altifalantes — **escolher voz final**)
5. **1v.5 — Wake word** (openWakeWord treinado para "Luna")
6. **1v.6 — Personalidade** (prompt-sistema final, testes)
7. **1v.7 — Memória RAG** (ChromaDB + factos iniciais sobre a família)
8. **1v.8 — Orquestração** (loop principal asyncio: wake → STT → RAG → LLM → TTS)
9. **1v.9 — Olhos animados** (SVG animado visível no teu ecrã, como se fosse o TFT)
10. **1v.10 — Luna-virtual completa** (tudo integrado, conversa real em PT-PT)

**Duração estimada:** 3-4 semanas a 2-3h/semana.
**Output:** software pronto para migrar ao Pi em 1 dia quando chegar.

### Fases seguintes (quando hardware chegar)

| Fase | Objectivo | HW necessário | Duração |
|---|---|---|---|
| 1 | Migrar software para Pi 5 + testar STT/TTS/LLM no bench | Vaga 1 + Vaga 2 | 1-2 sem |
| 2 | Optimizar + olhos no TFT real + memória persistente | — | 2 sem |
| 3 | Visão: reconhece Dany, Linda, Ivy, Thor | — | 2 sem |
| 4 | Corpo: chassis, motores, bateria, dock | Vaga 3 | 3-4 sem |
| 5 | Navegação: SLAM rudimentar, anti-colisão | — | 3 sem |
| 6 | Cabeça pan/tilt integrada | — | 1 sem |
| 7 | PWA + WireGuard + streaming + decisão Home Assistant | — | 2-3 sem |
| 8 | Patrol + saudações + rotinas + pré-buffer vídeo | — | 2 sem |
| 9 | Hardening (LUKS, fail2ban, VLAN) | — | 1 sem |
| 10 | LiDAR + SCD40 + dock premium | Vaga 4 | 2 sem |
| 11 | Modo Guardião Médico (a definir) | — | — |

---

## 12. Formato de cada passo

Cada instrução segue sempre 4 secções:

1. **O quê** — resumo 1 frase
2. **Porquê** — contexto técnico
3. **Como** — passo-a-passo com comandos exactos
4. **Verificar** — como saber que ficou bem

Entrega: texto + diagramas + comandos + screenshots quando aplicável.

---

## 13. Decisões tomadas

(Compiladas desde o início do projecto — resumo)

- Altura 36-38cm · peso 1.8-2.2kg
- Pi 5 **16GB** + AI HAT+ 2 (compra faseada)
- **LLM no Pi CPU, Whisper+visão no Hailo** (revisto após benchmarks)
- Qwen 2.5 3B primário · Gemma 3 4B alt · Qwen 2 1.5B via Hailo a testar
- Piper TTS PT-PT · openWakeWord "Luna"
- YOLOv8s · face_recognition
- Bateria 4× 18650 · proactividade alta
- Full-duplex áudio · pré-buffer vídeo Fase 8
- PWA + Face ID · sem PIN · sem gravação permanente
- Anti-furto ping-rede · auto-destruição remota
- Dany root · Linda admin
- Luna 20 msgs · app ilimitado
- Patrol 01h-06h · evita suite
- Chassis rover integrado Aliexpress
- Ecrã 3.5" TFT **horizontal 4:3**
- Paleta branco mate + preto + azul gelo
- Cabeça sem queixo · sem orelhinhas
- Viseira "infinity black" esconde câmara · LED verde gravação
- 2 anéis LED · parafusos magnéticos · 2 botões base
- Inclinação corpo 10-15° + tilt 45°
- Olhos apagados em ausência · respiração na dock
- **Fase 1-virtual começa já no Kali sem custos**
- **OS do Pi: Raspberry Pi OS Trixie** (Debian 13, suporte oficial AI HAT+ 2)

---

## 14. Glossário

(mantém-se do v0.3)

---

*Documento vivo. Parceiro: `LUNA_PROGRESS.md`.*
