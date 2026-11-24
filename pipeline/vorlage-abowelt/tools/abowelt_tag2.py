"""ABO-WELT Tag 2 (YouTube) – EREIGNIS-Tag „Wer bekommt Japan?“ (keine neuen Besitzer).
Japan blinkt FREI ab 0,0 s, Abo-Aufruf, Inseln-Fakt, Rundflug über die echten Besitzer aus welt.json,
Globi (Maskottchen, kein Abonnent) schnappt sich Russland, Zähler X/195 + NOCH N FREI, Loop-Ende auf Japan.
Harte Schnitte/Zooms alle 2–3 s. Aufruf (im Projektordner): /usr/bin/python3 tools/abowelt_tag2.py
liest welt.json, voice.json, assets/vo/timing.json, weltkarte.json; braucht tools/globi.py + tools/globi_strich.py
Karte: @svg-maps/world (CC BY 4.0) → in der Beschreibung „Karte: svg-maps (CC BY 4.0)“ nennen."""
import json, re, subprocess, sys, random, math
sys.path.insert(0, "tools"); import globi_strich as globi
T = json.load(open("assets/vo/timing.json")); V = json.load(open("voice.json"))
W = json.load(open("welt.json")); K = json.load(open("weltkarte.json"))["laender"]
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
GLOBI_COL = "#ff8a3d"
S0, MY = 1080 / 1010, 560          # Kartenmaßstab, Karten-Oberkante
FX, FY = 540, 860                   # Bildpunkt, auf den die Kamera zentriert
J = []                              # Zeitleiste der Karte (welt)
GJ = []                             # Zeitleiste Globi (Position)

# ---------- Geometrie (Pfade bestehen nur aus m/z mit relativen Linien) ----------
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
def area(p): return abs(sum(p[k][0] * p[(k + 1) % len(p)][1] - p[(k + 1) % len(p)][0] * p[k][1] for k in range(len(p)))) / 2
def zoom_for(box, zmax=8.0, fw=760, fh=820):
    return max(1.0, min(zmax, fw / max((box[2] - box[0]) * S0, 1), fh / max((box[3] - box[1]) * S0, 1)))
def wc(mx, my): return mx * S0, MY + my * S0
def campos(cx_m, cy_m, z):
    cx, cy = wc(cx_m, cy_m); return FX - z * cx, FY - z * cy
def screen(mx, my, cx_m, cy_m, z):
    x, y = campos(cx_m, cy_m, z); sx, sy = wc(mx, my); return x + z * sx, y + z * sy

SHOTS = []   # (t, cx, cy, z) – harte Schnitte; danach leichtes Hineindriften bis zum nächsten Schnitt
def shot(t, box=None, center=None, z=None, zmax=8.0):
    if center is None: center = ((box[0] + box[2]) / 2, (box[1] + box[3]) / 2)
    if z is None: z = zoom_for(box, zmax)
    SHOTS.append((round(t, 2), center[0], center[1], z))
    return z

# ---------- Karte ----------
owned = {o["land"]: o for o in OWN}
JP_COL = "#b9c2cf"
paths = []
for cid, c in K.items():
    col = owned[cid]["farbe"] if cid in owned else (JP_COL if cid == "jp" else "#3a4a70")
    paths.append(f'<path id="c-{cid}" d="{c["path"]}" fill="{col}" stroke="#141c33" stroke-width="0.6" vector-effect="non-scaling-stroke"/>')

def flag(id_, mx, my, txt, col, z, op=0):
    s = 1 / z / S0; wd = 46 + 30 * len(txt)
    return (f'<g id="{id_}" opacity="{op}" transform="translate({mx:.2f} {my:.2f}) scale({s:.4f})"><g id="{id_}-in">'
            f'<path d="M0 0 V-150" stroke="#111" stroke-width="8"/><rect x="0" y="-150" width="{wd}" height="70" rx="12" fill="{col}" stroke="#111" stroke-width="6"/>'
            f'<text x="{wd/2:.0f}" y="-101" text-anchor="middle" style="font:900 46px Inter,sans-serif;fill:#111">{txt}</text>'
            f'<circle r="14" fill="#fff" stroke="#111" stroke-width="6"/></g></g>')

