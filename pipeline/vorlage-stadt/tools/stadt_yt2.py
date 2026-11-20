"""YouTube-Stadt – Tag 2 (keine neuen Wünsche): Rundfahrt durch die 5 Häuser + leerer Bauplatz "DEIN HAUS?" + Aufruf.
Aufruf: python3 tools/stadt_yt2.py 2"""
import json, subprocess, sys
sys.path.insert(0, "tools"); import globi_strich as globi

TAG = int(sys.argv[1]) if len(sys.argv) > 1 else 2
T = json.load(open("assets/vo/timing.json")); V = json.load(open("voice.json"))
H = json.load(open("stadt.json"))["haeuser"]
F = lambda v: f"{v:.2f}".rstrip('0').rstrip('.')
def w(s, word, n=1):
    c = 0
    for x in T[s]["words"]:
        if x["w"] == word:
            c += 1
            if c == n: return round(T[s]["start"] + x["s"], 2)
    raise KeyError((s, word))
st = lambda k: T[k]["start"]
END = round(max(v["start"] + v["slot"] for v in T.values()), 2)
BAND = 1440   # ab hier dunkler Streifen (25 % der Höhe) mit Untertitel + Globi

ROWS = {0: (1010, .80), 1: (800, .68), 2: (615, .57)}
def pos(h):
    gy, sc = ROWS[h["reihe"]]
    return 1080 / 7 * (h["platz"] + .5), gy, sc
def G(cx, gy, sc, inner, cls=""): return f'<g transform="translate({cx:.1f} {gy:.1f}) scale({sc:.3f})"{cls}>{inner}</g>'
def emo(e, x, y, size): return f'<text x="{x:.0f}" y="{y:.0f}" text-anchor="middle" style="font:{size:.0f}px Noto Color Emoji">{e}</text>'
def board(cx, y, wd, ht, text, bg, fg, fs):
    return (f'<rect x="{cx - wd / 2:.1f}" y="{y:.1f}" width="{wd:.1f}" height="{ht:.1f}" rx="6" fill="{bg}" stroke="#111" stroke-width="3"/>'
            f'<text x="{cx:.1f}" y="{y + ht / 2 + fs * .36:.1f}" text-anchor="middle" style="font:900 {fs}px Inter,sans-serif;fill:{fg}">{text}</text>')
def car(x, y, s, col, plate=""):
    pl = f'<rect x="-22" y="-12" width="44" height="14" rx="2" fill="#fff" stroke="#111" stroke-width="1.5"/><text x="0" y="-1" text-anchor="middle" style="font:900 10px Inter,sans-serif;fill:#d62828">{plate}</text>' if plate else ""
    return (f'<g transform="translate({x:.1f} {y:.1f}) scale({s:.2f})"><path d="M-60 0 Q-60 -18 -44 -20 L-26 -22 Q-14 -40 8 -40 L26 -40 Q42 -38 52 -22 L60 -18 Q66 -14 64 0 Z" fill="{col}" stroke="#111" stroke-width="3"/>'
            f'<path d="M-58 -10 H62" stroke="#d62828" stroke-width="6"/><rect x="-8" y="-48" width="16" height="8" rx="3" fill="#3a86ff" class="blau"/>'
            f'<circle cx="-36" cy="2" r="11" fill="#222"/><circle cx="38" cy="2" r="11" fill="#222"/><circle cx="-36" cy="2" r="4" fill="#ccc"/><circle cx="38" cy="2" r="4" fill="#ccc"/>{pl}</g>')
def tree(x, gy, sc):
    return G(x, gy, sc, '<rect x="-6" y="-40" width="12" height="40" fill="#7a4e2d"/><circle cy="-58" r="26" fill="#3f9b47" stroke="#2c6e33" stroke-width="3"/>')

