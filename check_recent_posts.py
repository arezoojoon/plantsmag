import requests
from requests.auth import HTTPBasicAuth
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

WP_URL = "https://plantsmag.com/wp-json/wp/v2"
USER = "n8n-bloger"
PASS = "VQ05 3amn qMzu aPkX VLsu 6XiA"
AUTH = HTTPBasicAuth(USER, PASS)

print("Recent posts:")
res = requests.get(f"{WP_URL}/posts?per_page=10", auth=AUTH)
if res.status_code == 200:
    for p in res.json():
        print(f"ID: {p['id']}, Slug: {p['slug']}, Title: {p['title']['rendered']}, Media: {p.get('featured_media')}")
else:
    print("Failed to fetch.")
