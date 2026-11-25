"""STORY-FORMAT „In dieser Welt …“ – Die Zahl über dem Kopf, TEIL 5 = FINALE (Oma Hilde = Admin, Ben drückt den Knopf → Emojis, Mia zieht den Hebel AUS).
Aufruf: python3 tools/story5.py  (liest voice.json (= voice-teil5.json) + assets/vo/timing.json; Bausteine aus tools/bausteine.py + Figuren aus story4.py;
Musik = fester Hintergrund-Sound assets/bgm.mp3 über tools/story_musik.py). Regeln Trend-Scout 25.11.: Bild 0 = ADMIN mit Punch-Zoom, Untertitel bei 65 %,
Mia immer pinker Hoodie, Banner „FINALE“, Ende Schild „ÜBER MIR: ___?“ + Loop-Fahrt, Endbanner nur einmal."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bausteine import *
import math

# ---------- zusätzliche Mimik / Arme / Haare ----------
FACES["full"] = ('<path d="M-44 -6 Q-30 -18 -16 -6 M16 -6 Q30 -18 44 -6" stroke="#111" stroke-width="7" fill="none" stroke-linecap="round"/>'
                 '<rect x="-92" y="6" width="58" height="58" rx="26" fill="#f4a3a3" stroke="#111" stroke-width="4"/><rect x="34" y="6" width="58" height="58" rx="26" fill="#f4a3a3" stroke="#111" stroke-width="4"/>'
                 '<path d="M-14 40 Q0 50 14 40" stroke="#111" stroke-width="6" fill="none" stroke-linecap="round"/><rect x="-6" y="52" width="16" height="12" rx="4" fill="#e9a23b"/>')
FACES["worried"] = (E(-30, 0, 10) + E(30, 0, 10) + '<path d="M-48 -26 L-14 -36 M48 -26 L14 -36" stroke="#111" stroke-width="7" stroke-linecap="round"/>'
                    '<path d="M-22 44 Q0 30 22 44" stroke="#111" stroke-width="7" fill="none" stroke-linecap="round"/>')
FACES["joy"] = ('<path d="M-46 -2 Q-30 -20 -14 -2 M14 -2 Q30 -20 46 -2" stroke="#111" stroke-width="8" fill="none" stroke-linecap="round"/>'
                '<path d="M-40 18 Q0 86 40 18 Z" fill="#5a1a1a" stroke="#111" stroke-width="5"/><path d="M-32 22 H32" stroke="#fff" stroke-width="8"/>')
FACES["lookdown"] = WEYE(-30, -6, 0, 9) + WEYE(30, -6, 0, 9) + '<path d="M-22 40 H22" stroke="#111" stroke-width="7" stroke-linecap="round"/>'
FACES["deadpan"] = ('<path d="M-46 -6 H-14 M14 -6 H46" stroke="#111" stroke-width="8" stroke-linecap="round"/>' + E(-30, 4, 7) + E(30, 4, 7) +
                    '<path d="M-26 40 H26" stroke="#111" stroke-width="8" stroke-linecap="round"/>')
FACES["glow"] = ('<rect x="-52" y="-28" width="44" height="44" rx="10" fill="#39ff14" stroke="#111" stroke-width="4"/><rect x="8" y="-28" width="44" height="44" rx="10" fill="#39ff14" stroke="#111" stroke-width="4"/>'
                 '<rect x="-14" y="24" width="28" height="34" rx="12" fill="#5a1a1a" stroke="#111" stroke-width="4"/>')
FACES["plead"] = (E(-30, -2, 13) + E(30, -2, 13) + '<rect x="-25" y="-10" width="7" height="7" fill="#fff"/><rect x="35" y="-10" width="7" height="7" fill="#fff"/>'
                  '<path d="M-50 -34 L-16 -44 M50 -34 L16 -44" stroke="#111" stroke-width="7" stroke-linecap="round"/><path d="M-18 44 Q0 34 18 44" stroke="#111" stroke-width="6" fill="none" stroke-linecap="round"/>')
ARM["pray"] = ("M90 -250 Q160 -200 22 -330", (22, -330))
ARM["cross"] = ("M90 -250 Q170 -150 -40 -200", (-40, -200))
HAIR["theo"] = lambda c: (f'<path d="M-100 -30 L-104 -110 L-70 -96 L-60 -140 L-26 -104 L-6 -150 L20 -106 L52 -146 L62 -100 L104 -118 L100 -30 L80 -70 H-80 Z" fill="{c}" stroke="#111" stroke-width="4"/>'
                          '<path d="M20 -106 L52 -146 L62 -100 Z" fill="#00f5d4" stroke="#111" stroke-width="3"/>')
HOOD = ('<g id="{u}-hood"><path d="M-138 120 Q-150 -168 0 -172 Q150 -168 138 120 L104 110 Q106 -108 0 -112 Q-106 -108 -104 110 Z" fill="#141418" stroke="#000" stroke-width="5"/></g>')
def bag(u, x, y, r=0, L=300):
    return (f'<g id="{u}-bag" transform="translate({x} {y}) rotate({r})"><rect x="{-L}" y="-24" width="{L + 20}" height="48" rx="24" fill="#e9a23b" stroke="#111" stroke-width="5"/>'
            + "".join(f'<path d="M{-L + 40 + k * 60} -14 l22 28" stroke="#b5651d" stroke-width="7" stroke-linecap="round"/>' for k in range(max(1, (L - 40) // 60))) + '</g>')

# Mia – IMMER gleich: pinker Hoodie (Bauchtasche + Kordeln) + pinke Haarspange
MIA_PIN = '<rect x="46" y="-112" width="52" height="24" rx="8" fill="#ff006e" stroke="#111" stroke-width="4" transform="rotate(-14 72 -100)"/>'
HOODIE = ('<rect x="-62" y="-190" width="124" height="70" rx="16" fill="#d63a62" stroke="#111" stroke-width="4"/>'
          '<path d="M-26 -300 V-236 M26 -300 V-236" stroke="#fff" stroke-width="7" stroke-linecap="round"/><rect x="-34" y="-244" width="16" height="16" rx="5" fill="#fff"/><rect x="18" y="-244" width="16" height="16" rx="5" fill="#fff"/>')
MIA_EX = ("happy", "shock", "panic", "determined", "annoyed", "sad", "hope", "confused", "relief", "laugh", "joy", "worried", "plead")
def mia(uid, start="happy", arm=("down", "down"), arm2=None, behind=""):
    return person(uid, "mia", "#6b3e26", "#ef476f", exprs=MIA_EX, start=start, head_acc=MIA_PIN, arm=arm, arm2=arm2, extra=HOODIE, behind=behind)
THEO_EX = ("grin", "grinwink", "neutral", "determined", "worried", "happy", "shock", "laugh", "deadpan", "annoyed", "glow")
def theo(uid, start="grin", hood=False, arm=("down", "down"), arm2=None, extra="", chicken=False):
    if chicken:
        return person(uid, "chicken", "#1a1a1a", "#ffd60a", skin="#e0ac69", exprs=THEO_EX, start=start, arm=arm, arm2=arm2, extra=extra, pants="#fb8500")
    return person(uid, "theo", "#1a1a1a", "#1b1b1f", skin="#e0ac69", exprs=THEO_EX, start=start, arm=arm, arm2=arm2, extra=extra,
                  head_acc=HOOD.format(u=uid) if hood else "", pants="#3a3a44")
BEN_EX = ("happy", "full", "laugh", "determined", "hope", "neutral")
def ben(uid, start="happy", arm=("down", "down"), arm2=None, extra=""):
    return person(uid, "ben", "#ff9f1c", "#fb8500", skin="#e0ac69", exprs=BEN_EX, start=start, arm=arm, arm2=arm2, extra=extra)
OMA_EX = ("relief", "wink", "laugh", "happy", "annoyed", "lookdown", "neutral", "determined")
OMA_ACC = '<rect x="-64" y="-20" width="46" height="34" rx="16" fill="none" stroke="#555" stroke-width="5"/><rect x="18" y="-20" width="46" height="34" rx="16" fill="none" stroke="#555" stroke-width="5"/>'
def oma(uid, start="relief", arm=("down", "down"), arm2=None, extra=""):
    return person(uid, "oma", "#e0e0e0", "#9d4edd", exprs=OMA_EX, start=start, arm=arm, arm2=arm2, extra=extra, head_acc=OMA_ACC)
KR_ACC = '<rect x="-62" y="-22" width="48" height="36" rx="8" fill="none" stroke="#111" stroke-width="6"/><rect x="14" y="-22" width="48" height="36" rx="8" fill="none" stroke="#111" stroke-width="6"/><path d="M-14 -6 H14" stroke="#111" stroke-width="6"/>'
def krause(uid, start="neutral", arm=("down", "down")):
    return person(uid, "glatze", "#555", "#6c757d", exprs=("neutral", "laugh", "confused", "shock"), start=start, arm=arm, head_acc=KR_ACC)
def passant(uid, shirt, hair="mann", hcol="#3d2b1f", start="neutral", exprs=("neutral", "laugh"), arm=("down", "down")):
    return person(uid, hair, hcol, shirt, exprs=exprs, start=start, arm=arm)
RB = lambda uid, txt, size=110, y=-620, vis=True: badge(uid, txt, col=RED, fg="#fff", size=size, y=y, vis=vis)
GB = lambda uid, txt, size=70, y=-620, vis=True: badge(uid, txt, col=GREEN, fg="#fff", size=size, y=y, vis=vis)
WB = lambda uid, txt, size=70, y=-620, vis=True: badge(uid, txt, size=size, y=y, vis=vis)
def admin(uid, size=74, y=-620, vis=True):
    wd = 60 + size * .62 * 5
    return (f'<g id="{uid}" opacity="{1 if vis else 0}"><g id="{uid}-in"><rect x="{-wd/2 - 14:.0f}" y="{y - size - 14:.0f}" width="{wd + 28:.0f}" height="{size * 1.35 + 28:.0f}" rx="{size*.4:.0f}" fill="#39ff14" opacity=".35"/>'
            f'<rect x="{-wd/2:.0f}" y="{y - size:.0f}" width="{wd:.0f}" height="{size * 1.35:.0f}" rx="{size*.3:.0f}" fill="#0b0f0b" stroke="#39ff14" stroke-width="8"/>'
            f'<text x="0" y="{y + size * .12:.0f}" text-anchor="middle" style="font:900 {size}px Inter,monospace;fill:#39ff14">ADMIN</text></g></g>')

def night_lamp():
    return ('<rect x="980" y="300" width="22" height="1000" fill="#333"/><rect x="900" y="290" width="120" height="40" rx="12" fill="#444"/>'
            '<rect x="900" y="330" width="80" height="40" rx="10" fill="#ffe8a3"/><path d="M940 360 L380 1900 H1080 V560 Z" fill="url(#cone)"/>')
def sepia(content, label, ly=440):
    return (content + '<rect width="1080" height="1920" fill="#c9a26b" opacity=".38"/>'
            '<rect x="24" y="24" width="1032" height="1872" rx="30" fill="none" stroke="#fff" stroke-width="18" stroke-dasharray="40 24"/>'
            f'<text x="540" y="{ly}" text-anchor="middle" style="font:900 54px {FONT};fill:#fff;opacity:.9">{label}</text>')
def confetti(uid, y0=500, n=40):
    return (f'<g id="{uid}" opacity="0">' + "".join(f'<rect x="{(k * 97) % 1080}" y="{y0 + (k * 53) % 300}" width="24" height="36" fill="{("#ffd166", "#ef476f", "#06d6a0", "#118ab2")[k % 4]}" transform="rotate({k * 37} {(k * 97) % 1080} {y0 + (k * 53) % 300})"/>' for k in range(n)) + '</g>')
TILES = lambda bg="#e9ecef": f'<rect width="1080" height="1920" fill="{bg}"/>' + "".join(f'<rect x="{(k % 9) * 120}" y="{(k // 9) * 120}" width="118" height="118" fill="none" stroke="#ced4da" stroke-width="3"/>' for k in range(9 * 17))
def clock_face(cx, cy, r, hh, mm, uid="clk"):
    ah = math.radians((hh % 12 + mm / 60) * 30 - 90); am = math.radians(mm * 6 - 90)
    return (f'<g id="{uid}"><rect x="{cx - r - 14}" y="{cy - r - 14}" width="{2 * r + 28}" height="{2 * r + 28}" rx="{r * .35:.0f}" fill="#6b4226" stroke="#111" stroke-width="7"/>'
            f'<rect x="{cx - r}" y="{cy - r}" width="{2 * r}" height="{2 * r}" rx="{r * .3:.0f}" fill="#fefae0" stroke="#111" stroke-width="5"/>'
            + "".join(f'<rect x="{cx + (r - 26) * math.cos(math.radians(k * 30)) - 7:.0f}" y="{cy + (r - 26) * math.sin(math.radians(k * 30)) - 7:.0f}" width="14" height="14" fill="#111"/>' for k in range(12)) +
            f'<path d="M{cx} {cy} L{cx + r * .5 * math.cos(ah):.0f} {cy + r * .5 * math.sin(ah):.0f}" stroke="#111" stroke-width="16" stroke-linecap="round"/>'
            f'<path d="M{cx} {cy} L{cx + r * .78 * math.cos(am):.0f} {cy + r * .78 * math.sin(am):.0f}" stroke="#e63946" stroke-width="10" stroke-linecap="round"/><rect x="{cx - 14}" y="{cy - 14}" width="28" height="28" rx="6" fill="#111"/></g>')

TOILET = '<g transform="translate(330 1900)"><rect x="-150" y="-330" width="300" height="200" rx="30" fill="#fff" stroke="#111" stroke-width="7"/><rect x="-170" y="-150" width="340" height="80" rx="30" fill="#f8f9fa" stroke="#111" stroke-width="7"/><rect x="-110" y="-80" width="220" height="80" fill="#fff" stroke="#111" stroke-width="7"/></g>'
BASKET = '<g transform="translate(-170 -150)"><path d="M-70 -40 Q0 -140 70 -40" stroke="#6b4226" stroke-width="12" fill="none"/><rect x="-80" y="-50" width="160" height="110" rx="20" fill="#bc6c25" stroke="#111" stroke-width="5"/>' + \
         "".join(f'<g transform="translate({dx} -50)"><rect x="-8" y="-6" width="16" height="30" fill="#fff" stroke="#111" stroke-width="3"/><path d="M-30 -4 Q0 -46 30 -4 Z" fill="#e63946" stroke="#111" stroke-width="4"/><circle cx="-8" cy="-18" r="5" fill="#fff"/></g>' for dx in (-45, 0, 45)) + '</g>'

# ======================= TEIL 5 – FINALE: neue Bausteine =======================
FACES["dance"] = ('<path d="M-44 -6 Q-30 -18 -16 -6 M16 -6 Q30 -18 44 -6" stroke="#111" stroke-width="7" fill="none" stroke-linecap="round"/>'
                  '<path d="M-30 24 Q0 60 30 24 Z" fill="#5a1a1a" stroke="#111" stroke-width="5"/>')
OMA_EX = OMA_EX + ("joy", "shock", "grin")
THEO_EX = THEO_EX + ("confused", "relief", "joy")
BEN_EX = BEN_EX + ("shock", "confused", "plead", "joy", "grin", "worried")
MIA_EX = MIA_EX + ("grin", "grinwink")
def mia(uid, start="happy", arm=("down", "down"), arm2=None, behind="", extra=""):
    return person(uid, "mia", "#6b3e26", "#ef476f", exprs=MIA_EX, start=start, head_acc=MIA_PIN, arm=arm, arm2=arm2, extra=HOODIE + extra, behind=behind)
def ben(uid, start="happy", arm=("down", "down"), arm2=None, extra=""):
    return person(uid, "ben", "#ff9f1c", "#fb8500", skin="#e0ac69", exprs=BEN_EX, start=start, arm=arm, arm2=arm2, extra=extra)
def oma(uid, start="relief", arm=("down", "down"), arm2=None, extra=""):
    return person(uid, "oma", "#e0e0e0", "#9d4edd", exprs=OMA_EX, start=start, arm=arm, arm2=arm2, extra=extra, head_acc=OMA_ACC)
def theo(uid, start="grin", hood=False, arm=("down", "down"), arm2=None, extra="", chicken=False):
    if chicken:
        return person(uid, "chicken", "#1a1a1a", "#ffd60a", skin="#e0ac69", exprs=THEO_EX, start=start, arm=arm, arm2=arm2, extra=extra, pants="#fb8500")
    return person(uid, "theo", "#1a1a1a", "#1b1b1f", skin="#e0ac69", exprs=THEO_EX, start=start, arm=arm, arm2=arm2, extra=extra,
                  head_acc=HOOD.format(u=uid) if hood else "", pants="#3a3a44")
def krause(uid, start="neutral", arm=("down", "down")):
    return person(uid, "glatze", "#555", "#6c757d", exprs=("neutral", "laugh", "confused", "shock", "happy"), start=start, arm=arm, head_acc=KR_ACC)
def EB(uid, emo, size=96, y=-640, vis=False, col="#ffffff"):   # Emoji-Schild über dem Kopf
    return badge(uid, emo, col=col, size=size, y=y, chars=1.5, vis=vis)
def mush(x, y, s=1.0, uid=None):
    i = f' id="{uid}"' if uid else ""
    return (f'<g{i} transform="translate({x} {y}) scale({s})"><rect x="-14" y="-10" width="28" height="60" fill="#fff" stroke="#111" stroke-width="5"/>'
            '<path d="M-60 -6 Q0 -92 60 -6 Z" fill="#e63946" stroke="#111" stroke-width="6"/><circle cx="-18" cy="-34" r="9" fill="#fff"/><circle cx="20" cy="-26" r="7" fill="#fff"/></g>')
REMOTE = ('<g id="remote" opacity="0"><rect x="-44" y="-130" width="88" height="200" rx="18" fill="#343a40" stroke="#111" stroke-width="6"/>'
          '<path d="M30 -130 L70 -230" stroke="#111" stroke-width="7"/><circle cx="70" cy="-232" r="12" fill="#e63946" stroke="#111" stroke-width="4"/>'
          '<rect x="-26" y="-108" width="52" height="40" rx="6" fill="#39ff14"/>'
          + "".join(f'<rect x="{-26 + (k % 2) * 30}" y="{-56 + (k // 2) * 34}" width="22" height="22" rx="6" fill="{("#e63946", "#ffd166", "#2dc653", "#4cc9f0")[k % 4]}" stroke="#111" stroke-width="3"/>' for k in range(6)) + '</g>')
def keller_bg():
    bricks = "".join(f'<rect x="{(k % 7) * 160 - (80 if (k // 7) % 2 else 0)}" y="{(k // 7) * 80}" width="152" height="72" rx="6" fill="#6d4c41" opacity="{.55 + .1 * (k % 3)}"/>' for k in range(7 * 16))
    return (f'<rect width="1080" height="1920" fill="#3e2723"/>{bricks}<rect y="1260" width="1080" height="660" fill="#4a4e54"/><rect y="1260" width="1080" height="14" fill="#000" opacity=".3"/>'
            '<path d="M540 0 V160" stroke="#111" stroke-width="6"/><rect x="510" y="160" width="60" height="70" rx="26" fill="#ffe8a3" stroke="#111" stroke-width="5"/>'
            '<path d="M540 230 L-200 1920 H1280 Z" fill="#ffe8a3" opacity=".10"/>')
def computer(uid, x, base, s=1.0, screen=""):
    lamps = "".join(f'<rect id="{uid}-l{k}" x="{-220 + (k % 6) * 80}" y="{-560 + (k // 6) * 60}" width="40" height="34" rx="8" fill="{("#e63946", "#ffd166", "#2dc653")[k % 3]}" stroke="#111" stroke-width="4"/>' for k in range(12))
    reels = "".join(f'<g transform="translate({cx} -330)"><rect x="-80" y="-80" width="160" height="160" rx="40" fill="#adb5bd" stroke="#111" stroke-width="6"/><rect id="{uid}-r{j}" x="-24" y="-24" width="48" height="48" rx="8" fill="#495057" stroke="#111" stroke-width="5"/></g>' for j, cx in enumerate((-130, 130)))
    doily = ("".join(f'<circle cx="{-250 + k * 50}" cy="-940" r="30" fill="#fff" stroke="#ccc" stroke-width="3"/>' for k in range(11)) +
             '<rect x="-280" y="-960" width="560" height="40" rx="12" fill="#fff" stroke="#ccc" stroke-width="3"/>' +
             "".join(f'<circle cx="{-250 + k * 50}" cy="-940" r="9" fill="none" stroke="#bbb" stroke-width="3"/>' for k in range(11)))
    return (f'<g id="{uid}" transform="translate({x} {base}) scale({s})"><ellipse cx="0" cy="6" rx="330" ry="30" fill="#000" opacity=".3"/>'
            '<rect x="-290" y="-930" width="580" height="930" rx="26" fill="#c9b79c" stroke="#111" stroke-width="8"/><rect x="-290" y="-930" width="580" height="930" rx="26" fill="url(#shade)"/>'
            f'<rect x="-240" y="-880" width="480" height="270" rx="20" fill="#111" stroke="#555" stroke-width="10"/><g transform="translate(0 -745)">{screen}</g>'
            f'{lamps}{reels}<rect x="-240" y="-200" width="480" height="140" rx="14" fill="#8d7b63" stroke="#111" stroke-width="5"/>'
            + "".join(f'<rect x="{-220 + k * 55}" y="-170" width="40" height="80" rx="6" fill="#343a40"/>' for k in range(8)) + doily +
            f'<text x="0" y="-25" text-anchor="middle" style="font:900 36px Inter,monospace;fill:#111">SYSTEM v1.0</text></g>')
def sign(uid, lines, x, y, wd, size=70, col="#fff", fg="#111", vis=True, rot=0):
    h = 40 + len(lines) * size * 1.15
    txt = "".join(f'<text x="0" y="{-h/2 + 20 + (k + .82) * size * 1.15:.0f}" text-anchor="middle" style="font:900 {size}px {FONT};fill:{fg}">{l}</text>' for k, l in enumerate(lines))
    return (f'<g id="{uid}" opacity="{1 if vis else 0}" transform="translate({x} {y}) rotate({rot})"><g id="{uid}-in"><rect x="{-wd/2 + 8}" y="{-h/2 + 8:.0f}" width="{wd}" height="{h:.0f}" rx="24" fill="#000" opacity=".3"/>'
            f'<rect x="{-wd/2}" y="{-h/2:.0f}" width="{wd}" height="{h:.0f}" rx="24" fill="{col}" stroke="#111" stroke-width="8"/>{txt}</g></g>')
FLASH = lambda uid, col="#fff": f'<rect id="{uid}" width="1080" height="1920" fill="{col}" opacity="0"/>'


# Kamerafahrten enden spätestens beim nächsten Schnitt (sonst überschreibt eine laufende Fahrt den harten Schnitt) – wie liefer1.py
import bausteine as _B
CAMQ, CUTT = [], []
def cut(t, x, y, z):
    CUTT.append(t); _B.cut(t, x, y, z)
def cam(t, x, y, z, d=1.0, ease="power2.inOut"):
    CUTT.append(t); CAMQ.append((len(J), t, x, y, z, d, ease)); J.append("")
def cam_fix():
    for idx, t, x, y, z, d, ease in CAMQ:
        nxt = [c for c in CUTT if c > t + .001]
        if nxt: d = max(.1, min(d, min(nxt) - t - .02))
        ox, oy = _B._cam(x, y, z); _B.CUTS.append(round(t, 2))
        J[idx] = f'tl.to("#cam", {{ x: {ox:.0f}, y: {oy:.0f}, scale: {z}, duration: {d:.2f}, ease: "{ease}" }}, {F(t)});'

S = {}; FX = []
FY = 1560
# --- A0: Bild 0 – Nacht, Oma Hilde mit blinkendem ADMIN, Mia (pink) + Theo vorne
S["A0"] = (street_bg(night=True) + night_lamp() +
           fig(oma("om0", "wink", arm=("hip", "down"), extra=BASKET) + admin("aO0", size=66, y=-640), 540, FY, 1.5) +
           fig(mia("m0", "shock") + GB("bM0", "30.000", size=50, y=-640), 175, FY + 120, 1.2) +
           fig(theo("t0", "shock") + RB("bT0", "1", size=80, y=-640), 900, FY + 120, 1.2))
# --- RS: Rückblick-Montage (sepia, 3 Bilder)
S["RS"] = ('<g id="r1">' + sepia('<rect width="1080" height="1920" fill="#ffb4a2"/><rect y="1260" width="1080" height="660" fill="#adb5bd"/>' +
                                 fig(mia("m1", "joy", arm=("up", "up")) + GB("bM1", "30.000", size=80, y=-640), 540, FY, 1.6), "MIA: 30.000 TAGE", ly=330) + '</g>'
           '<g id="r2" opacity="0">' + sepia('<rect width="1080" height="1920" fill="#a8dadc"/><rect y="1260" width="1080" height="660" fill="#adb5bd"/>' +
                                 fig(theo("t1", "grinwink") + RB("bT1", "1", size=120, y=-640), 540, FY, 1.6), "THEO: 1", ly=330) + '</g>'
           '<g id="r3" opacity="0">' + sepia('<rect width="1080" height="1920" fill="#0b132b"/>'
                                 f'<rect x="140" y="560" width="800" height="300" rx="40" fill="{GREEN}" stroke="#111" stroke-width="10"/><text x="540" y="770" text-anchor="middle" style="font:900 150px {FONT};fill:#fff">😂 99/100</text>' +
                                 fig(oma("om1", "neutral") + admin("aO1", size=60, y=-640), 540, FY + 60, 1.0), "OMA HILDE: NEIN.", ly=330) + '</g>')
# --- P: Oma nah – Pilz klappt auf zur Fernbedienung
S["P"] = (street_bg(night=True) + night_lamp() +
          fig(oma("om2", "grin", arm=("down", "front"), extra=f'<g id="pmush" transform="translate(196 -360)">{mush(0, 0, 1.6)}</g><g transform="translate(196 -330) scale(1.3)">{REMOTE}</g>'), 470, FY, 1.55))
# --- K: Keller – Riesencomputer mit Häkeldeckchen, Oma links, Mia rechts
SCR_BEN = (f'<g id="scrBen" opacity="0"><rect x="-230" y="-125" width="460" height="250" fill="#0b132b"/>'
           f'<g transform="translate(-130 110) scale(.42)">{ben("bnS", "full")}</g>'
           f'<text id="kNum" x="80" y="20" text-anchor="middle" style="font:900 74px Inter,monospace;fill:#39ff14">20.100</text></g>')
S["K"] = (keller_bg() + computer("pc", 540, FY - 20, .82, SCR_BEN) +
          fig(oma("om3", "wink", arm=("hip", "down")) + admin("aO3", size=44, y=-640), 185, FY + 40, 1.15) +
          fig(mia("m3", "confused", arm=("down", "down"), arm2=("down", "out")) + GB("bM3", "30.000", size=40, y=-640), 900, FY + 40, 1.15))
# --- M: Monitor groß (Ben-Zahl / ERROR)
S["M"] = (keller_bg() + '<rect x="40" y="420" width="1000" height="760" rx="40" fill="#c9b79c" stroke="#111" stroke-width="10"/>'
          '<rect x="90" y="470" width="900" height="560" rx="24" fill="#0b132b" stroke="#555" stroke-width="12"/>'
          f'<g id="mBen"><g transform="translate(300 980) scale(.85)">{ben("bnM", "full")}</g>'
          f'<text id="mNum" x="730" y="760" text-anchor="middle" style="font:900 120px Inter,monospace;fill:#39ff14">20.100</text>'
          f'<text x="730" y="880" text-anchor="middle" style="font:900 60px Inter,monospace;fill:#39ff14">BEN</text></g>'
          f'<g id="mErr" opacity="0"><rect x="90" y="470" width="900" height="560" rx="24" fill="#2b0000"/>'
          f'<text x="540" y="700" text-anchor="middle" style="font:900 96px Inter,monospace;fill:#ff3b30">ERROR:</text>'
          f'<text x="540" y="840" text-anchor="middle" style="font:900 84px Inter,monospace;fill:#ff3b30">0 LACHER</text>'
          '<text x="540" y="950" text-anchor="middle" style="font:900 48px Inter,monospace;fill:#ff8fa3">USER: THEO</text></g>'
          '<g id="smoke" opacity="0">' + "".join(f'<rect x="{700 + k * 60}" y="{330 - k * 70}" width="{120 + k * 20}" height="{90 + k * 10}" rx="40" fill="#adb5bd" opacity=".85"/>' for k in range(4)) + '</g>'
          + "".join(f'<rect x="{150 + k * 110}" y="1080" width="60" height="50" rx="10" fill="{("#e63946", "#ffd166", "#2dc653")[k % 3]}" stroke="#111" stroke-width="4"/>' for k in range(8)))
# --- BP: Rückblende – Ben futtert Omas Pilzkorb  /  DR: Oma dreht am Rad
PILE = "".join(mush(-120 + (k % 5) * 60, -40 - (k // 5) * 40, .7) for k in range(10))
S["BP"] = sepia('<rect width="1080" height="1920" fill="#d8f3dc"/><rect y="1260" width="1080" height="660" fill="#95d5b2"/>' +
                fig(ben("bn1", "full", arm=("front", "front")), 540, FY, 1.55) +
                f'<g transform="translate(540 1440)"><rect x="-230" y="-60" width="460" height="170" rx="30" fill="#bc6c25" stroke="#111" stroke-width="7"/><g id="pile">{PILE}</g></g>', "")
WHEEL = ('<g id="wheel"><rect x="-200" y="-200" width="400" height="400" rx="200" fill="#ffd166" stroke="#111" stroke-width="10"/>'
         + "".join(f'<path d="M0 0 L{190 * math.cos(math.radians(k * 45)):.0f} {190 * math.sin(math.radians(k * 45)):.0f}" stroke="#111" stroke-width="10"/>' for k in range(8)) +
         '<rect x="-40" y="-40" width="80" height="80" rx="20" fill="#e63946" stroke="#111" stroke-width="6"/></g>')
S["DR"] = sepia(keller_bg() + f'<g transform="translate(700 600)">{WHEEL}</g><rect x="560" y="860" width="280" height="270" fill="#6d4c41" stroke="#111" stroke-width="7"/>'
                f'<text x="700" y="960" text-anchor="middle" style="font:900 60px {FONT};fill:#fff">BEN</text><text id="drNum" x="700" y="1060" text-anchor="middle" style="font:900 56px Inter,monospace;fill:#39ff14">20.100</text>' +
                fig(oma("om4", "annoyed", arm=("down", "out")), 260, FY, 1.3), "")
# --- PK: Draufsicht Parkplatz – Krauses Auto auf Omas Platz
CAR = ('<g id="car"><rect x="-110" y="-200" width="220" height="400" rx="50" fill="#e63946" stroke="#111" stroke-width="8"/>'
       '<rect x="-80" y="-120" width="160" height="90" rx="20" fill="#a8dadc" stroke="#111" stroke-width="5"/><rect x="-80" y="60" width="160" height="70" rx="20" fill="#a8dadc" stroke="#111" stroke-width="5"/>'
       f'<text x="0" y="20" text-anchor="middle" style="font:900 40px {FONT};fill:#fff">KRAUSE</text></g>')
S["PK"] = sepia('<rect width="1080" height="1920" fill="#6c757d"/>' + "".join(f'<rect x="{60 + k * 320}" y="380" width="14" height="760" fill="#fff"/>' for k in range(4)) +
                f'<rect x="400" y="1040" width="280" height="90" rx="14" fill="#fff" stroke="#111" stroke-width="5"/><text x="540" y="1100" text-anchor="middle" style="font:900 40px {FONT};fill:#9d4edd">OMA HILDE</text>'
                '<rect x="120" y="500" width="200" height="380" rx="46" fill="#3a86ff" stroke="#111" stroke-width="7"/><rect x="760" y="500" width="200" height="380" rx="46" fill="#ffd166" stroke="#111" stroke-width="7"/>'
                f'<g transform="translate(540 720)">{CAR}</g>'
                f'<g id="pkO" opacity="0" transform="translate(860 1640) scale(.7)">{oma("om5", "annoyed", arm=("down", "up"))}</g>', "")
# --- BT: Ben mit Baguette vor dem roten Knopf
BUTTON = ('<g transform="translate(780 1560)"><rect x="-120" y="-420" width="240" height="420" fill="#495057" stroke="#111" stroke-width="7"/>'
          '<rect x="-150" y="-470" width="300" height="60" rx="14" fill="#6c757d" stroke="#111" stroke-width="7"/>'
          '<g id="btn"><rect x="-100" y="-560" width="200" height="100" rx="40" fill="#e63946" stroke="#111" stroke-width="7"/><rect x="-70" y="-548" width="80" height="24" rx="10" fill="#fff" opacity=".5"/></g>'
          f'<rect x="-8" y="-700" width="16" height="140" fill="#111"/><rect x="-170" y="-800" width="340" height="110" rx="16" fill="#ffd166" stroke="#111" stroke-width="6"/><text x="0" y="-765" text-anchor="middle" style="font:900 38px {FONT};fill:#111">NICHT</text><text x="0" y="-715" text-anchor="middle" style="font:900 38px {FONT};fill:#111">DRÜCKEN!</text></g>')
S["BT"] = (keller_bg() + BUTTON + fig(ben("bn2", "determined", arm=("down", "front"), extra=f'<g id="bgt">{bag("bn2", 196, -330, -20, 260)}</g>') + WB("bB2", "12.000", size=50, y=-640), 300, FY, 1.45) + FLASH("btfl"))
# --- ALL: Keller-Reihe – Zahlen → Emojis
AX = {"bn": 150, "t": 410, "om": 680, "m": 935}; AS = 1.15
S["ALL"] = (keller_bg() + computer("pc2", 540, 1200, .55) +
            fig(ben("bn3", "neutral", arm=("down", "front"), extra=bag("bn3x", 196, -330, -20, 220)) + WB("bB3", "12.000", size=46, y=-640) + EB("eB3", "🥖", y=-660), AX["bn"], FY, AS) +
            fig(theo("t3", "neutral") + RB("bT3", "1", size=70, y=-640) + EB("eT3", "🐔", y=-660), AX["t"], FY, AS) +
            fig(oma("om6", "relief") + admin("aO6", size=46, y=-800) + EB("eO6", "🍄", y=-660), AX["om"], FY, AS) +
            fig(mia("m6", "worried") + GB("bM6", "30.000", size=44, y=-640) + EB("eM6", "❤️", y=-660, col="#ffe5ec"), AX["m"], FY, AS) +
            '<g id="sparks" opacity="0">' + "".join(f'<path d="M{100 + k * 110} {600 + (k * 137) % 300} l30 -60 l-10 50 l40 -10 l-50 70 l10 -40 Z" fill="#ffd60a" stroke="#111" stroke-width="3"/>' for k in range(9)) + '</g>' + FLASH("allfl"))
# --- KL: Schulklo-Tür mit 🧻
S["KL"] = (TILES() + '<g id="door"><rect x="300" y="620" width="480" height="1080" rx="14" fill="#4cc9f0" stroke="#111" stroke-width="8"/>'
           '<rect x="350" y="1140" width="44" height="90" rx="10" fill="#adb5bd" stroke="#111" stroke-width="4"/><rect x="480" y="700" width="120" height="64" rx="10" fill="#e63946" stroke="#111" stroke-width="4"/>'
           f'<text x="540" y="746" text-anchor="middle" style="font:900 36px {FONT};fill:#fff">WC</text></g>'
           '<rect y="1700" width="1080" height="220" fill="#adb5bd"/>' + f'<g transform="translate(540 1000)">{EB("eKL", "🧻", size=110, y=-380, vis=False)}</g>' +
           bubble("bubKL", ["BESETZT!"], 760, 1080, 520, tail=(-.6, 1), size=90))
# --- HB: Riesenhebel AN/AUS, Oma zeigt drauf
LEVER = ('<g transform="translate(700 1500)"><rect x="-200" y="-140" width="400" height="160" rx="20" fill="#495057" stroke="#111" stroke-width="8"/>'
         f'<text x="-110" y="-40" text-anchor="middle" style="font:900 64px {FONT};fill:{GREEN}">AN</text><text x="110" y="-40" text-anchor="middle" style="font:900 64px {FONT};fill:{RED}">AUS</text>'
         '<g id="lever"><rect x="-18" y="-760" width="36" height="640" rx="16" fill="#adb5bd" stroke="#111" stroke-width="7"/><rect x="-70" y="-860" width="140" height="130" rx="60" fill="#e63946" stroke="#111" stroke-width="8"/></g></g>')
S["HB"] = (keller_bg() + LEVER +
           fig(oma("om7", "determined", arm=("down", "out")) + EB("eO7", "🍄", y=-660, vis=True), 210, FY, 1.25) +
           f'<g id="hbM" opacity="0">{fig(mia("m7", "determined", arm=("down", "up")) + EB("eM7", "❤️", y=-660, vis=True, col="#ffe5ec"), 510, FY + 80, 1.3)}</g>' +
           '<g id="hbSp" opacity="0">' + "".join(f'<path d="M{620 + (k * 53) % 200} {620 + (k * 71) % 200} l{30 - (k % 3) * 30} -70" stroke="#ffd60a" stroke-width="12" stroke-linecap="round"/>' for k in range(10)) + '</g>' + FLASH("hbfl"))
# --- SP: Split AN = Zahlen | AUS = nichts
def mini_row(prefix, nums):
    return "".join(fig(f(f"{prefix}{k}", "neutral") + (WB(f"{prefix}b{k}", n, size=80, y=-640) if n else ""), 140 + k * 260 // 1, FY - 120, .8) for k, (f, n) in enumerate(nums))
S["SP"] = ('<rect width="540" height="1920" fill="#d8f3dc"/><rect x="540" width="540" height="1920" fill="#ffccd5"/><rect y="1300" width="1080" height="620" fill="#adb5bd"/>'
           f'<svg x="0" y="0" width="540" height="1920" overflow="hidden">{fig(ben("bnL", "worried") + WB("bL1", "12.000", size=50, y=-640), 150, FY, .95)}{fig(mia("mL", "worried") + GB("bL2", "30.000", size=50, y=-640), 400, FY, .95)}</svg>'
           f'<svg x="540" y="0" width="540" height="1920" overflow="hidden">{fig(ben("bnR", "happy"), 150, FY, .95)}{fig(mia("mR", "happy"), 400, FY, .95)}</svg>'
           '<rect x="530" width="20" height="1920" fill="#111"/>'
           f'<g id="labAN"><rect x="50" y="640" width="440" height="150" rx="30" fill="{GREEN}" stroke="#111" stroke-width="8"/><text x="270" y="742" text-anchor="middle" style="font:900 80px {FONT};fill:#fff">AN</text></g>'
           f'<g id="labAUS"><rect x="590" y="640" width="440" height="150" rx="30" fill="{RED}" stroke="#111" stroke-width="8"/><text x="810" y="742" text-anchor="middle" style="font:900 80px {FONT};fill:#fff">AUS</text></g>')
# --- BU: Ben umarmt sein Baguette
S["BU"] = (keller_bg() + fig(ben("bn4", "plead", arm=("cross", "cross"), extra=f'<g transform="translate(0 -200) rotate(-70)">{bag("bn4", 150, 0, 0, 300)}</g>') + EB("eB4", "🥖", y=-600, vis=True), 540, FY, 1.55))
# --- RM: Rückblende-Montage s20 (Mia mit 1, 100/100, Theo im Hühnerkostüm) – Mia im pinken Hoodie
S["RM"] = ('<g id="q1">' + sepia(street_bg(night=True) + fig(mia("m8", "worried") + RB("bM8", "1", size=120, y=-640), 540, FY, 1.6), "DIE 1") + '</g>'
           '<g id="q2" opacity="0">' + sepia(f'<rect width="1080" height="1920" fill="#8ecae6"/><rect x="140" y="660" width="800" height="300" rx="40" fill="{GREEN}" stroke="#111" stroke-width="10"/><text x="540" y="870" text-anchor="middle" style="font:900 150px {FONT};fill:#fff">😂 100/100</text>', "100 LACHER") + '</g>'
           '<g id="q3" opacity="0">' + sepia(street_bg() + fig(theo("t8", "annoyed", chicken=True), 540, FY, 1.6), "DAS HÜHNERKOSTÜM") + '</g>')
# --- Z: Straße Tag – über allen Köpfen nichts (auch Herr Krause kommt dazu)
ZF = FY - 80
ZX = [(110, "kr"), (330, "bn"), (560, "t"), (790, "om"), (990, "m")]
crowd2 = "".join(fig(passant(f"zp{k}", c, hair=h, exprs=("neutral", "confused", "laugh")), x, 1180, .5) for k, (x, c, h) in enumerate([(80, "#3a86ff", "mann"), (300, "#06d6a0", "lena"), (800, "#ffb703", "mann"), (1010, "#8338ec", "lena")]))
S["Z"] = (street_bg() + crowd2 +
          '<g id="ghost" opacity="0">' + "".join(f'<g transform="translate({x} {ZF - 640 * 1.0})">' + badge(f"gh{k}", n, col="#fff", size=46, y=0, vis=True) + '</g>'
                                                for k, (x, n) in enumerate([(110, "15.200"), (330, "20.100"), (560, "1"), (790, "ADMIN"), (990, "30.000")])) + '</g>' +
          fig(krause("kr2", "confused", arm=("down", "up")), 110, ZF, 1.0) + fig(ben("bn5", "confused", arm=("down", "front"), extra=bag("bn5x", 196, -330, -20, 220)), 330, ZF, 1.0) +
          fig(theo("t9", "confused"), 560, ZF, 1.0) + fig(oma("om8", "relief"), 790, ZF, 1.0) +
          fig(mia("m9", "grin", arm=("down", "down"), arm2=("down", "front"), extra='<g id="tally" opacity="0"><g transform="translate(196 -330)"><rect x="-40" y="-40" width="80" height="80" rx="10" fill="#fff" stroke="#111" stroke-width="4"/><path d="M-22 -24 V24 M-6 -24 V24 M10 -24 V24" stroke="#111" stroke-width="7"/></g></g>'), 990, ZF, 1.0) +
          '<g id="zpoof" opacity="0">' + "".join(f'<rect x="{x - 70}" y="{ZF - 700}" width="140" height="90" rx="44" fill="#fff" opacity=".85"/>' for x, _ in ZX) + '</g>')
# --- FM: Flohmarkt – Computer mit Preisschild „3 🍄“
S["FM"] = ('<rect width="1080" height="1920" fill="#bde0fe"/><rect x="-40" y="380" width="1160" height="140" fill="#ffafcc" stroke="#111" stroke-width="7"/>'
           + "".join(f'<path d="M{k * 120} 520 l60 80 l60 -80 Z" fill="{("#ffafcc", "#fff")[k % 2]}" stroke="#111" stroke-width="5"/>' for k in range(10)) +
           f'<text x="540" y="480" text-anchor="middle" style="font:900 80px {FONT};fill:#111">FLOHMARKT</text>'
           '<rect y="1260" width="1080" height="660" fill="#90be6d"/>' + computer("pc3", 680, 1420, .6) +
           '<rect x="300" y="1400" width="760" height="60" rx="10" fill="#bc6c25" stroke="#111" stroke-width="6"/>'
           f'<g id="tag3" opacity="0">{sign("tagS", ["PREIS: 3 🍄"], 680, 760, 440, size=64, col="#ffd166")}</g>' +
           fig(oma("om9", "joy", arm=("front", "down"), extra=f'<g id="omm">{mush(196, -400, 1.0)}{mush(150, -440, .9)}{mush(240, -430, .9)}</g>') + EB("eO9", "🍄", y=-660, vis=True), 220, FY, 1.2))
# --- Q: Mia hält Schild „ÜBER MIR: ___?“ (Schild 1105–1245 px = 58–65 %)
QSIGN = ('<g id="qs"><rect x="-340" y="0" width="680" height="140" rx="26" fill="#fff" stroke="#111" stroke-width="9"/>'
         f'<text x="0" y="95" text-anchor="middle" style="font:900 74px {FONT};fill:#111">ÜBER MIR: <tspan id="qemo" fill="#e63946">___?</tspan></text></g>')
S["Q"] = (street_bg() + fig(mia("m10", "grinwink", arm=("front", "front")), 540, FY - 100, 1.3) +
          f'<g transform="translate(540 1078)">{QSIGN}</g>' + f'<g transform="translate(540 {FY - 100})">{EB("eM10", "❤️", y=-680 * 1.3 + 40, size=110, vis=True, col="#ffe5ec")}</g>')
# --- E: Schluss – Straße Nacht wie Bild 0, ohne Zahlen (Loop-Fahrt)
S["E"] = (street_bg(night=True) + night_lamp() +
          '<g id="egh" opacity="0">' + f'<g transform="translate(540 {FY})">{admin("eA", size=66, y=-640 * 1.5)}</g>'
          f'<g transform="translate(175 {FY + 120})">{GB("eGm", "30.000", size=60, y=-640 * 1.2)}</g><g transform="translate(900 {FY + 120})">{RB("eGt", "1", size=96, y=-640 * 1.2)}</g></g>' +
          fig(oma("om10", "joy", arm=("hip", "down"), extra=BASKET), 540, FY, 1.5) +
          fig(mia("m11", "joy", arm=("down", "up")), 175, FY + 120, 1.2) +
          fig(theo("t11", "laugh", arm=("up", "down")), 900, FY + 120, 1.2) +
          '<g id="epoof" opacity="0">' + "".join(f'<rect x="{x - 90}" y="{y}" width="180" height="110" rx="54" fill="#fff" opacity=".85"/>' for x, y in ((540, 540), (175, 900), (900, 900))) + '</g>')

# ======================= Zeitplan =======================
J.append('tl.set("#cam", { x: 0, y: 0, scale: 1, svgOrigin: "0 0" }, 0);')
J.append('tl.set("#lever", { rotation: -30, svgOrigin: "0 -60" }, 0);')
s = st
def ww(sid, word, n=1, d=.1): return round(w(sid, word, n) - d, 2)
H_ = HEAD
t = {k: s(k) for k in T}
# s1: Bild 0 = Oma + ADMIN (Punch-Zoom 108→100 %, Plopp), Schnitt ≤ 1,5 s, Rückblick-Montage
cut(0, 540, 860, 1.08); cam(.02, 540, 860, 1.0, .45, "power2.out")
J.append('tl.fromTo("#aO0-in", { scale: 1.9, transformOrigin: "50% 50%" }, { scale: 1, duration: .3, ease: "back.out(2.4)", immediateRender: false }, 0);')
blink("#aO0-in", .4, 5, .12, .2)
FX += [("pop", 0, .5, .4), ("hit", .05, .3, .8)]
c1 = min(1.25, ww("s1", "Über") - .02)
ho0 = H_(540, FY, 1.5)
cut(c1, 540, ho0[1] - 110, 1.55); expr("om0", "wink", "grin", c1); FX += [("glitch", c1, .08, .3)]
tu = max(c1 + .6, ww("s1", "Über"))
ttg = ww("s1", "Tage"); thh = ww("s1", "hat", 1)
for k, (a, b) in enumerate(((tu, ttg), (ttg, thh), (thh, ww("s1", "Und")))):
    if k: J.append(f'tl.set("#r{k}", {{ opacity: 0 }}, {F(a)}); tl.set("#r{k + 1}", {{ opacity: 1 }}, {F(a)});')
    cut(a, 540, 900 - k * 30, 1.0 + .06 * (k % 2)); cam(a + .02, 540, 900, 1.1, max(.3, b - a), "none")
    FX += [("swoosh", a, .2, .4)]
tund = ww("s1", "Und")
cut(tund, 540, 1000, 1.15); expr("om0", "grin", "wink", tund)
tsy = ww("s1", "System")
cut(tsy, 540, ho0[1] - 110, 1.6); FX += [("hit", tsy, .3, .6)]; blink("#aO0-in", tsy, 5, .12, .2)
# s2: Antwort A – Pilz → Fernbedienung
ho2 = H_(470, FY, 1.55)
cut(t["s2"], 540, 1000, 1.2); FX += [("chime", t["s2"], .35, .8)]
tpz = ww("s2", "Pilz")
cut(tpz, 640, FY - 400 * 1.55, 1.6)
tfb = ww("s2", "Fernbedienung.", d=.15)
J.append(f'tl.to("#pmush", {{ scaleY: 0, transformOrigin: "50% 100%", duration: .15 }}, {F(tfb)});'); pop("#remote", tfb + .12, .3, "50% 100%")
cam(tfb + .1, 680, FY - 420 * 1.55, 1.85, .4, "power3.out"); FX += [("boing", tfb + .1, .4, .5)]
# s3: Keller – Riesencomputer von unten
cut(t["s3"], 540, 1500, 1.25); cam(t["s3"] + .03, 540, 900, 1.25, 1.2, "power2.inOut"); FX += [("whoosh", t["s3"], .4, .6), ("blips", t["s3"] + .3, .25, 1.2)]
J.append(f'tl.to("#pc [id^=pc-l]", {{ opacity: .3, duration: .12, yoyo: true, repeat: 40, stagger: {{ each: .05, from: "random" }}, ease: "steps(1)" }}, {F(t["s3"])});')
for j in range(2): J.append(f'tl.to("#pc-r{j}", {{ rotation: 720, transformOrigin: "50% 50%", duration: 6, ease: "none" }}, {F(t["s3"])});')
thk = ww("s3", "Häkeldeckchen.", d=.15)
cut(thk, 540, 760, 2.1); FX += [("pop", thk, .5, .3)]
# s4: Mia zeigt auf den Monitor – Ben 20.100 → 12.000
hm3 = H_(900, FY + 40, 1.15)
cut(t["s4"], 780, hm3[1] - 20, 1.6); expr("m3", "confused", "determined", t["s4"]); armswap("m3", t["s4"] + .2); FX += [("swoosh", t["s4"], .3, .4)]
J.append(f'tl.set("#scrBen", {{ opacity: 1 }}, {F(t["s4"])});')
tbn = ww("s4", "Ben")
cut(tbn, 540, 860, 1.05); FX += [("blips", tbn, .3, .5)]
tdn = ww("s4", "dann")
cam(tdn, 700, 760, 1.3, .3, "power3.out")
count("mNum", tdn + .05, 20100, 12000, .6); FX += [("glitch", tdn + .05, .2, .5)]
# s5: Rückblende – Ben futtert Pilze, Oma dreht am Rad
cut(t["s5"], 540, 1100, 1.1); cam(t["s5"] + .02, 540, 1000, 1.25, 1.2, "none"); FX += [("swoosh", t["s5"], .3, .4)]
J.append(f'tl.to("#pile", {{ scaleY: .1, transformOrigin: "50% 100%", duration: 1.0, ease: "steps(5)" }}, {F(t["s5"] + .2)});')
J.append(f'tl.fromTo("#bn1", {{ y: 0 }}, {{ y: -12, duration: .1, yoyo: true, repeat: 9, ease: "sine.inOut", immediateRender: false }}, {F(t["s5"] + .2)});')
FX += [("pop", t["s5"] + .3, .3, .2), ("pop", t["s5"] + .6, .3, .2), ("pop", t["s5"] + .9, .3, .2)]
tdh = ww("s5", "Da")
cut(tdh, 600, 900, 1.15); FX += [("tick", tdh, .3, 1.0)]
J.append(f'tl.to("#wheel", {{ rotation: -540, svgOrigin: "0 0", duration: 1.0, ease: "power2.inOut" }}, {F(tdh + .1)});')
count("drNum", tdh + .1, 20100, 12000, 1.0)
# s6: Krause parkt auf Omas Platz (Draufsicht)
cut(t["s6"], 540, 900, 1.0); cam(t["s6"] + .02, 540, 950, 1.12, 1.6, "none"); FX += [("whoosh", t["s6"], .4, .6)]
fly("#car", t["s6"] + .05, {"y": -900}, {"y": 0}, .8, "power2.out"); J.append('tl.set("#car", { y: -900 }, 0);')
tpp = ww("s6", "Parkplatz")
cut(tpp, 540, 1000, 1.25); pop("#pkO", tpp + .1, .3); FX += [("klong", tpp + .2, .3, .6)]
tmi = ww("s6", "Minus")
cut(tmi, 700, 1300, 1.3); FX += [("hit", tmi, .3, .6)]
# s7: Mia schockiert – Extrem-Nah
cut(t["s7"], hm3[0] - 10, hm3[1] + 20, 2.0); J.append(f'tl.set("#bM3", {{ opacity: 0 }}, {F(t["s7"])});'); expr("m3", "determined", "shock", t["s7"]); shake(t["s7"] + .05, 8, 14); FX += [("hit", t["s7"], .4, .8)]
tne = ww("s7", "nie")
cam(tne, hm3[0] - 10, hm3[1] + 40, 2.25, .25, "power3.out")
# s8: Oma lächelt, Lach-Zähler
ho3 = H_(185, FY + 40, 1.15)
cut(t["s8"], 300, ho3[1] + 10, 1.6); expr("om3", "wink", "happy", t["s8"]); FX += [("chime", t["s8"], .3, .6)]
tla = ww("s8", "lachen.")
cut(tla, 330, ho3[1] + 30, 1.9); expr("om3", "happy", "laugh", tla)
# s9 / s10 / s11 / s12 in der Reihe + Monitor + Knopf
ht3 = H_(AX["t"], FY, AS)
cut(t["s9"], AX["t"], ht3[1] - 40, 1.6); J.append(f'tl.set("#aO6", {{ opacity: 0 }}, {F(t["s9"])}); tl.set("#aO6", {{ opacity: 1 }}, {F(t["s10"])});'); expr("t3", "neutral", "confused", t["s9"]); FX += [("swoosh", t["s9"], .3, .4)]
J.append(f'tl.set("#mErr", {{ opacity: 1 }}, {F(t["s10"])}); tl.set("#mBen", {{ opacity: 0 }}, {F(t["s10"])});')
cut(t["s10"], 540, 760, 1.05); shake(t["s10"] + .3, 6, 10); FX += [("glitch", t["s10"], .3, .6)]
tpg = ww("s10", "Programm")
cut(tpg, 540, 700, 1.25); J.append(f'tl.fromTo("#smoke", {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: -60, duration: 1.0, immediateRender: false }}, {F(tpg)});'); FX += [("splat", tpg + .3, .3, .6)]
hb2 = H_(300, FY, 1.45)
cut(t["s11"], 540, 1500, 1.15); cam(t["s11"] + .02, 450, 1300, 1.25, 1.0, "none"); FX += [("whoosh", t["s11"], .3, .5)]
tkn = ww("s11", "Knopf.")
cut(tkn, 780, 900, 1.6); FX += [("riser", tkn, .2, 1.5)]
tbg = ww("s11", "Baguette.")
cut(tbg, 640, 1050, 1.35); J.append(f'tl.to("#bgt", {{ rotation: 25, svgOrigin: "196 -330", duration: .2, ease: "power3.in" }}, {F(tbg + .05)}); tl.to("#btn", {{ y: 30, duration: .1 }}, {F(tbg + .25)});')
expr("bn2", "determined", "grin", tbg)
# s12: Bzzzt – alle Zahlen → Emojis
t12 = t["s12"]
J.append(f'tl.to("#btfl", {{ opacity: .9, duration: .05, yoyo: true, repeat: 3, ease: "steps(1)" }}, {F(t12 - .05)});')
cut(t12, 540, 900, 1.0); FX += [("glitch", t12 - .25, .12, .3), ("hit", ww("s12", "Emojis.", d=.15), .25, .6)]; shake(t12, 10, 18)
J.append(f'tl.to("#allfl", {{ opacity: .8, duration: .06, yoyo: true, repeat: 5, ease: "steps(1)" }}, {F(t12)}); tl.set("#allfl", {{ opacity: 0 }}, {F(t12 + .45)});')
tem = ww("s12", "Emojis.", d=.15)
for b, e in (("bB3", "eB3"), ("bT3", "eT3"), ("aO6", "eO6"), ("bM6", "eM6")):
    J.append(f'tl.to("#{b}-in", {{ x: 10, duration: .05, yoyo: true, repeat: 7, ease: "steps(1)" }}, {F(t12 + .1)}); tl.set("#{b}", {{ opacity: 0 }}, {F(tem)});')
    pop(f"#{e}", tem, .3, "50% 50%")
for f_, e_ in (("bn3", "neutral"), ("t3", "confused"), ("om6", "relief"), ("m6", "worried")): expr(f_, e_, "shock", t12 + .1)
FX += [("pop", tem, .5, .3), ("pop", tem + .1, .5, .3)]
cam(tem, 540, 860, 1.12, .4, "power2.out")
# s13: Ben 🥖, Theo 🐔
hb3 = H_(AX["bn"], FY, AS)
cut(t["s13"], 300, hb3[1] - 60, 1.8); expr("bn3", "shock", "joy", t["s13"]); FX += [("boing", t["s13"], .35, .4)]
J.append(f'tl.fromTo("#eB3-in", {{ rotation: -12, transformOrigin: "50% 50%" }}, {{ rotation: 12, duration: .2, yoyo: true, repeat: 5, immediateRender: false }}, {F(t["s13"])});')
tth = ww("s13", "Theo:")
cut(tth, AX["t"], ht3[1] - 60, 1.9); expr("t3", "shock", "annoyed", tth); FX += [("pop", tth + .3, .5, .3)]
# s14: Schulklo – 🧻 + BESETZT!
cut(t["s14"], 540, 820, 1.05); pop("#eKL", t["s14"] + .1, .3, "50% 50%"); FX += [("pop", t["s14"] + .1, .5, .3)]
tbs = ww("s14", "Besetzt!", d=.15)
cut(tbs, 640, 1000, 1.3); pop("#bubKL", tbs, .2, "50% 50%"); shake(tbs, 7, 12); FX += [("klong", tbs, .4, .6)]
# s15: Oma mit tanzendem 🍄
ho6 = H_(AX["om"], FY, AS)
cut(t["s15"], 680, ho6[1] - 40, 1.7); expr("om6", "shock", "joy", t["s15"]); FX += [("boing", t["s15"], .35, .5)]
td = ww("s15", "tanzender")
cut(td, 680, ho6[1] - 140, 2.1); wobble("#eO6-in", td, 9, 14, .15, "rotation", "50% 100%"); FX += [("blips", td, .3, .8)]
# s16: Mia ❤️ – langsamer Zoom
hm6 = H_(AX["m"], FY, AS)
cut(t["s16"], 800, hm6[1] - 40, 1.6); cam(t["s16"] + .02, 800, hm6[1] - 60, 1.9, max(.5, t["s17"] - t["s16"] - .1), "none"); expr("m6", "shock", "hope", t["s16"])
J.append(f'tl.to("#eM6-in", {{ scale: 1.2, transformOrigin: "50% 50%", duration: .3, yoyo: true, repeat: 5, ease: "sine.inOut" }}, {F(t["s16"])});'); FX += [("chime", t["s16"], .35, .8)]
# s17: Riesenhebel von unten
cut(t["s17"], 700, 1400, 1.2); cam(t["s17"] + .02, 650, 1000, 1.2, 1.0); FX += [("klong", t["s17"], .3, .6)]
tan = ww("s17", "An")
cut(tan, 700, 900, 1.5)
tme = ww("s17", "Mia")
J.append(f'tl.set("#hbM", {{ opacity: 1 }}, {F(tme)});'); cut(tme, 510, H_(510, FY + 80, 1.3)[1] - 40, 1.6); FX += [("swoosh", tme, .3, .4)]
# s18: Split AN/AUS
cut(t["s18"], 270, 1100, 1.15); FX += [("pop", t["s18"], .5, .3)]
tau = ww("s18", "Aus:")
cut(tau, 810, 1100, 1.15); FX += [("pop", tau, .5, .3)]
# s19: Ben umarmt Baguette
cut(t["s19"], 540, 980, 1.15); cam(t["s19"] + .02, 540, 980, 1.25, 1.5, "none"); FX += [("boing", t["s19"] + .2, .35, .4)]
wobble("#bn4", t["s19"] + .1, 5, 4, .2)
# s20: Rückblende-Montage + Trommelwirbel
t20, t21 = t["s20"], t["s21"]
ts20 = [t20, ww("s20", "Die"), ww("s20", "Das")]
for k, a in enumerate(ts20):
    if k: J.append(f'tl.set("#q{k}", {{ opacity: 0 }}, {F(a)}); tl.set("#q{k + 1}", {{ opacity: 1 }}, {F(a)});')
    cut(a, 540, 900 + (k % 2) * 60, 1.0 + .08 * (k % 2)); cam(a + .02, 540, 900, 1.15, 1.0, "none")
    FX += [("swoosh", a, .2, .4)]
FX += [("wirbel", t20 + .2, .35, max(1.0, t21 - t20 + .6))]
# s21: Mia zieht – KLACK – AUS
hm7 = H_(510, FY + 80, 1.3)
cut(t21, 560, hm7[1] - 20, 1.7); expr("m7", "determined", "grin", t21)
tkl = ww("s21", "Klack.", d=.05)
J.append(f'tl.to("#lever", {{ rotation: 30, svgOrigin: "0 -60", duration: .18, ease: "power4.in" }}, {F(tkl - .12)});')
cut(tkl, 540, 900, 1.0); J.append(f'tl.set("#hbSp", {{ opacity: 1 }}, {F(tkl)}); tl.set("#hbSp", {{ opacity: 0 }}, {F(tkl + .5)});')
J.append(f'tl.to("#hbfl", {{ opacity: .9, duration: .05, yoyo: true, repeat: 3, ease: "steps(1)" }}, {F(tkl)});')
J.append(f'tl.set("#eO7, #eM7", {{ opacity: 0 }}, {F(tkl + .1)});')
FX += [("hit", tkl, .45, 1.0), ("klong", tkl, .35, .8)]; shake(tkl, 9, 18)
tas = ww("s21", "Aus.")
cam(tas, 600, 950, 1.1, .3, "power3.out")
# s22: Über allen Köpfen: nichts
cut(t["s22"], 540, 900, 1.0); cam(t["s22"] + .02, 540, 980, 1.1, 1.5, "none"); FX += [("whoosh", t["s22"], .3, .6)]
J.append(f'tl.set("#zpoof", {{ opacity: 1 }}, {F(t["s22"])}); tl.to("#zpoof", {{ opacity: 0, scale: 1.4, transformOrigin: "50% 50%", duration: .5 }}, {F(t["s22"] + .05)});')
tni = ww("s22", "nichts.")
cut(tni, 560, 1000, 1.3)
for k, (_, p) in enumerate(ZX[:4]):
    pass
# s23: Mia grinst, Strichzähler, Ben + Theo lachen
cut(t["s23"], 900, 980, 1.6); J.append(f'tl.set("#tally", {{ opacity: 1 }}, {F(t["s23"])});'); armswap("m9", t["s23"] + .1)
tlz = ww("s23", "zählen")
cut(tlz, 450, 1000, 1.4); expr("bn5", "confused", "joy", tlz); expr("t9", "confused", "laugh", tlz); expr("kr2", "confused", "laugh", tlz)
J.append(f'tl.fromTo("#t9, #bn5", {{ y: 0 }}, {{ y: -16, duration: .12, yoyo: true, repeat: 11, ease: "sine.inOut", immediateRender: false }}, {F(tlz)});'); FX += [("blips", tlz, .3, .8)]
# s24: Flohmarkt
cut(t["s24"], 540, 900, 1.05); cam(t["s24"] + .02, 450, 960, 1.2, 1.5, "none"); FX += [("swoosh", t["s24"], .3, .5)]
tdp = ww("s24", "drei")
cut(tdp, 680, 820, 1.5); pop("#tag3", tdp, .3, "50% 50%"); FX += [("pop", tdp, .5, .3), ("chime", tdp + .3, .3, .8)]
# s25: Mia mit Schild „ÜBER MIR: ___?“
cut(t["s25"], 540, 940, 1.0); FX += [("pop", t["s25"], .5, .3)]
J.append(f'tl.fromTo("#qs", {{ scale: .3, opacity: 0, transformOrigin: "50% 50%" }}, {{ scale: 1, opacity: 1, duration: .3, ease: "back.out(2.4)", immediateRender: false }}, {F(t["s25"] + .05)});')
temo = ww("s25", "Emoji")
tkm = ww("s25", "Kommentare!"); cut(tkm, 540, 900, 1.0); expr("m10", "grinwink", "grin", tkm); wobble("#qs", tkm, 3, 3, .15, "rotation", "50% 50%")
J.append(f'tl.to("#qemo", {{ opacity: .2, duration: .15, yoyo: true, repeat: 9, ease: "steps(1)" }}, {F(temo)});')
# s26: Folg … Loop-Fahrt zurück auf Bild 0 (Nacht-Straße), Zahlen geistern kurz, dann weg
t26 = t["s26"]
tfo = ww("s26", "Folg,")
cut(t26, 540, 900, 1.4); expr("m10", "grin", "joy", t26); J.append(f'tl.set("#qs", {{ opacity: 0 }}, {F(t26)});')
tin = ww("s26", "In")
ho10 = H_(540, FY, 1.5)
cut(tin, 540, ho10[1] - 40, 1.6); cam(tin + .02, 540, 860, 1.0, max(1.0, END - tin - .2), "sine.inOut"); FX += [("whoosh", tin, .3, .6)]
tza = ww("s26", "Zahl.")
J.append(f'tl.fromTo("#egh", {{ opacity: 0 }}, {{ opacity: .9, duration: .15, immediateRender: false }}, {F(tza)});')
tjn = ww("s26", "Jetzt")
J.append(f'tl.set("#egh", {{ opacity: 0 }}, {F(tjn + .25)}); tl.set("#epoof", {{ opacity: 1 }}, {F(tjn + .25)}); tl.to("#epoof", {{ opacity: 0, scale: 1.4, transformOrigin: "50% 50%", duration: .5 }}, {F(tjn + .3)});')
FX += [("pop", tjn + .25, .5, .3)]
J.append(f'tl.fromTo("#m11, #t11", {{ y: 0 }}, {{ y: -18, duration: .14, yoyo: true, repeat: {int((END - tjn) / .14)}, ease: "sine.inOut", immediateRender: false }}, {F(tjn + .3)});')
expr("om10", "joy", "grin", tjn + .3)

sets = [("A0", 0, tu), ("RS", tu, tund), ("A0", tund, t["s2"]), ("P", t["s2"], t["s3"]), ("K", t["s3"], tbn), ("M", tbn, t["s5"]), ("BP", t["s5"], tdh), ("DR", tdh, t["s6"]),
        ("PK", t["s6"], t["s7"]), ("K", t["s7"], t["s9"]), ("ALL", t["s9"], t["s10"]), ("M", t["s10"], t["s11"]), ("BT", t["s11"], t12), ("ALL", t12, t["s14"]),
        ("KL", t["s14"], t["s15"]), ("ALL", t["s15"], t["s17"]), ("HB", t["s17"], t["s18"]), ("SP", t["s18"], t["s19"]), ("BU", t["s19"], t20), ("RM", t20, t21),
        ("HB", t21, t["s22"]), ("Z", t["s22"], t["s24"]), ("FM", t["s24"], t["s25"]), ("Q", t["s25"], tin), ("E", tin, END)]

SM = lambda txt, px=46: f"<span style='font-size:{px}px'>{txt}</span>"
OBEN = [(0, SM("IN DIESER WELT:<br>DEINE ZAHL = TAGE, DIE DU NOCH HAST", 46)), (c1, "ÜBER OMA HILDE: <span style='color:#39ff14'>ADMIN</span>"),
        (tu, "⏪ WAS BISHER GESCHAH"), (tund, "OMA HILDE = <span style='color:#39ff14'>ADMIN</span>"), (t["s2"], "ANTWORT A ✅"), (t["s3"], "SYSTEM v1.0"),
        (t["s4"], "BEN: 20.100 → 12.000"), (t["s5"], "−8.100 🍄"), (t["s6"], "KRAUSE: 15.200 → 9.000"), (tmi, "−6.200 🚗"), (t["s7"], "NIE ECHT?!"),
        (t["s8"], "😂 = ZIEL"), (t["s9"], "THEO: — (3 JAHRE)"), (t["s10"], "ABGESTÜRZT 💥"), (t["s11"], "BEN WILL ADMIN SEIN"), (t12, "BZZZT ⚡"),
        (tem, "ZAHLEN → EMOJIS"), (t["s14"], "SCHULKLO: 🧻"), (t["s15"], "OMA HILDE: 🍄"), (t["s16"], "MIA: ❤️"), (t["s17"], "AN ODER AUS?"),
        (t["s18"], "AN = ZAHLEN | AUS = NICHTS"), (t["s19"], "🥖?"), (t20, "⏪ 1 · 100/100 · 🐔"), (tkl, "KLACK – AUS"), (t["s22"], "0 ZAHLEN"),
        (t["s23"], "LACHER: 1, 2, 3 …"), (t["s24"], "PREIS: 3 🍄"), (t["s25"], "DEIN EMOJI? 👇"), (tin, "DIE ZAHL ÜBER DEM KOPF – ENDE")]
tag = ('<div class="ui clip" data-start="0" data-duration="{0}" style="left:30px;top:30px;font:900 40px Inter,sans-serif;color:#fff;background:#e63946;border:4px solid #111;padding:4px 18px;border-radius:12px">FINALE</div>').format(F(END))
HOT = {"OMA", "HILDE", "ADMIN", "A", "PILZ", "FERNBEDIENUNG", "RIESENCOMPUTER", "HÄKELDECKCHEN", "BEN", "PILZE", "KRAUSE", "PARKPLATZ", "NIE", "ECHT", "LACHT",
       "THEO", "ZAHL", "ABGESTÜRZT", "KNOPF", "BAGUETTE", "BZZZT", "EMOJIS", "HUHN", "KLOPAPIER", "BESETZT", "TANZT", "HERZ", "AN", "AUS", "MIA", "EINS",
       "LACHER", "HÜHNERKOSTÜM", "KLACK", "NICHTS", "SELBST", "FLOHMARKT", "EMOJI", "KOMMENTARE", "WELT", "FOLG", "NICHT", "MEHR", "ZAHLEN"}
cam_fix()
finish(S, sets, OBEN, FX, HOT, tag, banner=("<span style='display:block;font-size:62px;-webkit-text-stroke:0;text-shadow:0 4px 0 #111;margin-bottom:14px'>MORGEN NEUE WELT</span>", "➕ FOLGEN"),
       oben_top=110, banner_top=300, cap_top=1250)