# ---------- Gebäude (lokale Koordinaten: Ursprung = Boden-Mitte) ----------
def flughafen(h):
    col = h.get("farbe", "#1d4ed8"); s = -1 if h.get("turm") == "links" else 1
    o = '<rect x="-160" y="-16" width="320" height="16" fill="#3a3f46"/>' + "".join(f'<rect x="{-150 + i * 40}" y="-9" width="22" height="3" fill="#fff"/>' for i in range(8))
    tx = s * 118
    o += f'<rect x="{tx - 8}" y="-190" width="16" height="174" fill="#dfe3e8" stroke="#111" stroke-width="3"/>'
    o += f'<path d="M{tx - 30} -222 H{tx + 30} L{tx + 22} -190 H{tx - 22} Z" fill="#bfe6ff" stroke="#111" stroke-width="3"/><rect x="{tx - 34}" y="-232" width="68" height="10" fill="{col}" stroke="#111" stroke-width="3"/>'
    o += f'<path d="M{tx} -232 V-252" stroke="#111" stroke-width="3"/><circle cx="{tx}" cy="-254" r="4" fill="#e63946"/>'
    bx = -s * 10
    o += f'<rect x="{bx - 85}" y="-82" width="170" height="66" fill="#eef3fa" stroke="#111" stroke-width="3"/><rect x="{bx - 77}" y="-64" width="154" height="26" fill="#bfe6ff" stroke="#111" stroke-width="2"/>'
    o += f'<rect x="{bx - 92}" y="-92" width="184" height="12" fill="{col}" stroke="#111" stroke-width="3"/>'
    o += board(bx, -124, 184, 30, "✈ " + h.get("schild", "FLUGHAFEN"), col, "#fff", 19)
    pl = (f'<g class="plane"><path d="M-80 -30 Q-80 -42 -60 -42 H50 Q78 -42 86 -32 Q78 -22 50 -22 H-60 Q-80 -22 -80 -30 Z" fill="#fff" stroke="#111" stroke-width="3"/>'
          f'<path d="M-78 -40 L-92 -66 H-72 L-52 -42 Z" fill="{col}" stroke="#111" stroke-width="3"/><path d="M-10 -30 L-34 -6 H-14 L18 -30 Z" fill="#dfe3e8" stroke="#111" stroke-width="3"/>'
          f'<path d="M-60 -30 H60" stroke="{col}" stroke-width="5"/>' + "".join(f'<circle cx="{-40 + i * 16}" cy="-36" r="3" fill="#457b9d"/>' for i in range(7)) + '</g>')
    return o + f'<g transform="translate({s * -20} 4)">{pl}</g>', -124, -70
def bundeshaus(h):
    o = '<rect x="-118" y="-14" width="236" height="14" fill="#cbbf9f" stroke="#111" stroke-width="3"/><rect x="-104" y="-24" width="208" height="10" fill="#ddd1b0" stroke="#111" stroke-width="3"/>'
    o += '<rect x="-96" y="-118" width="192" height="94" fill="#f3e9d2" stroke="#111" stroke-width="3"/>'
    o += "".join(f'<rect x="{-86 + i * 30}" y="-108" width="14" height="80" fill="#fff" stroke="#111" stroke-width="2"/>' for i in range(6))
    o += '<path d="M-108 -118 L0 -152 L108 -118 Z" fill="#efe2c2" stroke="#111" stroke-width="3" stroke-linejoin="round"/>'
    o += '<rect x="-42" y="-176" width="84" height="26" fill="#efe2c2" stroke="#111" stroke-width="3"/><path d="M-50 -176 A50 46 0 0 1 50 -176 Z" fill="#5fae8a" stroke="#111" stroke-width="3"/>'
    o += '<path d="M0 -222 V-272" stroke="#555" stroke-width="4"/><rect x="2" y="-272" width="46" height="46" fill="#d52b1e" stroke="#111" stroke-width="2"/><rect x="20" y="-263" width="10" height="28" fill="#fff"/><rect x="11" y="-254" width="28" height="10" fill="#fff"/>'
    o += board(0, -66, 170, 30, "🏛 BUNDESHAUS", "#264653", "#fff", 19)
    return o, -272, -110
