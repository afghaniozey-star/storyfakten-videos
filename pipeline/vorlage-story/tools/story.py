"""STORY-FORMAT (Comic-Geschichte mit Cliffhanger, Serie „In dieser Welt …“) – Teil 1: Die Zahl über dem Kopf.
Aufruf: python3 tools/story.py  (liest voice.json + assets/vo/timing.json, ruft tools/story_musik.py auf)"""
import json, re, subprocess, sys
T = json.load(open("assets/vo/timing.json")); V = json.load(open("voice.json"))
F = lambda v: f"{v:.2f}".rstrip('0').rstrip('.')
norm = lambda s: re.sub(r"[^a-zäöüß0-9]", "", s.lower())
def w(s, word, n=1):
    c = 0
    for x in T[s]["words"]:
        if norm(x["w"]) == norm(word):
            c += 1
            if c == n: return round(T[s]["start"] + x["s"], 2)
    raise KeyError((s, word, [x["w"] for x in T[s]["words"]]))
st = lambda k: T[k]["start"]
en = lambda k: round(T[k]["start"] + T[k]["slot"], 2)
END = round(max(en(k) for k in T), 2)
J = []

# ---------- Figuren ----------
FACES = {
 "happy":  '<circle cx="-30" cy="-5" r="9" fill="#111"/><circle cx="30" cy="-5" r="9" fill="#111"/><path d="M-32 28 Q0 55 32 28" stroke="#111" stroke-width="7" fill="none" stroke-linecap="round"/>',
 "neutral":'<circle cx="-30" cy="-5" r="9" fill="#111"/><circle cx="30" cy="-5" r="9" fill="#111"/><path d="M-22 35 H22" stroke="#111" stroke-width="7" stroke-linecap="round"/>',
 "shock":  '<circle cx="-30" cy="-8" r="20" fill="#fff" stroke="#111" stroke-width="4"/><circle cx="30" cy="-8" r="20" fill="#fff" stroke="#111" stroke-width="4"/><circle cx="-30" cy="-6" r="8" fill="#111"/><circle cx="30" cy="-6" r="8" fill="#111"/><ellipse cx="0" cy="40" rx="14" ry="18" fill="#5a1a1a"/>',
 "sad":    '<circle cx="-30" cy="-2" r="8" fill="#111"/><circle cx="30" cy="-2" r="8" fill="#111"/><path d="M-46 -26 L-14 -18 M46 -26 L14 -18" stroke="#111" stroke-width="6" stroke-linecap="round"/><path d="M-26 44 Q0 26 26 44" stroke="#111" stroke-width="7" fill="none" stroke-linecap="round"/><path d="M-34 12 q-6 14 0 20 q6 -6 0 -20" fill="#4cc9f0"/>',
 "laugh":  '<path d="M-42 -4 Q-30 -18 -18 -4 M18 -4 Q30 -18 42 -4" stroke="#111" stroke-width="7" fill="none" stroke-linecap="round"/><path d="M-30 22 Q0 70 30 22 Z" fill="#5a1a1a" stroke="#111" stroke-width="5"/>',
 "relief": '<path d="M-42 -2 Q-30 8 -18 -2 M18 -2 Q30 8 42 -2" stroke="#111" stroke-width="7" fill="none" stroke-linecap="round"/><path d="M-20 32 Q0 46 20 32" stroke="#111" stroke-width="7" fill="none" stroke-linecap="round"/>',
 "determined": '<circle cx="-30" cy="0" r="9" fill="#111"/><circle cx="30" cy="0" r="9" fill="#111"/><path d="M-48 -30 L-14 -18 M48 -30 L14 -18" stroke="#111" stroke-width="8" stroke-linecap="round"/><path d="M-20 36 H20" stroke="#111" stroke-width="8" stroke-linecap="round"/>',
}
HAIR = {
 "mia":  lambda c: f'<path d="M-95 -10 Q-100 -120 0 -118 Q100 -120 95 -10 Q90 -70 40 -80 Q0 -60 -60 -78 Q-90 -60 -95 -10 Z" fill="{c}"/><path d="M-92 -20 Q-120 80 -80 120 L-60 40 Z M92 -20 Q120 80 80 120 L60 40 Z" fill="{c}"/>',
 "lena": lambda c: f'<path d="M-95 -5 Q-95 -125 0 -120 Q95 -125 95 -5 Q70 -90 0 -85 Q-70 -90 -95 -5 Z" fill="{c}"/><circle cx="0" cy="-125" r="38" fill="{c}"/>',
 "oma":  lambda c: f'<path d="M-92 -10 Q-95 -115 0 -112 Q95 -115 92 -10 Q80 -80 0 -78 Q-80 -80 -92 -10 Z" fill="{c}"/><circle cx="0" cy="-120" r="34" fill="{c}"/>',
 "mann": lambda c: f'<path d="M-90 -30 Q-80 -118 0 -112 Q80 -118 90 -30 Q60 -82 0 -78 Q-60 -82 -90 -30 Z" fill="{c}"/>',
}
def person(uid, hair, hcol, shirt, skin="#f2c9a5", exprs=("happy",), start="happy", extra=""):
    faces = "".join(f'<g id="{uid}-{e}" opacity="{1 if e == start else 0}">{FACES[e]}</g>' for e in exprs)
    return (f'<g id="{uid}">'
            f'<rect x="-70" y="-60" width="55" height="62" rx="20" fill="#2b2d42"/><rect x="15" y="-60" width="55" height="62" rx="20" fill="#2b2d42"/>'
            f'<path d="M-95 -60 Q-100 -300 0 -305 Q100 -300 95 -60 Z" fill="{shirt}" stroke="#111" stroke-width="5"/>'
            f'<path d="M-90 -250 Q-150 -170 -120 -100" stroke="{shirt}" stroke-width="40" fill="none" stroke-linecap="round"/>'
            f'<path d="M90 -250 Q150 -170 120 -100" stroke="{shirt}" stroke-width="40" fill="none" stroke-linecap="round"/>'
            f'{extra}'
            f'<g transform="translate(0 -400)"><circle r="92" fill="{skin}" stroke="#111" stroke-width="5"/>{HAIR[hair](hcol)}'
            f'<circle cx="-55" cy="25" r="14" fill="#ff8fa3" opacity=".5"/><circle cx="55" cy="25" r="14" fill="#ff8fa3" opacity=".5"/>{faces}</g></g>')
