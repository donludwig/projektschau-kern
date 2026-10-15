/* Eigene Seiten: Hell/Dunkel-Schalter wie in der Demo (gleicher Speicherschlüssel). */
( function () {
	var b = document.getElementById( 'farbschema' ), h = document.documentElement;
	function thema() { return h.getAttribute( 'data-kern-theme' ) === 'dark' ? 'dark' : 'light'; }
	function zeige() { b.setAttribute( 'aria-checked', thema() === 'dark' ? 'true' : 'false' ); }
	b.addEventListener( 'click', function () {
		var t = thema() === 'dark' ? 'light' : 'dark';
		h.setAttribute( 'data-kern-theme', t );
		try { localStorage.setItem( 'ps-theme', t ); } catch ( e ) { /* privater Modus */ }
		zeige();
	} );
	zeige();
} )();
/* An der Stelle bleiben: Beim Umschalten von Farbschema oder Sprache in der Seite bleibt die Scrollposition stehen. Beim Sprachwechsel auf
 * eine andere Seite (Startseite, Dokumentation) reist die Stelle als ?stelle= mit: die wievielte Überschrift oben steht und wie weit der
 * Abschnitt schon durchgescrollt ist. Beide Sprachfassungen haben dieselbe Gliederung, die Texte sind verschieden lang. */
( function () {
	function ueberschriften() { return Array.prototype.slice.call( document.querySelectorAll( 'main h1, main h2, main h3' ) ); }
	function lage( el ) { return el.getBoundingClientRect().top + window.scrollY; }
	/* Sofort setzen: Das Kit schaltet weiches Scrollen ein, ein gewöhnliches scrollTo wäre als Fahrt über die Seite zu sehen */
	function setze( y ) { window.scrollTo( { top: y, left: 0, behavior: 'instant' } ); }
	function stelle() {
		var hs = ueberschriften(), y = window.scrollY, i = -1, a, b;
		hs.forEach( function ( h, k ) { if ( lage( h ) <= y + 1 ) { i = k; } } );
		if ( i < 0 ) { return y < 4 ? '' : '0:0:' + Math.round( y ); }
		a = lage( hs[ i ] ); b = i + 1 < hs.length ? lage( hs[ i + 1 ] ) : document.documentElement.scrollHeight;
		return ( i + 1 ) + ':' + Math.min( 1, ( y - a ) / Math.max( 1, b - a ) ).toFixed( 4 ) + ':0';
	}
	function springe( wert ) {
		var t = wert.split( ':' ), i = parseInt( t[ 0 ], 10 ), f = parseFloat( t[ 1 ] ), hs, a, b;
		if ( isNaN( i ) || isNaN( f ) ) { return; }
		if ( i === 0 ) { setze( parseInt( t[ 2 ], 10 ) || 0 ); return; }
		hs = ueberschriften();
		if ( i > hs.length ) { return; }
		a = lage( hs[ i - 1 ] ); b = i < hs.length ? lage( hs[ i ] ) : document.documentElement.scrollHeight;
		setze( Math.round( a + ( f * ( b - a ) ) ) );
	}
	/* Sprachwechsel auf eine andere Seite: Stelle an die Adresse hängen. In der Blasenphase, also nach den eigenen Klick-Handlern der Links */
	document.addEventListener( 'click', function ( e ) {
		var a = e.target.closest ? e.target.closest( '.start-lang a[href], .doku-lang a[href]' ) : null, h, teile, q, s;
		if ( ! a ) { return; }
		h = a.getAttribute( 'href' ); teile = h.split( '#' )[ 0 ].split( '?' ); q = new URLSearchParams( teile[ 1 ] || '' ); s = stelle();
		if ( s ) { q.set( 'stelle', s ); } else { q.delete( 'stelle' ); }
		a.setAttribute( 'href', teile[ 0 ] + ( q.toString() ? '?' + q.toString() : '' ) );
	} );
	/* Umschalten in der Seite (Farbschema überall, Sprache und Symbole in der Demo): Position merken und nach dem Neuzeichnen wiederherstellen */
	document.addEventListener( 'click', function ( e ) {
		var y;
		if ( ! e.target.closest || ! e.target.closest( '#farbschema, .ps-lang button, .ps-symbolschalter' ) ) { return; }
		y = window.scrollY;
		window.requestAnimationFrame( function () { setze( y ); window.requestAnimationFrame( function () { setze( y ); } ); } );
	}, true );
	/* Ankunft mit ?stelle=: hinspringen, sobald die Seite steht, und den Parameter aus der Adresse nehmen */
	( function () {
		var u = new URL( location.href ), wert = u.searchParams.get( 'stelle' );
		if ( ! wert ) { return; }
		if ( 'scrollRestoration' in history ) { history.scrollRestoration = 'manual'; }
		u.searchParams.delete( 'stelle' );
		try { history.replaceState( history.state, '', u.pathname + u.search + u.hash ); } catch ( e ) { /* Dateien von der Festplatte in manchen Browsern */ }
		springe( wert );
		document.documentElement.classList.remove( 'stelle-wartet' );
		if ( document.readyState !== 'complete' ) { window.addEventListener( 'load', function () { springe( wert ); } ); }
	} )();
} )();
/* Farbschema beim Seitenwechsel mitgeben: Jeder Klick auf einen Link innerhalb der Seite trägt ?theme= mit. So bleibt die Wahl auch dann
 * erhalten, wenn der Browser keinen Speicher erlaubt (privater Modus, Dateien von der Festplatte in Safari). */
