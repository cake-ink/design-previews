"""Micah, 2026-10-12: drop the reference images; a description on the wishlist
entry is enough.

So an entry is a short want and, optionally, a line saying what she means by
it. That is the better shape anyway: "Cover-ups" is a category, and the thing a
client actually needs to know is which cover-ups and how big.

The optional half is the design problem, same as everywhere else on this page.
Three states, all of which will happen:
  PLAIN  no descriptions — the approved panel, untouched
  ALL    every entry says more
  MIXED  some do, some do not

The rule that keeps mixed honest: a description is a second line under its
want, never a column beside it. An entry with nothing to add is simply a
shorter entry, which is what the hairline between entries already makes legible.
"""
import io, os

OUT = os.path.dirname(os.path.abspath(__file__))
TOKENS = io.open(f"{OUT}/_tokens.css", encoding="utf-8").read()
FONTS = io.open(f"{OUT}/_fonts.css", encoding="utf-8").read()

PLAIN = [("Cover-ups", None), ("Large-scale back pieces", None),
         ("Botanical blackwork", None), ("Lettering", None)]
ALL = [
    ("Cover-ups", "Especially older work that has gone soft. Bring the piece, not a plan."),
    ("Large-scale back pieces", "Booked as three or four sessions, drawn on your back first."),
    ("Botanical blackwork", "Native plants, nothing symmetrical."),
    ("Lettering", "Hand-drawn, not a font. Short pieces read best."),
]
MIXED = [
    ("Cover-ups", "Especially older work that has gone soft. Bring the piece, not a plan."),
    ("Large-scale back pieces", None),
    ("Botanical blackwork", "Native plants, nothing symmetrical."),
    ("Lettering", None),
]

CSS = """
*{box-sizing:border-box}
html,body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--font-body)}
.wrap{max-width:var(--page-content);margin:0 auto;padding:var(--space-md)}
.want{border:2px solid var(--ink);border-radius:var(--radius-lg);padding:var(--space-md)}
.want h2{margin:0 0 var(--space-xs);font-family:var(--font-display);font-size:15px;letter-spacing:var(--tracking-section-label);text-transform:uppercase;color:var(--muted)}
.want ul{list-style:none;margin:0;padding:0}
.want li+li{border-top:1px solid var(--line-soft);margin-top:var(--space-xs);padding-top:var(--space-xs)}
.want b{display:block;font-family:var(--font-header);font-weight:400;font-size:clamp(21px,6vw,26px);line-height:1.12;text-transform:uppercase}
/* A description is a second line under its want, never a column beside it:
   an entry with nothing to add is just a shorter entry. */
.want p{margin:var(--space-2xs) 0 0;font-size:15px;line-height:1.45;color:var(--muted);max-width:var(--measure-copy)}
"""


def panel(wants):
    items = "".join(
        f"<li><b>{w}</b>" + (f"<p>{d}</p>" if d else "") + "</li>" for w, d in wants)
    return f'<section class="want"><h2>Wants to tattoo more of</h2><ul>{items}</ul></section>'


def page(wants):
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>wishlist</title>
<style>{FONTS}{TOKENS}{CSS}</style></head><body><main class="wrap">{panel(wants)}</main></body></html>"""


FILES = {"wt-plain.html": page(PLAIN), "wt-all.html": page(ALL), "wt-mixed.html": page(MIXED)}

FIGS = [("wt-plain.html", "No descriptions", "the approved panel, untouched", 400),
        ("wt-all.html", "Every entry says more", "the want, then what she means by it", 620),
        ("wt-mixed.html", "Some do, some don't", "a bare want is a shorter entry, not a gap", 540)]

FILES["gallery-wt.html"] = f"""<!doctype html><html><head><meta charset="utf-8">
<title>Wishlist descriptions</title><style>
body{{margin:0;padding:26px;background:#EDE7DA;font-family:system-ui,sans-serif}}
h1{{margin:0 0 5px;font-size:19px;color:#002325}}
.note{{margin:0 0 20px;font-size:13.5px;color:#5C6B6C;max-width:1240px;line-height:1.55}}
.note b{{color:#002325}}
.row{{display:flex;gap:20px;align-items:flex-start;flex-wrap:wrap}}
figure{{margin:0}}
figcaption{{display:flex;flex-direction:column;gap:2px;margin:0 0 8px;font-size:13px;color:#002325}}
figcaption span{{font-size:11.5px;color:#5C6B6C}}
iframe{{border:1px solid #CFC6B4;border-radius:10px;background:#F7F2EA;display:block}}
</style></head><body>
<h1>Wishlist with descriptions instead of images, at 390</h1>
<p class="note">A want is a category; the description is the part a client can act on —
<b>which</b> cover-ups, and how big. The description is optional per entry, so a bare want has to
read as a shorter entry rather than a gap: it is a second line underneath, never a column beside,
and the hairline between entries does the separating either way.</p>
<div class="row">{"".join(
f'<figure><figcaption><b>{h}</b><span>{s}</span></figcaption>'
f'<iframe src="{f}" width="390" height="{ht}" scrolling="no" loading="eager"></iframe></figure>'
for f, h, s, ht in FIGS)}</div></body></html>"""

for name, text in FILES.items():
    io.open(f"{OUT}/{name}", "w", encoding="utf-8").write(text)
print(f"wrote {len(FILES)} files")
