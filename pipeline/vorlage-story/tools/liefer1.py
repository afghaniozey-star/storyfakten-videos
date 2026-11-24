"""STORY-FORMAT „In dieser Stadt …“ – NEUE SERIE „Liefer-Stadt“, TEIL 1: „Alles, was du laut sagst, wird per Drohne geliefert“.
Aufruf: python3 tools/liefer1.py  (liest voice.json + assets/vo/timing.json; Bausteine aus tools/bausteine.py;
Musik = fester Hintergrund-Sound assets/bgm.mp3 über tools/story_musik.py). Basis: tools/digga1.py (24.11.2026)."""
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

S = {}; FX = []
# --- A: Ortsschild an der Straße, Ich + 3 Drohnen (Bild 0)
S["A"] = (street_bg() + ortsschild(740, 760, .78) +
          fig(ich("ich1", "happy", arm=("down", "front")), 290, 1880, 1.55) +
          drone("dA1", 230, 420, .7) + drone("dA2", 560, 330, .55) + drone("dA3", 900, 470, .6) +
          f'<g id="pkA">{drone("dA4", 594, 1150, .8, parcel(160, 120, 160, "📦"), hov=False)}</g>')
# --- B: Kinderzimmer – Malte, Wand klappt auf, Kevin schwebt herein
BED = ('<rect x="40" y="1260" width="560" height="200" rx="20" fill="#e76f51" stroke="#111" stroke-width="8"/><rect x="40" y="1180" width="140" height="120" rx="30" fill="#fff" stroke="#111" stroke-width="6"/>'
       '<rect x="40" y="1450" width="40" height="120" fill="#6b4226" stroke="#111" stroke-width="6"/><rect x="560" y="1450" width="40" height="120" fill="#6b4226" stroke="#111" stroke-width="6"/>')
WALL = ('<g id="wall"><rect x="560" y="0" width="520" height="1200" fill="#bde0fe" stroke="#111" stroke-width="8"/>' + "".join(f'<rect x="{560 + k * 90}" y="0" width="45" height="1200" fill="#000" opacity=".03"/>' for k in range(6)) +
        '<rect x="700" y="330" width="280" height="300" fill="#8ecae6" stroke="#111" stroke-width="8"/><path d="M840 330 V630 M700 480 H980" stroke="#111" stroke-width="8"/>'
        f'<rect x="620" y="760" width="160" height="200" fill="#fff" stroke="#111" stroke-width="6"/><text x="700" y="880" text-anchor="middle" style="font:900 60px {FONT};fill:#e63946">⚽</text></g>')
S["B"] = ('<rect width="1080" height="1920" fill="#8ecae6"/>' + city_skyline(1200) +
          '<rect width="560" height="1200" fill="#bde0fe"/>' + "".join(f'<rect x="{k * 90}" y="0" width="45" height="1200" fill="#000" opacity=".03"/>' for k in range(7)) +
          WALL + '<rect y="1200" width="1080" height="720" fill="#c8a27c"/><rect y="1200" width="1080" height="16" fill="#000" opacity=".2"/>' + BED +
          fig(malte("ma1", "yawn", arm=("up", "down")), 330, 1330, 1.15) +
          bubble("bubB", ["BOCK AUF 'NEN", "ELEFANTEN!"], 330, 360, 560, tail=(0, 1), size=62) +
          f'<g id="eleB">{elephant("kv1", 790, 1820, .78, face="happy")}'
          f'<g id="eleDr">{"".join(drone(f"dB{k}", x, y, .55, ROPE(250 + (k % 2) * 40), hov=False) for k, (x, y) in enumerate(((520, 960), (700, 900), (880, 920), (1010, 990))))}</g></g>'
          '<g id="heftB" opacity="0"></g>')
# --- C: Ich flüstert (Nahaufnahme, Flur)
S["C"] = (room_bg("#cdb4db", "#9c6644", win=False) + '<rect x="620" y="300" width="300" height="420" fill="#fff8d6" stroke="#6b4226" stroke-width="14"/><text x="770" y="560" text-anchor="middle" style="font:900 180px ' + FONT + ';fill:#e63946">🤫</text>'
          + fig(ich("ich2", "whisper", extra=HANDMOUTH, head_acc=HANDFACE), 480, 1960, 2.1) +
          f'<g id="psst" opacity="0"><text x="700" y="700" text-anchor="middle" style="font:italic 900 80px {FONT};fill:#fff;stroke:#111;stroke-width:6px;paint-order:stroke">psst …</text></g>')
# --- D: Klassenzimmer – Herr Krause, 30 Drohnen mit Zetteln
NUMS = ["54", "57", "48", "65", "42", "63", "55", "49", "64", "58", "-3", "∞", "7", "560", "44", "56?"]
BOARD = ('<rect x="70" y="250" width="940" height="560" rx="16" fill="#2d6a4f" stroke="#6b4226" stroke-width="18"/>'
         f'<text id="task" x="540" y="390" text-anchor="middle" style="font:900 110px {FONT};fill:#fff">7 × 8 = ?</text>'
         '<g id="nums" opacity="0">' + "".join(
             f'<g transform="translate({130 + (k % 4) * 220} {520 + (k // 4) * 110})"><text x="0" y="0" style="font:900 56px {FONT};fill:#fff">{n}</text>'
             f'<path d="M-6 -50 L84 10 M84 -50 L-6 10" stroke="#e63946" stroke-width="10"/></g>' for k, n in enumerate(NUMS[4:16])) + '</g>')
