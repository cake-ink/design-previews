# Photo grids: the no-holes rule and See all

Design previews behind Micah's 2026-10-11/12 rulings on how tattoo photos lay
out and how the rest of them are reached. Everything here is rendered from the
product's own CSS — `_tokens.css`, `_base.css` (`pages/style.ts`),
`_about.css` (`pages/about.ts`) and `_landing.css` (`pages/landing.ts`) are
extracted verbatim, and the previews add only the rule under discussion. The
tiles are tonal stand-ins, not real work: accurate for rhythm and weight, not
for judging a crop.

## The rulings, in the order they were made

1. **First full width.** Where a count leaves a hole, the first photo leads at
   full width rather than the last.
2. **Every row holds images of one width, and no holes remain anywhere.** This
   governs: where a hero cannot close a row, the short row splits evenly
   instead.
3. **Over six opens "See all {N}".**
4. **See all opens its own section off the profile; back returns.** A route,
   not an in-place expansion and not an overlay.
5. **These are tattoo photos** — so the target is the portfolio on the main
   profile, not the About page's strip.

## The rule

Six columns underneath, because six divides by both two and three. A tile
spans 2 of 6 where the grid is three across, 3 of 6 where it is two across.
Then two moves close every count:

- **one tile over** → it leads, full width (the hero)
- **two tiles over** → that short row splits in half

### On the work grid (`.pf`, three across at every width)

The portfolio is uncapped, so this cannot be written per count. `:has()` reads
the remainder off the last tile's own position, which needs **no markup
change**:

```css
.pf{grid-template-columns:repeat(6,minmax(0,1fr))}
.pf .cell{grid-column:span 2}
.pf:has(.cell:last-child:nth-child(3n+1)) .cell:first-child{grid-column:span 6;aspect-ratio:16/10}
.pf:has(.cell:last-child:nth-child(3n+2)) .cell:nth-last-child(-n+2){grid-column:span 3;aspect-ratio:4/3}
```

`check-work.mjs` measures counts 1–15: every row's widths plus its gaps equal
the grid width, and every row's widths match each other.

```
n= 4  rows=1+3      n= 8  rows=3+3+2    n=12  rows=3+3+3+3
n= 5  rows=3+2      n=10  rows=1+3+3+3  n=14  rows=3+3+3+3+2
1 through 15: every row full, every row even
```

### On the About strip (`.photos`, two across then three at 760px)

Kept here for reference; superseded by ruling 5 unless that strip stays. It
needs breakpoint variants because its column count changes, and the version
rendered uses a `data-n` attribute. The `:has()` form above would work here
too and would avoid the markup change.

`check-rule.mjs` measures all six counts at both widths — 12 cases, all clean.

## The hero's crop

A hero cannot keep the tiles' aspect ratio. At 4:5 full width on a phone it is
390×487 and swallows the screen before the next photo. The previews use 16:10,
which costs a different `object-fit` crop on that one photo.

## What is still open

- **The About page strip.** `Z1-about-strip.png` shows it as it stands:
  public heading "In the studio" (`about.ts:143`), but the only label the
  artist ever sees is a bare "Photos" with a "+ Photo" button
  (`you-about.tsx:193`). Capped at six (`ABOUT_PHOTOS_MAX_COUNT`), and the
  public images are not buttons, so tapping one does nothing. Retitle, fold
  into the portfolio, or leave — undecided.
- **The booking page's revealed work grid** has the same hole the rule fixes,
  since `.pf` is a fixed three columns.

## Frames

| File | What it shows |
| --- | --- |
| `R1-phone.png` | the rule at 390, counts 1–6, every row full and even |
| `R2-wide.png` | the same at 1000, where a hero alone cannot close 2 and 5 |
| `Y1-section-back.png` | See all as its own section with the back idiom (on the About strip) |
| `W1-work-section.png` | the same on the real work grid, 14 pieces, with the viewer |
| `Z1-about-strip.png` | the About strip today, and the field artists upload through |

## Rebuilding

Scripts write their HTML next to themselves, so run them from `src/`.
Playwright resolves from the app checkout and Chromium needs an explicit
`executablePath` (the repo pins a newer Playwright than the image carries).

```sh
cd src
python3 build-work.py && node shoot-work.mjs && node check-work.mjs
```
