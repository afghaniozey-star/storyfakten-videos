"""ABO-WELT Tag 5 (YouTube) – EREIGNIS-Tag „WER BEKOMMT DIE TÜRKEI?“ (keine neuen Besitzer).
Bild 0: Punch-Zoom auf die blinkende Türkei, großes „?“ + FREI!-Stempel, Globi schaut von Russland herüber,
Pflichtsatz (Abo-Aufruf) gesprochen + eingeblendet am Anfang und Ende, Fortschrittsbalken oben links,
Europa 3 % / Asien 97 % mit leuchtendem Bosporus, Haselnuss-Berg + Glas, Ural-Linie in Russland („NUR GLOBI!“),
Split Russland/Türkei, großer Ladebalken 99 %, Rundflug über die 5 echten Besitzer, Japan + Italien FREI!,
Zähler 5/195 → NOCH 190 FREI, Loop-Ende = Bild 0. Keine weißen/grauen Überblendungen.
Aufruf (im Projektordner): /usr/bin/python3 tools/abowelt_tag5.py
liest welt.json, daten.json (= daten-tag5.json), voice.json (= voice-tag5.json), assets/vo/timing.json, weltkarte.json
Karte: @svg-maps/world (CC BY 4.0) → in der Beschreibung „Karte: svg-maps (CC BY 4.0)“ nennen."""
import json, re, subprocess, sys, random, math
sys.path.insert(0, "tools"); import globi_strich as globi
T = json.load(open("assets/vo/timing.json")); V = json.load(open("voice.json"))
W = json.load(open("welt.json")); K = json.load(open("weltkarte.json"))["laender"]
D = json.load(open("daten.json"))
F = lambda v: f"{v:.2f}".rstrip('0').rstrip('.')
norm = lambda s: re.sub(r"[^a-zäöüßå0-9]", "", s.lower())
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
OWN = W["besitzer"]; NOWN = len(OWN); TOTAL = W["laender_gesamt"]; FREI = TOTAL - NOWN
owned = {o["land"]: o for o in OWN}
assert not ({"tr", "it", "jp"} & set(owned)), "Türkei/Italien/Japan sind laut welt.json nicht mehr frei"
assert NOWN == 5 and FREI == 190
GLOBI_COL = "#ff8a3d"; BAIT_COL = "#ffffff"; FREE_COL = "#46578a"; TR_COL = "#e30a17"
EU_COL, AS_COL = "#3a86ff", "#ff9f1c"
S0, MY = 1080 / 1010, 560
FX, FY = 540, 860                   # Bildpunkt, auf den die Kamera zentriert (Karte füllt bis ~75 % Höhe)
J, GJ = [], []

# ---------- Geometrie ----------
def polys(cid):
    toks = re.findall(r"[mz]|-?\d*\.?\d+(?:e-?\d+)?", K[cid]["path"])
    out, cur, x, y, sx, sy, i = [], [], 0.0, 0.0, 0.0, 0.0, 0
    while i < len(toks):
        t = toks[i]
        if t == "m":
            if cur: out.append(cur)
            x += float(toks[i + 1]); y += float(toks[i + 2]); sx, sy = x, y; cur = [(x, y)]; i += 3
            while i < len(toks) and toks[i] not in "mz":
                x += float(toks[i]); y += float(toks[i + 1]); cur.append((x, y)); i += 2
        elif t == "z":
            if cur: out.append(cur); cur = []
            x, y = sx, sy; i += 1
        else: i += 1
    if cur: out.append(cur)
    return out
def inside(P, px, py):
    c = False
    for poly in P:
        n = len(poly)
        for k in range(n):
            (x1, y1), (x2, y2) = poly[k], poly[(k + 1) % n]
            if (y1 > py) != (y2 > py) and px < (x2 - x1) * (py - y1) / (y2 - y1 + 1e-12) + x1: c = not c
    return c
def zoom_for(box, zmax=8.0, fw=900, fh=900):
    return max(1.0, min(zmax, fw / max((box[2] - box[0]) * S0, 1), fh / max((box[3] - box[1]) * S0, 1)))
def wc(mx, my): return mx * S0, MY + my * S0
def campos(cx_m, cy_m, z):
    cx, cy = wc(cx_m, cy_m); return FX - z * cx, FY - z * cy
def screen(mx, my, cx_m, cy_m, z):
    x, y = campos(cx_m, cy_m, z); sx, sy = wc(mx, my); return x + z * sx, y + z * sy
ctr = lambda b: ((b[0] + b[2]) / 2, (b[1] + b[3]) / 2)
# Länge/Breite → Kartenpunkt (Mercator, an der Türkei-bbox geeicht: 26,0–44,8 °O, 35,8–42,1 °N)
_m = lambda la: math.log(math.tan(math.pi / 4 + math.radians(la) / 2))
_A = (355.7 - 333.2) / (_m(42.1) - _m(35.8)); _B = 333.2 + _A * _m(42.1)
def geo(lon, lat): return 546.9 + (lon - 26.0) * (600.7 - 546.9) / 18.8, _B - _A * _m(lat)
def dpath(P): return "".join("M" + " L".join(f"{x:.2f} {y:.2f}" for x, y in poly) + "Z" for poly in P)

SHOTS = []
def shot(t, box=None, center=None, z=None, zmax=8.0, drift=1.03):
    if center is None: center = ctr(box)
    if z is None: z = zoom_for(box, zmax)
    SHOTS.append((round(t, 2), center[0], center[1], z, drift)); return (center, z)

# ---------- Karte ----------
TRB = K["tr"]["bbox"]; TRC = ctr(TRB)
Z_TR = zoom_for(TRB, 30.0, fw=980, fh=640); Z0 = Z_TR * 1.08
TRP = polys("tr")
TR_EU = [p for p in TRP if max(x for x, _ in p) < 557]                      # Ostthrakien (westlich des Bosporus)
TR_AS = [p for p in TRP if p not in TR_EU]
ITB = K["it"]["bbox"]; ITC = ctr(ITB)
JPB = K["jp"]["bbox"]; JPC = ctr(JPB)
RU_BOX = [560, 50, 1005, 300]; Z_RU = zoom_for(RU_BOX, 3)
RU = polys("ru")
def inner_y(x, want):
    for d in range(0, 140):
        for yy in (want + d, want - d):
            if all(inside(RU, x + dx, yy + dy) for dx, dy in ((0, 0), (6, 0), (-6, 0), (0, 6), (0, -6))): return yy
    return want
RUF = (760, inner_y(760, 150))
WORLD_C = (505, 333)
URAL = [geo(66.5, 69.0), geo(65.0, 67.5), geo(63.5, 66.0), geo(59.5, 63.5), geo(59.0, 61.0), geo(59.3, 58.5), geo(59.5, 56.0),
        geo(58.8, 54.0), geo(59.0, 52.0), geo(57.0, 51.2), geo(54.5, 51.0), geo(52.0, 49.8), geo(51.4, 47.5), geo(49.0, 46.4),
        geo(47.6, 45.4), geo(45.5, 44.0), geo(42.5, 43.2), geo(40.2, 43.6)]           # Ural → Uralfluss → Kaspi → Kaukasus
BOSP = [geo(29.13, 41.25), geo(29.0, 41.0), geo(28.6, 40.85), geo(27.4, 40.6), geo(26.7, 40.35), geo(26.2, 40.0)]
HASEL = geo(38.4, 40.85)            # Schwarzmeerküste (Giresun/Ordu)
RU_SUED = geo(40.8, 44.6)           # Südrussland/Dagestan – Globi „schaut herüber“

