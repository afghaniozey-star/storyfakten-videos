"""OmniVoice-Synthese (kostenlos, lokal) für piper_flow.py.
Aufruf: /opt/omni/venv/bin/python omni_synth.py <projektordner>
Schreibt assets/vo/pf/<sid>-<hash>.wav, danach normal: python3 tools/piper_flow.py <projektordner>
voice.json braucht: "model": "omni-frau" """
import json, os, sys, hashlib, torch, soundfile as sf
from omnivoice import OmniVoice
root = sys.argv[1]; cfg = json.load(open(f"{root}/voice.json", encoding="utf-8"))
HERE = "/home/user/pl/pipeline/stimme-omni"
VOICES = {"omni-frau": ("frau-referenz.wav", "Dein Führerschein kostet im Schnitt dreitausendvierhundert Euro. Ab zweitausendsiebenundzwanzig soll sich das ändern. Das sind die krassesten Änderungen."),
          "omni-mann": ("mann-referenz.wav", "Hey, wusstest du das? Dieser Fußballer verdient in einer Minute mehr als du in einem ganzen Monat. Und das ist noch nicht mal das Krasseste.")}
REF, REF_TXT = VOICES[cfg["model"]]; REF = os.path.join(HERE, REF)
torch.set_num_threads(2)
os.makedirs(f"{root}/assets/vo/pf", exist_ok=True)
todo = []
for sc in cfg["scenes"]:
    text = " ".join(g[1] for g in sc["groups"])
    hk = hashlib.sha1(json.dumps([text, cfg["model"], cfg.get("length_scale"), cfg.get("sentence_silence")]).encode()).hexdigest()[:12]
    cp = f"{root}/assets/vo/pf/{sc['id']}-{hk}.wav"
    if not os.path.exists(cp): todo.append((sc["id"], text, cp))
if not todo: print("alles im Cache"); sys.exit()
m = OmniVoice.from_pretrained("k2-fsa/OmniVoice", device_map="cpu", dtype=torch.float32)
prompt = m.create_voice_clone_prompt(ref_audio=REF, ref_text=REF_TXT)
for sid, text, cp in todo:
    a = m.generate(text=text, voice_clone_prompt=prompt, language="de", speed=cfg.get("speed"))
    sf.write(cp, a[0], 24000); print(sid, round(len(a[0]) / 24000, 1), "s", flush=True)
