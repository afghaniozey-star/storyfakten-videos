"""Erkennungsmelodie der Serie „In dieser Welt …“ (selbst erzeugt, lizenzfrei): hüpfendes Dur-Thema
(C–G–Am–F, 120 BPM, Zupf-Melodie, springender Bass, Offbeat-Akkorde, Klatschen). Danach optional Spannung
(Ticken + Trommelwirbel) und Mitternachts-Glocken + Mystery-Fläche, am Ende kehrt das Thema leise zurück.
Aufruf: python3 tools/welt_melodie.py <dauer> <t_spannung> <t_mitternacht> <t_thema_zurueck>  -> assets/musik.wav
Zusätzlich erzeugt: assets/sfx2/klong.mp3, splat.mp3, wirbel.mp3, glitch.mp3, boing.mp3"""
import sys, subprocess, numpy as np
from scipy.signal import butter, sosfilt
SR = 44100
D, TS, TM, TR = map(float, sys.argv[1:5])
N = int(D * SR); out = np.zeros(N); rng = np.random.default_rng(7)
lp = lambda x, f: sosfilt(butter(2, f, "low", fs=SR, output="sos"), x)
hp = lambda x, f: sosfilt(butter(2, f, "high", fs=SR, output="sos"), x)
hz = lambda m: 440 * 2 ** ((m - 69) / 12)
def add(buf, sig, at, g=1.0):
    i = int(at * SR)
    if i >= len(buf) or i < 0: return
    n = min(len(sig), len(buf) - i); buf[i:i + n] += g * sig[:n]
def pluck(f, dur=.35, bright=3):
    n = int(dur * SR); t = np.arange(n) / SR
    return (np.sin(2*np.pi*f*t) + .5*np.sin(2*np.pi*2*f*t) + .25*np.sin(2*np.pi*bright*f*t)) * np.exp(-t*9) * np.minimum(1, t/.004)
def bass(f, dur=.22):
    n = int(dur * SR); t = np.arange(n) / SR
    return np.tanh(2*np.sin(2*np.pi*f*t)) * np.exp(-t*7) * np.minimum(1, t/.005)
def clap():
    n = int(.15 * SR); t = np.arange(n) / SR
    return hp(rng.standard_normal(n), 1200) * np.exp(-t*30)
def hat():
    n = int(.05 * SR); t = np.arange(n) / SR
    return hp(rng.standard_normal(n), 6000) * np.exp(-t*80)
def kick():
    n = int(.25 * SR); t = np.arange(n) / SR
    return np.sin(2*np.pi*np.cumsum(50 + 90*np.exp(-t*30))/SR) * np.exp(-t*12)
B = .5  # Schlag
CH = [(48, [60, 64, 67]), (43, [59, 62, 67]), (45, [60, 64, 69]), (41, [60, 65, 69])]  # C G Am F
MEL = [  # (Achtel-Position, Note) je 2 Takte = 16 Achtel; Motiv „hüpfend“
 [(0,72),(1,76),(2,79),(4,76),(5,79),(6,81),(7,79)],
 [(0,79),(1,77),(2,76),(3,74),(4,72),(6,74)],
 [(0,72),(1,76),(2,79),(4,81),(5,79),(6,76),(7,72)],
 [(0,74),(2,76),(3,74),(4,72),(6,67)]]
def theme(buf, t0, t1, g=1.0):
    t = t0; bar = 0
    while t < t1 - .05:
        root, tri = CH[bar % 4]
        for b in range(4):
            tb = t + b * B
            if tb >= t1: break
            add(buf, bass(hz(root if b % 2 == 0 else root + 12)), tb, .5 * g)
            add(buf, kick(), tb, .35 * g) if b % 2 == 0 else add(buf, clap(), tb, .22 * g)
            add(buf, hat(), tb + B/2, .12 * g)
            for m in tri: add(buf, pluck(hz(m), .18, 5), tb + B/2, .06 * g)
        for pos, m in MEL[bar % 4]:
            tm = t + pos * B / 2
            if tm < t1: add(buf, pluck(hz(m), .4), tm, .2 * g)
        t += 4 * B; bar += 1
def pad(freqs, dur):
    n = int(dur * SR); t = np.arange(n) / SR
    s = sum(np.sin(2*np.pi*f*t) + .3*np.sin(2*np.pi*2.003*f*t) for f in freqs)
    return lp(s, 1200) * np.minimum(1, t/1.0) * np.minimum(1, (dur - t)/1.0)
def wirbel(dur):
    n = int(dur * SR); t = np.arange(n) / SR
    hits = np.zeros(n)
    for k in np.arange(0, dur, .045): add(hits, lp(rng.standard_normal(int(.04*SR)), 3000) * np.exp(-np.arange(int(.04*SR))/SR*60), k)
    return hits * (.3 + .7 * t / dur)
theme(out, 0, TS)
# Spannung: Ticken + Herz-Bass + Wirbel bis Mitternacht
t = TS
while t < TM - .3:
    n = int(.04*SR); add(out, hp(rng.standard_normal(n), 3000) * np.exp(-np.arange(n)/SR*90), t, .25); t += .5
add(out, pad([hz(45), hz(52), hz(57)], TM - TS + .5), TS, .10)
add(out, wirbel(max(.5, TM - TS - .2)), TS + .1, .16)
# Mitternacht: Glocken + Mystery
for j in range(3):
    n = int(2.5 * SR); tt = np.arange(n) / SR
    add(out, sum(np.sin(2*np.pi*f*tt) * np.exp(-tt*a) for f, a in [(262, 1.2), (524, 2), (786, 3), (1048, 4)]), TM + j * .8, .14)
add(out, pad([hz(46), hz(49), hz(53), hz(56)], TR - TM + 1), TM + .5, .11)
theme(out, TR, D, .6)
fo = int(.8 * SR); out[-fo:] *= np.linspace(1, 0, fo)
out /= np.max(np.abs(out)) + 1e-9; out *= .7
def wr(path, sig):
    sig = sig / (np.max(np.abs(sig)) + 1e-9) * .9
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "s16le", "-ar", str(SR), "-ac", "1", "-i", "-", path], input=(sig * 32767).astype(np.int16).tobytes(), check=True)
wr("assets/musik.wav", out)
# Soundeffekte
t = np.arange(int(1.2*SR)) / SR
wr("assets/sfx2/klong.mp3", sum(np.sin(2*np.pi*f*t) * np.exp(-t*a) for f, a in [(420, 4), (1130, 6), (1870, 9), (2650, 12)]) + .5*np.exp(-t*40)*rng.standard_normal(len(t)))
t = np.arange(int(.5*SR)) / SR
wr("assets/sfx2/splat.mp3", lp(rng.standard_normal(len(t)), 900) * np.exp(-t*9) + .6*np.sin(2*np.pi*(120 - 80*t)*t)*np.exp(-t*12))
wr("assets/sfx2/wirbel.mp3", wirbel(2.0))
t = np.arange(int(.6*SR)) / SR
wr("assets/sfx2/glitch.mp3", np.sign(np.sin(2*np.pi*np.repeat(rng.integers(200, 1500, 30), len(t)//30 + 1)[:len(t)]*t)) * (rng.random(len(t)) > .1) * .6)
t = np.arange(int(.5*SR)) / SR
wr("assets/sfx2/boing.mp3", np.sin(2*np.pi*np.cumsum(220 + 160*np.sin(2*np.pi*9*t)*np.exp(-t*4))/SR) * np.exp(-t*5))
print("Musik", D)
