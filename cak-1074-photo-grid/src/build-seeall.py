"""Micah: over six photos opens a "See all {N}".

That pattern already ships one page over. landing.ts:319 renders the work grid
as six pieces plus `<details class="more-work">` whose summary reads
`See all {N}` closed and `Show less` open, revealing the rest in place. No JS,
no second route. These frames put the same thing on the About page's photos,
with the six-column rule from the last round governing both grids: the visible
six, and the remainder the details opens.

Six shown is always two clean rows of three (or three of two), so the hero
never appears up top in the overflow case. The remainder has its own count, so
it gets its own treatment: 7 photos reveals one full width, 9 reveals a hero
and a pair.
"""
import io, os

OUT = os.path.dirname(os.path.abspath(__file__))
TOKENS = io.open(f"{OUT}/_tokens.css", encoding="utf-8").read()
BASE = io.open(f"{OUT}/_base.css", encoding="utf-8").read()
ABOUT = io.open(f"{OUT}/_about.css", encoding="utf-8").read()

SHOWN = 6

LOOKS = [
    "radial-gradient(120% 90% at 22% 18%,#E8DFCD 0%,#BCAE95 38%,#6E6552 78%,#3C382E 100%)",
    "linear-gradient(168deg,#2B2F2C 0%,#434A44 46%,#8E9389 100%)",
    "radial-gradient(100% 80% at 78% 76%,#D9CFB8 0%,#9E9177 42%,#55503F 100%)",
    "linear-gradient(14deg,#3A2E26 0%,#7A5F49 52%,#C8A880 100%)",
    "radial-gradient(130% 100% at 50% 8%,#DCE2E0 0%,#9AA6A4 40%,#4E5A59 100%)",
    "linear-gradient(200deg,#1F2622 0%,#3D463D 40%,#9C9B82 100%)",
    "radial-gradient(110% 95% at 30% 70%,#C9BCA2 0%,#8A7C62 45%,#423B2C 100%)",
    "linear-gradient(150deg,#50463A 0%,#938166 55%,#D7C3A4 100%)",
    "radial-gradient(120% 85% at 70% 25%,#E2E6E2 0%,#A3ADA8 42%,#5A6360 100%)",
    "linear-gradient(190deg,#24302B 0%,#49584E 48%,#8FA096 100%)",
    "radial-gradient(100% 90% at 20% 80%,#DED2BA 0%,#A4947A 44%,#4B4436 100%)",
    "linear-gradient(26deg,#2E2823 0%,#6E5C48 50%,#B9A184 100%)",
]
GRAIN = ("repeating-linear-gradient(118deg,rgba(255,255,255,.055) 0 2px,"
         "rgba(0,0,0,.045) 2px 4px)")

# The grid rule from the last round, plus the See all pill lifted from
# landing.ts so the two pages read as one product rather than two.
RULE = """
.photos{grid-template-columns:repeat(6,minmax(0,1fr))}
.photos .ph{grid-column:span 3}
.photos[data-n="1"] .ph,
.photos[data-n="3"] .ph:first-child,
.photos[data-n="5"] .ph:first-child{grid-column:span 6;aspect-ratio:16/10}
@media (min-width:760px){
  .photos .ph{grid-column:span 2}
  .photos[data-n="2"] .ph{grid-column:span 3}
  .photos[data-n="3"] .ph:first-child,
  .photos[data-n="5"] .ph:first-child{grid-column:span 2;aspect-ratio:4/5}
  .photos[data-n="4"] .ph:first-child{grid-column:span 6;aspect-ratio:16/10}
  .photos[data-n="5"] .ph:nth-child(4),
  .photos[data-n="5"] .ph:nth-child(5){grid-column:span 3}
}
.more-photos summary{display:flex;align-items:center;justify-content:center;min-height:54px;margin-top:var(--space-sm);border-radius:var(--radius-pill);border:1.5px solid var(--line);font-family:var(--font-display);font-size:20px;letter-spacing:var(--tracking-display-action);text-transform:uppercase;color:var(--ink);cursor:pointer;list-style:none}
.more-photos summary::-webkit-details-marker{display:none}
.more-photos summary:hover{background:var(--card)}
.more-photos[open] summary{order:2}
.more-photos .open-label,.more-photos[open] .closed-label{display:none}
.more-photos[open] .open-label{display:inline}
.more-photos[open]{display:flex;flex-direction:column}
.more-photos .photos{margin-top:var(--space-2xs)}"""

PHOTO_CSS = """.ph{display:block;width:100%;aspect-ratio:4/5;border-radius:var(--radius-lg);
  position:relative;overflow:hidden}
.ph::after{content:attr(data-n);position:absolute;right:8px;bottom:6px;
  font:700 10px/1 var(--font-body,system-ui);color:rgba(255,255,255,.92);
  letter-spacing:.1em;text-shadow:0 1px 4px rgba(0,0,0,.55)}"""


