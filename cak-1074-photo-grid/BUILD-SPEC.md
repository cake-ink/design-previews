# About page: build spec

Approved direction: the ledger (`AB-c.png`) carrying the wishlist panel
(`AB-a.png`), extended per `AF-website.png`. Micah approved the render with the
wishlist panel above the ledger, so that placement stands.

## Correction to an earlier claim

I told Micah no price field existed anywhere. **That was wrong.**
`min_price_cents` is on the artist record (`schemas/src/index.ts:693`), is
editable in the studio (`you-page.tsx:73`), and already renders publicly on the
profile as `From $150` behind a `show_books_from` opt-in
(`landing.ts:106,304`), formatted by `moneyText` (`schemas/src/money.ts:14`).

So the shop minimum is built. What is missing from Rates is the **hourly rate**
and the **deposit amount** — and the About page must read the same
`min_price_cents` rather than introduce a second minimum that can disagree with
the profile.

`reply_time_minutes` is likewise already public ("Replies in ~4 hrs").

## Fields

Existing, reused as-is:

| Field | Where it lives |
| --- | --- |
| `about`, `about_since`, `works_at`, `guest_spots`, `styles`, socials | `artistPagePatchSchema` |
| `min_price_cents`, `show_books_from`, `books_open`, `reply_time_minutes` | artist record |
| `studio_name`, `studio_address` | `schemas/src/studio-address.ts` |

New patch keys, appended to `ARTIST_PAGE_PATCH_KEYS`:

| Key | Shape | Cap | Notes |
| --- | --- | --- | --- |
| `wishlist` | `string[]` | 6 items × 24 chars | mirrors `styles` exactly, including `PROFILE_STYLE_MAX_LENGTH` |
| `hourly_cents` | `number \| null` | — | same treatment as `min_price_cents`; rendered with `moneyText` |
| `deposit_cents` | `number \| null` | — | the amount; the existing `deposit` **policy** stays as the prose beside it |
| `wont_tattoo` | `string \| null` | 300 | `paragraphText`, like a policy |
| `languages` | `string[]` | 6 items × 24 chars | same shape as `wishlist` |
| `licence` | `string \| null` | 140 | `ONE_LINE` |
| `booking_horizon` | `string \| null` | 40 | `ONE_LINE`, free text ("booking into March") — a date would go stale silently |
| `show_studio_address` | `boolean` | — | **see below** |
| `access_note` | `string \| null` | 140 | `ONE_LINE`, parking and step-free entry |
| `about_photo` | `string \| null` | — | one key, replacing `about_photos` |

### The address needs an opt-in

`studio_address` is stored for reminder emails, where only a booked client sees
it. Publishing it is a different act: plenty of artists work from a private or
home studio and must not have the street address appear because a field
happened to be filled in years ago. So `show_studio_address` defaults **false**
and the studio control says what it does, exactly as `show_books_from` already
does for the minimum. Without it the row renders the studio name alone.

### Replacing the strip

`about_photos` (up to six, labelled "In the studio", not clickable) becomes
`about_photo` — one photo, the artist at work. Migration: keep `about_photos`
readable, take `[0]` as `about_photo` on first save, and leave the rest in R2
rather than deleting someone's uploads on a schema change. `ABOUT_PHOTOS_MAX_COUNT`
and the `.photos` grid rules then come out of `about.ts`.

## Work, split into shippable PRs

1. **The ledger** — rewrite `about.ts` around the row model, no new fields.
   Reuses `about`, `about_since`, `works_at`, `guest_spots`, `min_price_cents`.
   Ships a complete redesign on its own and is the one with the real test
   surface: a row renders only when its field is set, and a page with a name
   alone still renders.
2. **The wishlist** — `wishlist` key, the panel, the studio control. Smallest
   new-field PR; a good first one to prove the pattern.
3. **Rates** — `hourly_cents`, `deposit_cents`, the rates block. Must read
   `min_price_cents` for the minimum.
4. **Getting there** — `show_studio_address`, `access_note`, and the first
   public rendering of the stored address.
5. **Aftercare** — a public route and the page; the copy already exists in the
   automation templates.
6. **The rest** — `wont_tattoo`, `languages`, `licence`, `booking_horizon`.
   One PR; they are all the same shape.
7. **The photo** — `about_photo`, the migration, and deleting the strip.

## Tests each PR owes

- One case per row proving it renders when set and is absent when not.
- The bare page: a name and nothing else still renders, with no empty headings
  and no stray rules.
- `moneyText` output asserted against literal strings, not recomputed from
  cents (Greptile R18).
- The address: asserted **absent** with `show_studio_address` false even when
  `studio_address` is set. This is the security-shaped case of the set.

## Copy

New strings, all labels except two:

| String | Where |
| --- | --- |
| `Books`, `Rates`, `Getting there`, `Won't tattoo`, `Languages`, `At work`, `Aftercare`, `Licence` | ledger labels |
| `Wants to tattoo more of` | the wishlist panel |
| `Shop minimum`, `Hourly`, `Deposit` | rate labels |
| `comes off the total` | beside the deposit |
| `How to look after a fresh tattoo` | the aftercare link |
| `The same notes she sends after a session, here whenever you need them.` | under it — needs rewriting in second person for the real page |

`about.ts` is not in `CLIENT_APPOINTMENT_FILES`, so this page says **session**,
never *appointment*. `sitting` is banned outright.

## Not building, and why

Contact email or phone: the booking request is the channel, and publishing an
address invites booking around the product. Flash is the strongest remaining
idea but is a section with a claim flow, not a row. Reviews, map embeds, hours,
newsletter and merch: see the README.
