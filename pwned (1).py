import hashlib
import requests


password = "password123"

sha1_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
prefix = sha1_hash[:5]  
suffix = sha1_hash[5:]  


url = f"https://api.pwnedpasswords.com/range/{prefix}"
response = requests.get(url)

if response.status_code != 200:
    raise RuntimeError(f"Error: {response.status_code}")

found = False
hashes = (line.split(':') for line in response.text.splitlines())
for returned_suffix, count in hashes:
    if returned_suffix == suffix:
        print(f"Password found! Compromised {count} times.")
        found = True
if not found :
    print("Password is safe (not found in breaches).")

