"""Countdown-Video (Platz N -> Platz 1) mit Hook, Zwischenfragen, Fakten, Zoom, SFX, Musik und CTA.
Aufruf: python3 tools/countdown.py   – liest countdown.json, voice.json, assets/vo/timing.json
Vorher: tools/musik.py wird automatisch mit den richtigen Zeiten aufgerufen."""
import json, re, subprocess, sys
T = json.load(open("assets/vo/timing.json")); V = json.load(open("voice.json")); C = json.load(open("countdown.json"))
F = lambda v: f"{v:.2f}".rstrip('0').rstrip('.')
norm = lambda s: re.sub(r"[^a-zäöüß0-9]", "", s.lower())
def w(s, word, n=1):
    c = 0
    for x in T[s]["words"]:
        if norm(x["w"]) == norm(word):
            c += 1
            if c == n: return round(T[s]["start"] + x["s"], 2)
    raise KeyError((s, word))
st = lambda k: T[k]["start"]
en = lambda k: round(T[k]["start"] + T[k]["slot"], 2)
END = round(max(en(k) for k in T), 2)
items = sorted(C["items"], key=lambda i: -i["rang"]); NMAX = len(items)
U = C["einheit"]

def ball(b, r, uid):
    t, cols = b["typ"], b["farben"]
    if t == "voll": f = f'<rect x="{-r}" y="{-r}" width="{2*r}" height="{2*r}" fill="{cols[0]}"/>'
    elif t == "mitte": f = f'<rect x="{-r}" y="{-r}" width="{2*r}" height="{2*r}" fill="{cols[0]}"/><rect x="{-r*.34}" y="{-r}" width="{r*.68}" height="{2*r}" fill="{cols[1]}"/>'
    elif t == "band": f = f'<rect x="{-r}" y="{-r}" width="{2*r}" height="{2*r}" fill="{cols[0]}"/><rect x="{-r}" y="{r*.45}" width="{2*r}" height="{r*.28}" fill="{cols[1]}"/>'
    elif t == "streifen":
        n = b.get("n", 6); wd = 2 * r / n
        f = "".join(f'<rect x="{-r + k*wd:.1f}" y="{-r}" width="{wd + .6:.1f}" height="{2*r}" fill="{cols[k % len(cols)]}"/>' for k in range(n))
    else: f = f'<rect x="{-r}" y="{-r}" width="{2*r}" height="{2*r}" fill="{cols[0]}"/><text y="{r*.3}" text-anchor="middle" font-size="{r}">{b.get("emoji", "")}</text>'
    s = r / 50
    eyes = (f'<g transform="scale({s:.3f})"><ellipse cx="-17" cy="-6" rx="13" ry="15" fill="#fff" stroke="#111" stroke-width="3"/><ellipse cx="17" cy="-6" rx="13" ry="15" fill="#fff" stroke="#111" stroke-width="3"/>'
            f'<circle cx="-14" cy="-4" r="6" fill="#111"/><circle cx="20" cy="-4" r="6" fill="#111"/></g>')
    return (f'<svg viewBox="{-r-6} {-r-6} {2*r+12} {2*r+12}" width="{2*r+12}" height="{2*r+12}" style="overflow:visible"><defs><clipPath id="cp{uid}"><circle r="{r}"/></clipPath></defs>'
            f'<g clip-path="url(#cp{uid})">{f}</g><circle r="{r}" fill="none" stroke="#111" stroke-width="{max(4, r/10):.0f}"/>{eyes}</svg>')

def ui(id_, t0, t1, inner, style, cls="ui"): return f'<div id="{id_}" class="{cls} clip" data-start="{F(t0)}" data-duration="{F(max(.05, t1 - t0))}" style="{style}">{inner}</div>\n'
def chip(id_, txt, bg="#ffd60a", fg="#111", size=44):
    return f'<div id="{id_}" style="display:inline-block;background:{bg};color:{fg};font:900 {size}px/1.15 Inter,sans-serif;padding:14px 28px;border-radius:20px;border:5px solid #111;box-shadow:0 9px 0 #111;max-width:960px">{txt}</div>'
STROKE = "-webkit-text-stroke:{}px #111;paint-order:stroke fill"

