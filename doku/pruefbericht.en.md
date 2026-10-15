# Test report Projektschau for KERN

As of version 0.1.0 "Musterstadt", 15 October 2026. Where a check ran against an earlier state, the row gives its date. All checks were carried out by the author, with automated tools and AI-assisted reviews. There has been no check by independent third parties. The threat model is in [bedrohungsmodell.md](bedrohungsmodell.md) (German), the way to report vulnerabilities in [SECURITY.md](../SECURITY.md). Deutsche Fassung: [pruefbericht.md](pruefbericht.md).

## Structure

The pattern runs entirely in the browser: a renderer (`projektschau.js`), a stylesheet (`projektschau.css`) and a data package as JSON, plus the unmodified KERN kit under `vendor/kern/`. It has no server part and no login, sets no cookies and loads nothing from third-party servers. The only outside input is the data package. The renderer treats it as untrusted even when the operator provides it: it may come from a content system with several roles. The demo (`index.html`), the documentation (`doku/`) and the start page (`website/`) are static pages on the same kit. The checks focus on the path from the data package to the page.

## Checks

| Check | Method | Result |
|---|---|---|
| Data flow in the renderer | AI-assisted review for DOM XSS and for misuse (Trail of Bits "Sharp Edges" method): data package, address, hash, browser storage and embedded JSON up to the markup. As of 12 October 2026; the start page and the documentation scripts are not part of this review | Colours only as hex values; keys and language codes only in the expected format, otherwise the entry stays out; icons are parsed with `DOMParser` and reduced to the SVG shapes `path`, `circle`, `rect`, `line`, `polyline`, `polygon`, `ellipse`; numbers only as numbers; links only with `http`, `https`, `mailto`, `tel` or relative; no CSS selector built from data; `?lang=` is checked before it is stored; a failed fetch empties the element and logs the error to the console |
| Insecure defaults | AI-assisted review following the Trail of Bits "Insecure Defaults" method, from credentials to errors that fail open instead of closed. As of 12 October 2026 | no finding |
| Security review of the whole code | Claude Code `/security-review`, data flow from source to output. As of 12 October 2026 | no finding of severity medium or above |
| Attack strings in the renderer | `skripte/pruefe_xss.js` renders the sample data with payloads in area colour, key, language code, icon, number, link and year and searches for active markup | 10 of 10 checks passed |
| Fuzzing | `skripte/pruefe_fuzz.js 1000 42`: 1000 randomly mangled packages with a fixed seed (fields removed, wrong types, nested) | no exception, no active markup, no empty result |
| Unicode control characters | bidi and zero-width characters in texts and link texts (part of `pruefe_xss.js`) | removed |
| Data package, classes, tokens | `skripte/pruefe.py`: every `kern-` class and every `--kern-` token against the kit, formats in the data package, contrast of the area colours in light and dark | no finding; KERN kit 2.8.2 with 2678 classes and 522 tokens |
| Content security policy | Demo, documentation and start page under `default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; object-src 'none'; base-uri 'none'; form-action 'self'; frame-ancestors 'none'`, locally and on projektschau.thinkrepeat.com, there also on the own error pages 403 and 404 | no violations; the renderer sets its rules through `adoptedStyleSheets`, no page contains inline scripts or inline styles |
| Accessibility | axe-core 4.14 for WCAG 2.1 AA and 2.2 AA with best practices: demo, documentation and start page, light and dark, both languages, 1280, 390 and 320 pixels, with "reduce motion" (48 runs) | no violations. Without "reduce motion", contrast in the decorative motif of the start page drops for fractions of a second while cards fade in and filter buttons change colour; the motif is hidden from assistive technology, cards that are not selected turn grey instead of transparent |
| Keyboard, contrast, text adjustment | Demo: keyboard pass with a check of the focus ring, contrast of every text recalculated, also on hover; text spacing per WCAG 1.4.12, 200 % font size, reduced motion. As of 13 October 2026 | no finding |
| Browsers | Chromium, Firefox and WebKit (Playwright 1.64): demo with filters, timeline, language, dark mode, state in the address and after reload | no finding, no console errors |
| Load | 1000 cards in Chromium (`skripte/erzeuge_last.py`). As of 12 October 2026 | 205 ms to render, 5 ms per filter click |
| Markup | html-validate 11.16 on demo, documentation, start page and the rendered DOM of the demo | no finding |
| JavaScript and CSS | ESLint 10.12 and stylelint 17.16 on renderer, demo, documentation and start page | no finding |
| Lighthouse 13.5 | projektschau.thinkrepeat.com, mobile profile with simulated throttling | Demo: performance 86 to 90 depending on the run, documentation 81, start page 87; accessibility, best practices and SEO 100 on all three pages |
| Scanner against the live site | OWASP ZAP 2.17 (Docker image `zap-stable`), baseline scan against projektschau.thinkrepeat.com: spider and passive rules, no active scan | no failures, 63 rules passed. Warnings: `Permissions-Policy` and the cross-origin headers are not set; notes on caching |
| Links | all internal links of the pages on projektschau.thinkrepeat.com and all outside addresses | 251 internal links without error; of 43 outside addresses, two answer with a block for automated clients (uxdesign.cc with 403, LinkedIn with 999), one was unreachable (503) |
| Supply chain | KERN kit in a fixed version, SHA-512 checksum of the npm package before unpacking (`skripte/kern-sync.sh`); SHA-256 checksum for the release zip | kit, Fira Sans, Lucide and KERN logo listed with origin and licence in the bill of materials, licence texts in the package |
| Bill of materials | `SPDX_projektschau-kern.spdx.json` (SPDX 2.3), regenerated on every build; validated against the SPDX 2.3 JSON schema on 13 October 2026 | valid |
| Known vulnerabilities | query in the OSV database for `@kern-ux/native` 2.8.2 and `lucide` 1.49.0 | no matches |
| Secrets | gitleaks 8.30 over all commits | nothing found |

