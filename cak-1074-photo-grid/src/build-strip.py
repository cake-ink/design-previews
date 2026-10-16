"""The About page photo strip, as it exists today, plus the field artists
actually upload it through.

Nothing here is proposed. It is about.ts and you-about.tsx as they stand, so
the label mismatch can be looked at rather than described: the public page
says "In the studio", and the only thing the artist ever saw said "Photos".
"""
import io, os

OUT = os.path.dirname(os.path.abspath(__file__))
TOKENS = io.open(f"{OUT}/_tokens.css", encoding="utf-8").read()
BASE = io.open(f"{OUT}/_base.css", encoding="utf-8").read()
ABOUT = io.open(f"{OUT}/_about.css", encoding="utf-8").read()
STUDIO = io.open(f"{OUT}/_studio.css", encoding="utf-8").read()

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

PHOTO_CSS = """.ph{display:block;width:100%;aspect-ratio:4/5;border-radius:var(--radius-lg);
  position:relative;overflow:hidden}
.ph::after{content:attr(data-n);position:absolute;right:8px;bottom:6px;
  font:700 10px/1 var(--font-body,system-ui);color:rgba(255,255,255,.92);
  letter-spacing:.1em;text-shadow:0 1px 4px rgba(0,0,0,.55)}
/* the one thing added: a ring around the strip under discussion */
.callout{outline:2px dashed #B4562F;outline-offset:7px;border-radius:4px}"""


def photo(i, ratio="4/5"):
    return (f'<span class="ph" data-n="{i + 1}" style="aspect-ratio:{ratio};'
            f'background-image:{GRAIN},{LOOKS[i % len(LOOKS)]}"></span>')


WORDS = ("<p>I work mostly in fine line and blackwork, and I like projects that take "
         "more than one sitting. Most of what I do starts as a conversation.</p>"
         "<p>Walk-ins on the last Saturday of the month. Everything else is booked ahead.</p>")

SPOTS = ('<ul class="spots">'
         '<li><span class="when">Nov 8&ndash;10</span><span class="where">Ink &amp; Iron'
         '<span>Seattle, WA</span></span></li>'
         '<li><span class="when">Jan 17</span><span class="where">Black Rose Guest Week'
         '<span>Austin, TX</span></span></li></ul>')


def about(callout=True):
    strip = "".join(photo(i) for i in range(5))
    ring = " callout" if callout else ""
    return f"""<main class="wrap">
  <a class="back">&larr; <b>Mara Stone</b></a>
  <span class="portrait">{photo(4, "5/6")}</span>
  <div class="text">
    <div class="who"><h1>Mara Stone</h1><span class="pn">she/her</span></div>
    <p class="line">Portland, OR &middot; Fine line &middot; Blackwork</p>
    <dl class="facts">
      <div><dt>Tattooing since</dt><dd>2016</dd></div>
      <div><dt>Works at</dt><dd>Black Rose Tattoo</dd></div>
    </dl>
    <div class="words">{WORDS}</div>
    <section><h2 class="sh">Guest spots &amp; events</h2>{SPOTS}</section>
    <section><h2 class="sh">In the studio</h2>
      <div class="photos{ring}">{strip}</div>
    </section>
    <a class="btn">Request a booking</a>
  </div>
</main>"""


def studio_room():
    cells = "".join(
        f'<figure class="studio-you-cell">{photo(i, "1")}'
        f'<div class="studio-you-cell-acts"><button type="button">&larr;</button>'
        f'<button type="button">&#10005;</button></div></figure>' for i in range(5))
    return f"""<div style="padding:18px 16px">
  <div class="studio-you-field">
    <label>Where you work</label>
    <input class="studio-you-input" value="Black Rose Tattoo, Austin" readonly>
  </div>
  <div class="studio-you-section callout">Photos</div>
  <div class="studio-you-grid">{cells}
    <label class="studio-you-add">+ Photo</label>
  </div>
  <div class="studio-you-section">Guest spots and events</div>
</div>"""


def page(body, css):
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>strip</title>
<style>{TOKENS}{css}
{PHOTO_CSS}
html,body{{margin:0;background:var(--bg)}}
.wrap{{padding:14px 16px 24px}}
.studio-you-cell .ph{{aspect-ratio:1}}</style></head><body>{body}</body></html>"""


FILES = {
    "z1-about-390.html": page(about(), BASE + ABOUT),
    "z2-about-1000.html": page(about(), BASE + ABOUT),
    "z3-studio-room.html": page(studio_room(), BASE + STUDIO),
}

GAL = """<!doctype html><html><head><meta charset="utf-8"><title>{t}</title>
<style>
body{{margin:0;padding:26px;background:#EDE7DA;font-family:system-ui,sans-serif}}
h1{{margin:0 0 5px;font-size:19px;color:#002325}}
.note{{margin:0 0 20px;font-size:13.5px;color:#5C6B6C;max-width:1260px;line-height:1.55}}
.note b{{color:#002325}} .note code{{background:#E3DCCB;padding:1px 5px;border-radius:4px;font-size:12.5px}}
.ring{{color:#B4562F;font-weight:700}}
.row{{display:flex;gap:20px;align-items:flex-start;flex-wrap:wrap}}
figure{{margin:0}}
figcaption{{display:flex;flex-direction:column;gap:2px;margin:0 0 8px;font-size:13px;color:#002325}}
figcaption span{{font-size:11.5px;color:#5C6B6C}}
iframe{{border:1px solid #CFC6B4;border-radius:10px;background:#F7F2EA;display:block}}
</style></head><body><h1>{t}</h1><p class="note">{n}</p><div class="row">{f}</div></body></html>"""

FILES["gallery-z.html"] = GAL.format(
    t="The About page photo strip as it stands today",
    n=("Nothing proposed here — this is <code>about.ts</code> and <code>you-about.tsx</code> as "
       "they are now, with the strip <span class='ring'>ringed</span>. It sits near the bottom of "
       "the About page, after the bio and the guest spots, under the heading <b>In the studio</b>. "
       "The third frame is the only place the artist ever meets it: a section labelled plainly "
       "<b>Photos</b>, with a <b>+ Photo</b> button and no guidance. Capped at six, and the public "
       "photos are plain images &mdash; not buttons, so tapping one does nothing."),
    f=('<figure><figcaption><b>1 &middot; the About page, 390</b>'
       '<span>strip near the bottom, under &ldquo;In the studio&rdquo;</span></figcaption>'
       '<iframe src="z1-about-390.html" width="390" height="2010" scrolling="no" loading="eager"></iframe></figure>'
       '<figure><figcaption><b>2 &middot; the same page, 1000</b>'
       '<span>portrait column left, strip three across</span></figcaption>'
       '<iframe src="z2-about-1000.html" width="1000" height="1560" scrolling="no" loading="eager"></iframe></figure>'
       '<figure><figcaption><b>3 &middot; where she uploads them</b>'
       '<span>the About room &mdash; the label just says Photos</span></figcaption>'
       '<iframe src="z3-studio-room.html" width="430" height="700" scrolling="no" loading="eager"></iframe></figure>'))

for name, text in FILES.items():
    io.open(f"{OUT}/{name}", "w", encoding="utf-8").write(text)
print(f"wrote {len(FILES)} files")