# Japan: Inseln (größte Polygone + Küstenpunkte) für den Inseln-Fakt
JP = polys("jp"); JPB = K["jp"]["bbox"]
JPC = ((JPB[0] + JPB[2]) / 2, (JPB[1] + JPB[3]) / 2)
Z_JP = zoom_for(JPB, 11.0)                           # Bild 0 / Loop
Z_JP3 = Z_JP * 1.18                                 # Nahaufnahme Inseln
random.seed(2)
pts = [(sum(p[0] for p in poly) / len(poly), sum(p[1] for p in poly) / len(poly)) for poly in sorted(JP, key=area, reverse=True) if len(poly) > 2]
allv = [v for poly in JP for v in poly]
pts += random.sample(allv, min(len(allv), 90 - min(90, len(pts)))) if len(pts) < 90 else []
pts = pts[:90]; random.shuffle(pts)
dots = "".join(f'<circle class="isl" id="d{k}" cx="{x:.2f}" cy="{y:.2f}" r="{6.5 / Z_JP3 / S0:.3f}" fill="#ffd166" stroke="#111" stroke-width="{1.6 / Z_JP3 / S0:.3f}" opacity="0"/>' for k, (x, y) in enumerate(pts))
# Honshu-Mitte für „DEIN NAME?“-Fahne
jbig = max(JP, key=area); hx = sum(p[0] for p in jbig) / len(jbig); hy = sum(p[1] for p in jbig) / len(jbig)
Z_JP4 = Z_JP * .85
dein = flag("p-dein", hx, hy, "DEIN NAME?", "#ffffff", Z_JP4)

# Russland: Punkt für Globi-Fahne + 11 Uhren quer über das Land
RU = polys("ru"); RUB = K["ru"]["bbox"]
RU_BOX = [560, 50, 1005, 300]; Z_RU = zoom_for(RU_BOX, 3)
def inner_y(x, want):
    for d in range(0, 140):
        for yy in (want + d, want - d):
            if inside(RU, x, yy) and inside(RU, x + 6, yy) and inside(RU, x - 6, yy) and inside(RU, x, yy + 6) and inside(RU, x, yy - 6): return yy
    return want
RUF = (760, inner_y(760, 150))
CLOCKS = [(x, inner_y(x, 175 if x < 900 else 150)) for x in [575 + k * 41 for k in range(11)]]
def clock(k, x, y, z):
    s = 1 / z / S0; a = (k * 30) % 360
    return (f'<g id="ck{k}" opacity="0" transform="translate({x:.2f} {y:.2f}) scale({s:.4f})"><g id="ck{k}-in">'
            f'<circle r="30" fill="#fff" stroke="#111" stroke-width="6"/>'
            f'<path d="M0 0 L0 -20" stroke="#111" stroke-width="6" stroke-linecap="round" transform="rotate({a})"/>'
            f'<path d="M0 0 L0 -13" stroke="#e63946" stroke-width="6" stroke-linecap="round" transform="rotate({(a * 12) % 360 + 90})"/>'
            f'<text y="58" text-anchor="middle" style="font:900 26px Inter,sans-serif;fill:#fff;stroke:#111;stroke-width:6px;paint-order:stroke">{k + 1}</text></g></g>')
clocks = "".join(clock(k, x, y, Z_RU) for k, (x, y) in enumerate(CLOCKS))
gflag = flag("p-globi", RUF[0], RUF[1], "GLOBI", GLOBI_COL, Z_RU)

# Besitzer-Fahnen: Größe passend zur Rundflug-Nahaufnahme, nur im eigenen Schnitt sichtbar
ZO = {}; pins = ""
for o in OWN:
    box = o.get("fokus") or K[o["land"]]["bbox"]; ZO[o["land"]] = zoom_for(box, 8.0)
    x0, y0, x1, y1 = box
    pins += flag(f'p-{o["land"]}', (x0 + x1) / 2, (y0 + y1) / 2, o["name"], o["farbe"], ZO[o["land"]])

MAP = (f'<g id="cam"><rect x="-6000" y="-6000" width="14000" height="14000" fill="#0e3a66"/>'
       f'<g transform="translate(0 {MY}) scale({S0:.5f})">{"".join(paths)}{dots}{clocks}{pins}{dein}{gflag}</g></g>')

# ---------- Schnittliste ----------
t_s2b = w("s2", "nur")
shot(0, center=JPC, z=Z_JP)                                                     # Bild 0: Japan FREI
shot(st("s2"), center=(JPC[0] - 34, JPC[1] + 4), z=Z_JP * .62)                  # Abo-Box links neben Japan
shot(t_s2b - .05, center=(JPC[0] - 22, JPC[1] + 2), z=Z_JP * .8)                # Punch-in
shot(st("s3"), center=(JPC[0] + 2, JPC[1] - 3), z=Z_JP3)                         # Nahaufnahme Inseln
shot(w("s3", "vierzehntausendeinhundertfünfundzwanzig") - .05, center=(JPC[0] - 4, JPC[1] + 2), z=Z_JP3 * 1.1)
t_dop = w("s3", "Doppelt")
shot(t_dop - .05, center=(JPC[0] + 6, JPC[1] + 6), z=Z_JP3 * 1.25)              # noch näher
shot(st("s4"), center=(hx + 6, hy - 10), z=Z_JP4)                                # Fahne DEIN NAME?
t_s4b = w("s4", "bekommt")
shot(t_s4b - .05, center=(hx + 4, hy - 14), z=Z_JP4 * 1.3)
RUND = [("ca", "Kanada"), ("br", "Brasilien"), ("de", "Deutschland"), ("us", "USA"), ("au", "Australien")]
TR = {}
for cid, word in RUND:
    o = owned[cid]; box = o.get("fokus") or K[cid]["bbox"]
    t = w("s5", word) - .1 if word != "Kanada" else st("s5")
    TR[cid] = t; shot(t, box=box, zmax=8.0)
