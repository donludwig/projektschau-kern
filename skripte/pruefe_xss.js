#!/usr/bin/env node
/* Prüft den Renderer ohne Browser gegen Nutzlasten: Bereichsfarbe, Schlüssel und Sprachcode
 * dürfen nicht aus dem Stylesheet oder einem Attribut ausbrechen, Icons bleiben auf Formen beschränkt, Links nur mit
 * erlaubtem Schema, die Nummer wird maskiert. Aufruf aus dem Ordner kern/: node skripte/pruefe_xss.js
 * Ohne DOMParser (Node) fallen Icons ganz weg; die Form-Allowlist prüft der Browser-Lauf der Demo. */
const fs = require( 'fs' ), path = require( 'path' ), vm = require( 'vm' );
const wurzel = path.resolve( __dirname, '..' );
const daten = JSON.parse( fs.readFileSync( path.join( wurzel, 'daten/beispiel.json' ), 'utf8' ) );
const ctx = { window: {}, document: { baseURI: 'https://example.org/projekte/', querySelectorAll: () => [] }, URL, console };
ctx.window = ctx;
vm.runInNewContext( fs.readFileSync( path.join( wurzel, 'projektschau.js' ), 'utf8' ), ctx );
const render = ctx.Projektschau.render;
let fehler = 0;
function pruefe( name, html, verboten ) {
	const treffer = verboten.filter( ( v ) => html.includes( v ) );
	console.log( ( treffer.length ? 'FEHLER ' : 'ok     ' ) + name + ( treffer.length ? ' enthält ' + JSON.stringify( treffer ) : '' ) );
	if ( treffer.length ) { fehler++; }
}
const d = () => JSON.parse( JSON.stringify( daten ) );
let x = d(); x.bereiche[ 0 ].farben.hell.area = 'red}</style><img src=x onerror=alert(1)>';
pruefe( 'Bereichsfarbe bricht nicht aus dem Stylesheet aus', render( x, {} ), [ 'onerror', '<img' ] );
x = d(); x.bereiche[ 0 ].schluessel = 'a}</style><b>x'; x.projekte.forEach( ( p ) => { if ( p.bereich === daten.bereiche[ 0 ].schluessel ) { p.bereich = x.bereiche[ 0 ].schluessel; } } );
pruefe( 'Ungültiger Schlüssel bleibt draußen', render( x, {} ), [ '</style><b>', '--ps-area-a}' ] );
x = d(); x.sprachen = [ 'de', 'en onmouseover=alert(5) x' ];
pruefe( 'Ungültiger Sprachcode bleibt draußen', render( x, {} ), [ 'onmouseover', 'data-aria-en ' ] );
x = d(); x.projekte[ 0 ].icon_svg = '</svg><img src=x onerror=alert(3)>'; x.bereiche[ 0 ].icon_svg = '<path d="M1 1" onload="alert(1)"/><script>alert(1)</script><use href="#x"/>';
pruefe( 'Icon ohne Skript, Ereignis und use', render( x, {} ), [ 'onerror', '<img', 'onload', '<script', '<use' ] );
x = d(); x.projekte[ 0 ].titel = { de: 'moc.\u202eelgoog\u202c', en: 'a\u200bb' }; x.projekte[ 0 ].beschreibung = { de: 'um\u202egedreht <strong>f</strong>', en: 'x' };
pruefe( 'Bidi- und Zero-Width-Zeichen entfernt', render( x, {} ), [ '\u202e', '\u202c', '\u200b' ] );
x = d(); x.projekte[ 0 ].nr = '<img src=x onerror=alert(1)>';
pruefe( 'Nummer maskiert', render( x, {} ), [ '<img' ] );
x = d(); x.projekte[ 0 ].links = [ { url: 'javascript:alert(4)', text: { de: 'j', en: 'j' } }, { url: 'data:text/html,x', text: { de: 'd', en: 'd' } }, { url: ' JaVaScRiPt:alert(1)', text: { de: 'j2', en: 'j2' } }, { url: 'https://example.org/ok', text: { de: 'ok', en: 'ok' } }, { url: '/relativ', text: { de: 'r', en: 'r' } } ];
const h = render( x, {} );
pruefe( 'Links ohne javascript: und data:', h, [ 'javascript:', 'data:text' ] );
if ( ! h.includes( 'href="https://example.org/ok"' ) || ! h.includes( 'href="/relativ"' ) ) { console.log( 'FEHLER erlaubte Links fehlen' ); fehler++; } else { console.log( 'ok     erlaubte Links bleiben' ); }
x = d(); x.projekte[ 0 ].zeitleiste = { jahr: '20"]', sortierung: 202501, zeitraum: { de: 'x', en: 'x' } };
pruefe( 'Jahr maskiert', render( x, {} ), [ 'data-year="20"]' ] );
const n = ( render( daten, {} ).match( /<article/g ) || [] ).length;
if ( n !== daten.projekte.length ) { console.log( `FEHLER Demo rendert ${ n } statt ${ daten.projekte.length } Karten` ); fehler++; } else { console.log( `ok     Demo rendert ${ n } Karten` ); }
console.log( fehler ? `FEHLER: ${ fehler }` : 'ALLE PRÜFUNGEN BESTANDEN' );
process.exit( fehler ? 1 : 0 );
