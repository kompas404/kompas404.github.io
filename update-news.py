#!/usr/bin/env python3
"""
KOMPAS404 - Update Berita Terbaru dari Scraped Data
Membuat folder berita + download gambar Wikimedia untuk setiap artikel
"""
import os
import json
import shutil
from datetime import datetime

BASE = os.path.expanduser(r"C:\Users\ideapad gaming 3\kompas404-seo")

def load_scraped():
    """Load scraped articles from detik.com"""
    with open(os.path.join(BASE, "scraped-detik.json"), "r", encoding="utf-8") as f:
        return json.load(f)

def clean_html(html_content):
    """Remove unwanted elements from HTML"""
    import re
    # Remove scripts, styles, and iframes
    html_content = re.sub(r'<script[^>]*>.*?</script>', '', html_content, flags=re.DOTALL|re.IGNORECASE)
    html_content = re.sub(r'<style[^>]*>.*?</style>', '', html_content, flags=re.DOTALL|re.IGNORECASE)
    html_content = re.sub(r'<iframe[^>]*>.*?</iframe>', '', html_content, flags=re.DOTALL|re.IGNORECASE)
    
    # Remove class and id attributes
    html_content = re.sub(r'\s+class="[^"]*"', '', html_content)
    html_content = re.sub(r'\s+id="[^"]*"', '', html_content)
    html_content = re.sub(r'\s+data-[a-zA-Z0-9]+="[^"]*"', '', html_content)
    
    return html_content.strip()

def format_date(date_str):
    """Format date to Indonesian format"""
    try:
        # Clean up date format (fix double comma issue)
        date_str = date_str.replace(',,', ',')
        
        # Convert "Kamis, 27 Agu 2026 20:35 WIB" to "Kamis, 27 Agu 2026 20:35 WIB"
        parts = date_str.split()
        day_name = parts[0].rstrip(',')  # Kamis (remove trailing comma)
        day = parts[1]  # 27
        month_year = parts[2]  # Agu
        year = parts[3]  # 2026
        time_wib = ' '.join(parts[4:])  # 20:35 WIB
        
        month_map = {
            'Jan': 'Jan', 'Feb': 'Feb', 'Mar': 'Mar', 'Apr': 'Apr',
            'Mei': 'Mei', 'Jun': 'Jun', 'Jul': 'Jul', 'Agu': 'Agu',
            'Sep': 'Sep', 'Okt': 'Okt', 'Nov': 'Nov', 'Des': 'Des'
        }
        
        month = month_map.get(month_year[:3], month_year[:3])
        return f"{day_name}, {day} {month} {year} {time_wib}"
    except:
        # Return cleaned version if parsing fails
        return date_str.replace(',,', ',')