shot(st("s6"), box=RU_BOX, zmax=3)                                               # Alarm Russland
t_frueh = w("s7", "Frühstückt")
shot(st("s7"), center=(785, 175), z=Z_RU * 1.08)                                 # Uhren
shot(w("s7", "elf") - .05, center=(800, 165), z=Z_RU * 1.25)
shot(t_frueh - .05, center=(785, 175), z=Z_RU * 1.08)                            # Split (Karte darunter)
shot(w("s7", "neun") - .05, center=(785, 175), z=Z_RU * 1.15)                 # Punch-in auf den Split
shot(st("s8"), center=(RUF[0], RUF[1] + 20), z=Z_RU * 1.5)                       # Globi sitzt auf Russland
t_kom8 = w("s8", "Kommentier")
shot(t_kom8 - .05, center=(RUF[0] + 10, RUF[1] + 25), z=Z_RU * 1.9)
shot(st("s9"), center=(505, 333), z=1.0)                                         # ganze Welt
t_noch = w("s9", "Noch")
shot(t_noch - .05, center=(560, 300), z=1.35)
t_abo10 = w("s10", "Abonnier")
t_nur10 = w("s10", "nur")
shot(st("s10"), center=JPC, z=Z_JP)                                              # Loop: wie Bild 0
shot(t_abo10 - .05, center=(JPC[0] - 4, JPC[1] + 4), z=Z_JP * 1.12)
shot(t_nur10 - .05, center=JPC, z=Z_JP)                                          # letzte Einstellung = Bild 0
SHOTS.sort()
CUTS = []
for k, (t, cx, cy, z) in enumerate(SHOTS):
    t1 = SHOTS[k + 1][0] if k + 1 < len(SHOTS) else END
    last = k + 1 == len(SHOTS)
    drift = 1.0 if (last or t == 0) else 1.05      # Loop-Bild bleibt ruhig, sonst leichtes Hineindriften
    x, y = campos(cx, cy, z); x2, y2 = campos(cx, cy, z * drift)
    J.append(f'tl.set("#cam", {{ x: {x:.1f}, y: {y:.1f}, scale: {z:.3f} }}, {F(t)});')
    if drift != 1.0: J.append(f'tl.to("#cam", {{ x: {x2:.1f}, y: {y2:.1f}, scale: {z * drift:.3f}, duration: {t1 - t:.2f}, ease: "none" }}, {F(t)});')
    if t > 0: CUTS.append(t)
J.insert(0, 'tl.set("#cam", { svgOrigin: "0 0" }, 0);')

# ---------- Ereignisse auf der Karte ----------
def blink_jp(t0, t1):
    J.append(f'tl.fromTo("#c-jp", {{ fill: "{JP_COL}" }}, {{ fill: "#ffffff", duration: .22, yoyo: true, repeat: {max(1, int((t1 - t0) / .22) // 2 * 2 - 1)}, ease: "steps(1)", immediateRender: false }}, {F(t0)});')
    J.append(f'tl.set("#c-jp", {{ fill: "{JP_COL}" }}, {F(t1)});')
blink_jp(0, st("s2")); blink_jp(st("s10"), END)
# Inselpunkte ploppen auf (s3), werden danach ausgeblendet
t3a, t3b = st("s3") + .2, w("s3", "Inseln.") + .2
for k in range(len(pts)):
    tk = t3a + (t3b - t3a) * k / len(pts)
    J.append(f'tl.set("#d{k}", {{ opacity: 1 }}, {F(tk)});')
