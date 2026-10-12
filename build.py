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
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "src"
OUT = ROOT / "site"

NAV = [
    ("classes", "classes.html", "earth", "Classes"),
    ("schedule", "schedule.html", "sun", "Schedule"),
    ("coaches", "coaches.html", "air", "Coaches"),
    ("four7", "four7.html", "fire", "Four7"),
    ("coaching", "coaching.html", "water", "1-on-1"),
]


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


def main():
    layout = (SRC / "layout.html").read_text()
    for page in sorted((SRC / "pages").glob("*.html")):
        meta, body = parse(page.read_text())
        title = "Alchemy MMA" if page.stem == "index" else f"{meta['title']} | Alchemy MMA"
        html = (
            layout.replace("{{title}}", title)
            .replace("{{description}}", meta.get("description", ""))
            .replace("{{nav}}", nav_links(meta.get("nav", "")))
            .replace("{{body}}", body)
        )
        (OUT / page.name).write_text(html)
        print("built", page.name)


if __name__ == "__main__":
    main()
