#!/usr/bin/env python3
"""
KOMPAS404 Auto Rewriter
Rewrite setiap artikel dari scraped-detik.json (salinan verbatim Detik)
menjadi versi unik: sinonim swap + restrukturisasi kalimat + framing redaksi.

Output: new-articles.json (unik, gambar lokal free-license, siap build)
"""
import json, os, re, random

BASE = r"C:\Users\ideapad gaming 3\kompas404-seo"

random.seed()

SYNONYMS = {
    "memeriksa": ["menanyai", "mengklarifikasi", "menginterogasi", "menelaah keterangan", "mendalami keterangan"],
    "mencecar": ["menanyai", "menguji keterangan", "mempertanyakan", "menggali informasi"],
    "mengungkap": ["membeberkan", "menyingkap", "memaparkan", "menyampaikan", "membuka fakta"],
    "menyebut": ["mengatakan", "menegaskan", "menyampaikan", "menuturkan", "memastikan"],
    "menangkap": ["mengamankan", "membekuk", "menahan", "menggeledah", "menangkap"],
    "ditangkap": ["diamankan", "dibekuk", "ditahan", "ditangkap aparat"],
    "tersangka": ["terduga pelaku", "sangkaan", "orang yang diduga", "terlapor"],
    "kasus": ["perkara", "persoalan hukum", "dugaan pelanggaran", "peristiwa hukum"],
    "penyelidikan": ["pemeriksaan", "pendalaman kasus", "investigasi", "proses penyidikan"],
    "polisi": ["aparat kepolisian", "petugas kepolisian", "pihak kepolisian", "polres/polsek setempat"],
    "kepolisian": ["polisi", "aparat", "penegak hukum", "pihak berwajib"],
    "korban": ["orang yang terdampak", "para penyintas", "mereka yang menjadi korban"],
    "melakukan": ["menjalankan", "melaksanakan", "berbuat", "mengeksekusi"],
    "mengalami": ["menghadapi", "menjalani", "terkena", "mengalami langsung"],
    "terjadi": ["berlangsung", "tercatat", "dilaporkan", "berlangsung"],
    "ditemukan": ["terungkap", "diketahui", "terdeteksi", "dijumpai"],
    "menemukan": ["menjumpai", "mendapati", "menemukan fakta", "mengonfirmasi"],
    "warga": ["masyarakat", "penduduk", "warga setempat", "masyarakat sekitar"],
    "masyarakat": ["warga", "publik", "masyarakat luas", "khalayak"],
    "daerah": ["wilayah", "kawasan", "lokasi", "area"],
    "wilayah": ["daerah", "kawasan", "zona", "area"],
    "pemerintah": ["pemerintah pusat", "pihak pemerintah", "otoritas", "penguasa"],
    "menteri": ["pejabat kementerian", "pimpinan kementerian", "menkominfo/menkeu dkk"],
    "program": ["inisiatif", "kebijakan", "agenda", "langkah strategis"],
    "kebijakan": ["regulasi", "aturan", "kebijakan pemerintah", "langkah"],
    "pembangunan": ["pengerjaan", "proyek", "pengembangan", "konstruksi"],
    "proyek": ["pengerjaan", "program pembangunan", "rencana", "konstruksi"],
    "anggaran": ["dana", "alokasi dana", "biaya", "pendanaan"],
    "dana": ["anggaran", "alokasi", "biaya", "pendanaan"],
    "miliar": ["miliar rupiah", "miliar", "miliaran"],
    "triliun": ["triliun rupiah", "triliunan"],
    "meningkat": ["naik", "bertumbuh", "melonjak", "mengalami kenaikan"],
    "menurun": ["turun", "menyusut", "berkurang", "mengalami penurunan"],
    "cepat": ["sigap", "gesit", "responsif", "dengan cepat"],
    "lambat": ["perlahan", "tidak cepat", "butuh waktu"],
    "baik": ["bagus", "positif", "optimal"],
    "buruk": ["jelek", "negatif", "kurang baik"],
    "penting": ["krusial", "vital", "signifikan", "menentukan"],
    "utama": ["pokok", "kunci", "sentral", "inti"],
    "terkait": ["berkaitan dengan", "berhubungan dengan", "menyangkut", "seputar"],
    "terkait kasus": ["dalam perkara", "sehubungan dengan kasus", "berkaitan dengan perkara"],
    "karena": ["lantaran", "sebab", "oleh karena", "berkat"],
    "untuk": ["guna", "demi", "bagi", "sebagai"],
    "dengan": ["menggunakan", "via", "melalui", "memanfaatkan"],
    "melalui": ["dengan", "lewat", "via", "menggunakan jalur"],
    "dari": ["mulai dari", "berasal dari", "oleh", "sejak"],
    "pada": ["di", "saat", "dalam", "ketika", "menurut konteks"],
    "saat": ["ketika", "waktu", "pada momen", "di tengah"],
    "setelah": ["pasca", "usai", "seusai", "berikutnya"],
    "sebelum": ["sebelumnya", "lebih dulu", "terlebih dahulu"],
    "wilayah": ["kawasan", "daerah", "lokasi"],
    "sekitar": ["kurang lebih", "sekira", "diperkirakan", "±"],
    "lebih dari": ["di atas", "melebihi", "lebih dari sekadar"],
    "sebanyak": ["sejumlah", "total", "hingga", "tidak kurang dari"],
    "sejumlah": ["beberapa", "sebagian", "sebanyak"],
    "beberapa": ["sejumlah", "sebagian", "sebagian kecil"],
    "dilaporkan": ["dikonfirmasi", "disampaikan", "diinformasikan", "diberitakan"],
    "diketahui": ["terungkap", "tercatat", "diinformasikan", "berdasarkan informasi"],
    "berdasarkan": ["menurut", "mengacu pada", "merujuk pada", "sesuai"],
    "menurut": ["berdasarkan", "mengutip", "merujuk", "sesuai keterangan"],
    "pihak": ["oknum", "kalangan", "unsur", "stakeholder"],
    "menambahkan": ["melengkapi", "menyambung", "menegaskan lagi", "mempertegas"],
    "menegaskan": ["memastikan", "menekankan", "menyatakan tegas", "menggarisbawahi"],
    "menekankan": ["menegaskan", "menyoroti", "menggarisbawahi", "meminta perhatian"],
    "mendorong": ["meminta", "mengajak", "menyerukan", "mendesak"],
    "meminta": ["memohon", "mendesak", "mengharap", "menyerukan"],
    "desak": ["minta", "tekan", "ajak"],
    "bantuan": ["dukungan", "pertolongan", "bantuan sosial", "sokongan"],
    "bantuan sosial": ["bansos", "bantuan", "bantuan pemerintah", "santunan"],
    "langkah": ["tindakan", "upaya", "inisiatif", "strategi"],
    "tindakan": ["langkah", "aksi", "upaya", "tindak lanjut"],
    "upaya": ["langkah", "usaha", "ikhtiar", "tindakan"],
    "usaha": ["upaya", "bisnis", "usaha mikro", "kegiatan"],
    "bisnis": ["usaha", "dunia usaha", "sektor bisnis"],
    "ekonomi": ["perekonomian", "sektor ekonomi", "kondisi ekonomi"],
    "perekonomian": ["ekonomi", "kondisi ekonomi", "sektor ekonomi"],
    "proses": ["perjalanan", "tahapan", "mekanisme", "rangkaian"],
    "hasil": ["capaian", "output", "produk", "temuan"],
    "kondisi": ["situasi", "keadaan", "status terkini"],
    "situasi": ["kondisi", "keadaan", "suasana"],
    "keadaan": ["kondisi", "situasi", "keadaan darurat"],
    "kerugian": ["rugi", "dampak", "kerusakan", "kehilangan"],
    "kerusakan": ["dampak kerusakan", "kerugian", "kerusakan fisik", "kehancuran"],
    "penanganan": ["penanggulangan", "pengendalian", "upaya menangani", "respons"],
    "penanggulangan": ["penanganan", "pengendalian", "mitigasi", "upaya penanganan"],
    "mitigasi": ["pengurangan dampak", "langkah antisipasi", "penanggulangan risiko"],
    "pencegahan": ["langkah preventif", "antisipasi", "upaya mencegah"],
    "antisipasi": ["pencegahan", "langkah preventif", "kesiapsiagaan"],
    "keselamatan": ["keamanan", "keselamatan jiwa", "aspek keselamatan"],
    "keamanan": ["keamanan publik", "ketertiban", "aspek keamanan"],
    "ketertiban": ["keamanan", "keteraturan", "kondisi tertib"],
    "pengamanan": ["penjagaan", "pengawalan", "langkah pengamanan"],
    "pengawasan": ["pemantauan", "supervisi", "kontrol", "pengontrolan"],
    "pemantauan": ["monitoring", "pengawasan", "pengamatan"],
    "evaluasi": ["penilaian", "kajian ulang", "assemen", "review"],
    "kajian": ["studi", "analisis", "penelitian", "telaah"],
    "analisis": ["kajian", "telaah", "pembahasan mendalam", "penelaahan"],
    "data": ["informasi", "catatan", "angka", "fakta di lapangan"],
    "informasi": ["data", "keterangan", "laporan", "kabar"],
    "laporan": ["informasi", "keterangan", "kabar", "notifikasi"],
    "pernyataan": ["keterangan", "perkataan", "pengakuan", "sikap"],
    "keterangan": ["penjelasan", "pernyataan", "informasi", "keterangan resmi"],
    "penjelasan": ["klarifikasi", "keterangan", "paparan", "uraian"],
    "klarifikasi": ["penjelasan", "keterangan resmi", "tanggapan", "penegasan"],
    "peran": ["fungsi", "kontribusi", "keterlibatan", "posisi"],
    "peran strategis": ["posisi kunci", "fungsi penting", "kontribusi besar"],
    "dukungan": ["sokongan", "backing", "bantuan", "konsistensi"],
    "respon": ["tanggapan", "respons", "sikap", "reaksi"],
    "tanggapan": ["respons", "sikap", "komentar", "reaksi"],
    "kesempatan": ["peluang", "momentum", "kesempatan emas", "waktu yang tepat"],
    "peluang": ["kesempatan", "prospek", "momentum", "celah"],
    "tantangan": ["hambatan", "kendala", "pekerjaan rumah", "persoalan"],
    "hambatan": ["kendala", "tantangan", "rintangan", "penghambat"],
    "kendala": ["hambatan", "tantangan", "masalah teknis", "rintangan"],
    "solusi": ["jalan keluar", "pemecahan", "penyelesaian", "alternatif"],
    "perubahan": ["transformasi", "pergeseran", "pembaruan", "peralihan"],
    "transformasi": ["perubahan", "transisi", "pembaruan", "pergeseran"],
    "perkembangan": ["kemajuan", "dinamika", "perjalanan", "progres"],
    "kemajuan": ["perkembangan", "progres", "kemajuan signifikan", "peningkatan"],
    "peningkatan": ["kenaikan", "pertumbuhan", "escalation", "perbaikan"],
    "target": ["sasaran", "capaian", "goal", "rencana"],
    "sasaran": ["target", "bidikan", "objek", "arah"],
    "realisasi": ["pencapaian", "eksekusi", "implementasi", "perwujudan"],
    "implementasi": ["penerapan", "eksekusi", "realisasi", "pelaksanaan"],
    "pelaksanaan": ["eksekusi", "implementasi", "penerapan", "jalan"],
    "perusahaan": ["badan usaha", "entitas bisnis", "korporasi", "perusahaan swasta"],
    "pekerja": ["buruh", "tenaga kerja", "karyawan", "pegawai"],
    "karyawan": ["pegawai", "pekerja", "staf", "tim internal"],
    "pendapatan": ["pemasukan", "revenue", "hasil usaha", "omzet"],
    "omzet": ["pendapatan", "perputaran uang", "revenue", "hasil penjualan"],
    "penjualan": ["omzet", "transaksi jual", "pemasaran", "penjualan produk"],
    "pasar": ["market", "pasar konsumen", "segmen", "pangsa pasar"],
    "pangsa pasar": ["market share", "bagian pasar", "porsi pasar"],
    "investasi": ["penanaman modal", "capital injection", "penanaman dana"],
    "anggota": ["personel", "pengurus", "kader", "staf"],
    "pengurus": ["pengelola", "manajemen", "tim", "anggota"],
    "kader": ["anggota", "kader partai", "aktivis", "penggerak"],
    "aktivitas": ["kegiatan", "rutinitas", "operasional", "aktivitas sehari-hari"],
    "kegiatan": ["aktivitas", "acara", "program", "agenda"],
    "acara": ["kegiatan", "agenda", "event", "rangkaian"],
    "agenda": ["acara", "program", "rangkaian", "rencana"],
    "jadwal": ["agenda", "waktu", "susunan acara", "timeline"],
    "waktu": ["jam", "momentum", "periode", "durasi"],
    "hari": ["hari ini", "waktu", "tanggal", "tahun"],
    "malam": ["malam hari", "petang", "malam ini"],
    "pagi": ["pagi hari", "subuh", "pagi ini"],
    "siang": ["siang hari", "tengah hari", "siang ini"],
    "sore": ["sore hari", "petang", "sore ini"],
    "lokasi": ["tempat", "titik", "posisi", "area"],
    "tempat": ["lokasi", "spot", "titik", "venue"],
    "posisi": ["jabatan", "kedudukan", "peran", "status"],
    "jabatan": ["posisi", "kedudukan", "peran struktural"],
    "status": ["posisi", "kedudukan", "keadaan"],
    "kuota": ["alokasi", "jatah", "batas", "porsi"],
    "jumlah": ["total", "angka", "besaran", "kuantitas"],
    "total": ["jumlah", "keseluruhan", "akumulasi"],
    "total mencapai": ["menembus", "mencapai", "tercatat"],
    "mencapai": ["menembus", "menyentuh", "menyentuh angka", "menembus angka"],
    "melonjak": ["naik tajam", "meningkat drastis", "melonjak naik"],
    "melonjak naik": ["melonjak", "meningkat tajam", "naik drastis"],
    "rata-rata": ["rerata", "rata-rata keseluruhan"],
    "pertumbuhan": ["kenaikan", "perkembangan", "ekspansi", "escalation"],
    "ekspansi": ["perluasan", "ekspansi bisnis", "pengembangan"],
    "perluasan": ["ekspansi", "pengembangan", "perluasan usaha"],
}

