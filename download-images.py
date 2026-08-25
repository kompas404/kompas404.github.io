#!/usr/bin/env python3
"""Download article images locally to avoid detik/kompas watermarks"""
import json, os, requests
from urllib.parse import urlparse

BASE = os.path.expanduser(r"C:\Users\ideapad gaming 3\kompas404-seo")
IMG_DIR = os.path.join(BASE, "images")
os.makedirs(IMG_DIR, exist_ok=True)

with open(os.path.join(BASE, "new-articles.json"), "r", encoding="utf-8") as f:
    arts = json.load(f)

local_images = {}
for a in arts:
    url = a.get("image")
    if not url or not url.startswith("http"):
        continue
    slug = a["slug"].replace("berita/", "").replace("/", "-")[:40]
    ext = os.path.splitext(urlparse(url).path)[1] or ".jpg"
    if ext.lower() not in [".jpg", ".jpeg", ".png", ".webp"]:
        ext = ".jpg"
    fname = f"art_{slug}{ext}"
    fpath = os.path.join(IMG_DIR, fname)
    try:
        r = requests.get(url, headers={"Referer": "https://news.detik.com/"}, timeout=20)
        if r.status_code == 200 and len(r.content) > 5000:
            with open(fpath, "wb") as f:
                f.write(r.content)
            local_path = f"images/{fname}"
            local_images[a["slug"]] = local_path
            print(f"OK: {fname} ({len(r.content)//1024}KB)")
        else:
            print(f"FAIL {r.status_code}: {url[:60]}")
    except Exception as e:
        print(f"FAIL: {url[:60]} - {e}")

print(f"\nDownloaded {len(local_images)} images")

# Save mapping
with open(os.path.join(BASE, "image-map.json"), "w", encoding="utf-8") as f:
    json.dump(local_images, f, ensure_ascii=False, indent=2)
print("Saved image-map.json")