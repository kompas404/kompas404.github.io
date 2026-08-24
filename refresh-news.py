import json, re, os

with open("scraped-detik.json", "r", encoding="utf-8") as f:
    raw = json.load(f)

new_articles = []
for a in raw:
    # clean content - remove junk text
    content = a["content"]
    content = re.sub(r'SCROLL TO CONTINUE WITH CONTENT', '', content)
    content = re.sub(r'Lihat juga Video[^<]+<a[^>]+>[^<]+</a>', '', content)
    content = re.sub(r'<p>\s*</p>', '', content)
    content = re.sub(r'\s+', ' ', content).strip()
    
    slug = a["slug"]
    # fix duplicate slug collision
    existing = [x["slug"] for x in new_articles]
    if slug in existing:
        slug = slug + "-2"
    
    new_articles.append({
        "slug": slug,
        "title": a["title"],
        "category": a["category"],
        "breadcrumb": a["breadcrumb"],
        "date": a["date"],
        "image": a["image"],
        "image_alt": a["image_alt"],
        "content": content
    })

with open("new-articles.json", "w", encoding="utf-8") as f:
    json.dump(new_articles, f, ensure_ascii=False, indent=2)

print(f"Prepared {len(new_articles)} articles in new-articles.json")
