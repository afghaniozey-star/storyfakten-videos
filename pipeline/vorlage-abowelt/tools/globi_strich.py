"""Globi als Strichmännchen (eigene Zeichnung). Gleiche Schnittstelle wie globi.py:
   import globi_strich as globi; globi.build(T, END, GEST, left, top)"""
import globi as _g
_ORIG = _g.svg

TIE, TIE_D, SHOE, SKIN = "#ff8a3d", "#e46f22", "#1d4ed8", "#fff7ec"
INK, HALO = "#111", "#fff"

def line(d, w=7):
    # weiße Kontur darunter, damit er auf dunklem Hintergrund sichtbar bleibt
    return (f'<path d="{d}" stroke="{HALO}" stroke-width="{w + 10}" stroke-linecap="round" stroke-linejoin="round" fill="none"/>'
            f'<path d="{d}" stroke="{INK}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round" fill="none"/>')

def svg():
    arm = lambda id_, x: (f'<g transform="translate({x} 285)"><g id="{id_}">{line("M0 0 L0 -140")}'
                          f'<circle cy="-148" r="17" fill="{SKIN}" stroke="{HALO}" stroke-width="16"/><circle cy="-148" r="17" fill="{SKIN}" stroke="{INK}" stroke-width="6"/></g></g>')
    mouth = 'transform="translate(220 205) scale(.62) translate(-220 -340)"'
    vis = _ORIG()
    vis = vis[vis.index('<path id="g-smile"'):vis.index('</g>\n  </g>\n  <g transform="rotate(-10 220 372)">')] + "</g>"
    return f'''<svg viewBox="0 0 440 600" width="420" height="573" style="overflow:visible;margin-top:-50px;margin-left:-20px">
  <g id="g-body">
   {line("M220 250 L220 430")}
   {line("M220 430 L172 560")}{line("M220 430 L268 560")}
   <ellipse cx="160" cy="566" rx="34" ry="16" fill="{SHOE}" stroke="{HALO}" stroke-width="6"/><ellipse cx="280" cy="566" rx="34" ry="16" fill="{SHOE}" stroke="{HALO}" stroke-width="6"/>
   <path d="M210 262 L230 262 L238 360 L220 384 L202 360 Z" fill="{TIE}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>
   <path d="M210 262 L230 262 L226 280 L214 280 Z" fill="{TIE_D}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>
  </g>
  <g id="g-head">
   <circle cx="220" cy="150" r="100" fill="{SKIN}" stroke="{HALO}" stroke-width="20"/>
   <circle cx="220" cy="150" r="100" fill="{SKIN}" stroke="{INK}" stroke-width="7"/>
   {line("M196 52 Q190 28 176 20", 6)}{line("M220 50 Q222 24 236 14", 6)}{line("M242 54 Q256 34 274 32", 6)}
   <ellipse cx="188" cy="185" rx="18" ry="10" fill="#ffb4a8" opacity=".7"/><ellipse cx="252" cy="185" rx="18" ry="10" fill="#ffb4a8" opacity=".7"/>
   <circle cx="192" cy="140" r="11" fill="{INK}"/><circle cx="248" cy="140" r="11" fill="{INK}"/>
   <circle cx="195" cy="136" r="3.5" fill="#fff"/><circle cx="251" cy="136" r="3.5" fill="#fff"/>
   <g id="g-lid"><rect x="176" y="124" width="32" height="32" rx="8" fill="{SKIN}"/><rect x="232" y="124" width="32" height="32" rx="8" fill="{SKIN}"/>
    <path d="M178 142 Q192 150 206 142 M234 142 Q248 150 262 142" stroke="{INK}" stroke-width="5" fill="none" stroke-linecap="round"/></g>
   <g id="g-brow"><path d="M176 112 Q192 104 206 110 M234 110 Q248 104 264 112" stroke="{INK}" stroke-width="6" stroke-linecap="round" fill="none"/></g>
   <g {mouth}>{vis}</g>
  </g>
  {arm("g-la", 204)}{arm("g-ra", 236)}
</svg>'''

_g.svg = svg
# Posen für Strichmännchen: Arme schräg nach außen, damit sie nicht über dem Gesicht liegen
_g.POSES.update({"rest": (200, 160, 0), "wave": (205, 50, 0), "point": (200, 62, 0.6), "shrug": (245, 115, 1),
                 "shock": (305, 55, 1), "scratch": (200, 20, 0.4), "think": (200, 330, 0.3), "both": (300, 60, 0.8)})
build = _g.build
POSES = _g.POSES
