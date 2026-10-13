#!/usr/bin/env node
/* Fuzzing des Renderers: tausend zufällig verstümmelte Pakete aus daten/beispiel.json (Felder entfernt, falscher Typ,
 * null, Riesenwerte, Steuer- und Bidi-Zeichen, Nutzlasten) durch render(); er darf nie werfen und nie aktives Markup ausgeben.
 * Aufruf aus dem Ordner kern/: node skripte/pruefe_fuzz.js [anzahl] [seed] */
const fs = require( 'fs' ), path = require( 'path' ), vm = require( 'vm' );
const wurzel = path.resolve( __dirname, '..' );
const basis = JSON.parse( fs.readFileSync( path.join( wurzel, 'daten/beispiel.json' ), 'utf8' ) );
const ctx = { window: {}, document: { baseURI: 'https://example.org/p/', querySelectorAll: () => [] }, URL, console: { error() {} } };
ctx.window = ctx; vm.runInNewContext( fs.readFileSync( path.join( wurzel, 'projektschau.js' ), 'utf8' ), ctx );
const render = ctx.Projektschau.render;
const N = parseInt( process.argv[ 2 ] || '1000', 10 ); let seed = parseInt( process.argv[ 3 ] || '42', 10 );
const rnd = () => { seed = ( seed * 1103515245 + 12345 ) & 0x7fffffff; return seed / 0x7fffffff; };
const wahl = ( a ) => a[ Math.floor( rnd() * a.length ) ];
const WERTE = [ null, undefined, 0, -1, 1e21, NaN, '', ' ', 'x'.repeat( 5000 ), [], {}, [ 1, 2 ], { a: 1 }, true, false, '<img src=x onerror=alert(1)>', '"><svg onload=alert(1)>', 'javascript:alert(1)', '</style><script>alert(1)</script>', '‮evil‬', '​​', 'a\u0000b', '%00', '\\u003cscript\\u003e', '{"__proto__":{"x":1}}', '😀'.repeat( 50 ), 'kern-col-12', '../../etc/passwd' ];
const MARKER = /<[a-z][^>]*\son[a-z]+=|<script\b|srcdoc=/i; // nur echtes Markup: Attributwerte werden vorher geleert, maskierter Text (&lt;svg onload) zählt nicht
const HREF = /href="(javascript|data|vbscript):/i; // </style> steht einmal legitim (render() liefert den Stilblock), deshalb unten gezählt
function mutiere( obj, tiefe ) {
	if ( tiefe > 6 || obj === null || typeof obj !== 'object' ) { return rnd() < 0.3 ? wahl( WERTE ) : obj; }
	if ( Array.isArray( obj ) ) {
		const a = obj.map( ( v ) => mutiere( v, tiefe + 1 ) );
		if ( rnd() < 0.1 ) { a.push( wahl( WERTE ) ); }
		if ( rnd() < 0.1 ) { a.splice( Math.floor( rnd() * a.length ), 1 ); }
		return a;
	}
	const o = {};
	for ( const k of Object.keys( obj ) ) { if ( rnd() < 0.05 ) { continue; } o[ k ] = mutiere( obj[ k ], tiefe + 1 ); }
	if ( rnd() < 0.1 ) { o[ wahl( [ 'fremd', '__proto__', 'constructor', '' ] ) ] = wahl( WERTE ); }
	return o;
}
let wuerfe = 0, treffer = 0, leer = 0; const gruppen = {};
for ( let i = 0; i < N; i++ ) {
	const d = mutiere( JSON.parse( JSON.stringify( basis ) ), 0 );
	let html;
	try { html = render( d, { ansicht: rnd() < 0.5 ? 'karten' : 'zeitleiste', sprache: wahl( [ 'de', 'en', 'xx', '', null ] ), bereich: wahl( [ 'umwelt', 'all', '<x>', null ] ) } ); } catch ( e ) { wuerfe++; const ort = ( e.stack || '' ).split( '\n' ).find( ( l ) => /projektschau\.js|evalmachine/.test( l ) ) || ''; const k = String( e ).slice( 0, 70 ) + ' @' + ort.replace( /.*:(\d+):\d+.*/, '$1' ); gruppen[ k ] = ( gruppen[ k ] || 0 ) + 1; continue; }
	if ( typeof html !== 'string' ) { leer++; continue; }
	const ohneWerte = html.replace( /="[^"]*"/g, '=""' );
	const m = ohneWerte.match( MARKER ) || html.match( HREF ) || ( html.split( '</style>' ).length > 2 ? [ '</style> doppelt' ] : null ); if ( m ) { treffer++; if ( treffer <= 5 ) { console.log( `TREFFER ${ i }: ${ m[ 0 ] } bei ${ html.indexOf( m[ 0 ] ) }` ); } }
}
Object.entries( gruppen ).sort( ( a, b ) => b[ 1 ] - a[ 1 ] ).slice( 0, 12 ).forEach( ( [ k, n ] ) => console.log( `${ String( n ).padStart( 4 ) } × ${ k }` ) );
console.log( `${ N } Pakete: ${ wuerfe } Ausnahmen, ${ treffer } Markup-Treffer, ${ leer } ohne Ausgabe` );
console.log( wuerfe || treffer ? `FEHLER: ${ wuerfe + treffer }` : 'ALLE PRÜFUNGEN BESTANDEN' );
process.exit( wuerfe || treffer ? 1 : 0 );
