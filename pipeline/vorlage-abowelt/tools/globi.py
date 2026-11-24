"""Globi – sprechendes Maskottchen. build(...) liefert compositions/globi.html.
Mund folgt der Lautstärke der Sprachspur, Arme/Augenbrauen folgen einer Gesten-Liste."""
import json, math, subprocess
import numpy as np

FPS = 30
HOODIE, HOODIE_D = "#ff8a3d", "#e46f22"

def envelope(T, end):
    n = int(end * FPS) + 2
    env = np.zeros(n)
    for sid, v in T.items():
        a = np.frombuffer(subprocess.check_output(["ffmpeg", "-v", "quiet", "-i", f"assets/vo/{sid}.mp3", "-f", "f32le", "-ac", "1", "-ar", "16000", "-"]), np.float32)
        hop = 16000 // FPS
        rms = np.array([np.sqrt(np.mean(a[i:i + hop] ** 2)) for i in range(0, len(a) - hop, hop)])
        off = int(round((v["start"] + v["lead"]) * FPS))
        m = min(len(rms), n - off)
        env[off:off + m] = np.maximum(env[off:off + m], rms[:m])
    ref = np.percentile(env[env > 0.005], 92) if np.any(env > 0.005) else 1
    env = np.clip(env / ref, 0, 1)
    sm = np.convolve(env, [0.25, 0.5, 0.25], "same")
    return [round(float(x), 2) if x > 0.12 else 0 for x in sm]

RHUBARB = ["/opt/rhubarb/Rhubarb-Lip-Sync-1.14.0-Linux/rhubarb"]

def visemes(T, end):
    """Mundform pro Frame (Rhubarb, Buchstaben A–H, X). None, wenn Rhubarb fehlt."""
    import os, tempfile, glob
    exe = next((x for x in RHUBARB + glob.glob("/opt/rhubarb/*/rhubarb") if os.path.exists(x)), None)
    if not exe: return None
    n = int(end * FPS) + 2
    vis = ["X"] * n
    for sid, v in T.items():
        wav = os.path.join(tempfile.gettempdir(), f"rh-{sid}.wav")
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", f"assets/vo/{sid}.mp3", "-ar", "16000", "-ac", "1", wav], check=True)
        out = json.loads(subprocess.check_output([exe, "-r", "phonetic", "-f", "json", "-q", wav]))
        off = v["start"] + v["lead"]
        for c in out["mouthCues"]:
            for f in range(int((off + c["start"]) * FPS), min(n, int((off + c["end"]) * FPS) + 1)):
                vis[f] = c["value"]
    return "".join(vis)

# Arm-Winkel: 0 = nach oben, 180 = nach unten (im Uhrzeigersinn)
POSES = {
    "rest": (200, 160, 0), "wave": (200, 25, 0), "point": (200, 20, 0.6), "shrug": (285, 75, 1),
    "shock": (330, 30, 1), "scratch": (200, 345, 0.4), "think": (200, 320, 0.3), "both": (320, 40, 0.8),
}

def track(end, gestures):
    """gestures: Liste (start, dauer, pose). Weiche Übergänge, sonst 'rest'."""
    n = int(end * FPS) + 2
    la = np.full(n, 200.0); ra = np.full(n, 160.0); br = np.zeros(n)
    for t0, d, pose in gestures:
        L, R, B = POSES[pose]
        f0, f1 = int(t0 * FPS), int((t0 + d) * FPS)
        ramp = 5
        for f in range(max(0, f0 - ramp), min(n, f1 + ramp)):
            k = min(1, (f - (f0 - ramp)) / ramp, ((f1 + ramp) - f) / ramp)
            k = 0.5 - 0.5 * math.cos(math.pi * max(0, min(1, k)))
            wob = 12 * math.sin((f - f0) / FPS * 14) if pose == "wave" else 0
            la[f] = la[f] * (1 - k) + L * k; ra[f] = ra[f] * (1 - k) + (R + wob) * k; br[f] = max(br[f], B * k)
    return [round(x) for x in la], [round(x) for x in ra], [round(x, 2) for x in br]

def blinks(end):
    out, t = [], 1.3
    while t < end:
        out.append(round(t, 2)); t += 2.6 + (len(out) * 0.73) % 1.4
    return out

