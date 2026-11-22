"""Selbst erzeugte, lizenzfreie Spannungsmusik (kein fremdes Material).
Aufruf: python3 tools/musik.py <dauer> <pause_start> <finale> [bpm]  -> assets/musik.wav
  0 .. pause_start      : treibender Spannungs-Loop (a-Moll), wird lauter/dichter
  pause_start .. finale : Musik bricht weg, Trommelwirbel steigert sich
  finale .. dauer       : Einschlag + Dur-Akkord (Auflösung), Ausblenden"""
# --- Fester Hintergrund-Sound (Entscheidung des Nutzers): liegt assets/bgm.mp3 vor, wird NUR dieser benutzt ---
import os as _os, sys as _sys, subprocess as _sp
if _os.path.exists("assets/bgm.mp3"):
    _D = float(_sys.argv[1])
    _sp.run(["ffmpeg", "-y", "-v", "error", "-stream_loop", "-1", "-i", "assets/bgm.mp3", "-t", f"{_D:.2f}",
             "-af", f"loudnorm=I=-16:TP=-2,afade=t=in:d=0.3,afade=t=out:st={max(0, _D - 1.5):.2f}:d=1.5", "-ac", "1", "-ar", "44100", "assets/musik.wav"], check=True)
    print("Hintergrund-Sound: assets/bgm.mp3 (geloopt)", _D); _sys.exit(0)
# --- sonst: selbst erzeugte Musik ---

import sys, subprocess, numpy as np
from scipy.signal import butter, sosfilt
SR = 44100
D, P, FIN = map(float, sys.argv[1:4]); BPM = float(sys.argv[4]) if len(sys.argv) > 4 else 112
N = int(D * SR); t = np.arange(N) / SR; out = np.zeros(N)
rng = np.random.default_rng(7)
beat = 60 / BPM
lp = lambda x, f: sosfilt(butter(2, f, "low", fs=SR, output="sos"), x)
hp = lambda x, f: sosfilt(butter(2, f, "high", fs=SR, output="sos"), x)
def add(sig, at, g=1.0):
    i = int(at * SR)
    if i >= N: return
    n = min(len(sig), N - i); out[i:i + n] += g * sig[:n]
def env(n, a=0.005, r=0.2):
    e = np.ones(n); na = max(1, int(a * SR)); e[:na] = np.linspace(0, 1, na)
    return e * np.exp(-np.arange(n) / SR / r)
def kick():
    n = int(.35 * SR); tt = np.arange(n) / SR
    f = 50 + 110 * np.exp(-tt * 28); ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-tt * 9)
def hat(o=False):
    n = int((.25 if o else .05) * SR); return hp(rng.standard_normal(n), 7000) * env(n, .001, .09 if o else .015) * .35
def snare(g=1):
    n = int(.18 * SR); tt = np.arange(n) / SR
    return (hp(rng.standard_normal(n), 1500) * .6 + np.sin(2 * np.pi * 190 * tt) * .4) * np.exp(-tt * 22) * g
def saw(f, n): tt = np.arange(n) / SR; return 2 * ((tt * f) % 1) - 1
def note(f, dur, g=1, cut=1800, r=.18):
    n = int(dur * SR); return lp(saw(f, n) + .5 * saw(f * 1.005, n), cut) * env(n, .004, r) * g
hz = lambda m: 440 * 2 ** ((m - 69) / 12)

# --- 1) Spannungs-Loop ---
prog = [45, 45, 41, 43]          # A A F G (Bass, MIDI)
arp = [69, 72, 76, 72, 69, 72, 77, 72]
nb = int(P / beat)
for b in range(nb):
    at = b * beat; k = at / max(P, 1e-6)   # 0..1 Fortschritt
    bar = (b // 4) % 4; root = prog[bar]
    add(kick(), at, .9)
    for e in range(2):                      # Bass in Achteln
        add(note(hz(root - 12), beat / 2, .55, 300 + 500 * k, .12), at + e * beat / 2)
    if k > .25:
        for s in range(4): add(hat(), at + s * beat / 4, .5 + .5 * k)
    if b % 2 == 1 and k > .45: add(snare(.5), at)
    for s in range(2):                      # Arpeggio wird heller und lauter
        m = arp[(b * 2 + s) % 8] + (root - 45)
        add(note(hz(m), beat / 2, .12 + .2 * k, 900 + 3500 * k, .15), at + s * beat / 2)
# Riser vor der Pause
rn = int(min(4, P) * SR); rt = np.arange(rn) / rn
riser = hp(rng.standard_normal(rn), 800) * rt ** 2 * .35 + np.sin(2 * np.pi * np.cumsum(200 + 900 * rt ** 2) / SR) * rt ** 2 * .15
add(riser, P - rn / SR)
# --- 2) Trommelwirbel in der Pause ---
L = FIN - P
if L > 0.2:
    drone = lp(saw(hz(33), int(L * SR)), 160) * np.linspace(.15, .4, int(L * SR))
    add(drone, P)
    tt, i = 0.0, 0
    while tt < L - .05:
        q = tt / L; add(snare(.25 + .75 * q ** 1.5), P + tt)
        tt += .11 - .075 * q; i += 1
# --- 3) Auflösung ---
n = int(2.5 * SR); tt = np.arange(n) / SR
boom = np.sin(2 * np.pi * np.cumsum(40 + 80 * np.exp(-tt * 6)) / SR) * np.exp(-tt * 2.2) * 1.3
crash = hp(rng.standard_normal(n), 3000) * np.exp(-tt * 1.6) * .45
add(boom + crash, FIN)
chord = [57, 61, 64, 69, 73]     # A-Dur
R = D - FIN
if R > 0:
    for m in chord: add(note(hz(m), R, .16, 2600, R * .8), FIN)
    add(note(hz(33), R, .5, 220, R * .7), FIN)
    b = 0
    while FIN + b * beat < D - .3:
        at = FIN + b * beat; add(kick(), at, .8); add(hat(True), at + beat / 2, .5)
        if b % 2: add(snare(.6), at)
        b += 1
# Ausblenden + Normalisieren
fo = int(1.2 * SR); out[-fo:] *= np.linspace(1, 0, fo)
out /= np.max(np.abs(out)) + 1e-9; out *= .7
pcm = (np.clip(out, -1, 1) * 32767).astype(np.int16).tobytes()
subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "s16le", "-ar", str(SR), "-ac", "1", "-i", "-", "assets/musik.wav"], input=pcm, check=True)
print("Musik", D, "s, Pause", P, "Finale", FIN)