J.append(f'tl.set(".isl", {{ opacity: 0 }}, {F(st("s4"))});')
# DEIN NAME?-Fahne (s4) wackelt
J.append(f'tl.set("#p-dein", {{ opacity: 1 }}, {F(st("s4"))}); tl.fromTo("#p-dein-in", {{ scale: 0, transformOrigin: "0px 0px" }}, {{ scale: 1, duration: .35, ease: "back.out(2.5)" }}, {F(st("s4"))});')
J.append(f'tl.fromTo("#p-dein-in", {{ rotation: -6 }}, {{ rotation: 6, duration: .25, yoyo: true, repeat: {int((en("s4") - st("s4") - .4) / .25)}, ease: "sine.inOut", transformOrigin: "0px 0px" }}, {F(st("s4") + .35)});')
J.append(f'tl.set("#p-dein", {{ opacity: 0 }}, {F(en("s4"))});')
# Rundflug-Fahnen
cids = [c for c, _ in RUND]
for j, cid in enumerate(cids):
    t0 = TR[cid]; t1 = TR[cids[j + 1]] if j + 1 < len(cids) else st("s6")
    J.append(f'tl.set("#p-{cid}", {{ opacity: 1 }}, {F(t0)}); tl.fromTo("#p-{cid}-in", {{ scale: 0, transformOrigin: "0px 0px" }}, {{ scale: 1, duration: .3, ease: "back.out(2.5)" }}, {F(t0 + .05)});')
    J.append(f'tl.set("#p-{cid}", {{ opacity: 0 }}, {F(t1)});')
# Globi schnappt sich Russland (s6)
t_globi = w("s6", "Globi"); t_ru = w("s6", "Russland!")
J.append(f'tl.to("#c-ru", {{ fill: "{GLOBI_COL}", duration: .3 }}, {F(t_ru)});')
J.append(f'tl.set("#p-globi", {{ opacity: 1 }}, {F(t_ru - .15)}); tl.fromTo("#p-globi-in", {{ scale: 0, transformOrigin: "0px 0px" }}, {{ scale: 1, duration: .3, ease: "back.out(3)" }}, {F(t_ru - .15)});')
J.append(f'tl.set("#p-globi", {{ opacity: 0 }}, {F(st("s7"))}); tl.set("#p-globi", {{ opacity: 1 }}, {F(st("s8"))}); tl.set("#p-globi", {{ opacity: 0 }}, {F(st("s9"))});')
# 11 Uhren (s7)
t_elf = w("s7", "elf")
for k in range(11):
    tk = st("s7") + .25 + (t_elf + .5 - st("s7") - .25) * k / 10
    J.append(f'tl.set("#ck{k}", {{ opacity: 1 }}, {F(tk)}); tl.fromTo("#ck{k}-in", {{ scale: 0 }}, {{ scale: 1, duration: .2, ease: "back.out(3)" }}, {F(tk)});')
J.append(f'tl.set("[id^=ck]", {{ opacity: 0 }}, {F(t_frueh - .05)});')
# s9: freie Länder blitzen bei „Noch … frei“
random.seed(9)
free = [c for c in K if c not in owned and c not in ("ru", "jp") and K[c]["bbox"][2] - K[c]["bbox"][0] > 10]
used = set(); t = t_noch + .05
while t < en("s9") - .2:
    cid = random.choice(free); used.add(cid)
    J.append(f'tl.fromTo("#c-{cid}", {{ fill: "#3a4a70" }}, {{ fill: "#ffffff", duration: .1, yoyo: true, repeat: 1, immediateRender: false }}, {F(t)});')
    t += .07
for cid in used: J.append(f'tl.set("#c-{cid}", {{ fill: "#3a4a70" }}, {F(en("s9"))});')

# ---------- HTML-Ebenen ----------
def ui(id_, t0, t1, inner, style): return f'<div id="{id_}" class="ui clip" data-start="{F(t0)}" data-duration="{F(max(.05, t1 - t0))}" style="{style}">{inner}</div>\n'
def chip(id_, txt, bg="#fff", fg="#111", size=44):
    return f'<div id="{id_}" style="display:inline-block;max-width:1000px;background:{bg};color:{fg};font:900 {size}px/1.12 Inter,sans-serif;padding:12px 26px;border-radius:18px;border:5px solid #111;box-shadow:0 8px 0 #111">{txt}</div>'
html = ""
HEAD = [("s1", "WER BEKOMMT JAPAN?", 78, None), ("s2", "NUR ABONNENTEN BEKOMMEN EIN LAND", 60, None),
        ("s3", "14.125 INSELN", 84, "Quelle: GSI Japan (2023)"), ("s4", "WER ZUERST ABONNIERT + „JAPAN“ KOMMENTIERT", 54, None),
        ("s5", "BESITZER: " + " · ".join(o["name"] for o in OWN), 46, None), ("s6", "ALARM! GLOBI KLAUT RUSSLAND", 62, None),
        ("s7", "11 ZEITZONEN", 84, "Quelle: bpb"), ("s8", "HOLT ES ZURÜCK!", 84, None),
        ("s9", f"{NOWN}/{TOTAL} VERGEBEN – NOCH {FREI} FREI", 48, None), ("s10", "WER BEKOMMT JAPAN?", 78, None)]
