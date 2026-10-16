"""Three directions for the About page redesign.

The brief: the page is where an artist says more about herself — how long she
has tattooed, what she wants to tattoo more of, her background, and maybe one
big photo of her working. None of it required; the page still has to look
finished with any of it missing.

So each direction is rendered from one template against three content states,
not drawn three times by hand. If a direction only looks good full, the sparse
and bare frames will say so.

  FULL    everything set
  SPARSE  a name, a city, one paragraph, a year. No photo, no wishlist,
          no guest spots, no socials.
  BARE    a name. Nothing else at all.

Built on the real token set; the page CSS is written fresh per direction
because that is the thing being chosen.
"""
import io, os

OUT = os.path.dirname(os.path.abspath(__file__))
TOKENS = io.open(f"{OUT}/_tokens.css", encoding="utf-8").read()
# The display faces are embedded in the pages' shared CSS; pull only the
# @font-face blocks, since the layout rules here are written fresh.
FONTS = io.open(f"{OUT}/_fonts.css", encoding="utf-8").read()

GRAIN = ("repeating-linear-gradient(118deg,rgba(255,255,255,.055) 0 2px,"
         "rgba(0,0,0,.045) 2px 4px)")
WORKING = ("radial-gradient(135% 110% at 28% 16%,#E6DCC8 0%,#B6A88E 34%,"
           "#6B6250 70%,#332F27 100%)")
PORTRAIT = "radial-gradient(130% 100% at 50% 8%,#DCE2E0 0%,#9AA6A4 40%,#4E5A59 100%)"

FULL = {
    "name": "Mara Stone", "pronouns": "she/her", "place": "Portland, OR",
    "since": 2016, "worksAt": "Black Rose Tattoo",
    "bio": ["I started out painting signs, which is still how I think about a tattoo — "
            "it has to read from across the room and hold up close.",
            "Most of what I do starts as a conversation. I would rather spend an hour "
            "getting the idea right than redraw it on the day."],
    "wish": ["Cover-ups", "Large-scale back pieces", "Botanical blackwork", "Lettering"],
    "photo": True, "portrait": True,
    "spots": [("Nov 8–10", "Ink &amp; Iron", "Seattle, WA"),
              ("Jan 17", "Black Rose Guest Week", "Austin, TX")],
    "socials": True,
}
SPARSE = {
    "name": "Dani Okafor", "pronouns": None, "place": "Chicago, IL",
    "since": 2021, "worksAt": None,
    "bio": ["Three years in, mostly fine line. Still figuring out what I am best at, "
            "and happy to say so."],
    "wish": [], "photo": False, "portrait": False, "spots": [], "socials": False,
}
BARE = {
    "name": "Sam Reyes", "pronouns": None, "place": None, "since": None,
    "worksAt": None, "bio": [], "wish": [], "photo": False, "portrait": False,
    "spots": [], "socials": False,
}
STATES = [("full", FULL), ("sparse", SPARSE), ("bare", BARE)]


def years(a):
    """`since` is a year; the page says the span, not the arithmetic."""
    return None if not a["since"] else f"Tattooing since {a['since']}"


def plate(ratio="3/2"):
    return (f'<span class="plate" style="aspect-ratio:{ratio};'
            f'background-image:{GRAIN},{WORKING}"></span>')


def port():
    return (f'<span class="port" style="background-image:{GRAIN},{PORTRAIT}"></span>')


def spots_block(a, cls="spots"):
    if not a["spots"]:
        return ""
    rows = "".join(f'<li><span class="when">{w}</span>'
                   f'<span class="where">{p}<span>{c}</span></span></li>'
                   for w, p, c in a["spots"])
    return (f'<section><h2 class="sh">Guest spots</h2>'
            f'<ul class="{cls}">{rows}</ul></section>')


def links(a):
    if not a["socials"]:
        return ""
    return '<p class="links"><a href="#">Instagram</a><a href="#">TikTok</a></p>'