html, J, FX = "", [], []
# ---------- Hintergrund: Stadion-Nacht mit Scheinwerfern ----------
dots = "".join(f'<circle cx="{(k*137) % 1080}" cy="{(k*211) % 1900}" r="{1 + k % 3}" fill="#fff" opacity="{.15 + (k % 4)*.08:.2f}"/>' for k in range(70))
bg = (f'<svg viewBox="0 0 1080 1920" width="1080" height="1920" style="position:absolute;left:0;top:0"><defs>'
      f'<radialGradient id="g0" cx=".5" cy=".38" r=".75"><stop offset="0" stop-color="#1d2a6b"/><stop offset=".6" stop-color="#0b1030"/><stop offset="1" stop-color="#04050d"/></radialGradient>'
      f'<linearGradient id="beam" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".35"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient></defs>'
      f'<rect width="1080" height="1920" fill="url(#g0)"/>{dots}'
      f'<g id="sp1" transform="translate(120 -40) rotate(-20)"><path d="M-30 0 L30 0 L260 1500 L-260 1500 Z" fill="url(#beam)"/></g>'
      f'<g id="sp2" transform="translate(960 -40) rotate(20)"><path d="M-30 0 L30 0 L260 1500 L-260 1500 Z" fill="url(#beam)"/></g></svg>')
html += ui("bg", 0, END, bg, "left:0;top:0;width:1080px;height:1920px", "bgl")
J += [f'tl.fromTo("#sp1", {{ rotation: -28 }}, {{ rotation: 6, duration: 3.2, ease: "sine.inOut", yoyo: true, repeat: {int(END/3.2)}, svgOrigin: "120 -40" }}, 0);',
      f'tl.fromTo("#sp2", {{ rotation: 28 }}, {{ rotation: -6, duration: 2.7, ease: "sine.inOut", yoyo: true, repeat: {int(END/2.7)}, svgOrigin: "960 -40" }}, 0);']

# ---------- Titel oben ----------
html += ui("ttl", 0, END, f'<div style="font:900 38px Inter,sans-serif;color:#ffd60a;letter-spacing:.05em">{C["titel"][0]}</div><div style="font:900 70px/1.05 Inter,sans-serif;color:#fff;{STROKE.format(8)}">{C["titel"][1]}</div>', "left:0;right:0;top:90px;text-align:center")

# ---------- Kamera-Container (Zoom/Shake) ----------
cam = ""
# Hook
h = C["hook"]; hs = st(h["szene"]); hq = w(h["szene"], h["frage_wort"])
cam += ui("hk", hs, hq + .1, f'<div id="hk-n" style="font:900 300px/1 Inter,sans-serif;color:#ffd60a;{STROKE.format(16)}">{h["gross"]}</div>'
          f'<div id="hk-s" style="display:inline-block;margin-top:10px;transform:rotate(-6deg);border:10px solid #e63946;border-radius:18px;padding:6px 26px;font:900 92px/1 Inter,sans-serif;color:#e63946;background:rgba(0,0,0,.35)">{h["stempel"]}</div>',
          "left:0;right:0;top:520px;text-align:center")
J += [f'tl.fromTo("#hk-n", {{ scale: 3.2, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: .28, ease: "power4.in" }}, {F(hs + .02)});',
      f'tl.fromTo("#hk-s", {{ scale: 2.4, opacity: 0, rotation: -18 }}, {{ scale: 1, opacity: 1, rotation: -6, duration: .22, ease: "back.out(3)" }}, {F(w(h["szene"], "Prozent") + .3)});',
      f'tl.to("#hk", {{ opacity: 0, scale: .6, duration: .2 }}, {F(hq - .1)});']
FX += [("hit", hs + .25, .7, 1.4), ("pop", w(h["szene"], "Prozent") + .3, .6, .15)]
# Fragezeichen-Kugeln während der Frage
qballs = "".join(f'<div class="qb" style="display:inline-block;margin:0 8px;width:96px;height:96px;border-radius:50%;background:#2a3570;border:6px solid #111;font:900 64px/84px Inter,sans-serif;color:#ffd60a">?</div>' for _ in range(NMAX))
q_end = st(items[0]["szene"])
cam += ui("qq", hq, q_end, f'<div style="width:900px;margin:0 auto;line-height:120px">{qballs}</div>', "left:0;right:0;top:560px;text-align:center")
J.append(f'gsap.utils.toArray("#qq .qb").forEach((el, k) => tl.fromTo(el, {{ scale: 0, rotation: -90 }}, {{ scale: 1, rotation: 0, duration: .25, ease: "back.out(2.5)" }}, {F(hq)} + k * .08));')
FX.append(("blips", hq, .35, 1.0))

