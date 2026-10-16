"""Micah: See all opens a whole other section of all their work, and back
returns to the main profile.

So it is a route, not an overlay — which is what the back gesture needs, and
it matches how /@slug/about already hangs off /@slug. The About page's own
header idiom is `.back` reading `<- Mara Stone`, so the photos section reuses
that rather than the close button the earlier overlay sketch had.

Three frames: the profile with the pill, the section it opens, and the viewer
a photo opens from there (landing.ts' dialog#lightbox, the public twin of the
one requests uses).
"""
import io, os

OUT = os.path.dirname(os.path.abspath(__file__))
TOKENS = io.open(f"{OUT}/_tokens.css", encoding="utf-8").read()
BASE = io.open(f"{OUT}/_base.css", encoding="utf-8").read()
ABOUT = io.open(f"{OUT}/_about.css", encoding="utf-8").read()

N = 12
SHOWN = 6
NAME = "Mara Stone"

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

GRID_RULE = """
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
.seeall{display:flex;align-items:center;justify-content:center;min-height:54px;margin-top:var(--space-sm);border-radius:var(--radius-pill);border:1.5px solid var(--line);font-family:var(--font-display);font-size:20px;letter-spacing:var(--tracking-display-action);text-transform:uppercase;color:var(--ink);cursor:pointer;background:none;width:100%;text-decoration:none}
/* The section's own heading, sized like the About page's h1 rather than a
   section label, because here it is the page. */
.galhead{margin:var(--space-sm) 0 var(--space-md)}
.galhead h1{margin:0;font-family:var(--font-header);font-size:30px;line-height:1.05;letter-spacing:var(--tracking-display-heading);text-transform:uppercase;color:var(--ink)}
.galhead p{margin:var(--space-2xs) 0 0;color:var(--muted);font-size:14px}"""

LIGHTBOX = """
.lb{position:fixed;inset:0;z-index:9}
.lbbackdrop{position:fixed;inset:0;background:color-mix(in srgb,var(--ink) 62%,transparent)}
.lb .lbstage{position:fixed;inset:0;display:flex;align-items:center;justify-content:center;margin:0;padding:clamp(18px,4vw,48px);touch-action:pan-y;box-sizing:border-box}
.lb .lbstage .ph{width:min(92vw,880px);max-width:min(92vw,880px);aspect-ratio:4/5;max-height:82dvh;border-radius:var(--radius);box-shadow:var(--shadow-float)}
.lb button{position:fixed;width:44px;height:44px;border-radius:var(--radius-pill);border:1px solid var(--line);background:var(--bg);color:var(--ink);font-size:26px;line-height:1;cursor:pointer;box-shadow:var(--shadow-float)}
.lbclose{top:max(16px,env(safe-area-inset-top));right:max(16px,env(safe-area-inset-right))}
.lbmeta{position:fixed;left:50%;bottom:max(18px,env(safe-area-inset-bottom));transform:translateX(-50%);display:flex;align-items:center;gap:10px;border:1px solid var(--line);border-radius:var(--radius-pill);background:color-mix(in srgb,var(--bg) 88%,transparent);color:var(--ink);box-shadow:var(--shadow-float);padding:9px 14px;font-size:12px;font-weight:800;letter-spacing:var(--tracking-media-description);text-transform:uppercase;backdrop-filter:blur(10px)}"""

PHOTO_CSS = """.ph{display:block;width:100%;aspect-ratio:4/5;border-radius:var(--radius-lg);
  position:relative;overflow:hidden}
.ph::after{content:attr(data-n);position:absolute;right:8px;bottom:6px;
  font:700 10px/1 var(--font-body,system-ui);color:rgba(255,255,255,.92);
  letter-spacing:.1em;text-shadow:0 1px 4px rgba(0,0,0,.55)}"""


def photo(i):
    return (f'<span class="ph" data-n="{i + 1}" '
            f'style="background-image:{GRAIN},{LOOKS[i % len(LOOKS)]}"></span>')


