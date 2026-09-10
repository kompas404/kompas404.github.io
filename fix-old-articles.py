#!/usr/bin/env python3
import os, re

BASE = r'C:\Users\ideapad gaming 3\kompas404-seo'
berita_dir = os.path.join(BASE, 'berita')

NEW_STYLE = """
        :root {
            --bg-dark: #0d0d0d;
            --bg-card: #1a1a1a;
            --bg-card-alt: #121212;
            --gold: #d4a843;
            --gold-light: #f0c75e;
            --gold-dark: #b8922e;
            --red: #c41e3a;
            --red-bright: #e63946;
            --green: #1b5e20;
            --green-felt: #2e7d32;
            --green-accent: #388e3c;
            --text: #e0e0e0;
            --text-dim: #999;
            --text-muted: #777;
            --border: #2a2a2a;
            --border-gold: rgba(212,168,67,0.3);
        }
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, sans-serif;
            background: var(--bg-dark);
            color: var(--text);
            line-height: 1.7;
            background-image: 
                radial-gradient(ellipse at 50% 0%, rgba(212,168,67,0.06) 0%, transparent 70%),
                radial-gradient(ellipse at 80% 20%, rgba(196,30,58,0.04) 0%, transparent 60%);
        }
        header {
            background: linear-gradient(180deg, #0d0d0d 0%, #141414 40%, #1a1a1a 100%);
            color: white;
            padding: 30px 20px;
            text-align: center;
            border-bottom: 3px solid var(--gold);
            position: relative;
        }
        header::after {
            content: '';
            position: absolute;
            bottom: -3px;
            left: 0;
            width: 100%;
            height: 1px;
            background: linear-gradient(90deg, transparent, var(--red), var(--gold), var(--red), transparent);
        }
        .logo {
            display: block;
            margin: 0 auto 10px;
            border-radius: 12px;
            max-width: 100%;
            height: auto;
            object-fit: contain;
            filter: drop-shadow(0 0 12px rgba(212,168,67,0.25));
        }
        header h1 {
            font-size: 2.8em;
            font-weight: 900;
            letter-spacing: 2px;
            text-transform: uppercase;
            background: linear-gradient(180deg, var(--gold-light) 0%, var(--gold) 50%, var(--gold-dark) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-shadow: none;
            filter: drop-shadow(0 2px 4px rgba(0,0,0,0.5));
        }
        header h1 span {
            background: linear-gradient(180deg, var(--red-bright) 0%, var(--red) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        header p {
            margin-top: 6px;
            font-size: 1em;
            color: var(--gold);
            letter-spacing: 1px;
            opacity: 0.8;
        }
        nav {
            background: #111;
            padding: 14px 20px;
            display: flex;
            gap: 20px;
            justify-content: center;
            flex-wrap: wrap;
            box-shadow: 0 4px 16px rgba(0,0,0,0.5);
            position: sticky;
            top: 0;
            z-index: 100;
            border-bottom: 1px solid var(--border-gold);
        }
        nav a {
            color: var(--text-dim);
            text-decoration: none;
            font-weight: 600;
            padding: 6px 16px;
            border-radius: 4px;
            transition: all 0.2s;
            letter-spacing: 0.5px;
            text-transform: uppercase;
            font-size: 0.85em;
        }
        nav a:hover {
            background: var(--gold);
            color: #0d0d0d;
        }
        .container {
            max-width: 960px;
            margin: 0 auto;
            padding: 30px 20px;
        }
        .hero {
            background: linear-gradient(135deg, var(--bg-card) 0%, #1e1e1e 100%);
            border: 1px solid var(--border-gold);
            border-radius: 8px;
            padding: 40px 30px;
            text-align: center;
            box-shadow: 0 4px 24px rgba(0,0,0,0.4), inset 0 1px 0 rgba(212,168,67,0.05);
            margin-bottom: 30px;
            position: relative;
        }
        .hero::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 2px;
            background: linear-gradient(90deg, transparent, var(--gold), transparent);
        }
        .hero h2 {
            font-size: 1.8em;
            color: var(--gold-light);
            margin-bottom: 12px;
        }
        .hero p {
            font-size: 1.05em;
            color: var(--text-dim);
            max-width: 600px;
            margin: 0 auto 20px;
        }
        .hero .cta {
            display: inline-block;
            background: linear-gradient(135deg, var(--red) 0%, var(--red-bright) 100%);
            color: white;
            padding: 14px 36px;
            border-radius: 4px;
            text-decoration: none;
            font-weight: 700;
            font-size: 1.05em;
            transition: all 0.3s;
            letter-spacing: 0.5px;
            text-transform: uppercase;
            border: 1px solid var(--red-bright);
            box-shadow: 0 4px 12px rgba(196,30,58,0.3);
        }
        .hero .cta:hover {
            background: linear-gradient(135deg, var(--red-bright) 0%, #ff4757 100%);
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(196,30,58,0.4);
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 6px;
            padding: 25px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.3);
            transition: all 0.2s;
            border-left: 3px solid var(--green-accent);
        }
        .card:hover {
            transform: translateY(-3px);
            border-color: var(--gold);
            border-left-color: var(--gold);
            box-shadow: 0 8px 24px rgba(0,0,0,0.5);
        }
        .card h3 {
            color: var(--text);
            margin-bottom: 10px;
            font-size: 1.15em;
        }
        .card h3 a { color: var(--text); text-decoration: none; }
        .card h3 a:hover { color: var(--gold-light); }
        .card p { color: var(--text-dim); font-size: 0.92em; }
        .card .tag {
            display: inline-block;
            background: var(--red);
            color: white;
            padding: 3px 10px;
            border-radius: 3px;
            font-size: 0.75em;
            font-weight: 700;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .section-title {
            font-size: 1.5em;
            color: var(--gold);
            margin-bottom: 20px;
            padding-bottom: 8px;
            border-bottom: 2px solid var(--gold);
            display: inline-block;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .article-list {
            list-style: none;
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 6px;
            padding: 25px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.3);
            margin-bottom: 30px;
        }
        .article-list li {
            padding: 14px 0;
            border-bottom: 1px solid var(--border);
        }
        .article-list li:last-child { border-bottom: none; }
        .article-list a {
            color: var(--text);
            text-decoration: none;
            font-weight: 600;
            font-size: 1.02em;
        }
        .article-list a:hover { color: var(--gold-light); }
        .article-list .date {
            color: var(--text-muted);
            font-size: 0.82em;
            display: block;
            margin-top: 3px;
        }
        .seo-section {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 6px;
            padding: 30px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.3);
            margin-bottom: 30px;
        }
        .seo-section h3 { color: var(--gold); margin-bottom: 12px; }
        .seo-section p { color: var(--text-dim); margin-bottom: 14px; }
        footer {
            background: #0a0a0a;
            color: var(--text-muted);
            text-align: center;
            padding: 30px 20px;
            margin-top: 40px;
            border-top: 1px solid var(--border-gold);
        }
        footer a { color: var(--gold); text-decoration: none; }
        footer a:hover { color: var(--gold-light); }
        .banner-wrapper {
            margin-bottom: 24px;
            border-radius: 6px;
            overflow: hidden;
            border: 1px solid var(--border-gold);
            box-shadow: 0 4px 20px rgba(0,0,0,0.5);
        }
        .banner-img {
            width: 100%;
            height: auto;
            display: block;
        }
        .game-cta-section {
            background: linear-gradient(135deg, #121212 0%, #1a1a1a 100%);
            border: 1px solid var(--border-gold);
            border-radius: 6px;
            padding: 24px 30px;
            margin-bottom: 30px;
            text-align: center;
            position: relative;
        }
        .game-cta-section::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 2px;
            background: linear-gradient(90deg, transparent, var(--green-accent), var(--gold), var(--red), transparent);
        }
        .game-cta-section h3 {
            color: var(--gold-light);
            font-size: 1.3em;
            margin-bottom: 8px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .game-cta-section p {
            color: var(--text-dim);
            font-size: 0.95em;
            margin-bottom: 16px;
        }
        .game-link {
            display: inline-block;
            background: linear-gradient(135deg, var(--green-felt) 0%, var(--green-accent) 100%);
            color: #fff;
            padding: 12px 30px;
            border-radius: 4px;
            text-decoration: none;
            font-weight: 700;
            letter-spacing: 0.5px;
            text-transform: uppercase;
            border: 1px solid var(--green-accent);
            box-shadow: 0 4px 12px rgba(46,125,50,0.3);
            transition: all 0.3s;
        }
        .game-link:hover {
            background: linear-gradient(135deg, #388e3c 0%, #43a047 100%);
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(46,125,50,0.5);
        }
        .game-link .gold-text { color: var(--gold-light); }
        .breadcrumb {
            font-size: 0.85em;
            color: var(--text-muted);
            margin-bottom: 20px;
        }
        .breadcrumb a { color: var(--gold); text-decoration: none; }
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
        @media (max-width: 768px) {
            header h1 { font-size: 1.8em; }
            .article-title { font-size: 1.4em; }
            .article-detail { padding: 20px; }
            .game-cta-section { padding: 16px 20px; }
            .seo-section { padding: 20px; }
        }
"""

