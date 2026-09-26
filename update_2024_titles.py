import requests
from requests.auth import HTTPBasicAuth
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

WP_URL = "https://plantsmag.com/wp-json/wp/v2"
USER = "n8n-bloger"
PASS = "VQ05 3amn qMzu aPkX VLsu 6XiA"
AUTH = HTTPBasicAuth(USER, PASS)

print("Scanning for posts with '2024' in title...")

page = 1
total_pages = 1
updated_count = 0

while page <= total_pages:
    res = requests.get(f"{WP_URL}/posts?context=edit&per_page=100&page={page}", auth=AUTH)
    if res.status_code != 200:
        break
    
    if page == 1:
        total_pages = int(res.headers.get('X-WP-TotalPages', 1))
        
    posts = res.json()
    for post in posts:
        title = post['title']['raw']
        if "2024" in title:
            new_title = title.replace("2024", "2026")
            
            content = post['content']['raw']
            
            # Prevent double appending
            if "Updated September 2026" not in content:
                new_content = "<p><em>Updated September 2026</em></p>\n" + content
            else:
                new_content = content
            
            payload = {
                "title": new_title,
                "content": new_content
            }
            
            # The WP API doesn't change the slug if we don't pass it, so URL equity is retained.
            update_res = requests.post(f"{WP_URL}/posts/{post['id']}", json=payload, auth=AUTH)
            print(f"Updated '{title}' -> '{new_title}': {update_res.status_code}")
            updated_count += 1
            
    page += 1

print(f"\nDone. Updated {updated_count} posts.")
