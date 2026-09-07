#!/usr/bin/env python3
# ==============================================================================
# Platforma: InvataCyber.ro
# Challenge: Operațiunea HashXOR: Amprenta din Umbră
# Categorie: Cryptography / Password Cracking (Easy-Medium)
# ==============================================================================
"""
Script de administrare pentru generarea provocării CTF:
1. parole.txt -> Conține exact 100 de hash-uri MD5 provenite din parole comune.
2. flag.enc   -> Conține mesajul secret criptat cu Repeating-Key XOR
                 folosind parola în clar (nu hash-ul), salvat în format Hex.
"""

import os
import hashlib
import random

# ------------------------------------------------------------------------------
# 1. CONFIGURARE PROVOCARE
# ------------------------------------------------------------------------------
FLAG = "InvataCyber{m45t3r_0f_md5_cr4ck1ng_4nd_x0r}"
SECRET_MESSAGE = (
    f"Felicitari! Ai reusit sa spargi hash-urile MD5 si sa decriptezi "
    f"folosind XOR. Flag-ul tau este: {FLAG}"
)

# Lista de 100 de parole/cuvinte comune (ușor de spart cu rockyou.txt / CrackStation)
WORDLIST_100 = [
    "password", "123456", "12345678", "qwerty", "dragon",
    "baseball", "football", "letmein", "monkey", "shadow",
    "sunshine", "princess", "superman", "master", "michael",
    "welcome", "charlie", "jordan", "killer", "trustno1",
    "hunter", "system", "matrix", "falcon", "phantom",
    "whisper", "secret", "security", "hacker", "network",
    "cyber", "freedom", "phoenix", "diamond", "thunder",
    "dragonfly", "firewall", "terminal", "packet", "cookie",
    "access", "root", "oracle", "coffee", "guitar",
    "galaxy", "silver", "golden", "vampire", "wizard",
    "ninja", "samurai", "warrior", "spiderman", "batman",
    "ironman", "avenger", "captain", "legend", "destiny",
    "eclipse", "horizon", "infinity", "genesis", "paradise",
    "champion", "victory", "monster", "tiger", "panther",
    "cobra", "viper", "bullet", "rocket", "comet",
    "meteor", "nebula", "cosmos", "starlight", "supernova",
    "aurora", "blizzard", "tornado", "tsunami", "volcano",
    "earthquake", "avalanche", "solitude", "tempest", "inferno",
    "radiance", "serenity", "valkyrie", "chronos", "titan",
    "olympus", "atlantis", "excalibur", "cybersecurity", "stealth"
]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PAROLE_FILE = os.path.join(BASE_DIR, "parole.txt")
FLAG_FILE = os.path.join(BASE_DIR, "flag.enc")


def md5_hash(text: str) -> str:
    """Calculează hash-ul MD5 (32 caractere hexazecimale) al unui string."""
    return hashlib.md5(text.encode("utf-8")).hexdigest()


def repeating_key_xor(plaintext: bytes, key: bytes) -> bytes:
    """
    Criptează datele folosind operația matematică XOR la nivel de bytes:
    Byte_Criptat = Byte_Mesaj ^ Byte_Cheie.
    Cheia este aplicată circular folosind indexul modulo lungimea cheii (i % len(key)).
    """
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(plaintext)])


def main():
    print("[*] Incepe generarea provocarii pentru InvataCyber.ro...")

    # Verificăm că avem exact 100 de parole unice
    assert len(WORDLIST_100) == 100, f"Lista contine {len(WORDLIST_100)} cuvinte, nu 100!"
    assert len(set(WORDLIST_100)) == 100, "Exista duplicate in lista de cuvinte!"

    # Amestecăm lista pentru un plus de impredictibilitate
    shuffled_words = WORDLIST_100.copy()
    random.shuffle(shuffled_words)

    # 2. Alegem o parolă care va fi cheia de criptare (în clar)
    chosen_key = "cybersecurity"
    chosen_index = shuffled_words.index(chosen_key)
    chosen_md5 = md5_hash(chosen_key)

    print(f"[+] Cheia aleasa: '{chosen_key}'")
    print(f"[+] Hash-ul MD5 al cheii: {chosen_md5}")
    print(f"[+] Pozitionata la linia {chosen_index + 1} in parole.txt")

    # 3. Transformăm toate parolele în hash-uri MD5 și le salvăm în parole.txt
    with open(PAROLE_FILE, "w", encoding="utf-8") as f:
        for word in shuffled_words:
            f.write(md5_hash(word) + "\n")
    print(f"[+] Fisierul '{PAROLE_FILE}' a fost generat (100 de hash-uri MD5).")

    # 4. Criptăm mesajul secret folosind Repeating-Key XOR cu parola în clar
    plaintext_bytes = SECRET_MESSAGE.encode("utf-8")
    key_bytes = chosen_key.encode("utf-8")
    ciphertext_bytes = repeating_key_xor(plaintext_bytes, key_bytes)

    # 5. Salvăm ciphertext-ul în format hexazecimal în flag.enc
    ciphertext_hex = ciphertext_bytes.hex()
    with open(FLAG_FILE, "w", encoding="utf-8") as f:
        f.write(ciphertext_hex + "\n")
    print(f"[+] Fisierul '{FLAG_FILE}' a fost generat (format Hex).")

    print("\n[✔] Provocare generata cu succes!")
    print(f"    - Flag: {FLAG}")
    print(f"    - Cheie: {chosen_key}")
    print("    - Fisiere distribuite jucatorului: flag.enc, parole.txt")


if __name__ == "__main__":
    main()