# Rangliste unten (wird von unten nach oben gefüllt)
LY, LH = 1250, 50
lb = ""
for it in items:
    y = LY + (it["rang"] - 1) * LH
    lb += (f'<div style="position:absolute;left:150px;top:{y}px;width:780px;height:{LH-6}px;border-radius:12px;background:rgba(255,255,255,.07);border:2px solid rgba(255,255,255,.12)"></div>'
           f'<div class="lq" style="position:absolute;left:170px;top:{y+4}px;font:900 32px Inter,sans-serif;color:rgba(255,255,255,.35)">#{it["rang"]}  ???</div>'
           f'<div id="lr{it["rang"]}" style="position:absolute;left:150px;top:{y}px;width:780px;height:{LH-6}px;border-radius:12px;background:{"#ffd60a" if it["rang"] == 1 else "#1b2457"};border:3px solid #111;opacity:0">'
           f'<div style="position:absolute;left:14px;top:3px;font:900 32px Inter,sans-serif;color:{"#111" if it["rang"] == 1 else "#ffd60a"}">#{it["rang"]}</div>'
           f'<div style="position:absolute;left:84px;top:-1px">{ball(it["ball"], 19, "l" + str(it["rang"]))}</div>'
           f'<div style="position:absolute;left:140px;top:3px;font:900 32px Inter,sans-serif;color:{"#111" if it["rang"] == 1 else "#fff"}">{it["name"]}</div>'
           f'<div style="position:absolute;right:18px;top:3px;font:900 32px Inter,sans-serif;color:{"#111" if it["rang"] == 1 else "#ffd60a"}">{it["wert"]}</div></div>')
html += ui("lb", q_end, END, lb, "left:0;top:0;width:1080px;height:1920px")
J.append(f'tl.fromTo("#lb", {{ opacity: 0, y: 60 }}, {{ opacity: 1, y: 0, duration: .35 }}, {F(q_end)});')

