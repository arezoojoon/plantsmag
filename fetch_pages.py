import requests
from requests.auth import HTTPBasicAuth
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

WP_URL = "https://plantsmag.com/wp-json/wp/v2"
USER = "n8n-bloger"
PASS = "VQ05 3amn qMzu aPkX VLsu 6XiA"
AUTH = HTTPBasicAuth(USER, PASS)

print("Pages:")
res = requests.get(f"{WP_URL}/pages?per_page=100", auth=AUTH)
if res.status_code == 200:
    for p in res.json():
        print(f"ID: {p['id']}, Slug: {p['slug']}, Title: {p['title']['rendered']}")
else:
    print(f"Failed to fetch pages. Status code: {res.status_code}")
