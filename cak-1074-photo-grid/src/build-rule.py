"""Micah's two constraints, taken as absolute:
  1. every image in a row is the same width as the others in that row
  2. no holes, at any count, at any width

The grid is rebuilt on six columns so a row can be divided by two or by three.
A photo spans 3 on a phone (two per row) and 2 above 760px (three per row).
Where the count leaves exactly one photo over, that one leads at full width —
Micah's hero. Where it leaves two over, the short row splits evenly instead.
Between them those two moves close every count at both widths.

Rendered from the branch's own about.ts CSS with only the new rules added on.
"""
import io, os

OUT = os.path.dirname(os.path.abspath(__file__))
TOKENS = io.open(f"{OUT}/_tokens.css", encoding="utf-8").read()
BASE = io.open(f"{OUT}/_base.css", encoding="utf-8").read()
ABOUT = io.open(f"{OUT}/_about.css", encoding="utf-8").read()

LOOKS = [
    "radial-gradient(120% 90% at 22% 18%,#E8DFCD 0%,#BCAE95 38%,#6E6552 78%,#3C382E 100%)",
    "linear-gradient(168deg,#2B2F2C 0%,#434A44 46%,#8E9389 100%)",
    "radial-gradient(100% 80% at 78% 76%,#D9CFB8 0%,#9E9177 42%,#55503F 100%)",
    "linear-gradient(14deg,#3A2E26 0%,#7A5F49 52%,#C8A880 100%)",
    "radial-gradient(130% 100% at 50% 8%,#DCE2E0 0%,#9AA6A4 40%,#4E5A59 100%)",
    "linear-gradient(200deg,#1F2622 0%,#3D463D 40%,#9C9B82 100%)",
]
GRAIN = ("repeating-linear-gradient(118deg,rgba(255,255,255,.055) 0 2px,"
         "rgba(0,0,0,.045) 2px 4px)")

# THE PATCH. Written against `.ph` here because the harness draws spans; in
# about.ts every selector below reads `.photos img` instead, unchanged otherwise.
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
}"""

PHOTO_CSS = """.ph{display:block;width:100%;aspect-ratio:4/5;border-radius:var(--radius-lg);
  position:relative;overflow:hidden}
.ph::after{content:attr(data-n);position:absolute;right:8px;bottom:6px;
  font:700 10px/1 var(--font-body,system-ui);color:rgba(255,255,255,.92);
  letter-spacing:.1em;text-shadow:0 1px 4px rgba(0,0,0,.55)}"""


def photo(i):
    return (f'<span class="ph" data-n="{i + 1}" '
            f'style="background-image:{GRAIN},{LOOKS[i % len(LOOKS)]}"></span>')


def page(n, wide, patched):
    cells = "".join(photo(i) for i in range(n))
    section = (f'<section aria-labelledby="pt"><h2 class="sh" id="pt">'
               f'{n} photo{"s" if n > 1 else ""}</h2>'
               f'<div class="photos" data-n="{n}">{cells}</div></section>')
    if wide:
        body = ('<main class="wrap"><a class="back">&larr; <b>Mara Stone</b></a>'
                '<span class="portrait"><span class="ph" data-n="portrait" '
                f'style="aspect-ratio:5/6;background-image:{GRAIN},{LOOKS[4]}"></span></span>'
                f'<div class="text">{section}</div></main>')
    else:
        body = f'<main class="wrap"><div class="text">{section}</div></main>'
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>{n}</title>
<style>{TOKENS}{BASE}{ABOUT}
{PHOTO_CSS}
html,body{{margin:0;background:var(--bg)}}
.wrap{{padding:14px 16px 18px}}
{RULE if patched else ""}</style></head><body>{body}</body></html>"""


FILES = {}
for n in range(1, 7):
    FILES[f"r-p{n}.html"] = page(n, False, True)
    FILES[f"r-w{n}.html"] = page(n, True, True)
    FILES[f"r-p{n}-before.html"] = page(n, False, False)
    FILES[f"r-w{n}-before.html"] = page(n, True, False)

GAL = """<!doctype html><html><head><meta charset="utf-8"><title>{title}</title>
<style>
body{{margin:0;padding:26px 26px 30px;background:#EDE7DA;font-family:system-ui,sans-serif}}
h1{{margin:0 0 5px;font-size:19px;color:#002325}}
.note{{margin:0 0 20px;font-size:13.5px;color:#5C6B6C;max-width:1200px;line-height:1.55}}
.note b{{color:#002325}}
.row{{display:flex;gap:20px;align-items:flex-start;flex-wrap:wrap}}
figure{{margin:0}}
figcaption{{display:flex;flex-direction:column;gap:2px;margin:0 0 8px;font-size:13px;color:#002325}}
figcaption span{{font-size:11.5px;color:#4B6B58;font-weight:600}}
iframe{{border:1px solid #CFC6B4;border-radius:10px;background:#F7F2EA;display:block}}
</style></head><body><h1>{title}</h1><p class="note">{note}</p><div class="row">{figs}</div></body></html>"""

SHAPE_P = {1: "one full width", 2: "two halves", 3: "hero, then two halves",
           4: "two halves, two halves", 5: "hero, then two halves, two halves",
           6: "three rows of two"}
SHAPE_W = {1: "one full width", 2: "two halves", 3: "three thirds",
           4: "hero, then three thirds", 5: "three thirds, then two halves",
           6: "two rows of three"}


def figs(prefix, w, shapes):
    return "".join(
        f'<figure><figcaption><b>{n} photo{"s" if n > 1 else ""}</b>'
        f'<span>{shapes[n]}</span></figcaption>'
        f'<iframe src="{prefix}{n}.html" width="{w}" height="600" '
        f'scrolling="no" loading="eager"></iframe></figure>' for n in range(1, 7))


FILES["gallery-rp.html"] = GAL.format(
    title="Every count on a phone (390) — two per row, no holes",
    note=("Six columns underneath, so a row divides by two or by three. Where one photo is "
          "left over it leads at full width; otherwise rows are even pairs. <b>Every row holds "
          "images of one width, and no count leaves a hole.</b>"),
    figs=figs("r-p", 390, SHAPE_P))

FILES["gallery-rw.html"] = GAL.format(
    title="Every count at 1000 — three per row, no holes",
    note=("The same six columns, three per row above 760px. One left over leads at full width "
          "(1 and 4); two left over split the short row in half instead (2 and 5), which is the "
          "case a hero alone could not close. <b>No holes at any count.</b>"),
    figs=figs("r-w", 1000, SHAPE_W))

for name, text in FILES.items():
    io.open(f"{OUT}/{name}", "w", encoding="utf-8").write(text)
print(f"wrote {len(FILES)} files")