def militaer(h):
    o = '<rect x="-160" y="-12" width="320" height="12" fill="#9aa0a8" stroke="#111" stroke-width="2"/>'
    o += '<path d="M-140 -12 V-50 Q-140 -116 -60 -116 Q20 -116 20 -50 V-12 Z" fill="#6b7d3e" stroke="#111" stroke-width="3"/>'
    o += '<ellipse cx="-95" cy="-80" rx="20" ry="12" fill="#4a5a2a"/><ellipse cx="-30" cy="-95" rx="24" ry="10" fill="#8a9a55"/><ellipse cx="-10" cy="-50" rx="16" ry="12" fill="#4a5a2a"/><ellipse cx="-115" cy="-35" rx="14" ry="10" fill="#8a9a55"/>'
    o += '<rect x="-90" y="-62" width="62" height="50" fill="#2f3a1c" stroke="#111" stroke-width="3"/>'
    o += ('<g transform="translate(90 -12)"><rect x="-58" y="-26" width="116" height="20" rx="8" fill="#556b2f" stroke="#111" stroke-width="3"/>'
          '<rect x="-60" y="-8" width="120" height="16" rx="8" fill="#333" stroke="#111" stroke-width="2"/>' + "".join(f'<circle cx="{-46 + i * 23}" cy="0" r="5" fill="#777"/>' for i in range(5)) +
          '<rect x="-30" y="-46" width="56" height="22" rx="8" fill="#6b7d3e" stroke="#111" stroke-width="3"/><rect x="24" y="-40" width="62" height="8" fill="#556b2f" stroke="#111" stroke-width="2"/></g>')
    o += ('<g class="heli"><g transform="translate(120 -150)"><ellipse rx="30" ry="15" fill="#ffd60a" stroke="#111" stroke-width="3"/><path d="M26 -2 H62 L68 -12" stroke="#111" stroke-width="5" fill="none"/>'
          '<ellipse cx="-10" cy="-3" rx="12" ry="8" fill="#bfe6ff" stroke="#111" stroke-width="2"/><path d="M0 -15 V-22 M-44 -24 H44" stroke="#111" stroke-width="4"/><path d="M-20 15 V22 M20 15 V22 M-28 22 H28" stroke="#111" stroke-width="3"/></g></g>')
    o += board(-60, -148, 170, 30, "★ STÜTZPUNKT", "#3b4a1e", "#fff", 19)
    return o, -148, -70
def krankenhaus(h):
    o = '<rect x="-74" y="-178" width="148" height="178" fill="#fff" stroke="#111" stroke-width="3"/>'
    o += "".join(f'<rect x="{-60 + c * 44}" y="{-150 + r * 34}" width="32" height="22" fill="#bfe6ff" stroke="#111" stroke-width="2"/>' for r in range(4) for c in range(3) if not (r == 3 and c == 1))
    o += '<rect x="-20" y="-46" width="40" height="46" fill="#9fd3f5" stroke="#111" stroke-width="3"/><path d="M0 -46 V0" stroke="#111" stroke-width="2"/>'
    o += '<rect x="-9" y="-170" width="18" height="2" fill="none"/>'
    o += board(0, -214, 196, 32, "✚ KRANKENHAUS", "#e63946", "#fff", 20)
    o += '<g transform="translate(0 -128)"><rect x="-8" y="-22" width="16" height="44" fill="#e63946"/><rect x="-22" y="-8" width="44" height="16" fill="#e63946"/></g>'
    o += car(-118, -2, .85, "#fff", "112")
    return o, -214, -90
