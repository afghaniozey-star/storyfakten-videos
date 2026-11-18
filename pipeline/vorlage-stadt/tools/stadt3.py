"""Unsere Stadt (Hauptaccount) – Tag 3: neues Viertel rechts neben dem alten.
Aufruf: python3 tools/stadt3.py 3"""
import json, subprocess, sys
sys.path.insert(0, "tools"); import globi_strich as globi

TAG = int(sys.argv[1]) if len(sys.argv) > 1 else 3
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

ROWS = {0: (1010, .80), 1: (800, .68), 2: (615, .57)}
WALLS = ["#f4ede1", "#fde2b8", "#d8eef0", "#f6d6d6", "#e2f0d9", "#ece4f7", "#fff1c1"]
ROOFS = ["#e63946", "#2a9d8f", "#f4a261", "#457b9d", "#6d597a", "#e9c46a", "#264653"]
def pos(h):
    gy, sc = ROWS[h["reihe"]]
    return h.get("viertel", 0) * 1080 + 1080 / 7 * (h["platz"] + .5), gy, sc
def emo(e, x, y, size): return f'<text x="{x:.0f}" y="{y:.0f}" text-anchor="middle" style="font:{size:.0f}px Noto Color Emoji">{e}</text>'
def car(x, y, s, col, plate="", low=False):
    pl = f'<rect x="-22" y="2" width="44" height="14" rx="2" fill="#fff" stroke="#111" stroke-width="1.5"/><text x="0" y="13" text-anchor="middle" style="font:900 10px Inter,sans-serif;fill:#111">{plate}</text>' if plate else ""
    body = ('<path d="M-62 0 Q-62 -12 -44 -14 L-20 -18 Q-6 -30 16 -30 L30 -28 Q50 -22 62 -12 Q68 -6 64 0 Z"' if low else
            '<path d="M-60 0 Q-60 -18 -44 -20 L-26 -22 Q-14 -40 8 -40 L26 -40 Q42 -38 52 -22 L60 -18 Q66 -14 64 0 Z"')
    return (f'<g transform="translate({x:.1f} {y:.1f}) scale({s:.2f})">{body} fill="{col}" stroke="#111" stroke-width="3"/>'
            f'<circle cx="-36" cy="2" r="11" fill="#222"/><circle cx="38" cy="2" r="11" fill="#222"/><circle cx="-36" cy="2" r="4" fill="#ccc"/><circle cx="38" cy="2" r="4" fill="#ccc"/>{pl}</g>')
def sign(cx, y, sc, text, bg="#fff", fg="#111", wd=None):
    wd = wd or (30 + 15 * len(text)) * sc
    return (f'<rect x="{cx - wd / 2:.1f}" y="{y:.1f}" width="{wd:.1f}" height="{30 * sc:.1f}" rx="{6 * sc:.1f}" fill="{bg}" stroke="#111" stroke-width="2"/>'
            f'<text x="{cx:.1f}" y="{y + 22 * sc:.1f}" text-anchor="middle" style="font:900 {int(19 * sc)}px Inter,sans-serif;fill:{fg}">{text}</text>')