swarm = "".join(drone(f"dD{k}", 1300 + (k % 3) * 60, 300 + k * 90, .45, f'{ROPE(120)}<rect x="-70" y="120" width="140" height="90" fill="#fff" stroke="#111" stroke-width="6"/><text x="0" y="185" text-anchor="middle" style="font:900 52px {FONT};fill:#111">{NUMS[k % 16]}</text>', hov=False) for k in range(12))
S["D"] = (room_bg("#e9f5db", "#b08968", win=False) + BOARD +
          '<rect x="860" y="860" width="200" height="300" fill="#8ecae6" stroke="#111" stroke-width="8"/>' +
          wrap("kz", person("kr", "glatze", "#555", "#6c757d", exprs=("neutral", "shock", "confused", "angry"), start="neutral", arm=("down", "front"), head_acc=KR_ACC), 760, 1900, 1.55) +
          '<rect x="60" y="1500" width="560" height="60" rx="10" fill="#8d5524" stroke="#111" stroke-width="7"/><rect x="90" y="1560" width="500" height="360" fill="#a0522d" stroke="#111" stroke-width="7"/>' +
          bubble("bubD", ["WER BRINGT MIR", "DIE LÖSUNG?"], 520, 1020, 600, tail=(1, 1), size=60) +
          f'<g id="swarmD">{swarm}</g>')
# --- E: Omas Küche
CUP = ('<g transform="translate(760 1290)"><rect x="-70" y="-110" width="140" height="120" rx="20" fill="#fff" stroke="#111" stroke-width="7"/><path d="M70 -80 Q120 -60 70 -20" stroke="#111" stroke-width="10" fill="none"/>'
       '<path id="steam" d="M-30 -140 q-20 -30 0 -60 q20 -30 0 -60 M30 -140 q-20 -30 0 -60 q20 -30 0 -60" stroke="#fff" stroke-width="10" fill="none" opacity=".9"/></g>')
S["E"] = (room_bg("#f7e1d7", "#7f5539") + '<rect x="60" y="300" width="180" height="230" fill="#fefae0" stroke="#6b4226" stroke-width="12"/><rect x="100" y="360" width="100" height="120" rx="30" fill="#a7c957"/>' +
          fig(oma("om1", "relief", arm=("front", "down")), 380, 1900, 1.6) +
          '<rect x="560" y="1300" width="500" height="40" rx="10" fill="#6b4226" stroke="#111" stroke-width="5"/><rect x="780" y="1340" width="40" height="580" fill="#6b4226" stroke="#111" stroke-width="5"/>' + CUP +
          bubble("bubE", ["ACH, WÄR ICH", "NOCHMAL JUNG …"], 510, 520, 620, tail=(-1, 1), size=62) +
          f'<g id="skdr" transform="translate(1400 0)">{drone("dE", 820, 700, .7, ROPE(170) + "<g id=\"skb0\"><rect x=\"-150\" y=\"170\" width=\"300\" height=\"40\" rx=\"20\" fill=\"#ef476f\" stroke=\"#111\" stroke-width=\"6\"/><rect x=\"-110\" y=\"205\" width=\"40\" height=\"40\" rx=\"20\" fill=\"#ffd166\" stroke=\"#111\" stroke-width=\"5\"/><rect x=\"70\" y=\"205\" width=\"40\" height=\"40\" rx=\"20\" fill=\"#ffd166\" stroke=\"#111\" stroke-width=\"5\"/></g>", hov=False)}</g>')
# --- F: Skatepark – Oma Kickflip, Ich liegt daneben
BOARD_SK = '<g id="skF"><rect x="-170" y="0" width="340" height="44" rx="22" fill="#ef476f" stroke="#111" stroke-width="7"/><rect x="-130" y="36" width="46" height="46" rx="23" fill="#ffd166" stroke="#111" stroke-width="5"/><rect x="84" y="36" width="46" height="46" rx="23" fill="#ffd166" stroke="#111" stroke-width="5"/></g>'
S["F"] = (sky() + city_skyline(1150, "#90a4ae") + '<rect y="1150" width="1080" height="770" fill="#adb5bd"/>'
          '<path d="M620 1150 Q1000 1150 1080 700 V1150 Z" fill="#ced4da" stroke="#111" stroke-width="8"/><path d="M0 1500 H1080" stroke="#868e96" stroke-width="6"/>'
          f'<text x="200" y="1090" style="font:900 70px {FONT};fill:#fff;stroke:#111;stroke-width:5px;paint-order:stroke">SKATEPARK</text>' +
          f'<g transform="translate(470 1500)"><g id="omaF">{fig(oma("om2", "grin", arm=("up", "out")), 0, -80, 1.1)}<g transform="translate(0 -60)">{BOARD_SK}</g></g></g>'
          f'<g transform="translate(860 1780) rotate(-80)">{fig(ich("ich3", "sad", arm=("up", "out")), 0, 0, 1.0)}</g>'
          '<g id="starsF">' + "".join(f'<path d="M{x} {y} l12 26 l28 4 l-20 20 l6 28 l-26 -14 l-26 14 l6 -28 l-20 -20 l28 -4 z" fill="#ffd166" stroke="#111" stroke-width="3"/>' for x, y in ((700, 1560), (780, 1500), (860, 1540))) + '</g>')
# --- G: Straße – Malte niest, Hatschi wird geliefert
FLUFF = ('<g id="hat"><g id="hat-in">' + "".join(f'<rect x="{-180 + dx - 40}" y="{dy - 40}" width="120" height="120" rx="60" fill="#ffafcc" stroke="#111" stroke-width="5"/>' for dx, dy in
         ((40, -160), (180, -190), (320, -160), (0, -60), (360, -60), (40, 40), (180, 70), (320, 40))) +
         '<rect x="-150" y="-180" width="360" height="300" rx="150" fill="#ffafcc"/>' + WEYE(-10, -60, 0, 4).replace('width="38" height="38"', 'width="60" height="60"') + WEYE(110, -60, 0, 4).replace('width="38" height="38"', 'width="60" height="60"') +
         '<path d="M20 30 Q50 60 80 30" stroke="#111" stroke-width="7" fill="none" stroke-linecap="round"/>'
         f'<g transform="rotate(8 200 120)"><rect x="140" y="80" width="230" height="74" rx="12" fill="#fff" stroke="#111" stroke-width="6"/><text x="255" y="134" text-anchor="middle" style="font:900 44px {FONT};fill:#e63946">HATSCHI</text></g></g></g>')
