#!/usr/bin/env python3
"""Leitet aus einer Grundfarbe je Bereich eine Farbrampe nach dem KERN-Verfahren ab und daraus area, on und fg für hell und dunkel.

Aufruf: python3 skripte/farben.py "#4c8438" "#b4457a"
        python3 skripte/farben.py --rampe "#4c8438"   (zusätzlich alle 20 Stufen als OKLCH und Hex)
Gibt je Farbe den fertigen Block für bereiche[].farben als JSON aus; die Kontraste stehen auf stderr.

Verfahren (wie die Farbrampen des KERN-Kits, vgl. kern-ux.de, Design-System, Farbe):
- Gerechnet wird in OKLCH, nicht in sRGB oder HSL. Der Farbton (H) der Grundfarbe bleibt über die ganze Rampe gleich.
- Die Helligkeit (L) jeder Stufe ist fest: eine „universelle“ Skala von 025 bis 950, bei der jede Stufe über alle Farbtöne
  denselben Kontrast hat. Stufe 500 ist die Kontrastmitte (4,5:1 auf Weiß und auf Schwarz), 800 hell entspricht 200 dunkel.
  Die Skala unten ist der Mittelwert der elf Rampen aus @kern-ux/native 2.8.2.
- Das Chroma (C) folgt dem Profil der Kit-Rampen: Spitze um 550 bis 650, zu den Rändern abnehmend. Die Höhe des Profils
  wird so gewählt, dass die Rampe an der Helligkeit der Grundfarbe deren Chroma trifft. Farben außerhalb des sRGB-Raums
  werden durch Verringern des Chromas in den Raum geholt, L und H bleiben.
- Zuordnung: area = Stufe 500, on = Weiß, fg hell = Stufe 700, fg dunkel = Stufe 300 (die Spiegelung von 700).
  So verwendet auch KERN seine Aktionsfarbe: 700 im Hell-, 300 im Dunkelmodus.
"""
import json
import math
import sys

STUFEN = [25, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950]
# Universelle Helligkeit je Stufe (OKLCH L in Prozent), Mittel über die Rampen des Kits 2.8.2
HELLIGKEIT = [96.4, 93.8, 91.0, 86.5, 82.0, 78.1, 75.4, 70.8, 67.0, 63.2, 57.0, 53.5, 50.4, 46.9, 42.4, 38.6, 34.1, 30.1, 25.9, 20.9]
# Chroma-Profil je Stufe, normiert auf die Spitze (Mittel über die Rampen des Kits 2.8.2)
CHROMA_PROFIL = [0.07, 0.13, 0.19, 0.29, 0.39, 0.47, 0.53, 0.62, 0.70, 0.77, 0.88, 0.94, 0.98, 1.00, 0.97, 0.93, 0.87, 0.80, 0.70, 0.57]
WEISS, SCHWARZ = "#ffffff", "#000000"


