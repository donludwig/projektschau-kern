#!/usr/bin/env bash
# Holt das KERN-Kit (@kern-ux/native) in fester Version aus der npm-Registry und legt nur die benötigten Dateien unter vendor/kern/ ab.
# Kein npm nötig. Version und Prüfsumme sind fest eingetragen; bei einem Update beide Werte aus https://registry.npmjs.org/@kern-ux/native/<version> übernehmen.
set -euo pipefail
VERSION="2.8.2"
INTEGRITY="sha512-2AT25YD95iByLDUqY/fBou6Vt09tI1/RgpLy0lqUbLmV5aoeuUuz/BZ4zDJbbblyo96T3bywIlbwGbRUw0s+Og=="
ZIEL="$(cd "$(dirname "$0")/.." && pwd)/vendor/kern"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

curl -fsSL "https://registry.npmjs.org/@kern-ux/native/-/native-${VERSION}.tgz" -o "$TMP/kit.tgz"
IST="sha512-$(openssl dgst -sha512 -binary "$TMP/kit.tgz" | base64)"
[ "$IST" = "$INTEGRITY" ] || { echo "Prüfsumme stimmt nicht: $IST" >&2; exit 1; }
tar -xzf "$TMP/kit.tgz" -C "$TMP"
Q="$TMP/package"

rm -rf "$ZIEL"
mkdir -p "$ZIEL/fonts/fira-sans"
cp "$Q/dist/kern.min.css" "$Q/dist/kern-grid.min.css" "$ZIEL/"
cp "$Q/LICENSE.md" "$ZIEL/"
echo "$VERSION" > "$ZIEL/VERSION"
# Nur die Schnitte, die das Kit verwendet (400, 400 kursiv, 500, 600, 700).
for f in Regular Italic Medium SemiBold Bold; do cp "$Q/dist/fonts/fira-sans/FiraSans-$f.woff2" "$ZIEL/fonts/fira-sans/"; done
python3 - "$Q/dist/fonts/fira-sans.css" "$ZIEL/fonts/fira-sans.css" <<'PY'
import re, sys
css = open(sys.argv[1]).read()
behalten = {"Regular", "Italic", "Medium", "SemiBold", "Bold"}
bloecke = [b for b in re.findall(r"@font-face\s*\{.*?\}", css, re.S)
           if re.search(r"FiraSans-(\w+)\.woff2", b).group(1) in behalten]
open(sys.argv[2], "w").write("\n\n".join(bloecke) + "\n")
PY
echo "KERN-Kit $VERSION nach $ZIEL kopiert:"
du -sh "$ZIEL"
