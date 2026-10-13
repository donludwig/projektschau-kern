![Projektschau für KERN: Projektkarten in vier Bereichsfarben mit Filterleiste, darüber versetzt eine Zeitleiste](doku/katalog-bild.png)

# Projektschau für KERN

Projektübersicht mit Karten, Filtern und Zeitleiste auf Basis des [KERN UX-Standards](https://www.kern-ux.de). Ein Pattern für Initiativen, Vereine und Verwaltungen, die ihre Vorhaben auf einer Seite zeigen wollen: jede Karte ein Projekt mit Bereich, Einordnung, Status, Beschreibung, Aktivitäten, Partnern, Kennzahl und Links. Zwei Sprachen, Hell- und Dunkelmodus, Filter nach Bereich und Einordnung, Zeitleiste nach Jahren, Deep-Links über die Adresszeile.

Drei Dateien, kein Framework, kein Build: `projektschau.js`, `projektschau.css` und ein JSON-Datenpaket. Das KERN-Kit liegt unverändert unter `vendor/kern/`.

Das Pattern ist aus einer [Projektübersicht](https://ankerpunkt-hoherflaeming.de/projekte/) entstanden, die bei einem regionalen Netzwerk als laufendes Projekt im Einsatz ist. Parallel wird ein WordPress-Plugin mit demselben Datenformat entwickelt. Die Beispieldaten in `daten/beispiel.json` sind erfunden.

Quellcode: [github.com/donludwig/projektschau-kern](https://github.com/donludwig/projektschau-kern). Diese Seite gibt es auch auf Englisch: `README.en.md`.

## 1. Demo und Einbinden

`index.html` im Browser öffnen, ein Server ist nicht nötig. Die Beispieldaten liegen direkt in der Seite; dieselben Daten stehen in `daten/beispiel.json` für die Einbindung per `data-src`.

```html
<link rel="stylesheet" href="vendor/kern/fonts/fira-sans.css">
<link rel="stylesheet" href="vendor/kern/kern.min.css">
<link rel="stylesheet" href="vendor/kern/kern-grid.min.css">
<link rel="stylesheet" href="projektschau.css">
<script src="projektschau.js" defer></script>

<div data-projektschau data-src="daten/beispiel.json"></div>
```

Alternativ ohne `data-src`, mit dem Datenpaket direkt im Element:

```html
<div data-projektschau>
  <script type="application/json">{ "version": 1, "sprachen": ["de", "en"], … }</script>
</div>
```

Beim Einbetten `</` als `<\/` schreiben (`skripte/einbetten.py` tut das), sonst beendet ein `</script>` in einem Textfeld den Block, bevor der Renderer läuft.

Die Seite muss das KERN-Kit laden (Kit-Version in `vendor/kern/VERSION`). Das Kit ist nicht gekapselt: es setzt `html`, `body` und `:root` und gehört deshalb auf Seiten, die insgesamt mit KERN gestaltet sind. Die Breite bestimmt die Seite, zum Beispiel über `kern-container` (96 Prozent der Fensterbreite, höchstens 1536 Pixel). Hell und Dunkel folgen dem KERN-Mechanismus: `data-kern-theme="light|dark"` auf `<html>` oder die Systemeinstellung.

| Datei | Aufgabe |
|---|---|
| `index.html` | Demo-Seite. Lädt das Kit, das Ergänzungs-CSS und das Skript, enthält die Beispieldaten eingebettet und einen Hell/Dunkel-Umschalter. Ohne Inline-Skripte und -Styles, damit sie auch unter einer strengen Content-Security-Policy läuft. |
| `demo-theme.js`, `demo.js`, `demo.css` | Nur für die Demo-Seite: Farbschema vor dem ersten Rendern, Adressparameter, Umschalter, Doku-Link und die Gestaltung von Kopf- und Fußzeile. Kein Teil des Patterns. |
| `projektschau.js` | Liest das Datenpaket, erzeugt das gesamte Markup und steuert Filter, Ansicht, Sprache und Adresszeile. Rund 340 Zeilen, ohne Abhängigkeiten. |
| `projektschau.css` | Ergänzungen zum Kit: Raster, Bereichsfarben, Filterleiste, Zeitleiste. Rund 160 Zeilen, nur KERN-Tokens und die Bereichsfarben aus den Daten. |
| `daten/beispiel.json` | Datenpaket der Demo, 32 erfundene Projekte in vier Bereichen. Vorlage für eigene Daten. |
| `vendor/kern/` | KERN-Kit [`@kern-ux/native`](https://www.npmjs.com/package/@kern-ux/native) ([Quelle auf openCode](https://gitlab.opencode.de/kern-ux/kern-ux-plain); `kern.min.css`, `kern-grid.min.css`, Schriften), Version in `VERSION`, nur über `skripte/kern-sync.sh` aktualisieren. |
| `skripte/pruefe.py` | Prüft Klassen und Tokens gegen das Kit, das Datenpaket (Schlüssel, Sprachen, Farben, Nummern, Links), Kontraste und die eingebetteten Daten. |
| `skripte/pruefe_xss.js` | Rendert das Datenpaket mit Node ohne Browser und prüft Nutzlasten in Farben, Schlüsseln, Sprachen, Icons, Links, Nummer und Jahr. |
| `skripte/pruefe_fuzz.js` | Schickt tausend zufällig verstümmelte Pakete durch den Renderer: keine Ausnahme, kein aktives Markup. |
| `skripte/erzeuge_last.py` | Erzeugt ein Datenpaket mit vielen Karten (Standard 1000) und eine Demo-Seite dazu für den Lasttest im Browser. |
| `skripte/einbetten.py` | Schreibt `daten/beispiel.json` in den JSON-Block von `index.html`. |
| `skripte/farben.py` | Leitet aus einer Grundfarbe je Bereich die Werte `area`, `on` und `fg` für hell und dunkel ab, siehe 2.6. |
| `skripte/doku_html.py` | Erzeugt aus `README.md` und `README.en.md` die Seiten `doku/readme.html` und `doku/readme.en.html` im KERN-Stil: gleiche Kopf- und Fußzeile wie die Demo, mitlaufendes Inhaltsverzeichnis „Auf dieser Seite“, Kopierknöpfe an Codeblöcken, Tabellen in `kern-table-responsive`, DE/EN-Links. Braucht das Python-Modul `markdown`. |
| `skripte/kern-sync.sh` | Holt das Kit in fester Version mit Prüfsumme aus der npm-Registry. |

### Die Demo-Seite

`index.html` hat eine Kopfzeile mit den Links Demo und Dokumentation, dem Hell/Dunkel-Umschalter und einer Fußzeile mit den Lizenzhinweisen; die Doku-Seiten tragen dieselbe Kopf- und Fußzeile. Farbschema und Sprache werden beim Wechsel zwischen den Seiten in der Adresse mitgegeben (`?theme=dark&lang=en`), damit die Wahl auch dann erhalten bleibt, wenn der Browser keinen Speicher erlaubt, etwa Safari bei Dateien von der Festplatte. Beide Werte landen zusätzlich im `localStorage` unter `ps-theme` und `ps-lang`. Der README-Link zeigt immer auf die Fassung in der gerade aktiven Sprache.

### Optionen am Element

| Attribut | Werte | Wirkung |
|---|---|---|
| `data-src` | Pfad oder URL | Datenpaket per `fetch` laden; ein eingebetteter JSON-Block hat Vorrang |
| `data-ansicht` | `karten` (Vorgabe), `zeitleiste` | Startansicht |
| `data-bereich` | Schlüssel eines Bereichs | vorgewählter Bereichsfilter |
| `data-ebene` | 1 bis 4 | Überschriftenebene des Titels; Kartentitel und Jahre liegen eine Stufe darunter, Projekttitel in der Zeitleiste zwei |
| `data-sprache` | Sprachkürzel | Startsprache. Reihenfolge der Ermittlung: gespeicherte Wahl im Browser, dieses Attribut, Browsersprache, erste Sprache des Pakets. Die Demo setzt es aus `?lang=` in der Adresse. |
| `data-zeitleiste`, `data-einordnungsfilter`, `data-sprachumschalter` | `nein` | den jeweiligen Teil nicht rendern |
| `data-symbole` | `ja`, `nein` | Cover mit dem großen Projektsymbol über dem Kartenkopf, Fläche in der Bereichsfarbe. Ohne das Attribut gilt die im Browser gespeicherte Wahl des Symbolschalters, sonst aus. Die Demo setzt es aus `?symbole=` in der Adresse. |
| `data-symbolschalter` | `ja` | Checkbox „Symbole“ im Kopf links neben dem Sprachumschalter, mit der Lesende das Cover ein- und ausschalten; die Wahl wird im Browser gespeichert (`ps-symbole`) |

## 2. Daten

### 2.1 Aufbau des Datenpakets

Das Paket ist ein JSON-Objekt. Texte, die in mehreren Sprachen vorliegen, sind immer ein Objekt mit einem Eintrag je Sprachkürzel, zum Beispiel `{"de": "Umwelt", "en": "Environment"}`. Im Folgenden heißt das „Sprachpaar“.

```
{
  "version": 1,
  "sprachen": ["de", "en"],
  "texte": { … },
  "filter_alle": { "bereich": { "label": Sprachpaar, "icon_svg": "…" } },
  "bereiche": [ … ],
  "einordnungen": [ … ],
  "projekte": [ … ]
}
```

**`sprachen`:** Liste der Sprachkürzel. Die erste Sprache ist die Vorgabe. Mit einer Sprache entfällt der Sprachumschalter.

**`texte`:** alle Oberflächentexte, die nicht zu einem Projekt gehören.

| Pfad | Wo es erscheint |
|---|---|
| `kopf.titel` | Hauptüberschrift über der Übersicht |
| `kopf.einleitung` | Einleitungstext unter der Überschrift, HTML erlaubt |
| `filter.bereich_label`, `filter.einordnung_label` | Beschriftung der beiden Filterblöcke; auf schmalen Bildschirmen zugleich die Köpfe der Aufklapper |
| `filter.aria_bereich`, `filter.aria_einordnung` | `aria-label` der beiden Filtergruppen |
| `ansicht.karten`, `ansicht.zeitleiste`, `ansicht.aria` | Beschriftung des Umschalters Karten/Zeitleiste und dessen `aria-label` |
| `sprache.aria` | `aria-label` des Sprachumschalters |
| `symbole.label`, `symbole.aria` | Beschriftung und `aria-label` des Symbolschalters (Option `data-symbolschalter`) |
| `leerzustand.meldung`, `leerzustand.zuruecksetzen` | Meldung und Knopf, wenn kein Projekt zum Filter passt |
| `zeitleiste.aria` | `aria-label` der Zeitleiste |
| `fuss.ueber.ueberschrift`, `fuss.ueber.absaetze` | optionaler aufklappbarer Abschnitt am Ende; `absaetze` ist eine Liste von Sprachpaaren, HTML erlaubt. Fehlt `fuss`, gibt es den Abschnitt nicht. |

**`filter_alle.bereich`:** Beschriftung und Symbol des Filters „Alle“, der in beiden Filterblöcken vorn steht.

**`bereiche`:** die Bereiche, nach denen gefiltert wird. Die Reihenfolge der Liste ist die Reihenfolge der Filter.

| Feld | Bedeutung |
|---|---|
| `schluessel` | technischer Name, nur Kleinbuchstaben und Bindestrich, wird in Adresszeile und CSS-Variablen verwendet |
| `label` | Sprachpaar, erscheint auf Filter und Badge |
| `icon_svg` | Symbol, siehe 2.3 |
| `farben.hell`, `farben.dunkel` | je ein Objekt mit `area`, `on`, `fg`, siehe 2.4. Ein zusätzlicher Wert `brand` wird mitgeführt, aber nicht verwendet. |

**`einordnungen`:** die zweite Filterachse, zum Beispiel Hauptprojekt, Netzwerk, Veranstaltung, Idee.

| Feld | Bedeutung |
|---|---|
| `schluessel` | technischer Name wie bei den Bereichen |
| `label` | Sprachpaar, erscheint auf Filter und Karte |
| `label_zeitleiste` | Sprachpaar für die Zeitleiste; fehlt es, gilt `label` |
| `als_filter_chip` | `true`, wenn die Einordnung als Filter angeboten wird; mit `false` bleibt sie auf der Karte sichtbar, ist aber nicht filterbar |

**`projekte`:** die Karten. Ein Eintrag je Projekt, die Reihenfolge der Liste ist die Reihenfolge im Raster.

| Feld | Pflicht | Bedeutung |
|---|---|---|
| `nr` | ja | laufende Nummer, wird zweistellig gezeigt |
| `bereich` | ja | `schluessel` eines Bereichs |
| `einordnung` | ja | `schluessel` einer Einordnung |
| `icon_svg` | nein | Symbol, siehe 2.3; auf der Karte nur als Cover mit `data-symbole="ja"` |
| `titel` | ja | Sprachpaar |
| `status` | nein | Sprachpaar, kurze Zeile unter dem Titel, zum Beispiel „Laufend – seit 05/2025“ |
| `beschreibung` | nein | Sprachpaar, HTML erlaubt |
| `abschnitte` | nein | Liste; jeder Eintrag hat `typ` `liste` mit `label` und `punkte` (Liste von Sprachpaaren) oder `typ` `text` mit `label` und `text`. HTML in `punkte` und `text` erlaubt. Regel der Demo: Der erste Abschnitt einer Karte ist immer eine Liste mit mindestens zwei Punkten ([Abschnitt 4.5](#45-gestaltungsregeln)). |
| `kennzahl` | nein | Sprachpaar, eine hervorgehobene Zeile direkt nach Text oder Liste, HTML erlaubt; Regeln in 4.5 |
| `links` | nein | Liste mit `url` und `text` (Sprachpaar) |
| `zeitleiste` | nein | Objekt mit `sortierung`, `zeitraum`, `notiz`, siehe 2.2. Fehlt es oder ist es `null`, erscheint das Projekt nur in der Kartenansicht. |

Leere Werte schreibt man als `null` oder lässt das Feld weg; eine leere Liste `[]` ist ebenfalls erlaubt.

### 2.2 Zeitleiste

Ein Projekt wird nicht doppelt gepflegt. Die Zeitleiste liest Nummer, Bereich, Titel und Einordnung aus dem Projekt und braucht nur den kleinen Block `zeitleiste`:

| Feld | Bedeutung |
|---|---|
| `sortierung` | Zahl im Muster `JJJJMM`, zum Beispiel `202505`. Die ersten vier Ziffern bilden das Jahr, unter dem der Eintrag steht; die Zahl bestimmt die Reihenfolge innerhalb des Jahres. Bei gleicher Zahl entscheidet `nr`. |
| `zeitraum` | Sprachpaar, der Text neben der Linie, zum Beispiel „seit 05/2025“ oder „07/2024“ |
| `notiz` | Sprachpaar, optional, der kurze Stand unter dem Titel. Erscheint nur in der Zeitleiste, nicht auf der Karte. |

### 2.3 Symbole

`icon_svg` enthält nur das Innere eines SVG-Symbols im 24×24-Raster, ohne die `<svg>`-Hülle, zum Beispiel `<path d="M12 20v2"/><circle cx="12" cy="12" r="4"/>`. Das Skript setzt die Hülle mit `viewBox="0 0 24 24"`, Strichstärke 2 und `currentColor`, dadurch nimmt das Symbol die Textfarbe seiner Umgebung an. Die Demo verwendet Symbole aus dem [Lucide](https://lucide.dev)-Set (ISC-Lizenz); jedes Set mit Strich-Symbolen im 24er-Raster passt.

### 2.4 Bereichsfarben und Kontrast

Jeder Bereich bringt seine Farben mit, getrennt für hell und dunkel:

| Wert | Verwendung |
|---|---|
| `area` | Fläche der Bereichs-Badge und des aktiven Bereichsfilters; Grundlage für Kartentönung und Trennlinie |
| `on` | Text und Symbol auf `area`, in der Regel Weiß |
| `fg` | Textfarbe des Bereichs auf hellem Grund: Titel, Status, Kennzahl, Nummer, Symbol und inaktiver Filter; in der Zeitleiste Punkt, Titel und Einordnung |

Anforderungen, die `skripte/pruefe.py` nachrechnet: `on` auf `area` mindestens 4,5:1 in beiden Modi; `fg` hell auf Weiß mindestens 4,5:1. Für den Dunkelmodus braucht `fg` dunkel entsprechend Kontrast zum dunklen KERN-Hintergrund; dafür gibt es noch keine automatische Prüfung, der Wert ist beim Anlegen im Browser zu prüfen. Alle anderen Farben kommen aus den KERN-Tokens und sind nicht Teil der Daten.

### 2.5 Eigene Daten anlegen

1. `daten/beispiel.json` kopieren und die Listen `bereiche`, `einordnungen` und `projekte` ersetzen. Schlüssel vergeben, Farben je Bereich setzen, Symbole eintragen.
2. `texte` an die eigene Übersicht anpassen, mindestens `kopf.titel`.
3. Prüfen: `python3 skripte/pruefe.py` meldet unbekannte oder ungültige Schlüssel, fehlende Titel, falsche Formate und zu schwache Kontraste.
4. Entweder per `data-src` laden oder mit `python3 skripte/einbetten.py` in `index.html` einbetten. Das Prüfskript meldet, wenn eingebettete Daten und JSON-Datei auseinanderlaufen.

Vertrauensgrenze: Felder, in denen HTML erlaubt ist (Einleitung, Beschreibung, Abschnitte, Kennzahl, Fußtexte), werden auf eine Allowlist reduziert: `a` mit geprüftem `href`, `strong`, `em`, `p`, `br`, `ul`, `ol`, `li`; andere Elemente und alle übrigen Attribute fallen weg, ihr Text bleibt. Alle anderen Textfelder werden maskiert. Werte, die nicht maskiert werden können, prüft der Renderer auf ihr Format und lässt sie sonst aus: Schlüssel (`^[a-z][a-z0-9_-]{0,40}$`), Sprachcodes, Farben (Hex), Link-Adressen (nur `http`, `https`, `mailto`, `tel` und relative Pfade) und die Nummer (ganze Zahl); `icon_svg` wird auf die Formen `path`, `circle`, `rect`, `line`, `polyline`, `polygon`, `ellipse` mit Geometrie-Attributen reduziert. `skripte/pruefe_xss.js` prüft das ohne Browser mit Nutzlasten nach.

### 2.6 Farben programmatisch ableiten

Von Hand gepflegt wird je Bereich nur eine Grundfarbe. Alles Weitere lässt sich daraus berechnen, auf zwei Ebenen.

**Ebene 1, Datenpaket:** `skripte/farben.py` erzeugt aus einer Grundfarbe eine Farbrampe nach dem Verfahren des KERN-Kits und daraus den Block `farben` für `bereiche[]`:

```bash
python3 skripte/farben.py "#4c8438" "#b4457a"
python3 skripte/farben.py --rampe "#4c8438"
```

KERN baut seine Farbrampen nach der [„Universal Color Palette“](https://uxdesign.cc/the-universal-color-palette-9826deb94f7) im [Oklab](https://bottosson.github.io/posts/oklab/)-Farbraum, beschrieben auf der [KERN-Seite zur Farbe](https://www.kern-ux.de/2.0.6/design-system/farbe/): Die Stufen 025 bis 950 sind nach Helligkeit sortiert, jede Stufe hat über alle Farbtöne denselben Kontrast, Stufe 500 ist die Kontrastmitte mit 4,5:1 auf Weiß und auf Schwarz, und Hell- und Dunkelmodus entstehen durch Spiegelung (800 hell entspricht 200 dunkel). Das Skript bildet das nach:

| Schritt | Regel |
|---|---|
| Farbraum | Rechnung in OKLCH (Helligkeit L, Chroma C, Farbton H), nicht in sRGB oder HSL. Der Farbton der Grundfarbe bleibt über die ganze Rampe gleich. |
| Helligkeit je Stufe | feste Skala von 025 bis 950, der Mittelwert der elf Rampen aus `@kern-ux/native` 2.8.2 (zum Beispiel 300 = 75,4 %, 500 = 57,0 %, 700 = 42,4 %) |
| Chroma je Stufe | folgt dem Profil der [Kit-Rampen](https://www.kern-ux.de/design-system/foundations/farbe/) (Spitze um 550 bis 650, zu den Rändern abnehmend); die Höhe des Profils wird so gewählt, dass die Rampe an der Helligkeit der Grundfarbe deren Chroma trifft |
| Farbraumgrenze | liegt eine Stufe außerhalb von sRGB, wird nur das Chroma verringert; Helligkeit und Farbton bleiben |
| Stufe 500 | wird bei Bedarf um Zehntelprozent abgedunkelt, bis Weiß darauf sicher 4,5:1 erreicht |
| `area` | Stufe 500 |
| `on` | Weiß |
| `fg` hell | Stufe 700, wie KERN seine Aktionsfarbe im Hellmodus setzt (Kontrast auf Weiß rund 8:1) |
| `fg` dunkel | Stufe 300, die Spiegelung von 700, wie KERNs Aktionsfarbe im Dunkelmodus |

Die Grundfarbe selbst erscheint also nicht unverändert, sondern als Rampe in ihrem Farbton; `area` ist die 500er-Stufe dieses Farbtons. Die Beispieldaten sind so aus den vier Grundfarben der Demo entstanden. Das Skript gibt die Kontraste mit aus, `--rampe` zeigt alle zwanzig Stufen als OKLCH und Hex.

**Ebene 2, Darstellung:** Aus `area`, `on` und `fg` leitet `projektschau.css` zur Laufzeit alle weiteren Töne mit `color-mix` ab, es gibt keine weiteren Farbwerte in den Daten:

| Ton | Formel |
|---|---|
| Kartenfläche | Stufe 025 der Bereichsrampe (hell) bzw. 950 (dunkel), aus `area` mit der relativen Farbsyntax `oklch(from var(--ps-area) 96.4% calc(c * 0.08) h)` berechnet; Browser ohne diese Syntax bekommen eine `color-mix`-Näherung |
| Kartenrahmen, Trennlinie | Stufe 100 (hell) bzw. 900 (dunkel) der Bereichsrampe, ebenso berechnet |
| Bereichsfilter aktiv, Hover und Klick | `area`; Hover 88 % `area` mit Schwarz, Klick 78 % |
| Bereichsfilter inaktiv, Hover und Klick | Rand `area`, Text `fg`; Hover 10 % `area` über transparent, Klick 18 % |
| Nummer | `fg` mit 75 % Deckung |
| Titel, Status, Kennzahl, Punkt der Zeitleiste | `fg` unverändert |

Die Mischung läuft im Farbraum `oklab`, dadurch bleiben die Töne gleichmäßig hell. Im Dunkelmodus setzt das Skript die dunklen Werte für `area`, `on` und `fg` ein, die Formeln bleiben gleich und mischen dann mit den dunklen KERN-Tokens.

### 2.7 Browser

Der Renderer braucht nur Funktionen, die nach Baseline „Widely available“ seit 2023 in allen großen Browsern stehen: `DOMParser`, `URL`, `color-mix()` (seit Mai 2023), `aspect-ratio`, `:focus-visible`. Zwei neuere Funktionen nutzt er mit Rückfall: Die Stylesheet-Regeln setzt er über `adoptedStyleSheets` (Chrome 73, Edge 79, Firefox 101, Safari 16.4; Stand caniuse 2026-10-12), ältere Browser bekommen ein `<style>`-Element, das ohne strenge CSP ebenso funktioniert. Kartenflächen und Rahmen stehen zuerst als `color-mix()` und werden von der relativen Farbsyntax `oklch(from …)` überschrieben, wo sie voll unterstützt ist (Chrome und Edge 131, Firefox 133, Safari 18; Anteil 93 Prozent); ältere Browser zeigen die `color-mix()`-Fassung, die sich nur in Nuancen unterscheidet. Das KERN-Kit selbst nennt im Paket keine Browserliste. Geprüft am 2026-10-12 in Chromium, Firefox 157 und WebKit 27.2 über Playwright, siehe [Abschnitt 5](#5-prüfen-und-pflegen).

## 3. Verarbeitung und Ausgabe

### 3.1 Ablauf

1. **Start:** Beim Laden ruft das Skript für jedes `[data-projektschau]` die Funktion `init` auf. Sie liest die Optionen aus den Attributen und holt die Daten aus dem eingebetteten JSON-Block oder per `fetch` von `data-src`.
2. **Rendern:** `render(daten, optionen)` baut das komplette Markup als String. Es gibt keine Templates; jede Struktur steht in einer kleinen Funktion: `karte` für eine Karte, `zeitleisteHtml` für die Zeitleiste, `filterBtn`, `badge`, `btn` und `icon` für die Bausteine.
3. **Interaktion:** `interaktion(wurzel)` hängt die Ereignisse an das gerenderte Markup: Sprachwechsel, Filter, Ansicht, Zurücksetzen, Adresszeile, Aufklapper.

Über `window.Projektschau.render` und `window.Projektschau.init` sind beide Funktionen auch von außen aufrufbar, etwa um das Markup serverseitig vorzuerzeugen.

### 3.2 Wo welches Feld ausgespielt wird

Kartenansicht, von oben nach unten:

| Stelle | Feld | Markup |
|---|---|---|
| Spalte und Karte | – | `kern-col-12 kern-col-md-6 kern-col-lg-4 kern-col-xxl-3 ps-col` > `kern-card kern-layer kern-level-1 ps-card` mit `data-bereich` und `data-cat` |
| Badge Bereich | `bereiche[].icon_svg`, `bereiche[].label` | `kern-badge kern-badge--small ps-badge` in Bereichsfarbe, mit dem Bereichssymbol, auf Karte und Zeitleiste |
| Badge Einordnung | `einordnungen[].label` | `kern-badge kern-badge--small` neutral |
| Nummer | `nr` | `ps-num`, rechts, Bereichsfarbe gedämpft |
| Symbol | `icon_svg` | `kern-card__media ps-cover` über dem Kopf, sichtbar nur mit eingeschaltetem Cover (`data-symbole` oder Symbolschalter, [Abschnitt 1](#1-demo-und-einbinden)) |
| Titel | `titel` | `kern-title` in Bereichsfarbe, eine Stufe größer als im Kit |
| Status | `status` | `kern-subline kern-subline--small` in Bereichsfarbe |
| Beschreibung | `beschreibung` | `kern-body` |
| Abschnitte | `abschnitte[]` | `label` als `kern-label`, `liste` als `kern-list kern-list--bullet kern-list--small`, `text` als `kern-body kern-body--small` |
| Kennzahl | `kennzahl` | `kern-body ps-kpi` mit `<strong>`, Bereichsfarbe, direkt nach Text oder Liste |
| Trennlinie | nur wenn `links` vorhanden | `kern-divider kern-divider--decorative ps-card-divider` |
| Links | `links[]` | `kern-link kern-link--small` im `kern-card__footer`, 16 Pixel wie der übrige Kartentext |

Zeitleiste, je Jahr eine Gruppe:

| Stelle | Feld | Markup |
|---|---|---|
| Jahresüberschrift | aus `zeitleiste.sortierung` | `kern-heading kern-heading-medium ps-tl-jahr` |
| Zeitraum | `zeitleiste.zeitraum` | `ps-tl-zeit`, Spalte links, auf Mobil über dem Eintrag |
| Punkt auf der Linie | Farbe aus `bereiche[].farben.*.fg` | Pseudo-Element von `ps-tl-main` (Mobil: von `ps-row`) |
| Nummer, Badge, Titel, Einordnung | `nr`, `bereiche[].label`, `titel`, `einordnungen[].label_zeitleiste` | eine Zeile `ps-tl-kopf`, alle auf gemeinsamer Grundlinie |
| Notiz | `zeitleiste.notiz` | `kern-body kern-body--small ps-tl-notiz` |

Filterleiste: Bereichsfilter aus `bereiche` mit Symbol und Trefferzahl, Umschalter Karten/Zeitleiste rechts daneben, darunter der Einordnungsfilter aus den Einordnungen mit `als_filter_chip: true`. Die Trefferzahlen rechnen beide Achsen gegeneinander: der Zähler eines Bereichs zählt nur Projekte, die auch zur gewählten Einordnung passen, und umgekehrt.

### 3.3 Sprachen

Jedes Sprachpaar wird als Folge von Elementen mit `lang`-Attribut gerendert, eines je Sprache, zum Beispiel `<span lang="de">Umwelt</span><span lang="en">Environment</span>`. Für Blocktexte mit HTML sind es `div`-Elemente. Sind alle Varianten gleich oder gibt es nur eine Sprache, steht der Text ohne Hülle.

Das Skript erzeugt pro Sprache eine CSS-Regel und setzt sie in ein `<style>` vor den Wrapper: `.ps[data-lang="de"] [lang]:not([lang="de"]) { display: none }`. Der Sprachwechsel ändert nur `data-lang` und `lang` am Wrapper; die Texte bleiben alle im Dokument, Suchmaschinen und Screenreader sehen die aktive Sprache korrekt ausgezeichnet. `aria-label`-Texte liegen als `data-aria-<sprache>` am Element und werden beim Wechsel umgeschrieben. Die gewählte Sprache wird unter `ps-lang` im `localStorage` gemerkt.

### 3.4 Bereichsfarben im Markup

Beim Rendern schreibt das Skript die hellen Farben aller Bereiche als CSS-Variablen in ein erzeugtes `<style>` vor dem Wrapper, Regel `.ps { … }`: `--ps-area-umwelt`, `--ps-area-umwelt-on`, `--ps-area-umwelt-fg` und so weiter je Schlüssel. Ein `style`-Attribut wäre dafür ungeeignet, weil es die dunklen Regeln überstimmen würde. Die dunklen Farben stehen im selben `<style>` unter den KERN-Theme-Selektoren `[data-kern-theme="dark"] .ps`, `.kern-dark .ps` und, als Fallback für die Systemeinstellung, `@media (prefers-color-scheme: dark)`.

Jedes Element, das zu einem Bereich gehört (Karte, Zeitleistenzeile, Bereichsfilter, Badge), bekommt per `style`-Attribut drei generische Variablen zugewiesen: `--ps-area`, `--ps-area-on`, `--ps-area-fg`, die auf die Variablen seines Bereichs zeigen. Das CSS arbeitet nur mit diesen drei Namen und kennt die Bereiche nicht. Neue Bereiche brauchen deshalb keine CSS-Änderung.

### 3.5 Filter, Ansicht und Adresszeile

Jede Karte und jede Zeitleistenzeile trägt `data-bereich` und `data-cat`. Ein Filterklick setzt `aria-pressed` und die Button-Varianten um, prüft jedes Element gegen beide aktiven Filter und setzt die Klasse `is-hidden`. Jahre ohne sichtbare Zeile werden ausgeblendet, die erste und die letzte sichtbare Zeile eines Jahres bekommen die Klassen `ps-row--erste` und `ps-row--letzte` (dort beginnt und endet die Linie am Punkt), bei null Treffern erscheint der Leerzustand mit Zurücksetzen-Knopf. Die Live-Region `ps-live` meldet die Trefferzahl an Screenreader; die Texte dafür stehen im Skript (`LIVE`, `LEER`) und sind über die Optionen `live` und `leer` beim direkten Aufruf von `render` austauschbar.

Der Zustand steht in der Adresszeile hinter `#`, zum Beispiel `#bereich=kultur&filter=netzwerk&ansicht=zeitleiste`, und wird beim Laden und bei `hashchange` wiederhergestellt. So lässt sich jede Auswahl als Link weitergeben.

Bereichs- und Einordnungsfilter liegen je in einer KERN-Details-Komponente. Ab 48rem Fensterbreite setzt das Skript beide auf `open` und die Klasse `ps-panel--offen`, das CSS blendet dann die Köpfe aus und zeigt die Beschriftungen in der Zeile. Darunter dienen die Köpfe „Bereich“ und „Filter“ als Aufklapper in der Aktionsfarbe; der Bereichsblock ist anfangs offen, der Einordnungsblock zu.

## 4. Styling

### 4.1 Das KERN-Kit

Das Kit liegt unverändert unter `vendor/kern/` (`kern.min.css`, [Fira Sans](https://github.com/mozilla/Fira) in den Schnitten 400, 400 kursiv, 500, 600 und 700, Lizenz, Versionsdatei). Die Demo-Seite setzt `data-kern-theme` vor dem ersten Rendern aus dem `localStorage` (Schlüssel `ps-theme`), damit nichts aufblitzt. Das Raster füllt die Breite mit so vielen Spalten, wie Karten von mindestens 18rem Platz finden.

### 4.2 Verwendete KERN-Komponenten

| Komponente | Verwendung |
|---|---|
| `kern-card` mit `__container`, `__header`, `__body`, `__footer` | die Karte in der kompakten Variante `kern-card--small` (8 Pixel zwischen Kopf, Rumpf und Fuß, 16-Pixel-Texte), Innenabstand per eigener Regel 24 Pixel (`--kern-metric-space-large`) |
| `kern-hgroup`, `kern-title`, `kern-subline` | Titelblock der Karte mit Status |
| `kern-badge kern-badge--small` | Bereich und Einordnung auf Karte und Zeitleiste |
| `kern-btn` mit `--x-small`, `--primary`, `--secondary`, `--tertiary`, `kern-btn-wrapper` | Filter, Ansichts- und Sprachumschalter (x-small), Zurücksetzen (tertiary); aktiv ist `--primary`, inaktiv `--secondary`, Zustand zusätzlich in `aria-pressed` |
| `kern-details` mit `__header`, `__body` | Bereichs- und Einordnungsfilter, optionaler Abschnitt „Über“ |
| `kern-form-check` mit `__checkbox` und `kern-label` | Symbolschalter als Checkbox (das Kit hat keinen Schalter) |
| `kern-row`, `kern-col-12`, `kern-col-md-6`, `kern-col-lg-4`, `kern-col-xxl-3` (aus `kern-grid.min.css`) | Kartenraster: eine, zwei, drei und ab 1600 Pixel vier Spalten nach den KERN-Breakpoints |
| `kern-stack-lg`, `kern-stack-sm` | vertikale Abstände im Wrapper und im Kopf |
| `kern-layer kern-level-1` | die Karte als abgesetzte Fläche mit den Kontext-Tokens des Kits |
| `kern-divider kern-divider--decorative` | Trennlinie vor den Links |
| `kern-heading-x-large`, `kern-heading-medium`, `kern-body`, `kern-label`, `kern-list`, `kern-link`, `kern-sr-only` | Typografie, Listen, Links, Screenreader-Text |

KERN hat keinen Chip- oder Tag-Toggle, keinen Segmented Control und keine Tabs. Filter und Umschalter sind deshalb Buttons mit `aria-pressed`. Für den Umschalter Karten/Zeitlich ist im KERN-Projekt eine Komponente „Segmented Control“ vorgeschlagen ([Issue 1141 im KERN-Hauptrepositorium](https://gitlab.opencode.de/kern-ux/pattern-library/-/work_items/1141), Stand Oktober 2026 im Refinement, Semantik als `radiogroup` oder Button-Gruppe mit `aria-pressed` noch offen). Der Umschalter hier ist bis dahin Eigenbau aus zusammenhängenden KERN-Buttons und wird an die Komponente angeglichen, sobald sie im Kit ist.

### 4.3 Eigene Ergänzungen

Alle eigenen Klassen tragen das Präfix `ps-`, alle Werte kommen aus KERN-Tokens oder den drei Bereichsvariablen. Zwei gesetzte Werte bleiben, weil das Kit dafür keine Tokens hat: `--ps-tl-mitte` (17 Pixel) ist die Höhe der ersten Zeile in der Zeitleiste, an der Punkt und Zeitraum ausgerichtet sind, auf Mobil die halbe Zeilenhöhe aus dem Token; und 200 Millisekunden für den Übergang des Cover-Symbols. Alles andere, auch Punktgröße, Linienstärke und Zeitraumspalte, kommt aus Tokens.

| Klasse | Zweck |
|---|---|
| `.ps` | Wrapper; die Abstände kommen aus `kern-stack-lg` |
| `.ps-head`, `.ps-lede`, `.ps-kopfzeile`, `.ps-symbolschalter`, `.ps-lang` | Kopfbereich, Einleitung, Zeile rechts oben mit Symbolschalter und Sprachumschalter |
| `.ps-controls`, `.ps-controls-divider` | Filterleiste als Raster: Bereichsblock links, Umschalter rechts, Einordnungsblock darunter, `kern-divider` als Abschluss; haftet oben, leicht transparent mit Weichzeichnung |
| `.ps-filter`, `.ps-filter-label`, `.ps-view`, `.ps-count` | Filterzeilen als Raster (Beschriftung links, Buttons brechen in ihrer Spalte um), Ansichtsumschalter (bis 64rem als volle Zeile oben), Trefferzahl |
| `.ps-btn-bereich` | Bereichsfilter in Bereichsfarbe, aktiv gefüllt, inaktiv mit farbigem Rand, Hover und Aktiv als Abmischung der Bereichsfarbe |
| `.ps-seg` | zwei Buttons stoßen zu einem Umschalter zusammen; Farben und Radius bleiben die der Buttons |
| `.ps-panel`, `.ps-panel-bereich`, `.ps-panel-cat`, `.ps-panel--offen` | die beiden Filterblöcke als Details: auf Desktop offen ohne Kopf, auf Mobil aufklappbar mit Kopf in Beschriftungsgröße und Aktionsfarbe |
| `.ps-grid`, `.ps-col` | Zeile und Spalten des KERN-Grids mit 24 statt 32 Pixel Rinne (12 Pixel je Spaltenseite aus dem Token `large`); `.ps-col` streckt die Karte auf Zeilenhöhe |
| `.ps-card` | Fläche und ganz dezenter Rahmen als Stufen 025 und 100 der Bereichsrampe, im Dunkelmodus 950 und 900 |
| `.ps-cover`, `.ps-cover-icon` | optionales Cover 16:9 über dem Kartenkopf, Fläche Stufe 100 der Bereichsrampe (dunkel 900), Symbol 22 Prozent der Kartenbreite in `fg`, wächst bei Zeiger oder Fokus auf der Karte weich auf 115 Prozent (200 Millisekunden, entfällt bei reduzierter Bewegung); nur bei eingeschaltetem Cover sichtbar |
| `.ps-tags`, `.ps-badge`, `.ps-num` | Kopfzeile der Karte, Badge in Bereichsfarbe mit mehr Innenabstand, Nummer rechts |
| Regeln auf `.kern-title`, `.kern-subline`, `.ps-kpi` in `.ps-card` | Bereichsfarbe und Titelgröße; sie stehen in der Spezifität über den Kartenregeln des Kits, weil diese sonst gewinnen |
| `.ps-field`, Regeln auf `.kern-list--bullet` in der Karte | Feldbezeichnung ohne Abstand nach unten, Listen mit 4 statt 24 Pixel Abstand und 20 statt 32 Pixel Einrückung |
| `.ps-card-divider` | Trennlinie in der Rahmenmischung |
| `.ps-tl`, `.ps-year`, `.ps-tl-jahr`, `.ps-tl-liste`, `.ps-row`, `.ps-tl-zeit`, `.ps-tl-main`, `.ps-tl-kopf`, `.ps-tl-titel`, `.ps-tl-cat`, `.ps-tl-notiz` | Zeitleiste: Raster mit 96 Pixel Zeitraumspalte (3 × `x-large`), Linie 2 Pixel mit Punkt 16 Pixel, Linie beginnt und endet je Jahr am ersten und letzten sichtbaren Punkt, Kopfzeile auf Grundlinie; unter 40rem Zeitraum über dem Eintrag, Linie am Zeilenrand, Punkt beim Zeitraum |
| `.ps-empty` | Leerzustand: Text und tertiärer Button in `kern-stack-sm`, mit `role="status"` |
| `.ps-live` | Live-Region, visuell verborgen über `kern-sr-only` |

Die Abstufung der Bereichsfarbe auf der Karte, von kräftig nach leise: Badge und aktiver Filter (`area` voll), Titel, Status, Kennzahl, Punkt (`fg` voll), Nummer (`fg` mit 75 Prozent Deckung), Rahmen und Trennlinie (Stufe 100), Fläche (Stufe 025).

### 4.4 Wo sich was anpassen lässt

| Wunsch | Stelle |
|---|---|
| Farben eines Bereichs | nur in den Daten: `bereiche[].farben` |
| Texte der Oberfläche | nur in den Daten: `texte` |
| Welche Einordnungen filterbar sind | `einordnungen[].als_filter_chip` |
| Reihenfolge der Filter und Karten | Reihenfolge der Listen `bereiche` und `projekte` |
| Startansicht, Vorfilter, Überschriftenebene, Teile ausblenden | Attribute am Element, [Abschnitt 1](#1-demo-und-einbinden) |
| Stärke der Kartentönung oder des Rahmens | Prozentwerte in `.ps-card` und `.ps-card-divider` |
| Größe von Kartentitel oder Zeitleistentitel | Token-Zuweisung in den Regeln auf `.kern-title` in `.ps-card` bzw. `.ps-tl-titel`; passende Stufen sind `medium-static` (18), `large-static` (21), `medium-adaptive` (21/24) |
| Innenabstand der Karte | Token in der Regel auf `.ps-card .kern-card__container`; ohne sie gelten die 16 Pixel der kompakten Variante |
| Rinne des Rasters | Token in den Regeln auf `.ps-grid.kern-row` und `.ps-grid.kern-row > .ps-col`; ohne diese Regeln gelten die 2rem des Kits |
| Spaltenzahl des Rasters | `kern-col-*`-Klassen in `karte()` im Skript (Vorgabe 12, md 6, lg 4, xxl 3) |
| Haften der Filterleiste | `position: sticky` in `.ps-controls` entfernen |
| Breite der Zeitraumspalte | Token-Rechnung in `.ps-row` (3 × `x-large`, 96 Pixel) |
| Umbruchpunkte | `48rem` im Skript (Aufklapper), `64rem` im CSS (Ansichtsumschalter), `40rem` im CSS (Zeitleiste) |
| Texte der Live-Region | Konstanten `LIVE` und `LEER` im Skript oder Optionen `live`/`leer` bei `render` |
| Fokusfarbe, Aktionsfarbe, Schrift | nicht im Pattern, sondern über die KERN-Theme-Tokens der Seite, zum Beispiel `--kern-color-action-focus-default` auf `:root` |

Nicht vorgesehen: eigene Schriften (KERN legt Fira Sans fest), ein eigenes Farbsystem neben den Tokens, und eine Kapselung des Kits für Seiten, die nicht mit KERN gestaltet sind.

### 4.5 Gestaltungsregeln

Diese Regeln beschreiben, wie die Demo gestaltet ist. Wer das Pattern anpasst, hält sie ein oder ändert sie hier mit. Alle Werte sind KERN-Tokens; die Pixelangaben nennen den Wert des Tokens.

**Grundsätze**

- Nur Klassen, die im Kit existieren. Eigene Klassen tragen das Präfix `ps-` und ergänzen nur, was KERN nicht hat. Kein fester Farb- oder Pixelwert außer `--ps-tl-mitte`.
- Drei Textgrößen im Pattern: 16 Pixel (`small-static`) für alles Laufende, auch Badges, Nummer, Status, Listen, Links und Zeitraum; 21 Pixel, ab Desktop 24 (`medium-adaptive`) für den Kartentitel; 21 Pixel (`large-static`) für den Titel in der Zeitleiste. Dazu `kern-heading-x-large` für den Seitentitel und `kern-heading-medium` für das Jahr. Zeilenhöhe 24 Pixel (`medium-static`), beim Kartentitel 28 bzw. 32.
- Abstände in vier Stufen: 4 (`x-small`), 8 (`small`), 16 (`default`), 24 Pixel (`large`). Zusammengehöriges steht mit 4 oder 8 beieinander, Blöcke trennen 16 oder 24.
- Bereichsfarbe nur über die drei Variablen `--ps-area`, `--ps-area-on`, `--ps-area-fg`, abgestuft von kräftig nach leise (Ende von 4.3). Alles andere aus Kit-Tokens: Aktionsfarbe für Umschalter, Einordnungsfilter und Links, `decorative-border` für Linien, `text-muted` für den Zeitraum.
- Zustände: aktiv ist `kern-btn--primary`, inaktiv `kern-btn--secondary`, dazu `aria-pressed`. Fokus, Hover und Aktiv kommen vom Kit; bei Bereichsbuttons werden sie aus der Bereichsfarbe gemischt, wie das Kit es mit der Aktionsfarbe macht.
- Dunkelmodus spiegelt die Rampe: Fläche 950 statt 025, Rahmen und Trennlinie 900 statt 100, `fg` 300 statt 700. Keine eigenen Dunkelfarben.
- Symbole: Lucide, 1em in Buttons und Badges (Bereichssymbol auf Karte und Zeitleiste), immer in der Farbe des Textes daneben. Neben dem Kartentitel steht kein Symbol; das Projektsymbol erscheint nur als optionales Cover.

**Inhalte**

Die Regeln für Texte, damit alle Karten gleich aufgebaut sind.

- Titel ohne Schlusspunkt, Status als kurze Zeile nach dem Muster „Laufend – seit 05/2025“, „Geplant für 06/2026“ oder „Idee – noch nicht begonnen“.
- Beschreibung ein bis zwei Sätze, Kennzahl und Listenpunkte jeweils eine Zeile.
- Der erste Abschnitt unter der Beschreibung ist eine Liste mit mindestens zwei Punkten; jeder Punkt beginnt groß und endet ohne Schlusspunkt. Karten ohne Abschnitt bleiben kurz.
- Die Kennzahl beginnt groß („Rund 90 Einsätze je Monat“, nicht „rund …“), endet ohne Schlusspunkt und schreibt Tausender im Deutschen mit Punkt („2.300 Bilder“), im Englischen mit Komma. Sie folgt direkt auf Text oder Liste.
- Links stehen nur im Kartenfuß; der Linktext benennt das Ziel („Zum Garten“, „Programm“), nie „hier“ oder „mehr“.
- Zeitleiste: Zeitraum als „seit 05/2025“ oder „07/2024“, Notiz ein kurzer Satz ohne Schlusspunkt.
- Beide Sprachen gleich lang und gleich aufgebaut; Zahlen und Daten in beiden identisch.

**Seitenkopf**

| Element | Regel |
|---|---|
| Titel | Ebene aus `data-ebene` (Vorgabe `h1`), `kern-heading-x-large` |
| Einleitung | `kern-body kern-body--large`, Absätze mit 8 Pixel Abstand, Hinweis fett im Text |
| Sprachumschalter | rechts oben, zwei `kern-btn--x-small` (32 Pixel, wie Karten/Zeitlich) als zusammenhängender Umschalter (`ps-seg`), aktiv `primary`; `role="group"` mit Beschriftung aus den Daten |
| Symbolschalter | links neben dem Sprachumschalter mit 8 Pixel Abstand, eine KERN-Checkbox (`kern-form-check`, 32 Pixel) mit dem Label aus `texte.symbole.label`, `aria-label` aus `texte.symbole.aria`; Rahmen und Label in der Aktionsfarbe des Kits, angehakt wie im Kit; nur mit `data-symbolschalter="ja"` |
| Abstände | im Kopf `kern-stack-sm` (8 Pixel), zwischen Kopf, Filterleiste und Raster `kern-stack-lg` (32 Pixel) |

**Filterleiste**

| Element | Regel |
|---|---|
| Leiste | haftet am oberen Rand, Hintergrund 88 Prozent der Seitenfarbe mit 8 Pixel Weichzeichnung, 16 Pixel Innenabstand oben, Abschluss `kern-divider--decorative` |
| Aufbau | Raster: Bereichsblock links, Umschalter Karten/Zeitlich rechts in derselben Zeile, Einordnungsblock darunter; 16 Pixel zwischen den Blöcken |
| Beschriftung | `kern-label` in einer 80 Pixel breiten Spalte (2,5 × `x-large`), 4 Pixel nach unten versetzt, damit sie mittig zur ersten Buttonzeile steht |
| Buttons | `kern-btn--x-small`, 32 Pixel hoch, 8 Pixel Abstand in beiden Richtungen (der 8-Pixel-Außenabstand des Kits oben und unten ist entfernt), brechen in ihrer Spalte um |
| Bereichsbuttons | aktiv Fläche `area` und Text `on`, inaktiv Rand `area` und Text `fg`; Hover und Aktiv als Abmischung von `area` (88 und 78 Prozent mit Schwarz bzw. 10 und 18 Prozent über transparent); Symbol des Bereichs davor |
| Einordnungsbuttons | Aktionsfarbe des Kits, sonst wie Bereichsbuttons |
| Trefferzahl | in Klammern hinter dem Label, 80 Prozent Deckung, Zustand des Labels |
| Umschalter Karten/Zeitlich | zwei `kern-btn--x-small` als `ps-seg`, auf Höhe der ersten Buttonzeile; bis 64rem als volle Zeile über den Filtern mit zwei gleich breiten Hälften |
| Mobil (unter 48rem) | beide Blöcke als `kern-details`, Kopf in Beschriftungsgröße und Aktionsfarbe mit 20 Pixel Pfeil, Beschriftung auf eigener Zeile, Inhalt nicht eingerückt |

**Kartenraster**

| Element | Regel |
|---|---|
| Spalten | KERN-Grid: 1, ab `md` 2, ab `lg` 3, ab `xxl` 4 Spalten |
| Rinne | 24 Pixel (`large`) statt der 32 des Kits, 12 je Spaltenseite |
| Höhe | alle Karten einer Zeile gleich hoch; der Rumpf dehnt sich, Trennlinie und Links stehen immer am unteren Rand |

**Karte**

| Element | Regel |
|---|---|
| Komponente | `kern-card kern-card--small` als `kern-layer kern-level-1`; kompakte Variante wegen 8 Pixel Lücke zwischen Kopf, Rumpf und Fuß und 16-Pixel-Texten, Innenabstand aber 24 Pixel (`large`) |
| Fläche, Rahmen | Stufe 025 und 100 der Bereichsrampe (hell), 950 und 900 (dunkel), Rahmen 1 Pixel, Radius des Kits |
| Reihenfolge | optionales Cover, Kopfzeile, Titel, Status, Text, Felder mit Listen, Kennzahl, Trennlinie, Links |
| Cover (Option) | `kern-card__media` im Seitenverhältnis 16:9, Fläche Stufe 100 der Bereichsrampe, Projektsymbol 22 Prozent der Kartenbreite in `fg`, obere Ecken im Kartenradius; bei Zeiger oder Fokus auf der Karte wächst das Symbol weich auf 115 Prozent, bei reduzierter Bewegung ohne Übergang; nur bei eingeschaltetem Cover, sonst ist die Kopfzeile das erste Element |
| Kopfzeile | Bereichs-Badge mit Symbol, Einordnungs-Badge ohne Fläche, Nummer rechts; 4 Pixel zwischen den Badges, 8 Pixel nach unten |
| Badge | `kern-badge--small`, Innenabstand 2 und 8 Pixel, Fläche `area`, Text `on`, 16 Pixel halbfett; Symbol 1em mit 4 Pixel Abstand |
| Nummer | zweistellig mit führender Null, 16 Pixel normal, `fg` mit 75 Prozent Deckung, Tabellenziffern, ohne Grundlinien-Innenabstand, damit sie mit dem Badge auf einer Linie steht |
| Titel | `kern-title`, 21/24 Pixel, Farbe `fg`, ohne Symbol |
| Status | `kern-subline--small` direkt unter dem Titel ohne den oberen Grundlinienabstand des Kits, 16 Pixel, Farbe `fg` |
| Text | `kern-body`, 16 Pixel, Textfarbe des Kits |
| Feld | Bezeichnung `kern-label` halbfett, 4 Pixel Abstand zum Inhalt; darunter immer eine Liste `kern-list--bullet kern-list--small` mit mindestens zwei Punkten und 4 Pixel dazwischen, 20 Pixel eingerückt (`default` + `x-small`, das Kit nimmt 32). Kein Fließtext als erster Abschnitt, damit die Karten gleich aufgebaut sind; Karten ohne Abschnitt bleiben kurz |
| Kennzahl | `kern-body` fett, Farbe `fg`, folgt direkt auf Text oder Liste, nie an den unteren Rand geschoben (der ist für die Links reserviert); beginnt immer mit Großbuchstaben („Rund 90 Einsätze je Monat“), ohne Schlusspunkt; Tausender im Deutschen mit Punkt („2.300 Bilder“), im Englischen mit Komma |
| Trennlinie | `kern-divider--decorative` in Stufe 100, 16 Pixel darüber und 0 darunter; mit der 8-Pixel-Lücke der Karte sind es 24 zur Kennzahl und 8 zu den Links |
| Links | `kern-link kern-link--small`, 16 Pixel, Aktionsfarbe, unterstrichen, 16 Pixel nebeneinander, umbrechend |

**Zeitleiste**

| Element | Regel |
|---|---|
| Jahr | `kern-heading-medium`, 8 Pixel darunter, 24 Pixel zwischen den Jahren; Jahre ohne sichtbare Einträge werden ausgeblendet |
| Zeile | Raster mit 96 Pixel Zeitraumspalte (3 × `x-large`) und 16 Pixel Abstand zur Linie; 24 Pixel unter jedem Eintrag, 4 unter dem letzten |
| Zeitraum | `kern-body--small kern-body--muted`, rechtsbündig, auf Höhe der ersten Zeile |
| Linie, Punkt | Linie 2 Pixel (`border-width-default`) in `decorative-border`, Punkt 16 Pixel (`dimension-x-small`) in `area`, mittig auf der Linie; Linie beginnt am ersten und endet am letzten sichtbaren Punkt des Jahres |
| Kopfzeile | auf der Grundlinie: Nummer, Bereichs-Badge mit Bereichssymbol (2 Pixel angehoben, damit es mittig zur Titelzeile sitzt), Titel `kern-title` 21 Pixel in `fg`, Einordnung `kern-label--subtle` in `fg`; 8 Pixel Abstand, 4 beim Umbruch |
| Notiz | `kern-body--small`, 4 Pixel unter der Kopfzeile, Textfarbe des Kits |
| Mobil (unter 40rem) | Zeitraum über dem Eintrag, 8 Pixel darunter; Linie am linken Rand der ganzen Zeile, Punkt auf Höhe des Zeitraums; Leiste 8 Pixel eingerückt, damit der Punkt beim Scrollen hinter der Filterleiste verschwindet |

**Leerzustand und Meldungen**

| Element | Regel |
|---|---|
| Leerzustand | `kern-body` und `kern-btn--tertiary` in `kern-stack-sm`, kein Kasten, `role="status"`; Button nicht gedehnt |
| Live-Region | `kern-sr-only`, `aria-live="polite"`, meldet die Trefferzahl nach jedem Filtern |

## 5. Prüfen und pflegen

- `python3 skripte/pruefe.py` muss „ALLE PRÜFUNGEN BESTANDEN“ melden. Es prüft, dass jede verwendete `kern-*`-Klasse und jedes `--kern-*`-Token im Kit existiert, dass das Datenpaket schlüssig ist (bekannte Schlüssel, Titel in jeder Sprache), dass Badge- und Titelkontraste reichen und dass die eingebetteten Daten der JSON-Datei entsprechen.
- Nach jeder Änderung an `daten/beispiel.json`: `python3 skripte/einbetten.py`.
- Nach jeder Änderung an `README.md` oder `README.en.md`: `python3 skripte/doku_html.py` (braucht das Python-Modul [`markdown`](https://python-markdown.github.io)).
- `node skripte/pruefe_fuzz.js 1000 42` muss „ALLE PRÜFUNGEN BESTANDEN“ melden (Anzahl und Startwert frei wählbar).
- Druckansicht: Demo im Browser drucken oder über Playwright `emulateMedia({ media: 'print' })` prüfen; es dürfen nur Titel, Einleitung und Karten erscheinen.
- Lasttest: `python3 skripte/erzeuge_last.py 1000` schreibt `last-test.html` mit 1000 Karten (nicht im Repositorium); im Browser öffnen und Filter, Zeitleiste und Sprache prüfen. Gemessen: 205 ms bis zum ersten Rendern, 5 ms je Filterklick. Browser-Matrix und Barrierefreiheit (axe-core über Playwright) gehören nicht zu diesem Paket und laufen vor einem Release von Hand, die Content-Security-Policy mit einem Server, der `style-src 'self'` setzt.
- `node skripte/pruefe_xss.js` muss ebenfalls „ALLE PRÜFUNGEN BESTANDEN“ melden: Es rendert die Beispieldaten mit Nutzlasten in Bereichsfarbe, Schlüssel, Sprachcode, Icon, Nummer, Link und Jahr und sucht in der Ausgabe nach aktivem Markup. Nach jeder Änderung am Renderer laufen lassen.
- Sicherheitslücken melden: [`SECURITY.md`](SECURITY.md) nennt Adresse, Fristen und was zum Pattern gehört.
- Stückliste: `SPDX_projektschau-kern.spdx.json` (SPDX 2.3) nennt das Pattern, KERN-Kit, Fira Sans und die Symbole der Beispieldaten mit Version, Lizenz, Urheberangabe und Prüfsumme; die Lizenztexte liegen als `LICENSE`, `vendor/kern/LICENSE.md`, `LICENSE-fira-sans.txt` und `LICENSE-lucide.txt` daneben; sie wird beim Bauen des Pakets erzeugt, nicht von Hand ändern.
- Release: Zum Zip gehört eine Datei mit der SHA-256-Prüfsumme (`shasum -a 256 -c <zip>.sha256`).
- Kit aktualisieren: Version und Prüfsumme in `skripte/kern-sync.sh` eintragen, Skript ausführen, danach `pruefe.py`, weil neue Kit-Versionen Klassen umbenennen können.
- Im Browser prüfen: Kartenzahl, Filter mit Zählern, Sprachwechsel, Zeitleiste, hell und dunkel, Tastaturbedienung mit sichtbarem Fokus, Breiten 400, 820 und 1280 Pixel.

## 6. Barrierefreiheit

Selbsttest, kein Nachweis; Ziel, Prüfungen und offene Punkte stehen in [`ACCESSIBILITY.md`](ACCESSIBILITY.md). Alle Bedienelemente sind Buttons oder Links mit dem Fokusrahmen des Kits, in Darstellungsreihenfolge erreichbar. Filter und Umschalter tragen `aria-pressed`, Gruppen tragen `aria-label` in der aktiven Sprache. Ergebnisse werden über eine Live-Region angesagt. Symbole sind dekorativ (`aria-hidden`), jede Information steht auch als Text. Kontraste für Text und Flächen kommen aus KERN, für die Bereichsfarben gelten die Anforderungen aus 2.4. Ohne JavaScript bleibt das Element leer, weil die Karten aus dem Datenpaket gerendert werden; wer das vermeiden will, erzeugt das Markup mit `Projektschau.render` vorab auf dem Server.

## 7. Sicherheit

Dieses Pattern ist mit [Claude Code](https://claude.com/claude-code) entstanden ([Abschnitt 9](#9-entstehung-und-weiterführung)). Deshalb steht hier, was ich geprüft habe, mit welchen Werkzeugen und was noch aussteht. Alle Prüfungen habe ich selbst gemacht, mit automatischen Werkzeugen und KI-gestützten Reviews. Eine Prüfung durch unabhängige Dritte gab es nicht. Stand 13. Oktober 2026, Fassung 0.1.0.

Das Pattern läuft vollständig im Browser. Es hat keinen Server-Teil und keine Anmeldung, es erhebt keine Daten von Besucher:innen und stellt keine externen Anfragen; Kit, Schriften und Daten liegen lokal. Von außen kommt nur das Datenpaket: die JSON-Datei mit Bereichen, Projekten und Texten, die der Betreiber selbst bereitstellt ([Abschnitt 2](#2-daten); in der Demo `daten/beispiel.json`). Aus ihr baut der Renderer die Karten. Er prüft jedes Feld daraus, bevor es in die Seite gelangt, auch wenn die Datei vom Betreiber selbst stammt, denn sie kann aus einem Redaktionssystem mit mehreren Rollen kommen. Welches Feld wie behandelt wird, steht in [Abschnitt 2.5](#25-eigene-daten-anlegen). Die Prüfungen unten gelten vor allem dieser Strecke.

Alles, was das Paket von anderen mitbringt (KERN-Kit, Fira Sans, Symbole von Lucide), steht mit Herkunft und Lizenz in der Stückliste, das Kit zusätzlich mit Prüfsumme. Die Bestandteile mit Versionsnummer sind in der Schwachstellen-Datenbank [OSV](https://osv.dev) abgefragt, ohne Treffer ([Abschnitt 7.1](#71-was-geprüft-wurde)).

### 7.1 Was geprüft wurde

| Prüfung | Vorgehen | Ergebnis |
|---|---|---|
| Review auf DOM-XSS | KI-gestützter Code-Review von Renderer, Demo und Skripten; Quellen: Datenpaket, Adresse, Hash, Browserspeicher, eingebettetes JSON | 7 Befunde, behoben |
| Nutzlasten im Renderer | `skripte/pruefe_xss.js` rendert die Beispieldaten mit Nutzlasten in Farbe, Schlüssel, Sprachcode, Symbol, Nummer, Link und Jahr und sucht nach aktivem Markup | bestanden |
| Fuzzing | `skripte/pruefe_fuzz.js`: 1000 und 2000 zufällig verstümmelte Pakete mit festem Startwert (Felder entfernt, falsch typisiert, verschachtelt) | keine Ausnahme, kein aktives Markup |
| Unicode-Steuerzeichen | Bidi-, Zero-Width- und Steuerzeichen in Texten und Linktexten | werden entfernt |
| Fehlbedienung (Sharp Edges) | Methode von Trail of Bits: Optionen, Datenfelder, Einbettung und stille Fehlerpfade aus Sicht von Betrieb und Redaktion | 3 Befunde, behoben |
| Unsichere Voreinstellungen (Insecure Defaults) | Methode von Trail of Bits: von Zugangsdaten bis zu Fehlern, die offen statt geschlossen enden | kein Befund |
| Security-Review des gesamten Codes | Datenfluss von der Quelle bis zur Ausgabe | kein Befund ab Stufe Mittel; ein Hinweis umgesetzt |
| Content-Security-Policy | Demo unter `default-src 'self'` ohne `unsafe-inline` | läuft; der Renderer setzt seine Regeln über `adoptedStyleSheets`, die Demo kommt ohne Inline-Skripte und Inline-Stile aus |
| Geheimnisse in der Historie | gitleaks über alle Commits | keine Funde |
| Linter und Datenprüfung | ESLint und stylelint; `skripte/pruefe.py` prüft jede KERN-Klasse und jedes Token gegen das Kit, das Datenpaket und die Kontraste hell und dunkel | ohne Befund |
| Markup | html-validate auf Demo, Dokumentation und gerendertem DOM | ohne Befund |
| Barrierefreiheit | axe-core nach WCAG 2.1 AA und 2.2 AA mit Best Practices: Karten, Zeitleiste, hell und dunkel, beide Sprachen, Breiten 1280, 390 und 320 Pixel; Kontraste aller Texte nachgerechnet, auch beim Überfahren; Tastaturdurchgang mit Prüfung des Fokusrahmens; Textabstände, Schrift 200 %, reduzierte Bewegung | keine offenen Verstöße |
| Browser und Last | Chromium, Firefox und WebKit ohne Konsolenfehler; 1000 Karten | bestanden; 205 ms bis zum Rendern, 5 ms je Filterklick |
| Lighthouse 13.5 | Demo-Seite des Pakets, Mobil-Profil mit simulierter Drosselung, komprimierte Auslieferung | Barrierefreiheit 100, Best Practices 100, Leistung 81. Das Pattern selbst bringt komprimiert rund 29 KB mit (CSS, JavaScript, Beispieldaten); Kit und Schrift lädt eine KERN-Seite ohnehin |
| Lieferkette | KERN-Kit in fester Version, SHA-512-Prüfsumme vor dem Entpacken; SHA-256-Prüfsumme zum Zip | Kit, Fira Sans und Lucide erfasst, Lizenztexte im Paket |
| Stückliste | gegen das JSON-Schema von SPDX 2.3 geprüft; bei jedem Bauen mit dem Paketinhalt verglichen; KERN-Kit 2.8.2 und Lucide 1.49.0 in der Schwachstellen-Datenbank OSV abgefragt (13. Oktober 2026) | gültig und aktuell; keine bekannten Schwachstellen |

### 7.2 Werkzeuge

| Werkzeug | Wofür | Im Paket |
|---|---|---|
| `skripte/pruefe.py`, `skripte/pruefe_xss.js`, `skripte/pruefe_fuzz.js` | Datenpaket, Klassen, Tokens und Kontraste; Nutzlasten; Fuzzing | ja |
| [Claude Code](https://claude.com/claude-code) mit [`/security-review`](https://github.com/anthropics/claude-code-security-review) | Code-Reviews auf DOM-XSS und Security-Review des gesamten Codes | nein |
| [Trail of Bits Skills](https://github.com/trailofbits/skills): [sharp-edges](https://github.com/trailofbits/skills/tree/main/plugins/sharp-edges), [insecure-defaults](https://github.com/trailofbits/skills/tree/main/plugins/insecure-defaults) | Reviews auf Fehlbedienung und unsichere Voreinstellungen | nein |
| [axe-core](https://github.com/dequelabs/axe-core) 4.14 | Barrierefreiheit | nein |
| [Playwright](https://github.com/microsoft/playwright) 1.64 | Browser-Matrix, Tastatur, Kontraste, Content-Security-Policy, Druckansicht | nein |
| [Lighthouse](https://github.com/GoogleChrome/lighthouse) 13.5 | Barrierefreiheit, Best Practices, Leistung | nein |
| [html-validate](https://gitlab.com/html-validate/html-validate) 11.16 | Markup | nein |
| [ESLint](https://github.com/eslint/eslint) 10.12, [stylelint](https://github.com/stylelint/stylelint) 17.16 | JavaScript und CSS | nein |
| [gitleaks](https://github.com/gitleaks/gitleaks) 8.30 | Geheimnisse in der Historie | nein |
| [SPDX 2.3](https://spdx.github.io/spdx-spec/v2.3/) mit [JSON-Schema](https://github.com/spdx/spdx-spec/blob/support/2.3/schemas/spdx-schema.json) | Format und Prüfung der Stückliste `SPDX_projektschau-kern.spdx.json` | Stückliste ja, Schema nein |
| [OSV](https://osv.dev) ([Repositorium](https://github.com/google/osv.dev)) | bekannte Schwachstellen der Bestandteile | nein |

Die Werkzeuge außerhalb des Pakets laufen vor jedem Stand lokal. Die drei Prüfskripte im Paket brauchen nur Python und Node.js und laufen nach jeder Änderung am Renderer ([Abschnitt 5](#5-prüfen-und-pflegen)).

### 7.3 Was aussteht

- Unabhängige Prüfung: Es gab keinen Pentest und kein Audit durch Dritte.
- Screenreader und Nutzungstest: axe-core deckt nur einen Teil der Kriterien ab. Ein Durchgang mit Screenreader und ein Test mit Nutzer:innen stehen aus.
- KERN-Kit: Das [Kit](https://gitlab.opencode.de/kern-ux/kern-ux-plain) ist unverändert in fester Version eingebunden. Geprüft ist, dass das Paket der Registry entspricht und dass jede verwendete Klasse darin existiert. Das Kit selbst habe ich nicht geprüft.
- [Trusted Types](https://developer.mozilla.org/en-US/docs/Web/API/Trusted_Types_API): nicht getestet. Der Renderer setzt das geprüfte Markup an einer Stelle über `innerHTML`; eine Seite, die Trusted Types erzwingt, braucht dafür eine eigene Richtlinie.
- Automatische Prüfkette: Die Prüfungen laufen noch nicht bei jedem Stand von selbst, sondern lokal von Hand.
- Signatur: Zum Zip gehört eine SHA-256-Prüfsumme, eine Signatur noch nicht.
- Schwachstellen der Bestandteile: Die [Abfrage bei OSV](https://osv.dev) ist eine Momentaufnahme. Eine regelmäßige Abfrage gibt es noch nicht; für Fira Sans nennt die Stückliste keine Version, die sich abfragen ließe.
- Einbettende Seite: Server, Header und Content-Security-Policy gehören dem Betreiber. Wer `Projektschau.render` selbst aufruft und das Ergebnis weiterverarbeitet, verlässt die geprüfte Strecke.

Sicherheitslücken bitte vertraulich melden: [`SECURITY.md`](SECURITY.md) nennt Adresse und Fristen.

## 8. Lizenz

Code und Dokumentation: [EUPL-1.2](LICENSE) (englischer Wortlaut im Paket, [deutscher Lizenztext bei der EU](https://eupl.eu/1.2/de/); alle Sprachfassungen gelten gleich). KERN-Kit: EUPL-1.2 (`vendor/kern/LICENSE.md`). [Fira Sans](https://github.com/mozilla/Fira): [SIL Open Font License 1.1](https://openfontlicense.org). Symbole in den Beispieldaten nach [Lucide](https://lucide.dev) ([ISC](https://github.com/lucide-icons/lucide/blob/main/LICENSE)).

## 9. Entstehung und Weiterführung

### 9.1 Wie dieses Projekt entstanden ist

Ausgangspunkt ist eine [Projektübersicht](https://ankerpunkt-hoherflaeming.de/projekte/), die bei einem regionalen Netzwerk als laufendes Projekt im Einsatz ist; parallel entsteht daraus ein WordPress-Plugin. Von dort stammen das Datenpaket-Format, die Logik für Filter, Zeitleiste, Sprachen und Adresszeile sowie die Gestaltungsentscheidungen, die hier auf KERN übertragen wurden. Das KERN-Pattern ist mit Claude Code entstanden, dem Kommandozeilen-Werkzeug von Anthropic. Die Rollen: Der User gibt Richtung, Maßstab und Entscheidungen vor und prüft jeden Stand im Browser; die KI liest die Quellen ([KERN-Kit](https://www.npmjs.com/package/@kern-ux/native), [KERN-Doku](https://www.kern-ux.de), [Katalog-Bedingungen](https://katalog.kern-ux.de/de/nutzungsbedingungen), die bestehende Projektübersicht), schreibt Code und Doku, misst im Browser nach und erklärt, was Kit ist und was Eigenbau.

Der Ablauf in Stufen:

1. **Plan:** Erst wurde im Plan-Modus geklärt, was realistisch ist. Ergebnis: ein eigenständiges Projekt, EUPL-1.2 wegen der Katalog-Bedingungen, Standalone-Demo, Ziel KERN-Katalog.
2. **Gerüst:** KERN-Kit in fester Version holen, Renderer und CSS schreiben, Demo mit erfundenen Beispieldaten, Prüfskript.
3. **Angleichen ans Original:** Schritt für Schritt wurde die Darstellung an die bestehende Projektübersicht herangeführt, immer mit der Frage, was davon KERN-Standard ist. Bausteine aus dem Kit vor Eigenbau; Eigenbau nur aus KERN-Tokens und im README benannt.
4. **Feinarbeit per Screenshot:** Die meisten Anweisungen waren ein Bildschirmfoto plus ein Satz, etwa „Symbol mittig zur ersten Zeile der Überschrift“, „Bereich und Filter auf Höhe der ersten Zeile“, „der Strich darf nicht über den Punkt hinausschauen“. Jede Änderung wurde im Browser nachgemessen, dokumentiert und einzeln committet.
5. **Doku:** Eine README mit Abschnitten statt mehrerer Dokumente, zweisprachig, als Seiten im KERN-Stil erzeugt.

Was sich bewährt hat: Jede Antwort der KI nennt, was Kit ist und was Abweichung. Das Prüfskript läuft vor jedem Commit. Entscheidungen fallen klein und einzeln, nicht als großer Umbau. Und die Frage „ist das KERN-Standard?“ stand über jedem Vorschlag.

### 9.2 Dankeschön

Danke an [Axel Wolters](https://gitlab.opencode.de/OC000011858689), Senatskanzlei Hamburg und Vertreter des Auftraggebers Hamburg im Projekt KERN, für den Blick auf das KERN-Pattern, und an das ganze Team von [KERN](https://www.kern-ux.de) für den kontinuierlichen, tollen Austausch und die wohlwollende Atmosphäre. Kommt gerne dazu: [Community und Mitwirken bei KERN](https://www.kern-ux.de/community-und-mitwirken/). Danke an [Michael Plas](https://michaelplas.de) für den Blick auf die WordPress-Fassung. Was aus den Rückmeldungen wird, steht im Änderungsprotokoll.

### 9.3 Die Prompts zum Kopieren

Die wichtigsten Anweisungen in der Reihenfolge, in der sie gegeben wurden, sprachlich geglättet. Sie lassen sich für ein ähnliches Vorhaben übernehmen; Pfade und Adressen anpassen.

```
Bau eine KERN-Version hier in diesem Projekt neu auf, mit dem Wissen aus dem WordPress-Plugin. Nimm das Wissen aus dem KERN-UX-Theme für WordPress auf openCode mit und die letzte KERN-Version, sofern nötig. Gerne erst im Plan-Modus klären, was realistisch ist, gegebenenfalls eine Standalone-Version nur für KERN, da das Plugin für WordPress schon existiert.
```

```
Ergänze als Ziel, dass es in den KERN-Katalog gehen soll. Lies dazu die Doku und alle Anforderungen. Das WordPress-Plugin ist davon unabhängig, also ein Unterprojekt.
```

```
Fülle die Standalone-Demo-Seite mit Beispielinhalten, gerne rund 32 Karten und ein weiterer Filter. Bitte auch eine Kombination möglich machen, bei der nichts zu finden ist.
```

```
Fällt dir sonst noch etwas ein oder auf, was ich KERN-Standard machen kann? Bei deinen Vorschlägen bitte alles außer den KERN-Symbolen umsetzen.
```

```
Könntest du den Algorithmus auf das Farbsystem umstellen, das auch KERN für die Farbberechnung nutzt, und das in OKLCH rechnen? Siehe die KERN-Seite zur Farbe. Schreibe bitte auch, wie die Farben programmatisch aus den Grundfarben berechnet werden.
```

```
Beschreibe die Daten speziell für diesen Prototypen: wie sie angelegt werden und wie sie aufbereitet sind. Ziel ist, dass ein Programmierer eine komplette Doku liest, mit dem Hintergrund, wie die Daten aufgebaut sind und wo sie ausgespielt werden, dazu ein Teil zum Styling, was KERN-Komponenten sind, welche ergänzt wurden und wo sich was anpassen lässt.
```

```
README und Entwicklerdoku bitte als Standard-KERN-Doku wie auf der Webseite gestalten, DE und EN, als ein Dokument mit Abschnitten. Gibt es ein mitlaufendes Inhaltsverzeichnis in der Standard-Doku? Dann bitte übernehmen. Codebeispiele immer mit einem dezenten Kopierknopf und umbrechen lassen. Bitte immer die README aktualisieren und ganz unten ein Änderungsprotokoll nach Standard führen, wie beim Plugin.
```

Für die Feinarbeit reicht jeweils ein Bildschirmfoto mit ein, zwei Sätzen. Jede Zeile hier war ein eigener Auftrag:

```
Das Symbol soll mittig zur ersten Zeile der Überschrift stehen.
Bereich und Filter auf der Höhe der ersten Zeile.
Hier geht der Strich noch raus; beim letzten Punkt soll die Linie auch nicht mehr weiterlaufen.
Mobil sollen Bereich und Filter gleich aussehen, mit Aufklapper; der Filter-Aufklapper ist viel zu groß.
Ist der Abstand jetzt der Standard? Darf er auch kleiner als 1rem sein?
```

### 9.4 Wie sich das Projekt erweitern lässt

- **Eigene Daten:** `daten/beispiel.json` ersetzen, Farben je Bereich mit `skripte/farben.py` aus einer Grundfarbe ableiten, mit `skripte/pruefe.py` prüfen, mit `skripte/einbetten.py` in die Demo schreiben. [Abschnitt 2.5](#25-eigene-daten-anlegen).
- **In eine bestehende KERN-Seite einbauen:** die drei Dateien und das Kit einbinden, ein Element mit `data-projektschau` und `data-src` setzen. Startansicht, Vorfilter und Überschriftenebene über die Attribute aus [Abschnitt 1](#1-demo-und-einbinden).
- **Server-seitig rendern:** `Projektschau.render(daten, optionen)` liefert das Markup als String; so lässt sich die Übersicht auch ohne JavaScript im Browser ausliefern, zum Beispiel aus einem CMS oder einem kleinen Node-Skript.
- **Daten aus einer Quelle ziehen:** Das Datenpaket ist einfaches JSON. Ein Export aus einer Tabelle oder einem CMS genügt; das WordPress-Plugin, das parallel entsteht, nutzt dasselbe Paketformat.
- **Mehr Sprachen:** `sprachen` erweitern und jedes Sprachpaar ergänzen; der Umschalter wächst mit. Bei mehr als drei Sprachen wird die Reihe aus Knöpfen breit und auf schmalen Bildschirmen unübersichtlich; dann passt eine Auswahlliste (Dropdown) als Muster besser, etwa das Select-Feld des KERN-Kits. Die Doku-Seiten brauchen je Sprache eine Markdown-Datei und einen Eintrag in `skripte/doku_html.py`.
- **KERN-Symbole:** Für Kopierknopf, Hell/Dunkel und Aufklapper hat das Kit eigene Symbole (`kern-icon--content-copy`, `--light-mode`, `--dark-mode`, `--chevron-*`). Projekt- und Bereichssymbole bleiben Lucide, dafür hat KERN keine Motive.
- **Kit-Updates:** Version und Prüfsumme in `skripte/kern-sync.sh` eintragen, Skript laufen lassen, `pruefe.py` meldet umbenannte Klassen.
- **Dunkelmodus-Kontrast prüfen:** `pruefe.py` rechnet bisher nur die hellen Werte nach; eine Prüfung von `fg` dunkel gegen den dunklen KERN-Hintergrund wäre die nächste Ergänzung.
- **Kapselung des Kits:** Für Seiten, die nicht mit KERN gestaltet sind, bräuchte es ein auf den Wrapper gekapseltes Kit. Das ist bewusst nicht Teil des Patterns.

## 10. Über den Absender

![](doku/don-ludwig.jpg)

Feedback, Fragen oder einfach Hallo sagen: ich freu mich.

Don Ludwig, freier UX-Designer. Ich baue Design-Systeme, begleite agile Produktentwicklung und arbeite daran, die Zusammenarbeit zwischen Design und Entwicklung besser zu machen. Mein Prozess: nutzerzentriert denken, iterativ arbeiten, technische Rahmenbedingungen verstehen statt ignorieren. Für dieses Pattern habe ich mit Claude Code gearbeitet; wie, steht in [Abschnitt 9](#9-entstehung-und-weiterführung). Dieses Pattern ist aus der [Projektübersicht](https://ankerpunkt-hoherflaeming.de/projekte/) eines regionalen Netzwerks in Brandenburg entstanden; ein WordPress-Plugin mit demselben Datenformat ist in Arbeit.

[LinkedIn](https://www.linkedin.com/in/donludwig/) · [don@thinkrepeat.com](mailto:don@thinkrepeat.com) · [thinkrepeat.com](https://thinkrepeat.com) · [GitHub](https://github.com/donludwig)

## 11. Änderungen

Alle nennenswerten Änderungen stehen hier, neueste Version zuerst. Das Format folgt [Keep a Changelog](https://keepachangelog.com/de/1.1.0/), die Versionsnummern der [semantischen Versionierung](https://semver.org/lang/de/). Jede Version trägt einen Namen.

### 0.1.0 „Musterstadt“

Erste Veröffentlichung, benannt nach dem erfundenen Ort der Beispieldaten. Stand 2026-10-13.

#### Hinzugefügt

- **Karten:** jedes Projekt als Karte mit Bereich, Titel, Status, Beschreibung, Listen, Kennzahl und Links, in der Farbe seines Bereichs; wahlweise mit großem Symbol über dem Kartenkopf ([Abschnitt 3.2](#32-wo-welches-feld-ausgespielt-wird)).
- **Zeitleiste:** dieselben Projekte nach Jahren geordnet, mit Zeitraum und Notiz ([Abschnitt 2.2](#22-zeitleiste)).
- **Filter:** nach Bereich und Einordnung, mit Trefferzahlen und einem Hinweis, wenn nichts passt. Filter, Ansicht und Sprache stehen in der Adresszeile, ein Link führt also genau zu dieser Auswahl ([Abschnitt 3.5](#35-filter-ansicht-und-adresszeile)).
- **Zwei Sprachen** mit Umschalter ([Abschnitt 3.3](#33-sprachen)).
- **Hell und dunkel:** beide Farbschemata des KERN-Kits; die Farben eines Bereichs entstehen aus einer Grundfarbe ([Abschnitt 2.6](#26-farben-programmatisch-ableiten)).
- **Druckansicht:** Titel, Einleitung und die gefilterte Ansicht, ohne Bedienelemente.
- **Ohne Framework und Build:** eine JavaScript-Datei und eine CSS-Datei auf dem KERN-Kit 2.8.2, das unverändert im Paket liegt; keine externen Anfragen ([Abschnitt 1](#1-demo-und-einbinden)).
- **Datenpaket:** eine JSON-Datei mit Bereichen, Einordnungen, Projekten und Texten ([Abschnitt 2](#2-daten)); 32 erfundene Beispielprojekte in vier Bereichen liegen bei.
- **Barrierefreiheit:** Tastaturbedienung mit sichtbarem Fokus, Ansage der Ergebnisse, geprüfte Kontraste, die Systemeinstellung „Bewegung reduzieren“ wird beachtet. Selbsttest mit axe-core nach WCAG 2.1 AA und 2.2 AA ohne offene Verstöße ([Abschnitt 6](#6-barrierefreiheit)).
- **Sicherheit:** Der Renderer prüft jedes Feld des Datenpakets und läuft unter einer strengen Content-Security-Policy. Prüfskripte, Sicherheitsrichtlinie (`SECURITY.md`) und Stückliste (SPDX 2.3) liegen bei ([Abschnitt 7](#7-sicherheit)).
- **Demo und Dokumentation:** Demo-Seite, diese README in Deutsch und Englisch, beide auch als HTML-Seiten im KERN-Stil; Gestaltungs- und Inhaltsregeln für eigene Karten ([Abschnitt 4.5](#45-gestaltungsregeln)).
