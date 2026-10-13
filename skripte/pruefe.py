#!/usr/bin/env python3
"""Prüft das KERN-Unterprojekt ohne Browser: KERN-Klassen und -Tokens gegen das Kit, Datenpaket, Badge-Kontraste.

Aufruf aus dem Ordner kern/: python3 skripte/pruefe.py
Meldet am Ende „ALLE PRÜFUNGEN BESTANDEN“ oder die Befunde.
"""
import json
import re
import sys
from pathlib import Path

WURZEL = Path(__file__).resolve().parent.parent
KIT = (WURZEL / "vendor/kern/kern.min.css").read_text(encoding="utf-8") + (WURZEL / "vendor/kern/kern-grid.min.css").read_text(encoding="utf-8")
KIT_KLASSEN = set(re.findall(r"\.(kern-[\w-]+)", KIT))
KIT_TOKENS = set(re.findall(r"(--kern-[\w-]+)", KIT))
_m = re.search(r'\[data-kern-theme=dark\][^{]*\{[^}]*--kern-color-layout-background:\s*(#[0-9a-fA-F]{6})', KIT)
DUNKEL_HINTERGRUND = _m.group(1) if _m else "#101010"  # Fallback, falls das Kit den Token anders ablegt
befunde = []


def pruefe_klassen():
    for name in ("projektschau.js", "projektschau.css", "index.html", "doku/readme.html", "doku/readme.en.html"):
        text = (WURZEL / name).read_text(encoding="utf-8")
        # Teilstrings, die im Code zusammengesetzt werden (z. B. "kern-btn--" + Größe), enden mit einem Bindestrich und zählen nicht
        if name.endswith(".html"):
            # In HTML zählen nur Klassenattribute; Fließtext nennt auch kern-ux.de oder kern-sync.sh
            klassen = {k for attr in re.findall(r'class="([^"]*)"', text) for k in attr.split() if k.startswith("kern-")}
        else:
            klassen = {k for k in re.findall(r"(?<![\w-])(kern-[a-z0-9_-]+)", text) if not k.endswith("-")}
        for k in sorted(klassen - KIT_KLASSEN):
            befunde.append(f"{name}: Klasse {k} fehlt im KERN-Kit")
        for t in sorted(set(re.findall(r"(--kern-[\w-]+)", text)) - KIT_TOKENS):
            befunde.append(f"{name}: Token {t} fehlt im KERN-Kit")


def luminanz(hexfarbe):
    r, g, b = (int(hexfarbe.lstrip("#")[i:i + 2], 16) / 255 for i in (0, 2, 4))
    lin = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)


