"""Micah: a wishlist entry can carry a reference image, if she wants one.

"If she wants" is the whole problem. A wishlist will be part pictures and part
words — she has a shot of the cover-up she loved and nothing at all for
"lettering" — so the panel has to hold both without the text entries reading as
holes where a picture failed to load.

So an entry is a tile either way. With an image it is the image; without one
the phrase is set large on paper behind the same inner rule the work tiles
already use, which reads as flash rather than as a gap. Captions sit under
every tile, so a picture is never unexplained.

Three states, because all three will happen on day one:
  WORDS   nothing uploaded — what the approved panel already does
  ALL     every entry has a reference
  MIXED   two do, two do not — the state the design has to earn

The no-holes rule from the work grid applies unchanged: an odd count leads
full width.
"""
import io, os

OUT = os.path.dirname(os.path.abspath(__file__))
TOKENS = io.open(f"{OUT}/_tokens.css", encoding="utf-8").read()
FONTS = io.open(f"{OUT}/_fonts.css", encoding="utf-8").read()

GRAIN = ("repeating-linear-gradient(118deg,rgba(255,255,255,.055) 0 2px,"
         "rgba(0,0,0,.045) 2px 4px)")
REFS = [
    "radial-gradient(120% 90% at 25% 20%,#E2D7C2 0%,#AE9F84 38%,#5E5544 78%,#302C24 100%)",
    "linear-gradient(162deg,#272B28 0%,#444B44 48%,#8B9188 100%)",
    "radial-gradient(105% 85% at 72% 72%,#D6CAB2 0%,#9A8C72 44%,#4F4A3A 100%)",
    "linear-gradient(18deg,#382D25 0%,#79604A 54%,#C6A782 100%)",
]

WANTS_WORDS = [("Cover-ups", None), ("Large-scale back pieces", None),
               ("Botanical blackwork", None), ("Lettering", None)]
WANTS_ALL = [("Cover-ups", 0), ("Large-scale back pieces", 1),
             ("Botanical blackwork", 2), ("Lettering", 3)]
WANTS_MIXED = [("Cover-ups", 0), ("Large-scale back pieces", None),
               ("Botanical blackwork", 2), ("Lettering", None)]
WANTS_ODD = [("Cover-ups", 0), ("Large-scale back pieces", None), ("Botanical blackwork", 2)]

CSS = """
*{box-sizing:border-box}
html,body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--font-body)}
.wrap{max-width:var(--page-content);margin:0 auto;padding:var(--space-md)}
.want{border:2px solid var(--ink);border-radius:var(--radius-lg);padding:var(--space-md)}
.want h2{margin:0 0 var(--space-sm);font-family:var(--font-display);font-size:15px;letter-spacing:var(--tracking-section-label);text-transform:uppercase;color:var(--muted)}

/* Words only: the list the approved panel already shows. */
.want ul.words{list-style:none;margin:0;padding:0}
.want ul.words li{font-family:var(--font-header);font-weight:400;font-size:clamp(22px,6.5vw,28px);line-height:1.12;text-transform:uppercase}
.want ul.words li+li{border-top:1px solid var(--line-soft);margin-top:var(--space-2xs);padding-top:var(--space-2xs)}

/* Once any entry has a picture, every entry becomes a tile — six columns
   underneath so a short row still divides, exactly as the work grid does. */
.want ul.tiles{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:var(--space-xs)}
.want ul.tiles li{grid-column:span 3;min-width:0}
.want ul.tiles:has(li:last-child:nth-child(2n+1)) li:first-child{grid-column:span 6}
.tile{display:block;width:100%;aspect-ratio:1;border-radius:var(--radius-md);position:relative;overflow:hidden;background:var(--card2)}
.want ul.tiles:has(li:last-child:nth-child(2n+1)) li:first-child .tile{aspect-ratio:16/10}
/* A tile with no reference is not an empty frame: it is the words, set like
   flash, behind the same inner rule the work tiles carry. */
.tile.saidso{display:flex;align-items:center;justify-content:center;padding:var(--space-md);background:var(--card);border:1.5px solid var(--line)}
.tile.saidso span{font-family:var(--font-header);font-weight:400;font-size:clamp(17px,4.6vw,22px);line-height:1.05;text-transform:uppercase;text-align:center;color:var(--ink)}
.tile.shot::after{content:"";position:absolute;inset:9px;border:1.5px solid rgba(247,242,234,.42);border-radius:var(--radius-sm)}
.cap{display:block;margin-top:var(--space-2xs);font-size:14px;line-height:1.3;color:var(--ink);font-weight:700}
"""


def tile(label, ref):
    if ref is None:
        # The tile is already the words; captioning it would say them twice.
        return f'<span class="tile saidso"><span>{label}</span></span>'
    return (f'<span class="tile shot" style="background-image:{GRAIN},{REFS[ref]}"></span>'
            f'<span class="cap">{label}</span>')


def panel(wants):
    anyshot = any(r is not None for _, r in wants)
    if not anyshot:
        items = "".join(f"<li>{w}</li>" for w, _ in wants)
        return f'<section class="want"><h2>Wants to tattoo more of</h2><ul class="words">{items}</ul></section>'
    items = "".join(f"<li>{tile(w, r)}</li>" for w, r in wants)
    return f'<section class="want"><h2>Wants to tattoo more of</h2><ul class="tiles">{items}</ul></section>'


def page(wants):
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>wishlist</title>
<style>{FONTS}{TOKENS}{CSS}</style></head><body><main class="wrap">{panel(wants)}</main></body></html>"""


FILES = {
    "wl-words.html": page(WANTS_WORDS),
    "wl-all.html": page(WANTS_ALL),
    "wl-mixed.html": page(WANTS_MIXED),
    "wl-odd.html": page(WANTS_ODD),
}

FIGS = [("wl-words.html", "Nothing uploaded", "the panel as approved", 430),
        ("wl-all.html", "Every entry has one", "tiles, captioned", 760),
        ("wl-mixed.html", "Two do, two don't", "a wordless entry is flash, not a gap", 760),
        ("wl-odd.html", "Three entries", "odd count leads full width, no hole", 780)]

FILES["gallery-wl.html"] = f"""<!doctype html><html><head><meta charset="utf-8">
<title>Wishlist references</title><style>
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
<h1>Wishlist with reference images, at 390</h1>
<p class="note">A reference is optional per entry, so the panel has to hold words and pictures together.
Once any entry has one, <b>every entry becomes a tile</b>: a wordless entry sets its phrase like flash
behind the same inner rule the work tiles use, so it reads as a deliberate card rather than a picture
that failed to load. Captions sit under every tile. The no-holes rule carries over unchanged.</p>
<div class="row">{"".join(
f'<figure><figcaption><b>{h}</b><span>{s}</span></figcaption>'
f'<iframe src="{f}" width="390" height="{ht}" scrolling="no" loading="eager"></iframe></figure>'
for f, h, s, ht in FIGS)}</div></body></html>"""

for name, text in FILES.items():
    io.open(f"{OUT}/{name}", "w", encoding="utf-8").write(text)
print(f"wrote {len(FILES)} files")
