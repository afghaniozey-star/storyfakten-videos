"""ABO-WELT Tag 4 (YouTube) – EREIGNIS-Tag „WER BEKOMMT ITALIEN?“ (keine neuen Besitzer).
Bild 0: Punch-Zoom auf den blinkenden Stiefel (Italien in Flaggenfarben) mit großem „?“, Ladebalken
„Land wird vergeben … ?“ (55–72 % Bildhöhe, dauerhaft), Abo-Aufruf am Anfang und Ende,
62 Welterbe-Sterne + Pokal, Pizza rollt + Stempel KULTURERBE 2025, Lupe auf San Marino/Vatikan,
Stiefel kickt Fußball (Ladebalken 99 %), Rundflug über die 5 echten Besitzer, Japan FREI!, Globi auf Russland,
Zähler 5/195 → NOCH 190 FREI, Loop-Ende = Bild 0.
Aufruf (im Projektordner): /usr/bin/python3 tools/abowelt_tag4.py
liest welt.json, daten.json (= daten-tag4.json), voice.json (= voice-tag4.json), assets/vo/timing.json, weltkarte.json
Karte: @svg-maps/world (CC BY 4.0) → in der Beschreibung „Karte: svg-maps (CC BY 4.0)“ nennen."""
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
assert "it" not in owned and "jp" not in owned, "Italien/Japan sind laut welt.json nicht mehr frei"
GLOBI_COL = "#ff8a3d"; JP_COL = "#ffffff"; FREE_COL = "#3a4a70"
S0, MY = 1080 / 1010, 560
FX, FY = 540, 720                   # Bildpunkt, auf den die Kamera zentriert
J, GJ = [], []
ORTE = D["orte_karte"]

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

SHOTS = []
def shot(t, box=None, center=None, z=None, zmax=8.0, drift=1.05):
    if center is None: center = ctr(box)
    if z is None: z = zoom_for(box, zmax)
    SHOTS.append((round(t, 2), center[0], center[1], z, drift)); return z

# ---------- Karte ----------
ITB = K["it"]["bbox"]; ITC = (ctr(ITB)[0] - 1.5, ctr(ITB)[1])       # leicht nach links: Stiefel optisch mittig
Z_IT = zoom_for(ITB, 13.0); Z0 = Z_IT * 1.08
IT = polys("it")
SM = ctr(K["sm"]["bbox"]); VA = ctr(K["va"]["bbox"])
JPB = K["jp"]["bbox"]; JPC = ctr(JPB); Z_JP = zoom_for(JPB, 9.0)
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
    if cid in ("sm", "va"): col = "#ffffff"
    elif cid == "it": col = "url(#ittri)"
    elif cid in owned: col = owned[cid]["farbe"]
    elif cid == "jp": col = JP_COL
    elif cid == "ru": col = GLOBI_COL
    else: col = FREE_COL
    paths.append(f'<path id="c-{cid}" d="{c["path"]}" fill="{col}" stroke="#141c33" stroke-width="0.6" vector-effect="non-scaling-stroke"/>')
# Italien obenauf (damit es beim Kick über den Nachbarn liegt) + weiße Blink-Kopie
it_i = next(i for i, p in enumerate(paths) if 'id="c-it"' in p); paths.append(paths.pop(it_i))
paths.append(f'<path id="itwhite" d="{K["it"]["path"]}" fill="#ffffff" opacity="0" stroke="#141c33" stroke-width="0.6" vector-effect="non-scaling-stroke"/>')
DEFS = ('<defs><linearGradient id="ittri" x1="0" y1="0" x2="1" y2="0">'
        '<stop offset="0" stop-color="#009246"/><stop offset=".36" stop-color="#009246"/><stop offset=".36" stop-color="#ffffff"/>'
        '<stop offset=".64" stop-color="#ffffff"/><stop offset=".64" stop-color="#ce2b37"/><stop offset="1" stop-color="#ce2b37"/></linearGradient></defs>')

def flag(id_, mx, my, txt, col, z, k=1.0, op=0, fg="#111"):
    s = k / z / S0; wd = 46 + 30 * len(txt)
    return (f'<g id="{id_}" opacity="{op}" transform="translate({mx:.2f} {my:.2f}) scale({s:.4f})"><g id="{id_}-in">'
            f'<path d="M0 0 V-150" stroke="#111" stroke-width="8"/><rect x="0" y="-150" width="{wd}" height="70" rx="12" fill="{col}" stroke="#111" stroke-width="6"/>'
            f'<text x="{wd/2:.0f}" y="-101" text-anchor="middle" style="font:900 46px Inter,sans-serif;fill:{fg}">{txt}</text>'
            f'<circle r="14" fill="#fff" stroke="#111" stroke-width="6"/></g></g>')

FOC = {o["land"]: (o.get("fokus") or K[o["land"]]["bbox"]) for o in OWN}
CANADA_PT = (215, 150); US_PT = (215, 340)
PT = {cid: ctr(FOC[cid]) for cid in owned}; PT["ca"] = CANADA_PT; PT["us"] = US_PT
ZO = {cid: zoom_for(FOC[cid], 6.0) for cid in owned}
pins = ""
for o in OWN:
    cid = o["land"]
    pins += flag(f'p-{cid}', *PT[cid], o["name"], o["farbe"], ZO[cid])
    pins += flag(f'pw-{cid}', *PT[cid], o["name"], o["farbe"], 1.0, k=.62)
