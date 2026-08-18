#!/usr/bin/env python3
"""
KOMPAS404 Auto News Generator
Scrapes trending news from Google News Indonesia RSS,
generates article pages, rebuilds all site pages.
"""
import os, sys, json, hashlib, datetime, random
from pathlib import Path

try:
    import feedparser
except ImportError:
    print("ERROR: feedparser not installed. Run: pip install feedparser")
    sys.exit(1)

BASE = Path(os.environ.get("GITHUB_WORKSPACE", os.path.expanduser("~/kompas404-seo")))
ARTICLES_DB = BASE / "articles-db.json"

topics = [
    ("Teknologi", "https://news.google.com/rss/search?q=teknologi+indonesia&hl=id&gl=ID&ceid=ID:id"),
    ("Bisnis", "https://news.google.com/rss/search?q=bisnis+ekonomi+indonesia&hl=id&gl=ID&ceid=ID:id"),
    ("Olahraga", "https://news.google.com/rss/search?q=olahraga+sepakbola+indonesia&hl=id&gl=ID&ceid=ID:id"),
]

unsplash_images = {
    "Teknologi": [
        ("https://images.unsplash.com/photo-1518770660439-4636190af475?w=800&q=80", "Technology Circuit"),
        ("https://images.unsplash.com/photo-1488590528505-98d2b5aba04b?w=800&q=80", "Code on Screen"),
        ("https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=800&q=80", "Digital Globe"),
    ],
    "Bisnis": [
        ("https://images.unsplash.com/photo-1507679799987-c73779587ccf?w=800&q=80", "Business Professional"),
        ("https://images.unsplash.com/photo-1444653614773-995cb1ef9efa?w=800&q=80", "Financial Chart"),
    ],
    "Olahraga": [
        ("https://images.unsplash.com/photo-1461896836934-bd45ba05cf21?w=800&q=80", "Stadium"),
        ("https://images.unsplash.com/photo-1517649763962-0c623066013b?w=800&q=80", "Sports Action"),
    ],
}

def slugify(text):
    return text.lower().replace(' ', '-').replace('.', '').replace(',', '')[:60]

def load_db():
    if ARTICLES_DB.exists():
        return json.loads(ARTICLES_DB.read_text())
    return {"articles": {}, "seen_urls": []}

def save_db(db):
    ARTICLES_DB.parent.mkdir(parents=True, exist_ok=True)
    ARTICLES_DB.write_text(json.dumps(db, indent=2, ensure_ascii=False))

def fetch_news():
    db = load_db()
    new_articles = []

    for category, url in topics:
        try:
            feed = feedparser.parse(url)
            entries = feed.entries[:3]  # Max 3 per topic per run
            for entry in entries:
                if entry.link in db["seen_urls"]:
                    continue

                title = entry.title.split(' - ')[0].strip()
                if len(title) < 15 or len(title) > 120:
                    continue

                slug = slugify(title)
                slug_hash = hashlib.md5(entry.link.encode()).hexdigest()[:8]
                article_slug = f"{slug}-{slug_hash}"

                # Get image
                imgs = unsplash_images.get(category, unsplash_images["Teknologi"])
                img_url, img_alt = random.choice(imgs)

                # Build content
                summary = entry.get("summary", entry.get("description", ""))
                # Clean HTML
                import re
                summary = re.sub(r'<[^>]+>', ' ', summary)[:300].strip()
                if not summary:
                    summary = title

                paragraph = f"<p>KOMPAS404 - {summary}</p>"

                article_data = {
                    "slug": f"berita/{article_slug}",
                    "category": category,
                    "breadcrumb": title[:50],
                    "title": title,
                    "date": datetime.date.today().strftime("%d %B %Y"),
                    "image": img_url,
                    "image_alt": img_alt,
                    "content": paragraph,
                    "source_url": entry.link,
                }

                db["articles"][f"berita/{article_slug}"] = article_data
                db["seen_urls"].append(entry.link)
                new_articles.append(article_data)
                print(f"NEW: {category} -> {title}")

        except Exception as e:
            print(f"ERROR fetching {category}: {e}")

    # Keep only last 500 URLs
    if len(db["seen_urls"]) > 500:
        db["seen_urls"] = db["seen_urls"][-500:]

    save_db(db)
    return new_articles

def main():
    print(f"KOMPAS404 News Generator — {datetime.datetime.now()}")
    print(f"Workspace: {BASE}")

    new_articles = fetch_news()

    if not new_articles:
        print("Tidak ada artikel baru. Skip.")
        return

    print(f"\n{len(new_articles)} artikel baru ditemukan.")

    # Run build script
    build_script = BASE / "build-articles.py"
    if not build_script.exists():
        print("ERROR: build-articles.py not found!")
        return

    # Inject new articles into the build script's articles dict
    # This is a simple approach: write the new articles to a JSON file that build-articles reads
    new_articles_file = BASE / "new-articles.json"
    new_articles_file.write_text(json.dumps(new_articles, indent=2, ensure_ascii=False))

    # Run build
    import subprocess
    result = subprocess.run([sys.executable, str(build_script)], capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr)
        sys.exit(1)

    print("DONE - Semua halaman terupdate")

if __name__ == "__main__":
    main()