def svg():
    arm = lambda id_, x: (f'<g transform="translate({x} 470)"><g id="{id_}"><rect x="-17" y="-80" width="34" height="100" rx="17" fill="{HOODIE}"/>'
                          f'<g transform="translate(0 -92)"><circle r="27" fill="#fff" stroke="#cfd8e3" stroke-width="4"/><rect x="-7" y="-40" width="14" height="34" rx="7" fill="#fff" stroke="#cfd8e3" stroke-width="4"/></g></g></g>')
    return f'''<svg viewBox="0 0 440 600" width="340" height="464" style="overflow:visible">
  <g id="g-body"><path d="M95 600 Q95 455 220 440 Q345 455 345 600 Z" fill="{HOODIE}"/>
   <path d="M150 452 Q220 520 290 452 Q220 485 150 452 Z" fill="#fff" opacity=".35"/>
   <path d="M200 470 L196 540 M240 470 L244 540" stroke="#fff" stroke-width="6" stroke-linecap="round"/><circle cx="196" cy="545" r="7" fill="#fff"/><circle cx="244" cy="545" r="7" fill="#fff"/></g>
  {arm("g-la", 130)}{arm("g-ra", 310)}
  <g id="g-head">
   <g transform="rotate(-10 220 372)"><path d="M15 372 A205 46 0 0 1 425 372" fill="none" stroke="#5fd3ff" stroke-width="11" stroke-linecap="round" opacity=".85"/></g>
   <circle cx="220" cy="265" r="150" fill="#2f8fe8"/>
   <path d="M108 205 Q150 158 205 182 Q228 230 190 250 Q148 262 122 240 Z" fill="#46c46a"/><path d="M262 300 Q305 278 334 310 Q324 362 282 372 Q250 350 262 300 Z" fill="#46c46a"/>
   <path d="M148 330 Q175 318 186 345 Q170 366 148 352 Z" fill="#46c46a"/><path d="M250 150 Q290 140 300 170 Q280 185 255 175 Z" fill="#46c46a"/>
   <path d="M120 200 Q140 150 190 132" stroke="#fff" stroke-width="14" stroke-linecap="round" fill="none" opacity=".35"/>
   <circle cx="220" cy="265" r="150" fill="none" stroke="#1b6cc0" stroke-width="7"/>
   <circle cx="174" cy="246" r="34" fill="#fff"/><circle cx="266" cy="246" r="34" fill="#fff"/>
   <circle cx="181" cy="252" r="15" fill="#111"/><circle cx="259" cy="252" r="15" fill="#111"/><circle cx="186" cy="246" r="5" fill="#fff"/><circle cx="264" cy="246" r="5" fill="#fff"/>
   <g id="g-lid"><rect x="138" y="210" width="74" height="74" rx="22" fill="#2f8fe8"/><rect x="228" y="210" width="74" height="74" rx="22" fill="#2f8fe8"/><path d="M142 250 Q174 262 208 250 M232 250 Q266 262 298 250" stroke="#0d3b6e" stroke-width="6" fill="none" stroke-linecap="round"/></g>
   <rect x="133" y="207" width="82" height="80" rx="24" fill="none" stroke="#111" stroke-width="8"/><rect x="225" y="207" width="82" height="80" rx="24" fill="none" stroke="#111" stroke-width="8"/><path d="M215 240 L225 240" stroke="#111" stroke-width="8"/>
   <g id="g-brow"><path d="M145 192 Q172 178 200 190 M240 190 Q268 178 295 192" stroke="#0d3b6e" stroke-width="9" stroke-linecap="round" fill="none"/></g>
   <path id="g-smile" d="M178 330 Q220 372 262 330 Q220 352 178 330 Z" fill="#7a1f1f"/>
   <g id="g-open"><ellipse id="g-mo" cx="220" cy="338" rx="28" ry="10" fill="#7a1f1f"/><ellipse id="g-tg" cx="220" cy="346" rx="15" ry="5" fill="#ff8fa0"/></g>
   <g id="g-vis">
    <g id="m-X"><path d="M178 330 Q220 372 262 330 Q220 352 178 330 Z" fill="#7a1f1f"/></g>
    <g id="m-A"><path d="M186 340 Q220 352 254 340" stroke="#7a1f1f" stroke-width="8" fill="none" stroke-linecap="round"/></g>
    <g id="m-B"><ellipse cx="220" cy="340" rx="26" ry="10" fill="#7a1f1f"/><rect x="200" y="331" width="40" height="7" rx="3" fill="#fff"/></g>
    <g id="m-C"><ellipse cx="220" cy="342" rx="28" ry="17" fill="#7a1f1f"/><rect x="200" y="327" width="40" height="7" rx="3" fill="#fff"/><ellipse cx="220" cy="352" rx="14" ry="5" fill="#ff8fa0"/></g>
    <g id="m-D"><ellipse cx="220" cy="346" rx="32" ry="27" fill="#7a1f1f"/><rect x="198" y="321" width="44" height="8" rx="3" fill="#fff"/><ellipse cx="220" cy="362" rx="17" ry="8" fill="#ff8fa0"/></g>
    <g id="m-E"><ellipse cx="220" cy="344" rx="18" ry="20" fill="#7a1f1f"/><ellipse cx="220" cy="354" rx="10" ry="5" fill="#ff8fa0"/></g>
    <g id="m-F"><ellipse cx="220" cy="342" rx="11" ry="12" fill="#7a1f1f" stroke="#c0392b" stroke-width="4"/></g>
    <g id="m-G"><ellipse cx="220" cy="340" rx="25" ry="11" fill="#7a1f1f"/><rect x="198" y="330" width="44" height="9" rx="3" fill="#fff"/><path d="M196 348 Q220 356 244 348" stroke="#c0392b" stroke-width="5" fill="none"/></g>
    <g id="m-H"><ellipse cx="220" cy="342" rx="27" ry="18" fill="#7a1f1f"/><rect x="200" y="326" width="40" height="7" rx="3" fill="#fff"/><ellipse cx="220" cy="336" rx="12" ry="6" fill="#ff8fa0"/></g>
   </g>
  </g>
  <g transform="rotate(-10 220 372)"><path d="M15 372 A205 46 0 0 0 425 372" fill="none" stroke="#5fd3ff" stroke-width="11" stroke-linecap="round"/></g>
</svg>'''

