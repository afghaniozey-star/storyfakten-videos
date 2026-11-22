"""STORY-FORMAT „In dieser Welt …“ – Die Zahl über dem Kopf, TEIL 2 (Mia hat die 1, 100 Lacher).
Aufruf: python3 tools/story2.py  (liest voice.json + assets/vo/timing.json, ruft tools/welt_melodie.py auf)
Bausteine: person (mit Armen/Zubehör), badge, street_bg, room_bg, cam/cut, expr, pop, bubble."""
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

MIA_EX = ("happy", "shock", "panic", "determined", "annoyed", "disgust", "sad", "hope", "tired", "confused", "relief", "laugh")
def mia(uid, start="happy", acc="", arm=("down", "down"), arm2=None, outfit="normal"):
    if outfit == "chicken":
        return person(uid, "chicken", "#6b3e26", "#ffd60a", exprs=MIA_EX, start=start, head_acc=acc, arm=arm, arm2=arm2, pants="#fb8500")
    return person(uid, "mia", "#6b3e26", "#ef476f", exprs=MIA_EX, start=start, head_acc=acc, arm=arm, arm2=arm2)
LENA_EX = ("happy", "laugh", "relief", "neutral", "determined", "shock", "panic")
lena = lambda uid, start="happy", arm=("down", "down"), arm2=None: person(uid, "lena", "#f4d35e", "#06d6a0", exprs=LENA_EX, start=start, arm=arm, arm2=arm2)

S = {}
# --- Set M: Spiegel (s1) – Mia groß, rote 1 ab 0,0 s
MX, MFY, MS = 540, 1960, 1.75
S["M"] = (room_bg("#cdeac0", "#9fb8ad", win=False) + '<rect x="0" y="0" width="1080" height="1920" fill="#fff" opacity=".0"/>'
          + "".join(f'<rect x="{k * 120}" y="0" width="118" height="118" fill="none" stroke="#a9cfa0" stroke-width="3"/>' for k in range(9)) +
          '<rect x="90" y="250" width="900" height="1640" rx="60" fill="#6b4226" stroke="#111" stroke-width="8"/>'
          '<clipPath id="mir"><rect x="125" y="285" width="830" height="1570" rx="40"/></clipPath>'
          f'<g clip-path="url(#mir)"><rect x="100" y="250" width="900" height="1660" fill="#7f9db9"/><rect x="100" y="250" width="900" height="1660" fill="#2a3a55" opacity=".35"/>'
          f'{fig(mia("m1", "shock") + badge("bM1", "1", col=RED, fg="#fff", size=110, vis=True), MX, MFY, MS)}'
          '<path d="M200 420 L320 300 M210 540 L400 350 M760 1700 L900 1560" stroke="#fff" stroke-width="16" opacity=".3" stroke-linecap="round"/></g>'
          '<rect id="redvig" width="1080" height="1920" fill="url(#vig)" opacity=".6"/>')
# --- Set R: Rückblick Lena (s1)
S["R"] = (street_bg() + '<rect width="1080" height="1920" fill="#c9a26b" opacity=".35"/>'
          f'{fig(lena("l0", "laugh") + badge("bL0", "22.000", col=GREEN, fg="#fff", size=80, vis=True), 540, 1900, 1.7)}'
          '<rect x="20" y="20" width="1040" height="1880" rx="30" fill="none" stroke="#fff" stroke-width="18" stroke-dasharray="40 24"/>')
# --- Set F: Flur, Mütze + Kochtopf (s2–s3)
FX_, FFY, FS = 540, 1880, 1.75
mini = MINIBEANIE.format(t=682, t2=700, t3=735, t4=752)
S["F"] = (room_bg("#ffd6a5", "#a47148", win=False) +
          '<rect x="80" y="500" width="250" height="700" fill="#8d5524" stroke="#111" stroke-width="7"/><rect x="270" y="840" width="26" height="26" rx="6" fill="#ffd166" stroke="#111" stroke-width="3"/>'
          '<rect x="740" y="520" width="260" height="22" fill="#6b4226" stroke="#111" stroke-width="4"/>'
          + "".join(f'<rect x="{770 + k * 80}" y="540" width="16" height="40" fill="#333"/><rect x="{752 + k * 80}" y="580" width="52" height="{180 - k * 30}" rx="10" fill="{c}" stroke="#111" stroke-width="4"/>' for k, c in enumerate(("#4361ee", "#f72585", "#80ed99"))) +
          '<rect x="380" y="1240" width="340" height="60" rx="20" fill="#e76f51" opacity=".8"/>' +
          fig(mia("m2", "determined", acc=BEANIE.format(u="m2") + POT.format(u="m2"), arm=("down", "up"))
              + badge("bM2", "1", col=RED, fg="#fff", size=80, vis=True, inner='<g id="bM2-eyes" opacity="0"><rect x="-44" y="-640" width="14" height="14" fill="#fff"/><rect id="bM2-wk" x="30" y="-640" width="14" height="14" fill="#fff"/></g>' + mini), FX_, FFY, FS))
# --- Set K: Klassenzimmer (s4)
stu_cols = [("#ffbe0b", "#3d2b1f", "4.211"), ("#8338ec", "#111", "19.003"), ("#3a86ff", "#a0522d", "27.650"), ("#fb5607", "#f4d35e", "8.840")]
studs = ""
for k, (sh, hc, num) in enumerate(stu_cols):
    x = 150 + k * 260
    studs += fig(person(f"st{k}", "lena" if k % 2 else "mann", hc, sh, skin=("#f2c9a5", "#c68642", "#8d5524", "#f2c9a5")[k], exprs=("happy", "shock"), start="happy")
                 + badge(f"bS{k}", num, size=56, vis=True), x, 1230, .72)
    studs += f'<rect x="{x - 130}" y="1150" width="260" height="90" fill="#bc6c25" stroke="#111" stroke-width="5"/>'
teacher = person("tch", "glatze", "#555", "#6c757d", exprs=("neutral", "sad"), start="neutral", arm=("up", "down"),
                 head_acc='<rect x="-62" y="-22" width="48" height="36" rx="8" fill="none" stroke="#111" stroke-width="6"/><rect x="14" y="-22" width="48" height="36" rx="8" fill="none" stroke="#111" stroke-width="6"/><path d="M-14 -6 H14" stroke="#111" stroke-width="6"/>')
S["K"] = (room_bg("#e9f5db", "#b08968", win=False) +
          '<rect x="90" y="270" width="900" height="420" rx="16" fill="#2d6a4f" stroke="#6b4226" stroke-width="18"/>'
          '<text x="540" y="430" text-anchor="middle" style="font:900 96px Comic Sans MS,Inter,sans-serif;fill:#fff;opacity:.9">TEST</text><text x="540" y="560" text-anchor="middle" style="font:700 64px Inter,sans-serif;fill:#fff;opacity:.8">1 + 1 = ?</text>'
          + studs + fig(teacher + badge("bT", "15.200", size=66, vis=True), 840, 1900, 1.55) +
          '<rect id="chalk" x="575" y="1150" width="40" height="16" rx="6" fill="#fff" stroke="#111" stroke-width="3"/>' +
          fig(mia("m3", "shock", acc=BEANIE.format(u="m3") + POT.format(u="m3")) + badge("bM3", "1", col=RED, fg="#fff", size=76, y=-880, vis=True), 290, 1900, 1.5) +
          bubble("bub4", ["„Mia, heute", "kein Test.“"], 760, 720, 440, tail=(1, 1), size=50))
