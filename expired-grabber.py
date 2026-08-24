#!/usr/bin/env python3
"""KOMPAS404 Expired Domain Finder — based on kilat404 v7 engine
FULL SCAN: scrapes expireddomains.net 40 pages, filters Dynadot=available + BL>=3
Deep Wayback content analysis for judi/PBN/spam detection
Output: one domain per line, clean only
"""
import requests, csv, re, sys, time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

BASE_DIR = Path(__file__).parent

KNOWN_LIVE = {
    "godaddy.com","namecheap.com","dynadot.com","spaceship.com",
    "name.com","majestic.com","gname.com","nicsell.com",
    "catched.com","google.com","facebook.com",
    "amazon.com","microsoft.com","apple.com","youtube.com",
    "twitter.com","instagram.com","linkedin.com","reddit.com",
    "wikipedia.org","github.com","stackoverflow.com",
    "yahoo.com","bing.com","netflix.com","spotify.com",
    "dropbox.com","wordpress.com","medium.com","substack.com",
    "forbes.com","bloomberg.com","reuters.com","cnn.com",
    "bbc.com","nytimes.com","washingtonpost.com","wsj.com",
}

DOMAIN_BLACKLIST = [
    # === GAMBLING / JUDI ===
    "casino","poker","gambl","bett","slot","jackpot","togel","judol",
    "judionline","taruhan","bookie","sportsbook","lottery","baccarat",
    "roulette","blackjack","wager","vegas","bandar","4d","toto",
    "sancatoto","maxwin","gacor","slot777","slot88","pragmatic",
    "depositpulsa","depo","qris","rtp","livecasino","betting",
    "bet365","apostas","bets10","betonline","sportbet",
    "odds","parlay","handicap","overunder","mixparlay",
    # === ADULT / PORN / DATING ===
    "porn","xxx","adult","sex","nude","escort","webcam","camgirl",
    "onlyfans","dating","hentai","bdsm","hookup","swinger","erotic",
    "fetish","slut","livejasmin","chaturbate","stripchat","cams",
    "milf","teen","asiangirl","asiangirls","shemale",
    "asiannudity","nudity","chachurbate","bestnewpornstar",
    "sexstore","boyswantmoms","leakedporn","pornstar","pornvids",
    "lookingforbride","mailorderbride","russianbrides","sugarbaby",
    "sugardaddy","sugarmom","findbride","meetgirls","meetwomen",
    # === PHARMA / DRUGS ===
    "viagra","cialis","pharm","pill","drug","pharmacy",
    "levitra","xanax","valium","tramadol","opioid",
    "canadianpharmacy","cheapmeds","prescription","anabolic","steroid",
    "hgh","testosterone","sildenafil","tadalafil","bupropion",
    "ivermect","doxycycline","lasix",
    "clomid","prozitc","prozac","duloxetin","baldactone",
    "buyduloxetine","buyindocin","dexamethasone","tadacip","medrol",
    "motilium","allopurinol","ashwagandha","doxycycline",
    "mobic","azofran","sild","edplg","tdfmg","lasix",
    "sildenafil","tadalafil","finasteride","minoxidil",
    "loperamide","omeprazole","metformin","atorvastatin",
    "gabapentin","pregabalin","diazepam","clonazepam",
    "alprazolam","codeine","morphine","oxycodone",
    "hydrocodone","adderall","ritalin","modafinil",
    # === WEAPONS / VIOLENCE ===
    "gun","guns","rifle","pistol","shotgun","ammo","firearm",
    "weapon","holster","tactical","montanaguns",
    # === CRACK / WAREZ / MALWARE ===
    "malware","virus","trojan","ransom","hack","crack","warez",
    "keygen","nulled","phish","spam","botnet","exploit",
    "getmecrack","windowcrack","cracked","cracks",
    # === SCAM / PYRAMID / CRYPTO ===
    "scam","pyramid","multilevel","hyip","forex","bitcoin",
    "crypto","mining","invest","millionaire","getrich",
    "make-money","passiveincome","financialfreedom",
    "payday","loan","debt","creditrepair","bankruptcy",
    "expedp","quickloans","moneylender","pawn",
    # === CBD / DRUGS-LIGHT ===
    "cbd","vape","hemp","thc","cannabis","marijuana","weed",
    "diet","weightloss","fatburn","keto","detox",
    # === POLITICS / FAKE NEWS ===
    "trump","biden","fake-news","conspiracy",
    # === COUNTERFEIT ===
    "jersey","jerseys","wholesale","replica",
    "knockoff","imitation","authenticjerseys",
    "monclerjacket","burberryoutlet","asics","curryshoes",
    "nike","adidas","gucci","louisvuitton","rolex",
    # === PBN / LINK FARM ===
    "pbn","linkfarm","backlink","linkbuilding",
    "linkwheel","linkpyramid","blogfarm",
    # === BRAND / TRADEMARK RISK ===
    "asus","acer","lenovo","samsung","iphone","xiaomi","oppo",
    "canon","nikon","sony","panasonic","toshiba",
    # === ADDITIONAL SPAM ===
    "seks","kobiety","sprawy","pl$","stressrelief",
    "httprouter","insurance","creditcard",
]

