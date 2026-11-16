"""TÜRME-FORMAT (Standard, vom Nutzer gewünscht – wie das WM-Finale-Video):
Kugeln mit Augen stehen auf Ziegeltürmen, die Türme wachsen gemeinsam, bei jedem "raus!" fliegt eine Kugel
(kleinster Wert zuerst). Am Ende Duell der letzten zwei (Like vs. Kommentar), Pause mit Trommelwirbel,
Verlierer raus, Gewinner-Turm schießt hoch, Krone, Konfetti, Wow-Banner, Frage an die Zuschauer.
Aufruf: python3 tools/tuerme.py   – liest tuerme.json, voice.json, assets/vo/timing.json; ruft tools/musik.py auf."""
import json, re, subprocess, sys
T = json.load(open("assets/vo/timing.json")); V = json.load(open("voice.json")); C = json.load(open("tuerme.json"))
F = lambda v: f"{v:.2f}".rstrip('0').rstrip('.')
norm = lambda s: re.sub(r"[^a-zäöüß0-9]", "", s.lower())
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

IT = C["items"]                       # Reihenfolge = Ausscheiden; vorletztes = Duell-Verlierer, letztes = Sieger
N = len(IT); WIN = IT[-1]; LOS = IT[-2]
VAL = {i["code"]: i["wert"] for i in IT}
MAXV = C.get("skala", {}).get("max") or WIN["wert"] * 1.05
STEP = C.get("skala", {}).get("schritt") or max(1, round(MAXV / 8))
GROUND, R = 1580, 50
UNIT = (GROUND - 700) / MAXV          # Pixel pro Einheit, höchster Turm endet bei ~y=700
M = MAXV * 0.03                       # kleiner Überstand beim Wachsen
order = sorted(IT, key=lambda i: i["wert"])  # Anzeige: links klein -> rechts groß
X = {i["code"]: round(1080 / N * (k + .5)) for k, i in enumerate(order)}

def ball(b, r, uid):
    t, cols = b["typ"], b["farben"]
    if t == "voll": f = f'<rect x="{-r}" y="{-r}" width="{2*r}" height="{2*r}" fill="{cols[0]}"/>'
    elif t == "mitte": f = f'<rect x="{-r}" y="{-r}" width="{2*r}" height="{2*r}" fill="{cols[0]}"/><rect x="{-r*.34}" y="{-r}" width="{r*.68}" height="{2*r}" fill="{cols[1]}"/>'
    elif t == "band": f = f'<rect x="{-r}" y="{-r}" width="{2*r}" height="{2*r}" fill="{cols[0]}"/><rect x="{-r}" y="{r*.45}" width="{2*r}" height="{r*.28}" fill="{cols[1]}"/>'
    elif t == "quer":   # waagerechte Streifen (Länderflaggen)
        n = len(cols); h = 2 * r / n
        f = "".join(f'<rect x="{-r}" y="{-r + k*h:.1f}" width="{2*r}" height="{h + .6:.1f}" fill="{c}"/>' for k, c in enumerate(cols))
    elif t == "senkrecht":
        n = len(cols); wd = 2 * r / n
        f = "".join(f'<rect x="{-r + k*wd:.1f}" y="{-r}" width="{wd + .6:.1f}" height="{2*r}" fill="{c}"/>' for k, c in enumerate(cols))
    elif t == "streifen":
        n = b.get("n", 6); wd = 2 * r / n
        f = "".join(f'<rect x="{-r + k*wd:.1f}" y="{-r}" width="{wd + .6:.1f}" height="{2*r}" fill="{cols[k % len(cols)]}"/>' for k in range(n))
    else: f = f'<rect x="{-r}" y="{-r}" width="{2*r}" height="{2*r}" fill="{cols[0]}"/><text y="{r*.35}" text-anchor="middle" font-size="{r*1.1}">{b.get("emoji", "")}</text>'
    s = r / 50
    eyes = (f'<g transform="scale({s:.3f})"><ellipse cx="-17" cy="-6" rx="13" ry="15" fill="#fff" stroke="#111" stroke-width="3"/><ellipse cx="17" cy="-6" rx="13" ry="15" fill="#fff" stroke="#111" stroke-width="3"/>'
            f'<circle cx="-14" cy="-4" r="6" fill="#111"/><circle cx="20" cy="-4" r="6" fill="#111"/></g>')
    return f'<clipPath id="cp{uid}"><circle r="{r}"/></clipPath><g clip-path="url(#cp{uid})">{f}</g><circle r="{r}" fill="none" stroke="#111" stroke-width="5"/>{eyes}'

