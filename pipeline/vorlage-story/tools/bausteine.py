"""Gemeinsame Bausteine für Story-Videos (aus story2.py extrahiert, 23.11.2026): Klötzchen-Figuren, Hintergründe,
Kamera (cut/cam), Einblendungen oben, Einzelwort-Untertitel, Ton (bgm über story_musik.py + SFX), Schnitt-Prüfung.
Benutzt von tools/story3.py und tools/digga1.py: `from bausteine import *`."""
import json, re, subprocess, sys
T = json.load(open("assets/vo/timing.json")); V = json.load(open("voice.json"))
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
J = []
FONT = "Inter,sans-serif"

# ---------- Figuren (Klötzchen-Look: eckiger Kopf, eckiger Körper, Schatten) ----------
E = lambda cx, cy, r=9: f'<rect x="{cx - r}" y="{cy - r}" width="{2 * r}" height="{2 * r}" rx="{r * .35:.0f}" fill="#111"/>'
WEYE = lambda cx, cy, px, py: f'<rect x="{cx - 19}" y="{cy - 19}" width="38" height="38" rx="9" fill="#fff" stroke="#111" stroke-width="4"/>{E(cx + px, cy + py, 8)}'
FACES = {
 "happy":  E(-30, -5) + E(30, -5) + '<path d="M-32 28 Q0 55 32 28" stroke="#111" stroke-width="7" fill="none" stroke-linecap="round"/>',
 "neutral": E(-30, -5) + E(30, -5) + '<path d="M-22 35 H22" stroke="#111" stroke-width="7" stroke-linecap="round"/>',
 "shock":  WEYE(-30, -8, 0, 2) + WEYE(30, -8, 0, 2) + '<rect x="-15" y="22" width="30" height="38" rx="12" fill="#5a1a1a" stroke="#111" stroke-width="4"/>',
 "panic":  WEYE(-30, -8, 0, 0) + WEYE(30, -8, 0, 0) + '<path d="M-28 30 Q0 20 28 30 L24 52 Q0 44 -24 52 Z" fill="#5a1a1a" stroke="#111" stroke-width="4"/><path d="M62 -40 q-10 20 0 28 q10 -8 0 -28" fill="#4cc9f0" stroke="#111" stroke-width="2"/>',
 "sad":    E(-30, -2, 8) + E(30, -2, 8) + '<path d="M-46 -26 L-14 -18 M46 -26 L14 -18" stroke="#111" stroke-width="6" stroke-linecap="round"/><path d="M-26 44 Q0 26 26 44" stroke="#111" stroke-width="7" fill="none" stroke-linecap="round"/><path d="M-34 12 q-6 14 0 20 q6 -6 0 -20" fill="#4cc9f0"/>',
 "laugh":  '<path d="M-42 -4 Q-30 -18 -18 -4 M18 -4 Q30 -18 42 -4" stroke="#111" stroke-width="7" fill="none" stroke-linecap="round"/><path d="M-34 20 Q0 74 34 20 Z" fill="#5a1a1a" stroke="#111" stroke-width="5"/><path d="M-28 22 H28" stroke="#fff" stroke-width="7"/>',
 "relief": '<path d="M-42 -2 Q-30 8 -18 -2 M18 -2 Q30 8 42 -2" stroke="#111" stroke-width="7" fill="none" stroke-linecap="round"/><path d="M-20 32 Q0 46 20 32" stroke="#111" stroke-width="7" fill="none" stroke-linecap="round"/>',
 "determined": E(-30, 0) + E(30, 0) + '<path d="M-48 -30 L-14 -18 M48 -30 L14 -18" stroke="#111" stroke-width="8" stroke-linecap="round"/><path d="M-20 36 H20" stroke="#111" stroke-width="8" stroke-linecap="round"/>',
 "annoyed": WEYE(-30, -4, 0, -9) + WEYE(30, -4, 0, -9) + '<path d="M-50 -14 H-10 M10 -14 H50" stroke="#111" stroke-width="8" stroke-linecap="round"/><path d="M-24 40 Q-12 32 0 40 Q12 48 24 40" stroke="#111" stroke-width="6" fill="none" stroke-linecap="round"/>',
 "disgust": '<path d="M-46 -18 L-18 -4 L-46 10 M46 -18 L18 -4 L46 10" stroke="#111" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round"/><path d="M-28 36 Q-14 26 0 36 Q14 46 28 36" stroke="#111" stroke-width="6" fill="none"/><path d="M4 40 q8 22 18 2" fill="#ff5d8f" stroke="#111" stroke-width="3"/>',
 "wink":   '<path d="M-44 -4 Q-30 -14 -16 -4" stroke="#111" stroke-width="7" fill="none" stroke-linecap="round"/>' + E(30, -5) + '<path d="M-30 26 Q0 56 34 22" stroke="#111" stroke-width="7" fill="none" stroke-linecap="round"/>',
 "hope":   E(-30, -5, 12) + E(30, -5, 12) + '<rect x="-27" y="-12" width="7" height="7" fill="#fff"/><rect x="33" y="-12" width="7" height="7" fill="#fff"/><path d="M-30 26 Q0 54 30 26" stroke="#111" stroke-width="7" fill="none" stroke-linecap="round"/>',
 "confused": WEYE(-30, -6, 0, -9) + WEYE(30, -6, 0, -9) + '<path d="M-48 -34 L-14 -40 M14 -30 L48 -24" stroke="#111" stroke-width="7" stroke-linecap="round"/><ellipse cx="6" cy="40" rx="10" ry="12" fill="#5a1a1a" stroke="#111" stroke-width="3"/>',
 "tired":  '<path d="M-46 -2 H-14 M14 -2 H46" stroke="#111" stroke-width="7" stroke-linecap="round"/><path d="M-46 -12 Q-30 -20 -14 -12 M14 -12 Q30 -20 46 -12" stroke="#111" stroke-width="4" fill="none"/><path d="M-18 44 Q0 32 18 44" stroke="#111" stroke-width="6" fill="none" stroke-linecap="round"/>',
 "grin":   '<path d="M-56 14 Q0 82 56 14 Z" fill="#fff" stroke="#111" stroke-width="4"/><path d="M-36 24 V44 M-14 24 V56 M8 24 V57 M30 24 V46" stroke="#111" stroke-width="3"/>',
 "grinwink": '<path d="M-44 -18 Q-30 -26 -16 -18" stroke="#ffd166" stroke-width="6" fill="none" stroke-linecap="round"/><rect x="18" y="-26" width="22" height="16" rx="5" fill="#ffd166"/><path d="M-60 12 Q0 90 60 12 Z" fill="#fff" stroke="#111" stroke-width="4"/><path d="M-38 22 V44 M-14 22 V58 M10 22 V59 M34 22 V46" stroke="#111" stroke-width="3"/>',
}
# Klötzchen-Haare (eckig)
HAIR = {
 "mia":  lambda c: f'<path d="M-100 -20 V-100 Q-100 -112 -88 -112 H88 Q100 -112 100 -100 V-20 L70 -70 H-40 L-70 -40 Z" fill="{c}" stroke="#111" stroke-width="4"/><rect x="-112" y="-60" width="32" height="170" rx="8" fill="{c}" stroke="#111" stroke-width="4"/><rect x="80" y="-60" width="32" height="170" rx="8" fill="{c}" stroke="#111" stroke-width="4"/>',
 "lena": lambda c: f'<path d="M-100 -10 V-100 Q-100 -112 -88 -112 H88 Q100 -112 100 -100 V-10 L80 -70 H-80 Z" fill="{c}" stroke="#111" stroke-width="4"/><rect x="-40" y="-170" width="80" height="62" rx="18" fill="{c}" stroke="#111" stroke-width="4"/>',
 "oma":  lambda c: f'<path d="M-100 -10 V-96 Q-100 -108 -88 -108 H88 Q100 -108 100 -96 V-10 L84 -64 H-84 Z" fill="{c}" stroke="#111" stroke-width="4"/><rect x="-36" y="-160" width="72" height="56" rx="26" fill="{c}" stroke="#111" stroke-width="4"/>',
 "mann": lambda c: f'<path d="M-100 -30 V-98 Q-100 -110 -88 -110 H88 Q100 -110 100 -98 V-30 L80 -72 H-80 Z" fill="{c}" stroke="#111" stroke-width="4"/>',
 "ben":  lambda c: f'<path d="M-100 -40 L-80 -140 L-50 -100 L-20 -150 L10 -100 L40 -150 L60 -100 L95 -135 L100 -40 L80 -72 H-80 Z" fill="{c}" stroke="#111" stroke-width="4"/>',
 "glatze": lambda c: f'<path d="M-100 -20 V-60 L-80 -40 V-20 Z M100 -20 V-60 L80 -40 V-20 Z" fill="{c}"/>',
 "chicken": lambda c: '<path d="M-118 120 V-110 Q-118 -128 -100 -128 H100 Q118 -128 118 -110 V120 H96 V-80 H-96 V120 Z" fill="#ffd60a" stroke="#111" stroke-width="5"/>'
            '<path d="M-40 -128 L-30 -180 L-10 -140 L5 -195 L22 -140 L40 -178 L46 -128 Z" fill="#e63946" stroke="#111" stroke-width="5"/>'
            '<path d="M-30 -96 L30 -96 L0 -60 Z" fill="#fb8500" stroke="#111" stroke-width="4"/>',
 "hood": lambda c: '<path d="M-96 -10 V-90 Q-96 -100 -86 -100 H86 Q96 -100 96 -90 V-10 Q50 -46 0 -46 Q-50 -46 -96 -10 Z" fill="#0d0d10"/>',
}
ARM = {  # rechte Seite (links gespiegelt): Pfad + Handposition
 "down":  ("M90 -250 Q150 -170 128 -96", (128, -96)),
 "up":    ("M90 -250 Q170 -330 160 -470", (160, -470)),
 "front": ("M90 -250 Q180 -240 196 -330", (196, -330)),
 "mic":   ("M90 -250 Q180 -190 74 -300", (74, -300)),
 "hip":   ("M90 -250 Q190 -200 110 -150", (110, -150)),
 "out":   ("M90 -250 Q180 -260 250 -230", (250, -230)),
}
def arms(shirt, skin, l, r):
    s = ""
    for side, k in ((-1, l), (1, r)):
        p, (hx, hy) = ARM[k]
        if side < 0:
            nums = p.replace("M", " ").replace("Q", " ").split()
            nums = [str(-int(v)) if i % 2 == 0 else v for i, v in enumerate(nums)]
            p = f"M{nums[0]} {nums[1]} Q{nums[2]} {nums[3]} {nums[4]} {nums[5]}"
        s += (f'<path d="{p}" stroke="#111" stroke-width="50" fill="none" stroke-linecap="round"/><path d="{p}" stroke="{shirt}" stroke-width="40" fill="none" stroke-linecap="round"/>'
              f'<rect x="{side * hx - 24}" y="{hy - 24}" width="48" height="48" rx="12" fill="{skin}" stroke="#111" stroke-width="4"/>')
    return s
