# CAK-761 — decisions, 2026-10-12

Micah's answers to the questions open on [#1069](https://github.com/cake-ink/app/pull/1069),
the data PR at the bottom of the five-PR profile stack. Devon raised the first
two as "choices to record in the hub"; the third and fourth came out of them.

## 1. Dark mode — the client's setting wins when the artist hasn't chosen

**Decision:** if she never picked Light or Dark, the page follows the client's
device. If she picked either, her choice holds for everyone.

Devon described the current behaviour as the artist's choice overriding the
client's. The code is stronger than that: the public pages read no colour
preference at all — there is no `prefers-color-scheme` query in
`apps/api/src/pages/` or in `packages/tokens/`. A client with their phone in
dark mode gets a light page today unless the artist chose dark.

**Cost:** small. The dark rendering already exists and is tested — `body.dark`
in `APPEARANCE_CSS` (`pages/artist-shared.ts:17`), asserted in
`settings.test.ts`. What is new is triggering it from the device: an `auto`
class on `<body>` when `page_appearance` is null, plus one media query reusing
the existing dark declarations.

**Where it lands:** #1070 and #1074, where the pages render. **Not #1069**,
which only stores the field — so this does not reopen it.

## 2. Policy topics become free-form headings — but not yet

**Decision:** artists write their own policy headings rather than filling in a
fixed set of six. **Deferred until the stack lands**, as its own PR against main.

The fixed set (`PAGE_POLICY_TOPICS`, `artist-page.ts:28`) is a one-way door:
`pagePolicies()` filters stored rows against it at *read* time, so retiring a
topic later would stop rendering whatever artists had written under it,
silently, with no migration and no warning. Adding is safe; removing is not.

**Why deferred:** it touches 12 files across schemas, the API, the studio and
tests, and #1069 is green and mergeable today at the bottom of a stack that
also carries #1095 and #1109. Reopening it would hold all of that.

**What deferring costs:** a migration. Any artist who sets policies between the
stack landing and this change has text stored against topic ids, which has to
move to headings. Small, on a field barely anyone has filled in yet.

**Worth carrying into that PR:** free-form policies are structurally identical
to FAQs — `page_faqs` is already `{question, answer}[]` and policies would
become `{heading, text}[]`. Two boxes of the same shape, separated only by
which one she typed into. Merging them into one ordered list was offered and
not taken; it is the obvious thing to revisit when the PR is written.

## 3. "Before your session" — moot

It was a client-facing label using the artist's word, which Devon flagged and
left to Micah. Decision 2 dissolves it: with free-form headings there is no
product copy to get wrong, because the artist writes her own.

Had it stayed, the path was a `// client-vocabulary` marker on the line or
adding `artist-page.ts` to `CLIENT_APPOINTMENT_FILES` — `appointment` outside
that allowlist fails `vocabulary-check.mjs`.

## 4. #1069 merges as it is

Both of Devon's blockers were already fixed on the branch after he wrote:
the migration is renamed `0083` → `0090_artist-page-fields.sql` with the
`schema.ts:43` comment updated, and main is merged in at `94cebc7`. The PR is
green, `mergeable_state: clean`, not a draft, and all three Greptile threads
are resolved.

## Still with Devon, not Micah

From his 2026-10-12 review, all nonblocking:

- the PATCH route's post-write cover re-check (`index.ts:8161`) is untested —
  removing it leaves the suite green
- the upload route reads and writes the portfolio with no lock between
  (`index.ts:8263-8264`); predates the PR
- `invalid_page_policies` surfaces zod's default message in the studio; only a
  malformed client reaches it
- `normalizeSocialHandle` and `instagramUrl` want a row in
  `docs/architecture/patterns.md`
- the shape of the cover across #1070 and #1072 — his own open question
