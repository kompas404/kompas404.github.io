#!/bin/bash
# KOMPAS404 - Ping IndexNow setelah update berita
# Dipanggil dari GitHub Actions setelah push. Pings sitemap + URL baru.
set -euo pipefail

KEY="e8f3c12a4b564d7f8a2c1e9b6d3f7a01"
HOST="kompas404.github.io"
SITEMAP="https://${HOST}/sitemap.xml"

echo "=== PING INDEXNOW (sitemap) ==="
curl -sS -w "\nHTTP %{http_code}\n" \
  "https://api.indexnow.org/indexnow?url=${SITEMAP}&key=${KEY}" || echo "sitemap ping failed"

# Kalau ada file daftar URL baru (dibuat oleh generate step), submit
if [[ -f "indexnow-urls.json" ]]; then
  echo "=== PING INDEXNOW (URL baru dari indexnow-urls.json) ==="
  python3 - <<'PYEOF'
import json
key = "e8f3c12a4b564d7f8a2c1e9b6d3f7a01"
host = "kompas404.github.io"
try:
    with open("indexnow-urls.json", "r", encoding="utf-8") as f:
        urls = json.load(f)
    if not urls:
        print("No URLs to submit")
        raise SystemExit(0)
    payload = {
        "host": host,
        "key": key,
        "keyLocation": f"https://{host}/{key}.txt",
        "urlList": urls,
    }
    import urllib.request
    req = urllib.request.Request(
        "https://api.indexnow.org/indexnow",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        print(f"IndexNow response: HTTP {resp.status}")
except FileNotFoundError:
    print("indexnow-urls.json not found, skipping URL submission")
except Exception as e:
    print(f"IndexNow URL submission error: {e}")
PYEOF
else
  echo "Tidak ada indexnow-urls.json, cuma ping sitemap"
fi

echo "=== DONE ==="
