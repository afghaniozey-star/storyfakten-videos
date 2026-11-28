"""ABO-WELT Tag 6 (YouTube) – EREIGNIS-Tag „NORDAMERIKA-BÜNDNIS“ (keine neuen Besitzer).
Kanada (FINNY) und die USA (LIAM) sind Nachbarn und schließen ein Bündnis (🤝 + ❤️ an der Grenze), der dritte Nachbar
Mexiko ist FREI: „Wer holt sich Mexiko und tritt dem Bündnis bei?“. Fakt: Mexiko > 5 × Deutschland (CIA World Factbook),
5 Deutschland-Silhouetten poppen nacheinander. Pflichtsatz (Abo-Aufruf) gesprochen + eingeblendet am Anfang und Ende,
Fortschrittsbalken oben links, großer Ladebalken mit Trommelwirbel-Pause, Rundflug über die 5 echten Besitzer,
Türkei/Italien/Japan FREI!, Globi winkt von Russland, Zähler 5/195 → NOCH 190 FREI, Loop-Ende = Bild 0.
Aufruf (im Projektordner): /usr/bin/python3 tools/abowelt_tag6.py
liest welt.json, daten.json (= daten-tag6.json), voice.json (= voice-tag6.json), assets/vo/timing.json, weltkarte.json
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
assert not ({"mx", "tr", "it", "jp"} & set(owned)), "Mexiko/Türkei/Italien/Japan sind laut welt.json nicht mehr frei"
assert owned["ca"]["name"] == "FINNY" and owned["us"]["name"] == "LIAM"
assert NOWN == 5 and FREI == 190
GLOBI_COL = "#ff8a3d"; BAIT_COL = "#ffffff"; FREE_COL = "#46578a"; HI_COL = "#ffd166"
S0, MY = 1080 / 1010, 560
FX, FY = 540, 860
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
MXB = K["mx"]["bbox"]; MXC = (ctr(MXB)[0] - 4, ctr(MXB)[1] - 4)       # Zentrum etwas nach Nordwest (Hauptland)
Z_MX = zoom_for(MXB, 30.0, fw=900, fh=640)
NA_BOX = [70, 110, 300, 425]; Z_NA = zoom_for(NA_BOX, 6, 960, 960); Z0 = Z_NA * 1.08
NA_C = (180, 375)                                                         # Grenze ~y 640, Mexiko ~y 920 (über Untertitel/Abo-Block)
BORDER = (geo(-97, 49)[0] + 5, geo(-97, 49)[1])                          # 49. Breitengrad, Grenze Kanada/USA
ITB = K["it"]["bbox"]; ITC = ctr(ITB); JPB = K["jp"]["bbox"]; JPC = ctr(JPB); TRB = K["tr"]["bbox"]; TRC = ctr(TRB)
RU_BOX = [560, 50, 1005, 300]; Z_RU = zoom_for(RU_BOX, 3)
RU = polys("ru")
def inner_y(x, want):
    for d in range(0, 140):
        for yy in (want + d, want - d):
            if all(inside(RU, x + dx, yy + dy) for dx, dy in ((0, 0), (6, 0), (-6, 0), (0, 6), (0, -6))): return yy
    return want
RUF = (760, inner_y(760, 150))
WORLD_C = (505, 333)

paths = []
for cid, c in K.items():
    if cid in owned: col = owned[cid]["farbe"]
    elif cid in ("mx", "jp", "it", "tr"): col = BAIT_COL
    elif cid == "ru": col = GLOBI_COL
    else: col = FREE_COL
    paths.append(f'<path id="c-{cid}" d="{c["path"]}" fill="{col}" stroke="#141c33" stroke-width="0.6" vector-effect="non-scaling-stroke"/>')

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
pins += flag("pw-mx", MXC[0] - 2, MXC[1] + 20, "MEXIKO?", "#ffffff", 1.0, k=.62, fg="#e63946")
# Bündnis-Ansicht: FINNY / LIAM / MEXIKO? auf der Nordamerika-Karte
pins += flag("na-ca", 190, 240, "FINNY", owned["ca"]["farbe"], Z_NA, k=.8)
pins += flag("na-us", 140, 365, "LIAM", owned["us"]["farbe"], Z_NA, k=.8, fg="#fff")
pins += flag("na-mx", MXC[0] - 4, MXC[1] + 8, "MEXIKO?", "#ffffff", Z_NA, k=.8, fg="#e63946")
MAP = (f'<g id="cam"><rect x="-6000" y="-6000" width="14000" height="14000" fill="#0e3a66"/>'
       f'<g transform="translate(0 {MY}) scale({S0:.5f})">{"".join(paths)}{pins}</g></g>')

# ---------- Schnittliste ----------
shot(0, center=NA_C, z=Z0, drift=1.0)                                            # Bild 0 (Punch-Zoom 108 → 100 %)
t_sch1 = w("s1", "schließen"); t_cut1 = min(1.5, t_sch1 - .05)
shot(t_cut1, center=(BORDER[0], BORDER[1] + 4), z=Z_NA * 1.7)                    # Grenze groß: Handschlag
t_abo2 = w("s2", "Abonnier"); t_kom2 = w("s2", "kommentier"); t_nur2 = w("s2", "nur")
shot(st("s2"), center=NA_C, z=Z_NA * .85)
shot(t_kom2 - .05, center=MXC, z=Z_MX * .55)                                      # Sprechblase fliegt auf Mexiko
shot(t_nur2 - .05, center=MXC, z=Z_MX * .7)
t_lia3 = w("s3", "Liam"); t_nac3 = w("s3", "Nachbarn!")
shot(st("s3"), center=PT["ca"], z=ZO["ca"])                                       # FINNY / Kanada
shot(t_lia3 - .05, center=PT["us"], z=ZO["us"])                                   # LIAM / USA
shot(t_nac3 - .25, center=(BORDER[0], BORDER[1] + 10), z=Z_NA * 1.25)             # Bündnis an der Grenze
t_mex4 = w("s4", "Mexiko")
shot(st("s4"), center=NA_C, z=Z_NA * .95)                                               # ein Nachbar fehlt
shot(t_mex4 - .05, center=MXC, z=Z_MX)                                            # Mexiko FREI!
t_fue5 = w("s5", "fünfmal"); t_deu5 = w("s5", "Deutschland!")
shot(st("s5"), center=MXC, z=Z_MX * .8)
shot(t_fue5 - .05, center=(MXC[0], MXC[1] - 8), z=Z_MX * .62, drift=1.06)
t_mex6 = w("s6", "Mexiko"); t_bue6 = w("s6", "Bündnis")
shot(st("s6"), center=NA_C, z=Z_NA * .95, drift=1.02)                                         # Dreier-Ansicht
t_an7 = w("s7", "an"); t_hang = round(t_an7 + .35, 2)
shot(st("s7"), center=MXC, z=Z_MX * .85)                                          # großer Ladebalken
shot(t_hang, center=MXC, z=Z_MX * 1.1, drift=1.08)
RUND = [("ca", "Kanada"), ("br", "Brasilien"), ("de", "Deutschland"), ("us", "USA"), ("au", "Australien")]
TR = {}
for cid, word in RUND:
    TR[cid] = w("s8", word) - .05 if cid != "ca" else st("s8")
    shot(TR[cid], center=PT[cid] if cid in ("ca", "us") else ctr(FOC[cid]), z=ZO[cid])
t_it9 = w("s9", "Italien"); t_jp9 = w("s9", "Japan"); t_auf9 = w("s9", "Auf"); t_glo9 = w("s9", "Globi!")
Z_TR = zoom_for(TRB, 13.0, 820, 700); Z_JP = zoom_for(JPB, 9.0, 820, 700); Z_IT = zoom_for(ITB, 13.0, 820, 700)
shot(st("s9"), center=TRC, z=Z_TR)                                                # Türkei FREI!
shot(t_it9 - .05, center=ITC, z=Z_IT)                                             # Italien FREI!
shot(t_jp9 - .05, center=(JPC[0] + 4, JPC[1]), z=Z_JP)                            # Japan FREI!
shot(t_auf9 - .05, box=RU_BOX, zmax=3)                                            # Globi winkt
t_noch10 = w("s10", "Noch")
shot(st("s10"), center=WORLD_C, z=1.0)                                            # Welt + Zähler
shot(t_noch10 - .05, center=(540, 320), z=1.08)
t_wer11 = w("s11", "Wer"); t_abo11 = w("s11", "Abonnier"); t_nur11 = w("s11", "nur")
shot(st("s11"), center=MXC, z=Z_MX * .9)
shot(t_abo11 - .05, center=NA_C, z=Z_NA * .85)
LOOP_T = round(max(t_nur11 + .9, END - 2.2), 2)
SHOTS.append((LOOP_T, NA_C[0], NA_C[1], Z_NA, "loop"))                            # Bild-0-Einstellung, zoomt bis END auf Z0
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
        x2, y2 = campos(cx, cy, Z_NA)
        J.append(f'tl.to("#cam", {{ x: {x2:.1f}, y: {y2:.1f}, scale: {Z_NA:.3f}, duration: .6, ease: "power2.out" }}, 0);')
    elif drift != 1.0:
        x2, y2 = campos(cx, cy, z * drift)
        J.append(f'tl.to("#cam", {{ x: {x2:.1f}, y: {y2:.1f}, scale: {z * drift:.3f}, duration: {t1 - t:.2f}, ease: "none" }}, {F(t)});')
    if t > 0: CUTS.append(t)
    CAMAT.append((t, cx, cy, z))
J.insert(0, 'tl.set("#cam", { svgOrigin: "0 0" }, 0);')

# ---------- Ereignisse auf der Karte ----------
def show(id_, t0, t1, popd=.3):
    J.append(f'tl.set("#{id_}", {{ opacity: 1 }}, {F(t0)}); tl.fromTo("#{id_}-in", {{ scale: 0, transformOrigin: "0px 0px" }}, {{ scale: 1, duration: {popd}, ease: "back.out(2.5)" }}, {F(t0)});')
    J.append(f'tl.set("#{id_}", {{ opacity: 0 }}, {F(t1)});')
def blink(sel, c0, c1, t0, t1, per=.25):
    n = max(1, int((t1 - t0) / per) // 2 * 2 - 1)
    J.append(f'tl.fromTo("{sel}", {{ fill: "{c0}" }}, {{ fill: "{c1}", duration: {per}, yoyo: true, repeat: {n}, ease: "steps(1)", immediateRender: false }}, {F(t0)});')
    J.append(f'tl.set("{sel}", {{ fill: "{c0}" }}, {F(t1)});')
mxblink = lambda t0, t1: blink("#c-mx", BAIT_COL, HI_COL, t0, t1, .28)
mxblink(.15, st("s2")); mxblink(t_mex4 - .05, en("s5")); mxblink(st("s6") + .1, en("s6")); mxblink(st("s11") + .1, t_abo11 - .05); mxblink(LOOP_T, END)
# s3: Bündnis-Fahnen
show("p-ca", st("s3") + .05, t_lia3 - .05, .22); show("p-us", t_lia3, t_nac3 - .25, .22)
for id_, t0, t1 in (("na-ca", t_nac3 - .2, en("s3")), ("na-us", t_nac3 - .1, en("s3")),
                    ("na-ca", st("s6") + .05, en("s6")), ("na-us", st("s6") + .1, en("s6")), ("na-mx", t_mex6 - .05, en("s6"))):
    show(id_, t0, t1, .25)
blink("#c-ca", owned["ca"]["farbe"], "#ffc2d1", t_nac3 - .2, en("s3"), .2); blink("#c-us", owned["us"]["farbe"], "#8fd3ff", t_nac3 - .2, en("s3"), .2)
# s8: Besitzer-Fahnen
for k, (cid, _) in enumerate(RUND):
    t1 = TR[RUND[k + 1][0]] if k + 1 < len(RUND) else en("s8")
    show(f"p-{cid}", TR[cid] + .03, t1, .22)
# s9: Türkei, Italien, Japan blinken, Russland blinkt
blink("#c-tr", BAIT_COL, HI_COL, st("s9"), t_it9 - .05)
blink("#c-it", BAIT_COL, HI_COL, t_it9 - .05, t_jp9 - .05)
blink("#c-jp", BAIT_COL, HI_COL, t_jp9 - .05, t_auf9 - .05)
blink("#c-ru", GLOBI_COL, HI_COL, t_auf9, en("s9"), .2)
# s10: Weltansicht – alle Fahnen, Mexiko?, freie Länder blitzen
for cid in owned: show(f"pw-{cid}", st("s10") + .05, en("s10"), .25)
for id_ in ("pw-globi", "pw-mx"): show(id_, st("s10") + .05, en("s10"), .25)
for c_ in ("mx", "tr", "it", "jp"): blink(f"#c-{c_}", BAIT_COL, HI_COL, st("s10"), en("s10"))
random.seed(9)
free = [c for c in K if c not in owned and c not in ("ru", "jp", "it", "tr", "mx") and K[c]["bbox"][2] - K[c]["bbox"][0] > 10]
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
EMO = lambda id_, e, px: f'<div id="{id_}" style="display:inline-block;font:400 {px}px/1 \'Noto Color Emoji\'">{e}</div>'
html = ""
HEAD_TOP = 96
BAR_TOP = 222
SRC_TOP = 300
CAP_TOP = 1065
LOW1, LOW2 = 1240, 1370
html += ui("head", 0, END, chip("head-in", "NORDAMERIKA-BÜNDNIS 🤝", "#ffd166", "#111", 56, "white-space:nowrap"), f"left:30px;right:30px;top:{HEAD_TOP}px;text-align:center")
html += ui("src", st("s3"), en("s5"), f'<div style="display:inline-block;background:rgba(0,0,0,.72);border-radius:10px;padding:4px 14px;font:700 26px Inter,sans-serif;color:#fff">{D["quellenzeile"]}</div>', f"left:30px;top:{SRC_TOP - 10}px")
CNT = f'<div style="display:inline-block;background:rgba(0,0,0,.72);border-radius:14px;padding:6px 18px;font:900 42px/1.15 Inter,sans-serif;color:#fff"><span style="color:#06d6a0">{NOWN}</span>/{TOTAL}</div>'
html += ui("cnt", 0, END, CNT, f"right:30px;top:{BAR_TOP}px")
# Fortschrittsbalken oben links „Land wird vergeben … ?“
html += ui("lb", 0, END,
           '<div style="position:relative;width:640px;height:62px;background:#fff;border:5px solid #111;border-radius:31px;box-shadow:0 6px 0 #111;overflow:hidden">'
           '<div id="lbf" style="position:absolute;left:0;top:0;bottom:0;width:4%;background:#06d6a0"></div>'
           '<div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font:900 32px Inter,sans-serif;color:#111">'
           'LAND WIRD VERGEBEN …&nbsp;<span style="color:#e63946">?</span></div></div>',
           f"left:30px;top:{BAR_TOP}px")
J.append(f'tl.fromTo("#lbf", {{ width: "3%" }}, {{ width: "8%", duration: .3, yoyo: true, repeat: {int(st("s7") / .3) // 2 * 2 - 1}, ease: "sine.inOut" }}, 0);')
J.append(f'tl.to("#lbf", {{ width: "99%", duration: {t_hang - st("s7"):.2f}, ease: "power2.inOut" }}, {F(st("s7") + .1)});')
J.append(f'tl.set("#lbf", {{ width: "4%" }}, {F(LOOP_T)});')
J.append(f'tl.fromTo("#lbf", {{ width: "3%" }}, {{ width: "8%", duration: .3, yoyo: true, repeat: {max(1, int((END - LOOP_T) / .3) // 2 * 2 - 1)}, ease: "sine.inOut", immediateRender: false }}, {F(LOOP_T + .02)});')

# Handschlag + Herz an der Grenze (Bild 0, s1, s3, s6, Loop) – Position folgt der jeweiligen Kamera
def hs(id_, t0, t1, z, center, px=150, heart=True):
    X, Y = screen(*BORDER, *center, z)
    inner = EMO(id_ + "-in", "🤝", px) + (EMO(id_ + "-h", "❤️", int(px * .55)) if heart else "")
    return ui(id_, t0, t1, f'<div style="display:flex;align-items:flex-start;gap:4px">{inner}</div>', f"left:{X - px * .55:.0f}px;top:{Y - px * .5:.0f}px")
html += hs("hs0", 0, t_cut1, Z_NA, NA_C)
J.append('tl.fromTo("#hs0-in", { scale: 0 }, { scale: 1, duration: .3, ease: "back.out(3)", immediateRender: false }, .05);')
J.append('tl.fromTo("#hs0-h", { scale: 0 }, { scale: 1, duration: .3, ease: "back.out(3)", immediateRender: false }, .3);')
html += hs("hs1", t_cut1, st("s2"), Z_NA * 1.7, (BORDER[0], BORDER[1] + 4), 260)
J.append(f'tl.fromTo("#hs1-in", {{ scale: .6 }}, {{ scale: 1, duration: .25, ease: "back.out(3)", immediateRender: false }}, {F(t_cut1)});')
J.append(f'tl.to("#hs1-in", {{ y: -18, duration: .16, yoyo: true, repeat: {max(1, int((st("s2") - t_cut1) / .16) // 2 * 2 - 1)}, ease: "sine.inOut" }}, {F(t_cut1 + .25)});')
J.append(f'tl.fromTo("#hs1-h", {{ scale: 1 }}, {{ scale: 1.25, duration: .25, yoyo: true, repeat: {max(1, int((st("s2") - t_cut1) / .25) // 2 * 2 - 1)}, ease: "sine.inOut" }}, {F(t_cut1)});')
html += hs("hs3", t_nac3 - .2, en("s3"), Z_NA * 1.25, (BORDER[0], BORDER[1] + 10), 200)
J.append(f'tl.fromTo("#hs3-in", {{ scale: 0 }}, {{ scale: 1, duration: .3, ease: "back.out(3)", immediateRender: false }}, {F(t_nac3 - .2)});')
html += hs("hs6", st("s6") + .05, en("s6"), Z_NA * .95, NA_C, 130)
html += hs("hsL", LOOP_T, END, Z_NA, NA_C)
J.append(f'tl.fromTo("#hsL-in", {{ scale: 0 }}, {{ scale: 1, duration: .3, ease: "back.out(3)", immediateRender: false }}, {F(LOOP_T + .05)});')

# großes „?“ auf Mexiko (Bild 0, s6, s11, Loop)
QM = lambda id_, px=200: (f'<div id="{id_}" style="display:inline-block;font:900 {px}px/1 Inter,sans-serif;color:#ffd166;-webkit-text-stroke:{px // 13}px #111;paint-order:stroke fill;'
                          'filter:drop-shadow(0 12px 0 rgba(0,0,0,.45))">?</div>')
def qm(id_, t0, t1, z, center, px):
    X, Y = screen(*MXC, *center, z)
    global html
    html += ui(id_, t0, t1, QM(id_ + "-in", px), f"left:{X - px * .6:.0f}px;top:{Y - px * .75:.0f}px;width:{px * 1.2:.0f}px;text-align:center")
    J.append(f'tl.fromTo("#{id_}-in", {{ rotation: -8 }}, {{ rotation: 8, duration: .35, yoyo: true, repeat: {max(1, int((t1 - t0) / .35) - 1)}, ease: "sine.inOut" }}, {F(t0)});')
    J.append(f'tl.fromTo("#{id_}-in", {{ scale: 0 }}, {{ scale: 1, duration: .3, ease: "back.out(3)", immediateRender: false }}, {F(t0 + .03)});')
qm("q0", 0, t_cut1, Z_NA, NA_C, 170)
qm("q11", st("s11"), t_abo11 - .05, Z_MX * .9, MXC, 260)
qm("qL", LOOP_T, END, Z_NA, NA_C, 170)
FREIST = lambda id_, px=110: f'<div id="{id_}" style="display:inline-block;transform:rotate(-9deg);background:#fff;color:#e63946;font:900 {px}px/1 Inter,sans-serif;padding:8px 30px;border:10px solid #e63946;border-radius:22px;box-shadow:0 10px 0 #111">FREI!</div>'

# Pflichtsatz (Abo-Aufruf): Anfang bis Ende s2, Schluss ab „Abonnier“ in s11
ABO = (chip("{id}-a", "🔔 ABONNIER", "#e63946", "#fff", 60) + '<div style="height:12px"></div>' +
       chip("{id}-b", "💬 + KOMMENTIER DEIN WUNSCHLAND", "#fff", "#111", 40) + '<div style="height:12px"></div>' +
       chip("{id}-c", "NUR ABONNENTEN BEKOMMEN EIN LAND!", "#ffd166", "#111", 40))
html += ui("ab1", 0, en("s2"), ABO.replace("{id}", "ab1"), f"left:0;right:0;top:{LOW1}px;text-align:center")
html += ui("ab11", t_abo11 - .05, END, ABO.replace("{id}", "ab11"), f"left:0;right:0;top:{LOW1}px;text-align:center")
J.append(f'tl.to("#ab1-a", {{ scale: 1.08, duration: .35, yoyo: true, repeat: {int(t_abo2 / .35) // 2 * 2 - 1}, ease: "sine.inOut" }}, .4);')
J.append(f'tl.fromTo("#ab1-a", {{ scale: 1 }}, {{ scale: .82, duration: .09, yoyo: true, repeat: 1, ease: "power2.in", immediateRender: false }}, {F(t_abo2 + .12)});')
J.append(f'tl.to("#ab11-a", {{ scale: 1.08, duration: .35, yoyo: true, repeat: {int((END - t_abo11) / .35) - 1}, ease: "sine.inOut" }}, {F(t_abo11 + .3)});')
pop("ab1-b", t_kom2 - .05, 1.4, .25); pop("ab1-c", t_nur2 - .05, 1.4, .25)
pop("ab11-a", t_abo11 - .05, 1.5, .2); pop("ab11-c", t_nur11 - .05, 1.3, .2)
html += ui("hand", t_abo2 - .35, t_kom2 - .05, '<div id="hand-in" style="font:400 110px/1 \'Noto Color Emoji\';display:inline-block">👍</div>', f"left:700px;top:{LOW1 - 20}px")
J.append(f'tl.fromTo("#hand-in", {{ x: 260, y: 200 }}, {{ x: 0, y: 0, duration: .35, ease: "power2.out" }}, {F(t_abo2 - .35)});')
J.append(f'tl.to("#hand-in", {{ x: -30, duration: .09, yoyo: true, repeat: 1 }}, {F(t_abo2 + .12)});')
html += ui("bub2", t_kom2 - .05, en("s2"), chip("bub2-in", "💬 „MEXIKO!“", "#fff", "#111", 64), f"left:0;right:0;top:{FY - 300}px;text-align:center")
J.append(f'tl.fromTo("#bub2-in", {{ x: 420, y: 520, scale: .4, rotation: 12 }}, {{ x: 0, y: 0, scale: 1, rotation: -4, duration: .4, ease: "back.out(1.6)" }}, {F(t_kom2 - .05)});')

# s3: Namen oben, Bündnis-Schild + Grenze unten
html += ui("nm3a", st("s3") + .03, t_lia3 - .05, chip("nm3a-in", "KANADA · FINNY", owned["ca"]["farbe"], "#111", 56), f"left:0;right:0;top:{SRC_TOP + 30}px;text-align:center")
html += ui("nm3b", t_lia3, t_nac3 - .25, chip("nm3b-in", "USA · LIAM", owned["us"]["farbe"], "#fff", 56), f"left:0;right:0;top:{SRC_TOP + 30}px;text-align:center")
pop("nm3a-in", st("s3") + .03, .5, .18); pop("nm3b-in", t_lia3, .5, .18)
html += ui("bd3", t_nac3 - .2, en("s3"), chip("bd3-in", "NACHBARN = BÜNDNIS! 🤝", "#ffd166", "#111", 54), f"left:0;right:0;top:{LOW1 + 30}px;text-align:center")
pop("bd3-in", t_nac3 - .2)
html += ui("gr3", t_nac3 - .1, en("s3"), chip("gr3-in", "GEMEINSAME GRENZE: 8.891 KM", "#fff", "#111", 46), f"left:0;right:0;top:{LOW2 + 40}px;text-align:center")
pop("gr3-in", t_nac3 - .1)
# s4: „1 Nachbar fehlt“ → MEXIKO + FREI!
html += ui("fe4", st("s4") + .05, t_mex4 - .05, chip("fe4-in", "3. NACHBAR FEHLT … 🤔", "#fff", "#111", 56), f"left:0;right:0;top:{LOW1 + 30}px;text-align:center")
pop("fe4-in", st("s4") + .05)
html += ui("mx4", t_mex4 - .05, en("s4"), chip("mx4-in", "MEXIKO", "#fff", "#e63946", 64), f"left:0;right:0;top:{SRC_TOP + 30}px;text-align:center")
pop("mx4-in", t_mex4 - .05, .5, .18)
html += ui("fr4", t_mex4, en("s4"), FREIST("fr4-in"), f"left:0;right:0;top:{LOW1 + 10}px;text-align:center")
J.append(f'tl.fromTo("#fr4-in", {{ scale: 1.8 }}, {{ scale: 1, duration: .25, ease: "back.out(2)", immediateRender: false }}, {F(t_mex4)});')
# s5: Fläche zählt hoch + 5 Deutschland-Silhouetten (LÅKIs Land)
DEB = K["de"]["bbox"]; DEP = dpath(polys("de"))
DESIL = lambda id_: (f'<svg id="{id_}" viewBox="{DEB[0] - 1:.1f} {DEB[1] - 1:.1f} {DEB[2] - DEB[0] + 2:.1f} {DEB[3] - DEB[1] + 2:.1f}" width="150" height="{150 * (DEB[3] - DEB[1] + 2) / (DEB[2] - DEB[0] + 2):.0f}" '
                     f'style="overflow:visible;filter:drop-shadow(0 6px 0 rgba(0,0,0,.5))"><path d="{DEP}" fill="{owned["de"]["farbe"]}" stroke="#111" stroke-width="1.2" stroke-linejoin="round"/></svg>')
html += ui("km5", st("s5") + .05, en("s5"),
           f'<div id="km5-in" style="display:inline-block;background:#fff;border:6px solid #111;border-radius:22px;box-shadow:0 8px 0 #111;padding:8px 30px;text-align:center">'
           f'<div style="font:900 44px/1.1 Inter,sans-serif;color:#111">MEXIKO</div>'
           f'<div style="font:900 72px/1.05 Inter,sans-serif;color:#0b8f5a"><span id="km5-v">0</span> km²</div></div>',
           f"left:0;right:0;top:{SRC_TOP + 40}px;text-align:center")
pop("km5-in", st("s5") + .05, .4, .2)
J.append(f'(() => {{ const o = {{ v: 0 }}; tl.fromTo(o, {{ v: 0 }}, {{ v: 1964375, duration: .9, ease: "power2.out", onUpdate: () => {{ document.getElementById("km5-v").textContent = Math.round(o.v).toLocaleString("de-DE"); }} }}, {F(st("s5") + .1)}); }})();')
sils = "".join(f'<div style="display:inline-block;margin:0 4px">{DESIL(f"de5-{k}")}</div>' for k in range(5))
html += ui("de5", t_fue5 - .05, en("s5"),
           f'<div style="display:flex;justify-content:center;align-items:flex-end">{sils}</div>'
           f'<div style="height:14px"></div>' + chip("de5-t", "MEHR ALS 5 × DEUTSCHLAND!", "#ffd166", "#111", 52),
           f"left:0;right:0;top:{LOW1 - 10}px;text-align:center")
t_sil = [round(t_fue5 + k * max(.12, (t_deu5 - t_fue5 + .2) / 5), 2) for k in range(5)]
for k, ts in enumerate(t_sil): J.append(f'tl.fromTo("#de5-{k}", {{ scale: 0, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: .22, ease: "back.out(2.5)", immediateRender: false }}, {F(ts - .05)});')
J.append(f'tl.set("#de5-t", {{ opacity: 0 }}, {F(t_fue5 - .05)}); tl.fromTo("#de5-t", {{ opacity: 0, scale: 1.6 }}, {{ opacity: 1, scale: 1, duration: .25, ease: "back.out(2)", immediateRender: false }}, {F(t_deu5)});')
# s6: Dreier-Bündnis? Schild unten
html += ui("m6", st("s6") + .15, en("s6"), chip("m6-in", "3. MITGLIED? 💬 „MEXIKO!“", "#fff", "#e63946", 54), f"left:0;right:0;top:{LOW1 + 30}px;text-align:center")
pop("m6-in", st("s6") + .15)
# s7: großer Ladebalken über Mexiko, bleibt bei 99 % hängen → Trommelwirbel
html += ui("big7", st("s7") + .05, en("s7"),
           '<div id="big7-in" style="position:relative;margin:0 auto;width:960px;height:130px;background:#fff;border:8px solid #111;border-radius:65px;box-shadow:0 10px 0 #111;overflow:hidden">'
           '<div id="b7f" style="position:absolute;left:0;top:0;bottom:0;width:0%;background:#06d6a0"></div>'
           '<div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font:900 54px Inter,sans-serif;color:#111">'
           'LAND WIRD VERGEBEN …&nbsp;<span id="b7v" style="color:#e63946">0 %</span></div></div>', f"left:0;right:0;top:{FY - 360}px")
pop("big7-in", st("s7") + .05, .3, .25)
J.append(f'tl.fromTo("#b7f", {{ width: "0%" }}, {{ width: "99%", duration: {t_hang - st("s7") - .1:.2f}, ease: "power2.inOut" }}, {F(st("s7") + .15)});')
J.append(f'(() => {{ const o = {{ v: 0 }}; tl.fromTo(o, {{ v: 0 }}, {{ v: 99, duration: {t_hang - st("s7") - .1:.2f}, ease: "power2.inOut", onUpdate: () => {{ document.getElementById("b7v").textContent = Math.round(o.v) + " %"; }} }}, {F(st("s7") + .15)}); }})();')
J.append(f'tl.fromTo("#b7v", {{ opacity: 1 }}, {{ opacity: .25, duration: .25, yoyo: true, repeat: {max(1, int((en("s7") - t_hang) / .25) // 2 * 2 - 1)}, ease: "steps(1)", immediateRender: false }}, {F(t_hang + .1)});')
html += ui("hg7", t_hang + .1, en("s7"), chip("hg7-in", "… DICH? 🥁", "#e63946", "#fff", 64), f"left:0;right:0;top:{LOW1 + 30}px;text-align:center")
pop("hg7-in", t_hang + .1)
# s8: Name + Land oben
for k, (cid, _) in enumerate(RUND):
    o = owned[cid]; t1 = TR[RUND[k + 1][0]] if k + 1 < len(RUND) else en("s8")
    html += ui(f"nm{cid}", TR[cid] + .03, t1, chip(f"nm{cid}-in", f'{o["land_de"]} · {o["name"]}', o["farbe"], "#111", 56), f"left:0;right:0;top:{SRC_TOP + 30}px;text-align:center")
    pop(f"nm{cid}-in", TR[cid] + .03, .5, .18)
html += ui("own8", st("s8") + .05, en("s8"), chip("own8-in", f"{NOWN} ECHTE BESITZER", "#fff", "#111", 48), f"left:0;right:0;top:{LOW1 + 30}px;text-align:center")
# s9: FREI!-Stempel an Türkei / Italien / Japan, Globi winkt
for id_, t0, t1, nm in (("fr9a", st("s9") + .05, t_it9 - .05, "TÜRKEI"), ("fr9b", t_it9, t_jp9 - .05, "ITALIEN"), ("fr9c", t_jp9, t_auf9 - .05, "JAPAN")):
    html += ui(id_, t0, t1, FREIST(id_ + "-in"), f"left:80px;top:{LOW1 + 20}px")
    J.append(f'tl.fromTo("#{id_}-in", {{ scale: 1.6 }}, {{ scale: 1, duration: .25, ease: "back.out(2)" }}, {F(t0)});')
    html += ui(id_ + "n", t0, t1, chip(id_ + "n-in", nm, "#fff", "#e63946", 60), f"left:0;right:0;top:{SRC_TOP + 30}px;text-align:center")
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
# s11: „WER BEKOMMT MEXIKO?“
html += ui("wb11", st("s11") + .05, t_abo11 - .05, chip("wb11-in", "WER BEKOMMT MEXIKO?", "#fff", "#e63946", 64), f"left:0;right:0;top:{SRC_TOP + 30}px;text-align:center")
pop("wb11-in", st("s11") + .05)

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
def gpop(t): GJ.append(f'tl.fromTo("#g-wrap", {{ y: "+=220" }}, {{ y: "-=220", duration: .3, ease: "back.out(2)", immediateRender: false }}, {F(t)});')
def ghide(t): GJ.append(f'tl.set("#g-wrap", {{ opacity: 0 }}, {F(t)});')
GJ.append('tl.set("#g-wrap", { transformOrigin: "0 0", opacity: 0 }, 0);')
GEST = []
# s2: zeigt auf den Abo-Knopf
gset(st("s2"), .55, 170, CAP_TOP - 10); gpop(st("s2")); GEST.append((st("s2") + .1, en("s2") - st("s2") - .2, "point")); ghide(en("s2"))
# s7: kratzt sich nervös am Kopf (rechts neben dem Untertitel)
gset(st("s7") + .1, .55, 920, CAP_TOP - 20); gpop(st("s7") + .1); GEST.append((st("s7") + .1, en("s7") - st("s7") - .2, "scratch")); ghide(en("s7"))
# s9: winkt frech auf Russland
X9, Y9 = screen(RUF[0] - 75, RUF[1] + 30, *ctr(RU_BOX), zoom_for(RU_BOX, 3))
gset(t_auf9 - .05, .62, X9, min(Y9, 1000)); gpop(t_auf9 - .05); GEST.append((t_auf9, en("s9") - t_auf9 - .1, "wave")); ghide(en("s9"))
gh = globi.build({}, END, GEST, left=0, top=0)
gh = gh.replace('window.__timelines["globi"] = tl;', "\n      ".join(GJ) + '\n      window.__timelines["globi"] = tl;')
open("compositions/globi.html", "w", encoding="utf-8").write(gh)

# ---------- Untertitel: hart wechselnd, Schlüsselwörter ≥ 0,3 s ----------
HOT = {o["name"] for o in OWN} | {norm(o["land_de"]).upper() for o in OWN} | {"MEXIKO", "TÜRKEI", "ITALIEN", "JAPAN", "RUSSLAND", "ABONNIER", "ABONNENTEN", "GLOBI", "FREI",
       "5", "195", "190", "DICH", "5-MAL", "WUNSCHLAND", "BÜNDNIS", "NACHBARN", "NACHBAR", "DEUTSCHLAND", "LAND", "USA", "KANADA"}
caps = []
for sc in V["scenes"]:
    sid = sc["id"]; words = T[sid]["words"]; k = 0
    for disp, sp in sc["groups"]:
        dw = [d for d in disp.split() if any(ch.isalnum() for ch in d)]; swn = sp.split()
        idx = [*range(len(dw))] if len(dw) == len(swn) else [int(j * len(swn) / len(dw)) for j in range(len(dw))]
        for j, d in enumerate(dw): caps.append([round(T[sid]["start"] + words[min(len(words) - 1, k + idx[j])]["s"], 2), d, sid])
        k += len(swn)
key = lambda d: re.sub(r"[!?.,:–… ]", "", d.upper()) in HOT
for j in range(1, len(caps)):
    mind = .3 if key(caps[j - 1][1]) else .14
    caps[j][0] = round(max(caps[j][0], caps[j - 1][0] + mind), 2)
items = []
for j, (t0, d, sid) in enumerate(caps):
    nxt = caps[j + 1][0] if j + 1 < len(caps) else END
    te = min(nxt, t0 + 1.3, en(sid) + .2) if j + 1 < len(caps) else min(END, t0 + 1.6)
    up = d.upper(); col = "#ffd166" if key(d) else "#fff"
    fs = min(96, int(1250 / max(1, len(up))))
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
FXL = [("pop", 0.03, .55, .15), ("chime", .3, .3, 1.2)]
for t in CUTS:
    if t != LOOP_T: FXL.append(("swoosh", t - .05, .3, .5))
FXL += [("hit", t_cut1, .3, 1.0)]
FXL += [("pop", t_abo2 + .12, .55, .15), ("whoosh", t_kom2 - .05, .2, .6), ("pop", t_kom2 - .1, .35, .15)]
FXL += [("pop", st("s3") + .03, .45, .15), ("pop", t_lia3, .45, .15), ("chime", t_nac3 - .2, .3, 1.2)]
FXL += [("tick", st("s4") + .1, .3, .5), ("klong", t_mex4 - .05, .35, 1.0)]
FXL += [("blips", st("s5") + .1, .25, .9)] + [("pop", ts - .05, .45, .15) for ts in t_sil] + [("boing", t_deu5, .4, .55)]
FXL += [("pop", t_mex6 - .05, .45, .15), ("pop", st("s6") + .15, .4, .15)]
FXL += [("riser", st("s7") + .1, .25, min(1.5, t_hang - st("s7"))), ("klong", t_hang, .35, 1.0), ("wirbel", t_hang + .15, .45, min(2.04, en("s7") - t_hang - .15))]
for cid, _ in RUND: FXL.append(("pop", TR[cid] + .03, .45, .15))
FXL += [("pop", st("s9") + .05, .5, .15), ("pop", t_it9, .5, .15), ("pop", t_jp9, .5, .15), ("boing", t_auf9 - .05, .45, .55)]
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
print("Z_NA", round(Z_NA, 2), "Z_MX", round(Z_MX, 2), "Grenze", BORDER, "Handschlag Bild0", screen(*BORDER, *NA_C, Z_NA), "Mexiko Bild0", screen(*MXC, *NA_C, Z_NA))