# Kandidaten
fin = C["finale"]; FS = fin["szene"]
nxt = {}
seq = [it["szene"] for it in items]
for k, it in enumerate(items):
    s = it["szene"]; r = it["rang"]; t0 = st(s)
    t1 = st(seq[k + 1]) if k + 1 < len(seq) else END
    # bis zur nächsten Kandidatenszene (Fragen dazwischen überdecken)
    for q in C["fragen"]:
        if t0 < st(q["szene"]) < t1: t1 = st(q["szene"])
    big = r == 1
    tn = w(s, it["namewort"]) if it.get("namewort") else t0
    tv = w(s, it["wertwort"])
    tf = tv + .75
    R = 190 if big else 150
    inner = (f'<div id="rk{r}" style="font:900 {150 if not big else 170}px/1 Inter,sans-serif;color:#ffd60a;{STROKE.format(12)}">#{r}</div>'
             f'<div id="bl{r}" style="margin:10px auto 0;width:{2*R+12}px;height:{2*R+12}px;position:relative">'
             + (f'<div id="rays" style="position:absolute;left:50%;top:50%;width:1400px;height:1400px;margin:-700px 0 0 -700px;border-radius:50%;background:repeating-conic-gradient(rgba(255,214,10,.28) 0 10deg,transparent 10deg 20deg);opacity:0"></div>'
                f'<div id="crown" style="position:absolute;left:50%;top:-120px;margin-left:-90px;width:180px;opacity:0"><svg viewBox="-50 -55 100 60" width="180"><path d="M-44 0 L-44 -40 L-22 -18 L0 -50 L22 -18 L44 -40 L44 0 Z" fill="#ffd60a" stroke="#111" stroke-width="4"/></svg></div>' if big else "")
             + f'<div style="position:relative">{ball(it["ball"], R, "b" + str(r))}</div></div>'
             f'<div id="nm{r}" style="margin-top:14px;font:900 {84 if len(it["name"]) < 12 else 70}px/1 Inter,sans-serif;color:#fff;{STROKE.format(10)}">{it["name"]}</div>'
             f'<div id="vl{r}" style="margin-top:12px;font:900 {170 if big else 120}px/1 Inter,sans-serif;color:{"#ffd60a" if big else "#4cf0a8"};{STROKE.format(12)}"><span id="vn{r}">0</span> <span style="font-size:.45em">{U}</span></div>')
    cam += ui(f"it{r}", t0, t1, inner, f"left:0;right:0;top:{300 if big else 330}px;text-align:center")
    cam += ui(f"fk{r}", tf, t1, chip(f"fk{r}-in", "💡 " + it["fakt"], "#fff", "#111", 40), f"left:0;right:0;top:{1150 if not big else 1165}px;text-align:center")
    J += [f'tl.fromTo("#rk{r}", {{ scale: 3, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: .22, ease: "power3.in" }}, {F(t0)});',
          f'tl.fromTo("#bl{r}", {{ scale: 0, rotation: -200 }}, {{ scale: 1, rotation: 0, duration: .4, ease: "back.out(1.8)" }}, {F(tn)});',
          f'tl.fromTo("#nm{r}", {{ y: 40, opacity: 0 }}, {{ y: 0, opacity: 1, duration: .25, ease: "power2.out" }}, {F(tn + .1)});',
          f'tl.fromTo("#vl{r}", {{ scale: 2.2, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: .25, ease: "back.out(2)" }}, {F(tv - .05)});',
          f'(() => {{ const o = {{ v: 0 }}; tl.fromTo(o, {{ v: 0 }}, {{ v: {it["wert"]}, duration: {.9 if big else .35}, ease: "power1.out", onUpdate: () => {{ document.getElementById("vn{r}").textContent = Math.round(o.v); }} }}, {F(tv - .05)}); }})();',
          f'tl.fromTo("#fk{r}-in", {{ scale: .3, opacity: 0, rotation: -4 }}, {{ scale: 1, opacity: 1, rotation: -2, duration: .25, ease: "back.out(2.5)" }}, {F(tf)});',
          f'tl.fromTo("#cam", {{ scale: 1.1 }}, {{ scale: 1, duration: .45, ease: "power3.out", transformOrigin: "50% 40%" }}, {F(tv - .05)});',
          f'tl.fromTo("#lr{r}", {{ opacity: 0, x: -80 }}, {{ opacity: 1, x: 0, duration: .3, ease: "power2.out" }}, {F(tv + .2)});']
    if not big:
        J.append(f'tl.to("#it{r}", {{ scale: .2, y: {LY + (r - 1) * LH - 600}, opacity: 0, duration: .3, ease: "power2.in" }}, {F(t1 - .3)});')
        J.append(f'tl.to("#fk{r}", {{ opacity: 0, duration: .2 }}, {F(t1 - .3)});')
    FX += [("whoosh", t0 - .05, .45, .8), ("hit", tv - .05, .55 if not big else 1.0, 1.4), ("pop", tf, .4, .15), ("tick", tv + .2, .3, .3)]

# Zwischenfragen
for q in C["fragen"]:
    s = q["szene"]; t0, t1 = st(s), en(s)
    cam += ui("fq" + s, t0, t1, chip("fq" + s + "-in", q["text"], "#e63946", "#fff", 62), "left:0;right:0;top:700px;text-align:center")
    J += [f'tl.fromTo("#fq{s}-in", {{ scale: 2, opacity: 0, rotation: 8 }}, {{ scale: 1, opacity: 1, rotation: -3, duration: .3, ease: "back.out(2.5)" }}, {F(t0)});',
          f'tl.to("#fq{s}-in", {{ x: "+=8", duration: .05, yoyo: true, repeat: 7 }}, {F(t0 + .35)});',
          f'tl.to(".lq", {{ color: "rgba(255,214,10,.9)", duration: .2, yoyo: true, repeat: 3 }}, {F(t0 + .1)});']
    FX += [("swoosh", t0, .45, .6), ("riser", t0, .25, min(2.5, t1 - t0))]

# Spannungspause vor Platz 1: abdunkeln + langsamer Zoom
prev = items[-2]["szene"]
P0 = round(st(prev) + T[prev]["words"][-1]["e"] + .05, 2)
P0 = min(P0, st(FS) - .4)
FIN = w(FS, fin.get("namewort", items[-1].get("namewort", "Real")))
cam += ui("dim", P0, FIN + .05, "", "left:0;top:0;width:1080px;height:1920px;background:#000")
J += [f'tl.fromTo("#dim", {{ opacity: 0 }}, {{ opacity: .7, duration: .4 }}, {F(P0)});',
      f'tl.fromTo("#cam", {{ scale: 1 }}, {{ scale: 1.12, duration: {F(FIN - P0)}, ease: "power1.in", transformOrigin: "50% 40%" }}, {F(P0)});']