def badge(uid, text, col="#ffffff", fg="#111", y=-560, size=64, chars=None):
    wd = 60 + size * .62 * (chars or len(text))
    return (f'<g id="{uid}" opacity="0"><g id="{uid}-in"><rect x="{-wd/2:.0f}" y="{y - size:.0f}" width="{wd:.0f}" height="{size * 1.35:.0f}" rx="{size*.4:.0f}" fill="{col}" stroke="#111" stroke-width="6"/>'
            f'<text id="{uid}-t" x="0" y="{y + size * .12:.0f}" text-anchor="middle" style="font:900 {size}px Inter,sans-serif;fill:{fg}">{text}</text></g></g>')
def expr(uid, frm, to, t):
    J.append(f'tl.set("#{uid}-{frm}", {{ opacity: 0 }}, {F(t)}); tl.set("#{uid}-{to}", {{ opacity: 1 }}, {F(t)});')
def pop(sel, t, d=.3):
    J.append(f'tl.fromTo("{sel}", {{ opacity: 0, scale: .3, transformOrigin: "50% 100%" }}, {{ opacity: 1, scale: 1, duration: {d}, ease: "back.out(2.4)" }}, {F(t)});')
def show(sel, t0, t1):
    J.append(f'tl.set("{sel}", {{ opacity: 1 }}, {F(t0)}); tl.set("{sel}", {{ opacity: 0 }}, {F(t1)});')
def cam(t, x, y, z, d=1.0, ease="power2.inOut"):
    # Bildpunkt (x,y) in die Bildmitte (540, 820) holen, Zoom z
    ox = min(0, max(1080 - 1080 * z, 540 - z * x)); oy = min(0, max(1920 - 1920 * z, 820 - z * y))
    J.append(f'tl.to("#cam", {{ x: {ox:.0f}, y: {oy:.0f}, scale: {z}, duration: {d}, ease: "{ease}" }}, {F(t)});')