SHARED = """
*{box-sizing:border-box}
html,body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--font-body)}
.wrap{max-width:var(--page-content);margin:0 auto;padding:14px var(--space-md) var(--space-2xl)}
.back{display:inline-flex;align-items:center;gap:var(--space-2xs);min-height:44px;font-family:var(--font-display);font-size:18px;letter-spacing:var(--tracking-display-action);text-transform:uppercase;color:var(--muted);text-decoration:none}
.back b{color:var(--ink);font-weight:400}
.plate,.port{display:block;width:100%;border-radius:var(--radius-lg);position:relative;overflow:hidden}
/* the inner hairline the work tiles already use */
.plate::after{content:"";position:absolute;inset:10px;border:1.5px solid rgba(247,242,234,.45);border-radius:var(--radius-md);pointer-events:none}
.port{aspect-ratio:5/6;border-radius:var(--radius-2xl)}
.sh{font-family:var(--font-header);font-weight:400;font-size:clamp(26px,7vw,32px);line-height:.95;text-transform:uppercase;color:var(--ink);margin:var(--space-xl) 0 var(--space-sm)}
.spots{list-style:none;margin:0;padding:0;border-top:1px solid var(--line)}
.spots li{display:grid;grid-template-columns:minmax(0,8.5em) minmax(0,1fr);gap:var(--space-sm);align-items:baseline;padding:var(--space-sm) 0;border-bottom:1px solid var(--line)}
.spots .when{font-family:var(--font-display);font-size:20px;letter-spacing:var(--tracking-display-action);text-transform:uppercase}
.spots .where{font-weight:700}
.spots .where span{display:block;font-weight:400;color:var(--muted)}
.links{display:flex;flex-wrap:wrap;gap:var(--space-xs);margin:var(--space-lg) 0 0}
.links a{display:inline-flex;align-items:center;min-height:48px;padding:0 var(--space-md);border:1.5px solid var(--line);border-radius:var(--radius-pill);background:var(--card);color:var(--ink);font-weight:700;text-decoration:none}
.btn{display:flex;align-items:center;justify-content:center;min-height:56px;margin-top:var(--space-xl);border-radius:var(--radius-pill);background:var(--acc);color:var(--onacc);font-family:var(--font-display);font-size:21px;letter-spacing:var(--tracking-display-action);text-transform:uppercase;text-decoration:none}
"""

# ---------------------------------------------------------------- A: the plate
CSS_A = """
.hero{margin-top:var(--space-sm)}
.hero .plate{margin-bottom:var(--space-lg)}
.nm{font-family:var(--font-header);font-weight:400;line-height:.86;text-transform:uppercase;margin:0;
  font-size:clamp(44px,14vw,76px)}
/* with no photo the name is the picture, so it takes the room the photo had */
.noshot .nm{font-size:clamp(56px,19vw,104px);margin-top:var(--space-lg)}
.pn{display:block;margin-top:var(--space-xs);font-family:var(--font-display);font-size:19px;letter-spacing:var(--tracking-display-action);text-transform:uppercase;color:var(--muted)}
.meta{margin:var(--space-md) 0 0;padding-top:var(--space-md);border-top:2px solid var(--ink);font-weight:700}
.meta span+span::before{content:" · ";color:var(--muted);font-weight:400}
.words{margin-top:var(--space-lg);font-size:17px;line-height:1.62}
.words p{margin:0 0 var(--space-md)}
.want{margin-top:var(--space-xl);border:2px solid var(--ink);border-radius:var(--radius-lg);padding:var(--space-md) var(--space-md) var(--space-sm)}
.want h2{margin:0;font-family:var(--font-display);font-size:15px;letter-spacing:var(--tracking-section-label);text-transform:uppercase;color:var(--muted)}
.want ul{list-style:none;margin:var(--space-xs) 0 0;padding:0}
.want li{font-family:var(--font-header);font-weight:400;font-size:clamp(22px,6.5vw,28px);line-height:1.12;text-transform:uppercase}
.want li+li{border-top:1px solid var(--line-soft);margin-top:var(--space-2xs);padding-top:var(--space-2xs)}
"""


def render_a(a):
    shot = f'<div class="hero">{plate()}</div>' if a["photo"] else ""
    meta = [x for x in (a["place"], years(a), a["worksAt"]) if x]
    want = ""
    if a["wish"]:
        want = ('<section class="want"><h2>Wants to tattoo more of</h2><ul>'
                + "".join(f"<li>{w}</li>" for w in a["wish"]) + "</ul></section>")
    return f"""<main class="wrap{"" if a["photo"] else " noshot"}">
  <a class="back">&larr; <b>{a["name"]}</b></a>
  {shot}
  <h1 class="nm">{a["name"]}</h1>
  {f'<span class="pn">{a["pronouns"]}</span>' if a["pronouns"] else ""}
  {f'<p class="meta">{"".join(f"<span>{m}</span>" for m in meta)}</p>' if meta else ""}
  {f'<div class="words">{"".join(f"<p>{p}</p>" for p in a["bio"])}</div>' if a["bio"] else ""}
  {want}
  {spots_block(a)}
  {links(a)}
  <a class="btn">Request a session</a>
</main>"""


