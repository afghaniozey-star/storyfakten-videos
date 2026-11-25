"""ABO-WELT Tag 3 (YouTube) – EREIGNIS-Tag „Krone fürs größte Reich“ (keine neuen Besitzer).
Flächen-Ranking der echten Besitzer aus welt.json (Platz 5 → 3), Fotofinish USA vs. Kanada mit Balken,
Krone + Konfetti für Kanada, Twist: Globi (Maskottchen, kein Abonnent) sitzt auf Russland (größer),
„Holt euch die Krone!“, Japan blinkt FREI!, Zähler 5/195, Loop-Ende = Bild 0 (Nordamerika + Krone „?“).
Untertitel/Schilder zwischen 55 und 72 % Bildhöhe, Wortwechsel hart (keine Überblendung).
Aufruf (im Projektordner): /usr/bin/python3 tools/abowelt_tag3.py
liest welt.json, daten.json (Beispiel: daten-tag3.json) (Flächen/Fakten), voice.json, assets/vo/timing.json, weltkarte.json
Karte: @svg-maps/world (CC BY 4.0) → in der Beschreibung „Karte: svg-maps (CC BY 4.0)“ nennen.
Fläche: CIA World Factbook (Gesamtfläche)."""
import json, re, subprocess, sys, random
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
RANK = {r["land"]: r for r in D["reihenfolge"]}
assert set(RANK) == set(owned), "Datendatei passt nicht zu welt.json"
GLOBI_COL = "#ff8a3d"; JP_COL = "#ffffff"
S0, MY = 1080 / 1010, 560          # Kartenmaßstab, Karten-Oberkante
FX, FY = 540, 690                   # Bildpunkt, auf den die Kamera zentriert (Karte oberhalb der Untertitel)
J, GJ = [], []
de_num = lambda n: f"{n:,}".replace(",", ".")

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
def zoom_for(box, zmax=8.0, fw=820, fh=560):
    return max(1.0, min(zmax, fw / max((box[2] - box[0]) * S0, 1), fh / max((box[3] - box[1]) * S0, 1)))
def wc(mx, my): return mx * S0, MY + my * S0
def campos(cx_m, cy_m, z):
    cx, cy = wc(cx_m, cy_m); return FX - z * cx, FY - z * cy
def screen(mx, my, cx_m, cy_m, z):
    x, y = campos(cx_m, cy_m, z); sx, sy = wc(mx, my); return x + z * sx, y + z * sy
ctr = lambda b: ((b[0] + b[2]) / 2, (b[1] + b[3]) / 2)

SHOTS = []   # (t, cx, cy, z, drift)
def shot(t, box=None, center=None, z=None, zmax=8.0, drift=1.05):
    if center is None: center = ctr(box)
    if z is None: z = zoom_for(box, zmax)
    SHOTS.append((round(t, 2), center[0], center[1], z, drift)); return z

# ---------- Karte ----------
paths = []
for cid, c in K.items():
    col = owned[cid]["farbe"] if cid in owned else (JP_COL if cid == "jp" else ("#3a4a70"))
    if cid == "ru": col = GLOBI_COL       # Globi sitzt seit Tag 2 auf Russland
    paths.append(f'<path id="c-{cid}" d="{c["path"]}" fill="{col}" stroke="#141c33" stroke-width="0.6" vector-effect="non-scaling-stroke"/>')

def flag(id_, mx, my, txt, col, z, k=1.0, op=0):
    s = k / z / S0; wd = 46 + 30 * len(txt)
    return (f'<g id="{id_}" opacity="{op}" transform="translate({mx:.2f} {my:.2f}) scale({s:.4f})"><g id="{id_}-in">'
            f'<path d="M0 0 V-150" stroke="#111" stroke-width="8"/><rect x="0" y="-150" width="{wd}" height="70" rx="12" fill="{col}" stroke="#111" stroke-width="6"/>'
            f'<text x="{wd/2:.0f}" y="-101" text-anchor="middle" style="font:900 46px Inter,sans-serif;fill:#111">{txt}</text>'
            f'<circle r="14" fill="#fff" stroke="#111" stroke-width="6"/></g></g>')

NA = [70, 12, 330, 410]; Z_NA = zoom_for(NA, 4)            # Nordamerika: Kanada + USA (Bild 0 / Loop)
Z0 = Z_NA * 1.08                                           # Punch-Zoom 108 % → 100 %
WORLD_C, Z_W = (505, 300), 1.3
RU_BOX = [560, 50, 1005, 300]; Z_RU = zoom_for(RU_BOX, 3)
RU = polys("ru")
def inner_y(x, want):
    for d in range(0, 140):
        for yy in (want + d, want - d):
            if all(inside(RU, x + dx, yy + dy) for dx, dy in ((0, 0), (6, 0), (-6, 0), (0, 6), (0, -6))): return yy
    return want
RUF = (760, inner_y(760, 150))
JPB = K["jp"]["bbox"]; JPC = ctr(JPB); Z_JP = zoom_for(JPB, 9.0)
JP = polys("jp"); jbig = max(JP, key=lambda p: len(p)); hx = sum(p[0] for p in jbig) / len(jbig); hy = sum(p[1] for p in jbig) / len(jbig)

FOC = {o["land"]: (o.get("fokus") or K[o["land"]]["bbox"]) for o in OWN}
CANADA_PT = (215, 150); US_PT = (215, 340)                 # Fahnen-Punkte (Kanada Mitte, USA Mitte ohne Alaska)
PT = {cid: ctr(FOC[cid]) for cid in owned}; PT["ca"] = CANADA_PT; PT["us"] = US_PT
ZO = {cid: zoom_for(FOC[cid], 6.0) for cid in owned}
pins = ""
for o in OWN:
    cid = o["land"]
    pins += flag(f'p-{cid}', *PT[cid], o["name"], o["farbe"], ZO[cid])                 # eigene Nahaufnahme
    pins += flag(f'pw-{cid}', *PT[cid], o["name"], o["farbe"], Z_W, k=.62)             # Weltansicht