for sid, txt, size, src in HEAD:
    bg = "#e63946" if sid in ("s6", "s8") else "#ffd166"
    fg = "#fff" if sid in ("s6", "s8") else "#111"
    html += ui(f"h{sid}", st(sid), en(sid) if sid != "s10" else END, chip(f"h{sid}-in", txt, bg, fg, size), "left:30px;right:30px;top:110px;text-align:center")
    if sid not in ("s1", "s10"): J.append(f'tl.fromTo("#h{sid}-in", {{ scale: 1.35, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: .2, ease: "back.out(2)" }}, {F(st(sid))});')
    if src: html += ui(f"src{sid}", st(sid), en(sid), f'<div style="display:inline-block;background:rgba(0,0,0,.6);border-radius:10px;padding:4px 14px;font:700 28px Inter,sans-serif;color:#fff">{src}</div>', "left:40px;top:318px")
# Zähler oben rechts (außer s9, dort groß in der Mitte)
html += ui("cntA", 0, st("s9"), f'<div style="display:inline-block;background:rgba(0,0,0,.65);border-radius:14px;padding:6px 18px;font:900 44px Inter,sans-serif;color:#fff"><span style="color:#06d6a0">{NOWN}</span>/{TOTAL}</div>', "right:36px;top:306px")
html += ui("cntB", st("s10"), END, f'<div style="display:inline-block;background:rgba(0,0,0,.65);border-radius:14px;padding:6px 18px;font:900 44px Inter,sans-serif;color:#fff"><span style="color:#06d6a0">{NOWN}</span>/{TOTAL}</div>', "right:36px;top:306px")
# FREI!-Stempel auf Japan (s1 + s10, identisch)
def frei(id_, t0, t1):
    global html
    html += ui(id_, t0, t1, f'<div id="{id_}-in" style="display:inline-block;transform:rotate(-8deg);background:#fff;color:#e63946;font:900 110px/1 Inter,sans-serif;padding:10px 34px;border:10px solid #e63946;border-radius:22px;box-shadow:0 10px 0 #111">FREI!</div>', "left:0;right:0;top:1010px;text-align:center")
    J.append(f'tl.fromTo("#{id_}-in", {{ opacity: 1 }}, {{ opacity: .15, duration: .22, yoyo: true, repeat: {max(1, int((t1 - t0) / .22) // 2 * 2 - 1)}, ease: "steps(1)" }}, {F(t0 + .44)});')
frei("fr1", 0, st("s2")); frei("fr10", st("s10"), t_abo10 - .05); frei("fr10b", t_nur10 - .05, END)
# Abo-Banner (s1, s10) – gleiche Position wie Bild 0
ABO = (chip("{id}-a", "🔔 ABONNIER", "#e63946", "#fff", 60) + '<div style="height:16px"></div>' +
       chip("{id}-b", "💬 + KOMMENTIER DEIN WUNSCHLAND", "#fff", "#111", 42))
html += ui("ab1", 0, st("s2"), ABO.replace("{id}", "ab1"), "left:0;right:0;top:1290px;text-align:center")
html += ui("ab10", st("s10"), END, ABO.replace("{id}", "ab10"), "left:0;right:0;top:1290px;text-align:center")
J.append(f'tl.to("#ab10-a", {{ scale: 1.08, duration: .35, yoyo: true, repeat: {int((END - st("s10")) / .35) - 1}, ease: "sine.inOut" }}, {F(st("s10") + .2)});')
J.append(f'tl.to("#ab1-a", {{ scale: 1.08, duration: .35, yoyo: true, repeat: 3, ease: "sine.inOut" }}, .5);')
# s2: Abo-Box + Kommentar springen neben Japan auf
html += ui("abo2", st("s2"), en("s2"), chip("abo2-a", "🔔 ABONNIEREN", "#e63946", "#fff", 56) + '<div style="height:22px"></div>' +
           chip("abo2-b", "💬 „JAPAN!“", "#fff", "#111", 56), "left:50px;top:640px;width:520px;text-align:left")