def kontrast(a, b):
    la, lb = luminanz(a), luminanz(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def kartenflaeche(area_hex, L, faktor):
    """Kartenfläche aus der Bereichsfarbe wie in projektschau.css: gleicher Farbton, feste Helligkeit, gedämpftes Chroma."""
    sys.path.insert(0, str(WURZEL / "skripte"))
    import farben  # noqa: E402
    _, C, H = farben.rgb_zu_oklch(farben.hex_zu_rgb(area_hex))
    return farben.oklch_zu_hex(L, C * faktor, H)


def pruefe_daten():
    d = json.loads((WURZEL / "daten/beispiel.json").read_text(encoding="utf-8"))
    for feld in ("sprachen", "texte", "bereiche", "einordnungen", "projekte"):
        if feld not in d:
            befunde.append(f"beispiel.json: Feld {feld} fehlt")
    bereiche = {b["schluessel"]: b for b in d.get("bereiche", [])}
    einordnungen = {e["schluessel"] for e in d.get("einordnungen", [])}
    # Formate, die der Renderer nicht maskieren kann und deshalb prüft: hier dieselben Regeln
    for s in d.get("sprachen", []):
        if not re.fullmatch(r"[a-z]{2,3}(-[a-z0-9]{2,8})?", str(s), re.I):
            befunde.append(f"Sprache {s!r}: kein Sprachcode")
    for k in list(bereiche) + sorted(einordnungen):
        if not re.fullmatch(r"[a-z][a-z0-9_-]{0,40}", str(k)):
            befunde.append(f"Schlüssel {k!r}: nur a-z, 0-9, _ und -, Kleinbuchstabe am Anfang")
    for k, b in bereiche.items():
        for modus, f in ((b.get("farben") or {}).items()):
            for slot, wert in (f or {}).items():
                if not re.fullmatch(r"#[0-9a-f]{3,8}", str(wert), re.I):
                    befunde.append(f"Bereich {k} ({modus}.{slot}): {wert!r} ist keine Hex-Farbe")
    for p in d.get("projekte", []):
        if not isinstance(p.get("nr"), int):
            befunde.append(f"Projekt {p.get('nr')!r}: nr muss eine ganze Zahl sein")
        for l in p.get("links") or []:
            url = str(l.get("url", ""))
            if re.match(r"[a-z][a-z0-9+.-]*:", url, re.I) and not re.match(r"(https?|mailto|tel):", url, re.I):
                befunde.append(f"Projekt {p.get('nr')}: Link {url!r} mit nicht erlaubtem Schema")
        if p.get("bereich") not in bereiche:
            befunde.append(f"Projekt {p.get('nr')}: unbekannter Bereich {p.get('bereich')}")
        if p.get("einordnung") not in einordnungen:
            befunde.append(f"Projekt {p.get('nr')}: unbekannte Einordnung {p.get('einordnung')}")
        for s in d.get("sprachen", []):
            if not (p.get("titel") or {}).get(s):
                befunde.append(f"Projekt {p.get('nr')}: Titel fehlt in {s}")
    for k, b in bereiche.items():
        for modus in ("hell", "dunkel"):
            f = (b.get("farben") or {}).get(modus) or {}
            if f.get("area") and f.get("on"):
                c = kontrast(f["area"], f["on"])
                if c < 4.5:
                    befunde.append(f"Bereich {k} ({modus}): Badge-Kontrast {c:.2f} < 4,5")
        fg = ((b.get("farben") or {}).get("hell") or {}).get("fg")
        if fg and kontrast(fg, "#ffffff") < 4.5:
            befunde.append(f"Bereich {k} (hell): Titelfarbe fg {kontrast(fg, '#ffffff'):.2f} < 4,5 auf Weiß")
        # Kartenflächen wie in projektschau.css (oklch(from var(--ps-area) L calc(c * f) h)): hell 96,4 % / 0,08, dunkel 20,9 % / 0,65 (L in Prozent wie in farben.py).
        # Titel, Status und Kennzahl stehen in fg auf dieser Fläche; für beide Modi nachgerechnet.
        for modus, L, faktor, grund_seite in (("hell", 96.4, 0.08, "#ffffff"), ("dunkel", 20.9, 0.65, DUNKEL_HINTERGRUND)):
            f = (b.get("farben") or {}).get(modus) or {}
            if f.get("fg") and f.get("area"):
                flaeche = kartenflaeche(f["area"], L, faktor)
                for name, grund in (("Kartenfläche", flaeche), ("Seitenhintergrund", grund_seite)):
                    if kontrast(f["fg"], grund) < 4.5:
                        befunde.append(f"Bereich {k} ({modus}): Textfarbe fg {f['fg']} hat {kontrast(f['fg'], grund):.2f} < 4,5 auf {name} {grund}")
    print(f"Datenpaket: {len(d.get('projekte', []))} Projekte, {len(bereiche)} Bereiche, {len(einordnungen)} Einordnungen, Sprachen {d.get('sprachen')}")


def pruefe_inline():
    html = (WURZEL / "index.html").read_text(encoding="utf-8")
    m = re.search(r'<script type="application/json">(.*?)</script>', html, re.S)
    if not m:
        befunde.append("index.html: keine eingebetteten Beispieldaten")
        return
    if json.loads(m.group(1)) != json.loads((WURZEL / "daten/beispiel.json").read_text(encoding="utf-8")):
        befunde.append("index.html: eingebettete Daten weichen von daten/beispiel.json ab")


pruefe_klassen()
pruefe_daten()
pruefe_inline()
print(f"KERN-Kit {(WURZEL / 'vendor/kern/VERSION').read_text().strip()}: {len(KIT_KLASSEN)} Klassen, {len(KIT_TOKENS)} Tokens")
if befunde:
    print("\n".join(befunde))
    sys.exit(1)
print("ALLE PRÜFUNGEN BESTANDEN")