# --------------------------------------------------------------- B: the letter
CSS_B = """
.top{display:flex;align-items:flex-end;gap:var(--space-md);margin-top:var(--space-sm)}
.top .port{flex:none;width:clamp(96px,28vw,132px)}
.nm{font-family:var(--font-header);font-weight:400;line-height:.88;text-transform:uppercase;margin:0;font-size:clamp(38px,11vw,58px)}
.pn{font-family:var(--font-display);font-size:18px;letter-spacing:var(--tracking-display-action);text-transform:uppercase;color:var(--muted)}
.meta{margin:var(--space-md) 0 0;color:var(--muted);font-weight:700}
.meta span+span::before{content:" · ";font-weight:400}
/* her words are the page, so they are set larger than body copy */
.lede{margin-top:var(--space-lg);font-size:clamp(18px,4.8vw,21px);line-height:1.52}
.lede p{margin:0 0 var(--space-md)}
.lede .plate{margin:var(--space-lg) 0}
.want{margin-top:var(--space-lg);padding-left:var(--space-md);border-left:3px solid var(--acc)}
.want h2{margin:0 0 var(--space-2xs);font-family:var(--font-display);font-size:15px;letter-spacing:var(--tracking-section-label);text-transform:uppercase;color:var(--muted)}
.want p{margin:0;font-size:clamp(18px,4.8vw,21px);line-height:1.45}
@media (min-width:760px){
  /* the photo sits beside her words rather than interrupting them */
  .lede .plate{float:right;width:48%;margin:4px 0 var(--space-md) var(--space-lg)}
}
"""


def render_b(a):
    meta = [x for x in (a["place"], years(a), a["worksAt"]) if x]
    body = ""
    if a["bio"]:
        parts = [f"<p>{p}</p>" for p in a["bio"]]
        if a["photo"]:
            parts.insert(1 if len(parts) > 1 else 1, plate("4/3"))
        body = f'<div class="lede">{"".join(parts)}</div>'
    elif a["photo"]:
        body = f'<div class="lede">{plate("4/3")}</div>'
    want = ""
    if a["wish"]:
        run = ", ".join(w.lower() for w in a["wish"])
        want = (f'<section class="want"><h2>On my list</h2>'
                f'<p>Right now I most want to tattoo {run}.</p></section>')
    name = f'<div><h1 class="nm">{a["name"]}</h1>' + \
           (f'<span class="pn">{a["pronouns"]}</span>' if a["pronouns"] else "") + "</div>"
    top = f'<div class="top">{port() if a["portrait"] else ""}{name}</div>'
    return f"""<main class="wrap">
  <a class="back">&larr; <b>{a["name"]}</b></a>
  {top}
  {f'<p class="meta">{"".join(f"<span>{m}</span>" for m in meta)}</p>' if meta else ""}
  {body}
  {want}
  {spots_block(a)}
  {links(a)}
  <a class="btn">Request a session</a>
</main>"""


# --------------------------------------------------------------- C: the ledger
CSS_C = """
.nm{font-family:var(--font-header);font-weight:400;line-height:.88;text-transform:uppercase;margin:var(--space-sm) 0 0;font-size:clamp(42px,13vw,68px)}
.pn{display:block;margin-top:var(--space-2xs);font-family:var(--font-display);font-size:18px;letter-spacing:var(--tracking-display-action);text-transform:uppercase;color:var(--muted)}
.ledger{margin-top:var(--space-lg);border-top:2px solid var(--ink)}
.ledger .row{display:grid;grid-template-columns:minmax(0,7.5em) minmax(0,1fr);gap:var(--space-sm);align-items:baseline;padding:var(--space-md) 0;border-bottom:1px solid var(--line)}
.ledger dt{font-family:var(--font-display);font-size:14px;letter-spacing:var(--tracking-section-label);text-transform:uppercase;color:var(--muted)}
.ledger dd{margin:0;font-size:17px;line-height:1.55}
.ledger dd p{margin:0 0 var(--space-sm)}.ledger dd p:last-child{margin:0}
.ledger .big{font-family:var(--font-header);font-weight:400;font-size:28px;line-height:1;text-transform:uppercase}
.ledger ul{list-style:none;margin:0;padding:0}
.ledger li{font-family:var(--font-header);font-weight:400;font-size:22px;line-height:1.2;text-transform:uppercase}
.ledger .plate{margin-top:var(--space-xs)}
@media (max-width:420px){
  /* the label stops being a column and becomes a line above its entry */
  .ledger .row{grid-template-columns:minmax(0,1fr);gap:var(--space-2xs)}
}
"""