def haus(k, h):
    cx, gy, sc = pos(h); art = h.get("art", "")
    bw, bh, rh = 150 * sc, 112 * sc, 70 * sc
    x, y = cx - bw / 2, gy - bh
    sw = 4 * sc + 1
    o = ""
    # --- Großprojekte ohne normales Haus ---
    if art == "stadion":
        rx, ry, cy = 215 * sc, 92 * sc, gy - 70 * sc
        o += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#adb5bd" stroke="#111" stroke-width="{sw}"/>'
        o += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx * .92}" ry="{ry * .86}" fill="#e63946"/>'
        o += f'<ellipse cx="{cx}" cy="{cy + 6 * sc}" rx="{rx * .7}" ry="{ry * .58}" fill="#4caf50" stroke="#fff" stroke-width="3"/>'
        o += f'<path d="M{cx} {cy + 6 * sc - ry * .58} V{cy + 6 * sc + ry * .58}" stroke="#fff" stroke-width="3"/><circle cx="{cx}" cy="{cy + 6 * sc}" r="{14 * sc}" fill="none" stroke="#fff" stroke-width="3"/>'
        for fx in (-1, 1):
            lx = cx + fx * rx * .95
            o += f'<path d="M{lx} {cy} V{cy - 120 * sc}" stroke="#555" stroke-width="{5 * sc}"/><rect x="{lx - 16 * sc}" y="{cy - 136 * sc}" width="{32 * sc}" height="{18 * sc}" fill="#fff8b0" stroke="#111" stroke-width="2"/>'
        o += sign(cx, cy - ry - 34 * sc, sc * 1.4, "🏟️ STADION", "#fff", "#c1121f")
        return f'<g id="h{k}">{o}</g>', cy - ry - 34 * sc, (cx, cy)
    if art == "f1":
        rx, ry, cy = 190 * sc, 72 * sc, gy - 60 * sc
        o += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx + 22 * sc}" ry="{ry + 18 * sc}" fill="#7cc46b"/>'
        o += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="#e63946" stroke-width="{30 * sc}"/>'
        o += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="#fff" stroke-width="{30 * sc}" stroke-dasharray="{14 * sc} {14 * sc}"/>'
        o += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="#3a3f46" stroke-width="{22 * sc}"/>'
        o += f'<path d="M{cx - 6 * sc} {cy + ry - 11 * sc} h{12 * sc} v{22 * sc} h{-12 * sc} Z" fill="#fff"/>'
        o += f'<g class="f1car">{emo("🏎️", cx - rx + 10 * sc, cy + 16 * sc, 60 * sc)}</g>' + emo("🏁", cx + 40 * sc, cy + 20 * sc, 56 * sc)
        o += sign(cx, cy - ry - 40 * sc, sc * 1.4, "🏎️ FORMEL 1", "#111", "#fff")
        return f'<g id="h{k}">{o}</g>', cy - ry - 40 * sc, (cx, cy)
    if art == "bolz":
        fw, fh = 170 * sc, 70 * sc
        o += f'<rect x="{cx - fw / 2}" y="{gy - fh}" width="{fw}" height="{fh}" fill="#4caf50" stroke="#fff" stroke-width="4"/>'
        o += f'<path d="M{cx} {gy - fh} V{gy}" stroke="#fff" stroke-width="3"/><path d="M{cx - fw / 2 + 4} {gy - fh * .7} h{18 * sc} v{fh * .4} h{-18 * sc}" stroke="#fff" stroke-width="3" fill="none"/>'
        o += "".join(f'<path d="M{cx - fw / 2 + i * fw / 10} {gy - fh - 40 * sc} V{gy - fh}" stroke="#9aa3ad" stroke-width="2"/>' for i in range(11))
        o += f'<path d="M{cx - fw / 2} {gy - fh - 40 * sc} H{cx + fw / 2}" stroke="#9aa3ad" stroke-width="3"/>' + emo("⚽", cx + 30 * sc, gy - 20 * sc, 34 * sc)
        return f'<g id="h{k}">{o}</g>', gy - fh - 40 * sc, (cx, gy - fh / 2)
    if art == "hangar":
        hw, hh = 180 * sc, 110 * sc
        o += f'<path d="M{cx - hw / 2} {gy} V{gy - hh * .4} Q{cx - hw / 2} {gy - hh} {cx} {gy - hh} Q{cx + hw / 2} {gy - hh} {cx + hw / 2} {gy - hh * .4} V{gy} Z" fill="#9aa3ad" stroke="#111" stroke-width="{sw}"/>'
        o += "".join(f'<path d="M{cx - hw / 2 + i * hw / 6} {gy - hh * .25} V{gy}" stroke="#6c757d" stroke-width="2"/>' for i in range(1, 6))
        o += f'<rect x="{cx - hw * .3}" y="{gy - hh * .55}" width="{hw * .6}" height="{hh * .55}" fill="#495057" stroke="#111" stroke-width="2"/>'
        o += emo("✈️", cx + 10 * sc, gy - 18 * sc, 60 * sc) + sign(cx, gy - hh - 36 * sc, sc * 1.2, "HANGAR", "#fff", "#111")
        return f'<g id="h{k}">{o}</g>', gy - hh - 36 * sc, (cx, gy - hh / 2)
    # --- normale Gebäude ---
    wall = h.get("wand") or (WALLS[k % 7] if k else "#fff7ec"); roof = h.get("dach") or (ROOFS[k % 7] if k else "#e63946")
    flat = art in ("werkstatt", "feuerwehr", "kiosk", "laden", "polizei", "autohaus")
    if art == "feuerwehr": wall, roof = "#d62828", "#7a1010"
    if art == "werkstatt": wall, roof = "#adb5bd", "#495057"
    if art == "polizei": wall, roof = "#e9f1ff", "#1d4ed8"
    if art == "autohaus": wall, roof = "#dfe7ec", "#343a40"
    if art in ("laden", "autohaus"): bw *= 1.08; x = cx - bw / 2
    o += f'<rect x="{x}" y="{y}" width="{bw}" height="{bh}" fill="{wall}" stroke="#111" stroke-width="{sw}"/>'
    if flat:
        o += f'<rect x="{x - 6 * sc}" y="{y - 16 * sc}" width="{bw + 12 * sc}" height="{18 * sc}" fill="{roof}" stroke="#111" stroke-width="{3 * sc + 1}"/>'
        top = y - 16 * sc
    else:
        o += f'<path d="M{x - 12 * sc} {y} L{cx} {y - rh} L{x + bw + 12 * sc} {y} Z" fill="{roof}" stroke="#111" stroke-width="{sw}" stroke-linejoin="round"/>'
        top = y - rh
    if art in ("werkstatt", "feuerwehr"):
        gw = bw * .62
        o += f'<rect x="{cx - gw / 2}" y="{gy - bh * .62}" width="{gw}" height="{bh * .62}" fill="#e9ecef" stroke="#111" stroke-width="{3 * sc + 1}"/>'
        o += "".join(f'<path d="M{cx - gw / 2} {gy - bh * .62 + k2 * bh * .12} h{gw}" stroke="#868e96" stroke-width="{2 * sc + .5}"/>' for k2 in range(1, 5))
        o += sign(cx, y + 6 * sc, sc, "🔧 WERKSTATT" if art == "werkstatt" else "🚒 112", wd=bw - 16 * sc)
    elif art == "autohaus":
        o += f'<rect x="{x + 8 * sc}" y="{y + 40 * sc}" width="{bw - 16 * sc}" height="{bh - 46 * sc}" fill="#bfe6ff" stroke="#111" stroke-width="2"/>'
        o += sign(cx, y + 6 * sc, sc, h.get("schild", "AUTOHAUS"), "#111", "#fff", bw - 16 * sc)
    elif art == "laden":
        col = h.get("farbe", "#e63946")
        o += "".join(f'<path d="M{x + k2 * bw / 6} {y + 2 * sc} h{bw / 6} l{-6 * sc} {24 * sc} h{-bw / 6 + 12 * sc} Z" fill="{[col, "#fff"][k2 % 2]}" stroke="#111" stroke-width="1.5"/>' for k2 in range(6))
        o += f'<rect x="{x + 10 * sc}" y="{y + 34 * sc}" width="{bw * .42}" height="{bh * .42}" fill="#bfe6ff" stroke="#111" stroke-width="2"/>'
        o += f'<rect x="{cx + 10 * sc}" y="{gy - 54 * sc}" width="{34 * sc}" height="{54 * sc}" fill="#6b4a32" stroke="#111" stroke-width="2"/>'
        o += emo(h.get("emoji", ""), x + 10 * sc + bw * .21, y + 34 * sc + bh * .36, 40 * sc)
        big = h.get("gross", False)
        o += sign(cx, y - (60 if big else 48) * sc, sc * (1.25 if big else 1), h.get("schild", ""), h.get("schildfarbe", "#ffd60a"), "#111")
        top = y - (60 if big else 48) * sc
    elif art == "polizei":
        o += f'<rect x="{x + 14 * sc}" y="{y + 40 * sc}" width="{34 * sc}" height="{30 * sc}" fill="#bfe6ff" stroke="#111" stroke-width="2"/><rect x="{x + bw - 48 * sc}" y="{y + 40 * sc}" width="{34 * sc}" height="{30 * sc}" fill="#bfe6ff" stroke="#111" stroke-width="2"/>'
        o += f'<rect x="{cx - 17 * sc}" y="{gy - 54 * sc}" width="{34 * sc}" height="{54 * sc}" fill="#1d4ed8" stroke="#111" stroke-width="2"/>'
        o += sign(cx, y + 6 * sc, sc, "🚓 POLIZEI", "#1d4ed8", "#fff", bw - 16 * sc)
        o += f'<rect class="blau" x="{cx - 12 * sc}" y="{top - 14 * sc}" width="{24 * sc}" height="{14 * sc}" rx="{4 * sc}" fill="#3a86ff" stroke="#111" stroke-width="2"/>'
        o += car(x + bw + 22 * sc, gy - 4 * sc, sc * .85, "#ffffff", "POLIZEI")
        top -= 14 * sc
    else:
        o += f'<rect x="{cx - 17 * sc}" y="{gy - 54 * sc}" width="{34 * sc}" height="{54 * sc}" fill="#6b4a32" stroke="#111" stroke-width="{3 * sc + .5}"/>'
        o += f'<rect x="{x + 14 * sc}" y="{y + 20 * sc}" width="{34 * sc}" height="{30 * sc}" fill="#ffd166" stroke="#111" stroke-width="{3 * sc + .5}"/><rect x="{x + bw - 48 * sc}" y="{y + 20 * sc}" width="{34 * sc}" height="{30 * sc}" fill="#ffd166" stroke="#111" stroke-width="{3 * sc + .5}"/>'
    if art == "jugend":
        o += "".join(f'<path d="M{x + 6 * sc + i * 28 * sc} {gy - 10 * sc} q{8 * sc} {-22 * sc} {16 * sc} 0" stroke="{c}" stroke-width="{4 * sc}" fill="none"/>' for i, c in enumerate(["#ff006e", "#3a86ff", "#8338ec", "#06d6a0", "#ffbe0b"]))
        o += sign(cx, top - 42 * sc, sc, "🛹 JUGENDTREFF", "#111", "#ffbe0b"); top -= 42 * sc
    if art == "kiosk":
        o += "".join(f'<path d="M{x + k2 * bw / 6} {y + 2 * sc} h{bw / 6} l{-6 * sc} {26 * sc} h{-bw / 6 + 12 * sc} Z" fill="{["#e63946", "#fff"][k2 % 2]}" stroke="#111" stroke-width="1.5"/>' for k2 in range(6))
        o += sign(cx, y - 46 * sc, sc, "KIOSK", "#ffd60a"); top = y - 46 * sc
    if art == "pool":
        o += f'<rect x="{x + bw - 4 * sc}" y="{gy - 16 * sc}" width="{95 * sc}" height="{30 * sc}" rx="{12 * sc}" fill="#4cc9f0" stroke="#fff" stroke-width="{3 * sc}"/>'
    if art == "flagge":
        fx = x + bw - 8 * sc
        o += f'<path d="M{fx} {y - 10 * sc} V{y - 110 * sc}" stroke="#555" stroke-width="{4 * sc}"/><rect x="{fx}" y="{y - 110 * sc}" width="{58 * sc}" height="{40 * sc}" fill="#e41e20"/>'
        top = min(top, y - 110 * sc)
    if art in ("auto", "c63"):
        o += car(x + bw + 20 * sc, gy - 4 * sc, sc * .9, "#1d4ed8" if art == "auto" else "#111", "C63" if art == "c63" else "")
    if art == "feuerwehr":
        o += car(x - 30 * sc, gy - 4 * sc, sc * .8, "#d62828")
    if art == "autohaus":
        if h.get("super"):
            o += car(x + 10 * sc, gy - 2 * sc, sc * .85, "#e63946", low=True) + car(x + bw + 20 * sc, gy - 2 * sc, sc * .85, "#ffbe0b", low=True)
        else:
            o += car(x + 10 * sc, gy - 4 * sc, sc * .85, "#1d4ed8", "BMW") + car(x + bw + 20 * sc, gy - 4 * sc, sc * .85, "#f8f9fa", "BMW")
    return f'<g id="h{k}">{o}</g>', top, (cx, gy - bh / 2)