old_articles = [
    '3-tersangka-yang-kuras-duit-vilmei-miliaran-terancam-5-tahun',
    '6-bandara-ditutup-sementara-imbas-abu-anak-krakatau-terbaru',
    'abu-anak-krakatau-sampai-jakarta-warga-berburu-masker-di-kol',
    'abu-vulkanik-anak-krakatau-masih-menyelimuti-rumah-warga-cip',
    'antrean-penumpang-reschedule-mengular-di-soetta-imbas-erupsi',
    'begini-modus-eks-karyawan-kuras-saldo-tiktok-vilmei-rp-1-28',
    'cybersecurity-2026',
    'daftar-4-bandara-ditutup-sementara-dan-wilayah-terdampak-eru',
    'ekonomi-digital',
    'gubernur-ntt-sebut-pemerkosa-anak-korban-gempa-ntt-sudah-dip',
    'kepala-bmkg-ungkap-erupsi-anak-krakatau-jenis-strombolian-in',
    'menkes-ungkap-3-bahaya-abu-anak-krakatau-kalau-bisa-jangan-k',
    'penutupan-sementara-bandara-soetta-diperpanjang-dampak-erups',
    'penutupan-sementara-bandara-soetta-diperpanjang-sampai-pukul',
    'sambut-musim-hujan-pemulihan-sawah-di-kota-subulussalam-dipe',
    'sejumlah-warga-pandeglang-sesak-napas-akibat-abu-erupsi-anak',
    'sepakbola-terkini',
    'startup-indonesia',
    'teknologi-ai-2026',
    'tips-produktivitas',
    'walkot-sebut-56-santri-sesak-napas-imbas-kebakaran-ponpes-di',
]

count = 0
for name in old_articles:
    idx = os.path.join(berita_dir, name, 'index.html')
    if not os.path.exists(idx):
        print(f'MISSING: {name}')
        continue
    with open(idx, 'r', encoding='utf-8') as f:
        html = f.read()

    # Replace the old style block with new one
    old_style_match = re.search(r'<style>\s*.*?\s*</style>', html, re.DOTALL)
    if old_style_match:
        html = html[:old_style_match.start()] + '<style>\n' + NEW_STYLE.strip() + '\n    </style>' + html[old_style_match.end():]
        with open(idx, 'w', encoding='utf-8') as f:
            f.write(html)
        count += 1
        print(f'UPDATED: {name}')
    else:
        print(f'NO-STYLE: {name}')

print(f'\nDone: {count}/{len(old_articles)} articles updated')