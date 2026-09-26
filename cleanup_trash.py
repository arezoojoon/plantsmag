import json
import urllib.request
import base64
import time

WP_USER = 'n8n-bloger'
WP_APP_PASS = 'VQ05 3amn qMzu aPkX VLsu 6XiA'
auth = base64.b64encode(f"{WP_USER}:{WP_APP_PASS}".encode()).decode('utf-8')
headers = {
    'Authorization': f'Basic {auth}',
    'Content-Type': 'application/json'
}

trash_keywords = ['n8n', 'test']

with open('unindexed_urls.txt', 'r') as f:
    lines = f.readlines()

valid_urls = []
deleted = 0

for line in lines:
    parts = line.strip().split(',')
    if len(parts) != 2: continue
    url, post_id = parts
    
    is_trash = any(kw in url.lower() for kw in trash_keywords)
    if is_trash:
        print(f"Trashing test article: {url} (ID: {post_id})")
        req = urllib.request.Request(
            f'https://plantsmag.com/wp-json/wp/v2/posts/{post_id}',
            headers=headers,
            method='DELETE'
        )
        try:
            urllib.request.urlopen(req)
            deleted += 1
        except Exception as e:
            print(f"Failed to trash {post_id}: {e}")
        time.sleep(1)
    else:
        valid_urls.append(line.strip())

# Save valid ones to a new file for content injection
with open('unindexed_valid_urls.txt', 'w') as f:
    for u in valid_urls:
        f.write(u + "\n")
        
print(f"Deleted {deleted} test articles.")
print(f"Saved {len(valid_urls)} valid articles for SEO expansion.")
