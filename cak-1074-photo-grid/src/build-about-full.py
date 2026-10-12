"""The About page as a website replacement.

Direction C (the ledger) carrying A's wishlist panel, extended with the things
an artist's own site has that Cake has no home for yet. Each addition is one
more labelled row, which is the whole reason the ledger was the right pick:
the page grows by a row rather than by a redesign, and an artist who fills in
none of them still gets a finished page.

What already exists and is deliberately NOT duplicated here:
  policies and FAQs   landing.ts:321-324, collapsible rows on the profile
  the work grid       landing.ts, with its viewer
  books open/closed   a flag the profile already shows

What is new, and why a website has it:
  RATES          the first question every client asks; Cake stores no price
                 anywhere today, only a free-text deposit policy
  GETTING THERE  studio_name and studio_address are already stored and go out
                 in reminder emails, but no public page has ever shown them
  BOOKING INTO   "books open" is binary; a site says how far out
  WON'T TATTOO   the scope line that saves both sides a wasted request
  LANGUAGES      a real filter for a lot of clients
  AFTERCARE      they already send it after a session; a client cannot look it
                 up three weeks later
  LICENCE        the trust credential a shop site always carries
"""
import io, os

OUT = os.path.dirname(os.path.abspath(__file__))
TOKENS = io.open(f"{OUT}/_tokens.css", encoding="utf-8").read()
FONTS = io.open(f"{OUT}/_fonts.css", encoding="utf-8").read()

GRAIN = ("repeating-linear-gradient(118deg,rgba(255,255,255,.055) 0 2px,"
         "rgba(0,0,0,.045) 2px 4px)")
WORKING = ("radial-gradient(135% 110% at 28% 16%,#E6DCC8 0%,#B6A88E 34%,"
           "#6B6250 70%,#332F27 100%)")

FULL = {
    "name": "Mara Stone", "pronouns": "she/her", "place": "Portland, OR",
    "since": 2016,
    "studio": "Black Rose Tattoo", "address": "412 Main St, Portland, OR",
    "access": "Street parking on 5th. Step-free entrance, gender-neutral restroom.",
    "bio": ["I started out painting signs, which is still how I think about a tattoo — "
            "it has to read from across the room and hold up close.",
            "Most of what I do starts as a conversation. I would rather spend an hour "
            "getting the idea right than redraw it on the day."],
    "wish": ["Cover-ups", "Large-scale back pieces", "Botanical blackwork", "Lettering"],
    "wont": "No faces, hands or throats. I don't copy another artist's work, "
            "but I'm glad to talk about what drew you to it.",
    "rates": [("Shop minimum", "$150"), ("Hourly", "$180"),
              ("Deposit", "$100, comes off the total")],
    "booking": "Open · booking into March",
    "languages": "English, Spanish",
    "aftercare": True,
    "licence": "Oregon body art practitioner #BA-4471 · Bloodborne pathogens "
               "certified, renewed 2026",
    "photo": True,
    "spots": [("Nov 8–10", "Ink &amp; Iron", "Seattle, WA"),
              ("Jan 17", "Black Rose Guest Week", "Austin, TX")],
    "socials": True,
}
# The same page from someone who filled in almost nothing.
SPARSE = {
    "name": "Dani Okafor", "pronouns": None, "place": "Chicago, IL", "since": 2021,
    "studio": None, "address": None, "access": None,
    "bio": ["Three years in, mostly fine line. Still figuring out what I am best at, "
            "and happy to say so."],
    "wish": [], "wont": None, "rates": [], "booking": "Open",
    "languages": None, "aftercare": False, "licence": None, "photo": False,
    "spots": [], "socials": False,
}

