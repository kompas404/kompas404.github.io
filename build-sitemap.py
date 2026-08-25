import os
import xml.etree.ElementTree as ET
from datetime import datetime

BASE = r"C:\Users\ideapad gaming 3\kompas404-seo"
today = datetime.now().strftime("%Y-%m-%d")

# All pages - WITH trailing slash for consistency
pages = [
    ("/", 1.0, "daily"),
    ("/berita/", 0.9, "daily"),
    ("/teknologi/", 0.8, "daily"),
    ("/bisnis/", 0.8, "daily"),
    ("/olahraga/", 0.7, "daily"),
    ("/tentang/", 0.5, "monthly"),
]

# Add article pages from berita/
berita_dir = os.path.join(BASE, "berita")
if os.path.exists(berita_dir):
    for name in sorted(os.listdir(berita_dir)):
        article_path = os.path.join(berita_dir, name)
        if os.path.isdir(article_path) and name != "index.html":
            pages.append((f"/berita/{name}/", 0.7, "weekly"))

# Build XML with proper namespace
ns = "http://www.sitemaps.org/schemas/sitemap/0.9"
urlset = ET.Element("urlset", xmlns=ns)

for loc, priority, freq in pages:
    url = ET.SubElement(urlset, "url")
    ET.SubElement(url, "loc").text = f"https://kompas404.github.io{loc}"
    ET.SubElement(url, "lastmod").text = today
    ET.SubElement(url, "changefreq").text = freq
    ET.SubElement(url, "priority").text = str(priority)

tree = ET.ElementTree(urlset)
tree.write(os.path.join(BASE, "sitemap.xml"), encoding="UTF-8", xml_declaration=True)

# Pretty print
import re
with open(os.path.join(BASE, "sitemap.xml"), "r", encoding="utf-8") as f:
    content = f.read()

# Add newlines after each url entry
content = content.replace("></url>", ">\n</url>")
content = content.replace("><url>", ">\n<url>")

with open(os.path.join(BASE, "sitemap.xml"), "w", encoding="utf-8") as f:
    f.write(content)

print(f"Sitemap generated with {len(pages)} URLs")
print(f"Date: {today}")
print("Sample URLs:")
for loc, _, _ in pages[:5]:
    print(f"  https://kompas404.github.io{loc}")
