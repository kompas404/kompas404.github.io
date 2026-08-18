import os

BASE = os.path.expanduser(r"C:\Users\ideapad gaming 3\kompas404-seo")

with open(os.path.join(BASE, "index.html"), "r", encoding="utf-8") as f:
    html = f.read()

body_start = html.index("<body>")
head_part = html[:body_start + len("<body>")]

footer_start = html.index("    <footer>")
footer_part = html[footer_start:]

# Merge new articles from auto-generator if present
import json as _json
_new_articles_file = os.path.join(BASE, "new-articles.json")
_new_articles = {}
if os.path.exists(_new_articles_file):
    with open(_new_articles_file, encoding="utf-8") as _f:
        _new_list = _json.load(_f)
    for _a in _new_list:
        _slug = _a.pop("slug")
        _new_articles[_slug] = _a
    print(f"Loaded {len(_new_articles)} new auto-generated articles")

articles = {
    **_new_articles,
    "berita/teknologi-ai-2026": {
        "category": "Teknologi",
        "breadcrumb": "Teknologi AI 2026",
        "title": "Perkembangan AI Terbaru 2026",
        "date": "18 Agustus 2026",
        "image": "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=800&q=80",
        "image_alt": "Artificial Intelligence Technology",
        "content": '<p>KOMPAS404 - Tahun 2026 menjadi tonggak penting dalam perkembangan kecerdasan buatan (AI) global. Berbagai terobosan hadir mewarnai lanskap teknologi dunia.</p>\n<h2>Tren Utama AI 2026</h2>\n<ul><li><strong>AI Multimodal</strong> - Model yang mampu memproses teks, gambar, video, dan audio secara simultan kini menjadi standar industri.</li>\n<li><strong>AI Agent Otonom</strong> - Sistem AI yang dapat menjalankan tugas kompleks tanpa intervensi manusia.</li>\n<li><strong>Regulasi AI Global</strong> - Uni Eropa, AS, dan Indonesia mulai menerapkan framework regulasi AI.</li>\n<li><strong>AI di Sektor Kesehatan</strong> - Diagnosa berbasis AI mencapai akurasi tinggi untuk deteksi dini.</li></ul>\n<p>Indonesia tidak ketinggalan. Startup lokal mulai mengembangkan model AI berbahasa Indonesia yang kompetitif.</p>'
    },
    "berita/ekonomi-digital": {
        "category": "Bisnis",
        "breadcrumb": "Ekonomi Digital",
        "title": "Ekonomi Digital Indonesia 2026",
        "date": "17 Agustus 2026",
        "image": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&q=80",
        "image_alt": "Digital Economy Growth",
        "content": '<p>KOMPAS404 - Ekonomi digital Indonesia terus menunjukkan pertumbuhan impresif di 2026. Nilai transaksi e-commerce diproyeksikan menembus Rp800 triliun.</p>\n<h2>Pendorong Pertumbuhan</h2>\n<ul><li><strong>Penetrasi Internet</strong> - 215 juta pengguna, pasar digital terbesar di Asia Tenggara.</li>\n<li><strong>Adopsi QRIS</strong> - 50 juta merchant aktif, transaksi non-tunai melonjak.</li>\n<li><strong>Investasi Asing</strong> - VC global terus mengalir ke startup Indonesia.</li>\n<li><strong>UMKM Go Digital</strong> - 30 juta UMKM onboarding ke platform digital.</li></ul>\n<p>Fintech dan logistik menjadi subsektor paling agresif tahun ini.</p>'
    },
    "berita/sepakbola-terkini": {
        "category": "Olahraga",
        "breadcrumb": "Sepakbola",
        "title": "Update Sepakbola Terkini 2026",
        "date": "15 Agustus 2026",
        "image": "https://images.unsplash.com/photo-1579952363873-27f3bade9f55?w=800&q=80",
        "image_alt": "Football Stadium",
        "content": '<p>KOMPAS404 - Dunia sepakbola memasuki musim 2026/2027 dengan berbagai kejutan. Liga-liga top Eropa kembali bergulir.</p>\n<h2>Sorotan Utama</h2>\n<ul><li><strong>Premier League</strong> - Man City dan Arsenal bersaing ketat, Newcastle kuda hitam.</li>\n<li><strong>La Liga</strong> - Barcelona dan Real Madrid rombak skuad besar-besaran.</li>\n<li><strong>Liga Champions</strong> - Format Swiss league musim kedua, makin seru.</li>\n<li><strong>Timnas Indonesia</strong> - Garuda bersiap kualifikasi Piala Dunia 2030.</li></ul>\n<p>KOMPAS404 terus memberikan update dan analisis mendalam seputar sepakbola.</p>'
    },
    "berita/cybersecurity-2026": {
        "category": "Teknologi",
        "breadcrumb": "Cybersecurity",
        "title": "Ancaman Cybersecurity 2026",
        "date": "16 Agustus 2026",
        "image": "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=800&q=80",
        "image_alt": "Cyber Security",
        "content": '<p>KOMPAS404 - Lanskap ancaman keamanan siber di 2026 semakin kompleks. Serangan ransomware, phishing, dan supply chain attack terus berevolusi.</p>\n<h2>5 Ancaman Siber 2026</h2>\n<ol><li><strong>AI-Powered Attacks</strong> - AI generatif untuk phishing email yang sangat meyakinkan.</li>\n<li><strong>Ransomware-as-a-Service</strong> - Ekosistem afiliasi ransomware makin matang.</li>\n<li><strong>Deepfake Fraud</strong> - Social engineering tingkat tinggi dengan impersonasi.</li>\n<li><strong>Supply Chain Attack</strong> - Serangan via vendor pihak ketiga meningkat.</li>\n<li><strong>Cloud Misconfiguration</strong> - Kesalahan konfigurasi cloud jadi pintu masuk utama.</li></ol>\n<p>KOMPAS404 merekomendasikan zero-trust architecture dan AI-driven security.</p>'
    },
    "berita/startup-indonesia": {
        "category": "Bisnis",
        "breadcrumb": "Startup Indonesia",
        "title": "Startup Indonesia Naik Daun 2026",
        "date": "14 Agustus 2026",
        "image": "https://images.unsplash.com/photo-1559136555-9303baea8ebd?w=800&q=80",
        "image_alt": "Startup Office",
        "content": '<p>KOMPAS404 - Ekosistem startup Indonesia terus bergeliat di 2026. Unicorn dan decacorn lokal mencatatkan pencapaian signifikan.</p>\n<h2>Daftar Unicorn Indonesia 2026</h2>\n<ul><li><strong>GoTo Group</strong> - Valuasi lebih dari $25 miliar, ekosistem digital terbesar.</li>\n<li><strong>Sea Group (Shopee)</strong> - Dominasi e-commerce Asia Tenggara.</li>\n<li><strong>Traveloka</strong> - Ekspansi sukses ke Australia dan Timur Tengah.</li>\n<li><strong>OVO</strong> - 100 juta pengguna aktif, fintech terdepan.</li>\n<li><strong>Xendit</strong> - Pendanaan Seri D $500 juta, infrastructure payment.</li></ul>\n<p>Agritech dan climate tech muncul sebagai emerging sectors 2026.</p>'
    },
    "berita/tips-produktivitas": {
        "category": "Lifestyle",
        "breadcrumb": "Tips Produktivitas",
        "title": "Tips Produktivitas Harian 2026",
        "date": "13 Agustus 2026",
        "image": "https://images.unsplash.com/photo-1488190211105-8b0e65b80b4e?w=800&q=80",
        "image_alt": "Productive Workspace",
        "content": '<p>KOMPAS404 - Di era digital yang serba cepat, produktivitas menjadi kunci kesuksesan. Berikut tips yang bisa Anda terapkan.</p>\n<h2>5 Tips Produktivitas Efektif</h2>\n<ol><li><strong>Teknik Pomodoro</strong> - Fokus 25 menit, istirahat 5 menit. Ulangi 4 siklus.</li>\n<li><strong>Eisenhower Matrix</strong> - Kategorikan tugas urgent vs important, kerjakan yang penting dulu.</li>\n<li><strong>Digital Declutter</strong> - Bersihkan notifikasi, unsubscribe email, rapikan desktop.</li>\n<li><strong>Time Blocking</strong> - Blokir waktu di kalender untuk deep work tanpa gangguan.</li>\n<li><strong>Mindfulness Break</strong> - 5-10 menit meditasi di tengah kesibukan.</li></ol>\n<p>KOMPAS404 akan terus berbagi tips produktivitas harian. Stay productive!</p>'
    }
}