for cid in ("ca", "us"):
    o = owned[cid]; pins += flag(f'pn-{cid}', *PT[cid], o["name"], o["farbe"], Z_NA, k=.9)   # Nordamerika
pins += flag("p-globi", RUF[0], RUF[1], "GLOBI", GLOBI_COL, Z_RU)
pins += flag("pw-globi", RUF[0], RUF[1], "GLOBI", GLOBI_COL, 1.0, k=.62)
pins += flag("p-dein", hx, hy, "DEIN NAME?", "#ffffff", Z_JP * .8)
# Australien-Kopie für „ein ganzes Australien mehr“ (fliegt auf Russland)
AUC = ctr(K["au"]["bbox"]); RUC = (780, 175)
aucl = f'<g id="auclone" opacity="0"><path d="{K["au"]["path"]}" fill="{owned["au"]["farbe"]}" fill-opacity=".9" stroke="#fff" stroke-width="2.5" vector-effect="non-scaling-stroke"/></g>'
MAP = (f'<g id="cam"><rect x="-6000" y="-6000" width="14000" height="14000" fill="#0e3a66"/>'
       f'<g transform="translate(0 {MY}) scale({S0:.5f})">{"".join(paths)}{aucl}{pins}</g></g>')

# ---------- Schnittliste ----------
ORDER = ["de", "au", "br"]; SC = {"de": "s3", "au": "s4", "br": "s5"}
TB = {}
shot(0, center=ctr(NA), z=Z0, drift=1.0)                                      # Bild 0 (Zoom 108→100 % separat)
t_cut1 = min(1.4, w("s1", "Heute") - .05)
shot(t_cut1, center=WORLD_C, z=Z_W)                                           # erster Schnitt ≤ 1,5 s: alle Reiche
shot(w("s1", "Krone!") - .05, center=(WORLD_C[0] - 20, WORLD_C[1] - 30), z=Z_W * 1.15)
shot(st("s2"), center=(JPC[0] - 30, JPC[1] + 2), z=Z_JP * .62)                # Japan + Abo-Box
t_kom2 = w("s2", "kommentier"); t_nur2 = w("s2", "nur")
shot(t_kom2 - .05, center=(JPC[0] - 24, JPC[1] + 2), z=Z_JP * .72)
shot(t_nur2 - .05, center=(JPC[0] - 18, JPC[1]), z=Z_JP * .85)
for cid in ORDER:
    s = SC[cid]; word = "Rund" if cid == "de" else "Über"
    shot(st(s), box=FOC[cid], zmax=6.0)
    TB[cid] = w(s, word)
    c = ctr(FOC[cid]); shot(TB[cid] - .05, center=(c[0], c[1] + 4), z=ZO[cid] * 1.18)
t_liam = w("s6", "Liam"); t_finny6 = w("s6", "Finny!")
shot(st("s6"), center=ctr(NA), z=Z_NA)
shot(t_liam - .05, center=US_PT, z=Z_NA * 1.35)
shot(t_finny6 - .05, center=CANADA_PT, z=Z_NA * 1.35)
shot(t_finny6 + .65, center=ctr(NA), z=Z_NA * .95, drift=1.12)                 # Trommelwirbel: langsamer Zoom
t_ca7 = w("s7", "Kanada:")
shot(st("s7"), center=ctr(NA), z=Z_NA * .9)                                   # Balken-Fotofinish
shot(t_ca7 - .05, center=ctr(NA), z=Z_NA)
t_ca8 = w("s8", "Kanada"); t_seen = w("s8", "Seen."); t_ohne = w("s8", "Ohne")
shot(st("s8"), center=CANADA_PT, z=Z_NA * 1.15)                              # Krone + Konfetti
shot(t_ca8 - .05, center=(CANADA_PT[0], CANADA_PT[1] + 8), z=Z_NA * 1.35)
shot(t_seen - .05, center=(250, 230), z=Z_NA * 1.8)                          # Seen-Gebiet
shot(t_ohne - .05, center=US_PT, z=Z_NA * 1.4)
t_globi9 = w("s9", "Globi")
shot(st("s9"), center=ctr(NA), z=Z_NA * 1.1)                                  # „Aber Moment“ (Glitch auf Kanada)
shot(t_globi9 - .05, box=RU_BOX, zmax=3)
t_fast = w("s10", "Fast")
shot(st("s10"), center=(RUF[0], RUF[1] + 10), z=Z_RU * 1.25)                 # 17 Millionen
shot(t_fast - .05, center=(560, 250), z=1.0)                                  # Welt: Australien fliegt auf Russland
t_kom11 = w("s11", "Kommentier")
shot(st("s11"), center=(RUF[0], RUF[1] + 20), z=Z_RU * 1.5)                  # Globi mit Krone
shot(t_kom11 - .05, center=(RUF[0] + 10, RUF[1] + 25), z=Z_RU * 1.85)
t_imm12 = w("s12", "immer")
shot(st("s12"), center=(JPC[0] + 9, JPC[1]), z=Z_JP)                                           # Japan FREI
shot(t_imm12 - .05, center=(JPC[0] + 12, JPC[1] - 2), z=Z_JP * 1.12)
t_land13 = w("s13", "Länder")
shot(st("s13"), center=(505, 333), z=1.0)                                     # ganze Welt + Zähler
shot(t_land13 - .05, center=(560, 300), z=1.3)
t_kom14 = w("s14", "kommentier"); t_nur14 = w("s14", "nur")
shot(st("s14"), center=CANADA_PT, z=Z_NA * 1.3)
shot(t_kom14 - .05, center=ctr(NA), z=Z_NA * 1.4)
LOOP_T = t_nur14 - .05
SHOTS.append((round(LOOP_T, 2), ctr(NA)[0], ctr(NA)[1], Z_NA * 1.3, "loop"))  # fährt bis END zurück auf Bild 0
SHOTS.sort(key=lambda s: s[0])
CUTS = []
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
J.insert(0, 'tl.set("#cam", { svgOrigin: "0 0" }, 0);')