# --- sRGB <-> OKLCH (Björn Ottosson, Oklab) ---------------------------------------------------------------------------
def _lin(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _gamma(c):
    return 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055


def hex_zu_rgb(h):
    return tuple(int(h.lstrip("#")[i:i + 2], 16) / 255 for i in (0, 2, 4))


def rgb_zu_hex(rgb):
    return "#%02x%02x%02x" % tuple(round(max(0, min(1, c)) * 255) for c in rgb)


def rgb_zu_oklch(rgb):
    r, g, b = (_lin(c) for c in rgb)
    l = (0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b) ** (1 / 3)
    m = (0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b) ** (1 / 3)
    s = (0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b) ** (1 / 3)
    L = 0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s
    a = 1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s
    bb = 0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s
    return L * 100, math.hypot(a, bb), math.degrees(math.atan2(bb, a)) % 360


def oklch_zu_rgb(L, C, H):
    L /= 100
    a, bb = C * math.cos(math.radians(H)), C * math.sin(math.radians(H))
    l = (L + 0.3963377774 * a + 0.2158037573 * bb) ** 3
    m = (L - 0.1055613458 * a - 0.0638541728 * bb) ** 3
    s = (L - 0.0894841775 * a - 1.2914855480 * bb) ** 3
    r = 4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s
    g = -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s
    b = -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s
    return tuple(_gamma(c) for c in (r, g, b))


def im_raum(rgb):
    return all(-0.0005 <= c <= 1.0005 for c in rgb)


def oklch_zu_hex(L, C, H):
    """Reduziert das Chroma, bis die Farbe im sRGB-Raum liegt; L und H bleiben."""
    while C > 0 and not im_raum(oklch_zu_rgb(L, C, H)):
        C -= 0.002
    return rgb_zu_hex(oklch_zu_rgb(L, max(C, 0), H))


# --- Kontrast nach WCAG -------------------------------------------------------------------------------------------------
def luminanz(h):
    r, g, b = (_lin(c) for c in hex_zu_rgb(h))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def kontrast(a, b):
    la, lb = luminanz(a), luminanz(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


# --- Rampe -----------------------------------------------------------------------------------------------------------
def profil_bei(L):
    """Chroma-Profil an einer beliebigen Helligkeit, linear zwischen den Stufen."""
    if L >= HELLIGKEIT[0]:
        return CHROMA_PROFIL[0]
    if L <= HELLIGKEIT[-1]:
        return CHROMA_PROFIL[-1]
    for i in range(len(HELLIGKEIT) - 1):
        a, b = HELLIGKEIT[i], HELLIGKEIT[i + 1]
        if b <= L <= a:
            t = (a - L) / (a - b)
            return CHROMA_PROFIL[i] + t * (CHROMA_PROFIL[i + 1] - CHROMA_PROFIL[i])
    return 1.0


def rampe(grundfarbe):
    L0, C0, H = rgb_zu_oklch(hex_zu_rgb(grundfarbe))
    spitze = C0 / max(profil_bei(L0), 0.05)
    stufen = {}
    for stufe, L, p in zip(STUFEN, HELLIGKEIT, CHROMA_PROFIL):
        C = spitze * p
        h = oklch_zu_hex(L, C, H)
        if stufe == 500:
            # Kontrastmitte: 4,5:1 auf Weiß und Schwarz; bei Bedarf minimal dunkler, damit Weiß darauf sicher 4,5:1 erreicht
            while kontrast(h, WEISS) < 4.5 and L > 40:
                L -= 0.1
                h = oklch_zu_hex(L, C, H)
        stufen[stufe] = {"hex": h, "L": round(L, 2), "C": round(C, 4), "H": round(H, 2)}
    return stufen


def ableiten(grundfarbe):
    r = rampe(grundfarbe)
    return {
        "hell": {"area": r[500]["hex"], "on": WEISS, "fg": r[700]["hex"]},
        "dunkel": {"area": r[500]["hex"], "on": WEISS, "fg": r[300]["hex"]},
    }, r


if __name__ == "__main__":
    args = sys.argv[1:]
    zeige_rampe = "--rampe" in args
    farben = [a for a in args if not a.startswith("--")] or ["#4c8438"]
    for farbe in farben:
        f, r = ableiten(farbe.lower())
        print(json.dumps({"farben": f}, ensure_ascii=False))
        if zeige_rampe:
            for s in STUFEN:
                print(f"  {s:03d} {r[s]['hex']} oklch({r[s]['L']}% {r[s]['C']} {r[s]['H']})")
        print(
            f"  {farbe}: 500 auf Weiß {kontrast(f['hell']['area'], WEISS):.2f}, 500 auf Schwarz {kontrast(f['hell']['area'], SCHWARZ):.2f}, "
            f"700 auf Weiß {kontrast(f['hell']['fg'], WEISS):.2f}, 300 auf Schwarz {kontrast(f['dunkel']['fg'], SCHWARZ):.2f}",
            file=sys.stderr,
        )