# Auflösung: Blitz, Strahlen, Krone, Konfetti, Shake
cam += ui("flash", FIN, FIN + .5, "", "left:0;top:0;width:1080px;height:1920px;background:#fff")
J += [f'tl.fromTo("#flash", {{ opacity: 1 }}, {{ opacity: 0, duration: .45 }}, {F(FIN)});',
      f'tl.fromTo("#rays", {{ opacity: 0, rotation: 0 }}, {{ opacity: 1, rotation: 120, duration: {F(END - FIN)}, ease: "none" }}, {F(FIN)});',
      f'tl.fromTo("#crown", {{ opacity: 0, y: -200 }}, {{ opacity: 1, y: 0, duration: .45, ease: "bounce.out" }}, {F(w(FS, items[-1]["wertwort"]))});',
      f'tl.to("#cam", {{ x: "+=14", y: "-=10", duration: .04, yoyo: true, repeat: 9, ease: "none" }}, {F(FIN)});']
tw = w(FS, items[-1]["wertwort"])
J.append(f'tl.to("#cam", {{ x: "+=10", duration: .04, yoyo: true, repeat: 7, ease: "none" }}, {F(tw)});')
tww = w(FS, fin["wowwort"])
cam += ui("wow", tww, END, chip("wow-in", fin["wow"], "#ffd60a", "#111", 46), "left:0;right:0;top:1060px;text-align:center")
J.append(f'tl.fromTo("#wow-in", {{ scale: 1.8, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: .3, ease: "back.out(2)" }}, {F(tww)});')
J.append(f'tl.to("#fk1", {{ opacity: 0, duration: .15 }}, {F(tww - .1)});')
conf = "".join(f'<div class="cf" style="position:absolute;left:{(k*83) % 1040}px;top:-40px;width:18px;height:28px;border-radius:4px;background:{["#ffd60a","#e63946","#fff","#4cf0a8","#4cc9f0"][k % 5]}"></div>' for k in range(60))
html_conf = ui("cf", FIN, END, conf, "left:0;top:0;width:1080px;height:1920px;pointer-events:none")
J.append(f'gsap.utils.toArray(".cf").forEach((el, k) => tl.fromTo(el, {{ y: 0, rotation: 0 }}, {{ y: 1950 + (k % 7) * 40, rotation: 360 + k * 40, duration: 2.4 + (k % 5) * .35, ease: "none" }}, {F(FIN)} + (k % 12) * .07));')
FX += [("hit", FIN - .02, 1.0, 1.6), ("chime", tw, .6, 1.4), ("blips", FIN + .2, .4, 1.3), ("hit", tw, .7, 1.4)]
# CTA
c = C["cta"]; cs = st(c["szene"])
html_cta = ui("cta", cs, END, chip("cta-a", c["text"], "#fff", "#111", 56) + '<div style="height:18px"></div>' + chip("cta-b", c["sub"], "#e63946", "#fff", 40), "left:0;right:0;top:620px;text-align:center")
J += [f'tl.fromTo("#cta-a", {{ y: -60, opacity: 0 }}, {{ y: 0, opacity: 1, duration: .3, ease: "back.out(2)" }}, {F(cs)});',
      f'tl.fromTo("#cta-b", {{ y: 60, opacity: 0 }}, {{ y: 0, opacity: 1, duration: .3, ease: "back.out(2)" }}, {F(cs + .5)});',
      f'tl.to("#cta-b", {{ scale: 1.08, duration: .35, yoyo: true, repeat: 5, ease: "sine.inOut" }}, {F(cs + .9)});',
      f'tl.to("#it1", {{ opacity: .25, duration: .3 }}, {F(cs)});', f'tl.to("#wow", {{ opacity: 0, duration: .3 }}, {F(cs)});']
FX.append(("pop", cs, .5, .15))

html += f'<div id="cam" class="ui" style="left:0;top:0;width:1080px;height:1920px">{cam}</div>\n' + html_conf + html_cta

open("compositions/welt.html", "w", encoding="utf-8").write(f'''<template>
  <style>#root {{ position: absolute; inset: 0; overflow: hidden; }} .ui, .bgl {{ position: absolute; font-family: Inter, sans-serif; }}
    #dim {{ z-index: 5; }} #it1, #fk1, #wow, #flash {{ z-index: 6; }} #cf {{ z-index: 7; }} #cta {{ z-index: 8; }}</style>
  <div id="root" data-composition-id="welt" data-width="1080" data-height="1920">
{html}  </div>
  <script>(function () {{ const tl = gsap.timeline({{ paused: true }});
{chr(10).join("    " + j for j in J)}
    window.__timelines["welt"] = tl; }})();</script>
</template>
''')