CSS = """
*{box-sizing:border-box}
html,body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--font-body)}
.wrap{max-width:var(--page-content);margin:0 auto;padding:14px var(--space-md) var(--space-2xl)}
.back{display:inline-flex;align-items:center;gap:var(--space-2xs);min-height:44px;font-family:var(--font-display);font-size:18px;letter-spacing:var(--tracking-display-action);text-transform:uppercase;color:var(--muted);text-decoration:none}
.back b{color:var(--ink);font-weight:400}
.nm{font-family:var(--font-header);font-weight:400;line-height:.88;text-transform:uppercase;margin:var(--space-sm) 0 0;font-size:clamp(42px,13vw,68px)}
.pn{display:block;margin-top:var(--space-2xs);font-family:var(--font-display);font-size:18px;letter-spacing:var(--tracking-display-action);text-transform:uppercase;color:var(--muted)}

.ledger{margin-top:var(--space-lg);border-top:2px solid var(--ink)}
.ledger .row{display:grid;grid-template-columns:minmax(0,7.5em) minmax(0,1fr);gap:var(--space-sm);align-items:baseline;padding:var(--space-md) 0;border-bottom:1px solid var(--line)}
.ledger dt{font-family:var(--font-display);font-size:14px;letter-spacing:var(--tracking-section-label);text-transform:uppercase;color:var(--muted)}
.ledger dd{margin:0;font-size:17px;line-height:1.55}
.ledger dd p{margin:0 0 var(--space-sm)}.ledger dd p:last-child{margin:0}
.ledger .big{font-family:var(--font-header);font-weight:400;font-size:28px;line-height:1;text-transform:uppercase}
.ledger .sub{display:block;margin-top:var(--space-2xs);color:var(--muted);font-size:15px;line-height:1.45}
.ledger .plate{display:block;width:100%;aspect-ratio:3/2;border-radius:var(--radius-lg);position:relative;overflow:hidden;margin-top:var(--space-xs)}
.ledger .plate::after{content:"";position:absolute;inset:10px;border:1.5px solid rgba(247,242,234,.45);border-radius:var(--radius-md)}
.ledger a.link{color:var(--ink);text-underline-offset:3px}

/* Rates are numbers, so they get a number's treatment rather than a sentence. */
.rates{display:grid;gap:var(--space-xs)}
.rates div{display:flex;align-items:baseline;justify-content:space-between;gap:var(--space-sm)}
.rates dt{font-family:var(--font-body);font-size:15px;letter-spacing:0;text-transform:none;color:var(--muted)}
.rates .amt{font-family:var(--font-header);font-weight:400;font-size:24px;line-height:1;text-transform:uppercase;white-space:nowrap}
.rates .amt small{font-family:var(--font-body);font-size:14px;color:var(--muted);text-transform:none}

/* The one thing allowed to break the ruled rhythm: it is the only entry that
   looks forward rather than back. */
.want{margin:var(--space-lg) 0;border:2px solid var(--ink);border-radius:var(--radius-lg);padding:var(--space-md) var(--space-md) var(--space-sm)}
.want h2{margin:0;font-family:var(--font-display);font-size:15px;letter-spacing:var(--tracking-section-label);text-transform:uppercase;color:var(--muted)}
.want ul{list-style:none;margin:var(--space-xs) 0 0;padding:0}
.want li{font-family:var(--font-header);font-weight:400;font-size:clamp(22px,6.5vw,28px);line-height:1.12;text-transform:uppercase}
.want li+li{border-top:1px solid var(--line-soft);margin-top:var(--space-2xs);padding-top:var(--space-2xs)}

.links{display:flex;flex-wrap:wrap;gap:var(--space-xs);margin:var(--space-lg) 0 0}
.links a{display:inline-flex;align-items:center;min-height:48px;padding:0 var(--space-md);border:1.5px solid var(--line);border-radius:var(--radius-pill);background:var(--card);color:var(--ink);font-weight:700;text-decoration:none}
.btn{display:flex;align-items:center;justify-content:center;min-height:56px;margin-top:var(--space-xl);border-radius:var(--radius-pill);background:var(--acc);color:var(--onacc);font-family:var(--font-display);font-size:21px;letter-spacing:var(--tracking-display-action);text-transform:uppercase;text-decoration:none}
@media (max-width:420px){
  .ledger .row{grid-template-columns:minmax(0,1fr);gap:var(--space-2xs)}
}
"""