paths = []
for cid, c in K.items():
    if cid == "tr": col = TR_COL
    elif cid in owned: col = owned[cid]["farbe"]
    elif cid in ("jp", "it"): col = BAIT_COL
    elif cid == "ru": col = GLOBI_COL
    else: col = FREE_COL
    paths.append(f'<path id="c-{cid}" d="{c["path"]}" fill="{col}" stroke="#141c33" stroke-width="0.6" vector-effect="non-scaling-stroke"/>')
tr_i = next(i for i, p in enumerate(paths) if 'id="c-tr"' in p); paths.append(paths.pop(tr_i))
paths.append(f'<path id="trwhite" d="{K["tr"]["path"]}" fill="#ffffff" opacity="0" stroke="#141c33" stroke-width="0.6" vector-effect="non-scaling-stroke"/>')
paths.append(f'<g id="trkont" opacity="0"><path d="{dpath(TR_AS)}" fill="{AS_COL}" stroke="#141c33" stroke-width="0.6" vector-effect="non-scaling-stroke"/>'
             f'<path id="treu" d="{dpath(TR_EU)}" fill="{EU_COL}" stroke="#141c33" stroke-width="0.6" vector-effect="non-scaling-stroke"/></g>')
pl = lambda P: " ".join(f"{x:.2f},{y:.2f}" for x, y in P)
paths.append(f'<g id="bosp" opacity="0"><polyline points="{pl(BOSP)}" fill="none" stroke="#111" stroke-width="14" stroke-linecap="round" stroke-linejoin="round" vector-effect="non-scaling-stroke"/>'
             f'<polyline id="bosp-in" points="{pl(BOSP)}" fill="none" stroke="#fff35c" stroke-width="8" stroke-linecap="round" stroke-linejoin="round" vector-effect="non-scaling-stroke"/></g>')
paths.append(f'<g id="ural" opacity="0"><polyline points="{pl(URAL)}" fill="none" stroke="#111" stroke-width="16" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="1 0" vector-effect="non-scaling-stroke"/>'
             f'<polyline id="ural-in" points="{pl(URAL)}" fill="none" stroke="#fff35c" stroke-width="9" stroke-linecap="round" stroke-linejoin="round" vector-effect="non-scaling-stroke"/></g>')

def flag(id_, mx, my, txt, col, z, k=1.0, op=0, fg="#111"):
    s = k / z / S0; wd = 46 + 30 * len(txt)
    return (f'<g id="{id_}" opacity="{op}" transform="translate({mx:.2f} {my:.2f}) scale({s:.4f})"><g id="{id_}-in">'
            f'<path d="M0 0 V-150" stroke="#111" stroke-width="8"/><rect x="0" y="-150" width="{wd}" height="70" rx="12" fill="{col}" stroke="#111" stroke-width="6"/>'
            f'<text x="{wd/2:.0f}" y="-101" text-anchor="middle" style="font:900 46px Inter,sans-serif;fill:{fg}">{txt}</text>'
            f'<circle r="14" fill="#fff" stroke="#111" stroke-width="6"/></g></g>')

FOC = {o["land"]: (o.get("fokus") or K[o["land"]]["bbox"]) for o in OWN}
CANADA_PT = (215, 150); US_PT = (215, 340)
PT = {cid: ctr(FOC[cid]) for cid in owned}; PT["ca"] = CANADA_PT; PT["us"] = US_PT
ZO = {cid: zoom_for(FOC[cid], 6.0, 820, 700) for cid in owned}
pins = ""
for o in OWN:
    cid = o["land"]
    pins += flag(f'p-{cid}', *PT[cid], o["name"], o["farbe"], ZO[cid])
    pins += flag(f'pw-{cid}', *PT[cid], o["name"], o["farbe"], 1.0, k=.62)
pins += flag("pw-globi", RUF[0], RUF[1], "GLOBI", GLOBI_COL, 1.0, k=.62)
pins += flag("pw-jp", JPC[0] - 4, JPC[1] + 4, "FREI!", "#ffffff", 1.0, k=.62, fg="#e63946")
pins += flag("pw-tr", TRC[0] + 6, TRC[1], "TÜRKEI?", "#ffffff", 1.0, k=.62, fg="#e63946")
# s3: Kontinent-Fahnen in der Türkei
EUP = geo(27.3, 41.3); ASP = geo(34.5, 39.2)
pins += flag("f-eu", *EUP, "EUROPA 3 %", EU_COL, Z_TR, k=.62, fg="#fff")
pins += flag("f-as", *ASP, "ASIEN 97 %", AS_COL, Z_TR, k=.75)
# s5: Europa / Asien links + rechts vom Ural
pins += flag("f-rueu", *geo(44, 57), "EUROPA", EU_COL, Z_RU, k=.75, fg="#fff")
pins += flag("f-ruas", *geo(95, 63), "ASIEN", AS_COL, Z_RU, k=.75)
MAP = (f'<g id="cam"><rect x="-6000" y="-6000" width="14000" height="14000" fill="#0e3a66"/>'
       f'<g transform="translate(0 {MY}) scale({S0:.5f})">{"".join(paths)}{pins}</g></g>')

# ---------- Schnittliste ----------
BILD0 = (TRC, Z_TR)
shot(0, center=TRC, z=Z0, drift=1.0)                                             # Bild 0 (Punch-Zoom 108 → 100 %)
t_wer1 = w("s1", "Wer"); t_cut1 = min(1.4, t_wer1 - .05)
shot(t_cut1, center=(TRC[0] + 9, TRC[1] - 4), z=Z_TR * 1.35)                    # Osten + Globi groß
t_abo2 = w("s2", "Abonnier"); t_kom2 = w("s2", "kommentier"); t_nur2 = w("s2", "nur")
shot(st("s2"), center=(TRC[0] - 12, TRC[1] - 14), z=Z_TR * .55)                 # Europa + Türkei: Abo-Knopf
shot(t_kom2 - .05, center=(TRC[0] - 4, TRC[1] - 4), z=Z_TR * .8)                # Sprechblase fliegt auf die Türkei
shot(t_nur2 - .05, center=TRC, z=Z_TR * .95)
t_eu3 = w("s3", "Europa"); t_as3 = w("s3", "Asien.")
shot(st("s3"), center=TRC, z=Z_TR)                                               # Türkei zweifarbig
shot(t_eu3 - .05, center=geo(28.0, 40.9), z=Z_TR * 2.6)                          # Bosporus
shot(t_as3 - .05, center=(TRC[0] + 2, TRC[1]), z=Z_TR * .9)
t_has4 = w("s4", "Haselnuss"); t_kom4 = w("s4", "kommt")
shot(st("s4"), center=(HASEL[0] - 4, HASEL[1] + 4), z=Z_TR * 1.25)              # Schwarzmeerküste
shot(t_has4 - .05, center=(HASEL[0], HASEL[1] + 3), z=Z_TR * 1.7)                # Haselnuss-Berg
shot(t_kom4 - .05, center=(TRC[0] + 3, TRC[1] - 2), z=Z_TR * 1.05)
t_eu5 = w("s5", "Europa"); t_glo5 = w("s5", "Globi!")
shot(st("s5"), box=RU_BOX, zmax=3)                                               # Schnitt auf Russland
shot(t_eu5 - .05, center=geo(60, 58), z=Z_RU * 1.7)                              # Ural leuchtet
shot(t_glo5 - .05, center=ctr(RU_BOX), z=Z_RU * .95)                             # NUR GLOBI!
SPLIT_C = (TRC[0] + 6, 318.0); Z_SPLIT = zoom_for([536, 286, 620, 362], 30, 1000, 1100)
t_zw6 = w("s6", "zweite")
shot(st("s6"), center=SPLIT_C, z=Z_SPLIT)                                         # Split: oben Russland/Globi, unten Türkei
shot(t_zw6 - .05, center=SPLIT_C, z=Z_SPLIT * 1.12)
t_99 = w("s7", "neunundneunzig")
shot(st("s7"), center=(TRC[0], TRC[1] - 2), z=Z_TR * .85)                       # großer Ladebalken
shot(t_99 - .05, center=(TRC[0] + 1, TRC[1]), z=Z_TR * 1.15, drift=1.08)
RUND = [("ca", "Kanada"), ("br", "Brasilien"), ("de", "Deutschland"), ("us", "USA"), ("au", "Australien")]
TR = {}
for cid, word in RUND:
    TR[cid] = w("s8", word) - .05 if cid != "ca" else st("s8")
    shot(TR[cid], center=PT[cid] if cid in ("ca", "us") else ctr(FOC[cid]), z=ZO[cid])