J.append(f'tl.fromTo("#abo2-a", {{ scale: 0 }}, {{ scale: 1, duration: .3, ease: "back.out(2.5)" }}, {F(st("s2") + .05)}); tl.fromTo("#abo2-b", {{ scale: 0 }}, {{ scale: 1, duration: .3, ease: "back.out(2.5)" }}, {F(w("s2", "kommentier"))});')
# s3: Zähler bis 14.125
t_num = w("s3", "vierzehntausendeinhundertfünfundzwanzig")
html += ui("isn", st("s3") + .1, en("s3"), f'<div id="isn-in" style="display:inline-block;background:#fff;border:6px solid #111;border-radius:22px;box-shadow:0 10px 0 #111;padding:10px 34px;font:900 120px/1 Inter,sans-serif;color:#111"><span id="isn-v">0</span></div>', "left:0;right:0;top:1290px;text-align:center")
J.append(f'(() => {{ const o = {{ v: 0 }}; tl.fromTo(o, {{ v: 0 }}, {{ v: 14125, duration: {t3b - st("s3") - .2:.2f}, ease: "power1.out", onUpdate: () => {{ document.getElementById("isn-v").textContent = Math.round(o.v).toLocaleString("de-DE"); }} }}, {F(st("s3") + .15)}); }})();')
html += ui("x2", t_dop - .05, en("s3"), chip("x2-in", "×2 &nbsp;(1987: 6.852)", "#06d6a0", "#111", 54), "left:0;right:0;top:1120px;text-align:center")
J.append(f'tl.fromTo("#x2-in", {{ scale: 2.2, opacity: 0, rotation: -10 }}, {{ scale: 1, opacity: 1, rotation: -3, duration: .3, ease: "back.out(2)" }}, {F(t_dop - .05)});')
# s5: Land → Name
for j, cid in enumerate(cids):
    o = owned[cid]; t0 = TR[cid]; t1 = TR[cids[j + 1]] if j + 1 < len(cids) else en("s5")
    html += ui(f"rf{cid}", t0, t1, chip(f"rf{cid}-in", f'{o["land_de"]} → {o["name"]}', o["farbe"], "#111", 58), "left:0;right:0;top:1330px;text-align:center")
# s6: Alarm-Rahmen
html += ui("alarm", st("s6"), en("s6"), '<div id="alarm-in" style="position:absolute;inset:0;border:26px solid #e63946;box-shadow:inset 0 0 80px rgba(230,57,70,.8)"></div>', "left:0;top:0;width:1080px;height:1920px")
J.append(f'tl.fromTo("#alarm-in", {{ opacity: 1 }}, {{ opacity: 0, duration: .2, yoyo: true, repeat: {int((en("s6") - st("s6")) / .2) - 1}, ease: "steps(1)" }}, {F(st("s6"))});')
# s7: Split Moskau / ganz im Osten
t_neun = w("s7", "neun")
html += ui("splitL", t_frueh - .05, en("s7"),
           '<div style="position:absolute;inset:0;border-radius:26px;border:6px solid #111;overflow:hidden;background:linear-gradient(#ff9e6d,#ffd6a5 70%,#ffe8c9)">'
           '<div id="sun" style="position:absolute;left:150px;top:330px;width:190px;height:190px;border-radius:50%;background:#ffd166;box-shadow:0 0 60px #fff3b0"></div>'
           '<div style="position:absolute;left:0;right:0;bottom:0;height:200px;background:#7a5c4a"></div>'
           '<div style="position:absolute;left:0;right:0;top:26px;text-align:center;font:900 52px Inter,sans-serif;color:#111">MOSKAU</div>'
           '<div style="position:absolute;left:0;right:0;top:92px;text-align:center;font:900 110px/1 Inter,sans-serif;color:#111">7:00</div>'
           '<div style="position:absolute;right:30px;bottom:150px;font-size:90px">🥐☕</div></div>', "left:30px;top:470px;width:500px;height:760px")
html += ui("splitR", t_frueh + .35, en("s7"),
           '<div style="position:absolute;inset:0;border-radius:26px;border:6px solid #111;overflow:hidden;background:linear-gradient(#4f8fd8,#9cc9f0)">'
           '<div style="position:absolute;left:0;right:0;bottom:0;height:200px;background:#3d6b4f"></div>'
           '<div style="position:absolute;left:0;right:0;top:26px;text-align:center;font:900 46px Inter,sans-serif;color:#111">GANZ IM OSTEN</div>'
           '<div style="position:absolute;left:0;right:0;top:92px;text-align:center;font:900 110px/1 Inter,sans-serif;color:#111">16:00</div>'
           '<svg viewBox="-60 -60 120 120" width="230" height="230" style="position:absolute;left:135px;top:300px"><circle r="52" fill="#fff" stroke="#111" stroke-width="7"/>'
           '<path d="M0 0 V-38" stroke="#111" stroke-width="6" stroke-linecap="round"/><path d="M0 0 L-24 0" stroke="#111" stroke-width="8" stroke-linecap="round"/></svg></div>', "left:550px;top:470px;width:500px;height:760px")