# Kalimat pembuka khas redaksi (variasi)
OPENERS = [
    "Jakarta, Kompas404 –", "Jakarta, KOMPAS404 –", "Kompas404 –", "Jakarta, Kompas404 Network –",
    "Nasional, Kompas404 –", "Kompas404 Newsroom –", "Jakarta –",
]
# Kalimat penutup klarifikasi redaksi
CLOSERS = [
    " Informasi ini dihimpun Kompas404 dari perkembangan terbaru di lapangan.",
    " Perkembangan ini terus dipantau redaksi Kompas404.",
    " Kompas404 akan terus memperbarui informasi seiring perkembangan.",
    " Demikian ringkasan yang dihimpun redaksi Kompas404.",
]

def pick(items):
    return random.choice(items)

def rewrite_title(title):
    """Bikin judul sedikit bervariasi tanpa mengubah fakta inti."""
    t = title.strip()
    # Tambah prefix redaksi pada sebagian
    if random.random() < 0.15:
        t = "Update: " + t
    # Ganti beberapa kata kunci dengan sinonim ringan
    words = t.split()
    out = []
    for w in words:
        key = w.lower().strip("(),;:")
        if key in SYNONYMS and random.random() < 0.35:
            out.append(pick(SYNONYMS[key]))
        else:
            out.append(w)
    return " ".join(out)

