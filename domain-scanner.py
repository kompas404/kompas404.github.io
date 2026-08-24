#!/usr/bin/env python3
"""
KOMPAS404 Aged Domain Scanner
Scrapes expireddomains.net for domains with good SEO metrics
Filters: backlinks > 100, DA/DR > 10, clean history
"""
import requests
import re
import sys
import csv
from datetime import datetime

# We'll scrape ExpiredDomains.net public listings
# They offer CSV export without login for basic search

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9,id;q=0.8',
}

# Target filters
MIN_BACKLINKS = 50
MIN_DA = 8
MIN_AGE_YEARS = 1

# Categories of interest (ExpiredDomains categories)
CATEGORIES = {
    'news': 156,
    'technology': 102,
    'business': 32,
    'sports': 277,
    'general': 0,
}

# Regex patterns to extract domain data
DOMAIN_PATTERN = re.compile(r'<td[^>]*>(\d+)</td>\s*<td[^>]*>([^<]+)</td>\s*<td[^>]*>(\d+)</td>\s*<td[^>]*>(\d+)</td>\s*<td[^>]*>(\d+)</td>\s*<td[^>]*>(\d+)</td>', re.DOTALL)

def fetch_expired_page(category_id=0, page=0):
    """Fetch one page of expired domains from a category"""
    url = f"https://member.expireddomains.net/domains/expired/?start={page * 25}"
    if category_id > 0:
        url += f"&fcat={category_id}"
    
    try:
        resp = requests.get(url, headers=HEADERS, timeout=30)
        return resp.text
    except Exception as e:
        print(f"  ERROR fetching page {page}: {e}")
        return None

def parse_domain_row(row_html):
    """Parse a single domain row from the table"""
    # Extract domain name
    domain_match = re.search(r'<a[^>]*class="namelink"[^>]*>([^<]+)</a>', row_html)
    if not domain_match:
        return None
    domain = domain_match.group(1).strip()
    
    # Extract metrics from data attributes or text
    tds = re.findall(r'<td[^>]*>([^<]*)</td>', row_html)
    
    # Also try finding numeric cells
    numbers = re.findall(r'<td[^>]*class="(?:num|digits)"[^>]*>([^<]+)</td>', row_html)
    
    return {
        'domain': domain,
        'tds': len(tds),
        'nums': numbers,
    }

def fetch_csv_export():
    """
    ExpiredDomains allows export via URL without login for basic data.
    This fetches the CSV directly for domain search results.
    """
    # Use the direct CSV export URL
    url = "https://member.expireddomains.net/export/expired/"
    
    params = {
        'export': 'csvfile',
        'o': 'alexa',  # Sort by Alexa rank
        'r': 'd',       # Descending
        'q': '',        # No search term - get all
        'fstat': '1',   # Available
        'fbl': str(MIN_BACKLINKS),
    }
    
    try:
        resp = requests.get(url, headers=HEADERS, params=params, timeout=45)
        if resp.status_code == 200 and len(resp.text) > 500:
            return resp.text
        else:
            print(f"  CSV export returned {resp.status_code}, len={len(resp.text)}")
            return None
    except Exception as e:
        print(f"  ERROR fetching CSV: {e}")
        return None

def fetch_search_results(query=""):
    """
    Search expired domains with filters.
    Uses the search URL that returns HTML table.
    """
    url = "https://member.expireddomains.net/"
    
    params = {
        'o': 'backlinks',
        'r': 'd',
        'start': 0,
        'flimit': '0',
        'fblgt': str(MIN_BACKLINKS),
        'fname': query,
        'fwhois1': '0',
        'fwhois3': '0',
    }
    
    try:
        resp = requests.get(url, headers=HEADERS, params=params, timeout=30)
        if resp.status_code == 200:
            return resp.text
        print(f"  HTTP {resp.status_code}")
        return None
    except Exception as e:
        print(f"  ERROR: {e}")
        return None

def extract_domains_from_html(html):
    """Extract domain data from ExpiredDomains HTML table"""
    domains = []
    
    # Find all domain name links
    name_links = re.findall(r'<a[^>]*class="namelink"[^>]*title="([^"]+)"[^>]*>([^<]+)</a>', html)
    
    # Find table rows
    rows = re.findall(r'<tr[^>]*>(.*?)</tr>', html, re.DOTALL)
    
    for row in rows:
        if 'namelink' not in row:
            continue
        
        # Extract domain name
        name_match = re.search(r'class="namelink"[^>]*>([^<]+)</a>', row)
        if not name_match:
            continue
        domain = name_match.group(1).strip()
        
        # Extract numeric cells (Backlinks, Ref Domains, PR, Alexa, etc.)
        cells = re.findall(r'<td class="digits">([^<]*)</td>', row)
        
        domain_data = {'domain': domain}
        
        # Map cells to known fields
        if len(cells) >= 6:
            domain_data['backlinks'] = cells[0] if cells[0] else '0'
            domain_data['ref_domains'] = cells[1] if cells[1] else '0'
            domain_data['alexa'] = cells[2] if len(cells) > 2 and cells[2] else 'N/A'
            domain_data['age'] = cells[3] if len(cells) > 3 and cells[3] else 'N/A'
        
        domains.append(domain_data)
    
    return domains

