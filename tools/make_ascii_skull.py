"""Convierte el GIF de la calavera en un GIF animado de arte ASCII (blanco sobre negro).

Uso: python3 -I make_ascii_skull.py <entrada.gif> <salida.gif>
"""
import sys
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageSequence

SRC, DST = sys.argv[1], sys.argv[2]
COLS = 110
CROP = (18, 82, 288, 408)  # solo la pantalla negra, sin marco ni ruido del CRT
FLOOR = 70  # por debajo de este gris es fondo
STEP = 2  # usa 1 de cada STEP frames para reducir el peso
FONT = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 9)
RAMP = " .:-=+*/\\|()1{}[]#%@"  # claro -> denso, como la calavera de referencia
FG, BG = (214, 255, 226), (0, 0, 0)  # verde casi blanco

cw = int(FONT.getlength("M"))
ch = 11
src = Image.open(SRC)
cwid, chei = CROP[2] - CROP[0], CROP[3] - CROP[1]
rows = round(COLS * chei / cwid * cw / ch)
out_size = (COLS * cw, rows * ch)

frames = []
for i, fr in enumerate(ImageSequence.Iterator(src)):
    if i % STEP:
        continue
    g = fr.convert("L").crop(CROP).resize((COLS, rows), Image.LANCZOS)
    g = g.point(lambda v: 0 if v < FLOOR else min(255, (v - FLOOR) * 255 // (200 - FLOOR)))
    img = Image.new("RGB", out_size, BG)
    d = ImageDraw.Draw(img)
    px = g.load()
    for y in range(rows):
        line = "".join(RAMP[px[x, y] * (len(RAMP) - 1) // 255] for x in range(COLS))
        d.text((0, y * ch), line, font=FONT, fill=FG)
    frames.append(img.convert("P", palette=Image.ADAPTIVE, colors=4))

frames[0].save(DST, save_all=True, append_images=frames[1:], duration=60 * STEP, loop=0, optimize=True)
print(DST, len(frames), "frames", out_size)
