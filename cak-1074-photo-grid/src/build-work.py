"""The tattoo photos are the portfolio, so this is the work grid on the main
profile, not the About page's strip.

That changes the build for the better. The portfolio is uncapped
(`listPortfolio()` is never sliced), its tiles are already buttons, and
landing.ts already carries the viewer they open. So there is no cap to raise,
no uploader to touch, and no viewer to write — only the grid rule, and
swapping the in-place `<details>` for a section with a back link.

Because the portfolio has no cap, the grid rule cannot be written per count.
It is written with :has() instead, which reads the last tile's position to
learn the remainder and needs no markup change at all:

    one tile over  -> it leads, full width
    two tiles over -> that short row splits in half

`.pf` is three across at every width, so unlike the About strip this needs no
breakpoint variants.
"""
import io, os

OUT = os.path.dirname(os.path.abspath(__file__))
TOKENS = io.open(f"{OUT}/_tokens.css", encoding="utf-8").read()
BASE = io.open(f"{OUT}/_base.css", encoding="utf-8").read()
LANDING = io.open(f"{OUT}/_landing.css", encoding="utf-8").read()

N = 14
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

# THE PATCH. No data attribute, no count in the markup: :has() reads the
# remainder off the last tile's own position in the grid.
RULE = """
.pf{grid-template-columns:repeat(6,minmax(0,1fr))}
.pf .cell{grid-column:span 2}
/* one tile over: it leads, full width */
.pf:has(.cell:last-child:nth-child(3n+1)) .cell:first-child{grid-column:span 6;aspect-ratio:16/10}
/* two tiles over: that short row splits in half */
.pf:has(.cell:last-child:nth-child(3n+2)) .cell:nth-last-child(-n+2){grid-column:span 3;aspect-ratio:4/3}
.seeall{display:flex;align-items:center;justify-content:center;min-height:54px;margin-top:var(--space-sm);border-radius:var(--radius-pill);border:1.5px solid var(--line);font-family:var(--font-display);font-size:20px;letter-spacing:var(--tracking-display-action);text-transform:uppercase;color:var(--ink);cursor:pointer;background:none;width:100%;text-decoration:none}
.back{display:inline-flex;align-items:center;gap:var(--space-2xs);min-height:44px;font-family:var(--font-display);font-size:18px;letter-spacing:var(--tracking-display-action);text-transform:uppercase;color:var(--muted);text-decoration:none}
.back b{color:var(--ink);font-weight:400}
.galhead{margin:var(--space-xs) 0 var(--space-sm)}
.galhead h1{margin:0;font-family:var(--font-header);font-size:30px;line-height:1.05;text-transform:uppercase;color:var(--ink)}
.galhead p{margin:var(--space-2xs) 0 0;color:var(--muted);font-size:14px}"""

LIGHTBOX = """
.lb{position:fixed;inset:0;z-index:9}
.lbbackdrop{position:fixed;inset:0;background:color-mix(in srgb,var(--ink) 62%,transparent)}
.lb .lbstage{position:fixed;inset:0;display:flex;align-items:center;justify-content:center;margin:0;padding:clamp(18px,4vw,48px);box-sizing:border-box}
.lb .lbstage .shot{width:min(92vw,880px);aspect-ratio:1;max-height:82dvh;border-radius:var(--radius);box-shadow:var(--shadow-float)}
.lb button{position:fixed;width:44px;height:44px;border-radius:var(--radius-pill);border:1px solid var(--line);background:var(--bg);color:var(--ink);font-size:26px;line-height:1;cursor:pointer;box-shadow:var(--shadow-float)}
.lbclose{top:max(16px,env(safe-area-inset-top));right:max(16px,env(safe-area-inset-right))}
.lbmeta{position:fixed;left:50%;bottom:max(18px,env(safe-area-inset-bottom));transform:translateX(-50%);display:flex;align-items:center;gap:10px;border:1px solid var(--line);border-radius:var(--radius-pill);background:color-mix(in srgb,var(--bg) 88%,transparent);color:var(--ink);box-shadow:var(--shadow-float);padding:9px 14px;font-size:12px;font-weight:800;text-transform:uppercase;backdrop-filter:blur(10px)}"""

SHOT = """.cell.photo .shot{display:block;width:100%;height:100%;position:relative}
.cell.photo{position:relative;overflow:hidden}
.shot::after{content:attr(data-n);position:absolute;right:7px;bottom:5px;
  font:700 10px/1 var(--font-body,system-ui);color:rgba(255,255,255,.92);
  letter-spacing:.1em;text-shadow:0 1px 4px rgba(0,0,0,.55)}"""