S["G"] = (street_bg() + fig(malte("ma2", "happy", arm=("down", "down")), 330, 1900, 1.7) +
          bubble("bubG", ["HATSCHI!"], 330, 560, 460, tail=(0, 1), size=86) +
          f'<g id="hatdr" transform="translate(0 -1300)">{drone("dG", 800, 700, .7, ROPE(330), hov=False)}<g transform="translate(690 1150)">{FLUFF}</g></g>' + puff("pfG", 330, 1000, 70, "!"))
# --- H: Marktplatz – Bürgermeister, Kissen-Lastwagen
PODY = 1380
PILE = ('<g id="pile" transform="translate(0 -1600)">' + "".join(pillow(x, y, w_, h, c, r) for x, y, w_, h, c, r in (
    (300, 1800, 340, 160, "#ffc8dd", -8), (700, 1810, 360, 170, "#bde0fe", 6), (520, 1700, 380, 160, "#caffbf", 3), (220, 1640, 300, 150, "#fdffb6", -12),
    (830, 1640, 300, 150, "#ffd6a5", 10), (420, 1560, 320, 150, "#a0c4ff", -6), (660, 1540, 320, 150, "#ffadad", 8), (540, 1420, 300, 140, "#bdb2ff", -4),
    (360, 1430, 260, 130, "#9bf6ff", 12), (730, 1420, 260, 130, "#fdffb6", -10), (540, 1310, 240, 120, "#ffc6ff", 5))) + '</g>')
CRATE = ('<g id="bigdr" transform="translate(0 -1400)">' + drone("dH", 540, 520, 1.6, '<path d="M-140 30 L-300 300 M140 30 L300 300" stroke="#333" stroke-width="8"/>'
         '<rect x="-330" y="290" width="660" height="330" rx="20" fill="none" stroke="#333" stroke-width="10" stroke-dasharray="26 14"/>' +
         "".join(pillow(x, y, 200, 90, c, r) for x, y, c, r in ((-190, 360, "#ffc8dd", 6), (20, 350, "#bde0fe", -4), (220, 370, "#caffbf", 8), (-100, 470, "#fdffb6", -6), (130, 480, "#ffadad", 4), (-220, 560, "#a0c4ff", 3), (200, 570, "#bdb2ff", -5), (-10, 570, "#ffd6a5", 0))) +
         f'<text x="0" y="680" text-anchor="middle" style="font:900 60px {FONT};fill:#111">1 LKW RUHE</text>', hov=False) + '</g>')
HATONLY = f'<g id="hatonly" opacity="0" transform="translate(540 1300)">{HAIR["hut"]("#ccc").replace("<path d", "<path opacity=\"0\" d", 1)}</g>'
S["H"] = ('<rect width="1080" height="1920" fill="#dde5b6"/><rect x="60" y="320" width="960" height="1000" fill="#f8f9fa" stroke="#111" stroke-width="8"/>' +
          "".join(f'<rect x="{110 + k * 220}" y="440" width="70" height="880" fill="#e9ecef" stroke="#111" stroke-width="5"/>' for k in range(5)) +
          '<path d="M40 330 L540 120 L1040 330 Z" fill="#ced4da" stroke="#111" stroke-width="8"/>' f'<text x="540" y="290" text-anchor="middle" style="font:900 68px {FONT};fill:#111">RATHAUS</text>'
          '<rect y="1320" width="1080" height="600" fill="#bc6c25"/>' + "".join(f'<rect x="{k * 120}" y="1320" width="118" height="600" fill="none" stroke="#9c5a1f" stroke-width="3"/>' for k in range(9)) +
          f'<g id="bmH">{wrap("bmz", bm("bm1", "determined", arm=("front", "up")), 540, 1880, 1.6)}</g>' +
          f'<g id="podH" transform="translate(540 {PODY})"><rect x="-220" y="0" width="440" height="560" fill="#264653" stroke="#111" stroke-width="8"/><rect x="-250" y="-20" width="500" height="40" rx="10" fill="#2a9d8f" stroke="#111" stroke-width="7"/>'
          '<rect x="-60" y="140" width="120" height="120" rx="60" fill="#ffd166" stroke="#111" stroke-width="6"/>'
          '<path d="M60 -20 L170 -150" stroke="#333" stroke-width="10"/><rect x="146" y="-196" width="56" height="64" rx="24" fill="#555" stroke="#111" stroke-width="4"/></g>' +
          bubble("bubH", ["MEHR RUHE!"], 540, 650, 560, tail=(0, 1), size=90) +
          PILE + HATONLY + CRATE +
          f'<g id="bm2g" opacity="0">{wrap("bm2z", bm("bm2", "shout", arm=("up", "up")), 540, 1330, 1.15)}</g>' +
          bubble("bubH2", ["DAS IST JA ZUM", "MÄUSEMELKEN!"], 540, 560, 760, tail=(0, 1), size=70))
