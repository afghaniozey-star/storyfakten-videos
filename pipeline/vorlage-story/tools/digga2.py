"""STORY-FORMAT „In dieser Stadt …“ – Serie „Digga-Stadt“, TEIL 2: „3.850 Digga“ (Gesetz „Alter verboten“, Ohrwurm, Stadtbuch).
Aufruf: /usr/bin/python3 tools/digga2.py  (liest voice.json + assets/vo/timing.json; Bausteine aus tools/bausteine.py;
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


# ---------- Teil 2: Figuren-Varianten + neue Requisiten ----------
JONAS_EX = ("happy", "angry", "shock", "laugh", "confused", "panic", "neutral", "determined", "grin", "relief")
def jonas(uid, start="happy", shirt="#e63946", arm=("down", "down"), arm2=None, extra=""):
    return person(uid, "jonas", "#f4d35e", shirt, exprs=JONAS_EX, start=start, arm=arm, arm2=arm2, extra=extra)
def krause(uid, start="neutral", arm=("down", "front"), exprs=("neutral", "shock", "confused", "laugh", "happy"), extra=""):
    return person(uid, "glatze", "#555", "#6c757d", exprs=exprs, start=start, arm=arm, head_acc=KR_ACC, extra=extra)
SOCKPULLI = "#80ed99"
STRIPES = '<path d="M-98 -250 H98 M-98 -190 H98 M-98 -130 H98" stroke="#38b000" stroke-width="12"/>'
def oma(uid, start="happy", arm=("up", "up"), exprs=("happy", "laugh", "shock", "grin", "wink")):
    return person(uid, "oma", "#e0e0e0", SOCKPULLI, exprs=exprs, start=start, arm=arm, head_acc=OMA_ACC, extra=STRIPES)
def tiny(uid, k, ex="happy", arm=("up", "up")):
    hair = ("mann", "lena", "oma", "ich", "cap", "beanie")[k % 6]
    hc = ("#3d2b1f", "#f4d35e", "#ddd", "#111", "#7b2cbf", "#2d6a4f")[k % 6]
    sh = ("#e76f51", "#3a86ff", "#9d4edd", "#06d6a0", "#ffbe0b", "#ef476f")[k % 6]
    return person(uid, hair, hc, sh, skin=("#f2c9a5", "#c68642", "#8d5524")[k % 3], exprs=(ex,), start=ex, arm=arm)
def txt(x, y, s, size=60, col="#111", anchor="middle", extra=""):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" style="font:900 {size}px {FONT};fill:{col}" {extra}>{s}</text>'
def sign(uid, x, y, wd, h, lines, col="#fff", fg="#111", size=70, vis=True, rot=0):
    t = "".join(txt(0, -h / 2 + 30 + (k + .85) * size * 1.15 - 10, l, size, fg) for k, l in enumerate(lines))
    return (f'<g id="{uid}" opacity="{1 if vis else 0}" transform="translate({x} {y}) rotate({rot})"><g id="{uid}-in"><rect x="{-wd/2 + 8}" y="{-h/2 + 8}" width="{wd}" height="{h}" rx="26" fill="#000" opacity=".25"/>'
            f'<rect x="{-wd/2}" y="{-h/2}" width="{wd}" height="{h}" rx="26" fill="{col}" stroke="#111" stroke-width="8"/>{t}</g></g>')
def teacup(uid, x, y, s=1.0, inner=""):
    return (f'<g id="{uid}" transform="translate({x} {y}) scale({s})"><ellipse cx="0" cy="10" rx="230" ry="40" fill="#fff" stroke="#111" stroke-width="7"/>'
            f'{inner}'
            '<path d="M-170 -170 H170 L140 0 Q0 40 -140 0 Z" fill="#fff" stroke="#111" stroke-width="8"/><path d="M-160 -120 H160" stroke="#e63946" stroke-width="14"/>'
            '<path d="M168 -140 Q260 -130 240 -60 Q220 -10 150 -30" stroke="#111" stroke-width="30" fill="none"/><path d="M168 -140 Q260 -130 240 -60 Q220 -10 150 -30" stroke="#fff" stroke-width="16" fill="none"/>'
            '<g transform="translate(110 -170)"><rect x="-10" y="-210" width="30" height="210" fill="#ff006e" stroke="#111" stroke-width="5"/><rect x="-10" y="-210" width="30" height="40" fill="#fff" opacity=".6"/></g>'
            '<g opacity=".7"><rect x="100" y="-470" width="50" height="50" rx="25" fill="#ddd"/><rect x="130" y="-540" width="70" height="70" rx="35" fill="#eee"/></g></g>')
def chalkbox(uid, x, y, s=1.0, inner=""):
    return (f'<g id="{uid}" transform="translate({x} {y}) scale({s})">{inner}<rect x="-160" y="-170" width="320" height="170" rx="10" fill="#4361ee" stroke="#111" stroke-width="8"/>'
            f'<rect x="-160" y="-170" width="320" height="40" fill="#fff" opacity=".35"/>{txt(0, -60, "KREIDE", 62, "#fff")}</g>')
def matchbox(uid, x, y, s=1.0, inner=""):
    return (f'<g id="{uid}" transform="translate({x} {y}) scale({s})">{inner}<rect x="-220" y="-150" width="440" height="150" rx="8" fill="#f4a261" stroke="#111" stroke-width="8"/>'
            f'<rect x="-190" y="-130" width="380" height="110" fill="#e63946" stroke="#111" stroke-width="5"/>{txt(0, -55, "ZÜNDHÖLZER", 46, "#fff")}</g>')
def pigeon(uid, x, y, s=1.0, scrap=False):
    sc = '<g id="scrapb" opacity="0"><rect x="-480" y="-380" width="120" height="80" fill="#f1e3c4" stroke="#111" stroke-width="5" transform="rotate(-15 -420 -340)"/></g>' if scrap else ""
    return (f'<g id="{uid}" transform="translate({x} {y}) scale({s})"><g id="{uid}-in"><rect x="-230" y="-260" width="460" height="300" rx="140" fill="#adb5bd" stroke="#111" stroke-width="8"/><rect x="-330" y="-480" width="230" height="230" rx="80" fill="#8d99ae" stroke="#111" stroke-width="8"/>'
            '<rect x="-300" y="-300" width="170" height="60" rx="20" fill="#7b2cbf" opacity=".5"/>' + WEYE(-250, -400, -8, 0) + '<path d="M-330 -380 L-420 -350 L-330 -330 Z" fill="#fb8500" stroke="#111" stroke-width="5"/>'
            f'{sc}<rect x="100" y="-240" width="220" height="80" rx="30" fill="#6c757d" stroke="#111" stroke-width="6"/><path d="M-60 40 V120 M60 40 V120" stroke="#fb8500" stroke-width="16"/></g></g>')
def rapper(uid, hair, col, shirt):
    return person(uid, hair, col, shirt, exprs=("determined", "laugh"), start="determined", arm=("mic", "up"),
                  extra='<g transform="translate(74 -300)"><rect x="-14" y="-10" width="28" height="90" rx="8" fill="#333"/><rect x="-26" y="-60" width="52" height="56" rx="20" fill="#888" stroke="#111" stroke-width="4"/></g>'
                        '<path d="M-60 -290 Q0 -200 60 -290" stroke="#ffd166" stroke-width="14" fill="none"/>')
def ant_head(x, y, s):  # Fühler über Klötzchen-Kopf
    return f'<path d="M{x - 40 * s} {y - 90 * s} L{x - 80 * s} {y - 170 * s} M{x + 40 * s} {y - 90 * s} L{x + 80 * s} {y - 170 * s}" stroke="#111" stroke-width="{8 * s}" stroke-linecap="round"/>'
def notes(uid, x, y, n=4, col="#7b2cbf"):
    return (f'<g id="{uid}" opacity="0">' + "".join(f'<g transform="translate({x + (k % 2) * 160 - 80} {y - k * 110}) rotate({(-1) ** k * 12})"><rect x="0" y="-70" width="12" height="80" fill="{col}"/><rect x="-34" y="0" width="46" height="34" rx="16" fill="{col}" stroke="#111" stroke-width="3"/><path d="M12 -70 L50 -50 V-30 L12 -50 Z" fill="{col}"/></g>' for k in range(n)) + '</g>')
def mini_rathaus(x, y, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s})"><rect x="-140" y="-200" width="280" height="200" fill="#f8f9fa" stroke="#111" stroke-width="7"/><path d="M-160 -196 L0 -300 L160 -196 Z" fill="#ced4da" stroke="#111" stroke-width="7"/>'
            + "".join(f'<rect x="{-110 + k * 80}" y="-160" width="50" height="70" fill="#bde0fe" stroke="#111" stroke-width="4"/>' for k in range(3)) +
            f'<rect x="-30" y="-80" width="60" height="80" fill="#6b4226" stroke="#111" stroke-width="5"/>{txt(0, -212, "RATHAUS", 34)}</g>')
def ruler_v(uid, x, y0, y1, label, wd=110):
    n = int((y0 - y1) / 60)
    return (f'<g id="{uid}"><rect x="{x}" y="{y1}" width="{wd}" height="{y0 - y1}" fill="#ffd166" stroke="#111" stroke-width="7"/>' +
            "".join(f'<rect x="{x}" y="{y0 - k * 60}" width="{40 if k % 2 else 70}" height="7" fill="#111"/>' for k in range(1, n)) +
            f'<rect x="{x - 40}" y="{y1 - 100}" width="{wd + 80}" height="96" rx="22" fill="#111"/>{txt(x + wd / 2, y1 - 30, label, 64, "#ffd166")}</g>')
def confetti(uid, n=40, y0=200):
    cols = ("#e63946", "#ffd166", "#06d6a0", "#118ab2", "#ef476f", "#8338ec")
    return f'<g id="{uid}" opacity="0">' + "".join(f'<rect class="cf" x="{(k * 97) % 1060}" y="{y0 + (k * 53) % 500}" width="22" height="36" fill="{cols[k % 6]}" transform="rotate({k * 37 % 90} {(k * 97) % 1060} {y0 + (k * 53) % 500})"/>' for k in range(n)) + '</g>'
SEPIA = '<filter id="sepia"><feColorMatrix type="matrix" values=".39 .77 .19 0 0 .35 .69 .17 0 0 .27 .53 .13 0 0 0 0 0 1 0"/></filter>'

S = {}; FX = []
# --- N2 (s1, Hook): Riesen-Jonas neben dem Mini-Rathaus, ich winzig am Schnürsenkel, Messlatte 40 M
JGX, JGFY, JGS = 560, 1890, 3.55
S["N2"] = ('<rect width="1080" height="1920" fill="#a2d2ff"/>' +
           "".join(f'<rect x="{x}" y="{y}" width="{w_}" height="70" rx="35" fill="#fff" opacity=".9"/>' for x, y, w_ in ((60, 260, 220), (760, 420, 260), (120, 760, 180))) +
           '<rect y="1820" width="1080" height="100" fill="#6c757d"/>' +
           fig(jonas("jg1", "laugh", arm=("hip", "up")), JGX, JGFY, JGS) +
           '<path d="M500 1872 q-30 30 -60 10 M620 1872 q30 30 60 10" stroke="#fff" stroke-width="8" fill="none"/>' +
           mini_rathaus(170, 1890, .95) +
           fig(person("ichA", "ich", "#6b3e26", "#118ab2", exprs=("shock",), start="shock", arm=("up", "up")), 420, 1890, .16) +
           f'<g id="ichlab" transform="translate(420 1700)"><rect x="-88" y="-40" width="176" height="56" rx="16" fill="#fff" stroke="#111" stroke-width="5"/>{txt(0, 2, "ICH", 40)}</g>' +
           ruler_v("rul1", 930, 1890, 520, "40 M"))
# --- RB (s2): Rückblende sepia – Jonas brüllt ALTER und wächst durchs Dach
S["RB"] = (f'<defs>{SEPIA}</defs><g filter="url(#sepia)">' + street_bg() +
           wrap("jrb", jonas("jr1", "angry", arm=("up", "up")), 540, 1300, .9) +
           '<g><rect x="300" y="1020" width="480" height="300" fill="#e9c46a" stroke="#111" stroke-width="7"/><path d="M280 1030 L540 900 L800 1030 Z" fill="#9c4f1f" stroke="#111" stroke-width="7"/>'
           '<rect x="490" y="1180" width="100" height="140" fill="#6b4226" stroke="#111" stroke-width="5"/></g>' +
           bubble("bubrb", ["ALTER!", "ALTER!"], 760, 600, 400, tail=(-1, 1), size=80) + puff("pfrb", 540, 920, 90) + '</g>'
           f'<rect x="330" y="1640" width="420" height="90" rx="20" fill="#000" opacity=".6"/>{txt(540, 1705, "RÜCKBLENDE", 56, "#f1e3c4")}')
# --- SL (s3): Schulhof mit Riesen-Strichliste (Vogelperspektive)
tally = ""
for k in range(24):
    gx, gy = 70 + (k % 4) * 240, 360 + (k // 4) * 240
    tally += f'<g id="tl{k}" opacity="0">' + "".join(f'<rect x="{gx + j * 36}" y="{gy}" width="14" height="150" rx="6" fill="#fff"/>' for j in range(4)) + f'<path d="M{gx - 14} {gy + 120} L{gx + 140} {gy + 30}" stroke="#fff" stroke-width="14" stroke-linecap="round"/></g>'
S["SL"] = ('<rect width="1080" height="1920" fill="#8d99ae"/>' + "".join(f'<rect x="0" y="{k * 160}" width="1080" height="4" fill="#000" opacity=".06"/>' for k in range(12)) +
           tally + '<g transform="translate(860 1720)"><rect x="-260" y="-60" width="520" height="300" rx="40" fill="#e63946" stroke="#111" stroke-width="9"/><rect x="-220" y="-160" width="180" height="120" rx="30" fill="#e63946" stroke="#111" stroke-width="8"/></g>'
           f'{txt(860, 1800, "JONAS´", 48, "#fff")}{txt(860, 1860, "SCHUH", 48, "#fff")}' +
           sign("s3850", 520, 980, 560, 180, ["3.850 DIGGA"], col="#111", fg="#ffd166", size=86) +
           f'<g transform="translate(160 1720) scale(1.4)">' + f'<rect x="-96" y="-96" width="192" height="192" rx="26" fill="#f2c9a5" stroke="#111" stroke-width="5"/>{HAIR["jonas"]("#f4d35e")}<g>{FACES["shock"]}</g></g>')
# --- KZ (s4): Krause, nur die Augen über dem Pult, Tafel 3.850 s = 64 min
S["KZ"] = (room_bg("#e9f5db", "#b08968", win=False) + '<rect x="70" y="250" width="940" height="460" rx="16" fill="#2d6a4f" stroke="#6b4226" stroke-width="18"/>' +
           txt(540, 420, "3.850 s", 110, "#fff") + txt(540, 580, "= 64 min", 110, "#ffd166") +
           wrap("kzz", krause("kr1", "confused", arm=("down", "down")), 540, 1900, 1.15) +
           '<g id="chalk2"><rect x="780" y="260" width="60" height="26" rx="8" fill="#fff" stroke="#111" stroke-width="4"/></g>'
           '<rect x="160" y="1470" width="760" height="70" rx="10" fill="#8d5524" stroke="#111" stroke-width="7"/><rect x="190" y="1540" width="700" height="380" fill="#a0522d" stroke="#111" stroke-width="7"/>' +
           txt(540, 1760, "HERR KRAUSE", 58, "#ffd166"))
# --- TOT (s5): Riesen-Jonas über der Stadt – Digga, Digga, Digga, Wolken fliegen weg
skyline = "".join(f'<rect x="{x}" y="{1920 - h}" width="{wd}" height="{h}" fill="{c}" stroke="#111" stroke-width="5"/>' + "".join(f'<rect x="{x + 16 + (j % 2) * (wd / 2 - 8)}" y="{1920 - h + 20 + (j // 2) * 60}" width="24" height="30" fill="#fff8d6"/>' for j in range(int(h / 60) * 2 - 1))
                  for x, h, wd, c in ((0, 260, 140, "#f4a261"), (150, 360, 120, "#a8dadc"), (280, 220, 150, "#e9c46a"), (640, 300, 130, "#cdb4db"), (780, 400, 120, "#f6bd60"), (910, 250, 170, "#90be6d")))
S["TOT"] = ('<rect width="1080" height="1920" fill="#a2d2ff"/>' +
            '<g id="clouds">' + "".join(f'<g transform="translate({x} {y})"><rect x="-120" y="-40" width="240" height="80" rx="40" fill="#fff"/><rect x="-60" y="-80" width="120" height="80" rx="40" fill="#fff"/></g>' for x, y in ((180, 300), (880, 260), (130, 700), (950, 640))) + '</g>' +
            wrap("jtot", jonas("jt1", "determined", arm=("hip", "hip")), 540, 2350, 3.2) + skyline +
            bubble("bubt1", ["DIGGA!"], 290, 560, 360, tail=(1, 1), size=80) + bubble("bubt2", ["DIGGA!"], 780, 500, 360, tail=(-1, 1), size=80) + bubble("bubt3", ["DIGGA!"], 540, 360, 380, tail=(0, 1), size=90))
# --- BM (s6): Mini-Bürgermeister in der Streichholzschachtel mit Mega-Mikro, Stempel VERBOTEN
S["BM"] = ('<rect width="1080" height="1920" fill="#dde5b6"/>' + "".join(f'<rect x="{90 + k * 230}" y="200" width="80" height="1000" fill="#e9ecef" stroke="#111" stroke-width="5"/>' for k in range(5)) +
           '<rect y="1200" width="1080" height="720" fill="#9d0208"/><rect x="0" y="1300" width="1080" height="10" fill="#000" opacity=".2"/>' +
           matchbox("mbx", 260, 1720, 1.6, inner=fig(bgm_("bm1", "determined", arm=("down", "up")), 0, -60, .55)) +
           '<g transform="translate(400 1400)"><path d="M0 0 L60 -260" stroke="#333" stroke-width="16"/><rect x="20" y="-420" width="110" height="170" rx="50" fill="#555" stroke="#111" stroke-width="7"/><path d="M30 -380 H120 M30 -340 H120 M30 -300 H120" stroke="#888" stroke-width="6"/></g>' +
           sign("salt", 840, 900, 360, 200, ["ALTER"], size=100) +
           f'<g id="stamp" opacity="0" transform="translate(840 900) rotate(-14)"><rect x="-200" y="-70" width="400" height="140" rx="16" fill="none" stroke="#e63946" stroke-width="14"/>{txt(0, 34, "VERBOTEN", 86, "#e63946")}</g>'
           f'<g id="stmp" transform="translate(840 400)"><rect x="-40" y="-200" width="80" height="160" rx="20" fill="#6b4226" stroke="#111" stroke-width="6"/><rect x="-130" y="-50" width="260" height="70" rx="12" fill="#333" stroke="#111" stroke-width="6"/></g>')
# --- OM (s7): Sockengroße Oma im Sockenpulli auf dem Küchentisch, Plopp -> Teetasse
S["OM"] = (room_bg("#ffd6a5", "#9c6644") + '<rect x="0" y="1260" width="1080" height="660" fill="#e76f51"/>' + "".join(f'<rect x="{k * 120}" y="1260" width="60" height="660" fill="#fff" opacity=".18"/>' for k in range(9)) +
           '<g transform="translate(250 1500)"><rect x="-80" y="-360" width="160" height="300" rx="40" fill="#80ed99" stroke="#111" stroke-width="7"/><path d="M-80 -60 H120 Q160 -60 160 -20 V20 H-80 Z" fill="#80ed99" stroke="#111" stroke-width="7"/>'
           '<path d="M-80 -300 H80 M-80 -240 H80 M-80 -180 H80" stroke="#38b000" stroke-width="10"/>' + txt(0, -400, "SOCKE", 40) + '</g>' +
           wrap("omz", oma("om1", "happy", arm=("up", "up")) + '<g transform="translate(150 -470)"><rect x="-36" y="-36" width="72" height="72" rx="36" fill="#ff006e" stroke="#111" stroke-width="5"/></g>'
                + '<g transform="translate(-150 -470)"><rect x="-36" y="-36" width="72" height="72" rx="36" fill="#ffd166" stroke="#111" stroke-width="5"/></g>', 520, 1420, .62) +
           bubble("bubom", ["KOMM SCHON,", "DIGGA!"], 560, 640, 520, tail=(0, 1), size=66) + puff("pfom", 520, 1220, 80) +
           teacup("cup1", 850, 1640, .95, inner='<g id="cupoma" opacity="0">' + fig(oma("om2", "grin", arm=("up", "up")), 0, -150, .32) + '</g>'))
# --- AR (s8): Ameisen-Rapper auf Kronkorken-Bühne, Taube nickt
cap_ = ('<g transform="translate(540 1500)"><path d="' + " ".join(f'{"M" if k == 0 else "L"}{(380 if k % 2 == 0 else 350) * __import__("math").cos(k * 3.14159 / 18):.0f} {(380 if k % 2 == 0 else 350) * __import__("math").sin(k * 3.14159 / 18) * .28:.0f}' for k in range(36)) + ' Z" fill="#c1121f" stroke="#111" stroke-width="7"/>'
        '<ellipse cx="0" cy="-8" rx="300" ry="78" fill="#e63946" stroke="#111" stroke-width="5"/>' + txt(0, 10, "KRONKORKEN-BÜHNE", 40, "#fff") + '</g>')
grass = "".join(f'<path d="M{x} 1920 Q{x + 30} {1500 - (x * 7) % 300} {x + 60 + (x % 3) * 20} {1300 - (x * 13) % 400}" stroke="{("#2d6a4f", "#40916c", "#52b788")[x % 3]}" stroke-width="40" fill="none" stroke-linecap="round"/>' for x in range(-20, 1100, 90))
S["AR"] = ('<rect width="1080" height="1920" fill="#b7e4c7"/>' + grass + cap_ +
           wrap("ar1", rapper("ra1", "cap", "#7b2cbf", "#9d4edd") + ant_head(0, -400, 1), 390, 1470, .62) +
           wrap("ar2", rapper("ra2", "beanie", "#2d6a4f", "#06d6a0") + ant_head(0, -400, 1), 690, 1470, .62) +
           '<g transform="translate(150 1640)"><rect x="-90" y="-180" width="180" height="200" rx="16" fill="#222" stroke="#111" stroke-width="6"/><g id="spk1"><rect x="-60" y="-150" width="120" height="120" rx="60" fill="#555" stroke="#111" stroke-width="5"/><rect x="-26" y="-116" width="52" height="52" rx="26" fill="#111"/></g></g>'
           '<g transform="translate(930 1640)"><rect x="-90" y="-180" width="180" height="200" rx="16" fill="#222" stroke="#111" stroke-width="6"/><g id="spk2"><rect x="-60" y="-150" width="120" height="120" rx="60" fill="#555" stroke="#111" stroke-width="5"/><rect x="-26" y="-116" width="52" height="52" rx="26" fill="#111"/></g></g>' +
           pigeon("pig1", 1010, 1000, .85) + notes("nt1", 540, 1000, 4))
# --- KRAN (s9): Jonas singt und schrumpft im Beat auf Baukran-Höhe
CRANE = ('<g transform="translate(860 1820)"><path d="M-40 0 V-1100 M40 0 V-1100" stroke="#ffbe0b" stroke-width="22"/>' + "".join(f'<path d="M-40 {-k * 100} L40 {-(k + 1) * 100} M40 {-k * 100} L-40 {-(k + 1) * 100}" stroke="#ffbe0b" stroke-width="10"/>' for k in range(11)) +
         '<rect x="-560" y="-1150" width="760" height="50" fill="#ffbe0b" stroke="#111" stroke-width="6"/><path d="M-500 -1100 V-900" stroke="#333" stroke-width="6"/><rect x="-540" y="-900" width="80" height="60" fill="#555" stroke="#111" stroke-width="5"/>'
         '<rect x="-80" y="-1240" width="160" height="90" fill="#e63946" stroke="#111" stroke-width="6"/></g>')
S["KRAN"] = ('<rect width="1080" height="1920" fill="#a2d2ff"/>' + CRANE + '<line id="kranl" x1="0" y1="670" x2="1080" y2="670" stroke="#e63946" stroke-width="8" stroke-dasharray="30 18"/>' + txt(20, 650, "BAUKRAN", 44, "#e63946", "start") +
             wrap("jkr", jonas("jk1", "laugh", arm=("up", "mic")), 420, 1880, 3.4) + skyline.replace('fill="#fff8d6"', 'fill="#ffe8a3"') + notes("nt2", 300, 600, 4, "#e63946") +
             sign("s50", 780, 520, 300, 150, ["50 %"], col="#ffd166", size=100, vis=False))
# --- EAR (s10a): Riesen-Ohr, Ohrwurm mit Kopfhörern
S["EAR"] = ('<rect width="1080" height="1920" fill="#f2c9a5"/><path d="M300 300 Q900 200 900 900 Q900 1300 650 1500 Q560 1580 600 1700 Q560 1820 420 1760 Q300 1700 380 1500 Q480 1320 420 1200" fill="#e8b48f" stroke="#111" stroke-width="12"/>'
            '<path d="M420 500 Q760 440 760 880 Q760 1100 600 1220" stroke="#c98a65" stroke-width="40" fill="none"/><ellipse cx="560" cy="980" rx="110" ry="150" fill="#5a2a1a"/>' +
            '<g id="worm" transform="translate(560 980)"><g id="worm-in"><path d="M0 0 Q80 -160 220 -140 Q340 -120 340 -260" stroke="#ff8fab" stroke-width="80" fill="none" stroke-linecap="round"/>'
            '<rect x="280" y="-360" width="130" height="120" rx="40" fill="#ff8fab" stroke="#111" stroke-width="6"/>' + E(320, -310, 10) + E(370, -310, 10) +
            '<path d="M318 -280 Q345 -262 372 -280" stroke="#111" stroke-width="5" fill="none"/><path d="M270 -320 Q345 -440 420 -320" stroke="#111" stroke-width="14" fill="none"/><rect x="250" y="-330" width="40" height="70" rx="14" fill="#3a86ff" stroke="#111" stroke-width="5"/><rect x="400" y="-330" width="40" height="70" rx="14" fill="#3a86ff" stroke="#111" stroke-width="5"/></g></g>' +
            notes("nt3", 880, 700, 3, "#7b2cbf"))
# --- SING (s10b): Ganze Straße singt
singers = "".join(fig(tiny(f"sg{k}", k, "laugh", arm=("up", "up") if k % 2 else ("mic", "up")), 120 + k * 210, 1700 + (k % 2) * 80, .85 if k % 2 else .75) for k in range(5))
S["SING"] = (street_bg() + singers + notes("nt4", 300, 500, 4, "#e63946") + notes("nt5", 820, 520, 4, "#7b2cbf"))
# --- BAK / POOL / KL (s11): Bäckerin, Schwimmbad, Matheunterricht
S["BAK"] = (room_bg("#fefae0", "#dda15e", win=False) + '<rect x="0" y="1300" width="1080" height="160" fill="#bc6c25" stroke="#111" stroke-width="7"/>' + txt(540, 400, "BÄCKEREI", 110, "#bc6c25") +
            fig(person("bk1", "lena", "#6b3e26", "#fff", skin="#c68642", exprs=("laugh",), start="laugh", arm=("mic", "up"),
                       extra='<g transform="translate(74 -300)"><rect x="-60" y="-50" width="120" height="70" rx="35" fill="#e9c46a" stroke="#111" stroke-width="5"/><path d="M-30 -40 V10 M0 -45 V15 M30 -40 V10" stroke="#bc6c25" stroke-width="5"/></g>'), 540, 1660, 1.5) +
            "".join(f'<rect x="{80 + k * 170}" y="1330" width="130" height="80" rx="40" fill="#e9c46a" stroke="#111" stroke-width="5"/>' for k in range(6)) + puff("pfb", 880, 800, 70) + notes("nt6", 860, 700, 3))
S["POOL"] = ('<rect width="1080" height="1920" fill="#caf0f8"/><rect y="900" width="1080" height="1020" fill="#48cae4"/>' + "".join(f'<path d="M0 {950 + k * 140} Q270 {910 + k * 140} 540 {950 + k * 140} T1080 {950 + k * 140}" stroke="#fff" stroke-width="8" fill="none" opacity=".6"/>' for k in range(7)) +
             "".join(f'<g transform="translate({x} 1060)"><rect x="-96" y="-192" width="192" height="192" rx="26" fill="#f2c9a5" stroke="#111" stroke-width="5"/>{HAIR["mann"](c).replace("<path", "<path transform=\"translate(0 -96)\"", 1)}<g transform="translate(0 -96)">{FACES["laugh"]}</g></g>' for x, c in ((260, "#111"), (780, "#f4d35e"))) +
             "".join(f'<rect x="{x}" y="{y}" width="{r}" height="{r}" rx="{r / 2}" fill="#fff" stroke="#0096c7" stroke-width="4"/>' for x, y, r in ((330, 820, 40), (360, 740, 30), (850, 800, 44), (880, 700, 28), (300, 650, 24))) +
             '<rect y="1060" width="1080" height="860" fill="#48cae4" opacity=".75"/>' + notes("nt7", 540, 700, 3, "#023e8a") + puff("pfp", 540, 1400, 70) + txt(540, 360, "SCHWIMMBAD", 100, "#0077b6"))
S["KL"] = (room_bg("#e9f5db", "#b08968", win=False) + '<rect x="90" y="250" width="900" height="380" rx="16" fill="#2d6a4f" stroke="#6b4226" stroke-width="18"/>' + txt(540, 470, "MATHE: 7 × 8 = ?", 90, "#fff") +
           "".join(fig(tiny(f"kl{k}", k + 2, "laugh", arm=("up", "up")), 180 + k * 240, 1500, .95) for k in range(4)) +
           "".join(f'<rect x="{80 + k * 240}" y="1450" width="200" height="60" rx="8" fill="#8d5524" stroke="#111" stroke-width="5"/><rect x="{100 + k * 240}" y="1510" width="20" height="300" fill="#6b4226"/><rect x="{240 + k * 240}" y="1510" width="20" height="300" fill="#6b4226"/>' for k in range(4)) +
           notes("nt8", 540, 1000, 3, "#e63946") + puff("pfk", 220, 900, 70))
# --- KR2 (s12): Krause singt die zweite Stimme – Plopp – Kreideschachtel
S["KR2"] = (room_bg("#e9f5db", "#b08968", win=False) + '<rect x="90" y="250" width="900" height="380" rx="16" fill="#2d6a4f" stroke="#6b4226" stroke-width="18"/>' + txt(540, 470, "2. STIMME 🎶", 96, "#ffd166") +
            wrap("krz", krause("kr2", "laugh", arm=("front", "up")), 400, 1700, 1.45) +
            '<rect x="640" y="1500" width="420" height="40" rx="10" fill="#6b4226" stroke="#111" stroke-width="5"/><rect x="820" y="1540" width="40" height="380" fill="#6b4226" stroke="#111" stroke-width="5"/>' +
            chalkbox("cbx", 850, 1500, .85, inner='<g id="cbk" opacity="0">' + fig(krause("kr3", "happy", arm=("down", "up"), exprs=("happy",)), 0, -100, .3) + '</g>') +
            puff("pfkr", 400, 1100, 100) + notes("nt9", 720, 900, 3, "#7b2cbf"))
# --- ICH (s13): Ich halte mir den Mund zu, Füße wippen, Messlatte rutscht
S["ICH"] = (street_bg() + ruler_v("rul2", 860, 1920, 420, "ICH") +
            '<g id="mark" transform="translate(0 0)"><path d="M800 760 L860 790 L800 820 Z" fill="#e63946" stroke="#111" stroke-width="4"/></g>' +
            wrap("ichz", person("ich1", "ich", "#6b3e26", "#118ab2", exprs=("shock", "panic", "smug"), start="shock", arm=("mic", "down"), head_acc=MONO, extra=BOW), 430, 1700, 1.85) +
            sign("sicm", 300, 760, 400, 140, ["-30 CM"], col="#e63946", fg="#fff", size=90, vis=False))
# --- J100 (s14): 100 % – Jonas wieder normal, Konfetti
S["J100"] = (street_bg() + fig(jonas("jn1", "laugh", arm=("up", "up")), 540, 1750, 1.75) + cm_badge("b150", "1,50 M ✅", y=-640, size=80, vis=False).replace('<g id="b150"', '<g transform="translate(540 1750) scale(1.75)"><g id="b150"', 1) + '</g>' + confetti("conf1"))
# --- GB (s15): Alle anderen gummibärchengroß um Jonas´ Turnschuhe
gummies = "".join(f'<g transform="translate({x} {y}) scale(.9)"><rect x="-30" y="-80" width="60" height="80" rx="24" fill="{c}" stroke="#111" stroke-width="4" opacity=".9"/><rect x="-24" y="-112" width="48" height="40" rx="18" fill="{c}" stroke="#111" stroke-width="4" opacity=".9"/></g>'
                  for x, y, c in ((140, 1760, "#e63946"), (960, 1800, "#ffbe0b"), (880, 1640, "#06d6a0")))
tinies = "".join(fig(tiny(f"tn{k}", k, "panic" if k % 2 else "shock", arm=("up", "up")), 90 + (k * 137) % 900, 1650 + (k * 71) % 240, .16) for k in range(12))
S["GB"] = ('<rect width="1080" height="1920" fill="#adb5bd"/>' + "".join(f'<rect x="{k * 180}" y="0" width="4" height="1920" fill="#000" opacity=".08"/>' for k in range(7)) +
           fig(jonas("jg2", "confused", arm=("hip", "hip")), 540, 1620, 2.6) + tinies + gummies +
           f'<g transform="translate(150 1500)"><rect x="-110" y="-46" width="220" height="80" rx="20" fill="#fff" stroke="#111" stroke-width="5"/>{txt(0, 14, "= 🐻", 48)}</g>')
# --- BM2 (s16): Mini-Bürgermeister schwitzt, Schild größer als er
S["BM2"] = ('<rect width="1080" height="1920" fill="#dde5b6"/><rect y="1300" width="1080" height="620" fill="#9d0208"/>' +
            sign("salt2", 600, 800, 640, 420, ["ALTER", "❌ VERBOTEN"], size=110) +
            '<rect x="580" y="1010" width="40" height="560" fill="#8d5524" stroke="#111" stroke-width="5"/>' +
            fig(bgm_("bm2", "shock", arm=("down", "up")), 470, 1600, .62) +
            '<g id="sweat" opacity="0"><path d="M545 1260 q-16 34 0 46 q16 -12 0 -46" fill="#4cc9f0" stroke="#111" stroke-width="3"/><path d="M395 1250 q-14 30 0 40 q14 -10 0 -40" fill="#4cc9f0" stroke="#111" stroke-width="3"/></g>')
# --- SK (s17): Jonas trägt die Stadt im Schuhkarton (seitliche Fahrt)
BOX = lambda uid, inner="": (f'<g id="{uid}"><rect x="-300" y="-230" width="600" height="230" rx="10" fill="#f4a261" stroke="#111" stroke-width="8"/>{inner}'
                             f'<rect x="-300" y="-120" width="600" height="120" fill="#e76f51" stroke="#111" stroke-width="8"/>{txt(0, -40, "STADT", 56, "#fff")}</g>')
box_inner = ('<g transform="translate(-200 -110)">' + teacup("cupS", 0, 0, .3, inner=fig(oma("om3", "happy", exprs=("happy",)), 0, -40, .3)) + '</g>' +
             '<g transform="translate(0 -110)">' + chalkbox("cbS", 0, 0, .3, inner=fig(krause("kr4", "happy", exprs=("happy",)), 0, -100, .3)) + '</g>' +
             "".join(fig(tiny(f"bx{k}", k, "happy", arm=("up", "down")), 120 + k * 70, -100, .16) for k in range(3)))
S["SK"] = ('<rect width="1080" height="1920" fill="#a2d2ff"/><g id="skbg">' + street_bg().replace('<rect width="1080" height="1920" fill="#8ecae6"/>', '') + '<g transform="translate(1080 0)">' + street_bg().replace('<rect width="1080" height="1920" fill="#8ecae6"/>', '') + '</g></g>' +
           wrap("jsk", jonas("js1", "neutral", arm=("front", "front")) + f'<g transform="translate(0 -150) scale(.62)">{BOX("box1", box_inner)}</g>', 540, 1830, 1.75))
# --- BUCH (s18/s19): Uraltes Stadtbuch (Top-Shot), Bürgermeister rennt über die Seite
S["BUCH"] = ('<rect width="1080" height="1920" fill="#3d2b1f"/>' + "".join(f'<rect x="0" y="{k * 120}" width="1080" height="6" fill="#000" opacity=".2"/>' for k in range(16)) +
             '<rect x="40" y="330" width="1000" height="1360" rx="20" fill="#6b2d1f" stroke="#111" stroke-width="10"/>'
             '<rect x="70" y="360" width="460" height="1300" fill="#f1e3c4" stroke="#111" stroke-width="6"/><rect x="550" y="360" width="460" height="1300" fill="#f1e3c4" stroke="#111" stroke-width="6"/>'
             '<rect x="525" y="360" width="30" height="1300" fill="#000" opacity=".2"/>' +
             txt(300, 470, "SEITE 1", 58, "#6b2d1f") + txt(300, 570, "DIGGA", 76, "#111") + txt(300, 650, "= KLEIN ⬇", 66, "#e63946") + txt(300, 770, "ALTER", 76, "#111") + txt(300, 850, "= GROSS ⬆", 66, "#2d6a4f") +
             '<g id="p2">' + txt(780, 470, "SEITE 2", 58, "#6b2d1f") + txt(780, 620, "WER DIGGA", 56) + txt(780, 700, "UND ALTER", 56) + txt(780, 780, "IN EINEM", 56) + txt(780, 860, "SATZ SAGT …", 56) + '</g>' +
             '<g id="scrap"><path d="M550 960 L600 1000 L650 950 L700 1010 L760 960 L820 1020 L880 960 L940 1010 L1010 970 V1660 H550 Z" fill="#f1e3c4" stroke="#111" stroke-width="6"/>' + txt(780, 1120, "?????", 70, "#999") + '</g>' +
             '<path id="tearl" d="M550 960 L600 1000 L650 950 L700 1010 L760 960 L820 1020 L880 960 L940 1010 L1010 970" stroke="#111" stroke-width="6" fill="none" opacity="0"/>' +
             "".join(f'<rect x="{(k * 211) % 1000 + 40}" y="{(k * 137) % 1300 + 340}" width="10" height="10" rx="5" fill="#fff" opacity=".5"/>' for k in range(16)) +
             '<g id="bmrun">' + fig(bgm_("bm3", "determined", arm=("front", "hip")), 0, 0, .3) + '</g>')
# --- PIG (s19 Ende): Taube schnappt den Fetzen
S["PIG"] = ('<rect width="1080" height="1920" fill="#8ecae6"/><rect y="1300" width="1080" height="620" fill="#adb5bd"/>' + mini_rathaus(250, 1320, 1.6) + pigeon("pig2", 860, 1360, 1.25, scrap=True))
# --- SK2 (s20/s21): Im Schuhkarton – Oma aus der Teetasse, alle erstarren, Erde bebt
S["SK2"] = ('<rect width="1080" height="1920" fill="#f4a261"/>' + "".join(f'<rect x="0" y="{k * 140}" width="1080" height="6" fill="#000" opacity=".08"/>' for k in range(14)) +
            '<rect x="0" y="1500" width="1080" height="420" fill="#e76f51" stroke="#111" stroke-width="8"/>' +
            teacup("cup2", 300, 1500, 1.0, inner=fig(oma("om4", "grin", arm=("front", "up"), exprs=("grin", "shock")), 0, 40, .55)) +
            chalkbox("cb2", 800, 1500, .8, inner=fig(krause("kr5", "neutral", arm=("down", "down"), exprs=("neutral", "shock")), 0, -60, .42)) +
            fig(bgm_("bm4", "neutral", arm=("down", "down")), 640, 1740, .42) +
            fig(rapper("ra3", "cap", "#7b2cbf", "#9d4edd"), 140, 1800, .3) + fig(rapper("ra4", "beanie", "#2d6a4f", "#06d6a0"), 950, 1800, .3) +
            bubble("bubo", ["DIGGA, ALTER,", "WAS STEHT DA?"], 470, 520, 640, tail=(-1, 1), size=64) +
            '<rect id="dark2" width="1080" height="1920" fill="#000" opacity="0"/>')
# --- TIPP (s22): Jonas mit Schild DIGGA + ALTER = ___?
S["TIPP"] = (street_bg() + fig(jonas("jt2", "confused", arm=("front", "front")), 540, 1850, 1.9) +
             sign("stipp", 540, 1500, 760, 260, ["DIGGA + ALTER", "= ___ ?"], col="#fff", size=86) +
             f'<g transform="translate(860 1900) scale(.5)">{BOX("box2", box_inner.replace("cupS", "cupT").replace("cbS", "cbT").replace("om3", "om5").replace("kr4", "kr6").replace("bx", "by"))}</g>')
# --- LOOP (s23): wie Bild 0 – aber Jonas normal, die Stadt mini an seinem Schuh
S["LOOP"] = ('<rect width="1080" height="1920" fill="#a2d2ff"/>' + "".join(f'<rect x="{x}" y="{y}" width="{w_}" height="70" rx="35" fill="#fff" opacity=".9"/>' for x, y, w_ in ((60, 260, 220), (760, 420, 260))) +
             '<rect y="1820" width="1080" height="100" fill="#6c757d"/>' + fig(jonas("jl1", "grin", arm=("hip", "up")), JGX, JGFY, JGS) +
             mini_rathaus(170, 1890, .22) + "".join(fig(tiny(f"lp{k}", k, "shock", arm=("up", "up")), 280 + k * 40, 1890, .06) for k in range(4)) +
             f'<g transform="translate(200 1700)"><rect x="-120" y="-40" width="240" height="56" rx="16" fill="#fff" stroke="#111" stroke-width="5"/>{txt(0, 2, "DIE STADT", 38)}</g>' + ruler_v("rul3", 840, 1890, 520, "1,50 M"))

# ---------- Zeitplan ----------
J.append('tl.set("#cam", { x: 0, y: 0, scale: 1, svgOrigin: "0 0" }, 0);')
s = st
t = {k: st(k) for k in T}
LB = []  # Ladebalken (Zeit, Prozent, Text)
# s1 Hook: Punch-Zoom auf das Gesamtbild, Schnitt bei 1,5 s auf mich am Schnürsenkel, dann an Jonas hoch
cut(0, 540, 960, 1.08); cam(.02, 540, 960, 1.0, .35, "power3.out"); FX += [("hit", 0, .5, .8)]
J.append('tl.fromTo("#rul1", { scaleY: .2, transformOrigin: "50% 100%" }, { scaleY: 1, duration: .4, ease: "back.out(2)", immediateRender: false }, 0.05);')
c1 = 1.5
cut(c1, 420, 1800, 3.2); hide("#ichlab", c1, .01); cam(c1 + .05, 420, 1760, 3.4, 1.2, "none"); FX += [("whoosh", c1, .3, .4)]
tj1 = w("s1", "Jonas")
cut(tj1 - .1, JGX, 1800, 1.5); cam(tj1, JGX, 600, 1.25, 1.4, "power2.inOut"); FX += [("riser", tj1 - .1, .3, 1.4)]
t40 = w("s1", "vierzig")
J.append(f'tl.fromTo("#rul1", {{ scale: 1.08, transformOrigin: "50% 0%" }}, {{ scale: 1, duration: .3, ease: "back.out(3)", immediateRender: false }}, {F(t40)});'); FX += [("boing", t40, .4, .4)]
# s2 Rückblende: Jonas brüllt Alter und wächst ruckartig
t2 = t["s2"]
cut(t2, 540, 1000, 1.0)
J.append('tl.set("#bubrb", { opacity: 0 }, 0);'); pop("#bubrb", w("s2", "Alter.") - .15, .2, "50% 50%")
ta = w("s2", "Alter.") - .05
grow("#jrb", ta, .9, 1.6, .2, "back.out(3)"); cut(ta, 540, 900, 1.15); FX += [("boing", ta, .5, .4)]
tw2 = w("s2", "wächst") - .05
grow("#jrb", tw2, 1.6, 2.4, .2, "back.out(3)"); plopp("pfrb", tw2); cut(tw2, 540, 700, 1.0); shake(tw2, 7, 14); FX += [("hit", tw2, .4, .6)]
expr("jr1", "angry", "laugh", tw2)
# s3 Strichliste
t3 = t["s3"]
cut(t3, 540, 900, 1.0); cam(t3 + .05, 540, 1000, 1.08, 2.0, "none"); FX += [("whoosh", t3, .3, .5)]
for k in range(24):
    J.append(f'tl.fromTo("#tl{k}", {{ opacity: 0 }}, {{ opacity: 1, duration: .05, immediateRender: false }}, {F(t3 + .2 + k * .06)});')
t38 = w("s3", "dreitausendachthundertfünfzig") - .1
cut(t38, 520, 1100, 1.35); J.append(f'tl.fromTo("#s3850-in", {{ scale: 1.5, transformOrigin: "50% 50%" }}, {{ scale: 1, duration: .3, ease: "back.out(3)", immediateRender: false }}, {F(t38)});'); FX += [("pop", t38, .5, .3)]
# s4 Krause rechnet, Kreide fällt auf den Kopf
t4 = t["s4"]
cut(t4, 540, 1350, 1.6)
tr4 = w("s4", "Das") - .1
cut(tr4, 540, 520, 1.25)
tst4 = w("s4", "Stunde.") - .2
cut(tst4, 540, 1400, 1.9)
J.append(f'tl.to("#chalk2", {{ y: 1170, rotation: 200, duration: .4, ease: "power2.in", transformOrigin: "50% 50%" }}, {F(tst4 - .3)});'); FX += [("klong", tst4 + .1, .35, .5)]
expr("kr1", "confused", "shock", tst4 + .1)
# s5 Jonas legt los: Digga x3, Wolken fliegen weg, Ladebalken 1 %
t5 = t["s5"]
cut(t5, 540, 1100, 1.0); cam(t5 + .05, 540, 1000, 1.1, 1.0, "none")
for k in range(3): J.append(f'tl.set("#bubt{k + 1}", {{ opacity: 0 }}, 0);')
for k in range(3):
    tt = w("s5", "Digga,", k + 1) if k < 2 else w("s5", "Digga.")
    pop(f"#bubt{k + 1}", tt - .05, .18, "50% 50%"); FX += [("pop", tt, .55, .2)]; shake(tt, 5, 10)
    grow("#jtot", tt, 3.2 - k * .015, 3.2 - (k + 1) * .015, .15, "power3.in")
    if k == 1: cut(tt - .05, 540, 700, 1.3)
J.append(f'tl.to("#clouds", {{ x: 900, opacity: 0, duration: 1.2, ease: "power2.in" }}, {F(w("s5", "Digga,") )});')
expr("jt1", "determined", "grin", w("s5", "Digga,", 2))
LB.append((w("s5", "Digga.") + .1, 1, "SCHRUMPFEN …"))
# s6 Gesetz: Alter verboten – Stempel
t6 = t["s6"]
cut(t6, 300, 1350, 1.5); cam(t6 + .05, 300, 1300, 1.65, 1.4, "none")
tg6 = w("s6", "Gesetz:") - .1
cut(tg6, 620, 1100, 1.0)
tvb = w("s6", "verboten!") - .15
J.append(f'tl.fromTo("#stmp", {{ y: 0 }}, {{ y: 420, duration: .18, ease: "power3.in", immediateRender: false }}, {F(tvb - .18)}); tl.to("#stmp", {{ y: 0, duration: .3 }}, {F(tvb + .1)});')
J.append(f'tl.fromTo("#stamp", {{ opacity: 0, scale: 1.6 }}, {{ opacity: 1, scale: 1, duration: .12, immediateRender: false }}, {F(tvb)});'); shake(tvb, 6, 14); FX += [("hit", tvb, .6, .6)]
cut(tvb, 840, 950, 1.5)
# s7 Oma: Komm schon, Digga – Plopp – Teetasse
t7 = t["s7"]
cut(t7, 520, 1250, 1.6)
J.append(f'tl.to("#omz", {{ y: -40, duration: .14, yoyo: true, repeat: 7, ease: "sine.out" }}, {F(t7 + .1)});')
J.append('tl.set("#bubom", { opacity: 0 }, 0);'); pop("#bubom", w("s7", "Komm") - .1, .2, "50% 50%")
cut(w("s7", "Komm") - .1, 540, 1000, 1.2)
tp7 = w("s7", "Plopp.") - .1
plopp("pfom", tp7); grow("#omz", tp7, .62, .01, .25, "power3.in"); hide("#bubom", tp7, .05); FX += [("pop", tp7, .8, .3)]
J.append(f'tl.fromTo("#cupoma", {{ opacity: 0 }}, {{ opacity: 1, duration: .1, immediateRender: false }}, {F(tp7 + .3)});')
cut(w("s7", "Jetzt") - .15, 850, 1300, 2.2); FX += [("whoosh", w("s7", "Jetzt") - .15, .3, .4)]
# s8 Ameisen-Rapper
t8 = t["s8"]
cut(t8, 540, 1250, 1.3); cam(t8 + .05, 540, 1200, 1.45, 1.2, "none")
J.append(f'tl.to("#ar1, #ar2", {{ y: -20, duration: .16, yoyo: true, repeat: 15 }}, {F(t8 + .1)}); tl.to("#spk1, #spk2", {{ scale: 1.12, transformOrigin: "50% 50%", duration: .12, yoyo: true, repeat: 19 }}, {F(t8 + .1)});')
J.append(f'tl.fromTo("#nt1", {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: .4, immediateRender: false }}, {F(t8 + .3)});')
trf = w("s8", "Text:") - .1
cut(trf, 820, 900, 1.4)
J.append(f'tl.to("#pig1-in", {{ rotation: 10, transformOrigin: "-60% -40%", duration: .16, yoyo: true, repeat: 11 }}, {F(trf)});'); FX += [("boing", trf, .3, .3)]
# s9 Jonas singt mit – schrumpft im Beat auf Kranhöhe – 50 %
t9 = t["s9"]
cut(t9, 540, 960, 1.0); cam(t9 + .05, 540, 960, 1.0, .1)
J.append(f'tl.fromTo("#nt2", {{ opacity: 0 }}, {{ opacity: 1, duration: .2, immediateRender: false }}, {F(t9 + .1)}); tl.to("#nt2", {{ y: -40, duration: .3, yoyo: true, repeat: 5 }}, {F(t9 + .1)});')
t50 = w("s9", "Fünfzig") - .1
grow("#jkr", t9 + .2, 3.4, 2.4, t50 - t9 - .1, "steps(5)"); FX += [("boing", t9 + .2, .3, .3), ("boing", t9 + .6, .3, .3), ("boing", t9 + 1.0, .3, .3)]
cut(t50, 540, 1100, 1.15); cam(t50 + .05, 540, 960, 1.0, .6)
pop("#s50", t50, .25, "50% 50%"); FX += [("chime", t50, .4, .8)]
LB.append((t50, 50, "SCHRUMPFEN …"))
# s10 Ohrwurm: Ohr extrem nah, dann ganze Straße singt
t10 = t["s10"]
cut(t10, 560, 980, 1.6)
J.append(f'tl.fromTo("#worm-in", {{ scale: .1, transformOrigin: "0% 100%" }}, {{ scale: 1, duration: .7, ease: "back.out(1.6)", immediateRender: false }}, {F(t10 + .2)});')
J.append(f'tl.fromTo("#nt3", {{ opacity: 0 }}, {{ opacity: 1, duration: .2, immediateRender: false }}, {F(t10 + .6)});'); FX += [("splat", t10 + .2, .3, .4)]
cut(t10 + 1.1, 700, 800, 1.0)
tsg = w("s10", "Die") - .1
cut(tsg, 540, 1300, 1.15); cam(tsg + .05, 540, 1200, 1.0, 1.2, "none"); FX += [("whoosh", tsg, .3, .4)]
J.append(f'tl.fromTo("#nt4, #nt5", {{ opacity: 0 }}, {{ opacity: 1, duration: .2, immediateRender: false }}, {F(tsg + .2)});')
J.append(f'tl.to("#{",#".join(f"sg{k}" for k in range(5))}", {{ y: -30, duration: .2, yoyo: true, repeat: 7 }}, {F(tsg + .1)});')
# s11 Schnellschnitt Bäcker / Schwimmbad / Matheunterricht
t11 = t["s11"]
tpool = w("s11", "Schwimmbad,") - .2; tkl = w("s11", "Matheunterricht.") - .2
cut(t11, 540, 1150, 1.25); plopp("pfb", t11 + .3); FX += [("pop", t11 + .3, .4, .2)]
J.append(f'tl.fromTo("#nt6, #nt7, #nt8", {{ opacity: 0 }}, {{ opacity: 1, duration: .1, immediateRender: false }}, {F(t11)});')
cut(tpool, 540, 1000, 1.1); plopp("pfp", tpool + .3); FX += [("pop", tpool + .3, .4, .2)]
cut(tkl, 540, 1100, 1.0); plopp("pfk", tkl + .3); FX += [("pop", tkl + .3, .4, .2)]
J.append(f'tl.to("#{",#".join(f"kl{k}" for k in range(4))}", {{ y: -25, duration: .18, yoyo: true, repeat: 5 }}, {F(tkl)});')
# s12 Krause zweite Stimme – Plopp – Kreideschachtel
t12 = t["s12"]
cut(t12, 420, 1250, 1.3); cam(t12 + .05, 420, 1150, 1.5, 1.4, "none")
J.append(f'tl.fromTo("#nt9", {{ opacity: 0 }}, {{ opacity: 1, duration: .2, immediateRender: false }}, {F(t12 + .2)});')
tp12 = w("s12", "Plopp.") - .1
plopp("pfkr", tp12); grow("#krz", tp12, 1.45, .01, .25, "power3.in"); FX += [("pop", tp12, .8, .3)]
J.append(f'tl.fromTo("#cbk", {{ opacity: 0, y: 60 }}, {{ opacity: 1, y: 0, duration: .3, immediateRender: false }}, {F(tp12 + .35)});')
cut(tp12, 640, 1200, 1.0); cut(w("s12", "Kreideschachtel.") - .1, 850, 1380, 2.4)
# s13 Sogar ich – werter Freund
t13 = t["s13"]
cut(t13, 480, 1200, 1.4); expr("ich1", "shock", "panic", t13 + .1)
J.append(f'tl.to("#ich1", {{ y: -14, duration: .14, yoyo: true, repeat: 13 }}, {F(t13)});')
J.append(f'tl.to("#mark", {{ y: 300, duration: 1.4, ease: "steps(6)" }}, {F(t13 + .3)}); ')
grow("#ichz", t13 + .3, 1.85, 1.6, 1.4, "steps(6)")
pop("#sicm", t13 + .5, .25, "50% 50%"); FX += [("pop", t13 + .5, .5, .3)]
twf = w("s13", "werter") - .1
cut(twf, 430, 1100, 1.25); expr("ich1", "panic", "smug", twf); FX += [("chime", twf, .3, .8)]
# s14 100 % – Normal!
t14 = t["s14"]
cut(t14, 540, 1200, 1.2); LB.append((w("s14", "hundert") , 100, "SCHRUMPFEN …"))
J.append(f'tl.set("#conf1", {{ opacity: 1 }}, {F(w("s14", "hundert"))}); tl.fromTo("#conf1 .cf", {{ y: -300 }}, {{ y: 900, duration: 2.6, ease: "none", stagger: .02, immediateRender: false }}, {F(w("s14", "hundert"))});')
FX += [("chime", w("s14", "hundert"), .5, 1.2), ("riser", t14, .3, .8)]
t150 = w("s14", "Ein") - .1
pop("#b150", t150, .3, "50% 50%"); cut(t150, 540, 900, 1.35)
cut(w("s14", "Normal!") - .1, 540, 1100, 1.0); J.append(f'tl.to("#jn1", {{ y: -40, duration: .2, yoyo: true, repeat: 3 }}, {F(w("s14", "Normal!") - .1)});')
# s15 Alle gummibärchengroß
t15 = t["s15"]
cut(t15, 540, 900, 1.3); expr("jg2", "confused", "shock", w("s15", "Alle") - .1)
tgb = w("s15", "Gummibärchen.") - .3
cut(w("s15", "Alle") - .1, 540, 1650, 2.0); cam(w("s15", "Alle"), 540, 1700, 2.3, 1.2, "none")
cut(tgb, 220, 1700, 2.6); FX += [("boing", tgb, .4, .3)]
for k in range(12): J.append(f'tl.to("#tn{k}", {{ x: {(-1) ** k * 18}, duration: .12, yoyo: true, repeat: 15 }}, {F(t15)});')
# s16 Bürgermeister merkt es – Schweiß – Zoom
t16 = t["s16"]
cut(t16, 540, 900, 1.0)
tal = w("s16", "Alter") - .1
cut(tal, 600, 820, 1.3); J.append(f'tl.fromTo("#salt2-in", {{ scale: 1.15, transformOrigin: "50% 50%" }}, {{ scale: 1, duration: .25, ease: "back.out(3)", immediateRender: false }}, {F(tal)});')
tdk = w("s16", "Danke,") - .1
cut(tdk, 470, 1290, 1.6); cam(tdk + .05, 470, 1300, 2.6, 2.0, "power1.in")
J.append(f'tl.set("#sweat", {{ opacity: 1 }}, {F(tdk)}); tl.to("#sweat", {{ y: 40, duration: .6, repeat: 3 }}, {F(tdk)});'); FX += [("tick", tdk, .3, 1.5)]
# s17 Schuhkarton – seitliche Fahrt
t17 = t["s17"]
cut(t17, 540, 1300, 1.2)
J.append(f'tl.fromTo("#skbg", {{ x: 0 }}, {{ x: -1080, duration: {F(t["s18"] - t17)}, ease: "none", immediateRender: false }}, {F(t17)});')
J.append(f'tl.to("#jsk", {{ y: -18, duration: .2, yoyo: true, repeat: {int((t["s18"] - t17) / .2)} }}, {F(t17)});')
tbx = w("s17", "Schuhkarton.") - .3
cut(tbx, 540, 1350, 1.5); FX += [("whoosh", t17, .3, .5), ("pop", tbx, .4, .3)]
# s18 Stadtbuch Seite 1 – Bürgermeister rennt über die Seite
t18 = t["s18"]
cut(t18, 540, 1000, 1.0); cam(t18 + .05, 540, 1000, 1.06, 1.2, "none")
J.append(f'tl.set("#p2", {{ opacity: 0 }}, 0); tl.set("#bmrun", {{ x: 120, y: 1550 }}, 0); tl.to("#bmrun", {{ x: 460, y: 1150, duration: 1.6, ease: "none" }}, {F(t18 + .2)}); tl.to("#bmrun", {{ x: 160, y: 1060, duration: 1.2, ease: "none" }}, {F(t18 + 1.8)});')
ts1 = w("s18", "Seite") - .1
cut(ts1, 300, 700, 1.5); FX += [("swoosh", ts1, .3, .4)]
# s19 Seite 2 … abgerissen – Fetzen fliegt zur Taube
t19 = t["s19"]
cut(t19, 780, 750, 1.6); J.append(f'tl.set("#p2", {{ opacity: 1 }}, {F(t19)});'); FX += [("swoosh", t19, .3, .4)]
tab = w("s19", "abgerissen.") - .25
J.append(f'tl.to("#scrap", {{ x: 700, y: -900, rotation: 40, duration: .6, ease: "power2.in", transformOrigin: "50% 50%" }}, {F(tab)}); tl.set("#tearl", {{ opacity: 1 }}, {F(tab)});')
cut(tab, 780, 1100, 1.25); shake(tab, 5, 10); FX += [("splat", tab, .5, .4)]
tpig = round(tab + .7, 2)
cut(tpig, 760, 1000, 1.25); J.append(f'tl.set("#scrapb", {{ opacity: 1 }}, {F(tpig + .15)}); tl.fromTo("#pig2-in", {{ x: 300 }}, {{ x: 0, duration: .25, ease: "power2.out", immediateRender: false }}, {F(tpig)});')
FX += [("whoosh", tpig, .4, .4)]
# s20 Oma aus der Teetasse: Digga, Alter, was steht da?
t20 = t["s20"]
cut(t20, 300, 1250, 1.7)
J.append('tl.set("#bubo", { opacity: 0 }, 0);')
tdi = w("s20", "Digga,") - .1
pop("#bubo", tdi, .2, "50% 50%"); cut(tdi, 400, 1000, 1.25)
tal2 = w("s20", "Alter,") - .05
for uid in ("kr5", "bm4"): expr(uid, "neutral", "shock", tal2)
cut(tal2, 540, 1300, 1.0); cam(tal2 + .05, 540, 1150, 1.0, .5); FX += [("hit", tal2, .5, .6)]
# s21 Die Erde bebt – 99 %
t21 = t["s21"]
hide("#bubo", t21 - .05, .1)
cut(t21, 540, 1350, 1.15); shake(t21, 40, 18); FX += [("wirbel", t21, .5, min(2.5, t["s22"] - t21)), ("riser", t21, .4, 1.5)]
J.append(f'tl.to("#cup2", {{ rotation: 3, transformOrigin: "50% 100%", duration: .06, yoyo: true, repeat: 25 }}, {F(t21)}); tl.to("#dark2", {{ opacity: .35, duration: 1.0 }}, {F(t21)});')
expr("om4", "grin", "shock", t21 + .1)
LB.append((t21 + .1, 99, "??? …"))
# s22 Dein Tipp
t22 = t["s22"]
cut(t22, 540, 1050, 1.15); cam(t22 + .05, 540, 1050, 1.25, 2.0, "none"); FX += [("whoosh", t22, .3, .4)]
J.append(f'tl.to("#stipp-in", {{ scale: 1.05, transformOrigin: "50% 50%", duration: .3, yoyo: true, repeat: 5 }}, {F(w("s22", "Schreib"))});')
cut(w("s22", "Schreib") - .1, 540, 1300, 1.0)
# s23 Loop: von unten an Jonas hoch (spiegelt Bild 0)
t23 = t["s23"]
cut(t23, 300, 1800, 3.0); cam(t23 + .3, JGX, 700, 1.15, 1.6, "power2.inOut"); FX += [("riser", t23, .3, 1.5)]
tEND = round(END - 1.5, 2)

sets = [("N2", 0, t2), ("RB", t2, t3), ("SL", t3, t4), ("KZ", t4, t5), ("TOT", t5, t6), ("BM", t6, t7), ("OM", t7, t8), ("AR", t8, t9), ("KRAN", t9, t10),
        ("EAR", t10, tsg), ("SING", tsg, t11), ("BAK", t11, tpool), ("POOL", tpool, tkl), ("KL", tkl, t12), ("KR2", t12, t13), ("ICH", t13, t14), ("J100", t14, t15),
        ("GB", t15, t16), ("BM2", t16, t17), ("SK", t17, t18), ("BUCH", t18, tpig), ("PIG", tpig, t20), ("SK2", t20, t22), ("TIPP", t22, t23), ("LOOP", t23, END)]

# Ladebalken „SCHRUMPFEN … %“ (Dauer-Element oben links)
lb_html = (f'<div id="lb" class="ui" style="left:24px;top:34px;width:440px;background:#111;border:5px solid #ffd166;border-radius:16px;padding:6px 14px 10px">'
           f'<div style="font:900 34px Inter,sans-serif;color:#fff;white-space:nowrap"><span id="lbt">SCHRUMPFEN …</span> <span id="lbv" style="color:#ffd166">0 %</span></div>'
           f'<div style="margin-top:6px;height:22px;background:#333;border-radius:11px;overflow:hidden"><div id="lbb" style="height:22px;width:0%;background:#ffd166"></div></div></div>')
prevv, prevt = "0 %", "SCHRUMPFEN …"
for tt, v, lab in LB:
    settext("lbv", tt, f"{v} %", prevv); prevv = f"{v} %"
    if lab != prevt: settext("lbt", tt, lab, prevt); prevt = lab
    col = "#2dc653" if v == 100 else ("#e63946" if lab.startswith("?") else "#ffd166")
    J.append(f'tl.to("#lbb", {{ width: "{max(v, 1.5)}%", backgroundColor: "{col}", duration: .5, ease: "power2.out" }}, {F(tt)});')
    J.append(f'tl.fromTo("#lb", {{ scale: 1.2, transformOrigin: "0% 0%" }}, {{ scale: 1, duration: .3, ease: "back.out(3)", immediateRender: false }}, {F(tt)});')
J.append(f'tl.to("#lb", {{ x: "+=8", duration: .05, yoyo: true, repeat: 19 }}, {F(t21 + .2)});')
tag = f'<div class="ui clip" data-start="0" data-duration="{F(END)}" style="right:24px;top:40px;font:900 30px Inter,sans-serif;color:#fff;background:rgba(0,0,0,.55);padding:6px 14px;border-radius:12px">TEIL 2</div>'
R = "<span style='color:#ff4d5a'>"; G_ = "<span style='color:#2dc653'>"; X = "</span>"
OBEN = [(0, f"1x DIGGA = {R}1 CM KLEINER{X}"), (tj1 - .1, "JONAS: 40 M"), (t2, f"ALTER = {G_}+1 CM{X}"), (t3, "3.850 DIGGA"), (t4, "1 STD 4 MIN"), (t5, "SCHRUMPFEN … 1 %"),
        (t6, f"GESETZ: ALTER ❌"), (t7, "OMA: TEETASSE"), (t8, "DIGGA-SONG 🎤"), (t9, "JONAS SINGT MIT 🎶"), (t10, "OHRWURM 🐛"), (t11, "GANZE STADT"), (t12, "KRAUSE: KREIDE-BOX"),
        (t13, f"ICH: {R}-30 CM{X}"), (t14, f"1,50 M ✅"), (t15, "ALLE = GUMMIBÄRCHEN"), (t16, "ALTER ❌"), (t17, "1 SCHUHKARTON"), (t18, "SEITE 1"), (t19, "SEITE 2: ???"),
        (t20, "DIGGA + ALTER"), (t21, "??? … 99 %"), (t22, "DEIN TIPP: ___?"), (t23, "DIGGA + ALTER = ?")]
HOT = {"DIGGA", "ALTER", "JONAS", "PLOPP", "VERBOTEN", "OHRWURM", "GUMMIBÄRCHEN", "TEETASSE", "KREIDESCHACHTEL", "NORMAL", "PROZENT", "FINALE", "TIPP", "BEBT"}
from clampcam import clamp_cam; clamp_cam(J)  # tools/clampcam.py
finish(S, sets, OBEN, FX, HOT, tag, extra_ui=lb_html, banner=("FINALE?", "➕ FOLGEN"), oben_top=150, cap_top=1150, banner_top=360)
print("tpig", tpig, "t21", t21)

# Endbanner einzeilig halten (FINALE? + FOLGEN passt sonst nicht in 1080 px)
_h = open("compositions/welt.html", encoding="utf-8").read()
_h = _h.replace("padding:14px 40px;font:900 96px/1 Inter", "padding:14px 30px;white-space:nowrap;font:900 78px/1 Inter")
open("compositions/welt.html", "w", encoding="utf-8").write(_h)
