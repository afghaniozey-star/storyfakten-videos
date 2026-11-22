"""ABO-WELT (YouTube): „Jeder Abonnent bekommt ein Land“ – Weltkarte, Kamera fliegt zu jedem neuen Land,
Land färbt sich, Namens-Fahne poppt auf, Zähler „X / 195 Länder vergeben“, Ende mit Abo-Aufruf.
Aufruf: python3 tools/abowelt.py   – liest welt.json, voice.json, assets/vo/timing.json, weltkarte.json
Weltkarte: @svg-maps/world (CC BY 4.0) → in der Beschreibung „Karte: svg-maps (CC BY 4.0)“ nennen."""
import json, re, subprocess, sys, random
T = json.load(open("assets/vo/timing.json")); V = json.load(open("voice.json"))
W = json.load(open("welt.json")); K = json.load(open("weltkarte.json"))["laender"]
F = lambda v: f"{v:.2f}".rstrip('0').rstrip('.')
norm = lambda s: re.sub(r"[^a-zäöüßå0-9]", "", s.lower())
def w(s, word, n=1):
    c = 0
    for x in T[s]["words"]:
        if norm(x["w"]) == norm(word):
            c += 1
            if c == n: return round(T[s]["start"] + x["s"], 2)
    raise KeyError((s, word, [x["w"] for x in T[s]["words"]]))
st = lambda k: T[k]["start"]
en = lambda k: round(T[k]["start"] + T[k]["slot"], 2)
END = round(max(en(k) for k in T), 2)
TAG = W["tag"]; OWN = W["besitzer"]; NEW = [o for o in OWN if o["tag"] == TAG]; OLD = [o for o in OWN if o["tag"] < TAG]
S0, MY = 1080 / 1010, 560          # Kartenmaßstab, Karten-Oberkante
FX, FY = 540, 860                   # Bildpunkt, auf den die Kamera zentriert
J = []
def wc(mx, my): return mx * S0, MY + my * S0
def cam(t, box, d=1.0, ease="power2.inOut", zmax=7.0):
    x0, y0, x1, y1 = box
    cx, cy = wc((x0 + x1) / 2, (y0 + y1) / 2)
    bw, bh = (x1 - x0) * S0, (y1 - y0) * S0
    z = max(1.0, min(zmax, 760 / max(bw, 1), 820 / max(bh, 1)))
    J.append(f'tl.to("#cam", {{ x: {FX - z * cx:.1f}, y: {FY - z * cy:.1f}, scale: {z:.3f}, duration: {d}, ease: "{ease}" }}, {F(t)});')
    return z
FULL = [0, 0, 1010, 666]

# ---------- Karte ----------
owned = {o["land"]: o for o in OWN}
paths = []
for cid, c in K.items():
    col = owned[cid]["farbe"] if cid in owned and owned[cid]["tag"] < TAG else "#3a4a70"
    paths.append(f'<path id="c-{cid}" d="{c["path"]}" fill="{col}" stroke="#141c33" stroke-width="0.6" vector-effect="non-scaling-stroke"/>')
def pin(o, z):
    c = K[o["land"]]; x0, y0, x1, y1 = o.get("fokus") or c["bbox"]
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    s = 1 / z / S0   # Größe so, dass die Fahne beim Heranzoomen ~gleich groß wirkt
    nm = o["name"]; wd = 46 + 30 * len(nm)
    return (f'<g id="p-{o["land"]}" opacity="0" transform="translate({mx:.2f} {my:.2f}) scale({s:.4f})"><g id="p-{o["land"]}-in">'
            f'<path d="M0 0 V-150" stroke="#111" stroke-width="8"/><rect x="0" y="-150" width="{wd}" height="70" rx="12" fill="{o["farbe"]}" stroke="#111" stroke-width="6"/>'
            f'<text x="{wd/2:.0f}" y="-101" text-anchor="middle" style="font:900 46px Inter,sans-serif;fill:#111">{nm}</text>'
            f'<circle r="14" fill="#fff" stroke="#111" stroke-width="6"/></g></g>')
pins = ""; zooms = {}
for o in NEW:
    box = o.get("fokus") or K[o["land"]]["bbox"]
    zooms[o["land"]] = max(1.0, min(7.0, 760 / max((box[2] - box[0]) * S0, 1), 820 / max((box[3] - box[1]) * S0, 1)))
