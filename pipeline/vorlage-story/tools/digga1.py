"""STORY-FORMAT „In dieser Stadt …“ – NEUE SERIE „Digga-Stadt“, TEIL 1: „Jedes Digga kostet einen Zentimeter“.
Aufruf: python3 tools/digga1.py  (liest voice.json + assets/vo/timing.json; Bausteine aus tools/bausteine.py;
Musik = fester Hintergrund-Sound assets/bgm.mp3 über tools/story_musik.py)"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bausteine import *

# ---------- zusätzliche Mimik / Haare / Zubehör ----------
FACES["sneeze"] = ('<path d="M-46 -4 L-16 -4 M16 -4 L46 -4" stroke="#111" stroke-width="8" stroke-linecap="round"/><path d="M-50 -24 L-14 -14 M50 -24 L14 -14" stroke="#111" stroke-width="6" stroke-linecap="round"/>'
                   '<ellipse cx="0" cy="40" rx="22" ry="20" fill="#5a1a1a" stroke="#111" stroke-width="4"/>')
FACES["angry"] = (E(-30, 2) + E(30, 2) + '<path d="M-52 -34 L-12 -14 M52 -34 L12 -14" stroke="#111" stroke-width="9" stroke-linecap="round"/>'
                  '<path d="M-26 46 Q0 28 26 46" stroke="#111" stroke-width="8" fill="none" stroke-linecap="round"/>')
FACES["smug"] = ('<path d="M-46 -6 H-14" stroke="#111" stroke-width="8" stroke-linecap="round"/>' + E(30, -5) +
                 '<path d="M-24 34 Q4 48 30 28" stroke="#111" stroke-width="7" fill="none" stroke-linecap="round"/>')
HAIR["jonas"] = lambda c: (f'<path d="M-100 -30 V-96 Q-100 -112 -84 -112 H84 Q100 -112 100 -96 V-30 L80 -70 H-80 Z" fill="{c}" stroke="#111" stroke-width="4"/>'
                           '<path d="M-104 -70 Q-104 -150 0 -150 Q104 -150 104 -70 Z" fill="#e63946" stroke="#111" stroke-width="5"/><rect x="-150" y="-86" width="90" height="26" rx="10" fill="#c1121f" stroke="#111" stroke-width="4"/>')
HAIR["ich"] = lambda c: f'<path d="M-100 -36 V-100 Q-100 -114 -86 -114 H86 Q100 -114 100 -100 V-36 L74 -64 L40 -80 L0 -66 L-40 -84 L-76 -62 Z" fill="{c}" stroke="#111" stroke-width="4"/>'
HAIR["cap"] = lambda c: (f'<path d="M-104 -60 Q-104 -150 0 -150 Q104 -150 104 -60 Z" fill="{c}" stroke="#111" stroke-width="5"/><rect x="-20" y="-82" width="190" height="26" rx="10" fill="{c}" stroke="#111" stroke-width="4"/>')
HAIR["beanie"] = lambda c: (f'<path d="M-104 -40 V-110 Q-104 -150 -60 -152 H60 Q104 -150 104 -110 V-40 Z" fill="{c}" stroke="#111" stroke-width="5"/><rect x="-110" y="-62" width="220" height="40" rx="12" fill="#111" opacity=".3"/>')
HAIR["hut"] = lambda c: ('<path d="M-100 -30 V-90 L-80 -70 H80 L100 -90 V-30 Z" fill="#ccc"/><rect x="-140" y="-120" width="280" height="30" rx="10" fill="#111"/><rect x="-80" y="-250" width="160" height="140" rx="10" fill="#111"/><rect x="-80" y="-150" width="160" height="26" fill="#e63946"/>')
JONAS_EX = ("happy", "angry", "shock", "laugh", "confused", "sneeze", "panic", "joy" if "joy" in FACES else "laugh", "neutral")
JONAS_EX = tuple(dict.fromkeys(JONAS_EX))
def jonas(uid, start="happy", shirt="#e63946", arm=("down", "down"), arm2=None, extra=""):
    return person(uid, "jonas", "#f4d35e", shirt, exprs=JONAS_EX, start=start, arm=arm, arm2=arm2, extra=extra)
ICH_EX = ("happy", "smug", "shock", "laugh", "determined", "neutral")
MONO = '<rect x="12" y="-26" width="40" height="40" rx="8" fill="#cde" fill-opacity=".4" stroke="#d4a017" stroke-width="6"/><path d="M52 0 Q70 60 50 110" stroke="#d4a017" stroke-width="4" fill="none"/>'
BOW = '<g transform="translate(0 -292)"><path d="M0 0 L-60 -32 V32 Z M0 0 L60 -32 V32 Z" fill="#7b2cbf" stroke="#111" stroke-width="5"/><rect x="-14" y="-14" width="28" height="28" rx="6" fill="#5a189a" stroke="#111" stroke-width="4"/></g>'
def ich(uid, start="happy", fancy=False, arm=("down", "down")):
    return person(uid, "ich", "#6b3e26", "#118ab2", exprs=ICH_EX, start=start, arm=arm, head_acc=MONO if fancy else "", extra=BOW if fancy else "")
KR_ACC = '<rect x="-62" y="-22" width="48" height="36" rx="8" fill="none" stroke="#111" stroke-width="6"/><rect x="14" y="-22" width="48" height="36" rx="8" fill="none" stroke="#111" stroke-width="6"/><path d="M-14 -6 H14" stroke="#111" stroke-width="6"/>'
OMA_ACC = '<rect x="-64" y="-20" width="46" height="34" rx="16" fill="none" stroke="#555" stroke-width="5"/><rect x="18" y="-20" width="46" height="34" rx="16" fill="none" stroke="#555" stroke-width="5"/>'
SASH = '<path d="M-90 -290 L90 -80" stroke="#e63946" stroke-width="34"/><rect x="-24" y="-240" width="48" height="48" rx="24" fill="#ffd166" stroke="#111" stroke-width="4"/>'
def bgm_(uid, start="neutral", arm=("down", "down"), extra=""):
    return person(uid, "hut", "#ccc", "#264653", exprs=("neutral", "shock", "confused", "happy", "determined"), start=start, arm=arm, extra=SASH + extra)
def hamster(uid, s=1.0, x=0, y=0):
    return (f'<g id="{uid}" transform="translate({x} {y}) scale({s})"><rect x="-150" y="-260" width="300" height="260" rx="90" fill="#f4a261" stroke="#111" stroke-width="7"/>'
            '<rect x="-100" y="-150" width="200" height="150" rx="70" fill="#fff1e0"/><rect x="-130" y="-300" width="70" height="70" rx="30" fill="#f4a261" stroke="#111" stroke-width="6"/><rect x="60" y="-300" width="70" height="70" rx="30" fill="#f4a261" stroke="#111" stroke-width="6"/>'
            + E(-50, -190, 14) + E(50, -190, 14) + '<rect x="-14" y="-160" width="28" height="18" rx="8" fill="#ff8fa3" stroke="#111" stroke-width="3"/>'
            '<rect x="-95" y="-150" width="50" height="34" rx="16" fill="#ff8fa3" opacity=".6"/><rect x="45" y="-150" width="50" height="34" rx="16" fill="#ff8fa3" opacity=".6"/></g>')
def cm_badge(uid, text, y=-600, size=70, vis=True, col="#ffd166"):
    return badge(uid, text, col=col, fg="#111", size=size, y=y, vis=vis, chars=max(4, len(text)))
def grow(sel, t, a, b, d=.22, ease="back.out(2)"):
    J.append(f'tl.fromTo("{sel}", {{ scale: {a}, transformOrigin: "50% 100%" }}, {{ scale: {b}, duration: {d}, ease: "{ease}", immediateRender: false }}, {F(t)});')
def wrap(uid, content, x, fy, s):  # Figur mit eigener Schrumpf-Gruppe (Ursprung = Füße)
    return f'<g transform="translate({x} {fy})"><g id="{uid}" transform="scale({s})">{content}</g></g>'
def puff(uid, x, y, r=60):
    return (f'<g id="{uid}" opacity="0" transform="translate({x} {y})">' + "".join(f'<rect x="{dx - r / 2:.0f}" y="{dy - r / 2:.0f}" width="{r}" height="{r}" rx="{r / 2:.0f}" fill="#fff" stroke="#111" stroke-width="4"/>'
            for dx, dy in ((-r, 0), (r, 0), (0, -r), (0, r * .6), (-r * .7, -r * .7), (r * .7, -r * .7))) +
            f'<text x="0" y="{r * .25:.0f}" text-anchor="middle" style="font:900 {r * .8:.0f}px {FONT};fill:#e63946;stroke:#111;stroke-width:3px;paint-order:stroke">PLOPP</text></g>')
def plopp(uid, t, d=.45):
    J.append(f'tl.fromTo("#{uid}", {{ opacity: 1, scale: .3, transformOrigin: "50% 50%" }}, {{ opacity: 0, scale: 1.5, duration: {d}, ease: "power2.out", immediateRender: false }}, {F(t)});')

S = {}; FX = []
# --- A: Straße – Jonas winzig (Zoom), daneben Hamster und mein Riesen-Schuh
JX, JFY, JS = 760, 1880, .36
MARKLESS = street_bg().replace('height="16" fill="#fff"/>', 'height="16" fill="#8b9299"/>')
S["A"] = (MARKLESS + fig(ich("ich1", "laugh"), 300, 1900, 1.6) +
          hamster("ham1", .36 * .55, 900, 1885) +
          wrap("j1", jonas("jo1", "angry", arm=("down", "up")) + cm_badge("cm1", "10 CM") + bubble("bub1", ["DIGGA!"], 0, -860, 420, tail=(0, 1), size=80), JX, JFY, JS) +
          puff("pf1", JX, JFY - 260 * JS, 70 * JS * 1.4))
# --- B: Turnschuh-Wohnung
SHOE = ('<g><path d="M120 1860 V1350 Q120 1180 300 1160 L520 1140 Q600 1300 760 1380 L930 1450 Q1010 1490 1000 1600 V1860 Z" fill="#fff" stroke="#111" stroke-width="10"/>'
        '<rect x="100" y="1780" width="920" height="90" rx="30" fill="#e63946" stroke="#111" stroke-width="10"/>'
        '<path d="M380 1200 L470 1330 M440 1180 L540 1310 M330 1240 L420 1360" stroke="#111" stroke-width="10"/><path d="M600 1500 Q760 1440 960 1560" stroke="#3a86ff" stroke-width="30" fill="none"/>'
        '<rect x="170" y="1420" width="200" height="170" rx="16" fill="#8ecae6" stroke="#111" stroke-width="8"/><path d="M270 1420 V1590 M170 1505 H370" stroke="#111" stroke-width="6"/>'
        '<rect x="640" y="1600" width="120" height="180" rx="14" fill="#6b4226" stroke="#111" stroke-width="7"/><rect x="740" y="1690" width="14" height="14" rx="7" fill="#ffd166"/>'
        f'<rect x="420" y="1630" width="180" height="60" rx="10" fill="#ffd166" stroke="#111" stroke-width="5"/><text x="510" y="1675" text-anchor="middle" style="font:900 40px {FONT};fill:#111">JONAS</text>'
        '<path d="M520 1140 V1040 M500 1040 H540 V1000 H500 Z" stroke="#555" stroke-width="10" fill="#555"/></g>')
S["B"] = (street_bg() + '<rect y="1300" width="1080" height="620" fill="#95d5b2"/>' + SHOE +
          '<g id="winj">' + fig(jonas("jo2", "happy", arm=("down", "up")), 270, 1600, .32) + '</g>'
          '<rect x="170" y="1580" width="200" height="14" fill="#111"/>' +
          wrap("j2", jonas("jo3", "angry", arm=("hip", "hip")) + cm_badge("cm2", "9 CM") + bubble("bub4", ["DIGGA,", "NICHT LUSTIG!"], 0, -900, 560, tail=(0, 1), size=70), 860, 1800, JS) +
          puff("pf2", 860, 1800 - 80, 60))
# --- D: Ich mit Fliege + Monokel (von unten)
S["D"] = (street_bg() + fig(ich("ich2", "smug", fancy=True, arm=("down", "hip")), 540, 1950, 1.95) +
          bubble("bub5", ["WERTER", "FREUND."], 760, 640, 440, tail=(-1, 1), size=64))
# --- E: Schule mit Messlatte
stu = ""
for k, (x, sh, hc, hair) in enumerate(((150, "#ffbe0b", "#3d2b1f", "mann"), (380, "#8338ec", "#111", "lena"), (610, "#06d6a0", "#a0522d", "ich"))):
    stu += f'<g id="st{k}">' + fig(person(f"sp{k}", hair, hc, sh, skin=("#f2c9a5", "#c68642", "#8d5524")[k], exprs=("happy", "determined", "shock"), start="happy" if k != 2 else "determined"), x, 1900, 1.25) + '</g>'
RULER = ('<g><rect x="820" y="420" width="190" height="1480" fill="#ffd166" stroke="#111" stroke-width="8"/>' +
         "".join(f'<rect x="820" y="{1900 - k * 74}" width="{60 if k % 2 else 100}" height="8" fill="#111"/>' + (f'<text x="1000" y="{1912 - k * 74}" text-anchor="end" style="font:900 40px {FONT};fill:#111">{k * 10}</text>' if k % 2 == 0 and k else "") for k in range(20)) + '</g>')
S["E"] = ('<rect width="1080" height="1920" fill="#8ecae6"/><rect x="0" y="420" width="1080" height="900" fill="#e9c46a" stroke="#111" stroke-width="8"/>' +
          "".join(f'<rect x="{60 + k * 190}" y="520" width="130" height="150" fill="#fff8d6" stroke="#111" stroke-width="5"/>' for k in range(4)) +
          f'<rect x="300" y="300" width="480" height="130" rx="20" fill="#fff" stroke="#111" stroke-width="7"/><text x="540" y="390" text-anchor="middle" style="font:900 72px {FONT};fill:#111">SCHULE</text>'
          '<rect y="1320" width="1080" height="600" fill="#adb5bd"/>' + RULER + stu +
          '<path d="M60 1150 H680" stroke="#e63946" stroke-width="10" stroke-dasharray="30 16"/>' f'<text x="70" y="1130" style="font:900 44px {FONT};fill:#e63946">MIN. 1,40 M</text>')
# --- F: Klassenzimmer – Herr Krause hinterm Pult
S["F"] = (room_bg("#e9f5db", "#b08968", win=False) + '<rect x="90" y="270" width="900" height="420" rx="16" fill="#2d6a4f" stroke="#6b4226" stroke-width="18"/>'
          +
          wrap("kz", person("kr", "glatze", "#555", "#6c757d", exprs=("neutral", "shock", "confused", "angry"), start="neutral", arm=("down", "front"), head_acc=KR_ACC)
               + '<g id="chalk"><rect x="176" y="-350" width="40" height="18" rx="6" fill="#fff" stroke="#111" stroke-width="3"/></g>', 560, 1900, 1.6) +
          '<rect x="200" y="1430" width="720" height="70" rx="10" fill="#8d5524" stroke="#111" stroke-width="7"/><rect x="230" y="1500" width="660" height="420" fill="#a0522d" stroke="#111" stroke-width="7"/>'
          '<g id="chb" opacity="0"><rect x="420" y="1400" width="22" height="18" rx="5" fill="#fff" stroke="#111" stroke-width="3" transform="rotate(25 430 1410)"/><rect x="460" y="1404" width="22" height="18" rx="5" fill="#fff" stroke="#111" stroke-width="3" transform="rotate(-20 470 1412)"/></g>' +
          puff("pf3", 560, 1250, 90))
# --- G: Omas Wohnzimmer – Mini-Pulli
chair = ('<g><rect x="-170" y="-430" width="340" height="390" rx="40" fill="#9b2226" stroke="#111" stroke-width="6"/>'
         '<rect x="-200" y="-140" width="60" height="140" rx="20" fill="#7a1b1f" stroke="#111" stroke-width="5"/><rect x="140" y="-140" width="60" height="140" rx="20" fill="#7a1b1f" stroke="#111" stroke-width="5"/></g>')
KNIT = ('<g transform="translate(0 -200)"><path d="M-60 -40 L80 60 M60 -40 L-80 60" stroke="#adb5bd" stroke-width="10" stroke-linecap="round"/>'
        '<rect x="-40" y="0" width="80" height="60" rx="16" fill="#80ed99" stroke="#111" stroke-width="4"/></g><g transform="translate(150 -40)"><rect x="-50" y="-50" width="100" height="100" rx="50" fill="#80ed99" stroke="#111" stroke-width="5"/><path d="M-40 -20 Q0 10 40 -20 M-40 15 Q0 40 40 15" stroke="#38b000" stroke-width="5" fill="none"/></g>')
OX, OFY, OS = 320, 1900, 1.55
S["G"] = (room_bg("#f7e1d7", "#7f5539") + '<rect x="60" y="300" width="180" height="230" fill="#fefae0" stroke="#6b4226" stroke-width="12"/><rect x="100" y="360" width="100" height="120" rx="30" fill="#a7c957"/>' +
          wrap("oz", person("om", "oma", "#e0e0e0", "#9d4edd", exprs=("relief", "happy", "shock", "laugh"), start="relief", arm=("front", "front"), behind=chair, extra=KNIT, head_acc=OMA_ACC), OX, OFY, OS) +
          '<rect x="640" y="1500" width="400" height="40" rx="10" fill="#6b4226" stroke="#111" stroke-width="5"/><rect x="820" y="1540" width="40" height="380" fill="#6b4226" stroke="#111" stroke-width="5"/>' +
          wrap("j3", jonas("jo4", "laugh", shirt="#80ed99", arm=("hip", "up")) + cm_badge("cm3", "8 CM", size=80) +
               f'<text x="0" y="-160" text-anchor="middle" style="font:900 70px {FONT};fill:#111">XXS</text>', 760, 1500, .32) +
          '<g id="mom" opacity="0">' + wrap("om2w", person("om2", "oma", "#e0e0e0", "#80ed99", exprs=("shock",), start="shock", head_acc=OMA_ACC), 930, 1500, .3) + '</g>' +
          puff("pf4", OX, 1350, 90))
S["PT"] = ('<rect width="1080" height="1920" fill="#f7e1d7"/>' + "".join(f'<rect x="0" y="{k * 90}" width="1080" height="45" fill="#000" opacity=".03"/>' for k in range(22)) +
           '<g transform="translate(540 1150)"><rect x="-300" y="-300" width="600" height="600" rx="300" fill="#80ed99" stroke="#111" stroke-width="10"/>'
           + "".join(f'<path d="M-280 {-200 + k * 80} Q0 {-120 + k * 80} 280 {-200 + k * 80}" stroke="#38b000" stroke-width="10" fill="none"/>' for k in range(6)) +
           '<path d="M200 -200 L330 -420" stroke="#111" stroke-width="8"/></g>'
           '<g id="tag" transform="rotate(-10 700 650)"><rect x="440" y="520" width="520" height="300" rx="26" fill="#fff" stroke="#111" stroke-width="9"/><rect x="470" y="560" width="40" height="40" rx="20" fill="#f7e1d7" stroke="#111" stroke-width="5"/>'
           f'<text x="720" y="640" text-anchor="middle" style="font:900 52px {FONT};fill:#111">WOLLE</text><text x="720" y="760" text-anchor="middle" style="font:900 104px {FONT};fill:#e63946">89,99 €</text></g>')
# --- H: Park – Rap-Battle
def rapper(uid, hair, col, shirt):
    return person(uid, hair, col, shirt, exprs=("determined", "angry", "shock", "panic"), start="determined", arm=("mic", "up"),
                  extra='<g transform="translate(74 -300)"><rect x="-14" y="-10" width="28" height="90" rx="8" fill="#333"/><rect x="-26" y="-60" width="52" height="56" rx="20" fill="#888" stroke="#111" stroke-width="4"/></g>'
                        '<path d="M-60 -290 Q0 -200 60 -290" stroke="#ffd166" stroke-width="14" fill="none"/>')
crowd = "".join(f'<g transform="translate({x} {y}) scale({s})"><rect x="-98" y="-300" width="196" height="300" rx="22" fill="{c}" stroke="#111" stroke-width="5"/><rect x="-96" y="-496" width="192" height="192" rx="26" fill="#3d2b1f" stroke="#111" stroke-width="5"/></g>'
                for x, y, s, c in ((80, 2000, .9, "#e76f51"), (300, 2050, 1.0, "#3a86ff"), (540, 1990, .85, "#8338ec"), (770, 2060, 1.0, "#2a9d8f"), (1000, 2000, .9, "#ffbe0b")))
S["H"] = ('<rect width="1080" height="1920" fill="#8ecae6"/>' + "".join(f'<rect x="{x}" y="{y}" width="200" height="200" rx="60" fill="#52b788" stroke="#111" stroke-width="6"/>' for x, y in ((-40, 760), (900, 700), (120, 680))) +
          '<rect y="980" width="1080" height="940" fill="#74c69d"/><rect x="60" y="380" width="960" height="140" rx="20" fill="#111" stroke="#fff" stroke-width="6"/>'
          f'<text x="540" y="480" text-anchor="middle" style="font:900 90px {FONT};fill:#ffd166">RAP-BATTLE 🎤</text>'
          '<rect x="80" y="1260" width="920" height="120" fill="#6b4226" stroke="#111" stroke-width="8"/><rect x="80" y="1240" width="920" height="30" fill="#8d5524" stroke="#111" stroke-width="6"/>' +
          wrap("rz1", rapper("ra1", "cap", "#7b2cbf", "#9d4edd"), 320, 1250, 1.15) + wrap("rz2", rapper("ra2", "beanie", "#2d6a4f", "#06d6a0"), 760, 1250, 1.15) +
          '<g id="minimics" opacity="0">' + "".join(f'<g transform="translate({x} 1240)"><rect x="-4" y="-40" width="8" height="40" fill="#333"/><rect x="-9" y="-56" width="18" height="18" rx="8" fill="#888" stroke="#111" stroke-width="2"/></g>' for x in (300, 790)) + '</g>'
          '<g id="ants">' + "".join(f'<g id="ant{k}" transform="translate({x} 1238)"><rect x="-7" y="-14" width="14" height="14" rx="3" fill="{c}" stroke="#111" stroke-width="2"/><rect x="-5" y="-24" width="10" height="10" rx="2" fill="#f2c9a5" stroke="#111" stroke-width="2"/></g>' for k, (x, c) in enumerate(((340, "#9d4edd"), (740, "#06d6a0")))) + '</g>'
          + crowd + puff("pf5", 320, 900, 80) + puff("pf6", 760, 900, 80) +
          '<g id="pigeon" transform="translate(1300 1180)"><rect x="-230" y="-260" width="460" height="300" rx="140" fill="#adb5bd" stroke="#111" stroke-width="8"/><rect x="-330" y="-480" width="230" height="230" rx="80" fill="#8d99ae" stroke="#111" stroke-width="8"/>'
          '<rect x="-300" y="-300" width="170" height="60" rx="20" fill="#7b2cbf" opacity=".5"/>' + WEYE(-250, -400, -8, 0) + '<path d="M-330 -380 L-420 -350 L-330 -330 Z" fill="#fb8500" stroke="#111" stroke-width="5"/>'
          '<rect x="100" y="-240" width="220" height="80" rx="30" fill="#6c757d" stroke="#111" stroke-width="6"/><path d="M-60 40 V120 M60 40 V120" stroke="#fb8500" stroke-width="16"/></g>')
# --- I: Pressekonferenz am Rathaus
PODY = 1380
S["I"] = ('<rect width="1080" height="1920" fill="#dde5b6"/><rect x="60" y="320" width="960" height="1000" fill="#f8f9fa" stroke="#111" stroke-width="8"/>' +
          "".join(f'<rect x="{110 + k * 220}" y="440" width="70" height="880" fill="#e9ecef" stroke="#111" stroke-width="5"/>' for k in range(5)) +
          '<path d="M40 330 L540 120 L1040 330 Z" fill="#ced4da" stroke="#111" stroke-width="8"/>' f'<text x="540" y="290" text-anchor="middle" style="font:900 68px {FONT};fill:#111">RATHAUS</text>'
          '<rect y="1320" width="1080" height="600" fill="#9d0208"/>' +
          wrap("bmz", bgm_("bm", "neutral", arm=("front", "down")), 540, 1880, 1.7) +
          f'<g transform="translate(540 {PODY})"><rect x="-220" y="0" width="440" height="560" fill="#264653" stroke="#111" stroke-width="8"/><rect x="-250" y="-20" width="500" height="40" rx="10" fill="#2a9d8f" stroke="#111" stroke-width="7"/>'
          '<rect x="-60" y="140" width="120" height="120" rx="60" fill="#ffd166" stroke="#111" stroke-width="6"/>'
          '<g id="mics"><path d="M-60 -20 L-210 -130 M60 -20 L210 -130" stroke="#333" stroke-width="10"/><rect x="-246" y="-170" width="60" height="64" rx="24" fill="#555" stroke="#111" stroke-width="4"/><rect x="186" y="-170" width="60" height="64" rx="24" fill="#e63946" stroke="#111" stroke-width="4"/></g>'
          '<g id="match" opacity="0"><rect x="-90" y="-80" width="180" height="62" rx="6" fill="#f4a261" stroke="#111" stroke-width="5"/><rect x="-60" y="-70" width="120" height="42" fill="#e63946"/></g></g>' +
          '<g id="mmay" opacity="0">' + wrap("mmz", bgm_("bm2", "shock", arm=("up", "up")) + cm_badge("cm4", "12 CM", size=90), 540, PODY - 98, .2) + '</g>' +
          puff("pf7", 540, 1150, 90) +
          '<g transform="translate(140 1960) scale(1.3)"><rect x="-98" y="-300" width="196" height="300" rx="22" fill="#3a86ff" stroke="#111" stroke-width="5"/><rect x="-96" y="-496" width="192" height="192" rx="26" fill="#111" stroke="#111" stroke-width="5"/>'
          '<rect x="40" y="-470" width="150" height="110" rx="14" fill="#333" stroke="#111" stroke-width="5"/><rect x="90" y="-440" width="60" height="50" rx="25" fill="#8ecae6"/></g>'
          '<g transform="translate(960 1960) scale(1.3)"><rect x="-98" y="-300" width="196" height="300" rx="22" fill="#ffbe0b" stroke="#111" stroke-width="5"/><rect x="-96" y="-496" width="192" height="192" rx="26" fill="#6b3e26" stroke="#111" stroke-width="5"/>'
          '<rect x="-190" y="-460" width="150" height="110" rx="14" fill="#333" stroke="#111" stroke-width="5"/><rect x="-150" y="-430" width="60" height="50" rx="25" fill="#8ecae6"/></g>'
          '<rect id="flash" width="1080" height="1920" fill="#fff" opacity="0"/>')
S["R2"] = ('<rect width="1080" height="1920" fill="#dde5b6"/><rect x="60" y="320" width="960" height="1000" fill="#f8f9fa" stroke="#111" stroke-width="8"/>' +
           "".join(f'<rect x="{110 + k * 220}" y="440" width="70" height="880" fill="#e9ecef" stroke="#111" stroke-width="5"/>' for k in range(5)) + '<rect y="1320" width="1080" height="600" fill="#9d0208"/>' +
           fig(person("rep", "lena", "#e76f51", "#4361ee", skin="#c68642", exprs=("determined",), start="determined", arm=("down", "mic"),
                      extra='<g transform="translate(74 -300)"><rect x="-14" y="-10" width="28" height="90" rx="8" fill="#333"/><rect x="-30" y="-64" width="60" height="60" rx="22" fill="#e63946" stroke="#111" stroke-width="4"/></g>'), 420, 1950, 1.9) +
           bubble("bub15", ["WIE STOPPEN", "WIR DAS?"], 700, 560, 560, tail=(-1, 1), size=64))
# --- K1: Straße voller Mini-Leute + Riesen-Katze / K2: Bus mit Jonas + Hamstern
minis = "".join(fig(person(f"mn{k}", ("mann", "lena", "oma", "ich")[k % 4], ("#3d2b1f", "#f4d35e", "#ddd", "#111")[k % 4], ("#e76f51", "#3a86ff", "#9d4edd", "#06d6a0")[k % 4], exprs=("panic",), start="panic"), 120 + k * 120, 1240 + (k % 2) * 30, .22) for k in range(8))
CAT = ('<g id="cat" transform="translate(800 1300)"><rect x="-260" y="-420" width="520" height="420" rx="80" fill="#f77f00" stroke="#111" stroke-width="9"/>'
       '<path d="M-240 -380 L-200 -560 L-80 -420 Z M240 -380 L200 -560 L80 -420 Z" fill="#f77f00" stroke="#111" stroke-width="9" stroke-linejoin="round"/>'
       + WEYE(-100, -280, -10, 6).replace('width="38" height="38"', 'width="60" height="60"') + WEYE(100, -280, -10, 6).replace('width="38" height="38"', 'width="60" height="60"') +
       '<path d="M-30 -200 L0 -180 L30 -200" stroke="#111" stroke-width="7" fill="none"/><path d="M-60 -150 Q0 -110 60 -150" stroke="#111" stroke-width="7" fill="none"/><path d="M-200 -190 H-90 M-200 -160 H-90 M90 -190 H200 M90 -160 H200" stroke="#111" stroke-width="5"/>'
       '<rect x="-250" y="-40" width="140" height="80" rx="30" fill="#f77f00" stroke="#111" stroke-width="7"/></g>')
S["K1"] = (street_bg() + CAT + minis)
S["K2"] = ('<rect width="1080" height="1920" fill="#8ecae6"/><rect y="1500" width="1080" height="420" fill="#6c757d"/>'
           '<rect x="40" y="300" width="1000" height="1500" rx="90" fill="#ffd60a" stroke="#111" stroke-width="12"/><rect x="100" y="420" width="880" height="760" rx="40" fill="#bde0fe" stroke="#111" stroke-width="10"/>'
           f'<rect x="300" y="330" width="480" height="70" rx="14" fill="#111"/><text x="540" y="385" text-anchor="middle" style="font:900 54px {FONT};fill:#ffd166">LINIE 1 · MINI</text>' +
           hamster("ham2", .5, 250, 1100) + hamster("ham3", .5, 830, 1100) +
           wrap("j4", jonas("jo5", "determined" if "determined" in JONAS_EX else "happy", arm=("front", "front")) + cm_badge("cm5", "8 CM", size=80), 540, 1150, .78) +
           '<g transform="translate(540 1060)"><rect x="-160" y="-30" width="320" height="60" rx="30" fill="none" stroke="#111" stroke-width="22"/></g>'
           '<rect x="100" y="1180" width="880" height="60" fill="#111" opacity=".15"/>'
           '<rect x="110" y="1330" width="200" height="130" rx="60" fill="#fff8d6" stroke="#111" stroke-width="8"/><rect x="770" y="1330" width="200" height="130" rx="60" fill="#fff8d6" stroke="#111" stroke-width="8"/>'
           '<rect x="380" y="1360" width="320" height="90" rx="14" fill="#111"/>' + "".join(f'<rect x="{400 + k * 50}" y="1375" width="30" height="60" fill="#555"/>' for k in range(6)) +
           '<rect x="100" y="1780" width="160" height="120" rx="20" fill="#111"/><rect x="820" y="1780" width="160" height="120" rx="20" fill="#111"/>' +
           bubble("bub18", ["HATSCHI!", "ALTER."], 800, 640, 400, tail=(-1, 1), size=62) + puff("pf8", 400, 640, 70))
JONAS_EX = JONAS_EX
# --- M: Marktplatz – alle brüllen ALTER und wachsen
crowdM = ""
for k, (x, fy, s0) in enumerate(((130, 1900, .5), (330, 1820, .35), (540, 1900, .6), (760, 1830, .4), (950, 1900, .5), (230, 1500, .25), (850, 1500, .3))):
    crowdM += wrap(f"cm_{k}", person(f"cr{k}", ("mann", "lena", "oma", "ich", "cap", "beanie", "lena")[k], ("#3d2b1f", "#f4d35e", "#ddd", "#111", "#7b2cbf", "#2d6a4f", "#e76f51")[k],
                                     ("#e76f51", "#3a86ff", "#9d4edd", "#06d6a0", "#ffbe0b", "#ef476f", "#118ab2")[k], exprs=("laugh",), start="laugh", arm=("up", "up")) +
                   bubble(f"bubm{k}", ["ALTER!"], 0, -820, 420, size=80), x, fy, s0)
S["M"] = ('<rect width="1080" height="1920" fill="#8ecae6"/><rect x="0" y="600" width="1080" height="800" fill="#e9c46a" stroke="#111" stroke-width="6"/>' +
          "".join(f'<rect x="{50 + k * 210}" y="700" width="130" height="160" fill="#fff8d6" stroke="#111" stroke-width="5"/>' for k in range(5)) +
          '<rect y="1300" width="1080" height="620" fill="#ced4da"/>' + "".join(f'<rect x="{k * 120}" y="1300" width="118" height="620" fill="none" stroke="#adb5bd" stroke-width="3"/>' for k in range(9)) + crowdM)
# --- N: Riesen-Jonas neben dem Rathaus
TOWN = ('<rect x="90" y="760" width="560" height="1000" fill="#f8f9fa" stroke="#111" stroke-width="8"/><path d="M60 770 L370 560 L680 770 Z" fill="#ced4da" stroke="#111" stroke-width="8"/>'
        f'<text x="370" y="740" text-anchor="middle" style="font:900 56px {FONT};fill:#111">RATHAUS</text>' +
        "".join(f'<rect x="{140 + (k % 3) * 170}" y="{850 + (k // 3) * 260}" width="120" height="170" fill="#bde0fe" stroke="#111" stroke-width="5"/>' for k in range(9)) +
        '<rect x="300" y="1600" width="140" height="160" fill="#6b4226" stroke="#111" stroke-width="6"/>')
S["N"] = ('<rect width="1080" height="1920" fill="#a2d2ff"/><rect y="1760" width="1080" height="160" fill="#6c757d"/>' +
          fig(jonas("jo6", "laugh", arm=("hip", "up")), 860, 1960, 3.3) + TOWN +
          fig(bgm_("bm3", "shock", arm=("up", "up")), 310, 1100, .3) +
          f'<g id="b40" opacity="0"><rect x="60" y="300" width="330" height="130" rx="30" fill="#ffd166" stroke="#111" stroke-width="8"/><text x="225" y="395" text-anchor="middle" style="font:900 96px {FONT};fill:#111">40 M</text></g>'
          f'<g id="b3850" opacity="0"><rect x="40" y="460" width="560" height="140" rx="30" fill="#111" stroke="#fff" stroke-width="8"/><text id="b3850t" x="320" y="560" text-anchor="middle" style="font:900 84px {FONT};fill:#fff">0 / 3.850</text></g>')
# --- O: Bürgermeister mit Schild „VERBOTEN: ___“ + Riesen-Jonas im Hintergrund
SIGN = ('<rect x="-176" y="-680" width="22" height="220" fill="#8d5524" stroke="#111" stroke-width="4"/><rect x="154" y="-680" width="22" height="220" fill="#8d5524" stroke="#111" stroke-width="4"/>'
        f'<g transform="translate(0 -820)"><rect x="-230" y="-150" width="460" height="300" rx="24" fill="#fff" stroke="#111" stroke-width="10"/>'
        f'<text x="0" y="-40" text-anchor="middle" style="font:900 64px {FONT};fill:#e63946">VERBOTEN:</text>'
        f'<text id="blank" x="0" y="100" text-anchor="middle" style="font:900 110px {FONT};fill:#111">___ ?</text></g>')
S["O"] = ('<rect width="1080" height="1920" fill="#a2d2ff"/><rect y="1500" width="1080" height="420" fill="#6c757d"/>' +
          '<g transform="translate(870 760) scale(2.2)"><rect x="-98" y="96" width="196" height="240" rx="22" fill="#e63946" stroke="#111" stroke-width="5"/>'
          f'<g transform="translate(0 0)"><rect x="-96" y="-96" width="192" height="192" rx="26" fill="#f2c9a5" stroke="#111" stroke-width="5"/>{HAIR["jonas"]("#f4d35e")}'
          f'<g id="jo7-confused">{FACES["confused"]}</g><g id="jo7-laugh" opacity="0">{FACES["laugh"]}</g></g></g>' +
          '<g transform="translate(0 0)">' + TOWN.replace('x="90" y="760"', 'x="-160" y="760"') + '</g>' +
          fig(bgm_("bm4", "determined", arm=("up", "up"), extra=SIGN), 365, 1900, 1.5) +
          bubble("bub23", ["DIGGA."], 870, 400, 330, tail=(0, 1), size=72) + puff("pf9", 870, 700, 90) +
          f'<g id="c3850" opacity="0"><rect x="600" y="1070" width="460" height="120" rx="26" fill="#111" stroke="#fff" stroke-width="7"/><text x="830" y="1155" text-anchor="middle" style="font:900 74px {FONT};fill:#fff">1 / 3.850</text></g>')

# ---------- Zeitplan ----------
J.append('tl.set("#cam", { x: 0, y: 0, scale: 1, svgOrigin: "0 0" }, 0);')
s = st
DZ = []  # (Zeit, Zählerstand)
# s1 (0,0): Jonas (Zoom) sagt DIGGA – PLOPP – kleiner
cut(0, JX, JFY - 250, 3.7); cam(.05, JX, JFY - 265, 4.0, 1.2, "power1.out")
J.append('tl.set("#bub1", { opacity: 1 }, 0); tl.fromTo("#bub1-in", { scale: 1.4, transformOrigin: "50% 50%" }, { scale: 1, duration: .25, ease: "back.out(3)", immediateRender: false }, 0);')
FX += [("boing", 0, .4, .4)]
tk = w("s1", "kleiner.") - .25
plopp("pf1", tk); grow("#j1", tk, JS, JS * .88, .25, "power3.in"); settext("cm1-t", tk, "9 CM", "10 CM"); FX += [("pop", tk, .7, .3)]
DZ.append((tk, 1)); hide("#bub1", tk - .05, .05); expr("jo1", "angry", "shock", tk)
cut(w("s1", "Digga") - .1, JX, JFY - 230, 3.2) if w("s1", "Digga") - .1 > .9 else None
# s2: Kamera kippt nach unten – so groß wie ein Hamster
t2 = s("s2")
cut(t2, 640, 1450, 1.6); cam(t2 + .05, 640, 1550, 1.35, 1.6)
tha = w("s2", "Hamster.") - .2
cut(tha, 840, JFY - 150, 2.8); FX += [("boing", tha, .4, .4)]
J.append(f'tl.to("#ham1", {{ y: "-=8", duration: .15, yoyo: true, repeat: 5 }}, {F(tha)});')
expr("jo1", "shock", "angry", tha)
# s3: Turnschuh-Wohnung
t3 = s("s3")
cut(t3, 270, 1480, 3.0)
J.append(f'tl.to("#jo2-a1", {{ rotation: 10, transformOrigin: "50% 80%", duration: .2, yoyo: true, repeat: 7 }}, {F(t3)});')
tts = w("s3", "Turnschuh.") - .3
cut(tts, 560, 1300, 1.0); cam(tts + .05, 560, 1400, 1.12, 1.0, "none"); FX += [("whoosh", tts, .3, .5)]
# s4: Jonas wütend – PLOPP – 8 cm
t4 = s("s4")
J.append('tl.set("#bub4", { opacity: 0 }, 0);')
cut(t4, 860, 1800 - 230, 4.6); pop("#bub4", w("s4", "Digga,") - .1, .2, "50% 50%")
tp4 = w("s4", "Plopp.") - .1
plopp("pf2", tp4); grow("#j2", tp4, JS, JS * .88, .25, "power3.in"); settext("cm2-t", tp4, "8 CM", "9 CM"); FX += [("pop", tp4, .8, .3)]
hide("#bub4", tp4, .05); DZ.append((tp4, 2)); cut(tp4, 860, 1800 - 200, 3.8)
expr("jo3", "angry", "shock", tp4 + .1)
# s5: Ich mit Fliege + Monokel
t5 = s("s5")
cut(t5, 540, 1300, 1.25); cam(t5 + .05, 540, 1250, 1.4, 1.5, "none")
twf = w("s5", "werter") - .1
pop("#bub5", twf, .25, "50% 50%"); cut(twf, 600, 1000, 1.5); FX += [("chime", twf, .3, .8)]
expr("ich2", "smug", "happy", twf + .4)
# s6: Messlatte am Schuleingang
t6 = s("s6")
cut(t6, 540, 1000, 1.0)
tme = w("s6", "Messlatten") - .1
cut(tme, 700, 1200, 1.35)
J.append(f'tl.to("#st2", {{ y: -70, duration: .25, yoyo: true, repeat: 5, ease: "sine.inOut" }}, {F(tme + .1)});'); FX += [("boing", tme + .1, .3, .4)]
# s7: Krause lässt die Kreide fallen – Digga – PLOPP
t7 = s("s7")
cut(t7, 560, 1100, 1.3)
tkr = w("s7", "Kreide") - .1
J.append(f'tl.to("#chalk", {{ y: 260, rotation: 90, duration: .35, ease: "power2.in", transformOrigin: "50% 50%" }}, {F(tkr)}); tl.set("#chalk", {{ opacity: 0 }}, {F(tkr + .36)});')
J.append(f'tl.set("#chb", {{ opacity: 1 }}, {F(tkr + .36)}); tl.set("#chb", {{ opacity: 0 }}, {F(s("s9"))});'); FX += [("klong", tkr + .35, .25, .5)]
expr("kr", "neutral", "shock", tkr + .35)
cut(tkr + .4, 560, 1300, 1.7)
td7 = w("s7", "Digga.") - .05
plopp("pf3", td7); grow("#kz", td7, 1.6, 1.45, .25, "power3.in"); FX += [("pop", td7, .8, .3)]; DZ.append((td7, 3))
cut(td7, 560, 1150, 1.15)
# s8: nochmal, nochmal – nur noch Haare übers Pult
t8 = s("s8")
for k, word in enumerate(("nochmal.", "nochmal.")):
    tt = w("s8", word, k + 1) - .1
    plopp("pf3", tt); grow("#kz", tt, (1.45, 1.32)[k], (1.32, 1.2)[k], .22, "power3.in"); FX += [("pop", tt, .8, .3)]; DZ.append((tt, 4 + k))
    cut(tt, 560, 1250 + k * 80, 1.25 + k * .2)
expr("kr", "shock", "confused", w("s8", "Jetzt") - .1)
cam(w("s8", "Jetzt") - .1, 560, 1420, 1.9, .8)
# s9: Oma strickt Jonas einen Mini-Pulli
t9 = s("s9")
cut(t9, OX + 60, 1250, 1.4); cam(t9 + .05, OX + 60, 1300, 1.5, 1.5, "none")
J.append(f'tl.to("#om-a1, #om-a2", {{ rotation: 4, transformOrigin: "50% 20%", duration: .15, yoyo: true, repeat: 11 }}, {F(t9)});')
tso = w("s9", "Aus") - .1
cut(tso, 790, 1430, 3.2); FX += [("pop", tso, .4, .3)]
J.append(f'tl.to("#j3", {{ rotation: 6, transformOrigin: "50% 100%", duration: .2, yoyo: true, repeat: 5 }}, {F(tso)});')
# s10: Wollpreis – Digga – Oma schrumpft in den Pulli
t10 = s("s10")
tdg = w("s10", "Digga!") - .1
td10 = tdg
plopp("pf4", td10); grow("#oz", td10, OS, .01, .25, "power3.in"); FX += [("pop", td10, .8, .3)]; DZ.append((td10, 6))
expr("om", "relief", "shock", t10 + .2)
J.append(f'tl.fromTo("#mom", {{ opacity: 0 }}, {{ opacity: 1, duration: .1, immediateRender: false }}, {F(td10 + .3)});')
tjp = w("s10", "Jetzt") - .1
cut(t10 + .05, 700, 700, 1.3); cam(t10 + .1, 720, 680, 1.55, 1.2)
cut(td10, 540, 1150, 1.0); cut(tjp, 860, 1430, 3.0)
FX += [("hit", t10 + .05, .4, .6)]
# s11: Rap-Battle im Park
t11 = s("s11")
cut(t11, 540, 1000, 1.0); cam(t11 + .05, 540, 1050, 1.15, 1.6, "none")
J.append(f'tl.to("#rz1, #rz2", {{ y: -20, duration: .15, yoyo: true, repeat: 9 }}, {F(t11 + .2)});')
# s12: PLOPP-Gewitter – Ameisen
t12 = s("s12")
cut(t12, 540, 1100, 1.35)
tst = w("s12", "Strophe") - .2
for k in range(6):
    tt = tst + k * .22
    plopp("pf5" if k % 2 == 0 else "pf6", tt, .3); FX += [("pop", tt, .55, .2)]
grow("#rz1", tst, 1.15, .01, 1.3, "steps(6)"); grow("#rz2", tst + .1, 1.15, .01, 1.3, "steps(6)")
J.append(f'tl.set("#ants", {{ opacity: 0 }}, 0); tl.set("#ants", {{ opacity: 1 }}, {F(tst + 1.4)}); tl.set("#minimics", {{ opacity: 1 }}, {F(tst + 1.4)});')
DZ.append((tst, 10)); DZ.append((tst + .5, 25)); DZ.append((tst + 1.0, 43))
tam = w("s12", "Ameisen.") - .2
cut(max(tam, tst + 1.4), 540, 1215, 5.0)
J.append(f'tl.set("#rz1, #rz2", {{ opacity: 0 }}, {F(tst + 1.45)});')
# s13: Taube hält sie für Brotkrümel
t13 = s("s13")
cut(t13, 650, 1150, 1.3)
J.append(f'tl.to("#pigeon", {{ x: 980, duration: .6, ease: "power2.out" }}, {F(t13)}); tl.to("#pigeon", {{ rotation: 18, transformOrigin: "-70% 0%", duration: .15, yoyo: true, repeat: 7 }}, {F(t13 + .7)});')
FX += [("whoosh", t13, .4, .6)]
J.append(f'tl.to("#ant0, #ant1", {{ x: "-=180", duration: 1.6, ease: "none" }}, {F(t13 + .5)});')
tbr = w("s13", "Krümel.") - .3
cut(tbr, 620, 1215, 3.2); FX += [("boing", tbr + .2, .3, .3)]
# s14: Pressekonferenz
t14 = s("s14")
cut(t14, 540, 1000, 1.0); cam(t14 + .05, 540, 1150, 1.3, 1.8, "none")
for k in range(4): J.append(f'tl.fromTo("#flash", {{ opacity: .6 }}, {{ opacity: 0, duration: .15, immediateRender: false }}, {F(t14 + .2 + k * .45)});'); FX += [("tick", t14 + .2, .3, 1.5)]
# s15: Reporter fragt – Digga, keine Ahnung – Mikro riesig
t15 = s("s15")
cut(t15, 600, 1100, 1.2)
J.append('tl.set("#bub15", { opacity: 0 }, 0);'); pop("#bub15", w("s15", "Wie") - .1, .2, "50% 50%")
ter = w("s15", "Er:") - .1
cut(ter, 540, 1000, 1.55); expr("bm", "neutral", "confused", ter)
J.append(f'tl.to("#bm-a1", {{ y: -20, duration: .15, yoyo: true, repeat: 3 }}, {F(ter)});')
td15 = w("s15", "Digga,") - .05
plopp("pf7", td15); grow("#bmz", td15, 1.7, 1.3, .25, "power3.in"); FX += [("pop", td15, .8, .3)]; DZ.append((td15, 44))
cut(td15 + .3, 540, 1250, 1.7)
# s16: Er redet weiter – Streichholzschachtel
t16 = s("s16")
cut(t16, 540, 1150, 1.25)
for k in range(5):
    tt = t16 + .3 + k * .35
    plopp("pf7", tt, .3); FX += [("pop", tt, .5, .2)]
grow("#bmz", t16 + .3, 1.3, .01, 1.7, "steps(5)")
DZ.append((t16 + .6, 60)); DZ.append((t16 + 1.2, 80)); DZ.append((t16 + 1.8, 99))
tse = w("s16", "Am") - .1
J.append(f'tl.set("#match", {{ opacity: 1 }}, {F(tse)}); tl.fromTo("#mmay", {{ opacity: 0 }}, {{ opacity: 1, duration: .1, immediateRender: false }}, {F(tse)}); tl.set("#bmz", {{ opacity: 0 }}, {F(tse)});')
cut(tse, 540, PODY - 120, 3.6); FX += [("boing", tse, .3, .3)]
# s17: halbe Stadt mini, Riesen-Katze, Jonas fährt Bus
t17 = s("s17")
cut(t17, 540, 1100, 1.15); cam(t17 + .05, 600, 1150, 1.3, 1.5, "none")
J.append(f'tl.fromTo("#cat", {{ y: 40 }}, {{ y: 0, duration: .5, ease: "back.out(2)", immediateRender: false }}, {F(t17 + .1)});')
for k in range(8): J.append(f'tl.to("#mn{k}", {{ x: {(-1) ** k * 20}, duration: .12, yoyo: true, repeat: 9 }}, {F(t17 + .1)});')
tbu = w("s17", "Jonas") - .1
cut(tbu, 540, 1000, 1.0); cam(tbu + .05, 540, 950, 1.2, 1.0); FX += [("whoosh", tbu, .35, .5)]
J.append(f'tl.to("#j4", {{ rotation: 4, transformOrigin: "50% 100%", duration: .25, yoyo: true, repeat: 7 }}, {F(tbu)});')
thm = w("s17", "Hamstern") - .1
cut(thm, 430, 1060, 1.5)
# s18: Niesen – Alter – wächst
t18 = s("s18")
J.append('tl.set("#bub18", { opacity: 0 }, 0);')
cut(t18, 540, 950, 1.6); expr("jo5", JONAS_EX[0] if False else ("determined" if "determined" in JONAS_EX else "happy"), "sneeze", w("s18", "niest") - .1)
pop("#bub18", w("s18", "Alter.") - .3, .2, "50% 50%"); FX += [("splat", w("s18", "niest"), .5, .4)]
tw18 = w("s18", "wächst") - .1
plopp("pf8", tw18); grow("#j4", tw18, .78, .86, .3, "back.out(3)"); settext("cm5-t", tw18, "9 CM", "8 CM"); FX += [("riser", tw18 - .3, .3, .6), ("chime", tw18, .5, 1.0)]
expr("jo5", "sneeze", "shock", tw18); cut(tw18, 620, 820, 1.5)
# s19: Die ganze Stadt brüllt ALTER – alle wachsen
t19 = s("s19")
cut(t19, 540, 1330, 1.2)
for k in range(7): J.append(f'tl.set("#bubm{k}", {{ opacity: 0 }}, 0);')
for j in range(3):
    tt = w("s19", "Alter!", j + 1) - .1
    for k in range(7):
        s0 = (.5, .35, .6, .4, .5, .25, .3)[k]
        grow(f"#cm_{k}", tt, s0 * (1 + .25 * j), s0 * (1 + .25 * (j + 1)), .25, "back.out(3)")
        if j == 0: pop(f"#bubm{k}", tt + k * .03, .2, "50% 50%")
    FX += [("boing", tt, .5, .4)]; shake(tt, 7, 14)
    if j: cut(tt, 540, 1330 - j * 60, 1.2 + j * .08)
# s20: Jonas größer als das Rathaus
t20 = s("s20")
cut(t20, 540, 1300, 1.3); cam(t20 + .05, 540, 900, 1.0, 1.6, "power2.inOut"); FX += [("riser", t20, .35, 1.5)]
tra = w("s20", "Rathaus.") - .3
pop("#b40", tra, .3, "50% 50%"); FX += [("hit", tra, .5, .8)]; shake(tra, 9, 16)
# s21: Zurück auf normal? 3.850 Digga
t21 = s("s21")
cut(t21, 780, 700, 1.6); expr("jo6", "laugh", "confused", t21 + .1)
t38 = w("s21", "dreitausendachthundertfünfzig") - .1
cut(t38, 330, 600, 1.2); pop("#b3850", t38, .3, "50% 50%"); FX += [("pop", t38, .5, .3)]
# s22: Welches Wort soll verboten sein? Schild bleibt bis zum Ende
t22 = s("s22")
cut(t22, 540, 1100, 1.0)
J.append('tl.set("#bub23", { opacity: 0 }, 0);')
J.append(f'tl.to("#blank", {{ opacity: .2, duration: .3, yoyo: true, repeat: 40, ease: "steps(1)" }}, {F(t22 + .3)});')
tsk = w("s22", "Schreib") - .1
cut(t22 + 1.6, 365, 900, 1.35) if t22 + 1.6 < tsk - .5 else None
cut(tsk, 540, 1000, 1.0); cam(tsk + .05, 430, 1000, 1.2, 1.2)
t23 = s("s23")
cut(t23, 700, 900, 1.15)
tdn = w("s23", "Denn") - .1
cam(tdn, 760, 700, 1.3, .6)
tdl = w("s23", "Digga.") - .1
pop("#bub23", tdl, .2, "50% 50%"); plopp("pf9", tdl + .3); FX += [("pop", tdl + .3, .8, .3)]
J.append(f'tl.set("#jo7-confused", {{ opacity: 0 }}, {F(tdl)}); tl.set("#jo7-laugh", {{ opacity: 1 }}, {F(tdl)});')
pop("#c3850", tdl + .3, .3, "50% 50%"); DZ.append((tdl + .3, 100))
cam(tdl, 620, 950, 1.0, .5)
tEND = round(END - 1.5, 2)

sets = [("A", 0, t3), ("B", t3, t5), ("D", t5, t6), ("E", t6, t7), ("F", t7, t9), ("G", t9, t10), ("PT", t10, td10), ("G", td10, t11), ("H", t11, t14),
        ("I", t14, t15), ("R2", t15, ter), ("I", ter, t17), ("K1", t17, tbu), ("K2", tbu, t19), ("M", t19, t20), ("N", t20, t22), ("O", t22, END)]

# Digga-Zähler oben links
dz_html = (f'<div id="dz" class="ui" style="left:24px;top:36px;background:#111;border:5px solid #ffd166;border-radius:16px;padding:6px 16px;font:900 38px Inter,sans-serif;color:#fff">'
           f'DIGGA-ZÄHLER: <span id="dzv" style="color:#ffd166">0</span></div>')
prev = "0"
for tt, v in DZ:
    settext("dzv", tt, str(v), prev); prev = str(v)
    J.append(f'tl.fromTo("#dz", {{ scale: 1.25, transformOrigin: "0% 0%" }}, {{ scale: 1, duration: .25, ease: "back.out(3)", immediateRender: false }}, {F(tt)});')
tag = f'<div class="ui clip" data-start="0" data-duration="{F(END)}" style="right:24px;top:40px;font:900 34px Inter,sans-serif;color:#fff;background:rgba(0,0,0,.55);padding:6px 14px;border-radius:12px">DIGGA-STADT #1</div>'
OBEN = [(0, "<span style='color:#ff4d5a'>-1 CM</span> PRO DIGGA"), (t2, "9 CM 🐹"), (t3, "XXL-WOHNUNG"), (tp4, "<span style='color:#ff4d5a'>-1 CM</span>"), (t5, "0x DIGGA 🧐"),
        (t6, "08:00"), (t7, "09:15 · UNTERRICHT"), (td7, "<span style='color:#ff4d5a'>-1 CM</span>"), (t8, "3x"), (t9, "XXS"), (t10, "WOLLE: 89,99 €"), (td10, "OMA: XXS"), (t11, "RAP-BATTLE"),
        (t12 + .3, "37x DIGGA"), (t13, "LECKER?"), (t14, "🔴 LIVE"), (td15, "<span style='color:#ff4d5a'>-1 CM</span>"), (t16, "BÜRGERMEISTER: 12 CM"), (t17, "CHAOS"),
        (t18, "<span style='color:#2dc653'>+1 CM ?!</span>"), (t19, "<span style='color:#2dc653'>+1 +1 +1</span>"), (t20, "JONAS: 40 M"), (t21, "ZURÜCK AUF NORMAL?"),
        (t22, "DEIN VERBOTENES WORT? 👇")]
HOT = {"DIGGA", "1", "JONAS", "HAMSTER", "ALTER", "PLOPP", "AMEISEN", "TAUBE", "RATHAUS", "VERBOTEN", "KOMMENTARE", "WORT"}
finish(S, sets, OBEN, FX, HOT, tag, extra_ui=dz_html, banner=("TEIL 2?", "➕ FOLGEN"), oben_top=130, banner_top=250)