def photo(i):
    return (f'<span class="ph" data-n="{i + 1}" '
            f'style="background-image:{GRAIN},{LOOKS[i % len(LOOKS)]}"></span>')


def section(n, open_):
    """Six in the grid; the rest behind See all, each grid counted separately."""
    first = min(n, SHOWN)
    head = (f'<h2 class="sh" id="pt">In the studio</h2>'
            f'<div class="photos" data-n="{first}">'
            f'{"".join(photo(i) for i in range(first))}</div>')
    if n <= SHOWN:
        return f'<section aria-labelledby="pt">{head}</section>'
    rest = n - SHOWN
    return (f'<section aria-labelledby="pt">{head}'
            f'<details class="more-photos"{" open" if open_ else ""}>'
            f'<summary><span class="closed-label">See all {n}</span>'
            f'<span class="open-label">Show less</span></summary>'
            f'<div class="photos" data-n="{rest}">'
            f'{"".join(photo(i) for i in range(SHOWN, n))}</div>'
            f'</details></section>')


def page(n, wide, open_):
    s = section(n, open_)
    if wide:
        body = ('<main class="wrap"><a class="back">&larr; <b>Mara Stone</b></a>'
                '<span class="portrait"><span class="ph" data-n="portrait" '
                f'style="aspect-ratio:5/6;background-image:{GRAIN},{LOOKS[4]}"></span></span>'
                f'<div class="text">{s}</div></main>')
    else:
        body = f'<main class="wrap"><div class="text">{s}</div></main>'
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>{n}</title>
<style>{TOKENS}{BASE}{ABOUT}
{PHOTO_CSS}
html,body{{margin:0;background:var(--bg)}}
.wrap{{padding:14px 16px 18px}}
{RULE}</style></head><body>{body}</body></html>"""


FILES = {}
COUNTS = [7, 9, 12]
for n in COUNTS:
    FILES[f"s-p{n}-shut.html"] = page(n, False, False)
    FILES[f"s-p{n}-open.html"] = page(n, False, True)
    FILES[f"s-w{n}-shut.html"] = page(n, True, False)
    FILES[f"s-w{n}-open.html"] = page(n, True, True)

GAL = """<!doctype html><html><head><meta charset="utf-8"><title>{title}</title>
<style>
body{{margin:0;padding:26px 26px 30px;background:#EDE7DA;font-family:system-ui,sans-serif}}
h1{{margin:0 0 5px;font-size:19px;color:#002325}}
.note{{margin:0 0 20px;font-size:13.5px;color:#5C6B6C;max-width:1200px;line-height:1.55}}
.note b{{color:#002325}}
.note code{{background:#E3DCCB;padding:1px 5px;border-radius:4px;font-size:12.5px}}
.row{{display:flex;gap:20px;align-items:flex-start;flex-wrap:wrap}}
figure{{margin:0}}
figcaption{{display:flex;flex-direction:column;gap:2px;margin:0 0 8px;font-size:13px;color:#002325}}
figcaption span{{font-size:11.5px;color:#4B6B58;font-weight:600}}
iframe{{border:1px solid #CFC6B4;border-radius:10px;background:#F7F2EA;display:block}}
</style></head><body><h1>{title}</h1><p class="note">{note}</p><div class="row">{figs}</div></body></html>"""

REST = {7: "one left over → full width", 9: "three left over → hero, then a pair",
        12: "six left over → two clean rows"}


def figs(tag, w):
    out = []
    for n in COUNTS:
        out.append(f'<figure><figcaption><b>{n} photos · shut</b>'
                   f'<span>six, then the pill</span></figcaption>'
                   f'<iframe src="s-{tag}{n}-shut.html" width="{w}" height="600" '
                   f'scrolling="no" loading="eager"></iframe></figure>')
        out.append(f'<figure><figcaption><b>{n} photos · open</b>'
                   f'<span>{REST[n]}</span></figcaption>'
                   f'<iframe src="s-{tag}{n}-open.html" width="{w}" height="600" '
                   f'scrolling="no" loading="eager"></iframe></figure>')
    return "".join(out)


FILES["gallery-sp.html"] = GAL.format(
    title="Over six, on a phone (390) — See all, then Show less",
    note=("Six show, and <code>See all {N}</code> opens the rest in place — the same "
          "<code>&lt;details&gt;</code> the work grid on the booking page already uses, down to "
          "the copy. <b>Six is a clean two or three rows either way, so the hero never appears "
          "up top here.</b> The revealed set is counted on its own, so it gets the same "
          "no-holes treatment."),
    figs=figs("p", 390))

FILES["gallery-sw.html"] = GAL.format(
    title="Over six, at 1000 — the same pill, three per row",
    note=("Identical markup; only the column count changes at 760px. Note 9 photos: the "
          "revealed three make one full row here, where on a phone the same three need the hero. "
          "<b>One rule, both widths.</b>"),
    figs=figs("w", 1000))

for name, text in FILES.items():
    io.open(f"{OUT}/{name}", "w", encoding="utf-8").write(text)
print(f"wrote {len(FILES)} files")