def tagsvg(k, h, top):
    cx, gy, sc = pos(h)
    if h.get("art") in ("stadion", "f1"): sc *= 1.3
    lw = (24 + 13 * len(h["name"])) * sc
    return (f'<g id="t{k}"><rect x="{cx - lw / 2}" y="{top - 44 * sc}" width="{lw}" height="{32 * sc}" rx="{16 * sc}" fill="#fff" stroke="#1d3557" stroke-width="2"/>'
            f'<text x="{cx}" y="{top - 22 * sc}" text-anchor="middle" style="font:900 {int(20 * sc)}px Inter,sans-serif;fill:#1d3557">{h["name"]}</text></g>')

order = sorted(range(len(H)), key=lambda k: (-H[k]["reihe"], H[k].get("viertel", 0)))
houses, tags, C = "", "", {}
for k in order:
    s_, top, c_ = haus(k, H[k]); houses += s_; tags += tagsvg(k, H[k], top); C[k] = c_
idx = {h["name"]: k for k, h in enumerate(H)}
hills = ('<path d="M0 600 Q270 540 540 580 Q820 620 1080 550 Q1350 520 1620 570 Q1900 610 2160 560 L2160 1060 L0 1060 Z" fill="#7cc46b"/>'
         '<path d="M0 830 Q300 790 560 820 Q820 850 1080 800 Q1350 780 1620 815 Q1900 845 2160 805 L2160 1060 L0 1060 Z" fill="#6ab35a"/>'
         '<path d="M0 985 Q300 965 560 980 Q820 995 1080 975 Q1350 960 1620 980 Q1900 995 2160 975 L2160 1060 L0 1060 Z" fill="#5aa24b"/>'
         '<rect x="-200" y="1055" width="2560" height="500" fill="#5aa24b"/><rect x="1076" y="560" width="8" height="500" fill="#a7adb5"/>')