def render(a):
    rows = []
    if a["place"]:
        rows.append(("Where", f'<span class="big">{a["place"]}</span>'))
    if a["since"]:
        rows.append(("Tattooing since", f'<span class="big">{a["since"]}</span>'))
    if a["booking"]:
        rows.append(("Books", f'<span class="big">{a["booking"]}</span>'))
    if a["rates"]:
        items = "".join(
            f'<div><dt>{k}</dt><span class="amt">{v.split(",")[0]}'
            + (f'<small> {v.split(",", 1)[1]}</small>' if "," in v else "")
            + "</span></div>" for k, v in a["rates"])
        rows.append(("Rates", f'<dl class="rates">{items}</dl>'))
    if a["studio"] or a["address"]:
        where = " &middot; ".join(x for x in (a["studio"], a["address"]) if x)
        sub = f'<span class="sub">{a["access"]}</span>' if a["access"] else ""
        rows.append(("Getting there", f"{where}{sub}"))
    if a["bio"]:
        rows.append(("Background", "".join(f"<p>{p}</p>" for p in a["bio"])))
    if a["wont"]:
        rows.append(("Won’t tattoo", a["wont"]))
    if a["languages"]:
        rows.append(("Languages", a["languages"]))
    if a["photo"]:
        rows.append(("At work", f'<span class="plate" style="background-image:{GRAIN},{WORKING}"></span>'))
    if a["spots"]:
        rows.append(("Guest spots", "".join(
            f'<p><b>{p}</b> &middot; {c}<br><span style="color:var(--muted)">{w}</span></p>'
            for w, p, c in a["spots"])))
    if a["aftercare"]:
        rows.append(("Aftercare", '<a class="link" href="#">How to look after a fresh '
                                  'tattoo</a><span class="sub">The same notes she sends '
                                  'after a session, here whenever you need them.</span>'))
    if a["licence"]:
        rows.append(("Licence", f'<span class="sub" style="margin:0">{a["licence"]}</span>'))

    led = "".join(f'<div class="row"><dt>{k}</dt><dd>{v}</dd></div>' for k, v in rows)
    want = ""
    if a["wish"]:
        want = ('<section class="want"><h2>Wants to tattoo more of</h2><ul>'
                + "".join(f"<li>{w}</li>" for w in a["wish"]) + "</ul></section>")
    links = ('<p class="links"><a href="#">Instagram</a><a href="#">TikTok</a></p>'
             if a["socials"] else "")
    return f"""<main class="wrap">
  <a class="back">&larr; <b>{a["name"]}</b></a>
  <h1 class="nm">{a["name"]}</h1>
  {f'<span class="pn">{a["pronouns"]}</span>' if a["pronouns"] else ""}
  {want}
  {f'<dl class="ledger">{led}</dl>' if rows else ""}
  {links}
  <a class="btn">Request a session</a>
</main>"""


def page(body):
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>about</title>
<style>{FONTS}{TOKENS}{CSS}</style></head><body>{body}</body></html>"""


FILES = {"af-full.html": page(render(FULL)), "af-sparse.html": page(render(SPARSE))}

FILES["gallery-af.html"] = f"""<!doctype html><html><head><meta charset="utf-8">
<title>About as a website replacement</title><style>
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
<h1>About as a website replacement — the ledger, extended (390)</h1>
<p class="note">Direction C carrying A's wishlist panel, plus the entries an artist's own site has
that Cake has nowhere for: <b>rates, getting there, how far out she is booked, what she won't
tattoo, languages, aftercare and her licence</b>. Policies and FAQs are not here — they already
exist as collapsible rows on the profile. The second frame is the same page from someone who
filled in almost none of it.</p>
<div class="row">
<figure><figcaption><b>Filled in</b><span>every entry set</span></figcaption>
<iframe src="af-full.html" width="390" height="2560" scrolling="no" loading="eager"></iframe></figure>
<figure><figcaption><b>Barely filled in</b><span>a name, a city, a year, one paragraph</span></figcaption>
<iframe src="af-sparse.html" width="390" height="820" scrolling="no" loading="eager"></iframe></figure>
</div></body></html>"""

for name, text in FILES.items():
    io.open(f"{OUT}/{name}", "w", encoding="utf-8").write(text)
print(f"wrote {len(FILES)} files")