t_it9 = w("s9", "Italien"); t_auf9 = w("s9", "Auf"); t_glo9 = w("s9", "Globi!")
Z_JP = zoom_for(JPB, 9.0, 820, 700); Z_IT = zoom_for(ITB, 13.0, 820, 700)
shot(st("s9"), center=(JPC[0] + 4, JPC[1]), z=Z_JP)                             # Japan FREI!
shot(t_it9 - .05, center=ITC, z=Z_IT)                                            # Italien FREI!
shot(t_auf9 - .05, box=RU_BOX, zmax=3)                                           # Globi winkt
t_noch10 = w("s10", "Noch")
shot(st("s10"), center=WORLD_C, z=1.0)                                           # Welt + Zähler
shot(t_noch10 - .05, center=(540, 320), z=1.08)
t_wer11 = w("s11", "Wer"); t_abo11 = w("s11", "Abonnier"); t_nur11 = w("s11", "nur")
shot(st("s11"), center=(TRC[0] - 4, TRC[1] + 1), z=Z_TR * 1.45)
shot(t_abo11 - .05, center=(TRC[0] - 12, TRC[1] - 14), z=Z_TR * .55)
shot(t_nur11 - .05, center=(TRC[0] - 3, TRC[1] - 3), z=Z_TR * .8)
LOOP_T = round(max(t_nur11 + .9, END - 2.2), 2)
SHOTS.append((LOOP_T, TRC[0], TRC[1], Z_TR, "loop"))                             # Bild-0-Einstellung, zoomt bis END auf Z0 (= Bild 0)
SHOTS.sort(key=lambda s: s[0])
CUTS = []; CAMAT = []
for k, (t, cx, cy, z, drift) in enumerate(SHOTS):
    t1 = SHOTS[k + 1][0] if k + 1 < len(SHOTS) else END
    x, y = campos(cx, cy, z)
    J.append(f'tl.set("#cam", {{ x: {x:.1f}, y: {y:.1f}, scale: {z:.3f} }}, {F(t)});')
    if drift == "loop":
        x2, y2 = campos(cx, cy, Z0)
        J.append(f'tl.to("#cam", {{ x: {x2:.1f}, y: {y2:.1f}, scale: {Z0:.3f}, duration: {END - t:.2f}, ease: "sine.inOut" }}, {F(t)});')
    elif t == 0:
        x2, y2 = campos(cx, cy, Z_TR)
        J.append(f'tl.to("#cam", {{ x: {x2:.1f}, y: {y2:.1f}, scale: {Z_TR:.3f}, duration: .6, ease: "power2.out" }}, 0);')
    elif drift != 1.0:
        x2, y2 = campos(cx, cy, z * drift)
        J.append(f'tl.to("#cam", {{ x: {x2:.1f}, y: {y2:.1f}, scale: {z * drift:.3f}, duration: {t1 - t:.2f}, ease: "none" }}, {F(t)});')
    if t > 0: CUTS.append(t)
    CAMAT.append((t, cx, cy, z))
J.insert(0, 'tl.set("#cam", { svgOrigin: "0 0" }, 0);')
def cam_at(t):
    c = [s for s in CAMAT if s[0] <= t + 1e-6][-1]; return c[1], c[2], c[3]

# ---------- Ereignisse auf der Karte ----------
def show(id_, t0, t1, popd=.3):
    J.append(f'tl.set("#{id_}", {{ opacity: 1 }}, {F(t0)}); tl.fromTo("#{id_}-in", {{ scale: 0, transformOrigin: "0px 0px" }}, {{ scale: 1, duration: {popd}, ease: "back.out(2.5)" }}, {F(t0)});')
    J.append(f'tl.set("#{id_}", {{ opacity: 0 }}, {F(t1)});')
