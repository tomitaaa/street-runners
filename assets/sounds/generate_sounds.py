"""
Gerador de efeitos sonoros 8-bit para Street Runners.
Salva arquivos WAV na pasta assets/.
Execute: python3 assets/generate_sounds.py
"""
import wave, struct, math, os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
SAMPLE_RATE = 44100


def save_wav(filename: str, samples: list[float], sample_rate: int = SAMPLE_RATE):
    path = os.path.join(OUTPUT_DIR, filename)
    with wave.open(path, "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)          # 16 bits
        wf.setframerate(sample_rate)
        for s in samples:
            val = int(max(-1.0, min(1.0, s)) * 32767)
            wf.writeframes(struct.pack("<h", val))
    print(f"✔ {filename}  ({len(samples)/sample_rate:.2f}s)")


def square_wave(freq: float, duration: float, amp: float = 0.4) -> list[float]:
    n = int(SAMPLE_RATE * duration)
    return [amp * (1.0 if math.sin(2*math.pi*freq*i/SAMPLE_RATE) >= 0 else -1.0)
            for i in range(n)]


def noise(duration: float, amp: float = 0.3) -> list[float]:
    import random
    n = int(SAMPLE_RATE * duration)
    return [amp * (random.random()*2-1) for _ in range(n)]


def mix(*tracks: list[float]) -> list[float]:
    length = max(len(t) for t in tracks)
    result = [0.0] * length
    for t in tracks:
        for i, v in enumerate(t):
            result[i] += v
    peak = max(abs(v) for v in result) or 1
    return [v/peak * 0.9 for v in result]


def fade_out(samples: list[float], fade_samples: int) -> list[float]:
    out = samples[:]
    for i in range(fade_samples):
        factor = 1.0 - i/fade_samples
        out[-(fade_samples-i)] *= factor
    return out


# ── Engine idle: onda quadrada com varredura de frequência ──────────────────
def engine_idle():
    samples = []
    base_freq = 80.0
    for beat in range(6):
        freq = base_freq + beat * 5
        samples += square_wave(freq, 0.08, 0.25)
        samples += square_wave(freq * 1.5, 0.04, 0.15)
    return fade_out(samples, 2000)

save_wav("engine_idle.wav", engine_idle())


# ── Engine acelerando: subida de frequência (chirp) ─────────────────────────
def engine_accel():
    n = int(SAMPLE_RATE * 1.2)
    samples = []
    for i in range(n):
        t = i / SAMPLE_RATE
        freq = 60 + 220 * (i/n)**1.5        # sobe rápido no final
        val = 0.3 * (1.0 if math.sin(2*math.pi*freq*t) >= 0 else -1.0)
        samples.append(val)
    return fade_out(samples, 3000)

save_wav("engine_accel.wav", engine_accel())


# ── Colisão: barulho curto com grave ────────────────────────────────────────
def crash():
    boom  = square_wave(55,  0.05, 0.5)
    crunch = noise(0.18, 0.6)
    ring   = square_wave(220, 0.12, 0.2)
    combined = mix(
        boom  + [0.0]*int(SAMPLE_RATE*0.18),
        [0.0]*int(SAMPLE_RATE*0.05) + crunch,
        [0.0]*int(SAMPLE_RATE*0.08) + ring + [0.0]*int(SAMPLE_RATE*0.07),
    )
    return fade_out(combined, 4000)

save_wav("crash.wav", crash())


# ── Contagem regressiva: bipes agudos ────────────────────────────────────────
def countdown_beep(freq=880):
    beep = square_wave(freq, 0.12, 0.35)
    silence = [0.0] * int(SAMPLE_RATE * 0.08)
    return beep + silence

save_wav("countdown_beep.wav", countdown_beep(880))
save_wav("countdown_go.wav",   countdown_beep(1320))


# ── Volta completada: fanfarra ascendente ────────────────────────────────────
def lap_complete():
    notes = [523, 659, 784, 1047]   # Dó-Mi-Sol-Dó8
    samples = []
    for freq in notes:
        samples += square_wave(freq, 0.12, 0.4)
        samples += [0.0] * int(SAMPLE_RATE * 0.03)
    return fade_out(samples, 2000)

save_wav("lap_complete.wav", lap_complete())


# ── Off-road: ruído grave ────────────────────────────────────────────────────
def offroad():
    base = noise(0.5, 0.4)
    rumble = square_wave(45, 0.5, 0.15)
    return mix(base, rumble)

save_wav("offroad.wav", offroad())

print("\nTodos os sons gerados em assets/")
