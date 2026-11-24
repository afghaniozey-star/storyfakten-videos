"""STORY-FORMAT „In dieser Welt …“ – Die Zahl über dem Kopf, TEIL 4: „ADMIN“ (Theo hat absichtlich gelacht, 100 Lacher, Oma Hilde = ADMIN).
Aufruf: python3 tools/story4.py  (liest voice.json (= voice-teil4.json) + assets/vo/timing.json; Bausteine aus tools/bausteine.py;
Musik = fester Hintergrund-Sound assets/bgm.mp3 über tools/story_musik.py)
Regeln aus erkenntnisse.md (Trend-Scout 24.11.): Welt-Regel + Zahl ab 0,0 s im Bild (kein „?“-Kasten), Mia in JEDER Szene gleich
(pinker Hoodie + pinke Haarspange), Schnitt alle 2–3 s, A/B-Bild bis zum letzten Frame, ADMIN blinkt bis zum Schluss."""
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
def sepia(content, label):
    return (content + '<rect width="1080" height="1920" fill="#c9a26b" opacity=".38"/>'
            '<rect x="24" y="24" width="1032" height="1872" rx="30" fill="none" stroke="#fff" stroke-width="18" stroke-dasharray="40 24"/>'
            f'<text x="540" y="1840" text-anchor="middle" style="font:900 54px {FONT};fill:#fff;opacity:.9">{label}</text>')
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

S = {}; FX = []
# --- A: Bild 0 – Nacht, Theo mit roter 1, Mia mit 30.000, Passant im Hintergrund (Welt-Regel sofort sichtbar)
AMX, ATX = 310, 730
S["A"] = (street_bg(night=True) + night_lamp() +
          fig(passant("pa2", "#ffb703", hair="lena", hcol="#222") + WB("bPa2", "7.300", size=70, y=-610), 930, 1290, .5) +
          fig(mia("m1", "worried") + GB("bM1", "30.000", size=66, y=-640), AMX, 1900, 1.5) +
          fig(theo("t1", "grin") + RB("bT1", "1", size=130, y=-640), ATX, 1900, 1.65))
# --- R: Rückblick (3 Bilder aus Teil 3)
TOILET = '<g transform="translate(330 1900)"><rect x="-150" y="-330" width="300" height="200" rx="30" fill="#fff" stroke="#111" stroke-width="7"/><rect x="-170" y="-150" width="340" height="80" rx="30" fill="#f8f9fa" stroke="#111" stroke-width="7"/><rect x="-110" y="-80" width="220" height="80" fill="#fff" stroke="#111" stroke-width="7"/></g>'
S["R"] = ('<g id="r1">' + sepia(TILES("#dee2e6") + '<rect x="600" y="300" width="480" height="1500" fill="#495057"/>' + TOILET +
                                fig(theo("t2", "determined", arm=("down", "out")), 860, 1900, 1.6) + fig(mia("m2", "panic"), 330, 1780, 1.45) +
                                '<rect y="1800" width="1080" height="120" fill="#adb5bd"/>', "TEIL 3: THEO RETTET MIA") + '</g>'
          '<g id="r2" opacity="0">' + sepia('<rect width="1080" height="1920" fill="#ffb4a2"/><rect y="1120" width="1080" height="800" fill="#adb5bd"/>' +
                                             fig(mia("m3", "joy", arm=("up", "up")) + GB("bM3", "30.000", size=84, y=-640), 540, 1900, 1.75) + confetti("conf2", 300) , "MIA: 30.000 TAGE") + '</g>'
          '<g id="r3" opacity="0">' + sepia('<rect width="1080" height="1920" fill="#ffb4a2"/><rect y="1120" width="1080" height="800" fill="#adb5bd"/>' +
                                             fig(theo("t3", "grinwink") + RB("bT3", "1", size=120, y=-640), 540, 1900, 1.8), "THEO: 1 😏") + '</g>')
# --- C: Mia packt Theo am Kragen (Theo rechts)  /  C2: Gegenschuss (Theo vorne links, ganz ruhig)
CMX, CTX, CS = 380, 770, 1.7
S["C"] = (street_bg(night=True) +
          fig(theo("t4", "neutral", arm=("down", "down"), arm2=("out", "down")) + RB("bT4", "1", size=100, y=-640), CTX, 1900, CS) +
          fig(mia("m4", "determined", arm=("down", "front")) + GB("bM4", "30.000", size=64, y=-640), CMX, 1900, CS))
C2TX, C2MX = 330, 830
S["C2"] = (street_bg(night=True) + night_lamp() +
           fig(mia("m5", "determined", arm=("front", "down")) + GB("bM5", "30.000", size=64, y=-640), C2MX, 1900, 1.45) +
           fig(theo("t5", "neutral", arm=("down", "down"), arm2=("down", "front")) + RB("bT5", "1", size=100, y=-640), C2TX, 1900, 1.85))
# --- F: Rückblende-Blitz: Kapuzen-Theo lacht übertrieben, Zähler 100/100
S["F"] = sepia('<rect width="1080" height="1920" fill="#8ecae6"/><rect x="0" y="380" width="1080" height="900" fill="#f4a261" stroke="#111" stroke-width="6"/>'
               f'<rect x="80" y="420" width="920" height="150" rx="20" fill="#fff" stroke="#111" stroke-width="6"/><text x="540" y="530" text-anchor="middle" style="font:900 100px {FONT};fill:#9c4f1f">BÄCKEREI</text>'
               '<rect x="0" y="1280" width="1080" height="640" fill="#adb5bd"/>' +
               f'<g id="fth">{fig(theo("t6", "laugh", hood=True, arm=("up", "up")), 540, 1900, 1.75)}</g>'
               f'<g transform="translate(540 760)"><rect x="-330" y="-110" width="660" height="200" rx="34" fill="{GREEN}" stroke="#111" stroke-width="9"/><text x="0" y="40" text-anchor="middle" style="font:900 130px {FONT};fill:#fff">😂 100/100</text></g>', "TEIL 2: DER 100. LACHER")