# --- Set P: Pausenhof, Glückssocke (s5)
BX, BFY, BS = 820, 1900, 1.7
sock = ('<g id="sock"><path d="M-30 -60 V40 Q-30 80 10 80 H60 Q90 80 90 50 Q90 20 60 20 H30 V-60 Z" fill="#fff" stroke="#111" stroke-width="5"/><rect x="-30" y="-60" width="60" height="22" fill="#e63946"/>'
        '<rect x="20" y="40" width="22" height="22" rx="6" fill="#8d6e63" opacity=".7"/></g>')
stink = '<g id="stink">' + "".join(f'<path id="sk{k}" d="M{-40 + k * 40} -100 q-30 -40 0 -80 q30 -40 0 -80" stroke="#7bd389" stroke-width="16" fill="none" stroke-linecap="round" opacity=".85"/>' for k in range(3)) + \
        "".join(f'<g id="fly{k}"><rect x="-8" y="-8" width="16" height="16" rx="4" fill="#111"/><rect x="-14" y="-20" width="12" height="14" rx="5" fill="#cde" opacity=".8"/><rect x="2" y="-20" width="12" height="14" rx="5" fill="#cde" opacity=".8"/></g>' for k in range(3)) + '</g>'
ben = person("ben", "ben", "#ff9f1c", "#fb8500", exprs=("happy",), arm=("up", "hip"), skin="#e0ac69",
             extra=f'<g transform="translate(-200 -470) scale(1.3)">{sock}{stink}</g>')
S["P"] = (street_bg(fence=True) + fig(ben + badge("bB", "20.100", size=62, y=-600, vis=True), BX, BFY, BS) +
          fig(mia("m4", "happy", acc=BEANIE.format(u="m4") + POT.format(u="m4") + PIN.format(u="m4")) + badge("bM4", "1", col=RED, fg="#fff", size=76, y=-880, vis=True), 230, 1900, 1.4))
SOCK = (BX - 160 * BS, BFY - 470 * BS)
# --- Set O: Omas Wohnzimmer (s6–s7)
OX, OFY, OS = 330, 1900, 1.6
chair = ('<g><rect x="-160" y="-420" width="320" height="380" rx="40" fill="#9b2226" stroke="#111" stroke-width="6"/>'
         '<path d="M-200 40 Q0 110 200 40" stroke="#6b4226" stroke-width="22" fill="none" stroke-linecap="round"/><rect x="-150" y="-60" width="22" height="90" fill="#6b4226"/><rect x="128" y="-60" width="22" height="90" fill="#6b4226"/></g>')
tea = '<g transform="translate(-150 -150)"><rect x="-30" y="-40" width="60" height="56" rx="10" fill="#fff" stroke="#111" stroke-width="4"/><path d="M-10 -60 q-10 -20 0 -40 M10 -60 q-10 -20 0 -40" stroke="#ccc" stroke-width="6" fill="none"/></g>'
oma = person("oma", "oma", "#e0e0e0", "#9d4edd", exprs=("relief", "wink", "laugh"), start="relief", arm=("down", "hip"), arm2=("down", "up"), behind=chair, extra=tea,
             head_acc='<rect x="-64" y="-20" width="46" height="34" rx="16" fill="none" stroke="#555" stroke-width="5"/><rect x="18" y="-20" width="46" height="34" rx="16" fill="none" stroke="#555" stroke-width="5"/>')
icon = lambda x, col, hair: f'<g transform="translate({x} 0) scale(.42)"><rect x="-96" y="-96" width="192" height="192" rx="26" fill="#f2c9a5" stroke="#111" stroke-width="8"/>{HAIR[hair](col)}{FACES["neutral"]}</g>'
bub7 = (f'<g id="bub7" opacity="0" transform="translate(560 520)"><g id="bub7-in"><rect x="-430" y="-170" width="860" height="330" rx="44" fill="#fff" stroke="#111" stroke-width="7"/>'
        f'{icon(-260, "#f4d35e", "lena")}{icon(260, "#6b3e26", "mia")}<path d="M-150 0 H130 M100 -30 L140 0 L100 30" stroke="#111" stroke-width="12" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
        f'<text x="-260" y="120" text-anchor="middle" style="font:900 40px {FONT};fill:#111">LENA</text><text x="260" y="120" text-anchor="middle" style="font:900 40px {FONT};fill:#111">MIA</text>'
        f'<g id="one7" transform="translate(-260 -80)"><rect x="-34" y="-40" width="68" height="70" rx="14" fill="{RED}" stroke="#111" stroke-width="5"/><text x="0" y="16" text-anchor="middle" style="font:900 56px {FONT};fill:#fff">1</text></g></g></g>')
S["O"] = (room_bg("#f7e1d7", "#7f5539") + '<rect x="600" y="1240" width="460" height="80" rx="20" fill="#bc4749" opacity=".7"/>'
          '<rect x="60" y="300" width="180" height="230" fill="#fefae0" stroke="#6b4226" stroke-width="12"/><rect x="100" y="360" width="100" height="120" rx="30" fill="#a7c957"/>'
          + fig(oma + badge("bO", "900", size=72, y=-600, vis=True), OX, OFY, OS) +
          fig(mia("m5", "sad", arm=("down", "down")) + badge("bM5", "1", col=RED, fg="#fff", size=80, vis=True), 800, 1900, 1.5) + bub7)
# --- Set L: Lena springt rein (s8)
S["L"] = (street_bg() + fig(mia("m6", "panic", arm=("front", "front")) + badge("bM6", "1", col=RED, fg="#fff", size=80, vis=True), 280, 1900, 1.6) +
          fig(lena("l6", "determined", arm=("up", "up")) + badge("bL6", "22.000", col=GREEN, fg="#fff", size=64, vis=True), 800, 1900, 1.6) +
          bubble("bub8a", ["ICH HELFE DIR!"], 708, 790, 540, tail=(1, 1), size=54) +
          bubble("bub8b", ["ABER BLOSS NICHT", "BESCHÜTZEN!"], 390, 790, 600, tail=(-1, 1), size=46))
# --- Set U: Bus (s9a)
pax = ""
for k, (x, sh, sk, num) in enumerate(((150, "#8338ec", "#c68642", "9.120"), (930, "#3a86ff", "#f2c9a5", "30.400"))):
    pax += fig(person(f"px{k}", "mann" if k else "oma", "#333" if k else "#ddd", sh, skin=sk, exprs=("neutral", "laugh"), start="neutral") + badge(f"bP{k}", num, size=56, vis=True), x, 1700, 1.0)
