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
        # Convert "Kamis, 27 Agu 2026 20:35 WIB" to "Kamis, 27 Agu 2026 20:35 WIB"
        parts = date_str.split()
        day_name = parts[0]  # Kamis
        day = parts[1]  # 27
        month_year = parts[2]  # Agu
        time_wib = ' '.join(parts[3:])  # 20:35 WIB
        
        month_map = {
            'Jan': 'Jan', 'Feb': 'Feb', 'Mar': 'Mar', 'Apr': 'Apr',
            'Mei': 'Mei', 'Jun': 'Jun', 'Jul': 'Jul', 'Agu': 'Agu',
            'Sep': 'Sep', 'Okt': 'Okt', 'Nov': 'Nov', 'Des': 'Des'
        }
        
        month = month_map.get(month_year[:3], month_year[:3])
        return f"{day_name}, {day} {month} {day[3:] if len(day) > 1 else day} {time_wib}"
    except:
        return date_str

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
        body {{ font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.8; color: #333; background: #f5f5f5; margin: 0; }}
        .container {{ max-width: 1000px; margin: 0 auto; padding: 20px; }}
        header {{ background: linear-gradient(135deg, #1678f2 0%, #0d4ba3 100%); color: white; padding: 60px 20px; text-align: center; }}
        h1 {{ font-size: 32px; margin: 10px 0; }}
        .meta {{ opacity: 0.9; font-size: 14px; }}
        main {{ background: white; padding: 40px; border-radius: 8px; margin-top: -20px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); position: relative; }}
        .featured-image {{ width: 100%; height: 400px; object-fit: cover; border-radius: 8px; margin-bottom: 30px; }}
        .breadcrumb {{ color: #666; font-size: 14px; margin-bottom: 15px; }}
        h2 {{ color: #1678f2; margin-top: 30px; }}
        p {{ margin-bottom: 18px; text-align: justify; }}
        ul, ol {{ margin-bottom: 20px; padding-left: 30px; }}
        li {{ margin-bottom: 10px; }}
        footer {{ text-align: center; padding: 40px 20px; color: #666; font-size: 14px; }}
        @media (max-width: 768px) {{ h1 {{ font-size: 24px; }} .featured-image {{ height: 250px; }} main {{ padding: 20px; }} }}
    </style>
</head>
<body>
    <header>
        <h1>{title}</h1>
        <div class="meta">
            <span>Kategori: {content_data.get('category', 'Umum')}</span> • 
            <span>{formatted_date}</span>
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
        <p>&copy; 2026 KOMPAS404. All rights reserved.</p>
        <p><a href="{base_domain}" style="color: #1678f2;">Home</a> | <a href="{base_domain}/berita/" style="color: #1678f2;">Berita</a></p>
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
            "image_alt": title
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