def person(uid, hair, hcol, shirt, skin="#f2c9a5", exprs=("happy",), start="happy", extra="", head_acc="", arm=("down", "down"), arm2=None, pants="#2b2d42", behind=""):
    faces = "".join(f'<g id="{uid}-{e}" opacity="{1 if e == start else 0}">{FACES[e]}</g>' for e in exprs)
    a1 = f'<g id="{uid}-a1">{arms(shirt, skin, *arm)}</g>'
    a2 = f'<g id="{uid}-a2" opacity="0">{arms(shirt, skin, *arm2)}</g>' if arm2 else ""
    return (f'<g id="{uid}"><ellipse cx="0" cy="6" rx="120" ry="22" fill="#000" opacity=".22"/>{behind}'
            f'<rect x="-70" y="-70" width="58" height="72" rx="8" fill="{pants}" stroke="#111" stroke-width="5"/><rect x="12" y="-70" width="58" height="72" rx="8" fill="{pants}" stroke="#111" stroke-width="5"/>'
            f'<rect x="-98" y="-300" width="196" height="240" rx="22" fill="{shirt}" stroke="#111" stroke-width="5"/>'
            f'<rect x="-98" y="-300" width="196" height="240" rx="22" fill="url(#shade)"/>'
            f'{a1}{a2}{extra}'
            f'<g transform="translate(0 -400)"><rect x="-96" y="-96" width="192" height="192" rx="26" fill="#000" opacity=".18" transform="translate(8 8)"/>'
            f'<rect x="-96" y="-96" width="192" height="192" rx="26" fill="{skin}" stroke="#111" stroke-width="5"/>{HAIR[hair](hcol)}'
            f'<rect x="-70" y="16" width="26" height="18" rx="8" fill="#ff8fa3" opacity=".55"/><rect x="44" y="16" width="26" height="18" rx="8" fill="#ff8fa3" opacity=".55"/>{faces}{head_acc}</g></g>')