document.addEventListener( 'click', function ( e ) {
	var a = e.target.closest ? e.target.closest( 'a[href]' ) : null, h, teile, pfad, anker, q;
	if ( ! a ) { return; }
	h = a.getAttribute( 'href' );
	if ( /^(?:[a-z][a-z0-9+.-]*:|\/\/|#)/i.test( h ) || ! /\.html(?:[?#]|$)/.test( h ) ) { return; }
	teile = h.split( '#' ); anker = teile.length > 1 ? '#' + teile.slice( 1 ).join( '#' ) : '';
	pfad = teile[ 0 ].split( '?' ); q = new URLSearchParams( pfad[ 1 ] || '' );
	q.set( 'theme', document.documentElement.getAttribute( 'data-kern-theme' ) === 'dark' ? 'dark' : 'light' );
	a.setAttribute( 'href', pfad[ 0 ] + '?' + q.toString() + anker );
} );
/* Beim Umschalten des Farbschemas die Adresse nachführen: Steht dort noch ?theme= vom Seitenwechsel, gewönne es beim Neuladen gegen die Wahl */
new MutationObserver( function () {
	var u = new URL( location.href );
	if ( ! u.searchParams.has( 'theme' ) ) { return; }
	u.searchParams.set( 'theme', document.documentElement.getAttribute( 'data-kern-theme' ) === 'dark' ? 'dark' : 'light' );
	try { history.replaceState( history.state, '', u.pathname + u.search + u.hash ); } catch ( e ) { /* Dateien von der Festplatte in manchen Browsern */ }
} ).observe( document.documentElement, { attributes: true, attributeFilter: [ 'data-kern-theme' ] } );
/* Kopfzeile: verschwindet beim Runterscrollen, erscheint beim Hochscrollen und sobald sie den Tastaturfokus bekommt. Die Höhe steht
 * als --kopf-hoehe am Wurzelelement, damit haftende Teile darunter (Filterleiste, Inhaltsverzeichnis) und Sprungziele ausweichen. */
( function () {
	var kopf = document.querySelector( '.demo-kopf' ), h = document.documentElement, zuletzt = window.scrollY, wartet = false, sprung = 0, ruhe = 0, wende = window.scrollY;
	if ( ! kopf ) { return; }
	function messe() { h.style.setProperty( '--kopf-hoehe', kopf.offsetHeight + 'px' ); }
	function pruefe() {
		var y = window.scrollY;
		wartet = false;
		h.classList.toggle( 'kopf-oben', y < 4 );
		if ( ruhe > Date.now() ) { zuletzt = y; return; }
		if ( Math.abs( y - zuletzt ) < 6 ) { return; }
		/* Runter: sofort ausblenden. Hoch: erst einblenden, wenn ein Stück am Stück hochgescrollt wurde, sonst springt die Seite bei jeder kleinen Bewegung */
		if ( y > zuletzt ) { wende = y; }
		if ( y <= kopf.offsetHeight ) { h.classList.remove( 'kopf-weg' ); } else if ( y > zuletzt || sprung > Date.now() ) { h.classList.add( 'kopf-weg' ); } else if ( wende - y > 120 ) { h.classList.remove( 'kopf-weg' ); }
		zuletzt = y;
	}
	/* Nach einem Sprung zu einem Abschnitt bleibt die Kopfzeile kurz ausgeblendet, auch wenn der Sprung nach oben führt; sonst läge sie über der Überschrift */
	function merkeSprung() { sprung = Date.now() + 1500; if ( window.scrollY > kopf.offsetHeight ) { h.classList.add( 'kopf-weg' ); } }
	window.addEventListener( 'hashchange', merkeSprung );
	document.addEventListener( 'click', function ( e ) { var a = e.target.closest ? e.target.closest( 'a[href^="#"]' ) : null; if ( a ) { merkeSprung(); } } );
	if ( location.hash ) { merkeSprung(); }
	messe();
	h.classList.toggle( 'kopf-oben', window.scrollY < 4 );
	window.addEventListener( 'resize', messe );
	window.addEventListener( 'scroll', function () { if ( ! wartet ) { wartet = true; window.requestAnimationFrame( pruefe ); } }, { passive: true } );
	kopf.addEventListener( 'focusin', function () { h.classList.remove( 'kopf-weg' ); } );
	/* Filter, Ansicht und Sprache der Projektschau verändern die Höhe der Seite und damit die Scrollposition. Das ist kein Hochscrollen:
	 * Für einen Moment bleibt die Kopfzeile, wie sie ist. */
	document.addEventListener( 'click', function ( e ) { if ( e.target.closest && e.target.closest( '.ps button, .ps summary, .ps a' ) ) { ruhe = Date.now() + 900; } }, true );
	/* Klick in der Kopfzeile (Farbschema, Sprache): Sie bleibt stehen, damit der Wechsel zu sehen ist. Dasselbe gilt nach der Ankunft von
	 * einem Sprachwechsel, bei dem die Seite an ihre Stelle gesetzt wird. */
	kopf.addEventListener( 'click', function () { ruhe = Date.now() + 1200; h.classList.remove( 'kopf-weg' ); }, true );
	if ( h.classList.contains( 'kopf-bleibt' ) ) { ruhe = Date.now() + 1500; h.classList.remove( 'kopf-weg' ); }
} )();