clouds = "".join(f'<g opacity=".9"><ellipse cx="{x}" cy="{y}" rx="70" ry="28" fill="#fff"/><ellipse cx="{x + 50}" cy="{y - 14}" rx="50" ry="26" fill="#fff"/></g>' for x, y in [(160, 380), (820, 330), (520, 460), (1300, 360), (1900, 410)])

# ---------- Kamera ----------
js = []
def cam(cx, cy, Z): return f"translate({540 - Z * cx:.1f} {700 - Z * cy:.1f}) scale({Z})"
ALT, NEU, ALLE = cam(540, 790, 1.04), cam(1620, 790, 1.04), cam(1080, 830, .5)
cur = ALT
def go(t, tr, d=0.8):
    global cur
    js.append(f'tl.fromTo("#cam", {{ attr: {{ transform: "{cur}" }} }}, {{ attr: {{ transform: "{tr}" }}, duration: {d}, ease: "power2.inOut", immediateRender: false }}, {F(t)});'); cur = tr
def focus(name, Z=2.4, dy=-20):
    cx, cy = C[idx[name]]; cx = max(540 / Z, min(2160 - 540 / Z, cx)); return cam(cx, cy + dy, Z)
def tag_pop(k, t): js.append(f'tl.fromTo("#t{k}", {{ opacity: 0, y: 12 }}, {{ opacity: 1, y: 0, duration: .3, ease: "back.out(2.2)" }}, {F(t)});')
def bounce(k, t): js.append(f'tl.fromTo("#h{k}", {{ y: 0 }}, {{ keyframes: [{{ y: -18, duration: .15 }}, {{ y: 0, duration: .35, ease: "bounce.out" }}] }}, {F(t)});')
js.append(f'tl.fromTo("#cam", {{ attr: {{ transform: "{ALT}" }} }}, {{ attr: {{ transform: "{ALT}" }}, duration: .01 }}, 0);')
new = [k for k, h in enumerate(H) if h.get("tag") == TAG]
t_neu = w("s1", "Viertel.")
for j, k in enumerate(new):
    js.append(f'tl.fromTo("#h{k}", {{ opacity: 0, y: -80 }}, {{ opacity: 1, y: 0, duration: .45, ease: "bounce.out", immediateRender: true }}, {F(t_neu - .3 + j * .07)});')
    js.append(f'tl.set("#t{k}", {{ opacity: 0 }}, 0);')
