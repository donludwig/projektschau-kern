# Sicherheit

## Lücke melden

Wenn du eine Sicherheitslücke in der Projektschau für KERN findest, melde sie bitte vertraulich per E-Mail an **don@thinkrepeat.com** mit dem Betreff „Projektschau KERN Sicherheit“. Bitte kein öffentliches Ticket, keine Veröffentlichung, bevor eine Korrektur verfügbar ist.

Hilfreich in der Meldung: betroffene Fassung (`CHANGELOG.md`), ein Datenpaket oder eine Einbettung, die das Problem zeigt, erwartetes und tatsächliches Verhalten, Browser.

Ablauf:

- Eingangsbestätigung mit Einschätzung und geplantem Weg innerhalb von 14 Tagen.
- Korrektur als neue Fassung mit Eintrag in `CHANGELOG.md`, abgestimmt mit der meldenden Person. Veröffentlichung der Einzelheiten spätestens 90 Tage nach der Meldung, früher sobald die Korrektur verfügbar ist.
- Nennung der meldenden Person, wenn gewünscht.

## Was dazugehört

- `projektschau.js`, `projektschau.css`, die Demo-Seite mit `demo.js`, `demo-theme.js` und `demo.css`, die Dokumentation unter `doku/`, die Startseite unter `website/` sowie die Skripte unter `skripte/`.
- Die gebündelten Bestandteile unter `vendor/kern/` (KERN-Kit mit Fira Sans). Die Stückliste liegt als `SPDX_projektschau-kern.spdx.json` bei.

Die Vertrauensgrenze des Patterns: Das Datenpaket gilt als nicht vertrauenswürdig. Der Renderer prüft Farben, Schlüssel, Sprachcodes, Symbole, Links, Nummern und Jahre auf ihr Format und lässt in HTML-Feldern nur eine Positivliste an Auszeichnung durch (README, Abschnitt 2.5). Alles, was trotz dieser Prüfungen aktives Markup, fremde Stylesheets oder Skripte in die Seite bringt, ist eine Lücke.

Nicht dazu gehören Fehler im KERN-Kit selbst (bitte an das KERN-Team, kern-ux.de), die einbettende Seite, deren Server und Content-Security-Policy sowie Browser, die die Browser-Baseline der README nicht erfüllen.

## Zuständigkeit

Don Ludwig pflegt das Pattern und beantwortet Meldungen. Was geprüft ist, wie und was aussteht, steht im Prüfbericht `doku/pruefbericht.md`, das Bedrohungsmodell in `doku/bedrohungsmodell.md`.

---

# Security (English)

Report vulnerabilities privately to **don@thinkrepeat.com**, subject “Projektschau KERN Security”. Please do not open a public issue before a fix is available. Include the affected release (see `CHANGELOG.en.md`), a data package or embedding that shows the problem, and the browser.

You will receive an acknowledgement with an assessment within 14 days. Fixes ship as a new release with a changelog entry; details are published no later than 90 days after the report, earlier once the fix is out. Reporters are credited if they wish.

In scope: `projektschau.js`, `projektschau.css`, the demo, documentation and start page and the scripts, plus the bundled KERN kit under `vendor/kern/` (see `SPDX_projektschau-kern.spdx.json`). The data package is untrusted by design; anything that gets active markup, foreign stylesheets or scripts into the page despite the renderer’s checks is a vulnerability. Out of scope: bugs in the KERN kit itself (report to the KERN team), the embedding page, its server and content security policy, and browsers below the baseline stated in the README.

What is checked, how, and what is open is described in the test report `doku/pruefbericht.en.md`.