def create_news_folder(slug, title, content_data, image_url):
    """Create news folder and index.html for each article"""
    folder_name = slug[:60].replace('/', '-').replace(' ', '-')
    folder_path = os.path.join(BASE, "berita", folder_name)
    
    # Create folder if not exists
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    # Download and save image
    import requests
    from urllib.parse import urlparse
    
    img_filename = f"art_{folder_name}.jpg"
    img_path = os.path.join(BASE, "images", img_filename)
    
    headers = {"User-Agent": "KOMPAS404-Bot/1.0 (contact: admin@kompas404.my.id)"}
    
    try:
        if image_url and "detik.net.id" in image_url:
            print(f"  Downloading image...", end=" -> ")
            r = requests.get(image_url, headers=headers, timeout=15)
            if r.status_code == 200 and len(r.content) > 5000:
                ext = ".jpg"
                with open(img_path, "wb") as f:
                    f.write(r.content)
                print(f"OK ({len(r.content)//1024}KB)")
                local_image = f"images/{img_filename}"
            else:
                local_image = None
        else:
            local_image = None
    except Exception as e:
        print(f"  Failed: {e}")
        local_image = None
    
    # Prepare data
    formatted_date = format_date(content_data.get("date", ""))
    breadcrumb = title[:40]
    
    # Clean content
    clean_content = clean_html(content_data.get("content", ""))
    
    # Generate index.html template
    base_domain = "https://kompas404.github.io"
    
    # Handle image URL
    final_image = local_image or image_url or f"{base_domain}/images/icon-kompas404.png"
    image_alt = title
    
    if not local_image:
        # Use default placeholder if no image downloaded
        final_image = f"{base_domain}/images/icon-kompas404.png"
    
    html_template = f"""<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{title[:150]}">
    <meta name="keywords" content="KOMPAS404, berita, {breadcrumb.replace(',', '').replace(' ', ',')}">
    <meta name="author" content="KOMPAS404">
    
    <!-- Google Site Verification -->
    <meta name="google-site-verification" content="S7LzXYPST3GjWTL_eVCjp5j78-zTbUPpA35JUrG-fvA" />
    
    <!-- Favicon -->
        <link rel="icon" type="image/webp" sizes="32x32" href="../../iconkompas404.webp">
        <link rel="apple-touch-icon" href="../../iconkompas404.webp">
    <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
    <meta name="googlebot" content="index, follow">
    <link rel="canonical" href="{base_domain}/berita/{folder_name}/">
    <link rel="alternate" type="application/rss+xml" title="KOMPAS404 RSS Feed" href="{base_domain}/rss.xml">

    <!-- Open Graph -->
    <meta property="og:title" content="{title} — Kompas404">
    <meta property="og:description" content="{title[:150]}">
    <meta property="og:image" content="{base_domain}/{final_image}">
    <meta property="og:image:width" content="512">
    <meta property="og:image:height" content="512">
    <meta property="og:type" content="article">
    <meta property="og:url" content="{base_domain}/berita/{folder_name}/">
    <meta property="og:site_name" content="KOMPAS404">
    <meta property="og:locale" content="id_ID">

    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:image" content="{base_domain}/{final_image}">
    <meta name="twitter:title" content="{title} — Kompas404">
    <meta name="twitter:description" content="Berita terbaru dan analisis dari KOMPAS404. Update harian, faktual, terpercaya.">

    <!-- Schema.org structured data -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "NewsArticle",
        "mainEntityOfPage": {{
            "@type": "WebPage",
            "@id": "{base_domain}/berita/{folder_name}/"
        }},
        "headline": "{title}",
        "description": "{title[:150]}",
        "image": {{
            "@type": "ImageObject",
            "url": "{base_domain}/{final_image}",
            "width": 512,
            "height": 512
        }},  
        "datePublished": "{formatted_date}",
        "dateModified": "{formatted_date}",
        "author": {{
            "@type": "Organization",
            "name": "KOMPAS404",
            "url": "{base_domain}"
        }},
        "publisher": {{
            "@type": "Organization",
            "name": "KOMPAS404",
            "logo": {{
                "@type": "ImageObject",
                "url": "{base_domain}/iconkompas404.webp",
                "width": 256,
                "height": 256
            }}
        }},
        "isAccessibleForFree": true,
        "keywords": "{breadcrumb.replace(',', '').replace(' ', ',')}"
    }}
    </script>
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": "KOMPAS404",
        "alternateName": ["KOMPAS404 berita", "KOMPAS 404"],
        "url": "{base_domain}/",
        "description": "Portal berita dan informasi terkini — KOMPAS404",
        "inLanguage": "id-ID",
        "potentialAction": {{
            "@type": "SearchAction",
            "target": "{base_domain}/search?q={{search_term_string}}",
            "query-input": "required name=search_term_string"
        }},
        "license": "https://{base_domain}/tentang/",
        "sameAs": [
            "https://www.facebook.com/kompas404",
            "https://www.twitter.com/kompas404",
            "https://www.instagram.com/kompas404"
        ]
    }}
    </script>
    
    <title>{title} — Kompas404</title>
        <style>
            :root {{
                --bg-dark: #0d0d0d;
                --bg-card: #1a1a1a;
                --bg-card-alt: #121212;
                --gold: #d4a843;
                --gold-light: #f0c75e;
                --gold-dark: #b8922e;
                --red: #c41e3a;
                --red-bright: #e63946;
                --green-accent: #388e3c;
                --text: #e0e0e0;
                --text-dim: #999;
                --text-muted: #777;
                --border: #2a2a2a;
                --border-gold: rgba(212,168,67,0.3);
            }}
            *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, sans-serif;
                background: var(--bg-dark);
                color: var(--text);
                line-height: 1.7;
                background-image:
                    radial-gradient(ellipse at 50% 0%, rgba(212,168,67,0.06) 0%, transparent 70%),
                    radial-gradient(ellipse at 80% 20%, rgba(196,30,58,0.04) 0%, transparent 60%);
            }}
            header {{
                background: linear-gradient(180deg, #0d0d0d 0%, #141414 40%, #1a1a1a 100%);
                color: white;
                padding: 50px 20px;
                text-align: center;
                border-bottom: 3px solid var(--gold);
                position: relative;
            }}
            header::after {{
                content: '';
                position: absolute;
                bottom: -3px;
                left: 0;
                width: 100%;
                height: 1px;
                background: linear-gradient(90deg, transparent, var(--red), var(--gold), var(--red), transparent);
            }}
            .logo-area {{
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 15px;
                margin-bottom: 12px;
            }}
            .logo-area img {{
                height: 56px;
                border-radius: 10px;
                filter: drop-shadow(0 0 10px rgba(212,168,67,0.3));
            }}
            header h1 {{
                font-size: 2em;
                font-weight: 900;
                letter-spacing: 1px;
                text-transform: uppercase;
                background: linear-gradient(180deg, var(--gold-light) 0%, var(--gold) 50%, var(--gold-dark) 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                filter: drop-shadow(0 2px 4px rgba(0,0,0,0.5));
                line-height: 1.3;
            }}
            .meta {{
                margin-top: 10px;
                font-size: 0.9em;
                color: var(--gold);
                opacity: 0.85;
            }}
            .meta span {{
                background: var(--red);
                color: white;
                padding: 2px 10px;
                border-radius: 3px;
                font-weight: 700;
                font-size: 0.8em;
                text-transform: uppercase;
                margin-right: 8px;
            }}
            nav {{
                background: #111;
                padding: 12px 20px;
                display: flex;
                gap: 20px;
                justify-content: center;
                flex-wrap: wrap;
                box-shadow: 0 4px 16px rgba(0,0,0,0.5);
                position: sticky;
                top: 0;
                z-index: 100;
                border-bottom: 1px solid var(--border-gold);
            }}
            nav a {{
                color: var(--text-dim);
                text-decoration: none;
                font-weight: 600;
                padding: 5px 14px;
                border-radius: 4px;
                transition: all 0.2s;
                letter-spacing: 0.5px;
                text-transform: uppercase;
                font-size: 0.82em;
            }}
            nav a:hover {{
                background: var(--gold);
                color: #0d0d0d;
            }}
            .container {{
                max-width: 900px;
                margin: 0 auto;
                padding: 30px 20px;
            }}
            main {{
                background: var(--bg-card);
                border: 1px solid var(--border);
                border-radius: 8px;
                padding: 40px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.4);
                border-top: 3px solid var(--gold);
            }}
            .breadcrumb {{
                color: var(--text-muted);
                font-size: 0.82em;
                margin-bottom: 20px;
                padding-bottom: 15px;
                border-bottom: 1px solid var(--border);
            }}
            .featured-image {{
                width: 100%;
                height: 420px;
                object-fit: cover;
                border-radius: 6px;
                margin-bottom: 30px;
                border: 1px solid var(--border-gold);
                box-shadow: 0 4px 16px rgba(0,0,0,0.4);
            }}
            article {{ max-width: 100%; }}
            article h2 {{
                color: var(--gold-light);
                font-size: 1.4em;
                margin: 30px 0 15px;
            }}
            article p {{
                margin-bottom: 20px;
                text-align: justify;
                color: var(--text);
                font-size: 1.05em;
            }}
            article ul, article ol {{
                margin-bottom: 20px;
                padding-left: 30px;
                color: var(--text);
            }}
            article li {{
                margin-bottom: 10px;
                color: var(--text);
            }}
            footer {{
                text-align: center;
                padding: 30px 20px;
                color: var(--text-muted);
                font-size: 0.85em;
                border-top: 1px solid var(--border);
                margin-top: 40px;
                background: #0a0a0a;
            }}
            footer a {{
                color: var(--gold);
                text-decoration: none;
            }}
            footer a:hover {{
                color: var(--gold-light);
            }}
            @media (max-width: 768px) {{
                header h1 {{ font-size: 1.4em; }}
                .featured-image {{ height: 260px; }}
                main {{ padding: 20px; }}
                .logo-area img {{ height: 44px; }}
            }}
        </style>
    </head>
    <body>
        <nav>
            <a href="{base_domain}/">Home</a>
            <a href="{base_domain}/berita/">Berita</a>
            <a href="{base_domain}/teknologi/">Teknologi</a>
            <a href="{base_domain}/bisnis/">Bisnis</a>
            <a href="{base_domain}/olahraga/">Olahraga</a>
            <a href="{base_domain}/tentang/">Tentang</a>
        </nav>

        <header>
            <div class="logo-area">
                <img src="{base_domain}/iconkompas404.webp" alt="Kompas404">
                <h1>{title}</h1>
            </div>
            <div class="meta">
                <span>{content_data.get('category', 'Umum')}</span>
                {formatted_date}
            </div>
        </header>

        <div class="container">
            <main>
                <div class="breadcrumb">{breadcrumb}</div>

                <img src="{base_domain}/{final_image}" alt="{image_alt}" class="featured-image">

                <article>
                    {clean_content}
                </article>
            </main>
        </div>

        <footer>
            <p>&copy; 2026 <a href="{base_domain}/">KOMPAS404</a>. All rights reserved.</p>
            <p style="margin-top:8px;">
                <a href="{base_domain}/">Home</a> &bull;
                <a href="{base_domain}/berita/">Berita</a> &bull;
                <a href="{base_domain}/tentang/">Tentang</a>
            </p>
        </footer>
    </body>
    </html>"""
    
    # Write index.html
    with open(os.path.join(folder_path, "index.html"), "w", encoding="utf-8") as f:
        f.write(html_template)
    
    return final_image if final_image != f"{base_domain}/images/icon-kompas404.png" else None

