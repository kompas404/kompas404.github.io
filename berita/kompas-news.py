#!/usr/bin/env python3
"""Scrape Kompas headlines via Google News RSS."""
import feedparser
import json
import sys
from datetime import datetime

URL = "https://news.google.com/rss/search?q=site:kompas.com&hl=id&gl=ID&ceid=ID:id"

def fetch(limit=20):
    feed = feedparser.parse(URL)
    if feed.bozo and not feed.entries:
        print(f"[!] Feed parse error: {feed.bozo_exception}", file=sys.stderr)
        return None
    items = []
    for e in feed.entries[:limit]:
        items.append({
            "title": e.title,
            "link": e.link,
            "published": e.get("published", ""),
            "source": e.get("source", {}).get("title", "kompas.com"),
            "summary": e.get("summary", ""),
        })
    return items

def main():
    items = fetch(limit=30)
    if not items:
        sys.exit(1)
    out = {
        "scraped_at": datetime.now().isoformat(timespec="seconds"),
        "source_feed": "Google News RSS (site:kompas.com)",
        "count": len(items),
        "headlines": items,
    }
    out_path = "C:/Users/ideapad gaming 3/kompas404-seo/berita/kompas-headlines.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"[OK] {len(items)} headlines saved -> {out_path}")
    for i, it in enumerate(items, 1):
        print(f"{i:2}. {it['title'][:90]}")

if __name__ == "__main__":
    main()