S["U"] = ('<rect width="1080" height="1920" fill="#ffd166"/>'
          '<g id="city">' + "".join(f'<rect x="{k * 170}" y="{420 + (k * 37) % 120}" width="140" height="{420 - (k * 37) % 120}" fill="{("#6c757d", "#adb5bd", "#8d99ae")[k % 3]}"/>' for k in range(14)) + '</g>'
          '<rect x="0" y="300" width="1080" height="20" fill="#333"/><rect x="0" y="840" width="1080" height="1080" fill="#e9c46a"/><rect x="0" y="830" width="1080" height="24" fill="#333"/>'
          + "".join(f'<rect x="{k * 360 - 10}" y="300" width="20" height="540" fill="#333"/>' for k in range(4)) +
          '<rect x="0" y="380" width="1080" height="14" fill="#adb5bd"/>' + "".join(f'<rect x="{60 + k * 200}" y="394" width="10" height="60" fill="#adb5bd"/><rect x="{45 + k * 200}" y="450" width="40" height="40" rx="20" fill="none" stroke="#555" stroke-width="8"/>' for k in range(6)) +
          '<rect x="0" y="1500" width="1080" height="420" fill="#2a9d8f"/>' + pax +
          fig(mia("m7", "happy", arm=("down", "mic"), acc='') + badge("bM7", "1", col=RED, fg="#fff", size=80, vis=True), 540, 1900, 1.6) +
          f'<g transform="translate({540 + 74 * 1.6} {1900 - 300 * 1.6}) rotate(-20)"><rect x="-14" y="-10" width="28" height="90" rx="8" fill="#333"/><rect x="-26" y="-60" width="52" height="56" rx="20" fill="#888" stroke="#111" stroke-width="4"/></g>')
# --- Set H: Bäckerei, Hühnertanz (s9b)
S["H"] = ('<rect width="1080" height="1920" fill="#8ecae6"/><rect x="0" y="380" width="1080" height="900" fill="#f4a261" stroke="#111" stroke-width="6"/>'
          '<rect x="80" y="420" width="920" height="150" rx="20" fill="#fff" stroke="#111" stroke-width="6"/><text x="540" y="530" text-anchor="middle" style="font:900 100px Inter,sans-serif;fill:#9c4f1f">BÄCKEREI</text>'
          '<rect x="80" y="640" width="560" height="440" fill="#bde0fe" stroke="#111" stroke-width="7"/>' + "".join(f'<text x="{170 + k * 160}" y="{900}" text-anchor="middle" style="font:120px Noto Color Emoji">{e}</text>' for k, e in enumerate("🥐🥨🍞")) +
          '<rect x="0" y="1280" width="1080" height="640" fill="#adb5bd"/><rect x="0" y="1280" width="1080" height="16" fill="#777"/>' +
          fig(person("bak", "mann", "#3d2b1f", "#ffffff", exprs=("neutral", "laugh"), start="neutral", skin="#f2c9a5", arm=("down", "down"),
                     head_acc='<rect x="-80" y="-190" width="160" height="110" rx="40" fill="#fff" stroke="#111" stroke-width="5"/>') + badge("bK", "12.400", size=60, y=-660, vis=True), 840, 1500, 1.05) +
          '<g id="flour" opacity="0">' + "".join(f'<circle cx="{840 + dx}" cy="{1000 + dy}" r="{r}" fill="#fff" opacity=".85"/>' for dx, dy, r in ((-60, 0, 60), (40, -30, 70), (0, 40, 55), (90, 30, 45))) + '</g>' +
          fig(lena("l9", "happy", arm=("down", "front")) + badge("bL9", "22.000", col=GREEN, fg="#fff", size=60, vis=True), 190, 1880, 1.05) +
          f'<rect x="{190 + 196 * 1.05 - 30}" y="{1880 - 330 * 1.05 - 60}" width="60" height="100" rx="10" fill="#222" stroke="#111" stroke-width="4"/><circle id="rec" cx="{190 + 196 * 1.05}" cy="{1880 - 330 * 1.05 - 40}" r="10" fill="#e63946"/>' +
          f'<g id="dance">{fig(mia("m8", "laugh", arm=("out", "out"), outfit="chicken") + badge("bM8", "1", col=RED, fg="#fff", size=80, y=-640, vis=True), 520, 1900, 1.55)}</g>')
# --- Set C: Café, Gebiss in die Torte (s10)
CX, CFY, CS = 330, 1900, 1.6
cake = ('<g id="cake"><rect x="-200" y="-150" width="400" height="160" rx="20" fill="#f4acb7" stroke="#111" stroke-width="6"/><rect x="-200" y="-190" width="400" height="60" rx="30" fill="#fff" stroke="#111" stroke-width="6"/>'
        '<rect x="-20" y="-260" width="40" height="70" rx="10" fill="#e63946" stroke="#111" stroke-width="4"/></g>')
teeth = '<g id="teeth"><rect x="-56" y="-26" width="112" height="52" rx="22" fill="#ff8fa3" stroke="#111" stroke-width="5"/><rect x="-44" y="-14" width="88" height="26" rx="6" fill="#fff" stroke="#111" stroke-width="3"/><path d="M-22 -14 V12 M0 -14 V12 M22 -14 V12" stroke="#111" stroke-width="3"/></g>'
splash = '<g id="splash" opacity="0">' + "".join(f'<rect x="{-30 + dx}" y="{-30 + dy}" width="{s_}" height="{s_}" rx="{s_ / 2}" fill="#fff" stroke="#111" stroke-width="4"/>' for dx, dy, s_ in ((-150, -60, 70), (120, -90, 60), (-60, -160, 50), (60, -150, 80), (180, -20, 45), (-210, -10, 40))) + '</g>'
TAB = (790, 1500)
S["C"] = (room_bg("#fde2e4", "#b5838d", win=True) + fig(person("om2", "oma", "#e0e0e0", "#9d4edd", exprs=("relief", "laugh"), start="relief", arm=("down", "up")) + badge("bO2", "900", size=72, y=-600, vis=True), CX, CFY, CS) +
          f'<rect x="560" y="1500" width="460" height="40" rx="10" fill="#6b4226" stroke="#111" stroke-width="5"/><rect x="760" y="1540" width="60" height="380" fill="#6b4226" stroke="#111" stroke-width="5"/>'
          f'<g transform="translate({TAB[0]} {TAB[1]})">{cake}{splash}</g>'
          + fig(person("gst", "lena", "#e76f51", "#4361ee", exprs=("neutral", "laugh"), start="neutral", skin="#c68642") + badge("bG", "17.777", size=56, vis=True), 900, 1260, .8) +
          f'<g id="teethg" opacity="0" transform="translate({CX} {CFY - 365 * CS})">{teeth}</g>')
