#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Genera el icono del restaurante con Pillow (sin SVG, sin dependencias externas).
Produce: icono_restaurante.ico (multi-resolucion) + icono_restaurante.png (512x512)
"""
import subprocess, sys

def pip_install(pkg):
    subprocess.run([sys.executable, "-m", "pip", "install", pkg, "--quiet"], check=True)

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("[ERROR] Pillow no está instalado.")
    print("Instala Pillow manualmente y vuelve a ejecutar:")
    print(f"  {sys.executable} -m pip install pillow")
    sys.exit(1)

import math

# ── Colores del sistema ───────────────────────────────────────────
NARANJA      = (255, 159,  67, 255)   # #FF9F43
NARANJA_OSC  = (230, 126,  34, 255)   # #E67E22
OSCURO       = ( 44,  62,  80, 255)   # #2C3E50
BLANCO       = (255, 255, 255, 255)
TRANSP       = (  0,   0,   0,   0)

SIZE = 512
cx, cy = SIZE // 2, SIZE // 2


def dibujar_icono(size: int = 512) -> Image.Image:
    img  = Image.new("RGBA", (size, size), TRANSP)
    draw = ImageDraw.Draw(img)
    s    = size / 512          # factor de escala

    def sc(v):  return int(v * s)
    def scp(x, y): return (sc(x), sc(y))

    # ── Circulo exterior (naranja) ────────────────────────────────
    r_out = sc(248)
    draw.ellipse([cx - r_out, cy - r_out, cx + r_out, cy + r_out], fill=NARANJA)

    # ── Circulo interior (oscuro) ─────────────────────────────────
    r_in = sc(228)
    draw.ellipse([cx - r_in, cy - r_in, cx + r_in, cy + r_in], fill=OSCURO)

    # ── Domo / cloche ─────────────────────────────────────────────
    dome_top    = sc(195)
    dome_bottom = sc(310)
    dome_left   = sc(136)
    dome_right  = sc(376)

    draw.ellipse(
        [dome_left, dome_bottom - sc(14),
         dome_right, dome_bottom + sc(14)],
        fill=NARANJA
    )
    draw.chord(
        [dome_left, dome_top, dome_right, dome_bottom + sc(30)],
        start=180, end=360,
        fill=NARANJA
    )

    # Asa del domo
    draw.rounded_rectangle(
        [cx - sc(18), cy - sc(130), cx + sc(18), cy - sc(108)],
        radius=sc(9), fill=NARANJA
    )
    draw.ellipse(
        [cx - sc(22), cy - sc(138), cx + sc(22), cy - sc(120)],
        fill=NARANJA_OSC
    )

    # ── Plato base ────────────────────────────────────────────────
    draw.ellipse(
        [cx - sc(130), sc(317), cx + sc(130), sc(353)],
        fill=NARANJA_OSC
    )
    draw.ellipse(
        [cx - sc(130), sc(320), cx + sc(130), sc(344)],
        fill=NARANJA
    )

    # ── Tenedor (izquierda) ───────────────────────────────────────
    fx, fy = sc(160), sc(290)
    grosor = sc(9)
    # Mango
    draw.rounded_rectangle(
        [fx - grosor//2, fy, fx + grosor//2, fy + sc(65)],
        radius=sc(5), fill=NARANJA
    )
    # Dientes
    for dx in [-sc(12), -sc(4), sc(4)]:
        draw.rounded_rectangle(
            [fx + dx, fy - sc(58), fx + dx + sc(5), fy - sc(10)],
            radius=sc(3), fill=NARANJA
        )
    # Cuello
    draw.rectangle(
        [fx - grosor//2, fy - sc(12), fx + grosor//2, fy + sc(4)],
        fill=NARANJA
    )

    # ── Cuchillo (derecha) ────────────────────────────────────────
    kx, ky = sc(352), sc(290)
    # Mango
    draw.rounded_rectangle(
        [kx - grosor//2, ky, kx + grosor//2, ky + sc(65)],
        radius=sc(5), fill=NARANJA
    )
    # Hoja (triangulo)
    blade = [
        (kx - grosor//2, ky - sc(10)),
        (kx + sc(14),    ky - sc(55)),
        (kx + grosor//2, ky - sc(10)),
    ]
    draw.polygon(blade, fill=NARANJA)

    # ── Texto "RESTAURANTE" ───────────────────────────────────────
    try:
        font = ImageFont.truetype("arialbd.ttf", sc(30))
    except Exception:
        try:
            font = ImageFont.truetype("arial.ttf", sc(30))
        except Exception:
            font = ImageFont.load_default()

    texto = "RESTAURANTE"
    bbox  = draw.textbbox((0, 0), texto, font=font)
    tw    = bbox[2] - bbox[0]
    draw.text(
        (cx - tw // 2, sc(400)),
        texto, fill=NARANJA, font=font
    )

    # ── Estrellas decorativas ─────────────────────────────────────
    for sx, sy in [(sc(105), sc(170)), (sc(395), sc(170))]:
        draw.text((sx, sy), "*", fill=(*NARANJA[:3], 180), font=font)

    return img


def main():
    print("[*] Generando icono del restaurante con Pillow...")

    img = dibujar_icono(SIZE)

    # Guardar PNG
    img.save("icono_restaurante.png", format="PNG")
    print("[OK] icono_restaurante.png guardado (512x512)")

    # Guardar ICO multi-resolucion
    sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
    img.save("icono_restaurante.ico", format="ICO", sizes=sizes)
    print("[OK] icono_restaurante.ico guardado (multi-resolucion)")


if __name__ == "__main__":
    main()
