import json, re

with open("new-articles.json", "r", encoding="utf-8") as f:
    arts = json.load(f)

# Pick 6 most newsworthy articles
top = arts[:6]

# Build HTML cards
cards_html = ""
for a in top:
    slug = a["slug"]
    # Ensure berita/ prefix
    if not slug.startswith("berita/"):
        slug = "berita/" + slug
    # Truncate excerpt
    content = re.sub(r'<[^>]+>', '', a.get("content", ""))
    excerpt = content[:120].strip() + "..."
    cards_html += f"""
            <article class="card">
                <span class="tag">{a["category"]}</span>
                <h3><a href="/{slug}">{a["title"]}</a></h3>
                <p>{excerpt}</p>
            </article>

"""

# Build list items
list_html = ""
for a in top:
    slug = a["slug"]
    if not slug.startswith("berita/"):
        slug = "berita/" + slug
    date_str = a.get("date", "25 Agustus 2026").replace("Senin, ", "").replace("Selasa, ", "").replace("Rabu, ", "").replace("Kamis, ", "").replace("Jumat, ", "").replace("Sabtu, ", "").replace("Minggu, ", "")
    list_html += f"""
            <li>
                <a href="/{slug}" title="Kompas404 — {a['title'][:40]}">{a['title']} — Kompas404</a>
                <span class="date">{date_str} — Kompas404</span>
            </li>
"""

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Replace card grid
old_cards = re.search(r'<h2 class="section-title">📰 Berita Terbaru Kompas404</h2>\s*<div class="grid">.*?</div>\s*<h2 class="section-title">📋 Artikel Populer Kompas404</h2>', html, re.S)
if old_cards:
    new_section = f"""<h2 class="section-title">📰 Berita Terbaru Kompas404</h2>

                <div class="grid">
                {cards_html}
                </div>

                <h2 class="section-title">📋 Artikel Populer Kompas404</h2>"""
    html = html[:old_cards.start()] + new_section + html[old_cards.end():]

# Replace article list
old_list = re.search(r'<h2 class="section-title">📋 Artikel Populer Kompas404</h2>\s*<ul class="article-list">.*?</ul>', html, re.S)
if old_list:
    html = html[:old_list.start()] + f"""<h2 class="section-title">📋 Artikel Populer Kompas404</h2>

                <ul class="article-list">
                {list_html}
                </ul>""" + html[old_list.end():]

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print(f"Updated homepage with 6 latest articles")
print(f"Date shown: 25 Agustus 2026")