# --- U: Theo nah mit pulsierender 1, Uhr im Hintergrund
S["U"] = ('<rect width="1080" height="1920" fill="#1d3557"/>' + "".join(f'<rect x="{(k * 137) % 1060}" y="{60 + (k * 71) % 500}" width="6" height="6" fill="#fff"/>' for k in range(24)) +
          '<rect x="80" y="160" width="360" height="1760" fill="#6c757d" stroke="#111" stroke-width="7"/><path d="M60 170 L260 20 L460 170 Z" fill="#495057" stroke="#111" stroke-width="7"/>' +
          clock_face(260, 420, 150, 11, 20, "clk1") +
          f'<rect x="130" y="640" width="260" height="90" rx="14" fill="#111" stroke="#00f5d4" stroke-width="6"/><text x="260" y="708" text-anchor="middle" style="font:900 64px Inter,monospace;fill:#00f5d4">00:00</text>'
          '<rect y="1500" width="1080" height="420" fill="#495057"/>' +
          fig(theo("t7", "determined") + RB("bT7", "1", size=120, y=-640), 690, 2060, 2.0))
# --- D: Mia verschränkt die Arme, Gedankenblitz
BOLT = ('<g id="bolt" opacity="0"><path d="M860 640 L760 900 L850 900 L770 1120 L960 820 L870 820 L950 640 Z" fill="#ffd60a" stroke="#111" stroke-width="8" stroke-linejoin="round"/></g>')
SIGN = (f'<g id="sign" opacity="0"><rect x="90" y="620" width="400" height="230" rx="26" fill="#fff" stroke="#111" stroke-width="8"/>'
        f'<text x="290" y="720" text-anchor="middle" style="font:900 74px {FONT};fill:#111">100 😂</text><text x="290" y="810" text-anchor="middle" style="font:900 60px {FONT};fill:{RED}">= 1 WEG</text></g>')
S["D"] = (street_bg() + fig(mia("m8", "annoyed", arm=("cross", "cross")) + GB("bM8", "30.000", size=64, y=-640), 540, 1900, 1.8) + BOLT + SIGN)
# --- E: Theo todernst
S["E"] = ('<rect width="1080" height="1920" fill="#adb5bd"/>' + "".join(f'<rect x="0" y="{k * 120}" width="1080" height="60" fill="#000" opacity=".04"/>' for k in range(16)) +
          '<rect y="1500" width="1080" height="420" fill="#6c757d"/>' + fig(theo("t9", "deadpan") + RB("bT9", "1", size=100, y=-640), 540, 1960, 1.9))
# --- BN: Versuch 1 – Ben kaut Baguette
S["BN"] = (street_bg() +
           fig(theo("t10", "happy", arm=("down", "out")) + RB("bT10", "1", size=90, y=-640), 300, 1900, 1.55) +
           fig(ben("bn1", "neutral", arm=("down", "mic"), extra=bag("bn1", 74, -300, 120, 180)), 800, 1900, 1.55) +
           bubble("bub10", ["KENNST DU", "DEN SCHON …?"], 560, 700, 600, tail=(-.8, 1), size=58))
# --- KL: Versuch 2 – Herr Krause lacht hinter der Klo-Tür über seinen eigenen Witz
S["KL"] = (TILES() +
           fig(krause("kr1", "laugh", arm=("down", "up")), 900, 1720, 1.3) +
           '<g id="door"><rect x="420" y="520" width="380" height="1180" rx="14" fill="#4cc9f0" stroke="#111" stroke-width="8"/>'
           '<rect x="460" y="1080" width="40" height="80" rx="10" fill="#adb5bd" stroke="#111" stroke-width="4"/><rect x="560" y="620" width="100" height="56" rx="10" fill="#e63946" stroke="#111" stroke-width="4"/>'
           f'<text x="610" y="662" text-anchor="middle" style="font:900 30px {FONT};fill:#fff">WC</text></g>'
           '<rect y="1700" width="1080" height="220" fill="#adb5bd"/>' +
           fig(theo("t11", "neutral") + RB("bT11", "1", size=90, y=-640), 220, 1900, 1.5) +
           bubble("bub11", ["HAHA!"], 760, 470, 440, tail=(.7, 1), size=110) +
           '<g id="xx" opacity="0"><path d="M90 760 L350 1020 M350 760 L90 1020" stroke="#e63946" stroke-width="34" stroke-linecap="round"/></g>')
# --- H: Hühnerkostüm – Straße lacht
crowd = [(70, "#3a86ff", "mann"), (180, "#06d6a0", "lena"), (870, "#ffb703", "mann"), (975, "#8338ec", "ben"), (1060, "#ff006e", "lena")]
S["H"] = (street_bg() + "".join(f'<g id="cr{k}">' + fig(passant(f"c{k}", col, hair=h, hcol="#3d2b1f", arm=("down", "up")), x, 1300, .55) + '</g>' for k, (x, col, h) in enumerate(crowd)) +
          f'<g id="hT0">{fig(theo("t12", "deadpan") + RB("bT12", "1", size=90, y=-660), 620, 1900, 1.6)}</g>'
          f'<g id="hT1" opacity="0">{fig(theo("t13", "annoyed", chicken=True) + RB("bT13", "1", size=90, y=-660), 620, 1900, 1.6)}</g>' +
          fig(mia("m12", "laugh", arm=("down", "up")) + GB("bM12", "30.000", size=60, y=-640), 230, 1900, 1.45))