## Open items

- **Independent check:** no penetration test, no audit by third parties.
- **Screen reader and user test:** axe-core covers only part of the criteria. A screen reader pass and a test with people who maintain content are open.
- **KERN kit:** The author checked that the files match the registry package and that every class used exists in it, but not the kit itself.
- **Trusted Types:** not tested. The renderer sets the checked markup in one place through `innerHTML`; a page that enforces Trusted Types needs its own policy for it.
- **Automated pipeline:** The author runs the checks locally by hand. The OSV query is a snapshot; for Fira Sans the bill of materials gives no version that could be queried.
- **Signature:** The zip comes with a SHA-256 checksum, not with a signature.
- **Embedding page:** Server, headers and content security policy belong to the operator. Whoever calls `Projektschau.render` directly and processes the result leaves the checked path.

## Repeating the checks

From the package folder:

```
python3 skripte/pruefe.py
node skripte/pruefe_xss.js
node skripte/pruefe_fuzz.js 1000 42
python3 -m http.server 8771 --bind 127.0.0.1
```

With Playwright and axe-core from a separate `node_modules` folder, for example for one page of the running server:

```
NODE_PATH=/PATH/TO/node_modules node -e "
const { chromium } = require('playwright'); const { AxeBuilder } = require('@axe-core/playwright');
(async () => { const b = await chromium.launch(); const p = await (await b.newContext()).newPage();
  await p.goto('http://127.0.0.1:8771/index.html');
  const r = await new AxeBuilder({ page: p }).withTags(['wcag2a', 'wcag2aa', 'wcag21aa', 'wcag22aa', 'best-practice']).analyze();
  console.log(r.violations.length + ' violations'); await b.close(); })();"
```

`NODE_PATH` points to a `node_modules` folder containing `playwright` and `@axe-core/playwright`. For the content security policy, serve the pages from a server that sets the header above and check the console for content security policy messages.
