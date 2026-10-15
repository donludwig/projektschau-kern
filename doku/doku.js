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
	/* Inhaltsverzeichnis: den Abschnitt markieren, der gerade oben im Fenster steht */
	var tocLinks = Array.prototype.slice.call( document.querySelectorAll( '.doku-toc a' ) ), abschnitte = tocLinks.map( function ( a ) { return document.getElementById( a.getAttribute( 'href' ).slice( 1 ) ); } );
	var ziel = null;
	function markiere() {
		var aktiv = 0, ende = window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 2;
		/* Nach einem Klick bleibt das Ziel markiert, bis es oben angekommen ist oder die Seite zu Ende ist */
		if ( ziel !== null ) { if ( ende || ( abschnitte[ ziel ] && abschnitte[ ziel ].getBoundingClientRect().top <= 120 ) ) { ziel = null; } else { return; } }
		abschnitte.forEach( function ( el, i ) { if ( el && el.getBoundingClientRect().top <= 120 ) { aktiv = i; } } );
		/* Am Seitenende gilt der letzte Abschnitt, auch wenn er nicht mehr bis oben scrollen kann */
		if ( ende ) { aktiv = tocLinks.length - 1; }
		setzeAktiv( aktiv );
	}
	function setzeAktiv( aktiv ) { tocLinks.forEach( function ( a, i ) { if ( i === aktiv ) { a.setAttribute( 'aria-current', 'true' ); } else { a.removeAttribute( 'aria-current' ); } } ); }
	/* Klick im Verzeichnis markiert sofort den gewählten Abschnitt */
	tocLinks.forEach( function ( a, i ) { a.addEventListener( 'click', function () { ziel = i; setzeAktiv( i ); } ); } );
	window.addEventListener( 'scroll', markiere, { passive: true } );
	markiere();
	/* Codeblöcke in die Zwischenablage kopieren */
	Array.prototype.slice.call( document.querySelectorAll( '.doku-kopieren' ) ).forEach( function ( k ) {
		k.addEventListener( 'click', function () {
			var code = k.parentNode.querySelector( 'pre' ).textContent, label = k.querySelector( '.kern-label' );
			navigator.clipboard.writeText( code ).then( function () { label.textContent = k.getAttribute( 'data-kopiert' ); setTimeout( function () { label.textContent = ''; }, 1500 ); } );
		} );
	} );
	/* Alle Seitenlinks tragen Farbschema und Sprache in der Adresse mit, damit der Wechsel auch ohne Browserspeicher stimmt */
	var sy = new URLSearchParams( location.search ).get( 'symbole' );
	function zustand( pfad, lang ) { return pfad + '?theme=' + h.getAttribute( 'data-kern-theme' ) + '&lang=' + lang + ( sy ? '&symbole=' + sy : '' ); }
	Array.prototype.slice.call( document.querySelectorAll( '.doku-lang a' ) ).forEach( function ( x ) { x.addEventListener( 'click', function () { var l = x.getAttribute( 'data-lang' ); try { localStorage.setItem( 'ps-lang', l ); } catch ( e ) {} x.href = zustand( x.getAttribute( 'href' ).split( '?' )[ 0 ], l ); } ); } );
	var demoLink = document.querySelector( '.demo-navi a[href$="index.html"]' );
	demoLink.addEventListener( 'click', function () { demoLink.href = zustand( '../index.html', h.lang ); } );
	/* Tabellen, die breiter sind als ihr Rahmen: Rahmen mit der Tastatur erreichbar machen und benennen, sonst nicht */
	function tabellen() {
		document.querySelectorAll( '.kern-table-responsive' ).forEach( function ( r ) {
			if ( r.scrollWidth > r.clientWidth ) {
				r.setAttribute( 'tabindex', '0' ); r.setAttribute( 'role', 'group' ); r.setAttribute( 'aria-label', r.getAttribute( 'data-name' ) );
			} else {
				r.removeAttribute( 'tabindex' ); r.removeAttribute( 'role' ); r.removeAttribute( 'aria-label' );
			}
		} );
	}
	tabellen(); window.addEventListener( 'resize', tabellen );
} )();
