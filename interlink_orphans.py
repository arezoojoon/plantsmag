import urllib.request
import json
import base64
import time
import random

WP_USER = 'n8n-bloger'
WP_APP_PASS = 'VQ05 3amn qMzu aPkX VLsu 6XiA'
auth = base64.b64encode(f"{WP_USER}:{WP_APP_PASS}".encode()).decode('utf-8')
headers = {
    'Authorization': f'Basic {auth}',
    'Content-Type': 'application/json'
}

def get_posts(page=1):
    req = urllib.request.Request(f'https://plantsmag.com/wp-json/wp/v2/posts?per_page=100&page={page}', headers=headers)
    try:
        resp = urllib.request.urlopen(req)
        return json.loads(resp.read().decode())
    except:
        return []

def update_post_content(post_id, new_content):
    post_data = {"content": new_content}
    req = urllib.request.Request(
        f'https://plantsmag.com/wp-json/wp/v2/posts/{post_id}',
        data=json.dumps(post_data).encode(),
        headers=headers,
        method='POST'
    )
    try:
        urllib.request.urlopen(req)
        return True
    except Exception as e:
        print("Failed to update post:", e)
        return False

print("Fetching all posts for interlinking...")
all_posts = []
for p in range(1, 4):
    posts = get_posts(p)
    if not posts: break
    all_posts.extend(posts)

with open('unindexed_valid_urls.txt', 'r') as f:
    unindexed_lines = [line.strip().split(',') for line in f.readlines() if line.strip()]

unindexed_targets = []
for line in unindexed_lines:
    if len(line) == 2:
        url, pid = line
        # Find title
        for p in all_posts:
            if str(p['id']) == str(pid):
                unindexed_targets.append({'title': p['title']['rendered'], 'url': p['link'], 'id': pid})
                break

print(f"Found {len(unindexed_targets)} unindexed targets. Distributing links...")

# For each post, inject 3 random links to unindexed targets
updated = 0
for p in all_posts:
    content = p['content']['rendered']
    if "seo-semantic-related" in content:
        continue # Already linked
        
    targets = random.sample(unindexed_targets, min(3, len(unindexed_targets)))
    
    links_html = '<div class="seo-semantic-related" style="margin-top:2em; padding:1.5em; background:#f8fafc; border-radius:8px;">'
    links_html += '<h3 style="margin-top:0;">Explore More Expert Guides</h3><ul style="list-style-type:none; padding-left:0;">'
    for t in targets:
        links_html += f'<li style="margin-bottom:0.5em;">🌿 <a href="{t["url"]}" style="font-weight:600; text-decoration:none;">{t["title"]}</a></li>'
    links_html += '</ul></div>'
    
    new_content = content + "\n" + links_html
    if update_post_content(p['id'], new_content):
        updated += 1
        print(f"Injected links into {p['id']}")
    time.sleep(0.5)

print(f"Interlinking complete. Updated {updated} articles.")
