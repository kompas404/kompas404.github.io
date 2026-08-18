import os, sys

BASE = os.path.expanduser(r"C:\Users\ideapad gaming 3\kompas404-seo")

with open(os.path.join(BASE, "index.html"), "r", encoding="utf-8") as f:
    html = f.read()

body_start = html.index("<body>")
head_part = html[:body_start + len("<body>")]

footer_start = html.index("    <footer>")
footer_part = html[footer_start:]

CSS_START = html.index("<style>")
CSS_END = html.index("</style>") + len("</style>")
css_block = html[CSS_START:CSS_END]

articles = {
    "berita/teknologi-ai-2026": {
        "category": "Teknologi",
        "breadcrumb": "Teknologi AI 2026",
        "title": "Perkembangan AI Terbaru 2026",
        "date": "18 Agustus 2026",
        "content": '<p>KOMPAS404 - Tahun 2026 menjadi tonggak penting dalam perkembangan kecerdasan buatan (AI) global. Berbagai terobosan hadir mewarnai lanskap teknologi dunia, mulai dari model bahasa besar (LLM) generasi baru hingga sistem autonomous yang semakin canggih.</p>\n<h2>Tren Utama AI 2026</h2>\n<p>Beberapa tren utama yang mencuat di 2026 antara lain:</p>\n<ul><li><strong>AI Multimodal</strong> - Model yang mampu memproses teks, gambar, video, dan audio secara simultan kini menjadi standar industri.</li>\n<li><strong>AI Agent Otonom</strong> - Sistem AI yang dapat menjalankan tugas kompleks tanpa intervensi manusia semakin banyak diadopsi di sektor enterprise.</li>\n<li><strong>Regulasi AI Global</strong> - Uni Eropa, Amerika Serikat, dan Indonesia mulai menerapkan framework regulasi AI yang lebih ketat.</li>\n<li><strong>AI di Sektor Kesehatan</strong> - Diagnosa berbasis AI mencapai akurasi tinggi dalam deteksi dini kanker dan penyakit kardiovaskular.</li></ul>\n<p>Indonesia sendiri tidak ketinggalan. Beberapa startup lokal mulai mengembangkan model AI berbahasa Indonesia yang kompetitif. KOMPAS404 akan terus memantau perkembangan ini.</p>'
    },
    "berita/ekonomi-digital": {
        "category": "Bisnis",
        "breadcrumb": "Ekonomi Digital",
        "title": "Ekonomi Digital Indonesia 2026",
        "date": "17 Agustus 2026",
        "content": '<p>KOMPAS404 - Ekonomi digital Indonesia terus menunjukkan pertumbuhan impresif di tahun 2026. Nilai transaksi e-commerce diproyeksikan menembus Rp800 triliun, naik signifikan dari tahun sebelumnya.</p>\n<h2>Pendorong Pertumbuhan</h2>\n<p>Beberapa faktor kunci:</p>\n<ul><li><strong>Penetrasi Internet</strong> - Lebih dari 215 juta pengguna internet, pasar digital terbesar di Asia Tenggara.</li>\n<li><strong>Adopsi QRIS</strong> - 50 juta merchant, memudahkan transaksi non-tunai.</li>\n<li><strong>Investasi Asing</strong> - VC global terus mengalir ke startup Indonesia.</li>\n<li><strong>UMKM Go Digital</strong> - 30 juta UMKM onboarding ke platform digital.</li></ul>\n<p>KOMPAS404 mencatat fintech dan logistik sebagai subsektor paling agresif. Simak terus analisis ekonomi digital hanya di KOMPAS404.</p>'
    },
    "berita/sepakbola-terkini": {
        "category": "Olahraga",
        "breadcrumb": "Sepakbola",
        "title": "Update Sepakbola Terkini 2026",
        "date": "15 Agustus 2026",
        "content": '<p>KOMPAS404 - Dunia sepakbola memasuki musim kompetisi 2026/2027 dengan berbagai kejutan. Liga-liga top Eropa kembali bergulir dengan persaingan ketat.</p>\n<h2>Sorotan Utama</h2>\n<ul><li><strong>Premier League</strong> - Manchester City dan Arsenal bersaing ketat, Newcastle United tampil sebagai kuda hitam.</li>\n<li><strong>La Liga</strong> - Barcelona dan Real Madrid melakukan perombakan skuad besar-besaran.</li>\n<li><strong>Liga Champions</strong> - Format Swiss league memasuki musim kedua, semakin menarik.</li>\n<li><strong>Timnas Indonesia</strong> - Skuad Garuda bersiap kualifikasi Piala Dunia 2030.</li></ul>\n<p>KOMPAS404 akan terus memberikan update dan analisis mendalam seputar sepakbola.</p>'
    },
    "berita/cybersecurity-2026": {
        "category": "Teknologi",
        "breadcrumb": "Cybersecurity",
        "title": "Ancaman Cybersecurity 2026",
        "date": "16 Agustus 2026",
        "content": '<p>KOMPAS404 - Lanskap ancaman keamanan siber di 2026 semakin kompleks. Serangan ransomware, phishing, dan supply chain attack terus berevolusi.</p>\n<h2>5 Ancaman Siber yang Harus Diwaspadai</h2>\n<ol><li><strong>AI-Powered Attacks</strong> - Serangan siber memanfaatkan AI generatif untuk phishing email yang sangat meyakinkan.</li>\n<li><strong>Ransomware-as-a-Service</strong> - Model bisnis ransomware semakin matang dengan ekosistem afiliasi yang luas.</li>\n<li><strong>Deepfake Fraud</strong> - Teknologi deepfake untuk social engineering tingkat tinggi.</li>\n<li><strong>Supply Chain Attack</strong> - Serangan melalui vendor pihak ketiga terus meningkat.</li>\n<li><strong>Cloud Misconfiguration</strong> - Kesalahan konfigurasi cloud menjadi pintu masuk utama attacker.</li></ol>\n<p>KOMPAS404 merekomendasikan zero-trust architecture dan AI-driven security solutions.</p>'
    },
    "berita/startup-indonesia": {
        "category": "Bisnis",
        "breadcrumb": "Startup Indonesia",
        "title": "Startup Indonesia Naik Daun 2026",
        "date": "14 Agustus 2026",
        "content": '<p>KOMPAS404 - Ekosistem startup Indonesia terus bergeliat di 2026. Unicorn dan decacorn lokal mencatatkan pencapaian signifikan.</p>\n<h2>Daftar Startup Unicorn Indonesia 2026</h2>\n<ul><li><strong>GoTo Group</strong> - Valuasi lebih dari $25 miliar.</li>\n<li><strong>Sea Group (Shopee)</strong> - E-commerce raksasa Asia Tenggara.</li>\n<li><strong>Traveloka</strong> - Ekspansi ke Australia dan Timur Tengah.</li>\n<li><strong>OVO</strong> - 100 juta pengguna aktif.</li>\n<li><strong>Xendit</strong> - Pendanaan Seri D $500 juta.</li></ul>\n<p>KOMPAS404 mencatat agritech dan climate tech sebagai emerging sectors 2026.</p>'
    },
    "berita/tips-produktivitas": {
        "category": "Lifestyle",
        "breadcrumb": "Tips Produktivitas",
        "title": "Tips Produktivitas Harian 2026",
        "date": "13 Agustus 2026",
        "content": '<p>KOMPAS404 - Di era digital yang serba cepat, produktivitas menjadi kunci. Berikut tips yang bisa Anda terapkan sehari-hari.</p>\n<h2>5 Tips Produktivitas Efektif</h2>\n<ol><li><strong>Teknik Pomodoro</strong> - Fokus 25 menit, istirahat 5 menit. Setelah 4 siklus, istirahat 15-30 menit.</li>\n<li><strong>Eisenhower Matrix</strong> - Kategorikan tugas urgent vs important.</li>\n<li><strong>Digital Declutter</strong> - Bersihkan notifikasi, unsubscribe email tidak penting.</li>\n<li><strong>Time Blocking</strong> - Blokir waktu di kalender untuk deep work.</li>\n<li><strong>Mindfulness Break</strong> - 5-10 menit meditasi di tengah kesibukan.</li></ol>\n<p>KOMPAS404 akan terus berbagi tips produktivitas harian. Stay productive!</p>'
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

for slug, data in articles.items():
    path = os.path.join(BASE, slug, "index.html")
    os.makedirs(os.path.dirname(path), exist_ok=True)

    depth = slug.count("/")
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