def street_bg():
    houses = ""
    cols = [("#f4a261", "#9c4f1f"), ("#e9c46a", "#8a6d1f"), ("#a8dadc", "#457b9d"), ("#f6bd60", "#b5651d"), ("#cdb4db", "#6d597a")]
    for k, (wcol, rcol) in enumerate(cols):
        x = -40 + k * 240
        houses += (f'<rect x="{x}" y="640" width="220" height="420" fill="{wcol}" stroke="#111" stroke-width="5"/>'
                   f'<path d="M{x - 15} 650 L{x + 110} 520 L{x + 235} 650 Z" fill="{rcol}" stroke="#111" stroke-width="5"/>'
                   f'<rect x="{x + 30}" y="720" width="60" height="70" fill="#fff8d6" stroke="#111" stroke-width="4"/><rect x="{x + 130}" y="720" width="60" height="70" fill="#fff8d6" stroke="#111" stroke-width="4"/>'
                   f'<rect x="{x + 80}" y="900" width="60" height="160" fill="#6b4226" stroke="#111" stroke-width="4"/>')
    sun = '<g id="sun"><circle cx="880" cy="300" r="90" fill="#ffd166" stroke="#111" stroke-width="5"/><circle cx="855" cy="285" r="9" fill="#111"/><circle cx="905" cy="285" r="9" fill="#111"/><path d="M850 320 Q880 345 910 320" stroke="#111" stroke-width="6" fill="none" stroke-linecap="round"/></g>'
    return (f'<rect width="1080" height="1920" fill="#8ecae6"/>{sun}<circle cx="200" cy="260" r="50" fill="#fff" opacity=".9"/><circle cx="260" cy="250" r="60" fill="#fff" opacity=".9"/><circle cx="320" cy="265" r="45" fill="#fff" opacity=".9"/>'
            f'{houses}<rect y="1060" width="1080" height="200" fill="#c9c9c9"/><rect y="1060" width="1080" height="14" fill="#9a9a9a"/><rect y="1260" width="1080" height="660" fill="#6c757d"/>'
            + "".join(f'<rect x="{k * 220 + 40}" y="1500" width="120" height="16" fill="#fff"/>' for k in range(5)))
def room_bg(night=False):
    wall, floor = ("#1d2b53", "#0f1a33") if night else ("#ffe8d6", "#c8a27c")
    win = ('<rect x="680" y="380" width="280" height="300" fill="#0b132b" stroke="#111" stroke-width="8"/><circle cx="860" cy="470" r="50" fill="#f1faee"/><circle cx="880" cy="455" r="45" fill="#0b132b"/>'
           + "".join(f'<circle cx="{700 + k * 37 % 250}" cy="{400 + k * 53 % 260}" r="3" fill="#fff"/>' for k in range(9))) if night else \
          '<rect x="680" y="380" width="280" height="300" fill="#8ecae6" stroke="#111" stroke-width="8"/><path d="M820 380 V680 M680 530 H960" stroke="#111" stroke-width="8"/>'
    return f'<rect width="1080" height="1920" fill="{wall}"/>{win}<rect y="1180" width="1080" height="740" fill="{floor}"/>'

S = {}
# --- Set A: Straße (s1–s3a)
baker = person("bak", "mann", "#3d2b1f", "#ffffff", exprs=("happy",), extra='<rect x="-60" y="-230" width="120" height="170" rx="10" fill="#f1f1f1" stroke="#111" stroke-width="4"/>')
oma = person("oma", "oma", "#d9d9d9", "#9d4edd", exprs=("happy",))
stroller = ('<g id="baby"><circle cx="-60" cy="-20" r="22" fill="#333"/><circle cx="60" cy="-20" r="22" fill="#333"/><path d="M-90 -40 H90 Q100 -150 0 -160 Q-100 -150 -90 -40 Z" fill="#4cc9f0" stroke="#111" stroke-width="5"/>'
            '<circle cx="0" cy="-130" r="40" fill="#f2c9a5" stroke="#111" stroke-width="4"/><circle cx="-12" cy="-132" r="5" fill="#111"/><circle cx="12" cy="-132" r="5" fill="#111"/><path d="M-10 -115 Q0 -108 10 -115" stroke="#111" stroke-width="4" fill="none"/></g>')
S["A"] = (street_bg() + f'<g transform="translate(200 1330) scale(.85)">{baker}{badge("bB", "12.400", size=70)}</g>'
          f'<g transform="translate(540 1330) scale(.85)">{oma}{badge("bO", "900", size=70)}</g>'
          f'<g transform="translate(880 1330) scale(1.2)">{stroller}{badge("bY", "31.000", y=-200, size=48)}</g>'
          '<g id="qs" opacity="0">' + "".join(f'<g transform="translate({x} 1330) scale(.85)"><g transform="translate(0 -560)"><rect x="-75" y="-64" width="150" height="86" rx="26" fill="#fff" stroke="#111" stroke-width="6"/><text x="0" y="8" text-anchor="middle" style="font:900 64px Inter,sans-serif;fill:#111">?</text></g></g>' for x in (200, 540)) + '</g>')
