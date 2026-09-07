#!/usr/bin/env python3
# ==============================================================================
# Platforma: InvataCyber.ro
# Write-up / Solution Script
# Challenge: Operațiunea HashXOR: Amprenta din Umbră
# ==============================================================================
"""
Scriptul parcurge urmatorii pasi:
1. Citeste cele 100 de hash-uri MD5 din parole.txt.
2. Sparge hash-urile prin comparare cu un dictionar de cuvinte comune
   (sau o lista de cuvinte recuperate via CrackStation / rockyou.txt).
3. Citeste si converteste mesajul hexazecimal din flag.enc in bytes.
4. Aplica Repeating-Key XOR pentru fiecare parola in clar.
5. Identifica parola corecta si afiseaza flag-ul cand gaseste 'InvataCyber{'.
"""

import os
import hashlib
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PAROLE_FILE = os.path.join(BASE_DIR, "parole.txt")
FLAG_FILE = os.path.join(BASE_DIR, "flag.enc")

# Dictionar demonstrativ de candidati (in practica se poate citi linie cu linie din rockyou.txt)
COMMON_WORDLIST = [
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


def repeating_key_xor(ciphertext: bytes, key: bytes) -> bytes:
    """
    Decripteaza mesajul aplicand XOR intre fiecare byte din ciphertext
    si byte-ul corespunzator din cheie (repetata circular).
    Proprietatea XOR: Daca C = M ^ K, atunci M = C ^ K.
    """
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(ciphertext)])


def crack_md5_hashes(target_hashes: set, wordlist: list) -> list:
    """
    Compara hash-urile MD5 ale cuvintelor din dictionar cu lista tinta
    si returneaza lista parolelor gasite in clar.
    """
    cracked_passwords = []
    lookup = {}

    # Precomputam MD5 pentru cuvintele din dictionar
    for word in wordlist:
        h = hashlib.md5(word.encode("utf-8")).hexdigest()
        lookup[h] = word

    # Identificam parolele corespunzatoare
    for h in target_hashes:
        if h in lookup:
            cracked_passwords.append(lookup[h])

    return cracked_passwords


def main():
    print("[*] Pasul 1: Citire fisiere...")

    # 1. Citim hash-urile MD5 din parole.txt
    if not os.path.exists(PAROLE_FILE):
        print(f"[-] Eroare: Fisierul '{PAROLE_FILE}' nu a fost gasit! Ruleaza intai generate.py.")
        sys.exit(1)

    with open(PAROLE_FILE, "r", encoding="utf-8") as f:
        target_hashes = set(line.strip().lower() for line in f if line.strip())

    print(f"[+] S-au incarcat {len(target_hashes)} hash-uri MD5 tinta din parole.txt.")

    # 2. Citim ciphertext-ul hexazecimal din flag.enc si il transformam in bytes
    if not os.path.exists(FLAG_FILE):
        print(f"[-] Eroare: Fisierul '{FLAG_FILE}' nu a fost gasit! Ruleaza intai generate.py.")
        sys.exit(1)

    with open(FLAG_FILE, "r", encoding="utf-8") as f:
        hex_data = f.read().strip()
        ciphertext = bytes.fromhex(hex_data)

    print(f"[+] S-a decodat mesajul criptat ({len(ciphertext)} bytes).")

    # 3. Spargem hash-urile MD5
    print("[*] Pasul 2: Spargere hash-uri MD5...")
    cracked_passwords = crack_md5_hashes(target_hashes, COMMON_WORDLIST)
    print(f"[+] S-au spart cu succes {len(cracked_passwords)} parole din 100.")

    # 4. Brute-force Repeating-Key XOR
    print("[*] Pasul 3: Rulare brute-force XOR cu fiecare parola in clar...")
    found = False

    for password in cracked_passwords:
        key_bytes = password.encode("utf-8")
        decrypted_bytes = repeating_key_xor(ciphertext, key_bytes)

        # Incercam decodarea textului (ignorand eventualii octeti non-UTF8 din incercarile gresite)
        decrypted_text = decrypted_bytes.decode("utf-8", errors="ignore")

        # Verificam daca am gasit semnatura specifica platformei
        if "InvataCyber{" in decrypted_text:
            print("\n" + "=" * 60)
            print(f"[✔] PAROLA CORECTA IDENTIFICATA: '{password}'")
            print("=" * 60)
            print(f"[+] Text decriptat complet:\n{decrypted_text}\n")

            # Extragem exact flag-ul
            start = decrypted_text.find("InvataCyber{")
            end = decrypted_text.find("}", start) + 1
            flag = decrypted_text[start:end]

            print(f"[🎯] FLAG OBTINUT: {flag}")
            found = True
            break

    if not found:
        print("[-] Nu s-a putut decripta flag-ul cu parolele curente.")


if __name__ == "__main__":
    main()