# --- Z: 23:59 Countdown
S["Z"] = ('<rect width="1080" height="1920" fill="#0b132b"/>' + "".join(f'<rect x="{(k * 137) % 1060}" y="{60 + (k * 71) % 1700}" width="6" height="6" fill="#fff" opacity=".6"/>' for k in range(40)) +
          '<g id="zc"><rect x="60" y="560" width="960" height="420" rx="50" fill="#000" stroke="#ff3b30" stroke-width="12"/>'
          '<text id="zct" x="540" y="860" text-anchor="middle" style="font:900 250px Inter,monospace;fill:#ff3b30">23:59</text></g>'
          f'<g id="zn"><rect x="190" y="1080" width="700" height="240" rx="40" fill="{GREEN}" stroke="#111" stroke-width="10"/><text x="540" y="1240" text-anchor="middle" style="font:900 150px {FONT};fill:#fff">😂 99/100</text></g>'
          f'<g id="zf" opacity="0"><rect x="290" y="1400" width="500" height="160" rx="30" fill="#fff" stroke="#111" stroke-width="8"/><text x="540" y="1510" text-anchor="middle" style="font:900 96px {FONT};fill:{RED}">1 FEHLT!</text></g>')
# --- O: Oma Hilde mit Pilzkorb, Mia fleht, Theo (Huhn) daneben
BASKET = '<g transform="translate(-170 -150)"><path d="M-70 -40 Q0 -140 70 -40" stroke="#6b4226" stroke-width="12" fill="none"/><rect x="-80" y="-50" width="160" height="110" rx="20" fill="#bc6c25" stroke="#111" stroke-width="5"/>' + \
         "".join(f'<g transform="translate({dx} -50)"><rect x="-8" y="-6" width="16" height="30" fill="#fff" stroke="#111" stroke-width="3"/><path d="M-30 -4 Q0 -46 30 -4 Z" fill="#e63946" stroke="#111" stroke-width="4"/><circle cx="-8" cy="-18" r="5" fill="#fff"/></g>' for dx in (-45, 0, 45)) + '</g>'
OMX, OOX, OTX = 470, 830, 150
S["O"] = (street_bg(night=True) + night_lamp() +
          fig(theo("t14", "worried", chicken=True) + RB("bT14", "1", size=80, y=-660), OTX, 1700, 1.15) +
          f'<g id="omg">{fig(oma("om1", "relief", arm=("hip", "down"), extra=BASKET) + WB("bO1", "900", size=76, y=-640), OOX, 1900, 1.55)}</g>'
          f'<g id="mig">{fig(mia("m14", "plead", arm=("pray", "pray")) + GB("bM14", "30.000", size=60, y=-640), OMX, 1900, 1.5)}</g>' +
          bubble("bub14", ["BITTE LACH!"], 470, 560, 600, tail=(0, 1), size=80))
# --- G: Mitternacht – Glocke, Flackern, Theos 1 glitcht
GL = ('<g id="glt" opacity="0">' + "".join(f'<rect x="{-150 + (k * 71) % 300}" y="{-780 + (k * 53) % 200}" width="{40 + (k * 31) % 90}" height="18" fill="{("#00f5d4", "#f15bb5", "#fee440")[k % 3]}" opacity=".9"/>' for k in range(12)) + '</g>')
S["G"] = ('<rect width="1080" height="1920" fill="#10002b"/>' + clock_face(250, 360, 150, 0, 0, "clk2") +
          '<rect y="1500" width="1080" height="420" fill="#240046"/>' +
          fig(theo("t16", "worried", chicken=True) + RB("bT16", "1", size=120, y=-680) + GL, 600, 2060, 2.0) +
          '<rect id="flash" width="1080" height="1920" fill="#fff" opacity="0"/>')
# --- V: Reihe Ben / Krause / Oma – Theo sieht die echten Zahlen, über Oma: ADMIN
S["V"] = (street_bg(night=True) +
          fig(ben("bn3", "happy") + WB("bB3", "12.000", size=50, y=-640), 180, 1900, 1.3) +
          fig(krause("kr3", "neutral") + WB("bK3", "9.000", size=52, y=-640), 525, 1900, 1.3) +
          fig(oma("om3", "relief", arm=("down", "down"), arm2=("down", "front"),
                  extra='<g id="om3-mush" opacity="0"><g transform="translate(196 -380)"><rect x="-10" y="-10" width="20" height="44" fill="#fff" stroke="#111" stroke-width="4"/><path d="M-44 -6 Q0 -70 44 -6 Z" fill="#e63946" stroke="#111" stroke-width="5"/><circle cx="-12" cy="-26" r="7" fill="#fff"/></g></g>')
              + WB("bO3", "900", size=70, y=-640) + admin("aO3", size=58, y=-640, vis=False), 870, 1900, 1.45) +
          '<rect id="vfl" width="1080" height="1920" fill="#39ff14" opacity="0"/>')
# --- AB: Split – A: Oma am Riesen-Computer (System gebaut) | B: Oma gehackt (Glitch + Hacker-Maus)
SCREEN = ('<g id="scr" transform="translate(0 -70)"><rect x="40" y="860" width="460" height="420" rx="24" fill="#343a40" stroke="#111" stroke-width="8"/><rect x="66" y="886" width="408" height="300" rx="10" fill="#0b132b"/>'
          + fig(mia("m20", "happy") + GB("bM20", "30.000", size=90, y=-640), 170, 1180, .42)
          + fig(theo("t20", "grin") + RB("bT20", "1", size=120, y=-640), 370, 1180, .42) +
          '<rect x="80" y="1205" width="380" height="50" rx="10" fill="#495057"/>' + "".join(f'<rect x="{94 + k * 46}" y="1215" width="34" height="30" rx="6" fill="{("#e63946", "#2dc653", "#ffd166")[k % 3]}"/>' for k in range(8)) + '</g>')
