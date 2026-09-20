#!/usr/bin/env python3
"""
KOMPAS404 - Auto Rewriter + IndexNow URL Generator
Dipanggil dari GitHub Actions setelah scraper-detik.py.

Langkah:
1. Baca scraped-detik.json (hasil scrape detik, verbatim)
2. Rewrite konten jadi unik (indirect speech, parafrase, konteks redaksi)
3. Ganti gambar detik -> free-license (Wikimedia/Commons/Picsum via image-map)
4. Tulis new-articles.json (gabung dengan artikel lama + fresh rewrite)
5. Tulis indexnow-urls.json (daftar URL artikel fresh untuk ping IndexNow)

Catatan: artikel lama di-new-articles.json dipertahankan (pass-through).
"""
import json, os, re, random, sys, difflib

BASE = os.environ.get("GITHUB_WORKSPACE", os.path.expanduser(r"C:\Users\ideapad gaming 3\kompas404-seo"))
random.seed()

# ============ Konfigurasi Rewrite ============
OPENERS = [
    "Jakarta, Kompas404 –", "Kompas404 Newsroom –", "Jakarta, Kompas404 Network –",
    "Nasional, Kompas404 –", "Kompas404 –",
]
CLOSERS = [
    "Perkembangan selanjutnya akan terus dipantau redaksi Kompas404 dan disampaikan kepada pembaca seiring tersedianya informasi baru.",
    "Redaksi Kompas404 akan memperbarui informasi ini apabila terdapat perkembangan lebih lanjut dari pihak terkait.",
    "Kompas404 terus memantau situasi dan akan menyajikan pembaruan bagi pembaca setia.",
]

CONTEXT_PARAS = {
    "Hukum": [
        "Dalam penegakan hukum, transparansi proses penyidikan menjadi kunci kepercayaan publik. Kompas404 mencatat, aparat penegak hukum terus berupaya menuntaskan perkara sesuai ketentuan yang berlaku, termasuk memeriksa setiap pihak yang dinilai memiliki keterkaitan dengan peristiwa tersebut.",
        "Kasus semacam ini kerap menarik perhatian luas karena menyangkut rasa keadilan masyarakat. Karena itu, koordinasi antara penyidik, kejaksaan, dan lembaga terkait dinilai penting agar proses hukum berjalan objektif dan akuntabel.",
    ],
    "Teknologi": [
        "Perkembangan teknologi yang pesat selalu membawa konsekuensi baru, baik dari sisi kapasitas infrastruktur maupun dampak lingkungan. Para pemangku kebijakan pun dituntut menyusun regulasi yang adaptif agar inovasi tetap tumbuh tanpa mengorbankan keberlanjutan.",
        "Kompas404 menilai, era digital menuntut kesiapan sumber daya manusia dan infrastruktur pendukung. Investasi pada riset serta penguatan ekosistem inovasi menjadi faktor penentu daya saing bangsa di tengah persaingan global.",
    ],
    "Transportasi": [
        "Mobilitas masyarakat yang tinggi menuntut sistem transportasi yang aman, nyaman, dan andal. Setiap insiden di jalur transportasi menjadi pengingat pentingnya pengawasan operasional serta prosedur keselamatan yang ketat.",
        "Kompas404 menyoroti pentingnya evaluasi berkala terhadap sarana dan prasarana transportasi. Langkah preventif serta penegakan standar keselamatan dinilai mampu menekan risiko kecelakaan dan gangguan layanan di masa mendatang.",
    ],
    "Bisnis": [
        "Dinamika ekonomi yang bergerak cepat menuntut para pelaku usaha beradaptasi dengan perubahan pasar. Kebijakan yang tepat sasaran serta dukungan rantai pasok yang sehat menjadi fondasi pertumbuhan sektor bisnis nasional.",
        "Kompas404 mencatat, keberlanjutan usaha sangat bergantung pada inovasi dan kemitraan strategis. Pemerintah bersama pelaku industri diharapkan terus mendorong iklim investasi yang kondusif agar daya saing nasional meningkat.",
    ],
    "Politik": [
        "Dinamika politik nasional selalu menjadi perhatian publik karena berdampak langsung pada arah kebijakan. Proses pengambilan keputusan yang partisipatif dan transparan dinilai mampu memperkuat kepercayaan masyarakat terhadap lembaga negara.",
        "Kompas404 menilai, konsolidasi antarlembaga dan komunikasi politik yang sehat menjadi prasyarat penting dalam menjaga stabilitas pemerintahan. Aspirasi masyarakat harus terus ditampung melalui mekanisme yang demokratis.",
    ],
    "Lingkungan": [
        "Persoalan lingkungan kerap menuntut respons cepat karena dampaknya langsung dirasakan masyarakat. Edukasi serta kesiapsiagaan menjadi kunci dalam mengurangi risiko bencana dan menjaga kelestarian alam.",
        "Kompas404 menyoroti pentingnya kolaborasi antara pemerintah, akademisi, dan masyarakat dalam pengelolaan lingkungan. Pendekatan berbasis data dan teknologi dinilai mampu memperkuat upaya mitigasi dan adaptasi.",
    ],
    "Pendidikan": [
        "Akses pendidikan yang merata merupakan investasi jangka panjang bagi kemajuan bangsa. Pemerintah daerah bersama pusat terus berupaya menghadirkan layanan pendidikan berkualitas hingga ke wilayah terpencil.",
        "Kompas404 menilai, pemutakhiran data dan kebijakan berbasis bukti menjadi kunci dalam menuntaskan persoalan pendidikan. Kolaborasi antarpemangku kepentingan diperlukan agar setiap anak mendapatkan hak belajarnya.",
    ],
}