go(w("s1", "klein.") - .2, NEU, 1.3)
SHOTS = [("PAUL & LIAS", "s2", "Stadion.", 1.9), ("DSVD", "s3", "Formel", 1.9), ("SHADOW ✈️", "s3", "Hangar,", 2.4),
         ("CARL", "s4", "Carl", 2.4), ("LEONARD", "s4", "Leonard", 2.4), ("ROGAL DORN", "s5", "Rogal", 2.4), ("LORENZ", "s5", "Lorenz", 2.4),
         ("JUSTUS", "s6", "Justus", 2.4), ("04MG", "s6", "Null", 2.4), ("LIAM59", "s6", "Liam", 2.4),
         ("EFFE", "s7", "Effe", 2.4), ("POKCOLLECT", "s7", "Pockollekt.", 2.4), ("DARKEST", "s8", "Darkest", 2.4), ("D'", "s8", "Discounter.", 2.4), ("PAUL ⚽", "s8", "Paul", 2.4)]
for name, sc, word, Z in SHOTS:
    k = idx[name]; t = w(sc, word)
    go(t - .45, focus(name, Z), .55); tag_pop(k, t - .05); bounce(k, t)
js.append(f'tl.fromTo(".blau", {{ opacity: 1 }}, {{ opacity: .2, duration: .2, repeat: 15, yoyo: true }}, {F(w("s4", "Carl"))});')
go(st("s9") - .3, ALLE, 1.4)
for k in new: js.append(f'tl.to("#t{k}", {{ opacity: 1, duration: .2 }}, {F(st("s9") + .2)});')

