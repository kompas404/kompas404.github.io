#!/usr/bin/env python3
"""
KOMPAS404 Wikimedia Image Resolver v2
- Coba Wikipedia pageimages (keyword)
- Fallback: Wikimedia Commons category/API search (bebas lisensi)
- Fallback 2: Pexels/Unsplash source (free license) - safe fallback di luar Wikimedia
Semua gambar yang dihasilkan bebas hak cipta (free license).
"""
import json, os, re, time, random
import requests
from urllib.parse import quote, urlparse

BASE = os.environ.get("GITHUB_WORKSPACE", os.path.expanduser(r"C:\Users\ideapad gaming 3\kompas404-seo"))
IMG_DIR = os.path.join(BASE, "images")
os.makedirs(IMG_DIR, exist_ok=True)

H = {
    "User-Agent": "KOMPAS404-Bot/1.0 (contact: admin@kompas404.my.id)",
    "Accept": "application/json",
}

STOPWORDS = {
    'di','dan','yang','untuk','dari','dengan','ini','itu','akan','sudah',
    'ada','tidak','juga','lebih','atau','oleh','jadi','dalam','tersebut',
    'secara','sejak','pada','saat','setelah','sebelum','hingga','bahwa',
    'karena','namun','tetapi','lagi','bisa','harus','dapat','perlu',
    'kompas404','berita','terbaru','hari','jakarta','indonesia','update',
    'news','foto','gambar','2026','2025','2024','wib','polisi','tersangka',
    'kasus','ungkap','sebut','bongkar','dugaan','diam','sudah','selayaknya',
    'diapresiasi','sempat','viral','buka','palsu','diduga','targetkan',
    'orang','penumpang','korban','yang','hilang','di','laut','jawa','masi',
}

def keywords_from_title(title):
    words = re.sub(r'[^\w\s]', ' ', title).split()
    kw = [w for w in words if w.lower() not in STOPWORDS and len(w) > 2]
    return ' '.join(kw[:6])

def wiki_pageimage(keywords, timeout=8):
    try:
        url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={quote(keywords)}&srlimit=3&format=json"
        r = requests.get(url, headers=H, timeout=timeout)
        pages = r.json().get("query", {}).get("search", [])
        for page in pages[:2]:
            pt = page["title"]
            u2 = f"https://en.wikipedia.org/w/api.php?action=query&titles={quote(pt)}&prop=pageimages&piprop=thumbnail&pithumbsize=800&format=json"
            r2 = requests.get(u2, headers=H, timeout=timeout)
            for pid, pdata in r2.json().get("query", {}).get("pages", {}).items():
                thumb = pdata.get("thumbnail", {})
                src = thumb.get("source", "")
                if src and "upload.wikimedia.org" in src:
                    return src
    except Exception:
        pass
    return None

def commons_search(keywords, timeout=8):
    """Search Wikimedia Commons for free images."""
    try:
        url = f"https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrsearch={quote(keywords)}&gsrnamespace=6&gsrlimit=5&prop=imageinfo&iiprop=url&iiurlwidth=800&format=json"
        r = requests.get(url, headers=H, timeout=timeout)
        data = r.json()
        pages = data.get("query", {}).get("pages", {})
        if pages:
            # pick first with a thumbnail URL
            for pid in sorted(pages.keys(), key=lambda x: int(x)):
                ii = pages[pid].get("imageinfo", [])
                if ii and ii[0].get("thumburl"):
                    return ii[0]["thumburl"]
    except Exception:
        pass
    return None

def pexels_source(keywords, timeout=10):
    """Pexels public source images (free to use) - like source.unsplash.com but reliable."""
    try:
        # Use picsum for generic (Lorem Picsum - free, no attribution required)
        # but better: try pexels CDN known-good IDs for common topics
        r = requests.get(f"https://picsum.photos/seed/{quote(keywords[:20])}/800/500", headers={"User-Agent": "Mozilla/5.0"}, timeout=timeout, allow_redirects=True)
        if r.status_code == 200 and len(r.content) > 8000:
            return r.url
    except Exception:
        pass
    return None

def download(url, path):
    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=20, stream=True)
        if r.status_code == 200 and len(r.content) > 8000:
            ext = os.path.splitext(urlparse(url).path)[1] or ".jpg"
            if ext.lower() not in [".jpg", ".jpeg", ".png", ".webp"]:
                ext = ".jpg"
            if not path.lower().endswith(ext.lower()):
                path = path.rsplit(".", 1)[0] + ext
            with open(path, "wb") as f:
                f.write(r.content)
            return len(r.content)
    except Exception:
        pass
    return None

with open(os.path.join(BASE, "new-articles.json"), "r", encoding="utf-8") as f:
    arts = json.load(f)

# Preserve existing mappings so we don't re-download what's already free
image_map_path = os.path.join(BASE, "image-map.json")
if os.path.exists(image_map_path):
    with open(image_map_path, "r", encoding="utf-8") as f:
        local_images = json.load(f)
else:
    local_images = {}

ok_count = 0
fail_count = 0

for idx, a in enumerate(arts, 1):
    title = a["title"]
    slug_raw = a["slug"].replace("berita/", "")
    slug_key = slug_raw[:42].replace("/", "-").replace(" ", "-")
    fname = f"art_{slug_key}.jpg"
    fpath = os.path.join(IMG_DIR, fname)

    # Skip if already have local file AND not detik-sourced
    if os.path.exists(fpath) and fname in str(local_images.get(a["slug"], "")):
        print(f"[{idx}/{len(arts)}] SKIP (already local): {title[:45]}")
        ok_count += 1
        continue

    kw = keywords_from_title(title)
    print(f"[{idx}/{len(arts)}] {title[:55]}... | kw={kw[:40]}", end=" -> ")

    img_url = wiki_pageimage(kw)
    src = "wiki"
    if not img_url:
        img_url = commons_search(' '.join(kw.split()[:4]))
        src = "commons"
    if not img_url:
        img_url = pexels_source(kw)
        src = "picsum"

    if img_url:
        # remove any existing detik image file first
        if os.path.exists(fpath):
            os.remove(fpath)
        size = download(img_url, fpath)
        if size and size > 8000:
            local_images[a["slug"]] = f"images/{fname}"
            ok_count += 1
            print(f"OK ({src}) {size//1024}KB")
        else:
            if os.path.exists(fpath):
                os.remove(fpath)
            fail_count += 1
            print("FAIL small")
    else:
        fail_count += 1
        print("FAIL no image")

    time.sleep(0.3)

print(f"\nDownloaded {ok_count}/{len(arts)} images ({fail_count} failed)")
with open(image_map_path, "w", encoding="utf-8") as f:
    json.dump(local_images, f, ensure_ascii=False, indent=2)
print(f"Saved image-map.json ({len(local_images)} entries)")
