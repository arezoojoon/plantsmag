import requests
from requests.auth import HTTPBasicAuth
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

WP_URL = "https://plantsmag.com/wp-json/wp/v2"
USER = "n8n-bloger"
PASS = "VQ05 3amn qMzu aPkX VLsu 6XiA"
AUTH = HTTPBasicAuth(USER, PASS)

print("Fetching all posts to check for broken JSON titles...")
page = 1
fixed_count = 0

while True:
    res = requests.get(f"{WP_URL}/posts?per_page=100&page={page}", auth=AUTH)
    if res.status_code != 200:
        break
    data = res.json()
    if not data:
        break
    
    for p in data:
        title = p['title']['rendered']
        # Remove common JSON artifacts
        if '{"title":' in title or '{"title": "' in title or '"}' in title:
            clean_title = title.replace('{"title":', '').replace('{"title": "', '').replace('"}', '').replace('"', '').strip()
            # if there are stray braces
            clean_title = clean_title.replace('{', '').replace('}', '').strip()
            
            pid = p['id']
            print(f"Fixing Title ID {pid}: '{title}' -> '{clean_title}'")
            
            update_res = requests.post(f"{WP_URL}/posts/{pid}", json={"title": clean_title}, auth=AUTH)
            if update_res.status_code == 200:
                print(f"  Successfully updated title.")
                fixed_count += 1
            else:
                print(f"  Failed to update title.")
                
    page += 1

print(f"Finished. Fixed {fixed_count} titles.")
