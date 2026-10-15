# Prüfbericht Projektschau für KERN

Stand: Version 0.1.0 „Musterstadt“, 15. Oktober 2026. Wo eine Prüfung über einen früheren Stand lief, steht das Datum in der Zeile. Alle Prüfungen hat der Autor selbst durchgeführt, mit automatischen Werkzeugen und KI-gestützten Reviews. Eine Prüfung durch unabhängige Dritte gab es nicht. Das Bedrohungsmodell steht in [bedrohungsmodell.md](bedrohungsmodell.md), der Meldeweg für Sicherheitslücken in [SECURITY.md](../SECURITY.md). English version: [pruefbericht.en.md](pruefbericht.en.md).

## Aufbau

Das Pattern läuft vollständig im Browser: ein Renderer (`projektschau.js`), ein Stylesheet (`projektschau.css`) und ein Datenpaket als JSON, dazu das unveränderte KERN-Kit unter `vendor/kern/`. Es hat keinen Server-Teil und keine Anmeldung, setzt keine Cookies und lädt nichts von fremden Servern. Von außen kommt nur das Datenpaket. Der Renderer behandelt es als nicht vertrauenswürdig, auch wenn der Betreiber es selbst bereitstellt: Es kann aus einem Redaktionssystem mit mehreren Rollen stammen. Die Demo (`index.html`), die Dokumentation (`doku/`) und die Startseite (`website/`) sind statische Seiten auf demselben Kit. Die Prüfungen gelten vor allem der Strecke vom Datenpaket bis zur Seite.

## Prüfungen

| Prüfung | Vorgehen | Ergebnis |
|---|---|---|
| Datenfluss im Renderer | KI-gestützter Review auf DOM-XSS und auf Fehlbedienung (Methode „Sharp Edges“ von Trail of Bits): Datenpaket, Adresse, Hash, Browserspeicher und eingebettetes JSON bis zum Markup. Stand 12. Oktober 2026; die Startseite und die Skripte der Dokumentation sind nicht Teil dieses Reviews | Farben nur als Hex-Wert; Schlüssel und Sprachcodes nur im erwarteten Format, sonst bleibt der Eintrag draußen; Symbole werden mit `DOMParser` gelesen und auf die SVG-Formen `path`, `circle`, `rect`, `line`, `polyline`, `polygon`, `ellipse` reduziert; Nummern nur als Zahl; Links nur mit `http`, `https`, `mailto`, `tel` oder relativ; kein CSS-Selektor aus Daten; `?lang=` wird vor dem Speichern geprüft; ein fehlgeschlagener Abruf leert das Element und meldet den Fehler in der Konsole |
| Unsichere Voreinstellungen | KI-gestützter Review nach der Methode „Insecure Defaults“ von Trail of Bits, von Zugangsdaten bis zu Fehlern, die offen statt geschlossen enden. Stand 12. Oktober 2026 | kein Befund |
| Security-Review des gesamten Codes | Claude Code `/security-review`, Datenfluss von der Quelle bis zur Ausgabe. Stand 12. Oktober 2026 | kein Befund ab Schweregrad Mittel |
| Angriffstexte im Renderer | `skripte/pruefe_xss.js` rendert die Beispieldaten mit Nutzlasten in Bereichsfarbe, Schlüssel, Sprachcode, Symbol, Nummer, Link und Jahr und sucht nach aktivem Markup | 10 von 10 Prüfungen bestanden |
| Fuzzing | `skripte/pruefe_fuzz.js 1000 42`: 1000 zufällig verstümmelte Pakete mit festem Startwert (Felder entfernt, falsch typisiert, verschachtelt) | keine Ausnahme, kein aktives Markup, kein leeres Ergebnis |
| Unicode-Steuerzeichen | Bidi- und Zero-Width-Zeichen in Texten und Linktexten (Teil von `pruefe_xss.js`) | werden entfernt |
| Datenpaket, Klassen, Tokens | `skripte/pruefe.py`: jede `kern-`-Klasse und jedes `--kern-`-Token gegen das Kit, Formate im Datenpaket, Kontraste der Bereichsfarben hell und dunkel | ohne Befund; KERN-Kit 2.8.2 mit 2678 Klassen und 522 Tokens |
| Content-Security-Policy | Demo, Dokumentation und Startseite unter `default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; object-src 'none'; base-uri 'none'; form-action 'self'; frame-ancestors 'none'`, lokal und auf projektschau.thinkrepeat.com, dort auch auf den eigenen Fehlerseiten 403 und 404 | keine Verstöße; der Renderer setzt seine Regeln über `adoptedStyleSheets`, keine Seite enthält Inline-Skripte oder Inline-Stile |
| Barrierefreiheit | axe-core 4.14 nach WCAG 2.1 AA und 2.2 AA mit Best Practices: Demo, Dokumentation und Startseite, hell und dunkel, beide Sprachen, 1280, 390 und 320 Pixel, mit „Bewegung reduzieren“ (48 Läufe) | keine Verstöße. Ohne „Bewegung reduzieren“ sinkt der Kontrast im Zier-Motiv der Startseite für Bruchteile einer Sekunde, während Karten einblenden und Filterknöpfe die Farbe wechseln; das Motiv ist für Hilfstechnik ausgeblendet, nicht gewählte Karten werden grau statt durchsichtig |
| Tastatur, Kontraste, Textanpassung | Demo: Tastaturdurchgang mit Prüfung des Fokusrahmens, Kontraste aller Texte nachgerechnet, auch beim Überfahren; Textabstände nach WCAG 1.4.12, Schrift 200 %, reduzierte Bewegung. Stand 13. Oktober 2026 | ohne Befund |
| Browser | Chromium, Firefox und WebKit (Playwright 1.64): Demo mit Filter, Zeitleiste, Sprache, Dunkelmodus, Zustand in der Adresse und nach dem Neuladen | ohne Befund, keine Konsolenfehler |
| Last | 1000 Karten in Chromium (`skripte/erzeuge_last.py`). Stand 12. Oktober 2026 | 205 ms bis zum Rendern, 5 ms je Filterklick |
| Markup | html-validate 11.16 auf Demo, Dokumentation, Startseite und gerendertem DOM der Demo | ohne Befund |
| JavaScript und CSS | ESLint 10.12 und stylelint 17.16 über Renderer, Demo, Dokumentation und Startseite | ohne Befund |
| Lighthouse 13.5 | projektschau.thinkrepeat.com, Mobil-Profil mit simulierter Drosselung | Demo: Leistung 86 bis 90 je nach Lauf, Dokumentation 81, Startseite 87; Barrierefreiheit, Best Practices und SEO auf allen drei Seiten 100 |
| Scanner gegen die laufende Seite | OWASP ZAP 2.17 (Docker-Image `zap-stable`), Baseline-Scan gegen projektschau.thinkrepeat.com: Spider und passive Regeln, kein aktiver Scan | keine Fehler, 63 Regeln bestanden. Warnungen: `Permissions-Policy` und die Cross-Origin-Header sind nicht gesetzt; Hinweise zum Zwischenspeichern |
| Links | alle internen Verweise der Seiten auf projektschau.thinkrepeat.com und alle Adressen nach außen | 251 interne Verweise ohne Fehler; von 43 Adressen nach außen antworten zwei mit einer Sperre für Programme (uxdesign.cc mit 403, LinkedIn mit 999), eine war nicht erreichbar (503) |
| Lieferkette | KERN-Kit in fester Version, SHA-512-Prüfsumme des npm-Pakets vor dem Entpacken (`skripte/kern-sync.sh`); SHA-256-Prüfsumme zum Release-Zip | Kit, Fira Sans, Lucide und KERN-Logo mit Herkunft und Lizenz in der Stückliste, Lizenztexte im Paket |
| Stückliste | `SPDX_projektschau-kern.spdx.json` (SPDX 2.3), beim Bauen neu erzeugt; gegen das JSON-Schema von SPDX 2.3 geprüft am 13. Oktober 2026 | gültig |
| Bekannte Schwachstellen | Abfrage in der Datenbank OSV für `@kern-ux/native` 2.8.2 und `lucide` 1.49.0 | keine Treffer |
| Geheimnisse | gitleaks 8.30 über alle Commits | keine Funde |