def bauplatz():
    o = '<path d="M-170 0 Q-160 -22 -100 -24 H100 Q160 -22 170 0 Z" fill="#b5835a" stroke="#7a5233" stroke-width="3"/>'
    o += '<path d="M-130 -18 Q-110 -44 -86 -18 Z" fill="#d9a066" stroke="#7a5233" stroke-width="2"/><path d="M96 -18 Q118 -40 142 -18 Z" fill="#d9a066" stroke="#7a5233" stroke-width="2"/>'
    for x in (-150, 150):   # Absperrungen
        o += f'<g transform="translate({x} 0)"><rect x="-26" y="-50" width="52" height="16" fill="#fff" stroke="#111" stroke-width="2"/>' + "".join(f'<path d="M{-22 + i * 14} -36 l10 -12" stroke="#e63946" stroke-width="6"/>' for i in range(4)) + '<path d="M-20 -34 V0 M20 -34 V0" stroke="#111" stroke-width="4"/></g>'
    o += '<path d="M-100 -20 V-118 M100 -20 V-118" stroke="#6b4a32" stroke-width="12"/>'
    o += ('<g class="plot"><rect x="-172" y="-218" width="344" height="104" rx="12" fill="#ffd60a" stroke="#111" stroke-width="5"/>'
          '<text x="0" y="-160" text-anchor="middle" style="font:900 48px Inter,sans-serif;fill:#1d3557">DEIN HAUS?</text>'
          '<text x="0" y="-127" text-anchor="middle" style="font:900 22px Inter,sans-serif;fill:#c1121f">BAUPLATZ FREI</text></g>')
    o += '<g transform="translate(-40 -20)"><path d="M0 0 L12 -30 L24 0 Z" fill="#f77f00" stroke="#111" stroke-width="2"/><rect x="6" y="-16" width="12" height="5" fill="#fff"/></g>'
    o += '<g transform="translate(20 -20)"><path d="M0 0 L12 -30 L24 0 Z" fill="#f77f00" stroke="#111" stroke-width="2"/><rect x="6" y="-16" width="12" height="5" fill="#fff"/></g>'
    return o, -218, -120
ART = {"flughafen": flughafen, "bundeshaus": bundeshaus, "militaer": militaer, "krankenhaus": krankenhaus}

def tagsvg(k, name, cx, top, sc):
    ts = max(sc, .8); fs = 34 * ts; lw = (40 + 24 * len(name)) * ts; ht = 50 * ts; y = top - 12 * sc - ht
    return (f'<g id="t{k}"><rect x="{cx - lw / 2:.1f}" y="{y:.1f}" width="{lw:.1f}" height="{ht:.1f}" rx="{ht / 2:.1f}" fill="#fff" stroke="#1d3557" stroke-width="4"/>'
            f'<text x="{cx:.1f}" y="{y + ht / 2 + fs * .36:.1f}" text-anchor="middle" style="font:900 {fs:.0f}px Inter,sans-serif;fill:#1d3557">{name}</text></g>')

houses, tags, C, TOP = "", "", {}, {}
order = sorted(range(len(H)), key=lambda k: -H[k]["reihe"])
trees = "".join(tree(x, gy, sc) for x, gy, sc in [(60, 615, .57), (400, 600, .5), (700, 600, .5), (1030, 615, .57), (70, 800, .68), (250, 790, .6), (830, 790, .6), (1020, 800, .68),
                                                  (30, 1010, .8), (390, 1012, .8), (690, 1012, .8), (1050, 1010, .8)])
for k in order:
    h = H[k]; cx, gy, sc = pos(h)
    inner, top, mid = ART[h["art"]](h)
    houses += f'<g id="h{k}">{G(cx, gy, sc, inner)}</g>'
    tags += tagsvg(k, h["name"], cx, gy + top * sc, sc); C[k] = (cx, gy + mid * sc); TOP[k] = gy + top * sc
# Bauplatz vorne Mitte (Reihe 0, Platz 3)
bx, bgy, bsc = 540, 1010, .8
inner, btop, bmid = bauplatz()
houses += f'<g id="bp">{G(bx, bgy, bsc, inner)}</g>'
C["bp"] = (bx, bgy + bmid * bsc)
idx = {h["name"]: k for k, h in enumerate(H)}
hills = ('<path d="M-300 600 Q270 540 540 580 Q820 620 1380 550 L1380 1700 L-300 1700 Z" fill="#7cc46b"/>'
         '<path d="M-300 830 Q300 790 560 820 Q820 850 1380 800 L1380 1700 L-300 1700 Z" fill="#6ab35a"/>'
         '<path d="M-300 985 Q300 965 560 980 Q820 995 1380 975 L1380 1700 L-300 1700 Z" fill="#5aa24b"/>'
         '<rect x="-300" y="1040" width="1680" height="44" fill="#9aa0a8"/><path d="M-300 1062 H1380" stroke="#fff" stroke-width="4" stroke-dasharray="30 26"/>')
clouds = "".join(f'<g opacity=".9"><ellipse cx="{x}" cy="{y}" rx="70" ry="28" fill="#fff"/><ellipse cx="{x + 50}" cy="{y - 14}" rx="50" ry="26" fill="#fff"/></g>' for x, y in [(120, 330), (820, 300), (480, 420), (980, 460)])