# --- Set N: Nacht, Laterne (s11–s14)
NM, NL, NS_X = 210, 550, 885
lamp = '<rect x="980" y="300" width="22" height="1000" fill="#333"/><rect x="900" y="290" width="120" height="40" rx="12" fill="#444"/><rect x="900" y="330" width="80" height="40" rx="10" fill="#ffe8a3"/><path d="M940 360 L560 1700 H1080 V560 Z" fill="url(#cone)"/>'
hoodie = person("hd", "hood", "#111", "#1b1b1f", skin="#2b2b35", exprs=("grin", "grinwink"), start="grin", arm=("down", "down"),
                behind='<path d="M-140 -400 Q-150 -560 0 -566 Q150 -560 140 -400 L130 -300 H-130 Z" transform="translate(0 0)" fill="#141418" stroke="#000" stroke-width="5"/>')
S["N"] = (street_bg(night=True) + lamp +
          '<g id="clk"><rect x="250" y="600" width="580" height="210" rx="30" fill="#000" stroke="#444" stroke-width="8"/>'
          '<text id="clkt" x="540" y="755" text-anchor="middle" style="font:900 140px Inter,monospace;fill:#ff3b30;letter-spacing:6px">23:59</text></g>'
          f'<g id="hdg" opacity="0">{fig(hoodie, NS_X, 1900, 1.5)}</g>' +
          fig(lena("l11", "panic") + badge("bL11", "22.000", col=GREEN, fg="#fff", size=60, vis=True), NL, 1900, 1.45) +
          fig(mia("m9", "tired", outfit="chicken") + badge("bM9", "1", col=RED, fg="#fff", size=84, y=-640, vis=True), NM, 1900, 1.45) +
          '<g id="burst" opacity="0">' + "".join(f'<rect x="{NM - 12 + dx}" y="{1900 - 660 * 1.45 - 12 + dy}" width="24" height="24" rx="12" fill="#ff8fa3" stroke="#fff" stroke-width="3"/>' for dx, dy in ((-120, -40), (110, -60), (-80, 70), (90, 60), (0, -120), (-150, 20), (150, 10))) + '</g>' +
          bubble("bub14", ["„Willkommen", "im Club.“"], 790, 900, 420, tail=(1, 1), size=46) +
          '<g id="confetti" opacity="0">' + "".join(f'<rect x="{(k * 97) % 1080}" y="{560 + (k * 53) % 300}" width="22" height="34" fill="{("#ffd166", "#ef476f", "#06d6a0", "#118ab2")[k % 4]}" transform="rotate({k * 37} {(k * 97) % 1080} {560 + (k * 53) % 300})"/>' for k in range(36)) + '</g>')
# --- Set Z: A oder B (s15a)
halo = '<ellipse cx="0" cy="-570" rx="120" ry="34" fill="none" stroke="#ffd166" stroke-width="22"/>'
glitch = ('<g id="glt">' + "".join(f'<rect x="{-150 + (k * 71) % 300}" y="{-700 + (k * 113) % 650}" width="{40 + (k * 31) % 90}" height="22" fill="{("#00f5d4", "#f15bb5", "#fee440")[k % 3]}" opacity=".85"/>' for k in range(14)) + '</g>')
S["Z"] = ('<rect width="540" height="1920" fill="#fff3b0"/><rect x="540" width="540" height="1920" fill="#1a1a2e"/>'
          + "".join(f'<path d="M{270 + 400 * __import__("math").cos(k * .52):.0f} {1000 + 400 * __import__("math").sin(k * .52):.0f} L270 1000" stroke="#ffd166" stroke-width="12" opacity=".4"/>' for k in range(12)) +
          f'<g id="zA">{fig(mia("m10", "relief") + halo, 270, 1950, 1.6)}</g>'
          f'<g id="zB">{fig(mia("m11", "confused") + glitch, 810, 1950, 1.6)}</g>'
          '<rect x="530" width="20" height="1920" fill="#111"/>'
          f'<g id="labA" opacity="0"><rect x="70" y="650" width="400" height="230" rx="30" fill="#ffd166" stroke="#111" stroke-width="7"/><text x="270" y="770" text-anchor="middle" style="font:900 120px {FONT};fill:#111">A</text><text x="270" y="850" text-anchor="middle" style="font:900 44px {FONT};fill:#111">UNSTERBLICH</text></g>'
          f'<g id="labB" opacity="0"><rect x="610" y="650" width="400" height="230" rx="30" fill="#f15bb5" stroke="#111" stroke-width="7"/><text x="810" y="770" text-anchor="middle" style="font:900 120px {FONT};fill:#fff">B</text><text x="810" y="850" text-anchor="middle" style="font:900 40px {FONT};fill:#fff">FEHLER IM SYSTEM</text></g>')
# --- Set W: Rückfahrt Straße mit vielen Zahlen (s15b)
crowd = ""
for k, (x, fy, s, sh, num) in enumerate(((120, 1500, .8, "#ffbe0b", "12.400"), (350, 1470, .75, "#8338ec", "900"), (960, 1500, .8, "#3a86ff", "31.000"), (720, 1460, .72, "#fb5607", "22.000"))):
    crowd += fig(person(f"cw{k}", ("mann", "oma", "lena", "lena")[k], ("#3d2b1f", "#ddd", "#111", "#f4d35e")[k], sh, exprs=("happy",)) + badge(f"bC{k}", num, size=64, vis=True, col=GREEN if num == "22.000" else "#fff", fg="#fff" if num == "22.000" else "#111"), x, fy, s)
S["W"] = (street_bg() + crowd + fig(mia("m12", "confused"), 330, 1900, 1.25) + fig(hoodie.replace('id="hd', 'id="hw').replace('"grin"', '"grin"'), 760, 1900, 1.25) +
          '')

# ---------- Zeitplan ----------
tL, tJ = w("s1", "Lena"), w("s1", "Jetzt")
tW = w("s9", "Sie")
tZ2 = w("s15", "Denn")
tEND = round(END - 1.5, 2)
sets = [("M", 0, tL - .1), ("R", tL - .1, tJ - .1), ("M", tJ - .1, st("s2")), ("F", st("s2"), st("s4")), ("K", st("s4"), st("s5")), ("P", st("s5"), st("s6")),
        ("O", st("s6"), st("s8")), ("L", st("s8"), st("s9")), ("U", st("s9"), tW - .1), ("H", tW - .1, st("s10")), ("C", st("s10"), st("s11")),
        ("N", st("s11"), st("s15")), ("Z", st("s15"), tZ2 - .1), ("W", tZ2 - .1, END)]
