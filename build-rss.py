#!/usr/bin/env python3
"""KOMPAS404 - Build RSS feed dynamically from new-articles.json"""
import json
import os
import re
from datetime import datetime, timedelta, timezone

BASE = os.environ.get("GITHUB_WORKSPACE", r"C:\Users\ideapad gaming 3\kompas404-seo")

MONTHS_ID = {
    "Jan": "Jan", "Feb": "Feb", "Mar": "Mar", "Apr": "Apr", "Mei": "May",
    "Jun": "Jun", "Jul": "Jul", "Agu": "Aug", "Sep": "Sep", "Okt": "Oct",
    "Nov": "Nov", "Des": "Dec",
}

def parse_id_date(s):
    """Parse 'Rabu, 16 Sep 2026 20:28 WIB' or '16 September 2026' -> datetime (UTC+7 naive)"""
    if not s:
        return None
    m = re.search(r'(\d{1,2})\s+(\w+)\s+(\d{4})(?:\s+(\d{1,2}):(\d{2}))?', s)
    if not m:
        return None
    dd, mon, y = m.group(1), m.group(2), m.group(3)
    hh = int(m.group(4) or 0)
    mm = int(m.group(5) or 0)
    months = {
        "Jan":1,"Feb":2,"Mar":3,"Apr":4,"Mei":5,"May":5,"Jun":6,"Jul":7,
        "Agu":8,"Aug":8,"Sep":9,"Okt":10,"Oct":10,"Nov":11,"Des":12,"Dec":12,
    }
    mo = months.get(mon[:3])
    if not mo:
        return None
    return datetime(int(y), mo, int(dd), hh, mm, tzinfo=timezone(timedelta(hours=7)))

def rfc822(dt):
    if dt is None:
        dt = datetime.now(timezone(timedelta(hours=7)))
    # RFC 822: 'Wed, 16 Sep 2026 20:28:00 +0700'
    days = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
    months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    return f"{days[dt.weekday()]}, {dt.day:02d} {months[dt.month-1]} {dt.year} {dt.hour:02d}:{dt.minute:02d}:{dt.second:02d} +0700"

def clean_text(s):
    s = re.sub(r'<[^>]+>', ' ', s or '')
    s = re.sub(r'\s+', ' ', s).strip()
    return s

def main():
    with open(os.path.join(BASE, "new-articles.json"), "r", encoding="utf-8") as f:
        arts = json.load(f)

    # Sort newest first (already should be, but be safe)
    def key(a):
        dt = parse_id_date(a.get("date", ""))
        return dt.timestamp() if dt else 0
    arts = sorted(arts, key=key, reverse=True)

    items = []
    for a in arts[:25]:  # top 25
        title = clean_text(a.get("title", "")) or "KOMPAS404 Berita"
        slug = a.get("slug", "").lstrip("/")
        link = f"https://kompas404.github.io/{slug}"
        desc = clean_text(a.get("content", ""))[:250]
        cat = a.get("category", "Berita")
        dt = parse_id_date(a.get("date", ""))
        items.append(f"""    <item>
        <title>{title} — KOMPAS404</title>
        <link>{link}</link>
        <description>{desc}</description>
        <pubDate>{rfc822(dt)}</pubDate>
        <category>{cat}</category>
    </item>""")

    now = datetime.now(timezone(timedelta(hours=7)))
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
    <title>KOMPAS404 - Portal Berita &amp; Informasi Terkini</title>
    <link>https://kompas404.github.io</link>
    <description>KOMPAS404 menyajikan berita terbaru, analisis tajam, dan informasi faktual setiap hari. Teknologi, bisnis, olahraga, lifestyle.</description>
    <language>id-ID</language>
    <lastBuildDate>{rfc822(now)}</lastBuildDate>
    <pubDate>{rfc822(now)}</pubDate>
    <generator>KOMPAS404 RSS Generator</generator>
    <image>
        <url>https://kompas404.github.io/logo-kompas404.png</url>
        <title>KOMPAS404</title>
        <link>https://kompas404.github.io</link>
        <width>160</width>
        <height>160</height>
    </image>
    <atom:link href="https://kompas404.github.io/rss.xml" rel="self" type="application/rss+xml"/>

{chr(10).join(items)}
</channel>
</rss>
"""
    with open(os.path.join(BASE, "rss.xml"), "w", encoding="utf-8") as f:
        f.write(xml)
    print(f"RSS built with {len(items)} items")

if __name__ == "__main__":
    main()