# ---------- UI ----------
def ui(id_, t0, t1, inner, style): return f'    <div id="{id_}" class="ui clip" data-start="{F(t0)}" data-duration="{F(t1 - t0)}" style="{style}">{inner}</div>\n'
def chip(id_, txt, bg="#fff", fg="#1d3557", size=44, extra=""):
    return f'<div id="{id_}" style="display:inline-block;background:{bg};color:{fg};font:900 {size}px Inter,sans-serif;padding:12px 28px;border-radius:16px;box-shadow:0 10px 30px rgba(0,0,0,.25);{extra}">{txt}</div>'
n_alt = len([h for h in H if h.get("tag") != TAG and h.get("art") != "hangar"])
n_neu_res = 15
total = n_alt + n_neu_res
html = ui("ttl", 0, END, f'<div style="display:inline-block;background:rgba(255,255,255,.94);border-radius:24px;padding:14px 34px;text-align:center"><div style="font:900 60px Inter,sans-serif;color:#1d3557">🏘️ UNSERE STADT</div>'
          f'<div style="font:800 32px Inter,sans-serif;color:#c96f53">TAG {TAG} · HÄUSER: <span id="cnt">{n_alt}</span> · ZIEL: 300</div></div>', "left:0;right:0;top:110px;text-align:center")
js.append(f'tl.call(() => (document.getElementById("cnt").textContent = "{n_alt}"), null, 0.01); tl.call(() => (document.getElementById("cnt").textContent = "{total}"), null, {F(t_neu + .8)});')
html += ui("vt", w("s1", "Viertel.") - .2, st("s2") - .2, chip("vt-in", "🏗️ NEUES VIERTEL!", "#e63946", "#fff", 54), "left:0;right:0;top:300px;text-align:center")
js.append(f'tl.fromTo("#vt-in", {{ opacity: 0, scale: 1.5 }}, {{ opacity: 1, scale: 1, duration: .3, ease: "back.out(2)" }}, {F(w("s1", "Viertel.") - .2)});')
WISH = [("s2", "🏟️ WUNSCH: STADION ✓"), ("s3", "🏎️ F1-STRECKE + ✈️ HANGAR ✓"), ("s4", "🚓 POLIZEI + 🛹 JUGENDTREFF ✓"), ("s5", "🏎️ SUPERSPORT vs. BMW"),
        ("s6", "🍝 RESTAURANT · 🍕 PIZZERIA · 🍦 EIS ✓"), ("s7", "🥙 DER DÖNER-KRIEG"), ("s8", "🛒 SUPERMARKT · DISCOUNTER · ⚽ ✓")]
for j, (sc, txt) in enumerate(WISH):
    t0, t1 = st(sc) + .2, st(sc) + T[sc]["slot"] - .15
    html += ui(f"w{j}", t0, t1, chip(f"w{j}-in", txt, "#fff", "#1d3557", 38, "border:5px solid #2a9d8f"), "left:0;right:0;top:300px;text-align:center")
    js.append(f'tl.fromTo("#w{j}-in", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: .3, ease: "back.out(2)" }}, {F(t0)});')
