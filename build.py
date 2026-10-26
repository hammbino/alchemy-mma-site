"""Build the static site.

Each file in src/pages/ starts with a front-matter block:

    ---
    title: Classes
    nav: classes
    description: One sentence for search results.
    ---
    <main>...</main>

The body is wrapped in src/layout.html and written to site/<same name>.
Run: python3 build.py
"""
import hashlib
import html
import re
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "src"
OUT = ROOT / "site"

# Each page is marked by one shape from the logo, in the menu and on the page heading.
NAV = [
    ("classes", "classes.html", "earth", "Classes"),
    ("schedule", "schedule.html", "orb", "Schedule"),
    ("coaches", "coaches.html", "air", "Coaches"),
    ("four7", "four7.html", "triangle", "Four7"),
    ("coaching", "coaching.html", "water", "1-on-1"),
    ("groups", "groups.html", "group", "Groups"),
    ("pricing", "pricing.html", "ascent", "Pricing"),
    ("about", "about.html", "circle", "About"),
]

# The shop is a preview until Brian has a Utah sales tax license.
# Set this to False before the domain switch if the license hasn't come through:
# the Shop link comes out of the menu and shop.html is not published.
SHOW_SHOP = True
if SHOW_SHOP:
    NAV.insert(-1, ("shop", "shop.html", "sun", "Shop"))


# Addresses from the old Gymdesk-built site, so saved links and search results still land somewhere.
# Each becomes a tiny page at site/<path>.html that forwards to the target.
GYMDESK = "https://alchemy-mma.gymdesk.com/"
REDIRECTS = {
    "login": GYMDESK + "login",
    "signup": GYMDESK + "signup",
    "contact": "index.html#contact",
    "instructors": "coaches.html",
    "instructors/bio/id/68968": "coaches.html#brian",
    "instructors/bio/id/74699": "coaches.html#rad",
    "page/AboutUs": "about.html",
    "page/Future Programs": "classes.html",
    "page/what-we-teach-goes-beyond-the-mats": "about.html",
}


def write_redirects():
    for path, target in REDIRECTS.items():
        if not target.startswith("http"):
            target = "../" * path.count("/") + target
        out = OUT / f"{path}.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(
            f'<!doctype html><meta charset="utf-8"><title>Alchemy MMA</title>'
            f'<meta http-equiv="refresh" content="0; url={target}">'
            f'<link rel="canonical" href="{target}">'
            f'<p>This page has moved. <a href="{target}">Continue to Alchemy MMA</a>.</p>\n'
        )
    print("wrote", len(REDIRECTS), "redirects")


def parse(text):
    _, head, body = text.split("---", 2)
    meta = {}
    for line in head.strip().splitlines():
        key, _, value = line.partition(":")
        meta[key.strip()] = value.strip()
    return meta, body.strip()


def nav_links(active):
    items = []
    for key, href, glyph, label in NAV:
        current = ' aria-current="page"' if key == active else ""
        items.append(
            f'<li><a href="{href}"{current}><svg class="glyph"><use href="#g-{glyph}"/></svg>{label}</a></li>'
        )
    return "\n      ".join(items)


ASK = re.compile(r'<([a-z0-9]+)\b([^>]*?)\sdata-ask="([^"]*)"')
PAGE_ORDER = ["index"] + [href[:-5] for _, href, _, _ in NAV]

# Things Brian is still following up on. They are not marked on the pages.
FOLLOW_UPS = [
    "Micah's updated photo and complete biography",
    "Final family discount percentages",
    "Private training pricing and coach availability",
    "Jason's final feedback on the Four7 System and its history",
    "Any additional photos for the About and coaching pages (Meet the owners uses Brian's Facebook profile photo for now)",
    "An Alchemy MMA Facebook page, when there is one (the footer links to Brian's profile for now)",
    "Product details and the Utah sales tax license number for the shop",
]

# The pink banner shows only while the draft still has open questions.
REVIEW_BAR = """<div class="review-bar" role="note">
  <span>Draft for review. <a href="review.html">{n} questions for Brian</a> are outlined in pink.</span>
  <button type="button" class="review-toggle" aria-pressed="false">Hide markers</button>
</div>
"""


