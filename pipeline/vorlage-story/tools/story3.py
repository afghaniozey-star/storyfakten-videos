"""STORY-FORMAT „In dieser Welt …“ – Die Zahl über dem Kopf, TEIL 3: „Fehler im System“ (Theo, Update Sonntag 12 Uhr).
Aufruf: python3 tools/story3.py  (liest voice.json + assets/vo/timing.json; Bausteine aus tools/bausteine.py;
Musik = fester Hintergrund-Sound assets/bgm.mp3 über tools/story_musik.py)"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bausteine import *
import math

# ---------- zusätzliche Mimik / Haare / Zubehör ----------
FACES["full"] = ('<path d="M-44 -6 Q-30 -18 -16 -6 M16 -6 Q30 -18 44 -6" stroke="#111" stroke-width="7" fill="none" stroke-linecap="round"/>'
                 '<rect x="-92" y="6" width="58" height="58" rx="26" fill="#f4a3a3" stroke="#111" stroke-width="4"/><rect x="34" y="6" width="58" height="58" rx="26" fill="#f4a3a3" stroke="#111" stroke-width="4"/>'
                 '<path d="M-14 40 Q0 50 14 40" stroke="#111" stroke-width="6" fill="none" stroke-linecap="round"/><rect x="-6" y="52" width="16" height="12" rx="4" fill="#e9a23b"/>')
FACES["facepalm"] = ('<path d="M-24 44 Q-12 36 0 44 Q12 52 24 44" stroke="#111" stroke-width="6" fill="none" stroke-linecap="round"/>'
                     '<rect x="-84" y="-44" width="128" height="62" rx="18" fill="#f2c9a5" stroke="#111" stroke-width="5"/><path d="M-50 -44 V-8 M-18 -44 V-8 M14 -44 V-8" stroke="#111" stroke-width="3"/>')
FACES["worried"] = (E(-30, 0, 10) + E(30, 0, 10) + '<path d="M-48 -26 L-14 -36 M48 -26 L14 -36" stroke="#111" stroke-width="7" stroke-linecap="round"/>'
                    '<path d="M-22 44 Q0 30 22 44" stroke="#111" stroke-width="7" fill="none" stroke-linecap="round"/>')
FACES["joy"] = ('<path d="M-46 -2 Q-30 -20 -14 -2 M14 -2 Q30 -20 46 -2" stroke="#111" stroke-width="8" fill="none" stroke-linecap="round"/>'
                '<path d="M-40 18 Q0 86 40 18 Z" fill="#5a1a1a" stroke="#111" stroke-width="5"/><path d="M-32 22 H32" stroke="#fff" stroke-width="8"/>')
HAIR["theo"] = lambda c: (f'<path d="M-100 -30 L-104 -110 L-70 -96 L-60 -140 L-26 -104 L-6 -150 L20 -106 L52 -146 L62 -100 L104 -118 L100 -30 L80 -70 H-80 Z" fill="{c}" stroke="#111" stroke-width="4"/>'
                          '<path d="M20 -106 L52 -146 L62 -100 Z" fill="#00f5d4" stroke="#111" stroke-width="3"/>')
HOOD = ('<g id="{u}-hood"><path d="M-138 120 Q-150 -168 0 -172 Q150 -168 138 120 L104 110 Q106 -108 0 -112 Q-106 -108 -104 110 Z" fill="#141418" stroke="#000" stroke-width="5"/>'
        '<rect x="-96" y="-96" width="192" height="192" rx="26" fill="#000" opacity=".5"/></g>')
def bag(u, x, y, r=0, L=300):  # Baguette: rechtes Ende in der Hand (x, y), ragt um L nach links
    return (f'<g id="{u}-bag" transform="translate({x} {y}) rotate({r})"><rect x="{-L}" y="-24" width="{L + 20}" height="48" rx="24" fill="#e9a23b" stroke="#111" stroke-width="5"/>'
            + "".join(f'<path d="M{-L + 40 + k * 60} -14 l22 28" stroke="#b5651d" stroke-width="7" stroke-linecap="round"/>' for k in range(max(1, (L - 40) // 60))) + '</g>')
BACKPACK = '<rect x="-120" y="-310" width="240" height="230" rx="30" fill="#2a9d8f" stroke="#111" stroke-width="6"/><rect x="-80" y="-200" width="160" height="90" rx="18" fill="#21867a" stroke="#111" stroke-width="5"/>'
def empty(uid, y=-580, vis=True, col="#fff"):
    return (f'<g id="{uid}" opacity="{1 if vis else 0}"><rect x="-95" y="{y - 72}" width="190" height="100" rx="26" fill="#000" fill-opacity=".25" stroke="{col}" stroke-width="8" stroke-dasharray="20 14"/>'
            f'<text x="0" y="{y + 8}" text-anchor="middle" style="font:900 72px {FONT};fill:{col}">?</text></g>')

MIA_EX = ("happy", "shock", "panic", "determined", "annoyed", "sad", "hope", "tired", "confused", "relief", "laugh", "facepalm", "joy", "worried")
def mia(uid, start="happy", acc="", arm=("down", "down"), arm2=None, outfit="normal", extra="", behind=""):
    if outfit == "chicken":
        return person(uid, "chicken", "#6b3e26", "#ffd60a", exprs=MIA_EX, start=start, head_acc=acc, arm=arm, arm2=arm2, pants="#fb8500", extra=extra, behind=behind)
    return person(uid, "mia", "#6b3e26", "#ef476f", exprs=MIA_EX, start=start, head_acc=acc, arm=arm, arm2=arm2, extra=extra, behind=behind)
THEO_EX = ("grin", "grinwink", "neutral", "determined", "worried", "happy", "shock")
def theo(uid, start="grin", hood=False, arm=("down", "down"), arm2=None, extra=""):
    return person(uid, "theo", "#1a1a1a", "#1b1b1f", skin="#e0ac69", exprs=THEO_EX, start=start, arm=arm, arm2=arm2, extra=extra,
                  head_acc=HOOD.format(u=uid) if hood else "", pants="#3a3a44")
BEN_EX = ("happy", "full", "laugh", "determined", "hope")
def ben(uid, start="happy", arm=("down", "down"), arm2=None, extra=""):
    return person(uid, "ben", "#ff9f1c", "#fb8500", skin="#e0ac69", exprs=BEN_EX, start=start, arm=arm, arm2=arm2, extra=extra)
OMA_EX = ("relief", "wink", "laugh", "happy")
OMA_ACC = '<rect x="-64" y="-20" width="46" height="34" rx="16" fill="none" stroke="#555" stroke-width="5"/><rect x="18" y="-20" width="46" height="34" rx="16" fill="none" stroke="#555" stroke-width="5"/>'
def oma(uid, start="relief", arm=("down", "down"), arm2=None, extra=""):
    return person(uid, "oma", "#e0e0e0", "#9d4edd", exprs=OMA_EX, start=start, arm=arm, arm2=arm2, extra=extra, head_acc=OMA_ACC)
KR_ACC = '<rect x="-62" y="-22" width="48" height="36" rx="8" fill="none" stroke="#111" stroke-width="6"/><rect x="14" y="-22" width="48" height="36" rx="8" fill="none" stroke="#111" stroke-width="6"/><path d="M-14 -6 H14" stroke="#111" stroke-width="6"/>'
def krause(uid, start="neutral", arm=("down", "down")):
    return person(uid, "glatze", "#555", "#6c757d", exprs=("neutral", "confused", "shock", "determined"), start=start, arm=arm, head_acc=KR_ACC)
LENA_EX = ("happy", "laugh", "neutral", "shock")
lena = lambda uid, start="happy": person(uid, "lena", "#f4d35e", "#06d6a0", exprs=LENA_EX, start=start)
GREENB = GREEN

def night_lamp():
    return ('<rect x="980" y="300" width="22" height="1000" fill="#333"/><rect x="900" y="290" width="120" height="40" rx="12" fill="#444"/>'
            '<rect x="900" y="330" width="80" height="40" rx="10" fill="#ffe8a3"/><path d="M940 360 L380 1900 H1080 V560 Z" fill="url(#cone)"/>')
def sepia(content, label):
    return (content + '<rect width="1080" height="1920" fill="#c9a26b" opacity=".38"/>'
            '<rect x="24" y="24" width="1032" height="1872" rx="30" fill="none" stroke="#fff" stroke-width="18" stroke-dasharray="40 24"/>'
            f'<text x="540" y="1840" text-anchor="middle" style="font:900 54px {FONT};fill:#fff;opacity:.9">{label}</text>')
def confetti(uid, y0=500, n=40):
    return (f'<g id="{uid}" opacity="0">' + "".join(f'<rect x="{(k * 97) % 1080}" y="{y0 + (k * 53) % 300}" width="24" height="36" fill="{("#ffd166", "#ef476f", "#06d6a0", "#118ab2")[k % 4]}" transform="rotate({k * 37} {(k * 97) % 1080} {y0 + (k * 53) % 300})"/>' for k in range(n)) + '</g>')

S = {}; FX = []
# --- N: Nacht, Laterne – Cliffhanger-Bild aus Teil 2 (Mia im Hühnerkostüm + Fremder, über beiden NICHTS)
NMX, NTX, NS = 300, 790, 1.6
S["N"] = (street_bg(night=True) + night_lamp() +
          fig(mia("m1", "confused", outfit="chicken") + empty("eM1", y=-650), NMX, 1900, NS) +
          fig(theo("t1", "grin", hood=True) + empty("eT1") +
              '<g id="err" opacity="0"><rect x="-160" y="-690" width="320" height="110" rx="18" fill="#111" stroke="#ff3b30" stroke-width="8"/>'
              f'<text id="errt" x="0" y="-612" text-anchor="middle" style="font:900 62px Inter,monospace;fill:#ff3b30">ERROR 404</text>'
              + "".join(f'<rect x="{-150 + (k * 71) % 280}" y="{-680 + (k * 41) % 95}" width="{30 + (k * 23) % 50}" height="12" fill="{("#00f5d4", "#f15bb5", "#fee440")[k % 3]}" opacity=".9"/>' for k in range(8)) + '</g>',
              NTX, 1900, NS))
# --- R: Rückblick-Montage (4 Bilder)
S["R"] = ('<g id="r1">' + sepia(street_bg() + fig(lena("l0", "shock") + badge("bL0", "1", col=RED, fg="#fff", size=110, vis=True), 540, 1900, 1.8), "TEIL 1: LENA HAT DIE 1") + '</g>'
          '<g id="r2" opacity="0">' + sepia(room_bg("#ffd6a5", "#a47148", win=False) + fig(mia("m2", "annoyed", acc=BEANIE.format(u="m2") + POT.format(u="m2")) + badge("bM2", "1", col=RED, fg="#fff", size=100, y=-820, vis=True), 540, 1900, 1.75), "JETZT HAT MIA DIE 1") + '</g>'
          '<g id="r3" opacity="0">' + sepia('<rect width="1080" height="1920" fill="#8ecae6"/><rect x="0" y="380" width="1080" height="900" fill="#f4a261" stroke="#111" stroke-width="6"/>'
                                            f'<rect x="80" y="420" width="920" height="150" rx="20" fill="#fff" stroke="#111" stroke-width="6"/><text x="540" y="530" text-anchor="middle" style="font:900 100px {FONT};fill:#9c4f1f">BÄCKEREI</text>'
                                            '<rect x="0" y="1280" width="1080" height="640" fill="#adb5bd"/>' + fig(mia("m3", "laugh", arm=("out", "out"), outfit="chicken") + badge("bM3", "1", col=RED, fg="#fff", size=100, y=-660, vis=True), 540, 1900, 1.75), "100 LACHER SAMMELN") + '</g>'
          '<g id="r4" opacity="0">' + sepia(street_bg(night=True) + fig(mia("m4", "joy", outfit="chicken", arm=("up", "up")), 540, 1900, 1.75) +
                                            f'<g transform="translate(540 760)"><rect x="-330" y="-110" width="660" height="200" rx="34" fill="{GREEN}" stroke="#111" stroke-width="9"/><text x="0" y="40" text-anchor="middle" style="font:900 130px {FONT};fill:#fff">😂 100/100</text></g>', "GESCHAFFT!") + '</g>')
# --- Z: A/B-Split aus Teil 2
halo = '<ellipse cx="0" cy="-570" rx="120" ry="34" fill="none" stroke="#ffd166" stroke-width="22"/>'
glitch = ('<g id="glt">' + "".join(f'<rect x="{-150 + (k * 71) % 300}" y="{-700 + (k * 113) % 650}" width="{40 + (k * 31) % 90}" height="22" fill="{("#00f5d4", "#f15bb5", "#fee440")[k % 3]}" opacity=".85"/>' for k in range(14)) + '</g>')
S["Z"] = ('<rect width="540" height="1920" fill="#fff3b0"/><rect x="540" width="540" height="1920" fill="#1a1a2e"/>'
          + "".join(f'<path d="M{270 + 400 * math.cos(k * .52):.0f} {1000 + 400 * math.sin(k * .52):.0f} L270 1000" stroke="#ffd166" stroke-width="12" opacity=".4"/>' for k in range(12)) +
          f'<g id="zA">{fig(mia("m10", "relief") + halo, 270, 1950, 1.6)}</g>'
          f'<g id="zB">{fig(mia("m11", "confused") + glitch, 810, 1950, 1.6)}</g>'
          '<rect x="530" width="20" height="1920" fill="#111"/>'
          f'<g id="labA"><rect x="70" y="650" width="400" height="230" rx="30" fill="#ffd166" stroke="#111" stroke-width="7"/><text x="270" y="770" text-anchor="middle" style="font:900 120px {FONT};fill:#111">A</text><text x="270" y="850" text-anchor="middle" style="font:900 44px {FONT};fill:#111">UNSTERBLICH</text></g>'
          f'<g id="labB"><rect x="610" y="650" width="400" height="230" rx="30" fill="#f15bb5" stroke="#111" stroke-width="7"/><text x="810" y="770" text-anchor="middle" style="font:900 120px {FONT};fill:#fff">B</text><text x="810" y="850" text-anchor="middle" style="font:900 40px {FONT};fill:#fff">FEHLER IM SYSTEM</text></g>'
          '<g id="xA" opacity="0"><path d="M90 670 L450 860 M450 670 L90 860" stroke="#e63946" stroke-width="30" stroke-linecap="round"/></g>'
          f'<g id="okB" opacity="0"><rect x="600" y="640" width="420" height="250" rx="36" fill="none" stroke="{GREEN}" stroke-width="16"/><text x="980" y="660" text-anchor="middle" style="font:900 110px {FONT};fill:{GREEN};stroke:#111;stroke-width:5px;paint-order:stroke">✔</text></g>')
# --- U: Countdown am Himmel
S["U"] = (street_bg(night=True) +
          '<g id="cdg"><rect x="90" y="250" width="900" height="380" rx="40" fill="#000" stroke="#00f5d4" stroke-width="10"/>'
          f'<text x="540" y="350" text-anchor="middle" style="font:900 62px {FONT};fill:#00f5d4">UPDATE IN</text>'
          '<text id="cdt" x="540" y="540" text-anchor="middle" style="font:900 150px Inter,monospace;fill:#fff">4T 11:59</text></g>'
          '<path d="M540 630 V720" stroke="#00f5d4" stroke-width="8" stroke-dasharray="16 12"/>' +
          fig(mia("m12", "shock", outfit="chicken") + empty("eM12", y=-650), 330, 1900, 1.55) + fig(theo("t12", "neutral", hood=True), 760, 1900, 1.55))
# --- P: Tag, Straße mit Zaun: Passant, Mia, Oma Hilde (Pfeil: Zahl wird geklaut)
FORK = '<g transform="translate(150 -480) rotate(18)"><rect x="-8" y="-10" width="16" height="120" rx="6" fill="#adb5bd" stroke="#111" stroke-width="3"/><path d="M-22 -60 V-10 H22 V-60 M0 -60 V-10" stroke="#adb5bd" stroke-width="9" fill="none"/><rect x="-40" y="-110" width="80" height="44" rx="10" fill="#f4acb7" stroke="#111" stroke-width="4"/></g>'
PMX, POX = 470, 840
S["P"] = (street_bg(fence=True) + fig(person("ps", "mann", "#3d2b1f", "#3a86ff", exprs=("neutral", "shock"), start="neutral") + badge("bPs", "12.400", size=66, vis=True), 170, 1480, .95) +
          fig(oma("om1", "relief", arm=("down", "up"), extra=FORK) + badge("bO1", "900", size=76, y=-600, vis=True), POX, 1900, 1.5) +
          fig(mia("m13", "happy") + empty("eM13"), PMX, 1900, 1.5) +
          f'<g id="arw" opacity="0"><path id="arwp" d="M230 1000 Q380 760 {PMX - 40} {1900 - 600 * 1.5 + 10}" stroke="#ff3b30" stroke-width="22" fill="none" stroke-linecap="round" stroke-dasharray="30 18"/>'
          f'<path d="M{PMX - 90} {1900 - 600 * 1.5 - 10} L{PMX - 40} {1900 - 600 * 1.5 + 14} L{PMX - 96} {1900 - 600 * 1.5 + 50}" stroke="#ff3b30" stroke-width="22" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>')
# --- K: Mias Zimmer, Plan mit Rucksack + Karte
MAP = (f'<g id="map"><rect x="-260" y="-200" width="520" height="380" rx="16" fill="#fefae0" stroke="#111" stroke-width="7"/>'
       '<path d="M-200 120 L-90 -110 L0 30 L60 -60 L170 120 Z" fill="#95d5b2" stroke="#2d6a4f" stroke-width="6"/><path d="M-110 -70 L-90 -110 L-70 -70 Z" fill="#fff"/>'
       '<path d="M-220 150 Q-60 60 30 140 T240 100" stroke="#e76f51" stroke-width="8" fill="none" stroke-dasharray="18 12"/>'
       f'<path id="mapx" d="M-115 -150 L-65 -100 M-65 -150 L-115 -100" stroke="#e63946" stroke-width="14" stroke-linecap="round"/><text x="-10" y="-150" style="font:900 40px {FONT};fill:#111">ALLEIN!</text></g>')
S["K"] = (room_bg("#cfe8ff", "#8d99ae", win=True) + '<rect x="70" y="330" width="360" height="300" fill="#f1faee" stroke="#6b4226" stroke-width="10"/>'
          f'<text x="250" y="420" text-anchor="middle" style="font:900 48px {FONT};fill:#111">SONNTAG</text><text x="250" y="500" text-anchor="middle" style="font:900 48px {FONT};fill:#e63946">12:00</text><text x="250" y="580" text-anchor="middle" style="font:900 60px {FONT}">⚠</text>' +
          fig(mia("m14", "determined", arm=("front", "front"), behind=BACKPACK, extra=f'<g transform="translate(0 -170) scale(.7)">{MAP}</g>') + empty("eM14"), 540, 1900, 1.7))
# --- C: Klassenzimmer, Ben + Baguette
S["C"] = (room_bg("#e9f5db", "#b08968", win=False) +
          '<rect x="90" y="270" width="900" height="420" rx="16" fill="#2d6a4f" stroke="#6b4226" stroke-width="18"/>'
          f'<text x="540" y="440" text-anchor="middle" style="font:900 92px Comic Sans MS,{FONT};fill:#fff;opacity:.9">MONTAG</text><text x="540" y="580" text-anchor="middle" style="font:700 60px {FONT};fill:#fff;opacity:.8">Bio: Geister? 👻</text>' +
          fig(mia("m15", "annoyed") + empty("eM15"), 230, 1900, 1.6) +
          fig(ben("bn1", "hope", arm=("front", "down"), extra=bag("bn1", -196, -330, 0, 180)) + badge("bB1", "20.100", size=62, y=-600, vis=True), 900, 1900, 1.6))
# --- L: Laptop über die Schulter + Lehrer
S["L"] = (room_bg("#e9f5db", "#b08968", win=False) + '<rect x="90" y="270" width="900" height="420" rx="16" fill="#2d6a4f" stroke="#6b4226" stroke-width="18"/>'
          + fig(krause("kr1", "neutral", arm=("front", "front")) + badge("bK1", "15.200", size=60, vis=True), 760, 1600, 1.15) +
          '<rect x="120" y="1240" width="860" height="70" rx="10" fill="#6b4226" stroke="#111" stroke-width="5"/>'
          '<g id="lap"><rect x="200" y="760" width="680" height="460" rx="24" fill="#343a40" stroke="#111" stroke-width="8"/><rect x="230" y="790" width="620" height="390" rx="10" fill="#f8f9fa"/>'
          f'<text x="540" y="860" text-anchor="middle" style="font:700 44px {FONT};fill:#495057">SCHÜLER-SUCHE</text><rect x="280" y="890" width="520" height="70" rx="12" fill="#fff" stroke="#adb5bd" stroke-width="4"/><text x="300" y="940" style="font:700 46px {FONT};fill:#111">Mia</text>'
          f'<g id="l404" opacity="0"><text x="540" y="1100" text-anchor="middle" style="font:900 120px {FONT};fill:#e63946">MIA? 404</text></g>'
          '<rect x="150" y="1220" width="780" height="40" rx="14" fill="#495057" stroke="#111" stroke-width="6"/></g>'
          '<g transform="translate(130 1980) scale(1.6)"><rect x="-96" y="-300" width="192" height="240" rx="22" fill="#6c757d" stroke="#111" stroke-width="5"/><rect x="-96" y="-496" width="192" height="192" rx="26" fill="#f2c9a5" stroke="#111" stroke-width="5"/><path d="M-96 -420 H-80 V-360 H-96 Z M96 -420 H80 V-360 H96 Z" fill="#555"/></g>')
# --- B: Klassenbuch
S["B"] = ('<rect width="1080" height="1920" fill="#b08968"/>' + "".join(f'<rect x="0" y="{k * 160}" width="1080" height="6" fill="#000" opacity=".08"/>' for k in range(12)) +
          '<g transform="rotate(-4 540 1000)"><rect x="80" y="380" width="920" height="1200" rx="20" fill="#1d3557" stroke="#111" stroke-width="8"/><rect x="110" y="400" width="860" height="1160" rx="10" fill="#fdfcf7" stroke="#111" stroke-width="5"/>'
          f'<text x="540" y="500" text-anchor="middle" style="font:900 64px {FONT};fill:#1d3557">KLASSENBUCH 8B</text>' +
          "".join(f'<text x="180" y="{640 + k * 130}" style="font:700 64px Comic Sans MS,{FONT};fill:#222">{n}</text><text x="860" y="{640 + k * 130}" style="font:900 64px {FONT};fill:{GREEN}">✔</text>'
                  for k, n in enumerate(("Anna", "Ben", "", "Lena", "Tim", "Zoe"))) +
          f'<g id="qm" opacity="0"><text x="180" y="900" style="font:900 120px {FONT};fill:#e63946">?</text><text x="300" y="900" style="font:700 52px Comic Sans MS,{FONT};fill:#e63946">(Mia??)</text></g>'
          '<path d="M140 520 H940" stroke="#e63946" stroke-width="4"/></g>')
S["B2"] = (room_bg("#e9f5db", "#b08968", win=False) + '<rect x="90" y="270" width="900" height="420" rx="16" fill="#2d6a4f" stroke="#6b4226" stroke-width="18"/>'
           f'<text x="540" y="480" text-anchor="middle" style="font:900 200px {FONT};fill:#fff;opacity:.85">?</text>' +
           fig(mia("m16", "annoyed") + f'<g transform="translate(0 -560)"><rect x="-90" y="-72" width="180" height="100" rx="26" fill="#fff" stroke="#111" stroke-width="7"/><text x="0" y="8" text-anchor="middle" style="font:900 72px {FONT};fill:#e63946">?</text></g>', 540, 1900, 1.85))
# --- M: Berg (Totale), Mia winzig
S["M"] = ('<rect width="1080" height="1920" fill="#a2d2ff"/><rect x="760" y="200" width="150" height="150" rx="30" fill="#ffd166" stroke="#111" stroke-width="5"/>'
          '<path d="M-200 1920 L540 420 L1300 1920 Z" fill="#6c757d" stroke="#111" stroke-width="8"/><path d="M400 704 L540 420 L680 704 L620 660 L560 720 L500 650 L450 720 Z" fill="#fff" stroke="#111" stroke-width="6"/>'
          '<path d="M-200 1920 L200 1300 L600 1920 Z" fill="#52796f" stroke="#111" stroke-width="6"/><path d="M500 1920 L950 1200 L1400 1920 Z" fill="#354f52" stroke="#111" stroke-width="6"/>'
          '<path d="M300 1700 Q500 1500 420 1300 T560 900 T540 520" stroke="#e9c46a" stroke-width="12" fill="none" stroke-dasharray="26 18"/>'
          f'<g id="mclimb">{fig(mia("m17", "determined", behind=BACKPACK), 470, 1340, .45)}</g>'
          '<g transform="translate(540 420)"><rect x="-4" y="-120" width="8" height="120" fill="#333"/><path d="M4 -120 L80 -96 L4 -72 Z" fill="#e63946"/></g>' +
          fig(ben("bn0", "happy"), 600, 470, .22))
# --- S: Gipfel (Ben sitzt schon oben)
S["S"] = ('<rect width="1080" height="1920" fill="#a2d2ff"/>' + "".join(f'<rect x="{x}" y="{y}" width="{wd}" height="70" rx="35" fill="#fff" opacity=".9"/>' for x, y, wd in ((90, 260, 260), (640, 420, 300), (300, 560, 200))) +
          '<path d="M-100 1920 L540 1150 L1180 1920 Z" fill="#6c757d" stroke="#111" stroke-width="8"/><path d="M380 1340 L540 1150 L700 1340 L640 1300 L560 1360 L490 1290 L440 1360 Z" fill="#fff" stroke="#111" stroke-width="6"/>'
          '<g transform="translate(540 1150)"><rect x="-6" y="-260" width="12" height="260" fill="#333"/><path d="M6 -260 L130 -220 L6 -180 Z" fill="#e63946"/></g>' +
          fig(mia("m18", "shock", behind=BACKPACK) + empty("eM18"), 280, 1900, 1.6) +
          fig(ben("bn2", "laugh", arm=("up", "down"), extra=bag("bn2", 160, -470, 110, 300)) + badge("bB2", "20.100", size=62, y=-600, vis=True), 800, 1900, 1.6) +
          bubble("bub14", ["ICH LASS DICH", "NICHT ALLEIN!"], 640, 640, 620, tail=(1, 1), size=56))
# --- W: Wald, Oma beim Pilzesammeln
BASKET = '<g transform="translate(-170 -150)"><path d="M-70 -40 Q0 -140 70 -40" stroke="#6b4226" stroke-width="12" fill="none"/><rect x="-80" y="-50" width="160" height="110" rx="20" fill="#bc6c25" stroke="#111" stroke-width="5"/>' + \
         "".join(f'<g transform="translate({dx} -50)"><rect x="-8" y="-6" width="16" height="30" fill="#fff" stroke="#111" stroke-width="3"/><path d="M-30 -4 Q0 -46 30 -4 Z" fill="#e63946" stroke="#111" stroke-width="4"/><circle cx="-8" cy="-18" r="5" fill="#fff"/></g>' for dx in (-45, 0, 45)) + '</g>'
tree = lambda x, s=1.0: (f'<g transform="translate({x} 1500) scale({s})"><rect x="-60" y="-700" width="120" height="720" fill="#7f5539" stroke="#111" stroke-width="6"/>'
                         '<rect x="-260" y="-1150" width="520" height="520" rx="120" fill="#2d6a4f" stroke="#111" stroke-width="7"/><rect x="-200" y="-1300" width="400" height="300" rx="100" fill="#40916c" stroke="#111" stroke-width="7"/></g>')
S["W"] = ('<rect width="1080" height="1920" fill="#d8f3dc"/>' + tree(120, .9) + tree(980, .85) + '<rect y="1500" width="1080" height="420" fill="#74c69d"/>' +
          f'<g id="omw">{fig(oma("om2", "wink", arm=("hip", "down"), extra=BASKET) + badge("bO2", "900", size=76, y=-600, vis=True), 760, 1900, 1.5)}</g>' +
          '<g transform="translate(560 1900)"><rect x="-90" y="-1000" width="180" height="1010" fill="#7f5539" stroke="#111" stroke-width="7"/></g>' +
          fig(mia("m19", "panic", behind=BACKPACK) + empty("eM19"), 280, 1900, 1.6))
# --- T: Schulklo von außen (zwei Türen) / T2: von innen, Theo reißt Tür auf
door = lambda x, lab, uid: (f'<g id="{uid}"><rect x="{x}" y="520" width="380" height="1180" rx="14" fill="#4cc9f0" stroke="#111" stroke-width="8"/>'
                            f'<rect x="{x + 300}" y="1080" width="40" height="80" rx="10" fill="#adb5bd" stroke="#111" stroke-width="4"/><rect x="{x + 140}" y="620" width="100" height="56" rx="10" fill="#e63946" stroke="#111" stroke-width="4"/>'
                            f'<text x="{x + 190}" y="662" text-anchor="middle" style="font:900 34px {FONT};fill:#fff">{lab}</text></g>')
S["T"] = ('<rect width="1080" height="1920" fill="#e9ecef"/>' + "".join(f'<rect x="{(k % 9) * 120}" y="{(k // 9) * 120}" width="118" height="118" fill="none" stroke="#ced4da" stroke-width="3"/>' for k in range(9 * 17)) +
          door(70, "BESETZT", "d1") + door(630, "BESETZT", "d2") + '<rect y="1700" width="1080" height="220" fill="#adb5bd"/>' +
          '<g transform="translate(260 1790)"><rect x="-80" y="-20" width="70" height="40" rx="12" fill="#ef476f" stroke="#111" stroke-width="4"/><rect x="10" y="-20" width="70" height="40" rx="12" fill="#ef476f" stroke="#111" stroke-width="4"/></g>' +
          '<g transform="translate(820 1790)"><rect x="-80" y="-20" width="70" height="40" rx="12" fill="#2b2d42" stroke="#111" stroke-width="4"/><rect x="10" y="-20" width="70" height="40" rx="12" fill="#2b2d42" stroke="#111" stroke-width="4"/></g>' +
          bubble("bub16", ["BESETZT!"], 760, 600, 520, tail=(0, 1), size=86))
TOILET = '<g transform="translate(330 1900)"><rect x="-150" y="-330" width="300" height="200" rx="30" fill="#fff" stroke="#111" stroke-width="7"/><rect x="-170" y="-150" width="340" height="80" rx="30" fill="#f8f9fa" stroke="#111" stroke-width="7"/><rect x="-110" y="-80" width="220" height="80" fill="#fff" stroke="#111" stroke-width="7"/></g>'
S["T2"] = ('<rect width="1080" height="1920" fill="#dee2e6"/>' + "".join(f'<rect x="{(k % 9) * 120}" y="{(k // 9) * 120}" width="118" height="118" fill="none" stroke="#ced4da" stroke-width="3"/>' for k in range(9 * 17)) +
           '<rect x="600" y="300" width="480" height="1500" fill="#495057"/>' +
           fig(theo("t2", "determined", arm=("down", "out")) + empty("eT2"), 860, 1900, 1.6) +
           '<g id="d3"><rect x="590" y="300" width="490" height="1500" fill="#4cc9f0" stroke="#111" stroke-width="10"/><rect x="640" y="1000" width="40" height="90" rx="10" fill="#adb5bd" stroke="#111" stroke-width="4"/></g>' +
           TOILET + fig(mia("m20", "panic", behind=BACKPACK) + empty("eM20"), 330, 1780, 1.45) + '<rect y="1800" width="1080" height="120" fill="#adb5bd"/>' +
           bubble("bub17", ["ZU MIR!"], 780, 560, 400, tail=(.5, 1), size=86))
# --- Y: leerer Schulhof (Rücken an Rücken, Update, 30.000, die 1)
YMX, YTX, YS = 380, 720, 1.6
S["Y"] = ('<rect width="1080" height="1920" fill="#ffb4a2"/><rect y="0" width="1080" height="900" fill="#e5989b" opacity=".5"/>'
          '<rect x="0" y="560" width="1080" height="560" fill="#b5838d" stroke="#111" stroke-width="6"/>' + "".join(f'<rect x="{60 + k * 200}" y="640" width="120" height="110" fill="#fff8d6" stroke="#111" stroke-width="5"/>' for k in range(5)) +
          f'<rect x="420" y="430" width="240" height="140" rx="16" fill="#111" stroke="#fff" stroke-width="6"/><text id="yclk" x="540" y="530" text-anchor="middle" style="font:900 84px Inter,monospace;fill:#ff3b30">11:59</text>'
          '<rect y="1120" width="1080" height="800" fill="#adb5bd"/><path d="M0 1500 H1080" stroke="#fff" stroke-width="10" stroke-dasharray="60 40"/>' +
          f'<g id="ym">{fig(mia("m21", "worried", behind=BACKPACK) + badge("bM21", "00.000", size=70, y=-600) + empty("eM21", y=-600), YMX, 1900, YS)}</g>' +
          f'<g id="yt">{fig("<g transform=\"scale(-1 1)\">" + theo("t3", "neutral") + "</g>" + badge("bT3", "1", col=RED, fg="#fff", size=100, y=-600) + empty("eT3", y=-600), YTX, 1900, YS)}</g>' +
          confetti("conf20"))
# --- AB: Kommentar-Frage (A: Mia rettet Theo / B: Theo plant was)
PLAN = '<g transform="translate(-170 -230) rotate(-15)"><rect x="-70" y="-90" width="140" height="180" rx="10" fill="#fefae0" stroke="#111" stroke-width="5"/><text x="0" y="-30" text-anchor="middle" style="font:900 40px Inter,sans-serif;fill:#e63946">PLAN</text><path d="M-46 0 H46 M-46 30 H30 M-46 60 H40" stroke="#111" stroke-width="6"/></g>'
S["AB"] = ('<rect width="540" height="1920" fill="#caffbf"/><rect x="540" width="540" height="1920" fill="#2b2d42"/>' +
           "".join(f'<path d="M{270 + 420 * math.cos(k * .52):.0f} {1100 + 420 * math.sin(k * .52):.0f} L270 1100" stroke="#fff" stroke-width="12" opacity=".5"/>' for k in range(12)) +
           '<svg x="0" y="0" width="540" height="1920" overflow="hidden">' +
           fig(mia("m22", "determined", arm=("down", "hip")) + empty("eM22", y=-600, col="#111"), 150, 1950, 1.45) +
           fig(theo("t4", "happy", arm=("hip", "down")) + badge("bT4", "1", col=RED, fg="#fff", size=90, y=-600, vis=True), 410, 1950, 1.45) +
           '</svg>'
           '<svg x="540" y="0" width="540" height="1920" overflow="hidden">' +
           fig(theo("t5", "grinwink", arm=("down", "hip"), extra=PLAN) + badge("bT5", "1", col=RED, fg="#fff", size=110, y=-600, vis=True) + empty("eT5", y=-600, vis=False), 300, 1950, 1.7) + '</svg>'
           '<rect x="530" width="20" height="1920" fill="#111"/>'
           f'<g id="labA2"><rect x="50" y="560" width="440" height="230" rx="30" fill="#ffd166" stroke="#111" stroke-width="7"/><text x="270" y="680" text-anchor="middle" style="font:900 120px {FONT};fill:#111">A</text><text x="270" y="760" text-anchor="middle" style="font:900 46px {FONT};fill:#111">JA, RETTEN!</text></g>'
           f'<g id="labB2"><rect x="590" y="560" width="440" height="230" rx="30" fill="#f15bb5" stroke="#111" stroke-width="7"/><text x="810" y="680" text-anchor="middle" style="font:900 120px {FONT};fill:#fff">B</text><text x="810" y="760" text-anchor="middle" style="font:900 40px {FONT};fill:#fff">THEO PLANT WAS!</text></g>')

# ---------- Zeitplan ----------
J.append('tl.set("#cam", { x: 0, y: 0, scale: 1, svgOrigin: "0 0" }, 0);')
s = st
# s1 (0,0): Zwei-Einstellung – über beiden leer, dann Mia nah, Reißschwenk zum Fremden
hmx = HEAD(NMX, 1900, NS); htx = HEAD(NTX, 1900, NS)
cut(0, 545, 1150, 1.12); cam(.05, 545, 1100, 1.22, 1.2, "power1.out")
J.append('tl.to("#eM1, #eT1", { opacity: .35, duration: .2, yoyo: true, repeat: 9, ease: "steps(1)" }, .2); tl.set("#eM1, #eT1", { opacity: 1 }, 2.4);')
FX += [("glitch", 0, .25, .3), ("hit", .02, .5, 1.0)]
t = w("s1", "Zahl") - .1
cut(t, hmx[0] + 30, hmx[1] - 200, 1.75); cam(t + .05, hmx[0] + 30, hmx[1] - 300, 1.85, 1.0)
t = w("s1", "Fremden") - .15
cut(t, htx[0] - 20, htx[1] - 200, 1.75); FX += [("swoosh", t - .05, .45, .5)]
J.append(f'tl.fromTo("#t1", {{ x: 60 }}, {{ x: 0, duration: .25, ease: "power3.out", immediateRender: false }}, {F(t)});')
t = w("s1", "Und") - .05
cut(t, 545, 1150, 1.15)
t = w("s1", "schlecht.") - .25
expr("t1", "grin", "worried", t); expr("m1", "confused", "shock", t + .1)
cam(t, htx[0] - 60, htx[1] - 150, 1.6, .5, "power3.out")
FX += [("hit", t, .45, .8)]
# s2: Rückblick-Montage (4 Bilder, ca. 0,7–1 s)
t2 = s("s2"); t3 = s("s3")
d2 = (t3 - t2) / 4
for k in range(4):
    a = t2 + k * d2
    if k: J.append(f'tl.set("#r{k}", {{ opacity: 0 }}, {F(a)}); tl.set("#r{k + 1}", {{ opacity: 1 }}, {F(a)});')
    cut(a, 540, 1050 - k * 40, 1.0 + .05 * (k % 2)); cam(a + .02, 540, 1000, 1.12 + .05 * (k % 2), d2, "none")
    FX += [("swoosh", a, .3, .4)]
# s3: A/B-Split -> A durchgestrichen -> Kapuze fällt -> B leuchtet
cut(t3, 540, 1000, 1.0); cam(t3 + .05, 270, 1000, 1.25, .6)
J.append(f'tl.to("#labA", {{ scale: 1.1, transformOrigin: "50% 50%", duration: .2, yoyo: true, repeat: 1 }}, {F(t3 + .1)});')
J.append(f'tl.to("#glt", {{ x: 12, duration: .06, yoyo: true, repeat: 30, ease: "steps(1)" }}, {F(t3)});')
tn = w("s3", "Nein.") - .1
pop("#xA", tn, .2, "50% 50%"); J.append(f'tl.to("#zA", {{ opacity: .35, duration: .2 }}, {F(tn)});'); FX += [("klong", tn, .3, .6)]
te = w("s3", "Er") - .1
cut(te, htx[0], htx[1] - 120, 1.85)
J.append(f'tl.set("#t1-worried", {{ opacity: 0 }}, {F(te)}); tl.set("#t1-grin", {{ opacity: 1 }}, {F(te)}); tl.set("#t1-hood", {{ opacity: 1 }}, 0);')
J.append(f'tl.set("#t1-worried", {{ opacity: 1 }}, {F(w("s1", "schlecht.") - .25)});')
tk = w("s3", "runter:") - .3
fly("#t1-hood", tk, {"y": 0, "opacity": 1}, {"y": -260, "opacity": 0, "rotation": -12}, .45, "power2.in"); FX += [("whoosh", tk, .4, .6)]
tb = w("s3", "Antwort") - .1
cut(tb, 810, 1000, 1.0); cam(tb + .02, 810, 820, 1.3, .5)
pop("#okB", tb + .05, .3, "50% 50%"); FX += [("chime", tb, .45, 1.2)]
J.append(f'tl.to("#labB", {{ scale: 1.1, transformOrigin: "50% 50%", duration: .18, yoyo: true, repeat: 5 }}, {F(tb + .2)});')
tf = w("s3", "Fehler") - .1
FX += [("glitch", tf + .55, .16, .4)]; shake(tf, 5, 10)
# s4: Theo von unten + ERROR 404, Mia dreht sich weg
t4 = s("s4")
cut(t4, NTX - 30, 1330, 1.15); cam(t4 + .05, NTX - 30, 1300, 1.25, 1.4, "none")
expr("t1", "grin", "happy", t4)
pop("#err", t4 + .2, .3, "50% 50%"); J.append(f'tl.set("#eT1", {{ opacity: 0 }}, {F(t4 + .2)});'); FX += [("glitch", t4 + 1.05, .16, .3)]
J.append(f'tl.to("#err", {{ x: 12, duration: .08, yoyo: true, repeat: 23, ease: "steps(1)" }}, {F(t4 + .6)}); tl.set("#err", {{ x: 0 }}, {F(t4 + .6 + .08 * 24 + .01)});')
ts = w("s4", "Seit") - .1
cut(ts, hmx[0] + 40, hmx[1] - 150, 1.7); expr("m1", "shock", "annoyed", ts)
fly("#m1", ts + .2, {"scaleX": 1, "transformOrigin": "50% 50%"}, {"scaleX": -1}, .25, "power2.inOut"); FX += [("swoosh", ts + .2, .3, .4)]
# s5: Countdown am Himmel
t5 = s("s5")
cut(t5, 540, 1000, 1.0); cam(t5 + .05, 540, 900, 1.15, 1.5)
pop("#cdg", t5 + .05, .3, "50% 0%"); FX += [("hit", t5 + .05, .4, .8)]
J.append(f'(() => {{ const o = {{ v: 59 }}; tl.fromTo(o, {{ v: 59 }}, {{ v: 50, duration: 4, ease: "none", immediateRender: false, onUpdate: () => {{ document.getElementById("cdt").textContent = "4T 11:" + String(Math.ceil(o.v)).padStart(2, "0"); }} }}, {F(t5)}); }})();')
FX += [("tick", t5 + .3, .35, 2.5)]
td = w("s5", "Dann") - .1
cut(td, 330, 1000, 1.7); expr("m12", "shock", "confused", td)
J.append(f'tl.to("#eM12", {{ scale: 1.25, transformOrigin: "50% 50%", duration: .2, yoyo: true, repeat: 5 }}, {F(td + .1)});')
# s6: Pfeil vom Passanten zu Mia – Zahl wird geklaut
t6 = s("s6")
cut(t6, 380, 1150, 1.15)
J.append(f'tl.fromTo("#arw", {{ opacity: 0 }}, {{ opacity: 1, duration: .1, immediateRender: false }}, {F(t6 + .2)}); tl.fromTo("#arwp", {{ strokeDashoffset: 300 }}, {{ strokeDashoffset: 0, duration: 1.0, ease: "none", immediateRender: false }}, {F(t6 + .2)});')
FX += [("whoosh", t6 + .2, .4, .7)]
expr("ps", "neutral", "shock", t6 + .5)
tn6 = w("s6", "Nähe.") - .5
hm13 = HEAD(PMX, 1900, 1.5)
cut(tn6, hm13[0], hm13[1] - 120, 1.6); expr("m13", "happy", "shock", tn6); FX += [("hit", tn6, .35, .6)]
hide("#arw", tn6)
# s7: Kamerafahrt zu Oma Hilde (900)
t7 = s("s7")
ho1 = HEAD(POX, 1900, 1.5)
cut(t7, hm13[0], hm13[1] - 100, 1.5); cam(t7 + .1, ho1[0] - 40, ho1[1] - 100, 1.5, .9)
wobble("#om1-a1", w("s7", "Oma") - .1, 5, 5, .2, "rotation", "50% 60%")
expr("om1", "relief", "happy", w("s7", "Oma"))
tn7 = w("s7", "Neunhundert.") - .1
cam(tn7, ho1[0], ho1[1] - 200, 1.7, .35, "power3.out")
J.append(f'tl.to("#bO1-in", {{ scale: 1.2, transformOrigin: "50% 50%", duration: .2, yoyo: true, repeat: 5 }}, {F(tn7)});'); FX += [("boing", tn7, .45, .5)]
expr("om1", "happy", "wink", tn7 + .3)
# s8: Plan – allein sein
t8 = s("s8")
cut(t8, 540, 1150, 1.1); cam(t8 + .05, 540, 1250, 1.3, 1.6, "none")
tsg = w("s8", "ganz") - .1
pop("#mapx", tsg, .25, "50% 50%"); FX += [("pop", tsg, .5, .3)]
# s9: Montag – Ben piekst mit Baguette
t9 = s("s9")
cut(t9, 540, 1000, 1.0)
tbn = w("s9", "Ben") - .1
cut(tbn, 560, 1250, 1.3)
tpk = w("s9", "Baguette:") - .15
J.append(f'tl.fromTo("#bn1-bag", {{ x: -196 }}, {{ x: -236, duration: .14, yoyo: true, repeat: 7, ease: "sine.inOut", immediateRender: false }}, {F(tpk)}); tl.set("#bn1-bag", {{ x: -196 }}, {F(tpk + .14 * 8 + .01)});')
FX += [("boing", tpk, .3, .4), ("boing", tpk + .3, .3, .4)]
tbg = w("s9", "Bist") - .1
hm15 = HEAD(230, 1900, 1.6)
cut(tbg, hm15[0] + 140, hm15[1] - 60, 1.8); expr("m15", "annoyed", "tired", tbg)
# s10: Ben isst das Baguette auf
t10 = s("s10")
hb1 = HEAD(900, 1900, 1.6)
cut(t10, hb1[0] - 120, hb1[1] - 40, 1.5)
J.append(f'tl.to("#bn1-bag", {{ scaleX: 0, transformOrigin: "100% 50%", duration: 1.0, ease: "steps(4)" }}, {F(t10 + .2)});')
expr("bn1", "hope", "full", t10 + .3); FX += [("pop", t10 + .3, .4, .2), ("pop", t10 + .6, .4, .2), ("pop", t10 + .9, .4, .2)]
J.append(f'tl.fromTo("#bn1", {{ y: 0 }}, {{ y: -10, duration: .12, yoyo: true, repeat: 9, ease: "sine.inOut", immediateRender: false }}, {F(t10 + .3)});')
ttb = w("s10", "Test") - .1
cut(ttb, 640, 1150, 1.15); expr("m15", "tired", "relief", ttb); FX += [("chime", ttb, .35, .8)]
# s11: Lehrer findet Mia nicht
t11 = s("s11")
cut(t11, 540, 1000, 1.0); cam(t11 + .05, 540, 980, 1.2, 1.2)
tc = w("s11", "Computer.") - .4
pop("#l404", tc, .3, "50% 50%"); FX += [("glitch", tc + .75, .16, .4)]
expr("kr1", "neutral", "confused", tc)
cut(tc + .9, 760, 1200, 1.7) if tc + .9 < s("s12") - .3 else None
# s12: Klassenbuch – Fragezeichen, dann Mia genervt
t12 = s("s12")
cut(t12, 540, 900, 1.05); cam(t12 + .05, 400, 880, 1.35, 1.2)
tq = w("s12", "Fragezeichen.") - .15
pop("#qm", tq, .3, "0% 50%"); FX += [("pop", tq, .55, .3)]
tm16 = min(tq + .8, s("s13") - .6)
cut(tm16, 540, 1050, 1.25); cam(tm16 + .05, 540, 1150, 1.45, .8)
# s13: Berg-Totale, Kamera fliegt hoch
t13 = s("s13")
cut(t13, 470, 1150, 2.6); cam(t13 + .1, 540, 700, 1.0, 2.6, "power2.inOut")
J.append(f'tl.fromTo("#mclimb", {{ x: 0, y: 0 }}, {{ x: 40, y: -60, duration: 3, ease: "none", immediateRender: false }}, {F(t13)});')
FX += [("whoosh", t13 + .3, .35, 1.0)]
# s14: Gipfel – Ben sitzt oben
t14 = s("s14")
cut(t14, 600, 1100, 1.15)
pop("#bub14", w("s14", "Ich") - .1, .25, "50% 50%"); FX += [("boing", w("s14", "Ich") - .1, .4, .4)]
J.append(f'tl.to("#bn2-bag", {{ rotation: 80, duration: .2, yoyo: true, repeat: 5, transformOrigin: "50% 50%" }}, {F(t14 + .2)});')
tal = w("s14", "allein!") - .1
hm18 = HEAD(280, 1900, 1.6)
cut(tal, hm18[0] + 40, hm18[1] - 120, 1.8); expr("m18", "shock", "facepalm", tal); hide("#bub14", tal, .05); FX += [("klong", tal, .3, .6)]
# s15: Wald – Oma Hilde mit Pilzen
t15 = s("s15")
cut(t15, 540, 1050, 1.0)
fly("#omw", t15 + .3, {"x": -260}, {"x": 0}, .5, "back.out(1.6)"); J.append('tl.set("#omw", { x: -260 }, 0);'); FX += [("boing", t15 + .3, .4, .4)]
tpz = w("s15", "Pilzesammeln.") - .3
ho2 = HEAD(760, 1900, 1.5)
cut(tpz, ho2[0] - 60, ho2[1] - 120, 1.7)
J.append(f'tl.to("#bO2-in", {{ scale: 1.2, transformOrigin: "50% 50%", duration: .18, yoyo: true, repeat: 3 }}, {F(tpz + .2)});')
# s16: Schulklo – Besetzt!
t16 = s("s16")
cut(t16, 540, 1000, 1.0); cam(t16 + .05, 540, 1000, 1.1, 1.0, "none")
tbs = w("s16", "Besetzt!") - .15
cut(tbs, 800, 900, 1.35); pop("#bub16", tbs, .2, "50% 50%"); shake(tbs, 7, 12); FX += [("hit", tbs, .4, .6)]
# s17: 11:59 – Theo reißt die Tür auf
t17 = s("s17")
cut(t17, 400, 1250, 1.3); cam(t17 + .05, 400, 1250, 1.45, 1.2, "none")
J.append(f'tl.to("#m20", {{ x: 6, duration: .05, yoyo: true, repeat: 15, ease: "none" }}, {F(t17 + .2)});')
tdo = w("s17", "reißt") - .1
J.append(f'tl.to("#d3", {{ scaleX: .06, transformOrigin: "100% 50%", duration: .22, ease: "power3.in" }}, {F(tdo)});')
cut(tdo + .2, 700, 1100, 1.1); FX += [("whoosh", tdo, .55, .6), ("hit", tdo + .2, .45, .6)]
expr("m20", "panic", "shock", tdo + .2)
tzm = w("s17", "Zu") - .1
pop("#bub17", tzm, .2, "50% 50%")
cam(tzm, 860, 1250, 1.45, .3, "power3.out")
# s18: Rücken an Rücken auf dem leeren Schulhof
t18 = s("s18")
cut(t18, 540, 1000, 1.0); cam(t18 + .05, 545, 1150, 1.2, 1.6, "none")
J.append(f'tl.set("#bT3", {{ opacity: 0 }}, 0); tl.set("#bM21", {{ opacity: 0 }}, 0);')
tvm = w("s18", "Von") - .1
cut(tvm, YTX - 40, HEAD(YTX, 1900, YS)[1] - 120, 1.7); expr("t3", "neutral", "determined", tvm)
# s19: 12:00 – über Mia rattert eine Zahl
t19 = s("s19")
settext("yclk", t19, "12:00", "11:59")
hm21 = HEAD(YMX, 1900, YS)
cut(t19, YMX, 1350, 1.45); cam(t19 + .05, YMX, 1250, 1.6, 1.5, "none")
FX += [("chime", t19, .5, 1.4)]
tra = w("s19", "rattert") - .2
J.append(f'tl.set("#eM21", {{ opacity: 0 }}, {F(tra)}); tl.set("#bM21", {{ opacity: 1 }}, {F(tra)}); tl.set("#eT3", {{ opacity: 0 }}, {F(tra)});')
J.append(f'(() => {{ const o = {{ v: 0 }}; tl.fromTo(o, {{ v: 0 }}, {{ v: 1, duration: {F(s("s20") + .15 - tra)}, ease: "none", immediateRender: false, onUpdate: () => {{ const n = Math.floor((Math.sin(o.v * 977) * .5 + .5) * 99999); document.getElementById("bM21-t").textContent = String(n).padStart(5, "0").replace(/(\\d\\d)(\\d\\d\\d)/, "$1.$2"); }} }}, {F(tra)}); }})();')
FX += [("blips", tra, .45, 1.2), ("riser", tra, .3, 1.5)]
expr("m21", "worried", "hope", tra)
# s20: 30.000 – Jubel
t20 = s("s20")
settext("bM21-t", t20 + .2, "30.000", "00.000")
J.append(f'tl.to("#bM21-in rect:nth-of-type(2)", {{ attr: {{ fill: "{GREEN}" }}, duration: .1 }}, {F(t20 + .2)}); tl.to("#bM21-t", {{ fill: "#fff", duration: .1 }}, {F(t20 + .2)});')
J.append(f'tl.fromTo("#bM21-in", {{ scale: 2.2, transformOrigin: "50% 50%" }}, {{ scale: 1, duration: .3, ease: "power4.in", immediateRender: false }}, {F(t20 + .2)});')
cut(t20 + .2, YMX + 60, 1150, 1.3); FX += [("hit", t20 + .2, .6, 1.0), ("chime", t20 + .3, .4, 1.0)]
J.append(f'tl.fromTo("#conf20", {{ opacity: 1, y: -300 }}, {{ y: 500, duration: 1.8, ease: "power1.in", immediateRender: false }}, {F(t20 + .2)}); tl.to("#conf20", {{ opacity: 0, duration: .3 }}, {F(t20 + 1.8)});')
expr("m21", "hope", "joy", t20 + .2)
J.append(f'tl.fromTo("#ym", {{ y: 0 }}, {{ y: -90, duration: .2, yoyo: true, repeat: 5, ease: "power2.out", immediateRender: false }}, {F(t20 + .4)});')
tj = w("s20", "springt") - .1
cam(tj, YMX + 40, 1250, 1.5, .6)
# s21: Zoom auf Theo – über ihm eine 1
t21 = s("s21")
cut(t21, 545, 1100, 1.15); expr("m21", "joy", "confused", t21 + .3)
J.append(f'tl.to("#ym", {{ x: -40, duration: .3 }}, {F(t21 + .3)});')
t1t = w("s21", "Eins.") - .25
J.append(f'tl.set("#eT3", {{ opacity: 0 }}, {F(t1t)}); tl.fromTo("#bT3", {{ opacity: 0 }}, {{ opacity: 1, duration: .05, immediateRender: false }}, {F(t1t)});')
J.append(f'tl.fromTo("#bT3-in", {{ scale: 3, transformOrigin: "50% 50%" }}, {{ scale: 1, duration: .25, ease: "power4.in", immediateRender: false }}, {F(t1t)});')
ht3 = HEAD(YTX, 1900, YS)
cut(w("s21", "Über") - .1, YTX, ht3[1] - 160, 1.5); cam(w("s21", "Über"), YTX, ht3[1] - 220, 1.9, 1.8, "power1.in")
FX += [("hit", t1t, .8, 1.5)]; shake(t1t + .25, 7, 12)
expr("m21", "confused", "shock", t1t + .2)
# s22: Theo grinst – die Regel
t22 = s("s22")
cut(t22, YTX, ht3[1] - 60, 2.1); expr("t3", "determined", "grinwink", t22 + .1); FX += [("blips", t22 + .1, .35, .5)]
cam(t22 + .1, YTX, ht3[1] - 30, 2.4, 2.0, "none")
tr = w("s22", "Regel.") - .4
cut(tr, 545, 1150, 1.2)
# s23/s24: A oder B – Bild bleibt bis zum letzten Frame
t23 = s("s23")
cut(t23, 540, 1000, 1.0)
for lab in ("A2", "B2"): J.append(f'tl.set("#lab{lab}", {{ opacity: 0 }}, 0);')
ta = w("s23", "A:") - .1; tb2 = w("s23", "B:") - .1
pop("#labA2", ta, .3, "50% 50%"); pop("#labB2", tb2, .3, "50% 50%"); FX += [("pop", ta, .5, .3), ("pop", tb2, .5, .3)]
cut(ta, 330, 1000, 1.25); cut(tb2, 750, 1000, 1.25)
tsc = w("s23", "Schreib") - .1
cut(tsc, 540, 1000, 1.0)
J.append(f'tl.to("#labA2", {{ scale: 1.08, duration: .2, yoyo: true, repeat: 3, transformOrigin: "50% 50%" }}, {F(tsc)}); tl.to("#labB2", {{ scale: 1.08, duration: .2, yoyo: true, repeat: 3, transformOrigin: "50% 50%" }}, {F(tsc + .1)});')
t24 = s("s24")
cam(t24, 380, 1000, 1.12, .4)
tdn = w("s24", "Denn") - .1
cam(tdn, 700, 1000, 1.12, .5)
tfj = w("s24", "Fast") - .1
cam(tfj, 540, 1000, 1.0, .6)
tEND = round(END - 1.5, 2)
# Loop: die rote 1 über Theo flackert kurz auf „leer“
tl_ = END - .7
J.append(f'tl.to("#bT5", {{ opacity: 0, duration: .06, yoyo: true, repeat: 3, ease: "steps(1)" }}, {F(tl_)}); tl.set("#eT5", {{ opacity: 1 }}, {F(END - .25)}); tl.set("#bT5", {{ opacity: 0 }}, {F(END - .25)});')
FX += [("glitch", tl_, .3, .5)]

sets = [("N", 0, t2), ("R", t2, t3), ("Z", t3, te), ("N", te, tb), ("Z", tb, t4), ("N", t4, t5), ("U", t5, t6), ("P", t6, t8), ("K", t8, t9), ("C", t9, t11),
        ("L", t11, t12), ("B", t12, tm16), ("B2", tm16, t13), ("M", t13, t14), ("S", t14, t15), ("W", t15, t16), ("T", t16, t17), ("T2", t17, t18), ("Y", t18, t23), ("AB", t23, END)]

OBEN = [(0, "ZAHL: <span style='color:#ff4d5a'>???</span>"), (t2, "TEIL 1 + 2"), (t3, "UNSTERBLICH?"), (tb, "B ✔ FEHLER IM SYSTEM"), (t4, "SEIT 3 JAHREN"), (t5, "UPDATE: SO 12:00"),
        (t6, "⚠ ZAHL WIRD GEKLAUT"), (t7, "NEBEN MIA: 900"), (t8, "PLAN: ALLEIN"), (t9, "GEISTER-TEST"), (ttb, "10/10"), (t11, "MIA? 404"), (t12, "NAME: ?"),
        (t13, "SO · 11:30"), (tal, "NEIN!"), (t15, "SO · 11:45"), (t16, "SO · 11:58"), (t17, "<span style='color:#ff4d5a'>11:59</span>"), (t18, "KEINE ZAHL = SICHER?"),
        (t19, "12:00 UPDATE"), (t20 + .2, "30.000 TAGE 🎉"), (t21, "…"), (t1t, "THEO: <span style='color:#ff4d5a'>1</span>"), (t22, "DIE REGEL 😏"),
        (t23, "A oder B? 👇")]
J.append(f'tl.to("#ob0-in", {{ opacity: .4, duration: .15, yoyo: true, repeat: 9, ease: "steps(1)" }}, .3);')
tag = (f'<div class="ui clip" data-start="0" data-duration="{F(t2)}" style="left:30px;top:40px;font:900 36px Inter,sans-serif;color:#fff;background:rgba(0,0,0,.55);padding:6px 16px;border-radius:12px">IN DIESER WELT … #3</div>'
       f'<div class="ui clip" data-start="{F(t2)}" data-duration="{F(t3 - t2)}" style="left:30px;top:40px;font:900 40px Inter,sans-serif;color:#111;background:#ffd166;padding:6px 18px;border-radius:12px">⏪ WAS BISHER GESCHAH</div>'
       f'<div class="ui clip" data-start="{F(t3)}" data-duration="{F(END - t3)}" style="left:30px;top:40px;font:900 36px Inter,sans-serif;color:#fff;background:rgba(0,0,0,.55);padding:6px 16px;border-radius:12px">IN DIESER WELT … #3</div>')
HOT = {"1", "NICHTS", "THEO", "UPDATE", "900", "B", "A", "ALLEIN", "GEIST", "FRAGEZEICHEN", "BESETZT", "30.000", "EINE", "REGEL", "FAST", "JEDER"}
finish(S, sets, OBEN, FX, HOT, tag, banner=("TEIL 4?", "➕ FOLGEN"))
