import os, json, re

BASE = r"C:\Users\ideapad gaming 3\kompas404-seo"
berita_dir = os.path.join(BASE, "berita")

# Load freshly scraped articles (detik) -- these have full data incl. image
scraped = []
scraped_path = os.path.join(BASE, "scraped-detik.json")
if os.path.exists(scraped_path):
    with open(scraped_path, "r", encoding="utf-8") as f:
        scraped = json.load(f)

def entry_with_image(e):
    """Ensure an article entry always has an 'image' key."""
    if "image" not in e or not e.get("image"):
        e["image"] = "https://kompas404.github.io/images/icon-kompas404.png"
    return e

# Start with scraped (newest) first
all_articles = []
seen_slugs = set()
for a in scraped:
    slug = a.get("slug", "")
    if not slug.startswith("berita/"):
        slug = "berita/" + slug
    if slug in seen_slugs:
        continue
    seen_slugs.add(slug)
    e = {
        "slug": slug,
        "title": a.get("title", ""),
        "category": a.get("category", "Berita"),
        "breadcrumb": a.get("breadcrumb") or a.get("title", "")[:30],
        "date": a.get("date", ""),
        "image": a.get("image", ""),
        "image_alt": a.get("image_alt") or a.get("title", "")[:50],
        "content": a.get("content", ""),
    }
    all_articles.append(entry_with_image(e))

# Load previous new-articles.json (so existing/local/legacy articles survive)
prev_path = os.path.join(BASE, "new-articles.json")
if os.path.exists(prev_path):
    try:
        with open(prev_path, "r", encoding="utf-8") as f:
            prev = json.load(f)
        for a in prev:
            slug = a.get("slug", "")
            if not slug.startswith("berita/"):
                slug = "berita/" + slug
            if slug in seen_slugs:
                continue
            seen_slugs.add(slug)
            e = {
                "slug": slug,
                "title": a.get("title", ""),
                "category": a.get("category", "Berita"),
                "breadcrumb": a.get("breadcrumb") or a.get("title", "")[:30],
                "date": a.get("date", ""),
                "image": a.get("image", ""),
                "image_alt": a.get("image_alt") or a.get("title", "")[:50],
                "content": a.get("content", ""),
            }
            all_articles.append(entry_with_image(e))
    except Exception as ex:
        print(f"Warn: previous new-articles.json unreadable: {ex}")

# Scan folders for any article never registered (safety net)
for folder in sorted(os.listdir(berita_dir)):
    folder_path = os.path.join(berita_dir, folder)
    if not os.path.isdir(folder_path):
        continue
    idx = os.path.join(folder_path, "index.html")
    if not os.path.exists(idx):
        continue
    slug = f"berita/{folder}"
    if slug in seen_slugs:
        continue
    try:
        with open(idx, "r", encoding="utf-8") as f:
            html = f.read()
        m = re.search(r'<meta property="og:title" content="([^"]+?)(?:\s*[—\-]\s*Kompas404)?"', html)
        title = m.group(1).strip() if m else folder.replace("-", " ").title()
        m = re.search(r'<span>([^<]+)</span>\s*([^<]+)', html)
        if m:
            category = m.group(1).strip()
            date = m.group(2).strip()
        else:
            category = "Umum"
            date = "Agustus 2026"
        m = re.search(r'<p>([^<]{50,200})', html)
        excerpt = m.group(1)[:150] if m else title
        seen_slugs.add(slug)
        all_articles.append({
            "slug": slug,
            "title": title,
            "category": category,
            "date": date,
            "breadcrumb": title[:30],
            "image": "https://kompas404.github.io/images/icon-kompas404.png",
            "image_alt": title,
            "content": excerpt,
        })
    except Exception as e:
        print(f"Skip {folder}: {e}")

# Sort by date desc (newest first) -- best-effort parse of Indonesian dates
def _date_key(a):
    d = a.get("date", "")
    m = re.search(r'(\d{1,2})\s+(\w+)\s+(\d{4})\s+(\d{1,2}):(\d{2})', d)
    if m:
        dd, mon, y, hh, mm = m.groups()
        months = {"Jan":1,"Feb":2,"Mar":3,"Apr":4,"Mei":5,"May":5,"Jun":6,"Jul":7,"Agu":8,"Aug":8,"Sep":9,"Okt":10,"Oct":10,"Nov":11,"Des":12,"Dec":12}
        return (int(y), months.get(mon[:3], 1), int(dd), int(hh), int(mm))
    # fallback: date without time
    m = re.search(r'(\d{1,2})\s+(\w+)\s+(\d{4})', d)
    if m:
        dd, mon, y = m.groups()
        months = {"Jan":1,"Feb":2,"Mar":3,"Apr":4,"Mei":5,"May":5,"Jun":6,"Jul":7,"Agu":8,"Aug":8,"Sep":9,"Okt":10,"Oct":10,"Nov":11,"Des":12,"Dec":12}
        return (int(y), months.get(mon[:3], 1), int(dd), 0, 0)
    return (0, 0, 0, 0, 0)

all_articles.sort(key=_date_key, reverse=True)

print(f"Total articles collected: {len(all_articles)}")

with open(os.path.join(BASE, "new-articles.json"), "w", encoding="utf-8") as f:
    json.dump(all_articles, f, ensure_ascii=False, indent=2)

print("Saved new-articles.json with all articles (newest first, all with image)")
