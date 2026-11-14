"""Erzeugt Soundeffekte rein per Code (keine Fremdquellen, kein Urheberrecht).
Aufruf: python3 sfx_synth.py <zielordner>"""
import sys, subprocess, numpy as np
SR = 44100
out = sys.argv[1] if len(sys.argv) > 1 else "."
rng = np.random.default_rng(7)
t_ = lambda d: np.arange(int(SR * d)) / SR
def env(n, a=0.005, r=0.2, d=None):
    t = np.arange(n) / SR; d = d or n / SR
    e = np.minimum(1, t / max(a, 1e-4)) * np.exp(-np.maximum(0, t - a) / r)
    return e
def lp(x, cut):  # einfacher Tiefpass
    a = np.exp(-2 * np.pi * cut / SR); y = np.zeros_like(x); s = 0.0
    for i, v in enumerate(x): s = (1 - a) * v + a * s; y[i] = s
    return y
def sweep_noise(d, f0, f1, q=0.15):  # Rauschen durch wandernden Bandpass -> Whoosh
    n = int(SR * d); x = rng.standard_normal(n); y = np.zeros(n); b1 = b2 = 0.0
    f = np.geomspace(f0, f1, n)
    for i in range(n):
        w = 2 * np.pi * f[i] / SR; r = 1 - q * w
        y[i] = x[i] + 2 * r * np.cos(w) * b1 - r * r * b2; b2, b1 = b1, y[i]
    return y / (np.abs(y).max() + 1e-9)
def save(name, x, peak=-4):
    x = x / (np.abs(x).max() + 1e-9) * 10 ** (peak / 20)
    fade = min(len(x), int(0.01 * SR)); x[-fade:] *= np.linspace(1, 0, fade)
    pcm = (x * 32767).astype(np.int16).tobytes()
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "s16le", "-ar", str(SR), "-ac", "1", "-i", "-", "-b:a", "192k", f"{out}/{name}.mp3"], input=pcm, check=True)
    print(name, f"{len(x)/SR:.2f}s")
# Pop: kurzer Ton, der schnell nach unten gleitet
t = t_(0.12); save("pop", np.sin(2 * np.pi * np.cumsum(np.geomspace(900, 300, len(t))) / SR) * env(len(t), 0.002, 0.03))
# Tick-Rolle: 22 Klicks, schneller werdend, am Ende ein kleines Ding
x = np.zeros(int(SR * 2.4)); tt = 0.0
for i in range(22):
    p = int(tt * SR); k = t_(0.012); x[p:p + len(k)] += np.sin(2 * np.pi * 2400 * k) * env(len(k), 0.0005, 0.003) * 0.8; tt += 0.07 * (0.97 ** i)
p = int(tt * SR); k = t_(0.5); x[p:p + len(k)] += (np.sin(2 * np.pi * 1760 * k) + 0.4 * np.sin(2 * np.pi * 3520 * k)) * env(len(k), 0.002, 0.12)
save("tick", x[: p + len(k)])
# Whoosh: Rauschen, Bandpass wandert hoch und runter, Lautstärke an- und abschwellend
d = 0.9; n = int(SR * d); w = sweep_noise(d, 300, 2500) * np.sin(np.pi * np.linspace(0, 1, n)) ** 2; save("whoosh", w)
# Swoosh: kürzer, heller, nach vorne
d = 0.45; n = int(SR * d); w = sweep_noise(d, 900, 5000, 0.2) * np.sin(np.pi * np.linspace(0, 1, n) ** 0.6) ** 2; save("swoosh", w)
# Riser: zwei verstimmte Sägezähne + Rauschen, steigend, endet abrupt
d = 2.5; t = t_(d); f = np.geomspace(110, 880, len(t))
saw = lambda f: 2 * ((np.cumsum(f) / SR) % 1) - 1
x = (saw(f) + saw(f * 1.01)) * 0.4 + sweep_noise(d, 400, 6000) * 0.5; x = lp(x, 3500) * np.linspace(0.05, 1, len(t)) ** 2; save("riser", x)
# Einschlag: Sub-Fall + Rauschstoß
t = t_(1.6); sub = np.sin(2 * np.pi * np.cumsum(np.geomspace(120, 35, len(t))) / SR) * env(len(t), 0.003, 0.5)
nz = lp(rng.standard_normal(len(t)), 1800) * env(len(t), 0.001, 0.08); save("hit", sub + nz * 0.8)
# Glöckchen: harmonische Teiltöne mit Abklingen
t = t_(1.4); f0 = 1318.5; x = sum(a * np.sin(2 * np.pi * f0 * m * t) * np.exp(-t * (2.5 + m)) for m, a in [(1, 1), (2.01, 0.5), (3.02, 0.3), (4.2, 0.15)])
save("chime", x * np.minimum(1, t / 0.003))
# Blips: Folge kurzer Töne, ansteigend
x = np.zeros(int(SR * 1.3))
for i in range(16):
    p = int(i * 0.07 * SR); k = t_(0.05); x[p:p + len(k)] += np.sin(2 * np.pi * (600 + i * 45) * k) * env(len(k), 0.001, 0.015)
save("blips", x)
