import json, re, os

with open("scraped-detik.json", "r", encoding="utf-8") as f:
    raw = json.load(f)

# Load local image map if exists (from download-images.py)
_image_map = {}
_map_path = os.path.join(os.getcwd(), "image-map.json")
if os.path.exists(_map_path):
    with open(_map_path, "r", encoding="utf-8") as f:
        _image_map = _json.load(f) if False else {}
import json as _json2
if os.path.exists(_map_path):
    with open(_map_path, "r", encoding="utf-8") as f:
        _image_map = _json2.load(f)

new_articles = []
for a in raw:
    # clean content - remove junk text
    content = a["content"]
    content = re.sub(r'SCROLL TO CONTINUE WITH CONTENT', '', content)
    content = re.sub(r'Lihat juga Video[^<]+<a[^>]+>[^<]+</a>', '', content)
    content = re.sub(r'<p>\s*</p>', '', content)
    content = re.sub(r'\s+', ' ', content).strip()

    raw_slug = a["slug"]

    # Map to local image if available
    img_url = a["image"]
    for key, local_path in _image_map.items():
        if key.startswith(raw_slug[:30]) or raw_slug[:30].startswith(key[:30]):
            img_url = local_path
            break

    new_articles.append({
        "slug": "berita/" + raw_slug,  # ALWAYS prefix with berita/
        "title": a["title"],
        "category": a["category"],
        "breadcrumb": a["breadcrumb"],
        "date": a["date"],
        "image": img_url,  # local path or original URL
        "image_alt": a["image_alt"],
        "content": content
    })

with open("new-articles.json", "w", encoding="utf-8") as f:
    json.dump(new_articles, f, ensure_ascii=False, indent=2)

print(f"Prepared {len(new_articles)} articles in new-articles.json (all with berita/ prefix)")
if _image_map:
    print(f"Image map: {len(_image_map)} local images available")