defs = ('<defs><pattern id="brick" width="40" height="24" patternUnits="userSpaceOnUse"><rect width="40" height="24" fill="#c98b5a"/>'
        '<path d="M0 0 H40 M0 12 H40 M20 0 V12 M0 12 V24 M40 12 V24" stroke="#8a5a36" stroke-width="2.5"/></pattern>'
        '<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0d1b3e"/><stop offset=".55" stop-color="#2b4c8c"/><stop offset="1" stop-color="#7fb2e5"/></linearGradient></defs>')
stars = "".join(f'<circle cx="{(k * 137) % 1080}" cy="{(k * 97) % 700 + 20}" r="{1 + k % 3}" fill="#fff" opacity="{.3 + (k % 4) * .15}"/>' for k in range(40))
gl = []
v = STEP
while v <= MAXV:
    y = GROUND - v * UNIT
    gl.append(f'<path d="M0 {y:.0f} H1080" stroke="rgba(255,255,255,.18)" stroke-width="2" stroke-dasharray="10 10"/>'
              f'<text x="12" y="{y - 8:.0f}" style="font:800 24px Inter,sans-serif;fill:rgba(255,255,255,.55)">{v:g}</text>')
    v += STEP
grid = "".join(gl)
TW = min(92, int(1080 / N * .72))
towers = ""
for i in IT:
    c, x = i["code"], X[i["code"]]
    towers += (f'<rect id="t{c}" x="{x - TW/2}" y="{GROUND}" width="{TW}" height="0" fill="url(#brick)" stroke="#5b3a22" stroke-width="3"/>'
               f'<g id="o{c}" opacity="0"><rect x="{x - 46}" y="0" width="92" height="40" rx="8" fill="#e63946" stroke="#fff" stroke-width="3"/>'
               f'<text x="{x}" y="29" text-anchor="middle" style="font:900 26px Inter,sans-serif;fill:#fff">RAUS</text></g>'
               f'<g id="b{c}" transform="translate({x} {GROUND - R})">{ball(i["ball"], R, c)}</g>'
               f'<text x="{x}" y="{GROUND + 44}" text-anchor="middle" style="font:900 {28 if len(i.get("kurz", c)) <= 5 else 22}px Inter,sans-serif;fill:#fff">{i.get("kurz", c)}</text>')
crown = '<g id="crown" opacity="0"><path d="M-44 0 L-44 -40 L-22 -18 L0 -50 L22 -18 L44 -40 L44 0 Z" fill="#ffd60a" stroke="#111" stroke-width="4"/></g>'
SVG = (f'{defs}<rect width="1080" height="1920" fill="url(#sky)"/>{stars}{grid}'
       f'<rect y="{GROUND}" width="1080" height="{1920 - GROUND}" fill="#3a5a2a"/><rect y="{GROUND}" width="1080" height="10" fill="#6fa84a"/>{towers}{crown}')

# ---------- Zeitplan ----------
out = {i["code"]: w(i["raus"]["szene"], i["raus"].get("wort", "raus!"), i["raus"].get("n", 1)) for i in IT[:-1]}
D = C["duell"]; S = C["sieger"]
first = IT[0]["raus"]["szene"]
KEY = [(0, 0), (st(first) - .4, IT[0]["wert"] * .5)]
for i in IT[:-2]:
    c = i["code"]; KEY += [(out[c] - .05, VAL[c] + M), (out[c] + .5, VAL[c] + 1.5 * M)]