# --- Set B: Mia + Lena (s3b–s5)
mia = lambda uid, st="happy": person(uid, "mia", "#6b3e26", "#ef476f", exprs=("happy", "shock", "determined", "relief", "sad"), start=st)
lena = lambda uid, st="happy": person(uid, "lena", "#f4d35e", "#06d6a0", exprs=("happy", "laugh", "relief", "neutral"), start=st)
S["B"] = (street_bg() + f'<g transform="translate(300 1400) scale(1.05)">{mia("m1")}{badge("bM1", "24.817", size=60)}</g>'
          f'<g transform="translate(780 1400) scale(1.05)">{lena("l1")}{badge("bL1", "1", col="#e63946", fg="#fff", size=90)}</g>')
# --- Set C: Montage (s6)
def card(uid, emo, x):
    return (f'<g id="{uid}" opacity="0" transform="translate({x} 760)"><g id="{uid}-in"><rect x="-150" y="-150" width="300" height="300" rx="40" fill="#fff" stroke="#111" stroke-width="8"/>'
            f'<text x="0" y="60" text-anchor="middle" style="font:170px Noto Color Emoji">{emo}</text>'
            f'<path d="M-120 -120 L120 120 M120 -120 L-120 120" stroke="#e63946" stroke-width="26" stroke-linecap="round"/></g></g>')
S["C"] = (room_bg() + '<g id="cards">' + card("c1", "🚲", 220) + card("c2", "🚗", 540) + card("c3", "🏊", 860) + '</g>'
          f'<g id="sofa" opacity="0"><rect x="120" y="1100" width="840" height="220" rx="60" fill="#8338ec" stroke="#111" stroke-width="6"/><rect x="80" y="1020" width="120" height="300" rx="50" fill="#7027d1" stroke="#111" stroke-width="6"/><rect x="880" y="1020" width="120" height="300" rx="50" fill="#7027d1" stroke="#111" stroke-width="6"/>'
          f'<g transform="translate(380 1250) scale(.95)">{mia("m2", "determined")}</g><g transform="translate(700 1250) scale(.95)">{lena("l2", "neutral")}{badge("bL2", "1", col="#e63946", fg="#fff", size=90)}</g></g>'
          '<g id="pz" opacity="0" transform="translate(460 430)"><g id="pz-in"><rect x="-210" y="-150" width="420" height="300" rx="30" fill="#fff" stroke="#111" stroke-width="8"/><text x="0" y="70" text-anchor="middle" style="font:220px Noto Color Emoji">🍕</text></g></g>'
          f'<g id="bub" opacity="0"><path d="M300 330 H1020 Q1050 330 1050 360 V560 Q1050 590 1020 590 H760 L700 680 L700 590 H330 Q300 590 300 560 V360 Q300 330 330 330 Z" fill="#fff" stroke="#111" stroke-width="7"/>'
          f'<text x="675" y="440" text-anchor="middle" style="font:900 54px Inter,sans-serif;fill:#111">„Was ist denn heute</text><text x="675" y="515" text-anchor="middle" style="font:900 54px Inter,sans-serif;fill:#111">mit dir los?“ 😂</text></g>')
# --- Set D: Schlafzimmer nachts (s8–s9)
S["D"] = (room_bg(True) + '<rect x="80" y="1080" width="920" height="200" rx="30" fill="#e0e1dd" stroke="#111" stroke-width="6"/><rect x="60" y="960" width="80" height="340" rx="20" fill="#6b4226" stroke="#111" stroke-width="6"/>'
          f'<g transform="translate(360 1260) scale(.95)">{mia("m3", "sad")}{badge("bM3", "24.816", size=60)}</g>'
          f'<g transform="translate(720 1260) scale(.95)">{lena("l3", "neutral")}{badge("bL3", "1", col="#e63946", fg="#fff", size=80, chars=6)}</g>'
          '<g id="clk"><rect x="240" y="170" width="600" height="230" rx="30" fill="#000" stroke="#444" stroke-width="8"/>'
          '<text id="clkt" x="540" y="330" text-anchor="middle" style="font:900 150px Inter,monospace;fill:#ff3b30;letter-spacing:6px">23:59</text></g>'
          '<text id="cd" x="540" y="520" text-anchor="middle" opacity="0" style="font:900 110px Inter,sans-serif;fill:#fff">60</text>'
          '<rect id="nightdim" width="1080" height="1920" fill="#000" opacity=".25"/>')