VOCAB = {
    "polisi": "aparat kepolisian",
    "kepolisian": "pihak kepolisian",
    "warga": "masyarakat",
    "masyarakat": "publik",
    "korban": "orang yang terdampak",
    "tersangka": "terduga pelaku",
    "kasus": "perkara",
    "melakukan": "menjalankan",
    "menyebut": "menuturkan",
    "mengatakan": "menyampaikan",
    "menambahkan": "melengkapi keterangan",
    "mengungkap": "membeberkan",
    "membongkar": "menguak",
    "menegaskan": "memastikan",
    "ditangkap": "diamankan aparat",
    "menangkap": "mengamankan",
    "karena": "lantaran",
    "untuk": "guna",
    "dengan": "melalui",
    "saat": "ketika",
    "setelah": "pasca",
    "mengalami": "menghadapi",
    "terjadi": "berlangsung",
    "ditemukan": "terungkap",
    "pemerintah": "pihak pemerintah",
    "daerah": "wilayah",
    "wilayah": "kawasan",
    "miliar": "miliar rupiah",
    "meningkat": "mengalami kenaikan",
    "langkah": "upaya",
    "tindakan": "langkah",
    "bantuan": "dukungan",
    "program": "inisiatif",
    "pembangunan": "pengerjaan",
    "proyek": "program pembangunan",
    "anggaran": "alokasi dana",
    "proses": "rangkaian",
    "hasil": "capaian",
    "kondisi": "situasi",
    "situasi": "keadaan",
    "penanganan": "penanggulangan",
    "pengawasan": "pemantauan",
    "evaluasi": "penilaian",
    "perubahan": "transformasi",
    "penting": "krusial",
    "terkait": "sehubungan dengan",
}

