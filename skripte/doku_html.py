#!/usr/bin/env python3
"""Erzeugt aus README.md und README.en.md je eine HTML-Seite im KERN-Stil (doku/readme.html, doku/readme.en.html).

Aufruf aus dem Ordner kern/: python3 skripte/doku_html.py
Braucht das Python-Modul markdown. Die Markdown-Dateien bleiben die Quelle; die HTML-Dateien nicht von Hand ändern.
"""
import re
import sys
from pathlib import Path

import markdown
from markdown.extensions.toc import slugify_unicode

WURZEL = Path(__file__).resolve().parent.parent
# (Quelle, Ziel, Sprache, Beschriftungen)
SEITEN = [
    ("README.md", "readme.html", "de", {"demo": "Demo", "readme": "Dokumentation", "theme": "Hell / Dunkel", "theme_aria": "Dunkles Farbschema", "sprache": "Sprache wählen", "seiten": "Seiten", "skip": "Zum Inhalt springen", "kopieren": "Kopieren", "kopiert": "Kopiert", "kopieren_aria": "Code in die Zwischenablage kopieren", "inhalt": "Auf dieser Seite",
        "fuss": 'Code unter <a class="kern-link" href="../LICENSE">EUPL-1.2</a>. KERN-Kit (<a class="kern-link" href="../vendor/kern/LICENSE.md">EUPL-1.2</a>, Version in <code>vendor/kern/VERSION</code>), <a class="kern-link" href="https://github.com/mozilla/Fira">Fira Sans</a> (<a class="kern-link" href="https://openfontlicense.org">SIL OFL 1.1</a>), Symbole nach <a class="kern-link" href="https://lucide.dev">Lucide</a> (ISC). Alle Inhalte der Demo sind erfunden.'}),
    ("README.en.md", "readme.en.html", "en", {"demo": "Demo", "readme": "Documentation", "theme": "Light / Dark", "theme_aria": "Dark colour scheme", "sprache": "Choose language", "seiten": "Pages", "skip": "Skip to content", "kopieren": "Copy", "kopiert": "Copied", "kopieren_aria": "Copy code to clipboard", "inhalt": "On this page",
        "fuss": 'Code under <a class="kern-link" href="../LICENSE">EUPL-1.2</a>. KERN kit (<a class="kern-link" href="../vendor/kern/LICENSE.md">EUPL-1.2</a>, version in <code>vendor/kern/VERSION</code>), <a class="kern-link" href="https://github.com/mozilla/Fira">Fira Sans</a> (<a class="kern-link" href="https://openfontlicense.org">SIL OFL 1.1</a>), icons after <a class="kern-link" href="https://lucide.dev">Lucide</a> (ISC). All demo content is fictitious.'}),
]

KLASSEN = [
    (r"<h1 id=", '<h1 class="kern-heading-x-large" id='),
    (r"<h2 id=", '<h2 class="kern-heading-large" id='),
    (r"<h3 id=", '<h3 class="kern-heading-medium" id='),
    (r"<h4 id=", '<h4 class="kern-heading-small" id='),
    (r"<p>", '<p class="kern-body">'),
    (r"<ul>", '<ul class="kern-list kern-list--bullet">'),
    (r"<ol>", '<ol class="kern-list kern-list--number">'),
    (r"<a ", '<a class="kern-link" '),
    (r"<table>", '<div class="kern-table-responsive"><table class="kern-table kern-table--striped">'),
    (r"</table>", "</table></div>"),
    (r"<thead>", '<thead class="kern-table__header">'),
    (r"<tbody>", '<tbody class="kern-table__body">'),
    (r"<tr>", '<tr class="kern-table__row">'),
    (r"<th>", '<th class="kern-table__cell">'),
    (r"<td>", '<td class="kern-table__cell">'),
]