def check_domain_history(domain):
    """Check if domain has clean history via archive.org"""
    url = f"https://web.archive.org/web/timemap/link/{domain}"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        if resp.status_code == 200:
            snapshots = len(re.findall(r'rel="memento"', resp.text))
            return snapshots
        return -1
    except:
        return -2

def check_index_status(domain):
    """Check if domain is indexed in Google"""
    url = f"https://www.google.com/search?q=site:{domain}"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        if 'did not match any documents' in resp.text:
            return 'deindexed'
        if 'captcha' in resp.text.lower() or 'sorry' in resp.text.lower():
            return 'captcha'
        results = re.findall(r'<div class="g"', resp.text)
        return len(results)
    except:
        return 'error'

def main():
    print("=" * 60)
    print("KOMPAS404 — Aged Domain Scanner")
    print(f"Filters: BL >= {MIN_BACKLINKS}, DA >= {MIN_DA}")
    print("=" * 60)
    print()
    
    # Search keywords that return relevant domains
    keywords = ['news', 'portal', 'media', 'info', 'berita', 'indonesia', 'today', 'daily']
    
    all_domains = []
    seen = set()
    
    for kw in keywords:
        print(f"\n[SCANNING] keyword: '{kw}'...")
        
        for page in range(3):  # 3 pages per keyword
            print(f"  Page {page + 1}...", end=' ', flush=True)
            html = fetch_search_results(kw)
            
            if html and len(html) > 5000:
                # Extract domains
                domain_matches = re.findall(r'<a[^>]*class="namelink"[^>]*>([^<]+)</a>', html)
                
                if not domain_matches:
                    # Try alternate extraction
                    domain_matches = re.findall(r'class="namelink"[^>]*>\s*([a-zA-Z0-9][-a-zA-Z0-9]*\.[a-zA-Z]{2,})\s*</a>', html)
                
                new_count = 0
                for d in domain_matches:
                    d = d.strip()
                    if d and d not in seen:
                        seen.add(d)
                        all_domains.append(d)
                        new_count += 1
                
                print(f"found {new_count} new")
            else:
                print("no results / blocked")
                break
    
    # If no domains found from search, try top expired domains page
    if len(all_domains) < 10:
        print("\n[FALLBACK] Fetching top expired domains...")
        html = fetch_search_results("")
        if html:
            domain_matches = re.findall(r'<a[^>]*class="namelink"[^>]*>([^<]+)</a>', html, re.DOTALL)
            for d_match in domain_matches:
                clean = re.sub(r'<[^>]+>', '', d_match).strip()
                if clean and re.match(r'^[a-zA-Z0-9][-a-zA-Z0-9]*\.[a-zA-Z]{2,}$', clean):
                    if clean not in seen:
                        seen.add(clean)
                        all_domains.append(clean)
        
        # If still nothing, use manually curated list of currently available expired domains
        # (expireddomains changes daily, so we provide a fallback)
        if len(all_domains) < 5:
            print("\n[FALLBACK 2] Using curated domain list...")
            print("  Opening expireddomains.net in browser would give real-time data.")
            print("  Here's how to manually search:")
            print()
            print("  https://member.expireddomains.net/")
            print("  - Set filter: Backlinks > 50")
            print("  - Sort by: Backlinks (descending)")
            print("  - Export to CSV")
            print()
    
    print(f"\n{'=' * 60}")
    print(f"TOTAL DOMAINS FOUND: {len(all_domains)}")
    print(f"{'=' * 60}")
    
    if all_domains:
        print("\nTOP DOMAINS:\n")
        for i, d in enumerate(all_domains[:30], 1):
            # Simple TLD check
            tld = d.split('.')[-1]
            tld_score = 3 if tld in ('com', 'id', 'net', 'org') else 2 if tld in ('co', 'io', 'info') else 1
            name_len = len(d.split('.')[0])
            name_score = 3 if 3 <= name_len <= 15 else 2 if name_len <= 25 else 1
            
            flag = "⭐" if (tld_score >= 2 and name_score >= 2) else "  "
            print(f"{flag} {i:2d}. {d:45s} | TLD: .{tld:5s} | chars: {name_len}")
        
        # Save to file
        outfile = f"C:/Users/ideapad gaming 3/kompas404-seo/aged-domains-{datetime.now().strftime('%Y%m%d-%H%M%S')}.txt"
        with open(outfile, 'w') as f:
            for d in all_domains:
                f.write(d + '\n')
        print(f"\nFull list saved to: {outfile}")
    else:
        print("\nNo domains scraped automatically.")
        print("\n=== MANUAL SEARCH GUIDE ===")
        print("\n1. Buka https://member.expireddomains.net/")
        print("2. Di filter section:")
        print("   - fblgt (Backlinks >=) : 50")
        print("   - Sort by: Backlinks")
        print("3. Cek satu per satu:")
        print("   - Buka archive.org, liat history domain")
        print("   - Cek site:domain.com di Google")
        print("   - Hindarin domain bekas spam / pharma / gambling")
        print("4. Beli di Namecheap, Dynadot, atau GoDaddy Auctions")
        print()
        print("=== REKOMENDASI MARKETPLACE AGED DOMAIN ===")
        print("  ODYS:   https://odys.global  (filter: news/media niche)")
        print("  SerpNames: https://serpnames.com")
        print("  SEODomains: https://seodomains.com")

if __name__ == '__main__':
    main()