def classify_category(title, content):
    t = ((title or "") + " " + re.sub(r'<[^>]+>', ' ', content or "")).lower()
    rules = [
        (["narkoba", "polisi", "ditangkap", "tersangka", "kejahatan", "hukum", "kriminal", "pidana", "praperadilan", "perkosa", "bunuh", "pembunuhan", "penipuan", "korupsi", "suap", "upal", "uang palsu", "eksploitasi", "tendang", "dalam kasus", "kasus"], "Hukum"),
        (["krl", "kereta", "commuter", "transportasi", "tol", "jalan", "macet", "kendaraan", "bandara", "kapal", "virgo", "evakuasi", "laut", "reschedule", "penumpang", "tronton", "truk"], "Transportasi"),
        (["ruu", "dpr", "paripurna", "undang-undang", "legislasi", "mpr", "politik", "prabowo", "pemilu", "partai", "gerindra", "golkar", "nasdem", "ktt", "presiden", "walikota", "bupati"], "Politik"),
        (["pendidikan", "sekolah", "kampus", "ptn", "mahasiswa", "guru", "siswa", "beasiswa", "pgtc", "putus sekolah", "diklat", "belajar"], "Pendidikan"),
        (["bisnis", "ekonomi", "investasi", "keuangan", "perusahaan", "bawang", "ekspor", "umkm", "brics", "pasar", "budidaya"], "Bisnis"),
        (["sepakbola", "liga", "bola", "pertandingan", "atlet", "olahraga", "timnas"], "Olahraga"),
        (["lingkungan", "hutan", "karhutla", "kebakaran", "alam", "satwa", "konservasi", "erupsi", "abu", "krakatau", "semeru", "iklim", "gunung"], "Lingkungan"),
        (["gempa", "bencana", "banjir", "longsor", "darurat"], "Lingkungan"),
        (["transjakarta", "bus", "angkutan", "rute", "layanan"], "Transportasi"),
        (["teknologi", "kecerdasan buatan", "artificial intelligence", "siber", "digital", "startup", "aplikasi", "software", "hardware", "listrik", "energi"], "Teknologi"),
        (["polwan", "polri", "kapolri", "brimob", "patroli", "razia"], "Hukum"),
    ]
    for kws, cat in rules:
        if any(kw in t for kw in kws):
            return cat
    return "Berita"

def vocab_swap(text):
    if not text:
        return text
    words = text.split()
    out = []
    used = set()
    for w in words:
        key = w.lower().strip("(),;:'\"")
        if key in VOCAB and w.lower() not in used and random.random() < 0.6:
            repl = VOCAB[key]
            if w[0].isupper():
                repl = repl[:1].upper() + repl[1:]
            out.append(repl)
            used.add(w.lower())
        else:
            out.append(w)
    s = " ".join(out)
    s = re.sub(r'\s+', ' ', s).strip()
    s = re.sub(r'\s+([,\.\;])', r'\1', s)
    return s

def to_indirect(sentence, speaker):
    q = sentence.strip().strip('"').strip('\u201c').strip('\u201d').strip()
    q = re.sub(r'\s+', ' ', q)
    if q.startswith('"'):
        q = q[1:]
    if q.endswith('"'):
        q = q[:-1]
    fmt = random.randint(1, 4)
    if fmt == 1:
        return f"{speaker} mengungkapkan, \"{vocab_swap(q)}\""
    elif fmt == 2:
        return f"Menurut keterangan {speaker}, {vocab_swap(q[:1].lower() + q[1:] if q else q)}"
    elif fmt == 3:
        return f"{speaker} menegaskan bahwa {vocab_swap(q[:1].lower() + q[1:] if q else q)}"
    else:
        return f"Dalam penyampaiannya, {speaker} menjelaskan {vocab_swap(q[:1].lower() + q[1:] if q else q)}"