MOUSE = ('<g transform="translate(985 1930) scale(.62)"><ellipse cx="0" cy="6" rx="110" ry="20" fill="#000" opacity=".3"/>'
         '<rect x="-70" y="-230" width="140" height="230" rx="30" fill="#141418" stroke="#000" stroke-width="5"/>'
         '<rect x="-150" y="-430" width="80" height="80" rx="40" fill="#adb5bd" stroke="#111" stroke-width="5"/><rect x="70" y="-430" width="80" height="80" rx="40" fill="#adb5bd" stroke="#111" stroke-width="5"/>'
         '<rect x="-90" y="-400" width="180" height="170" rx="40" fill="#adb5bd" stroke="#111" stroke-width="5"/>'
         '<path d="M-104 -300 V-380 Q-104 -430 0 -436 Q104 -430 104 -380 V-300 Q60 -340 0 -340 Q-60 -340 -104 -300 Z" fill="#141418"/>'
         '<rect x="-50" y="-320" width="30" height="30" rx="6" fill="#39ff14"/><rect x="20" y="-320" width="30" height="30" rx="6" fill="#39ff14"/><rect x="-14" y="-276" width="28" height="20" rx="8" fill="#ff8fa3" stroke="#111" stroke-width="3"/>'
         '<rect x="-120" y="-150" width="240" height="110" rx="10" fill="#495057" stroke="#111" stroke-width="5"/><rect x="-100" y="-136" width="200" height="80" fill="#39ff14" opacity=".55"/>'
         '<path d="M70 -20 Q180 40 160 120" stroke="#adb5bd" stroke-width="14" fill="none" stroke-linecap="round"/></g>')
glitchB = ('<g id="gltB">' + "".join(f'<rect x="{560 + (k * 71) % 480}" y="{1050 + (k * 113) % 820}" width="{40 + (k * 31) % 110}" height="22" fill="{("#00f5d4", "#f15bb5", "#fee440")[k % 3]}" opacity=".85"/>' for k in range(16)) + '</g>')
S["AB"] = ('<rect width="540" height="1920" fill="#fff3b0"/><rect x="540" width="540" height="1920" fill="#1a1a2e"/>' +
           '<svg x="0" y="0" width="540" height="1920" overflow="hidden">' + SCREEN +
           fig(oma("om5", "happy", arm=("front", "down")) + admin("aO5", size=62, y=-640), 300, 2230, 1.12) + '</svg>'
           '<svg x="540" y="0" width="540" height="1920" overflow="hidden">' +
           fig(oma("om6", "annoyed") + admin("aO6", size=62, y=-640), 250, 2230, 1.12) + '</svg>' + glitchB + MOUSE +
           '<rect x="530" width="20" height="1920" fill="#111"/>'
           f'<g id="labA"><rect x="40" y="550" width="460" height="230" rx="30" fill="#ffd166" stroke="#111" stroke-width="7"/><text x="270" y="660" text-anchor="middle" style="font:900 110px {FONT};fill:#111">A</text>'
           f'<text x="270" y="740" text-anchor="middle" style="font:900 40px {FONT};fill:#111">SYSTEM GEBAUT</text></g>'
           f'<g id="labB"><rect x="580" y="550" width="460" height="230" rx="30" fill="#f15bb5" stroke="#111" stroke-width="7"/><text x="810" y="660" text-anchor="middle" style="font:900 110px {FONT};fill:#fff">B</text>'
           f'<text x="810" y="740" text-anchor="middle" style="font:900 40px {FONT};fill:#fff">GEHACKT</text></g>')

# ---------- Zeitplan ----------
J.append('tl.set("#cam", { x: 0, y: 0, scale: 1, svgOrigin: "0 0" }, 0);')
s = st
H_ = HEAD
# s1 (0,0): Welt-Regel + Theos rote 1 + Mias 30.000 sofort groß im Bild
t1 = s("s1")
cut(0, 520, 1250, 1.1); cam(.05, 520, 1200, 1.2, 1.6, "power1.out")
J.append('tl.to("#bT1-in", { scale: 1.18, transformOrigin: "50% 50%", duration: .3, yoyo: true, repeat: 5, ease: "sine.inOut" }, 0);')
FX += [("hit", 0, .18, 1.0)]
tj = w("s1", "jedem") - .1
cut(tj, 540, 1150, 1.0); FX += [("swoosh", tj - .05, .4, .5)]
tt = w("s1", "Tage") - .1
cut(tt, AMX + 40, 1900 - 640 * 1.5 + 60, 1.85); expr("m1", "worried", "happy", tt); FX += [("pop", tt, .5, .3)]
tth = w("s1", "Theo") - .1
cut(tth, ATX - 20, 1900 - 640 * 1.65 + 120, 1.75); cam(tth + .05, ATX - 20, 1900 - 640 * 1.65 + 40, 2.0, 1.0, "power3.out")
J.append(f'tl.fromTo("#bT1-in", {{ scale: 2.2, transformOrigin: "50% 50%" }}, {{ scale: 1, duration: .25, ease: "power4.in", immediateRender: false }}, {F(tth + .2)});')
FX += [("hit", tth + .2, .3, 1.2)]; shake(tth + .45, 6, 12)
# s2: Rückblick-Montage (3 Bilder)
t2 = s("s2"); t3 = s("s3")
d2 = (t3 - t2) / 3
for k in range(3):
    a = t2 + k * d2
    if k: J.append(f'tl.set("#r{k}", {{ opacity: 0 }}, {F(a)}); tl.set("#r{k + 1}", {{ opacity: 1 }}, {F(a)});')
    cut(a, 540, 1050 - k * 40, 1.0 + .05 * (k % 2)); cam(a + .02, 540, 1000, 1.12 + .05 * (k % 2), d2, "none")
    FX += [("swoosh", a, .15, .4)]