lv = LOS["wert"]
KEY += [(st(D["szene"]) + .4, lv - 2 * M), (en(D["szene"]) - .2, lv), (out[LOS["code"]] - .05, lv + M)]
tw0 = w(S["szene"], S["namewort"]); tz = w(S["szene"], S["zahlwort"])
KEY += [(max(tw0, out[LOS["code"]] + .3), lv + 3 * M), (tz + .1, WIN["wert"])]
KEY.sort()
js = f'''const KEY = {json.dumps(KEY)}, VAL = {json.dumps(VAL)}, X = {json.dumps(X)}, OUT = {json.dumps(out)};
const G = {GROUND}, U = {UNIT:.5f}, R = {R}, WIN = {json.dumps(WIN["code"])}, MAXL = {WIN["wert"]};
const lev = (t) => {{ for (let i = 1; i < KEY.length; i++) if (t <= KEY[i][0]) {{ const [a, la] = KEY[i - 1], [b, lb] = KEY[i]; const k = (t - a) / Math.max(1e-6, b - a); const e = k < .5 ? 2 * k * k : 1 - Math.pow(-2 * k + 2, 2) / 2; return la + (lb - la) * e; }} return KEY[KEY.length - 1][1]; }};
const $ = (i) => document.getElementById(i);
const draw = (t) => {{
  const L = lev(t);
  for (const c in VAL) {{
    const h = Math.min(L, VAL[c]) * U, top = G - h;
    $("t" + c).setAttribute("y", top); $("t" + c).setAttribute("height", h);
    const o = OUT[c]; let by = top - R, rot = 0, op = 1;
    if (o !== undefined && t > o) {{ const d = t - o; by = top - R + 900 * d * d + 60 * d; rot = 260 * d; op = Math.max(0, 1 - d * 1.2); }}
    else if (c === WIN && L >= MAXL - 0.001) {{ by = top - R - 10 * Math.abs(Math.sin(t * 6)); }}
    else {{ by = top - R - 4 * Math.abs(Math.sin(t * 5 + X[c])); }}
    $("b" + c).setAttribute("transform", "translate(" + X[c] + " " + by.toFixed(1) + ") rotate(" + rot.toFixed(1) + ")"); $("b" + c).style.opacity = op;
    const oo = $("o" + c); if (o !== undefined && t > o) {{ oo.setAttribute("opacity", 1); oo.setAttribute("transform", "translate(0 " + (top - 46) + ")"); }} else oo.setAttribute("opacity", 0);
  }}
  $("lv").textContent = Math.min(MAXL, Math.floor(L + 0.02)).toLocaleString("de-DE");
  const ger = G - MAXL * U - 2 * R - 14; $("crown").setAttribute("transform", "translate(" + X[WIN] + " " + ger + ")");
}};
const tl = gsap.timeline({{ paused: true }}); const o = {{ t: 0 }};
tl.fromTo(o, {{ t: 0 }}, {{ t: {END}, duration: {END}, ease: "none", onUpdate: () => draw(o.t) }}, 0); draw(0);
'''
def ui(id_, t0, t1, inner, style): return f'    <div id="{id_}" class="ui clip" data-start="{F(t0)}" data-duration="{F(max(.05, t1 - t0))}" style="{style}">{inner}</div>\n'
def banner(id_, txt, bg="#ffd60a", fg="#111", size=44):
    return f'<div id="{id_}" style="display:inline-block;max-width:980px;background:{bg};color:{fg};font:900 {size}px/1.15 Inter,sans-serif;padding:12px 26px;border-radius:18px;border:4px solid #111;box-shadow:0 8px 0 #111">{txt}</div>'