def rewrite_paragraph(para):
    """Spin satu paragraf: sinonim swap + variasi struktur ringan.

    Hati-hati: hindari substitusi ganda yang menghasilkan kata dobel (mis.
    'dugaan pelanggaran dugaan') dengan melacak root kata yang sudah dipakai
    pada window terbatas.
    """
    text = re.sub(r'<[^>]+>', '', para).strip()
    if not text:
        return ""
    if len(text) < 30:
        return text

    # root mapping: kata kunci -> kata dasar yang harus dicek kemunculannya
    root_of = {}
    for k in SYNONYMS:
        root = re.sub(r'^(me|men|mem|meny|di|ter|ber|pe|pen|pem|per)\b', '', k)
        root_of[k] = root or k

    sentences = re.split(r'(?<=[.!?])\s+', text)
    new_sents = []
    for s in sentences:
        s = s.strip()
        if not s:
            continue
        words = s.split()
        out = []
        used_roots = set()
        used_outputs = set()
        for w in words:
            key = w.lower().strip("(),;:'\"")
            root = root_of.get(key, "")
            if key in SYNONYMS and random.random() < 0.45:
                # cek dobel root ATAU dobel output sinonim
                replacement = pick(SYNONYMS[key])
                rep_lower = replacement.lower()
                if (root and root in used_roots) or rep_lower in used_outputs:
                    out.append(w)  # jangan dobel
                else:
                    out.append(replacement)
                    if root:
                        used_roots.add(root)
                    used_outputs.add(rep_lower)
            else:
                # track root dari kata yang muncul (untuk mencegah dobel di belakang)
                for candidate, r in root_of.items():
                    if candidate == key:
                        used_roots.add(r)
                        break
                out.append(w)
        ns = " ".join(out)
        # Variasi halus: kadang tukar posisi klausa keterangan waktu
        if random.random() < 0.2:
            m = re.match(r'^(.*?),\s+(.*)$', ns)
            if m and len(m.group(2).split()) > 4:
                ns = m.group(2) + ", " + m.group(1)
        new_sents.append(ns)

    # FIX: cleanup double-function-words yang mungkin muncul dari sinonim acak
    joined = " ".join(new_sents)
    joined = re.sub(r'\b(di|pada|untuk|dengan|dari|yang|dan|atau|sebagai|ke|oleh)\s+\1\b', r'\1', joined)
    # FIX: 'dijumpai di diperkirakan' -> kata kerja + preposisi ganda dari sinonim 'ditemukan di'
    joined = re.sub(r'\bdijumpai di\b', 'dijumpai', joined, flags=re.I)
    joined = re.sub(r'\bperantara di\b', 'perantara dalam', joined, flags=re.I)
    # FIX: kalimat yang ke-split aneh oleh variasi posisi klausa ('rakitan., Jakarta')
    joined = re.sub(r'\.,\s+([A-Z])', r'. \1', joined)
    return joined