# ---------- Kamera ----------
js = []
AY = 880
def cam(cx, cy, Z): return f"translate({540 - Z * cx:.1f} {AY - Z * cy:.1f}) scale({Z})"
ALLE = cam(540, 780, 1.15)
START = cam(540, 790, 1.25)
cur = START
def go(t, tr, d=0.8):
    global cur
    js.append(f'tl.fromTo("#cam", {{ attr: {{ transform: "{cur}" }} }}, {{ attr: {{ transform: "{tr}" }}, duration: {d}, ease: "power2.inOut", immediateRender: false }}, {F(t)});'); cur = tr
def focus(key, Z=2.0, dy=0):
    cx, cy = C[key]; cx = max(540 / Z, min(1080 - 540 / Z, cx)); return cam(cx, cy + dy, Z)
def tag_pop(k, t): js.append(f'tl.fromTo("#t{k}", {{ y: -26 }}, {{ y: 0, duration: .5, ease: "bounce.out" }}, {F(t)});')
def bounce(k, t): js.append(f'tl.fromTo("#h{k}", {{ y: 0 }}, {{ keyframes: [{{ y: -18, duration: .15 }}, {{ y: 0, duration: .35, ease: "bounce.out" }}] }}, {F(t)});')
js.append(f'tl.fromTo("#cam", {{ attr: {{ transform: "{START}" }} }}, {{ attr: {{ transform: "{START}" }}, duration: .01 }}, 0);')
go(0.0, ALLE, max(1.2, st("s2") - .4))
SHOTS = [("FINNY", "s2", "Finny", 2.0), ("FABERTRANS", "s2", "Fabertrans", 2.0), ("LÅKI", "s3", "Loki", 1.8), ("LIAM", "s3", "Liam", 1.9), ("LAITH", "s4", "Leis", 1.8)]
for name, sc, word, Z in SHOTS:
    k = idx[name]; t = w(sc, word)
    go(t - .5, focus(k, Z, -10), .6); tag_pop(k, t - .05); bounce(k, t)
js.append(f'tl.fromTo(".plane", {{ x: 0 }}, {{ x: 60, duration: 2.2, ease: "power1.inOut" }}, {F(w("s2", "Finny"))});')
js.append(f'tl.fromTo(".heli", {{ y: 0 }}, {{ y: -14, duration: .5, repeat: 9, yoyo: true, ease: "sine.inOut" }}, {F(w("s3", "Liam") - .5)});')
js.append(f'tl.fromTo(".blau", {{ opacity: 1 }}, {{ opacity: .15, duration: .2, repeat: 11, yoyo: true }}, {F(w("s4", "Leis"))});')
# s4b: Übersicht über alle 5 Häuser
t_ov = st("s4b")
go(t_ov - .1, ALLE, 1.0)
for j, k in enumerate(range(len(H))): bounce(k, w("s4b", "Häuser") + j * .12); tag_pop(k, w("s4b", "Häuser") + j * .12)
t_hier = w("s5", "hier?")
go(t_hier - .55, focus("bp", 1.7, -30), .9)
js.append(f'tl.fromTo("#bp .plot", {{ scale: 1, transformOrigin: "50% 100%" }}, {{ keyframes: [{{ scale: 1.12, duration: .18 }}, {{ scale: 1, duration: .4, ease: "bounce.out" }}] }}, {F(w("s5", "Bauplatz,"))});')
go(st("s6") + .1, focus("bp", 1.85, -95), 1.0)
js.append(f'tl.fromTo("#bp .plot", {{ scale: 1, transformOrigin: "50% 100%" }}, {{ scale: 1.06, duration: .45, repeat: {int((END - st("s6")) / .45)}, yoyo: true, ease: "sine.inOut" }}, {F(st("s6") + .1)});')

