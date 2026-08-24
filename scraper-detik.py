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

DETIK_URLS = [
    "https://news.detik.com/berita/d-8633317/2-pelajar-babel-ditangkap-usai-ketahuan-bakar-lahan-kosong-ngaku-cuma-iseng",
    "https://news.detik.com/berita/d-8633314/mobil-tertemper-krl-di-karet-jakpus-kai-pastikan-tak-ada-korban",
    "https://news.detik.com/berita/d-8633311/napi-di-garut-kalapas-rasa-sahabat-cikal-bakal-lahirnya-paskopi",
    "https://news.detik.com/berita/d-8633298/habitat-satwa-terdampak-imbas-karhutla-di-kalbar-3-orang-utan-dievakuasi",
    "https://news.detik.com/berita/d-8633292/rebutan-gamelan-sekaten-kubu-pb-xiv-purbaya-polisikan-lda",
    "https://news.detik.com/berita/d-8633286/herman-deru-pastikan-penanganan-karhutla-di-sumsel-terus-diperkuat",
    "https://news.detik.com/berita/d-8633262/terungkap-kejinya-rahmat-dimas-bunuh-ojol-tidur-dari-reka-ulang",
    "https://news.detik.com/berita/d-8633259/mobil-tertemper-krl-di-jalur-tanah-abang-karet-perjalanan-sempat-terganggu",
    "https://news.detik.com/berita/d-8633254/situs-purba-di-sukabumi-tak-terawat-banyak-temuan-sampah-pakaian-dalam-bekas",
    "https://news.detik.com/berita/d-8633241/pb-possi-perkuat-regenerasi-instruktur-selam-untuk-sdm-berkualitas",
]

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

def extract_detik(url):
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

    # content - find article body
    m = re.search(r'<div[^>]*class="detail__body[^"]*"[^>]*>(.*?)</div>\s*<div', html, re.S)
    if not m:
        m = re.search(r'<article[^>]*>(.*?)</article>', html, re.S)
    body = m.group(1) if m else ""

    # extract paragraphs
    paras = re.findall(r'<p[^>]*>(.*?)</p>', body, re.S)
    content = []
    for p in paras:
        clean = re.sub(r'<[^>]+>', '', p).strip()
        if len(clean) > 30:
            content.append(clean)

    return {"title": title, "img_url": img_url, "date": date_str, "content": content, "url": url}

def rewrite(text):
    """Simple rewrite - just return as-is for now, full spin in spin-copy.py"""
    return text

articles = []
for url in DETIK_URLS:
    print(f"Fetching: {url}")
    data = extract_detik(url)
    if data and data["content"]:
        slug = re.sub(r'[^a-z0-9]+', '-', data["title"].lower())[:60]
        slug = re.sub(r'-+', '-', slug).strip('-')
        print(f"  -> {data['title'][:60]} | img: {bool(data['img_url'])} | paras: {len(data['content'])}")
        articles.append({
            "slug": slug,
            "title": data["title"],
            "date": data["date"],
            "image": data["img_url"],
            "image_alt": data["title"][:50],
            "content": '\n'.join([f'<p>{rewrite(p)}</p>' for p in data['content']]),
            "category": "Berita",
            "breadcrumb": data["title"][:30],
        })

print(f"\nTotal: {len(articles)} articles scraped")
with open("scraped-detik.json","w",encoding="utf-8") as f:
    json.dump(articles, f, ensure_ascii=False, indent=2)
print("Saved to scraped-detik.json")