categories = [
    ("berita/index.html", "Berita", "Semua Berita KOMPAS404", ["teknologi-ai-2026", "ekonomi-digital", "sepakbola-terkini", "cybersecurity-2026", "startup-indonesia", "tips-produktivitas"]),
    ("teknologi/index.html", "Teknologi", "Berita Teknologi KOMPAS404", ["teknologi-ai-2026", "cybersecurity-2026"]),
    ("bisnis/index.html", "Bisnis", "Berita Bisnis KOMPAS404", ["ekonomi-digital", "startup-indonesia"]),
    ("olahraga/index.html", "Olahraga", "Berita Olahraga KOMPAS404", ["sepakbola-terkini"]),
    ("tentang/index.html", "Tentang", "Tentang KOMPAS404", None),
]

ARTICLE_DETAIL_CSS = """
        .article-detail {
            background: #1a1a1a;
            border: 1px solid #2a2a2a;
            border-radius: 6px;
            padding: 30px;
            margin-bottom: 20px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.3);
        }
        .article-title {
            color: #f0c75e;
            font-size: 1.8em;
            margin: 10px 0 8px;
        }
        .article-meta {
            color: #777;
            font-size: 0.85em;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 1px solid #2a2a2a;
        }
        .article-featured-img {
            width: 100%;
            height: auto;
            border-radius: 4px;
            margin-bottom: 20px;
            border: 1px solid #2a2a2a;
        }
        .article-body { color: #e0e0e0; line-height: 1.8; }
        .article-body h2 { color: #d4a843; font-size: 1.3em; margin: 24px 0 12px; }
        .article-body ul, .article-body ol { margin: 10px 0 20px 20px; }
        .article-body li { margin-bottom: 8px; color: #bbb; }
        .article-body strong { color: #f0c75e; }
        .article-body p { margin-bottom: 14px; }
"""

