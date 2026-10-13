#!/usr/bin/env python3
"""Schreibt daten/beispiel.json in den JSON-Block von index.html, damit die Demo ohne Server läuft.

Aufruf aus dem Ordner kern/: python3 skripte/einbetten.py
"""
import json
import re
from pathlib import Path

WURZEL = Path(__file__).resolve().parent.parent
daten = json.loads((WURZEL / "daten/beispiel.json").read_text(encoding="utf-8"))
inline = json.dumps(daten, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
html = (WURZEL / "index.html").read_text(encoding="utf-8")
neu, n = re.subn(r'(<script type="application/json">).*?(</script>)', lambda m: m.group(1) + inline + m.group(2), html, count=1, flags=re.S)
if n != 1:
    raise SystemExit("index.html: JSON-Block nicht gefunden")
(WURZEL / "index.html").write_text(neu, encoding="utf-8")
print(f"index.html: {len(daten['projekte'])} Projekte eingebettet")