# ---------- Ereignisse auf der Karte ----------
def show(id_, t0, t1, popd=.3):
    J.append(f'tl.set("#{id_}", {{ opacity: 1 }}, {F(t0)}); tl.fromTo("#{id_}-in", {{ scale: 0, transformOrigin: "0px 0px" }}, {{ scale: 1, duration: {popd}, ease: "back.out(2.5)" }}, {F(t0)});')
    J.append(f'tl.set("#{id_}", {{ opacity: 0 }}, {F(t1)});')
def blink(sel, c0, c1, t0, t1, per=.25):
    n = max(1, int((t1 - t0) / per) // 2 * 2 - 1)
    J.append(f'tl.fromTo("{sel}", {{ fill: "{c0}" }}, {{ fill: "{c1}", duration: {per}, yoyo: true, repeat: {n}, ease: "steps(1)", immediateRender: false }}, {F(t0)});')
    J.append(f'tl.set("{sel}", {{ fill: "{c0}" }}, {F(t1)});')
# Bild 0 + Loop: Nordamerika-Fahnen
J.append(f'tl.set(["#pn-ca", "#pn-us"], {{ opacity: 1 }}, 0); tl.set(["#pn-ca", "#pn-us"], {{ opacity: 0 }}, {F(t_cut1)});')   # ab Bild 0 sichtbar (= letztes Bild)
J.append(f'tl.set(["#pn-ca", "#pn-us"], {{ opacity: 1 }}, {F(LOOP_T)});')
# Weltansicht s1: alle Fahnen
for cid in owned: show(f"pw-{cid}", t_cut1, st("s2"), .25)
show("pw-globi", t_cut1, st("s2"), .25)
# Japan blinkt gelb/weiß, wann immer es zu sehen ist
blink("#c-jp", JP_COL, "#ffd166", t_cut1, st("s3")); blink("#c-jp", JP_COL, "#ffd166", st("s12"), en("s13"))
# Ranking-Fahnen
for cid in ORDER: show(f"p-{cid}", st(SC[cid]) + .05, en(SC[cid]))
# s6: Duell-Fahnen
J.append(f'tl.set(["#pn-ca", "#pn-us"], {{ opacity: 1 }}, {F(st("s6"))}); tl.set(["#pn-ca", "#pn-us"], {{ opacity: 0 }}, {F(st("s7"))});')
# s8: keine FINNY-Fahne (Krone + Namens-Schild reichen; Fahne würde in der Nahaufnahme die Kopfzeile verdecken)
J.append(f'tl.set("#pn-us", {{ opacity: 1 }}, {F(t_ohne - .05)}); tl.set("#pn-us", {{ opacity: 0 }}, {F(en("s8"))});')
J.append(f'tl.set("#pn-ca", {{ opacity: 1 }}, {F(st("s9"))}); tl.set("#pn-ca", {{ opacity: 0 }}, {F(t_globi9 - .05)});')
J.append(f'tl.set(["#pn-ca", "#pn-us"], {{ opacity: 1 }}, {F(st("s14"))});')
# s9/s11: Globi-Fahne auf Russland, Russland blinkt
J.append(f'tl.set("#p-globi", {{ opacity: 1 }}, {F(t_globi9 - .05)}); tl.set("#p-globi", {{ opacity: 0 }}, {F(t_fast - .05)});')
blink("#c-ru", GLOBI_COL, "#ffd166", t_globi9, en("s9"), .2)
show("pw-globi", t_fast - .05, en("s10"), .2)
# s10: Australien-Kopie fliegt auf Russland
J.append(f'tl.set("#auclone", {{ opacity: 1, x: 0, y: 0 }}, {F(t_fast)}); tl.to("#auclone", {{ x: {RUC[0] - AUC[0]:.1f}, y: {RUC[1] - AUC[1]:.1f}, duration: .9, ease: "power2.inOut" }}, {F(t_fast + .1)});')
J.append(f'tl.set("#auclone", {{ opacity: 0 }}, {F(en("s10"))});')
# s12: DEIN NAME? auf Japan
show("p-dein", st("s12") + .1, en("s12"))
J.append(f'tl.fromTo("#p-dein-in", {{ rotation: -6 }}, {{ rotation: 6, duration: .25, yoyo: true, repeat: {max(1, int((en("s12") - st("s12") - .5) / .25))}, ease: "sine.inOut", transformOrigin: "0px 0px" }}, {F(st("s12") + .4)});')
# s13: freie Länder blitzen
random.seed(9)
free = [c for c in K if c not in owned and c not in ("ru", "jp") and K[c]["bbox"][2] - K[c]["bbox"][0] > 10]
used = set(); t = st("s13") + .2
while t < en("s13") - .2:
    cid = random.choice(free); used.add(cid)
    J.append(f'tl.fromTo("#c-{cid}", {{ fill: "#3a4a70" }}, {{ fill: "#ffffff", duration: .1, yoyo: true, repeat: 1, immediateRender: false }}, {F(t)});')
    t += .07
for cid in used: J.append(f'tl.set("#c-{cid}", {{ fill: "#3a4a70" }}, {F(en("s13"))});')

# ---------- HTML-Ebenen ----------
def ui(id_, t0, t1, inner, style): return f'<div id="{id_}" class="ui clip" data-start="{F(t0)}" data-duration="{F(max(.05, t1 - t0))}" style="{style}">{inner}</div>\n'
def chip(id_, txt, bg="#fff", fg="#111", size=44, extra=""):
    return f'<div id="{id_}" style="display:inline-block;max-width:1000px;background:{bg};color:{fg};font:900 {size}px/1.12 Inter,sans-serif;padding:12px 26px;border-radius:18px;border:5px solid #111;box-shadow:0 8px 0 #111;{extra}">{txt}</div>'
def pop(id_, t, s0=0, d=.3): J.append(f'tl.fromTo("#{id_}", {{ scale: {s0} }}, {{ scale: 1, duration: {d}, ease: "back.out(2.5)", immediateRender: false }}, {F(t)});')
html = ""
CAP_TOP = 1065          # Untertitel 1065–1165 px (55–61 %)
LOW1, LOW2 = 1200, 1300  # Schilder darunter, enden spätestens bei ~1380 px (72 %)
r = {c: RANK[c] for c in RANK}
HEAD = [("s1", "WER HAT DAS GRÖSSTE REICH?", 70, "#ffd166", "#111"), ("s2", "NUR ABONNENTEN BEKOMMEN EIN LAND", 58, "#ffd166", "#111"),
        ("s3", "PLATZ 5", 100, "#fff", "#111"), ("s4", "PLATZ 4", 100, "#fff", "#111"), ("s5", "PLATZ 3", 100, "#cd7f32", "#111"),
        ("s6", "FOTOFINISH!", 96, "#e63946", "#fff"), ("s7", "PLATZ 1 ODER 2?", 86, "#fff", "#111"),
        ("s8", "👑 KRONE FÜR FINNY", 80, "#ffd166", "#111"), ("s9", "ABER MOMENT …", 90, "#e63946", "#fff"),
        ("s10", "RUSSLAND IST GRÖSSER!", 72, GLOBI_COL, "#111"), ("s11", "HOLT EUCH DIE KRONE!", 80, "#e63946", "#fff"),
        ("s12", "JAPAN IST NOCH FREI!", 80, "#fff", "#e63946"), ("s13", f"{NOWN}/{TOTAL} VERGEBEN", 80, "#ffd166", "#111"),
        ("s14", "WER HAT DAS GRÖSSTE REICH?", 70, "#ffd166", "#111")]
for sid, txt, size, bg, fg in HEAD:
    t1 = en(sid) if sid != "s14" else END
    t0 = st(sid) if sid != "s14" else LOOP_T            # Loop: Kopfzeile wie Bild 0 erst in der Schluss-Fahrt
    if sid == "s14":
        html += ui("hs14a", st("s14"), LOOP_T, chip("hs14a-in", "NUR ABONNENTEN BEKOMMEN EIN LAND", "#ffd166", "#111", 58), "left:30px;right:30px;top:110px;text-align:center")
        pop("hs14a-in", st("s14"), 1.35, .2)
    html += ui(f"h{sid}", t0, t1, chip(f"h{sid}-in", txt, bg, fg, size), "left:30px;right:30px;top:110px;text-align:center")
    if sid not in ("s1", "s14"): J.append(f'tl.fromTo("#h{sid}-in", {{ scale: 1.35 }}, {{ scale: 1, duration: .2, ease: "back.out(2)" }}, {F(st(sid))});')
# Quellenzeile während der Flächen-Szenen
html += ui("src", st("s3"), en("s10"), '<div style="display:inline-block;background:rgba(0,0,0,.6);border-radius:10px;padding:4px 14px;font:700 28px Inter,sans-serif;color:#fff">Fläche: CIA World Factbook (Gesamtfläche)</div>', "left:40px;top:300px")
# Zähler oben rechts (außer s3–s10 wegen Quellenzeile und s13 groß in der Mitte)
CNT = f'<div style="display:inline-block;background:rgba(0,0,0,.65);border-radius:14px;padding:6px 18px;font:900 44px Inter,sans-serif;color:#fff"><span style="color:#06d6a0">{NOWN}</span>/{TOTAL}</div>'
html += ui("cntA", 0, st("s3"), CNT, "right:36px;top:300px"); html += ui("cntB", st("s11"), st("s13"), CNT, "right:36px;top:300px")
html += ui("cntC", st("s14"), END, CNT, "right:36px;top:300px")
# Krone (SVG)
def crown(id_, w_=230, q=False):
    qm = '<text x="100" y="118" text-anchor="middle" style="font:900 74px Inter,sans-serif;fill:#111">?</text>' if q else ""
    return (f'<svg id="{id_}" viewBox="0 0 200 150" width="{w_}" height="{w_ * .75:.0f}" style="overflow:visible;filter:drop-shadow(0 10px 0 rgba(0,0,0,.45))">'
            '<path d="M18 135 L8 40 L58 85 L100 18 L142 85 L192 40 L182 135 Z" fill="#ffd166" stroke="#111" stroke-width="8" stroke-linejoin="round"/>'
            '<rect x="16" y="118" width="168" height="24" rx="6" fill="#f4b400" stroke="#111" stroke-width="7"/>'
            '<circle cx="8" cy="40" r="11" fill="#ef476f" stroke="#111" stroke-width="6"/><circle cx="100" cy="18" r="12" fill="#06d6a0" stroke="#111" stroke-width="6"/>'
            f'<circle cx="192" cy="40" r="11" fill="#118ab2" stroke="#111" stroke-width="6"/>{qm}</svg>')
# Bild 0 / Loop: Krone mit „?“ über Nordamerika (identisch)
cx0, cy0 = 860, 560                 # rechts neben der FINNY-Fahne (über Grönland)
for id_, t0, t1 in (("cr0", 0, t_cut1), ("crL", LOOP_T, END)):
    html += ui(id_, t0, t1, f'<div id="{id_}-in" style="display:inline-block">{crown(id_ + "-s", 230, True)}</div>', f"left:{cx0 - 115}px;top:{cy0 - 86}px")
    J.append(f'tl.fromTo("#{id_}-in", {{ y: 0, rotation: -6 }}, {{ y: -22, rotation: 6, duration: .4, yoyo: true, repeat: {max(1, int((t1 - t0) / .4) - 1)}, ease: "sine.inOut" }}, {F(t0)});')
J.append('tl.fromTo("#cr0-in", { scale: 0 }, { scale: 1, duration: .35, ease: "back.out(3)", immediateRender: false }, .05);')
# Abo-Banner (Anfang bis Ende s2, Schluss s14) – zwischen 62 und 72 % Bildhöhe
ABO = (chip("{id}-a", "🔔 ABONNIER", "#e63946", "#fff", 58) + '<div style="height:14px"></div>' +
       chip("{id}-b", "💬 + KOMMENTIER DEIN WUNSCHLAND", "#fff", "#111", 40))
html += ui("ab1", 0, en("s2"), ABO.replace("{id}", "ab1"), f"left:0;right:0;top:{LOW1}px;text-align:center")
html += ui("ab14", st("s14"), END, ABO.replace("{id}", "ab14"), f"left:0;right:0;top:{LOW1}px;text-align:center")
J.append(f'tl.to("#ab1-a", {{ scale: 1.08, duration: .35, yoyo: true, repeat: {int(en("s2") / .35) - 1}, ease: "sine.inOut" }}, .4);')
J.append(f'tl.to("#ab14-a", {{ scale: 1.08, duration: .35, yoyo: true, repeat: {int((END - st("s14")) / .35) - 1}, ease: "sine.inOut" }}, {F(st("s14") + .2)});')
pop("ab1-b", t_kom2 - .05, 1.4, .25)
# s2: Kommentar-Beispiel neben Japan + FREI!-Stempel
html += ui("jp2", t_kom2 - .05, en("s2"), chip("jp2-in", "💬 „JAPAN!“", "#fff", "#111", 60), "left:60px;top:520px")
pop("jp2-in", t_kom2 - .05)
def frei(id_, t0, t1, top, size=110):
    global html
    html += ui(id_, t0, t1, f'<div id="{id_}-in" style="display:inline-block;transform:rotate(-8deg);background:#fff;color:#e63946;font:900 {size}px/1 Inter,sans-serif;padding:10px 34px;border:10px solid #e63946;border-radius:22px;box-shadow:0 10px 0 #111">FREI!</div>', f"left:0;right:0;top:{top}px;text-align:center")
    J.append(f'tl.fromTo("#{id_}-in", {{ scale: 1.6 }}, {{ scale: 1, duration: .25, ease: "back.out(2)" }}, {F(t0)});')
    J.append(f'tl.fromTo("#{id_}-in", {{ opacity: 1 }}, {{ opacity: .35, duration: .25, yoyo: true, repeat: {max(1, int((t1 - t0 - .3) / .25) // 2 * 2 - 1)}, ease: "steps(1)" }}, {F(t0 + .5)});')
# Japan-Stempel in s2 (rechts neben Japan, Japan liegt rechts im Bild)
frei("fr2", st("s2") + .1, en("s2"), 830, 90)
J.append('tl.set("#fr2", { left: "380px" }, 0);')
frei("fr12", st("s12") + .05, en("s12"), 870, 120)
# kleines FREI!-Schild in der Weltansicht s1 (an Japan) – Position aus Kamera berechnet
jx, jy = screen(JPC[0], JPC[1], WORLD_C[0], WORLD_C[1], Z_W)
html += ui("frw", t_cut1, st("s2"), '<div style="display:inline-block;background:#fff;color:#e63946;font:900 34px Inter,sans-serif;padding:2px 12px;border:5px solid #e63946;border-radius:10px">JAPAN: FREI!</div>', f"left:{jx - 270:.0f}px;top:{jy + 40:.0f}px")
# s3–s5: Fläche (zählt hoch) + Fakt
for cid in ORDER:
    s = SC[cid]; d = RANK[cid]; o = owned[cid]
    html += ui(f"ar{cid}", TB[cid] - .05, en(s), f'<div id="ar{cid}-in" style="display:inline-block;background:#fff;border:6px solid #111;border-radius:22px;box-shadow:0 8px 0 #111;padding:6px 30px;font:900 78px/1.05 Inter,sans-serif;color:#111"><span id="ar{cid}-v">0</span> km²</div>', f"left:0;right:0;top:{LOW1}px;text-align:center")
    J.append(f'(() => {{ const o = {{ v: 0 }}; tl.fromTo(o, {{ v: 0 }}, {{ v: {d["flaeche_km2"]}, duration: .7, ease: "power2.out", onUpdate: () => {{ document.getElementById("ar{cid}-v").textContent = Math.round(o.v).toLocaleString("de-DE"); }} }}, {F(TB[cid])}); }})();')
    pop(f"ar{cid}-in", TB[cid] - .05, .4, .2)
    html += ui(f"nm{cid}", st(s) + .05, en(s), chip(f"nm{cid}-in", f'{o["land_de"]} · {o["name"]}', o["farbe"], "#111", 52), "left:0;right:0;top:330px;text-align:center")
    html += ui(f"fk{cid}", TB[cid] + .5, en(s), chip(f"fk{cid}-in", d["fakt"], "#06d6a0" if cid != "de" else "#ffd166", "#111", 44), f"left:0;right:0;top:{LOW2 + 10}px;text-align:center")
    pop(f"fk{cid}-in", TB[cid] + .5)
# s6: VS-Schild + Trommelwirbel-Spannung
html += ui("vs6", t_finny6 - .05, en("s6"), '<div id="vs6-in" style="display:inline-block;background:#111;color:#fff;font:900 120px/1 Inter,sans-serif;padding:14px 40px;border:8px solid #fff;border-radius:30px">LIAM <span style="color:#ffd166">VS</span> FINNY</div>', f"left:0;right:0;top:{LOW1}px;text-align:center")
pop("vs6-in", t_finny6 - .05, 2.0, .3)
J.append(f'tl.to("#vs6-in", {{ x: 6, duration: .05, yoyo: true, repeat: {int((en("s6") - t_finny6 - .4) / .05)}, ease: "none" }}, {F(t_finny6 + .35)});')
# s7: Fotofinish-Balken (USA vs. Kanada)
us, ca = RANK["us"], RANK["ca"]
BH = 560 / 10_000_000
def bar(id_, x, col, name, land):
    return (f'<div style="position:absolute;left:{x}px;bottom:0;width:300px;height:640px">'
            f'<div id="{id_}" style="position:absolute;left:0;right:0;bottom:0;height:0;background:{col};border:6px solid #111;border-bottom:none;border-radius:20px 20px 0 0;overflow:visible">'
            f'<div style="position:absolute;left:-30px;right:-30px;top:-118px;text-align:center;font:900 52px/1 Inter,sans-serif;color:#fff;-webkit-text-stroke:10px #111;paint-order:stroke fill">{land}</div>'
            f'<div style="position:absolute;left:-30px;right:-30px;top:-62px;text-align:center;font:900 44px/1 Inter,sans-serif;color:{col};-webkit-text-stroke:9px #111;paint-order:stroke fill">{name}</div>'
            f'<div style="position:absolute;left:0;right:0;top:24px;text-align:center;font:900 46px/1 Inter,sans-serif;color:#111"><span id="{id_}-v">0</span></div>'
            f'<div style="position:absolute;left:0;right:0;top:78px;text-align:center;font:900 34px/1 Inter,sans-serif;color:#111">km²</div></div></div>')
html += ui("bars", st("s7"), en("s7"),
           '<div style="position:absolute;inset:0;background:rgba(11,26,51,.72)"></div>'
           f'<div style="position:absolute;left:190px;top:390px;width:700px;height:640px">{bar("bus", 0, owned["us"]["farbe"], "LIAM", "USA")}{bar("bca", 400, owned["ca"]["farbe"], "FINNY", "KANADA")}'
           '<div style="position:absolute;left:-40px;right:-40px;bottom:-8px;height:10px;background:#fff;border-radius:5px"></div></div>',
           "left:0;top:0;width:1080px;height:1060px")
t_us7 = w("s7", "USA:")
J.append(f'tl.set("#bca", {{ opacity: 0 }}, {F(st("s7"))}); tl.set("#bca", {{ opacity: 1 }}, {F(t_ca7)});')
for id_, t0, val in (("bus", t_us7, us["flaeche_km2"]), ("bca", t_ca7, ca["flaeche_km2"])):
    J.append(f'tl.to("#{id_}", {{ height: {val * BH:.0f}, duration: 1.1, ease: "power2.out" }}, {F(t0)});')
    J.append(f'(() => {{ const o = {{ v: 0 }}; tl.fromTo(o, {{ v: 0 }}, {{ v: {val}, duration: 1.1, ease: "power2.out", onUpdate: () => {{ document.getElementById("{id_}-v").textContent = Math.round(o.v).toLocaleString("de-DE"); }} }}, {F(t0)}); }})();')
diff = ca["flaeche_km2"] - us["flaeche_km2"]
html += ui("dif7", t_ca7 + 1.1, en("s7"), chip("dif7-in", f"+{de_num(diff)} km²", "#ffd166", "#111", 60), f"left:0;right:0;top:{LOW1}px;text-align:center")
pop("dif7-in", t_ca7 + 1.1, 2.0, .25)
# s8: Krone fällt auf Kanada + Konfetti
kx, ky = screen(CANADA_PT[0], CANADA_PT[1], CANADA_PT[0], CANADA_PT[1], Z_NA * 1.15)
html += ui("cr8", st("s8"), t_seen - .05, f'<div id="cr8-in" style="display:inline-block">{crown("cr8-s", 300)}</div>', f"left:{kx - 150:.0f}px;top:{ky - 330:.0f}px")
J.append(f'tl.fromTo("#cr8-in", {{ y: -900, rotation: -25 }}, {{ y: 0, rotation: 0, duration: .45, ease: "bounce.out" }}, {F(st("s8"))});')
html += ui("w8", t_ca8 - .05, t_seen - .05, chip("w8-in", f'👑 {owned["ca"]["name"]} · {de_num(ca["flaeche_km2"])} km²', owned["ca"]["farbe"], "#111", 50), f"left:0;right:0;top:{LOW1}px;text-align:center")
pop("w8-in", t_ca8 - .05)
html += ui("wa8", t_seen - .05, t_ohne - .05, chip("wa8-in", ca["fakt"], "#4cc9f0", "#111", 56), f"left:0;right:0;top:{LOW1}px;text-align:center")
pop("wa8-in", t_seen - .05)
html += ui("us8", t_ohne - .05, en("s8"), chip("us8-in", f'{owned["us"]["name"]}: {us["fakt"]}', owned["us"]["farbe"], "#fff", 46), f"left:0;right:0;top:{LOW1}px;text-align:center")
pop("us8-in", t_ohne - .05)
random.seed(4)
COLS = ["#ffd166", "#ef476f", "#06d6a0", "#118ab2", "#ffffff", "#f78c6b"]
conf = ""
for k in range(90):
    x = random.uniform(0, 1060); wd = random.uniform(14, 26); ht = wd * random.uniform(.4, .8)
    conf += f'<div class="cf" id="cf{k}" style="position:absolute;left:{x:.0f}px;top:-60px;width:{wd:.0f}px;height:{ht:.0f}px;background:{random.choice(COLS)};border:2px solid #111"></div>'
    J.append(f'tl.fromTo("#cf{k}", {{ y: 0, rotation: 0 }}, {{ y: {random.uniform(1300, 2050):.0f}, x: {random.uniform(-160, 160):.0f}, rotation: {random.uniform(-720, 720):.0f}, duration: {random.uniform(1.8, 2.8):.2f}, ease: "power1.in" }}, {F(st("s8") + .35 + random.uniform(0, .5))});')
html += ui("conf", st("s8") + .3, en("s8"), conf, "left:0;top:0;width:1080px;height:1920px;overflow:hidden")
# s9: Glitch-Rahmen
html += ui("alarm", st("s9"), en("s9"), '<div id="alarm-in" style="position:absolute;inset:0;border:26px solid #e63946;box-shadow:inset 0 0 80px rgba(230,57,70,.8)"></div>', "left:0;top:0;width:1080px;height:1920px")
J.append(f'tl.fromTo("#alarm-in", {{ opacity: 1 }}, {{ opacity: 0, duration: .2, yoyo: true, repeat: {int((en("s9") - st("s9")) / .2) - 1}, ease: "steps(1)" }}, {F(st("s9"))});')
# s10: 17 Millionen + Fakt
gl = D["twist"]
html += ui("ru10", st("s10"), en("s10"), f'<div id="ru10-in" style="display:inline-block;background:#fff;border:6px solid #111;border-radius:22px;box-shadow:0 8px 0 #111;padding:6px 30px;font:900 76px/1.05 Inter,sans-serif;color:#111"><span id="ru10-v">0</span> km²</div>', f"left:0;right:0;top:{LOW1}px;text-align:center")
J.append(f'(() => {{ const o = {{ v: 0 }}; tl.fromTo(o, {{ v: 0 }}, {{ v: {gl["flaeche_km2"]}, duration: .8, ease: "power2.out", onUpdate: () => {{ document.getElementById("ru10-v").textContent = Math.round(o.v).toLocaleString("de-DE"); }} }}, {F(st("s10") + .1)}); }})();')
html += ui("fk10", t_fast - .05, en("s10"), chip("fk10-in", gl["fakt"], GLOBI_COL, "#111", 50), f"left:0;right:0;top:{LOW2 + 10}px;text-align:center")
pop("fk10-in", t_fast - .05)
# s11: Kommentar-Bubble
html += ui("ru11", t_kom11 - .05, en("s11"), chip("ru11-in", "💬 „RUSSLAND!“", "#fff", "#111", 62), f"left:0;right:0;top:{LOW1 + 20}px;text-align:center")
pop("ru11-in", t_kom11 - .05)
# s13: Zähler groß
html += ui("big13", st("s13") + .05, en("s13"),
           f'<div id="big13-in" style="display:inline-block;background:rgba(11,26,51,.88);border:6px solid #fff;border-radius:28px;padding:10px 40px">'
           f'<div style="font:900 150px/1 Inter,sans-serif;color:#fff"><span style="color:#06d6a0">{NOWN}</span>/{TOTAL}</div>'
           f'<div style="font:900 60px/1.1 Inter,sans-serif;color:#ffd166;margin-top:6px">NOCH {FREI} FREI!</div></div>', "left:0;right:0;top:690px;text-align:center")
J.append(f'tl.fromTo("#big13-in", {{ scale: 0, y: -400 }}, {{ scale: 1, y: 0, duration: .35, ease: "back.out(1.8)" }}, {F(st("s13") + .05)});')
# Weißer Blitz bei jedem harten Schnitt
for k, t in enumerate(CUTS):
    if t == LOOP_T: continue
    html += ui(f"fl{k}", t, t + .12, f'<div id="fl{k}-in" style="position:absolute;inset:0;background:#fff"></div>', "left:0;top:0;width:1080px;height:1920px")
    J.append(f'tl.fromTo("#fl{k}-in", {{ opacity: .4 }}, {{ opacity: 0, duration: .12 }}, {F(t)});')

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
GEST = [(t_globi9 + .1, en("s9") - t_globi9 - .2, "both"), (st("s10") + .1, 1.4, "point"), (st("s11"), en("s11") - st("s11"), "both")]
gh = globi.build({}, END, GEST, left=0, top=0)
gh = gh.replace('<g id="g-brow">', '<g id="g-tongue" style="display:none"><path d="M204 206 Q220 252 236 206 Z" fill="#ff6b81" stroke="#111" stroke-width="5"/></g><g id="g-brow">', 1)
CR = ('<g id="g-crown" style="display:none" transform="translate(130 -28) scale(.9)">'
      '<path d="M18 135 L8 40 L58 85 L100 18 L142 85 L192 40 L182 135 Z" fill="#ffd166" stroke="#111" stroke-width="8" stroke-linejoin="round"/>'
      '<rect x="16" y="118" width="168" height="24" rx="6" fill="#f4b400" stroke="#111" stroke-width="7"/>'
      '<circle cx="100" cy="18" r="12" fill="#06d6a0" stroke="#111" stroke-width="6"/></g>')
anchor = '\n  <g transform="translate(204 285)">'
assert anchor in gh, "Globi-SVG hat sich geändert"
i_head_end = gh.index(anchor); i_close = gh.rindex("</g>", 0, i_head_end)
gh = gh[:i_close] + CR + gh[i_close:]                    # Krone als letztes Element im Kopf (bewegt sich mit)
def gset(t, k, X, Y, op=1, rot=0): x, y = GK(k, X, Y); GJ.append(f'tl.set("#g-wrap", {{ x: {x:.0f}, y: {y:.0f}, scale: {k}, rotation: {rot}, opacity: {op} }}, {F(t)});')
GJ.append('tl.set("#g-wrap", { transformOrigin: "0 0", opacity: 0 }, 0);')
# s9: Globi sitzt auf Russland (ploppt bei „Globi“ auf)
X9, Y9 = screen(RUF[0] - 75, RUF[1] + 30, *ctr(RU_BOX), Z_RU)   # links neben der GLOBI-Fahne
gset(t_globi9 - .05, .62, X9, min(Y9, 1000))
GJ.append(f'tl.fromTo("#g-wrap", {{ y: "+=260" }}, {{ y: "-=260", duration: .3, ease: "back.out(2)", immediateRender: false }}, {F(t_globi9 - .05)});')
# s10: Globi zeigt neben der Zahl (nur erste Einstellung), danach weg
X10, Y10 = screen(RUF[0] - 60, RUF[1] + 30, RUF[0], RUF[1] + 10, Z_RU * 1.25)
gset(st("s10"), .62, X10, min(Y10, 1000))
gset(t_fast - .05, .62, X10, min(Y10, 1000), op=0)
# s11: Globi groß mit Krone, Zunge raus
gset(st("s11"), .82, 600, 1010)
GJ.append(f'tl.fromTo("#g-wrap", {{ rotation: -4 }}, {{ rotation: 4, duration: .3, yoyo: true, repeat: {int((en("s11") - st("s11")) / .3) - 1}, ease: "sine.inOut" }}, {F(st("s11"))});')
GJ.append(f'tl.set("#g-crown", {{ display: "inline" }}, {F(st("s11"))}); tl.fromTo("#g-crown", {{ y: -300 }}, {{ y: 0, duration: .35, ease: "bounce.out" }}, {F(st("s11"))});')
GJ.append(f'tl.set("#g-tongue", {{ display: "inline" }}, {F(t_kom11)}); tl.set("#g-tongue", {{ display: "none" }}, {F(en("s11"))});')
gset(en("s11"), .5, -400, 1200, op=0)
gh = gh.replace('window.__timelines["globi"] = tl;', "\n      ".join(GJ) + '\n      window.__timelines["globi"] = tl;')
open("compositions/globi.html", "w", encoding="utf-8").write(gh)

# ---------- Untertitel: hart wechselnd, Schlüsselwörter ≥ 0,3 s ----------
HOT = {o["name"] for o in OWN} | {norm(o["land_de"]).upper() for o in OWN} | {"JAPAN", "RUSSLAND", "ABONNIER", "ABONNENTEN", "GLOBI", "FREI", "KRONE",
       "LÅKI", "5", "4", "3", "360.000", "195", "190", "17", "9,8", "10", "WUNSCHLAND", "REICH", "SEEN", "WASSER", "AUSTRALIEN", "MILLIONEN", "MOMENT"}
CAPMAP = {"s7": [0, 1, 2, 5, 6, 7, 8, 9]}   # Anzeige 9,8 / 10 ↔ gesprochen „neun Komma acht“ / „zehn“
caps = []
for sc in V["scenes"]:
    sid = sc["id"]; words = T[sid]["words"]; k = 0
    for disp, sp in sc["groups"]:
        dw = [d for d in disp.split() if any(ch.isalnum() for ch in d)]; swn = sp.split()
        idx = CAPMAP.get(sid) or ([*range(len(dw))] if len(dw) == len(swn) else [int(j * len(swn) / len(dw)) for j in range(len(dw))])
        assert len(idx) == len(dw), (sid, dw)
        for j, d in enumerate(dw): caps.append([round(T[sid]["start"] + words[min(len(words) - 1, k + idx[j])]["s"], 2), d, sid])
        k += len(swn)
key = lambda d: re.sub(r"[!?.,:–]", "", d.upper()) in HOT
for j in range(1, len(caps)):
    mind = .3 if key(caps[j - 1][1]) else .14
    caps[j][0] = round(max(caps[j][0], caps[j - 1][0] + mind), 2)
items = []
for j, (t0, d, sid) in enumerate(caps):
    nxt = caps[j + 1][0] if j + 1 < len(caps) else END
    te = min(nxt, t0 + 1.3, en(sid) + .2) if j + 1 < len(caps) else min(END, t0 + 1.6)
    up = d.upper(); col = "#ffd166" if key(d) else "#fff"
    fs = min(96, int(1500 / max(1, len(up))))
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
FXL = [("pop", 0.05, .55, .15), ("pop", .5, .35, .15)]
for t in CUTS:
    if t != LOOP_T: FXL.append(("swoosh", t - .05, .3, .5))
FXL += [("pop", t_kom2 - .05, .5, .15)]
for cid in ORDER: FXL += [("pop", st(SC[cid]) + .05, .5, .15), ("tick", TB[cid], .22, .7), ("boing", TB[cid] + .5, .3, .55)]
FXL += [("klong", t_finny6 - .05, .35, 1.2), ("wirbel", t_finny6 + .35, .5, min(2.04, st("s7") - t_finny6 + .3))]
FXL += [("tick", t_us7, .22, 1.1), ("tick", t_ca7, .22, 1.1), ("chime", t_ca7 + 1.1, .3, 1.4)]
FXL += [("hit", st("s8") + .35, .5, 1.6), ("chime", st("s8") + .4, .35, 1.4), ("blips", st("s8") + .5, .25, 1.33), ("pop", t_seen - .05, .45, .15), ("boing", t_ohne - .05, .35, .55)]
FXL += [("glitch", st("s9") + .02, .3, .6), ("boing", t_globi9 - .05, .45, .55)]
FXL += [("tick", st("s10") + .1, .22, .8), ("whoosh", t_fast + .1, .55, .94)]
FXL += [("hit", st("s11"), .4, 1.6), ("pop", t_kom11 - .05, .5, .15)]
FXL += [("pop", st("s12") + .05, .5, .15), ("blips", st("s13") + .1, .3, 1.33), ("pop", st("s14"), .45, .15)]
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