def merge_css(orig_css, extra_css):
    end = orig_css.rfind("</style>")
    return orig_css[:end] + extra_css + orig_css[end:]

head_with_extra_css = merge_css(head_part, ARTICLE_DETAIL_CSS)

# Generate article pages
for slug, data in articles.items():
    path = os.path.join(BASE, slug, "index.html")
    os.makedirs(os.path.dirname(path), exist_ok=True)

    # berita/x = 2 dirs deep from root -> ../../
    depth = slug.count("/") + 1
    prefix = "../" * depth

    page = head_with_extra_css.replace(
        '<link rel="icon" type="image/png" sizes="32x32" href="icon-kompas404.png">',
        f'<link rel="icon" type="image/png" sizes="32x32" href="{prefix}icon-kompas404.png">'
    ).replace(
        '<link rel="apple-touch-icon" href="icon-kompas404.png">',
        f'<link rel="apple-touch-icon" href="{prefix}icon-kompas404.png">'
    )

    page += f"""
    <title>{data['title']} — KOMPAS404</title>
</head>
<body>

    <header>
        <a href="/"><img src="{prefix}logo-kompas404.png" alt="KOMPAS404 Logo" class="logo" width="160" height="160"></a>
        <a href="/" style="text-decoration:none;"><h1>KOMPAS<span>404</span></h1></a>
        <p>Portal Berita & Informasi Terkini — KOMPAS404</p>
    </header>

    <nav>
        <a href="/">Beranda</a>
        <a href="{prefix}berita">Berita</a>
        <a href="{prefix}teknologi">Teknologi</a>
        <a href="{prefix}bisnis">Bisnis</a>
        <a href="{prefix}olahraga">Olahraga</a>
        <a href="{prefix}tentang">Tentang</a>
    </nav>

    <div class="container">

        <div class="breadcrumb">
            <a href="/">KOMPAS404</a> &rsaquo; <a href="{prefix}berita">Berita</a> &rsaquo; {data['breadcrumb']}
        </div>

        <article class="article-detail">
            <span class="tag">{data['category']}</span>
            <h1 class="article-title">{data['title']}</h1>
            <div class="article-meta">
                {data['date']} — <span>KOMPAS404</span>
            </div>
            <img src="{data['image']}" alt="{data['image_alt']}" class="article-featured-img" width="800" height="400" loading="lazy">
            <div class="article-body">
                {data['content']}
            </div>
        </article>

        <div style="text-align:center;margin:30px 0;">
            <a href="{prefix}berita" class="cta">Kembali ke Berita</a>
        </div>

    </div>

{footer_part}"""

    with open(path, "w", encoding="utf-8") as f:
        f.write(page)
    print(f"Created: {slug}/index.html")