def build(T, end, gestures, left=18, top=1222):
    env = envelope(T, end)
    vis = visemes(T, end)
    la, ra, br = track(end, gestures)
    bl = blinks(end)
    return f'''<template>
  <style>
    #root {{ position: absolute; inset: 0; pointer-events: none; }}
    #g-wrap {{ position: absolute; left: {left}px; top: {top}px; width: 340px; height: 464px; filter: drop-shadow(0 12px 18px rgba(0,0,0,.35)); }}
  </style>
  <div id="root" data-composition-id="globi" data-width="1080" data-height="1920">
    <div id="g-wrap" class="clip" data-start="0" data-duration="{end:.2f}" data-layout-ignore>{svg()}</div>
  </div>
  <script>
    (function () {{
      const VIS = {json.dumps(vis)};
      const ENV = {json.dumps(env)}, LA = {json.dumps(la)}, RA = {json.dumps(ra)}, BR = {json.dumps(br)}, BL = {json.dumps(bl)};
      const $ = (i) => document.getElementById(i);
      const draw = (t) => {{
        const f = Math.max(0, Math.min(ENV.length - 1, Math.round(t * {FPS})));
        const v = ENV[f];
        if (VIS) {{
          $("g-smile").style.display = "none"; $("g-open").style.display = "none";
          const m = VIS[Math.min(f, VIS.length - 1)];
          ["X","A","B","C","D","E","F","G","H"].forEach((k) => ($("m-" + k).style.display = k === m ? "" : "none"));
        }} else {{
          $("g-vis").style.display = "none";
          $("g-smile").style.display = v > 0 ? "none" : "";
          $("g-open").style.display = v > 0 ? "" : "none";
        }}
        $("g-mo").setAttribute("ry", (6 + 24 * v).toFixed(1)); $("g-mo").setAttribute("rx", (24 + 8 * v).toFixed(1));
        $("g-tg").setAttribute("cy", (338 + 14 * v).toFixed(1));
        $("g-la").setAttribute("transform", "rotate(" + LA[Math.min(f, LA.length - 1)] + ")");
        $("g-ra").setAttribute("transform", "rotate(" + RA[Math.min(f, RA.length - 1)] + ")");
        $("g-brow").setAttribute("transform", "translate(0 " + (-14 * BR[Math.min(f, BR.length - 1)]).toFixed(1) + ")");
        const blink = BL.some((b) => t >= b && t < b + 0.12);
        $("g-lid").style.display = blink ? "" : "none";
        const bob = Math.sin(t * 2.4) * 2.5 + v * 3;
        $("g-head").setAttribute("transform", "rotate(" + bob.toFixed(2) + " 220 400)");
      }};
      const tl = gsap.timeline({{ paused: true }});
      const o = {{ t: 0 }};
      tl.fromTo(o, {{ t: 0 }}, {{ t: {end:.2f}, duration: {end:.2f}, ease: "none", onUpdate: () => draw(o.t) }}, 0);
      draw(0);
      window.__timelines["globi"] = tl;
    }})();
  </script>
</template>
'''