def badge(uid, text, col="#ffffff", fg="#111", y=-580, size=64, chars=None, vis=False, inner=""):
    wd = 60 + size * .62 * (chars or len(text))
    return (f'<g id="{uid}" opacity="{1 if vis else 0}"><g id="{uid}-in"><rect x="{-wd/2 + 6:.0f}" y="{y - size + 8:.0f}" width="{wd:.0f}" height="{size * 1.35:.0f}" rx="{size*.3:.0f}" fill="#000" opacity=".25"/>'
            f'<rect x="{-wd/2:.0f}" y="{y - size:.0f}" width="{wd:.0f}" height="{size * 1.35:.0f}" rx="{size*.3:.0f}" fill="{col}" stroke="#111" stroke-width="6"/>'
            f'<text id="{uid}-t" x="0" y="{y + size * .12:.0f}" text-anchor="middle" style="font:900 {size}px {FONT};fill:{fg}">{text}</text>{inner}</g></g>')
RED, GREEN = "#e63946", "#2dc653"
def expr(uid, frm, to, t):
    J.append(f'tl.set("#{uid}-{frm}", {{ opacity: 0 }}, {F(t)}); tl.set("#{uid}-{to}", {{ opacity: 1 }}, {F(t)});')
def armswap(uid, t):
    J.append(f'tl.set("#{uid}-a1", {{ opacity: 0 }}, {F(t)}); tl.set("#{uid}-a2", {{ opacity: 1 }}, {F(t)});')