for o in OLD: pins += pin(o, 2.2).replace('opacity="0"', 'opacity="1"', 1)
for o in NEW: pins += pin(o, zooms[o["land"]])
MAP = (f'<g id="cam"><rect x="-6000" y="-6000" width="14000" height="14000" fill="#0e3a66"/>'
       f'<g transform="translate(0 {MY}) scale({S0:.5f})">{"".join(paths)}{pins}</g></g>')

# ---------- Zeitplan ----------
J.append('tl.set("#cam", { x: 0, y: 0, scale: 1, svgOrigin: "0 0" }, 0);')
# Hook: zufällige Länder blinken (Glücksrad-Effekt)
random.seed(TAG)
free = [c for c in K if c not in owned and K[c]["bbox"][2] - K[c]["bbox"][0] > 12]
used = set()
cols = ["#ef476f", "#ffd166", "#06d6a0", "#118ab2", "#f78c6b", "#c77dff"]
t = 0.15
while t < st("s2") - .3:
    cid = random.choice(free)
    J.append(f'tl.fromTo("#c-{cid}", {{ fill: "#3a4a70" }}, {{ fill: "{random.choice(cols)}", duration: .08, yoyo: true, repeat: 1, immediateRender: false }}, {F(t)});')
    used.add(cid)
    t += .12
for cid in used: J.append(f'tl.set("#c-{cid}", {{ fill: "#3a4a70" }}, {F(st("s2"))});')
cnt = len(OLD)
for o in NEW:
    s = o["szene"]; t0 = st(s)
    cam(t0 - .1, o.get("fokus") or K[o["land"]]["bbox"], 1.0)
    tn = t0 + .45   # Zeitpunkt, an dem der Name fällt (gesprochenes Wort, sonst kurz nach Szenenstart)
    try: tn = w(s, o.get("sprechname", o["name"].capitalize()))
    except KeyError: pass
    J.append(f'tl.to("#c-{o["land"]}", {{ fill: "{o["farbe"]}", duration: .35 }}, {F(tn + .1)});')
    J.append(f'tl.fromTo("#p-{o["land"]}", {{ opacity: 0 }}, {{ opacity: 1, duration: .05 }}, {F(tn + .15)});')
    J.append(f'tl.fromTo("#p-{o["land"]}-in", {{ scale: 0, transformOrigin: "0px 0px" }}, {{ scale: 1, duration: .4, ease: "back.out(2.5)" }}, {F(tn + .15)});')
    cnt += 1
    J.append(f'tl.call(() => {{ document.getElementById("cnt").textContent = "{cnt}"; }}, null, {F(tn + .15)}); tl.call(() => {{ document.getElementById("cnt").textContent = "{cnt - 1}"; }}, null, {F(tn + .1)});')
    J.append(f'tl.fromTo("#cntbox", {{ scale: 1.25 }}, {{ scale: 1, duration: .3, ease: "back.out(3)" }}, {F(tn + .15)});')
# Zoom raus + „frei“
tz = st("s8")
cam(tz - .1, FULL, 1.2, zmax=1)
for word, cid in (("Japan?", "jp"), ("Frankreich?", "fr")):
    try:
        tw = w("s8", word)
        J.append(f'tl.to("#c-{cid}", {{ fill: "#ffffff", duration: .15, yoyo: true, repeat: 3 }}, {F(tw)});')
    except KeyError: pass

# ---------- HTML-Ebenen ----------
def ui(id_, t0, t1, inner, style): return f'<div id="{id_}" class="ui clip" data-start="{F(t0)}" data-duration="{F(max(.05, t1 - t0))}" style="{style}">{inner}</div>\n'
def chip(id_, txt, bg="#fff", fg="#111", size=44):
    return f'<div id="{id_}" style="display:inline-block;max-width:980px;background:{bg};color:{fg};font:900 {size}px/1.15 Inter,sans-serif;padding:12px 26px;border-radius:18px;border:5px solid #111;box-shadow:0 8px 0 #111">{txt}</div>'
