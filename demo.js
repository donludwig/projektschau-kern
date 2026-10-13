/* Demo-Seite: Adressparameter an die Projektschau durchreichen, Hell/Dunkel-Schalter, Dokumentations-Link. Läuft mit defer vor
 * projektschau.js (Reihenfolge im Kopf), damit data-sprache und data-symbole vor dem Rendern gesetzt sind. Kein Teil des Patterns. */
/* Sprache (?lang=) und Symbole (?symbole=) aus der Adresse an die Projektschau durchreichen; läuft vor projektschau.js (defer) */
( function () { var q = new URLSearchParams( location.search ), el = document.querySelector( '[data-projektschau]' ), l = q.get( 'lang' ), sy = q.get( 'symbole' ); if ( l && /^[a-z]{2,3}$/i.test( l ) ) { el.setAttribute( 'data-sprache', l ); try { localStorage.setItem( 'ps-lang', l ); } catch ( e ) {} } if ( sy === 'ja' || sy === 'nein' ) { el.setAttribute( 'data-symbole', sy ); try { localStorage.setItem( 'ps-symbole', sy ); } catch ( e ) {} } } )();

( function () {
	var b = document.getElementById( 'farbschema' ), h = document.documentElement;
	function zeige() { b.setAttribute( 'aria-checked', h.getAttribute( 'data-kern-theme' ) === 'dark' ? 'true' : 'false' ); }
	b.addEventListener( 'click', function () {
		var t = h.getAttribute( 'data-kern-theme' ) === 'dark' ? 'light' : 'dark';
		h.setAttribute( 'data-kern-theme', t );
		try { localStorage.setItem( 'ps-theme', t ); } catch ( e ) {}
		zeige();
	} );
	zeige();
	/* Dokumentations-Link folgt der Sprache der Projektschau (gespeicherte Wahl, beim Klick die aktuelle) */
	var rl = document.getElementById( 'readme-link' );
	function readmeZiel() { var ps = document.querySelector( '.ps' ), l = ps ? ps.getAttribute( 'data-lang' ) : null; if ( ! l ) { try { l = localStorage.getItem( 'ps-lang' ); } catch ( e ) {} } var sy = ps ? ( ps.getAttribute( 'data-symbole' ) === 'ja' ? 'ja' : 'nein' ) : null; if ( ! sy ) { try { sy = localStorage.getItem( 'ps-symbole' ) || 'nein'; } catch ( e ) { sy = 'nein'; } } if ( rl ) { rl.href = ( l === 'en' ? 'doku/readme.en.html' : 'doku/readme.html' ) + '?theme=' + h.getAttribute( 'data-kern-theme' ) + '&symbole=' + sy; } }
	readmeZiel();
	if ( rl ) { rl.addEventListener( 'click', readmeZiel ); }
	b.addEventListener( 'click', readmeZiel );
	document.addEventListener( 'click', function ( e ) { if ( e.target.closest && e.target.closest( '.ps-lang button, .ps-symbolschalter' ) ) { setTimeout( readmeZiel, 0 ); } } );
} )();