# ---------- UI ----------
def ui(id_, t0, t1, inner, style): return f'    <div id="{id_}" class="ui clip" data-start="{F(t0)}" data-duration="{F(t1 - t0)}" style="{style}">{inner}</div>\n'
def chip(id_, txt, bg="#fff", fg="#1d3557", size=44, extra=""):
    return f'<div id="{id_}" style="display:inline-block;background:{bg};color:{fg};font:900 {size}px Inter,sans-serif;padding:12px 28px;border-radius:16px;box-shadow:0 10px 30px rgba(0,0,0,.25);{extra}">{txt}</div>'
html = ui("ttl", 0, END, f'<div style="display:inline-block;background:rgba(255,255,255,.94);border-radius:24px;padding:12px 34px;text-align:center"><div style="font:900 56px Inter,sans-serif;color:#1d3557">🏙️ UNSERE YOUTUBE-STADT</div>'
          f'<div style="font:800 32px Inter,sans-serif;color:#c96f53">TAG {TAG} · HÄUSER: {len(H)} · DEINS FEHLT NOCH!</div></div>', "left:0;right:0;top:70px;text-align:center")
# Hook ab 0,0 s voll sichtbar (kein Einblenden)
html += ui("hook", 0, w("s2", "Finny") - .55, chip("hook-in", "🔨 DIESE STADT BAUT IHR!", "#e63946", "#fff", 62), "left:0;right:0;top:250px;text-align:center")
html += ui("hook2", w("s1", "Tag"), w("s2", "Finny") - .55, chip("hook2-in", f"TAG {TAG} 🏗️", "#1d3557", "#ffd166", 54), "left:0;right:0;top:360px;text-align:center")
js.append(f'tl.fromTo("#hook2-in", {{ scale: 1.5 }}, {{ scale: 1, duration: .3, ease: "back.out(2)" }}, {F(w("s1", "Tag"))});')
CH = [("FINNY", "✈️ FINNY: FLUGHAFEN 1 ✓"), ("FABERTRANS", "✈️ FABERTRANS: FLUGHAFEN 2 ✓"), ("LÅKI", "🏛️ LÅKI: BUNDESHAUS ✓"), ("LIAM", "⭐ LIAM: MILITÄRSTÜTZPUNKT ✓"), ("LAITH", "🏥 LAITH: KRANKENHAUS ✓")]
times = [w(sc, word) - .3 for _, sc, word, _ in SHOTS] + [t_ov]
html += ui("ov", t_ov + .1, t_hier - .45, chip("ov-in", "🏘️ 5 HÄUSER – UND ES GEHT WEITER!", "#2a9d8f", "#fff", 46), "left:0;right:0;top:250px;text-align:center")
js.append(f'tl.fromTo("#ov-in", {{ opacity: 0, scale: 1.4 }}, {{ opacity: 1, scale: 1, duration: .3, ease: "back.out(2)" }}, {F(t_ov + .1)});')
for j, (name, txt) in enumerate(CH):
    t0, t1 = times[j], times[j + 1] - .05
    html += ui(f"c{j}", t0, t1, chip(f"c{j}-in", txt, "#fff", "#1d3557", 42, "border:5px solid #2a9d8f"), "left:0;right:0;top:250px;text-align:center")
    js.append(f'tl.fromTo("#c{j}-in", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: .25, ease: "back.out(2)" }}, {F(t0)});')
html += ui("bpc", t_hier - .4, st("s6"), chip("bpc-in", "🏗️ BAUPLATZ FREI – FÜR WEN?", "#e63946", "#fff", 50), "left:0;right:0;top:250px;text-align:center")
js.append(f'tl.fromTo("#bpc-in", {{ opacity: 0, scale: 1.4 }}, {{ opacity: 1, scale: 1, duration: .3, ease: "back.out(2)" }}, {F(t_hier - .4)});')
cta = ('<div id="cta-in" style="background:#ffd166;border:6px solid #1d3557;border-radius:28px;padding:22px 26px;text-align:center;box-shadow:0 14px 40px rgba(0,0,0,.3);font:900 50px/1.18 Inter,sans-serif;color:#1d3557">'
       '💬 KOMMENTIER DEINEN NAMEN<br>+ DEIN WUNSCHHAUS<br>🔔 UND ABONNIER!<br><span id="cta-r" style="color:#c1121f;font-size:58px">MORGEN STEHT DEIN HAUS!</span></div>')