html = ui("ttl", 0, END, '<div style="font:900 40px Inter,sans-serif;color:#ffd166;letter-spacing:.04em">JEDER ABONNENT BEKOMMT</div><div style="font:900 78px/1 Inter,sans-serif;color:#fff;-webkit-text-stroke:9px #111;paint-order:stroke fill">EIN LAND 🌍</div>', "left:0;right:0;top:90px;text-align:center")
html += ui("cntw", 0, END, f'<div id="cntbox" style="display:inline-block;background:rgba(0,0,0,.6);border-radius:16px;padding:8px 22px;font:900 40px Inter,sans-serif;color:#fff"><span id="cnt" style="color:#06d6a0">{len(OLD)}</span> / {W["laender_gesamt"]} LÄNDER VERGEBEN</div>', "left:0;right:0;top:260px;text-align:center")
J.append(f'tl.fromTo("#ttl", {{ scale: 1.4, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: .25, ease: "back.out(2)" }}, 0);')
html += ui("hk", .2, st("s3") - .1, chip("hk-in", "🔔 NUR FÜR ABONNENTEN!", "#e63946", "#fff", 50), "left:0;right:0;top:360px;text-align:center")
J.append(f'tl.fromTo("#hk-in", {{ scale: 0, rotation: -8 }}, {{ scale: 1, rotation: -2, duration: .3, ease: "back.out(2.5)" }}, {F(st("s2"))});')
for o in NEW:
    s = o["szene"]; t0 = st(s); t1 = en(s) - .05
    html += ui(f"fk{o['land']}", t0 + .7, t1, chip(f"fk{o['land']}-in", f'{o["land_de"]} → {o["name"]}<br><span style="font-size:.75em;font-weight:800">{o["fakt"]}</span>', o["farbe"], "#111", 48), "left:0;right:0;top:1380px;text-align:center")
    J.append(f'tl.fromTo("#fk{o["land"]}-in", {{ y: 80, opacity: 0 }}, {{ y: 0, opacity: 1, duration: .3, ease: "back.out(2)" }}, {F(t0 + .7)});')
frei = W["laender_gesamt"] - len(OWN)
html += ui("fr", st("s8"), en("s8"), chip("fr-in", f"🟦 NOCH {frei} LÄNDER FREI!", "#ffd166", "#111", 56), "left:0;right:0;top:1380px;text-align:center")
J.append(f'tl.fromTo("#fr-in", {{ scale: 2, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: .3, ease: "back.out(2)" }}, {F(st("s8"))}); tl.to("#fr-in", {{ scale: 1.06, duration: .3, yoyo: true, repeat: 5 }}, {F(st("s8") + .4)});')
cs = st("s9")
html += ui("cta", cs, END, chip("cta-a", "🔔 ABONNIEREN", "#e63946", "#fff", 64) + '<div style="height:20px"></div>' + chip("cta-b", "💬 + DEIN WUNSCHLAND KOMMENTIEREN", "#fff", "#111", 42) + '<div style="height:14px"></div><div style="font:800 34px Inter,sans-serif;color:#fff;-webkit-text-stroke:6px #111;paint-order:stroke fill">Nur Abonnenten bekommen ein Land!</div>', "left:0;right:0;top:1300px;text-align:center")
J += [f'tl.fromTo("#cta-a", {{ scale: 0 }}, {{ scale: 1, duration: .35, ease: "back.out(2.5)" }}, {F(cs)});',
      f'tl.fromTo("#cta-b", {{ y: 60, opacity: 0 }}, {{ y: 0, opacity: 1, duration: .3 }}, {F(cs + .4)});',
      f'tl.to("#cta-a", {{ scale: 1.08, duration: .35, yoyo: true, repeat: 7, ease: "sine.inOut" }}, {F(cs + .8)});']

open("compositions/welt.html", "w", encoding="utf-8").write(f'''<template>
  <style>#root {{ position: absolute; inset: 0; overflow: hidden; background: #0b1a33; }} .ui {{ position: absolute; font-family: Inter, sans-serif; }}</style>
  <div id="root" data-composition-id="welt" data-width="1080" data-height="1920">
    <svg class="clip" data-start="0" data-duration="{F(END)}" viewBox="0 0 1080 1920" style="position:absolute;left:0;top:0;width:1080px;height:1920px" data-layout-ignore>{MAP}</svg>
    {html}
  </div>
  <script>(function () {{ const tl = gsap.timeline({{ paused: true }});
{chr(10).join("    " + j for j in J)}
    window.__timelines["welt"] = tl; }})();</script>
</template>
''')