def blink(sel, c0, c1, t0, t1, per=.25):
    n = max(1, int((t1 - t0) / per) // 2 * 2 - 1)
    J.append(f'tl.fromTo("{sel}", {{ fill: "{c0}" }}, {{ fill: "{c1}", duration: {per}, yoyo: true, repeat: {n}, ease: "steps(1)", immediateRender: false }}, {F(t0)});')
    J.append(f'tl.set("{sel}", {{ fill: "{c0}" }}, {F(t1)});')
def wblink(t0, t1, per=.28):      # Türkei blinkt weiß (Bild 0 / Loop)
    n = max(1, int((t1 - t0) / per) // 2 * 2 - 1)
    J.append(f'tl.fromTo("#trwhite", {{ opacity: 0 }}, {{ opacity: 1, duration: {per}, yoyo: true, repeat: {n}, ease: "steps(1)", immediateRender: false }}, {F(t0)});')
    J.append(f'tl.set("#trwhite", {{ opacity: 0 }}, {F(t1)});')
wblink(.15, st("s2")); wblink(st("s6") + .1, en("s6")); wblink(st("s11") + .1, t_abo11 - .05); wblink(LOOP_T, END)
# s3: Türkei zweifarbig, Bosporus leuchtet
J.append(f'tl.set("#trkont", {{ opacity: 1 }}, {F(st("s3"))}); tl.set("#trkont", {{ opacity: 0 }}, {F(en("s3"))});')
show("f-eu", st("s3") + .2, en("s3"), .25); show("f-as", st("s3") + .35, en("s3"), .25)
J.append(f'tl.set("#bosp", {{ opacity: 1 }}, {F(t_eu3 - .05)}); tl.set("#bosp", {{ opacity: 0 }}, {F(en("s3"))});')
J.append(f'tl.fromTo("#bosp-in", {{ attr: {{ stroke: "#fff35c" }} }}, {{ attr: {{ stroke: "#ffffff" }}, duration: .18, yoyo: true, repeat: 9, ease: "steps(1)", immediateRender: false }}, {F(t_eu3)});')
J.append(f'tl.fromTo("#treu", {{ attr: {{ fill: "{EU_COL}" }} }}, {{ attr: {{ fill: "#9cc8ff" }}, duration: .2, yoyo: true, repeat: 5, ease: "steps(1)", immediateRender: false }}, {F(t_eu3)});')
# s5: Ural leuchtet, Kontinent-Fahnen
J.append(f'tl.set("#ural", {{ opacity: 1 }}, {F(t_eu5 - .05)}); tl.set("#ural", {{ opacity: 0 }}, {F(en("s5"))});')
J.append(f'tl.fromTo("#ural-in", {{ attr: {{ stroke: "#fff35c" }} }}, {{ attr: {{ stroke: "#ffffff" }}, duration: .2, yoyo: true, repeat: 11, ease: "steps(1)", immediateRender: false }}, {F(t_eu5)});')
show("f-rueu", st("s5") + .15, t_eu5 - .05, .25); show("f-ruas", st("s5") + .3, t_eu5 - .05, .25)
blink("#c-ru", GLOBI_COL, "#ffd166", t_glo5 - .05, en("s5"), .2)
# s8: Besitzer-Fahnen
for k, (cid, _) in enumerate(RUND):
    t1 = TR[RUND[k + 1][0]] if k + 1 < len(RUND) else en("s8")
    show(f"p-{cid}", TR[cid] + .03, t1, .22)
# s9: Japan + Italien blinken, Russland blinkt
blink("#c-jp", BAIT_COL, "#ffd166", st("s9"), t_it9 - .05)
blink("#c-it", BAIT_COL, "#ffd166", t_it9 - .05, t_auf9 - .05)
blink("#c-ru", GLOBI_COL, "#ffd166", t_auf9, en("s9"), .2)
# s10: Weltansicht – alle Fahnen, Japan/Italien FREI!, Türkei?, freie Länder blitzen
for cid in owned: show(f"pw-{cid}", st("s10") + .05, en("s10"), .25)
for id_ in ("pw-globi", "pw-jp", "pw-tr"): show(id_, st("s10") + .05, en("s10"), .25)
blink("#c-jp", BAIT_COL, "#ffd166", st("s10"), en("s10")); blink("#c-it", BAIT_COL, "#ffd166", st("s10"), en("s10")); wblink(st("s10") + .1, en("s10"))
random.seed(9)
free = [c for c in K if c not in owned and c not in ("ru", "jp", "it", "tr") and K[c]["bbox"][2] - K[c]["bbox"][0] > 10]
used = set(); t = t_noch10 + .05
while t < en("s10") - .2:
    cid = random.choice(free); used.add(cid)
    J.append(f'tl.fromTo("#c-{cid}", {{ fill: "{FREE_COL}" }}, {{ fill: "#ffffff", duration: .1, yoyo: true, repeat: 1, immediateRender: false }}, {F(t)});')
    t += .07
for cid in used: J.append(f'tl.set("#c-{cid}", {{ fill: "{FREE_COL}" }}, {F(en("s10"))});')

# ---------- HTML-Ebenen ----------
def ui(id_, t0, t1, inner, style): return f'<div id="{id_}" class="ui clip" data-start="{F(t0)}" data-duration="{F(max(.05, t1 - t0))}" style="{style}">{inner}</div>\n'
def chip(id_, txt, bg="#fff", fg="#111", size=44, extra=""):
    return f'<div id="{id_}" style="display:inline-block;max-width:1000px;background:{bg};color:{fg};font:900 {size}px/1.12 Inter,sans-serif;padding:12px 26px;border-radius:18px;border:5px solid #111;box-shadow:0 8px 0 #111;{extra}">{txt}</div>'
def pop(id_, t, s0=0, d=.3): J.append(f'tl.fromTo("#{id_}", {{ scale: {s0} }}, {{ scale: 1, duration: {d}, ease: "back.out(2.5)", immediateRender: false }}, {F(t)});')
html = ""
HEAD_TOP = 96
BAR_TOP = 222                  # Fortschrittsbalken oben links / Zähler oben rechts
SRC_TOP = 300
CAP_TOP = 1065                 # Untertitel 1065–1165 px (55–61 %)
LOW1, LOW2 = 1240, 1370        # Schilder darunter, enden vor ~1530 px (unten 20 % frei)
# Titelbanner durchgehend
html += ui("head", 0, END, chip("head-in", "WER BEKOMMT DIE TÜRKEI?", "#ffd166", "#111", 56, "white-space:nowrap"), f"left:30px;right:30px;top:{HEAD_TOP}px;text-align:center")
html += ui("src", st("s3"), en("s4"), f'<div style="display:inline-block;background:rgba(0,0,0,.72);border-radius:10px;padding:4px 14px;font:700 26px Inter,sans-serif;color:#fff">{D["quellenzeile"]}</div>', f"left:30px;top:{SRC_TOP}px")
# Zähler oben rechts (dauerhaft)
CNT = f'<div style="display:inline-block;background:rgba(0,0,0,.72);border-radius:14px;padding:6px 18px;font:900 42px/1.15 Inter,sans-serif;color:#fff"><span style="color:#06d6a0">{NOWN}</span>/{TOTAL}</div>'
html += ui("cnt", 0, END, CNT, f"right:30px;top:{BAR_TOP}px")
# Fortschrittsbalken oben links „Land wird vergeben … ?“ (springt in s7 auf 99 %)
html += ui("lb", 0, END,
           '<div style="position:relative;width:640px;height:62px;background:#fff;border:5px solid #111;border-radius:31px;box-shadow:0 6px 0 #111;overflow:hidden">'
           '<div id="lbf" style="position:absolute;left:0;top:0;bottom:0;width:4%;background:#06d6a0"></div>'
           '<div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font:900 32px Inter,sans-serif;color:#111">'
           'LAND WIRD VERGEBEN …&nbsp;<span id="lbq" style="color:#e63946">?</span><span id="lb99" style="color:#e63946;display:none">99 %</span></div></div>',
           f"left:30px;top:{BAR_TOP}px")
J.append(f'tl.fromTo("#lbf", {{ width: "3%" }}, {{ width: "8%", duration: .3, yoyo: true, repeat: {int(t_99 / .3) // 2 * 2 - 1}, ease: "sine.inOut" }}, 0);')
J.append(f'tl.to("#lbf", {{ width: "99%", duration: .45, ease: "power3.out" }}, {F(t_99 - .05)});')
J.append(f'tl.set("#lbq", {{ display: "none" }}, {F(t_99 - .05)}); tl.set("#lb99", {{ display: "inline" }}, {F(t_99 - .05)});')
J.append(f'tl.fromTo("#lb99", {{ opacity: 1 }}, {{ opacity: .3, duration: .3, yoyo: true, repeat: {max(1, int((LOOP_T - t_99) / .3) // 2 * 2 - 1)}, ease: "steps(1)", immediateRender: false }}, {F(t_99 + .5)});')
J.append(f'tl.set("#lbf", {{ width: "4%" }}, {F(LOOP_T)}); tl.set("#lbq", {{ display: "inline" }}, {F(LOOP_T)}); tl.set("#lb99", {{ display: "none", opacity: 1 }}, {F(LOOP_T)});')
J.append(f'tl.fromTo("#lbf", {{ width: "3%" }}, {{ width: "8%", duration: .3, yoyo: true, repeat: {max(1, int((END - LOOP_T) / .3) // 2 * 2 - 1)}, ease: "sine.inOut", immediateRender: false }}, {F(LOOP_T + .02)});')

# Bild 0 / s11 / Loop: großes „?“ auf der Türkei + FREI!-Stempel
QM = lambda id_: (f'<div id="{id_}" style="display:inline-block;font:900 280px/1 Inter,sans-serif;color:#ffd166;-webkit-text-stroke:22px #111;paint-order:stroke fill;'
                  'filter:drop-shadow(0 12px 0 rgba(0,0,0,.45))">?</div>')
for id_, t0, t1 in (("q0", 0, t_cut1), ("q11", st("s11"), t_abo11 - .05), ("qL", LOOP_T, END)):
    html += ui(id_, t0, t1, QM(id_ + "-in"), f"left:{FX - 160}px;top:{FY - 200}px;width:320px;text-align:center")
    J.append(f'tl.fromTo("#{id_}-in", {{ rotation: -8 }}, {{ rotation: 8, duration: .35, yoyo: true, repeat: {max(1, int((t1 - t0) / .35) - 1)}, ease: "sine.inOut" }}, {F(t0)});')
J.append('tl.fromTo("#q0-in", { scale: 0 }, { scale: 1, duration: .3, ease: "back.out(3)", immediateRender: false }, .03);')
J.append(f'tl.fromTo("#q11-in", {{ scale: 0 }}, {{ scale: 1, duration: .3, ease: "back.out(3)", immediateRender: false }}, {F(st("s11") + .05)});')
J.append(f'tl.fromTo("#qL-in", {{ scale: 0 }}, {{ scale: 1, duration: .3, ease: "back.out(3)", immediateRender: false }}, {F(LOOP_T + .05)});')
FREIST = lambda id_: f'<div id="{id_}" style="display:inline-block;transform:rotate(-9deg);background:#fff;color:#e63946;font:900 110px/1 Inter,sans-serif;padding:8px 30px;border:10px solid #e63946;border-radius:22px;box-shadow:0 10px 0 #111">FREI!</div>'
for id_, t0, t1 in (("fr0", 0, t_cut1), ("frL", LOOP_T, END)):
    html += ui(id_, t0, t1, FREIST(id_ + "-in"), f"left:50px;top:{FY - 400}px")
J.append('tl.fromTo("#fr0-in", { scale: 1.8 }, { scale: 1, duration: .25, ease: "back.out(2)", immediateRender: false }, .08);')
J.append(f'tl.fromTo("#frL-in", {{ scale: 1.8 }}, {{ scale: 1, duration: .25, ease: "back.out(2)", immediateRender: false }}, {F(LOOP_T + .08)});')

# Pflichtsatz (Abo-Aufruf): Anfang bis Ende s2, Schluss ab „Abonnier“ in s11
ABO = (chip("{id}-a", "🔔 ABONNIER", "#e63946", "#fff", 60) + '<div style="height:12px"></div>' +
       chip("{id}-b", "💬 + KOMMENTIER DEIN WUNSCHLAND", "#fff", "#111", 40) + '<div style="height:12px"></div>' +
       chip("{id}-c", "NUR ABONNENTEN BEKOMMEN EIN LAND!", "#ffd166", "#111", 40))
html += ui("ab1", 0, en("s2"), ABO.replace("{id}", "ab1"), f"left:0;right:0;top:{LOW1}px;text-align:center")
html += ui("ab11", t_abo11 - .05, END, ABO.replace("{id}", "ab11"), f"left:0;right:0;top:{LOW1}px;text-align:center")
J.append(f'tl.to("#ab1-a", {{ scale: 1.08, duration: .35, yoyo: true, repeat: {int(t_abo2 / .35) // 2 * 2 - 1}, ease: "sine.inOut" }}, .4);')
J.append(f'tl.fromTo("#ab1-a", {{ scale: 1 }}, {{ scale: .82, duration: .09, yoyo: true, repeat: 1, ease: "power2.in", immediateRender: false }}, {F(t_abo2 + .12)});')   # Knopf wird gedrückt
J.append(f'tl.to("#ab11-a", {{ scale: 1.08, duration: .35, yoyo: true, repeat: {int((END - t_abo11) / .35) - 1}, ease: "sine.inOut" }}, {F(t_abo11 + .3)});')
pop("ab1-b", t_kom2 - .05, 1.4, .25); pop("ab1-c", t_nur2 - .05, 1.4, .25)
pop("ab11-a", t_abo11 - .05, 1.5, .2); pop("ab11-c", t_nur11 - .05, 1.3, .2)
# Daumen drückt den Abo-Knopf (s2)
html += ui("hand", t_abo2 - .35, t_kom2 - .05, '<div id="hand-in" style="font:400 110px/1 \'Noto Color Emoji\';display:inline-block">👍</div>', f"left:700px;top:{LOW1 - 20}px")
J.append(f'tl.fromTo("#hand-in", {{ x: 260, y: 200 }}, {{ x: 0, y: 0, duration: .35, ease: "power2.out" }}, {F(t_abo2 - .35)});')
J.append(f'tl.to("#hand-in", {{ x: -30, duration: .09, yoyo: true, repeat: 1 }}, {F(t_abo2 + .12)});')
# Sprechblase „TÜRKEI!“ fliegt auf die Türkei (s2)
html += ui("bub2", t_kom2 - .05, en("s2"), chip("bub2-in", "💬 „TÜRKEI!“", "#fff", "#111", 64), f"left:0;right:0;top:{FY - 230}px;text-align:center")
J.append(f'tl.fromTo("#bub2-in", {{ x: 420, y: 520, scale: .4, rotation: 12 }}, {{ x: 0, y: 0, scale: 1, rotation: -4, duration: .4, ease: "back.out(1.6)" }}, {F(t_kom2 - .05)});')

# s3: Kontinent-Schilder unten
html += ui("k3", st("s3") + .1, en("s3"), chip("k3a", "EUROPA 3 %", EU_COL, "#fff", 54) + '<span style="display:inline-block;width:24px"></span>' + chip("k3b", "ASIEN 97 %", AS_COL, "#111", 54),
           f"left:0;right:0;top:{LOW1 + 20}px;text-align:center")
pop("k3a", st("s3") + .1); pop("k3b", st("s3") + .25)
html += ui("bo3", t_eu3 - .05, t_as3 - .05, chip("bo3-in", "BOSPORUS = GRENZE", "#fff35c", "#111", 48), f"left:0;right:0;top:{LOW2 + 20}px;text-align:center")
pop("bo3-in", t_eu3 - .05)
html += ui("kk3", t_as3 - .05, en("s3"), chip("kk3-in", "1 LAND · 2 KONTINENTE", "#fff", "#111", 48), f"left:0;right:0;top:{LOW2 + 20}px;text-align:center")
pop("kk3-in", t_as3 - .05)

# s4: Haselnuss-Berg + Glas (ohne Logo) + Schild 58 %
NUT = lambda x, y, r, rot: (f'<g transform="translate({x:.0f} {y:.0f}) rotate({rot:.0f}) scale({r:.2f})">'
                            '<ellipse cx="0" cy="6" rx="26" ry="24" fill="#a0622d" stroke="#111" stroke-width="5"/>'
                            '<path d="M-26 0 Q0 -14 26 0 Q22 -24 0 -27 Q-22 -24 -26 0 Z" fill="#d9a066" stroke="#111" stroke-width="5"/>'
                            '<ellipse cx="-9" cy="10" rx="6" ry="9" fill="#c98a4b" opacity=".8"/></g>')
random.seed(58); nuts = []
for row in range(6):
    n = 9 - row
    for k in range(n):
        x = 60 + (k - (n - 1) / 2) * 52 * 1.0 + 300 + random.uniform(-8, 8)
        y = 330 - row * 40 + random.uniform(-6, 6)
        nuts.append(NUT(x, y, random.uniform(.9, 1.15), random.uniform(-40, 40)))
PILE = f'<svg viewBox="0 0 720 400" width="720" height="400" style="overflow:visible;filter:drop-shadow(0 10px 0 rgba(0,0,0,.4))">{"".join(nuts)}</svg>'
JAR = ('<svg viewBox="0 0 200 260" width="190" height="247" style="overflow:visible;filter:drop-shadow(0 10px 0 rgba(0,0,0,.4))">'
       '<rect x="40" y="10" width="120" height="42" rx="10" fill="#fff" stroke="#111" stroke-width="7"/>'
       '<path d="M30 60 Q30 50 44 50 H156 Q170 50 170 60 V230 Q170 252 148 252 H52 Q30 252 30 230 Z" fill="#5a2e14" stroke="#111" stroke-width="7"/>'
       '<rect x="44" y="110" width="112" height="90" rx="12" fill="#fff" stroke="#111" stroke-width="5"/>'
       '<g transform="translate(100 156) scale(1.2)"><ellipse cx="0" cy="6" rx="26" ry="24" fill="#a0622d" stroke="#111" stroke-width="5"/>'
       '<path d="M-26 0 Q0 -14 26 0 Q22 -24 0 -27 Q-22 -24 -26 0 Z" fill="#d9a066" stroke="#111" stroke-width="5"/></g></svg>')
html += ui("pile4", st("s4") + .05, en("s4"), f'<div id="pile4-in" style="display:inline-block">{PILE}</div>', f"left:{FX - 420}px;top:{FY - 330}px")
J.append(f'tl.fromTo("#pile4-in", {{ y: -1100 }}, {{ y: 0, duration: .5, ease: "bounce.out" }}, {F(st("s4") + .05)});')
J.append(f'tl.fromTo("#pile4-in", {{ scale: 1 }}, {{ scale: 1.25, duration: .2, yoyo: true, repeat: 1, ease: "power2.out", transformOrigin: "50% 100%", immediateRender: false }}, {F(t_has4 - .05)});')
html += ui("jar4", t_has4 - .05, en("s4"), f'<div id="jar4-in" style="display:inline-block">{JAR}</div>', f"left:{FX + 250}px;top:{FY - 180}px")
J.append(f'tl.fromTo("#jar4-in", {{ y: 0 }}, {{ y: -90, duration: .22, yoyo: true, repeat: {max(1, int((en("s4") - t_has4) / .22) // 2 * 2 - 1)}, ease: "power2.out" }}, {F(t_has4)});')
html += ui("h4", t_has4 - .05, en("s4"),
           f'<div id="h4-in" style="display:inline-block;background:#fff;border:6px solid #111;border-radius:22px;box-shadow:0 8px 0 #111;padding:8px 30px;text-align:center">'
           f'<div style="font:900 72px/1.05 Inter,sans-serif;color:#a0622d">🌰 <span id="h4-v">0</span> %</div>'
           f'<div style="font:900 40px/1.15 Inter,sans-serif;color:#111">ALLER HASELNÜSSE</div><div style="font:700 28px/1.2 Inter,sans-serif;color:#555">(FAO 2023)</div></div>',
           f"left:0;right:0;top:{LOW1}px;text-align:center")
pop("h4-in", t_has4 - .05, .4, .2)
J.append(f'(() => {{ const o = {{ v: 0 }}; tl.fromTo(o, {{ v: 0 }}, {{ v: 58, duration: .8, ease: "power2.out", onUpdate: () => {{ document.getElementById("h4-v").textContent = Math.round(o.v); }} }}, {F(t_has4)}); }})();')
html += ui("j4", st("s4") + .1, t_has4 - .05, chip("j4-in", "JEDE 2. HASELNUSS? 🌰", "#fff", "#111", 52), f"left:0;right:0;top:{LOW1 + 30}px;text-align:center")
pop("j4-in", st("s4") + .1)

# s5: Russland – Schild + NUR GLOBI!
html += ui("ru5", st("s5") + .05, en("s5"), chip("ru5-in", "RUSSLAND: EUROPA + ASIEN", GLOBI_COL, "#111", 52), f"left:0;right:0;top:{SRC_TOP + 30}px;text-align:center")
pop("ru5-in", st("s5") + .05)
html += ui("ng5", t_glo5 - .05, en("s5"), f'<div id="ng5-in" style="display:inline-block;transform:rotate(-6deg);background:#ffd166;color:#e63946;font:900 120px/1 Inter,sans-serif;padding:10px 40px;border:10px solid #111;border-radius:26px;box-shadow:0 12px 0 #111">NUR GLOBI!</div>', f"left:0;right:0;top:{LOW1 + 10}px;text-align:center")
J.append(f'tl.fromTo("#ng5-in", {{ scale: 2 }}, {{ scale: 1, duration: .25, ease: "back.out(2)" }}, {F(t_glo5 - .05)});')
html += ui("ur5", t_eu5 - .05, t_glo5 - .05, chip("ur5-in", "URAL = GRENZE", "#fff35c", "#111", 52), f"left:0;right:0;top:{LOW1 + 30}px;text-align:center")
pop("ur5-in", t_eu5 - .05)

# s6: Split – oben Russland/Globi, unten Türkei „?“ + Kommentar
html += ui("sp6a", st("s6") + .05, en("s6"), chip("sp6a-in", "1 × GLOBI ✅", GLOBI_COL, "#111", 48), f"left:40px;top:{SRC_TOP + 40}px")
html += ui("sp6b", st("s6") + .15, en("s6"), chip("sp6b-in", "2. LAND? 💬", "#fff", "#e63946", 64), f"left:0;right:0;top:{LOW1 + 20}px;text-align:center")
pop("sp6a-in", st("s6") + .05); pop("sp6b-in", st("s6") + .15)
html += ui("q6", st("s6") + .1, en("s6"), QM("q6-in").replace("280px", "220px"), f"left:{FX - 130}px;top:{FY - 100}px;width:260px;text-align:center")
pop("q6-in", st("s6") + .1)

# s7: großer Ladebalken über der Türkei
html += ui("big7", st("s7") + .05, en("s7"),
           '<div id="big7-in" style="position:relative;margin:0 auto;width:960px;height:130px;background:#fff;border:8px solid #111;border-radius:65px;box-shadow:0 10px 0 #111;overflow:hidden">'
           '<div id="b7f" style="position:absolute;left:0;top:0;bottom:0;width:0%;background:#06d6a0"></div>'
           '<div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font:900 54px Inter,sans-serif;color:#111">'
           'LAND WIRD VERGEBEN …&nbsp;<span id="b7v" style="color:#e63946">0 %</span></div></div>', f"left:0;right:0;top:{FY - 330}px")
pop("big7-in", st("s7") + .05, .3, .25)
J.append(f'tl.fromTo("#b7f", {{ width: "0%" }}, {{ width: "99%", duration: {max(.5, t_99 - st("s7") + .2):.2f}, ease: "power2.inOut" }}, {F(st("s7") + .15)});')
J.append(f'(() => {{ const o = {{ v: 0 }}; tl.fromTo(o, {{ v: 0 }}, {{ v: 99, duration: {max(.5, t_99 - st("s7") + .2):.2f}, ease: "power2.inOut", onUpdate: () => {{ document.getElementById("b7v").textContent = Math.round(o.v) + " %"; }} }}, {F(st("s7") + .15)}); }})();')
J.append(f'tl.fromTo("#b7v", {{ opacity: 1 }}, {{ opacity: .25, duration: .25, yoyo: true, repeat: {max(1, int((en("s7") - t_99 - .4) / .25) // 2 * 2 - 1)}, ease: "steps(1)", immediateRender: false }}, {F(t_99 + .4)});')
html += ui("hg7", t_99 + .2, en("s7"), chip("hg7-in", "… HÄNGT FEST! 😬", "#e63946", "#fff", 52), f"left:0;right:0;top:{LOW1 + 30}px;text-align:center")
pop("hg7-in", t_99 + .2)

# s8: Name + Land oben
for k, (cid, _) in enumerate(RUND):
    o = owned[cid]; t1 = TR[RUND[k + 1][0]] if k + 1 < len(RUND) else en("s8")
    html += ui(f"nm{cid}", TR[cid] + .03, t1, chip(f"nm{cid}-in", f'{o["land_de"]} · {o["name"]}', o["farbe"], "#111", 56), f"left:0;right:0;top:{SRC_TOP + 30}px;text-align:center")
    pop(f"nm{cid}-in", TR[cid] + .03, .5, .18)
html += ui("own8", st("s8") + .05, en("s8"), chip("own8-in", f"{NOWN} ECHTE BESITZER", "#fff", "#111", 48), f"left:0;right:0;top:{LOW1 + 30}px;text-align:center")
# s9: FREI!-Stempel an Japan / Italien, Globi winkt
for id_, t0, t1 in (("fr9a", st("s9") + .05, t_it9 - .05), ("fr9b", t_it9, t_auf9 - .05)):
    html += ui(id_, t0, t1, FREIST(id_ + "-in"), f"left:80px;top:{FY + 20}px")
    J.append(f'tl.fromTo("#{id_}-in", {{ scale: 1.6 }}, {{ scale: 1, duration: .25, ease: "back.out(2)" }}, {F(t0)});')
html += ui("jp9", st("s9") + .05, t_it9 - .05, chip("jp9-in", "JAPAN", "#fff", "#e63946", 60), f"left:0;right:0;top:{SRC_TOP + 30}px;text-align:center")
html += ui("it9", t_it9, t_auf9 - .05, chip("it9-in", "ITALIEN", "#fff", "#e63946", 60), f"left:0;right:0;top:{SRC_TOP + 30}px;text-align:center")
html += ui("ru9", t_auf9 - .05, en("s9"), chip("ru9-in", "RUSSLAND: GLOBI", GLOBI_COL, "#111", 56), f"left:0;right:0;top:{SRC_TOP + 30}px;text-align:center")
html += ui("ho9", t_glo9 - .05, en("s9"), chip("ho9-in", "HOLT ES ZURÜCK! 💬 „RUSSLAND!“", "#fff", "#111", 44), f"left:0;right:0;top:{LOW1 + 30}px;text-align:center")
pop("ho9-in", t_glo9 - .05)
# s10: Zähler groß 5/195 → NOCH 190 FREI
html += ui("big10", st("s10") + .05, en("s10"),
           f'<div id="big10-in" style="display:inline-block;background:rgba(11,26,51,.92);border:6px solid #fff;border-radius:28px;padding:10px 40px">'
           f'<div style="font:900 120px/1 Inter,sans-serif;color:#fff"><span style="color:#06d6a0">{NOWN}</span>/{TOTAL}</div>'
           f'<div id="big10-f" style="font:900 64px/1.1 Inter,sans-serif;color:#ffd166;margin-top:6px;opacity:0">NOCH {FREI} FREI!</div></div>', f"left:0;right:0;top:{LOW1}px;text-align:center")
J.append(f'tl.fromTo("#big10-in", {{ scale: 0, y: -400 }}, {{ scale: 1, y: 0, duration: .35, ease: "back.out(1.8)" }}, {F(st("s10") + .05)});')
J.append(f'tl.fromTo("#big10-f", {{ opacity: 0, scale: 1.8 }}, {{ opacity: 1, scale: 1, duration: .25, ease: "back.out(2)", immediateRender: false }}, {F(t_noch10 - .05)});')

open("compositions/welt.html", "w", encoding="utf-8").write(f'''<template>
  <style>#root {{ position: absolute; inset: 0; overflow: hidden; background: #0b1a33; }} .ui {{ position: absolute; font-family: Inter, sans-serif; }}</style>
  <div id="root" data-composition-id="welt" data-width="1080" data-height="1920">
    <svg class="clip" data-start="0" data-duration="{F(END)}" viewBox="0 0 1080 1920" style="position:absolute;left:0;top:0;width:1080px;height:1920px" data-layout-ignore>{MAP}</svg>
    {html}
  </div>
  <script>(function () {{ const tl = gsap.timeline({{ paused: true }});
{chr(10).join("    " + j for j in J)}
    window.__timelines["welt"] = tl; }})();</script>
</template>
''')

# ---------- Globi (stumm, Maskottchen) ----------
GK = lambda k, X, Y: (X - 190 * k, Y - 490 * k)
def gset(t, k, X, Y, op=1):
    x, y = GK(k, X, Y); GJ.append(f'tl.set("#g-wrap", {{ x: {x:.0f}, y: {y:.0f}, scale: {k}, opacity: {op} }}, {F(t)});')
def gto(t, d, k, X, Y, ease="power2.out"):
    x, y = GK(k, X, Y); GJ.append(f'tl.to("#g-wrap", {{ x: {x:.0f}, y: {y:.0f}, scale: {k}, duration: {d:.2f}, ease: "{ease}" }}, {F(t)});')
def gpop(t): GJ.append(f'tl.fromTo("#g-wrap", {{ y: "+=220" }}, {{ y: "-=220", duration: .3, ease: "back.out(2)", immediateRender: false }}, {F(t)});')
def ghide(t): GJ.append(f'tl.set("#g-wrap", {{ opacity: 0 }}, {F(t)});')
GJ.append('tl.set("#g-wrap", { transformOrigin: "0 0", opacity: 0 }, 0);')
GEST = []
# Bild 0 / Loop: schaut von Südrussland herüber (folgt dem Punch-Zoom)
def g_bild0(t0, z_from, z_to, d, ease):
    X1, Y1 = screen(*RU_SUED, TRC[0], TRC[1], z_from); X2, Y2 = screen(*RU_SUED, TRC[0], TRC[1], z_to)
    gset(t0, .5, X1, Y1 + 90); gto(t0, d, .5, X2, Y2 + 90, ease)
g_bild0(0, Z0, Z_TR, .6, "power2.out"); GEST.append((0, t_cut1, "think"))
# s1 2. Einstellung: groß rechts oben
c, z = (TRC[0] + 9, TRC[1] - 4), Z_TR * 1.35
X, Y = screen(*RU_SUED, *c, z); gset(t_cut1, .6, min(X, 960), max(Y + 20, 640)); GEST.append((t_cut1, st("s2") - t_cut1, "shock"))
# s2: zeigt auf den Abo-Knopf (links über dem Pflichtsatz)
gset(st("s2"), .55, 170, CAP_TOP - 10); gpop(st("s2")); GEST.append((st("s2") + .1, en("s2") - st("s2") - .2, "point"))
ghide(en("s2"))
# s4: Globi mit Haselnüssen (Backen voll) – rechts oben
gset(t_has4 - .05, .55, 930, FY - 200); gpop(t_has4 - .05); GEST.append((t_has4, en("s4") - t_has4 - .1, "both")); ghide(en("s4"))
# s5: sitzt breit auf Russland
X5, Y5 = screen(RUF[0] - 75, RUF[1] + 30, *ctr(RU_BOX), Z_RU * .95)
gset(t_glo5 - .05, .62, X5, min(Y5, 1000)); gpop(t_glo5 - .05); GEST.append((t_glo5, en("s5") - t_glo5 - .1, "both")); ghide(en("s5"))
# s6: Split – Globi oben auf Russland, nervös
X6, Y6 = screen(*geo(40.5, 50.5), *SPLIT_C, Z_SPLIT)
gset(st("s6"), .55, X6, Y6); GEST.append((st("s6"), en("s6") - st("s6"), "shock")); ghide(en("s6"))
# s7: beißt Fingernägel (rechts unten neben dem Ladebalken)
gset(st("s7") + .1, .55, 920, CAP_TOP - 20); gpop(st("s7") + .1); GEST.append((st("s7") + .1, en("s7") - st("s7") - .2, "scratch")); ghide(en("s7"))
# s9: winkt frech auf Russland
X9, Y9 = screen(RUF[0] - 75, RUF[1] + 30, *ctr(RU_BOX), Z_RU)
gset(t_auf9 - .05, .62, X9, min(Y9, 1000)); gpop(t_auf9 - .05); GEST.append((t_auf9, en("s9") - t_auf9 - .1, "wave")); ghide(en("s9"))
# s11 Loop: wie Bild 0
X, Y = screen(*RU_SUED, TRC[0], TRC[1], Z_TR); X2, Y2 = screen(*RU_SUED, TRC[0], TRC[1], Z0)
gset(LOOP_T, .5, X, Y + 90); gto(LOOP_T, END - LOOP_T, .5, X2, Y2 + 90, "sine.inOut"); GEST.append((LOOP_T, END - LOOP_T, "think"))
gh = globi.build({}, END, GEST, left=0, top=0)
gh = gh.replace('window.__timelines["globi"] = tl;', "\n      ".join(GJ) + '\n      window.__timelines["globi"] = tl;')
# Haselnüsse in den Backen (s4)
NUTS_G = (f'<div id="gnut" class="clip" data-start="{F(t_has4)}" data-duration="{F(en("s4") - t_has4)}" style="position:absolute;left:{930 - 64}px;top:{FY - 200 - 240}px;font:400 46px/1 \'Noto Color Emoji\'">🌰<span style="display:inline-block;width:36px"></span>🌰</div>')
gh = gh.replace('</div>\n  <script>', NUTS_G + '</div>\n  <script>', 1)
open("compositions/globi.html", "w", encoding="utf-8").write(gh)

# ---------- Untertitel: hart wechselnd, Schlüsselwörter ≥ 0,3 s ----------
HOT = {o["name"] for o in OWN} | {norm(o["land_de"]).upper() for o in OWN} | {"TÜRKEI", "ITALIEN", "JAPAN", "RUSSLAND", "ABONNIER", "ABONNENTEN", "GLOBI", "FREI",
       "99", "%", "5", "195", "190", "WUNSCHLAND", "EUROPA", "ASIEN", "HASELNUSS", "KONTINENTEN", "ZWEITE", "LAND", "USA"}
caps = []
for sc in V["scenes"]:
    sid = sc["id"]; words = T[sid]["words"]; k = 0
    for disp, sp in sc["groups"]:
        dw = [d for d in disp.split() if any(ch.isalnum() for ch in d) or d == "%"]; swn = sp.split()
        idx = [*range(len(dw))] if len(dw) == len(swn) else [int(j * len(swn) / len(dw)) for j in range(len(dw))]
        for j, d in enumerate(dw): caps.append([round(T[sid]["start"] + words[min(len(words) - 1, k + idx[j])]["s"], 2), d, sid])
        k += len(swn)
# „99 %“ als ein Untertitel
mrg = []
for c_ in caps:
    if c_[1] == "%" and mrg: mrg[-1][1] += " %"
    else: mrg.append(c_)
caps = mrg
key = lambda d: re.sub(r"[!?.,:–… ]", "", d.upper()) in HOT or d.strip().endswith("%")
for j in range(1, len(caps)):
    mind = .3 if key(caps[j - 1][1]) else .14
    caps[j][0] = round(max(caps[j][0], caps[j - 1][0] + mind), 2)
items = []
for j, (t0, d, sid) in enumerate(caps):
    nxt = caps[j + 1][0] if j + 1 < len(caps) else END
    te = min(nxt, t0 + 1.3, en(sid) + .2) if j + 1 < len(caps) else min(END, t0 + 1.6)
    up = d.upper(); col = "#ffd166" if key(d) else "#fff"
    fs = min(96, int(1250 / max(1, len(up))))           # lange Wörter kleiner (max ~900 px breit)
    items.append(f'<div id="w{j}" class="wd clip" data-start="{F(t0)}" data-duration="{F(max(.12, te - t0))}"><span style="color:{col};font-size:{fs}px">{up}</span></div>')
open("compositions/caps.html", "w", encoding="utf-8").write(f'''<template>
  <style>#root {{ position: absolute; inset: 0; }} .wd {{ position: absolute; left: 0; right: 0; top: {CAP_TOP}px; text-align: center; }}
    .wd span {{ display: inline-block; font: 900 96px/1 Inter, sans-serif; white-space: nowrap; -webkit-text-stroke: 14px #000; paint-order: stroke fill; }}</style>
  <div id="root" data-composition-id="caps" data-width="1080" data-height="1920">{"".join(items)}</div>
  <script>(function () {{ const tl = gsap.timeline({{ paused: true }}); window.__timelines["caps"] = tl; }})();</script>
</template>
''')

# ---------- Ton (fester Hintergrund-Sound über story_musik.py → assets/bgm.mp3) ----------
subprocess.run([sys.executable, "tools/story_musik.py", F(END), "1", "2", "3"], check=True)
FXL = [("pop", 0.03, .55, .15), ("boing", .5, .3, .55)]
for t in CUTS:
    if t != LOOP_T: FXL.append(("swoosh", t - .05, .3, .5))
FXL += [("pop", t_abo2 + .12, .55, .15), ("whoosh", t_kom2 - .05, .2, .6), ("pop", t_kom2 - .1, .35, .15)]
FXL += [("pop", st("s3") + .2, .4, .15), ("riser", t_eu3 - .3, .2, .8), ("chime", t_as3 - .05, .25, 1.2)]
FXL += [("hit", st("s4") + .3, .3, 1.2), ("blips", t_has4, .25, .9), ("boing", t_has4 + .3, .25, .5)]
FXL += [("klong", st("s5") + .02, .3, 1.0), ("tick", t_eu5, .25, .5), ("boing", t_glo5 - .05, .45, .55), ("chime", t_glo5 + .1, .25, 1.2)]
FXL += []
FXL += [("riser", st("s7") + .1, .25, min(1.5, t_99 - st("s7"))), ("klong", t_99 - .05, .35, 1.0), ("wirbel", t_99 + .3, .4, min(2.04, st("s8") - t_99 - .35))]
for cid, _ in RUND: FXL.append(("pop", TR[cid] + .03, .45, .15))
FXL += [("pop", st("s9") + .05, .5, .15), ("pop", t_it9, .5, .15), ("boing", t_auf9 - .05, .45, .55)]
FXL += [("hit", st("s10") + .05, .45, 1.6), ("blips", t_noch10 + .05, .3, 1.33)]
FXL += [("pop", st("s11") + .05, .45, .15), ("pop", t_abo11 - .05, .45, .15), ("boing", LOOP_T + .05, .3, .55)]
Hh = lambda id_, ti: f'      <div id="{id_}" data-composition-id="{id_}" data-composition-src="compositions/{id_}.html" data-start="0" data-duration="{F(END)}" data-track-index="{ti}" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index:{ti}"></div>'
lines = [Hh("welt", 2), Hh("caps", 3), Hh("globi", 6), f'      <audio id="musik" class="clip" data-start="0" data-duration="{F(END)}" data-track-index="5" data-volume="0.15" src="assets/musik.wav"></audio>']
for k in T:
    d = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"assets/vo/{k}.mp3"]))
    lines.append(f'      <audio id="vo-{k}" class="clip" data-start="{T[k]["start"] + T[k]["lead"]:.2f}" data-duration="{d:.2f}" data-track-index="4" data-volume="1" src="assets/vo/{k}.mp3"></audio>')
