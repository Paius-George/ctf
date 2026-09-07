# CTF Challenges — InvataCyber.ro

*[Versiunea în română →](README.md)*

This repository contains practical security challenges developed for the [InvataCyber.ro](https://invatacyber.ro) educational platform. Each folder includes the challenge materials, a problem description, and a step-by-step write-up.

Standard flag format:
```text
InvataCyber{...}
```

---

## Available Challenges

| Challenge | Category | Difficulty | Summary |
| --- | --- | --- | --- |
| [Blind-Sql](./Blind-Sql) | Web Security | Medium | Boolean-based blind SQL injection via session cookie. |
| [Cryptography & Password Cracking](./Cryptography%20:%20Password%20Cracking) | Cryptography | Easy-Medium | MD5 hash recovery and byte-level Repeating-Key XOR decryption. |

---

## Challenge Structure

Each challenge operates as a self-contained directory:

- **`README.md`**: Walkthrough in Romanian.
- **`README.eng.md`**: Walkthrough in English.
- **`solve.py`**: Automated solver or exploitation script.
- **Lab files**: Databases, encrypted messages, or generator scripts.

---

## Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/<username>/<repo>.git
   cd <repo>
   ```
2. Navigate to the desired challenge directory.
3. Review the provided materials and attempt to find the flag before reading the walkthrough.