html += ui("cta", st("s6"), END, cta, "left:40px;right:40px;top:240px")
js.append(f'tl.fromTo("#cta-in", {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: .3, ease: "back.out(2)" }}, {F(st("s6"))});')
js.append(f'tl.fromTo("#cta-r", {{ scale: 1 }}, {{ keyframes: [{{ scale: 1.15, duration: .15 }}, {{ scale: 1, duration: .35, ease: "bounce.out" }}] }}, {F(w("s6", "morgen"))});')

open("compositions/welt.html", "w", encoding="utf-8").write(f'''<template>
  <style>#root {{ position: absolute; inset: 0; overflow: hidden; background: #5fb4ee; }} .ui {{ position: absolute; font-family: Inter, sans-serif; }} #cta-r {{ display: inline-block; }}</style>
  <div id="root" data-composition-id="welt" data-width="1080" data-height="1920">
    <svg class="clip" data-start="0" data-duration="{F(END)}" viewBox="0 0 1080 1920" style="position:absolute;left:0;top:0;width:1080px;height:1920px" data-layout-ignore>
      <defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5fb4ee"/><stop offset="1" stop-color="#d7efff"/></linearGradient></defs>
      <rect width="1080" height="{BAND}" fill="url(#sky)"/>
      <g id="cam" transform="{START}">{clouds}{hills}{trees}{houses}{tags}</g>
      <rect y="{BAND}" width="1080" height="{1920 - BAND}" fill="#2d3038"/><rect y="{BAND}" width="1080" height="8" fill="#ffd166"/>
    </svg>
{html}  </div>
  <script>(function () {{ const tl = gsap.timeline({{ paused: true }});
{chr(10).join("    " + j for j in js)}
    window.__timelines["welt"] = tl; }})();</script>
</template>
''')

# ---------- Untertitel (im unteren Streifen) ----------
HOT = {"DOPPELT", "HÄUSER", "TAG", "ANFANG", "BAUT", "IHR", "2", "YOUTUBE-STADT", "5", "FINNY", "FABERTRANS", "FLUGHÄFEN", "LÅKI", "BUNDESHAUS", "LIAM", "MILITÄRSTÜTZPUNKT", "PANZER", "LAITH", "KRANKENHAUS",
       "BAUPLATZ", "FREI", "WEN", "NAMEN", "WUNSCHHAUS", "ABONNIER", "HAUS"}
caps = []
for sc in V["scenes"]:
    sid = sc["id"]; words = T[sid]["words"]; k = 0
    for disp, sp in sc["groups"]:
        dw = [d for d in disp.split() if any(ch.isalnum() for ch in d)]; swn = sp.split()
        for i, d in enumerate(dw):
            j = k + int(i * len(swn) / len(dw))
            caps.append((round(T[sid]["start"] + words[j]["s"], 2), d))
        k += len(swn)
items, cjs = [], []
for i, (t0, d) in enumerate(caps):
    t1 = caps[i + 1][0] if i + 1 < len(caps) else END
    t1 = min(t1, t0 + 1.4); dur = max(0.2, t1 - t0 - 0.02)
    up = d.upper().strip(":.,?!–")
    col = "#ffd166" if up in HOT else "#fff"
    fs = min(100, int(1300 / max(1, len(up))))
    items.append(f'<div id="w{i}" class="wd clip" data-start="{F(t0)}" data-duration="{F(dur)}"><span id="w{i}-in" style="color:{col};font-size:{fs}px;white-space:nowrap">{d.upper().rstrip(":.,")}</span></div>')
    cjs.append(f'tl.fromTo("#w{i}-in", {{ scale: 1.25, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.09, ease: "power2.out" }}, {F(t0)});' if t0 > 0.05 else "")
open("compositions/caps.html", "w", encoding="utf-8").write(f'''<template>
  <style>#root {{ position: absolute; inset: 0; }} .wd {{ position: absolute; left: 0; right: 0; top: {BAND + 42}px; text-align: center; }}
    .wd span {{ display: inline-block; font: 900 100px/1 Inter, sans-serif; -webkit-text-stroke: 14px #000; paint-order: stroke fill; text-shadow: 0 8px 20px rgba(0,0,0,.45); }}</style>
  <div id="root" data-composition-id="caps" data-width="1080" data-height="1920">{"".join(items)}</div>
  <script>(function () {{ const tl = gsap.timeline({{ paused: true }}); {" ".join(cjs)} window.__timelines["caps"] = tl; }})();</script>
</template>
''')

