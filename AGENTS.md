# Hinweise für Coding-Agenten

Projektschau für KERN: ein Pattern aus Renderer (`projektschau.js`), Stylesheet (`projektschau.css`) und Datenpaket (JSON) auf dem KERN UX-Standard. Kein Framework, kein Build. Die README beschreibt Datenformat, Einbindung und Gestaltungsregeln; Sicherheit und Prüfungen stehen in `doku/pruefbericht.md` und `doku/bedrohungsmodell.md`.

## Vor jedem Commit

```
python3 skripte/pruefe.py          # Klassen und Tokens gegen das Kit, Datenpaket, Kontraste
node skripte/pruefe_xss.js         # Angriffstexte in jedem Datenfeld
node skripte/pruefe_fuzz.js 1000 42
```

Alle drei müssen „ALLE PRÜFUNGEN BESTANDEN“ melden. Nach Änderungen an `README.md` oder `README.en.md`: `python3 skripte/doku_html.py`. Nach Änderungen an `daten/beispiel.json`: `python3 skripte/einbetten.py`.

## Regeln

- `vendor/kern/` bleibt unverändert. Ein neues Kit nur über `skripte/kern-sync.sh` mit fester Version und Prüfsumme.
- Nur `kern-`-Klassen und `--kern-`-Tokens, die im Kit existieren; eigene Klassen mit eigenem Präfix: `ps-` im Pattern, `demo-` und `doku-` in Demo und Dokumentation, `start-` auf der Startseite unter `website/`. Farben nur über Tokens, nie als feste Werte; hell und dunkel immer beide prüfen.
- Keine Inline-Skripte, keine Inline-Stile, keine `style`-Attribute: Alle Seiten laufen unter `default-src 'self'` ohne `unsafe-inline`.
- Keine Anfragen an fremde Server, keine Schriften oder Skripte von einem CDN.
- Das Datenpaket gilt als nicht vertrauenswürdig. Jedes neue Feld bekommt eine Formatprüfung im Renderer und einen Fall in `skripte/pruefe_xss.js`.
- Barrierefreiheit nach WCAG 2.1 und 2.2 AA ist Anforderung: Tastatur, sichtbarer Fokus, Ansage von Ergebnissen, „Bewegung reduzieren“.
- README, CHANGELOG und Prüfbericht gibt es auf Deutsch und Englisch; beide Fassungen gemeinsam ändern. Neue Änderungen in `CHANGELOG.md` und `CHANGELOG.en.md` eintragen.
- Keine Zugangsdaten, lokalen Pfade oder persönlichen Daten ins Repositorium.