def number_asks(stem, body, asks):
    """Give every data-ask element a number and an anchor, and collect it for the review list."""

    def tag(m):
        name, attrs, question = m.groups()
        n = len(asks) + 1
        anchor = re.search(r'\sid="([^"]+)"', attrs)
        anchor = anchor.group(1) if anchor else f"ask-{n}"
        extra = "" if f'id="{anchor}"' in attrs else f' id="{anchor}"'
        asks.append((n, stem, anchor, html.unescape(question)))
        return f'<{name}{attrs}{extra} data-n="{n}" data-ask="{question}"'

    return ASK.sub(tag, body)


def version(name):
    """Short content hash, so browsers fetch the file again whenever it changes."""
    return hashlib.sha1((OUT / name).read_bytes()).hexdigest()[:8]


def render(layout, stem, meta, body, total):
    title = "Alchemy MMA" if stem == "index" else f"{meta['title']} | Alchemy MMA"
    return (
        layout.replace("{{title}}", title)
        .replace("{{description}}", meta.get("description", ""))
        .replace("{{nav}}", nav_links(meta.get("nav", "")))
        .replace("{{review_bar}}", REVIEW_BAR.format(n=total) if total else "")
        .replace("{{css_v}}", version("styles.css"))
        .replace("{{js_v}}", version("main.js"))
        .replace("{{body}}", body)
    )


def review_page(asks):
    """A single page listing every question for Brian, linked to where it sits on the site."""
    titles = {"index": "Home"}
    for key, href, _, label in NAV:
        titles[href[:-5]] = label
    groups = []
    for stem in PAGE_ORDER:
        items = [a for a in asks if a[1] == stem]
        if not items:
            continue
        rows = "\n".join(
            f'        <li><span class="ask-n">{n}</span><p>{html.escape(q)}</p>'
            f'<a href="{stem}.html#{anchor}">See it on the page</a></li>'
            for n, _, anchor, q in items
        )
        groups.append(f"    <h2>{titles[stem]}</h2>\n    <ol class=\"ask-list\">\n{rows}\n    </ol>")
    body = (
        '<main id="main">\n<header class="page-head"><div class="wrap">\n'
        f"  <h1>Questions for Brian</h1>\n  <p>{len(asks)} spots on the site need Brian to confirm or fill in a detail. "
        "Each one is outlined in pink with its number on the page.</p>\n</div></header>\n"
        '<section class="panel vellum"><div class="wrap review">\n'
        + "\n".join(groups)
        + '\n    <h2>Brian is following up on</h2>\n    <ul class="learn photo-asks">\n'
        + "".join(f"      <li>{html.escape(f)}</li>\n" for f in FOLLOW_UPS)
        + "    </ul>\n</div></section>\n</main>"
    )
    return body


def main():
    layout = (SRC / "layout.html").read_text()
    pages = {p.stem: parse(p.read_text()) for p in (SRC / "pages").glob("*.html")}
    if not SHOW_SHOP:
        pages.pop("shop", None)
        (OUT / "shop.html").unlink(missing_ok=True)
        print("shop hidden: shop.html left out")
    asks = []
    numbered = {}
    for stem in PAGE_ORDER:
        meta, body = pages[stem]
        numbered[stem] = (meta, number_asks(stem, body, asks))
    for stem, (meta, body) in numbered.items():
        (OUT / f"{stem}.html").write_text(render(layout, stem, meta, body, len(asks)))
        print("built", f"{stem}.html")
    write_redirects()

    review = OUT / "review.html"
    if asks:
        review_meta = {"title": "Questions for Brian", "description": "Review list for the Alchemy MMA site draft."}
        review.write_text(render(layout, "review", review_meta, review_page(asks), len(asks)))
        print("built review.html with", len(asks), "questions")
    else:
        review.unlink(missing_ok=True)
        print("no open questions: review bar and review.html left out")

    lines = ["# Questions for Brian", "", "Generated by build.py from the pink-outlined spots on the site. "
             "Each number matches the label on the page.", ""]
    if not asks:
        lines.append("No open questions on the site right now.\n")
    for stem in PAGE_ORDER:
        items = [a for a in asks if a[1] == stem]
        if items:
            lines.append(f"## {stem}.html")
            lines += [f"{n}. {q}" for n, _, _, q in items]
            lines.append("")
    lines += ["## Brian is following up on"] + [f"- {f}" for f in FOLLOW_UPS] + [""]
    (ROOT / "FOR-BRIAN.md").write_text("\n".join(lines))


if __name__ == "__main__":
    main()