def pop(sel, t, d=.3, origin="50% 100%"):
    J.append(f'tl.fromTo("{sel}", {{ opacity: 0, scale: .3, transformOrigin: "{origin}" }}, {{ opacity: 1, scale: 1, duration: {d}, ease: "back.out(2.4)", immediateRender: false }}, {F(t)});')
def hide(sel, t, d=.15):
    J.append(f'tl.to("{sel}", {{ opacity: 0, duration: {d} }}, {F(t)});')
def show(sel, t0, t1):
    J.append(f'tl.set("{sel}", {{ opacity: 1 }}, {F(t0)}); tl.set("{sel}", {{ opacity: 0 }}, {F(t1)});')
def _cam(x, y, z):
    ox = min(0, max(1080 - 1080 * z, 540 - z * x)); oy = min(0, max(1920 - 1920 * z, 900 - z * y))
    return ox, oy
def cam(t, x, y, z, d=1.0, ease="power2.inOut"):
    ox, oy = _cam(x, y, z)  # Bildpunkt (x,y) nach (540, 900) holen, Zoom z
    J.append(f'tl.to("#cam", {{ x: {ox:.0f}, y: {oy:.0f}, scale: {z}, duration: {d}, ease: "{ease}" }}, {F(t)});')
def cut(t, x, y, z):
    ox, oy = _cam(x, y, z)
    J.append(f'tl.set("#cam", {{ x: {ox:.0f}, y: {oy:.0f}, scale: {z} }}, {F(t)});')
def shake(t, n=9, a=16):
    J.append(f'tl.to("#shk", {{ x: "+={a}", duration: .04, yoyo: true, repeat: {n}, ease: "none" }}, {F(t)}); tl.set("#shk", {{ x: 0 }}, {F(t + .04 * (n + 1) + .01)});')
def bubble(uid, lines, x, y, wd, tail=(0, 1), size=54):
    h = 50 + len(lines) * size * 1.2
    tx, ty = tail
    txt = "".join(f'<text x="0" y="{-h/2 + 40 + (k + .8) * size * 1.2 - 14:.0f}" text-anchor="middle" style="font:900 {size}px {FONT};fill:#111">{l}</text>' for k, l in enumerate(lines))
    tp = f'<path d="M{-30 + tx * 40} {h/2 - 4:.0f} L{tx * 120} {h/2 + 90:.0f} L{30 + tx * 40} {h/2 - 4:.0f} Z" fill="#fff" stroke="#111" stroke-width="7" stroke-linejoin="round"/>'
    return (f'<g id="{uid}" opacity="0" transform="translate({x} {y})"><g id="{uid}-in">'
            f'<rect x="{-wd/2 + 10}" y="{-h/2 + 10:.0f}" width="{wd}" height="{h:.0f}" rx="40" fill="#000" opacity=".25"/>{tp}'
            f'<rect x="{-wd/2}" y="{-h/2:.0f}" width="{wd}" height="{h:.0f}" rx="40" fill="#fff" stroke="#111" stroke-width="7"/>'
            f'<path d="M{-30 + tx * 40} {h/2 - 6:.0f} L{30 + tx * 40} {h/2 - 6:.0f}" stroke="#fff" stroke-width="10"/>{txt}</g></g>')