pins += flag("p-globi", RUF[0], RUF[1], "GLOBI", GLOBI_COL, Z_RU)
pins += flag("pw-globi", RUF[0], RUF[1], "GLOBI", GLOBI_COL, 1.0, k=.62)
pins += flag("pw-jp", JPC[0] - 4, JPC[1] + 4, "FREI!", "#ffffff", 1.0, k=.62, fg="#e63946")
pins += flag("pw-it", ITC[0], ITC[1], "ITALIEN?", "#ffffff", 1.0, k=.62, fg="#e63946")
# Welterbe-Orte (Fahnen) in s3
SITES = [("KOLOSSEUM", ORTE["rom_kolosseum"]), ("PISA", ORTE["pisa"]), ("VENEDIG", ORTE["venedig"])]
for k_, (nm, (mx, my)) in enumerate(SITES): pins += flag(f"ws{k_}", mx, my, nm, "#ffd166", Z_IT, k=.55)
# 62 Goldsterne in Italien (zufällig, innerhalb des Umrisses)
random.seed(62); STARS = []
while len(STARS) < 62:
    px, py = random.uniform(ITB[0], ITB[2]), random.uniform(ITB[1], ITB[3])
    if inside(IT, px, py) and all((px - a) ** 2 + (py - b) ** 2 > 2.2 for a, b in STARS): STARS.append((px, py))
STAR_D = "M0 -10 L2.9 -4 L9.5 -3.1 L4.7 1.5 L5.9 8.1 L0 5 L-5.9 8.1 L-4.7 1.5 L-9.5 -3.1 L-2.9 -4 Z"
stars = "".join(f'<g transform="translate({x:.2f} {y:.2f}) scale({1.35 / Z_IT / S0:.4f})"><g id="st{k}">'
                f'<path d="{STAR_D}" transform="scale(1.9)" fill="#ffd166" stroke="#111" stroke-width="2.2"/></g></g>' for k, (x, y) in enumerate(STARS))
# San Marino / Vatikan: Punkte in (übertriebener) Echtgröße – Vatikan so klein, dass nachgezoomt werden muss
mini = (f'<circle id="dot-sm" cx="{SM[0]:.2f}" cy="{SM[1]:.2f}" r="0.16" fill="#e63946" stroke="#fff" stroke-width="2" vector-effect="non-scaling-stroke" opacity="0"/>'
        f'<circle id="dot-va" cx="{VA[0]:.2f}" cy="{VA[1]:.2f}" r="0.035" fill="#ffd166" stroke="#111" stroke-width="1.5" vector-effect="non-scaling-stroke" opacity="0"/>')
MAP = (f'<g id="cam"><rect x="-6000" y="-6000" width="14000" height="14000" fill="#0e3a66"/>'
       f'<g transform="translate(0 {MY}) scale({S0:.5f})">{DEFS}{"".join(paths)}{mini}<g id="stars">{stars}</g>{pins}</g></g>')

# ---------- Schnittliste ----------
shot(0, center=ITC, z=Z0, drift=1.0)                                            # Bild 0 (Punch-Zoom 108 → 100 %)
t_wer1 = w("s1", "Wer"); t_cut1 = min(1.4, t_wer1 - .05)
shot(t_cut1, center=(ITC[0] + 3, ITC[1] + 6), z=Z_IT * 1.45)                    # 1. harter Schnitt ≤ 1,5 s: Süden + Ladebalken
t_abo2 = w("s2", "Abonnier"); t_kom2 = w("s2", "kommentier"); t_nur2 = w("s2", "nur")
shot(st("s2"), center=(ITC[0] + 2, ITC[1] - 18), z=Z_IT * .5)                   # Europa: Abo-Knopf
shot(t_kom2 - .05, center=(ITC[0], ITC[1] - 4), z=Z_IT * .75)                  # Sprechblase fliegt auf den Stiefel
shot(t_nur2 - .05, center=ITC, z=Z_IT * .9)
t_62 = w("s3", "zweiundsechzig"); t_mehr3 = w("s3", "mehr")
shot(st("s3"), center=ITC, z=Z_IT)                                              # Pokal + Sterne
shot(t_mehr3 - .05, center=(ITC[0] - 2, ITC[1] - 3), z=Z_IT * 1.12)
t_kul4 = w("s4", "Kulturerbe."); t_piz4 = w("s4", "Pizza")
shot(st("s4"), center=ITC, z=Z_IT * .92)                                        # Pizza rollt
shot(t_kul4 - .05, center=(ITC[0] + 1, ITC[1] + 2), z=Z_IT * 1.05)             # Stempel
shot(t_piz4 - .05, center=(ITC[0] + 4, ITC[1] + 4), z=Z_IT * 1.25)
t_san5 = w("s5", "San"); t_vat5 = w("s5", "Vatikan,"); t_kl5 = w("s5", "kleinste"); t_gib5 = w("s5", "Gibt's")
Z_SM, Z_VA, Z_VA2 = 55.0, 95.0, 300.0
shot(st("s5"), center=ITC, z=Z_IT * .95)                                        # „Aber Achtung“
shot(t_san5 - .05, center=SM, z=Z_SM)                                           # Lupe: San Marino
shot(t_vat5 - .05, center=VA, z=Z_VA)                                           # Lupe: Vatikan (winzig)
shot(t_kl5 - .05, center=VA, z=Z_VA2, drift=1.08)                               # Lupe muss nachzoomen
shot(t_gib5 - .05, center=(ITC[0] - 1, ITC[1] - 4), z=Z_IT * 1.1)              # EXTRA!
t_ita6 = w("s6", "Italien"); t_stf6 = w("s6", "Stiefel.")
shot(st("s6"), center=(ITC[0] + 3, ITC[1] + 2), z=Z_IT * .85)                  # Kick
shot(t_ita6 - .05, center=(ITC[0] - 6, ITC[1] - 2), z=Z_IT * .62)
shot(t_stf6 - .05, center=ITC, z=Z_IT * .95)                                    # Ladebalken 99 %
RUND = [("ca", "Kanada"), ("br", "Brasilien"), ("de", "Deutschland"), ("us", "USA"), ("au", "Australien")]
TR = {}
for cid, word in RUND:
    TR[cid] = w("s7", word) - .05 if cid != "ca" else st("s7")
    shot(TR[cid], box=FOC[cid], zmax=6.0)
