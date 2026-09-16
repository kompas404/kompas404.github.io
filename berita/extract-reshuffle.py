#!/usr/bin/env python3
"""Extract full article content from RSS items by following each link."""
import feedparser
import json
import re
import sys
from datetime import datetime
from urllib.parse import urlparse, parse_qs

import requests
from bs4 import BeautifulSoup

RSS_URL = "https://news.google.com/rss/search?q=site:kompas.com+reshuffle+menkeu+purbaya+suahasil&hl=id&gl=ID&ceid=ID:id"
OUT_PATH = "C:/Users/ideapad gaming 3/kompas404-seo/berita/reshuffle-menkeu-articles.json"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"

def get_real_url(google_news_url):
    try:
        r = requests.get(google_news_url, allow_redirects=True, timeout=20, headers={"User-Agent": UA})
        return r.url
    except Exception:
        return google_news_url

def extract_article(url, title=""):
    try:
        r = requests.get(url, timeout=20, headers={"User-Agent": UA, "Accept-Language": "id,en;q=0.9"})
        r.raise_for_status()
    except Exception as e:
        return {"title": title, "url": url, "error": str(e), "body": ""}
    soup = BeautifulSoup(r.text, "html.parser")
    for tag in soup(["script", "style", "nav", "aside", "footer", "header", "noscript", "iframe"]):
        tag.decompose()
    # Kompas-specific: article paragraphs often live in .read__content p
    candidates = [
        soup.select("div.read__content p"),
        soup.select("article p"),
        soup.select("div.article-content p"),
        soup.select("div#content p"),
        soup.select("div.content p"),
    ]
    paragraphs = []
    seen = set()
    for group in candidates:
        for p in group:
            txt = p.get_text(" ", strip=True)
            if txt and len(txt) > 30 and txt not in seen:
                seen.add(txt)
                paragraphs.append(txt)
        if paragraphs:
            break
    body = "\n\n".join(paragraphs)
    if not body:
        body = soup.get_text("\n", strip=True)[:3000]
    real_title = ""
    if soup.title and soup.title.string:
        real_title = soup.title.string.strip()
    return {
        "title_google": title,
        "title_real": real_title,
        "url": url,
        "body": body,
        "word_count": len(body.split()),
    }

def main():
    feed = feedparser.parse(RSS_URL)
    items = []
    seen_urls = set()
    for e in feed.entries:
        link = e.link
        real = get_real_url(link)
        if real in seen_urls:
            continue
        seen_urls.add(real)
        items.append((real, e.title, e.get("published", "")))
    print(f"[i] Resolved {len(items)} unique URLs from RSS")

    out = {
        "scraped_at": datetime.now().isoformat(timespec="seconds"),
        "query": "reshuffle menkeu purbaya suahasil",
        "articles": [],
    }
    for i, (url, title, pub) in enumerate(items, 1):
        print(f"[{i}/{len(items)}] {title[:70]}...")
        art = extract_article(url, title)
        art["published"] = pub
        out["articles"].append(art)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"\n[OK] Saved {len(out['articles'])} articles -> {OUT_PATH}")

if __name__ == "__main__":
    main()