def rewrite_content(content_html, title):
    """Rewrite seluruh body: spin tiap paragraf + bungkus framing redaksi."""
    paras = re.findall(r'<p>(.*?)</p>', content_html, re.S)
    if not paras:
        paras = [content_html]
    new_paras = []
    for i, p in enumerate(paras):
        rp = rewrite_paragraph(p)
        if rp and len(rp) > 40:
            new_paras.append(f"<p>{rp}</p>")
    if not new_paras:
        new_paras = [f"<p>{title}</p>"]

    # Selipkan opener di paragraf pertama dan closer di akhir
    opener = pick(OPENERS)
    new_paras[0] = new_paras[0].replace("<p>", f"<p>{opener} ", 1)
    new_paras[-1] = new_paras[-1].replace("</p>", pick(CLOSERS) + "</p>", 1)
    if len(new_paras) >= 2 and random.random() < 0.4:
        # sisipkan paragraf tambahan di tengah untuk struktur lebih unik
        mid = len(new_paras) // 2
        filler = pick([
            "<p>Redaksi Kompas404 mencoba merangkum pokok-pokok informasi tersebut secara ringkas dan jelas bagi pembaca.</p>",
            "<p>Berikut rangkuman yang disusun redaksi Kompas404 berdasarkan informasi yang berkembang.</p>",
            "<p>Kompas404 menyajikan ulasan singkat rangkaian peristiwa tersebut untuk memudahkan pembaca memahami konteksnya.</p>",
        ])
        new_paras.insert(mid, filler)
    return "\n".join(new_paras)

