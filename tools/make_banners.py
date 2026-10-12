"""Genera banners SVG animados de arte ASCII (cabecera y pie) en verde casi blanco sobre negro.

Uso: python3 -I make_banners.py <carpeta_assets>
Las animaciones son CSS dentro del SVG: GitHub las respeta cuando va como <img>.
"""
import math
import random
import sys

OUT = sys.argv[1]
W, H = 900, 96
COLS, ROWS = 150, 8
CW, CH = W / COLS, H / ROWS
FG = "#D6FFE2"
RAMP = " .:-=+*/\\|()1{}[]#%@01"


def banner(path, label, seed):
    rnd = random.Random(seed)
    rows = []
    for r in range(ROWS):
        line = []
        for c in range(COLS):
            # denso en los bordes, vacio en el centro donde va el texto
            edge = abs(c - COLS / 2) / (COLS / 2)
            p = max(0.0, edge**1.6 - 0.08) + 0.05 * math.sin(c / 7 + r)
            idx = int(min(1.0, max(0.0, p * rnd.uniform(0.5, 1.4))) * (len(RAMP) - 1))
            line.append(RAMP[idx])
        rows.append("".join(line))

    css = [
        "text{font-family:'DejaVu Sans Mono','Courier New',monospace;fill:%s;white-space:pre}" % FG,
        ".r{font-size:%.1fpx;opacity:.55;animation:f 3.2s ease-in-out infinite}" % (CH * 0.95),
        "@keyframes f{0%,100%{opacity:.25}50%{opacity:.8}}",
        ".s{animation:m 4s linear infinite}",
        "@keyframes m{from{transform:translateX(-120px)}to{transform:translateX(%dpx)}}" % (W + 120),
        ".t{font-size:17px;font-weight:bold;letter-spacing:5px;animation:g 5s steps(1) infinite}",
        "@keyframes g{0%,92%,100%{opacity:1;transform:translateX(0)}94%{opacity:.5;transform:translateX(-3px)}96%{opacity:1;transform:translateX(3px)}98%{opacity:.6}}",
    ]
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        f"<style>{''.join(css)}</style>",
        f'<rect width="{W}" height="{H}" fill="#000"/>',
    ]
    for r, line in enumerate(rows):
        delay = -rnd.uniform(0, 3.2)
        out.append(
            f'<text class="r" x="0" y="{(r + 0.85) * CH:.1f}" textLength="{W}" '
            f'lengthAdjust="spacing" style="animation-delay:{delay:.2f}s">{line.replace("&", "&amp;").replace("<", "&lt;")}</text>'
        )
    out.append('<g class="s"><rect width="60" height="%d" fill="%s" opacity=".08"/></g>' % (H, FG))
    out.append(f'<text class="t" x="{W/2}" y="{H/2 + 6}" text-anchor="middle">{label}</text>')
    out.append("</svg>")
    open(path, "w").write("\n".join(out))
    print(path)


banner(f"{OUT}/header.svg", "[ HELLO WORLD.. GIANPIERE ]", 7)
banner(f"{OUT}/footer.svg", "&gt; EOF // GIANPIERE OREJUELA", 21)