def fig(content, x, fy, s):
    return f'<g transform="translate({x} {fy}) scale({s})">{content}</g>'
HEAD = lambda x, fy, s: (x, fy - 400 * s)
BADGE = lambda x, fy, s, y=-580: (x, fy + (y - 20) * s)

def street_bg(night=False, fence=False):
    houses = ""
    cols = [("#f4a261", "#9c4f1f"), ("#e9c46a", "#8a6d1f"), ("#a8dadc", "#457b9d"), ("#f6bd60", "#b5651d"), ("#cdb4db", "#6d597a")]
    for k, (wcol, rcol) in enumerate(cols):
        x = -40 + k * 240
        win = "#ffd166" if night else "#fff8d6"
        houses += (f'<rect x="{x}" y="640" width="220" height="460" fill="{wcol}" stroke="#111" stroke-width="5"/>'
                   f'<path d="M{x - 15} 650 L{x + 110} 520 L{x + 235} 650 Z" fill="{rcol}" stroke="#111" stroke-width="5"/>'
                   f'<rect x="{x + 30}" y="720" width="60" height="70" fill="{win if k % 2 else "#334"}" stroke="#111" stroke-width="4"/><rect x="{x + 130}" y="720" width="60" height="70" fill="{win}" stroke="#111" stroke-width="4"/>'
                   f'<rect x="{x + 80}" y="940" width="60" height="160" fill="#6b4226" stroke="#111" stroke-width="4"/>')
    sky = "#0b132b" if night else "#8ecae6"
    deco = ("".join(f'<rect x="{(k * 137) % 1060}" y="{60 + (k * 71) % 420}" width="6" height="6" fill="#fff"/>' for k in range(30)) +
            '<rect x="140" y="160" width="130" height="130" rx="20" fill="#f1faee"/>') if night else \
           ('<rect x="800" y="230" width="160" height="160" rx="30" fill="#ffd166" stroke="#111" stroke-width="5"/>'
            '<rect x="150" y="230" width="200" height="70" rx="35" fill="#fff" opacity=".9"/><rect x="200" y="200" width="110" height="70" rx="35" fill="#fff" opacity=".9"/>')
    fen = "".join(f'<rect x="{k * 60}" y="980" width="34" height="130" fill="#e9ecef" stroke="#111" stroke-width="3"/>' for k in range(19)) if fence else ""
    g = (f'<rect width="1080" height="1920" fill="{sky}"/>{deco}{houses}{fen}<rect y="1100" width="1080" height="200" fill="#c9c9c9"/><rect y="1100" width="1080" height="14" fill="#9a9a9a"/>'
         f'<rect y="1300" width="1080" height="620" fill="#6c757d"/>' + "".join(f'<rect x="{k * 220 + 40}" y="1560" width="120" height="16" fill="#fff"/>' for k in range(5)))
    if night: g += '<rect width="1080" height="1920" fill="#000814" opacity=".55"/>'
    return g
def room_bg(wall="#ffe8d6", floor="#c8a27c", win=True):
    w_ = ('<rect x="700" y="330" width="280" height="300" fill="#8ecae6" stroke="#111" stroke-width="8"/><path d="M840 330 V630 M700 480 H980" stroke="#111" stroke-width="8"/>') if win else ""
    return (f'<rect width="1080" height="1920" fill="{wall}"/>' + "".join(f'<rect x="{k * 90}" y="0" width="45" height="1200" fill="#000" opacity=".03"/>' for k in range(12)) +
            f'{w_}<rect y="1200" width="1080" height="720" fill="{floor}"/><rect y="1200" width="1080" height="16" fill="#000" opacity=".2"/>'
            + "".join(f'<rect x="0" y="{1300 + k * 140}" width="1080" height="5" fill="#000" opacity=".08"/>' for k in range(5)))

