#!/usr/bin/env python3
"""
KOMPAS404 Spin Copywriting Tool
Buat variant unik dari satu teks untuk content marketing & SEO.
Usage: python spin-copy.py
"""

import re
import random
import os

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

SYNONYMS = {
    "sangat": ["amat", "banget", "sekali", "terlalu", "ekstrem"],
    "baik": ["bagus", "mantap", "oke", "menarik", "berkualitas"],
    "buruk": ["jelek", "kurang bagus", "biasa saja", "medokore"],
    "cepat": ["gesit", "sigap", "kilat", "tercepat", "lancang"],
    "lambat": ["lemot", "sedikit lama", "tidak cepat", "perlahan"],
    "besar": ["besar", "gede", "luar biasa", "masif", "fantastis"],
    "kecil": ["mini", "mungil", "terdeteksi", "compact", "ringkas"],
    "murah": ["terjangkau", "hemat", "ekonomis", "dicurah", "glowing"],
    "mahal": ["pricey", "berbayar tinggi", "premium", "exklusif"],
    " baru": ["terbaru", "anyar", "segar", "fresh", "update"],
    " lama": ["sebelumnya", "terdahulu", " lama", " lampau"],
    "penting": ["krusial", "utama", "vital", "essential", "niscaya"],
    "mudah": ["gampang", "simpel", "no ribet", "praktis", "enteng"],
    "sulit": ["susah", "rumit", "complex", "berat", "challenging"],
    "cantik": ["elegan", "menawan", "indah", "kece", "aesthetic"],
    "ganteng": ["keren", "kece", "m apa aja", "stylish", "trendi"],
    "enak": ["sedap", "mantap", "lezat", "niiiiom", "yummy"],
    "nikmat": ["sedap", "enak banget", "mantap", "juara", "top markotop"],
    "bagus": ["kece", "keren", "mantap", "best", "recommended"],
    "terbaik": ["terpilih", " paling jitu", "the best", "juara satu", "nomer satu"],
    "terlaris": ["best seller", "favorit", "paling dibutuhkan", "hot item"],
    "promo": ["diskon", "penawaran", "bonus", "giveaway", "sale"],
    "gratis": ["free", "cuma-cuma", "tanpa biaya", "zero cost", "dapatkan bebas"],
    "diskon": ["potongan harga", "hemat", "murah", "bonus", "cashback"],
    "uang": ["dana", "budget", "modal", "financial", "biaya"],
    "hasil": ["output", "hasil akhir", "produk", "keuntungan", "benefit"],
    "sistem": ["metode", "cara", "teknik", "strategi", "workflow"],
    "kerja": ["bekerja", "menghasilkan", "menggerakkan", "menjalankan", "eksekusi"],
    "produk": ["barang", "item", "produk", "jasa", "commodity"],
    "layanan": ["service", "fitur", "fasilitas", "benefit", "keunggulan"],
    "konsumen": ["pelanggan", "customer", "pembeli", "user", "klien"],
    "bisnis": ["usaha", "business", "pekerjaan", "kerjaan", "project"],
    "internet": ["online", "digital", "web", "cyber", " dunia maya"],
    "media": ["platform", "saluran", "jalur", "channel", "mesin"],
    "social media": ["sosmed", "medsos", "platform sosial", " akun online"],
    "Indonesia": ["NKRI", "tanah air", "archipelago", "RI", "Nusantara"],
    "Jakarta": ["JKT", "ibu kota", "metropolitan", "capital city", " Jabodetabek"],
    "uang": ["dana", "financial", "budget", "modal", "cash"],
    "kekinian": ["terkini", "update", "hits", "viral", "trending"],
    "keren": ["kece", "mantap", "cool", "best", "recommended"],
    "mantap": ["keren", "kece", "jitu", "top", "the best"],
    "luar biasa": ["fantastis", "menakjubkan", "epic", "super", " amazing"],
    "selalu": ["konsisten", "terus", "setiap saat", "nonstop", "always on"],
    "pernah": ["sudah", "telah", "dulu", "sebelumnya", " pernah terjadi"],
    "akan": ["bakal", "nantinya", "ke depan", "soon", "coming soon"],
    "sedang": ["kini", "现在", "aktual", "while", "on progress"],
    "tahu": ["tau", "ngerti", "paham", "understand", "get it"],
    "pakai": ["gunakan", "pake", "apply", "implement", "gunake"],
    "buat": ["untuk", "menuju", "membuat", "menghasilkan", "create"],
    "dari": ["daripada", "by", "via", "lewat", "dengan"],
    "dengan": ["pakai", "menggunakan", "via", "by", "gunakan"],
    "yang": ["yang", "yg", "yang mana", "the", "this"],
    " ini": [" ini", " ni", " yang ini", "the", "this one"],
    " itu": [" itu", " tuh", " yang itu", "that", "that one"],
    "dan": ["&", " plus", " juga", " serta", "together with"],
    "atau": ["atau", "atau bisa juga", "alternatifnya", "atau kalau", "either"],
    " jadi": ["menjadi", "maka", "transform", "convert", "result"],
    "tersebut": ["tersebut", "itu", "disebut", "dibarengan", "yang ada"],
    " agar": [" supaya", " untuk", "biar", "in order to", "so that"],
    " tetapi": ["namun", "tapi", "tetapi", "however", "although"],
    " karena": ["soalnya", "makanya", "karena", "due to", "since"],
    " kalau": ["jika", "bila", "apabila", "when", "kalau misalkan"],
    " wajib": ["harus", "mesti", "wajib banget", "should", "must"],
    " bisa": ["dapat", "mampu", "bisa aja", "able to", "can"],
    " harus": ["wajib", "perlu", "harus banget", "must", "need to"],
    " belum": ["belum", "belum ada", "masih belum", "not yet", "still not"],
    " semua": ["seluruh", "semua", "total", "all", "entire"],
    " beberapa": ["beberapa", "sebagian", "macam", "some", "various"],
    " lebih": ["lebih", " lbh", " tambahan", "more", "additional"],
    " paling": ["terpaling", " nomor satu", "the most", "top", "best"],
    " gak": ["nggak", "ngga", "no", "not", "enggak"],
    " ga": ["nggak", "ngga", "no", "not", "enggak"],
    " gak": ["nggak", "ngga", "no", "not", "enggak"],
    " nggak": ["nggak", "gak", "no", "not", "enggak"],
    " ngga": ["nggak", "gak", "no", "not", "enggak"],
}