def rewrite_content(content_html, title, category):
    category = classify_category(title, content_html) or category
    paras = re.findall(r'<p>(.*?)</p>', content_html, re.S)
    if not paras:
        paras = [content_html]

    all_sents = []
    for p in paras:
        text = re.sub(r'<[^>]+>', '', p).strip()
        sentences = re.split(r'(?<=[.!?])\s+', text)
        merged_sents = []
        i = 0
        while i < len(sentences):
            cur = sentences[i].strip()
            while i + 1 < len(sentences) and cur.count('"') % 2 == 1 and not re.search(r'[”"]\s*[,.]?\s*(?:ujar|kata|katanya|tutur|ucap|ungkap|jelas|terang)', cur, re.I):
                i += 1
                cur = cur + " " + sentences[i].strip()
            merged_sents.append(cur)
            i += 1
        for s in merged_sents:
            s = s.strip()
            if not s:
                continue
            if re.match(r'^(Dikutip dari|Dalam rekaman|Dari satu titik|Suasananya begitu|Berikut ini|Simak juga|Baca juga)', s, re.I):
                continue
            quote_m = re.search(r'[“"](.+?)[”"]\s*[,.]?\s*(?:ujar|kata|katanya|tutur|ucap|ungkap|jelas|terang)', s, re.I)
            if quote_m:
                content = quote_m.group(1)
                sp = None
                sp_m = re.search(r'(?:ujar|kata|katanya|tutur|ucap|ungkap|jelas|terang)\s+([A-Z][^,\.]{2,60})', s, re.I)
                if sp_m:
                    sp = sp_m.group(1).strip()
                elif re.search(r'([A-Z][^,\.]{3,60})\s+(?:mengatakan|menyebut|menegaskan|menuturkan|mengungkapkan|memastikan)', s):
                    sp = re.search(r'([A-Z][^,\.]{3,60})\s+(?:mengatakan|menyebut|menegaskan|menuturkan|mengungkapkan|memastikan)', s).group(1).strip()
                else:
                    sp = "pejabat terkait"
                all_sents.append(("QUOTE", content, sp))
                rest = s[quote_m.end():].strip(" ,")
                if rest and len(rest) > 25 and not re.match(r'^(ujar|kata|tutur|ucap|jelas|terang|kata)', rest, re.I):
                    all_sents.append(("TEXT", rest, None))
            else:
                all_sents.append(("TEXT", s, None))

    texts = [(t, sp) for typ, t, sp in all_sents if typ == "TEXT"]
    quotes = [(t, sp) for typ, t, sp in all_sents if typ == "QUOTE"]

    rewritten = []
    if texts:
        lead = texts[0][0]
        lead2 = re.sub(r'^(Jakarta|Nasional)[,.]?\s*', '', lead)
        lead2 = re.sub(r'^([A-Z][^,]{3,40}),\s*', r'\1 ', lead2)
        rewritten.append(vocab_swap(lead2))
        if len(texts) > 1 and len(texts[1][0]) < 60:
            rewritten.append(vocab_swap(texts[1][0]))

    for q, sp in quotes:
        rewritten.append(to_indirect(q, sp))

    start = 1 if len(texts) > 1 and len(texts[1][0]) < 60 else 1
    for t, _ in texts[start:]:
        if len(t) > 25:
            tt = vocab_swap(t)
            if len(tt) > 140:
                parts = re.split(r'(?<=[,;])\s+', tt)
                if len(parts) >= 2:
                    mid = len(parts) // 2
                    left = " ".join(parts[:mid]).strip().rstrip(',')
                    right = " ".join(parts[mid:]).strip()
                    if right and left:
                        left = left + "."
                        right = right[:1].upper() + right[1:] if right[0].islower() else right
                        tt = left + " " + right
            rewritten.append(tt)

    if len(rewritten) < 3:
        while len(rewritten) < 3 and rewritten:
            rewritten.append(rewritten[-1])

    opener = random.choice(OPENERS)
    rewritten[0] = f"{opener} {rewritten[0]}"

    ctx_paras = CONTEXT_PARAS.get(category, CONTEXT_PARAS.get("Hukum"))
    if ctx_paras and len(rewritten) >= 3:
        mid = len(rewritten) // 2
        rewritten.insert(mid, random.choice(ctx_paras))

    rewritten.append(random.choice(CLOSERS))

    if len(rewritten) >= 6:
        for i in range(3, len(rewritten) - 1):
            if len(rewritten[i]) < 200 and i != 2 and i != 3:
                p = rewritten.pop(i)
                rewritten.insert(random.randint(2, 3), p)
                break

    return "\n".join(f"<p>{p}</p>" for p in rewritten)


