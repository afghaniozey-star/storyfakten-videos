"""Wie fix_timing.py, aber mit Whisper "medium" und ffmpeg-Dekodierung (PyAV-Fehler umgangen). Aufruf: /usr/bin/python3 tools/fix_timing_medium.py s10 s14"""
import json, subprocess, sys, numpy as np
from faster_whisper import WhisperModel
m = WhisperModel("medium", compute_type="int8")
T = json.load(open("assets/vo/timing.json"))
for sid in sys.argv[1:]:
    a = np.frombuffer(subprocess.check_output(["ffmpeg", "-v", "quiet", "-i", f"tmpwav/{sid}.wav", "-f", "f32le", "-ac", "1", "-ar", "16000", "-"]), np.float32)
    segs, _ = m.transcribe(a, language="de", word_timestamps=True)
    ww = [x for s in segs for x in s.words]; W = T[sid]["words"]; L = T[sid]["lead"]
    if len(ww) != len(W): print(sid, "Wortzahl passt nicht", len(ww), len(W)); continue
    for i, x in enumerate(ww):
        W[i]["s"] = round(float(x.start) + L, 2); W[i]["e"] = round(float(ww[i + 1].start if i + 1 < len(ww) else x.end) + L, 2)
    print(sid, "repariert")
json.dump(T, open("assets/vo/timing.json", "w"), ensure_ascii=False, indent=1)
