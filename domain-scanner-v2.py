#!/usr/bin/env python3
"""KOMPAS404 Aged Domain Scanner v2 - Fixed extraction"""
import requests, re, sys

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://www.expireddomains.net/',
}

URL = "https://www.expireddomains.net/expired-domains/"

def fetch():
    resp = requests.get(URL, headers=HEADERS, params={'o':'backlinks','r':'d','start':'0'}, timeout=30)
    return resp.text if resp.status_code == 200 else None

def parse(html):
    """Parse domains from ExpiredDomains HTML"""
    domains = []
    
    # Split into table rows
    rows = html.split('<tr>')
    
    for row in rows:
        # Look for domain link - class is "namelinks" (plural)
        dm = re.search(r'class="namelinks"[^>]*>([^<]+)</a>', row)
        if not dm:
            continue
        domain = dm.group(1).strip()
        
        # Skip obvious spam domains
        skip_words = ['porn', 'xxx', 'sex', 'fuck', 'nude', 'cam', 'dating', 'casino',
                      'gambl', 'poker', 'slot', 'bet', 'pharma', 'viagra', 'cialis',
                      'pill', 'essay', 'loan', 'payday', 'mortgage', 'insurance',
                      'lawyer', 'attorney']
        if any(w in domain.lower() for w in skip_words):
            continue
        
        # Extract all digit cells (backlinks, ref domains, etc.)
        digits = re.findall(r'class="digits"[^>]*>([^<]+)<', row)
        
        # Extract TLD
        tld = domain.rsplit('.', 1)[-1] if '.' in domain else ''
        
        info = {
            'domain': domain,
            'tld': tld,
            'digits': digits,
        }
        
        # Try to parse backlinks (usually first digit column)
        if digits:
            try:
                info['bl'] = int(digits[0].replace(',', '').replace('.', ''))
            except:
                info['bl'] = 0
        else:
            info['bl'] = 0
        
        domains.append(info)
    
    return domains

def main():
    print("=" * 65)
    print("KOMPAS404 — Aged Domain Scanner")
    print("=" * 65)
    
    html = fetch()
    if not html or len(html) < 5000:
        print("ERROR: Can't fetch expireddomains.net")
        sys.exit(1)
    
    print(f"  Fetched: {len(html)} bytes OK")
    
    domains = parse(html)
    print(f"  Parsed: {len(domains)} clean domains\n")
    
    if not domains:
        print("No domains found. Site structure may have changed.")
        sys.exit(1)
    
    # Sort by backlinks descending
    domains.sort(key=lambda x: x['bl'], reverse=True)
    
    # FIX: Prioritize high-value TLDs
    good_tld = {'com', 'net', 'org', 'id', 'io', 'co'}
    
    print(f"{'=' * 65}")
    print(f"{'TOP 30 AGED DOMAINS':^65}")
    print(f"{'=' * 65}")
    print(f"{'#':<3} {'Domain':<35} {'TLD':<6} {'BL':>8}")
    print(f"{'--':<3} {'------':<35} {'---':<6} {'--':>8}")
    
    recommended = []
    shown = 0
    for i, d in enumerate(domains):
        if shown >= 40:
            break
        
        name = d['domain']
        tld = d['tld']
        bl = d['bl']
        
        # Score for recommendation
        score = 0
        if tld in good_tld: score += 2
        if bl >= 100: score += 3
        elif bl >= 50: score += 2
        name_len = len(name.split('.')[0])
        if 4 <= name_len <= 20: score += 1
        
        star = ''
        if score >= 4:
            star = ' ⭐'
            recommended.append(d)
        
        print(f"{shown+1:<3} {name:<35} {tld:<6} {bl:>8,}{star}")
        shown += 1
    
    print(f"\n{'=' * 65}")
    print(f"RECOMMENDED ({len(recommended)} domains):")
    print(f"{'=' * 65}")
    for i, d in enumerate(recommended[:15], 1):
        print(f"  {i:2d}. {d['domain']:40s} BL={d['bl']:,}")
    
    # Save
    out = "C:/Users/ideapad gaming 3/kompas404-seo/aged-domains.txt"
    with open(out, 'w') as f:
        for d in domains:
            f.write(f"{d['domain']}\tBL={d['bl']}\tTLD={d['tld']}\n")
    print(f"\nFull list: {out}")
    
    if recommended:
        print("\n=== NEXT STEPS ===")
        print("1. Pick 3-5 domains from recommended list")
        print("2. Check history: archive.org/web/*/DOMAIN")
        print("3. Check index: google.com/search?q=site:DOMAIN")
        print("4. Buy at: namecheap.com / dynadot.com / godaddy.com")
        print("5. Setup cloaking + point to kompas404.github.io")

if __name__ == '__main__':
    main()