## Was aussteht

- **Unabhängige Prüfung:** kein Pentest, kein Audit durch Dritte.
- **Screenreader und Nutzungstest:** axe-core deckt nur einen Teil der Kriterien ab. Ein Durchgang mit Screenreader und ein Test mit Menschen, die Inhalte pflegen, stehen aus.
- **KERN-Kit:** Der Autor hat geprüft, dass die Dateien dem Paket der Registry entsprechen und jede verwendete Klasse darin existiert, das Kit selbst aber nicht.
- **Trusted Types:** nicht getestet. Der Renderer setzt das geprüfte Markup an einer Stelle über `innerHTML`; eine Seite, die Trusted Types erzwingt, braucht dafür eine eigene Richtlinie.
- **Automatische Prüfkette:** Der Autor startet die Prüfungen lokal von Hand. Die Abfrage bei OSV ist eine Momentaufnahme; für Fira Sans nennt die Stückliste keine Version, die sich abfragen ließe.
- **Signatur:** Zum Zip gehört eine SHA-256-Prüfsumme, keine Signatur.
- **Einbettende Seite:** Server, Header und Content-Security-Policy gehören dem Betreiber. Wer `Projektschau.render` selbst aufruft und das Ergebnis weiterverarbeitet, verlässt die geprüfte Strecke.

## Prüfungen wiederholen

Aus dem Paketordner:

```
python3 skripte/pruefe.py
node skripte/pruefe_xss.js
node skripte/pruefe_fuzz.js 1000 42
python3 -m http.server 8771 --bind 127.0.0.1
```

Mit Playwright und axe-core aus einem eigenen Ordner `node_modules`, zum Beispiel für eine Seite des laufenden Servers:

```
NODE_PATH=/PFAD/ZU/node_modules node -e "
const { chromium } = require('playwright'); const { AxeBuilder } = require('@axe-core/playwright');
(async () => { const b = await chromium.launch(); const p = await (await b.newContext()).newPage();
  await p.goto('http://127.0.0.1:8771/index.html');
  const r = await new AxeBuilder({ page: p }).withTags(['wcag2a', 'wcag2aa', 'wcag21aa', 'wcag22aa', 'best-practice']).analyze();
  console.log(r.violations.length + ' Verstöße'); await b.close(); })();"
```

`NODE_PATH` zeigt auf einen Ordner `node_modules` mit `playwright` und `@axe-core/playwright`. Für die Content-Security-Policy die Seiten über einen Server ausliefern, der den Header oben setzt, und die Konsole auf Meldungen zur Content-Security-Policy prüfen.
