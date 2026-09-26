import json
import urllib.request
import urllib.parse
import os
import time
import subprocess

SSH_CMD = 'ssh -p 65002 u284669846@187.124.245.99'

print("Uploading get_failed_images.php...")
os.system('scp -P 65002 d:\\project\\plantsmag\\get_failed_images.php u284669846@187.124.245.99:/home/u284669846/domains/plantsmag.com/public_html/')

print("Getting posts to fix...")
os.system(f'{SSH_CMD} "php /home/u284669846/domains/plantsmag.com/public_html/get_failed_images.php > /tmp/failed_images.json"')
os.system(f'scp -P 65002 u284669846@187.124.245.99:/tmp/failed_images.json failed_images.json')

try:
    with open('failed_images.json', 'r', encoding='utf-8') as f:
        posts = json.load(f)
except Exception as e:
    print("Error parsing JSON:", e)
    exit(1)

print(f"Found {len(posts)} posts to fix.")

for p in posts:
    print(f"\nProcessing Post {p['id']}: {p['title']}", flush=True)
    encoded_title = urllib.parse.quote(p['title'] + " professional nature plant green minimal --no text watermark logo")
    import random
    seed = random.randint(100000, 999999)
    image_url = f"https://image.pollinations.ai/prompt/{encoded_title}?width=1200&height=630&model=flux&nologo=true&seed={seed}"
    
    local_img = f"img_{p['id']}_{seed}.jpg"
    print(f"Downloading {image_url}", flush=True)
    
    req = urllib.request.Request(image_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
    success = False
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=60) as response:
                with open(local_img, 'wb') as f:
                    f.write(response.read())
            if os.path.exists(local_img) and os.path.getsize(local_img) > 10000:
                success = True
                break
        except Exception as e:
            print(f"Attempt {attempt+1} failed to download image: {e}", flush=True)
            time.sleep(2)
        
    if success:
        print("Uploading to server...", flush=True)
        remote_tmp = f"/home/u284669846/domains/plantsmag.com/public_html/tmp_upload/{local_img}"
        os.system(f'scp -P 65002 {local_img} u284669846@187.124.245.99:{remote_tmp}')
        
        print("Importing to WP...", flush=True)
        title_clean = p["title"].replace("'", "")
        wp_cmd = f'{SSH_CMD} "wp --path=/home/u284669846/domains/plantsmag.com/public_html media import {remote_tmp} --post_id={p["id"]} --featured_image --title=\'{title_clean}\' --porcelain"'
        os.system(wp_cmd)
        
        os.system(f'{SSH_CMD} "rm -f {remote_tmp}"')
        os.remove(local_img)
        print("Success!", flush=True)
    else:
        print("Failed to download image completely.", flush=True)
        if os.path.exists(local_img):
            os.remove(local_img)

print("Flushing cache...", flush=True)
os.system(f'{SSH_CMD} "wp --path=/home/u284669846/domains/plantsmag.com/public_html cache flush"')
os.system(f'{SSH_CMD} "wp --path=/home/u284669846/domains/plantsmag.com/public_html litespeed-purge all"')
print("Done!", flush=True)
