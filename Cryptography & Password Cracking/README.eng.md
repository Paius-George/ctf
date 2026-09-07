# Manual Walkthrough: Operation HashXOR

- **Platform:** InvataCyber.ro
- **Category:** Cryptography / Password Cracking
- **Difficulty:** Easy-Medium

This guide covers solving the challenge without writing custom scripts, using web tools and standard CTF utilities.

## Requirements

- A text editor or viewer (`cat`, Notepad, VS Code)
- [CrackStation](https://crackstation.net/) or a local hash-cracking tool (`hashcat`, `john`)
- [CyberChef](https://gchq.github.io/cyberchef/)

## 1. File Analysis

The challenge provides two files:

- `flag.enc`: A continuous string of hexadecimal characters (`0-9`, `a-f`). This represents raw encrypted binary data stored in hex format.
- `parole.txt`: 100 lines, each exactly 32 hexadecimal characters long. A 32-character hex string corresponds to a 128-bit digest, typical for MD5 hashes.

## 2. Cracking the MD5 Hashes

The hashes correspond to common dictionary words.

### Online: CrackStation
1. Open [CrackStation](https://crackstation.net/).
2. Copy the contents of `parole.txt` into the input area.
3. Complete the captcha and click **Crack Hashes**.

The output table lists the plaintext password for each hash (such as `password`, `123456`, `cybersecurity`, and `matrix`).

### Offline: hashcat or John the Ripper
If you have a local wordlist such as `rockyou.txt`:

```bash
# Using hashcat (mode 0 = MD5):
hashcat -m 0 -a 0 parole.txt /usr/share/wordlists/rockyou.txt -o cracked.txt

# Using John the Ripper:
john --format=raw-md5 --wordlist=/usr/share/wordlists/rockyou.txt parole.txt
john --show --format=raw-md5 parole.txt
```

## 3. Decrypting with CyberChef

The challenge description specifies repeating-key XOR encryption applied at the byte level.

1. Open [CyberChef](https://gchq.github.io/cyberchef/).
2. Paste the hex string from `flag.enc` into the **Input** panel.
3. In the **Recipe** panel, add the following operations in order:
   - **From Hex** (converts the hex text into raw bytes)
   - **XOR** (set the key format to **UTF8**)
4. Enter the candidate passwords in the **Key** field.

Among the recovered passwords, `cybersecurity` directly matches the theme of the platform. Setting this word as the key displays the plaintext in the **Output** panel:

```text
Felicitari! Ai reusit sa spargi hash-urile MD5 si sa decriptezi folosind XOR. Flag-ul tau este: InvataCyber{m45t3r_0f_md5_cr4ck1ng_4nd_x0r}
```

## 4. Flag

```text
InvataCyber{m45t3r_0f_md5_cr4ck1ng_4nd_x0r}
```

The flag can be submitted and verified on the InvataCyber.ro platform.