# --- Set E: Spiegel (s10–s11)
S["E"] = (room_bg(True) + '<rect x="250" y="250" width="580" height="1000" rx="290" fill="#a8b8c8" stroke="#6b4226" stroke-width="30"/>'
          '<clipPath id="mir"><rect x="265" y="265" width="550" height="970" rx="275"/></clipPath>'
          f'<g clip-path="url(#mir)"><rect x="250" y="250" width="580" height="1000" fill="#2a3a55"/><g transform="translate(540 1330) scale(1.05)">{mia("m4", "relief")}{badge("bM4", "1", col="#e63946", fg="#fff", size=100)}</g></g>'
          '<path d="M330 380 L420 300 M340 470 L470 340" stroke="#fff" stroke-width="12" opacity=".35" stroke-linecap="round"/>'
          '<radialGradient id="vig" cx=".5" cy=".45" r=".7"><stop offset=".55" stop-color="#e63946" stop-opacity="0"/><stop offset="1" stop-color="#7a0010" stop-opacity=".85"/></radialGradient>'
          '<rect id="redvig" width="1080" height="1920" fill="url(#vig)" opacity="0"/>')

# ---------- Zeitplan ----------
tA0, tB0 = 0, w("s3", "Bis")
tC0, tD0, tE0 = st("s6"), st("s8"), w("s10", "Dann")
tEND = st("s12")
sets = [("A", tA0, tB0), ("B", tB0, tC0), ("C", tC0, tD0), ("D", tD0, tE0), ("E", tE0, tEND)]
# Set A: Hook – Fragezeichen über Köpfen, dann echte Zahlen
J.append('tl.set("#cam", { x: 0, y: 0, scale: 1, svgOrigin: "0 0" }, 0);')
pop("#qs", .3)
J.append(f'tl.to("#qs", {{ opacity: 0, duration: .2 }}, {F(st("s2") - .1)});')
pop("#bB", w("s2", "Bäcker:") + .2); pop("#bO", w("s2", "Oma") + .2); pop("#bY", w("s2", "Baby:") + .2)
cam(st("s2") - .1, 200, 1000, 1.3, .9); cam(w("s2", "Oma") - .2, 540, 1000, 1.3, .7); cam(w("s2", "Baby:") - .2, 880, 1050, 1.3, .7); cam(st("s3"), 540, 820, 1, .9)
# Set B: Lena – die Eins
J.append(f'tl.set("#cam", {{ x: 0, y: 0, scale: 1 }}, {F(tB0)});')
pop("#bM1", tB0 + .2)
t1 = w("s4", "Eins.") - .3
pop("#bL1", t1, .4)
J.append(f'tl.to("#bL1-in", {{ scale: 1.15, duration: .25, yoyo: true, repeat: 9, ease: "sine.inOut", transformOrigin: "50% 50%" }}, {F(t1 + .4)});')
cam(st("s4") - .2, 780, 900, 1.5, 1.4)
expr("m1", "happy", "shock", t1 + .1)
cam(st("s5"), 300, 950, 1.45, .8); expr("m1", "shock", "determined", w("s5", "Sie"))
# Set C: Montage + Sofa + Lachen
J.append(f'tl.set("#cam", {{ x: 0, y: 0, scale: 1 }}, {F(tC0)});')
for uid, word in (("c1", "Fahrrad."), ("c2", "Straße."), ("c3", "Schwimmbad.")):
    J.append(f'tl.fromTo("#{uid}", {{ opacity: 0 }}, {{ opacity: 1, duration: .05 }}, {F(w("s6", word) - .1)});')
    J.append(f'tl.fromTo("#{uid}-in", {{ scale: 2, rotation: -15, transformOrigin: "50% 50%" }}, {{ scale: 1, rotation: 0, duration: .3, ease: "back.out(2)" }}, {F(w("s6", word) - .1)});')