# Zubehör
BEANIE = ('<g id="{u}-bean"><path d="M-104 -40 V-110 Q-104 -150 -60 -152 H60 Q104 -150 104 -110 V-40 Z" fill="#3a86ff" stroke="#111" stroke-width="5"/>'
          '<rect x="-110" y="-62" width="220" height="40" rx="12" fill="#265fd1" stroke="#111" stroke-width="5"/>'
          '<path d="M-70 -140 V-70 M-30 -150 V-70 M10 -150 V-70 M50 -145 V-70" stroke="#1f4fb0" stroke-width="5"/><rect x="-24" y="-186" width="48" height="40" rx="16" fill="#fff" stroke="#111" stroke-width="4"/></g>')
POT = ('<g id="{u}-pot"><rect x="-130" y="-262" width="44" height="22" rx="8" fill="#495057" stroke="#111" stroke-width="4"/><rect x="86" y="-262" width="44" height="22" rx="8" fill="#495057" stroke="#111" stroke-width="4"/>'
       '<rect x="-96" y="-290" width="192" height="130" rx="10" fill="#adb5bd" stroke="#111" stroke-width="5"/><rect x="-96" y="-290" width="60" height="130" fill="#fff" opacity=".25"/>'
       '<rect x="-106" y="-300" width="212" height="24" rx="10" fill="#ced4da" stroke="#111" stroke-width="5"/></g>')
MINIBEANIE = ('<g id="mini" opacity="0"><path d="M-46 -{t} V-{t2} Q-46 -{t3} 0 -{t3} Q46 -{t3} 46 -{t2} V-{t} Z" fill="#3a86ff" stroke="#111" stroke-width="5"/>'
              '<rect x="-52" y="-{t}" width="104" height="22" rx="8" fill="#265fd1" stroke="#111" stroke-width="4"/><rect x="-12" y="-{t4}" width="24" height="22" rx="8" fill="#fff" stroke="#111" stroke-width="3"/></g>')
PIN = '<g id="{u}-pin" opacity="0"><rect x="-14" y="-6" width="28" height="44" rx="6" fill="#ff006e" stroke="#111" stroke-width="4" transform="rotate(-12)"/></g>'
DEFS = ('<defs><linearGradient id="shade" x1="0" x2="1"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".22"/></linearGradient>'
        '<radialGradient id="cone" cx=".5" cy="0" r="1"><stop offset="0" stop-color="#ffe8a3" stop-opacity=".55"/><stop offset="1" stop-color="#ffe8a3" stop-opacity="0"/></radialGradient>'
        '<radialGradient id="vig" cx=".5" cy=".45" r=".7"><stop offset=".55" stop-color="#e63946" stop-opacity="0"/><stop offset="1" stop-color="#7a0010" stop-opacity=".8"/></radialGradient></defs>')

# ---------- Zusatz 23.11.2026: Schnitt-Protokoll, Zähler, Abschluss ----------
CUTS = []
_cut0, _cam0 = cut, cam
def cut(t, x, y, z):
    CUTS.append(round(t, 2)); _cut0(t, x, y, z)
def cam(t, x, y, z, d=1.0, ease="power2.inOut"):
    CUTS.append(round(t, 2)); _cam0(t, x, y, z, d, ease)
def blink(sel, t, n=7, d=.15, lo=.15):
    J.append(f'tl.to("{sel}", {{ opacity: {lo}, duration: {d}, yoyo: true, repeat: {n}, ease: "steps(1)" }}, {F(t)}); tl.set("{sel}", {{ opacity: 1 }}, {F(t + d * (n + 1) + .01)});')
def count(el_id, t, a, b, dur=.5, fmt="de", suffix="", prefix=""):
    f = 'Math.round(o.v).toLocaleString("de-DE")' if fmt == "de" else 'Math.round(o.v)'
    J.append(f'(() => {{ const o = {{ v: {a} }}; tl.fromTo(o, {{ v: {a} }}, {{ v: {b}, duration: {dur}, ease: "power1.out", immediateRender: false, onUpdate: () => {{ document.getElementById("{el_id}").textContent = "{prefix}" + {f} + "{suffix}"; }} }}, {F(t)}); }})();')
def settext(el_id, t, txt, before):
    J.append(f'tl.call(() => {{ document.getElementById("{el_id}").textContent = {json.dumps(txt)}; }}, null, {F(t)}); tl.call(() => {{ document.getElementById("{el_id}").textContent = {json.dumps(before)}; }}, null, {F(max(0, t - .03))});')