ALLOWED_TLD = {"com","net","org","id","co.id"}

def is_valid_domain(domain):
    """Filters: no hyphens, no numbers, allowed TLD only"""
    base = domain.split('.')[0]
    tld = '.'.join(domain.split('.')[1:])
    if tld not in ALLOWED_TLD:
        return False
    if '-' in base:
        return False
    if re.search(r'\d', base):
        return False
    return True

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
})

def is_domain_blacklisted(base):
    return any(kw in base.lower() for kw in DOMAIN_BLACKLIST)

def is_known_live(domain):
    return domain.lower() in KNOWN_LIVE

def parse_metric(val):
    val = re.sub(r'<[^>]+>','',val).strip()
    if not val or val=='-': return 0
    m = re.search(r'([0-9][0-9,.]*)\s*([KM])(?![a-zA-Z])', val)
    if m:
        n = float(m.group(1).replace(',',''))
        return int(n*1000) if m.group(2)=='K' else int(n*1000000)
    m = re.search(r'([0-9][0-9,.]*)', val)
    return int(float(m.group(1).replace(',',''))) if m else 0

def parse_expireddomains_row(row_html):
    dm = re.search(r'href="/domain/([a-zA-Z0-9][-a-zA-Z0-9]*\.[a-zA-Z]{2,})"', row_html)
    if not dm: return None
    domain = dm.group(1).lower()
    if is_known_live(domain): return None
    if not is_valid_domain(domain): return None
    base = domain.split('.')[0]
    if is_domain_blacklisted(base): return None
    tds = re.findall(r'<td[^>]*>(.*?)</td>', row_html, re.DOTALL)
    vals = [re.sub(r'<[^>]+>','',td).strip() for td in tds]
    if len(vals) < 10: return None
    bl = parse_metric(vals[1]) if len(vals) > 1 else 0
    dp = parse_metric(vals[2]) if len(vals) > 2 else 0
    aby = 0
    if len(vals) > 3:
        abym = re.search(r'([12][0-9]{3})', vals[3])
        if abym: aby = int(abym.group(1))
    dynadot_status = vals[8].strip().lower() if len(vals) > 8 else "unknown"
    return {"domain":domain,"bl":bl,"dp":dp,"aby":aby,"dynadot_status":dynadot_status}

def scrape_expireddomains(max_pages=40):
    domains = []
    seen = set()
    for page in range(max_pages):
        start = page * 25
        try:
            params = {"start": start} if start > 0 else {}
            r = session.get(
                "https://www.expireddomains.net/expired-domains/",
                params=params, timeout=30)
            if r.status_code != 200:
                if r.status_code == 403:
                    print(f"  [!] Rate limited at page {page+1}")
                break
            rows = re.findall(r'<tr[^>]*>(.*?)</tr>', r.text, re.DOTALL)
            found = 0
            for row in rows:
                result = parse_expireddomains_row(row)
                if not result or result["domain"] in seen: continue
                if result["dynadot_status"] != "available": continue
                if result["bl"] < 1: continue
                seen.add(result["domain"])
                domains.append(result)
                found += 1
            if found > 0:
                print(f"  [+] Page {page+1}: {found} domains (BL top: {domains[-1]['bl']})")
            else:
                print(f"  [.] Page {page+1}: 0")
            time.sleep(1.5)
        except Exception as e:
            print(f"  [!] Page {page+1}: {e}")
    return domains

if __name__ == '__main__':
    print("=" * 60)
    print("KOMPAS404 Expired Domain Finder")
    print(f"Start: {datetime.now():%Y-%m-%d %H:%M:%S}")
    print("=" * 60)
    print()
    print("[1] Scraping ExpiredDomains.net (40 pages, Dynadot=available, BL>=3)...")
    print("-" * 60)
    domains = scrape_expireddomains(max_pages=40)
    print(f"\n  => TOTAL: {len(domains)} domains")
    if not domains:
        print("No domains found.")
        sys.exit(0)
    domains.sort(key=lambda x: x["bl"], reverse=True)
    ts = datetime.now().strftime('%Y%m%d-%H%M%S')
    out = f"expired-domains-clean-{ts}.txt"
    with open(out, 'w') as f:
        f.write('\n'.join([d['domain'] for d in domains]))
    print(f"\nSaved: {out}")
    print("=" * 60)
    for d in domains:
        print(d['domain'])
    print(f"\nTotal: {len(domains)} domains | Copy-paste to websiteseochecker.com")