for j, (n, at, vol, dur) in enumerate(FXL):
    lines.append(f'      <audio id="fx-{j}" class="clip" data-start="{F(max(0, at))}" data-duration="{F(min(dur, END - max(0, at)))}" data-volume="{vol}" data-track-index="{20 + j}" src="assets/sfx2/{n}.mp3"></audio>')
open("index.html", "w", encoding="utf-8").write(f'''<!doctype html>
<html lang="de" data-resolution="portrait"><head><meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" /><script src="assets/gsap.min.js"></script>
<style>* {{ margin: 0; padding: 0; box-sizing: border-box; }} html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #0b1a33; }} #root {{ width: 100%; height: 100%; }}</style></head>
<body><div id="root" data-composition-id="main" data-start="0" data-duration="{F(END)}" data-width="1080" data-height="1920">
{chr(10).join(lines)}
</div><script>window.__timelines = window.__timelines || {{}}; window.__timelines["main"] = gsap.timeline({{ paused: true }});</script></body></html>
''')
print("Ende", END, "Schnitte", len(CUTS), [F(t) for t in CUTS])
gaps = [b - a for a, b in zip([0] + CUTS, CUTS + [END])]
print("längste Einstellung", F(max(gaps)), "s")
print("Türkei-Teilflächen EU/AS:", len(TR_EU), len(TR_AS))
