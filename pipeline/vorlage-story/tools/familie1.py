"""STORY „In dieser Stadt …“ – NEUE SERIE „Familiengruppen-Stadt“, TEIL 1: Jede Familiengruppe darf nur 20 Nachrichten am Tag,
wer überzieht, dessen Gruppe wird laut über der Stadt vorgelesen. Erzähler hat die Gruppe stummgeschaltet (1.400 ungelesen) -> Twist.
Aufruf: /usr/bin/python3 tools/familie1.py  (liest voice.json + assets/vo/timing.json; Bausteine aus tools/bausteine.py;
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
R = "<span style='color:#ff4d5a'>"; G_ = "<span style='color:#2dc653'>"; X = "</span>"
# --- SPLIT: links ich 2 Nachrichten, rechts Mama 63 (40 Daumen)
def split(sfx, ich_n, mama_n, ich_ex="smug", mama_ex="laugh", ich_col="#2dc653"):
    L = street_bg() + fig(ich_(f"i{sfx}", ich_ex), 270, 1450, 1.15) + sign(f"bi{sfx}", 270, 700, 380 if len(ich_n) < 4 else 470, 140, [f"💬 {ich_n}"], col=ich_col, fg="#fff", size=86)
    Rr = ('<rect width="1080" height="1920" fill="#ffd6a5"/>' + street_bg().replace('#8ecae6', '#ffd6a5') + fig(mama(f"m{sfx}", mama_ex), 800, 1450, 1.15) +
          sign(f"bm{sfx}", 800, 700, 400, 140, [f"💬 {mama_n}"], col="#e63946", fg="#fff", size=86) + (sign(f"bd{sfx}", 800, 540, 300, 110, ["👍 40"], col="#ffd166", size=66) if sfx != "z" else ""))
    return (f'<defs><clipPath id="cl{sfx}"><rect width="540" height="1920"/></clipPath><clipPath id="cr{sfx}"><rect x="540" width="540" height="1920"/></clipPath></defs>'
            f'<g clip-path="url(#cl{sfx})">{L}</g><g clip-path="url(#cr{sfx})">{Rr}</g><rect x="532" width="16" height="1920" fill="#fff" stroke="#111" stroke-width="4"/>'
            + ("" if sfx == "z" else sign(f"lim{sfx}", 540, 400, 470, 120, ["LIMIT: 20"], col="#fff", size=72)))
S["SPLIT"] = split("a", "2", "63")
S["LOOP"] = split("z", "1.400", "63", ich_ex="panic", mama_ex="shock", ich_col="#e63946")
S["RATHAUS"] = ('<rect width="1080" height="1920" fill="#8ecae6"/><rect x="800" y="200" width="150" height="150" rx="30" fill="#ffd166" stroke="#111" stroke-width="5"/>' + rathaus(540, 1300, 1.2) +
                '<rect y="1300" width="1080" height="620" fill="#ced4da"/>' + zaehler("za", 540, 470, "0 / 20") + crowd("r", "neutral", exprs=("neutral", "shock")))
# Küche: Mama tippt beim Frühstück
S["KUECHE"] = (room_bg("#ffe8d6", "#c8a27c") + fig(mama("mk", "determined", arm=("front", "front")), 540, 1700, 1.45) +
               '<rect x="120" y="1450" width="840" height="70" rx="12" fill="#bc6c25" stroke="#111" stroke-width="7"/>' +
               '<text x="260" y="1440" text-anchor="middle" style="font:120px Noto Color Emoji">☕</text><text x="830" y="1440" text-anchor="middle" style="font:120px Noto Color Emoji">🥐</text>' +
               zaehler("zk", 540, 640, "0 / 20", .85))
def stadt(sfx, extra, ex="shock", night=False, exprs=None):
    return street_bg(night=night) + mast(f"ma{sfx}", 540, 1180, 1.0) + extra + crowd(sfx, ex, exprs=exprs)
S["VORLESEN"] = stadt("v", sign("sgv", 540, 400, 820, 230, ["ÜBERZIEHEN =", "LAUT VORLESEN"], col="#ffd166", size=78))
S["STUMM"] = (room_bg("#cdb4db", "#9a8c98") + fig(ich_("i5", "smug", arm=("down", "front")), 540, 1750, 1.5) +
              sign("sg5", 540, 560, 760, 150, ["🔕 STUMM"], col="#fff", size=90) + sign("sg5b", 540, 760, 820, 150, ["1.400 UNGELESEN"], col="#e63946", fg="#fff", size=80, vis=False))
S["OMA"] = (room_bg("#fde2e4", "#b08968") + fig(oma_("o6", "happy"), 540, 1750, 1.5) +
            photo("ph1", 230, 560, "🍝", .9, -8) + photo("ph2", 820, 600, "🍝", .9, 7) +
            photo("ph3", 540, 520, "", 1.05, 0, inner='<g transform="scale(.62) translate(0 -10)"><rect x="-160" y="-150" width="320" height="300" fill="#fff" stroke="#111" stroke-width="9"/><text x="0" y="50" text-anchor="middle" style="font:150px Noto Color Emoji">🍝</text></g>'))
S["MILCH"] = stadt("m", bubble("bubm", ["WER HAT DIE", "MILCH GEKAUFT? 🥛"], 540, 400, 860, size=70), ex="confused", exprs=("confused", "laugh"))
S["BUS"] = ('<rect width="1080" height="1920" fill="#8ecae6"/>' + street_bg().replace('<rect width="1080" height="1920" fill="#8ecae6"/>', '') +
            '<g transform="translate(560 1560)"><rect x="-480" y="-420" width="960" height="420" rx="40" fill="#ffbe0b" stroke="#111" stroke-width="9"/>'
            '<rect x="-430" y="-370" width="300" height="200" rx="20" fill="#bde0fe" stroke="#111" stroke-width="7"/><rect x="-90" y="-370" width="240" height="200" rx="20" fill="#bde0fe" stroke="#111" stroke-width="7"/>'
            '<rect x="190" y="-370" width="240" height="200" rx="20" fill="#bde0fe" stroke="#111" stroke-width="7"/><rect x="-360" y="-30" width="140" height="140" rx="70" fill="#222"/><rect x="220" y="-30" width="140" height="140" rx="70" fill="#222"/></g>' +
            fig(tiny("drv", 0, "grin", exprs=("grin",)), 400, 1720, .62) + bubble("bubb", ["ICH! 🙋"], 400, 720, 460, size=90))
S["JONAS"] = (room_bg("#caf0f8", "#8d99ae") + fig(jonas("j8", "happy", arm=("front", "front")), 320, 1750, 1.35) +
              "".join(sign(f"jw{k}", 740, 560 + k * 165, 380, 136, [wd], col="#dcf8c6", size=76, vis=False) for k, wd in enumerate(("HALLO.", "ICH.", "BIN.", "PLEITE."))))
S["BGM"] = (street_bg() + '<rect x="330" y="1250" width="420" height="380" rx="16" fill="#6b4226" stroke="#111" stroke-width="8"/>' + fig(bgm_("b9"), 540, 1300, 1.2) +
            sign("sg9", 540, 420, 640, 150, ["LIMIT WEG!"], col="#fff", size=90) + zaehler("z9", 540, 650, "20 / 20", .7, col="#ffd166"))
S["LAUT"] = stadt("l", bubble("bubl", ["„LIMIT WEG!“", "– DER BÜRGERMEISTER"], 540, 400, 860, size=66), ex="laugh", exprs=("laugh",))
thumbs = "".join(f'<text class="th" x="{110 + (k % 8) * 122}" y="{330 + (k // 8) * 120}" text-anchor="middle" style="font:90px Noto Color Emoji">👍</text>' for k in range(40))
S["MAMA2"] = (street_bg() + fig(mama("m10", "grin", arm=("front", "front")), 540, 1750, 1.5) + sign("sg10", 540, 1000, 360, 130, ["💬 63"], col="#e63946", fg="#fff", size=86) +
              f'<g id="thumbs" opacity="0">{thumbs}</g>' + sign("sg10b", 540, 520, 560, 200, ["👍 ×40"], col="#ffd166", size=120, vis=False))
S["ALARM"] = ('<rect width="1080" height="1920" fill="#8ecae6"/>' + rathaus(540, 1300, 1.2) + '<rect y="1300" width="1080" height="620" fill="#ced4da"/>' +
              zaehler("zal", 540, 470, "20 / 20", col="#e63946") + crowd("a", "shock") + '<rect id="red11" width="1080" height="1920" fill="url(#vig)" opacity="0"/>')
S["ICH2"] = (room_bg("#cdb4db", "#9a8c98") + fig(ich_("i11", "shock", arm=("up", "up"), extra=""), 540, 1750, 1.5) +
             sign("sg11", 540, 560, 760, 150, ["🔕 → 🔊"], col="#fff", size=100) + zaehler("z11", 540, 820, "0", .8, col="#e63946"))
S["MORGEN"] = stadt("g", bubble("bubg", ["„GUTEN MORGEN,", "IHR LIEBEN! 🌞“"], 540, 400, 860, size=70), ex="neutral", exprs=("neutral", "laugh"))
billboard = ('<g transform="translate(540 650)"><rect x="-420" y="-300" width="840" height="560" rx="20" fill="#fff" stroke="#111" stroke-width="12"/><rect x="-390" y="-270" width="780" height="500" fill="#ffd6a5"/>'
             '<g transform="translate(0 330) scale(1.05)">' + person("bb", "topf", "#6b3e26", "#118ab2", exprs=("braces",), start="braces") + '</g>'
             '<rect x="-470" y="-360" width="220" height="100" rx="20" fill="#e63946" stroke="#111" stroke-width="7"/>' + txt(-360, -288, "#612", 64, "#fff") + '</g>'
             '<rect x="420" y="900" width="30" height="350" fill="#495057"/><rect x="630" y="900" width="30" height="350" fill="#495057"/>')
S["FOTO"] = (street_bg() + billboard + crowd("f", "shock", exprs=("shock", "laugh"), arm=("up", "up")))
S["SPANNUNG"] = ('<rect width="1080" height="1920" fill="#0b132b"/>' + mast("ms", 540, 1500, 1.4) + sign("sg14", 540, 520, 900, 220, ["NACHRICHT", "#1.347"], col="#111", fg="#ffd166", size=90) +
                 crowd("s", "shock", y=1950) + '<rect width="1080" height="1920" fill="#000814" opacity=".35"/>')
S["KNOPF"] = (room_bg("#fde2e4", "#b08968") + fig(oma_("o14", "grin", arm=("down", "front"), extra=""), 380, 1750, 1.4) +
              '<g transform="translate(800 1150)"><rect x="-180" y="-220" width="360" height="440" rx="30" fill="#6b4226" stroke="#111" stroke-width="8"/>'
              '<circle cx="0" cy="-60" r="110" fill="#333" stroke="#111" stroke-width="6"/><g id="knob" transform="translate(0 110)"><circle r="70" fill="#ced4da" stroke="#111" stroke-width="7"/><rect x="-8" y="-66" width="16" height="44" fill="#e63946"/></g></g>' +
              '<text x="800" y="780" text-anchor="middle" style="font:150px Noto Color Emoji">🔊</text>')
S["TIPP"] = (street_bg(night=True) + fig(ich_("i15", "panic", arm=("front", "front"), extra=""), 540, 1850, 1.8) + sign("st15", 540, 640, 920, 230, ["WAS STEHT IN", "#1.347?"], col="#ffd166", size=86))

# ---------- Zeitplan ----------
J.append('tl.set("#cam", { x: 0, y: 0, scale: 1, svgOrigin: "0 0" }, 0);')
t = {k: st(k) for k in T}
ww = lambda s, word, n=1, o=-.1: round(w(s, word, n) + o, 2)
# s1 Hook: Split sofort mit Zahlen + LIMIT 20, Punch-Zoom; bei "nur zwanzig" Schnitt auf Rathaus-Zähler
cut(0, 540, 960, 1.08); cam(.02, 540, 960, 1.0, .35, "power3.out"); FX += [("hit", 0, .5, .8)]
blink("#lima-in", .4, 7, .15, .3)
c1 = min(ww("s1", "nur"), 1.9); cut(c1, 540, 700, 1.15); cam(c1 + .05, 540, 600, 1.35, 1.2, "none"); FX += [("whoosh", c1, .3, .4)]
setz("za", ww("s1", "zwanzig"), "20 / 20", "0 / 20", "#ffd166"); FX += [("chime", ww("s1", "zwanzig"), .4, .5)]
# s2 Split: ich 2 vs Mama 63 / 40 Daumen
t2 = t["s2"]; cut(t2, 270, 1150, 1.4); tm = ww("s2", "Mama:", o=-.2)
cut(tm, 800, 1150, 1.4); FX += [("swoosh", tm, .4, .4)]
td = ww("s2", "Davon"); cut(td, 800, 600, 1.7); pop("#bda", td, .25, "50% 50%"); FX += [("pop", td, .5, .3)]
# s3 Rathaus-Zähler, dann Mama beim Frühstück knackt die 20
t3 = t["s3"]; cut(t3, 540, 1100, 1.0); cam(t3 + .05, 540, 600, 1.4, 1.5, "power1.inOut"); setz("za", t3, "0 / 20", "20 / 20", "#2dc653")
tk = ww("s3", "Mama"); cut(tk, 540, 1100, 1.05); cam(tk + .05, 540, 1000, 1.25, 1.0, "none")
count("zk-t", tk + .2, 0, 20, max(.3, w("s3", "zwanzig") - tk - .2), suffix=" / 20"); FX += [("blips", tk + .2, .3, 1.0)]
tz = ww("s3", "zwanzig"); J.append(f'tl.set("#zk-t", {{ fill: "#e63946" }}, {F(tz)});'); blink("#zk-in", tz, 7, .12, .2); cut(tz, 540, 700, 1.5); FX += [("klong", tz, .5, .5)]
expr("mk", "determined", "grin", tz); cut(ww("s3", "Frühstück", o=-.15), 380, 1300, 1.6)
# s4 Überziehen = laut vorlesen
t4 = t["s4"]; cut(t4, 540, 1300, 1.0); cam(t4 + .05, 540, 1100, 1.2, 1.4, "none")
tl4 = ww("s4", "laut"); cut(tl4, 540, 620, 1.35); blare("mav", tl4); shake(tl4 + .1, 7, 10); FX += [("glitch", tl4 + .3, .22, .4)]
pop("#sgv", ww("s4", "vorgelesen", o=-.3), .25, "50% 50%"); J.append('tl.set("#sgv", { opacity: 0 }, 0);'); cut(ww("s4", "vorgelesen", o=-.3), 540, 900, 1.0)
# s5 Geheimnis: stumm, 1.400 ungelesen
t5 = t["s5"]; cut(t5, 540, 1100, 1.4); cam(t5 + .05, 540, 1000, 1.6, 1.4, "none"); FX += [("riser", t5, .3, 1.0)]
tst = ww("s5", "stumm", o=-.2); cut(tst, 540, 650, 1.3); pop("#sg5-in", tst, .25, "50% 50%"); FX += [("pop", tst, .5, .3)]
t14 = ww("s5", "Vierzehnhundert"); cut(t14, 540, 900, 1.0); pop("#sg5b", t14, .3, "50% 50%"); J.append(f'tl.set("#sg5b", {{ opacity: 1 }}, {F(t14 + .3)});')
blink("#sg5b-in", t14 + .4, 7, .15, .3); FX += [("hit", t14, .5, .5)]
# s6 Oma: Foto, noch eins, Foto vom Foto
t6 = t["s6"]; cut(t6, 540, 1200, 1.2); cam(t6 + .05, 540, 1150, 1.35, 1.2, "none")
for k, (word, n) in enumerate((("Foto", 1), ("eins.", 1), ("Foto", 2))):
    tp = ww("s6", word, n, -.15) if word != "eins." else ww("s6", "noch", o=-.1)
    pop(f"#ph{k + 1}", tp, .3, "50% 50%"); J.append(f'tl.set("#ph{k + 1}", {{ opacity: 1 }}, {F(tp + .31)});'); FX += [("pop", tp, .5, .3)]
    cut(tp, (230, 820, 540)[k], 700 if k < 2 else 600, (1.3, 1.3, 1.0)[k])
expr("o6", "happy", "laugh", ww("s6", "Foto", 3))
# s7 Mama überzieht -> Milch-Frage über der Stadt -> Busfahrer antwortet
t7 = t["s7"]; cut(t7, 540, 1300, 1.0); blare("mam", t7 + .2); shake(t7 + .2, 7, 10); FX += [("glitch", t7 + .2, .22, .4)]
J.append('tl.set("#bubm", { opacity: 0 }, 0);'); tw = ww("s7", "Wer"); pop("#bubm", tw, .25, "50% 50%"); cut(tw, 540, 600, 1.2); FX += [("pop", tw, .5, .3)]
tb = ww("s7", "Busfahrer", o=-.3); cut(tb, 400, 1300, 1.0); J.append('tl.set("#bubb", { opacity: 0 }, 0);'); pop("#bubb", ww("s7", "antwortet", o=-.2), .25, "50% 50%")
cut(ww("s7", "antwortet", o=-.2), 400, 1000, 1.4); FX += [("boing", ww("s7", "antwortet", o=-.2), .4, .3)]
expr("cm0", "confused", "laugh", tb); expr("cm2", "confused", "laugh", tb)
# s8 Jonas: ein Wort pro Nachricht
t8 = t["s8"]; cut(t8, 320, 1250, 1.3); cam(t8 + .05, 320, 1150, 1.5, 1.3, "none")
for k, word in enumerate(("Hallo.", "Ich.", "Bin.", "Pleite.")):
    tj = ww("s8", word, o=-.08); pop(f"#jw{k}", tj, .2, "50% 50%"); J.append(f'tl.set("#jw{k}", {{ opacity: 1 }}, {F(tj + .21)});'); FX += [("pop", tj, .5, .25)]
    if k == 0: cut(tj, 640, 900, 1.0)
expr("j8", "happy", "sad", ww("s8", "Pleite.", o=-.08)); cut(ww("s8", "Pleite.", o=-.08), 540, 960, 1.05)
# s9 Bürgermeister: Limit weg – seine Nachricht ist die 21.
t9 = t["s9"]; cut(t9, 540, 1000, 1.1); cam(t9 + .05, 540, 900, 1.3, 1.2, "none")
t21 = ww("s9", "einundzwanzigste"); cut(t21, 540, 700, 1.4); setz("z9", t21, "21 / 20", "20 / 20", "#e63946"); blink("#z9-in", t21, 7, .12, .2); FX += [("klong", t21, .5, .5)]
expr("b9", "determined", "shock", t21)
tla = ww("s9", "Laut."); cut(tla, 540, 1200, 1.0); blare("mal", tla); shake(tla + .1, 7, 10); J.append('tl.set("#bubl", { opacity: 0 }, 0);'); pop("#bubl", tla + .1, .25, "50% 50%"); FX += [("glitch", tla + .45, .2, .4)]
cut(ww("s9", "alle."), 540, 1500, 1.3)
# s10 Mama: Nachricht 63, 40 x Daumen hoch
t10 = t["s10"]; cut(t10, 540, 1200, 1.2); cam(t10 + .05, 540, 1150, 1.4, 1.2, "none")
t63 = ww("s10", "dreiundsechzig"); cut(t63, 540, 1000, 1.5); FX += [("chime", t63, .4, .5)]
tvm = ww("s10", "Vierzigmal"); cut(tvm, 540, 900, 1.0)
J.append(f'tl.set("#thumbs", {{ opacity: 1 }}, {F(tvm)}); tl.fromTo("#thumbs .th", {{ opacity: 0, scale: .2, transformOrigin: "50% 50%" }}, {{ opacity: 1, scale: 1, duration: .15, stagger: .03, immediateRender: false }}, {F(tvm)});')
FX += [("blips", tvm, .35, 1.4)]
tdh = ww("s10", "Daumen"); pop("#sg10b", tdh, .3, "50% 50%"); J.append(f'tl.set("#sg10b", {{ opacity: 1 }}, {F(tdh + .31)});'); cut(tdh, 540, 700, 1.25); FX += [("hit", tdh, .5, .5)]
expr("m10", "grin", "laugh", tdh)
# s11 Zähler piept – meine stumme Gruppe wird vorgelesen – alle 1.400
t11 = t["s11"]; cut(t11, 540, 900, 1.0); cam(t11 + .05, 540, 600, 1.5, 1.5, "power1.in"); blink("#zal-in", t11 + .2, 11, .12, .15); shake(t11 + .3, 11, 12)
J.append(f'tl.to("#red11", {{ opacity: .9, duration: .3 }}, {F(t11 + .2)});'); FX += [("tick", t11, .5, 1.6), ("riser", t11 + .3, .35, 1.2)]
tsg = ww("s11", "stumme", o=-.3); cut(tsg, 540, 1100, 1.3); expr("i11", "shock", "panic", tsg); FX += [("hit", tsg, .6, .5)]
tal = ww("s11", "Alle"); cut(tal, 540, 800, 1.3); count("z11-t", tal, 0, 1400, .8); FX += [("blips", tal, .3, .9)]
# s12 Nachricht 1: Guten Morgen, ihr Lieben – Stadt kichert
t12 = t["s12"]; cut(t12, 540, 900, 1.3); blare("mag", t12 + .1, 11); shake(t12 + .1, 9, 12); FX += [("glitch", ww("s12", "knacken.") + .3, .2, .4)]
J.append('tl.set("#bubg", { opacity: 0 }, 0);'); tgm = ww("s12", "Guten"); pop("#bubg", tgm, .25, "50% 50%"); cut(tgm, 540, 650, 1.15); FX += [("pop", tgm, .5, .3)]
tki = ww("s12", "kichert.", o=-.4); cut(tki, 540, 1300, 1.0)
for k in range(5): expr(f"cg{k}", "neutral", "laugh", tki + k * .05)
# s13 Nachricht 612: Foto mit Zahnspange + Topfhaarschnitt
t13 = t["s13"]; cut(t13, 540, 900, 1.0); FX += [("whoosh", t13, .35, .4)]
tzs = ww("s13", "Zahnspange"); cut(tzs, 540, 700, 1.6); FX += [("boing", tzs, .45, .3)]
tth = ww("s13", "Topfhaarschnitt."); cut(tth, 540, 560, 1.8)
tsh = ww("s13", "ganze", o=-.2); cut(tsh, 540, 1500, 1.1); cam(tsh + .05, 540, 1100, .9 if False else 1.0, 1.0, "power1.out")
for k in range(5): expr(f"cf{k}", "shock", "laugh", tsh + .3 + k * .06)
# s14 Nachricht 1.347 – Stadt hält die Luft an – Oma dreht lauter (Trommelwirbel)
t14 = t["s14"]; cut(t14, 540, 900, 1.0); cam(t14 + .05, 540, 600, 1.4, 2.0, "power1.in"); FX += [("riser", t14, .3, 1.5)]
tlu = ww("s14", "Luft", o=-.4); cut(tlu, 540, 1600, 1.3); FX += [("wirbel", tlu, .45, 3.0)]
tom = ww("s14", "Oma", o=-.15); cut(tom, 380, 1250, 1.3); J.append(f'tl.to("#knob", {{ rotation: 150, transformOrigin: "50% 50%", duration: .8, ease: "power2.inOut" }}, {F(tom + .3)});')
cut(ww("s14", "lauter.", o=-.1), 800, 1150, 1.5); shake(ww("s14", "lauter.") + .2, 9, 10)
# s15 Frage
t15 = t["s15"]; cut(t15, 540, 960, 1.1); cam(t15 + .05, 540, 960, 1.2, 1.6, "none"); FX += [("hit", t15, .5, .5)]
J.append(f'tl.to("#st15-in", {{ scale: 1.05, transformOrigin: "50% 50%", duration: .3, yoyo: true, repeat: 5 }}, {F(t15 + .3)});')
# s16 Loop: Split vom Anfang – jetzt ich 1.400 (rot) vs Mama 63
t16 = t["s16"]; cut(t16, 540, 960, 1.15); cam(t16 + .3, 540, 960, 1.0, 1.2, "power2.inOut"); FX += [("whoosh", t16, .35, .4)]
blink("#biz-in", t16 + .3, 11, .2, .3)
# Schlussbild bleibt ohne Zoom (nichts abgeschnitten, keine Überlappung mit Banner/Box)

sets = [("SPLIT", 0, c1), ("RATHAUS", c1, t2), ("SPLIT", t2, t3), ("RATHAUS", t3, tk), ("KUECHE", tk, t4), ("VORLESEN", t4, t5), ("STUMM", t5, t6), ("OMA", t6, t7),
        ("MILCH", t7, tb), ("BUS", tb, t8), ("JONAS", t8, t9), ("BGM", t9, tla), ("LAUT", tla, t10), ("MAMA2", t10, t11), ("ALARM", t11, tsg), ("ICH2", tsg, t12),
        ("MORGEN", t12, t13), ("FOTO", t13, t14), ("SPANNUNG", t14, tom), ("KNOPF", tom, t15), ("TIPP", t15, t16), ("LOOP", t16, END)]
tag = f'<div class="ui clip" data-start="0" data-duration="{F(END)}" style="right:24px;top:40px;font:900 30px Inter,sans-serif;color:#fff;background:rgba(0,0,0,.55);padding:6px 14px;border-radius:12px">TEIL 1</div>'
cta = (f'<div class="ui clip" data-start="{F(t16 + .1)}" data-duration="{F(END - t16 - .1)}" style="left:60px;right:60px;top:1400px;text-align:center">'
       f'<div id="cta-in" style="display:inline-block;background:#fff;color:#111;border:7px solid #111;border-radius:26px;padding:16px 26px;font:900 54px/1.18 Inter,sans-serif">'
       f'Folg mir und schreib <span style="color:#e63946">‚Teil 2‘</span> in die Kommentare, dann kommt die Fortsetzung!</div></div>')
J.append(f'tl.fromTo("#cta-in", {{ y: 80, opacity: 0 }}, {{ y: 0, opacity: 1, duration: .3, ease: "back.out(2)", immediateRender: false }}, {F(t16 + .12)});')
OBEN = [(0, f"MAX. {R}20 NACHRICHTEN{X} AM TAG"), (t2, f"ICH {G_}2{X} vs MAMA {R}63{X}"), (t3, "⏰ ZÄHLER ÜBERM RATHAUS"), (tk, f"MAMA: {R}20{X} BEIM FRÜHSTÜCK"), (t4, "📢 ÜBERZOGEN = VORLESEN"),
        (t5, "🤫 MEIN GEHEIMNIS"), (t6, "OMA: 📸 📸 📸"), (t7, f"MAMA: {R}21{X} 📢"), (t8, "JONAS: 1 WORT = 1 NACHRICHT"), (t9, "BÜRGERMEISTER 🎩"),
        (t10, f"{R}40×{X} 👍"), (t11, f"🚨 {R}1.400{X} UNGELESEN"), (t12, "NACHRICHT #1"), (t13, "NACHRICHT #612"), (t14, f"NACHRICHT {R}#1.347{X}"), (t15, "WAS STEHT DRIN?"),
        (t16, f"ICH {R}1.400{X} vs MAMA 63")]
HOT = {"FAMILIENGRUPPE", "NACHRICHTEN", "MAMA", "OMA", "ZÄHLER", "GEHEIMNIS", "STUMM", "UNGELESEN", "FOTO", "MILCH", "BUSFAHRER", "JONAS", "PLEITE", "BÜRGERMEISTER",
       "LAUT", "DAUMEN", "ZAHNSPANGE", "TOPFHAARSCHNITT", "LAUTER", "TEIL"}
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