J.append(f'tl.set(["#splitL", "#splitR"], {{ scale: 1.05, transformOrigin: "50% 50%" }}, {F(t_neun - .05)});')
J.append(f'tl.fromTo("#sun", {{ y: 160 }}, {{ y: 0, duration: 1.6, ease: "power2.out" }}, {F(t_frueh)});')
html += ui("p9", t_neun - .05, en("s7"), chip("p9-in", "+9 STUNDEN", "#e63946", "#fff", 70), "left:0;right:0;top:1270px;text-align:center")
J.append(f'tl.fromTo("#p9-in", {{ scale: 2.4, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: .25, ease: "back.out(2)" }}, {F(t_neun - .05)});')
# s8: Kommentar-Bubble
html += ui("ru8", t_kom8 - .05, en("s8"), chip("ru8-in", "💬 „RUSSLAND!“", "#fff", "#111", 60), "left:0;right:0;top:1330px;text-align:center")
J.append(f'tl.fromTo("#ru8-in", {{ scale: 0 }}, {{ scale: 1, duration: .3, ease: "back.out(2.5)" }}, {F(t_kom8 - .05)});')
# s9: Zähler groß in der Mitte
html += ui("big9", st("s9") + .15, en("s9"),
           f'<div id="big9-in" style="display:inline-block;background:rgba(11,26,51,.85);border:6px solid #fff;border-radius:28px;padding:16px 40px">'
           f'<div style="font:900 170px/1 Inter,sans-serif;color:#fff"><span style="color:#06d6a0">{NOWN}</span>/{TOTAL}</div>'
           f'<div id="nf9" style="font:900 64px/1.1 Inter,sans-serif;color:#ffd166;margin-top:8px">NOCH {FREI} FREI!</div></div>', "left:0;right:0;top:1230px;text-align:center")
J.append(f'tl.fromTo("#big9-in", {{ scale: 0, y: -500 }}, {{ scale: 1, y: 0, duration: .4, ease: "back.out(1.8)" }}, {F(st("s9") + .15)});')
J.append(f'tl.fromTo("#nf9", {{ opacity: 0 }}, {{ opacity: 1, duration: .1 }}, {F(t_noch)}); tl.fromTo("#nf9", {{ scale: 1.5 }}, {{ scale: 1, duration: .3, ease: "back.out(2)" }}, {F(t_noch)});')
# Weißer Blitz bei jedem harten Schnitt (kurz, unterstützt den Schnitt)
for k, t in enumerate(CUTS):
    html += ui(f"fl{k}", t, t + .12, f'<div id="fl{k}-in" style="position:absolute;inset:0;background:#fff"></div>', "left:0;top:0;width:1080px;height:1920px")
    J.append(f'tl.fromTo("#fl{k}-in", {{ opacity: .45 }}, {{ opacity: 0, duration: .12 }}, {F(t)});')

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
GK = lambda k, X, Y: (X - 190 * k, Y - 490 * k)        # Füße auf Bildpunkt (X, Y)
GEST = [(st("s2") + .05, en("s2") - st("s2") - .2, "point"), (t_ru - .1, 1.2, "both"), (st("s7") + .2, 1.2, "point"),
        (st("s8"), en("s8") - st("s8"), "both")]
gh = globi.build({}, END, GEST, left=0, top=0)
gh = gh.replace('<g id="g-brow">', '<g id="g-tongue" style="display:none"><path d="M204 206 Q220 252 236 206 Z" fill="#ff6b81" stroke="#111" stroke-width="5"/></g><g id="g-brow">', 1)
def gset(t, k, X, Y, op=1, rot=0): x, y = GK(k, X, Y); GJ.append(f'tl.set("#g-wrap", {{ x: {x:.0f}, y: {y:.0f}, scale: {k}, rotation: {rot}, opacity: {op} }}, {F(t)});')
def gto(t, d, k, X, Y, rot=0, ease="power2.out"): x, y = GK(k, X, Y); GJ.append(f'tl.to("#g-wrap", {{ x: {x:.0f}, y: {y:.0f}, scale: {k}, rotation: {rot}, duration: {d}, ease: "{ease}" }}, {F(t)});')
GJ.append('tl.set("#g-wrap", { transformOrigin: "0 0", opacity: 0 }, 0);')
gset(st("s2"), .55, 220, 1240); GJ.append(f'tl.fromTo("#g-wrap", {{ y: "+=300" }}, {{ y: "-=300", duration: .3, ease: "back.out(2)", immediateRender: false }}, {F(st("s2"))});')
gset(st("s3"), .55, 220, 1240, op=0)
# s6: Globi saust von links über die Karte nach Russland
RX, RY = screen(RUF[0], RUF[1], (RU_BOX[0] + RU_BOX[2]) / 2, (RU_BOX[1] + RU_BOX[3]) / 2, Z_RU)
gset(t_globi - .25, .5, -260, 1150, rot=-25)
gto(t_globi - .25, max(.3, t_ru - t_globi + .1), .5, RX - 40, RY + 10, rot=0, ease="power3.out")
# s7: Globi beim Frühstück (links im Split)
gset(st("s7"), .42, 170, 1130, op=0); gset(t_frueh + .05, .42, 170, 1130)
# s8: Globi groß auf Russland, Zunge raus
z8 = Z_RU * 1.5; X8, Y8 = screen(RUF[0] + 30, RUF[1] + 18, RUF[0], RUF[1] + 20, z8)
gset(st("s8"), .85, 600, 1250)
GJ.append(f'tl.fromTo("#g-wrap", {{ rotation: -4 }}, {{ rotation: 4, duration: .3, yoyo: true, repeat: {int((en("s8") - st("s8")) / .3) - 1}, ease: "sine.inOut" }}, {F(st("s8"))});')
GJ.append(f'tl.set("#g-tongue", {{ display: "inline" }}, {F(st("s8") + .15)}); tl.set("#g-tongue", {{ display: "none" }}, {F(en("s8"))});')
gset(st("s9"), .5, -400, 1200, op=0)
gh = gh.replace('window.__timelines["globi"] = tl;', "\n      ".join(GJ) + '\n      window.__timelines["globi"] = tl;')
open("compositions/globi.html", "w", encoding="utf-8").write(gh)

