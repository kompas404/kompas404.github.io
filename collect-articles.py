import os, json, re

BASE = r"C:\Users\ideapad gaming 3\kompas404-seo"
berita_dir = os.path.join(BASE, "berita")

# Load static articles from build-articles.py (hardcoded legacy)
legacy = {
    "berita/teknologi-ai-2026": {
        "category": "Teknologi", "breadcrumb": "Teknologi AI 2026",
        "title": "Perkembangan AI Terbaru 2026",
        "date": "18 Agustus 2026",
        "content": '<p>Tahun 2026 menjadi tonggak penting dalam perkembangan kecerdasan buatan (AI) global. Tren utama: AI Multimodal, AI Agent Otonom, Regulasi AI Global, dan AI di Sektor Kesehatan.</p>'
    },
    "berita/ekonomi-digital": {
        "category": "Bisnis", "breadcrumb": "Ekonomi Digital",
        "title": "Ekonomi Digital Indonesia 2026",
        "date": "17 Agustus 2026",
        "content": '<p>Ekonomi digital Indonesia terus menunjukkan pertumbuhan impresif di 2026. Nilai transaksi e-commerce diproyeksikan menembus Rp800 triliun.</p>'
    },
    "berita/sepakbola-terkini": {
        "category": "Olahraga", "breadcrumb": "Sepakbola",
        "title": "Update Sepakbola Terkini 2026",
        "date": "15 Agustus 2026",
        "content": '<p>Dunia sepak bola memasuki musim 2026/2027 dengan berbagai kejutan. Premier League, La Liga, Liga Champions, dan Timnas Indonesia menjadi sorotan.</p>'
    },
    "berita/cybersecurity-2026": {
        "category": "Teknologi", "breadcrumb": "Cybersecurity",
        "title": "Ancaman Cybersecurity 2026",
        "date": "16 Agustus 2026",
        "content": '<p>Lanskap ancaman keamanan siber di 2026 semakin kompleks. AI-Powered Attacks, Ransomware-as-a-Service, Deepfake Fraud, dan Supply Chain Attack.</p>'
    },
    "berita/startup-indonesia": {
        "category": "Bisnis", "breadcrumb": "Startup Indonesia",
        "title": "Startup Indonesia Naik Daun 2026",
        "date": "14 Agustus 2026",
        "content": '<p>Ekosistem startup Indonesia terus bergeliat di 2026. GoTo, Sea Group, Traveloka, OVO, dan Xendit menjadi unicorn terdepan.</p>'
    },
    "berita/tips-produktivitas": {
        "category": "Lifestyle", "breadcrumb": "Tips Produktivitas",
        "title": "Tips Produktivitas Harian 2026",
        "date": "13 Agustus 2026",
        "content": '<p>Di era digital yang serba cepat, produktivitas menjadi kunci. Teknik Pomodoro, Eisenhower Matrix, Digital Declutter, dan Time Blocking.</p>'
    },
}

# 2 new articles
new_articles = [
    {
        "slug": "berita/umkm-digital-2026-qris-meroket",
        "title": "UMKM Digital 2026: QRIS Meledak, Marketplace Lokal Jadi Magnet Investor",
        "category": "Bisnis",
        "date": "Senin, 14 September 2026 10:00 WIB",
        "content": "Sektor UMKM Indonesia memasuki fase baru di 2026. QRIS sudah jadi standar pembayaran de facto. Lebih dari 52 juta merchant aktif menerima QRIS."
    },
    {
        "slug": "berita/ruu-pdp-turunan-2026-pelaku-usaha-digital",
        "title": "RUU PDP Turunan 2026: Pelaku Usaha Digital Wajib Patuh Mulai 2027",
        "category": "Politik",
        "date": "Senin, 14 September 2026 11:30 WIB",
        "content": "Pembahasan regulasi turunan UU PDP memasuki babak kritis. DPO wajib, pelaporan insiden 72 jam, data localization terbatas."
    }
]

# Scan all berita folders - extract title from h1 and meta span
all_articles = []

# Add new articles first
for a in new_articles:
    all_articles.append({
        "slug": a["slug"],
        "title": a["title"],
        "category": a["category"],
        "date": a["date"],
        "breadcrumb": a["title"][:30],
        "content": a["content"]
    })

# Add legacy static
for slug, data in legacy.items():
    all_articles.append({
        "slug": slug,
        "title": data["title"],
        "category": data["category"],
        "date": data["date"],
        "breadcrumb": data["breadcrumb"],
        "content": data["content"]
    })

# Scan folder for old articles - try to extract metadata
for folder in sorted(os.listdir(berita_dir)):
    folder_path = os.path.join(berita_dir, folder)
    if not os.path.isdir(folder_path):
        continue
    idx = os.path.join(folder_path, "index.html")
    if not os.path.exists(idx):
        continue
    slug = f"berita/{folder}"
    if any(a["slug"] == slug for a in all_articles):
        continue
    try:
        with open(idx, "r", encoding="utf-8") as f:
            html = f.read()
        # Try meta og:title first
        m = re.search(r'<meta property="og:title" content="([^"]+?)(?:\s*[—\-]\s*Kompas404)?"', html)
        title = m.group(1).strip() if m else folder.replace("-", " ").title()
        m = re.search(r'<span>([^<]+)</span>\s*([^<]+)', html)
        if m:
            category = m.group(1).strip()
            date = m.group(2).strip()
        else:
            category = "Umum"
            date = "Agustus 2026"
        # Excerpt
        m = re.search(r'<p>([^<]{50,200})', html)
        excerpt = m.group(1)[:150] if m else title
        all_articles.append({
            "slug": slug,
            "title": title,
            "category": category,
            "date": date,
            "breadcrumb": title[:30],
            "content": excerpt
        })
    except Exception as e:
        print(f"Skip {folder}: {e}")

print(f"Total articles collected: {len(all_articles)}")

# Save full list
with open(os.path.join(BASE, "new-articles.json"), "w", encoding="utf-8") as f:
    json.dump(all_articles, f, ensure_ascii=False, indent=2)

print("Saved new-articles.json with all articles")
