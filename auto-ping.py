#!/usr/bin/env python3
"""
KOMPAS404 Auto-Ping & Feed Submission
Ping search engines + submit RSS to aggregators
Run: python3 auto-ping.py
"""
import urllib.request
import urllib.parse
import sys

SITE_URL = "https://kompas404.github.io"
RSS_URL = "https://kompas404.github.io/rss.xml"
SITEMAP_URL = "https://kompas404.github.io/sitemap.xml"

USER_AGENT = "KOMPAS404-Ping/1.0 (kompas404.github.io)"

# ============================================================
# 1. INDEXNOW (Bing + Yandex + Seznam)
# ============================================================
INDEXNOW_KEY = "e8f3c12a4b564d7f8a2c1e9b6d3f7a01"
INDEXNOW_HOST = "kompas404.github.io"
INDEXNOW_URLS = [
    SITE_URL + "/",
    SITE_URL + "/berita",
    SITE_URL + "/teknologi",
    SITE_URL + "/bisnis",
    SITE_URL + "/olahraga",
    SITE_URL + "/tentang",
    SITE_URL + "/berita/teknologi-ai-2026",
    SITE_URL + "/berita/ekonomi-digital",
    SITE_URL + "/berita/cybersecurity-2026",
    SITE_URL + "/berita/sepakbola-terkini",
    SITE_URL + "/berita/startup-indonesia",
    SITE_URL + "/berita/tips-produktivitas",
]

INDEXNOW_ENDPOINTS = [
    "https://www.bing.com/indexnow",
    "https://yandex.com/indexnow",
    "https://indexnow.seznam.cz/indexnow",
]

print("[1] Submitting via IndexNow...")
import json
payload = json.dumps({
    "host": INDEXNOW_HOST,
    "key": INDEXNOW_KEY,
    "keyLocation": f"{SITE_URL}/indexnow-{INDEXNOW_KEY}.txt",
    "urlList": INDEXNOW_URLS
}).encode("utf-8")

for endpoint in INDEXNOW_ENDPOINTS:
    try:
        req = urllib.request.Request(endpoint, data=payload,
            headers={"Content-Type": "application/json", "User-Agent": USER_AGENT})
        resp = urllib.request.urlopen(req, timeout=10)
        print(f"  OK  {endpoint.split('//')[1].split('/')[0]}: HTTP {resp.status}")
    except Exception as e:
        print(f"  WARN {endpoint.split('//')[1].split('/')[0]}: {e}")

# ============================================================
# 2. SUBMIT RSS TO AGGREGATORS
# ============================================================
RSS_PINGS = [
    ("Feedburner", f"https://feedburner.google.com/fb/a/ping?url={urllib.parse.quote(RSS_URL, safe='')}"),
    ("Superfeedr", f"https://superfeedr.com/publisher/ping?hub.mode=publish&hub.url={urllib.parse.quote(RSS_URL, safe='')}"),
    ("Feedly", f"https://cloud.feedly.com/v3/feed/{urllib.parse.quote(RSS_URL, safe='')}"),
]

print("\n[2] Submitting RSS feed...")
for name, url in RSS_PINGS:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        resp = urllib.request.urlopen(req, timeout=10)
        print(f"  OK  {name}: HTTP {resp.status}")
    except Exception as e:
        print(f"  WARN {name}: {e}")

# ============================================================
# 3. WEBSUB HUBS
# ============================================================
HUBS = [
    "https://websub.flus.io/",
    "https://pubsubhubbub.appspot.com/",
]

print("\n[3] Notifying WebSub hubs...")
for hub in HUBS:
    data = urllib.parse.urlencode({
        "hub.mode": "publish",
        "hub.url": RSS_URL
    }).encode("utf-8")
    try:
        req = urllib.request.Request(hub, data=data,
            headers={"Content-Type": "application/x-www-form-urlencoded", "User-Agent": USER_AGENT})
        resp = urllib.request.urlopen(req, timeout=10)
        print(f"  OK  {hub}: HTTP {resp.status}")
    except Exception as e:
        print(f"  WARN {hub}: {e}")

print("\nDONE - All pings sent!")
print(f"Sitemap: {SITEMAP_URL}")
print(f"RSS Feed: {RSS_URL}")
print(f"Site: {SITE_URL}")