# ---------- Untertitel ----------
HOT = {o["name"] for o in OWN} | {norm(o["land_de"]).upper() for o in OWN} | {"JAPAN", "RUSSLAND", "ABONNIER", "ABONNIERT", "ABONNENTEN", "GLOBI", "FREI", "14.125", "11", "9", "5", "195", "190", "WUNSCHLAND", "INSELN"}
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
    te = min(caps[j + 1][0] if j + 1 < len(caps) else END, t0 + 1.3)
    up = d.upper()
    col = "#ffd166" if re.sub(r"[!?.,:–]", "", up) in HOT else "#fff"
    fs = min(96, int(1500 / max(1, len(up))))
    items.append(f'<div id="w{j}" class="wd clip" data-start="{F(t0)}" data-duration="{F(max(.15, te - t0 - .02))}"><span id="w{j}-in" style="color:{col};font-size:{fs}px">{up}</span></div>')
    cj.append(f'tl.fromTo("#w{j}-in", {{ scale: 1.2, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: .08 }}, {F(t0)});' if t0 > .05 else "")
open("compositions/caps.html", "w", encoding="utf-8").write(f'''<template>
  <style>#root {{ position: absolute; inset: 0; }} .wd {{ position: absolute; left: 0; right: 0; top: 1640px; text-align: center; }}
    .wd span {{ display: inline-block; font: 900 96px/1 Inter, sans-serif; white-space: nowrap; -webkit-text-stroke: 14px #000; paint-order: stroke fill; }}</style>
  <div id="root" data-composition-id="caps" data-width="1080" data-height="1920">{"".join(items)}</div>
  <script>(function () {{ const tl = gsap.timeline({{ paused: true }}); {" ".join(cj)} window.__timelines["caps"] = tl; }})();</script>
</template>
''')

# ---------- Ton (fester Hintergrund-Sound über story_musik.py → assets/bgm.mp3) ----------
subprocess.run([sys.executable, "tools/story_musik.py", F(END), "1", "2", "3"], check=True)
FXL = [("pop", 0.0, .5, .15), ("pop", .45, .35, .15)]
for t in CUTS: FXL.append(("swoosh", t - .05, .35, .5))
FXL += [("pop", st("s2") + .05, .5, .15), ("pop", w("s2", "kommentier"), .5, .15)]
FXL += [("tick", st("s3") + .2, .25, min(1.67, t3b - st("s3")))]
FXL += [("boing", t_dop - .05, .4, .55), ("boing", st("s4") + .05, .35, .55)]
for cid in cids: FXL.append(("pop", TR[cid] + .05, .5, .15))
FXL += [("glitch", st("s6") + .02, .12, .5), ("whoosh", t_globi - .25, .7, .94), ("hit", t_ru - .1, .45, 1.6)]
FXL += [("blips", st("s7") + .25, .3, 1.33), ("chime", t_frueh, .3, 1.4), ("klong", t_neun - .05, .35, 1.2)]
FXL += [("boing", st("s8") + .15, .45, .55), ("pop", t_kom8 - .05, .5, .15)]
FXL += [("hit", st("s9") + .15, .4, 1.6), ("blips", t_noch, .3, 1.33)]
FXL += [("pop", st("s10"), .5, .15)]
Hh = lambda id_, ti: f'      <div id="{id_}" data-composition-id="{id_}" data-composition-src="compositions/{id_}.html" data-start="0" data-duration="{F(END)}" data-track-index="{ti}" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index:{ti}"></div>'
lines = [Hh("welt", 2), Hh("caps", 3), Hh("globi", 6), f'      <audio id="musik" class="clip" data-start="0" data-duration="{F(END)}" data-track-index="5" data-volume="0.2" src="assets/musik.wav"></audio>']
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