def tokenize(text):
    """Split text into tokens preserving punctuation and spacing."""
    tokens = []
    word = ""
    for char in text:
        if char.isalnum() or char in "'-":
            word += char
        else:
            if word:
                tokens.append(word)
                word = ""
            tokens.append(char)
    if word:
        tokens.append(word)
    return tokens

def build_pattern(text):
    """Build spin pattern with alternatives."""
    result = []
    i = 0
    while i < len(text):
        if text[i:i+2] == "{{":
            end = text.find("}}", i)
            if end != -1:
                content = text[i+2:end]
                alternatives = [a.strip() for a in content.split("|")]
                result.append(("spin", alternatives))
                i = end + 2
                continue
        result.append(("text", text[i]))
        i += 1
    return result

def generate_spin(text, level=1):
    """Generate one spin variation."""
    result = []
    i = 0
    while i < len(text):
        if text[i:i+2] == "{{":
            end = text.find("}}", i)
            if end != -1:
                content = text[i+2:end]
                alternatives = [a.strip() for a in content.split("|")]
                chosen = random.choice(alternatives)
                result.append(chosen)
                i = end + 2
                continue
        char = text[i]
        result.append(char)
        i += 1
    return "".join(result)

def auto_spin_text(text, level=2):
    """Automatically add spin syntax to text based on synonyms."""
    result = text
    
    # Sort by length descending to avoid partial replacements
    words_to_spin = []
    for key, alternatives in SYNONYMS.items():
        clean_key = key.strip()
        if clean_key.lower() in result.lower():
            # Find case-preserved occurrence
            pattern = re.compile(re.escape(clean_key), re.IGNORECASE)
            matches = list(pattern.finditer(result))
            for m in matches:
                original = m.group()
                # Add original + alternatives
                all_options = [original] + alternatives[:level]
                spin_group = "{" + "|".join(all_options) + "}"
                # Replace just this one occurrence
                result = result[:m.start()] + spin_group + result[m.end():]
    
    return result

def count_spin_variations(text):
    """Count how many unique variations a spin text can produce."""
    count = 1
    i = 0
    while i < len(text):
        if text[i:i+2] == "{{":
            end = text.find("}}", i)
            if end != -1:
                content = text[i+2:end]
                alternatives = [a.strip() for a in content.split("|")]
                count *= len(alternatives)
                i = end + 2
                continue
        i += 1
    return count