def render_c(a):
    rows = []
    if a["place"]:
        rows.append(("Where", f'<span class="big">{a["place"]}</span>'))
    if a["since"]:
        rows.append(("Tattooing since", f'<span class="big">{a["since"]}</span>'))
    if a["worksAt"]:
        rows.append(("Works at", a["worksAt"]))
    if a["bio"]:
        rows.append(("Background", "".join(f"<p>{p}</p>" for p in a["bio"])))
    if a["wish"]:
        rows.append(("Wants to tattoo",
                     "<ul>" + "".join(f"<li>{w}</li>" for w in a["wish"]) + "</ul>"))
    if a["photo"]:
        rows.append(("At work", plate("3/2")))
    if a["spots"]:
        rows.append(("Guest spots", "".join(
            f'<p><b>{p}</b> &middot; {c}<br><span style="color:var(--muted)">{w}</span></p>'
            for w, p, c in a["spots"])))
    led = "".join(f'<div class="row"><dt>{k}</dt><dd>{v}</dd></div>' for k, v in rows)
    return f"""<main class="wrap">
  <a class="back">&larr; <b>{a["name"]}</b></a>
  <h1 class="nm">{a["name"]}</h1>
  {f'<span class="pn">{a["pronouns"]}</span>' if a["pronouns"] else ""}
  {f'<dl class="ledger">{led}</dl>' if rows else ""}
  {links(a)}
  <a class="btn">Request a session</a>
</main>"""


DIRS = [("a", "The plate", CSS_A, render_a),
        ("b", "The letter", CSS_B, render_b),
        ("c", "The ledger", CSS_C, render_c)]


def page(css, body):
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>about</title>
<style>{FONTS}{TOKENS}{SHARED}{css}</style></head><body>{body}</body></html>"""


FILES = {}
for key, _, css, fn in DIRS:
    for state, data in STATES:
        FILES[f"ab-{key}-{state}.html"] = page(css, fn(data))

GAL = """<!doctype html><html><head><meta charset="utf-8"><title>{t}</title>
<style>
body{{margin:0;padding:26px;background:#EDE7DA;font-family:system-ui,sans-serif}}
h1{{margin:0 0 5px;font-size:19px;color:#002325}}
.note{{margin:0 0 4px;font-size:13.5px;color:#5C6B6C;max-width:1280px;line-height:1.55}}
.note b{{color:#002325}}
.lead{{margin:22px 0 10px;font-size:15px;font-weight:700;color:#002325}}
.lead span{{font-weight:400;color:#5C6B6C}}
.row{{display:flex;gap:18px;align-items:flex-start;flex-wrap:wrap}}
figure{{margin:0}}
figcaption{{display:flex;flex-direction:column;gap:2px;margin:0 0 8px;font-size:12.5px;color:#002325}}
figcaption span{{font-size:11px;color:#5C6B6C}}
iframe{{border:1px solid #CFC6B4;border-radius:10px;background:#F7F2EA;display:block}}
</style></head><body><h1>{t}</h1><p class="note">{n}</p>{s}</body></html>"""

CAP = {"full": ("everything set", "photo, wishlist, background, spots, socials"),
       "sparse": ("a name, a city, a year, one paragraph", "no photo, no wishlist, no spots"),
       "bare": ("a name, and nothing else", "the hardest case")}
BLURB = {
    "a": "Photo first, name huge beneath it, and the wishlist as a bordered panel set in the "
         "header face. With no photo the name grows into the space the photo had, so the page "
         "opens on a statement either way.",
    "b": "Her words are the page. The portrait is small and sits beside the name; the working "
         "photo drops into the prose and floats beside it on a wide screen. The wishlist is a "
         "sentence in her voice rather than a list.",
    "c": "Every entry is a labelled row on a hairline rule — a shop ledger. Missing entries are "
         "not gaps, they are rows that never existed, which is why this one survives the bare "
         "case best. The photo is just another entry.",
}

sections = []
for key, title, _, _ in DIRS:
    figs = "".join(
        f'<figure><figcaption><b>{CAP[s][0]}</b><span>{CAP[s][1]}</span></figcaption>'
        f'<iframe src="ab-{key}-{s}.html" width="390" height="{h}" scrolling="no" loading="eager"></iframe></figure>'
        for s, h in (("full", 1700), ("sparse", 760), ("bare", 420)))
    sections.append(f'<p class="lead">{key.upper()} &middot; {title} '
                    f'<span>&mdash; {BLURB[key]}</span></p><div class="row">{figs}</div>')

# One gallery per direction: nine frames on one sheet renders each too small
# to judge type at, and these are type-led layouts.
for (key, title, _, _), sec in zip(DIRS, sections):
    FILES[f"gallery-about-{key}.html"] = GAL.format(
        t=f"About page — {key.upper()}: {title}, at three levels of emptiness (390)",
        n=("All three frames come from one template fed three content states. "
           "<b>Nothing is required</b>, so the sparse and bare frames are the real test: a page "
           "with only a name still has to look finished rather than broken. Tiles are tonal "
           "stand-ins, not real work."),
        s=sec)

for name, text in FILES.items():
    io.open(f"{OUT}/{name}", "w", encoding="utf-8").write(text)
print(f"wrote {len(FILES)} files")
