# Kinshasa Visitor Guide

Bilingual (English / French) static page listing hotels, restaurants, parks and gardens, zoo and wildlife, leisure parks, culture, day trips from Kinshasa, Lubumbashi and the national parks of DR Congo. Every entry links to the source it was read in. A "Before you travel" panel states the health and security advice in force on the check date.

Last full check: **24 October 2026**.

## Files

| File | Role |
|---|---|
| `index.html` | The generated page. Self-contained: open it in a browser or put it on any web host (GitHub Pages works as is). |
| `build/places.py` | All place entries, English and French. Add or change entries here. |
| `build/ui.py` | Interface text, the travel-advice panel, the "recently changed" list, the links section and the footer. |
| `build/build.py` | The generator. `python build/build.py` rewrites `index.html`. `--artifact <path>` also writes the fragment used for the claude.ai Artifact. |

Do not edit `index.html` by hand: the next build overwrites it.

## Rules for editing

- Write only what a linked source says. Date anything approximate ("2023 guide", "latest review seen: Aug 2026").
- An entry that rests on one non-official source gets the `single` badge; unclear hours or prices get `call`; a place near an area named in government advice gets `advice`; a latest review older than a year gets `dated`.
- Every entry needs an English text and a French text. The French text is a first draft, not yet reviewed by a native speaker.
- Before republishing, re-read the UK FCDO, France Diplomatie and WHO pages and update the panel in `ui.py`. The Ebola, security and entry statements in it are dated 24 October 2026 and go stale quickly.
- TripAdvisor ratings, hours and addresses were read on 24 October 2026. Restaurants and leisure venues in Kinshasa open and close often.

## Checks that were run on 24 October 2026

- Tag balance, unique ids, working in-page anchors, equal count of English and French text spans.
- Status of every external link (the sites that block scripts, such as TripAdvisor, Hilton, Marriott and UNESCO's conservation pages, were verified from search results or in the browser instead).
- Search, district filter and language switch tested in headless Chrome; layout checked at 1280 px and 390 px, in light and dark themes, in English and French.
