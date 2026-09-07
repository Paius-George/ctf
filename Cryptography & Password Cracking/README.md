# Rezolvare manuală: Operațiunea HashXOR
*[English version →](README.eng.md)*

- **Platformă:** InvataCyber.ro
- **Categorie:** Cryptography / Password Cracking
- **Dificultate:** Easy-Medium

Pașii de mai jos arată rezolvarea provocării fără scripturi proprii, folosind unelte web și utilitare obișnuite pentru CTF.

## Unelte necesare

- Editor de text sau utilitar de afișare (`cat`, Notepad, VS Code)
- [CrackStation](https://crackstation.net/) sau un utilitar local de hash cracking (`hashcat`, `john`)
- [CyberChef](https://gchq.github.io/cyberchef/)

## 1. Analiza fișierelor

Provocarea conține două fișiere:

- `flag.enc`: un șir de caractere hexazecimale (`0-9`, `a-f`). Reprezintă date binare criptate, salvate ca text hex.
- `parole.txt`: 100 de linii, fiecare având exact 32 de caractere hexazecimale. Lungimea de 32 de caractere corespunde unui rezumat de 128 de biți, specific algoritmului MD5.

## 2. Decodarea hash-urilor MD5

Parolele din listă sunt cuvinte comune și pot fi recuperate direct.

### Varianta online: CrackStation
1. Deschide [CrackStation](https://crackstation.net/).
2. Copiază conținutul din `parole.txt` în câmpul de căutare.
3. Completează verificarea captcha și apasă **Crack Hashes**.

Tabelul de rezultate va afișa parolele asociate fiecărui hash (de exemplu `password`, `123456`, `cybersecurity`, `matrix`).

### Varianta locală: hashcat sau John the Ripper
Dacă ai instalat dicționarul `rockyou.txt`:

```bash
# Cu hashcat (modul 0 = MD5):
hashcat -m 0 -a 0 parole.txt /usr/share/wordlists/rockyou.txt -o parole_sparte.txt

# Cu John the Ripper:
john --format=raw-md5 --wordlist=/usr/share/wordlists/rockyou.txt parole.txt
john --show --format=raw-md5 parole.txt
```

## 3. Decriptarea în CyberChef

Descrierea indică o criptare cu cheie repetitivă XOR aplicată pe octeți.

1. Deschide [CyberChef](https://gchq.github.io/cyberchef/).
2. Copiază textul din `flag.enc` în panoul **Input**.
3. În panoul **Recipe**, adaugă operațiile:
   - **From Hex** (convertește textul hexazecimal în octeți)
   - **XOR** (setează tipul cheii pe **UTF8**)
4. Testează cuvintele recuperate în câmpul **Key**.

Dintre cele 100 de parole recuperate, termenul legat direct de tematica provocării este `cybersecurity`. La introducerea acestei chei, panoul **Output** afișează mesajul în clar:

```text
Felicitari! Ai reusit sa spargi hash-urile MD5 si sa decriptezi folosind XOR. Flag-ul tau este: InvataCyber{m45t3r_0f_md5_cr4ck1ng_4nd_x0r}
```

## 4. Flag

```text
InvataCyber{m45t3r_0f_md5_cr4ck1ng_4nd_x0r}
```

Flag-ul poate fi trimis și validat pe platforma InvataCyber.ro.