# Generate category pages
for cat_path, cat_name, cat_desc, article_slugs in categories:
    path = os.path.join(BASE, cat_path)
    os.makedirs(os.path.dirname(path), exist_ok=True)

    depth = cat_path.count("/")
    prefix = "../" * depth if depth > 0 else ""

    is_tentang = cat_name == "Tentang"

    if is_tentang:
        content_html = """
        <div class="article-detail">
            <h1 class="article-title">Tentang KOMPAS404</h1>
            <div class="article-body">
                <p><strong>KOMPAS404</strong> adalah portal berita dan media informasi digital yang hadir untuk memberikan akses informasi terkini kepada masyarakat Indonesia.</p>
                <p>Misi <strong>KOMPAS404</strong> adalah menyajikan berita faktual, analisis tajam, dan konten edukatif yang relevan dengan kebutuhan pembaca modern.</p>
                <p>Kami berkomitmen pada akurasi, kecepatan, dan kedalaman analisis. Setiap konten di <strong>KOMPAS404</strong> melewati proses editorial yang ketat untuk memastikan kualitas.</p>
                <p><strong>KOMPAS404</strong> selalu update 24/7 sehingga Anda tidak ketinggalan informasi penting.</p>
                <p>Kontak: <a href="mailto:admin@kompas404.my.id" style="color:#d4a843;">admin@kompas404.my.id</a></p>
            </div>
        </div>
        """
    else:
        items_html = ""
        for slug in article_slugs:
            a = articles[f"berita/{slug}"]
            excerpt = a['content'].split('</p>')[0].replace('<p>KOMPAS404 - ', '').replace('<p>', '')[:120]
            items_html += f"""
            <article class="card">
                <span class="tag">{a['category']}</span>
                <h3><a href="/berita/{slug}/">{a['title']}</a></h3>
                <p>{excerpt}...</p>
            </article>"""
        content_html = f"""<h2 class="section-title">{cat_desc}</h2>
        <div class="grid">{items_html}
        </div>"""

    cat_page = head_with_extra_css.replace(
        '<link rel="icon" type="image/png" sizes="32x32" href="icon-kompas404.png">',
        f'<link rel="icon" type="image/png" sizes="32x32" href="{prefix}icon-kompas404.png">'
    ).replace(
        '<link rel="apple-touch-icon" href="icon-kompas404.png">',
        f'<link rel="apple-touch-icon" href="{prefix}icon-kompas404.png">'
    )
    cat_page += f"""
    <title>{cat_name} — KOMPAS404 | Portal Berita & Informasi Terkini</title>
</head>
<body>

    <header>
        <a href="/"><img src="{prefix}logo-kompas404.png" alt="KOMPAS404 Logo" class="logo" width="160" height="160"></a>
        <a href="/" style="text-decoration:none;"><h1>KOMPAS<span>404</span></h1></a>
        <p>Portal Berita & Informasi Terkini — KOMPAS404</p>
    </header>

    <nav>
        <a href="/">Beranda</a>
        <a href="{prefix}berita">Berita</a>
        <a href="{prefix}teknologi">Teknologi</a>
        <a href="{prefix}bisnis">Bisnis</a>
        <a href="{prefix}olahraga">Olahraga</a>
        <a href="{prefix}tentang">Tentang</a>
    </nav>

    <div class="container">

        <div class="breadcrumb">
            <a href="/">KOMPAS404</a> &rsaquo; {cat_name}
        </div>

        {content_html}

    </div>

{footer_part}"""

    with open(path, "w", encoding="utf-8") as f:
        f.write(cat_page)
    print(f"Created: {cat_path}")

print("DONE - All pages generated!")