def seite(titel: str, inhalt: str, navi: str, sprache: str, t: dict, toc: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="{sprache}" data-kern-theme="light">
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<title>{titel} – Projektschau für KERN</title>
	<script>
		/* Reihenfolge: Adresse (?theme=, für Seitenwechsel ohne Browserspeicher), gespeicherte Wahl, Systemeinstellung */
		( function () {{ var t = new URLSearchParams( location.search ).get( 'theme' ); if ( t !== 'dark' && t !== 'light' ) {{ t = null; try {{ t = localStorage.getItem( 'ps-theme' ); }} catch ( e ) {{}} }} if ( ! t && window.matchMedia && matchMedia( '(prefers-color-scheme: dark)' ).matches ) {{ t = 'dark'; }} if ( t ) {{ document.documentElement.setAttribute( 'data-kern-theme', t ); try {{ localStorage.setItem( 'ps-theme', t ); }} catch ( e ) {{}} }} }} )();
	</script>
	<link rel="icon" href="data:,">
	<link rel="stylesheet" href="../vendor/kern/fonts/fira-sans.css">
	<link rel="stylesheet" href="../vendor/kern/kern.min.css">
	<link rel="stylesheet" href="../vendor/kern/kern-grid.min.css">
	<style>
		.demo-kopf {{ display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: var(--kern-metric-space-small, 8px); padding: var(--kern-metric-space-small, 8px) 0; margin-bottom: var(--kern-metric-space-large, 24px); border-bottom: var(--kern-metric-border-width-light, 1px) solid var(--kern-color-decorative-border-contextual, #c0c3d5); }}
		.demo-navi {{ display: flex; gap: var(--kern-metric-space-default, 16px); margin-inline: auto var(--kern-metric-space-default, 16px); }}
		@media (max-width: 48rem) {{ .demo-kopf > p {{ flex: 1 1 100%; }} .demo-navi {{ margin-inline-start: 0; }} #farbschema {{ margin-inline-start: auto; }} }}
		.demo-fuss {{ margin-top: calc(var(--kern-metric-space-x-large, 32px) * 3); padding-bottom: var(--kern-metric-space-x-large, 32px); }}
		.demo-fuss .kern-divider {{ margin-bottom: var(--kern-metric-space-default, 16px); }}
		.demo-navi .kern-link {{ display: inline-flex; align-items: center; min-height: 24px; padding-block: 0; line-height: 1; }}
		.demo-skip {{ position: absolute; inset-block-start: var(--kern-metric-space-small, 8px); inset-inline-start: var(--kern-metric-space-small, 8px); z-index: 100; padding: var(--kern-metric-space-small, 8px) var(--kern-metric-space-default, 16px); border-radius: var(--kern-metric-border-radius-default, 4px); background: var(--kern-color-layout-background-default, #fff); transform: translateY(-300%); }}
		.demo-skip:focus {{ transform: none; }}
		/* Links im Fuß in der Schriftgröße des Fußtexts, ohne den Grundlinienabstand des Kit-Links */
		.demo-fuss .kern-link {{ font-size: inherit; line-height: inherit; padding: 0; }}
		.demo-navi [aria-current] {{ text-decoration: none; color: var(--kern-color-layout-text-default, #131525); font-weight: var(--kern-typography-font-weight-semi-bold, 600); }}
		.ps-icon {{ width: 1em; height: 1em; flex: none; margin-inline-end: var(--kern-metric-space-x-small, 4px); color: var(--kern-color-action-default-contextual, #2044aa); }}
		[data-kern-theme="dark"] .demo-sonne, :root:not([data-kern-theme="dark"]) .demo-mond {{ display: none; }}
		/* Schmale Bildschirme: Farbschalter mit zwei Feldern, Sonne und Mond, das gewählte Feld gefüllt; der Name bleibt als aria-label */
		@media (max-width: 48rem) {{
			.demo-kopf > #farbschema {{ padding: 0; gap: 0; min-height: 0; align-items: stretch; overflow: hidden; background: none; border: var(--kern-metric-border-width-light, 1px) solid var(--kern-color-action-default-contextual, #2044aa); color: var(--kern-color-action-default-contextual, #2044aa); }}
			.demo-kopf > #farbschema .ps-icon {{ display: block; box-sizing: content-box; width: 1rem; height: 1rem; margin: 0; padding: var(--kern-metric-space-small, 8px) var(--kern-metric-space-default, 16px); }}
			.demo-kopf > #farbschema .kern-label {{ position: absolute; width: 1px; height: 1px; overflow: hidden; clip-path: inset(50%); white-space: nowrap; }}
			:root:not([data-kern-theme="dark"]) .demo-kopf > #farbschema .demo-sonne, [data-kern-theme="dark"] .demo-kopf > #farbschema .demo-mond {{ background: var(--kern-color-action-default-contextual, #2044aa); color: var(--kern-color-action-on-default-contextual, #fff); }}
		}}
		/* Gleiche Lage wie der Sprachumschalter der Demo: 24 px unter der Kopfzeile, 24 px über dem Inhalt */
		.doku-lang {{ gap: 0; justify-content: flex-end; margin-bottom: var(--kern-metric-space-small, 8px); }}
		/* Überschrift und Einleitung wie in der Demo: 8 px unter dem Schalter, Einleitung in der großen Textstufe */
		.doku > h1 + p {{ margin-top: calc(-1 * var(--kern-metric-space-small, 8px)); }}
		.doku-lang .kern-btn {{ margin: 0; border-radius: 0; }}
		.doku-lang .kern-btn--secondary {{ border-color: var(--kern-color-action-default-contextual, #2044aa); }}
		.doku-lang .kern-btn + .kern-btn {{ margin-inline-start: -1px; }}
		.doku-lang .kern-btn:first-child {{ border-start-start-radius: var(--kern-metric-border-radius-default, 4px); border-end-start-radius: var(--kern-metric-border-radius-default, 4px); }}
		.doku-lang .kern-btn:last-child {{ border-start-end-radius: var(--kern-metric-border-radius-default, 4px); border-end-end-radius: var(--kern-metric-border-radius-default, 4px); }}
		.doku-lang .kern-btn:focus-visible, .doku-lang .kern-btn--primary {{ z-index: 1; }}
		.doku-layout {{ display: grid; grid-template-columns: minmax(0, 52rem) 1fr; gap: var(--kern-metric-space-x-large, 32px); align-items: start; }}
		.doku {{ max-width: 52rem; display: flex; flex-direction: column; gap: var(--kern-metric-space-default, 16px); }}
		/* Mitlaufendes Inhaltsverzeichnis wie in der KERN-Doku: rechts, haftet beim Scrollen, aktiver Abschnitt hervorgehoben */
		.doku-toc {{ position: sticky; top: var(--kern-metric-space-large, 24px); max-width: 18rem; justify-self: end; width: 100%; border-left: var(--kern-metric-border-width-light, 1px) solid var(--kern-color-decorative-border-contextual, #c0c3d5); padding-left: var(--kern-metric-space-default, 16px); }}
		.doku-toc .kern-label {{ display: block; padding: 0 0 var(--kern-metric-space-small, 8px); }}
		.doku-toc ul {{ list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: var(--kern-metric-space-x-small, 4px); }}
		.doku-toc .kern-link {{ text-decoration: none; color: var(--kern-color-layout-text-muted, #51577a); font-size: var(--kern-typography-font-size-small-static, 16px); line-height: var(--kern-typography-line-height-medium-static, 24px); }}
		.doku-toc .kern-link:hover, .doku-toc .kern-link:focus-visible {{ text-decoration: underline; }}
		.doku-toc .kern-link[aria-current="true"] {{ color: var(--kern-color-action-default, #2044aa); font-weight: var(--kern-typography-font-weight-semi-bold, 600); }}
		@media (max-width: 64rem) {{ .doku-layout {{ grid-template-columns: 1fr; }} .doku-toc {{ position: static; order: -1; max-width: none; border-left: 0; padding-left: 0; }} }}
		.doku h2 {{ margin-top: var(--kern-metric-space-x-large, 32px); }}
		.doku h3 {{ margin-top: var(--kern-metric-space-default, 16px); }}
		.doku-code {{ position: relative; }}
		.doku-code .kern-btn {{ position: absolute; right: var(--kern-metric-space-small, 8px); bottom: var(--kern-metric-space-small, 8px); margin: 0; min-height: 0; padding: var(--kern-metric-space-x-small, 4px); opacity: .6; }}
		.doku-code .kern-btn .kern-label:empty {{ display: none; }}
		.doku-code .kern-btn:hover, .doku-code .kern-btn:focus-visible {{ opacity: 1; }}
		.doku-code .kern-btn .kern-label {{ padding: var(--kern-metric-space-2x-small, 2px) var(--kern-metric-space-x-small, 4px); font-size: var(--kern-font-size-14, .875rem); }}
		.doku-code .ps-icon {{ margin: 0; width: 1.25rem; height: 1.25rem; }}
		.doku pre {{ width: 100%; box-sizing: border-box; margin: 0; padding: var(--kern-metric-space-default, 16px) var(--kern-metric-space-default, 16px) calc(var(--kern-metric-space-x-large, 32px) + var(--kern-metric-space-small, 8px)); white-space: pre-wrap; overflow-wrap: anywhere; border-radius: var(--kern-metric-border-radius-default, 4px); background: var(--kern-color-layout-background-default-surface, #f3f4f7); border: var(--kern-metric-border-width-light, 1px) solid var(--kern-color-decorative-border-contextual, #c0c3d5); }}
		.doku code {{ overflow-wrap: anywhere; font-family: var(--kern-typography-font-family-fira-mono, monospace); font-size: var(--kern-font-size-14, .875rem); color: var(--kern-color-layout-text-default, #131525); }}
		.doku :not(pre) > code {{ padding: 0 var(--kern-metric-space-x-small, 4px); border-radius: var(--kern-metric-border-radius-small, 2px); background: var(--kern-color-layout-background-default-surface, #f3f4f7); }}
		.doku .kern-list--bullet li, .doku .kern-list--number li {{ padding-block: 0; }}
		.doku .kern-table__cell {{ vertical-align: top; }}
		.doku .kern-table__cell:first-child code {{ white-space: nowrap; }}
		/* Links im Fließtext erben Zeilenhöhe und Schriftgröße, sonst vergrößert der Grundlinienabstand des Kit-Links die Zeile */
		.doku p .kern-link, .doku li .kern-link, .doku td .kern-link {{ display: inline; padding: 0; line-height: inherit; font-size: inherit; }}
		.doku-autor {{ display: flex; gap: var(--kern-metric-space-large, 24px); align-items: flex-start; }}
		.doku-foto {{ width: 6rem; height: 6rem; flex: none; object-fit: cover; border-radius: 50%; }}
		.doku-autor-links {{ margin-top: var(--kern-metric-space-small, 8px); gap: var(--kern-metric-space-default, 16px) var(--kern-metric-space-large, 24px); flex-wrap: wrap; }}
		@media (max-width: 40rem) {{ .doku-autor {{ flex-direction: column; }} }}
		/* Tabellen scrollen auf schmalen Bildschirmen in ihrer KERN-Hülle statt die Seite zu verbreitern */
		.doku {{ min-width: 0; }}
		.doku > * {{ min-width: 0; max-width: 100%; }}
		.doku .kern-table-responsive {{ width: 100%; }}
		@media (prefers-reduced-motion: reduce) {{ html {{ scroll-behavior: auto; }} }}
		.doku .kern-table-responsive[tabindex]:focus-visible {{ outline: 4px solid var(--kern-color-action-focus-default-contextual, #454B6B); outline-offset: 2px; }}
		.doku .kern-table {{ min-width: 36rem; }}
	</style>
</head>
<body>
	<a class="kern-link demo-skip" href="#inhalt">{t["skip"]}</a>
	<div class="kern-container">
		<header class="demo-kopf">
			<p class="kern-body kern-body--bold">Projektschau für KERN · {titel}</p>
			<nav class="demo-navi" aria-label="{t["seiten"]}">{navi}</nav>
			<button type="button" class="kern-btn kern-btn--tertiary kern-btn--small" id="farbschema" role="switch" aria-checked="false" aria-label="{t["theme_aria"]}">
				<svg class="ps-icon demo-sonne" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/></svg>
				<svg class="ps-icon demo-mond" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
				<span class="kern-label">{t["theme"]}</span>
			</button>
		</header>
		<div class="kern-btn-wrapper doku-lang" role="group" aria-label="{t["sprache"]}">
			<a class="kern-btn kern-btn--x-small {"kern-btn--primary" if sprache == "de" else "kern-btn--secondary"}" href="readme.html" data-lang="de" aria-current="{"page" if sprache == "de" else "false"}"><span class="kern-label">DE</span></a>
			<a class="kern-btn kern-btn--x-small {"kern-btn--primary" if sprache == "en" else "kern-btn--secondary"}" href="readme.en.html" data-lang="en" aria-current="{"page" if sprache == "en" else "false"}"><span class="kern-label">EN</span></a>
		</div>
		<div class="doku-layout">
		<main id="inhalt" class="doku">
{inhalt}
		</main>
		<nav class="doku-toc" aria-label="{t["inhalt"]}"><span class="kern-label">{t["inhalt"]}</span><ul>{toc}</ul></nav>
		</div>
		<footer class="demo-fuss">
			<hr class="kern-divider kern-divider--decorative">
			<p class="kern-body kern-body--small kern-body--muted">{t["fuss"]}</p>
		</footer>
	</div>
	<script>
		( function () {{
			var b = document.getElementById( 'farbschema' ), h = document.documentElement;
			function zeige() {{ b.setAttribute( 'aria-checked', h.getAttribute( 'data-kern-theme' ) === 'dark' ? 'true' : 'false' ); }}
			b.addEventListener( 'click', function () {{
				var t = h.getAttribute( 'data-kern-theme' ) === 'dark' ? 'light' : 'dark';
				h.setAttribute( 'data-kern-theme', t );
				try {{ localStorage.setItem( 'ps-theme', t ); }} catch ( e ) {{}}
				zeige();
			}} );
			zeige();
			/* Inhaltsverzeichnis: den Abschnitt markieren, der gerade oben im Fenster steht */
			var tocLinks = Array.prototype.slice.call( document.querySelectorAll( '.doku-toc a' ) ), abschnitte = tocLinks.map( function ( a ) {{ return document.getElementById( a.getAttribute( 'href' ).slice( 1 ) ); }} );
			var ziel = null;
			function markiere() {{
				var aktiv = 0, ende = window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 2;
				/* Nach einem Klick bleibt das Ziel markiert, bis es oben angekommen ist oder die Seite zu Ende ist */
				if ( ziel !== null ) {{ if ( ende || ( abschnitte[ ziel ] && abschnitte[ ziel ].getBoundingClientRect().top <= 120 ) ) {{ ziel = null; }} else {{ return; }} }}
				abschnitte.forEach( function ( el, i ) {{ if ( el && el.getBoundingClientRect().top <= 120 ) {{ aktiv = i; }} }} );
				/* Am Seitenende gilt der letzte Abschnitt, auch wenn er nicht mehr bis oben scrollen kann */
				if ( ende ) {{ aktiv = tocLinks.length - 1; }}
				setzeAktiv( aktiv );
			}}
			function setzeAktiv( aktiv ) {{ tocLinks.forEach( function ( a, i ) {{ if ( i === aktiv ) {{ a.setAttribute( 'aria-current', 'true' ); }} else {{ a.removeAttribute( 'aria-current' ); }} }} ); }}
			/* Klick im Verzeichnis markiert sofort den gewählten Abschnitt */
			tocLinks.forEach( function ( a, i ) {{ a.addEventListener( 'click', function () {{ ziel = i; setzeAktiv( i ); }} ); }} );
			window.addEventListener( 'scroll', markiere, {{ passive: true }} );
			markiere();
			/* Codeblöcke in die Zwischenablage kopieren */
			Array.prototype.slice.call( document.querySelectorAll( '.doku-kopieren' ) ).forEach( function ( k ) {{
				k.addEventListener( 'click', function () {{
					var code = k.parentNode.querySelector( 'pre' ).textContent, label = k.querySelector( '.kern-label' );
					navigator.clipboard.writeText( code ).then( function () {{ label.textContent = k.getAttribute( 'data-kopiert' ); setTimeout( function () {{ label.textContent = ''; }}, 1500 ); }} );
				}} );
			}} );
			/* Alle Seitenlinks tragen Farbschema und Sprache in der Adresse mit, damit der Wechsel auch ohne Browserspeicher stimmt */
			var sy = new URLSearchParams( location.search ).get( 'symbole' );
			function zustand( pfad, lang ) {{ return pfad + '?theme=' + h.getAttribute( 'data-kern-theme' ) + '&lang=' + lang + ( sy ? '&symbole=' + sy : '' ); }}
			Array.prototype.slice.call( document.querySelectorAll( '.doku-lang a' ) ).forEach( function ( x ) {{ x.addEventListener( 'click', function () {{ var l = x.getAttribute( 'data-lang' ); try {{ localStorage.setItem( 'ps-lang', l ); }} catch ( e ) {{}} x.href = zustand( x.getAttribute( 'href' ).split( '?' )[ 0 ], l ); }} ); }} );
			var demoLink = document.querySelector( '.demo-navi a[href$="index.html"]' );
			demoLink.addEventListener( 'click', function () {{ demoLink.href = zustand( '../index.html', h.lang ); }} );
			/* Tabellen, die breiter sind als ihr Rahmen: Rahmen mit der Tastatur erreichbar machen und benennen, sonst nicht */
			function tabellen() {{
				document.querySelectorAll( '.kern-table-responsive' ).forEach( function ( r ) {{
					if ( r.scrollWidth > r.clientWidth ) {{
						r.setAttribute( 'tabindex', '0' ); r.setAttribute( 'role', 'group' ); r.setAttribute( 'aria-label', r.getAttribute( 'data-name' ) );
					}} else {{
						r.removeAttribute( 'tabindex' ); r.removeAttribute( 'role' ); r.removeAttribute( 'aria-label' );
					}}
				}} );
			}}
			tabellen(); window.addEventListener( 'resize', tabellen );
		}} )();
	</script>
</body>
</html>
"""


# Skripte und Stile der Seite liegen als Dateien neben ihr, damit sie unter einer strengen Content-Security-Policy
# (script-src 'self'; style-src 'self') läuft. Beide Sprachfassungen nutzen dieselben Dateien.
AUSLAGERN = (
    (r"\t<script>\n(.*?)\t</script>\n", "doku-frueh.js", '\t<script src="doku-frueh.js"></script>\n'),
    (r"\t<style>\n(.*?)\t</style>\n", "doku.css", '\t<link rel="stylesheet" href="doku.css">\n'),
    (r"\t<script>\n(.*?)\t</script>\n", "doku.js", '\t<script src="doku.js"></script>\n'),
)


def auslagern(html: str) -> str:
    for muster, datei, verweis in AUSLAGERN:
        m = re.search(muster, html, re.S)
        if not m:
            sys.exit(f"{datei}: Block nicht gefunden")
        inhalt = "".join(z[2:] if z.startswith("\t\t") else z for z in m.group(1).splitlines(keepends=True))
        (WURZEL / "doku" / datei).write_text(inhalt, encoding="utf-8")  # beide Sprachfassungen kommen aus derselben Vorlage
        html = html[:m.start()] + verweis + html[m.end():]
    return html


def main() -> None:
    for quelle, ziel, sprache, t in SEITEN:
        titel = t["readme"]
        md = (WURZEL / quelle).read_text(encoding="utf-8")
        # Das Kopfbild der README ist für die Ansicht im Repositorium gedacht; die HTML-Seite beginnt mit der Überschrift
        md = re.sub(r"\A!\[[^\]]*\]\(doku/katalog-bild\.png\)\n+", "", md)
        html = markdown.markdown(md, extensions=["tables", "fenced_code", "toc"], extension_configs={"toc": {"slugify": slugify_unicode}})
        for muster, ersatz in KLASSEN:
            html = re.sub(muster, ersatz, html)
        # Verweise auf die Markdown-Dateien zeigen auf die HTML-Fassungen; Dateipfade im Repo bleiben
        # Kopierknopf unter dem Block, nur Symbol (Lucide „copy“, ISC); nach dem Klick kurz die Rückmeldung als Text
        knopf = (f'<button type="button" class="kern-btn kern-btn--tertiary kern-btn--x-small doku-kopieren" aria-label="{t["kopieren_aria"]}" data-kopiert="{t["kopiert"]}">'
                 '<svg class="ps-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect width="14" height="14" x="8" y="8" rx="2" ry="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/></svg>'
                 '<span class="kern-label" aria-live="polite"></span></button>')
        html = html.replace("<pre>", '<div class="doku-code"><pre>').replace("</pre>", "</pre>" + knopf + "</div>")
        # Tabellen lassen sich auf schmalen Bildschirmen seitlich verschieben; das Skript der Seite macht den Rahmen dann mit der Tastatur erreichbar und benennt ihn
        html = html.replace('<div class="kern-table-responsive">', '<div class="kern-table-responsive" data-name="%s">' % ("Table, scrolls sideways" if sprache == "en" else "Tabelle, seitlich verschiebbar"))
        # Erste Einleitung nach der Hauptüberschrift in der großen Textstufe, wie die Lede der Demo
        html = re.sub(r'(<h1 class="kern-heading-x-large">.*?</h1>\n<p class=")kern-body(">)', r'\1kern-body kern-body--large\2', html, count=1, flags=re.S)
        html = html.replace('src="doku/', 'src="').replace('<img alt="" src="don-ludwig.jpg"', '<img class="doku-foto" alt="Don Ludwig" src="don-ludwig.jpg" width="320" height="320"')
        # Absender-Block: Bild rund, Text daneben, Links darunter als horizontale KERN-Liste
        def autor(m):
            img, p1, p2, links = m.group(1), m.group(2), m.group(3), m.group(4)
            li = "".join(f"<li>{a}</li>" for a in re.findall(r"<a [^>]*>.*?</a>", links))
            return f'<div class="doku-autor">{img}<div class="kern-stack-sm">{p1}{p2}<ul class="kern-list kern-list--horizontal doku-autor-links">{li}</ul></div></div>'
        html = re.sub(r'<p class="kern-body">(<img class="doku-foto"[^>]*/>)</p>\n(<p class="kern-body">.*?</p>)\n(<p class="kern-body">.*?</p>)\n(<p class="kern-body">.*?</p>)', autor, html, count=1, flags=re.S)
        html = html.replace('href="README.md"', 'href="readme.html"').replace('href="README.en.md"', 'href="readme.en.html"')
        # Relative Verweise der README gelten vom Paketordner aus; die Seite liegt eine Ebene tiefer in doku/
        html = re.sub(r'href="(?![a-z][a-z0-9+.-]*:|#|/|\.\./|readme\.)([^"]+)"', r'href="../\1"', html)
        html = html.replace('href="https://', 'rel="noopener" href="https://')
        navi = f'<a class="kern-link" href="../index.html">{t["demo"]}</a><a class="kern-link" href="{ziel}" aria-current="page">{t["readme"]}</a>'
        toc = "".join(f'<li><a class="kern-link" href="#{i}">{re.sub("<[^>]+>", "", txt)}</a></li>' for i, txt in re.findall(r'<h2 class="kern-heading-large" id="([^"]+)">(.*?)</h2>', html))
        (WURZEL / "doku" / ziel).write_text(auslagern(seite(titel, html, navi, sprache, t, toc)), encoding="utf-8")
        print(f"{ziel}: {len(html)} Zeichen aus {quelle}")


if __name__ == "__main__":
    main()