FX = []
J.append('tl.set("#cam", { x: 0, y: 0, scale: 1, svgOrigin: "0 0" }, 0);')
# s1: Spiegel – rote 1 groß ab 0,0
bm = BADGE(MX, MFY, MS)
cut(0, bm[0], bm[1] + 330, 1.25); cam(.05, bm[0], bm[1] + 300, 1.4, 1.6, "power1.out")
J.append('tl.fromTo("#bM1-in", { scale: 1.25, transformOrigin: "50% 50%" }, { scale: 1, duration: .35, ease: "back.out(3)", immediateRender: false }, 0);')
J.append(f'tl.to("#bM1-in", {{ scale: 1.12, duration: .3, yoyo: true, repeat: 3, ease: "sine.inOut", transformOrigin: "50% 50%" }}, .5);')
FX += [("hit", 0, .7, 1.2)]
cut(tL - .1, 540, 1000, 1.15); cam(tL, 540, 950, 1.3, 1.5)
FX += [("swoosh", tL - .15, .4, .6)]
cut(tJ - .1, 540, 1000, 1.0); cam(tJ, bm[0], bm[1] + 120, 2.0, .6, "power3.in")
FX += [("whoosh", tJ - .1, .45, .8), ("hit", w("s1", "Eins") - .05, .8, 1.3)]
J.append(f'tl.to("#bM1-in", {{ scale: 1.2, duration: .2, yoyo: true, repeat: 3, ease: "sine.inOut", transformOrigin: "50% 50%" }}, {F(w("s1", "Eins"))});')
shake(w("s1", "Eins"))
# s2: Mütze auf – die 1 hüpft drüber
hm = HEAD(FX_, FFY, FS)
cut(st("s2"), hm[0], hm[1] - 80, 1.45)
J.append('tl.set("#m2-pot", { opacity: 0 }, 0); tl.set("#m2-bean", { opacity: 0 }, 0);')
tb = w("s2", "Mütze") - .15
J.append(f'tl.fromTo("#m2-bean", {{ opacity: 1, y: -300 }}, {{ y: 0, duration: .35, ease: "bounce.out", immediateRender: false }}, {F(tb)});')
FX += [("swoosh", tb, .4, .5)]
th = w("s2", "schwebt") - .2
J.append(f'tl.to("#bM2-in", {{ y: -100, duration: .35, ease: "back.out(3)" }}, {F(th)});')
FX += [("boing", th, .45, .5)]
cut(w("s2", "Die") - .05, hm[0], hm[1] - 260, 1.25)
# s3: Kochtopf – die 1 trägt Mütze
cut(st("s3"), 540, 1000, 1.0)
tp = w("s3", "Kochtopf") - .1
J.append(f'tl.fromTo("#m2-pot", {{ opacity: 1, y: -500 }}, {{ y: 0, duration: .3, ease: "power3.in", immediateRender: false }}, {F(tp)});')
expr("m2", "determined", "annoyed", tp + .3); shake(tp + .3, 5, 10)
FX += [("klong", tp + .3, .28, 1.0)]
J.append(f'tl.to("#bM2-in", {{ y: -220, duration: .3, ease: "back.out(3)" }}, {F(tp + .4)});')
tj = w("s3", "Jetzt") - .1
bb = BADGE(FX_, FFY, FS, -580 - 220)
cam(tj, bb[0], bb[1] + 40, 1.9, .6)
tm_ = w("s3", "Mütze.") - .25
pop("#mini", tm_, .35); J.append(f'tl.set("#bM2-eyes", {{ opacity: 1 }}, {F(tm_)}); tl.to("#bM2-wk", {{ scaleY: .15, transformOrigin: "50% 50%", duration: .12, yoyo: true, repeat: 1 }}, {F(tm_ + .5)});')
FX += [("pop", tm_, .5, .3)]
# s4: Schule – alle starren, Lehrer flüstert
cut(st("s4"), 540, 1000, 1.0); cam(st("s4") + .05, 540, 1050, 1.08, 2.0, "none")
ts4 = w("s4", "totenstill.") - .1
for k in range(4): expr(f"st{k}", "happy", "shock", ts4 + k * .08)
FX += [("tick", ts4, .4, 1.0)]
tlh = w("s4", "Lehrer") - .1
ht = HEAD(840, 1900, 1.55)
cut(tlh, ht[0], 1108, 1.45)
expr("tch", "neutral", "sad", tlh)
J.append(f'tl.fromTo("#chalk", {{ x: 0, y: 0 }}, {{ x: -260, y: 700, rotation: 200, duration: .7, ease: "power2.in", immediateRender: false }}, {F(tlh + .2)});')
pop("#bub4", w("s4", "Mia,") - .1, .3)
hm3 = HEAD(290, 1900, 1.5)
cut(w("s4", "keinen") - .05, hm3[0], hm3[1] - 150, 1.5); J.append(f'tl.set("#bub4", {{ opacity: 0 }}, {F(w("s4", "keinen") - .05)});')
expr("m3", "shock", "hope", w("s4", "keinen"))
# s5: Glückssocke von unten, Gegenschuss Mia
cut(st("s5"), SOCK[0] + 40, SOCK[1] + 80, 1.45)
pop("#sock", w("s5", "Glückssocke.") - .2, .3, "50% 50%")
FX += [("pop", w("s5", "Glückssocke.") - .2, .5, .3)]
for k in range(3):
    J.append(f'tl.fromTo("#sk{k}", {{ y: 0 }}, {{ y: -40, duration: .5, yoyo: true, repeat: 9, ease: "sine.inOut", immediateRender: false }}, {F(st("s5") + k * .15)});')
    J.append(f'tl.fromTo("#fly{k}", {{ x: {-80 + k * 70}, y: {-120 - k * 40} }}, {{ x: {80 - k * 50}, y: {-200 + k * 30}, duration: .35, yoyo: true, repeat: 13, ease: "sine.inOut", immediateRender: false }}, {F(st("s5"))});')
