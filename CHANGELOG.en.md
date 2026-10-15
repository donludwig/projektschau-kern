# Changelog

All notable changes are listed here, newest version first. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), version numbers follow [semantic versioning](https://semver.org/). Each version carries a name.

## 0.1.0 "Musterstadt"

First release, named after the fictitious town of the sample data. As of 2026-10-15.

### Added

- **Cards:** every project as a card with area, title, status, description, lists, key figure and links, in the colour of its area; optionally with a large symbol above the card head ([section 3.2](README.en.md#32-where-each-field-is-shown)).
- **Timeline:** the same projects ordered by year, with period and note ([section 2.2](README.en.md#22-timeline)).
- **Filters:** by area and category, with hit counts and a notice when nothing matches. Filters, view and language are kept in the address, so a link leads to exactly this selection ([section 3.5](README.en.md#35-filters-view-and-address-bar)).
- **Two languages** with a switch ([section 3.3](README.en.md#33-languages)).
- **Light and dark:** both colour schemes of the KERN kit; the colours of an area are derived from one base colour ([section 2.6](README.en.md#26-deriving-colours-programmatically)).
- **Print view:** title, introduction and the filtered view, without controls.
- **No framework, no build:** one JavaScript file and one CSS file on top of KERN kit 2.8.2, which is included unchanged; no external requests ([section 1](README.en.md#1-demo-and-integration)).
- **Data package:** one JSON file with areas, categories, projects and texts ([section 2](README.en.md#2-data)); 32 fictitious sample projects in four areas are included.
- **Accessibility:** keyboard operation with visible focus, results are announced, checked contrasts, the system setting “reduce motion” is respected. Self-test with axe-core for WCAG 2.1 AA and 2.2 AA with no open violations ([section 6](README.en.md#6-accessibility)).
- **Security:** the renderer checks every field of the data package and runs under a strict content security policy. Check scripts, test report, threat model, security policy (`SECURITY.md`) and bill of materials (SPDX 2.3) are included ([section 7](README.en.md#7-security)).
- **Demo and documentation:** demo page, this README in German and English, both also as HTML pages in KERN style; design and content rules for your own cards ([section 4.5](README.en.md#45-design-rules)).
- **Start page:** the start page of projektschau.thinkrepeat.com in German and English under `website/`, as an example of how to present the pattern ([section 1](README.en.md#1-demo-and-integration)).

Deutsche Fassung: [CHANGELOG.md](CHANGELOG.md).