t_auf8 = w("s8", "Auf"); t_glo8 = w("s8", "Globi!")
shot(st("s8"), center=(JPC[0] + 4, JPC[1]), z=Z_JP)                            # Japan FREI!
shot(t_auf8 - .05, box=RU_BOX, zmax=3)                                          # Globi auf Russland
shot(t_glo8 + .45, center=ctr(RU_BOX), z=Z_RU * .92, drift=1.1)                 # Trommelwirbel: langsamer Zoom
t_noch9 = w("s9", "Noch")
shot(st("s9"), center=WORLD_C, z=1.0)                                           # Welt + Zähler
shot(t_noch9 - .05, center=(540, 320), z=1.08)
t_abo10 = w("s10", "Abonnier"); t_nur10 = w("s10", "nur")
shot(st("s10"), center=ITC, z=Z_IT * .85)
shot(t_abo10 - .05, center=(ITC[0] + 2, ITC[1] - 18), z=Z_IT * .5)
LOOP_T = round(max(t_nur10 - .05, END - 3.0), 2)
SHOTS.append((LOOP_T, ITC[0], ITC[1], Z_IT * .8, "loop"))                       # fährt bis END zurück auf Bild 0
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
        x2, y2 = campos(cx, cy, Z_IT)
        J.append(f'tl.to("#cam", {{ x: {x2:.1f}, y: {y2:.1f}, scale: {Z_IT:.3f}, duration: .6, ease: "power2.out" }}, 0);')
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
def wblink(t0, t1, per=.28):      # Italien blinkt weiß (Bild 0 / Loop)
    n = max(1, int((t1 - t0) / per) // 2 * 2 - 1)
    J.append(f'tl.fromTo("#itwhite", {{ opacity: 0 }}, {{ opacity: 1, duration: {per}, yoyo: true, repeat: {n}, ease: "steps(1)", immediateRender: false }}, {F(t0)});')
    J.append(f'tl.set("#itwhite", {{ opacity: 0 }}, {F(t1)});')
wblink(.15, st("s2")); wblink(LOOP_T, END)
# s3: Welterbe-Fahnen + 62 Sterne nacheinander
for k_ in range(len(SITES)): show(f"ws{k_}", st("s3") + .25 + .2 * k_, en("s3"), .25)
dt = (t_mehr3 - .1 - t_62) / 62
for k, _ in enumerate(STARS):
    J.append(f'tl.fromTo("#st{k}", {{ scale: 0, transformOrigin: "50% 50%" }}, {{ scale: 1, duration: .18, ease: "back.out(3)" }}, {F(t_62 + k * dt)});')
J.append(f'tl.set("#stars", {{ opacity: 0 }}, {F(en("s3"))});')
# s5: Mini-Länder blinken
J.append(f'tl.set("#dot-sm", {{ opacity: 1 }}, {F(t_san5 - .05)}); tl.set("#dot-va", {{ opacity: 1 }}, {F(t_vat5 - .05)});')
J.append(f'tl.fromTo("#dot-sm", {{ fill: "#e63946" }}, {{ fill: "#ffffff", duration: .2, yoyo: true, repeat: 7, ease: "steps(1)", immediateRender: false }}, {F(t_san5)});')
J.append(f'tl.fromTo("#dot-va", {{ fill: "#ffd166" }}, {{ fill: "#e63946", duration: .2, yoyo: true, repeat: 15, ease: "steps(1)", immediateRender: false }}, {F(t_vat5)});')
J.append(f'tl.set(["#dot-sm", "#dot-va"], {{ opacity: 0 }}, {F(en("s5"))});')
# s6: Stiefel kickt
J.append(f'tl.fromTo(["#c-it", "#itwhite"], {{ rotation: 0 }}, {{ rotation: -9, duration: .16, yoyo: true, repeat: 1, ease: "power2.out", svgOrigin: "508 318", immediateRender: false }}, {F(st("s6") + .15)});')
# s7: Besitzer-Fahnen
for k, (cid, _) in enumerate(RUND):
    t1 = TR[RUND[k + 1][0]] if k + 1 < len(RUND) else en("s7")
    show(f"p-{cid}", TR[cid] + .03, t1, .22)
# s8: Japan blinkt, Globi-Fahne, Russland blinkt
blink("#c-jp", JP_COL, "#ffd166", st("s8"), t_auf8 - .05)
show("p-globi", t_auf8, en("s8"), .25)
blink("#c-ru", GLOBI_COL, "#ffd166", t_auf8, t_glo8 + .4, .2)
# s9: Weltansicht – alle Fahnen, Japan FREI!, Italien?, freie Länder blitzen
for cid in owned: show(f"pw-{cid}", st("s9") + .05, en("s9"), .25)
for id_ in ("pw-globi", "pw-jp"): show(id_, st("s9") + .05, en("s9"), .25)
blink("#c-jp", JP_COL, "#ffd166", st("s9"), en("s9")); wblink(st("s9") + .1, en("s9"))
random.seed(9)
free = [c for c in K if c not in owned and c not in ("ru", "jp", "it", "sm", "va") and K[c]["bbox"][2] - K[c]["bbox"][0] > 10]
used = set(); t = t_noch9 + .05
while t < en("s9") - .2:
    cid = random.choice(free); used.add(cid)
    J.append(f'tl.fromTo("#c-{cid}", {{ fill: "{FREE_COL}" }}, {{ fill: "#ffffff", duration: .1, yoyo: true, repeat: 1, immediateRender: false }}, {F(t)});')
    t += .07
for cid in used: J.append(f'tl.set("#c-{cid}", {{ fill: "{FREE_COL}" }}, {F(en("s9"))});')

# ---------- HTML-Ebenen ----------
def ui(id_, t0, t1, inner, style): return f'<div id="{id_}" class="ui clip" data-start="{F(t0)}" data-duration="{F(max(.05, t1 - t0))}" style="{style}">{inner}</div>\n'
def chip(id_, txt, bg="#fff", fg="#111", size=44, extra=""):
    return f'<div id="{id_}" style="display:inline-block;max-width:1000px;background:{bg};color:{fg};font:900 {size}px/1.12 Inter,sans-serif;padding:12px 26px;border-radius:18px;border:5px solid #111;box-shadow:0 8px 0 #111;{extra}">{txt}</div>'
def pop(id_, t, s0=0, d=.3): J.append(f'tl.fromTo("#{id_}", {{ scale: {s0} }}, {{ scale: 1, duration: {d}, ease: "back.out(2.5)", immediateRender: false }}, {F(t)});')
html = ""
CAP_TOP = 1065          # Untertitel 1065–1165 px
BAR_TOP = 1185          # Ladebalken 1185–1265 px (62–66 %)
LOW1, LOW2 = 1300, 1415  # Schilder darunter, enden vor ~1520 px (79 %)
HSZ = lambda txt: min(72, int(1380 / max(10, len(txt))))
HEAD = [("h1", 0, st("s2"), "WER BEKOMMT ITALIEN?", "#ffd166", "#111"),
        ("h2a", st("s2"), t_nur2 - .05, "ABONNIEREN + WUNSCHLAND", "#e63946", "#fff"),
        ("h2b", t_nur2 - .05, en("s2"), "NUR ABONNENTEN BEKOMMEN EIN LAND", "#ffd166", "#111"),
        ("h3", st("s3"), en("s3"), "62 WELTERBE – PLATZ 1", "#ffd166", "#111"),
        ("h4", st("s4"), en("s4"), "KÜCHE = KULTURERBE", "#fff", "#111"),
        ("h5", st("s5"), en("s5"), "2 LÄNDER IM LAND!", "#e63946", "#fff"),
        ("h6", st("s6"), en("s6"), "ERSTER = GANZER STIEFEL", "#06d6a0", "#111"),
        ("h7", st("s7"), en("s7"), f"{NOWN} BESITZER", "#fff", "#111"),
        ("h8a", st("s8"), t_auf8 - .05, "JAPAN: FREI!", "#fff", "#e63946"),
        ("h8b", t_auf8 - .05, en("s8"), "RUSSLAND: GLOBI", GLOBI_COL, "#111"),
        ("h9", st("s9"), en("s9"), f"NOCH {FREI} FREI", "#ffd166", "#111"),
        ("h10a", st("s10"), t_abo10 - .05, "WER BEKOMMT ITALIEN?", "#ffd166", "#111"),
        ("h10b", t_abo10 - .05, LOOP_T, "NUR ABONNENTEN BEKOMMEN EIN LAND", "#ffd166", "#111"),
        ("h10c", LOOP_T, END, "WER BEKOMMT ITALIEN?", "#ffd166", "#111")]
for id_, t0, t1, txt, bg, fg in HEAD:
    if t1 - t0 < .05: continue
    html += ui(id_, t0, t1, chip(f"{id_}-in", txt, bg, fg, HSZ(txt)), "left:30px;right:30px;top:110px;text-align:center")
    if id_ not in ("h1", "h10c"): J.append(f'tl.fromTo("#{id_}-in", {{ scale: 1.35 }}, {{ scale: 1, duration: .2, ease: "back.out(2)" }}, {F(t0)});')
# Quellenzeilen
def src(id_, t0, t1, txt):
    return ui(id_, t0, t1, f'<div style="display:inline-block;background:rgba(0,0,0,.6);border-radius:10px;padding:4px 14px;font:700 28px Inter,sans-serif;color:#fff">{txt}</div>', "left:40px;top:300px")
html += src("src3", st("s3"), en("s3"), D["fakten"][0]["quellenzeile"])
html += src("src4", st("s4"), en("s4"), D["fakten"][1]["quellenzeile"])
html += src("src5", t_vat5 - .05, en("s5"), "Vatikan 0,44 km² · San Marino 61 km²")
# Zähler oben rechts
CNT = f'<div style="display:inline-block;background:rgba(0,0,0,.65);border-radius:14px;padding:6px 18px;font:900 44px Inter,sans-serif;color:#fff"><span style="color:#06d6a0">{NOWN}</span>/{TOTAL}</div>'
html += ui("cntA", 0, st("s3"), CNT, "right:36px;top:300px"); html += ui("cntC", st("s10"), END, CNT, "right:36px;top:300px")

# Ladebalken „Land wird vergeben … ?“ (dauerhaft, 62–66 % Bildhöhe)
html += ui("lb", 0, END,
           '<div style="position:relative;margin:0 auto;width:780px;height:80px;background:#fff;border:6px solid #111;border-radius:40px;box-shadow:0 8px 0 #111;overflow:hidden">'
           '<div id="lbf" style="position:absolute;left:0;top:0;bottom:0;width:4%;background:#06d6a0"></div>'
           '<div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font:900 40px Inter,sans-serif;color:#111">'
           'LAND WIRD VERGEBEN …&nbsp;<span id="lbq" style="color:#e63946">?</span><span id="lb99" style="color:#e63946;display:none">99 %</span></div></div>',
           f"left:0;right:0;top:{BAR_TOP}px")
J.append(f'tl.fromTo("#lbf", {{ width: "3%" }}, {{ width: "7%", duration: .3, yoyo: true, repeat: {int(t_stf6 / .3) // 2 * 2 - 1}, ease: "sine.inOut" }}, 0);')
J.append(f'tl.to("#lbf", {{ width: "99%", duration: .45, ease: "power3.out" }}, {F(t_stf6 - .05)});')
J.append(f'tl.set("#lbq", {{ display: "none" }}, {F(t_stf6 - .05)}); tl.set("#lb99", {{ display: "inline" }}, {F(t_stf6 - .05)});')
J.append(f'tl.fromTo("#lb99", {{ opacity: 1 }}, {{ opacity: .3, duration: .3, yoyo: true, repeat: {max(1, int((LOOP_T - t_stf6) / .3) // 2 * 2 - 1)}, ease: "steps(1)", immediateRender: false }}, {F(t_stf6 + .5)});')
J.append(f'tl.set("#lbf", {{ width: "4%" }}, {F(LOOP_T)}); tl.set("#lbq", {{ display: "inline" }}, {F(LOOP_T)}); tl.set("#lb99", {{ display: "none", opacity: 1 }}, {F(LOOP_T)});')
J.append(f'tl.fromTo("#lbf", {{ width: "3%" }}, {{ width: "7%", duration: .3, yoyo: true, repeat: {max(1, int((END - LOOP_T) / .3) // 2 * 2 - 1)}, ease: "sine.inOut", immediateRender: false }}, {F(LOOP_T + .02)});')

# Bild 0 / Loop: großes „?“ auf dem Stiefel
QM = lambda id_: (f'<div id="{id_}" style="display:inline-block;font:900 300px/1 Inter,sans-serif;color:#ffd166;-webkit-text-stroke:22px #111;paint-order:stroke fill;'
                  'filter:drop-shadow(0 12px 0 rgba(0,0,0,.45))">?</div>')
for id_, t0, t1 in (("q0", 0, t_cut1), ("qL", LOOP_T, END)):
    html += ui(id_, t0, t1, QM(id_ + "-in"), f"left:{FX - 160}px;top:{FY - 200}px;width:320px;text-align:center")
    J.append(f'tl.fromTo("#{id_}-in", {{ rotation: -8 }}, {{ rotation: 8, duration: .35, yoyo: true, repeat: {max(1, int((t1 - t0) / .35) - 1)}, ease: "sine.inOut" }}, {F(t0)});')
J.append('tl.fromTo("#q0-in", { scale: 0 }, { scale: 1, duration: .3, ease: "back.out(3)", immediateRender: false }, .03);')
J.append(f'tl.fromTo("#qL-in", {{ scale: 0 }}, {{ scale: 1, duration: .3, ease: "back.out(3)", immediateRender: false }}, {F(LOOP_T + .05)});')

# Abo-Aufruf (Anfang bis Ende s2, Schluss ab „Abonnier“ in s10)
ABO = (chip("{id}-a", "🔔 ABONNIER", "#e63946", "#fff", 58) + '<div style="height:14px"></div>' +
       chip("{id}-b", "💬 + KOMMENTIER DEIN WUNSCHLAND", "#fff", "#111", 40))
html += ui("ab1", 0, en("s2"), ABO.replace("{id}", "ab1"), f"left:0;right:0;top:{LOW1}px;text-align:center")
html += ui("ab10", t_abo10 - .05, END, ABO.replace("{id}", "ab10"), f"left:0;right:0;top:{LOW1}px;text-align:center")
J.append(f'tl.to("#ab1-a", {{ scale: 1.08, duration: .35, yoyo: true, repeat: {int(t_abo2 / .35) // 2 * 2 - 1}, ease: "sine.inOut" }}, .4);')
J.append(f'tl.fromTo("#ab1-a", {{ scale: 1 }}, {{ scale: .82, duration: .09, yoyo: true, repeat: 1, ease: "power2.in", immediateRender: false }}, {F(t_abo2 + .12)});')   # Knopf wird gedrückt
J.append(f'tl.to("#ab10-a", {{ scale: 1.08, duration: .35, yoyo: true, repeat: {int((END - t_abo10) / .35) - 1}, ease: "sine.inOut" }}, {F(t_abo10 + .3)});')
pop("ab1-b", t_kom2 - .05, 1.4, .25); pop("ab10-a", t_abo10 - .05, 1.5, .2)
# Finger drückt den Abo-Knopf (s2)
html += ui("hand", t_abo2 - .35, t_kom2 - .05, '<div id="hand-in" style="font:400 120px/1 \'Noto Color Emoji\';display:inline-block">👆</div>', f"left:610px;top:{LOW1 + 40}px")
J.append(f'tl.fromTo("#hand-in", {{ x: 260, y: 260 }}, {{ x: 0, y: 0, duration: .35, ease: "power2.out" }}, {F(t_abo2 - .35)});')
J.append(f'tl.to("#hand-in", {{ y: -18, duration: .09, yoyo: true, repeat: 1 }}, {F(t_abo2 + .12)});')
# Sprechblase „ITALIEN!“ fliegt auf den Stiefel (s2)
html += ui("bub2", t_kom2 - .05, en("s2"), chip("bub2-in", "💬 „ITALIEN!“", "#fff", "#111", 64), f"left:0;right:0;top:{FY - 60}px;text-align:center")
J.append(f'tl.fromTo("#bub2-in", {{ x: 420, y: 520, scale: .4, rotation: 12 }}, {{ x: 0, y: 0, scale: 1, rotation: -4, duration: .4, ease: "back.out(1.6)" }}, {F(t_kom2 - .05)});')

# s3: Pokal „1“ landet auf dem Stiefel + Zähler 62
TROPHY = ('<svg viewBox="0 0 200 240" width="230" height="276" style="overflow:visible;filter:drop-shadow(0 10px 0 rgba(0,0,0,.45))">'
          '<path d="M40 20 H160 V70 Q160 140 100 150 Q40 140 40 70 Z" fill="#ffd166" stroke="#111" stroke-width="8" stroke-linejoin="round"/>'
          '<path d="M40 40 Q0 40 8 80 Q16 110 48 112 M160 40 Q200 40 192 80 Q184 110 152 112" fill="none" stroke="#111" stroke-width="9"/>'
          '<rect x="88" y="148" width="24" height="40" fill="#f4b400" stroke="#111" stroke-width="7"/>'
          '<rect x="50" y="186" width="100" height="34" rx="6" fill="#f4b400" stroke="#111" stroke-width="7"/>'
          '<text x="100" y="112" text-anchor="middle" style="font:900 84px Inter,sans-serif;fill:#111">1</text></svg>')
html += ui("tro3", st("s3") + .05, en("s3"), f'<div id="tro3-in" style="display:inline-block">{TROPHY}</div>', f"left:{FX - 440}px;top:{FY - 330}px")
J.append(f'tl.fromTo("#tro3-in", {{ y: -900, rotation: -20 }}, {{ y: 0, rotation: 0, duration: .45, ease: "bounce.out" }}, {F(st("s3") + .05)});')
html += ui("n62", t_62 - .05, en("s3"), f'<div id="n62-in" style="display:inline-block;background:#fff;border:6px solid #111;border-radius:22px;box-shadow:0 8px 0 #111;padding:6px 30px;font:900 70px/1.05 Inter,sans-serif;color:#111">⭐ <span id="n62-v">0</span> WELTERBE</div>', f"left:0;right:0;top:{LOW1}px;text-align:center")
J.append(f'(() => {{ const o = {{ v: 0 }}; tl.fromTo(o, {{ v: 0 }}, {{ v: 62, duration: {t_mehr3 - t_62:.2f}, ease: "none", onUpdate: () => {{ document.getElementById("n62-v").textContent = Math.round(o.v); }} }}, {F(t_62)}); }})();')
pop("n62-in", t_62 - .05, .4, .2)
html += ui("pl3", t_mehr3 - .05, en("s3"), chip("pl3-in", "🏆 PLATZ 1 DER WELT", "#ffd166", "#111", 54), f"left:0;right:0;top:{LOW2 + 10}px;text-align:center")
pop("pl3-in", t_mehr3 - .05)

# s4: Pizza rollt über die Karte, Nudeln regnen, Stempel
PIZZA = ('<svg viewBox="-110 -110 220 220" width="300" height="300" style="overflow:visible;filter:drop-shadow(0 10px 0 rgba(0,0,0,.4))">'
         '<circle r="104" fill="#e9a447" stroke="#111" stroke-width="7"/><circle r="84" fill="#d62828" stroke="#111" stroke-width="4"/>'
         + "".join(f'<ellipse cx="{x}" cy="{y}" rx="18" ry="12" fill="#fff3c4"/>' for x, y in ((-40, -30), (30, -50), (45, 25), (-20, 45), (0, 0), (-60, 20)))
         + "".join(f'<circle cx="{x}" cy="{y}" r="15" fill="#9b2226" stroke="#111" stroke-width="3"/>' for x, y in ((-10, -55), (55, -10), (15, 55), (-55, -5), (-30, 20), (25, 15)))
         + '<path d="M0 -104 V104 M-104 0 H104 M-74 -74 L74 74 M74 -74 L-74 74" stroke="#b5762a" stroke-width="3"/></svg>')
html += ui("piz4", st("s4"), en("s4"), f'<div id="piz4-in" style="display:inline-block">{PIZZA}</div>', f"left:{FX - 150}px;top:{FY - 150}px")
J.append(f'tl.fromTo("#piz4-in", {{ x: -900, rotation: -720 }}, {{ x: 0, rotation: 0, duration: .9, ease: "power2.out" }}, {F(st("s4"))});')
J.append(f'tl.fromTo("#piz4-in", {{ scale: 1 }}, {{ scale: 1.3, duration: .18, yoyo: true, repeat: 1, ease: "power2.out", immediateRender: false }}, {F(t_piz4 - .05)});')
random.seed(5); nud = ""
for k in range(26):
    x = random.uniform(20, 1030); wd = random.uniform(60, 110)
    nud += (f'<svg id="nu{k}" viewBox="0 0 100 40" width="{wd:.0f}" height="{wd * .4:.0f}" style="position:absolute;left:{x:.0f}px;top:-80px;overflow:visible">'
            f'<path d="M5 20 Q17 2 29 20 T53 20 T77 20 T95 20" fill="none" stroke="#111" stroke-width="11" stroke-linecap="round"/>'
            f'<path d="M5 20 Q17 2 29 20 T53 20 T77 20 T95 20" fill="none" stroke="#ffe08a" stroke-width="6" stroke-linecap="round"/></svg>')
    J.append(f'tl.fromTo("#nu{k}", {{ y: 0, rotation: 0 }}, {{ y: {random.uniform(1150, 1500):.0f}, rotation: {random.uniform(-400, 400):.0f}, duration: {random.uniform(1.4, 2.2):.2f}, ease: "power1.in" }}, {F(st("s4") + .3 + random.uniform(0, 1.2))});')
html += ui("nud4", st("s4") + .25, en("s4"), nud, "left:0;top:0;width:1080px;height:1180px;overflow:hidden")
html += ui("stp4", t_kul4 - .05, en("s4"), f'<div id="stp4-in" style="display:inline-block;transform:rotate(-10deg);background:rgba(255,255,255,.92);color:#1d4ed8;font:900 74px/1.05 Inter,sans-serif;padding:12px 34px;border:10px solid #1d4ed8;border-radius:22px;box-shadow:0 10px 0 #111;text-align:center">KULTURERBE<br>2025</div>', f"left:0;right:0;top:{LOW1 + 40}px;text-align:center")
J.append(f'tl.fromTo("#stp4-in", {{ scale: 2.4, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: .22, ease: "power4.in" }}, {F(t_kul4 - .05)});')

# s5: Lupe + Namensschilder + EXTRA!
LUPE = ('<svg viewBox="0 0 420 420" width="420" height="420" style="overflow:visible">'
        '<line x1="310" y1="310" x2="410" y2="410" stroke="#111" stroke-width="44" stroke-linecap="round"/>'
        '<line x1="310" y1="310" x2="405" y2="405" stroke="#8b5a2b" stroke-width="28" stroke-linecap="round"/>'
        '<circle cx="190" cy="190" r="170" fill="rgba(255,255,255,.06)" stroke="#111" stroke-width="30"/>'
        '<circle cx="190" cy="190" r="170" fill="none" stroke="#d9e2ec" stroke-width="16"/></svg>')
html += ui("lupe", t_san5 - .05, t_gib5 - .05, f'<div id="lupe-in" style="display:inline-block">{LUPE}</div>', f"left:{FX - 190}px;top:{FY - 190}px")
J.append(f'tl.fromTo("#lupe-in", {{ x: 300, y: -260, scale: .7 }}, {{ x: 0, y: 0, scale: 1, duration: .3, ease: "power2.out" }}, {F(t_san5 - .05)});')
J.append(f'tl.fromTo("#lupe-in", {{ scale: 1.25 }}, {{ scale: 1, duration: .25, ease: "back.out(2)", immediateRender: false }}, {F(t_kl5 - .05)});')
html += ui("nsm", t_san5 + .05, t_vat5 - .05, chip("nsm-in", "SAN MARINO · 61 km²", "#e63946", "#fff", 52), f"left:0;right:0;top:{FY + 230}px;text-align:center")
pop("nsm-in", t_san5 + .05)
html += ui("nva", t_vat5 + .05, t_kl5 - .05, chip("nva-in", "VATIKAN … WO?", "#ffd166", "#111", 56), f"left:0;right:0;top:{FY + 230}px;text-align:center")
pop("nva-in", t_vat5 + .05)
html += ui("kva", t_kl5 - .05, t_gib5 - .05, chip("kva-in", "VATIKAN · 0,44 km² · KLEINSTES LAND", "#ffd166", "#111", 40), f"left:0;right:0;top:{FY + 230}px;text-align:center")
pop("kva-in", t_kl5 - .05)
html += ui("ext5", t_gib5 - .05, en("s5"), f'<div id="ext5-in" style="display:inline-block;transform:rotate(-8deg);background:#ffd166;color:#e63946;font:900 130px/1 Inter,sans-serif;padding:10px 40px;border:10px solid #111;border-radius:26px;box-shadow:0 12px 0 #111">EXTRA!</div>', f"left:0;right:0;top:{LOW1 - 10}px;text-align:center")
J.append(f'tl.fromTo("#ext5-in", {{ scale: 2 }}, {{ scale: 1, duration: .25, ease: "back.out(2)" }}, {F(t_gib5 - .05)});')
html += ui("ext5b", t_gib5 + .2, en("s5"), chip("ext5b-in", "+ SAN MARINO + VATIKAN", "#fff", "#111", 44), f"left:0;right:0;top:{FY + 250}px;text-align:center")
pop("ext5b-in", t_gib5 + .2)

# s6: Fußball fliegt vom Zeh quer über die Karte, Kommentar-Blase, 99 %
BALL = ('<svg viewBox="-60 -60 120 120" width="120" height="120" style="overflow:visible">'
        '<circle r="54" fill="#fff" stroke="#111" stroke-width="7"/>'
        '<path d="M0 -20 L19 -6 L12 16 L-12 16 L-19 -6 Z" fill="#111"/>'
        '<path d="M0 -20 V-52 M19 -6 L50 -16 M12 16 L31 43 M-12 16 L-31 43 M-19 -6 L-50 -16" stroke="#111" stroke-width="6"/></svg>')
tx, ty = screen(*ORTE["zeh_kalabrien"], ITC[0] + 3, ITC[1] + 2, Z_IT * .85)
html += ui("ball6", st("s6") + .2, t_ita6 + .2, f'<div id="ball6-in" style="display:inline-block">{BALL}</div>', f"left:{tx - 60:.0f}px;top:{ty - 60:.0f}px")
J.append(f'tl.fromTo("#ball6-in", {{ x: 0, y: 0, rotation: 0 }}, {{ x: {-tx - 200:.0f}, y: {-ty + 320:.0f}, rotation: -900, duration: 1.0, ease: "power1.out" }}, {F(st("s6") + .3)});')
html += ui("bub6", t_ita6 - .05, en("s6"), chip("bub6-in", "💬 „ITALIEN!“ = 🥇", "#fff", "#111", 60), f"left:0;right:0;top:{LOW1}px;text-align:center")
pop("bub6-in", t_ita6 - .05)

# s7: Name + Land oben
for k, (cid, _) in enumerate(RUND):
    o = owned[cid]; t1 = TR[RUND[k + 1][0]] if k + 1 < len(RUND) else en("s7")
    html += ui(f"nm{cid}", TR[cid] + .03, t1, chip(f"nm{cid}-in", f'{o["land_de"]} · {o["name"]}', o["farbe"], "#111", 56), "left:0;right:0;top:300px;text-align:center")
    pop(f"nm{cid}-in", TR[cid] + .03, .5, .18)
# s8: FREI!-Stempel an Japan
html += ui("fr8", st("s8") + .05, t_auf8 - .05, '<div id="fr8-in" style="display:inline-block;transform:rotate(-8deg);background:#fff;color:#e63946;font:900 120px/1 Inter,sans-serif;padding:10px 34px;border:10px solid #e63946;border-radius:22px;box-shadow:0 10px 0 #111">FREI!</div>', f"left:80px;top:{FY + 110}px")
J.append(f'tl.fromTo("#fr8-in", {{ scale: 1.6 }}, {{ scale: 1, duration: .25, ease: "back.out(2)" }}, {F(st("s8") + .05)});')
html += ui("ru8", t_glo8 - .05, en("s8"), chip("ru8-in", "HOLT ES ZURÜCK! 💬 „RUSSLAND!“", "#fff", "#111", 46), f"left:0;right:0;top:{LOW1}px;text-align:center")
pop("ru8-in", t_glo8 - .05)
# s9: Zähler groß 5/195 → NOCH 190 FREI
html += ui("big9", st("s9") + .05, en("s9"),
           f'<div id="big9-in" style="display:inline-block;background:rgba(11,26,51,.88);border:6px solid #fff;border-radius:28px;padding:10px 40px">'
           f'<div style="font:900 120px/1 Inter,sans-serif;color:#fff"><span style="color:#06d6a0">{NOWN}</span>/{TOTAL}</div>'
           f'<div id="big9-f" style="font:900 64px/1.1 Inter,sans-serif;color:#ffd166;margin-top:6px;opacity:0">NOCH {FREI} FREI!</div></div>', f"left:0;right:0;top:{LOW1 - 10}px;text-align:center")
J.append(f'tl.fromTo("#big9-in", {{ scale: 0, y: -400 }}, {{ scale: 1, y: 0, duration: .35, ease: "back.out(1.8)" }}, {F(st("s9") + .05)});')
J.append(f'tl.fromTo("#big9-f", {{ opacity: 0, scale: 1.8 }}, {{ opacity: 1, scale: 1, duration: .25, ease: "back.out(2)", immediateRender: false }}, {F(t_noch9 - .05)});')
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

# ---------- Globi (stumm, Maskottchen) auf Russland ----------
GK = lambda k, X, Y: (X - 190 * k, Y - 490 * k)
GEST = [(t_auf8 + .1, en("s8") - t_auf8 - .2, "wave")]
gh = globi.build({}, END, GEST, left=0, top=0)
def gset(t, k, X, Y, op=1, rot=0): x, y = GK(k, X, Y); GJ.append(f'tl.set("#g-wrap", {{ x: {x:.0f}, y: {y:.0f}, scale: {k}, rotation: {rot}, opacity: {op} }}, {F(t)});')
GJ.append('tl.set("#g-wrap", { transformOrigin: "0 0", opacity: 0 }, 0);')
X8, Y8 = screen(RUF[0] - 75, RUF[1] + 30, *ctr(RU_BOX), Z_RU)
gset(t_auf8 - .05, .62, X8, min(Y8, 1000))
GJ.append(f'tl.fromTo("#g-wrap", {{ y: "+=260" }}, {{ y: "-=260", duration: .3, ease: "back.out(2)", immediateRender: false }}, {F(t_auf8 - .05)});')
gset(en("s8"), .62, X8, min(Y8, 1000), op=0)
gh = gh.replace('window.__timelines["globi"] = tl;', "\n      ".join(GJ) + '\n      window.__timelines["globi"] = tl;')
open("compositions/globi.html", "w", encoding="utf-8").write(gh)

# ---------- Untertitel: hart wechselnd, Schlüsselwörter ≥ 0,3 s ----------
HOT = {o["name"] for o in OWN} | {norm(o["land_de"]).upper() for o in OWN} | {"ITALIEN", "JAPAN", "RUSSLAND", "ABONNIER", "ABONNIERT", "ABONNENTEN", "GLOBI", "FREI",
       "62", "5", "195", "190", "WUNSCHLAND", "WELTERBESTÄTTEN", "KULTURERBE", "PIZZA", "SAN", "MARINO", "VATIKAN", "KLEINSTE", "EXTRA", "STIEFEL", "ZUERST", "LAND", "USA"}
caps = []
for sc in V["scenes"]:
    sid = sc["id"]; words = T[sid]["words"]; k = 0
    for disp, sp in sc["groups"]:
        dw = [d for d in disp.split() if any(ch.isalnum() for ch in d)]; swn = sp.split()
        idx = [*range(len(dw))] if len(dw) == len(swn) else [int(j * len(swn) / len(dw)) for j in range(len(dw))]
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
FXL = [("pop", 0.03, .55, .15), ("boing", .5, .3, .55)]
for t in CUTS:
    if t != LOOP_T: FXL.append(("swoosh", t - .05, .3, .5))
FXL += [("pop", t_abo2 + .12, .55, .15), ("whoosh", t_kom2 - .05, .2, .6), ("pop", t_kom2 - .1, .35, .15)]
FXL += [("hit", st("s3") + .4, .25, 1.6)] + [("tick", t_62 + k * (t_mehr3 - t_62) / 12, .14, .3) for k in range(12)] + [("chime", t_mehr3 - .05, .3, 1.4)]
FXL += [("whoosh", st("s4") - .3, .2, .6), ("splat", en("s4") - .35, .35, .4), ("boing", en("s4") - .3, .25, .3)]
FXL += [("riser", t_san5 - .4, .2, .8), ("tick", t_san5, .25, .5), ("klong", t_gib5 - .05, .3, 1.2)]
FXL += [("hit", st("s6") + .3, .45, 1.6), ("whoosh", st("s6") + .35, .4, .94), ("pop", t_ita6 - .05, .45, .15), ("chime", t_stf6 - .05, .3, 1.4)]
for cid, _ in RUND: FXL.append(("pop", TR[cid] + .03, .45, .15))
FXL += [("pop", st("s8") + .05, .5, .15), ("boing", t_auf8 - .05, .45, .55), ("wirbel", t_glo8 + .35, .45, min(2.04, st("s9") - t_glo8 - .25))]
FXL += [("hit", st("s9") + .05, .45, 1.6), ("blips", t_noch9 + .05, .3, 1.33)]
FXL += [("pop", t_abo10 - .05, .45, .15), ("boing", LOOP_T + .05, .3, .55)]
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