tw = w("s6", "weicht") - .4
J.append(f'tl.to("#cards", {{ opacity: 0, duration: .3 }}, {F(tw)});')
J.append(f'tl.fromTo("#sofa", {{ opacity: 0 }}, {{ opacity: 1, duration: .4 }}, {F(tw)});')
J.append(f'tl.fromTo("#pz", {{ opacity: 0 }}, {{ opacity: 1, duration: .05 }}, {F(w("s6b", "Pizza,") - .2)}); tl.fromTo("#pz-in", {{ scale: 2, rotation: 20, transformOrigin: "50% 50%" }}, {{ scale: 1, rotation: 0, duration: .35, ease: "back.out(2)" }}, {F(w("s6b", "Pizza,") - .2)}); tl.to("#pz", {{ opacity: 0, duration: .25 }}, {F(st("s7") - .1)});')
expr("l2", "neutral", "laugh", st("s7")); pop("#bub", w("s7", "Was") - .1)
J.append(f'tl.to("#bub", {{ opacity: 0, duration: .2 }}, {F(st("s7b"))});')
pop("#bL2", w("s7b", "Eins") - .2, .35); expr("m2", "determined", "shock", w("s7b", "starrt"))
J.append(f'tl.to("#bL2-in", {{ scale: 1.15, duration: .25, yoyo: true, repeat: 5, ease: "sine.inOut", transformOrigin: "50% 50%" }}, {F(w("s7b", "Eins") + .2)});')
cam(st("s7"), 620, 900, 1.2, .8); cam(st("s7b") + .3, 700, 760, 1.45, 1.2)
# Set D: Nacht, Uhr, Mitternacht
J.append(f'tl.set("#cam", {{ x: 0, y: 0, scale: 1 }}, {F(tD0)});')
pop("#bM3", tD0 + .3); pop("#bL3", tD0 + .5)
J.append(f'tl.to("#clkt", {{ opacity: .35, duration: .5, yoyo: true, repeat: 7, ease: "steps(1)" }}, {F(w("s8", "Dreiundzwanzig"))});')
cam(w("s8", "Dreiundzwanzig") - .2, 540, 600, 1.25, 1.6)
t60 = st("s8b")
J.append(f'tl.set("#cd", {{ opacity: 1 }}, {F(t60)});')
J.append(f'(() => {{ const o = {{ v: 60 }}; tl.fromTo(o, {{ v: 60 }}, {{ v: 0, duration: {F(w("s9", "Mitternacht.") - t60)}, ease: "none", immediateRender: false, onUpdate: () => {{ document.getElementById("cd").textContent = Math.ceil(o.v); }} }}, {F(t60)}); }})();')
J.append(f'tl.set("#cd", {{ opacity: 0 }}, {F(w("s9", "Mitternacht."))});')
cam(t60 + .2, 540, 900, 1.15, 1.0)
tm = w("s9", "Mitternacht.")
J.append(f'tl.call(() => {{ document.getElementById("clkt").textContent = "00:00"; }}, null, {F(tm)}); tl.call(() => {{ document.getElementById("clkt").textContent = "23:59"; }}, null, {F(tm - .05)});')
J.append(f'tl.set("#clkt", {{ opacity: 1 }}, {F(tm)}); tl.fromTo("#nightdim", {{ opacity: .9 }}, {{ opacity: .25, duration: .6, immediateRender: false }}, {F(tm)});')
cam(tm + .3, 720, 950, 1.3, .8)
tz = w("s9", "springt")
J.append(f'(() => {{ const o = {{ v: 1 }}; tl.fromTo(o, {{ v: 1 }}, {{ v: 22000, duration: 1.2, ease: "power2.in", onUpdate: () => {{ document.getElementById("bL3-t").textContent = Math.round(o.v).toLocaleString("de-DE"); }} }}, {F(tz)}); }})();')
J.append(f'tl.to("#bL3-in rect", {{ attr: {{ fill: "#2dc653" }}, duration: .3 }}, {F(tz + 1.0)});')
expr("l3", "neutral", "relief", tz + 1.1)
expr("m3", "sad", "relief", st("s10"))
# Set E: Spiegel – Cliffhanger
J.append(f'tl.set("#cam", {{ x: 0, y: 0, scale: 1 }}, {F(tE0)});')
cam(tE0, 540, 800, 1.05, .1)
ts = w("s11", "Eins.") - .5
J.append(f'tl.fromTo("#bM4", {{ opacity: 0 }}, {{ opacity: 1, duration: .05 }}, {F(ts)});')
J.append(f'tl.fromTo("#bM4-in", {{ scale: 3, transformOrigin: "50% 50%" }}, {{ scale: 1, duration: .25, ease: "power4.in" }}, {F(ts)});')
expr("m4", "relief", "shock", ts + .1)
J.append(f'tl.to("#redvig", {{ opacity: 1, duration: .4 }}, {F(ts)});')
J.append(f'tl.to("#cam", {{ x: "+=16", duration: .04, yoyo: true, repeat: 9, ease: "none" }}, {F(ts + .25)});')
cam(ts + .4, 540, 760, 1.5, 2.5, "power1.in")