cam(st("s5") + .2, SOCK[0] + 20, SOCK[1] + 200, 1.3, 1.4)
tu = w("s5", "Ungewaschen.") - .1
hm4 = HEAD(230, 1900, 1.4)
cut(tu, hm4[0], hm4[1] - 120, 1.6); expr("m4", "happy", "disgust", tu)
pop("#m4-pin", tu + .3, .25, "50% 50%"); FX += [("whoosh", tu - .05, .35, .5), ("pop", tu + .3, .5, .3)]
J.append(f'tl.set("#m4-pin", {{ x: 0, y: 0 }}, 0);')
# s6/s7: Oma Hilde + die Regel
ho = HEAD(OX, OFY, OS)
cut(st("s6"), ho[0] + 40, ho[1] - 60, 1.45); cam(st("s6") + .05, ho[0] + 40, ho[1] - 60, 1.7, 2.6, "none")
J.append(f'tl.fromTo("#oma", {{ rotation: -2, transformOrigin: "50% 100%" }}, {{ rotation: 2, duration: 1.1, yoyo: true, repeat: 9, ease: "sine.inOut", immediateRender: false }}, {F(st("s6"))});')
cut(w("s6", "Sie") - .05, 560, 1050, 1.0)
t7 = st("s7")
armswap("oma", t7); expr("oma", "relief", "wink", t7); FX += [("pop", t7, .4, .3)]
pop("#bub7", t7 + .05, .3, "50% 50%")
J.append(f'tl.to("#one7", {{ x: 260, y: -80, duration: .6, ease: "power2.inOut" }}, {F(w("s7", "übernimmt") - .2)});')
FX += [("whoosh", w("s7", "übernimmt") - .2, .4, .6)]
cut(t7, 560, 900, 1.05)
tlo = w("s7", "Loswerden") - .1
hide("#bub7", tlo); cut(tlo, 600, 1250, 1.2); expr("m5", "sad", "hope", w("s7", "Lachen."))
# s8: Lena springt rein
hl6 = HEAD(800, 1900, 1.6); hm6 = HEAD(280, 1900, 1.6)
t8 = st("s8")
J.append(f'tl.fromTo("#l6", {{ x: 700, y: -300 }}, {{ x: 0, y: 0, duration: .45, ease: "back.out(1.6)", immediateRender: false }}, {F(t8)});')
FX += [("boing", t8, .5, .5)]
cut(t8, 640, 1100, 1.0); cut(w("s8", "Ich") - .1, hl6[0] - 80, hl6[1] - 200, 1.45)
pop("#bub8a", w("s8", "Ich") - .1, .25, "50% 50%")
tmi = w("s8", "Mia:") - .1
hide("#bub8a", tmi, .05); cut(tmi, hm6[0] + 80, hm6[1] - 200, 1.45); pop("#bub8b", w("s8", "aber") - .1, .25, "50% 50%"); shake(tmi, 5, 8)
cut(w("s8", "beschützen!") - .05, 540, 1100, 1.05)
expr("l6", "determined", "shock", w("s8", "beschützen!"))
# s9: Bus + Hühnertanz
cut(st("s9"), 540, 1150, 1.05); cam(st("s9") + .05, 540, 1150, 1.2, 2.0)
J.append(f'tl.fromTo("#city", {{ x: 0 }}, {{ x: -900, duration: 4, ease: "none", immediateRender: false }}, {F(st("s9"))});')
J.append(f'tl.to("#shk", {{ y: "+=6", duration: .12, yoyo: true, repeat: 15, ease: "sine.inOut" }}, {F(st("s9"))}); tl.set("#shk", {{ y: 0 }}, {F(tW - .1)});')
tz = w("s9", "Zwölf")
for k in range(2): expr(f"px{k}", "neutral", "laugh", tz - .2)
FX += [("pop", tz - .1, .4, .3)]
cut(tW - .1, 520, 1150, 1.0); cam(w("s9", "Hühnerkostüm") - .1, 520, 1000, 1.35, .8)
J.append(f'tl.fromTo("#dance", {{ rotation: -6, transformOrigin: "50% 100%" }}, {{ rotation: 6, duration: .25, yoyo: true, repeat: 15, ease: "sine.inOut", immediateRender: false }}, {F(tW)});')
J.append(f'tl.fromTo("#m8", {{ y: 0 }}, {{ y: -30, duration: .125, yoyo: true, repeat: 31, ease: "sine.out", immediateRender: false }}, {F(tW)});')
J.append(f'tl.to("#rec", {{ opacity: .1, duration: .3, yoyo: true, repeat: 11, ease: "steps(1)" }}, {F(tW)});')
tbk = w("s9", "Bäckerei.") - .2
expr("bak", "neutral", "laugh", tbk); J.append(f'tl.fromTo("#flour", {{ opacity: 1, scale: .4, transformOrigin: "50% 50%" }}, {{ opacity: 0, scale: 1.6, duration: 1.0, ease: "power2.out", immediateRender: false }}, {F(tbk)});')
FX += [("pop", tbk, .45, .3)]
tf = w("s9", "Fünfzig.")
cut(tf - .1, 640, 1100, 1.0)
# s10: Gebiss in die Torte
hc = HEAD(CX, CFY, CS)
cut(st("s10"), hc[0] + 40, hc[1] - 80, 1.5); expr("om2", "relief", "laugh", st("s10") + .1)
J.append(f'tl.fromTo("#om2", {{ y: 0 }}, {{ y: -14, duration: .15, yoyo: true, repeat: 19, ease: "sine.inOut", immediateRender: false }}, {F(st("s10") + .1)});')
tg = w("s10", "Gebiss") - .1
cut(tg, 560, 1150, 1.05)
dx, dy = TAB[0] - CX, (TAB[1] - 190) - (CFY - 365 * CS)
J.append(f'tl.set("#teethg", {{ opacity: 1 }}, {F(tg)}); tl.fromTo("#teeth", {{ x: 0, y: 0, rotation: 0 }}, {{ x: {dx}, duration: 1.0, ease: "none", rotation: 540, immediateRender: false }}, {F(tg)});')
J.append(f'tl.fromTo("#teeth", {{ y: 0 }}, {{ y: -260, duration: .5, ease: "power2.out", immediateRender: false }}, {F(tg)}); tl.to("#teeth", {{ y: {dy}, duration: .5, ease: "power2.in" }}, {F(tg + .5)});')
FX += [("whoosh", tg, .4, .8)]
tt = tg + 1.0
cut(tt, TAB[0], TAB[1] - 120, 1.8); J.append(f'tl.fromTo("#splash", {{ opacity: 1, scale: .3, transformOrigin: "50% 100%" }}, {{ scale: 1.2, duration: .3, ease: "back.out(2)", immediateRender: false }}, {F(tt)});')
FX += [("splat", tt, .8, .6)]
shake(tt, 5, 12)
expr("gst", "neutral", "laugh", tt + .1)
ta = w("s10", "Achtundneunzig.") - .1
cut(max(ta, tt + .9), 640, 1150, 1.05)
# s11: 23:59, 99 Lacher – Spannung
t11 = st("s11")
cut(t11, 540, 1050, 1.0); cam(t11 + .05, 540, 1100, 1.12, 2.0, "none")
J.append(f'tl.set("#hdg", {{ opacity: 0 }}, 0); tl.to("#bM9", {{ opacity: .25, duration: .18, yoyo: true, repeat: 15, ease: "steps(1)" }}, {F(t11 + .3)}); tl.set("#bM9", {{ opacity: 1 }}, {F(st("s12") - .05)});')
J.append(f'tl.to("#clkt", {{ opacity: .35, duration: .5, yoyo: true, repeat: 5, ease: "steps(1)" }}, {F(t11)});')
te = w("s11", "Einer") - .1
cut(te, 540, 705, 1.6)
# s12: der Fremde, 100!
t12 = st("s12")
hh = HEAD(NS_X, 1900, 1.5)
cut(t12, hh[0] - 120, hh[1] + 60, 1.45)
J.append(f'tl.fromTo("#hdg", {{ opacity: 0 }}, {{ opacity: 1, duration: .6, immediateRender: false }}, {F(t12)});')
th0 = w("s12", "Hundert!") - .15
J.append(f'tl.set("#clk", {{ opacity: 0 }}, {F(t12)}); tl.set("#clk", {{ opacity: 1 }}, {F(th0)}); tl.set("#clk", {{ opacity: 0 }}, {F(st("s14"))});')
cut(th0, 540, 1050, 1.0)
J.append(f'tl.fromTo("#confetti", {{ opacity: 1, y: -200 }}, {{ y: 300, duration: 1.4, ease: "power1.in", immediateRender: false }}, {F(th0)}); tl.to("#confetti", {{ opacity: 0, duration: .3 }}, {F(th0 + 1.2)});')
expr("m9", "tired", "laugh", th0); expr("l11", "panic", "happy", th0)
FX += [("pop", th0, .6, .3), ("chime", th0 + .05, .45, 1.2)]
# s13: Mitternacht – die 1 platzt
t13 = st("s13")
J.append(f'tl.call(() => {{ document.getElementById("clkt").textContent = "00:00"; }}, null, {F(t13)}); tl.call(() => {{ document.getElementById("clkt").textContent = "23:59"; }}, null, {F(t13 - .05)});')
cut(t13, 540, 705, 1.4)
tbu = w("s13", "Mia") - .1
hm9 = HEAD(NM, 1900, 1.45)
cut(tbu, hm9[0] + 120, hm9[1] - 220, 1.5)
J.append(f'tl.to("#bM9-in", {{ scale: 1.7, opacity: 0, duration: .25, transformOrigin: "50% 50%", ease: "power2.out" }}, {F(tbu + .4)});')
J.append(f'tl.fromTo("#burst", {{ opacity: 1, scale: .4, transformOrigin: "50% 50%" }}, {{ scale: 1.5, opacity: 0, duration: .6, ease: "power2.out", immediateRender: false }}, {F(tbu + .4)});')
FX += [("pop", tbu + .4, .8, .3)]
expr("m9", "laugh", "confused", tbu + .3); expr("l11", "happy", "shock", tbu + .6)
cam(w("s13", "Über") - .1, hm9[0] + 150, hm9[1] - 160, 1.3, 1.2)
# s14: Über dem Fremden auch nicht – Willkommen im Club
t14 = st("s14")
cam(t14, hh[0] - 100, hh[1] - 150, 1.45, .9)
tgr = w("s14", "grinst:") - .1
expr("hd", "grin", "grinwink", tgr); FX += [("blips", tgr, .35, .5)]
pop("#bub14", w("s14", "Willkommen") - .1, .25, "50% 50%")
cam(w("s14", "Willkommen"), hh[0] - 60, hh[1] - 120, 1.75, 1.6, "none")
# s15: A oder B, Rückfahrt
t15 = st("s15")
cut(t15, 540, 1000, 1.0)
J.append(f'tl.to("#glt", {{ x: 12, duration: .06, yoyo: true, repeat: 40, ease: "steps(1)" }}, {F(t15)});')
pop("#labA", w("s15", "unsterblich") - .1, .3, "50% 50%"); pop("#labB", w("s15", "Fehler") - .1, .3, "50% 50%")
FX += [("chime", w("s15", "unsterblich") - .3, .15, .5), ("glitch", w("s15", "Fehler") - .3, .12, .3)]
J.append(f'tl.to("#labA", {{ scale: 1.08, duration: .2, yoyo: true, repeat: 3, transformOrigin: "50% 50%" }}, {F(w("s15", "Schreib"))}); tl.to("#labB", {{ scale: 1.08, duration: .2, yoyo: true, repeat: 3, transformOrigin: "50% 50%" }}, {F(w("s15", "Schreib") + .1)});')
cut(tZ2 - .1, 545, 1150, 1.7); cam(tZ2, 540, 1000, 1.0, 2.6, "power2.inOut")
FX += [("whoosh", tZ2 - .1, .4, .8)]
FX += [("whoosh", tEND, .4, .8), ("pop", tEND + .1, .5, .3)]

