"""STORY-FORMAT „In dieser Stadt …“ – NEUE SERIE „Die Kompliment-Stadt“, TEIL 1: „In dieser Stadt bezahlt man mit Komplimenten“.
Aufruf: python3 tools/kompliment1.py  (liest voice.json (= voice-kompliment1.json) + assets/vo/timing.json; Bausteine aus tools/bausteine.py + Helfer aus liefer1.py;
Musik = fester Hintergrund-Sound assets/bgm.mp3 über tools/story_musik.py). Regeln Trend-Scout 25.11.: Bild 0 = Krause pleite auf dem Bordstein mit Punch-Zoom,
Konto-Zähler oben links, Untertitel bei 65 %, Ende Schild „DEIN BESTES KOMPLIMENT: ___?“ + Loop-Fahrt auf Bild 0, Endbanner „TEIL 2? ➕ FOLGEN“ nur einmal."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bausteine import *

# ---------- zusätzliche Mimik / Haare / Zubehör ----------
FACES["sneeze"] = ('<path d="M-46 -4 L-16 -4 M16 -4 L46 -4" stroke="#111" stroke-width="8" stroke-linecap="round"/><path d="M-50 -24 L-14 -14 M50 -24 L14 -14" stroke="#111" stroke-width="6" stroke-linecap="round"/>'
                   '<ellipse cx="0" cy="40" rx="22" ry="20" fill="#5a1a1a" stroke="#111" stroke-width="4"/>')
FACES["angry"] = (E(-30, 2) + E(30, 2) + '<path d="M-52 -34 L-12 -14 M52 -34 L12 -14" stroke="#111" stroke-width="9" stroke-linecap="round"/>'
                  '<path d="M-26 46 Q0 28 26 46" stroke="#111" stroke-width="8" fill="none" stroke-linecap="round"/>')
FACES["shout"] = (E(-30, 0) + E(30, 0) + '<path d="M-52 -34 L-12 -16 M52 -34 L12 -16" stroke="#111" stroke-width="9" stroke-linecap="round"/>'
                  '<rect x="-34" y="18" width="68" height="56" rx="18" fill="#5a1a1a" stroke="#111" stroke-width="5"/><rect x="-24" y="20" width="48" height="10" fill="#fff"/>')
FACES["yawn"] = ('<path d="M-46 -2 H-14 M14 -2 H46" stroke="#111" stroke-width="7" stroke-linecap="round"/>'
                 '<ellipse cx="0" cy="44" rx="24" ry="30" fill="#5a1a1a" stroke="#111" stroke-width="5"/>')
FACES["whisper"] = (E(-30, -6) + E(30, -6) + '<path d="M-48 -30 L-14 -24 M48 -30 L14 -24" stroke="#111" stroke-width="6" stroke-linecap="round"/>')
HAIR["ich"] = lambda c: f'<path d="M-100 -36 V-100 Q-100 -114 -86 -114 H86 Q100 -114 100 -100 V-36 L74 -64 L40 -80 L0 -66 L-40 -84 L-76 -62 Z" fill="{c}" stroke="#111" stroke-width="4"/>'
HAIR["cap"] = lambda c: (f'<path d="M-104 -60 Q-104 -150 0 -150 Q104 -150 104 -60 Z" fill="{c}" stroke="#111" stroke-width="5"/><rect x="-20" y="-82" width="190" height="26" rx="10" fill="{c}" stroke="#111" stroke-width="4"/>')
HAIR["hut"] = lambda c: ('<path d="M-100 -30 V-90 L-80 -70 H80 L100 -90 V-30 Z" fill="#ccc"/><rect x="-140" y="-120" width="280" height="30" rx="10" fill="#111"/><rect x="-80" y="-250" width="160" height="140" rx="10" fill="#111"/><rect x="-80" y="-150" width="160" height="26" fill="#e63946"/>')
HAIR["backhead"] = lambda c: f'<rect x="-96" y="-96" width="192" height="150" rx="26" fill="{c}" stroke="#111" stroke-width="4"/>'

YEL = "#ffd60a"
JACKE = '<path d="M0 -296 V-64" stroke="#111" stroke-width="6"/><path d="M-60 -300 L0 -250 L60 -300" stroke="#111" stroke-width="6" fill="#f4c20d"/><rect x="-80" y="-170" width="50" height="40" rx="8" fill="#f4c20d" stroke="#111" stroke-width="4"/><rect x="30" y="-170" width="50" height="40" rx="8" fill="#f4c20d" stroke="#111" stroke-width="4"/>'
ICH_EX = ("happy", "shock", "laugh", "determined", "panic", "neutral", "shout", "whisper", "sad")
def ich(uid, start="happy", arm=("down", "down"), extra="", behind="", head_acc=""):
    return person(uid, "ich", "#6b3e26", YEL, exprs=ICH_EX, start=start, arm=arm, extra=JACKE + extra, behind=behind, head_acc=head_acc)
MALTE_EX = ("happy", "yawn", "shock", "panic", "sneeze", "confused", "shout", "laugh")
def malte(uid, start="happy", arm=("down", "down"), extra=""):
    return person(uid, "cap", "#38b000", "#3a86ff", skin="#c68642", exprs=MALTE_EX, start=start, arm=arm, extra=extra)
SOCK = lambda x, y, c: f'<path d="M{x} {y} v30 h16 v-30 z M{x} {y + 30} h28 v14 h-28 z" fill="{c}" stroke="#111" stroke-width="3"/>'
OMA_SOCKS = "".join(SOCK(x, y, c) for x, y, c in ((-70, -270, "#ffd166"), (20, -265, "#ef476f"), (-40, -190, "#06d6a0"), (40, -180, "#ffd166"), (-80, -130, "#ef476f"), (10, -120, "#118ab2")))
OMA_ACC = '<rect x="-64" y="-20" width="46" height="34" rx="16" fill="none" stroke="#555" stroke-width="5"/><rect x="18" y="-20" width="46" height="34" rx="16" fill="none" stroke="#555" stroke-width="5"/>'
def oma(uid, start="relief", arm=("down", "down"), extra="", behind=""):
    return person(uid, "oma", "#e0e0e0", "#9d4edd", exprs=("relief", "happy", "shock", "laugh", "grin"), start=start, arm=arm, extra=OMA_SOCKS + extra, head_acc=OMA_ACC, behind=behind)
KR_ACC = '<rect x="-62" y="-22" width="48" height="36" rx="8" fill="none" stroke="#111" stroke-width="6"/><rect x="14" y="-22" width="48" height="36" rx="8" fill="none" stroke="#111" stroke-width="6"/><path d="M-14 -6 H14" stroke="#111" stroke-width="6"/>'
KETTE = ('<path d="M-80 -296 Q0 -170 80 -296" stroke="#d4a017" stroke-width="14" fill="none" stroke-dasharray="16 8"/>'
         '<rect x="-30" y="-230" width="60" height="60" rx="30" fill="#ffd166" stroke="#111" stroke-width="5"/>')
def bm(uid, start="neutral", arm=("down", "down"), extra=""):
    return person(uid, "hut", "#ccc", "#264653", exprs=("neutral", "shock", "shout", "angry", "determined", "happy"), start=start, arm=arm, extra=KETTE + extra)

def drone(uid, x, y, s=1.0, cargo="", hov=True):
    """Neutrale weiße Liefer-Drohne (kein Logo). Ursprung = Mitte des Rumpfs, Fracht hängt darunter."""
    rot = "".join(f'<rect x="{dx - 6}" y="-56" width="12" height="30" fill="#555"/><ellipse class="rot" cx="{dx}" cy="-58" rx="80" ry="11" fill="#adb5bd" stroke="#111" stroke-width="4" opacity=".85"/>' for dx in (-170, 170))
    body = (f'<rect x="-190" y="-34" width="380" height="18" rx="9" fill="#ced4da" stroke="#111" stroke-width="4"/>{rot}'
            '<rect x="-80" y="-48" width="160" height="80" rx="26" fill="#fff" stroke="#111" stroke-width="6"/>'
            '<rect x="-24" y="10" width="48" height="34" rx="14" fill="#111"/><rect x="-10" y="20" width="14" height="12" rx="5" fill="#4cc9f0"/>'
            '<rect x="50" y="-36" width="16" height="16" rx="8" fill="#2dc653"/>')
    inner = f'<g class="hov">{cargo}{body}</g>' if hov else f'{cargo}{body}'
    return f'<g transform="translate({x} {y}) scale({s})"><g id="{uid}">{inner}</g></g>'
ROPE = lambda L: f'<path d="M-40 30 L-80 {L} M40 30 L80 {L}" stroke="#333" stroke-width="5"/>'
def parcel(w_=140, h=110, y0=200, lab=""):
    return (f'{ROPE(y0)}<rect x="{-w_ / 2}" y="{y0}" width="{w_}" height="{h}" rx="10" fill="#d4a373" stroke="#111" stroke-width="6"/>'
            f'<rect x="-14" y="{y0}" width="28" height="{h}" fill="#e9c46a" stroke="#111" stroke-width="3"/>' +
            (f'<text x="0" y="{y0 + h / 2 + 14}" text-anchor="middle" style="font:900 34px {FONT};fill:#111">{lab}</text>' if lab else ""))

def elephant(uid, x, fy, s, face="happy", heft=False, tag=True):
    G = "#9aa5b1"; D = "#7d8995"
    eye = {"happy": '<path d="M-350 -468 Q-334 -484 -318 -468" stroke="#111" stroke-width="8" fill="none" stroke-linecap="round"/>',
           "shock": WEYE(-334, -470, -4, 0), "panic": WEYE(-334, -470, -4, -6) + '<path d="M-290 -540 q-12 24 0 32 q12 -8 0 -32" fill="#4cc9f0" stroke="#111" stroke-width="2"/>'}
    eyes = "".join(f'<g id="{uid}-e{k}" opacity="{1 if k == face else 0}">{v}</g>' for k, v in eye.items())
    hf = (f'<g id="{uid}-heft" opacity="{1 if heft else 0}" transform="rotate(-18 -500 -120)"><rect x="-600" y="-200" width="190" height="140" rx="8" fill="#fff" stroke="#111" stroke-width="6"/>'
          + "".join(f'<path d="M-585 {-170 + k * 24} H-425" stroke="#8ecae6" stroke-width="4"/>' for k in range(5)) +
          f'<rect x="-600" y="-200" width="190" height="34" fill="#e63946" stroke="#111" stroke-width="6"/><text x="-505" y="-174" text-anchor="middle" style="font:900 24px {FONT};fill:#fff">HAUSAUFGABEN</text>'
          '<path d="M-470 -60 l12 22 l14 -24 l12 22" stroke="#111" stroke-width="4" fill="none"/></g>')
    tg = (f'<path d="M-250 -330 L-210 -270 L-170 -330" stroke="#111" stroke-width="5" fill="none"/><rect x="-300" y="-280" width="180" height="70" rx="14" fill="{YEL}" stroke="#111" stroke-width="6"/>'
          f'<text x="-210" y="-230" text-anchor="middle" style="font:900 46px {FONT};fill:#111">KEVIN</text>') if tag else ""
    return (f'<g transform="translate({x} {fy}) scale({s})"><g id="{uid}"><ellipse cx="-20" cy="6" rx="320" ry="30" fill="#000" opacity=".22"/>'
            f'<path d="M230 -330 Q300 -300 290 -220" stroke="#111" stroke-width="18" fill="none"/>'
            + "".join(f'<rect x="{lx}" y="-170" width="84" height="172" rx="16" fill="{G if k % 2 else D}" stroke="#111" stroke-width="7"/>' for k, lx in enumerate((-250, -130, 50, 150))) +
            f'<rect x="-270" y="-440" width="520" height="310" rx="70" fill="{G}" stroke="#111" stroke-width="8"/><rect x="-270" y="-440" width="520" height="310" rx="70" fill="url(#shade)"/>'
            f'<path id="{uid}-trunk" d="M-370 -330 Q-400 -200 -470 -150 Q-500 -120 -470 -96" stroke="#111" stroke-width="66" fill="none" stroke-linecap="round"/><path d="M-370 -330 Q-400 -200 -470 -150 Q-500 -120 -470 -96" stroke="{G}" stroke-width="52" fill="none" stroke-linecap="round"/>'
            f'<rect x="-420" y="-580" width="250" height="270" rx="60" fill="{G}" stroke="#111" stroke-width="8"/>'
            f'<rect x="-250" y="-590" width="170" height="250" rx="50" fill="{D}" stroke="#111" stroke-width="7"/><rect x="-225" y="-560" width="120" height="190" rx="40" fill="#f4acb7" opacity=".55"/>'
            f'<path d="M-330 -350 Q-370 -300 -420 -320" stroke="#111" stroke-width="22" fill="none" stroke-linecap="round"/><path d="M-330 -350 Q-370 -300 -420 -320" stroke="#fff" stroke-width="13" fill="none" stroke-linecap="round"/>'
            f'{eyes}<rect x="-400" y="-430" width="36" height="22" rx="8" fill="#ff8fa3" opacity=".6"/>{tg}{hf}</g></g>')

def mouse(x, y, s=1.0, rot=0, cls="mz"):
    return (f'<g transform="translate({x} {y}) rotate({rot}) scale({s})"><g class="{cls}">'
            '<path d="M50 10 Q100 0 110 -40" stroke="#111" stroke-width="6" fill="none"/>'
            '<rect x="-60" y="-40" width="120" height="70" rx="30" fill="#adb5bd" stroke="#111" stroke-width="5"/>'
            '<rect x="-74" y="-80" width="44" height="44" rx="22" fill="#ffafcc" stroke="#111" stroke-width="5"/><rect x="-10" y="-84" width="44" height="44" rx="22" fill="#ffafcc" stroke="#111" stroke-width="5"/>'
            '<rect x="-66" y="-30" width="12" height="12" rx="4" fill="#111"/><rect x="-80" y="-6" width="14" height="12" rx="6" fill="#ff5d8f"/>'
            '<path d="M-20 30 L-34 60 H6 L-6 30 Z" fill="#dee2e6" stroke="#111" stroke-width="4"/><path d="M-32 34 Q-14 6 4 34" stroke="#111" stroke-width="3" fill="none"/></g></g>')

def pillow(x, y, w_, h, c, r=0):
    return (f'<g transform="translate({x} {y}) rotate({r})"><rect x="{-w_ / 2}" y="{-h / 2}" width="{w_}" height="{h}" rx="{h * .4:.0f}" fill="{c}" stroke="#111" stroke-width="6"/>'
            f'<rect x="{-w_ / 2 + 14}" y="{-h / 2 + 14}" width="{w_ - 28}" height="{h - 28}" rx="{h * .3:.0f}" fill="none" stroke="#111" stroke-width="3" stroke-dasharray="10 8"/></g>')

def puff(uid, x, y, r=60, txt="PUFF"):
    return (f'<g id="{uid}" opacity="0" transform="translate({x} {y})">' + "".join(f'<rect x="{dx - r / 2:.0f}" y="{dy - r / 2:.0f}" width="{r}" height="{r}" rx="{r / 2:.0f}" fill="#fff" stroke="#111" stroke-width="4"/>'
            for dx, dy in ((-r, 0), (r, 0), (0, -r), (0, r * .6), (-r * .7, -r * .7), (r * .7, -r * .7))) +
            f'<text x="0" y="{r * .25:.0f}" text-anchor="middle" style="font:900 {r * .7:.0f}px {FONT};fill:#e63946;stroke:#111;stroke-width:3px;paint-order:stroke">{txt}</text></g>')
def plopp(uid, t, d=.45):
    J.append(f'tl.fromTo("#{uid}", {{ opacity: 1, scale: .3, transformOrigin: "50% 50%" }}, {{ opacity: 0, scale: 1.5, duration: {d}, ease: "power2.out", immediateRender: false }}, {F(t)});')
def wrap(uid, content, x, fy, s):
    return f'<g transform="translate({x} {fy})"><g id="{uid}" transform="scale({s})">{content}</g></g>'
def ortsschild(x, y, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s})"><rect x="-200" y="120" width="24" height="560" fill="#868e96" stroke="#111" stroke-width="5"/><rect x="176" y="120" width="24" height="560" fill="#868e96" stroke="#111" stroke-width="5"/>'
            f'<rect x="-310" y="-170" width="620" height="330" rx="22" fill="{YEL}" stroke="#111" stroke-width="10"/><rect x="-290" y="-150" width="580" height="290" rx="14" fill="none" stroke="#111" stroke-width="6"/>'
            f'<text x="0" y="-40" text-anchor="middle" style="font:900 96px {FONT};fill:#111">LIEFERSTADT</text>'
            f'<text x="0" y="40" text-anchor="middle" style="font:800 40px {FONT};fill:#111">Was du laut sagst,</text>'
            f'<text x="0" y="96" text-anchor="middle" style="font:800 40px {FONT};fill:#111">wird geliefert.</text></g>')
def sky(c="#8ecae6"):
    return (f'<rect width="1080" height="1920" fill="{c}"/><rect x="150" y="230" width="200" height="70" rx="35" fill="#fff" opacity=".9"/><rect x="200" y="200" width="110" height="70" rx="35" fill="#fff" opacity=".9"/>'
            '<rect x="720" y="420" width="220" height="70" rx="35" fill="#fff" opacity=".8"/>')
def city_skyline(y=1300, c="#577590"):
    out = ""
    for k, (wd, h) in enumerate(((160, 380), (120, 520), (180, 300), (140, 620), (200, 420), (130, 500), (170, 340))):
        x = sum(v[0] for v in ((160, 0), (120, 0), (180, 0), (140, 0), (200, 0), (130, 0), (170, 0))[:k]) - 30
        out += f'<rect x="{x}" y="{y - h}" width="{wd}" height="{h}" fill="{c}" stroke="#111" stroke-width="4"/>' + "".join(
            f'<rect x="{x + 20 + (j % 2) * (wd - 70)}" y="{y - h + 30 + (j // 2) * 80}" width="30" height="40" fill="#ffe066" opacity=".8"/>' for j in range(min(8, h // 80 * 2)))
    return out
HANDMOUTH = ('<path d="M90 -250 Q150 -300 40 -360" stroke="#111" stroke-width="50" fill="none" stroke-linecap="round"/><path d="M90 -250 Q150 -300 40 -360" stroke="' + YEL + '" stroke-width="40" fill="none" stroke-linecap="round"/>'
             '')
HANDFACE = ('<g transform="rotate(-12 0 40)">' + "".join(f'<rect x="{-52 + k * 26}" y="{4 + abs(k - 1.5) * 6:.0f}" width="26" height="{78 - abs(k - 1.5) * 10:.0f}" rx="12" fill="#f2c9a5" stroke="#111" stroke-width="4"/>' for k in range(4)) +
            '<rect x="-56" y="56" width="108" height="40" rx="14" fill="#f2c9a5" stroke="#111" stroke-width="4"/></g>')
MEGA = ('<path d="M-90 -250 Q-170 -320 -110 -380" stroke="#111" stroke-width="50" fill="none" stroke-linecap="round"/><path d="M-90 -250 Q-170 -320 -110 -380" stroke="' + YEL + '" stroke-width="40" fill="none" stroke-linecap="round"/>'
        '<path d="M90 -250 Q170 -320 110 -380" stroke="#111" stroke-width="50" fill="none" stroke-linecap="round"/><path d="M90 -250 Q170 -320 110 -380" stroke="' + YEL + '" stroke-width="40" fill="none" stroke-linecap="round"/>'
        '<rect x="-130" y="-410" width="48" height="48" rx="12" fill="#f2c9a5" stroke="#111" stroke-width="4"/><rect x="82" y="-410" width="48" height="48" rx="12" fill="#f2c9a5" stroke="#111" stroke-width="4"/>')
def props(uid, vis=True):
    """Propeller aus dem Rücken (hinter dem Körper)."""
    one = lambda sx: (f'<path d="M{sx * 60} -260 L{sx * 190} -420" stroke="#111" stroke-width="26" stroke-linecap="round"/><path d="M{sx * 60} -260 L{sx * 190} -420" stroke="#adb5bd" stroke-width="16" stroke-linecap="round"/>'
                      f'<rect x="{sx * 190 - 10}" y="-450" width="20" height="40" fill="#555"/><ellipse class="rot" cx="{sx * 190}" cy="-452" rx="110" ry="14" fill="#adb5bd" stroke="#111" stroke-width="5" opacity=".85"/>')
    return f'<g id="{uid}" opacity="{1 if vis else 0}">{one(-1)}{one(1)}</g>'

# Kamerafahrten enden spätestens beim nächsten Schnitt (sonst überschreibt eine laufende Fahrt den harten Schnitt)
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
import math

# ======================= KOMPLIMENT-STADT: Figuren =======================
FACES["blush"] = ('<rect x="-96" y="-96" width="192" height="192" rx="26" fill="#ff4d6d" opacity=".55"/>' + '<path d="M-44 -6 Q-30 -18 -16 -6 M16 -6 Q30 -18 44 -6" stroke="#111" stroke-width="7" fill="none" stroke-linecap="round"/>'
                  '<path d="M-20 34 Q0 46 20 34" stroke="#111" stroke-width="7" fill="none" stroke-linecap="round"/>'
                  '<g class="steam"><rect x="-150" y="-60" width="50" height="40" rx="20" fill="#fff" opacity=".9"/><rect x="100" y="-60" width="50" height="40" rx="20" fill="#fff" opacity=".9"/>'
                  '<rect x="-180" y="-110" width="40" height="34" rx="17" fill="#fff" opacity=".8"/><rect x="140" y="-110" width="40" height="34" rx="17" fill="#fff" opacity=".8"/></g>')
FACES["forced"] = (E(-30, -6, 10) + E(30, -6, 10) + '<path d="M-50 -34 L-14 -26 M50 -34 L14 -26" stroke="#111" stroke-width="6" stroke-linecap="round"/>'
                   '<rect x="-48" y="18" width="96" height="34" rx="10" fill="#fff" stroke="#111" stroke-width="5"/><path d="M-24 18 V52 M0 18 V52 M24 18 V52" stroke="#111" stroke-width="3"/>'
                   '<path d="M62 -40 q-10 20 0 28 q10 -8 0 -28" fill="#4cc9f0" stroke="#111" stroke-width="2"/>')
FACES["sweat"] = (WEYE(-30, -8, 0, 2) + WEYE(30, -8, 0, 2) + '<path d="M-24 40 Q-12 30 0 40 Q12 50 24 40" stroke="#111" stroke-width="6" fill="none" stroke-linecap="round"/>'
                  '<path d="M66 -60 q-14 28 0 40 q14 -12 0 -40" fill="#4cc9f0" stroke="#111" stroke-width="3"/><path d="M-70 -40 q-12 24 0 34 q12 -10 0 -34" fill="#4cc9f0" stroke="#111" stroke-width="3"/>')
FACES["kiss"] = ('<path d="M-46 -4 Q-30 -16 -14 -4 M14 -4 Q30 -16 46 -4" stroke="#111" stroke-width="7" fill="none" stroke-linecap="round"/>'
                 '<rect x="-14" y="26" width="28" height="24" rx="12" fill="#e63946" stroke="#111" stroke-width="4"/>')
FACES["frozen"] = WEYE(-30, -6, 0, 0) + WEYE(30, -6, 0, 0) + '<path d="M-22 40 H22" stroke="#111" stroke-width="7" stroke-linecap="round"/>' + \
                  '<rect x="-96" y="-96" width="192" height="192" rx="26" fill="#a8dadc" opacity=".45"/>'
FACES["point"] = E(-30, 0) + E(30, 0) + '<path d="M-50 -30 L-12 -20 M50 -30 L12 -20" stroke="#111" stroke-width="8" stroke-linecap="round"/><path d="M-28 34 Q0 52 28 34" stroke="#111" stroke-width="7" fill="none" stroke-linecap="round"/>'
FACES["cry"] = FACES["sad"] + '<path d="M30 12 q-6 14 0 20 q6 -6 0 -20" fill="#4cc9f0"/>'
HOODIE_I = ('<path d="M-26 -300 V-236 M26 -300 V-236" stroke="#fff" stroke-width="7" stroke-linecap="round"/><rect x="-62" y="-190" width="124" height="70" rx="16" fill="#1f9e94" stroke="#111" stroke-width="4"/>')
ICH_EX = ("happy", "shock", "laugh", "determined", "panic", "neutral", "sweat", "grin", "confused", "hope")
def ich(uid, start="happy", arm=("down", "down"), extra="", arm2=None):
    return person(uid, "ich", "#6b3e26", "#2ec4b6", exprs=ICH_EX, start=start, arm=arm, arm2=arm2, extra=HOODIE_I + extra)
PAUL_EX = ("happy", "shock", "determined", "laugh", "grin", "wink", "hope", "plead_")
FACES["plead_"] = E(-30, -2, 13) + E(30, -2, 13) + '<path d="M-18 44 Q0 34 18 44" stroke="#111" stroke-width="6" fill="none" stroke-linecap="round"/>'
def paul(uid, start="happy", arm=("down", "down"), extra="", arm2=None):
    return person(uid, "cap", "#e63946", "#06d6a0", skin="#c68642", exprs=PAUL_EX, start=start, arm=arm, arm2=arm2, extra=extra)
STRICK = ('<path d="M0 -296 V-64" stroke="#111" stroke-width="5"/>' + "".join(f'<rect x="-10" y="{-270 + k * 50}" width="20" height="20" rx="10" fill="#ffd166" stroke="#111" stroke-width="3"/>' for k in range(4))
          + "".join(f'<path d="M{-90 + k * 30} -300 V-62" stroke="#7b2cbf" stroke-width="4" opacity=".5"/>' for k in range(7)))
def oma(uid, start="relief", arm=("down", "down"), extra="", head_acc=""):
    return person(uid, "oma", "#e0e0e0", "#9d4edd", exprs=("relief", "happy", "shock", "laugh", "grin", "sad", "wink"), start=start, arm=arm, extra=STRICK + extra, head_acc=OMA_ACC + head_acc)
DUCK = lambda x, y, s=1: f'<g transform="translate({x} {y}) scale({s})"><rect x="-14" y="-8" width="28" height="18" rx="8" fill="#ffd60a" stroke="#111" stroke-width="2"/><rect x="4" y="-20" width="14" height="14" rx="6" fill="#ffd60a" stroke="#111" stroke-width="2"/><path d="M18 -14 l8 3 l-8 3 z" fill="#fb8500"/></g>'
TIE = ('<path d="M-22 -300 L22 -300 L30 -270 L40 -120 L0 -80 L-40 -120 L-30 -270 Z" fill="#2dc653" stroke="#111" stroke-width="5"/>' + DUCK(0, -240, 1.0) + DUCK(-4, -180, 1.0) + DUCK(4, -125, 1.0))
KR_EX = ("neutral", "sad", "forced", "shock", "happy", "grin", "point", "determined", "laugh", "annoyed")
def krause(uid, start="neutral", arm=("down", "down"), extra="", arm2=None):
    return person(uid, "glatze", "#555", "#6c757d", exprs=KR_EX, start=start, arm=arm, arm2=arm2, head_acc=KR_ACC, extra=TIE + extra)
SASH = ('<path d="M-98 -300 L-60 -300 L98 -110 L98 -70 Z" fill="#e63946" stroke="#111" stroke-width="4"/>')
def bm(uid, start="neutral", arm=("down", "down"), extra="", arm2=None):
    return person(uid, "hut", "#ccc", "#264653", exprs=("neutral", "shock", "happy", "kiss", "frozen", "determined", "grin"), start=start, arm=arm, arm2=arm2, extra=KETTE + SASH + extra)
APRON = '<rect x="-70" y="-250" width="140" height="190" rx="16" fill="#fff" stroke="#111" stroke-width="4"/><rect x="-40" y="-200" width="80" height="50" rx="8" fill="#f4a261" stroke="#111" stroke-width="3"/>'
def baeckerin(uid, start="neutral", arm=("down", "down"), arm2=None):
    return person(uid, "lena", "#f4a261", "#e76f51", exprs=("neutral", "annoyed", "happy", "laugh"), start=start, arm=arm, arm2=arm2, extra=APRON)
def verk(uid, start="neutral", arm=("down", "down"), arm2=None):
    return person(uid, "mann", "#222", "#4361ee", exprs=("neutral", "blush", "shock", "happy", "tired"), start=start, arm=arm, arm2=arm2, skin="#e0ac69")
def kid(uid, shirt, hair="lena", hcol="#5e3023", start="happy", exprs=("happy", "sad", "cry", "shock")):
    return person(uid, hair, hcol, shirt, exprs=exprs, start=start)
HEARTC = lambda x, y, s=1: f'<g transform="translate({x} {y}) scale({s})"><rect x="-40" y="-40" width="80" height="80" rx="40" fill="#ffd166" stroke="#111" stroke-width="5"/><text x="0" y="18" text-anchor="middle" style="font:900 50px {FONT};fill:#e63946">♥</text></g>'
def sign(uid, lines, x, y, wd, size=70, col="#fff", fg="#111", vis=True, rot=0, cls=""):
    h = 40 + len(lines) * size * 1.15
    txt = "".join(f'<text x="0" y="{-h/2 + 20 + (k + .82) * size * 1.15:.0f}" text-anchor="middle" style="font:900 {size}px {FONT};fill:{fg}">{l}</text>' for k, l in enumerate(lines))
    return (f'<g id="{uid}" opacity="{1 if vis else 0}" transform="translate({x} {y}) rotate({rot})"><g id="{uid}-in"><rect x="{-wd/2 + 8}" y="{-h/2 + 8:.0f}" width="{wd}" height="{h:.0f}" rx="24" fill="#000" opacity=".3"/>'
            f'<rect x="{-wd/2}" y="{-h/2:.0f}" width="{wd}" height="{h:.0f}" rx="24" fill="{col}" stroke="#111" stroke-width="8"/>{txt}</g></g>')
def sepia(content, label, ly=440):
    return (content + '<rect width="1080" height="1920" fill="#c9a26b" opacity=".38"/>'
            '<rect x="24" y="24" width="1032" height="1872" rx="30" fill="none" stroke="#fff" stroke-width="18" stroke-dasharray="40 24"/>'
            f'<text x="540" y="{ly}" text-anchor="middle" style="font:900 54px {FONT};fill:#fff;opacity:.9">{label}</text>')
FLASH = lambda uid, col="#fff": f'<rect id="{uid}" width="1080" height="1920" fill="{col}" opacity="0"/>'
NOTE = lambda x, y, r=0, s=1: (f'<g transform="translate({x} {y}) rotate({r}) scale({s})"><rect x="-120" y="-50" width="240" height="100" rx="8" fill="#fff" stroke="#111" stroke-width="4"/>'
                               f'<text x="0" y="-6" text-anchor="middle" style="font:900 30px {FONT};fill:#e63946">SCHÖNE</text><text x="0" y="32" text-anchor="middle" style="font:900 30px {FONT};fill:#e63946">SCHUHE</text></g>')
def notes_pile(y0, n=60, seed=1):
    return "".join(NOTE((k * 137 + seed * 53) % 1100 - 10, y0 + (k * 71) % 260, (k * 47) % 60 - 30, .8) for k in range(n))
def wallet(uid, x, y, s=1):
    return (f'<g id="{uid}" transform="translate({x} {y}) scale({s})"><rect x="-90" y="-60" width="180" height="120" rx="14" fill="#7f5539" stroke="#111" stroke-width="6"/>'
            '<rect x="-80" y="-100" width="160" height="60" rx="10" fill="#9c6644" stroke="#111" stroke-width="5"/><path d="M-60 -70 H60" stroke="#5c3d2e" stroke-width="4" stroke-dasharray="8 6"/></g>')
MOTH = '<g id="moth" opacity="0"><rect x="-14" y="-10" width="28" height="20" rx="10" fill="#adb5bd" stroke="#111" stroke-width="3"/><path d="M-10 -6 L-40 -30 L-34 6 Z M10 -6 L40 -30 L34 6 Z" fill="#dee2e6" stroke="#111" stroke-width="3"/></g>'
def rathaus(x, y, s=1, gold=False, uid="rh"):
    c, r = ("#ffd166", "#d4a017") if gold else ("#e9ecef", "#adb5bd")
    return (f'<g id="{uid}" transform="translate({x} {y}) scale({s})"><rect x="-300" y="-500" width="600" height="500" fill="{c}" stroke="#111" stroke-width="8"/>'
            f'<path d="M-340 -500 L0 -720 L340 -500 Z" fill="{r}" stroke="#111" stroke-width="8"/><rect x="-60" y="-860" width="120" height="200" fill="{c}" stroke="#111" stroke-width="7"/>'
            f'<rect x="-40" y="-830" width="80" height="80" rx="40" fill="#fff" stroke="#111" stroke-width="5"/>'
            + "".join(f'<rect x="{-250 + k * 110}" y="-420" width="60" height="120" rx="8" fill="#8ecae6" stroke="#111" stroke-width="5"/>' for k in range(5)) +
            f'<rect x="-70" y="-200" width="140" height="200" rx="10" fill="#6b4226" stroke="#111" stroke-width="6"/><text x="0" y="-560" text-anchor="middle" style="font:900 56px {FONT};fill:#111">RATHAUS</text>'
            + ('<g class="spark">' + "".join(f'<path d="M{-340 + k * 120} {-760 + (k % 3) * 120} l14 -40 l14 40 l40 14 l-40 14 l-14 40 l-14 -40 l-40 -14 Z" fill="#fff" stroke="#111" stroke-width="3"/>' for k in range(7)) + '</g>' if gold else "") + '</g>')
KEY = '<g transform="translate(175 -500) rotate(-60)"><rect x="-26" y="-26" width="52" height="52" rx="26" fill="#ffd166" stroke="#111" stroke-width="5"/><rect x="20" y="-8" width="90" height="16" fill="#ffd166" stroke="#111" stroke-width="4"/><rect x="80" y="8" width="14" height="22" fill="#ffd166" stroke="#111" stroke-width="3"/></g>'

S = {}; FX = []
FY = 1560
def curb(y=1460): return f'<rect x="0" y="{y}" width="1080" height="70" fill="#adb5bd" stroke="#111" stroke-width="6"/><rect x="0" y="{y + 70}" width="1080" height="400" fill="#6c757d"/>'
KSIGN = sign("kSign", ["NEHME AUCH", "HALBE", "KOMPLIMENTE"], 0, 0, 430, size=52, col="#d4a373")
# --- A: Bild 0 – Krause sitzt pleite auf dem Bordstein
S["A"] = (street_bg() + curb() + f'<g transform="translate(270 1100) rotate(-6)">{KSIGN}</g>' +
          fig(krause("kr0", "sad", arm=("down", "front"), extra=wallet("kw0", 196, -330, .7) + f'<g transform="translate(196 -420)">{MOTH}</g>'), 720, FY + 30, 1.35) +
          '<rect x="0" y="1500" width="1080" height="40" fill="#adb5bd" stroke="#111" stroke-width="5"/>')
# --- B: Rückblende – Krause verteilt Sechsen
SIX = lambda x, y, r: f'<g transform="translate({x} {y}) rotate({r})"><rect x="-60" y="-75" width="120" height="150" fill="#fff" stroke="#111" stroke-width="5"/><text x="0" y="40" text-anchor="middle" style="font:900 100px {FONT};fill:#e63946">6</text></g>'
S["B"] = sepia(room_bg("#e9f5db", "#b08968", win=False) + '<rect x="120" y="300" width="840" height="400" fill="#2d6a4f" stroke="#6b4226" stroke-width="16"/>'
               f'<text x="540" y="540" text-anchor="middle" style="font:900 90px {FONT};fill:#fff">LOB: 0</text>' +
               fig(krause("kr1", "annoyed", arm=("down", "out")), 330, FY, 1.25) +
               fig(kid("kd1", "#ffb703", start="cry", exprs=("cry",)), 760, FY + 60, .85) + fig(kid("kd2", "#8338ec", hair="mann", start="cry", exprs=("cry",)), 960, FY + 60, .85) +
               '<g id="sixes">' + SIX(620, 1000, -15) + SIX(820, 920, 12) + SIX(1000, 1040, -8) + '</g>', "VOR 30 JAHREN … BIS HEUTE", ly=820)
# --- C: Bäckerei – Krause (links) / Bäckerin (rechts hinter Theke)
BREAD = "".join(f'<g transform="translate({120 + k * 170} 620)"><rect x="-70" y="-40" width="140" height="80" rx="40" fill="#e9a23b" stroke="#111" stroke-width="5"/><path d="M-30 -30 l-10 50 M0 -34 l-10 60 M30 -30 l-10 50" stroke="#9c6644" stroke-width="5"/></g>' for k in range(6))
S["C"] = (room_bg("#fff1e6", "#b08968", win=False) + '<rect x="40" y="520" width="1000" height="220" fill="#ddb892" stroke="#6b4226" stroke-width="10"/>' + BREAD +
          f'<text x="540" y="470" text-anchor="middle" style="font:900 80px {FONT};fill:#9c6644">BÄCKEREI</text>' +
          fig(baeckerin("bk", "neutral", arm=("down", "down"), arm2=("down", "front")), 810, FY - 40, 1.3) +
          '<rect x="560" y="1180" width="520" height="380" fill="#ddb892" stroke="#6b4226" stroke-width="10"/><rect x="560" y="1180" width="520" height="40" fill="#b08968"/>' +
          '<g id="crumb" opacity="0"><rect x="770" y="1150" width="22" height="18" rx="6" fill="#e9a23b" stroke="#111" stroke-width="3"/></g>' +
          fig(krause("kr2", "neutral", arm=("down", "down")), 280, FY, 1.3) +
          bubble("bubC", ["IHR BROT IST …", "NICHT VERBRANNT."], 420, 640, 640, tail=(-.6, 1), size=54))
# --- D: Lupe auf den Krümel
S["D"] = ('<rect width="1080" height="1920" fill="#ddb892"/>' + "".join(f'<rect x="0" y="{k * 90}" width="1080" height="6" fill="#b08968" opacity=".5"/>' for k in range(22)) +
          '<g transform="translate(540 860)"><rect x="-320" y="-320" width="640" height="640" rx="320" fill="#fff8e1" stroke="#111" stroke-width="22"/>'
          '<rect x="-60" y="-50" width="120" height="96" rx="30" fill="#e9a23b" stroke="#111" stroke-width="7"/><rect x="-30" y="-30" width="22" height="16" rx="6" fill="#ffd8a8"/>'
          '<rect x="240" y="240" width="80" height="320" rx="30" fill="#6b4226" stroke="#111" stroke-width="8" transform="rotate(-45 280 400)"/></g>')
# --- E: Ich entrollt meterlangen Spickzettel
ROLL = ('<g id="roll"><rect x="-150" y="0" width="300" height="1100" fill="#fff" stroke="#111" stroke-width="6"/>' +
        "".join(f'<rect x="-120" y="{30 + k * 44}" width="{180 + (k * 37) % 60}" height="14" rx="6" fill="#adb5bd"/>' for k in range(24)) + '</g>')
S["E"] = (room_bg("#cdeac0", "#9c6644") + fig(ich("ich1", "determined", arm=("front", "front")), 540, FY - 260, 1.3) +
          f'<g transform="translate(540 1050)">{ROLL}</g>' + '<rect y="1880" width="1080" height="40" fill="#7f5539"/>')
# --- F: Handyladen – Paul am Schaufenster
PHONE = lambda x, y, s=1, uid="ph": (f'<g id="{uid}" transform="translate({x} {y}) scale({s})"><rect x="-60" y="-110" width="120" height="220" rx="20" fill="#111" stroke="#555" stroke-width="5"/>'
                                    '<rect x="-48" y="-90" width="96" height="170" rx="10" fill="#4cc9f0"/><rect x="-20" y="88" width="40" height="10" rx="5" fill="#555"/></g>')
S["F"] = (street_bg() + '<rect x="80" y="520" width="920" height="760" fill="#cfe8ff" stroke="#111" stroke-width="12" opacity=".95"/>'
          f'<rect x="80" y="440" width="920" height="90" fill="#4361ee" stroke="#111" stroke-width="8"/><text x="540" y="505" text-anchor="middle" style="font:900 60px {FONT};fill:#fff">HANDYLADEN</text>'
          + PHONE(700, 820, 1.4) + sign("pTag", ["♥ 1 KOMPLIMENT"], 700, 1060, 420, size=44, col="#ffd166") +
          fig(paul("pa1", "hope", arm=("front", "down")), 330, FY + 60, 1.35))
# --- G: Verkäufer – Augenbrauen-Lineal / rot + Handy wirft
RULER = ('<g id="ruler" opacity="0" transform="translate(0 -40)"><rect x="-150" y="-26" width="300" height="34" fill="#ffd166" stroke="#111" stroke-width="4"/>'
         + "".join(f'<path d="M{-140 + k * 20} -26 v{14 if k % 5 else 24}" stroke="#111" stroke-width="3"/>' for k in range(15)) + '</g>')
S["G"] = ('<rect width="1080" height="1920" fill="#e0fbfc"/><rect y="1300" width="1080" height="620" fill="#98c1d9"/>'
          '<rect x="0" y="1200" width="1080" height="120" fill="#3d5a80" stroke="#111" stroke-width="6"/>' +
          fig(verk("vk", "neutral", arm=("down", "down"), arm2=("down", "out")), 680, FY, 1.45).replace('</g></g></g>', '</g></g></g>', 1) +
          f'<g transform="translate(680 {FY - 400 * 1.45}) scale(1.45)">{RULER}</g>' +
          fig(paul("pa2", "wink", arm=("down", "down"), arm2=("down", "up")), 160, FY + 80, 1.2) +
          f'<g id="flyph" opacity="0">{PHONE(0, 0, 1.0, "ph2")}</g>')
# --- H: Oma auf dem Berg aus Herz-Münzen
COINS = "".join(HEARTC(540 + (k % 9 - 4) * (90 - (k // 9) * 9) , 1560 - (k // 9) * 70, 1.0) for k in range(63))
S["H"] = (sky("#bde0fe") + city_skyline(1300, "#a3b1c6") + '<rect y="1300" width="1080" height="620" fill="#adb5bd"/>' +
          '<path d="M60 1620 L540 1050 L1020 1620 Z" fill="#ffd166" stroke="#111" stroke-width="8"/>' + COINS +
          fig(oma("om1", "happy", arm=("up", "up")), 540, 1120, 1.0))
# --- I: Oma kneift in die Wange – 3 Opfer
VICT = [kid("v0", "#ffb703", start="shock", exprs=("shock",)), person("v1", "cap", "#ffd60a", "#ffd60a", exprs=("shock",), start="shock"), bm("v2", "shock")]
VLAB = ["KIND", "POSTBOTE", "BÜRGERMEISTER"]
S["I"] = (street_bg() + fig(oma("om2", "grin", arm=("down", "front")), 330, FY, 1.35) +
          "".join(f'<g id="vic{k}" opacity="{1 if k == 0 else 0}">' + fig(VICT[k], 760, FY + (60 if k == 0 else 0), .95 if k == 0 else 1.2) + '</g>' for k in range(3)) +
          bubble("bubI", ["GROSS GEWORDEN!"], 540, 520, 720, tail=(-.4, 1), size=64))
# --- J: Badewanne von oben – Mini-Yacht
S["J"] = ('<rect width="1080" height="1920" fill="#e9ecef"/>' + "".join(f'<rect x="{(k % 9) * 120}" y="{(k // 9) * 120}" width="118" height="118" fill="none" stroke="#ced4da" stroke-width="3"/>' for k in range(9 * 17)) +
          '<rect x="160" y="420" width="760" height="1100" rx="300" fill="#fff" stroke="#111" stroke-width="12"/><rect x="210" y="470" width="660" height="1000" rx="260" fill="#90e0ef"/>'
          + "".join(f'<rect x="{260 + (k * 97) % 520}" y="{520 + (k * 131) % 880}" width="60" height="44" rx="22" fill="#fff" opacity=".85"/>' for k in range(14)) +
          '<g transform="translate(540 650)"><rect x="-96" y="-96" width="192" height="192" rx="26" fill="#f2c9a5" stroke="#111" stroke-width="5"/>' + HAIR["oma"]("#e0e0e0") +
          FACES["laugh"] + OMA_ACC + '<rect x="-110" y="-150" width="220" height="70" rx="16" fill="#fff" stroke="#111" stroke-width="5"/><rect x="-130" y="-96" width="260" height="22" rx="10" fill="#111"/><rect x="-26" y="-140" width="52" height="40" rx="10" fill="#ffd166" stroke="#111" stroke-width="3"/></g>'
          '<g id="yacht" transform="translate(540 1150)"><path d="M-170 0 H170 L120 70 H-120 Z" fill="#fff" stroke="#111" stroke-width="7"/><rect x="-80" y="-60" width="140" height="60" fill="#e9ecef" stroke="#111" stroke-width="6"/>'
          f'<rect x="-50" y="-48" width="30" height="24" fill="#8ecae6"/><rect x="0" y="-48" width="30" height="24" fill="#8ecae6"/><text x="0" y="50" text-anchor="middle" style="font:900 30px {FONT};fill:#264653">OMA I</text></g>')
# --- K: Bürgermeister mit Plan „GOLDENES RATHAUS“
PLAN = (f'<g id="plan" transform="translate(90 -330)"><rect x="-10" y="-200" width="420" height="300" fill="#caf0f8" stroke="#111" stroke-width="6"/>'
        f'<g transform="translate(200 60) scale(.3)">{rathaus(0, 0, 1, True, "rhp")}</g><text x="200" y="-160" text-anchor="middle" style="font:900 30px {FONT};fill:#023e8a">GOLDENES RATHAUS</text></g>')
S["K"] = (street_bg() + rathaus(820, 1150, .6) + fig(bm("bm1", "determined", arm=("down", "front"), extra=PLAN), 330, FY, 1.35))
# --- L: Spiegel / Bank-Automat
S["L"] = (room_bg("#f8edeb", "#b5838d", win=False) + '<rect x="560" y="300" width="440" height="900" rx="200" fill="#caf0f8" stroke="#6b4226" stroke-width="20"/>'
          '<rect x="600" y="340" width="120" height="400" rx="60" fill="#fff" opacity=".5"/>' +
          f'<svg x="560" y="300" width="440" height="900" overflow="hidden"><g transform="translate(-560 -300)">{fig(bm("bm3", "kiss", arm=("down", "down")), 840, FY - 120, 1.2)}</g></svg>' +
          fig(bm("bm2", "kiss", arm=("down", "down")), 330, FY, 1.35) +
          '<g id="kissH" opacity="0"><text x="560" y="760" text-anchor="middle" style="font:900 120px Inter">💋</text></g>')
S["L2"] = ('<rect width="1080" height="1920" fill="#495057"/><rect x="200" y="300" width="680" height="1300" rx="30" fill="#adb5bd" stroke="#111" stroke-width="10"/>'
           f'<text x="540" y="420" text-anchor="middle" style="font:900 80px {FONT};fill:#111">BANK ♥</text>'
           '<rect x="260" y="470" width="560" height="420" rx="20" fill="#0b132b" stroke="#111" stroke-width="8"/>'
           f'<g id="atmX" opacity="0"><path d="M400 560 L680 800 M680 560 L400 800" stroke="#e63946" stroke-width="40" stroke-linecap="round"/></g>'
           + "".join(f'<rect x="{300 + (k % 3) * 170}" y="{960 + (k // 3) * 110}" width="140" height="80" rx="14" fill="#dee2e6" stroke="#111" stroke-width="5"/>' for k in range(9)) +
           '<rect x="340" y="1300" width="400" height="30" rx="10" fill="#111"/>')
# --- M: Kompliment-Drucker 3000 (Tuch fliegt weg)
DRUCK = ('<g transform="translate(540 1500)"><rect x="-420" y="-1000" width="840" height="1000" rx="30" fill="#ff8fab" stroke="#111" stroke-width="10"/>'
         f'<rect x="-360" y="-940" width="720" height="140" rx="20" fill="#fff" stroke="#111" stroke-width="7"/><text x="0" y="-890" text-anchor="middle" style="font:900 52px {FONT};fill:#e63946">KOMPLIMENT-</text><text x="0" y="-830" text-anchor="middle" style="font:900 52px {FONT};fill:#e63946">DRUCKER 3000</text>'
         + "".join(f'<g transform="translate({-300 + k * 150} -680)"><rect x="-50" y="-50" width="100" height="100" rx="50" fill="#adb5bd" stroke="#111" stroke-width="6"/><rect class="gear" x="-12" y="-46" width="24" height="92" fill="#495057"/></g>' for k in range(5)) +
         '<rect x="-300" y="-500" width="600" height="80" rx="16" fill="#111"/><g id="slotN"></g>'
         + "".join(f'<rect x="{-330 + k * 120}" y="-360" width="70" height="60" rx="12" fill="{("#ffd166", "#2dc653", "#4cc9f0")[k % 3]}" stroke="#111" stroke-width="4"/>' for k in range(6)) + '</g>')
S["M"] = ('<rect width="1080" height="1920" fill="#3c096c"/><rect y="1500" width="1080" height="420" fill="#240046"/>' + DRUCK +
          '<g id="cloth"><path d="M80 420 Q540 300 1000 420 L1040 1520 H40 Z" fill="#6a040f" stroke="#111" stroke-width="8"/></g>' +
          fig(bm("bm4", "grin", arm=("down", "up")), 150, FY + 260, .9) + FLASH("mfl"))
# --- N: Ausgabeschacht – Zettel fliegen in die Kamera
S["N"] = ('<rect width="1080" height="1920" fill="#ff8fab"/><rect x="90" y="700" width="900" height="200" rx="30" fill="#111"/>'
          + "".join(f'<g class="nfly" id="nf{k}">{NOTE(540, 820, 0, 1.3)}</g>' for k in range(6)))
# --- O: Stadt versinkt in Zetteln
swim = "".join(f'<g class="swim">' + fig(person(f"sw{k}", h, "#3d2b1f", c, exprs=("shock", "laugh"), start="shock", arm=("up", "up")), x, 1500, .6) + '</g>' for k, (x, c, h) in enumerate(((200, "#3a86ff", "mann"), (540, "#ffb703", "lena"), (880, "#8338ec", "mann"))))
S["O"] = (street_bg() + swim + '<g id="sea">' + '<rect x="0" y="1280" width="1080" height="640" fill="#fff"/>' + notes_pile(1240, 70) + notes_pile(1500, 50, 3) + '</g>' +
          fig(ich("ich2", "shock", arm=("up", "up")), 700, 1720, .9))
# --- P: Preistafel + Schubkarre
S["P"] = (room_bg("#fff1e6", "#b08968", win=False) + '<rect x="140" y="320" width="800" height="420" rx="20" fill="#2b2d42" stroke="#6b4226" stroke-width="14"/>'
          f'<text x="540" y="460" text-anchor="middle" style="font:900 64px {FONT};fill:#fff">1 BRÖTCHEN</text>'
          f'<text x="540" y="560" text-anchor="middle" style="font:900 56px {FONT};fill:#adb5bd;text-decoration:line-through">1 ♥</text>'
          f'<text id="pPrice" x="540" y="680" text-anchor="middle" style="font:900 100px {FONT};fill:#ffd166">300 ♥</text>' +
          '<g id="karre"><g transform="translate(560 1560)"><rect x="-260" y="-260" width="420" height="180" fill="#e63946" stroke="#111" stroke-width="8"/><rect x="-80" y="-80" width="100" height="100" rx="50" fill="#333" stroke="#111" stroke-width="6"/>'
          '<path d="M160 -240 L300 -160" stroke="#111" stroke-width="14"/>' + "".join(NOTE(-220 + (k % 4) * 110, -300 - (k // 4) * 50, (k * 37) % 50 - 25, .55) for k in range(16)) + '</g>' +
          fig(paul("pa3", "shock", arm=("front", "front")), 960, FY, 1.05) + '</g>')
# --- Q: Paul kniet am Kiosk – Gedicht
S["Q"] = (street_bg() + '<rect x="520" y="560" width="520" height="900" fill="#ffb703" stroke="#111" stroke-width="10"/><rect x="560" y="700" width="440" height="300" fill="#8ecae6" stroke="#111" stroke-width="6"/>'
          f'<text x="780" y="640" text-anchor="middle" style="font:900 70px {FONT};fill:#111">KIOSK</text>' +
          f'<svg x="560" y="700" width="440" height="300" overflow="hidden"><g transform="translate(-560 -700)">{fig(verk("ks", "tired"), 780, 1300, .8)}</g></svg>' +
          fig(paul("pa4", "hope", arm=("up", "front")), 300, FY + 120, 1.2) +
          bubble("bubQ", ["DU BIST SO NETT,", "WIE EIN … BETT!"], 400, 560, 640, tail=(-.4, 1), size=50))
# --- R: Hand – Herzberg → Zahnstocher
S["R"] = ('<rect width="1080" height="1920" fill="#fefae0"/><rect y="1260" width="1080" height="660" fill="#ddb892"/>'
          '<g id="rHeap">' + "".join(HEARTC(300 + (k % 6 - 2.5) * 70, 1220 - (k // 6) * 60, .9) for k in range(24)) + '</g>'
          '<g id="pick" opacity="0" transform="translate(760 1000) rotate(-30)"><rect x="-180" y="-8" width="360" height="16" rx="8" fill="#e9c46a" stroke="#111" stroke-width="4"/></g>'
          f'<g transform="translate(780 1180)"><rect x="-90" y="-60" width="180" height="120" rx="40" fill="#f2c9a5" stroke="#111" stroke-width="6"/><rect x="-160" y="-30" width="80" height="60" rx="30" fill="#9d4edd" stroke="#111" stroke-width="6"/></g>')
# --- S2: Bank-Schild dreht sich
S["S"] = ('<rect width="1080" height="1920" fill="#495057"/><rect x="100" y="420" width="880" height="900" fill="#dee2e6" stroke="#111" stroke-width="10"/>'
          + "".join(f'<rect x="{160 + k * 200}" y="900" width="60" height="420" fill="#adb5bd" stroke="#111" stroke-width="5"/>' for k in range(5)) +
          '<path d="M60 420 L540 220 L1020 420 Z" fill="#adb5bd" stroke="#111" stroke-width="10"/>'
          '<g id="bsA"><rect x="180" y="560" width="720" height="240" rx="20" fill="#fff" stroke="#111" stroke-width="8"/>'
          f'<text x="540" y="700" text-anchor="middle" style="font:900 64px {FONT};fill:#e63946">BANK: ♥ = GELD</text></g>'
          '<g id="bsB" opacity="0"><rect x="180" y="560" width="720" height="240" rx="20" fill="#ffd166" stroke="#111" stroke-width="8"/>'
          f'<text x="540" y="660" text-anchor="middle" style="font:900 58px {FONT};fill:#111">NUR NOCH</text><text x="540" y="750" text-anchor="middle" style="font:900 58px {FONT};fill:#111">EHRLICHKEIT</text></g>'
          '<g id="alarm"><rect x="470" y="140" width="140" height="100" rx="40" fill="#e63946" stroke="#111" stroke-width="7"/></g>' + FLASH("sfl", "#e63946"))
# --- T: Krause – Bürgermeister: „LANGWEILIG.“
S["T"] = (street_bg() + rathaus(540, 1150, .55) + fig(bm("bm5", "happy"), 760, FY, 1.35) +
          fig(krause("kr3", "neutral", arm=("down", "down"), arm2=("down", "front")), 300, FY, 1.35) +
          bubble("bubT", ["IHRE REDE WAR", "LANGWEILIG."], 400, 520, 620, tail=(-.5, 1), size=60))
# --- U: Kaching – goldenes Rathaus, Krause mit Schlüssel
S["U"] = (sky("#ffe5a0") + rathaus(600, 1300, .9, True, "rhg") + '<rect y="1300" width="1080" height="620" fill="#adb5bd"/>' +
          fig(krause("kr4", "laugh", arm=("down", "up"), extra=KEY), 220, FY, 1.2))
# --- V: Krause zeigt auf mich (Finger in die Kamera)
FINGER = ('<g id="fing"><path d="M90 -250 Q160 -260 150 -320" stroke="#111" stroke-width="50" fill="none" stroke-linecap="round"/><path d="M90 -250 Q160 -260 150 -320" stroke="#6c757d" stroke-width="40" fill="none" stroke-linecap="round"/>'
          '<rect x="110" y="-390" width="80" height="70" rx="20" fill="#f2c9a5" stroke="#111" stroke-width="4"/><rect x="134" y="-470" width="30" height="90" rx="14" fill="#f2c9a5" stroke="#111" stroke-width="4"/></g>')
S["V"] = ('<rect width="1080" height="1920" fill="#ffd166"/>' + "".join(f'<path d="M540 900 L{540 + 1400 * math.cos(math.radians(k * 20)):.0f} {900 + 1400 * math.sin(math.radians(k * 20)):.0f}" stroke="#ffb703" stroke-width="60"/>' for k in range(18)) +
          fig(krause("kr5", "point", arm=("down", "down"), extra=FINGER), 540, FY, 1.45))
# --- W: Krawatte groß / Ich schwitzt
S["W"] = ('<rect width="1080" height="1920" fill="#d8f3dc"/>' + f'<g transform="translate(540 380) scale(4)">{TIE}</g>')
S["W2"] = (street_bg() + fig(ich("ich3", "sweat", arm=("down", "down")), 540, FY, 1.5))
# --- X: Ich hält Schild „DEIN BESTES KOMPLIMENT: ___?“ (Schild 1080–1245 px)
XS = ('<g id="xs"><rect x="-400" y="0" width="800" height="165" rx="26" fill="#fff" stroke="#111" stroke-width="9"/>'
      f'<text x="0" y="68" text-anchor="middle" style="font:900 52px {FONT};fill:#111">DEIN BESTES KOMPLIMENT:</text>'
      f'<text id="xq" x="0" y="140" text-anchor="middle" style="font:900 64px {FONT};fill:#e63946">___?</text></g>')
S["X"] = (street_bg() + fig(ich("ich4", "sweat", arm=("front", "front")), 540, FY - 175, 1.25) + f'<g transform="translate(540 1045)">{XS}</g>')
# --- Y: Schluss – wie Bild 0: Krause auf dem Bordstein, jetzt mit Rathaus-Schlüssel
S["Y"] = (street_bg() + curb() + f'<g transform="translate(270 1100) rotate(-6)">{sign("ySign", ["NEHME AUCH", "HALBE", "KOMPLIMENTE"], 0, 0, 430, size=52, col="#d4a373")}</g>' +
          '<g id="yx" opacity="0"><path d="M80 960 L460 1240 M460 960 L80 1240" stroke="#e63946" stroke-width="30" stroke-linecap="round"/></g>' +
          fig(krause("kr6", "grin", arm=("down", "up"), extra=KEY), 720, FY + 30, 1.35) +
          '<rect x="0" y="1500" width="1080" height="40" fill="#adb5bd" stroke="#111" stroke-width="5"/>')

# ======================= Zeitplan =======================
J.append('tl.set("#cam", { x: 0, y: 0, scale: 1, svgOrigin: "0 0" }, 0);')
def ww(sid, word, n=1, d=.1): return round(w(sid, word, n) - d, 2)
t = {k: st(k) for k in T}
KZ = []   # (Zeit, Name, Wert)
hk0 = HEAD(720, FY + 30, 1.35)
# s1: Bild 0 – Punch-Zoom 108→100 % + Plopp; erster Schnitt ≤ 1,2 s auf das Schild
cut(0, 540, 900, 1.08); cam(.02, 540, 900, 1.0, .45, "power2.out"); FX += [("pop", 0, .5, .4), ("klong", .05, .25, .6)]
pop("#kSign", .05, .35, "50% 50%")
KZ.append((0, "KRAUSE", "0"))
c1 = min(1.2, ww("s1", "Komplimenten.") - .05)
cut(c1, 300, 1060, 1.6); FX += [("swoosh", c1, .3, .4)]
wobble("#kSign", c1, 3, 4, .15, "rotation", "50% 0%")
tdh = ww("s1", "Deshalb")
cut(tdh, 720, hk0[1] - 40, 1.7); expr("kr0", "sad", "neutral", tdh)
tpl = ww("s1", "pleite.")
cut(tpl, 840, 1060, 1.6); expr("kr0", "neutral", "sad", tpl)
J.append(f'tl.fromTo("#moth", {{ opacity: 1, x: 0, y: 0 }}, {{ x: 120, y: -260, duration: 1.0, ease: "sine.inOut", immediateRender: false }}, {F(tpl + .1)});'); FX += [("boing", tpl + .1, .3, .4)]
# s2: Rückblende
cut(t["s2"], 540, 1000, 1.05); cam(t["s2"] + .02, 540, 950, 1.15, 1.5, "none"); FX += [("swoosh", t["s2"], .3, .4)]
fly("#sixes", t["s2"] + .2, {"x": -300, "opacity": 0}, {"x": 0, "opacity": 1}, .4)
tgl = ww("s2", "Schüler.")
cut(tgl, 860, 1100, 1.4); FX += [("splat", tgl, .25, .5)]
KZ.append((t["s2"], "KRAUSE", "0"))
# s3: Bäckerei – Krause zwingt sich ein Lächeln
hk2 = HEAD(280, FY, 1.3); hbk = HEAD(810, FY - 40, 1.3)
cut(t["s3"], 540, 900, 1.0); FX += [("chime", t["s3"], .2, .5)]
tih = ww("s3", "Ihr")
cut(tih, 380, hk2[1] - 120, 1.4); expr("kr2", "neutral", "forced", tih); pop("#bubC", tih, .25, "50% 100%"); FX += [("pop", tih, .4, .3)]
tnv = ww("s3", "Nicht")
cut(tnv, hbk[0] - 60, hbk[1] - 30, 1.7); hide("#bubC", tnv, .05); expr("bk", "neutral", "annoyed", tnv); FX += [("tick", tnv, .3, .6)]
# s4: ein Krümel
cut(t["s4"], 650, 1050, 1.3); armswap("bk", t["s4"] + .2); J.append(f'tl.set("#crumb", {{ opacity: 1 }}, {F(t["s4"] + .4)});')
tkr = ww("s4", "Krümel.")
cut(tkr, 540, 900, 1.0); FX += [("pop", tkr, .4, .3)]; J.append(f'tl.fromTo("#setD g", {{ scale: .6, svgOrigin: "540 860" }}, {{ scale: 1, duration: .3, ease: "back.out(2)", immediateRender: false }}, {F(tkr)});')
tei = ww("s4", "einzigen.")
cam(tei, 540, 880, 1.3, .25, "power3.out"); FX += [("klong", tei, .3, .5)]
KZ.append((tkr, "KRAUSE", "0 (+1 KRÜMEL)"))
# s5: Ich – Spickzettel
hi1 = HEAD(540, FY - 260, 1.3)
cut(t["s5"], 540, hi1[1] - 20, 1.6); expr("ich1", "determined", "grin", t["s5"]); FX += [("swoosh", t["s5"], .3, .4)]
tsp = ww("s5", "Spickzettel")
cut(tsp, 540, 1350, 1.1); cam(tsp + .02, 540, 1500, 1.1, 1.0, "power1.out")
J.append(f'tl.fromTo("#roll", {{ scaleY: .05, transformOrigin: "50% 0%" }}, {{ scaleY: 1, duration: .8, ease: "bounce.out", immediateRender: false }}, {F(tsp)});'); FX += [("whoosh", tsp, .4, .6)]
J.append('tl.set("#roll", { scaleY: .05, transformOrigin: "50% 0%" }, 0);')
KZ.append((t["s5"], "ICH", "100"))
# s6: Paul am Schaufenster
hp1 = HEAD(330, FY + 60, 1.35)
cut(t["s6"], 540, 1000, 1.05); FX += [("swoosh", t["s6"], .3, .4)]
tha = ww("s6", "Handy.")
cut(tha, 700, 920, 1.6); pop("#pTag", tha, .3, "50% 50%"); FX += [("pop", tha, .4, .3)]
KZ.append((t["s6"], "PAUL", "3"))
# s7: Augenbrauen
hv = HEAD(680, FY, 1.45)
cut(t["s7"], 420, 1000, 1.15); expr("pa2", "wink", "grin", t["s7"]); armswap("pa2", t["s7"] + .1)
tab = ww("s7", "Augenbrauen")
cut(tab, hv[0], hv[1] - 40, 2.0); pop("#ruler", tab + .1, .3, "50% 50%"); FX += [("blips", tab, .3, .6)]
# s8: Verkäufer wird rot, wirft das Handy
cut(t["s8"], hv[0] - 20, hv[1] - 10, 1.7); expr("vk", "neutral", "blush", t["s8"] + .2); hide("#ruler", t["s8"], .05); FX += [("boing", t["s8"] + .2, .4, .5)]
J.append(f'tl.fromTo("#vk-blush .steam", {{ y: 0, opacity: 1 }}, {{ y: -40, opacity: .2, duration: .4, repeat: 3, immediateRender: false }}, {F(t["s8"] + .2)});')
tgr = ww("s8", "Handy")
cut(tgr, 420, 1000, 1.1); armswap("vk", tgr); expr("pa2", "grin", "laugh", tgr + .4)
J.append(f'tl.set("#flyph", {{ opacity: 1 }}, {F(tgr)}); tl.fromTo("#flyph", {{ x: 680, y: 900, rotation: 0 }}, {{ x: 200, y: 1100, rotation: -540, duration: .45, ease: "power1.out", immediateRender: false }}, {F(tgr)});')
J.append('tl.set("#flyph", { x: 680, y: 900 }, 0);'); FX += [("whoosh", tgr, .4, .5), ("chime", tgr + .5, .3, .6)]
KZ.append((tgr + .4, "PAUL", "2 + 📱"))
# s9: Oma auf dem Münzberg
cut(t["s9"], 540, 1500, 1.15); cam(t["s9"] + .02, 540, 800, 1.15, 1.6, "power2.inOut"); FX += [("riser", t["s9"], .2, 1.5)]
tom = ww("s9", "Oma.")
cut(tom, 540, 760, 1.6); expr("om1", "happy", "laugh", tom); FX += [("chime", tom, .4, .8)]
KZ.append((t["s9"], "OMA", "1.000.000"))
# s10: Wangen-Kneifen – 3 harte Schnitte
ho2 = HEAD(330, FY, 1.35)
cut(t["s10"], 420, 1000, 1.25)
tbi = ww("s10", "Bist")
cut(tbi, 540, 960, 1.15); pop("#bubI", tbi, .25, "50% 100%"); FX += [("boing", tbi, .4, .4)]
tgw = ww("s10", "groß"); tge = ww("s10", "geworden!")
for k, a in enumerate((tbi, tgw, tge)):
    if k: J.append(f'tl.set("#vic{k - 1}", {{ opacity: 0 }}, {F(a)}); tl.set("#vic{k}", {{ opacity: 1 }}, {F(a)});')
    if k: cut(a, 540 + (k % 2) * 60, 980 - k * 20, 1.15 + .1 * k)
    J.append(f'tl.fromTo("#vic{k}", {{ x: 0 }}, {{ x: -10, duration: .05, yoyo: true, repeat: 5, ease: "none", immediateRender: false }}, {F(a + .05)});'); FX += [("pop", a + .05, .4, .2)]
# s11: Yacht in der Badewanne
cut(t["s11"], 540, 900, 1.0); FX += [("swoosh", t["s11"], .3, .4)]
tyc = ww("s11", "Yacht.")
cut(tyc, 540, 1100, 1.5); wobble("#yacht", tyc, 7, 6, .2, "rotation", "50% 50%"); FX += [("splat", tyc, .3, .4)]
tbw = ww("s11", "Badewanne.")
cam(tbw, 540, 900, 1.0, .3, "power3.out"); FX += [("boing", tbw + .2, .3, .4)]
# s12: Bürgermeister + Plan
hb1 = HEAD(330, FY, 1.35)
cut(t["s12"], 400, 1000, 1.2); FX += [("swoosh", t["s12"], .3, .4)]
J.append(f'tl.fromTo("#plan", {{ scaleX: .1, transformOrigin: "0% 50%" }}, {{ scaleX: 1, duration: .35, ease: "back.out(2)", immediateRender: false }}, {F(ww("s12", "goldenes"))});')
tgo = ww("s12", "goldenes")
cut(tgo, 700, 860, 1.6); FX += [("chime", tgo, .3, .6)]
tpr = ww("s12", "Preis:")
cut(tpr, 540, 1000, 1.05); FX += [("klong", tpr, .3, .5)]
KZ.append((t["s12"], "BÜRGERMEISTER", "200"))
# s13: Spiegel / Automat
cut(t["s13"], 540, 900, 1.15); J.append(f'tl.fromTo("#kissH", {{ opacity: 1, scale: .4, svgOrigin: "560 760" }}, {{ scale: 1.2, duration: .4, immediateRender: false }}, {F(t["s13"] + .3)}); tl.set("#kissH", {{ opacity: 0 }}, {F(t["s13"] + 1.2)});'); FX += [("pop", t["s13"] + .3, .4, .3)]
tba = ww("s13", "Bank:")
cut(tba, 540, 800, 1.1); FX += [("blips", tba, .3, .4)]
tzn = ww("s13", "Zählt")
J.append(f'tl.set("#atmX", {{ opacity: 1 }}, {F(tzn)});'); cam(tzn, 540, 700, 1.3, .2, "power3.out"); FX += [("klong", tzn, .4, .6)]; shake(tzn, 6, 12)
# s14: Drucker-Enthüllung
cut(t["s14"], 540, 1300, 1.1); FX += [("wirbel", t["s14"], .3, 1.2)]
tdr = ww("s14", "Kompliment-Drucker.")
J.append(f'tl.to("#cloth", {{ y: -1600, rotation: -12, duration: .5, ease: "power2.in" }}, {F(tdr - .1)});')
J.append(f'tl.to("#mfl", {{ opacity: .9, duration: .06, yoyo: true, repeat: 3, ease: "steps(1)" }}, {F(tdr + .3)});')
cut(tdr + .3, 540, 900, 1.0); cam(tdr + .32, 540, 760, 1.15, .8, "power2.out"); FX += [("whoosh", tdr - .1, .4, .6), ("hit", tdr + .3, .35, .8)]
J.append(f'tl.to("#setM .gear", {{ rotation: 360, transformOrigin: "50% 50%", duration: .6, repeat: 8, ease: "none" }}, {F(tdr + .3)});')
# s15: Rrrt – Zettel in die Kamera
cut(t["s15"], 540, 900, 1.0); FX += [("blips", t["s15"], .3, 1.0)]
for k in range(6):
    a = t["s15"] + .1 + k * max(.25, (t["s16"] - t["s15"] - .3) / 6)
    J.append(f'tl.fromTo("#nf{k}", {{ x: 0, y: 0, scale: .4, rotation: 0, svgOrigin: "540 820", opacity: 1 }}, {{ x: {(k % 3 - 1) * 300}, y: {600 + k * 40}, scale: 3.2, rotation: {(k % 2) * 60 - 30}, duration: .5, ease: "power2.in", immediateRender: false }}, {F(a)});')
    FX += [("pop", a, .25, .2)]
J.append('tl.set(".nfly", { opacity: 0 }, 0);')
tss = ww("s15", "Schöne", 2)
cut(tss, 540, 860, 1.12); shake(tss, 6, 10)
# s16: Stadt versinkt
cut(t["s16"], 540, 1200, 1.1); cam(t["s16"] + .02, 540, 1000, 1.0, 1.2, "none"); FX += [("whoosh", t["s16"], .3, .6)]
J.append(f'tl.fromTo("#sea", {{ y: 300 }}, {{ y: 0, duration: 1.4, ease: "power2.out", immediateRender: false }}, {F(t["s16"])});')
J.append(f'tl.to("#setO .swim", {{ y: -20, duration: .3, yoyo: true, repeat: 9, ease: "sine.inOut", stagger: .1 }}, {F(t["s16"])});')
tvs = ww("s16", "versinkt")
cut(tvs, 700, 1300, 1.5); FX += [("splat", tvs, .3, .5)]
# s17: Inflation
cut(t["s17"], 540, 600, 1.2); FX += [("klong", t["s17"], .3, .5)]
tbr = ww("s17", "Brötchen:")
cut(tbr, 540, 520, 1.5); J.append(f'tl.fromTo("#pPrice", {{ scale: 2, svgOrigin: "540 650" }}, {{ scale: 1, duration: .3, ease: "back.out(2)", immediateRender: false }}, {F(tbr + .3)});')
tst = ww("s17", "Stück.")
cut(tst, 650, 1150, 1.1); fly("#karre", tst, {"x": 900}, {"x": 0}, .4, "power2.out"); J.append('tl.set("#karre", { x: 900 }, 0);'); FX += [("whoosh", tst, .4, .5)]
KZ.append((t["s17"], "♥ WERT", "📉"))
# s18: Paul – Gedicht am Kiosk
hp4 = HEAD(300, FY + 120, 1.2)
cut(t["s18"], 540, 1000, 1.05); FX += [("swoosh", t["s18"], .3, .4)]
tge2 = ww("s18", "Gedicht.")
cut(tge2, 420, 900, 1.35); pop("#bubQ", tge2, .25, "50% 100%"); FX += [("chime", tge2, .3, .5)]
tre = ww("s18", "Reim.")
cut(tre, 780, 900, 1.7); FX += [("tick", tre, .3, .6)]
KZ.append((t["s18"], "PAUL", "1 GEDICHT"))
# s19: Omas Million → Zahnstocher
cut(t["s19"], 420, 1100, 1.4); FX += [("blips", t["s19"], .3, .5)]
tzs = ww("s19", "Zahnstocher.")
J.append(f'tl.to("#rHeap", {{ x: -700, duration: .3, ease: "power2.in" }}, {F(tzs - .1)}); tl.set("#pick", {{ opacity: 1 }}, {F(tzs + .1)});')
cut(tzs + .1, 760, 1000, 1.8); FX += [("pop", tzs + .1, .4, .3)]
KZ.append((t["s19"], "OMA", "1.000.000")); KZ.append((tzs + .1, "OMA", "1 🦷"))
# s20: Bank-Schild dreht sich
cut(t["s20"], 540, 700, 1.1); FX += [("klong", t["s20"], .3, .6)]
tab2 = ww("s20", "Ab")
J.append(f'tl.to("#bsA", {{ scaleY: 0, svgOrigin: "540 680", duration: .15 }}, {F(tab2)}); tl.set("#bsB", {{ opacity: 1 }}, {F(tab2 + .15)}); tl.fromTo("#bsB", {{ scaleY: 0, svgOrigin: "540 680" }}, {{ scaleY: 1, duration: .15, immediateRender: false }}, {F(tab2 + .15)});')
cut(tab2 + .15, 540, 680, 1.4); FX += [("hit", tab2 + .15, .35, .6)]
J.append(f'tl.to("#sfl", {{ opacity: .35, duration: .2, yoyo: true, repeat: 7, ease: "steps(1)" }}, {F(tab2 + .2)}); tl.set("#sfl", {{ opacity: 0 }}, {F(tab2 + 1.9)});')
J.append(f'tl.to("#alarm", {{ opacity: .3, duration: .15, yoyo: true, repeat: 9, ease: "steps(1)" }}, {F(t["s20"])});')
# s21: Krause sagt dem Bürgermeister die Wahrheit
hk3 = HEAD(300, FY, 1.35); hb5 = HEAD(760, FY, 1.35)
cut(t["s21"], 540, 1000, 1.05); armswap("kr3", t["s21"] + .3); FX += [("swoosh", t["s21"], .3, .4)]
tih2 = ww("s21", "Ihre")
cut(tih2, 380, 900, 1.35); pop("#bubT", tih2, .25, "50% 100%"); expr("kr3", "neutral", "determined", tih2)
tlw = ww("s21", "langweilig.")
cut(tlw, hb5[0] - 20, hb5[1] - 40, 1.8); hide("#bubT", tlw, .05); expr("bm5", "happy", "frozen", tlw + .1); FX += [("klong", tlw + .1, .35, .6)]
# s22: Kaching!
cut(t["s22"], 540, 900, 1.0); FX += [("chime", t["s22"], .5, 1.0), ("blips", t["s22"] + .2, .3, 1.0)]
J.append(f'tl.to("#rhg .spark", {{ opacity: .2, duration: .15, yoyo: true, repeat: 15, ease: "steps(1)" }}, {F(t["s22"])});')
tmi = ww("s22", "Millionär.")
cut(tmi, 300, 1000, 1.5); expr("kr4", "laugh", "grin", tmi)
tka = ww("s22", "kauft")
cut(tka, 600, 800, 1.2); cam(tka + .02, 600, 900, 1.0, 1.0, "power1.out")
KZ.append((t["s22"], "KRAUSE", "1.000.000"))
# s23: Finger in die Kamera
hk5 = HEAD(540, FY, 1.45)
cut(t["s23"], 540, 1000, 1.2); FX += [("whoosh", t["s23"], .3, .5)]
tmi2 = ww("s23", "mich:")
cut(tmi2, 700, 880, 2.2); FX += [("hit", tmi2, .35, .6)]; J.append(f'tl.fromTo("#fing", {{ scale: .7, transformOrigin: "90px -250px" }}, {{ scale: 1, duration: .2, ease: "back.out(3)", immediateRender: false }}, {F(tmi2)});')
tkw = ww("s23", "Krawatte.")
cut(tkw, 540, hk5[1] - 20, 1.6); FX += [("tick", tkw, .3, .8)]
KZ.append((t["s23"], "ICH", "100"))
# s24: Krawatte groß / Ich schwitzt
cut(t["s24"], 540, 860, 1.0); cam(t["s24"] + .02, 540, 900, 1.15, 1.0, "none"); FX += [("boing", t["s24"], .3, .4)]
ten = ww("s24", "Enten")
cut(ten, 540, 1000, 1.3); FX += [("pop", ten, .3, .3)]
tma = ww("s24", "mach")
hi3 = HEAD(540, FY, 1.5)
cut(tma, 540, hi3[1] - 40, 1.8); cam(tma + .02, 540, hi3[1] - 40, 2.1, 1.6, "none"); FX += [("wirbel", tma, .3, 1.4)]
J.append(f'tl.fromTo("#ich3", {{ x: 0 }}, {{ x: -6, duration: .05, yoyo: true, repeat: 15, ease: "none", immediateRender: false }}, {F(tma + .3)});')
# s25: Schild
cut(t["s25"], 540, 900, 1.0); FX += [("pop", t["s25"], .5, .3)]
J.append(f'tl.fromTo("#xs", {{ scale: .3, opacity: 0, transformOrigin: "50% 50%" }}, {{ scale: 1, opacity: 1, duration: .3, ease: "back.out(2.4)", immediateRender: false }}, {F(t["s25"] + .05)});')
J.append(f'tl.to("#xq", {{ opacity: .2, duration: .15, yoyo: true, repeat: 9, ease: "steps(1)" }}, {F(t["s25"] + .5)});')
tre2 = ww("s25", "rettet")
cut(tre2, 540, 900, 1.0); expr("ich4", "sweat", "hope", tre2); wobble("#xs", tre2, 3, 3, .15, "rotation", "50% 50%"); FX += [("boing", tre2, .3, .4)]
# s26: Folg … Loop zurück auf Bild 0
cut(t["s26"], 540, 900, 1.0); expr("ich4", "hope", "grin", t["s26"])
tin = ww("s26", "In")
hk6 = HEAD(720, FY + 30, 1.35)
cut(tin, 700, hk6[1] - 10, 1.6); cam(tin + .02, 540, 900, 1.0, max(1.0, END - tin - .2), "sine.inOut"); FX += [("whoosh", tin, .3, .6)]
tme = ww("s26", "Meistens.")
J.append(f'tl.set("#yx", {{ opacity: 1 }}, {F(tme)}); tl.fromTo("#yx", {{ scale: .3, svgOrigin: "270 1100" }}, {{ scale: 1, duration: .25, ease: "back.out(3)", immediateRender: false }}, {F(tme)});')
expr("kr6", "grin", "laugh", tme); FX += [("pop", tme, .45, .3)]
J.append(f'tl.fromTo("#kr6", {{ y: 0 }}, {{ y: -14, duration: .14, yoyo: true, repeat: {max(1, int((END - tme) / .14))}, ease: "sine.inOut", immediateRender: false }}, {F(tme + .1)});')
KZ.append((t["s26"], "ICH", "100"))
KZ.append((tin, "KRAUSE", "1.000.000"))

sets = [("A", 0, t["s2"]), ("B", t["s2"], t["s3"]), ("C", t["s3"], tkr), ("D", tkr, t["s5"]), ("E", t["s5"], t["s6"]), ("F", t["s6"], t["s7"]), ("G", t["s7"], t["s9"]),
        ("H", t["s9"], t["s10"]), ("I", t["s10"], t["s11"]), ("J", t["s11"], t["s12"]), ("K", t["s12"], t["s13"]), ("L", t["s13"], tba), ("L2", tba, t["s14"]),
        ("M", t["s14"], t["s15"]), ("N", t["s15"], t["s16"]), ("O", t["s16"], t["s17"]), ("P", t["s17"], t["s18"]), ("Q", t["s18"], t["s19"]), ("R", t["s19"], t["s20"]),
        ("S", t["s20"], t["s21"]), ("T", t["s21"], t["s22"]), ("U", t["s22"], t["s23"]), ("V", t["s23"], t["s24"]), ("W", t["s24"], tma), ("W2", tma, t["s25"]),
        ("X", t["s25"], tin), ("Y", tin, END)]
OBEN = [(0, "HIER ZAHLT MAN<br>MIT KOMPLIMENTEN ♥"), (tdh, "HERR KRAUSE: PLEITE"), (t["s2"], "30 JAHRE · LOB: 0"), (tih, "KOMPLIMENT-VERSUCH …"),
        (tkr, "1 KRÜMEL"), (t["s5"], "100 ♥ AUF DEM ZETTEL"), (t["s6"], "NEUES HANDY: ♥ 1"), (tab, "SYMMETRIE 10/10"), (tgr, "GRATIS 📱"),
        (t["s9"], "REICHSTE PERSON DER STADT"), (t["s10"], "70 JAHRE · x ∞"), (t["s11"], "YACHT XXL ⛵"), (t["s12"], "PREIS: ♥ 10.000"), (tzn, "ZÄHLT NICHT ❌"),
        (t["s14"], "???"), (tdr + .3, "KOMPLIMENT-DRUCKER 3000"), (t["s15"], "RRRT! RRRT!"), (t["s16"], "1.000.000 ZETTEL"), (t["s17"], "INFLATION 📈 300x"),
        (t["s18"], "KAUGUMMI = 1 GEDICHT"), (t["s19"], "♥ 1.000.000 → 1 ZAHNSTOCHER"), (t["s20"], "🚨 NEUE REGEL 🚨"), (t["s21"], "EHRLICH SEIN = REICH"),
        (t["s22"], "KACHING! 💰"), (t["s23"], "EHRLICH. JETZT."), (t["s24"], "🦆🦆🦆"), (t["s25"], "DEIN KOMPLIMENT? 👇"), (tin, "DIE KOMPLIMENT-STADT")]
kz_html = (f'<div id="kz" class="ui" style="left:24px;top:36px;background:#111;border:5px solid #ff4d6d;border-radius:16px;padding:6px 16px;font:900 36px Inter,sans-serif;color:#fff">'
           f'<span id="kzl">KRAUSE</span>: <span style="color:#ff4d6d">♥</span> <span id="kzv" style="color:#ffd166">0</span></div>')
prev = ("KRAUSE", "0")
for tt_, nm, v in sorted(KZ):
    if tt_ <= 0: continue
    settext("kzl", tt_, nm, prev[0]); settext("kzv", tt_, v, prev[1]); prev = (nm, v)
tag = f'<div class="ui clip" data-start="0" data-duration="{F(END)}" style="right:24px;top:40px;font:900 34px Inter,sans-serif;color:#fff;background:rgba(0,0,0,.55);padding:6px 14px;border-radius:12px">KOMPLIMENT-STADT #1</div>'
HOT = {"KOMPLIMENTEN", "KOMPLIMENTE", "KOMPLIMENT", "KRAUSE", "PLEITE", "KRÜMEL", "EINEN", "SPICKZETTEL", "PAUL", "HANDY", "AUGENBRAUEN", "SYMMETRISCH", "GRATIS", "OMA",
       "MILLION", "YACHT", "BADEWANNE", "RATHAUS", "BANK", "KOMPLIMENT-DRUCKER", "RRRT", "SCHÖNE", "SCHUHE", "SCHUHEN", "BRÖTCHEN", "GEDICHT", "REIM", "ZAHNSTOCHER",
       "EHRLICHKEIT", "LANGWEILIG", "KACHING", "MILLIONÄR", "KRAWATTE", "ENTEN", "GRÜN", "TEIL", "MEISTENS", "FOLG", "ZÄHLT", "NICHT"}
cam_fix()
finish(S, sets, OBEN, FX, HOT, tag, extra_ui=kz_html, banner=("TEIL 2?", "➕ FOLGEN"), oben_top=130, banner_top=300, cap_top=1250)