J.append(f'tl.fromTo("#conf2", {{ opacity: 1, y: -200 }}, {{ y: 300, duration: {F(d2)}, ease: "none", immediateRender: false }}, {F(t2 + d2)}); tl.set("#conf2", {{ opacity: 0 }}, {F(t2 + 2 * d2)});')
FX += [("blips", t2 + d2, .12, .6)]
# s3: Mia packt Theo am Kragen
hm4 = H_(CMX, 1900, CS); ht4 = H_(CTX, 1900, CS)
cut(t3, 575, 1300, 1.25); cam(t3 + .05, 575, 1250, 1.35, 1.0)
J.append(f'tl.fromTo("#t4", {{ x: 0 }}, {{ x: -14, duration: .07, yoyo: true, repeat: 5, ease: "none", immediateRender: false }}, {F(t3 + .15)});'); FX += [("whoosh", t3 + .05, .4, .5)]
tr = w("s3", "rette") - .15
cut(tr, hm4[0] + 30, hm4[1] - 60, 1.9); FX += [("hit", tr, .35, .6)]
tn = w("s3", "nehm") - .1
cut(tn, 575, 1450, 1.1); cam(tn + .05, 575, 1350, 1.2, .9)
J.append(f'tl.to("#bT4-in", {{ scale: 1.2, transformOrigin: "50% 50%", duration: .2, yoyo: true, repeat: 3 }}, {F(tn + .2)});')
# s4: Gegenschuss – Theo schiebt die Hand weg, ganz ruhig
t4 = s("s4")
ht5 = H_(C2TX, 1900, 1.85)
cut(t4, ht5[0] + 120, 950, 1.45); FX += [("swoosh", t4, .4, .5)]
tnein = w("s4", "Nein.") - .05
armswap("t5", tnein); FX += [("klong", tnein, .3, .6)]
J.append(f'tl.fromTo("#m5", {{ x: 0 }}, {{ x: 40, duration: .25, ease: "power2.out", immediateRender: false }}, {F(tnein + .05)});')
ta = w("s4", "absichtlich") - .15
cut(ta, ht5[0], ht5[1] - 80, 2.0); expr("t5", "neutral", "grin", ta); FX += [("blips", ta, .3, .5)]
# s5: Rückblende-Blitz, dann Mias Gesicht
t5 = s("s5")
cut(t5, 540, 1100, 1.05); cam(t5 + .02, 540, 1050, 1.2, .8, "none")
J.append(f'tl.fromTo("#fth", {{ y: 0 }}, {{ y: -40, duration: .1, yoyo: true, repeat: 7, ease: "sine.inOut", immediateRender: false }}, {F(t5)});')
FX += [("glitch", t5, .3, .4)]
tdu = w("s5", "Du") - .12
hm5 = H_(C2MX, 1900, 1.45)
cut(tdu, hm5[0] - 20, hm5[1] - 40, 2.1); expr("m5", "determined", "shock", tdu); FX += [("hit", tdu, .5, .8)]; shake(tdu + .1, 6, 14)
# s6: Theo zeigt auf Mia (Einstellung C: Theo rechts), zuckt mit den Schultern
t6 = s("s6")
cut(t6, 575, 1250, 1.2); armswap("t4", t6 + .2); expr("t4", "neutral", "grin", t6 + .2); FX += [("swoosh", t6 + .2, .3, .4)]
expr("m4", "determined", "shock", t6)
tdw = w("s6", "Das") - .1
cut(tdw, ht4[0] - 30, ht4[1] - 40, 1.85); expr("t4", "grin", "grinwink", tdw)
J.append(f'tl.fromTo("#t4-a2", {{ y: 0 }}, {{ y: -26, duration: .18, yoyo: true, repeat: 3, ease: "sine.inOut", immediateRender: false }}, {F(tdw + .3)});')
FX += [("boing", tdw + .3, .35, .5)]
# s7: Theos 1 pulsiert, Uhr im Hintergrund
t7 = s("s7")
cut(t7, 690, 2060 - 640 * 2 + 40, 1.35); cam(t7 + .05, 690, 2060 - 640 * 2 + 40, 1.55, 1.4, "none")
J.append(f'tl.to("#bT7-in", {{ scale: 1.15, transformOrigin: "50% 50%", duration: .35, yoyo: true, repeat: 11, ease: "sine.inOut" }}, {F(t7)});'); FX += [("tick", t7 + .1, .35, 1.6)]
tmn = w("s7", "Mitternacht,") - .1
cut(tmn, 260, 560, 1.6); cam(tmn + .05, 260, 560, 1.8, .8); FX += [("klong", tmn, .3, 1.0)]
J.append(f'tl.to("#clk1 path:nth-of-type(2)", {{ rotation: 240, svgOrigin: "260 420", duration: 1.0, ease: "power2.in" }}, {F(tmn)});')
tdr = w("s7", "Darauf") - .1
ht7 = H_(690, 2060, 2.0)
cut(tdr, 690, 1000, 1.3); expr("t7", "determined", "grin", tdr); FX += [("blips", tdr, .3, .6)]
# s8: Mia – Arme verschränkt, Gedankenblitz
t8 = s("s8")
hm8 = H_(540, 1900, 1.8)
cut(t8, 540, 1300, 1.2); FX += [("swoosh", t8, .3, .4)]
tth8 = w("s8", "Theo") - .1
cut(tth8, 640, 1000, 1.35); pop("#bolt", tth8, .25, "50% 100%"); expr("m8", "annoyed", "determined", tth8); FX += [("hit", tth8, .35, .6)]
tdn = w("s8", "Dann") - .1
cut(tdn, 400, 1000, 1.25); pop("#sign", tdn, .3, "50% 50%"); FX += [("pop", tdn, .5, .3)]
# s9: Theo todernst
t9 = s("s9")
ht9 = H_(540, 1960, 1.9)
cut(t9, 540, 1550, 1.2); cam(t9 + .05, 540, 1000, 1.35, 1.4, "power2.inOut"); FX += [("klong", t9 + .1, .3, .6)]
# s10: Versuch 1 – Ben kaut
t10 = s("s10")
cut(t10, 550, 1250, 1.15); FX += [("swoosh", t10, .3, .4)]
twz = w("s10", "Theo") - .1
ht10 = H_(300, 1900, 1.55)
cut(twz, 440, 1000, 1.25); pop("#bub10", twz + .1, .25, "50% 100%"); FX += [("boing", twz + .1, .35, .4)]
tbk = w("s10", "Ben", 2) - .1
hb1 = H_(800, 1900, 1.55)
cut(tbk, hb1[0] - 80, hb1[1] - 30, 1.85); hide("#bub10", tbk, .05); expr("bn1", "neutral", "full", tbk)
J.append(f'tl.to("#bn1-bag", {{ scaleX: .2, transformOrigin: "100% 50%", duration: 1.2, ease: "steps(4)" }}, {F(tbk + .1)});')
J.append(f'tl.fromTo("#bn1", {{ y: 0 }}, {{ y: -10, duration: .12, yoyo: true, repeat: 9, ease: "sine.inOut", immediateRender: false }}, {F(tbk + .1)});')
FX += [("pop", tbk + .2, .4, .2), ("pop", tbk + .5, .4, .2), ("pop", tbk + .8, .4, .2)]
# s11: Versuch 2 – Herr Krause lacht über seinen eigenen Witz
t11 = s("s11")
cut(t11, 540, 1150, 1.05)
tla = w("s11", "lacht!") - .15
cut(tla, 780, 760, 1.35); pop("#bub11", tla, .2, "50% 50%"); shake(tla, 7, 12); FX += [("hit", tla, .35, .6)]
J.append(f'tl.fromTo("#kr1", {{ y: 0 }}, {{ y: -20, duration: .1, yoyo: true, repeat: 11, ease: "sine.inOut", immediateRender: false }}, {F(tla)});')
tub = w("s11", "Über") - .1
hk1 = H_(900, 1720, 1.3)
cut(tub, hk1[0] - 60, hk1[1] - 20, 1.9)
tz = w("s11", "Zählt") - .1
ht11 = H_(220, 1900, 1.5)
cut(tz, 300, ht11[1] + 60, 1.45); expr("t11", "neutral", "annoyed", tz); pop("#xx", tz + .05, .2, "50% 50%"); FX += [("klong", tz, .35, .6)]
# s12: Hühnerkostüm – ganze Straße lacht, Zähler rast hoch
t12 = s("s12")
cut(t12, 420, 1250, 1.25); expr("m12", "laugh", "joy", t12)
thk = w("s12", "Hühnerkostüm.") - .2
J.append(f'tl.set("#hT0", {{ opacity: 0 }}, {F(thk)}); tl.set("#hT1", {{ opacity: 1 }}, {F(thk)});')
fly("#hT1", thk, {"y": -120, "scaleY": .8, "transformOrigin": "50% 100%"}, {"y": 0, "scaleY": 1}, .3, "back.out(2)")
cut(thk, 620, 1250, 1.45); FX += [("whoosh", thk - .1, .4, .5), ("boing", thk + .1, .45, .5)]
tst = w("s12", "ganze") - .1
cut(tst, 540, 1100, 1.0)
for k in range(len(crowd)):
    expr(f"c{k}", "neutral", "laugh", tst + .05 * k)
    J.append(f'tl.fromTo("#cr{k}", {{ y: 0 }}, {{ y: -16, duration: .14, yoyo: true, repeat: 13, ease: "sine.inOut", immediateRender: false }}, {F(tst + .05 * k)});')
