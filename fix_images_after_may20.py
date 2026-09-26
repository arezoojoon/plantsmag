import requests
from requests.auth import HTTPBasicAuth
import random
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

WP_URL = "https://plantsmag.com/wp-json/wp/v2"
USER = "n8n-bloger"
PASS = "VQ05 3amn qMzu aPkX VLsu 6XiA"
AUTH = HTTPBasicAuth(USER, PASS)

PEXELS_KEY = "KVWk5AKKw27xLrQsnlgJMLKhBQO0IxYZAE6PMODWZSCRAt12UMUIcxjC"

def fetch_pexels_image(keyword):
    headers = {"Authorization": PEXELS_KEY}
    res = requests.get(f"https://api.pexels.com/v1/search?query={keyword}&per_page=15", headers=headers)
    if res.status_code == 200:
        data = res.json()
        if data.get('photos'):
            photo = random.choice(data['photos'])
            img_url = photo['src']['large2x']
            alt = photo.get('alt', keyword)
            return img_url, alt
    return None, None

def upload_image_to_wp(img_url, alt_text):
    res = requests.get(img_url)
    if res.status_code != 200:
        return None
    
    filename = f"image_may20_{random.randint(1000,99999)}.jpg"
    headers = {
        'Content-Disposition': f'attachment; filename="{filename}"',
        'Content-Type': 'image/jpeg'
    }
    upload_res = requests.post(f"{WP_URL}/media", headers=headers, data=res.content, auth=AUTH)
    if upload_res.status_code == 201:
        media_id = upload_res.json()['id']
        return media_id
    print("Upload failed:", upload_res.text)
    return None

def update_post_featured_media(post_id, media_id):
    res = requests.post(f"{WP_URL}/posts/{post_id}", json={"featured_media": media_id}, auth=AUTH)
    return res.status_code == 200

target_date = "2026-05-20T00:00:00"

print("Fetching posts from May 20th onwards...")
posts = []
page = 1
while True:
    res = requests.get(f"{WP_URL}/posts?after={target_date}&per_page=100&page={page}", auth=AUTH)
    if res.status_code != 200:
        break
    data = res.json()
    if not data:
        break
    for p in data:
        posts.append(p)
    page += 1

print(f"Found {len(posts)} posts published after {target_date}.")

for p in posts:
    title = p['title']['rendered']
    pid = p['id']
    old_media_id = p.get('featured_media')
    print(f"Fixing post {pid}: {title}")
    
    # Clean up the title for better search
    # Replace JSON-like patterns if present in the title
    clean_title = title.replace('{"title":', '').replace('"}', '').replace('"', '').strip()
    words = clean_title.replace('-', ' ').split()
    keyword = " ".join(words[:2]) if len(words) >= 2 else "plant"
    
    img_url, alt = fetch_pexels_image(keyword)
    if not img_url:
        img_url, alt = fetch_pexels_image("houseplant")
        
    if img_url:
        print(f"  Downloaded from Pexels for keyword '{keyword}'...")
        media_id = upload_image_to_wp(img_url, alt)
        if media_id:
            if update_post_featured_media(pid, media_id):
                print(f"  Successfully updated post {pid} with new media {media_id}")
                
                # Delete the old dummy image
                if old_media_id and old_media_id != 0:
                    del_res = requests.delete(f"{WP_URL}/media/{old_media_id}?force=true", auth=AUTH)
                    if del_res.status_code == 200:
                        print(f"  Deleted old dummy image {old_media_id}")
            else:
                print(f"  Failed to update post {pid}")
        else:
            print(f"  Failed to upload media to WP")
    else:
        print("  Failed to find any image on Pexels")

print("All posts processed.")