html = ui("ttl", 0, END, f'<div style="font:900 40px Inter,sans-serif;color:#ffd60a;letter-spacing:.04em">{C["titel"][0]}</div><div style="font:900 72px/1 Inter,sans-serif;color:#fff;-webkit-text-stroke:8px #111;paint-order:stroke fill">{C["titel"][1]}</div>', "left:0;right:0;top:100px;text-align:center")
html += ui("cnt", 0, END, f'<div style="display:inline-block;background:rgba(0,0,0,.55);border-radius:14px;padding:6px 20px;font:900 34px Inter,sans-serif;color:#fff">{C["einheit"]}: <span id="lv" style="color:#ffd60a">0</span></div>', "left:0;right:0;top:250px;text-align:center")
J, FX = [], []
# Hook (erste 2 Sekunden)
H = C["hook"]; th = w(H["szene"], H["wort"])
html += ui("hk", .2, st(first) - .2, banner("hk-in", H["banner"], "#e63946", "#fff", 50), "left:0;right:0;top:330px;text-align:center")
J.append(f'tl.fromTo("#hk-in", {{ opacity: 0, scale: 1.8 }}, {{ opacity: 1, scale: 1, duration: .25, ease: "back.out(2)" }}, {F(min(th, 1.2))});')
FX += [("riser", .1, .25, 2.5), ("pop", min(th, 1.2), .5, .12)]
# Fakten-Zettel bei jedem Ausscheiden
for k, i in enumerate(IT[:-1]):
    c = i["code"]; t0 = out[c]
    t1 = out[IT[k + 1]["code"]] - .1 if k + 1 < N - 1 else t0 + 2.2
    if i is LOS: t1 = min(t1, tw0 - .1)
    if i is not LOS and k + 1 == N - 2: t1 = min(t1, st(D["szene"]) - .05)
    if i.get("fakt"):
        html += ui(f"fk{c}", t0 + .15, t1, banner(f"fk{c}-in", "💡 " + i["fakt"], "#fff", "#111", 36), "left:0;right:0;top:340px;text-align:center")
        J.append(f'tl.fromTo("#fk{c}-in", {{ opacity: 0, scale: .4, rotation: -4 }}, {{ opacity: 1, scale: 1, rotation: -2, duration: .25, ease: "back.out(2.5)" }}, {F(t0 + .15)});')
    FX += [("whoosh", t0 - .05, .45, .9), ("hit", t0 + .25, .4, 1.6)]
# Zwischenfragen (optional): {"szene": "e3", "text": "NA, WER FEHLT NOCH? 🤔", "wort": "Na"}
for q in C.get("fragen", []):
    t0 = w(q["szene"], q["wort"]); t1 = en(q["szene"]) - .05
    html += ui("fq" + q["szene"], t0, t1, banner("fq" + q["szene"] + "-in", q["text"], "#e63946", "#fff", 46), "left:0;right:0;top:460px;text-align:center")
    J.append(f'tl.fromTo("#fq{q["szene"]}-in", {{ scale: 2, opacity: 0, rotation: 6 }}, {{ scale: 1, opacity: 1, rotation: -3, duration: .3, ease: "back.out(2.5)" }}, {F(t0)});')
    FX.append(("swoosh", t0, .4, .6))
