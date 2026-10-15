# Änderungen

Alle nennenswerten Änderungen stehen hier, neueste Version zuerst. Das Format folgt [Keep a Changelog](https://keepachangelog.com/de/1.1.0/), die Versionsnummern der [semantischen Versionierung](https://semver.org/lang/de/). Jede Version trägt einen Namen.

## 0.1.0 „Musterstadt“

Erste Veröffentlichung, benannt nach dem erfundenen Ort der Beispieldaten. Stand 2026-10-15.

### Hinzugefügt

- **Karten:** jedes Projekt als Karte mit Bereich, Titel, Status, Beschreibung, Listen, Kennzahl und Links, in der Farbe seines Bereichs; wahlweise mit großem Symbol über dem Kartenkopf ([Abschnitt 3.2](README.md#32-wo-welches-feld-ausgespielt-wird)).
- **Zeitleiste:** dieselben Projekte nach Jahren geordnet, mit Zeitraum und Notiz ([Abschnitt 2.2](README.md#22-zeitleiste)).
- **Filter:** nach Bereich und Einordnung, mit Trefferzahlen und einem Hinweis, wenn nichts passt. Filter, Ansicht und Sprache stehen in der Adresszeile, ein Link führt also genau zu dieser Auswahl ([Abschnitt 3.5](README.md#35-filter-ansicht-und-adresszeile)).
- **Zwei Sprachen** mit Umschalter ([Abschnitt 3.3](README.md#33-sprachen)).
- **Hell und dunkel:** beide Farbschemata des KERN-Kits; die Farben eines Bereichs entstehen aus einer Grundfarbe ([Abschnitt 2.6](README.md#26-farben-programmatisch-ableiten)).
- **Druckansicht:** Titel, Einleitung und die gefilterte Ansicht, ohne Bedienelemente.
- **Ohne Framework und Build:** eine JavaScript-Datei und eine CSS-Datei auf dem KERN-Kit 2.8.2, das unverändert im Paket liegt; keine externen Anfragen ([Abschnitt 1](README.md#1-demo-und-einbinden)).
- **Datenpaket:** eine JSON-Datei mit Bereichen, Einordnungen, Projekten und Texten ([Abschnitt 2](README.md#2-daten)); 32 erfundene Beispielprojekte in vier Bereichen liegen bei.
- **Barrierefreiheit:** Tastaturbedienung mit sichtbarem Fokus, Ansage der Ergebnisse, geprüfte Kontraste, die Systemeinstellung „Bewegung reduzieren“ wird beachtet. Selbsttest mit axe-core nach WCAG 2.1 AA und 2.2 AA ohne offene Verstöße ([Abschnitt 6](README.md#6-barrierefreiheit)).
- **Sicherheit:** Der Renderer prüft jedes Feld des Datenpakets und läuft unter einer strengen Content-Security-Policy. Prüfskripte, Prüfbericht, Bedrohungsmodell, Sicherheitsrichtlinie (`SECURITY.md`) und Stückliste (SPDX 2.3) liegen bei ([Abschnitt 7](README.md#7-sicherheit)).
- **Demo und Dokumentation:** Demo-Seite, diese README in Deutsch und Englisch, beide auch als HTML-Seiten im KERN-Stil; Gestaltungs- und Inhaltsregeln für eigene Karten ([Abschnitt 4.5](README.md#45-gestaltungsregeln)).
- **Startseite:** die Startseite von projektschau.thinkrepeat.com in Deutsch und Englisch unter `website/`, als Beispiel für die Vorstellung des Patterns ([Abschnitt 1](README.md#1-demo-und-einbinden)).

English version: [CHANGELOG.en.md](CHANGELOG.en.md).
