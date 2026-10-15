# Bedrohungsmodell der Projektschau für KERN

Kurzfassung: was geschützt wird, wem vertraut wird, über welche Wege Daten hereinkommen und welche Prüfung jede Annahme absichert. Ergebnisse der Prüfungen stehen im [Prüfbericht](pruefbericht.md).

## Pattern

### Was geschützt wird

Die einbettende Seite und ihre Besucher:innen: Das Pattern darf aus einem Datenpaket kein aktives Markup, keine fremden Stylesheets und keine Skripte erzeugen.

### Vertrauen

| Was | Vertrauen |
|---|---|
| `projektschau.js`, `projektschau.css`, KERN-Kit unter `vendor/kern/` | vertrauenswürdig; Kit in fester Version mit Prüfsumme |
| Datenpaket (JSON, eingebettet oder per `fetch`) | nicht vertrauenswürdig |
| Adresszeile und Browserspeicher | nicht vertrauenswürdig |
| Einbettende Seite, ihr Server, ihre Content-Security-Policy | Sache der Betreiber:innen |

### Wege hinein

| Weg | Annahme | Abgesichert durch |
|---|---|---|
| Felder des Datenpakets | Jeder Wert kann fehlen, den falschen Typ haben oder Markup enthalten | Formatprüfung für Farben, Schlüssel, Sprachcodes, Nummern, Jahre und Links; Positivliste für HTML-Felder; Symbole auf Formen reduziert; `pruefe_xss.js`, `pruefe_fuzz.js` |
| Unicode-Steuerzeichen in Texten | Linktexte können optisch umgedreht oder versteckt werden | Filter in `esc()` und in HTML-Feldern |
| `?lang=`, Filter in der Adresse, gespeicherte Wahl | frei wählbar | Vergleich gegen vorhandene Werte |
| Neue Kit-Version | Klassen und Tokens können sich ändern, das Paket könnte manipuliert sein | `kern-sync.sh` mit Prüfsumme, `pruefe.py` gegen das Kit, Stückliste |
| Startseite unter `website/` mit `?theme=` und `?stelle=` | frei wählbar | `theme` nur gegen `dark`/`light` verglichen; `stelle` nur als Zahlen gelesen und ausschließlich zum Scrollen benutzt, ungültige oder negative Werte werden verworfen |
| KERN-Logo als Inline-SVG der Startseite | gebündelter Bestandteil eines Dritten, nicht unter der EUPL | unverändert aus der Quelldatei übernommen, nur zwei Füllfarben durch Variablen ersetzt; in der Stückliste geführt |

### Restrisiken

- Wer `render()` selbst einbettet und das Ergebnis weiterverarbeitet, verlässt die geprüfte Strecke.
- Ohne Content-Security-Policy der einbettenden Seite fehlt die zweite Verteidigungslinie; Pattern, Demo, Dokumentation und Startseite laufen unter `script-src 'self'; style-src 'self'` ohne Inline-Skripte und Inline-Stile.
- Barrierefreiheit und Sicherheit sind selbst geprüft; ein externer Nachweis steht aus.

## Seite projektschau.thinkrepeat.com

### Was geschützt wird

Die Besucher:innen der Seite, die Dateien auf dem Webspace und der FTP-Zugang. Die Seite ist statisch: kein Server-Code, keine Formulare, keine Anfragen an Dritte.

### Wege hinein

| Weg | Annahme | Abgesichert durch |
|---|---|---|
| Adressparameter `?theme=`, `?lang=`, `?stelle=` und Browserspeicher | frei wählbar | wie beim Pattern; die Seite setzt sie nie als Markup ein |
| Eingeschleuste Skripte oder Stile | Ein Fehler im Markup oder eine manipulierte Datei könnte fremden Code laden | Content-Security-Policy per `.htaccess` (`default-src 'self'`, keine Inline-Skripte und -Stile, `frame-ancestors 'none'`, `object-src 'none'`, `base-uri 'none'`), dazu `X-Content-Type-Options: nosniff` und `Referrer-Policy: no-referrer`; Ordnerlisten sind gesperrt, HTTP leitet auf HTTPS um |
| Veröffentlichung per FTPS-Skript des Autors (nicht im Paket) | Das Passwort könnte mitgelesen werden, ein falscher Zielordner könnte fremde Dateien überschreiben, ein abgebrochener Upload halbe Dateien hinterlassen | explizites FTPS mit Zertifikatsprüfung, auch für die Daten; Passwort im Schlüsselbund, nie im Repositorium; in einen nicht leeren Ordner ohne eigene Dateiliste wird nur nach ausdrücklicher Übernahme geschrieben; Dateien gehen unter Zwischennamen hoch und werden dann umbenannt; gelöscht wird nur, was in der eigenen Liste steht, ohne `..` und absolute Pfade; Liste und Zwischendateien sind per `.htaccess` gesperrt; Tests des Skripts gegen einen nachgebauten Server |

### Restrisiken

- Fehlerseiten des Hosters (403, 404) liegen außerhalb des Ordners; ob sie die Header der `.htaccess` tragen, hängt vom Hoster ab.
- `Permissions-Policy` und die Cross-Origin-Header (COEP, COOP, CORP) sind nicht gesetzt; die Seite bindet nichts von außen ein und fragt keine Gerätefunktionen an.
- Wer Zugriff auf den Rechner und den entsperrten Schlüsselbund hat, kann die Seite ersetzen.
