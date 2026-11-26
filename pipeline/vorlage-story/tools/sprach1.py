"""STORY-FORMAT „In dieser Stadt …“ – NEUE SERIE „Sprachnachrichten-Stadt“, TEIL 1: Jede Sprachnachricht über 1 Minute läuft über die Stadt-Lautsprecher.
Aufruf: /usr/bin/python3 tools/sprach1.py  (liest voice.json + assets/vo/timing.json; Bausteine aus tools/bausteine.py, Figuren wie digga1/digga2;
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

# ---------- Sprachnachrichten-Stadt: Figuren + Requisiten ----------
ICH_EX2 = ("happy", "smug", "shock", "panic", "determined", "neutral", "grin", "laugh", "confused")
def ich_(uid, start="happy", arm=("down", "down"), extra="", exprs=ICH_EX2):
    return person(uid, "ich", "#6b3e26", "#118ab2", exprs=exprs, start=start, arm=arm, extra=extra)
CURLERS = "".join(f'<rect x="{x - 22}" y="-132" width="44" height="34" rx="12" fill="{c}" stroke="#111" stroke-width="4"/>' for x, c in ((-60, "#ff8fab"), (0, "#4cc9f0"), (60, "#ffd166")))
def oma_(uid, start="happy", arm=("down", "front"), extra="", exprs=("happy", "laugh", "grin", "wink", "smug", "determined")):
    return person(uid, "oma", "#e0e0e0", "#9d4edd", exprs=exprs, start=start, arm=arm, head_acc=OMA_ACC + CURLERS, extra=extra)
def emil(uid, start="happy", arm=("down", "front"), extra="", exprs=("happy", "shock", "panic", "laugh", "sad", "neutral")):
    return person(uid, "cap", "#e63946", "#f77f00", skin="#c68642", exprs=exprs, start=start, arm=arm, extra=extra)
TIE = '<path d="M0 -296 L-18 -270 L0 -150 L18 -270 Z" fill="#2d6a4f" stroke="#111" stroke-width="4"/>'
def krause_(uid, start="neutral", arm=("down", "mic"), extra="", exprs=("neutral", "smug", "wink", "shock", "determined", "happy")):
    return person(uid, "glatze", "#555", "#adb5bd", exprs=exprs, start=start, arm=arm, head_acc=KR_ACC, extra=TIE + extra)
PHONE_R = '<g transform="translate(196 -330)"><rect x="-30" y="-56" width="60" height="104" rx="12" fill="#222" stroke="#111" stroke-width="4"/><rect x="-22" y="-46" width="44" height="80" rx="6" fill="#8ecae6"/></g>'
PHONE_M = '<g transform="translate(74 -300)"><rect x="-30" y="-56" width="60" height="104" rx="12" fill="#222" stroke="#111" stroke-width="4"/><rect x="-22" y="-46" width="44" height="80" rx="6" fill="#8ecae6"/><rect x="-8" y="-6" width="16" height="16" rx="8" fill="#e63946"/></g>'
TABLET = '<g transform="translate(196 -330)"><rect x="-70" y="-90" width="140" height="170" rx="16" fill="#222" stroke="#111" stroke-width="5"/><rect x="-58" y="-78" width="116" height="146" rx="8" fill="#cdb4db"/><rect x="-14" y="-20" width="28" height="28" rx="14" fill="#e63946"/></g>'
def mast(uid, x, y, s=1.0, rot=0):
    horn = lambda dx, r: (f'<g transform="translate({dx} -560) rotate({r})"><path d="M0 -30 L130 -90 V90 L0 30 Z" fill="#adb5bd" stroke="#111" stroke-width="7"/>'
                          f'<rect x="-40" y="-36" width="50" height="72" rx="10" fill="#6c757d" stroke="#111" stroke-width="6"/><rect x="120" y="-90" width="22" height="180" rx="8" fill="#ced4da" stroke="#111" stroke-width="5"/></g>')
    return (f'<g transform="translate({x} {y}) scale({s})"><rect x="-18" y="-560" width="36" height="560" fill="#495057" stroke="#111" stroke-width="6"/>'
            f'<g id="{uid}" transform="rotate({rot} 0 -560)">{horn(30, 0)}<g transform="scale(-1 1)">{horn(30, 0)}</g></g>'
            f'<g id="{uid}-w" opacity="0">' + "".join(f'<path d="M{200 + k * 50} {-640 + k * 10} Q{240 + k * 60} -560 {200 + k * 50} {-480 - k * 10}" stroke="#ffd166" stroke-width="12" fill="none" stroke-linecap="round"/>' for k in range(3)) +
            "".join(f'<path d="M{-200 - k * 50} {-640 + k * 10} Q{-240 - k * 60} -560 {-200 - k * 50} {-480 - k * 10}" stroke="#ffd166" stroke-width="12" fill="none" stroke-linecap="round"/>' for k in range(3)) + '</g></g>')
def duck(uid, x, y, s=1.0, vis=True):
    return (f'<g id="{uid}" opacity="{1 if vis else 0}" transform="translate({x} {y}) scale({s})"><ellipse cx="0" cy="6" rx="130" ry="18" fill="#000" opacity=".2"/>'
            '<rect x="-120" y="-150" width="240" height="150" rx="60" fill="#ffd60a" stroke="#111" stroke-width="7"/><rect x="-40" y="-300" width="150" height="150" rx="50" fill="#ffd60a" stroke="#111" stroke-width="7"/>'
            '<path d="M100 -230 L180 -215 L100 -195 Z" fill="#fb8500" stroke="#111" stroke-width="5"/>' + E(50, -240, 11) +
            '<path d="M20 -268 L80 -256" stroke="#111" stroke-width="7" stroke-linecap="round"/><path d="M-30 6 V30 M30 6 V30" stroke="#fb8500" stroke-width="14"/></g>')
def wave(x, y, n=18, wd=520, h=70, col="#2dc653", uid=None):
    idp = f' id="{uid}"' if uid else ""
    return f'<g{idp}>' + "".join(f'<rect x="{x + k * wd / n:.0f}" y="{y - (h * (.3 + .7 * abs(((k * 37) % 11) / 10))) / 2:.0f}" width="{wd / n * .55:.0f}" height="{h * (.3 + .7 * abs(((k * 37) % 11) / 10)):.0f}" rx="6" fill="{col}"/>' for k in range(n)) + '</g>'
def vbadge(uid, x, y, t, col, wd=330, vis=True, size=86):
    return sign(uid, x, y, wd, 130, [t], col=col, fg="#fff", size=size, vis=vis)
def bus_bg():
    return ('<rect width="1080" height="1920" fill="#8ecae6"/>' + street_bg().replace('<rect width="1080" height="1920" fill="#8ecae6"/>', ''))

S = {}; FX = []
# --- SPLIT (s1/s2 + Loop s23): links ich 0:59, rechts Oma 14:00 vor dröhnendem Mast
def split(sfx, ich_label="0:59"):
    L = (street_bg() + fig(ich_(f"i{sfx}", "smug", arm=("down", "front"), extra=PHONE_R), 270, 1450, 1.15) +
         vbadge(f"bi{sfx}", 270, 700, ich_label, "#2dc653", wd=340 if len(ich_label) < 6 else 470))
    crowdR = "".join(fig(tiny(f"cr{sfx}{k}", k, "panic", arm=("up", "up")), 600 + k * 170, 1900, .55) for k in range(3))
    Rr = ('<rect width="1080" height="1920" fill="#ffd6a5"/>' + street_bg().replace('#8ecae6', '#ffd6a5') + mast(f"m{sfx}", 980, 1330, 1.1) +
          fig(oma_(f"o{sfx}", "laugh", arm=("down", "front"), extra=TABLET), 790, 1450, 1.15) + crowdR + vbadge(f"bo{sfx}", 800, 700, "14:00", "#e63946", wd=360))
    return (f'<defs><clipPath id="cl{sfx}"><rect width="540" height="1920"/></clipPath><clipPath id="cr{sfx}"><rect x="540" width="540" height="1920"/></clipPath></defs>'
            f'<g clip-path="url(#cl{sfx})">{L}</g><g clip-path="url(#cr{sfx})">{Rr}</g><rect x="532" width="16" height="1920" fill="#fff" stroke="#111" stroke-width="4"/>')
S["SPLIT"] = split("a")
S["LOOP"] = split("z", "6:00:00")
# --- SWISH (s2): ich gross mit Daumen weg vom Handy, dann Oma mit endloser Wellenform
S["S2"] = (street_bg() + fig(ich_("i2", "smug", arm=("down", "front"), extra=PHONE_R), 300, 1700, 1.6) + vbadge("b2i", 320, 600, "0:59", "#2dc653") +
           '<g transform="translate(1080 0)">' + street_bg().replace('#8ecae6', '#ffd6a5') + fig(oma_("o2", "grin", arm=("down", "front"), extra=TABLET), 300, 1700, 1.6) +
           '<g id="owave">' + wave(560, 1150, 40, 1600, 120, "#e63946") + '</g>' + vbadge("b2o", 320, 600, "14:00", "#e63946", wd=380) + '</g>')
# --- MARKT (s3): Marktplatz, Mast im Vordergrund, Omas Stimme + Rezept-Icons
icons = "".join(f'<text class="ic" x="{x}" y="{y}" text-anchor="middle" style="font:120px Noto Color Emoji">{e}</text>' for x, y, e in ((200, 700, "🥔"), (420, 560, "🥒"), (640, 720, "🥚"), (860, 580, "🧅"), (300, 900, "🥔"), (760, 900, "🥄")))
S["MARKT"] = ('<rect width="1080" height="1920" fill="#8ecae6"/><rect x="0" y="700" width="1080" height="700" fill="#e9c46a" stroke="#111" stroke-width="6"/>' +
              "".join(f'<rect x="{50 + k * 210}" y="800" width="130" height="160" fill="#fff8d6" stroke="#111" stroke-width="5"/>' for k in range(5)) +
              '<rect y="1400" width="1080" height="520" fill="#ced4da"/>' + "".join(fig(tiny(f"mk{k}", k, "confused", arm=("down", "down")), 120 + k * 210, 1700 + (k % 2) * 60, .45) for k in range(5)) +
              mast("m3", 830, 1900, 2.0) + bubble("bub3", ["HALLO SCHATZ,", "IST DAS AN?"], 380, 520, 600, tail=(1, 1), size=66) + f'<g id="icons" opacity="0">{icons}</g>' +
              sign("rez", 300, 1000, 520, 130, ["🥔 REZEPT 3:00"], col="#fff", size=64, vis=False))
# --- FREEZE (s4a): Stadt bleibt stehen
S["FREEZE"] = (street_bg() + '<g transform="translate(700 1500)"><rect x="-260" y="-160" width="520" height="160" rx="30" fill="#3a86ff" stroke="#111" stroke-width="7"/><rect x="-170" y="-260" width="320" height="120" rx="26" fill="#bde0fe" stroke="#111" stroke-width="7"/>'
               '<rect x="-200" y="-20" width="90" height="90" rx="45" fill="#222"/><rect x="110" y="-20" width="90" height="90" rx="45" fill="#222"/></g>' +
               "".join(fig(tiny(f"fz{k}", k + 1, "shock", arm=("front", "down")), x, 1800, .7) for k, x in enumerate((150, 420, 930))) + mast("m4", 120, 1350, 1.0) +
               sign("stop", 540, 900, 380, 140, ["⏸ STOPP"], col="#e63946", fg="#fff", size=80, vis=False))
# --- BUS (s4b): durch die Busscheibe – Busfahrer schreibt mit
S["BUS"] = ('<rect width="1080" height="1920" fill="#ffd60a"/><rect x="60" y="260" width="960" height="900" rx="40" fill="#bde0fe" stroke="#111" stroke-width="12"/>' +
            fig(person("drv", "mann", "#3d2b1f", "#264653", exprs=("determined",), start="determined", arm=("front", "front")), 540, 1560, 1.5) +
            '<g transform="translate(540 1330)"><rect x="-260" y="-40" width="520" height="80" rx="40" fill="none" stroke="#111" stroke-width="30"/></g>' +
            '<g id="note" transform="translate(560 1250) rotate(-6)"><rect x="-200" y="-90" width="400" height="180" rx="12" fill="#fff8d6" stroke="#111" stroke-width="7"/>' + txt(0, -20, "2 ZWIEBELN", 52) + txt(0, 50, "1 GURKE …", 52) + '</g>' +
            '<rect y="1160" width="1080" height="760" fill="#264653" opacity=".25"/>')
# --- PROFI (s5): Stoppuhr, bei 0:59 loslassen
S["PROFI"] = (street_bg() + fig(ich_("i5", "determined", arm=("front", "front"), extra=PHONE_R), 540, 1800, 2.0) +
              '<g transform="translate(260 760)"><rect x="-150" y="-150" width="300" height="300" rx="150" fill="#fff" stroke="#111" stroke-width="12"/><rect x="-30" y="-200" width="60" height="50" rx="10" fill="#111"/>' +
              '<g id="hand5"><rect x="-8" y="-120" width="16" height="125" rx="8" fill="#e63946"/></g>' + f'<text id="sw5" x="0" y="90" text-anchor="middle" style="font:900 60px {FONT};fill:#111">0:57</text></g>' +
              vbadge("b5", 780, 760, "0:59 ✅", "#2dc653", wd=380, vis=False))
# --- PHONE (s6a): Display 1:01 blinkt rot / EMIL (s6b)
S["PHONE"] = ('<rect width="1080" height="1920" fill="#222"/><rect x="190" y="200" width="700" height="1500" rx="80" fill="#111" stroke="#555" stroke-width="12"/><rect x="230" y="300" width="620" height="1300" rx="30" fill="#e9ecef"/>' +
              txt(540, 650, "EMIL ➜ MAMA", 56) + wave(270, 760, 16, 540, 110, "#e63946") +
              f'<text id="pt6" x="540" y="1080" text-anchor="middle" style="font:900 200px {FONT};fill:#e63946">1:01</text>' +
              '<g transform="translate(540 1380)"><rect x="-90" y="-90" width="180" height="180" rx="90" fill="#e63946" stroke="#111" stroke-width="7"/><rect x="-26" y="-50" width="52" height="80" rx="26" fill="#fff"/></g>')
S["EMIL"] = (street_bg() + mast("m6a", 140, 1350, 1.0) + mast("m6b", 940, 1350, 1.0) + fig(emil("e6", "happy", arm=("down", "front"), extra=PHONE_R), 540, 1800, 1.8) +
             '<g id="alarm" opacity="0"><rect x="0" y="0" width="1080" height="1920" fill="#e63946" opacity=".25"/></g>')
# --- TURN (s7): Totale, alle drehen sich zu Emil
crowd7 = "".join(f'<g id="tc{k}">' + fig(tiny(f"t7{k}", k, "shock", arm=("down", "down")), x, fy, s) + '</g>' for k, (x, fy, s) in enumerate(((120, 1900, .7), (320, 1850, .6), (760, 1850, .6), (960, 1900, .7), (220, 1500, .4), (860, 1500, .4))))
S["TURN"] = (street_bg() + mast("m7", 540, 1100, 1.0) + fig(emil("e7", "neutral", arm=("down", "front"), extra=PHONE_R), 540, 1680, .8) + crowd7 +
             bubble("bub7", ["MAMA, ICH HAB", "ANGST VOR ENTEN."], 540, 330, 760, tail=(0, 1), size=62))
# --- DOOR (s8): Ente vor der Tür
S["DOOR"] = ('<rect width="1080" height="1920" fill="#e9c46a"/>' + "".join(f'<rect x="0" y="{k * 80}" width="1080" height="6" fill="#000" opacity=".06"/>' for k in range(24)) +
             '<rect x="200" y="520" width="680" height="1200" fill="#3d2b1f" stroke="#111" stroke-width="12"/>' +
             fig(emil("e8", "neutral", arm=("down", "down"), exprs=("neutral", "shock", "sad")), 540, 1700, 1.0) +
             '<g id="door8"><rect x="210" y="530" width="660" height="1180" fill="#9c6644" stroke="#111" stroke-width="8"/><rect x="760" y="1100" width="40" height="40" rx="20" fill="#ffd166" stroke="#111" stroke-width="4"/>'
             '<rect x="280" y="620" width="520" height="380" rx="12" fill="none" stroke="#7f5539" stroke-width="10"/><rect x="280" y="1160" width="520" height="460" rx="12" fill="none" stroke="#7f5539" stroke-width="10"/></g>'
             '<rect y="1720" width="1080" height="200" fill="#adb5bd"/><rect x="330" y="1720" width="420" height="60" fill="#6b4226" stroke="#111" stroke-width="5"/>' + txt(540, 1765, "WILLKOMMEN", 36, "#fff") +
             duck("d1", 380, 1880, .9) + duck("d2", 720, 1880, .9, vis=False))
# --- MATHE (s9): Krause von unten mit Handy, ganze Stadt hört Bruchrechnung
S["MATHE"] = (room_bg("#e9f5db", "#b08968", win=False) + '<rect x="90" y="250" width="900" height="420" rx="16" fill="#2d6a4f" stroke="#6b4226" stroke-width="18"/>' +
              txt(540, 620, "½ + ¼ = ¾", 100, "#fff") +
              fig(krause_("k9", "smug", arm=("down", "mic"), extra=PHONE_M), 540, 2000, 2.1) +
              mast("m9", 960, 1200, .8) + vbadge("b9", 260, 860, "45:00", "#e63946", wd=340, vis=False))
# --- BAECK (s10a): ganze Stadt rechnet / TAUBE (s10b)
S["BAECK"] = (room_bg("#fefae0", "#dda15e", win=False) + txt(540, 400, "BÄCKEREI", 110, "#bc6c25") + '<rect x="0" y="1300" width="1080" height="160" fill="#bc6c25" stroke="#111" stroke-width="7"/>' +
              fig(person("bk", "lena", "#6b3e26", "#fff", skin="#c68642", exprs=("smug",), start="smug", arm=("front", "front")), 540, 1300, 1.2) +
              '<g transform="translate(540 1330)"><rect x="-260" y="-60" width="520" height="110" rx="55" fill="#e9c46a" stroke="#111" stroke-width="7"/>' + "".join(f'<path d="M{-195 + k * 65} -60 V50" stroke="#111" stroke-width="6"/>' for k in range(7)) + '</g>' +
              sign("ach", 540, 1600, 360, 140, ["8 × ⅛"], col="#fff", size=90))
S["TAUBE"] = ('<rect width="1080" height="1920" fill="#e9d8a6"/>' + "".join(f'<rect x="{(k * 173) % 1060}" y="{(k * 97) % 1900}" width="8" height="8" rx="4" fill="#bb9457" opacity=".6"/>' for k in range(60)) +
              f'<g id="frac" opacity="0">{txt(540, 1550, "½ + ½ = 1", 150, "#6b4226")}</g>' + pigeon("pg10", 720, 1300, 1.2) + '<rect id="ok10" opacity="0" x="0" y="0" width="0" height="0"/>' +
              sign("tok", 540, 1780, 260, 120, ["✅"], col="#2dc653", size=80, vis=False))
# --- AUTO (s11): Bürgermeister im Dienstwagen / TUNNEL (s12)
CAR = lambda uid, inner: (f'<g id="{uid}"><rect x="-420" y="-200" width="840" height="200" rx="50" fill="#111" stroke="#000" stroke-width="7"/><path d="M-260 -200 L-180 -360 H200 L300 -200 Z" fill="#111" stroke="#000" stroke-width="7"/>'
                          f'<path d="M-230 -210 L-165 -340 H185 L265 -210 Z" fill="#bde0fe"/>{inner}<rect x="-420" y="-120" width="840" height="24" fill="#ffd166"/>'
                          '<rect x="-330" y="-40" width="130" height="130" rx="65" fill="#333" stroke="#000" stroke-width="7"/><rect x="200" y="-40" width="130" height="130" rx="65" fill="#333" stroke="#000" stroke-width="7"/>'
                          '<rect x="370" y="-180" width="40" height="40" rx="10" fill="#fff8d6"/><path d="M-200 -380 V-430 M-200 -430 H-120 V-400 H-200" stroke="#111" stroke-width="6" fill="#e63946"/></g>')
mayor_in = f'<g clip-path="url(#carwin)">' + fig(bgm_("bm11", "determined", arm=("down", "mic"), extra=PHONE_M), 20, 40, .7) + '</g>'
S["AUTO"] = (bus_bg() + '<defs><clipPath id="carwin"><path d="M-230 -210 L-165 -340 H185 L265 -210 Z"/></clipPath></defs>' +
             '<g transform="translate(540 1500) scale(1.0)">' + CAR("car11", mayor_in) + '</g>')
S["TUNNEL"] = ('<rect width="1080" height="1920" fill="#8ecae6"/><path d="M0 1700 Q0 600 540 600 Q1080 600 1080 1700 Z" fill="#6c757d" stroke="#111" stroke-width="10"/>' +
               '<rect x="-200" y="500" width="400" height="1300" fill="#90be6d"/><path d="M500 1700 Q500 900 800 900 Q1080 900 1080 1700 Z" fill="#111"/>' +
               '<rect y="1700" width="1080" height="220" fill="#495057"/>' + txt(800, 860, "TUNNEL", 60, "#fff") +
               '<g id="carT" transform="translate(150 1700) scale(.55)">' + CAR("car12", "") + '</g>' + mast("m12", 260, 1700, .9) +
               f'<g id="static" opacity="0">' + "".join(f'<rect x="{(k * 131) % 1060}" y="{300 + (k * 89) % 1300}" width="{30 + (k * 7) % 60}" height="8" fill="#fff" opacity=".8"/>' for k in range(70)) + '</g>' +
               bubble("bub12", ["KRRRRRR …"], 540, 700, 520, tail=(-1, 1), size=80))
# --- STAR (s13): Oma als Star mit Kopfhörern und Profi-Mikro, Fanmeile
HEADP = '<path d="M-110 -40 Q-110 -150 0 -150 Q110 -150 110 -40" stroke="#111" stroke-width="18" fill="none"/><rect x="-130" y="-50" width="44" height="90" rx="16" fill="#e63946" stroke="#111" stroke-width="5"/><rect x="86" y="-50" width="44" height="90" rx="16" fill="#e63946" stroke="#111" stroke-width="5"/>'
MIC = '<g transform="translate(-60 -330)"><rect x="-10" y="0" width="20" height="200" fill="#333"/><rect x="-44" y="-110" width="88" height="120" rx="40" fill="#555" stroke="#111" stroke-width="6"/></g>'
fans = "".join(f'<g transform="translate({x} 1900)">' + fig(tiny(f"fn{k}", k, "laugh", arm=("up", "up")), 0, 0, .55) + f'<g transform="translate(0 -420)"><rect x="-90" y="-50" width="180" height="70" rx="10" fill="#fff" stroke="#111" stroke-width="5"/>{txt(0, 2, "OMA 4EVER", 30, "#e63946")}</g></g>' for k, x in enumerate((110, 320, 540, 760, 970)))
S["STAR"] = ('<rect width="1080" height="1920" fill="#cdb4db"/><rect x="190" y="220" width="700" height="760" rx="20" fill="#3d2b1f" stroke="#111" stroke-width="12"/><rect x="220" y="250" width="640" height="700" fill="#ffd6a5"/>' +
             '<g clip-path="url(#winS)">' + fig(oma_("o13", "grin", arm=("front", "up"), extra=MIC.replace("translate(-60 -330)", "translate(130 -330)")), 540, 1300, 1.3).replace("<g transform=\"translate(0 -400)\">", "<g transform=\"translate(0 -400)\">", 1) + '</g>' +
             '<defs><clipPath id="winS"><rect x="220" y="250" width="640" height="700"/></clipPath></defs>' +
             f'<g transform="translate(540 1300) scale(1.3)"><g transform="translate(0 -400)">{HEADP}</g></g>' +
             '<rect y="980" width="1080" height="940" fill="#adb5bd"/>' + fans +
             f'<g id="fanc"><rect x="290" y="1010" width="500" height="120" rx="30" fill="#111" stroke="#fff" stroke-width="6"/><text id="fct" x="540" y="1092" text-anchor="middle" style="font:900 70px {FONT};fill:#ffd166">0 FANS</text></g>')
# --- WERB (s14): Krause mit Werbeschild
S["WERB"] = ('<rect width="1080" height="1920" fill="#ffd166"/>' + "".join(f'<path d="M540 900 L{540 + 1400 * __import__("math").cos(k * .5236):.0f} {900 + 1400 * __import__("math").sin(k * .5236):.0f}" stroke="#ffbe0b" stroke-width="90"/>' for k in range(12)) +
             fig(krause_("k14", "wink", arm=("up", "up"), exprs=("wink", "smug")), 540, 2150, 1.7) +
             sign("ad", 540, 800, 820, 300, ["MATHE-NACHHILFE", "KRAUSE ✏️"], col="#fff", size=74))
# --- WALK (s15): ich laufe stolz, Masten schweigen
S["WALK"] = ('<rect width="1080" height="1920" fill="#8ecae6"/><g id="wbg">' + street_bg().replace('<rect width="1080" height="1920" fill="#8ecae6"/>', '') + mast("m15a", 300, 1300, .9) + mast("m15b", 900, 1300, .9) +
             '<g transform="translate(1080 0)">' + street_bg().replace('<rect width="1080" height="1920" fill="#8ecae6"/>', '') + mast("m15c", 500, 1300, .9) + '</g></g>' +
             txt(300, 600, "zzz", 70, "#555") + txt(900, 600, "zzz", 70, "#555") +
             '<g id="walker">' + fig(ich_("i15", "smug", arm=("hip", "front"), extra=PHONE_R), 540, 1650, 1.7) + '</g>' + vbadge("b15", 540, 600, "0:59 – IMMER", "#2dc653", wd=600, vis=False, size=76))
# --- KNACK (s16): alle Masten drehen sich, Ladebalken
S["KNACK"] = ('<rect width="1080" height="1920" fill="#5e6472"/>' + street_bg(night=False).replace('#8ecae6', '#9aa5b1') + mast("m16a", 160, 1500, 1.1) + mast("m16b", 540, 1350, 1.1) + mast("m16c", 920, 1500, 1.1) +
              '<g id="bolts" opacity="0">' + "".join(f'<path d="M{x} 520 L{x + 40} 600 L{x - 10} 620 L{x + 50} 720" stroke="#ffd166" stroke-width="12" fill="none"/>' for x in (130, 510, 890)) + '</g>' +
              '<g transform="translate(540 1650)"><rect x="-380" y="-70" width="760" height="140" rx="30" fill="#111" stroke="#fff" stroke-width="6"/>' + txt(0, -10, "WIRD ABGESPIELT …", 50, "#fff") +
              '<rect x="-330" y="20" width="660" height="30" rx="15" fill="#333"/><rect id="lb16" x="-330" y="20" width="0" height="30" rx="15" fill="#e63946"/></g>')
# --- ANZ (s17a): Riesen-Anzeige am Rathaus / SCHOCK (s17b)
S["ANZ"] = ('<rect width="1080" height="1920" fill="#dde5b6"/><rect x="60" y="400" width="960" height="1300" fill="#f8f9fa" stroke="#111" stroke-width="8"/><path d="M40 410 L540 200 L1040 410 Z" fill="#ced4da" stroke="#111" stroke-width="8"/>' +
            txt(540, 370, "RATHAUS", 64) + '<rect x="120" y="480" width="840" height="760" rx="20" fill="#111" stroke="#333" stroke-width="12"/>' +
            f'<g transform="translate(540 780) scale(1.2)"><rect x="-96" y="-96" width="192" height="192" rx="26" fill="#f2c9a5" stroke="#111" stroke-width="5"/>{HAIR["ich"]("#6b3e26")}{FACES["neutral"]}</g>' +
            txt(540, 1130, "ICH · 6:00:00", 110, "#e63946") + '<rect y="1700" width="1080" height="220" fill="#adb5bd"/>' + "".join(fig(tiny(f"az{k}", k, "shock", arm=("down", "down")), 150 + k * 260, 1900, .45) for k in range(4)))
S["SCHOCK"] = (street_bg() + fig(ich_("i17", "shock", arm=("down", "front"), extra='<g id="ice" transform="translate(196 -330)"><path d="M-30 -10 L0 80 L30 -10 Z" fill="#e9c46a" stroke="#111" stroke-width="4"/><rect x="-34" y="-70" width="68" height="64" rx="30" fill="#ff8fab" stroke="#111" stroke-width="4"/></g>'), 540, 2000, 2.0))
# --- XRAY (s18): Röntgenblick in die Hosentasche
S["XRAY"] = ('<rect width="1080" height="1920" fill="#0b132b"/>' + "".join(f'<rect x="0" y="{k * 12}" width="1080" height="3" fill="#4cc9f0" opacity=".06"/>' for k in range(160)) +
             '<path d="M140 300 H940 V1700 Q540 1800 140 1700 Z" fill="none" stroke="#4cc9f0" stroke-width="12" opacity=".7"/>' +
             '<g transform="translate(540 1050) rotate(-8)"><rect x="-180" y="-340" width="360" height="680" rx="50" fill="none" stroke="#bde0fe" stroke-width="14"/><rect x="-140" y="-280" width="280" height="540" rx="20" fill="#4cc9f0" opacity=".25"/>'
             '<g id="rec"><rect x="-70" y="-70" width="140" height="140" rx="70" fill="#e63946"/></g>' + txt(0, 160, "REC", 70, "#e63946") + '</g>' +
             '<path d="M700 1300 q80 -60 140 0 q-40 80 -140 0" fill="none" stroke="#bde0fe" stroke-width="10" opacity=".7"/>' + txt(780, 1440, "TASCHENTUCH", 34, "#bde0fe"))
# --- BEAT (s19): Rückblende Bus / LACH (Gegenwart)
S["BEAT"] = (f'<defs>{SEPIA}</defs><g filter="url(#sepia)">' + '<rect width="1080" height="1920" fill="#ffd60a"/><rect x="60" y="300" width="960" height="700" rx="40" fill="#bde0fe" stroke="#111" stroke-width="12"/>' +
             fig(ich_("i19", "grin", arm=("mic", "front")), 540, 1750, 1.9) + bubble("bub19", ["BUM-TSS-KA!"], 660, 640, 540, tail=(-1, 1), size=80) +
             '<rect y="1400" width="1080" height="520" fill="#264653" opacity=".2"/></g>' + f'<rect x="330" y="1640" width="420" height="90" rx="20" fill="#000" opacity=".6"/>{txt(540, 1705, "HEUTE FRÜH", 56, "#f1e3c4")}')
S["LACH"] = (street_bg() + fig(emil("e19", "laugh", arm=("hip", "hip"), exprs=("laugh",)), 380, 1650, 1.6) + duck("d19", 820, 1650, 1.2) +
             f'<g transform="translate(820 1300)"><rect x="-70" y="-60" width="140" height="80" rx="20" fill="#fff" stroke="#111" stroke-width="5"/>{txt(0, 2, "QUAK!", 40)}</g>')
# --- GEHEIM (s20): Zoom auf den Lautsprecher, Krause lauscht, Ladebalken 99 %
S["GEHEIM"] = ('<rect width="1080" height="1920" fill="#3d405b"/>' + street_bg(night=True) + mast("m20", 540, 1250, 1.5) +
               fig(krause_("k20", "shock", arm=("down", "down"), exprs=("shock",)), 180, 1960, 1.1) + fig(emil("e20", "shock", arm=("down", "down"), exprs=("shock",)), 900, 1960, 1.1) +
               bubble("bub20", ["OKAY, KEINER HÖRT ZU …"], 540, 620, 820, tail=(0, 1), size=58) +
               '<g transform="translate(540 1400)"><rect x="-380" y="-70" width="760" height="140" rx="30" fill="#111" stroke="#fff" stroke-width="6"/>' +
               f'<text id="g20t" x="0" y="-10" text-anchor="middle" style="font:900 50px {FONT};fill:#fff">GEHEIMNIS … 0 %</text><rect x="-330" y="20" width="660" height="30" rx="15" fill="#333"/><rect id="lb20" x="-330" y="20" width="0" height="30" rx="15" fill="#e63946"/></g>')
# --- REGLER (s21): Oma dreht lauter
S["REGLER"] = ('<rect width="1080" height="1920" fill="#cdb4db"/>' + fig(oma_("o21", "smug", arm=("front", "front"), exprs=("smug", "wink")), 540, 1850, 2.0) +
               '<g transform="translate(540 1650)"><rect x="-400" y="-60" width="800" height="300" rx="30" fill="#343a40" stroke="#111" stroke-width="8"/>' +
               '<g id="knob"><rect x="-130" y="-130" width="260" height="260" rx="130" fill="#adb5bd" stroke="#111" stroke-width="10"/><rect x="-14" y="-125" width="28" height="90" rx="10" fill="#e63946"/></g>' +
               txt(-280, 140, "LEISE", 40, "#fff") + txt(280, 140, "LAUT 🔊", 40, "#fff") + '</g>')
# --- TIPP (s22): ich mit Schild MEIN GEHEIMNIS: ___?
S["TIPP"] = (street_bg(night=True) + mast("m22a", 140, 1250, 1.0) + mast("m22b", 940, 1250, 1.0) + fig(ich_("i22", "panic", arm=("front", "front"), exprs=("panic",)), 540, 1850, 1.9) +
             sign("st22", 540, 1500, 800, 260, ["MEIN GEHEIMNIS:", "___ ?"], col="#fff", size=82))

# ---------- Zeitplan ----------
J.append('tl.set("#cam", { x: 0, y: 0, scale: 1, svgOrigin: "0 0" }, 0);')
t = {k: st(k) for k in T}
VM = []  # Sprachnachrichten-Leiste (Zeit, Absender, Zeit, Farbe)
# s1 Hook: Split-Bild, Punch-Zoom, Schnitt bei 1,5 s auf den Mast hinter Oma
cut(0, 540, 960, 1.08); cam(.02, 540, 960, 1.0, .35, "power3.out"); FX += [("hit", 0, .5, .8)]
pop("#bia", .05, .25, "50% 50%"); pop("#boa", .2, .25, "50% 50%")
J.append(f'tl.set("#ma-w", {{ opacity: 1 }}, 0); tl.to("#ma-w", {{ opacity: .2, duration: .15, yoyo: true, repeat: {int(t["s2"] / .15)} }}, 0);')
for k in range(3): J.append(f'tl.to("#cra{k}", {{ x: {(-1) ** k * 10}, duration: .1, yoyo: true, repeat: 20 }}, 0);')
c1 = 1.5
cut(c1, 860, 1300, 1.7); cam(c1 + .05, 860, 1250, 1.85, 1.4, "none"); FX += [("whoosh", c1, .3, .4)]
tls = w("s1", "Lautsprecher")
cut(tls - .1, 540, 960, 1.0)
VM += [(0, "ICH", "0:59", "#2dc653")]
# s2 Reißschwenk ich -> Oma
t2 = t["s2"]
cut(t2, 320, 1200, 1.15); FX += [("whoosh", t2, .3, .4)]
tom = w("s2", "Oma:") - .2
J.append(f'tl.fromTo("#cam", {{ x: {-(0)} }}, {{ x: -1180, duration: .45, ease: "power3.inOut", immediateRender: false }}, {F(tom)});'); CUTS.append(tom); FX += [("swoosh", tom, .4, .4)]
J.append(f'tl.fromTo("#owave", {{ x: 0 }}, {{ x: -900, duration: 2.5, ease: "none", immediateRender: false }}, {F(tom + .3)});')
VM += [(tom, "OMA", "14:00", "#e63946")]
# s3 Marktplatz
t3 = t["s3"]
J.append(f'tl.set("#cam", {{ x: 0 }}, {F(t3)});')
cut(t3, 600, 1300, 1.3); cam(t3 + .05, 540, 1100, 1.1, 1.6, "none"); J.append('tl.set("#bub3", { opacity: 0 }, 0);'); pop("#bub3", w("s3", "Hallo") - .1, .2, "50% 50%")
J.append(f'tl.set("#m3-w", {{ opacity: 1 }}, {F(t3)}); tl.to("#m3-w", {{ opacity: .2, duration: .15, yoyo: true, repeat: 30 }}, {F(t3)});')
tdr = w("s3", "Dann") - .1
hide("#bub3", tdr, .1); cut(tdr, 540, 900, 1.0)
J.append(f'tl.set("#icons", {{ opacity: 1 }}, {F(tdr)}); tl.fromTo("#icons .ic", {{ x: -700 }}, {{ x: 900, duration: 2.4, ease: "none", stagger: .15, immediateRender: false }}, {F(tdr)});')
pop("#rez", w("s3", "Kartoffelsalat-Rezept.") - .2, .25, "50% 50%"); FX += [("pop", w("s3", "Kartoffelsalat-Rezept.") - .2, .5, .3)]
VM += [(tdr, "OMA", "3:00 🥔", "#e63946")]
# s4 Stadt bleibt stehen / Busfahrer schreibt mit
t4 = t["s4"]
cut(t4, 540, 1300, 1.1); pop("#stop", t4 + .3, .2, "50% 50%"); FX += [("hit", t4 + .3, .4, .5)]
tbf = w("s4", "Der") - .1
cut(tbf, 540, 1250, 1.2); cam(tbf + .05, 560, 1250, 1.5, 1.4, "none")
J.append(f'tl.fromTo("#note", {{ rotation: -10 }}, {{ rotation: -4, duration: .2, yoyo: true, repeat: 7, immediateRender: false }}, {F(tbf)});'); FX += [("tick", tbf, .3, 1.0)]
VM += [(t4, "OMA", "3:12 / 14:00", "#e63946")]
# s5 Profi
t5 = t["s5"]
cut(t5, 540, 1200, 1.0); cam(t5 + .05, 450, 1100, 1.15, 1.6, "none")
J.append(f'tl.fromTo("#hand5", {{ rotation: 0, transformOrigin: "50% 100%" }}, {{ rotation: 354, duration: {F(max(.5, w("s5", "loslassen.") - t5 - .3))}, ease: "none", immediateRender: false }}, {F(t5 + .2)});')
tlos = w("s5", "loslassen.") - .1
settext("sw5", (t5 + tlos) / 2, "0:58", "0:57"); settext("sw5", tlos, "0:59", "0:58")
pop("#b5", tlos, .25, "50% 50%"); FX += [("chime", tlos, .4, .8)]; expr("i5", "determined", "smug", tlos)
cut(tlos, 540, 1000, 1.0)
VM += [(t5, "ICH", "0:59 ✅", "#2dc653")]
# s6 Emil: 1:01
t6 = t["s6"]
cut(t6, 540, 1300, 1.25); expr("e6", "happy", "neutral", t6)
tem = w("s6", "Eine") - .1
cut(tem, 540, 1000, 1.25); cam(tem + .05, 540, 1050, 1.4, 1.0, "none")
J.append(f'tl.to("#pt6", {{ opacity: .15, duration: .15, yoyo: true, repeat: 9, ease: "steps(1)" }}, {F(tem + .2)});'); FX += [("glitch", tem + .2, .4, .6)]
tsec = w("s6", "Sekunde.") + .2
temil = round(min(tsec, t["s7"] - .6), 2)
cut(temil, 540, 1250, 1.3); expr("e6", "neutral", "shock", temil); J.append(f'tl.set("#alarm", {{ opacity: 1 }}, {F(temil)}); tl.to("#alarm", {{ opacity: 0, duration: .2, yoyo: true, repeat: 5 }}, {F(temil)});')
J.append(f'tl.to("#m6a", {{ rotation: 25, duration: .3 }}, {F(temil)}); tl.to("#m6b", {{ rotation: -25, duration: .3 }}, {F(temil)});'); FX += [("hit", temil, .5, .6)]
VM += [(tem, "EMIL", "1:01 ❌", "#e63946")]
# s7 ganze Stadt hört
t7 = t["s7"]
cut(t7, 540, 1300, 1.0); J.append('tl.set("#bub7", { opacity: 0 }, 0);'); pop("#bub7", w("s7", "Mama,") - .1, .2, "50% 50%")
J.append(f'tl.set("#m7-w", {{ opacity: 1 }}, {F(t7)}); tl.to("#m7-w", {{ opacity: .2, duration: .15, yoyo: true, repeat: 20 }}, {F(t7)});')
for k in range(6): J.append(f'tl.fromTo("#tc{k}", {{ scaleX: 1 }}, {{ scaleX: -1, transformOrigin: "50% 50%", duration: .15, immediateRender: false }}, {F(w("s7", "Mama,") + k * .05)});')
expr("e7", "neutral", "panic", w("s7", "Enten.") - .3)
cut(w("s7", "Angst") - .1, 540, 1150, 2.4); FX += [("boing", w("s7", "Angst") - .1, .4, .3)]
# s8 Ente vor der Tür – Tür zu, Tür auf: zwei Enten
t8 = t["s8"]
cut(t8, 540, 1300, 1.0)
J.append(f'tl.set("#door8", {{ scaleX: 0, transformOrigin: "0% 50%" }}, 0); tl.set("#door8", {{ scaleX: 0 }}, {F(t8)});')
expr("e8", "neutral", "shock", w("s8", "Ente") - .1)
cut(w("s8", "Ente") - .1, 460, 1650, 1.8); FX += [("boing", w("s8", "Ente"), .4, .3)]
tz8 = w("s8", "Tür.") - .2
J.append(f'tl.to("#door8", {{ scaleX: 1, duration: .2, ease: "power2.in" }}, {F(tz8)}); tl.to("#door8", {{ scaleX: 0, duration: .25 }}, {F(tz8 + .7)}); tl.set("#d2", {{ opacity: 1 }}, {F(tz8 + .4)});')
expr("e8", "shock", "sad", tz8 + .7); cut(tz8, 540, 1300, 1.0); FX += [("klong", tz8 + .2, .4, .5), ("pop", tz8 + .9, .4, .3)]
# s9 Krause schickt Matheunterricht
t9 = t["s9"]
cut(t9, 540, 1250, 1.2); cam(t9 + .05, 540, 1200, 1.35, 1.6, "none")
tsch = w("s9", "schickt") - .1
cut(tsch, 600, 900, 1.0); J.append(f'tl.set("#m9-w", {{ opacity: 1 }}, {F(tsch)}); tl.to("#m9-w", {{ opacity: .2, duration: .15, yoyo: true, repeat: 15 }}, {F(tsch)});')
t45 = w("s9", "Fünfundvierzig") - .1
pop("#b9", t45, .25, "50% 50%"); cut(t45, 400, 1150, 1.3); FX += [("pop", t45, .5, .3)]; expr("k9", "smug", "determined", t45)
VM += [(tsch, "KRAUSE", "45:00", "#e63946")]
# s10 Bruchrechnen – Bäckerin / Taube
t10 = t["s10"]
cut(t10, 540, 1200, 1.1); FX += [("whoosh", t10, .3, .4)]
tsog = w("s10", "Sogar") - .1
cut(tsog, 600, 1300, 1.0); cam(tsog + .05, 600, 1400, 1.15, 1.0, "none")
J.append(f'tl.to("#pg10-in", {{ rotation: -14, transformOrigin: "-60% -40%", duration: .12, yoyo: true, repeat: 7 }}, {F(tsog)}); tl.fromTo("#frac", {{ opacity: 0 }}, {{ opacity: 1, duration: .6, immediateRender: false }}, {F(tsog + .2)});')
pop("#tok", w("s10", "Tauben.") + .1, .25, "50% 50%"); FX += [("chime", w("s10", "Tauben.") + .1, .4, .8)]
# s11 Bürgermeister im Auto
t11 = t["s11"]
cut(t11, 540, 1300, 1.1); cam(t11 + .05, 560, 1250, 1.45, 1.8, "none")
cut(w("s11", "Per") - .1, 560, 1200, 1.8)
# s12 Tunnel – Rauschen
t12 = t["s12"]
cut(t12, 540, 1200, 1.0)
J.append(f'tl.fromTo("#carT", {{ x: 0 }}, {{ x: 650, duration: 1.4, ease: "power1.in", immediateRender: false }}, {F(t12 + .2)});'); FX += [("whoosh", t12 + .6, .4, .6)]
J.append('tl.set("#bub12", { opacity: 0 }, 0);')
tkr = w("s12", "Krrrrr.") - .2
pop("#bub12", tkr - .3, .2, "50% 50%"); J.append(f'tl.set("#static", {{ opacity: 1 }}, {F(tkr - .3)}); tl.to("#static", {{ x: 30, duration: .05, yoyo: true, repeat: 30 }}, {F(tkr - .3)});')
J.append(f'tl.set("#m12-w", {{ opacity: 1 }}, {F(tkr - .3)});')
cut(tkr - .3, 400, 1100, 1.3); shake(tkr, 12, 10); FX += [("glitch", tkr - .3, .5, 1.2)]
VM += [(t11, "BÜRGERMEISTER", "2:00", "#e63946"), (tkr - .3, "BÜRGERMEISTER", "KRRRR", "#e63946")]
# s13 Oma ist Star
t13 = t["s13"]
cut(t13, 540, 700, 1.4); FX += [("riser", t13, .3, 1.0)]
tst = w("s13", "Jeden") - .1
cut(tst, 540, 650, 1.15)
tfan = w("s13", "Achtzigtausend") - .2
cut(tfan, 540, 1300, 1.0); count("fct", tfan, 0, 80000, .9, suffix=" FANS"); FX += [("pop", tfan, .4, .3), ("chime", tfan + .9, .4, .8)]
J.append(f'tl.to("#{",#".join(f"fn{k}" for k in range(5))}", {{ y: -30, duration: .2, yoyo: true, repeat: 7 }}, {F(tfan)});')
VM += [(t13, "OMA", "2:00:00", "#e63946")]
# s14 Werbung
t14 = t["s14"]
cut(t14, 540, 900, 1.0); cam(t14 + .05, 540, 900, 1.12, 1.6, "none"); J.append(f'tl.fromTo("#ad-in", {{ scale: 1.3, transformOrigin: "50% 50%" }}, {{ scale: 1, duration: .3, ease: "back.out(3)", immediateRender: false }}, {F(t14 + .1)});')
FX += [("chime", t14 + .1, .4, .6)]
cut(w("s14", "Herrn") - .1, 540, 1150, 1.3)
# s15 ich laufe stolz
t15 = t["s15"]
cut(t15, 540, 1200, 1.0)
J.append(f'tl.fromTo("#wbg", {{ x: 0 }}, {{ x: -1080, duration: {F(t["s16"] - t15)}, ease: "none", immediateRender: false }}, {F(t15)}); tl.to("#walker", {{ y: -16, duration: .2, yoyo: true, repeat: {int((t["s16"] - t15) / .2)} }}, {F(t15)});')
pop("#b15", w("s15", "Neunundfünfzig") - .1, .25, "50% 50%"); cut(w("s15", "Neunundfünfzig") - .1, 540, 1100, 1.15)
VM += [(t15, "ICH", "0:59", "#2dc653")]
# s16 Knacken
t16 = t["s16"]
cut(t16, 540, 1100, 1.0)
tkn = w("s16", "knacken") - .1
J.append(f'tl.set("#bolts", {{ opacity: 1 }}, {F(tkn)}); tl.to("#bolts", {{ opacity: 0, duration: .1, yoyo: true, repeat: 7 }}, {F(tkn)});')
for m in ("m16a", "m16b", "m16c"): J.append(f'tl.to("#{m}", {{ rotation: 360, duration: .7, ease: "power2.inOut" }}, {F(tkn)});')
J.append(f'tl.to("#lb16", {{ attr: {{ width: 600 }}, duration: {F(t["s17"] - t16)}, ease: "none" }}, {F(t16)});')
shake(tkn, 8, 12); FX += [("hit", tkn, .25, .5), ("glitch", w("s16", "Lautsprecher.") + .7, .35, .5)]; cut(tkn + .4, 540, 1300, 1.3)
VM += [(tkn, "???", "WIRD ABGESPIELT …", "#e63946")]
# s17 Absender: ich, 6 Stunden
t17 = t["s17"]
cut(t17, 540, 800, 1.35); FX += [("hit", t17, .4, .5)]
tlg = w("s17", "Länge:") - .1
cut(tlg, 540, 1100, 1.25)
tsx = w("s17", "sechs") - .1
cut(tsx, 540, 1200, 1.4); J.append(f'tl.to("#ice", {{ y: 600, rotation: 120, duration: .6, ease: "power2.in" }}, {F(tsx + .2)});'); FX += [("splat", tsx + .8, .4, .4)]
VM += [(t17, "ICH", "6:00:00", "#e63946")]
# s18 Röntgen Hosentasche
t18 = t["s18"]
cut(t18, 540, 1000, 1.0); cam(t18 + .05, 540, 1050, 1.3, 2.5, "none"); FX += [("glitch", t18, .3, .4)]
J.append(f'tl.to("#rec", {{ opacity: .2, duration: .3, yoyo: true, repeat: 9, ease: "steps(1)" }}, {F(t18)});')
cut(w("s18", "Hosentasche") - .1, 600, 1150, 1.6)
# s19 Beatbox – Rückblende, dann Emil + Ente lachen
t19 = t["s19"]
cut(t19, 540, 1200, 1.15); J.append(f'tl.to("#bub19-in", {{ scale: 1.1, transformOrigin: "50% 50%", duration: .12, yoyo: true, repeat: 9 }}, {F(t19 + .2)});'); J.append(f'tl.set("#bub19", {{ opacity: 1 }}, {F(t19)});')
FX += [("tick", t19 + .2, .3, .8)]
tsl = w("s19", "Schlecht.") - .1
cut(tsl, 540, 1300, 1.1); J.append(f'tl.to("#e19, #d19", {{ y: -20, duration: .12, yoyo: true, repeat: 9 }}, {F(tsl)});'); FX += [("boing", tsl, .4, .3)]
# s20 Geheimnis – Ladebalken 99 %
t20 = t["s20"]
cut(t20, 540, 1000, 1.1); cam(t20 + .05, 540, 850, 1.6, t["s21"] - t20, "power1.in")
J.append('tl.set("#bub20", { opacity: 0 }, 0);'); pop("#bub20", w("s20", "Okay,") - .1, .2, "50% 50%")
tgh = w("s20", "Zeit") - .1
J.append(f'tl.to("#lb20", {{ attr: {{ width: 653 }}, duration: {F(t["s21"] - tgh)}, ease: "power2.out" }}, {F(tgh)});')
for k, p in enumerate((25, 50, 75, 99)): settext("g20t", tgh + k * (t["s21"] - tgh) / 4, f"GEHEIMNIS … {p} %", f"GEHEIMNIS … {(0, 25, 50, 75)[k]} %")
FX += [("wirbel", tgh, .5, min(3.0, t["s21"] - tgh + .5))]
VM += [(tgh, "ICH", "GEHEIMNIS … 99 %", "#e63946")]
# s21 Oma dreht lauter
t21 = t["s21"]
cut(t21, 540, 1500, 1.6); J.append(f'tl.to("#knob", {{ rotation: 150, transformOrigin: "50% 50%", duration: .8, ease: "power2.inOut" }}, {F(t21 + .2)});'); FX += [("riser", t21, .4, 1.2)]
cut(t21 + 1.1, 540, 1050, 1.15); expr("o21", "smug", "wink", t21 + 1.1); FX += [("chime", t21 + 1.1, .4, .6)]
VM += [(t21 + .2, "ICH", "🔊 LAUTER", "#e63946")]
# s22 Tipp
t22 = t["s22"]
cut(t22, 540, 1050, 1.15); cam(t22 + .05, 540, 1050, 1.25, 2.0, "none"); FX += [("whoosh", t22, .3, .4)]
J.append(f'tl.set("#m22a-w, #m22b-w", {{ opacity: 1 }}, {F(t22)}); tl.to("#m22a-w, #m22b-w", {{ opacity: .2, duration: .15, yoyo: true, repeat: 20 }}, {F(t22)});')
J.append(f'tl.to("#st22-in", {{ scale: 1.05, transformOrigin: "50% 50%", duration: .3, yoyo: true, repeat: 5 }}, {F(w("s22", "Schreib"))});')
# s23 Loop – zurück zum Split-Bild, jetzt mit 6:00:00 über mir
t23 = t["s23"]
cut(t23, 270, 1100, 1.6); cam(t23 + .3, 540, 960, 1.0, 1.2, "power2.inOut"); FX += [("whoosh", t23, .3, .4)]
J.append(f'tl.set("#mz-w", {{ opacity: 1 }}, {F(t23)});')
tEND = round(END - 1.5, 2)

sets = [("SPLIT", 0, t2), ("S2", t2, t3), ("MARKT", t3, t4), ("FREEZE", t4, tbf), ("BUS", tbf, t5), ("PROFI", t5, t6), ("EMIL", t6, tem), ("PHONE", tem, temil), ("EMIL", temil, t7),
        ("TURN", t7, t8), ("DOOR", t8, t9), ("MATHE", t9, t10), ("BAECK", t10, tsog), ("TAUBE", tsog, t11), ("AUTO", t11, t12), ("TUNNEL", t12, t13), ("STAR", t13, t14), ("WERB", t14, t15),
        ("WALK", t15, t16), ("KNACK", t16, t17), ("ANZ", t17, tsx), ("SCHOCK", tsx, t18), ("XRAY", t18, t19), ("BEAT", t19, tsl), ("LACH", tsl, t20), ("GEHEIM", t20, t21), ("REGLER", t21, t22),
        ("TIPP", t22, t23), ("LOOP", t23, END)]

# Sprachnachrichten-Leiste oben links (Dauer-Element)
bars = "".join(f'<div style="display:inline-block;width:7px;margin-right:4px;height:{10 + (k * 37) % 26}px;background:currentColor;border-radius:3px;vertical-align:middle"></div>' for k in range(12))
vm_html = (f'<div id="vm" class="ui" style="left:24px;top:34px;background:#111;border:5px solid #fff;border-radius:40px;padding:8px 22px 8px 14px;font:900 34px Inter,sans-serif;color:#fff;white-space:nowrap">'
           f'<span style="display:inline-block;width:44px;height:44px;border-radius:22px;background:#2dc653;text-align:center;line-height:44px;font-size:24px;vertical-align:middle">▶</span> '
           f'<span id="vmc" style="color:#2dc653">{bars}</span> <span id="vmn" style="vertical-align:middle">ICH</span> <span id="vmt" style="color:#2dc653;vertical-align:middle">0:59</span></div>')
pn, pt, pc = "ICH", "0:59", "#2dc653"
for tt, n, tm, col in VM[1:]:
    if n != pn: settext("vmn", tt, n, pn); pn = n
    if tm != pt: settext("vmt", tt, tm, pt); pt = tm
    if col != pc: J.append(f'tl.set("#vmt, #vmc", {{ color: "{col}" }}, {F(tt)});'); pc = col
    J.append(f'tl.fromTo("#vm", {{ scale: 1.15, transformOrigin: "0% 0%" }}, {{ scale: 1, duration: .25, ease: "back.out(3)", immediateRender: false }}, {F(tt)});')
J.append(f'tl.set("#vmt, #vmc", {{ color: "#2dc653" }}, 0);')
J.append(f'tl.to("#vmc", {{ opacity: .4, duration: .2, yoyo: true, repeat: {int(END / .2)}, ease: "steps(1)" }}, 0);')
tag = f'<div class="ui clip" data-start="0" data-duration="{F(END)}" style="right:24px;top:40px;font:900 30px Inter,sans-serif;color:#fff;background:rgba(0,0,0,.55);padding:6px 14px;border-radius:12px">TEIL 1</div>'
R = "<span style='color:#ff4d5a'>"; G_ = "<span style='color:#2dc653'>"; X = "</span>"
OBEN = [(0, f"ÜBER 1 MIN = {R}ALLE HÖREN MIT{X}"), (t2, f"{G_}0:59{X} vs {R}14:00{X}"), (t3, "3:00 KARTOFFELSALAT"), (t4, "3:12 / 14:00"), (t5, f"PROFI: {G_}0:59{X}"),
        (t6, f"{R}1:01 ❌{X}"), (t7, "🦆 ANGST?"), (t8, "1 ENTE"), (tz8 + .4, "2 ENTEN"), (t9, "45:00 MATHE"), (t10, "½ + ½ = 1"), (t11, "GESETZ WEG?"), (t12, "2:00 RAUSCHEN"),
        (t13, "FANS: 80.000"), (t14, "WERBUNG"), (t15, f"{G_}0:59{X} – IMMER"), (t16, "NEUE NACHRICHT …"), (t17, f"ICH: {R}6:00:00{X}"), (t18, "HOSENTASCHE 🎙️"),
        (t19, "BEATBOX: 2/10"), (t20, "GEHEIMNIS … 99 %"), (t21, "🔊 LAUTER"), (t22, "DEIN TIPP: ___?"), (t23, f"ICH: {R}6:00:00{X}")]
HOT = {"SPRACHNACHRICHT", "LAUTSPRECHER", "OMA", "EMIL", "ENTEN", "ENTE", "TUNNEL", "FANS", "ICH", "GEHEIMNIS", "STUNDEN", "LAUTER", "SCHLECHT", "KRRRRR", "TIPP", "SEKUNDE", "MINUTE"}
from clampcam import clamp_cam; clamp_cam(J)  # tools/clampcam.py
finish(S, sets, OBEN, FX, HOT, tag, extra_ui=vm_html, banner=("TEIL 2?", "➕ FOLGEN"), oben_top=150, cap_top=1150, banner_top=360)

# Endbanner einzeilig halten
_h = open("compositions/welt.html", encoding="utf-8").read()
_h = _h.replace("padding:14px 40px;font:900 96px/1 Inter", "padding:14px 30px;white-space:nowrap;font:900 84px/1 Inter")
open("compositions/welt.html", "w", encoding="utf-8").write(_h)