# Duell
d0, d1 = st(D["szene"]) + .2, out[LOS["code"]] - .1
html += ui("vs", d0, d1, banner("vs-in", D["vs"], "#fff", "#111", 36), "left:0;right:0;top:340px;text-align:center")
html += ui("lk", w(D["szene"], D.get("likewort", "Like")) - .1, d1, '<div style="display:flex;justify-content:center;gap:16px">' + banner("lk-a", D["like"], "#ffd60a", "#111", 38) + banner("lk-b", D["kommentar"], "#fafafa", "#111", 38) + '</div>', "left:0;right:0;top:440px")
J += [f'tl.fromTo("#vs-in", {{ opacity: 0, y: -30 }}, {{ opacity: 1, y: 0, duration: .3 }}, {F(d0)});',
      f'tl.fromTo("#lk-a", {{ opacity: 0, scale: .4 }}, {{ opacity: 1, scale: 1, duration: .25, ease: "back.out(2)" }}, {F(w(D["szene"], D.get("likewort", "Like")) - .1)});',
      f'tl.fromTo("#lk-b", {{ opacity: 0, scale: .4 }}, {{ opacity: 1, scale: 1, duration: .25, ease: "back.out(2)" }}, {F(w(D["szene"], D.get("kommentarwort", "Kommentar")) - .1)});']
FX += [("riser", st(D["szene"]) + .2, .3, 2.5), ("pop", w(D["szene"], D.get("likewort", "Like")) - .1, .5, .12), ("pop", w(D["szene"], D.get("kommentarwort", "Kommentar")) - .1, .5, .12)]
# Sieger: Blitz, Krone, Konfetti, Wow
tw = tz + .3
html += ui("flash", tw - .1, tw + .4, "", "left:0;top:0;width:1080px;height:1920px;background:#fff")
J.append(f'tl.fromTo("#flash", {{ opacity: .9 }}, {{ opacity: 0, duration: .45 }}, {F(tw - .1)});')
html += ui("win", tw, en(S["szene"]), banner("win-in", S["wow"], "#ffd60a", "#111", 40), "left:0;right:0;top:340px;text-align:center")
J += [f'tl.fromTo("#win-in", {{ opacity: 0, scale: 1.6 }}, {{ opacity: 1, scale: 1, duration: .3, ease: "back.out(2)" }}, {F(tw)});',
      f'tl.fromTo("#crown", {{ opacity: 0 }}, {{ opacity: 1, duration: .2 }}, {F(tw)});']
conf = "".join(f'<div class="cf" style="position:absolute;left:{(k * 83) % 1040}px;top:-40px;width:16px;height:26px;border-radius:4px;background:{["#ffd60a", "#dd0000", "#111", "#2cf0a2", "#4cc9f0"][k % 5]}"></div>' for k in range(40))
html += ui("cf", tw, END, conf, "left:0;top:0;width:1080px;height:1920px;pointer-events:none")
J.append(f'gsap.utils.toArray(".cf").forEach((el, k) => tl.fromTo(el, {{ y: 0, rotation: 0 }}, {{ y: 1900 + (k % 7) * 40, rotation: 360 + k * 40, duration: 2.6 + (k % 5) * .3, ease: "none" }}, {F(tw)} + (k % 10) * .06));')
FX += [("hit", tw - .2, .8, 1.6), ("chime", tw, .5, 1.4), ("blips", tw + .3, .35, 1.3)]
# CTA
cs = st(C["cta"]["szene"])
html += ui("cta", cs, END, banner("cta-in", C["cta"]["text"], "#fff", "#111", 36), "left:0;right:0;top:340px;text-align:center")
J += [f'tl.fromTo("#cta-in", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: .3 }}, {F(cs)});',
      f'tl.to("#cta-in", {{ scale: 1.06, duration: .35, yoyo: true, repeat: 5, ease: "sine.inOut" }}, {F(cs + .5)});']
FX.append(("pop", cs, .5, .12))

open("compositions/welt.html", "w", encoding="utf-8").write(f'''<template>
  <style>#root {{ position: absolute; inset: 0; overflow: hidden; }} .ui {{ position: absolute; font-family: Inter, sans-serif; }}</style>
  <div id="root" data-composition-id="welt" data-width="1080" data-height="1920">
    <svg class="clip" data-start="0" data-duration="{F(END)}" viewBox="0 0 1080 1920" style="position:absolute;left:0;top:0;width:1080px;height:1920px" data-layout-ignore>{SVG}</svg>
{html}  </div>
  <script>(function () {{ {js}
{chr(10).join(J)}
    window.__timelines["welt"] = tl; }})();</script>
</template>
''')