def main():
    scraped_path = os.path.join(BASE, "scraped-detik.json")
    with open(scraped_path, "r", encoding="utf-8") as f:
        scraped = json.load(f)

    image_map_path = os.path.join(BASE, "image-map.json")
    image_map = {}
    if os.path.exists(image_map_path):
        with open(image_map_path, "r", encoding="utf-8") as f:
            image_map = json.load(f)

    prev_path = os.path.join(BASE, "new-articles.json")
    prev = []
    if os.path.exists(prev_path):
        with open(prev_path, "r", encoding="utf-8") as f:
            prev = json.load(f)

    scraped_slugs = set()
    for s in scraped:
        slug = s.get("slug", "")
        if not slug.startswith("berita/"):
            slug = "berita/" + slug
        scraped_slugs.add(slug)

    existing = []
    for a in prev:
        slug = a.get("slug", "")
        if not slug.startswith("berita/"):
            slug = "berita/" + slug
        if slug in scraped_slugs:
            continue
        img = image_map.get(slug, a.get("image", ""))
        existing.append({
            "slug": slug,
            "title": a.get("title", ""),
            "category": a.get("category", "Berita"),
            "breadcrumb": a.get("breadcrumb") or a.get("title", "")[:30],
            "date": a.get("date", ""),
            "image": img if img else "https://kompas404.github.io/images/icon-kompas404.png",
            "image_alt": a.get("image_alt") or a.get("title", "")[:50],
            "content": a.get("content", ""),
        })

    fresh = []
    indexnow_urls = []
    for s in scraped:
        slug = s.get("slug", "")
        if not slug.startswith("berita/"):
            slug = "berita/" + slug
        title = s.get("title", "")
        category = classify_category(s.get("title", ""), s.get("content", ""))
        content_html = s.get("content", "")
        rewritten = rewrite_content(content_html, title, category)

        # Agressive pass kalau masih terlalu mirip dengan detik
        def _clean(h):
            return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', h or '')).strip()
        raw = s.get("content", "")
        sim = difflib.SequenceMatcher(None, _clean(rewritten)[:800], _clean(raw)[:800]).ratio()
        if sim > 0.55:
            paras2 = re.findall(r'<p>(.*?)</p>', rewritten, re.S)
            agg = agressive_pass([f"<p>{p}</p>" for p in paras2])
            rewritten = "\n".join(f"<p>{p}</p>" for p in agg)

        img = image_map.get(slug, s.get("image", ""))
        fresh.append({
            "slug": slug,
            "title": title,
            "category": category,
            "breadcrumb": s.get("breadcrumb") or title[:30],
            "date": s.get("date", ""),
            "image": img if img else "https://kompas404.github.io/images/icon-kompas404.png",
            "image_alt": s.get("image_alt") or title[:50],
            "content": rewritten,
        })
        indexnow_urls.append(f"https://kompas404.github.io/{slug}/")

    all_articles = fresh + existing

    def _date_key(a):
        d = a.get("date", "")
        m = re.search(r'(\d{1,2})\s+(\w+)\s+(\d{4})\s+(\d{1,2}):(\d{2})', d)
        months = {"Jan":1,"Feb":2,"Mar":3,"Apr":4,"Mei":5,"May":5,"Jun":6,"Jul":7,"Agu":8,"Aug":8,"Sep":9,"Okt":10,"Oct":10,"Nov":11,"Des":12,"Dec":12}
        if m:
            dd, mon, y, hh, mm = m.groups()
            return (int(y), months.get(mon[:3], 1), int(dd), int(hh), int(mm))
        m2 = re.search(r'(\d{1,2})\s+(\w+)\s+(\d{4})', d)
        if m2:
            dd, mon, y = m2.groups()
            return (int(y), months.get(mon[:3], 1), int(dd), 0, 0)
        return (0, 0, 0, 0, 0)

    all_articles.sort(key=_date_key, reverse=True)

    with open(os.path.join(BASE, "new-articles.json"), "w", encoding="utf-8") as f:
        json.dump(all_articles, f, ensure_ascii=False, indent=2)

    with open(os.path.join(BASE, "indexnow-urls.json"), "w", encoding="utf-8") as f:
        json.dump(indexnow_urls, f, ensure_ascii=False, indent=2)

    print(f"Rewritten {len(all_articles)} articles (fresh={len(fresh)}, existing={len(existing)})")
    print(f"IndexNow URLs: {len(indexnow_urls)}")


def agressive_pass(body):
    sents = []
    for p in body:
        clean_p = re.sub(r'<[^>]+>', '', p).strip()
        for s in re.split(r'(?<=[.!?])\s+', clean_p):
            s = s.strip()
            if s:
                sents.append(s)
    if len(sents) < 4:
        return body
    sents = [s for s in sents if not re.match(r'^(Kompas404 terus|Redaksi Kompas404|Perkembangan selanjutnya)', s)]
    lead = sents[0]
    rest = sents[1:]
    if len(rest) >= 4:
        mid_i = len(rest) // 2
        moved = rest.pop(mid_i)
        rest.insert(1, moved)
        if len(rest) >= 5:
            moved2 = rest.pop(len(rest) // 2)
            rest.insert(2, moved2)
    paragraphs = []
    cur = lead
    for s in rest:
        if len(cur) + len(s) < 260:
            cur = cur + " " + s
        else:
            paragraphs.append(cur)
            cur = s
    if cur:
        paragraphs.append(cur)
    return paragraphs


if __name__ == "__main__":
    main()
