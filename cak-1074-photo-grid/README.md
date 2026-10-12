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

## The About page redesign

A later brief, and a bigger one: the About page is where an artist says more
about herself — how long she has tattooed, what she wants to tattoo more of,
her background, and maybe one big photo of her working. **None of it is
required; the page still has to look finished with any of it missing.**

That constraint is the design problem, so each direction is rendered from one
template fed three content states rather than drawn three times by hand. A
direction that only works full is caught by its own sparse and bare frames.

- **FULL** — everything set.
- **SPARSE** — a name, a city, a year, one paragraph. No photo, no wishlist,
  no guest spots, no socials.
- **BARE** — a name. Nothing else at all.

| | Direction | Holds up when empty because |
| --- | --- | --- |
| `AB-a.png` | **The plate** — photo first, name huge beneath, wishlist as a bordered panel in the header face | with no photo the name grows into the space the photo had, so the page opens on a statement either way |
| `AB-b.png` | **The letter** — her words are the page; the portrait is small, the working photo drops into the prose | the prose is the structure, so losing the furniture around it costs least |
| `AB-c.png` | **The ledger** — every entry a labelled row on a hairline rule | a missing entry is not a gap, it is a row that never existed |

At BARE all three converge on the same thing — a name and the booking button —
which is the honest answer rather than a failure of the renders.

The wishlist is the one genuinely new field. It wants the same shape as
`styles`: a short list of free-text items, each a couple of words.

Two bugs the frames caught, both fixed here and worth not repeating in the
real page:

- `content:" \00b7 "` loses its trailing space — CSS consumes the whitespace
  that terminates a hex escape, so the separator rendered as `OR ·Tattooing`.
  The literal character has no such rule.
- The letter's wishlist was written in third person (*"Right now she most
  wants to tattoo…"*) while every other word on the page is the artist's own
  voice. Now first person.

The display faces are embedded in the pages' shared CSS; `_fonts.css` is just
the three `@font-face` blocks lifted out of `_base.css`, because these
directions write their layout rules fresh and should not inherit the existing
page's.

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

## About as a website replacement

`AF-website.png` — direction C carrying A's wishlist panel, extended with what
an artist's own site has that Cake has no home for. The page grows by a row
rather than by a redesign, which is the reason the ledger was the right pick;
the second frame is the same page from someone who filled in almost none of it.

Already on the profile and deliberately not duplicated: **policies and FAQs**
(`landing.ts:321-324`), the **work grid**, and **books open/closed**.

| New entry | Why a site has it | State in Cake today |
| --- | --- | --- |
| **Rates** | the first question every client asks | no price field exists anywhere; only a free-text deposit policy |
| **Getting there** | address, parking, step-free access | `studio_name`/`studio_address` are stored and go out in reminder emails, but **no public page has ever rendered them** |
| **Books / booking into** | how far out they are | `books_open` is a binary flag |
| **Won't tattoo** | scope, saving both sides a wasted request | nothing |
| **Languages** | a real filter for many clients | nothing |
| **Aftercare** | a client needs it three weeks later, not once | sent after a session (CAK-586); nowhere to look up |
| **Licence** | the trust credential a shop site always carries | nothing |

Considered and left out, with reasons:

- **Contact email or phone.** A website has a contact page; Cake deliberately
  should not. The booking request *is* the channel, and publishing an address
  invites booking around the product. This is a product decision, not an
  omission.
- **Flash / available designs.** Genuinely replaces a shop's flash page and is
  the strongest remaining idea, but it is a section with its own claim flow,
  not a ledger row.
- **Reviews.** High trust value, but it is a solicitation and moderation
  system rather than a field.
- **Map embed.** These pages carry no third-party scripts. A link to maps does
  the job.
- **Opening hours.** An artist's hours are the booking calendar.
- **Newsletter, merch, gift cards.** Separate products.

Open question in the render: the wishlist panel currently sits above the
ledger, so it is the first thing after the name. That is a deliberate editorial
bet — she leads with what she wants to make — but a client may want where, when
and how much first.

## Wishlist references

`WL-wishlist.png` — Micah, 2026-10-12: a wishlist entry can carry a reference
image if she wants one. "If she wants" is the design problem: a real wishlist
will be part pictures and part words, and the words must not read as pictures
that failed to load.

So an entry is a tile either way. With a reference it is the reference; without
one the phrase is set large on paper behind the same inner rule the work tiles
carry, which reads as flash rather than as a gap — and it carries no caption,
because the tile is already the words. The no-holes rule applies unchanged, so
an odd count leads full width.

Worth settling before this is built: a reference is very often **someone
else's tattoo**. On a public page that is an attribution question, not just a
storage one. The studio copy should say plainly that these are references
rather than her work, and the public caption may need to say it too.
