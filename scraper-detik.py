#!/usr/bin/env python3
"""
KOMPAS404 News Scraper - Fetches latest articles from detik.com
Run: python3 scraper-detik.py
"""
import requests
import re
import os
import json
from datetime import datetime

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "id-ID,id;q=0.9,en;q=0.8",
}

def get_latest_urls():
    """Fetch latest article URLs from detik.com berita index"""
    try:
        r = requests.get("https://news.detik.com/indeks", headers=HEADERS, timeout=15)
        html = r.text
    except Exception as e:
        print(f"Failed to fetch index: {e}")
        return []

    # Extract article URLs from detik.com berita section
    links = re.findall(r'href="(https://news\.detik\.com/berita/d-[0-9]+/[^"]+)"', html)
    # Deduplicate while preserving order
    seen, urls = set(), []
    for url in links:
        if url not in seen and "/film/" not in url and "/kultur/" not in url:
            seen.add(url)
            urls.append(url)
    return urls[:15]  # Get top 15 latest

def download_image(url, folder):
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        if r.status_code == 200:
            ext = url.split('?')[0].split('.')[-1]
            if ext not in ['jpg','jpeg','png','webp']: ext = 'jpg'
            fname = f"{folder}/img_{hash(url)}.{ext}"
            with open(fname,'wb') as f:
                f.write(r.content)
            return fname
    except: pass
    return None

def extract_article(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        html = r.text
    except Exception as e:
        return None

    # title
    m = re.search(r'<h1[^>]*>([^<]+)</h1>', html)
    if not m: return None
    title = m.group(1).strip()

    # image
    m = re.search(r'<meta property="og:image" content="([^"]+)"', html)
    img_url = m.group(1) if m else None

    # date
    m = re.search(r'<div[^>]*class="detail__date[^"]*"[^>]*>([^<]+)</div>', html)
    date_str = m.group(1).strip() if m else datetime.now().strftime("%d %b %Y %H:%M WIB")

    # content
    m = re.search(r'<div[^>]*class="detail__body[^"]*"[^>]*>(.*?)</div>\s*<div', html, re.S)
    if not m:
        m = re.search(r'<article[^>]*>(.*?)</article>', html, re.S)
    body = m.group(1) if m else ""

    paras = re.findall(r'<p[^>]*>(.*?)</p>', body, re.S)
    content = []
    for p in paras:
        clean = re.sub(r'<[^>]+>', '', p).strip()
        if len(clean) > 30 and "SCROLL" not in clean.upper() and "video" not in clean.lower():
            content.append(clean)

    return {"title": title, "img_url": img_url, "date": date_str, "content": content, "url": url}

def guess_category(title, content):
    t = (title + " ".join(content)).lower()
    if any(w in t for w in ['teknologi','ai','siber','digital','startup','aplikasi']): return "Teknologi"
    if any(w in t for w in ['bisnis','ekonomi','uang','investas','uang']): return "Bisnis"
    if any(w in t for w in ['sepakbola','liga','bola','pertandingan','atlet']): return "Olahraga"
    if any(w in t for w in ['hukum','polisi','kriminal','pencurian','pembunuhan']): return "Hukum"
    if any(w in t for w in ['lingkungan','hutan','karhutla','kebakaran']): return "Lingkungan"
    if any(w in t for w in ['krl','kereta','commuter','transportasi']): return "Transportasi"
    return "Berita"

print("Fetching latest article URLs from detik.com...")
urls = get_latest_urls()
print(f"Found {len(urls)} article URLs")

articles = []
for url in urls:
    print(f"Scraping: {url[:80]}")
    data = extract_article(url)
    if data and data["content"] and len(data["content"]) >= 3:
        slug = re.sub(r'[^a-z0-9]+', '-', data["title"].lower())[:60]
        slug = re.sub(r'-+', '-', slug).strip('-')
        # avoid duplicate slugs
        existing = [a["slug"] for a in articles]
        if slug in existing:
            slug = f"{slug}-detik"
        print(f"  OK -> {data['title'][:60]} | img: {bool(data['img_url'])} | paras: {len(data['content'])}")
        articles.append({
            "slug": slug,
            "title": data["title"],
            "date": data["date"],
            "image": data["img_url"],
            "image_alt": data["title"][:50],
            "content": '\n'.join([f'<p>{p}</p>' for p in data['content']]),
            "category": guess_category(data["title"], data["content"]),
            "breadcrumb": data["title"][:30],
        })

print(f"\nTotal: {len(articles)} articles scraped")
with open("scraped-detik.json","w",encoding="utf-8") as f:
    json.dump(articles, f, ensure_ascii=False, indent=2)
print("Saved to scraped-detik.json")

def guess_category(title, content):
    t = (title + " ".join(content)).lower()
    if any(w in t for w in ['teknologi','ai','siber','digital','startup','aplikasi']): return "Teknologi"
    if any(w in t for w in ['bisnis','ekonomi','uang','investas','uang']): return "Bisnis"
    if any(w in t for w in ['sepakbola','liga','bola','pertandingan','atlet']): return "Olahraga"
    if any(w in t for w in ['hukum','polisi','kriminal','pencurian','pembunuhan']): return "Hukum"
    if any(w in t for w in ['lingkungan','hutan','karhutla','kebakaran']): return "Lingkungan"
    if any(w in t for w in ['krl','kereta','commuter','transportasi']): return "Transportasi"
    return "Berita"