tlc = w("s12", "lacht.") - .1
cam(tlc, 950, 1000, 1.6, .5, "power3.out")
count("hk", t12 + .2, 54, 97, s("s13") - t12 - .3, fmt="int")
FX += [("blips", tst, .35, 1.2)]
# s13: 23:59 – 99/100 – Trommelwirbel
t13 = s("s13")
cut(t13, 540, 780, 1.0); cam(t13 + .05, 540, 900, 1.06, 1.4, "none")
J.append(f'tl.to("#zc", {{ opacity: .45, duration: .25, yoyo: true, repeat: 15, ease: "steps(1)" }}, {F(t13)});')
FX += [("tick", t13, .2, 1.7), ("wirbel", t13 + .4, .33, 2.0)]
t99 = w("s13", "Neunundneunzig.") - .1
cut(t99, 540, 1200, 1.3)
tef = w("s13", "Einer") - .1
cut(tef, 540, 1150, 1.0); pop("#zf", tef, .25, "50% 50%"); FX += [("hit", tef, .35, .6)]
# s14: Oma Hilde mit Pilzkorb, Mia fleht
t14 = s("s14")
cut(t14, 540, 1250, 1.05)
fly("#omg", t14 + .2, {"x": 380}, {"x": 0}, .5, "back.out(1.4)"); J.append('tl.set("#omg", { x: 380 }, 0);'); FX += [("whoosh", t14 + .2, .35, .5)]
tpk = w("s14", "Pilze.") - .2
ho1 = H_(OOX, 1900, 1.55)
cut(tpk, ho1[0] - 40, 1100, 1.4)
tmf = w("s14", "Mia") - .1
hm14 = H_(OMX, 1900, 1.5)
cut(tmf, hm14[0], hm14[1] - 60, 1.55)
fly("#mig", tmf, {"x": -200}, {"x": 0}, .3, "power2.out"); J.append('tl.set("#mig", { x: -200 }, 0);')
J.append(f'tl.set("#mig", {{ x: -200 }}, {F(tmf - .02)});')
tbl = w("s14", "Bitte") - .1
pop("#bub14", tbl, .2, "50% 50%"); FX += [("boing", tbl, .4, .4)]
J.append(f'tl.fromTo("#m14-a1", {{ y: 0 }}, {{ y: -16, duration: .1, yoyo: true, repeat: 9, ease: "sine.inOut", immediateRender: false }}, {F(tbl)});')
# s15: Oma mustert Theo im Hühnerkostüm – Pause – Nein
t15 = s("s15")
hide("#bub14", t15, .05)
cut(t15, ho1[0], ho1[1] - 30, 2.0); expr("om1", "relief", "annoyed", t15)
tlg = w("s15", "lange") - .2
ht14 = H_(OTX, 1700, 1.15)
cut(tlg, OTX + 60, ht14[1] - 140, 2.2); cam(tlg + .05, OTX + 60, 1650, 2.2, 1.3, "sine.inOut"); FX += [("tick", tlg, .3, 1.3)]
expr("om1", "annoyed", "lookdown", tlg)
tnn = w("s15", "Nein.") - .15
cut(tnn, ho1[0], ho1[1] - 10, 2.3); expr("om1", "lookdown", "neutral", tnn)
wobble("#om1", tnn + .05, 3, 3, .15, "rotation", "50% 100%"); FX += [("klong", tnn, .45, .8)]
expr("t14", "worried", "shock", tnn)
# s16: Mitternacht – Glocke, Flackern, die 1 glitcht
t16 = s("s16")
cut(t16, 560, 1000, 1.12)
for k in range(2): FX += [("klong", t16 - .35 + k * .3, .2, 1.0)]
J.append(f'tl.to("#flash", {{ opacity: .7, duration: .06, yoyo: true, repeat: 5, ease: "steps(1)" }}, {F(t16)}); tl.set("#flash", {{ opacity: 0 }}, {F(t16 + .45)});')
tbb = w("s16", "bleibt.") - .2
cut(tbb, 600, 2060 - 680 * 2 + 40, 2.0)
J.append(f'tl.set("#glt", {{ opacity: 1 }}, {F(tbb)}); tl.to("#bT16-in", {{ x: 14, duration: .05, yoyo: true, repeat: 15, ease: "steps(1)" }}, {F(tbb)}); tl.set("#bT16-in", {{ x: 0 }}, {F(tbb + .82)}); tl.set("#glt", {{ opacity: 0 }}, {F(tbb + .82)});')
FX += [("glitch", tbb, .15, .6)]
tjz = w("s16", "jetzt") - .1
ht16 = H_(600, 2060, 2.0)
cut(tjz, ht16[0], ht16[1] - 20, 2.2); expr("t16", "worried", "glow", tjz); FX += [("riser", tjz, .15, 2.0)]
# s17: Schnelle Schwenks – Ben 12.000, Krause 9.000
t17 = s("s17")
cut(t17, 180, 1900 - 640 * 1.3 + 60, 1.9); FX += [("swoosh", t17, .4, .5)]
J.append(f'tl.fromTo("#bB3-in", {{ scale: 1.6, transformOrigin: "50% 50%" }}, {{ scale: 1, duration: .25, ease: "back.out(2)", immediateRender: false }}, {F(t17 + .05)});')
tkr = w("s17", "Krause:") - .15
cam(tkr, 525, 1900 - 640 * 1.3 + 60, 1.9, .22, "power3.inOut"); FX += [("swoosh", tkr, .4, .5)]
J.append(f'tl.fromTo("#bK3-in", {{ scale: 1.6, transformOrigin: "50% 50%" }}, {{ scale: 1, duration: .25, ease: "back.out(2)", immediateRender: false }}, {F(tkr + .2)});')
# s18: Harter Zoom auf Oma – ADMIN
t18 = s("s18")
cut(t18, 700, 1250, 1.2); cam(t18 + .05, 870, 1250, 1.35, .8, "power2.out"); FX += [("whoosh", t18, .15, .6)]
tad = w("s18", "Ädmin.") - .3
cam(tad, 870, 1900 - 640 * 1.45 + 40, 2.2, .18, "power4.in")
J.append(f'tl.set("#bO3", {{ opacity: 0 }}, {F(tad + .18)}); tl.set("#aO3", {{ opacity: 1 }}, {F(tad + .18)});')
J.append(f'tl.to("#vfl", {{ opacity: .45, duration: .05, yoyo: true, repeat: 3, ease: "steps(1)" }}, {F(tad + .18)}); tl.set("#vfl", {{ opacity: 0 }}, {F(tad + .4)});')
FX += [("hit", w("s18", "Ädmin.") + .72, .4, 1.4), ("glitch", w("s18", "Ädmin.") + .72, .15, .5)]; shake(tad + .2, 8, 14)
t19 = s("s19"); t20 = s("s20")
nb = int((t20 - (tad + .5)) / .3)
J.append(f'tl.to("#aO3-in", {{ opacity: .25, duration: .15, yoyo: true, repeat: {max(1, nb)}, ease: "steps(1)" }}, {F(tad + .5)});')
# s19: Oma zwinkert in die Kamera
ho3 = H_(870, 1900, 1.45)
cut(t19, ho3[0], 1000, 1.3); cam(t19 + .05, ho3[0] - 20, 1050, 1.5, 1.6, "none")
tzw = w("s19", "zwinkert:") - .25
expr("om3", "relief", "wink", tzw); armswap("om3", tzw); J.append(f'tl.set("#om3-mush", {{ opacity: 1 }}, {F(tzw)});'); FX += [("chime", tzw, .35, .8)]
# s20/s21: A/B-Split bis zum letzten Frame, ADMIN blinkt über beiden
cut(t20, 540, 1000, 1.0)
nb2 = int((END - t20) / .3) + 2
J.append(f'tl.to("#aO5-in, #aO6-in", {{ opacity: .5, duration: .15, yoyo: true, repeat: {nb2}, ease: "steps(1)" }}, {F(t20)});')
J.append(f'tl.to("#gltB", {{ x: 14, duration: .07, yoyo: true, repeat: {int((END - t20) / .07)}, ease: "steps(1)" }}, {F(t20)});')
for lab in ("A", "B"): J.append(f'tl.set("#lab{lab}", {{ opacity: 0 }}, 0);')
tA = w("s20", "A:") - .1; tB = w("s20", "B:") - .1
pop("#labA", tA, .3, "50% 50%"); pop("#labB", tB, .3, "50% 50%"); FX += [("pop", tA, .5, .3), ("pop", tB, .5, .3)]
cut(tA, 300, 1150, 1.3); cut(tB, 780, 1150, 1.3)
tsc = w("s20", "Schreib") - .1
cut(tsc, 540, 1000, 1.0)
J.append(f'tl.to("#labA", {{ scale: 1.08, duration: .2, yoyo: true, repeat: 3, transformOrigin: "50% 50%" }}, {F(tsc)}); tl.to("#labB", {{ scale: 1.08, duration: .2, yoyo: true, repeat: 3, transformOrigin: "50% 50%" }}, {F(tsc + .1)});')
t21 = s("s21")
cam(t21, 540, 1050, 1.12, .5)
tdn2 = w("s21", "Denn") - .1
cam(tdn2, 270, 1060, 1.6, .5)       # Bildschirm: Theos 1 + Mias 30.000 (Spiegel von Bild 0)
tfj = w("s21", "Fast") - .1
J.append(f'tl.set("#aO5-in, #aO6-in", {{ opacity: 1 }}, {F(END - .12)});')
cam(tfj, 540, 1000, 1.0, .35, "power3.out"); FX += [("glitch", END - .6, .12, .4)]

