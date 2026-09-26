import pandas as pd
import json
import urllib.request
import base64

# Read Performance report
xl = pd.ExcelFile('https___plantsmag.com_-Performance-on-Search-2026-07-06.xlsx')
if 'Pages' in xl.sheet_names:
    df_pages = xl.parse('Pages')
    indexed_urls = set(df_pages['Top pages'].dropna().tolist())
else:
    print("No 'Pages' sheet found in Performance report")
    indexed_urls = set()

# Fetch all WP published posts
WP_USER = 'n8n-bloger'
WP_APP_PASS = 'VQ05 3amn qMzu aPkX VLsu 6XiA'
auth = base64.b64encode(f"{WP_USER}:{WP_APP_PASS}".encode()).decode('utf-8')
headers = {
    'Authorization': f'Basic {auth}',
    'Content-Type': 'application/json'
}

print("Fetching all published posts from WP...")
wp_urls = {}
for page in range(1, 5): # Fetch up to 400 posts (100 per page)
    req = urllib.request.Request(f'https://plantsmag.com/wp-json/wp/v2/posts?per_page=100&page={page}', headers=headers)
    try:
        resp = urllib.request.urlopen(req)
        posts = json.loads(resp.read().decode())
        if not posts: break
        for p in posts:
            wp_urls[p['link']] = p['id']
    except Exception as e:
        print(f"Page {page} error or no more posts:", e)
        break

all_wp_urls = set(wp_urls.keys())

unindexed = all_wp_urls - indexed_urls
print(f"Total WP Posts: {len(all_wp_urls)}")
print(f"Total URLs with impressions: {len(indexed_urls)}")
print(f"Estimated Unindexed URLs: {len(unindexed)}")

with open('unindexed_urls.txt', 'w') as f:
    for u in unindexed:
        f.write(f"{u},{wp_urls[u]}\n")
print("Saved to unindexed_urls.txt")
