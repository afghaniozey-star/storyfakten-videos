import re
def clamp_cam(J):
    """Kamerafahrten (#cam tl.to) enden spätestens beim nächsten Kamera-Ereignis (sonst überschreiben sie harte Schnitte)."""
    ev = []
    for i, j in enumerate(J):
        m = re.match(r'tl\.(to|set)\("#cam", \{.*?\}, ([0-9.]+)\);$', j)
        if m: ev.append((float(m.group(2)), i, m.group(1)))
    ev.sort()
    n = 0
    for k, (t0, i, kind) in enumerate(ev):
        if kind != "to": continue
        nxt = [t for t, _, _ in ev[k + 1:] if t > t0 + 1e-3]
        if not nxt: continue
        d = float(re.search(r'duration: ([0-9.]+)', J[i]).group(1))
        if t0 + d > nxt[0] - .01:
            J[i] = re.sub(r'duration: [0-9.]+', f'duration: {max(.05, nxt[0] - t0 - .02):.2f}', J[i], 1); n += 1
    print("Kamerafahrten gekürzt:", n)