def main():
    print("Loading scraped articles...")
    articles = load_scraped()
    print(f"Found {len(articles)} articles")
    
    new_articles = []
    image_paths = {}
    
    for i, art in enumerate(articles):
        slug = art.get("slug", "").replace("/", "-").strip("-")
        title = art.get("title", "")
        content_data = {k: v for k, v in art.items() if k not in ["slug"]}
        image_url = art.get("image")
        
        print(f"\n[{i+1}/{len(articles)}] Processing: {title[:60]}...")
        
        final_img = create_news_folder(slug, title, content_data, image_url)
        
        if final_img:
            image_paths[f"berita/{slug}/"] = final_img
        
        # Save to new-articles.json
        new_articles.append({
            "slug": f"berita/{slug}",
            "title": title,
            "category": content_data.get("category", "Teknologi"),
            "date": format_date(content_data.get("date", "")),
            "image": f"images/art_{slug}.jpg" if final_img else None,
            "image_alt": title,
            "breadcrumb": title[:30],
            "content": content_data.get("content", "")
        })
    
    # Save new-articles.json
    with open(os.path.join(BASE, "new-articles.json"), "w", encoding="utf-8") as f:
        json.dump(new_articles, f, ensure_ascii=False, indent=2)
    print(f"\n✓ Saved {len(new_articles)} articles to new-articles.json")
    
    # Save image-map.json
    with open(os.path.join(BASE, "image-map.json"), "w", encoding="utf-8") as f:
        json.dump(image_paths, f, ensure_ascii=False, indent=2)
    print("✓ Saved image-map.json")
    
    print("\n✅ Process complete!")

if __name__ == "__main__":
    main()
