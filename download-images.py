#!/usr/bin/env python3
"""
KOMPAS404 Image Downloader - Fast Wikimedia Version
Uses Wikipedia/Wikimedia API to find contextually relevant free images.
No API key needed, no watermark, fully free to use.
"""
import json, os, requests, re
from urllib.parse import quote, urlparse

BASE = os.path.expanduser(r"C:\Users\ideapad gaming 3\kompas404-seo")
IMG_DIR = os.path.join(BASE, "images")
os.makedirs(IMG_DIR, exist_ok=True)

H = {"User-Agent": "KOMPAS404-Bot/1.0 (contact: admin@kompas404.my.id)"}

def get_wiki_image(keywords, title, timeout=8):
    """Get a relevant image from Wikipedia/Wikimedia given keywords"""
    # Try Wikipedia pageimages first (fastest)
    try:
        search_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={quote(keywords)}&srlimit=3&format=json"
        r = requests.get(search_url, headers=H, timeout=timeout)
        pages = r.json().get("query", {}).get("search", [])
        if not pages:
            return None

        for page in pages[:2]:
            page_title = page["title"]
            img_url = f"https://en.wikipedia.org/w/api.php?action=query&titles={quote(page_title)}&prop=pageimages&piprop=thumbnail&pithumbsize=800&format=json"
            r2 = requests.get(img_url, headers=H, timeout=timeout)
            data = r2.json()
            pages_data = data.get("query", {}).get("pages", {})
            for pid, pdata in pages_data.items():
                thumb = pdata.get("thumbnail", {})
                if thumb:
                    src = thumb.get("source", "")
                    if src and "upload.wikimedia.org" in src:
                        return src
    except:
        pass
    return None

def download(url, path):
    """Download image, return size or None"""
    try:
        r = requests.get(url, headers=H, timeout=15)
        if r.status_code == 200 and len(r.content) > 5000:
            ext = os.path.splitext(urlparse(url).path)[1] or ".jpg"
            if ext.lower() not in [".jpg", ".jpeg", ".png", ".webp"]:
                ext = ".jpg"
            if not path.lower().endswith(ext.lower()):
                path = path.rsplit(".", 1)[0] + ext
            with open(path, "wb") as f:
                f.write(r.content)
            return len(r.content)
    except:
        pass
    return None

def keywords_from_title(title):
    """Extract search keywords from article title"""
    stopwords = {
        'di','dan','yang','untuk','dari','dengan','ini','itu','akan','sudah',
        'ada','tidak','juga','lebih','atau','oleh','jadi','dalam','tersebut',
        'secara','sejak','pada','saat','setelah','sebelum','hingga','bahwa',
        'karena','namun','tetapi','lagi','bisa','harus','dapat','perlu',
        'kompas404','berita','terbaru','hari','jakarta','indonesia','update',
        'news','foto','gambar','2026','2025','2024'
    }
    words = re.sub(r'[^\w\s]', ' ', title).split()
    kw = [w for w in words if w.lower() not in stopwords and len(w) > 2]
    return ' '.join(kw[:5])

with open(os.path.join(BASE, "new-articles.json"), "r", encoding="utf-8") as f:
    arts = json.load(f)

local_images = {}
ok_count = 0

for a in arts:
    title = a["title"]
    slug_raw = a["slug"].replace("berita/", "")
    kw = keywords_from_title(title)

    print(f"[{ok_count}/{len(arts)}] {title[:55]}... | kw={kw[:40]}", end=" -> ")

    img_url = get_wiki_image(kw, title)
    if not img_url:
        # Try shorter keywords
        img_url = get_wiki_image(' '.join(kw.split()[:3]), title)

    if img_url:
        slug_key = slug_raw[:42].replace("/", "-").replace(" ", "-")
        fname = f"art_{slug_key}.jpg"
        fpath = os.path.join(IMG_DIR, fname)
        size = download(img_url, fpath)
        if size and size > 8000:
            local_images[a["slug"]] = f"images/{fname}"
            ok_count += 1
            print(f"OK {fname} ({size//1024}KB)")
        else:
            print("FAIL small")
    else:
        print("FAIL no image")

print(f"\nDownloaded {ok_count}/{len(arts)} images")

# Save map (only downloaded ones - build-articles.py falls back to original URL)
with open(os.path.join(BASE, "image-map.json"), "w", encoding="utf-8") as f:
    json.dump(local_images, f, ensure_ascii=False, indent=2)
print(f"Saved image-map.json ({len(local_images)} entries)")