def fly(sel, t, fr, to, d=.4, ease="power2.out"):
    J.append(f'tl.fromTo("{sel}", {json.dumps(fr)}, {{ ...{json.dumps(to)}, duration: {d}, ease: "{ease}", immediateRender: false }}, {F(t)});')
def wobble(sel, t, n, a=6, d=.25, prop="rotation", origin="50% 100%"):
    J.append(f'tl.fromTo("{sel}", {{ {prop}: {-a}, transformOrigin: "{origin}" }}, {{ {prop}: {a}, duration: {d}, yoyo: true, repeat: {n}, ease: "sine.inOut", immediateRender: false }}, {F(t)}); tl.set("{sel}", {{ {prop}: 0 }}, {F(t + d * (n + 1) + .01)});')

def shot_check(set_starts, END):
    b = sorted(set(round(x, 2) for x in list(set_starts) + CUTS if 0 <= x < END))
    gaps = [(round(b2 - b1, 2), b1) for b1, b2 in zip(b, b[1:] + [END])]
    big = [g for g in gaps if g[0] > 3.5]
    print(f"Einstellungen: {len(b)} in {END:.1f}s (Ø {END / max(1, len(b)):.2f}s), längste {max(gaps)[0]}s bei {max(gaps)[1]}s; >3,5s: {big}")

