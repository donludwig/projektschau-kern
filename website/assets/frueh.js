/* Läuft sofort im Kopf: Kommt die Seite mit ?stelle= an (Sprachwechsel), bleibt sie unsichtbar, bis das Skript am Seitenende sie an die
 * Stelle gesetzt hat. So ist kein Sprung vom Seitenanfang zu sehen. Nach anderthalb Sekunden wird sie in jedem Fall gezeigt. */
if ( /[?&]stelle=/.test( location.search ) ) {
	document.documentElement.classList.add( 'stelle-wartet', 'kopf-bleibt' );
	setTimeout( function () { document.documentElement.classList.remove( 'stelle-wartet' ); }, 1500 );
}