# ---------- Ein-Wort-Untertitel ----------
HOT = {h.upper() for h in C.get("hot", [])} | {"RAUS!"}
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
    t1 = min(caps[j + 1][0] if j + 1 < len(caps) else END, t0 + 1.4)
    up = d.upper().strip("–…")
    col = "#ffd60a" if up in HOT or up.rstrip("!?.,:") in {x.rstrip("!?.,:") for x in HOT} else "#fff"
    fs = min(100, int(1600 / max(1, len(up))))
    items.append(f'<div id="w{j}" class="wd clip" data-start="{F(t0)}" data-duration="{F(max(.2, t1 - t0 - .02))}"><span id="w{j}-in" style="color:{col};font-size:{fs}px">{up}</span></div>')
    cj.append(f'tl.fromTo("#w{j}-in", {{ scale: 1.25, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: .09 }}, {F(t0)});')
open("compositions/caps.html", "w", encoding="utf-8").write(f'''<template>
  <style>#root {{ position: absolute; inset: 0; }} .wd {{ position: absolute; left: 0; right: 0; top: 1700px; text-align: center; }}
    .wd span {{ display: inline-block; font: 900 100px/1 Inter, sans-serif; white-space: nowrap; -webkit-text-stroke: 14px #000; paint-order: stroke fill; }}</style>
  <div id="root" data-composition-id="caps" data-width="1080" data-height="1920">{"".join(items)}</div>
  <script>(function () {{ const tl = gsap.timeline({{ paused: true }}); {" ".join(cj)} window.__timelines["caps"] = tl; }})();</script>
</template>
''')

# ---------- Musik + Ton ----------
P0 = round(st(D["szene"]) + T[D["szene"]]["words"][-1]["e"] + .05, 2)
FIN = round(tw - .1, 2)
subprocess.run([sys.executable, "tools/musik.py", F(END), F(P0), F(FIN)], check=True)
Hh = lambda id_, ti: f'      <div id="{id_}" data-composition-id="{id_}" data-composition-src="compositions/{id_}.html" data-start="0" data-duration="{F(END)}" data-track-index="{ti}" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index:{ti}"></div>'
lines = [Hh("welt", 2), Hh("caps", 3), f'      <audio id="musik" class="clip" data-start="0" data-duration="{F(END)}" data-track-index="5" data-volume="0.18" src="assets/musik.wav"></audio>']
for k in T:
    d = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"assets/vo/{k}.mp3"]))
    lines.append(f'      <audio id="vo-{k}" class="clip" data-start="{T[k]["start"] + T[k]["lead"]:.2f}" data-duration="{d:.2f}" data-track-index="4" data-volume="1" src="assets/vo/{k}.mp3"></audio>')
for j, (n, at, vol, dur) in enumerate(FX):
    lines.append(f'      <audio id="fx-{j}" class="clip" data-start="{F(max(0, at))}" data-duration="{F(min(dur, END - max(0, at)))}" data-volume="{vol}" data-track-index="{20 + j}" src="assets/sfx2/{n}.mp3"></audio>')
open("index.html", "w", encoding="utf-8").write(f'''<!doctype html>
<html lang="de" data-resolution="portrait"><head><meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" /><script src="assets/gsap.min.js"></script>
<style>* {{ margin: 0; padding: 0; box-sizing: border-box; }} html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #0d1b3e; }} #root {{ width: 100%; height: 100%; }}</style></head>
<body><div id="root" data-composition-id="main" data-start="0" data-duration="{F(END)}" data-width="1080" data-height="1920">
{chr(10).join(lines)}
</div><script>window.__timelines = window.__timelines || {{}}; window.__timelines["main"] = gsap.timeline({{ paused: true }});</script></body></html>
''')
print("Ende", END, "Pause", P0, "Finale", FIN)