# ---------- Lach-Zähler (UI) ----------
cnt_keys = [(w("s7", "hundert") - .2, 0), (tz - .1, 12), (tf - .1, 50), (ta, 98), (w("s11", "Neunundneunzig") - .1, 99), (th0, 100)]
J.append(f'tl.fromTo("#cnt", {{ opacity: 0, scale: .3 }}, {{ opacity: 1, scale: 1, duration: .3, ease: "back.out(2.4)", immediateRender: false }}, {F(cnt_keys[0][0])});')
FX += [("pop", cnt_keys[0][0], .5, .3)]
J.append(f'tl.to("#cnt", {{ x: 300, y: -150, scale: .55, duration: .4, ease: "power2.inOut" }}, {F(t8 - .05)});')
prev = 0
for tk, v in cnt_keys[1:]:
    J.append(f'(() => {{ const o = {{ v: {prev} }}; tl.fromTo(o, {{ v: {prev} }}, {{ v: {v}, duration: .5, ease: "power1.out", immediateRender: false, onUpdate: () => {{ document.getElementById("cntv").textContent = Math.round(o.v); }} }}, {F(tk)}); }})();')
    J.append(f'tl.fromTo("#cnt-in", {{ scale: 1.35 }}, {{ scale: 1, duration: .3, ease: "back.out(3)", immediateRender: false }}, {F(tk + .4)});')
    FX.append(("blips", tk, .3, .5)); prev = v
J.append(f'tl.call(() => {{ document.getElementById("cntv").textContent = "0"; }}, null, {F(cnt_keys[0][0])});')
J.append(f'tl.to("#cnt-in", {{ backgroundColor: "#2dc653", duration: .2 }}, {F(th0 + .3)}); tl.to("#cnt", {{ opacity: 0, duration: .3 }}, {F(t13 + .2)});')

sets_svg = "".join(f'<g id="set{k}{i}" opacity="0">{S[k]}</g>' if k != "M" or i == 0 else "" for i, (k, _, _) in enumerate(sets))
for i, (k, a, b) in enumerate(sets):
    sid = f"#set{k}0" if k == "M" else f"#set{k}{i}"
    show(sid, a, b)

# Einblendungen oben
OBEN = [(0, "TEIL 2 – MEINE ZAHL IST <span style='color:#ff4d5a'>1</span>"), (st("s2"), "VERSTECK 1/2"), (st("s3"), "FAIL ❌"), (st("s4"), "08:00 · SCHULE"), (st("s5"), "10/10 GERUCH 🤢"),
        (st("s6"), "OMA HILDE · 900"), (w("s7", "Loswerden") - .1, "AUSWEG: 100 LACHER"), (st("s8"), "TEAM 🤝"), (st("s9"), "12 → 50"), (st("s10"), "98/100"),
        (st("s11"), "NOCH 1 LACHER!"), (st("s12"), "100/100 ✅"), (st("s13"), "MITTERNACHT 🔔"), (st("s14"), "???"), (st("s15"), "A oder B? 👇")]
ob = []
for k, (t0, txt) in enumerate(OBEN):
    t1 = OBEN[k + 1][0] if k + 1 < len(OBEN) else tEND
    big = k == 0
    ob.append(f'<div id="ob{k}" class="ui clip" data-start="{F(t0)}" data-duration="{F(t1 - t0)}" style="left:0;right:0;top:{150 if big else 110}px;text-align:center">'
              f'<div id="ob{k}-in" style="display:inline-block;background:#111;color:#fff;border:6px solid #fff;border-radius:22px;padding:{"16px 34px" if big else "10px 28px"};font:900 {64 if big else 54}px/1.1 Inter,sans-serif">{txt}</div></div>')
    J.append(f'tl.fromTo("#ob{k}-in", {{ scale: 1.4, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: .22, ease: "back.out(2)", immediateRender: false }}, {F(t0 + .01)});')
