"""Selbst erzeugte, lizenzfreie Story-Musik: ruhige Moll-Flächen + Spieluhr, ab "Zahl 1" Herzschlag,
Mitternachts-Glocke, Schock-Einschlag beim Spiegel. Aufruf: python3 tools/story_musik.py <dauer> <t_eins> <t_mitternacht> <t_spiegel>"""
import sys, subprocess, numpy as np
from scipy.signal import butter, sosfilt
SR = 44100
D, T1, TM, TS = map(float, sys.argv[1:5])
N = int(D * SR); out = np.zeros(N); rng = np.random.default_rng(3)
lp = lambda x, f: sosfilt(butter(2, f, "low", fs=SR, output="sos"), x)
hz = lambda m: 440 * 2 ** ((m - 69) / 12)
def add(sig, at, g=1.0):
    i = int(at * SR)
    if i >= N or i < 0: return
    n = min(len(sig), N - i); out[i:i + n] += g * sig[:n]
def pad(freqs, dur):
    n = int(dur * SR); t = np.arange(n) / SR
    s = sum(np.sin(2 * np.pi * f * t) + .3 * np.sin(2 * np.pi * 2.003 * f * t) for f in freqs)
    env = np.minimum(1, t / 1.2) * np.minimum(1, (dur - t) / 1.2)
    return lp(s, 1400) * env
def pluck(f, dur=1.2):
    n = int(dur * SR); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * f * t) + .4 * np.sin(2 * np.pi * 3 * f * t)) * np.exp(-t * 4)
def heart():
    n = int(.5 * SR); t = np.arange(n) / SR
    b = lambda d: np.sin(2 * np.pi * (45 + 40 * np.exp(-(t - d) * 30)) * (t - d)) * np.exp(-np.maximum(0, t - d) * 18) * (t >= d)
    return b(0) + .7 * b(.18)
chords = [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]]   # Am F C G
bar = 3.2
# 1) Flächen bis Mitternacht (nach "Eins" dunkler/leiser)
t = 0.0; k = 0
while t < TM - .2:
    d = min(bar, TM - t)
    add(pad([hz(m - 12) for m in chords[k % 4]], d + .8), t, .10 if t < T1 else .07)
    t += bar; k += 1
# Spieluhr nur im fröhlichen Anfang
arp = [69, 72, 76, 72, 74, 72, 69, 67]
t = 0.2; i = 0
while t < T1 - .3:
    add(pluck(hz(arp[i % 8] + 12)), t, .06); t += .4; i += 1
# 2) Herzschlag ab der "Eins", wird schneller bis Mitternacht
t = T1; per = 1.0
while t < TM - .4:
    add(heart(), t, .5); t += per; per = max(.55, per * .97)
# 3) Mitternachts-Glocke (3 Schläge) + kurze Erleichterung (Dur)
for j in range(3):
    n = int(2.5 * SR); tt = np.arange(n) / SR
    bell = sum(np.sin(2 * np.pi * f * tt) * np.exp(-tt * a) for f, a in [(330, 1.2), (660, 2), (990, 3), (1320, 4)])
    add(bell, TM + j * .9, .12)
add(pad([hz(60), hz(64), hz(67)], max(.5, TS - TM - 2.5)), TM + 2.4, .09)
# 4) Spiegel-Schock: tiefer Einschlag + dunkle Fläche + Herzschlag langsam
n = int(3 * SR); tt = np.arange(n) / SR
boom = np.sin(2 * np.pi * np.cumsum(35 + 60 * np.exp(-tt * 5)) / SR) * np.exp(-tt * 1.5)
add(boom, TS, 1.0); add(lp(rng.standard_normal(n), 900) * np.exp(-tt * 1.2) * .3, TS)
add(pad([hz(45), hz(48), hz(51)], D - TS), TS + .3, .12)
t = TS + 1.2
while t < D - .6:
    add(heart(), t, .45); t += 1.1
fo = int(1.0 * SR); out[-fo:] *= np.linspace(1, 0, fo)
out /= np.max(np.abs(out)) + 1e-9; out *= .7
subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "s16le", "-ar", str(SR), "-ac", "1", "-i", "-", "assets/musik.wav"],
               input=(np.clip(out, -1, 1) * 32767).astype(np.int16).tobytes(), check=True)
print("Story-Musik", D)