pct = total / 300 * 100
html += ui("ch", st("s9"), st("s10") - .1, f'<div id="ch-in" style="background:rgba(20,22,45,.9);border-radius:24px;padding:22px 50px 26px"><div style="font:900 42px Inter,sans-serif;color:#ffd166;text-align:center;margin-bottom:18px">🏆 {total} / 300 · DANN SIND WIR GRÖSSER ALS ARNIS</div>'
           f'<div style="height:22px;border-radius:11px;background:#3b4d72;overflow:hidden"><div id="ch-b" style="width:{pct:.1f}%;height:100%;background:#2cf0a2;transform-origin:0 50%"></div></div></div>', "left:30px;right:30px;top:290px")
js.append(f'tl.fromTo("#ch-in", {{ opacity: 0, y: -30 }}, {{ opacity: 1, y: 0, duration: .35 }}, {F(st("s9"))}); tl.fromTo("#ch-b", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 1 }}, {F(st("s9") + .3)});')
html += ui("cta", st("s10"), END, chip("cta-in", "➕ FOLGEN + 💬 DEIN WUNSCHHAUS", "#ffd166", "#1d3557", 44), "left:0;right:0;top:300px;text-align:center")
js.append(f'tl.fromTo("#cta-in", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: .3, ease: "back.out(2)" }}, {F(st("s10"))});')
html += ui("mor", w("s10", "Morgen") - .2, END, chip("mor-in", f"🔨 MORGEN: TAG {TAG + 1}", "#1d3557", "#fff", 40), "left:0;right:0;top:420px;text-align:center")
js.append(f'tl.fromTo("#mor-in", {{ opacity: 0, scale: 1.4 }}, {{ opacity: 1, scale: 1, duration: .3, ease: "back.out(2)" }}, {F(w("s10", "Morgen") - .2)});')

open("compositions/welt.html", "w", encoding="utf-8").write(f'''<template>
  <style>#root {{ position: absolute; inset: 0; overflow: hidden; background: #5fb4ee; }} .ui {{ position: absolute; font-family: Inter, sans-serif; }}</style>
  <div id="root" data-composition-id="welt" data-width="1080" data-height="1920">
    <svg class="clip" data-start="0" data-duration="{F(END)}" viewBox="0 0 1080 1920" style="position:absolute;left:0;top:0;width:1080px;height:1920px" data-layout-ignore>
      <defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5fb4ee"/><stop offset="1" stop-color="#d7efff"/></linearGradient></defs>
      <rect width="1080" height="1100" fill="url(#sky)"/>
      <g id="cam" transform="{ALT}">{clouds}{hills}{houses}{tags}</g>
      <rect y="1060" width="1080" height="50" fill="#9aa0a8"/><rect y="1110" width="1080" height="810" fill="#2d3038"/>
    </svg>
{html}  </div>
  <script>(function () {{ const tl = gsap.timeline({{ paused: true }});
{chr(10).join("    " + j for j in js)}
    window.__timelines["welt"] = tl; }})();</script>
</template>
''')

# ---------- Untertitel ----------
HOT = {"21", "KLEIN", "VIERTEL", "PAUL", "LIAS", "STADION", "FORMEL-1-STRECKE", "DSVD", "SHADOW", "HANGAR", "FLUGZEUG", "CARL", "POLIZEIPRÄSIDIUM", "LEONARD", "JUGENDTREFF",
       "ROGAL", "DORN", "SUPERSPORTWAGEN", "LORENZ", "BMW", "JUSTUS", "RESTAURANT", "04MG", "PIZZERIA", "LIAM", "EISDIELE", "EFFE", "EFES-KEBAB-SCHILD", "POKCOLLECT", "DÖNER-KRIEG",
       "DARKEST", "SUPERMARKT", "D'", "DISCOUNTER", "BOLZPLATZ", "36", "264", "ARNIS", "FOLG", "WUNSCHHAUS"}
caps = []
for sc in V["scenes"]:
    sid = sc["id"]; words = T[sid]["words"]; k = 0
    for disp, sp in sc["groups"]:
        dw, swn = disp.split(), sp.split()
        for i, d in enumerate(dw):
            if not any(ch.isalnum() for ch in d): continue
            j = k + int(i * len(swn) / len(dw))
            caps.append((round(T[sid]["start"] + words[j]["s"], 2), d))
        k += len(swn)