# --- I: Mäuse-Regen über dem Marktplatz + Nahaufnahme einer Maus
import random
rnd = random.Random(7)
mice = "".join(f'<g class="mfall" data-k="{k}">{mouse(rnd.randint(30, 1050), rnd.randint(-200, 1700), rnd.uniform(.5, 1.0), rnd.randint(-30, 30))}</g>' for k in range(70))
S["I"] = ('<rect width="1080" height="1920" fill="#8ecae6"/>' + city_skyline(1400, "#90a4ae") + '<rect y="1400" width="1080" height="520" fill="#bc6c25"/>' +
          f'<g id="miceI">{mice}</g>' + mouse(540, 1150, 4.2, -8, "mbig") +
          '<g id="bucket" opacity="0"></g>')
# --- K: Chaos-Totale: Himmel schwarz vor Drohnen, Kevin auf dem Dach, Oma skatet, Ich auf Mülleimer
houses = ""
for k, (x, wd, h, c) in enumerate(((-20, 300, 520, "#f4a261"), (290, 260, 420, "#a8dadc"), (560, 260, 380, "#e9c46a"), (830, 270, 600, "#cdb4db"))):
    houses += (f'<rect x="{x}" y="{1250 - h}" width="{wd}" height="{h}" fill="{c}" stroke="#111" stroke-width="6"/>' +
               "".join(f'<rect x="{x + 40 + (j % 2) * (wd - 130)}" y="{1250 - h + 60 + (j // 2) * 130}" width="70" height="80" fill="#fff8d6" stroke="#111" stroke-width="4"/>' for j in range(2 * (h // 160))))
dark_swarm = "".join(drone(f"dK{k}", rnd.randint(0, 1080), rnd.randint(40, 640), rnd.uniform(.2, .38), hov=False) for k in range(46))
miceK = "".join(mouse(rnd.randint(20, 1060), rnd.randint(1290, 1560), .45, rnd.randint(-20, 20)) for k in range(26))
TRASH = '<g><rect x="-110" y="-300" width="220" height="300" rx="14" fill="#2a9d8f" stroke="#111" stroke-width="8"/><rect x="-130" y="-330" width="260" height="44" rx="12" fill="#21867a" stroke="#111" stroke-width="8"/><path d="M-50 -260 V-40 M0 -260 V-40 M50 -260 V-40" stroke="#1b6f65" stroke-width="10"/></g>'
S["K"] = ('<rect width="1080" height="1920" fill="#8ecae6"/><rect id="darkK" width="1080" height="1920" fill="#22223b" opacity=".85"/>' + houses +
          elephant("kv2", 965, 650, .42, face="panic", tag=True) +
          '<rect y="1250" width="1080" height="670" fill="#6c757d"/>' + "".join(f'<rect x="{k * 220 + 40}" y="1640" width="120" height="16" fill="#fff"/>' for k in range(5)) +
          f'<g id="swK">{dark_swarm}</g>' + f'<g id="miceK">{miceK}</g>' +
          f'<g id="omaK" transform="translate(-300 0)"><g transform="translate(200 1600)">{fig(oma("om3", "laugh", arm=("up", "out")), 0, -60, .55)}<g transform="translate(0 -50) scale(.55)">{BOARD_SK.replace("skF", "skK")}</g></g></g>' +
          f'<g id="ichK" opacity="0"><g transform="translate(360 1900)">{TRASH}{fig(ich("ich4", "determined", extra=MEGA), 0, -330, 1.25)}</g></g>' +
          bubble("bubK", ["ALLE DROHNEN SOLLEN", "VERSCHWINDEN!"], 540, 540, 900, tail=(-1, 1), size=66) +
          "".join(puff(f"pfK{k}", x, y, 70) for k, (x, y) in enumerate(((180, 250), (520, 180), (860, 300), (330, 520), (720, 560)))))
# --- N: Wendung – Rücken mit Propellern / dann von vorn, hebt ab
BACKVIEW = ('<g><ellipse cx="0" cy="6" rx="120" ry="22" fill="#000" opacity=".22"/>' + props("prN", vis=True) +
            '<rect x="-70" y="-70" width="58" height="72" rx="8" fill="#2b2d42" stroke="#111" stroke-width="5"/><rect x="12" y="-70" width="58" height="72" rx="8" fill="#2b2d42" stroke="#111" stroke-width="5"/>'
            f'<rect x="-98" y="-300" width="196" height="240" rx="22" fill="{YEL}" stroke="#111" stroke-width="5"/><rect x="-98" y="-300" width="196" height="240" rx="22" fill="url(#shade)"/>'
            + arms(YEL, "#f2c9a5", "down", "down") +
            '<g transform="translate(0 -400)"><rect x="-96" y="-96" width="192" height="192" rx="26" fill="#f2c9a5" stroke="#111" stroke-width="5"/><rect x="-96" y="-96" width="192" height="170" rx="26" fill="#6b3e26" stroke="#111" stroke-width="5"/></g></g>')
S["N"] = ('<rect width="1080" height="1920" fill="#8ecae6"/>' + city_skyline(1350) + '<rect y="1350" width="1080" height="570" fill="#6c757d"/>' +
          f'<g id="backN">{wrap("bkz", BACKVIEW, 540, 1800, 1.9)}</g>' +
          f'<g id="frontN" opacity="0"><g id="liftN">{fig(ich("ich5", "shock", arm=("out", "out"), behind=props("prN2")), 540, 1700, 1.6)}</g></g>' +
          f'<g id="surr" opacity="0"><text x="240" y="760" style="font:italic 900 90px {FONT};fill:#fff;stroke:#111;stroke-width:7px;paint-order:stroke">BRRRR</text></g>')
# --- O: Malte unten ruft, Ich wird weggezogen
S["O"] = (street_bg() + fig(malte("ma3", "shout", arm=("up", "down")), 300, 1900, 1.4) +
          bubble("bubO", ["BOCK AUF", "PIZZA! 🍕"], 330, 860, 480, tail=(0, 1), size=70) +
          f'<g id="flyO"><g transform="translate(760 1150)">{fig(ich("ich6", "panic", arm=("up", "out"), behind=props("prO")), 0, 0, .7)}</g></g>')
# --- P: Finale – Ich fliegt mit Schild „BESTELLUNG: ___?“ über dem Ortsschild (Loop zu Bild 0)
SIGN = ('<g transform="translate(0 -170)"><rect x="-280" y="-150" width="560" height="300" rx="24" fill="#fff" stroke="#111" stroke-width="10"/>'
        f'<text x="0" y="-50" text-anchor="middle" style="font:900 66px {FONT};fill:#e63946">BESTELLUNG:</text>'
        f'<text id="blank" x="0" y="96" text-anchor="middle" style="font:900 120px {FONT};fill:#111">___ ?</text></g>')
S["P"] = (sky() + city_skyline(1500) + '<rect y="1500" width="1080" height="420" fill="#6c757d"/>' + ortsschild(900, 1240, .5) +
          f'<g id="ichP"><g class="hov">{fig(ich("ich7", "laugh", arm=("front", "front"), behind=props("prP"), extra=SIGN), 390, 1300, 1.15)}</g></g>' +
          drone("dP1", 900, 380, .45) + drone("dP2", 150, 300, .35))

# ---------- Zeitplan ----------
J.append('tl.set("#cam", { x: 0, y: 0, scale: 1, svgOrigin: "0 0" }, 0);')
J.append(f'tl.fromTo(".rot", {{ scaleX: 1, transformOrigin: "50% 50%" }}, {{ scaleX: .25, duration: .05, yoyo: true, repeat: {int(END / .05)}, ease: "none" }}, 0);')
J.append(f'tl.fromTo(".hov", {{ y: 0 }}, {{ y: -14, duration: .45, yoyo: true, repeat: {int(END / .45)}, ease: "sine.inOut" }}, 0);')
s = st
LZ = []  # (Zeit, Text)
# s1 (0,0): Ortsschild + Ich, Drohne bringt sofort ein Paket
cut(0, 540, 1000, 1.0)
J.append('tl.fromTo("#pkA", { x: 600, y: -700 }, { x: 0, y: 0, duration: 1.1, ease: "power2.out" }, 0);')
FX += [("whoosh", 0, .5, .6)]
cut(s("s1") + 1.4, 600, 1100, 1.2)
tge = w("s1", "geliefert.") - .1
cut(min(tge, END), 330, 1150, 1.7); expr("ich1", "happy", "laugh", tge); FX += [("pop", tge, .5, .3)]
# s2: Kinderzimmer – Malte gähnt
t2 = s("s2")
J.append('tl.set("#eleB", { y: -1700 }, 0);')
cut(t2, 330, 1050, 1.5); expr("ma1", "yawn", "yawn", t2)
pop("#bubB", w("s2", "Ich") - .1, .25, "50% 100%"); cut(w("s2", "Ich") - .1, 380, 760, 1.25)
FX += [("boing", w("s2", "Elefanten.") - .1, .4, .4)]
# s3: Wand klappt auf, Kevin schwebt mit 4 Drohnen herein
t3 = s("s3")
hide("#bubB", t3, .1)
J.append(f'tl.to("#wall", {{ scaleX: 0, transformOrigin: "100% 50%", duration: .5, ease: "power2.in" }}, {F(t3)});')
cut(t3, 540, 960, 1.0); FX += [("whoosh", t3, .5, .6), ("klong", t3 + .45, .35, .5)]
tel = w("s3", "Elefant") - .2
J.append(f'tl.to("#eleB", {{ y: 0, duration: 1.0, ease: "power2.out" }}, {F(t3 + .4)});')
J.append(f'tl.to("#eleDr", {{ y: -1500, duration: .8, ease: "power2.in" }}, {F(t3 + 1.6)});')
FX += [("hit", t3 + 1.35, .5, .6)]; shake(t3 + 1.4, 7, 14); LZ.append((t3 + 1.4, "1"))
expr("ma1", "yawn", "shock", t3 + 1.4)
cut(t3 + 1.45, 700, 1350, 1.15)
# s4: Kevin frisst die Hausaufgaben (Nahaufnahme)
t4 = s("s4")
cut(t4, 600, 1620, 1.9)
tfr = w("s4", "frisst") - .1
J.append(f'tl.set("#kv1-heft", {{ opacity: 1 }}, {F(tfr - .2)});')
cut(tfr - .2, 420, 1700, 2.4); FX += [("splat", tfr, .4, .4)]
J.append(f'tl.to("#kv1-heft", {{ rotation: 25, transformOrigin: "50% 50%", duration: .12, yoyo: true, repeat: 9 }}, {F(tfr)});')
tha = w("s4", "Hausaufgaben") - .1
expr("ma1", "shock", "panic", tha); cut(tha, 330, 900, 1.8)
J.append(f'tl.to("#kv1-heft", {{ scale: 0, transformOrigin: "50% 50%", duration: .3 }}, {F(tha + .6)});')
# s5: Ich flüstere nur noch
t5 = s("s5")
cut(t5, 480, 1150, 1.0); cam(t5 + .05, 480, 1080, 1.25, 1.4, "none")
tfl = w("s5", "flüstere") - .1
cut(tfl, 520, 1000, 1.6); pop("#psst", tfl, .25, "50% 50%")
# s6: Mathe – Herr Krause
t6 = s("s6")
cut(t6, 540, 900, 1.0); cam(t6 + .05, 600, 900, 1.12, 1.2, "none")
tkr = w("s6", "Wer") - .1
pop("#bubD", tkr, .25, "100% 100%"); cut(tkr, 600, 950, 1.3)
# s7: 30 Drohnen fliegen rein, 30 Lösungen, alle falsch
t7 = s("s7")
hide("#bubD", t7, .1)
cut(t7, 540, 960, 1.0)
for k in range(12):
    tx = 170 + (k % 4) * 245 - (1300 + (k % 3) * 60); ty = 330 + (k // 4) * 170 - (300 + k * 90)
    J.append(f'tl.fromTo("#dD{k}", {{ x: 0, y: 0 }}, {{ x: {tx}, y: {ty}, duration: .7, ease: "power2.out", immediateRender: false }}, {F(t7 + .1 + k * .07)});')
FX += [("whoosh", t7 + .1, .5, .8), ("blips", t7 + .4, .3, 1.0)]
LZ.append((t7 + .4, "11")); LZ.append((t7 + .8, "21")); LZ.append((t7 + 1.2, "31"))
expr("kr", "neutral", "shock", t7 + .5)
tlo = w("s7", "Lösungen.") - .3
J.append(f'tl.to("#swarmD", {{ opacity: 0, duration: .2 }}, {F(tlo)}); tl.set("#nums", {{ opacity: 1 }}, {F(tlo)}); tl.set("#task", {{ opacity: .35 }}, {F(tlo)});')
cut(tlo, 540, 560, 1.15)
tfa = w("s7", "falsch.") - .15
cut(tfa, 760, 1000, 1.5); expr("kr", "shock", "angry", tfa); FX += [("hit", tfa, .5, .5)]
# s8: Oma seufzt beim Kaffee
t8 = s("s8")
cut(t8, 430, 1150, 1.2); cam(t8 + .05, 430, 1100, 1.35, 1.6, "none")
J.append(f'tl.fromTo("#steam", {{ y: 0, opacity: .9 }}, {{ y: -30, opacity: .3, duration: .8, repeat: 4, ease: "none", immediateRender: false }}, {F(t8)});')
tac = w("s8", "Ach,") - .1
pop("#bubE", tac, .25, "0% 100%"); cut(tac, 480, 800, 1.3)
# s9: Drohne bringt Skateboard → Oma Kickflip, Ich fällt
t9 = s("s9")
hide("#bubE", t9, .1)
cut(t9, 700, 1000, 1.1)
J.append(f'tl.fromTo("#skdr", {{ x: 1400 }}, {{ x: 0, duration: .6, ease: "power2.out", immediateRender: false }}, {F(t9)});'); FX += [("whoosh", t9, .5, .6)]
expr("om1", "relief", "shock", t9 + .5); LZ.append((t9 + .5, "32"))
tsk = w("s9", "Oma") - .1
cut(tsk, 470, 1200, 1.1)
J.append(f'tl.fromTo("#omaF", {{ y: 0 }}, {{ y: -200, duration: .45, yoyo: true, repeat: 3, ease: "power2.out", immediateRender: false }}, {F(tsk)});')
J.append(f'tl.fromTo("#skF", {{ rotation: 0, transformOrigin: "50% 50%" }}, {{ rotation: 360, duration: .45, repeat: 1, ease: "none", immediateRender: false }}, {F(tsk + .05)});')
FX += [("swoosh", tsk, .5, .5), ("klong", tsk + .9, .4, .4)]
tbe = w("s9", "Besser") - .1
cut(tbe, 760, 1650, 1.7); FX += [("splat", tbe, .4, .4)]
J.append(f'tl.fromTo("#starsF", {{ rotation: 0, transformOrigin: "50% 50%" }}, {{ rotation: 30, duration: .3, yoyo: true, repeat: 5, immediateRender: false }}, {F(tbe)});')
# s10: Malte niest – Hatschi wird geliefert
t10 = s("s10")
cut(t10, 330, 1250, 1.55)
tha1 = w("s10", "Hatschi!") - .1
expr("ma2", "happy", "sneeze", tha1); pop("#bubG", tha1, .2, "50% 100%"); plopp("pfG", tha1); FX += [("splat", tha1, .5, .4)]; shake(tha1, 5, 10)
tpr = w("s10", "Prompt") - .1
hide("#bubG", tpr, .1)
J.append(f'tl.fromTo("#hatdr", {{ y: -1300 }}, {{ y: 0, duration: .7, ease: "power2.out", immediateRender: false }}, {F(tpr)});'); FX += [("whoosh", tpr, .5, .6)]
cut(tpr, 600, 1050, 1.0); LZ.append((tpr + .6, "33"))
tke = w("s10", "Keiner") - .1
expr("ma2", "sneeze", "confused", tke); cut(tke, 820, 1100, 1.8)
J.append(f'tl.to("#hat-in", {{ scaleY: .9, scaleX: 1.08, transformOrigin: "50% 100%", duration: .25, yoyo: true, repeat: 5 }}, {F(tke)});')
tfl2 = w("s10", "flauschig.") - .2
cut(tfl2, 760, 1060, 1.9); FX += [("chime", tfl2, .4, .8)]
# s11: Bürgermeister fordert Ruhe
t11 = s("s11")
cut(t11, 540, 1000, 1.0); cam(t11 + .05, 540, 1050, 1.25, 1.4, "none")
tru = w("s11", "Mehr") - .1
pop("#bubH", tru, .25, "50% 100%"); cut(tru, 540, 900, 1.6); FX += [("hit", tru, .3, .4)]
expr("bm1", "determined", "shout", tru)
# s12: Riesen-Drohne bringt einen Lastwagen Kissen – begraben
t12 = s("s12")
hide("#bubH", t12, .1)
cut(t12, 540, 960, 1.0)
J.append(f'tl.fromTo("#bigdr", {{ y: -1400 }}, {{ y: 0, duration: .9, ease: "power2.out", immediateRender: false }}, {F(t12)});'); FX += [("riser", t12, .35, 1.0)]
expr("bm1", "shout", "shock", t12 + .6)
tdi = w("s12", "Direkt") - .2
J.append(f'tl.fromTo("#pile", {{ y: -1600 }}, {{ y: 0, duration: .45, ease: "bounce.out", immediateRender: false }}, {F(tdi)});')
J.append(f'tl.to("#bigdr", {{ y: -1500, duration: .7, ease: "power2.in" }}, {F(tdi + .2)});')
J.append(f'tl.set("#bmH, #podH", {{ opacity: 0 }}, {F(tdi + .4)}); tl.set("#hatonly", {{ opacity: 1 }}, {F(tdi + .4)});')
FX += [("hit", tdi + .35, .6, .6)]; shake(tdi + .35, 9, 16); LZ.append((tdi + .35, "34"))
cut(tdi + .45, 540, 1250, 1.6)
# s13: Er brüllt – Mäusemelken – 10.000 Mäuse
t13 = s("s13")
J.append(f'tl.set("#bm2g", {{ opacity: 1 }}, {F(t13)}); tl.set("#hatonly", {{ opacity: 0 }}, {F(t13)});')
cut(t13, 540, 820, 1.45); pop("#bubH2", t13 + .2, .25, "50% 100%"); FX += [("boing", t13, .4, .4)]
tzt = w("s13", "Zehntausend") - .25
J.append(f'tl.fromTo(".mfall", {{ y: -1900 }}, {{ y: 0, duration: 1.4, stagger: .012, ease: "power1.in", immediateRender: false }}, {F(tzt)});')
cut(tzt, 540, 960, 1.0); FX += [("blips", tzt, .35, 1.2), ("tick", tzt, .3, 1.2)]
count("lzv", tzt, 34, 10034, 1.2)
tme = w("s13", "Eimern.") - .3
cut(tme, 540, 1200, 1.0); cam(tme + .05, 540, 1220, 1.15, .8, "none")
# s14: Totale – Himmel schwarz vor Drohnen, Kevin aufs Dach, Oma skatet
t14 = s("s14")
cut(t14, 540, 960, 1.0)
J.append(f'tl.fromTo("#omaK", {{ x: -300 }}, {{ x: 1300, duration: 3.2, ease: "none", immediateRender: false }}, {F(t14 + .2)});'); FX += [("whoosh", t14, .4, .6)]
for k in range(46): J.append(f'tl.to("#dK{k}", {{ x: {rnd.randint(-120, 120)}, y: {rnd.randint(-60, 60)}, duration: 1.2, yoyo: true, repeat: 3, ease: "sine.inOut" }}, {F(t14)});')
count("lzv", t14 + .1, 10034, 99999, 2.2)
tkv = w("s14", "Kevin") - .1
cut(tkv, 930, 520, 2.1); FX += [("boing", tkv + .2, .4, .4)]
J.append(f'tl.to("#kv2", {{ x: -8, duration: .06, yoyo: true, repeat: 15 }}, {F(tkv)});')
tda = w("s14", "Dach.") - .1
cut(tda, 400, 1450, 1.6)
# s15: Ich auf dem Mülleimer, schreie
t15 = s("s15")
J.append(f'tl.set("#ichK", {{ opacity: 1 }}, {F(t15)});')
cut(t15, 360, 1250, 1.5); cam(t15 + .05, 360, 1180, 1.7, 1.4, "none")
tsc = w("s15", "schreie:") - .1
expr("ich4", "determined", "shout", tsc)
pop("#bubK", tsc + .1, .25, "0% 100%"); cut(tsc, 540, 900, 1.0); shake(tsc + .2, 7, 12); FX += [("hit", tsc + .2, .3, .4)]
# s16: PUFF – Stille – alle Drohnen weg
t16 = s("s16")
P16 = w("s16", "puff!") - .12
hide("#bubK", t16, .05)
cut(t16, 540, 700, 1.15)
for k in range(5): plopp(f"pfK{k}", P16 + k * .06, .55)
J.append(f'tl.set("#swK", {{ opacity: 0 }}, {F(P16 + .1)}); tl.to("#darkK", {{ opacity: 0, duration: .6 }}, {F(P16 + .1)});')
FX += [("pop", P16, .8, .4), ("glitch", P16, .3, .3)]
expr("ich4", "shout", "neutral", P16 + .25)
tsl = w("s16", "Stille.") - .1
cut(tsl, 360, 1250, 1.6); cam(tsl + .05, 360, 1250, 1.75, 1.6, "none")
settext("lzv", P16 + .1, "0", "99.999")
# s17: Wendung – Propeller wachsen aus dem Rücken
t17 = s("s17")
cut(t17, 540, 1200, 1.0)
J.append(f'tl.fromTo("#prN", {{ scale: 0, transformOrigin: "50% 100%" }}, {{ scale: 1, duration: .6, ease: "back.out(2)", immediateRender: false }}, {F(t17 + .3)}); tl.set("#prN", {{ scale: 0 }}, 0);')
pop("#surr", t17 + .2, .25, "50% 50%"); FX += [("riser", t17, .35, 1.2), ("tick", t17 + .2, .3, 1.0)]
tpp = w("s17", "Propeller") - .1
cut(tpp, 540, 1000, 1.45); hide("#surr", tpp, .1)
tiw = w("s17", "Irgendwer") - .2
J.append(f'tl.set("#backN", {{ opacity: 0 }}, {F(tiw)}); tl.set("#frontN", {{ opacity: 1 }}, {F(tiw)});')
J.append(f'tl.fromTo("#liftN", {{ y: 0 }}, {{ y: -260, duration: 1.4, ease: "power1.inOut", immediateRender: false }}, {F(tiw)});')
cut(tiw, 540, 1000, 1.6); cam(tiw + .05, 540, 820, 1.6, 1.2, "power1.inOut"); FX += [("whoosh", tiw, .4, .6)]
# s18: Malte ruft – Pizza – ich fliege los
t18 = s("s18")
cut(t18, 480, 1150, 1.2)
tpz = w("s18", "Pizza!") - .3
pop("#bubO", w("s18", "Ich") - .1, .25, "50% 100%"); cut(tpz, 540, 960, 1.0)
LZ.append((tpz + .3, "1"))
tfl3 = w("s18", "fliege") - .2
J.append(f'tl.to("#flyO", {{ x: 700, y: -500, duration: .9, ease: "power2.in" }}, {F(tfl3)});'); FX += [("whoosh", tfl3, .5, .7)]
expr("ich6", "panic", "shock", tfl3); cut(tfl3, 760, 820, 1.35)
# s19: Frage – Schild BESTELLUNG ___? bleibt bis zum Ende
t19 = s("s19")
cut(t19, 400, 1000, 1.3)
J.append(f'tl.to("#blank", {{ opacity: .2, duration: .3, yoyo: true, repeat: 40, ease: "steps(1)" }}, {F(t19 + .3)});')
FX += [("chime", t19, .35, .8)]
tsr = w("s19", "Schreib's") - .1
cut(tsr, 400, 1150, 1.45)
tbs = w("s19", "Bestellung") - .1
cut(tbs, 600, 1050, 1.2)
# s20: Folgen + Loop-Satz – letzte 3 s Kamerafahrt zurück aufs Ortsschild (wie Bild 0)
t20 = s("s20")
cut(t20, 400, 1050, 1.45)
tdn = w("s20", "Denn") - .1
cut(tdn, 420, 1000, 1.3)
tcam = round(END - 3.0, 2)
cam(tcam, 540, 1000, 1.0, 2.8, "power2.inOut")
sets = [("A", 0, t2), ("B", t2, t5), ("C", t5, t6), ("D", t6, t8), ("E", t8, tsk), ("F", tsk, t10), ("G", t10, t11), ("H", t11, tzt), ("I", tzt, t14),
        ("K", t14, t17), ("N", t17, t18), ("O", t18, t19), ("P", t19, END)]

# Liefer-Zähler oben links (ab Bild 0)
lz_html = (f'<div id="lz" class="ui" style="left:24px;top:36px;background:#111;border:5px solid {YEL};border-radius:16px;padding:6px 16px;font:900 38px Inter,sans-serif;color:#fff">'
           f'<span id="lzl">LIEFERUNGEN:</span> <span id="lzv" style="color:{YEL}">0</span></div>')
prev = "0"
for tt, v in LZ:
    if tt < tzt or tt > t16:
        settext("lzv", tt, v, prev)
    prev = v
    J.append(f'tl.fromTo("#lz", {{ scale: 1.25, transformOrigin: "0% 0%" }}, {{ scale: 1, duration: .25, ease: "back.out(3)", immediateRender: false }}, {F(tt)});')
# Ab der Wendung zählt der Zähler „DROHNEN“
settext("lzl", P16 + .1, "DROHNEN:", "LIEFERUNGEN:")
settext("lzl", tpz + .3, "LIEFERUNGEN:", "DROHNEN:")
settext("lzv", t17 + .5, "1 (ICH)", "0")
settext("lzv", tpz + .3, "100.000", "1 (ICH)")
tag = f'<div class="ui clip" data-start="0" data-duration="{F(END)}" style="right:24px;top:40px;font:900 34px Inter,sans-serif;color:#fff;background:rgba(0,0,0,.55);padding:6px 14px;border-radius:12px">LIEFER-STADT #1</div>'
OBEN = [(0, "ALLES, WAS DU LAUT SAGST,<br>WIRD GELIEFERT 🚁"), (t2, "„BOCK AUF 'NEN ELEFANTEN“"), (t3, "LIEFERZEIT: 10 SEK."), (t4, "KEVIN 🐘 FRISST HAUSAUFGABEN"), (t5, "PSST – NUR NOCH FLÜSTERN"),
        (t6, "MATHE"), (t7, "30 LÖSUNGEN – <span style='color:#ff4d5a'>ALLE FALSCH</span>"), (t8, "„WÄR ICH NOCHMAL JUNG …“"), (tsk, "OMA: KICKFLIP <span style='color:#2dc653'>✔</span> · ICH: <span style='color:#ff4d5a'>✘</span>"),
        (tpr, "LIEFERUNG: 1x HATSCHI"), (t11, "BÜRGERMEISTER-REDE"), (t12, "LIEFERUNG: RUHE (1 LKW KISSEN)"), (tzt, "10.000 MÄUSE 🐭"), (t14, "CHAOS"),
        (t15, "„ALLE DROHNEN SOLLEN VERSCHWINDEN!“"), (P16 + .1, "PUFF! DROHNEN: 0"), (t17 + .5, "DROHNEN: 1 (DU)"), (t18, "NEUE BESTELLUNG: PIZZA 🍕"),
        (t19, "DEINE BESTELLUNG? 👇")]
HOT = {"DROHNE", "DROHNEN", "ELEFANT", "ELEFANTEN", "KEVIN", "HATSCHI", "RUHE", "MÄUSE", "MÄUSEMELKEN", "PROPELLER", "PIZZA", "BESTELLUNG", "KOMMENTARE", "GELIEFERT", "LAUT", "KISSEN", "SKATEBOARD", "FALSCH"}
cam_fix()
finish(S, sets, OBEN, FX, HOT, tag, extra_ui=lz_html, banner=("TEIL 2?", "➕ FOLGEN"), oben_top=130, banner_top=250, cap_top=1250)