sets = [("A", 0, t2), ("R", t2, t3), ("C", t3, t4), ("C2", t4, t5), ("F", t5, tdu), ("C2", tdu, t6), ("C", t6, t7), ("U", t7, t8), ("D", t8, t9), ("E", t9, t10),
        ("BN", t10, t11), ("KL", t11, t12), ("H", t12, t13), ("Z", t13, t14), ("O", t14, t16), ("G", t16, t17), ("V", t17, t20), ("AB", t20, END)]

SM = lambda txt, px=46: f"<span style='font-size:{px}px'>{txt}</span>"
OBEN = [(0, SM("IN DIESER WELT:<br>DEINE ZAHL = TAGE, DIE DU NOCH HAST", 46)), (tth, "ÜBER THEO: <span style='color:#ff4d5a'>1</span>"),
        (t2, "⏪ RÜCKBLICK"), (t3, "PLAN A: RETTEN"), (t4, "PLAN B?"), (t5, "ABSICHTLICH?!"), (t6, "„DU WARST LUSTIG GENUG“"),
        (t7, SM("WER EINE <span style='color:#ff4d5a'>1</span> HAT, SIEHT UM 00:00,<br>WER DIE ZAHLEN MACHT", 44)), (tdr, "SEIT 3 JAHREN"),
        (t8, "AUSWEG: 100 LACHER"), (t9, "0/100"), (t10, "VERSUCH 1: BEN – 0/100"), (t11, "VERSUCH 2: HERR KRAUSE"), (tz, "ZÄHLT NICHT ❌"),
        (t12, "HÜHNERKOSTÜM: <span id='hk'>54</span>/100"), (t13, "<span style='color:#ff4d5a'>23:59</span> – 99/100"), (t14, "LETZTE CHANCE: OMA HILDE"),
        (t15, "…"), (tnn, "NEIN. 😐"), (t16, "00:00"), (t17, "BEN: 12.000 | KRAUSE: 9.000"), (t18, "ÜBER OMA HILDE: ???"),
        (tad + .18, "<span style='color:#39ff14'>ADMIN</span>"), (t19, SM("„HÄTTEST DU MAL<br>NICHT GELACHT.“", 54)),
        (t20, "SCHREIB A ODER B! 👇"), (t21, "FINALE MORGEN – TEIL 5")]
tag = ('<div class="ui clip" data-start="0" data-duration="{0}" style="left:30px;top:40px;font:900 34px Inter,sans-serif;color:#fff;background:rgba(0,0,0,.55);padding:6px 16px;border-radius:12px">DIE ZAHL ÜBER DEM KOPF · TEIL 4</div>').format(F(END))
HOT = {"1", "EINE", "EINS", "THEO", "MIA", "RETTE", "NEIN", "ABSICHTLICH", "WAS", "MITTERNACHT", "ZAHLEN", "100", "LACHER", "LUSTIG", "BEN", "BAGUETTE",
       "KRAUSE", "HÜHNERKOSTÜM", "LACHT", "NEIN", "OMA", "HILDE", "ADMIN", "GELACHT", "A", "B", "FINALE", "FAST", "JEDER"}
finish(S, sets, OBEN, FX, HOT, tag, banner=("<span style='font-size:62px;-webkit-text-stroke:0;text-shadow:0 4px 0 #111'>TEIL 5 – FINALE MORGEN</span><br>", "➕ FOLGEN"), oben_top=110, banner_top=300)