def finish(S, sets, OBEN, FX, HOT, tag_html, extra_ui="", banner=("TEIL 2?", "➕ FOLGEN"), oben_top=120, cap_top=1560, mus_vol=.16, banner_top=330):
    tEND = round(END - 1.5, 2)
    keys = []
    for k, a, b in sets:
        if k not in keys: keys.append(k)
    sets_svg = "".join(f'<g id="set{k}" opacity="0">{S[k]}</g>' for k in keys)
    for k, a, b in sets: show(f"#set{k}", a, b)
    ob = []
    for k, (t0, txt) in enumerate(OBEN):
        t1 = OBEN[k + 1][0] if k + 1 < len(OBEN) else END
        ob.append(f'<div id="ob{k}" class="ui clip" data-start="{F(t0)}" data-duration="{F(t1 - t0)}" style="left:0;right:0;top:{oben_top}px;text-align:center">'
                  f'<div id="ob{k}-in" style="display:inline-block;background:#111;color:#fff;border:6px solid #fff;border-radius:22px;padding:10px 28px;font:900 58px/1.1 Inter,sans-serif">{txt}</div></div>')
        J.append(f'tl.fromTo("#ob{k}-in", {{ scale: 1.4, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: .22, ease: "back.out(2)", immediateRender: false }}, {F(t0 + .01)});')
    end_b = (f'<div id="endc" class="ui clip" data-start="{F(tEND)}" data-duration="{F(END - tEND)}" style="left:0;right:0;top:{banner_top}px;text-align:center">'
             f'<div id="e1" style="display:inline-block;background:#e63946;border:8px solid #111;border-radius:30px;padding:14px 40px;font:900 96px/1 Inter,sans-serif;color:#fff;-webkit-text-stroke:3px #111">{banner[0]} <span style="background:#fff;color:#111;border-radius:18px;padding:4px 18px;-webkit-text-stroke:0">{banner[1]}</span></div></div>')
    J.append(f'tl.fromTo("#e1", {{ scale: 2, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: .3, ease: "back.out(2)", immediateRender: false }}, {F(tEND + .02)}); tl.to("#e1", {{ scale: 1.06, duration: .25, yoyo: true, repeat: 3, ease: "sine.inOut" }}, {F(tEND + .4)});')
    FX.append(("whoosh", tEND, .35, .6))
    open("compositions/welt.html", "w", encoding="utf-8").write(f'''<template>
  <style>#root {{ position: absolute; inset: 0; overflow: hidden; background: #000; }} .ui {{ position: absolute; font-family: Inter, sans-serif; }}</style>
  <div id="root" data-composition-id="welt" data-width="1080" data-height="1920">
    <svg class="clip" data-start="0" data-duration="{F(END)}" viewBox="0 0 1080 1920" style="position:absolute;left:0;top:0;width:1080px;height:1920px" data-layout-ignore>{DEFS}<g id="shk"><g id="cam">{sets_svg}</g></g></svg>
    {"".join(ob)}{tag_html}{extra_ui}{end_b}
  </div>
  <script>(function () {{ const tl = gsap.timeline({{ paused: true }});
{chr(10).join("    " + j for j in J)}
    window.__timelines["welt"] = tl; }})();</script>
</template>
''')
    # Einzelwort-Untertitel
    caps = []
    for sc in V["scenes"]:
        sid = sc["id"]; words = T[sid]["words"]; k = 0
        for disp, sp in sc["groups"]:
            dw, swn = disp.split(), sp.split()
            for j, d in enumerate(dw):
                if not any(ch.isalnum() for ch in d): continue
                caps.append((round(T[sid]["start"] + words[min(len(words) - 1, k + int(j * len(swn) / len(dw)))]["s"], 2), d.strip("„“")))
            k += len(swn)
    items, cj = [], []
    for j, (t0, d) in enumerate(caps):
        te = min(caps[j + 1][0] if j + 1 < len(caps) else END, t0 + 1.3, END)
        up = d.upper()
        col = "#ffd166" if (up.rstrip("!?.,:…") in HOT or any(ch.isdigit() for ch in up)) else "#fff"
        fs = min(104, int(1500 / max(1, len(up))))
        items.append(f'<div id="w{j}" class="wd clip" data-start="{F(t0)}" data-duration="{F(max(.15, te - t0 - .02))}"><span id="w{j}-in" style="color:{col};font-size:{fs}px">{up}</span></div>')
        cj.append(f'tl.fromTo("#w{j}-in", {{ scale: 1.25, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: .08 }}, {F(t0)});')
    open("compositions/caps.html", "w", encoding="utf-8").write(f'''<template>
  <style>#root {{ position: absolute; inset: 0; }} .wd {{ position: absolute; left: 0; right: 0; top: {cap_top}px; text-align: center; }}
    .wd span {{ display: inline-block; font: 900 104px/1 Inter, sans-serif; white-space: nowrap; -webkit-text-stroke: 16px #000; paint-order: stroke fill; }}</style>
  <div id="root" data-composition-id="caps" data-width="1080" data-height="1920">{"".join(items)}</div>
  <script>(function () {{ const tl = gsap.timeline({{ paused: true }}); {" ".join(cj)} window.__timelines["caps"] = tl; }})();</script>
</template>
''')
    # Ton: fester Hintergrund-Sound (assets/bgm.mp3) über story_musik.py + Soundeffekte
    subprocess.run([sys.executable, "tools/story_musik.py", F(END), "1", "2", "3"], check=True)
    Hh = lambda id_, ti: f'      <div id="{id_}" data-composition-id="{id_}" data-composition-src="compositions/{id_}.html" data-start="0" data-duration="{F(END)}" data-track-index="{ti}" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index:{ti}"></div>'
    lines = [Hh("welt", 2), Hh("caps", 3), f'      <audio id="musik" class="clip" data-start="0" data-duration="{F(END)}" data-track-index="5" data-volume="{mus_vol}" src="assets/musik.wav"></audio>']
    for k in T:
        d = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"assets/vo/{k}.mp3"]))
        lines.append(f'      <audio id="vo-{k}" class="clip" data-start="{T[k]["start"] + T[k]["lead"]:.2f}" data-duration="{d:.2f}" data-track-index="4" data-volume="1" src="assets/vo/{k}.mp3"></audio>')
    for j, (n, at, vol, dur) in enumerate(sorted(FX, key=lambda x: x[1])):
        lines.append(f'      <audio id="fx-{j}" class="clip" data-start="{F(max(0, at))}" data-duration="{F(min(dur, END - max(0, at)))}" data-volume="{vol}" data-track-index="{20 + j}" src="assets/sfx2/{n}.mp3"></audio>')
    open("index.html", "w", encoding="utf-8").write(f'''<!doctype html>
<html lang="de" data-resolution="portrait"><head><meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" /><script src="assets/gsap.min.js"></script>
<style>* {{ margin: 0; padding: 0; box-sizing: border-box; }} html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #000; }} #root {{ width: 100%; height: 100%; }}</style></head>
<body><div id="root" data-composition-id="main" data-start="0" data-duration="{F(END)}" data-width="1080" data-height="1920">
{chr(10).join(lines)}
</div><script>window.__timelines = window.__timelines || {{}}; window.__timelines["main"] = gsap.timeline({{ paused: true }});</script></body></html>
''')
    shot_check([a for _, a, _ in sets], END)
    print("Ende", END, "Banner ab", tEND, "FX", len(FX))