# ---------- Ein-Wort-Untertitel ----------
HOT = {h.upper() for h in C.get("hot", [])}
caps = []
for sc in V["scenes"]:
    sid = sc["id"]; words = T[sid]["words"]; k = 0
    for disp, sp in sc["groups"]:
        dw, swn = disp.split(), sp.split()
        for i, d in enumerate(dw):
            if not any(ch.isalnum() for ch in d): continue
            caps.append((round(T[sid]["start"] + words[min(len(words) - 1, k + int(i * len(swn) / len(dw)))]["s"], 2), d))
        k += len(swn)
it_, cj = [], []
for i, (t0, d) in enumerate(caps):
    t1 = min(caps[i + 1][0] if i + 1 < len(caps) else END, t0 + 1.2)
    up = d.upper().strip("–…")
    col = "#ffd60a" if up in HOT or up.rstrip("!?.,:") in {x.rstrip("!?.,:") for x in HOT} else "#fff"
    fs = min(92, int(1500 / max(1, len(up))))
    it_.append(f'<div id="w{i}" class="wd clip" data-start="{F(t0)}" data-duration="{F(max(.15, t1 - t0 - .02))}"><span id="w{i}-in" style="color:{col};font-size:{fs}px">{up}</span></div>')
    cj.append(f'tl.fromTo("#w{i}-in", {{ scale: 1.25, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: .08 }}, {F(t0)});')
open("compositions/caps.html", "w", encoding="utf-8").write(f'''<template>
  <style>#root {{ position: absolute; inset: 0; }} .wd {{ position: absolute; left: 0; right: 0; top: 1700px; text-align: center; }}
    .wd span {{ display: inline-block; font: 900 92px/1 Inter, sans-serif; white-space: nowrap; -webkit-text-stroke: 13px #000; paint-order: stroke fill; }}</style>
  <div id="root" data-composition-id="caps" data-width="1080" data-height="1920">{"".join(it_)}</div>
  <script>(function () {{ const tl = gsap.timeline({{ paused: true }}); {" ".join(cj)} window.__timelines["caps"] = tl; }})();</script>
</template>
''')

# ---------- Musik + Ton ----------
subprocess.run([sys.executable, "tools/musik.py", F(END), F(P0), F(FIN)], check=True)
H = lambda id_, ti: f'      <div id="{id_}" data-composition-id="{id_}" data-composition-src="compositions/{id_}.html" data-start="0" data-duration="{F(END)}" data-track-index="{ti}" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index:{ti}"></div>'
lines = [H("welt", 2), H("caps", 3), f'      <audio id="musik" class="clip" data-start="0" data-duration="{F(END)}" data-track-index="5" data-volume="0.2" src="assets/musik.wav"></audio>']
for k in T:
    d = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"assets/vo/{k}.mp3"]))
    lines.append(f'      <audio id="vo-{k}" class="clip" data-start="{T[k]["start"] + T[k]["lead"]:.2f}" data-duration="{d:.2f}" data-track-index="4" data-volume="1" src="assets/vo/{k}.mp3"></audio>')
for j, (n, at, vol, dur) in enumerate(FX):
    lines.append(f'      <audio id="fx-{j}" class="clip" data-start="{F(max(0, at))}" data-duration="{F(min(dur, END - max(0, at)))}" data-volume="{vol}" data-track-index="{20 + j}" src="assets/sfx2/{n}.mp3"></audio>')
open("index.html", "w", encoding="utf-8").write(f'''<!doctype html>
<html lang="de" data-resolution="portrait"><head><meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" /><script src="assets/gsap.min.js"></script>
<style>* {{ margin: 0; padding: 0; box-sizing: border-box; }} html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #0b1030; }} #root {{ width: 100%; height: 100%; }}</style></head>
<body><div id="root" data-composition-id="main" data-start="0" data-duration="{F(END)}" data-width="1080" data-height="1920">
{chr(10).join(lines)}
</div><script>window.__timelines = window.__timelines || {{}}; window.__timelines["main"] = gsap.timeline({{ paused: true }});</script></body></html>
''')
print("Ende", END, "Pause", P0, "Finale", FIN)
