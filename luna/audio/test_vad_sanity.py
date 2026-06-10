"""Teste de sanidade do Silero VAD com sinal sintético."""

import numpy as np
import onnxruntime as ort
from pathlib import Path

MODEL_PATH = Path(__file__).resolve().parents[2] / "models" / "vad" / "silero_vad.onnx"
SAMPLE_RATE = 16000

# Carregar modelo
opts = ort.SessionOptions()
opts.intra_op_num_threads = 1
sess = ort.InferenceSession(str(MODEL_PATH), sess_options=opts,
                             providers=["CPUExecutionProvider"])

# Inspeccionar a API real do modelo
print("=== Inputs do modelo ===")
for inp in sess.get_inputs():
    print(f"  Nome: {inp.name}")
    print(f"  Forma: {inp.shape}")
    print(f"  Tipo: {inp.type}")
    print()

print("=== Outputs do modelo ===")
for out in sess.get_outputs():
    print(f"  Nome: {out.name}")
    print(f"  Forma: {out.shape}")
    print(f"  Tipo: {out.type}")
    print()

# Teste 1 — silêncio (deveria dar prob baixa)
silence = np.zeros(512, dtype=np.float32).reshape(1, -1)
state = np.zeros((2, 1, 128), dtype=np.float32)
sr = np.array(SAMPLE_RATE, dtype=np.int64)

try:
    out = sess.run(None, {"input": silence, "state": state, "sr": sr})
    print(f"Silêncio: prob={out[0][0][0]:.4f}")
except Exception as e:
    print(f"Erro com 'input/state/sr': {e}")
    # Tentar outra API
    try:
        out = sess.run(None, {"input": silence, "sr": sr})
        print(f"Silêncio (sem state): prob={out[0][0][0]:.4f}")
    except Exception as e2:
        print(f"Erro com 'input/sr': {e2}")

# Teste 2 — fala sintética (sinusoide a 200 Hz, parece voz)
t = np.linspace(0, 512/SAMPLE_RATE, 512, endpoint=False)
voice_like = (0.3 * np.sin(2*np.pi*200*t)).astype(np.float32).reshape(1, -1)
state = np.zeros((2, 1, 128), dtype=np.float32)

try:
    out = sess.run(None, {"input": voice_like, "state": state, "sr": sr})
    print(f"Sinusoide 200Hz: prob={out[0][0][0]:.4f}")
except Exception as e:
    print(f"Erro: {e}")

# Teste 3 — chunks consecutivos com sinusoide (VAD precisa de história)
print("\n=== Sequência de 30 chunks consecutivos com sinusoide ===")
state = np.zeros((2, 1, 128), dtype=np.float32)
for i in range(30):
    t = np.linspace(i*512/SAMPLE_RATE, (i+1)*512/SAMPLE_RATE, 512, endpoint=False)
    chunk = (0.3 * np.sin(2*np.pi*200*t)).astype(np.float32).reshape(1, -1)
    out = sess.run(None, {"input": chunk, "state": state, "sr": sr})
    prob = out[0][0][0]
    state = out[1]
    if i % 5 == 0:
        print(f"  Chunk {i:2d}: prob={prob:.4f}")