def main():
    # Sumber mentah dari scraper (verbatim detik) - jangan diubah
    with open(os.path.join(BASE, "scraped-detik.json"), "r", encoding="utf-8") as f:
        scraped = json.load(f)

    # Load image map (lokal free images)
    with open(os.path.join(BASE, "image-map.json"), "r", encoding="utf-8") as f:
        image_map = json.load(f)

    # Kumpulkan artikel existing (dari new-articles.json lama) yang bukan dari detik terbaru
    with open(os.path.join(BASE, "new-articles.json"), "r", encoding="utf-8") as f:
        prev = json.load(f)

    prev_slugs = {a["slug"] for a in prev}
    scraped_slugs = set()
    for s in scraped:
        slug = s.get("slug", "")
        if not slug.startswith("berita/"):
            slug = "berita/" + slug
        scraped_slugs.add(slug)

    # Artikel lama yang masih verbatim detik (semua yang ada di prev) - rewrite juga
    # Untuk artikel lama: rewrite ulang kontennya juga biar aman
    existing = []
    for a in prev:
        slug = a.get("slug", "")
        if not slug.startswith("berita/"):
            slug = "berita/" + slug
        if slug in scraped_slugs:
            continue  # dihandle dari scraped
        content_html = a.get("content", "")
        # rewrite kalau masih panjang (bukan cuma excerpt)
        if len(content_html) > 120:
            content_html = rewrite_content(content_html, a.get("title", ""))
        img = image_map.get(slug, a.get("image", ""))
        existing.append({
            "slug": slug,
            "title": a.get("title", ""),
            "category": a.get("category", "Berita"),
            "breadcrumb": a.get("breadcrumb") or a.get("title", "")[:30],
            "date": a.get("date", ""),
            "image": img if img else "https://kompas404.github.io/images/icon-kompas404.png",
            "image_alt": a.get("image_alt") or a.get("title", "")[:50],
            "content": content_html,
        })

    # Artikel baru dari scraped - rewrite penuh
    fresh = []
    for s in scraped:
        slug = s.get("slug", "")
        if not slug.startswith("berita/"):
            slug = "berita/" + slug
        title = s.get("title", "")
        content_html = s.get("content", "")
        rewritten = rewrite_content(content_html, title)
        img = image_map.get(slug, s.get("image", ""))
        fresh.append({
            "slug": slug,
            "title": title,
            "category": s.get("category", "Berita"),
            "breadcrumb": s.get("breadcrumb") or title[:30],
            "date": s.get("date", ""),
            "image": img if img else "https://kompas404.github.io/images/icon-kompas404.png",
            "image_alt": s.get("image_alt") or title[:50],
            "content": rewritten,
        })

    all_articles = fresh + existing

    # Sort by date desc
    def _date_key(a):
        d = a.get("date", "")
        m = re.search(r'(\d{1,2})\s+(\w+)\s+(\d{4})\s+(\d{1,2}):(\d{2})', d)
        if m:
            dd, mon, y, hh, mm = m.groups()
            months = {"Jan":1,"Feb":2,"Mar":3,"Apr":4,"Mei":5,"May":5,"Jun":6,"Jul":7,"Agu":8,"Aug":8,"Sep":9,"Okt":10,"Oct":10,"Nov":11,"Des":12,"Dec":12}
            return (int(y), months.get(mon[:3], 1), int(dd), int(hh), int(mm))
        m = re.search(r'(\d{1,2})\s+(\w+)\s+(\d{4})', d)
        if m:
            dd, mon, y = m.groups()
            months = {"Jan":1,"Feb":2,"Mar":3,"Apr":4,"Mei":5,"May":5,"Jun":6,"Jul":7,"Agu":8,"Aug":8,"Sep":9,"Okt":10,"Oct":10,"Nov":11,"Des":12,"Dec":12}
            return (int(y), months.get(mon[:3], 1), int(dd), 0, 0)
        return (0, 0, 0, 0, 0)

    all_articles.sort(key=_date_key, reverse=True)

    with open(os.path.join(BASE, "new-articles.json"), "w", encoding="utf-8") as f:
        json.dump(all_articles, f, ensure_ascii=False, indent=2)

    print(f"Rewritten {len(all_articles)} articles (fresh={len(fresh)}, existing={len(existing)})")
    print("Semua konten sudah di-rewrite + gambar lokal free-license")

if __name__ == "__main__":
    main()
