"""Piper flüssig: jede Szene in EINEM Stück, Wortzeiten per faster-whisper ausgerichtet."""
import json, os, subprocess, sys, re, difflib, numpy as np
root = sys.argv[1]; cfg = json.load(open(f"{root}/voice.json", encoding="utf-8"))
from faster_whisper import WhisperModel
wm = WhisperModel("small", compute_type="int8")
os.makedirs(f"{root}/assets/vo", exist_ok=True)
norm = lambda s: re.sub(r"[^a-zäöüß0-9]", "", s.lower())
t, caps, timing = 0.0, [], {}
for sc in cfg["scenes"]:
    sid = sc["id"]; LEAD = sc.get("lead", cfg.get("lead", 0.1))
    text = " ".join(g[1] for g in sc["groups"])
    os.makedirs(f"{root}/tmpwav", exist_ok=True); raw = f"{root}/tmpwav/{sid}-raw.wav"; wav = f"{root}/tmpwav/{sid}.wav"
    import hashlib, shutil
    hk = hashlib.sha1(json.dumps([text, cfg["model"], cfg.get("length_scale"), cfg.get("sentence_silence")]).encode()).hexdigest()[:12]
    cp = f"{root}/assets/vo/pf/{sid}-{hk}.wav"; os.makedirs(f"{root}/assets/vo/pf", exist_ok=True)
    if os.path.exists(cp): shutil.copy(cp, raw)
    else:
      subprocess.run([sys.executable, "-m", "piper", "-m", cfg["model"], "-f", raw, "--length-scale", str(cfg.get("length_scale", 0.9)), "--sentence-silence", str(cfg.get("sentence_silence", 0.12))], input=text.encode(), check=True, capture_output=True)
      shutil.copy(raw, cp)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", raw, "-af", "silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse", wav], check=True)
    a = np.frombuffer(subprocess.check_output(["ffmpeg", "-v", "quiet", "-i", wav, "-f", "f32le", "-ac", "1", "-ar", "16000", "-"]), np.float32)
    talk = len(a) / 16000
    segs, _ = wm.transcribe(a, language="de", word_timestamps=True, initial_prompt=text)
    ww = [x for s in segs for x in s.words]
    if len(ww) < 0.6 * len(text.split()):
        segs, _ = wm.transcribe(a, language="de", word_timestamps=True)
        ww = [x for s in segs for x in s.words]
    mine = text.split()
    A = [norm(x) for x in mine]; B = [norm(x.word) for x in ww]
    st = [None] * len(mine)
    for blk in difflib.SequenceMatcher(None, A, B, autojunk=False).get_matching_blocks():
        for k in range(blk.size): st[blk.a + k] = ww[blk.b + k].start
    if st[0] is None: st[0] = 0.0
    i = 0
    while i < len(mine):
        if st[i] is None:
            j = i
            while j < len(mine) and st[j] is None: j += 1
            t0 = st[i - 1]; t1 = st[j] if j < len(mine) else talk
            L = [len(x) + 1 for x in mine[i - 1:j]]; tot = sum(L); acc = 0
            for k in range(i, j): acc += L[k - i]; st[k] = t0 + (t1 - t0) * acc / tot
            i = j
        else: i += 1
    for k in range(1, len(st)): st[k] = max(st[k], st[k - 1] + 0.05)
    words = [{"w": x, "s": round(st[k] + LEAD, 2), "e": round((st[k + 1] if k + 1 < len(st) else talk) + LEAD, 2)} for k, x in enumerate(mine)]
    slot = round(LEAD + talk + sc.get("tail", cfg.get("tail", 0.4)), 2)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", wav, "-ar", "44100", "-b:a", "160k", f"{root}/assets/vo/{sid}.mp3"], check=True)
    idx = 0; gst = []
    for disp, sp in sc["groups"]: gst.append(st[idx]); idx += len(sp.split())
    for gi, (disp, sp) in enumerate(sc["groups"]):
        a0 = t + LEAD + gst[gi] - 0.05
        b0 = t + LEAD + gst[gi + 1] - 0.08 if gi + 1 < len(gst) else t + slot - 0.08
        caps.append([round(max(a0, t + 0.1), 2), round(b0, 2), disp])
    timing[sid] = {"start": round(t, 2), "slot": slot, "lead": LEAD, "words": words}
    print(f"{sid}: Länge {slot:.2f}s (gesprochen {talk:.2f}s), Treffer {sum(1 for b in difflib.SequenceMatcher(None, A, B, autojunk=False).get_matching_blocks() for _ in range(b.size))}/{len(mine)}")
    t = round(t + slot, 2)
json.dump(timing, open(f"{root}/assets/vo/timing.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
sj = json.load(open(f"{root}/script.json", encoding="utf-8")); sj["captions"] = caps
json.dump(sj, open(f"{root}/script.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"fertig: Gesamtlänge {t:.2f}s")
