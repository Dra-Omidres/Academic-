# -*- coding: utf-8 -*-
"""Logo del Curso SEDA y fondo de Zoom.

Logo elegido por la Dra. Omidres el 11/10/2026: la propuesta «cuatro ejes» (un anillo de
cuatro tramos: obesidad, diabetes, nutrición y salud digital) con el logo de SEDA dentro.
El logo de SEDA se usa tal como lo envió la Sociedad (activos/logo-seda/logo-seda-original.webp):
solo se recorta su círculo, no se redibuja ni se recolorea.

Genera, en activos/logo/:
  logo-curso-seda.svg / .png           versión clara (fondos blancos)
  logo-curso-seda-oscuro.svg / .png    versión oscura (fondos verdes)
  simbolo-curso-seda.svg / .png        solo el anillo con el logo de SEDA
y en la raíz del proyecto:
  SEDA_Fondo_Zoom.png                  1920 × 1080, el fondo virtual para los docentes

Se renderiza con el Chromium instalado en el entorno.
"""
import base64, io, math, os, subprocess, tempfile
from PIL import Image, ImageDraw

AQUI = os.path.dirname(os.path.abspath(__file__))
SALIDA = os.path.join(AQUI, 'activos', 'logo')
CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'

TEAL='#0D5A62'; GOLD='#B8852B'; MINT='#C8E1DF'; INK='#1A2325'; MUTED='#5F7073'
MID='#3E8A90'; LIGHT='#7FB7B2'; GOLDL='#E9C27A'; MID_OSC='#5FA8AD'
FONT="'Liberation Sans', Arial, Helvetica, sans-serif"
SUB='OBESIDAD · DIABETES · NUTRICIÓN · SALUD DIGITAL'

# ---------- logo de SEDA: recorte circular, sin tocar el dibujo ----------
# El círculo exterior azul ocupa x 144–1452, y 262–1570 del original (medido sobre el archivo).
orig = Image.open(os.path.join(AQUI, 'activos', 'logo-seda', 'logo-seda-original.webp')).convert('RGBA')
cx, cy, r = (144+1452)/2, (262+1570)/2, (1452-144)/2 + 2
seda = orig.crop((int(cx-r), int(cy-r), int(cx+r), int(cy+r)))
mask = Image.new('L', (seda.width*4, seda.height*4), 0)
ImageDraw.Draw(mask).ellipse((0, 0, mask.width-1, mask.height-1), fill=255)
mask = mask.resize(seda.size, Image.LANCZOS)
seda.putalpha(mask)
seda = seda.resize((800, 800), Image.LANCZOS)
seda.save(os.path.join(AQUI, 'activos', 'logo-seda', 'logo-seda-circulo.png'))
buf = io.BytesIO(); seda.save(buf, 'PNG')
SEDA_URI = 'data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode()

# ---------- símbolo: anillo de cuatro tramos con SEDA dentro ----------
def arco(cx, cy, r, a0, a1, col, w):
    p = lambda a: (cx + r*math.cos(math.radians(a)), cy + r*math.sin(math.radians(a)))
    (x0, y0), (x1, y1) = p(a0), p(a1)
    return (f'<path d="M{x0:.1f} {y0:.1f} A{r} {r} 0 0 1 {x1:.1f} {y1:.1f}" stroke="{col}" '
            f'stroke-width="{w}" fill="none" stroke-linecap="round"/>')

def simbolo(oscuro=False):
    # caja de 132: anillo de radio 58 y trazo 12; el logo de SEDA ocupa el círculo interior
    cols = [MINT if oscuro else TEAL, MID_OSC if oscuro else MID, GOLD, LIGHT]
    anillo = ''.join(arco(66, 66, 58, -80+90*i, -10+90*i, cols[i], 12) for i in range(4))
    return anillo + f'<image href="{SEDA_URI}" x="20" y="20" width="92" height="92"/>'

def logo(oscuro=False):
    t = '#FFFFFF' if oscuro else INK; s = GOLDL if oscuro else TEAL; sub = MINT if oscuro else MUTED
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="720" height="140" viewBox="0 0 720 140">
<g transform="translate(4,4)">{simbolo(oscuro)}</g>
<text x="172" y="80" font-family="{FONT}" font-size="58" fill="{t}"><tspan>Curso </tspan><tspan font-weight="700" fill="{s}">SEDA</tspan></text>
<text x="174" y="112" font-family="{FONT}" font-size="14.5" letter-spacing="1.7" fill="{sub}">{SUB}</text></svg>'''

piezas = {
    'logo-curso-seda': (logo(), 720, 140),
    'logo-curso-seda-oscuro': (logo(True), 720, 140),
    'simbolo-curso-seda': (f'<svg xmlns="http://www.w3.org/2000/svg" width="140" height="140" '
                           f'viewBox="0 0 140 140"><g transform="translate(4,4)">{simbolo()}</g></svg>', 140, 140),
}

def render(svg_path, ancho, alto, png_path):
    """Chromium a 3× sobre fondo transparente; se recorta al tamaño exacto."""
    with tempfile.TemporaryDirectory() as tmp:
        html = os.path.join(tmp, 'p.html')
        open(html, 'w').write(f'<!doctype html><html><body style="margin:0;background:transparent">'
                              f'<img src="file://{svg_path}" style="width:{ancho*3}px;display:block">'
                              f'</body></html>')
        subprocess.run([CHROME, '--headless', '--no-sandbox', '--disable-gpu', '--hide-scrollbars',
                        '--default-background-color=00000000', '--allow-file-access-from-files',
                        f'--window-size={ancho*3+100},{alto*3+400}', f'--screenshot={png_path}',
                        'file://' + html], check=True, capture_output=True)
    Image.open(png_path).crop((0, 0, ancho*3, alto*3)).save(png_path)

for nombre, (svg, w, h) in piezas.items():
    ruta = os.path.join(SALIDA, nombre + '.svg')
    open(ruta, 'w').write(svg)
    render(ruta, w, h, os.path.join(SALIDA, nombre + '.png'))

# ---------- fondo de Zoom 1920×1080 ----------
# Claro y liso para que la persona destaque; el logo arriba a la izquierda, lejos de la cara.
W, H = 1920, 1080
fondo = Image.new('RGB', (W, H)); px = fondo.load()
c0, c1 = (255, 255, 255), (227, 239, 237)
fx, fy, R = W*0.5, H*0.6, math.hypot(W*0.55, H*0.75)
for y in range(H):
    for x in range(W):
        t = min(1, math.hypot(x-fx, y-fy)/R); t = t*t*(3-2*t)
        px[x, y] = tuple(int(c0[i] + (c1[i]-c0[i])*t) for i in range(3))
lg = Image.open(os.path.join(SALIDA, 'logo-curso-seda.png')).convert('RGBA')
lg = lg.resize((660, int(660*lg.height/lg.width)), Image.LANCZOS)
fondo.paste(lg, (64, 52), lg)
d = ImageDraw.Draw(fondo)
d.rectangle([0, H-14, W, H-10], fill=GOLD); d.rectangle([0, H-10, W, H], fill=TEAL)
fondo.save(os.path.join(AQUI, 'SEDA_Fondo_Zoom.png'))
print('logo y fondo generados')