def apply_spin(text, iterations=5):
    """Generate multiple spin variations."""
    variations = []
    for _ in range(iterations):
        variations.append(generate_spin(text))
    return variations

def spin_article_mode():
    """Full article spinning with paragraph-level variety."""
    print("\n[MODE: ARTICLE SPIN]")
    print("Paste artikel lengkap (kosongkan baris untuk selesai):")
    print("-" * 50)
    
    lines = []
    while True:
        try:
            line = input()
            if line.strip() == "":
                break
            lines.append(line)
        except EOFError:
            break
    
    article = "\n\n".join(lines)
    if not article.strip():
        print("Tidak ada input.")
        return
    
    print(f"\n[+] Teks terbaca: {len(article)} karakter")
    print(f"[+] Estimated spin variations: {count_spin_variations(article):,}")
    print("\n[1] Generate variasi spin")
    print("[2] Tambah spin syntax manual")
    print("[3] Auto-spin dengan synonyms")
    print("[4] Generate semua variasi + save")
    print("[5] Baca dari file (.txt)")
    
    opt = input("\nPilih: ").strip()
    
    if opt == "1":
        n = int(input("Berapa variasi? (default 5): ").strip() or "5")
        variations = apply_spin(article, n)
        for idx, v in enumerate(variations, 1):
            print(f"\n--- VARIASI {idx} ---")
            print(v)
    
    elif opt == "2":
        print("\nFormat: {teks asli|alternatif1|alternatif2}")
        print("Contoh: {halo|bang|hallo|yo|hi}")
        spin_text = input("\nMasukkan teks dengan spin syntax: ")
        print(f"\n[+] Variasicount: {count_spin_variations(spin_text):,}")
        print("\n--- HASIL ---")
        variations = apply_spin(spin_text, 10)
        for idx, v in enumerate(variations, 1):
            print(f"{idx}. {v}")
    
    elif opt == "3":
        level = int(input("Level spin (1-3, default 2): ").strip() or "2")
        spun = auto_spin_text(article, level)
        print(f"\n[+] Spin syntax ditambahkan")
        print(f"[+] Variasicount: {count_spin_variations(spun):,}")
        print("\n--- AUTO-SPUN TEXT ---")
        print(spun)
        print("\n--- SAMPLE VARIATIONS ---")
        variations = apply_spin(spun, 5)
        for idx, v in enumerate(variations, 1):
            print(f"{idx}. {v}")
    
    elif opt == "4":
        n = int(input("Berapa variasi? ").strip() or "10")
        variations = apply_spin(article, n)
        out_file = f"spin_output_{random.randint(1000,9999)}.txt"
        with open(out_file, "w", encoding="utf-8") as f:
            for idx, v in enumerate(variations, 1):
                f.write(f"=== VARIASI {idx} ===\n{v}\n\n")
        print(f"\n[+] Saved: {out_file} ({n} variasi)")
    
    elif opt == "5":
        filepath = input("File path: ").strip()
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                article = f.read()
            print(f"[+] Loaded: {len(article)} chars")
            print("\n[1] Generate variasi")
            print("[2] Auto-spin synonyms")
            sub = input("Pilih: ").strip()
            if sub == "1":
                n = int(input("Berapa variasi? ").strip() or "10")
                variations = apply_spin(article, n)
                for idx, v in enumerate(variations, 1):
                    print(f"\n--- VAR {idx} ---")
                    print(v)
            elif sub == "2":
                spun = auto_spin_text(article, 2)
                print(f"\n[+] Variasicount: {count_spin_variations(spun):,}")
                print(spun)
        except FileNotFoundError:
            print(f"File tidak ditemukan: {filepath}")
    
    else:
        print("Pilihan tidak valid.")