tag = (f'<div id="tg0" class="ui clip" data-start="0" data-duration="{F(tJ - .1)}" style="left:30px;top:40px;font:900 40px Inter,sans-serif;color:#111;background:#ffd166;padding:6px 18px;border-radius:12px">⏪ WAS BISHER GESCHAH</div>'
       f'<div id="tg1" class="ui clip" data-start="{F(tJ - .1)}" data-duration="{F(tEND - tJ + .1)}" style="left:30px;top:40px;font:900 36px Inter,sans-serif;color:#fff;background:rgba(0,0,0,.55);padding:6px 16px;border-radius:12px">IN DIESER WELT … #2</div>')
cnt = (f'<div id="cnt" class="ui clip" data-start="{F(cnt_keys[0][0])}" data-duration="{F(t13 + .6 - cnt_keys[0][0])}" style="left:0;right:0;top:330px;text-align:center;opacity:0">'
       f'<div id="cnt-in" style="display:inline-block;background:#ffd166;border:8px solid #111;border-radius:30px;padding:14px 40px;font:900 130px/1 Inter,sans-serif;color:#111">😂 <span id="cntv">0</span>/100</div></div>')
end_card = (f'<div id="endc" class="ui clip" data-start="{F(tEND)}" data-duration="{F(END - tEND)}" style="left:0;top:0;width:1080px;height:1920px;background:linear-gradient(rgba(0,0,0,0) 20%, rgba(0,0,0,.55) 45%, rgba(0,0,0,.55) 65%, rgba(0,0,0,0) 85%);text-align:center">'
            f'<div id="e1" style="margin-top:700px;font:900 190px/1 Inter,sans-serif;color:#ffd166;-webkit-text-stroke:10px #111;paint-order:stroke fill">TEIL 3?</div>'
            f'<div id="e2" style="display:inline-block;margin-top:50px;background:#fff;border:6px solid #111;border-radius:24px;padding:18px 44px;font:900 70px Inter,sans-serif;color:#111">➕ FOLGEN</div></div>')
J += [f'tl.fromTo("#e1", {{ scale: 2.2, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: .3, ease: "back.out(2)", immediateRender: false }}, {F(tEND + .02)});',
      f'tl.fromTo("#e2", {{ scale: .3, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: .3, ease: "back.out(2)", immediateRender: false }}, {F(tEND + .2)});',
      f'tl.to("#e2", {{ scale: 1.08, duration: .25, yoyo: true, repeat: 3, ease: "sine.inOut" }}, {F(tEND + .55)});']

open("compositions/welt.html", "w", encoding="utf-8").write(f'''<template>
  <style>#root {{ position: absolute; inset: 0; overflow: hidden; background: #000; }} .ui {{ position: absolute; font-family: Inter, sans-serif; }}</style>
  <div id="root" data-composition-id="welt" data-width="1080" data-height="1920">
    <svg class="clip" data-start="0" data-duration="{F(END)}" viewBox="0 0 1080 1920" style="position:absolute;left:0;top:0;width:1080px;height:1920px" data-layout-ignore>{DEFS}<g id="shk"><g id="cam">{sets_svg}</g></g></svg>
    {"".join(ob)}{tag}{cnt}{end_card}
  </div>
  <script>(function () {{ const tl = gsap.timeline({{ paused: true }});
{chr(10).join("    " + j for j in J)}
    window.__timelines["welt"] = tl; }})();</script>
</template>
''')

# ---------- Einzelwort-Untertitel (Bildmitte) ----------
HOT = {"1", "100", "100!", "900,", "12", "50.", "98.", "23", "59.", "99", "A", "B!", "3?", "EINS", "NICHTS", "MITTERNACHT."}
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
    if t0 >= tEND - .05: continue
    te = min(caps[j + 1][0] if j + 1 < len(caps) else END, t0 + 1.3, tEND)
    up = d.upper()
    col = "#ffd166" if (up in HOT or any(ch.isdigit() for ch in up)) else "#fff"
    fs = min(104, int(1500 / max(1, len(up))))
    items.append(f'<div id="w{j}" class="wd clip" data-start="{F(t0)}" data-duration="{F(max(.15, te - t0 - .02))}"><span id="w{j}-in" style="color:{col};font-size:{fs}px">{up}</span></div>')
    cj.append(f'tl.fromTo("#w{j}-in", {{ scale: 1.25, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: .08 }}, {F(t0)});')
open("compositions/caps.html", "w", encoding="utf-8").write(f'''<template>
  <style>#root {{ position: absolute; inset: 0; }} .wd {{ position: absolute; left: 0; right: 0; top: 1560px; text-align: center; }}
    .wd span {{ display: inline-block; font: 900 104px/1 Inter, sans-serif; white-space: nowrap; -webkit-text-stroke: 16px #000; paint-order: stroke fill; }}</style>
  <div id="root" data-composition-id="caps" data-width="1080" data-height="1920">{"".join(items)}</div>
  <script>(function () {{ const tl = gsap.timeline({{ paused: true }}); {" ".join(cj)} window.__timelines["caps"] = tl; }})();</script>
</template>
''')

# ---------- Ton ----------
subprocess.run([sys.executable, "tools/welt_melodie.py", F(END), F(st("s11")), F(t13), F(t15)], check=True)
Hh = lambda id_, ti: f'      <div id="{id_}" data-composition-id="{id_}" data-composition-src="compositions/{id_}.html" data-start="0" data-duration="{F(END)}" data-track-index="{ti}" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index:{ti}"></div>'
lines = [Hh("welt", 2), Hh("caps", 3), f'      <audio id="musik" class="clip" data-start="0" data-duration="{F(END)}" data-track-index="5" data-volume="0.16" src="assets/musik.wav"></audio>']
for k in T:
    d = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"assets/vo/{k}.mp3"]))
    lines.append(f'      <audio id="vo-{k}" class="clip" data-start="{T[k]["start"] + T[k]["lead"]:.2f}" data-duration="{d:.2f}" data-track-index="4" data-volume="1" src="assets/vo/{k}.mp3"></audio>')
for j, (n, at, vol, dur) in enumerate(FX):
    lines.append(f'      <audio id="fx-{j}" class="clip" data-start="{F(max(0, at))}" data-duration="{F(min(dur, END - max(0, at)))}" data-volume="{vol}" data-track-index="{20 + j}" src="assets/sfx2/{n}.mp3"></audio>')
open("index.html", "w", encoding="utf-8").write(f'''<!doctype html>
<html lang="de" data-resolution="portrait"><head><meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" /><script src="assets/gsap.min.js"></script>
<style>* {{ margin: 0; padding: 0; box-sizing: border-box; }} html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #000; }} #root {{ width: 100%; height: 100%; }}</style></head>
<body><div id="root" data-composition-id="main" data-start="0" data-duration="{F(END)}" data-width="1080" data-height="1920">
{chr(10).join(lines)}
</div><script>window.__timelines = window.__timelines || {{}}; window.__timelines["main"] = gsap.timeline({{ paused: true }});</script></body></html>
''')
print("Ende", END, "Endkarte", tEND, "FX", len(FX))
