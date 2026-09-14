# Provocări CTF — InvataCyber.ro

*[English version →](README.eng.md)*
<img width="3168" height="1344" alt="image" src="https://github.com/user-attachments/assets/bc4dfba1-e2c8-4333-9855-4afbc55795b3" />

Acest depozit conține provocările practice create pentru platforma [InvataCyber.ro](https://invatacyber.ro). Fiecare director include fișierele de laborator, scenariul de lucru și un ghid pas cu pas de rezolvare.

Formatul standard al flag-urilor:
```text
InvataCyber{...}
```

---

## Provocări disponibile

| Provocare | Categorie | Dificultate | Descriere pe scurt |
| --- | --- | --- | --- |
| [Blind-Sql](./Blind-Sql) | Web Security | Mediu | Injecție SQL oarbă bazată pe răspunsuri booleene într-un cookie de sesiune. |
| [Cryptography & Password Cracking](./Cryptography%20&%20Password%20Cracking) | Criptografie | Ușor-Mediu | Spargerea hash-urilor MD5 și decriptarea unui mesaj cu Repeating-Key XOR. |

---

## Structura fiecărui laborator

Fiecare director este gândit să funcționeze de sine stătător:

- **`README.md`**: Ghidul de rezolvare în limba română (write-up manual sau ghid pas cu pas).
- **`README.eng.md`**: Versiunea în limba engleză a documentației.
- **`solve.py`**: Script de rezolvare sau automatizare a exploatării.
- **Fișiere de lucru**: Baze de date demonstrative, fișiere criptate sau scripturi de generare.

---