def tile(i):
    return (f'<button class="cell photo" type="button"><span class="shot" data-n="{i + 1}" '
            f'style="background-image:{GRAIN},{LOOKS[i % len(LOOKS)]}"></span></button>')


def grid(count, start=0):
    return (f'<div class="pf">{"".join(tile(i) for i in range(start, start + count))}</div>')


def profile():
    return (f'<main class="wrap"><section class="work">'
            f'<h2 class="sh">Recent work<span class="ct">{N}</span></h2>'
            f'{grid(SHOWN)}<a class="seeall">See all {N}</a></section></main>')


def section(n=N):
    return (f'<main class="wrap"><a class="back">&larr; <b>{NAME}</b></a>'
            f'<div class="galhead"><h1>Recent work</h1><p>{n} pieces</p></div>'
            f"{grid(n)}</main>")


def viewer(index):
    return (f'<div class="lb"><div class="lbbackdrop"></div>'
            f'<div class="lbstage"><span class="shot" data-n="{index + 1}" '
            f'style="background-image:{GRAIN},{LOOKS[index % len(LOOKS)]}"></span></div>'
            f'<button class="lbclose" aria-label="Close">&times;</button>'
            f'<p class="lbmeta">{index + 1} / {N}</p></div>')


def page(body):
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>w</title>
<style>{TOKENS}{BASE}{LANDING}
{SHOT}
html,body{{margin:0;background:var(--bg)}}
.wrap{{padding:14px 16px 24px;max-width:none}}
{RULE}{LIGHTBOX}</style></head><body>{body}</body></html>"""


FILES = {
    "w1-profile.html": page(profile()),
    "w2-section.html": page(section()),
    "w3-viewer.html": page(section() + viewer(8)),
}
# Count sweep for the checker: the rule must hold for any portfolio size.
for n in range(1, 16):
    FILES[f"wc-{n}.html"] = page(page_body := f'<main class="wrap">{grid(n)}</main>')

GAL = """<!doctype html><html><head><meta charset="utf-8"><title>{t}</title>
<style>
body{{margin:0;padding:26px;background:#EDE7DA;font-family:system-ui,sans-serif}}
h1{{margin:0 0 5px;font-size:19px;color:#002325}}
.note{{margin:0 0 20px;font-size:13.5px;color:#5C6B6C;max-width:1240px;line-height:1.55}}
.note b{{color:#002325}} .note code{{background:#E3DCCB;padding:1px 5px;border-radius:4px;font-size:12.5px}}
.row{{display:flex;gap:20px;align-items:flex-start;flex-wrap:wrap}}
figure{{margin:0}}
figcaption{{display:flex;flex-direction:column;gap:2px;margin:0 0 8px;font-size:13px;color:#002325}}
figcaption span{{font-size:11.5px;color:#5C6B6C}}
iframe{{border:1px solid #CFC6B4;border-radius:10px;background:#F7F2EA;display:block}}
</style></head><body><h1>{t}</h1><p class="note">{n}</p><div class="row">{f}</div></body></html>"""

FILES["gallery-w2.html"] = GAL.format(
    t="Recent work: See all opens its own section — at 390",
    n=("The tattoo photos are the portfolio, so this is the main profile's work grid. It is "
       "<b>uncapped and already clickable</b>, and landing.ts already carries the viewer — so "
       "nothing here needs a cap raised, an uploader changed, or a viewer written. "
       "14 pieces: four rows of three, then the last two split the row. No holes."),
    f=('<figure><figcaption><b>1 &middot; the profile</b><span>six pieces, then See all 14</span></figcaption>'
       '<iframe src="w1-profile.html" width="390" height="620" scrolling="no" loading="eager"></iframe></figure>'
       '<figure><figcaption><b>2 &middot; See all tapped</b><span>its own section, all 14, back at the top</span></figcaption>'
       '<iframe src="w2-section.html" width="390" height="1080" scrolling="no" loading="eager"></iframe></figure>'
       '<figure><figcaption><b>3 &middot; a piece tapped</b><span>the viewer landing.ts already has</span></figcaption>'
       '<iframe src="w3-viewer.html" width="390" height="1080" scrolling="no" loading="eager"></iframe></figure>'))

for name, text in FILES.items():
    io.open(f"{OUT}/{name}", "w", encoding="utf-8").write(text)
print(f"wrote {len(FILES)} files")
