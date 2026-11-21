"""Whisper-Abschrift einzelner Dateien: python3 tools/abschrift.py a.wav b.mp4 ..."""
import sys, subprocess, numpy as np
from faster_whisper import WhisperModel
m = WhisperModel(sys.argv[1] if sys.argv[1] in ("small", "medium") else "small", compute_type="int8")
for f in sys.argv[1:]:
    if f in ("small", "medium"): continue
    a = np.frombuffer(subprocess.check_output(["ffmpeg", "-v", "quiet", "-i", f, "-f", "f32le", "-ac", "1", "-ar", "16000", "-"]), np.float32)
    segs, _ = m.transcribe(a, language="de")
    print(f, "|", " ".join(x.text.strip() for x in segs), flush=True)