# ---------- Untertitel ----------
HOT = {o["name"] for o in OWN} | {o["land_de"] for o in OWN} | {"ABONNENT", "LAND!", "ABONNIER", "WELT."}
caps = []
for sc in V["scenes"]:
    sid = sc["id"]; words = T[sid]["words"]; k = 0
    for disp, sp in sc["groups"]:
        dw, swn = disp.split(), sp.split()
        for j, d in enumerate(dw):
            if not any(ch.isalnum() for ch in d): continue
            caps.append((round(T[sid]["start"] + words[min(len(words) - 1, k + int(j * len(swn) / len(dw)))]["s"], 2), d))
        k += len(swn)
items, cj = [], []
for j, (t0, d) in enumerate(caps):
    te = min(caps[j + 1][0] if j + 1 < len(caps) else END, t0 + 1.3)
    up = d.upper()
    col = "#ffd166" if up.rstrip("!?.,:–") in {x.rstrip("!?.,:") for x in HOT} else "#fff"
    fs = min(96, int(1500 / max(1, len(up))))
    items.append(f'<div id="w{j}" class="wd clip" data-start="{F(t0)}" data-duration="{F(max(.15, te - t0 - .02))}"><span id="w{j}-in" style="color:{col};font-size:{fs}px">{up}</span></div>')
    cj.append(f'tl.fromTo("#w{j}-in", {{ scale: 1.2, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: .08 }}, {F(t0)});')
open("compositions/caps.html", "w", encoding="utf-8").write(f'''<template>
  <style>#root {{ position: absolute; inset: 0; }} .wd {{ position: absolute; left: 0; right: 0; top: 1660px; text-align: center; }}
    .wd span {{ display: inline-block; font: 900 96px/1 Inter, sans-serif; white-space: nowrap; -webkit-text-stroke: 14px #000; paint-order: stroke fill; }}</style>
  <div id="root" data-composition-id="caps" data-width="1080" data-height="1920">{"".join(items)}</div>
  <script>(function () {{ const tl = gsap.timeline({{ paused: true }}); {" ".join(cj)} window.__timelines["caps"] = tl; }})();</script>
</template>
''')

# ---------- Ton (fester Hintergrund-Sound über story_musik.py → assets/bgm.mp3) ----------
subprocess.run([sys.executable, "tools/story_musik.py", F(END), "1", "2", "3"], check=True)
FXL = [("whoosh", .05, .4, .8)]
for o in NEW:
    s = o["szene"]; FXL += [("whoosh", st(s) - .1, .35, .8), ("pop", st(s) + .55, .6, .15), ("chime", st(s) + .6, .35, 1.0)]
FXL += [("whoosh", st("s8") - .1, .4, .8), ("pop", st("s9"), .5, .15)]
Hh = lambda id_, ti: f'      <div id="{id_}" data-composition-id="{id_}" data-composition-src="compositions/{id_}.html" data-start="0" data-duration="{F(END)}" data-track-index="{ti}" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index:{ti}"></div>'
lines = [Hh("welt", 2), Hh("caps", 3), f'      <audio id="musik" class="clip" data-start="0" data-duration="{F(END)}" data-track-index="5" data-volume="0.22" src="assets/musik.wav"></audio>']
for k in T:
    d = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"assets/vo/{k}.mp3"]))
    lines.append(f'      <audio id="vo-{k}" class="clip" data-start="{T[k]["start"] + T[k]["lead"]:.2f}" data-duration="{d:.2f}" data-track-index="4" data-volume="1" src="assets/vo/{k}.mp3"></audio>')
for j, (n, at, vol, dur) in enumerate(FXL):
    lines.append(f'      <audio id="fx-{j}" class="clip" data-start="{F(max(0, at))}" data-duration="{F(min(dur, END - max(0, at)))}" data-volume="{vol}" data-track-index="{20 + j}" src="assets/sfx2/{n}.mp3"></audio>')
open("index.html", "w", encoding="utf-8").write(f'''<!doctype html>
<html lang="de" data-resolution="portrait"><head><meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" /><script src="assets/gsap.min.js"></script>
<style>* {{ margin: 0; padding: 0; box-sizing: border-box; }} html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #0b1a33; }} #root {{ width: 100%; height: 100%; }}</style></head>
<body><div id="root" data-composition-id="main" data-start="0" data-duration="{F(END)}" data-width="1080" data-height="1920">
{chr(10).join(lines)}
</div><script>window.__timelines = window.__timelines || {{}}; window.__timelines["main"] = gsap.timeline({{ paused: true }});</script></body></html>
''')
print("Ende", END, "neue Länder", [o["land"] for o in NEW])