items, cjs = [], []
for i, (t0, d) in enumerate(caps):
    t1 = caps[i + 1][0] if i + 1 < len(caps) else END
    t1 = min(t1, t0 + 1.4); dur = max(0.2, t1 - t0 - 0.02)
    up = d.upper().strip(":.,?!–")
    col = "#ffd166" if up in HOT else "#fff"
    fs = min(104, int(1650 / max(1, len(up))))
    items.append(f'<div id="w{i}" class="wd clip" data-start="{F(t0)}" data-duration="{F(dur)}"><span id="w{i}-in" style="color:{col};font-size:{fs}px;white-space:nowrap">{d.upper().rstrip(":.,")}</span></div>')
    cjs.append(f'tl.fromTo("#w{i}-in", {{ scale: 1.25, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.09, ease: "power2.out" }}, {F(t0)});')
open("compositions/caps.html", "w", encoding="utf-8").write(f'''<template>
  <style>#root {{ position: absolute; inset: 0; }} .wd {{ position: absolute; left: 0; right: 0; top: 1130px; text-align: center; }}
    .wd span {{ display: inline-block; font: 900 104px/1 Inter, sans-serif; -webkit-text-stroke: 14px #000; paint-order: stroke fill; text-shadow: 0 8px 20px rgba(0,0,0,.45); }}</style>
  <div id="root" data-composition-id="caps" data-width="1080" data-height="1920">{"".join(items)}</div>
  <script>(function () {{ const tl = gsap.timeline({{ paused: true }}); {" ".join(cjs)} window.__timelines["caps"] = tl; }})();</script>
</template>
''')

GEST = [(w("s1", "klein.") - .2, 1.2, "shrug"), (w("s1", "Viertel.") - .1, 1.4, "both"), (w("s2", "größte") - .1, 1.2, "shock"), (w("s3", "Flugzeug.") - .2, 1.2, "point"),
        (w("s4", "gechillt.") - .3, 1.2, "wave"), (w("s5", "sehen,") - .2, 1.2, "think"), (w("s6", "lecker:") - .2, 1.2, "both"), (w("s7", "Krieg") - .2, 1.4, "shock"),
        (w("s8", "Bolzplatz.") - .2, 1.2, "point"), (w("s9", "Häuser!") - .2, 1.4, "both"), (w("s10", "Folg") - .1, 1.2, "point"), (w("s10", "weitergebaut.") - .2, 1.2, "wave")]
open("compositions/globi.html", "w", encoding="utf-8").write(globi.build(T, END, GEST, left=30, top=1260))

FX = [("whoosh", w("s1", "klein.") - .2, .4)] + [("pop", t_neu - .3 + j * .14, .25) for j in range(8)] + [("hit", t_neu, .5)]
for name, sc, word, Z in SHOTS: FX.append(("pop", w(sc, word), .4))
for sc in ("s2", "s3", "s4", "s5", "s6", "s7", "s8"): FX.append(("whoosh", st(sc) - .45, .25))
FX += [("hit", w("s7", "Krieg"), .5), ("riser", st("s9") - 1.6, .25), ("hit", st("s9") + .05, .5), ("chime", st("s10") + .05, .35)]
D = {"pop": .12, "whoosh": .9, "chime": 1.4, "blips": 1.3, "riser": 2.5, "hit": 1.6}
Hh = lambda id_, dur, ti: f'      <div id="{id_}" data-composition-id="{id_}" data-composition-src="compositions/{id_}.html" data-start="0" data-duration="{F(dur)}" data-track-index="{ti}" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index:{ti}"></div>'
lines = [Hh("welt", END, 2), Hh("caps", END, 3), Hh("globi", END, 5)]
for k in T:
    d = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"assets/vo/{k}.mp3"]))
    lines.append(f'      <audio id="vo-{k}" class="clip" data-start="{T[k]["start"] + T[k]["lead"]:.2f}" data-duration="{d:.2f}" data-track-index="4" data-volume="1" src="assets/vo/{k}.mp3"></audio>')
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
print("Tag", TAG, "Gebäude", len(H), "Bewohner", total, "Ende", END)
