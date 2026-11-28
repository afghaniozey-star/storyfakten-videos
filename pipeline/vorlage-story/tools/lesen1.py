"""STORY „In dieser Stadt …“ – NEUE SERIE „Lesebestätigungs-Stadt“, TEIL 1: Keine Nachricht bleibt über 10 Minuten unbeantwortet,
wer überzieht, trägt einen blauen Haken mit Minutenzahl über dem Kopf. Erzähler liest heimlich im Flugmodus -> Twist: 6 Tage.
Aufruf: /usr/bin/python3 tools/lesen1.py  (liest voice.json + assets/vo/timing.json; Bausteine aus tools/bausteine.py;
Musik = fester Hintergrund-Sound assets/bgm.mp3 über tools/story_musik.py)"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bausteine import *

# ---------- Mimik / Haare / Zubehör ----------
FACES["smug"] = '<path d="M-46 -6 H-14" stroke="#111" stroke-width="8" stroke-linecap="round"/>' + E(30, -5) + '<path d="M-24 34 Q4 48 30 28" stroke="#111" stroke-width="7" fill="none" stroke-linecap="round"/>'
FACES["braces"] = ('<path d="M-56 14 Q0 82 56 14 Z" fill="#fff" stroke="#111" stroke-width="4"/><path d="M-50 30 H50" stroke="#8d99ae" stroke-width="7"/>' +
                   "".join(f'<rect x="{x - 6}" y="24" width="12" height="12" fill="#adb5bd" stroke="#111" stroke-width="2"/>' for x in (-36, -14, 8, 30)) + E(-30, -10) + E(30, -10))
HAIR["ich"] = lambda c: f'<path d="M-100 -36 V-100 Q-100 -114 -86 -114 H86 Q100 -114 100 -100 V-36 L74 -64 L40 -80 L0 -66 L-40 -84 L-76 -62 Z" fill="{c}" stroke="#111" stroke-width="4"/>'
HAIR["topf"] = lambda c: f'<path d="M-112 10 V-80 Q-112 -128 -60 -128 H60 Q112 -128 112 -80 V10 H86 V-40 H-86 V10 Z" fill="{c}" stroke="#111" stroke-width="5"/><path d="M-86 -40 H86" stroke="#111" stroke-width="5"/>'
HAIR["jonas"] = lambda c: (f'<path d="M-100 -30 V-96 Q-100 -112 -84 -112 H84 Q100 -112 100 -96 V-30 L80 -70 H-80 Z" fill="{c}" stroke="#111" stroke-width="4"/>'
                           '<path d="M-104 -70 Q-104 -150 0 -150 Q104 -150 104 -70 Z" fill="#e63946" stroke="#111" stroke-width="5"/><rect x="-150" y="-86" width="90" height="26" rx="10" fill="#c1121f" stroke="#111" stroke-width="4"/>')
HAIR["hut"] = lambda c: '<path d="M-100 -30 V-90 L-80 -70 H80 L100 -90 V-30 Z" fill="#ccc"/><rect x="-140" y="-120" width="280" height="30" rx="10" fill="#111"/><rect x="-80" y="-250" width="160" height="140" rx="10" fill="#111"/><rect x="-80" y="-150" width="160" height="26" fill="#e63946"/>'
HAIR["cap"] = lambda c: f'<path d="M-104 -60 Q-104 -150 0 -150 Q104 -150 104 -60 Z" fill="{c}" stroke="#111" stroke-width="5"/><rect x="-20" y="-82" width="190" height="26" rx="10" fill="{c}" stroke="#111" stroke-width="4"/>'
OMA_ACC = '<rect x="-64" y="-20" width="46" height="34" rx="16" fill="none" stroke="#555" stroke-width="5"/><rect x="18" y="-20" width="46" height="34" rx="16" fill="none" stroke="#555" stroke-width="5"/>'
CURLERS = "".join(f'<rect x="{x - 22}" y="-132" width="44" height="34" rx="12" fill="{c}" stroke="#111" stroke-width="4"/>' for x, c in ((-60, "#ff8fab"), (0, "#4cc9f0"), (60, "#ffd166")))
SASH = '<path d="M-90 -290 L90 -80" stroke="#e63946" stroke-width="34"/><rect x="-24" y="-240" width="48" height="48" rx="24" fill="#ffd166" stroke="#111" stroke-width="4"/>'
PHONE_R = '<g transform="translate(196 -330)"><rect x="-30" y="-56" width="60" height="104" rx="12" fill="#222" stroke="#111" stroke-width="4"/><rect x="-22" y="-46" width="44" height="80" rx="6" fill="#8ecae6"/></g>'
TABLET = '<g transform="translate(196 -330)"><rect x="-70" y="-90" width="140" height="170" rx="16" fill="#222" stroke="#111" stroke-width="5"/><rect x="-58" y="-78" width="116" height="146" rx="8" fill="#cdb4db"/></g>'
EXI = ("happy", "smug", "shock", "panic", "determined", "neutral", "grin", "confused", "sad")
def ich_(uid, start="happy", arm=("down", "front"), extra=PHONE_R): return person(uid, "ich", "#6b3e26", "#118ab2", exprs=EXI, start=start, arm=arm, extra=extra)
EXM = ("happy", "grin", "determined", "laugh", "shock", "wink")
def mama(uid, start="happy", arm=("down", "front"), extra=PHONE_R): return person(uid, "lena", "#7f4f24", "#ff70a6", exprs=EXM, start=start, arm=arm, extra=extra)
def oma_(uid, start="happy", arm=("down", "front"), extra=TABLET): return person(uid, "oma", "#e0e0e0", "#9d4edd", exprs=("happy", "laugh", "grin", "wink", "smug"), start=start, arm=arm, head_acc=OMA_ACC + CURLERS, extra=extra)
def jonas(uid, start="happy", arm=("down", "front")): return person(uid, "jonas", "#f4d35e", "#06d6a0", exprs=("happy", "sad", "neutral", "panic"), start=start, arm=arm, extra=PHONE_R)
def bgm_(uid, start="determined", arm=("down", "mic"), extra=""): return person(uid, "hut", "#ccc", "#264653", exprs=("determined", "shock", "panic"), start=start, arm=arm, extra=SASH + extra)
def tiny(uid, k, ex="happy", arm=("down", "down"), exprs=None):
    hair = ("mann", "lena", "oma", "ich", "cap", "mann")[k % 6]
    hc = ("#3d2b1f", "#f4d35e", "#ddd", "#111", "#7b2cbf", "#2d6a4f")[k % 6]
    sh = ("#e76f51", "#3a86ff", "#9d4edd", "#06d6a0", "#ffbe0b", "#ef476f")[k % 6]
    return person(uid, hair, hc, sh, skin=("#f2c9a5", "#c68642", "#8d5524")[k % 3], exprs=exprs or (ex,), start=ex, arm=arm)
def txt(x, y, s, size=60, col="#111", anchor="middle", uid=""):
    i = f' id="{uid}"' if uid else ""
    return f'<text{i} x="{x}" y="{y}" text-anchor="{anchor}" style="font:900 {size}px {FONT};fill:{col}">{s}</text>'
def sign(uid, x, y, wd, h, lines, col="#fff", fg="#111", size=70, vis=True, rot=0):
    t = "".join(txt(0, -h / 2 + 30 + (k + .85) * size * 1.15 - 10, l, size, fg) for k, l in enumerate(lines))
    return (f'<g id="{uid}" opacity="{1 if vis else 0}" transform="translate({x} {y}) rotate({rot})"><g id="{uid}-in"><rect x="{-wd/2 + 8}" y="{-h/2 + 8}" width="{wd}" height="{h}" rx="26" fill="#000" opacity=".25"/>'
            f'<rect x="{-wd/2}" y="{-h/2}" width="{wd}" height="{h}" rx="26" fill="{col}" stroke="#111" stroke-width="8"/>{t}</g></g>')
def zaehler(uid, x, y, val, s=1.0, col="#2dc653", vis=True):
    return (f'<g id="{uid}" opacity="{1 if vis else 0}" transform="translate({x} {y}) scale({s})"><g id="{uid}-in"><rect x="-290" y="-110" width="580" height="220" rx="26" fill="#111" stroke="#e63946" stroke-width="12"/>'
            f'<text x="-250" y="-62" style="font:900 34px {FONT};fill:#aaa">💬 HEUTE</text>'
            f'<text id="{uid}-t" x="0" y="80" text-anchor="middle" style="font:900 120px {FONT};fill:{col}">{val}</text></g></g>')
def setz(uid, t, val, prev, col=None):
    settext(f"{uid}-t", t, val, prev)
    if col: J.append(f'tl.set("#{uid}-t", {{ fill: "{col}" }}, {F(t)});')
def mast(uid, x, y, s=1.0):
    horn = lambda dx: (f'<g transform="translate({dx} -560)"><path d="M0 -30 L130 -90 V90 L0 30 Z" fill="#adb5bd" stroke="#111" stroke-width="7"/>'
                       f'<rect x="-40" y="-36" width="50" height="72" rx="10" fill="#6c757d" stroke="#111" stroke-width="6"/><rect x="120" y="-90" width="22" height="180" rx="8" fill="#ced4da" stroke="#111" stroke-width="5"/></g>')
    return (f'<g transform="translate({x} {y}) scale({s})"><rect x="-18" y="-560" width="36" height="560" fill="#495057" stroke="#111" stroke-width="6"/>'
            f'<g id="{uid}">{horn(30)}<g transform="scale(-1 1)">{horn(30)}</g></g>'
            f'<g id="{uid}-w" opacity="0">' + "".join(f'<path d="M{200 + k * 50} {-640 + k * 10} Q{240 + k * 60} -560 {200 + k * 50} {-480 - k * 10}" stroke="#ffd166" stroke-width="12" fill="none" stroke-linecap="round"/>' for k in range(3)) +
            "".join(f'<path d="M{-200 - k * 50} {-640 + k * 10} Q{-240 - k * 60} -560 {-200 - k * 50} {-480 - k * 10}" stroke="#ffd166" stroke-width="12" fill="none" stroke-linecap="round"/>' for k in range(3)) + '</g></g>')
def blare(uid, t, n=9):
    J.append(f'tl.set("#{uid}-w", {{ opacity: 1 }}, {F(t)}); tl.to("#{uid}-w", {{ opacity: .2, duration: .12, yoyo: true, repeat: {n}, ease: "steps(1)" }}, {F(t)});')
def rathaus(x, y, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s})"><rect x="-340" y="-420" width="680" height="420" fill="#f8f9fa" stroke="#111" stroke-width="8"/><path d="M-380 -416 L0 -620 L380 -416 Z" fill="#ced4da" stroke="#111" stroke-width="8"/>'
            + "".join(f'<rect x="{-290 + k * 150}" y="-350" width="90" height="120" fill="#bde0fe" stroke="#111" stroke-width="5"/>' for k in range(5)) +
            f'<rect x="-60" y="-170" width="120" height="170" fill="#6b4226" stroke="#111" stroke-width="6"/>{txt(0, -440, "RATHAUS", 56)}</g>')
def crowd(sfx, ex="shock", y=1900, s=.55, n=5, arm=("down", "down"), exprs=None):
    return "".join(fig(tiny(f"c{sfx}{k}", k, ex, arm=arm, exprs=exprs), 110 + k * 215, y + (k % 2) * 30, s) for k in range(n))
def photo(uid, x, y, emo, s=1.0, rot=0, inner=None, vis=False):
    body = inner if inner is not None else f'<text x="0" y="50" text-anchor="middle" style="font:150px Noto Color Emoji">{emo}</text>'
    return (f'<g id="{uid}" opacity="{1 if vis else 0}" transform="translate({x} {y}) rotate({rot}) scale({s})"><rect x="-150" y="-140" width="316" height="300" fill="#000" opacity=".25"/>'
            f'<rect x="-160" y="-150" width="320" height="300" fill="#fff" stroke="#111" stroke-width="7"/><rect x="-136" y="-126" width="272" height="220" fill="#ffe8d6"/>{body}</g>')

S = {}; FX = []
def confetti_svg(uid, n=40, y0=200):
    cols = ("#e63946", "#ffd166", "#06d6a0", "#118ab2", "#ef476f", "#8338ec")
    return f'<g id="{uid}" opacity="0">' + "".join(f'<rect class="cf" x="{(k * 97) % 1060}" y="{y0 + (k * 53) % 500}" width="22" height="36" fill="{cols[k % 6]}" transform="rotate({k * 37 % 90} {(k * 97) % 1060} {y0 + (k * 53) % 500})"/>' for k in range(n)) + '</g>'
R = "<span style='color:#ff4d5a'>"; G_ = "<span style='color:#2dc653'>"; B_ = "<span style='color:#4cc9f0'>"; X = "</span>"
HAIR["mia"] = lambda c: (f'<path d="M-100 -20 V-100 Q-100 -112 -88 -112 H88 Q100 -112 100 -100 V-20 L70 -70 H-40 L-70 -40 Z" fill="{c}" stroke="#111" stroke-width="4"/>'
                         f'<rect x="-112" y="-60" width="32" height="170" rx="8" fill="{c}" stroke="#111" stroke-width="4"/><rect x="80" y="-60" width="32" height="170" rx="8" fill="{c}" stroke="#111" stroke-width="4"/>')
HANDMUND = '<rect x="-46" y="14" width="92" height="56" rx="16" fill="#f2c9a5" stroke="#111" stroke-width="5"/>'
SWEAT = '<g class="sw">' + "".join(f'<path d="M{x} {y} q-12 24 0 32 q12 -8 0 -32" fill="#4cc9f0" stroke="#111" stroke-width="3"/>' for x, y in ((-112, -60), (112, -40), (-96, 30), (104, 50))) + '</g>'
def mia(uid, start="happy", arm=("down", "front"), extra=PHONE_R, head_acc=""):
    return person(uid, "mia", "#3d2b1f", "#ffbe0b", exprs=("happy", "sad", "shock", "panic", "annoyed", "neutral"), start=start, arm=arm, extra=extra, head_acc=head_acc)
def jonas2(uid, start="panic", arm=("down", "front")): return person(uid, "jonas", "#f4d35e", "#06d6a0", exprs=("panic", "relief"), start=start, arm=arm, extra=PHONE_R, head_acc=SWEAT)
def haken(uid, x, y, label, s=1.0, vis=True, col="#1d9bf0"):
    wd = 170 + 50 * len(label) if label else 150
    return (f'<g id="{uid}" opacity="{1 if vis else 0}" transform="translate({x} {y}) scale({s})"><g id="{uid}-in"><rect x="{-wd/2 + 8:.0f}" y="-62" width="{wd:.0f}" height="132" rx="34" fill="#000" opacity=".25"/>'
            f'<rect x="{-wd/2:.0f}" y="-70" width="{wd:.0f}" height="132" rx="34" fill="{col}" stroke="#111" stroke-width="8"/>'
            f'<path d="M{-wd/2 + 28:.0f} -6 l22 24 l40 -50 M{-wd/2 + 62:.0f} -6 l22 24 l40 -50" stroke="#fff" stroke-width="14" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<text id="{uid}-t" x="{-wd/2 + 150:.0f}" y="22" style="font:900 76px {FONT};fill:#fff">{label}</text></g></g>')
S = {}; FX = []
# --- SPLIT: links ich 3 Minuten (grün), rechts Mia 41 Minuten mit blauem Haken
def split(sfx, ich_lab, ich_ex="smug", mia_ex="annoyed", ich_haken=False):
    ib = haken(f"bi{sfx}", 270, 700, ich_lab, .78, col="#e63946") if ich_haken else sign(f"bi{sfx}", 270, 700, 400, 140, [f"⏱ {ich_lab}"], col="#2dc653", fg="#fff", size=80)
    L = street_bg() + fig(ich_(f"i{sfx}", ich_ex), 270, 1450, 1.15) + ib
    Rr = ('<rect width="1080" height="1920" fill="#ffd6a5"/>' + street_bg().replace('#8ecae6', '#ffd6a5') + fig(mia(f"m{sfx}", mia_ex), 800, 1450, 1.15) + haken(f"bm{sfx}", 800, 700, "41 MIN", .78))
    return (f'<defs><clipPath id="cl{sfx}"><rect width="540" height="1920"/></clipPath><clipPath id="cr{sfx}"><rect x="540" width="540" height="1920"/></clipPath></defs>'
            f'<g clip-path="url(#cl{sfx})">{L}</g><g clip-path="url(#cr{sfx})">{Rr}</g><rect x="532" width="16" height="1920" fill="#fff" stroke="#111" stroke-width="4"/>'
            + ("" if sfx == "z" else sign(f"lim{sfx}", 540, 400, 560, 120, ["LIMIT: 10 MIN"], col="#fff", size=68)))
S["SPLIT"] = split("a", "3 MIN")
S["LOOP"] = split("z", "6 TAGE", ich_ex="panic", mia_ex="shock", ich_haken=True)
S["UHR"] = (street_bg() + '<g transform="translate(540 840) scale(.85)"><circle r="300" fill="#fff" stroke="#111" stroke-width="14"/><path id="zeiger" d="M0 0 V-230" stroke="#e63946" stroke-width="18" stroke-linecap="round"/>'
            + "".join(f'<rect x="-6" y="-290" width="12" height="40" fill="#111" transform="rotate({k * 30})"/>' for k in range(12)) +
            f'<circle r="22" fill="#111"/></g>' + sign("sgu", 540, 440, 520, 130, ["⏳ 10:00"], col="#111", fg="#ffd166", size=96) + crowd("u", "neutral"))
S["HAKEN"] = (street_bg() + fig(tiny("t3", 1, "sad", exprs=("sad",)), 540, 1700, 1.3) + haken("h3", 540, 780, "17 MIN", 1.0, vis=False) +
              "".join(fig(tiny(f"c3{k}", k + 2, "shock", arm=("down", "front")), x, 1900, .5) + haken(f"h3{k}", x, 1560, m, .45) for k, (x, m) in enumerate(((120, "12"), (960, "25")))))
_sb = street_bg().replace('<rect width="1080" height="1920" fill="#8ecae6"/>', '')
S["MIA"] = ('<rect width="1080" height="1920" fill="#8ecae6"/><g id="wbg">' + _sb + '<g transform="translate(1080 0)">' + _sb + '</g></g>' +
            '<g id="walker">' + fig(mia("m4", "annoyed", arm=("down", "front")), 540, 1780, 1.3) + haken("h4", 540, 990, "41 MIN", .9) + '</g>' +
            crowd("s4", "shock", y=1950, s=.5) + bubble("bub4", ["„SORRY,", "WAR DUSCHEN 🚿“"], 540, 470, 760, size=72))
S["FLUG"] = (room_bg("#cdb4db", "#9a8c98") + fig(ich_("i5", "smug"), 540, 1750, 1.5) + sign("sg5", 540, 520, 720, 150, ["✈️ FLUGMODUS"], col="#fff", size=86) +
             sign("sg5b", 540, 740, 620, 150, ["KEIN HAKEN ❌"], col="#e63946", fg="#fff", size=78, vis=False))
S["OMA"] = (room_bg("#fde2e4", "#b08968") + fig(oma_("o6", "happy"), 540, 1750, 1.5) + sign("sg6", 540, 560, 500, 140, ["⏱ 1 MIN"], col="#2dc653", fg="#fff", size=86) +
            bubble("bub6a", ["MATRATZEN –20 %"], 540, 380, 720, size=66) + bubble("bub6b", ["❤️ ❤️ ❤️"], 760, 800, 440, tail=(-1, 1), size=80))
S["JONAS"] = (room_bg("#caf0f8", "#8d99ae") + fig(jonas2("j7"), 540, 1750, 1.5) + sign("sg7", 540, 520, 560, 200, ["9:50"], col="#111", fg="#ffd166", size=150))
lights = "".join(haken(f"hb{k}", x, y, "", .5) for k, (x, y) in enumerate(((180, 500), (900, 520), (130, 800), (950, 820), (230, 1100), (860, 1120), (540, 380))))
S["BGM"] = (street_bg(night=True) + f'<g id="lights">{lights}</g>' + fig(bgm_("b8", "panic", arm=("up", "up")), 540, 1700, 1.3) + sign("sg8", 540, 640, 380, 150, ["212"], col="#1d9bf0", fg="#fff", size=110) +
            sign("sg8b", 540, 1250, 420, 140, ["☀️ JULI"], col="#ffd166", size=80, vis=False))
S["STAR"] = (street_bg() + fig(ich_("i9", "grin", arm=("up", "up"), extra=""), 540, 1600, 1.3) + sign("sg9", 540, 600, 560, 150, ["🏆 < 3 MIN"], col="#ffd166", size=86) +
             crowd("p", "laugh", arm=("up", "up"), exprs=("laugh",)) + confetti_svg("cf9"))
S["MITTAG"] = (street_bg() + fig(ich_("i10", "happy", arm=("down", "front"), extra=PHONE_R), 540, 1700, 1.4) + haken("h10", 540, 820, "6 TAGE", 1.0, vis=False, col="#1d9bf0") + crowd("q", "neutral", y=1960, s=.45))
S["STARREN"] = (street_bg() + haken("h11", 540, 450, "6 TAGE", .9, col="#e63946") + crowd("st", "shock", y=1750, s=.75, n=5))
S["MUND"] = ('<rect width="1080" height="1920" fill="#ffd6a5"/>' + street_bg().replace('#8ecae6', '#ffd6a5') + fig(mia("m11", "shock", arm=("down", "down"), extra="", head_acc=HANDMUND), 540, 1750, 1.5))
S["FLUESTER"] = (street_bg(night=True) + fig(bgm_("b11", "shock", arm=("down", "down")), 360, 1750, 1.4) + bubble("bub11", ["„DU BIST SCHLIMMER", "ALS ICH.“"], 600, 520, 820, tail=(-1, 1), size=68))
blurline = lambda y, wd: f'<rect x="250" y="{y}" width="{wd}" height="36" rx="18" fill="#adb5bd"/>'
S["HANDY"] = ('<rect width="1080" height="1920" fill="#222"/><rect x="190" y="200" width="700" height="1500" rx="80" fill="#111" stroke="#555" stroke-width="12"/><rect x="230" y="300" width="620" height="1300" rx="30" fill="#ece5dd"/>'
              '<text x="790" y="380" text-anchor="middle" style="font:70px Noto Color Emoji">✈️</text>' + txt(300, 385, "18:42", 44, "#111", "start") +
              '<rect x="250" y="520" width="520" height="190" rx="26" fill="#fff" stroke="#111" stroke-width="4"/>' + blurline(560, 440) + blurline(620, 360) +
              txt(740, 690, "✓✓", 40, "#1d9bf0", "end") + sign("sg12", 540, 1000, 560, 140, ["GELESEN 👀"], col="#ffd166", size=72, vis=False) +
              sign("sg12b", 540, 1250, 640, 140, ["NIE BEANTWORTET"], col="#e63946", fg="#fff", size=66, vis=False))
S["NAME"] = ('<rect width="1080" height="1920" fill="#222"/><rect x="190" y="200" width="700" height="1500" rx="80" fill="#111" stroke="#555" stroke-width="12"/><rect x="230" y="300" width="620" height="1300" rx="30" fill="#ece5dd"/>'
             '<rect x="230" y="300" width="620" height="200" rx="30" fill="#075e54"/><rect x="270" y="350" width="100" height="100" rx="50" fill="#adb5bd"/>'
             '<rect x="400" y="370" width="300" height="60" rx="16" fill="#888" opacity=".9"/><text id="herz13" x="760" y="430" text-anchor="middle" style="font:90px Noto Color Emoji">❤️</text>' +
             '<rect x="270" y="620" width="480" height="160" rx="26" fill="#fff" stroke="#111" stroke-width="4"/>' + '<rect x="290" y="660" width="400" height="36" rx="18" fill="#adb5bd"/><rect x="290" y="720" width="300" height="36" rx="18" fill="#adb5bd"/>' +
             sign("sg13", 540, 1150, 760, 150, ["MEHR SAG ICH NICHT 🤐"], col="#111", fg="#fff", size=60, vis=False))
S["OMA2"] = (room_bg("#fde2e4", "#b08968") + fig(oma_("o14", "wink"), 540, 1750, 1.5) + bubble("bub14a", ["❤️"], 330, 520, 300, size=110) + bubble("bub14b", ["⚠️ MAHNUNG"], 700, 800, 560, tail=(-1, 1), size=76) +
             '<rect id="dark14" width="1080" height="1920" fill="#000" opacity="0"/>')
S["TIPP"] = (street_bg(night=True) + fig(ich_("i15", "panic", arm=("front", "front"), extra=""), 540, 1600, 1.4) + sign("st15", 540, 640, 940, 230, ["WESSEN", "NACHRICHT?"], col="#ffd166", size=96))

# ---------- Zeitplan ----------
J.append('tl.set("#cam", { x: 0, y: 0, scale: 1, svgOrigin: "0 0" }, 0);')
t = {k: st(k) for k in T}
ww = lambda s, word, n=1, o=-.1: round(w(s, word, n) + o, 2)
def popkeep(sel, tt, d=.25):
    pop(sel, tt, d, "50% 50%"); J.append(f'tl.set("{sel}", {{ opacity: 1 }}, {F(tt + d + .01)});')
# s1 Hook: Split mit Zahlen + LIMIT 10 MIN ab 0,0 s; bei "zehn" Schnitt auf die Uhr
cut(0, 540, 960, 1.08); cam(.02, 540, 960, 1.0, .35, "power3.out"); FX += [("hit", 0, .5, .8)]
blink("#lima-in", .4, 7, .15, .3)
c1 = min(ww("s1", "zehn"), 1.9); cut(c1, 540, 800, 1.1); cam(c1 + .05, 540, 800, 1.3, 1.5, "none"); FX += [("tick", c1, .5, 1.5)]
J.append(f'tl.fromTo("#zeiger", {{ rotation: 0, svgOrigin: "0 0" }}, {{ rotation: 300, svgOrigin: "0 0", duration: {F(max(.5, t["s2"] - c1))}, ease: "none", immediateRender: false }}, {F(c1)});')
# s2 Split: ich 3 Min vs Mia 41 Min
t2 = t["s2"]; cut(t2, 270, 1150, 1.4); tm = ww("s2", "Mia:", o=-.2); cut(tm, 800, 1150, 1.4); FX += [("swoosh", tm, .4, .4)]
cut(ww("s2", "einundvierzig"), 800, 720, 1.7); FX += [("chime", ww("s2", "einundvierzig"), .4, .5)]
# s3 Blauer Haken über dem Kopf, mit Minutenzahl, für alle sichtbar
t3 = t["s3"]; cut(t3, 540, 1300, 1.1); cam(t3 + .05, 540, 1250, 1.25, 1.0, "none")
th = ww("s3", "Haken"); popkeep("#h3", th); cut(th, 540, 900, 1.2); FX += [("pop", th, .5, .3)]
tmz = ww("s3", "Minutenzahl."); cut(tmz, 600, 780, 1.8); blink("#h3-in", tmz, 5, .12, .3)
tfa = ww("s3", "Für"); cut(tfa, 540, 1300, .99 if False else 1.0); FX += [("whoosh", tfa, .3, .4)]
# s4 Mia mit 41 – alle starren – "Sorry, war duschen"
t4 = t["s4"]; cut(t4, 540, 1200, 1.1)
J.append(f'tl.fromTo("#wbg", {{ x: 0 }}, {{ x: -1080, duration: {F(t["s5"] - t4)}, ease: "none", immediateRender: false }}, {F(t4)}); tl.to("#walker", {{ y: -14, duration: .15, yoyo: true, repeat: {int((t["s5"] - t4) / .15)} }}, {F(t4)});')
cut(ww("s4", "Alle"), 540, 1700, 1.3); FX += [("klong", ww("s4", "Alle"), .4, .4)]
J.append('tl.set("#bub4", { opacity: 0 }, 0);'); tti = ww("s4", "Sorry,"); popkeep("#bub4", tti); cut(ww("s4", "tippt:"), 540, 800, 1.2); FX += [("pop", tti, .5, .3)]
expr("m4", "annoyed", "sad", tti)
# s5 Geheimnis: Flugmodus, kein Haken
t5 = t["s5"]; cut(t5, 540, 1100, 1.45); cam(t5 + .05, 540, 1000, 1.6, 1.3, "none"); FX += [("riser", t5, .3, 1.0)]
tfl = ww("s5", "Flugmodus.", o=-.3); cut(tfl, 540, 700, 1.2); pop("#sg5-in", tfl, .25, "50% 50%"); FX += [("whoosh", tfl, .4, .5)]
tkh = ww("s5", "keinen"); popkeep("#sg5b", tkh); cut(tkh, 540, 900, 1.0); FX += [("hit", tkh, .5, .4)]
# s6 Oma antwortet in 1 Minute – sogar dem Matratzenladen – mit drei Herzen
t6 = t["s6"]; cut(t6, 540, 1000, 1.2); J.append('tl.set("#bub6a", { opacity: 0 }, 0); tl.set("#bub6b", { opacity: 0 }, 0);')
tma = ww("s6", "Matratzenladen.", o=-.3); popkeep("#bub6a", tma); cut(tma, 540, 600, 1.3); FX += [("pop", tma, .5, .3)]
the = ww("s6", "Herzen."); tdr = ww("s6", "drei"); popkeep("#bub6b", tdr); cut(tdr, 700, 900, 1.3); expr("o6", "happy", "laugh", tdr); FX += [("chime", tdr, .45, .6)]
# s7 Jonas: 9:59, schwitzt
t7 = t["s7"]; cut(t7, 540, 1100, 1.3); cam(t7 + .05, 540, 1000, 1.45, 1.2, "none")
t9 = ww("s7", "neun"); cut(t9, 540, 600, 1.4); FX += [("tick", t9, .5, 1.6)]
J.append(f'(() => {{ const o = {{ v: 50 }}; tl.fromTo(o, {{ v: 50 }}, {{ v: 59, duration: 1.4, ease: "none", immediateRender: false, onUpdate: () => {{ document.getElementById("sg7-in").querySelector("text").textContent = "9:" + Math.round(o.v); }} }}, {F(t9)}); }})();')
J.append(f'tl.call(() => {{ document.getElementById("sg7-in").querySelector("text").textContent = "9:50"; }}, null, {F(max(0, t9 - .05))});')
tsc = ww("s7", "schwitzt"); cut(tsc, 540, 1150, 1.7); J.append(f'tl.fromTo("#j7 .sw", {{ y: 0 }}, {{ y: 30, duration: .3, repeat: 5, ease: "power1.in", immediateRender: false }}, {F(tsc)});'); FX += [("splat", tsc, .4, .4)]
cut(ww("s7", "Immer."), 540, 1300, 1.15)
# s8 Bürgermeister: 212 offen, leuchtet wie ein Weihnachtsbaum – im Juli
t8 = t["s8"]; cut(t8, 540, 1100, 1.2); cam(t8 + .05, 540, 900, 1.35, 1.2, "none")
t212 = ww("s8", "zweihundertzwölf"); cut(t212, 540, 700, 1.5)
J.append(f'(() => {{ const o = {{ v: 0 }}; tl.fromTo(o, {{ v: 0 }}, {{ v: 212, duration: .8, ease: "power1.out", immediateRender: false, onUpdate: () => {{ document.querySelector("#sg8-in text").textContent = Math.round(o.v); }} }}, {F(t212)}); }})();')
FX += [("blips", t212, .35, .9)]
twb = ww("s8", "Weihnachtsbaum.", o=-.3); cut(twb, 540, 900, 1.0)
for k in range(7):
    J.append(f'tl.to("#hb{k}-in rect:nth-of-type(2)", {{ fill: "{("#e63946", "#ffd166", "#2dc653", "#ff70a6")[k % 4]}", duration: .15, yoyo: true, repeat: 9, ease: "steps(1)" }}, {F(twb + k * .04)});')
FX += [("chime", twb, .5, .8)]
tju = ww("s8", "Juli."); popkeep("#sg8b", tju - .1); cut(tju - .1, 540, 1250, 1.4); FX += [("boing", tju, .4, .3)]
# s9 Stadtbester – Leute klatschen
t9s = t["s9"]; cut(t9s, 540, 900, 1.2); cam(t9s + .05, 540, 800, 1.35, 1.2, "none"); FX += [("chime", t9s, .4, .6)]
tkl = ww("s9", "Leute"); cut(tkl, 540, 1300, 1.0); J.append(f'tl.set("#cf9", {{ opacity: 1 }}, {F(tkl)}); tl.fromTo("#cf9 .cf", {{ y: -300 }}, {{ y: 900, duration: 2.2, ease: "none", immediateRender: false }}, {F(tkl)});')
for k in range(5): wobble(f"#cp{k}", tkl, 7, 8, .18)
FX += [("riser", tkl, .25, 1.0)]
# s10 Heute Mittag: blauer Haken über mir – 6 Tage
t10 = t["s10"]; cut(t10, 540, 1150, 1.2); cam(t10 + .05, 540, 1100, 1.35, 1.0, "none")
th10 = ww("s10", "Haken"); popkeep("#h10", th10); cut(th10, 540, 1000, 1.2); expr("i10", "happy", "shock", th10); FX += [("klong", th10, .5, .5)]
t6t = ww("s10", "sechs"); cut(t6t, 540, 820, 1.7); J.append(f'tl.set("#h10-in rect:nth-of-type(2)", {{ fill: "#e63946" }}, {F(t6t)});'); blink("#h10-in", t6t, 9, .12, .25)
shake(t6t + .1, 9, 14); FX += [("hit", t6t, .7, .6)]
# s11 Stadt starrt – Mia Hand vor dem Mund – Bürgermeister flüstert
t11 = t["s11"]; cut(t11, 540, 1300, 1.0); cam(t11 + .05, 540, 900, 1.2, 1.4, "none")
tmi = ww("s11", "Mia", o=-.15); cut(tmi, 540, 1200, 1.4); FX += [("swoosh", tmi, .4, .4)]
tbf = ww("s11", "Bürgermeister", o=-.15); cut(tbf, 450, 1100, 1.2); J.append('tl.set("#bub11", { opacity: 0 }, 0);')
tdu = ww("s11", "Du"); popkeep("#bub11", tdu); cut(tdu, 560, 800, 1.15); FX += [("pop", tdu, .4, .3)]
# s12 gelesen – im Flugmodus – nie wieder angefasst
t12 = t["s12"]; cut(t12, 540, 700, 1.4); cam(t12 + .05, 540, 750, 1.6, 1.2, "none")
popkeep("#sg12", ww("s12", "gelesen.", o=-.2)); FX += [("pop", ww("s12", "gelesen.", o=-.2), .4, .3)]
tim = ww("s12", "Heimlich,"); cut(tim, 790, 400, 1.6)
tnw = ww("s12", "nie"); cut(tnw, 540, 1000, 1.0); popkeep("#sg12b", tnw); FX += [("klong", tnw, .45, .5)]
# s13 Herz hinter dem Namen – mehr sag ich nicht
t13 = t["s13"]; cut(t13, 540, 500, 1.4); cam(t13 + .05, 600, 420, 1.8, 1.4, "none")
thz = ww("s13", "Herz."); cut(thz, 760, 400, 2.4); J.append(f'tl.fromTo("#herz13", {{ scale: .4, transformOrigin: "50% 50%" }}, {{ scale: 1.2, duration: .3, yoyo: true, repeat: 3, ease: "sine.inOut", immediateRender: false }}, {F(thz)});')
FX += [("chime", thz, .5, .6)]
tms = ww("s13", "Mehr"); popkeep("#sg13", tms); cut(tms, 540, 1000, 1.0)
# s14 Oma: Herz + Mahnung, Trommelwirbel vor dem Finale
t14 = t["s14"]; cut(t14, 540, 1100, 1.2); J.append('tl.set("#bub14a", { opacity: 0 }, 0); tl.set("#bub14b", { opacity: 0 }, 0);')
popkeep("#bub14a", ww("s14", "Herz.", o=-.25)); FX += [("pop", ww("s14", "Herz.", o=-.25), .4, .3)]
tmh = ww("s14", "Mahnung."); popkeep("#bub14b", tmh); cut(tmh, 650, 900, 1.3); expr("o14", "wink", "smug", tmh); FX += [("hit", tmh, .5, .4)]
J.append(f'tl.to("#dark14", {{ opacity: .45, duration: 1.2 }}, {F(tmh + .4)});'); cam(tmh + .4, 600, 900, 1.5, max(.5, t["s15"] - tmh - .45), "power1.in")
FX += [("wirbel", tmh + .3, .45, max(.8, t["s15"] - tmh - .2))]
# s15 Frage
t15 = t["s15"]; cut(t15, 540, 960, 1.1); cam(t15 + .05, 540, 960, 1.2, 1.6, "none"); FX += [("hit", t15, .5, .5)]
J.append(f'tl.to("#st15-in", {{ scale: 1.05, transformOrigin: "50% 50%", duration: .3, yoyo: true, repeat: 5 }}, {F(t15 + .3)});')
# s16 Loop: Split vom Anfang – jetzt ich mit rotem Haken 6 TAGE vs Mia 41 MIN
t16 = t["s16"]; cut(t16, 540, 960, 1.15); cam(t16 + .3, 540, 960, 1.0, 1.2, "power2.inOut"); FX += [("whoosh", t16, .35, .4)]
blink("#biz-in", t16 + .3, 11, .2, .3)
# Schlussbild bleibt ohne Zoom (nichts abgeschnitten, keine Überlappung mit Banner/Box)
expr("mz", "shock", "sad", round(t16 + 2.6, 2)); expr("iz", "panic", "sad", round(t16 + 2.6, 2)); pop("#bmz-in", round(t16 + 2.6, 2), .25, "50% 50%"); FX += [("pop", t16 + 2.6, .35, .3)]

sets = [("SPLIT", 0, c1), ("UHR", c1, t2), ("SPLIT", t2, t3), ("HAKEN", t3, t4), ("MIA", t4, t5), ("FLUG", t5, t6), ("OMA", t6, t7), ("JONAS", t7, t8), ("BGM", t8, t9s),
        ("STAR", t9s, t10), ("MITTAG", t10, t11), ("STARREN", t11, tmi), ("MUND", tmi, tbf), ("FLUESTER", tbf, t12), ("HANDY", t12, t13), ("NAME", t13, t14), ("OMA2", t14, t15),
        ("TIPP", t15, t16), ("LOOP", t16, END)]
tag = f'<div class="ui clip" data-start="0" data-duration="{F(END)}" style="right:24px;top:40px;font:900 30px Inter,sans-serif;color:#fff;background:rgba(0,0,0,.55);padding:6px 14px;border-radius:12px">TEIL 1</div>'
cta = (f'<div class="ui clip" data-start="{F(t16 + .1)}" data-duration="{F(END - t16 - .1)}" style="left:60px;right:60px;top:1400px;text-align:center">'
       f'<div id="cta-in" style="display:inline-block;background:#fff;color:#111;border:7px solid #111;border-radius:26px;padding:16px 26px;font:900 54px/1.18 Inter,sans-serif">'
       f'Folg mir und schreib <span style="color:#e63946">‚Teil 2‘</span> in die Kommentare, dann kommt die Fortsetzung!</div></div>')
J.append(f'tl.fromTo("#cta-in", {{ y: 80, opacity: 0 }}, {{ y: 0, opacity: 1, duration: .3, ease: "back.out(2)", immediateRender: false }}, {F(t16 + .12)});')
OBEN = [(0, f"ANTWORT IN {R}10 MIN{X} – PFLICHT"), (t2, f"ICH {G_}3 MIN{X} vs MIA {R}41 MIN{X}"), (t3, f"ZU SPÄT = {B_}✓✓{X} ÜBERM KOPF"), (t4, f"MIA: {B_}✓✓{X} 41"), (t5, "🤫 MEIN GEHEIMNIS"),
        (t6, f"OMA: {G_}1 MIN{X} ❤️"), (t7, f"JONAS: {R}9:59{X} 😰"), (t8, f"BÜRGERMEISTER: {B_}212{X} OFFEN"), (t9s, "🏆 STADTBESTER"), (t10, "HEUTE MITTAG …"),
        (t11, f"ICH: {R}6 TAGE{X} 😱"), (t12, "✈️ HEIMLICH GELESEN"), (t13, "HINTER DEM NAMEN: ❤️"), (t14, "OMA: ❤️ + ⚠️"), (t15, "WESSEN NACHRICHT?"),
        (t16, f"ICH {R}6 TAGE{X} vs MIA 41 MIN")]
HOT = {"NACHRICHT", "MINUTEN", "MIA", "HAKEN", "MINUTENZAHL", "DUSCHEN", "GEHEIMNIS", "FLUGMODUS", "OMA", "HERZEN", "JONAS", "BÜRGERMEISTER", "WEIHNACHTSBAUM", "JULI",
       "STADTBESTER", "TAGE", "SCHLIMMER", "HERZ", "MAHNUNG", "TEIL"}
try:
    from clampcam import clamp_cam; clamp_cam(J)
except Exception as e:
    print("clampcam übersprungen:", e)
finish(S, sets, OBEN, FX, HOT, tag, extra_ui=cta, banner=("TEIL 2?", "➕ FOLGEN"), oben_top=150, cap_top=1250, banner_top=360)
_h = open("compositions/welt.html", encoding="utf-8").read()
_h = _h.replace("padding:14px 40px;font:900 96px/1 Inter", "padding:14px 30px;white-space:nowrap;font:900 84px/1 Inter")
open("compositions/welt.html", "w", encoding="utf-8").write(_h)
import re as _re
_c = open("compositions/caps.html", encoding="utf-8").read()
_c = _re.sub(r'<div id="w\d+" class="wd clip" data-start="([0-9.]+)"[^>]*>.*?</div>', lambda m: "" if float(m.group(1)) >= t16 - .05 else m.group(0), _c)
open("compositions/caps.html", "w", encoding="utf-8").write(_c)
