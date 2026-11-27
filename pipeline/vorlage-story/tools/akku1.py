"""STORY „In dieser Stadt …“ – NEUE SERIE „Akku-Stadt“, TEIL 1: Jeder hat seinen Handy-Akku über dem Kopf, bei 0 % schläfst du sofort ein.
Aufruf: python3 tools/akku1.py  (liest voice.json + assets/vo/timing.json; Bausteine aus tools/bausteine.py; Figuren wie sprach1;
Musik = fester Hintergrund-Sound assets/bgm.mp3 über tools/story_musik.py)"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bausteine import *

# ---------- Figuren (wie Sprachnachrichten-Stadt) ----------
for k, v in {"sleep": '<path d="M-46 0 Q-30 10 -14 0 M14 0 Q30 10 46 0" stroke="#111" stroke-width="7" fill="none" stroke-linecap="round"/><ellipse cx="0" cy="38" rx="12" ry="9" fill="#5a1a1a"/>',
             "smug": '<path d="M-46 -6 H-14" stroke="#111" stroke-width="8" stroke-linecap="round"/>' + E(30, -5) + '<path d="M-24 34 Q4 48 30 28" stroke="#111" stroke-width="7" fill="none" stroke-linecap="round"/>'}.items():
    FACES.setdefault(k, v)
for k in ("panic", "grin", "wink", "sad", "determined", "confused", "laugh", "neutral", "shock", "happy"):
    FACES.setdefault(k, FACES["happy"])
HAIR.setdefault("ich", lambda c: f'<path d="M-100 -36 V-100 Q-100 -114 -86 -114 H86 Q100 -114 100 -100 V-36 L74 -64 L40 -80 L0 -66 L-40 -84 L-76 -62 Z" fill="{c}" stroke="#111" stroke-width="4"/>')
HAIR.setdefault("cap", lambda c: f'<path d="M-104 -60 Q-104 -150 0 -150 Q104 -150 104 -60 Z" fill="{c}" stroke="#111" stroke-width="5"/><rect x="-20" y="-82" width="190" height="26" rx="10" fill="{c}" stroke="#111" stroke-width="4"/>')
HAIR.setdefault("hut", lambda c: '<path d="M-100 -30 V-90 L-80 -70 H80 L100 -90 V-30 Z" fill="#ccc"/><rect x="-140" y="-120" width="280" height="30" rx="10" fill="#111"/><rect x="-80" y="-250" width="160" height="140" rx="10" fill="#111"/><rect x="-80" y="-150" width="160" height="26" fill="#e63946"/>')
KR_ACC = '<rect x="-62" y="-22" width="48" height="36" rx="8" fill="none" stroke="#111" stroke-width="6"/><rect x="14" y="-22" width="48" height="36" rx="8" fill="none" stroke="#111" stroke-width="6"/><path d="M-14 -6 H14" stroke="#111" stroke-width="6"/>'
OMA_ACC = '<rect x="-64" y="-20" width="46" height="34" rx="16" fill="none" stroke="#555" stroke-width="5"/><rect x="18" y="-20" width="46" height="34" rx="16" fill="none" stroke="#555" stroke-width="5"/>'
CURLERS = "".join(f'<rect x="{x - 22}" y="-132" width="44" height="34" rx="12" fill="{c}" stroke="#111" stroke-width="4"/>' for x, c in ((-60, "#ff8fab"), (0, "#4cc9f0"), (60, "#ffd166")))
TIE = '<path d="M0 -296 L-18 -270 L0 -150 L18 -270 Z" fill="#2d6a4f" stroke="#111" stroke-width="4"/>'
SASH = '<path d="M-90 -290 L90 -80" stroke="#e63946" stroke-width="34"/><rect x="-24" y="-240" width="48" height="48" rx="24" fill="#ffd166" stroke="#111" stroke-width="4"/>'
PHONE_R = '<g transform="translate(196 -330)"><rect x="-30" y="-56" width="60" height="104" rx="12" fill="#222" stroke="#111" stroke-width="4"/><rect x="-22" y="-46" width="44" height="80" rx="6" fill="#8ecae6"/></g>'
CABLE_R = '<g transform="translate(196 -330)"><rect x="-26" y="-40" width="52" height="70" rx="10" fill="#fff" stroke="#111" stroke-width="5"/><rect x="-14" y="-62" width="8" height="24" fill="#999"/><rect x="6" y="-62" width="8" height="24" fill="#999"/><path d="M0 30 Q-40 160 -200 260" stroke="#fff" stroke-width="14" fill="none"/></g>'
NEEDLES = '<g transform="translate(0 -230)"><path d="M-120 -40 L60 40 M120 -40 L-60 40" stroke="#bc6c25" stroke-width="10" stroke-linecap="round"/><rect x="-70" y="-10" width="140" height="80" rx="30" fill="#ff8fab" stroke="#111" stroke-width="5"/></g>'
EXI = ("happy", "smug", "shock", "panic", "determined", "neutral", "grin", "sleep", "confused")
def ich_(uid, start="happy", arm=("down", "down"), extra="", exprs=EXI): return person(uid, "ich", "#6b3e26", "#118ab2", exprs=exprs, start=start, arm=arm, extra=extra)
def oma_(uid, start="happy", arm=("down", "front"), extra="", exprs=("happy", "laugh", "grin", "wink", "smug", "sleep", "sad")):
    return person(uid, "oma", "#e0e0e0", "#9d4edd", exprs=exprs, start=start, arm=arm, head_acc=OMA_ACC + CURLERS, extra=extra)
def emil(uid, start="happy", arm=("down", "front"), extra="", exprs=("happy", "shock", "panic", "sleep", "neutral")):
    return person(uid, "cap", "#e63946", "#f77f00", skin="#c68642", exprs=exprs, start=start, arm=arm, extra=extra)
def krause_(uid, start="neutral", arm=("down", "front"), extra="", exprs=("neutral", "smug", "shock", "determined")):
    return person(uid, "glatze", "#555", "#adb5bd", exprs=exprs, start=start, arm=arm, head_acc=KR_ACC, extra=TIE + extra)
def bgm_(uid, start="neutral", arm=("front", "front"), extra=""):
    return person(uid, "hut", "#ccc", "#264653", exprs=("neutral", "happy", "sleep"), start=start, arm=arm, extra=SASH + extra)
def tiny(uid, k, ex="happy", arm=("down", "down")):
    hair = ("mann", "lena", "oma", "ich", "cap", "mann")[k % 6]
    hc = ("#3d2b1f", "#f4d35e", "#ddd", "#111", "#7b2cbf", "#2d6a4f")[k % 6]
    sh = ("#e76f51", "#3a86ff", "#9d4edd", "#06d6a0", "#ffbe0b", "#ef476f")[k % 6]
    return person(uid, hair, hc, sh, skin=("#f2c9a5", "#c68642", "#8d5524")[k % 3], exprs=(ex, "sleep"), start=ex, arm=arm)
def txt(x, y, s, size=60, col="#111", anchor="middle"): return f'<text x="{x}" y="{y}" text-anchor="{anchor}" style="font:900 {size}px {FONT};fill:{col}">{s}</text>'
def sign(uid, x, y, wd, h, lines, col="#fff", fg="#111", size=70, vis=True, rot=0):
    t = "".join(txt(0, -h / 2 + 30 + (k + .85) * size * 1.15 - 10, l, size, fg) for k, l in enumerate(lines))
    return (f'<g id="{uid}" opacity="{1 if vis else 0}" transform="translate({x} {y}) rotate({rot})"><g id="{uid}-in"><rect x="{-wd/2 + 8}" y="{-h/2 + 8}" width="{wd}" height="{h}" rx="26" fill="#000" opacity=".25"/>'
            f'<rect x="{-wd/2}" y="{-h/2}" width="{wd}" height="{h}" rx="26" fill="{col}" stroke="#111" stroke-width="8"/>{t}</g></g>')
# Akku-Anzeige über dem Kopf: Kasten mit Füllbalken + Prozent
BCOL = lambda p: "#2dc653" if p >= 50 else ("#ffbe0b" if p >= 20 else "#e63946")
def akku(uid, x, y, p, s=1.0, vis=True):
    wfill = max(6, 220 * p / 100)
    return (f'<g id="{uid}" opacity="{1 if vis else 0}" transform="translate({x} {y}) scale({s})"><g id="{uid}-in">'
            f'<rect x="-130" y="-60" width="260" height="120" rx="22" fill="#111" stroke="#fff" stroke-width="8"/><rect x="130" y="-24" width="26" height="48" rx="8" fill="#fff"/>'
            f'<rect id="{uid}-f" x="-110" y="-40" width="{wfill:.0f}" height="80" rx="10" fill="{BCOL(p)}"/>'
            f'<text id="{uid}-t" x="0" y="26" text-anchor="middle" style="font:900 72px {FONT};fill:#fff;stroke:#111;stroke-width:6px;paint-order:stroke">{p} %</text></g></g>')
def setakku(uid, t, p, prev, d=.0):
    J.append(f'tl.call(() => {{ document.getElementById("{uid}-t").textContent = "{p} %"; }}, null, {F(t)}); tl.call(() => {{ document.getElementById("{uid}-t").textContent = "{prev} %"; }}, null, {F(max(0, t - .01))});')
    J.append(f'tl.to("#{uid}-f", {{ attr: {{ width: {max(6, 220 * p / 100):.0f} }}, fill: "{BCOL(p)}", duration: {max(.05, d)} }}, {F(t)});')
def zzz(uid, x, y, vis=False):
    return f'<g id="{uid}" opacity="{1 if vis else 0}">' + "".join(txt(x + k * 50, y - k * 60, "Z", 70 + k * 20, "#fff") for k in range(3)) + '</g>'
def socket(x, y): return f'<g transform="translate({x} {y})"><rect x="-70" y="-70" width="140" height="140" rx="20" fill="#f8f9fa" stroke="#111" stroke-width="6"/><circle cx="-24" cy="0" r="12" fill="#111"/><circle cx="24" cy="0" r="12" fill="#111"/></g>'

S = {}; FX = []
# --- SPLIT: links ich 2 %, rechts Oma 100 %
def split(sfx, pi, po):
    L = street_bg() + fig(ich_(f"i{sfx}", "panic" if pi < 50 else "grin", arm=("down", "front"), extra=PHONE_R), 270, 1500, 1.15) + akku(f"ai{sfx}", 270, 760, pi, .95)
    Rr = ('<rect width="1080" height="1920" fill="#ffd6a5"/>' + street_bg().replace('#8ecae6', '#ffd6a5') +
          fig(oma_(f"o{sfx}", "laugh" if po > 50 else "sad", arm=("down", "front")), 800, 1500, 1.15) + akku(f"ao{sfx}", 800, 760, po, .95))
    return (f'<defs><clipPath id="cl{sfx}"><rect width="540" height="1920"/></clipPath><clipPath id="cr{sfx}"><rect x="540" width="540" height="1920"/></clipPath></defs>'
            f'<g clip-path="url(#cl{sfx})">{L}</g><g clip-path="url(#cr{sfx})">{Rr}</g><rect x="532" width="16" height="1920" fill="#fff" stroke="#111" stroke-width="4"/>')
S["SPLIT"] = split("a", 2, 100)
S["LOOP"] = split("z", 100, 3)
S["STADT"] = (street_bg() + "".join(fig(tiny(f"t1{k}", k, "happy"), 140 + k * 200, 1500, .62) + akku(f"a1{k}", 140 + k * 200, 1060, (87, 54, 23, 71, 9)[k], .55) for k in range(5)))
S["SCHLAF"] = (street_bg() + fig(tiny("t1s", 3, "sleep"), 540, 1700, 1.6) + akku("a1s", 540, 760, 0, 1.0) + zzz("z1", 700, 900, True))
S["STECK"] = (room_bg("#cdb4db", "#9a8c98", win=True) + socket(900, 1200) + fig(oma_("o3", "sleep", arm=("down", "down")), 520, 1650, 1.5) +
              '<path d="M520 960 Q700 900 830 1200" stroke="#fff" stroke-width="16" fill="none"/><path d="M520 960 Q700 900 830 1200" stroke="#111" stroke-width="4" fill="none" stroke-dasharray="1 0" opacity=".3"/>' +
              akku("a3", 520, 420, 100, 1.0) + zzz("z3", 700, 600, True))
S["KLASSE"] = (room_bg("#e9f5db", "#b08968", win=False) + '<rect x="90" y="250" width="900" height="380" rx="16" fill="#2d6a4f" stroke="#6b4226" stroke-width="18"/>' +
               txt(540, 470, "MATHETEST", 110, "#fff") + fig(emil("e4", "panic", arm=("front", "front")), 540, 1700, 1.5) +
               '<rect x="160" y="1500" width="760" height="60" rx="10" fill="#bc6c25" stroke="#111" stroke-width="7"/>' + akku("a4", 540, 830, 1, 1.0) + zzz("z4", 720, 1000))
S["KRAUSE"] = (room_bg("#e9f5db", "#b08968", win=False) + fig(krause_("k6", "smug", arm=("down", "front"),
               extra='<g transform="translate(196 -330)"><rect x="-60" y="-90" width="120" height="180" rx="20" fill="#111" stroke="#fff" stroke-width="6"/><rect x="-40" y="-60" width="80" height="40" rx="8" fill="#2dc653"/><text x="0" y="40" text-anchor="middle" style="font:900 34px Inter,sans-serif;fill:#fff">⚡</text></g>'), 400, 1750, 1.5) +
               sign("sg6", 760, 700, 520, 230, ["NUR GEGEN", "EINE 1!"], col="#ffd166", size=80, vis=False))
crowd7 = "".join(fig(tiny(f"t7{k}", k, "neutral"), 110 + k * 215, 1880, .55) + akku(f"a7{k}", 110 + k * 215, 1460, (64, 41, 88, 23, 57)[k], .5) for k in range(5))
S["REDE"] = (street_bg() + '<rect x="380" y="900" width="320" height="300" rx="16" fill="#6b4226" stroke="#111" stroke-width="8"/>' + fig(bgm_("b7", "happy"), 540, 1000, 1.0) +
             sign("sg7", 540, 300, 600, 150, ["REDE: 4:00:00"], col="#fff", size=80) + crowd7)
crowd8 = "".join(fig(tiny(f"t8{k}", k, "sleep"), 110 + k * 215, 1880, .55) + akku(f"a8{k}", 110 + k * 215, 1460, 0, .5) for k in (0, 1, 3, 4))
S["OMA98"] = (street_bg(night=True) + crowd8 + fig(oma_("o8", "smug", arm=("front", "front"), extra=NEEDLES), 540, 1600, 1.4) + akku("a8o", 540, 760, 98, 1.0))
S["RENN"] = ('<rect width="1080" height="1920" fill="#8ecae6"/><g id="wbg">' + street_bg().replace('<rect width="1080" height="1920" fill="#8ecae6"/>', '') + '</g>' +
             '<g id="walker">' + fig(ich_("i9", "determined", arm=("down", "front"), extra=PHONE_R), 540, 1750, 1.5) + '</g>' + akku("a9", 540, 760, 2, 1.0))
S["HANDY"] = ('<rect width="1080" height="1920" fill="#222"/><rect x="190" y="200" width="700" height="1500" rx="80" fill="#111" stroke="#555" stroke-width="12"/><rect x="230" y="300" width="620" height="1300" rx="30" fill="#ff006e"/>' +
              txt(540, 900, "▶", 260, "#fff") + txt(540, 1150, "NOCH EIN VIDEO …", 60, "#fff") + akku("a10", 540, 420, 2, .9))
S["KABEL"] = (street_bg() + fig(ich_("i11", "shock", arm=("down", "front"), extra=PHONE_R), 280, 1700, 1.2) + akku("a11i", 280, 900, 1, .75) +
              fig(oma_("o11", "grin", arm=("down", "front"), extra=CABLE_R), 780, 1700, 1.2) + akku("a11o", 780, 900, 97, .75) +
              bubble("bub12", ["Ich lade dich auf –", "aber nur, wenn du", "mich jeden Sonntag", "anrufst!"], 540, 500, 860, size=54))
S["SWAP"] = (street_bg() + fig(ich_("i14", "shock", arm=("up", "up")), 280, 1700, 1.2) + akku("a14i", 280, 900, 1, .75) +
             fig(oma_("o14", "grin", arm=("down", "front")), 780, 1700, 1.2) + akku("a14o", 780, 900, 97, .75) +
             '<path d="M330 1190 Q540 1100 730 1190" stroke="#fff" stroke-width="16" fill="none"/>' + '<g id="spark" opacity="0">' + "".join(txt(330 + k * 100, 1150 - (k % 2) * 40, "⚡", 70) for k in range(5)) + '</g>')
lines15 = "".join(f'<path d="M540 1150 Q{(540 + x) / 2:.0f} {700 - abs(540 - x) * .3:.0f} {x} {y}" stroke="#ffd60a" stroke-width="8" fill="none" opacity=".9"/>' for x, y in ((110, 1050), (300, 980), (780, 980), (970, 1050), (200, 1250), (880, 1250)))
S["NETZ"] = (street_bg(night=True) + '<g id="net" opacity="0">' + lines15 + '</g>' + fig(oma_("o15", "smug", arm=("front", "front"), extra=NEEDLES), 540, 1500, 1.0) + akku("a15", 540, 980, 3, .6))
S["DUNKEL"] = ('<rect width="1080" height="1920" fill="#0b132b"/>' + fig(oma_("o16", "sleep", arm=("down", "down")), 540, 1700, 1.6) + akku("a16", 540, 760, 3, 1.0) +
               '<rect id="dark16" width="1080" height="1920" fill="#000" opacity="0"/>')
S["TIPP"] = (street_bg(night=True) + fig(ich_("i17", "panic", arm=("front", "front"), exprs=("panic",)), 540, 1850, 1.8) + akku("a17", 540, 760, 100, 1.0) +
             sign("st17", 540, 300, 860, 170, ["WAS SOLL ICH TUN?"], col="#ffd166", size=78))

# ---------- Zeitplan ----------
J.append('tl.set("#cam", { x: 0, y: 0, scale: 1, svgOrigin: "0 0" }, 0);')
t = {k: st(k) for k in T}
# s1 Hook: Split-Bild sofort, Punch-Zoom; bei "0 %" Schnitt auf Schläfer
cut(0, 540, 960, 1.08); cam(.02, 540, 960, 1.0, .35, "power3.out"); FX += [("hit", 0, .5, .8)]
J.append(f'tl.to("#aia-in", {{ opacity: .3, duration: .2, yoyo: true, repeat: 15, ease: "steps(1)" }}, 0);')
c1 = round(min(1.6, w("s1", "Akku") - .1), 2)
cut(c1, 540, 1100, 1.0); FX += [("whoosh", c1, .3, .4)]
tnull = w("s1", "null") - .15
J.append(f'tl.set("#t1s-sleep", {{ opacity: 1 }}, 0);')
cut(tnull, 540, 1200, 1.3); cam(tnull + .05, 540, 1100, 1.45, 1.2, "none"); FX += [("klong", tnull + .3, .4, .5)]
# s2 Split: ich 2 % vs Oma 100 %
t2 = t["s2"]; cut(t2, 270, 1150, 1.4); tom = w("s2", "Oma:") - .2
cut(tom, 800, 1150, 1.4); FX += [("swoosh", tom, .4, .4), ("chime", tom + .4, .4, .6)]
# s3 Oma an der Steckdose
t3 = t["s3"]; J.append(f'tl.set("#cam", {{ x: 0 }}, {F(t3)});'); cut(t3, 540, 1300, 1.1); cam(t3 + .05, 640, 1150, 1.3, 1.6, "none")
tlw = w("s3", "Lockenwicklern.") - .2; cut(tlw, 520, 1050, 2.0); FX += [("boing", tlw, .4, .3)]
# s4/s5 Emil im Mathetest
t4 = t["s4"]; cut(t4, 540, 1250, 1.1); te1 = w("s4", "Prozent.") - .3
J.append(f'tl.to("#a4-in", {{ opacity: .2, duration: .15, yoyo: true, repeat: 13, ease: "steps(1)" }}, {F(te1)});'); cut(te1, 540, 900, 1.5); FX += [("tick", te1, .4, 1.6)]
cut(w("s4", "Mitten") - .1, 540, 800, 1.0)
t5 = t["s5"]; tz = w("s5", "Zack.") - .05
setakku("a4", tz, 0, 1); expr("e4", "panic", "sleep", tz); J.append(f'tl.set("#z4", {{ opacity: 1 }}, {F(tz)}); tl.to("#e4", {{ rotation: 22, transformOrigin: "50% 100%", duration: .3, ease: "power2.in" }}, {F(tz + .1)});')
cut(tz, 540, 1300, 1.2); shake(tz + .35, 8, 14); FX += [("hit", tz + .35, .6, .6), ("splat", tz + .4, .4, .4)]
cut(w("s5", "Gesicht") - .1, 640, 1500, 1.8)
# s6 Krause + Powerbank
t6 = t["s6"]; cut(t6, 500, 1200, 1.2); cam(t6 + .05, 560, 1250, 1.4, 1.4, "none"); FX += [("chime", t6 + .5, .35, .6)]
teins = w("s6", "nur") - .1; cut(teins, 640, 800, 1.0); pop("#sg6", teins + .05, .25, "50% 50%"); FX += [("pop", teins + .05, .5, .3)]
# s7 Rede 4 Stunden -> alle 0 %
t7 = t["s7"]; cut(t7, 540, 1100, 1.2); cam(t7 + .05, 540, 1050, 1.35, 1.2, "none")
tvs = w("s7", "Vier") - .1; cut(tvs, 540, 500, 1.1); FX += [("tick", tvs, .3, 1.0)]
tnu = w("s7", "fällt") - .2; cut(tnu, 540, 1500, 1.05); FX += [("klong", tnu + .4, .5, .6)]
for k in range(5):
    setakku(f"a7{k}", tnu + .1, 0, (64, 41, 88, 23, 57)[k], .5); J.append(f'tl.to("#t7{k}", {{ rotation: {(-1) ** k * 80}, transformOrigin: "50% 100%", duration: .3 }}, {F(tnu + .5 + k * .08)});')
    expr(f"t7{k}", "neutral", "sleep", tnu + .5)
# s8 Nur Oma nicht – strickt
t8 = t["s8"]; cut(t8, 540, 1300, 1.0); t98 = w("s8", "Achtundneunzig") - .1; cut(t98, 540, 900, 1.3); FX += [("chime", t98, .4, .6)]
tsk = w("s8", "strickt.") - .2; cut(tsk, 540, 1350, 1.6); J.append(f'tl.to("#o8", {{ rotation: 4, transformOrigin: "50% 100%", duration: .15, yoyo: true, repeat: 7 }}, {F(tsk)});')
# s9 Rennen + scrollen kostet 1 %
t9 = t["s9"]; cut(t9, 540, 1200, 1.0)
J.append(f'tl.fromTo("#wbg", {{ x: 0 }}, {{ x: -1080, duration: {F(t["s10"] - t9)}, ease: "none", immediateRender: false }}, {F(t9)}); tl.to("#walker", {{ y: -18, duration: .15, yoyo: true, repeat: {int((t["s10"] - t9) / .15)} }}, {F(t9)});')
tvi = w("s9", "Jedes") - .1; cut(tvi, 600, 950, 1.3); FX += [("whoosh", tvi, .3, .4)]
J.append(f'tl.to("#a9-in", {{ opacity: .25, duration: .2, yoyo: true, repeat: 9, ease: "steps(1)" }}, {F(tvi)});')
# s10 Ein Video noch -> 1 %
t10 = t["s10"]; cut(t10, 540, 950, 1.0); cam(t10 + .05, 540, 900, 1.2, 1.5, "none"); FX += [("blips", t10, .3, 1.0)]
tp1 = w("s10", "Ein", 2) - .1; setakku("a10", tp1, 1, 2); cut(tp1, 540, 450, 1.6); FX += [("hit", tp1, .5, .6)]
J.append(f'tl.to("#a10-in", {{ opacity: .2, duration: .12, yoyo: true, repeat: 9, ease: "steps(1)" }}, {F(tp1)});')
# s11-s13 Oma mit Kabel
t11 = t["s11"]; cut(t11, 280, 1300, 1.3); tom11 = w("s11", "Oma.") - .1; cut(tom11, 780, 1250, 1.4); FX += [("boing", tom11, .4, .3)]
cut(w("s11", "Ladekabel.") - .2, 840, 1400, 2.2)
t12 = t["s12"]; cut(t12, 540, 1000, 1.0); J.append('tl.set("#bub12", { opacity: 0 }, 0);'); pop("#bub12", t12 + .1, .25, "50% 50%"); FX += [("pop", t12 + .1, .4, .3)]
cut(w("s12", "jeden") - .1, 540, 800, 1.2)
t13 = t["s13"]; hide("#bub12", t13, .1); cut(t13, 280, 1250, 1.5); expr("i11", "shock", "determined", t13)
tst = w("s13", "steckt") - .1; cut(tst, 540, 1350, 1.1); FX += [("klong", tst + .3, .4, .4)]
# s14 Twist: Akkus tauschen
t14 = t["s14"]; cut(t14, 540, 1300, 1.0); J.append(f'tl.set("#spark", {{ opacity: 1 }}, {F(t14)}); tl.to("#spark", {{ opacity: .1, duration: .1, yoyo: true, repeat: 15 }}, {F(t14)});')
th = w("s14", "hundert.") - .3
J.append(f'(() => {{ const o = {{ v: 1 }}; tl.fromTo(o, {{ v: 1 }}, {{ v: 100, duration: .7, ease: "power2.in", immediateRender: false, onUpdate: () => {{ document.getElementById("a14i-t").textContent = Math.round(o.v) + " %"; }} }}, {F(th - .5)}); }})();')
J.append(f'tl.to("#a14i-f", {{ attr: {{ width: 220 }}, fill: "#2dc653", duration: .7 }}, {F(th - .5)});'); cut(th, 280, 1050, 1.4); FX += [("riser", th - .6, .4, .8), ("chime", th + .2, .5, .8)]
expr("i14", "shock", "grin", th + .2)
td = w("s14", "drei.") - .3
J.append(f'(() => {{ const o = {{ v: 97 }}; tl.fromTo(o, {{ v: 97 }}, {{ v: 3, duration: .6, ease: "power2.in", immediateRender: false, onUpdate: () => {{ document.getElementById("a14o-t").textContent = Math.round(o.v) + " %"; }} }}, {F(td - .4)}); }})();')
J.append(f'tl.to("#a14o-f", {{ attr: {{ width: 7 }}, fill: "#e63946", duration: .6 }}, {F(td - .4)});'); cut(td, 780, 1050, 1.5); shake(td + .2, 8, 14); FX += [("hit", td + .2, .7, .8)]
# s15 Netz: Oma hat die ganze Stadt geladen
t15 = t["s15"]; cut(t15, 540, 1200, 1.4); cam(t15 + .05, 540, 1150, 1.0, 2.0, "power1.inOut")
J.append(f'tl.fromTo("#net", {{ opacity: 0 }}, {{ opacity: 1, duration: .6, immediateRender: false }}, {F(w("s15", "ganze") - .2)}); tl.to("#net", {{ opacity: .4, duration: .2, yoyo: true, repeat: 9 }}, {F(w("s15", "ganze") + .5)});')
FX += [("riser", t15, .35, 1.2)]
# s16 Dunkel – niemand lädt Oma auf
t16 = t["s16"]; cut(t16, 540, 1200, 1.2); cam(t16 + .05, 540, 900, 1.6, T["s16"]["slot"], "power1.in")
J.append(f'tl.to("#a16-in", {{ opacity: .15, duration: .25, yoyo: true, repeat: 11, ease: "steps(1)" }}, {F(t16 + .3)}); tl.to("#dark16", {{ opacity: .55, duration: {F(T["s16"]["slot"])} }}, {F(t16)});')
FX += [("wirbel", t16 + .3, .4, min(3.0, T["s16"]["slot"]))]
# s17 Tipp
t17 = t["s17"]; cut(t17, 540, 1050, 1.15); cam(t17 + .05, 540, 1050, 1.25, 2.0, "none"); FX += [("whoosh", t17, .3, .4)]
J.append(f'tl.to("#st17-in", {{ scale: 1.05, transformOrigin: "50% 50%", duration: .3, yoyo: true, repeat: 5 }}, {F(t17 + .3)});')
# s18 Loop zurück zum Split – jetzt ich 100 %, Oma 3 %
t18 = t["s18"]; cut(t18, 540, 960, 1.15); cam(t18 + .3, 540, 960, 1.0, 1.2, "power2.inOut"); FX += [("whoosh", t18, .3, .4)]
J.append(f'tl.to("#aoz-in", {{ opacity: .2, duration: .25, yoyo: true, repeat: 15, ease: "steps(1)" }}, {F(t18)});')

sets = [("SPLIT", 0, c1), ("STADT", c1, tnull), ("SCHLAF", tnull, t2), ("SPLIT", t2, t3), ("STECK", t3, t4), ("KLASSE", t4, t6), ("KRAUSE", t6, t7), ("REDE", t7, t8), ("OMA98", t8, t9),
        ("RENN", t9, t10), ("HANDY", t10, t11), ("KABEL", t11, t14), ("SWAP", t14, t15), ("NETZ", t15, t16), ("DUNKEL", t16, t17), ("TIPP", t17, t18), ("LOOP", t18, END)]
tag = f'<div class="ui clip" data-start="0" data-duration="{F(END)}" style="right:24px;top:40px;font:900 30px Inter,sans-serif;color:#fff;background:rgba(0,0,0,.55);padding:6px 14px;border-radius:12px">TEIL 1</div>'
R = "<span style='color:#ff4d5a'>"; G_ = "<span style='color:#2dc653'>"; X = "</span>"
OBEN = [(0, f"AKKU ÜBERM KOPF · {R}0 % = SCHLAF{X}"), (t2, f"ICH {R}2 %{X} vs OMA {G_}100 %{X}"), (t3, "🔌 OMA LÄDT NACHTS"), (t4, f"EMIL: {R}1 %{X}"), (t5, f"{R}0 %{X} 💤"),
        (t6, "⚡ POWERBANK = NUR GEGEN 1"), (t7, "REDE: 4 STUNDEN"), (t8, f"OMA: {G_}98 %{X} 🧶"), (t9, "1 VIDEO = 1 %"), (t10, f"{R}1 %{X} …"), (t11, "🔌 OMA?!"),
        (t14, f"ICH {G_}100 %{X} · OMA {R}3 %{X}"), (t15, "OMA = AKKU DER STADT"), (t16, f"OMA: {R}3 %{X} …"), (t17, "WAS SOLL ICH TUN?"), (t18, f"ICH {G_}100 %{X} · OMA {R}3 %{X}")]
HOT = {"AKKU", "OMA", "EMIL", "PROZENT", "NULL", "EINGESCHLAFEN", "POWERBANK", "EINS", "STUNDEN", "LADEKABEL", "SONNTAG", "DEAL", "HUNDERT", "DREI", "STADT", "TEIL"}
try:
    from clampcam import clamp_cam; clamp_cam(J)
except Exception as e:
    print("clampcam übersprungen:", e)
finish(S, sets, OBEN, FX, HOT, tag, banner=("TEIL 2?", "➕ FOLGEN"), oben_top=150, cap_top=1620, banner_top=360)
_h = open("compositions/welt.html", encoding="utf-8").read()
_h = _h.replace("padding:14px 40px;font:900 96px/1 Inter", "padding:14px 30px;white-space:nowrap;font:900 84px/1 Inter")
open("compositions/welt.html", "w", encoding="utf-8").write(_h)