sets_svg = "".join(f'<g id="set{k}" opacity="0">{S[k]}</g>' for k, _, _ in sets)
for k, a, b in sets: show(f"#set{k}", a, b)
end_card = (f'<div id="endc" class="ui clip" data-start="{F(tEND)}" data-duration="{F(END - tEND)}" style="left:0;top:0;width:1080px;height:1920px;background:#000;text-align:center">'
            f'<div id="e1" style="margin-top:640px;font:900 190px/1 Inter,sans-serif;color:#e63946">TEIL 2?</div>'
            f'<div id="e2" style="display:inline-block;margin-top:60px;background:#fff;border-radius:24px;padding:18px 40px;font:900 60px Inter,sans-serif;color:#111">➕ FOLGEN</div>'
            f'<div style="margin-top:50px;font:800 44px Inter,sans-serif;color:#bbb">Was steht in Teil 2? 👇</div></div>')
J += [f'tl.fromTo("#e1", {{ scale: 2.2, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: .35, ease: "back.out(2)" }}, {F(tEND + .05)});',
      f'tl.to("#e2", {{ scale: 1.08, duration: .35, yoyo: true, repeat: 5, ease: "sine.inOut" }}, {F(tEND + .6)});']
hook = (f'<div id="hk" class="ui clip" data-start="0" data-duration="{F(st("s2"))}" style="left:0;right:0;top:110px;text-align:center">'
        f'<div id="hk-in" style="display:inline-block;background:#111;color:#fff;border:5px solid #fff;border-radius:22px;padding:14px 30px;font:900 52px/1.15 Inter,sans-serif">IN DIESER WELT SIEHT JEDER,<br><span style="color:#ffd166">WIE VIELE TAGE DU NOCH LEBST</span></div></div>')
J.append('tl.fromTo("#hk-in", { scale: 1.3, opacity: 0 }, { scale: 1, opacity: 1, duration: .25, ease: "back.out(2)" }, 0);')
tag = f'<div id="tg" class="ui clip" data-start="0" data-duration="{F(tEND)}" style="left:30px;top:40px;font:900 38px Inter,sans-serif;color:#fff;background:rgba(0,0,0,.55);padding:6px 16px;border-radius:12px">IN DIESER WELT … #1</div>'

open("compositions/welt.html", "w", encoding="utf-8").write(f'''<template>
  <style>#root {{ position: absolute; inset: 0; overflow: hidden; background: #000; }} .ui {{ position: absolute; font-family: Inter, sans-serif; }}</style>
  <div id="root" data-composition-id="welt" data-width="1080" data-height="1920">
    <svg class="clip" data-start="0" data-duration="{F(END)}" viewBox="0 0 1080 1920" style="position:absolute;left:0;top:0;width:1080px;height:1920px" data-layout-ignore><g id="cam">{sets_svg}</g></svg>
    {hook}{tag}{end_card}
  </div>
  <script>(function () {{ const tl = gsap.timeline({{ paused: true }});
{chr(10).join("    " + j for j in J)}
    window.__timelines["welt"] = tl; }})();</script>
</template>
''')

# ---------- Untertitel (Wortgruppen, Mitte unten) ----------
HOT = {"EINS.", "EINE", "TAGE", "LENA", "MIA", "MITTERNACHT.", "SPIEGEL.", "22.000.", "EINS", "TEIL"}
caps = []
for sc in V["scenes"]:
    sid = sc["id"]; words = T[sid]["words"]; k = 0
    for disp, sp in sc["groups"]:
        dw, swn = disp.split(), sp.split()
        for j, d in enumerate(dw):
            if not any(ch.isalnum() for ch in d): continue
            caps.append((round(T[sid]["start"] + words[min(len(words) - 1, k + int(j * len(swn) / len(dw)))]["s"], 2), d))
        k += len(swn)