def headline_spin_mode():
    """Quick headline/title spinning."""
    print("\n[MODE: HEADLINE SPIN]")
    print("Masukkan headline (Enter untuk selesai):")
    print("-" * 50)
    
    headlines = []
    while True:
        try:
            line = input("Headline: ").strip()
            if not line:
                break
            headlines.append(line)
        except EOFError:
            break
    
    if not headlines:
        print("Tidak ada headline.")
        return
    
    print(f"\n[+] {len(headlines)} headline(s) diproses")
    print(f"[+] Estimated total variations: {sum(count_spin_variations(h) for h in headlines):,}")
    print("\n" + "=" * 60)
    
    for idx, hl in enumerate(headlines, 1):
        spun = auto_spin_text(hl, 2)
        vars_count = count_spin_variations(spun)
        print(f"\n[{idx}] ORIGINAL: {hl}")
        print(f"    SPUN: {spun}")
        print(f"    Variations: {vars_count:,}")
        print(f"    Samples:")
        variations = apply_spin(spun, 5)
        for i, v in enumerate(variations, 1):
            print(f"      {i}. {v}")
    
    save = input("\nSave ke file? (y/n): ").strip().lower()
    if save == "y":
        out_file = f"headline_spin_{random.randint(1000,9999)}.txt"
        with open(out_file, "w", encoding="utf-8") as f:
            for idx, hl in enumerate(headlines, 1):
                spun = auto_spin_text(hl, 2)
                variations = apply_spin(spun, 10)
                f.write(f"=== HEADLINE {idx} ===\n")
                f.write(f"Original: {hl}\n\n")
                for i, v in enumerate(variations, 1):
                    f.write(f"{i}. {v}\n")
                f.write("\n")
        print(f"[+] Saved: {out_file}")

def bulk_spin_mode():
    """Bulk spin untuk banyak teks."""
    print("\n[MODE: BULK SPIN]")
    print("Masukkan banyak teks (kosongkan baris untuk selesai):")
    print("-" * 50)
    
    texts = []
    while True:
        try:
            line = input().strip()
            if line == "":
                break
            texts.append(line)
        except EOFError:
            break
    
    if not texts:
        print("Tidak ada teks.")
        return
    
    n = int(input(f"\nBerapa variasi per teks? (default 3): ").strip() or "3")
    
    print(f"\n[+] {len(texts)} teks, {n} variasi masing-masing")
    print(f"[+] Total output: {len(texts) * n} variasi")
    
    out_file = f"bulk_spin_{random.randint(1000,9999)}.txt"
    with open(out_file, "w", encoding="utf-8") as f:
        for idx, text in enumerate(texts, 1):
            spun = auto_spin_text(text, 2)
            vars_count = count_spin_variations(spun)
            variations = apply_spin(spun, n)
            f.write(f"=== ITEM {idx} ===\n")
            f.write(f"Original: {text}\n")
            f.write(f"Spin syntax: {spun}\n")
            f.write(f"Variations: {vars_count:,}\n\n")
            for i, v in enumerate(variations, 1):
                f.write(f"{i}. {v}\n")
            f.write("\n")
    
    print(f"\n[+] Saved: {out_file}")

def synonym_finder():
    """Cari synonyms untuk kata tertentu."""
    print("\n[MODE: SYNONYM FINDER]")
    word = input("Kata: ").strip().lower()
    
    found = []
    for key, alts in SYNONYMS.items():
        if key.strip().lower() == word:
            found.append((key, alts))
        elif key.strip().lower() in word or word in key.strip().lower():
            found.append((key, alts))
    
    if found:
        print(f"\n[+] Ditemukan {len(found)} match:")
        for key, alts in found:
            print(f"  '{key}' -> {', '.join(alts)}")
    else:
        print("Tidak ditemukan. Mencoba fuzzy match...")
        for key, alts in SYNONYMS.items():
            if any(c in key for c in word) or any(c in word for c in key):
                print(f"  '{key}' -> {', '.join(alts)}")

def main():
    print("=" * 60)
    print("   KOMPAS404 SPIN COPYWRITING TOOL v1.0")
    print("   Generate unique content variations")
    print("=" * 60)
    
    while True:
        print("\n[MENU UTAMA]")
        print("1. Article Spin      — Spin artikel panjang")
        print("2. Headline Spin     — Spin judul/headline")
        print("3. Bulk Spin         — Spin banyak teks sekaligus")
        print("4. Synonym Finder    — Cari alternatif kata")
        print("5. Exit")
        
        choice = input("\nPilih menu (1-5): ").strip()
        
        if choice == "1":
            spin_article_mode()
        elif choice == "2":
            headline_spin_mode()
        elif choice == "3":
            bulk_spin_mode()
        elif choice == "4":
            synonym_finder()
        elif choice == "5":
            print("\nTerima kasih. Bye!")
            break
        else:
            print("Pilihan tidak valid.")
        
        input("\nTekan Enter untuk kembali ke menu...")

if __name__ == "__main__":
    main()