def about_page():
    cells = "".join(photo(i) for i in range(SHOWN))
    return (f'<main class="wrap"><a class="back">&larr; <b>{NAME}</b></a>'
            f'<div class="text"><section aria-labelledby="pt">'
            f'<h2 class="sh" id="pt">In the studio</h2>'
            f'<div class="photos" data-n="{SHOWN}">{cells}</div>'
            f'<a class="seeall">See all {N}</a>'
            f"</section></div></main>")


def gallery_page():
    cells = "".join(photo(i) for i in range(N))
    return (f'<main class="wrap solo"><a class="back">&larr; <b>{NAME}</b></a>'
            f'<div class="text"><div class="galhead"><h1>In the studio</h1>'
            f'<p>{N} photos</p></div>'
            f'<div class="photos" data-n="{N}">{cells}</div></div></main>')


def viewer(index):
    return (f'<div class="lb"><div class="lbbackdrop"></div>'
            f'<div class="lbstage">{photo(index)}</div>'
            f'<button class="lbclose" aria-label="Close">&times;</button>'
            f'<p class="lbmeta">{index + 1} / {N}</p></div>')


def page(body):
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>s</title>
<style>{TOKENS}{BASE}{ABOUT}
{PHOTO_CSS}
html,body{{margin:0;background:var(--bg)}}
.wrap{{padding:14px 16px 24px}}
{GRID_RULE}{LIGHTBOX}</style></head><body>{body}</body></html>"""


FILES = {
    "y1-about.html": page(about_page()),
    "y2-gallery.html": page(gallery_page()),
    "y3-viewer.html": page(gallery_page() + viewer(6)),
}

GAL = """<!doctype html><html><head><meta charset="utf-8"><title>{t}</title>
<style>
body{{margin:0;padding:26px 26px 30px;background:#EDE7DA;font-family:system-ui,sans-serif}}
h1{{margin:0 0 5px;font-size:19px;color:#002325}}
.note{{margin:0 0 20px;font-size:13.5px;color:#5C6B6C;max-width:1240px;line-height:1.55}}
.note b{{color:#002325}} .note code{{background:#E3DCCB;padding:1px 5px;border-radius:4px;font-size:12.5px}}
.row{{display:flex;gap:20px;align-items:flex-start;flex-wrap:wrap}}
figure{{margin:0}}
figcaption{{display:flex;flex-direction:column;gap:2px;margin:0 0 8px;font-size:13px;color:#002325}}
figcaption span{{font-size:11.5px;color:#5C6B6C}}
iframe{{border:1px solid #CFC6B4;border-radius:10px;background:#F7F2EA;display:block}}
</style></head><body><h1>{t}</h1><p class="note">{n}</p><div class="row">{f}</div></body></html>"""

FILES["gallery-y.html"] = GAL.format(
    t="See all opens its own section; back returns to the profile — at 390",
    n=("A route, not an overlay, so the phone's back gesture and the browser's back button both "
       "work and the gallery can be linked. It hangs off the profile the way "
       "<code>/@mara/about</code> already does, and reuses that page's own back idiom — "
       "<b>&larr; MARA STONE</b> — rather than a close button. Tapping a photo there opens the "
       "same viewer requests uses."),
    f=(f'<figure><figcaption><b>1 &middot; the profile</b><span>six photos, then See all 12</span>'
       f'</figcaption><iframe src="y1-about.html" width="390" height="930" scrolling="no" loading="eager"></iframe></figure>'
       f'<figure><figcaption><b>2 &middot; See all tapped</b><span>its own section, all twelve, back at the top</span>'
       f'</figcaption><iframe src="y2-gallery.html" width="390" height="1500" scrolling="no" loading="eager"></iframe></figure>'
       f'<figure><figcaption><b>3 &middot; a photo tapped</b><span>viewer at 7 of 12</span>'
       f'</figcaption><iframe src="y3-viewer.html" width="390" height="930" scrolling="no" loading="eager"></iframe></figure>'))

for name, text in FILES.items():
    io.open(f"{OUT}/{name}", "w", encoding="utf-8").write(text)
print(f"wrote {len(FILES)} files")
