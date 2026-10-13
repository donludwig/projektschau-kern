#!/usr/bin/env python3
"""Erzeugt ein Datenpaket mit vielen Karten für den Lasttest des Renderers (Standard 1000) aus daten/beispiel.json.

Aufruf aus dem Ordner kern/: python3 skripte/erzeuge_last.py [anzahl]  →  /tmp/ps-last.json und /tmp/ps-last.html
"""
import json
import sys
from pathlib import Path

WURZEL = Path(__file__).resolve().parent.parent
n = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
d = json.loads((WURZEL / "daten/beispiel.json").read_text(encoding="utf-8"))
basis = d["projekte"]
projekte = []
for i in range(n):
    p = json.loads(json.dumps(basis[i % len(basis)]))
    p["nr"] = i + 1
    for s in d["sprachen"]:
        p["titel"][s] = f"{p['titel'][s]} {i + 1}"
    if p.get("zeitleiste"):
        p["zeitleiste"]["sortierung"] = 202401 + (i % 36)
        p["zeitleiste"]["jahr"] = str(2024 + (i % 36) // 12)
    projekte.append(p)
d["projekte"] = projekte
Path("/tmp/ps-last.json").write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
html = (WURZEL / "index.html").read_text(encoding="utf-8")
html = html.replace('<script type="application/json">', '<script type="application/json" data-last="1">', 1)
start = html.index('<script type="application/json" data-last="1">') + len('<script type="application/json" data-last="1">')
ende = html.index("</script>", start)
html = html[:start] + json.dumps(d, ensure_ascii=False).replace("</", "<\\/") + html[ende:]
Path("/tmp/ps-last.html").write_text(html, encoding="utf-8")
print(f"{n} Karten → /tmp/ps-last.json, /tmp/ps-last.html")