items, cj = [], []
for j, (t0, d) in enumerate(caps):
    if t0 >= tEND - .05: continue
    te = min(caps[j + 1][0] if j + 1 < len(caps) else END, t0 + 1.3, tEND)
    up = d.upper()
    col = "#ffd166" if up in HOT or up.rstrip("!?.,:") in {x.rstrip("!?.,:") for x in HOT} else "#fff"
    fs = min(96, int(1500 / max(1, len(up))))
    items.append(f'<div id="w{j}" class="wd clip" data-start="{F(t0)}" data-duration="{F(max(.15, te - t0 - .02))}"><span id="w{j}-in" style="color:{col};font-size:{fs}px">{up}</span></div>')
    cj.append(f'tl.fromTo("#w{j}-in", {{ scale: 1.2, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: .08 }}, {F(t0)});')
open("compositions/caps.html", "w", encoding="utf-8").write(f'''<template>
  <style>#root {{ position: absolute; inset: 0; }} .wd {{ position: absolute; left: 0; right: 0; top: 1640px; text-align: center; }}
    .wd span {{ display: inline-block; font: 900 96px/1 Inter, sans-serif; white-space: nowrap; -webkit-text-stroke: 14px #000; paint-order: stroke fill; }}</style>
  <div id="root" data-composition-id="caps" data-width="1080" data-height="1920">{"".join(items)}</div>
  <script>(function () {{ const tl = gsap.timeline({{ paused: true }}); {" ".join(cj)} window.__timelines["caps"] = tl; }})();</script>
</template>
''')

# ---------- Ton ----------
subprocess.run([sys.executable, "tools/story_musik.py", F(END), F(t1), F(tm), F(ts)], check=True)
FX = [("pop", w("s2", "Bäcker:") + .2, .45, .15), ("pop", w("s2", "Oma") + .2, .45, .15), ("pop", w("s2", "Baby:") + .2, .45, .15),
      ("hit", t1, .7, 1.5), ("whoosh", tC0, .35, .8)]
FX += [("pop", w("s6", x) - .1, .55, .15) for x in ("Fahrrad.", "Straße.", "Schwimmbad.")]
FX += [("pop", w("s6b", "Pizza,") - .2, .5, .15), ("pop", w("s7b", "Eins") - .2, .5, .15), ("pop", w("s7", "Was") - .1, .4, .15), ("tick", w("s8", "Dreiundzwanzig"), .5, 2.0), ("chime", tz + 1.0, .5, 1.4), ("hit", ts, .9, 1.6), ("whoosh", tEND, .4, .8)]
Hh = lambda id_, ti: f'      <div id="{id_}" data-composition-id="{id_}" data-composition-src="compositions/{id_}.html" data-start="0" data-duration="{F(END)}" data-track-index="{ti}" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index:{ti}"></div>'
lines = [Hh("welt", 2), Hh("caps", 3), f'      <audio id="musik" class="clip" data-start="0" data-duration="{F(END)}" data-track-index="5" data-volume="0.22" src="assets/musik.wav"></audio>']
for k in T:
    d = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"assets/vo/{k}.mp3"]))
    lines.append(f'      <audio id="vo-{k}" class="clip" data-start="{T[k]["start"] + T[k]["lead"]:.2f}" data-duration="{d:.2f}" data-track-index="4" data-volume="1" src="assets/vo/{k}.mp3"></audio>')
for j, (n, at, vol, dur) in enumerate(FX):
    lines.append(f'      <audio id="fx-{j}" class="clip" data-start="{F(max(0, at))}" data-duration="{F(min(dur, END - max(0, at)))}" data-volume="{vol}" data-track-index="{20 + j}" src="assets/sfx2/{n}.mp3"></audio>')
open("index.html", "w", encoding="utf-8").write(f'''<!doctype html>
<html lang="de" data-resolution="portrait"><head><meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" /><script src="assets/gsap.min.js"></script>
<style>* {{ margin: 0; padding: 0; box-sizing: border-box; }} html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #000; }} #root {{ width: 100%; height: 100%; }}</style></head>
<body><div id="root" data-composition-id="main" data-start="0" data-duration="{F(END)}" data-width="1080" data-height="1920">
{chr(10).join(lines)}
</div><script>window.__timelines = window.__timelines || {{}}; window.__timelines["main"] = gsap.timeline({{ paused: true }});</script></body></html>
''')
print("Ende", END, "Eins", t1, "Mitternacht", tm, "Spiegel", ts)