# ---------- Globi (stumm, klein im Streifen) ----------
GEST = [(0.05, 1.3, "both"), (w("s2", "Finny") - .1, 1.2, "point"), (w("s3", "Panzer!") - .2, 1.2, "shock"), (w("s4", "Leben") - .1, 1.2, "wave"), (w("s2b", "Doppelt") - .1, 1.2, "both"), (w("s4b", "Häuser") - .1, 1.4, "both"),
        (t_hier - .1, 1.3, "shrug"), (w("s5", "wen?") - .1, 1.6, "think"), (st("s6") + .1, 1.4, "point"), (w("s6", "morgen") - .1, 2.0, "both")]
gh = globi.build({}, END, GEST, left=26, top=BAND + 200)
gh = gh.replace("width: 340px; height: 464px;", "width: 340px; height: 464px; transform: scale(.5); transform-origin: 0 0;")
open("compositions/globi.html", "w", encoding="utf-8").write(gh)

# ---------- Musik + Effekte ----------
P = round(st("s6") - next(x for x in V["scenes"] if x["id"] == "s5")["tail"] + .1, 2); FIN = st("s6")
subprocess.run([sys.executable, "tools/musik.py", str(END), str(P), str(FIN), "104"], check=True)
FX = [("whoosh", w(sc, word) - .5, .3) for _, sc, word, _ in SHOTS] + [("pop", w(sc, word), .35) for _, sc, word, _ in SHOTS]
FX += [("hit", 0.0, .35), ("whoosh", t_ov - .1, .3), ("blips", w("s4b", "Häuser"), .3), ("whoosh", t_hier - .55, .35), ("pop", w("s5", "Bauplatz,"), .4), ("chime", st("s6") + .05, .35)]
D = {"pop": .12, "whoosh": .9, "chime": 1.4, "blips": 1.3, "riser": 2.5, "hit": 1.6}
Hh = lambda id_, dur, ti: f'      <div id="{id_}" data-composition-id="{id_}" data-composition-src="compositions/{id_}.html" data-start="0" data-duration="{F(dur)}" data-track-index="{ti}" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index:{ti}"></div>'
lines = [Hh("welt", END, 2), Hh("caps", END, 3), Hh("globi", END, 5)]
for k in T:
    d = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"assets/vo/{k}.mp3"]))
    lines.append(f'      <audio id="vo-{k}" class="clip" data-start="{T[k]["start"] + T[k]["lead"]:.2f}" data-duration="{d:.2f}" data-track-index="4" data-volume="1" src="assets/vo/{k}.mp3"></audio>')
lines.append(f'      <audio id="mus" class="clip" data-start="0" data-duration="{F(END)}" data-track-index="10" data-volume="0.3" src="assets/musik.wav"></audio>')
for j, (nm, at, vol) in enumerate(FX):
    lines.append(f'      <audio id="fx-{j}" class="clip" data-start="{F(max(0, at))}" data-duration="{F(min(D[nm], END - at))}" data-volume="{vol}" data-track-index="{20 + j}" src="assets/sfx2/{nm}.mp3"></audio>')
open("index.html", "w", encoding="utf-8").write(f'''<!doctype html>
<html lang="de" data-resolution="portrait">
  <head><meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" /><script src="assets/gsap.min.js"></script>
    <style>* {{ margin: 0; padding: 0; box-sizing: border-box; }} html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #5fb4ee; }} #root {{ width: 100%; height: 100%; }}</style></head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{F(END)}" data-width="1080" data-height="1920">
{chr(10).join(lines)}
    </div>
    <script>window.__timelines = window.__timelines || {{}}; window.__timelines["main"] = gsap.timeline({{ paused: true }});</script>
  </body>
</html>
''')
print("Tag", TAG, "Häuser", len(H), "Ende", END, "Pause", P, "Finale", FIN)
