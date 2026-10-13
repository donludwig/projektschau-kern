# Barrierefreiheit

Stand 13. Oktober 2026, Fassung 0.1.0. Diese Erklärung ist ein Selbsttest und kein externer Nachweis.

## Ziel

Die Projektschau für KERN soll die Anforderungen der WCAG 2.1 und 2.2 auf Stufe AA erfüllen. Das gilt für das Pattern selbst (Karten, Filter, Zeitleiste, Sprachumschalter), für die Demo-Seite und für die HTML-Dokumentation.

## Was umgesetzt ist

- Alle Bedienelemente sind Buttons oder Links, mit der Tastatur in der Reihenfolge der Darstellung erreichbar und mit dem Fokusrahmen des KERN-Kits.
- Filter und Umschalter melden ihren Zustand über `aria-pressed`, Gruppen tragen einen Namen in der aktiven Sprache.
- Die Zahl der Treffer wird nach jedem Filterklick angesagt.
- Symbole sind dekorativ, jede Information steht auch als Text.
- Texte und Flächen nutzen die Farben des KERN-Kits. Für die Bereichsfarben prüft `skripte/pruefe.py` den Kontrast von 4,5:1 in beiden Farbschemata.
- Jede Sprachfassung ist mit ihrem Sprachcode ausgezeichnet.
- Die Systemeinstellung „Bewegung reduzieren“ schaltet Übergänge und weiches Scrollen ab.
- Die Druckansicht zeigt Titel, Einleitung und die gefilterte Ansicht.

## Wie geprüft wurde

- axe-core 4.14 über Playwright nach WCAG 2.1 AA und 2.2 AA mit Best Practices: Karten und Zeitleiste, hell und dunkel, Deutsch und Englisch, Breiten 1280, 390 und 320 Pixel, in Chromium, Firefox und WebKit. Ergebnis: keine offenen Verstöße.
- Kontraste aller sichtbaren Texte nachgerechnet, auch im Zustand beim Überfahren.
- Tastaturdurchgang mit Prüfung des Fokusrahmens.
- Textabstände nach WCAG 1.4.12, Schriftgröße 200 % und Darstellung bei 320 Pixel Breite ohne abgeschnittene Inhalte.
- Markup mit html-validate, dazu Lighthouse (Barrierefreiheit 100).

## Was aussteht

- Ein Durchgang mit Screenreader (NVDA, JAWS, VoiceOver).
- Ein Test mit Nutzer:innen.
- Eine Prüfung durch unabhängige Dritte, etwa nach BITV 2.0 oder EN 301 549.

## Bekannte Grenzen

- Ohne JavaScript bleibt die Übersicht leer, weil die Karten im Browser aus dem Datenpaket entstehen. Wer das vermeiden will, erzeugt das Markup mit `Projektschau.render` vorab auf dem Server.
- Die Inhalte der Karten kommen aus dem Datenpaket. Verständliche Texte, sinnvolle Linktexte und ausreichend kontrastreiche Bereichsfarben liegen in der Hand derer, die das Paket pflegen; `skripte/pruefe.py` prüft die Kontraste.
- Das KERN-Kit ist unverändert eingebunden. Seine Barrierefreiheit ist Sache des KERN-Projekts.

## Rückmeldung

Wenn du auf eine Barriere stößt, schreib bitte an **don@thinkrepeat.com** oder eröffne ein Ticket im [Repositorium](https://github.com/donludwig/projektschau-kern/issues). Hilfreich sind die Ansicht, der Browser und das Hilfsmittel, mit dem das Problem auftritt.

---

# Accessibility (English)

As of 13 October 2026, release 0.1.0. This statement is a self-assessment, not an external audit.

The pattern, its demo page and the HTML documentation aim to meet WCAG 2.1 and 2.2 at level AA. All controls are buttons or links, reachable by keyboard with the focus ring of the KERN kit; filters and switches expose their state, results are announced, symbols are decorative, each language version carries its language code, and the system setting “reduce motion” is respected.

Checked with axe-core 4.14 through Playwright (cards and timeline, light and dark, German and English, widths 1280, 390 and 320 pixels, in Chromium, Firefox and WebKit) with no open violations, plus recalculated contrasts, a keyboard pass, text spacing, 200 % font size, html-validate and Lighthouse.

Still to come: a pass with a screen reader, a test with users, and a review by independent third parties. Known limits: without JavaScript the overview stays empty; the content of the cards comes from the data package and is the responsibility of whoever maintains it; the KERN kit is included unchanged.

Feedback: **don@thinkrepeat.com** or an issue in the [repository](https://github.com/donludwig/projektschau-kern/issues).
