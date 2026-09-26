import json
import subprocess
import urllib.request
import urllib.parse
import os
import time

SSH_CMD = 'ssh -p 65002 u284669846@187.124.245.99'
WP_PATH = '--path=/home/u284669846/domains/plantsmag.com/public_html'

def run_wp_cli(cmd):
    full_cmd = f'{SSH_CMD} "wp {WP_PATH} {cmd}"'
    result = subprocess.run(full_cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip()

def get_all_posts():
    print("Fetching all posts...")
    output = run_wp_cli('post list --post_type=post --post_status=publish --fields=ID,post_title --format=json --count=500')
    try:
        posts = json.loads(output)
        return posts
    except Exception as e:
        print("Failed to parse posts", e)
        return []

def get_thumbnail_url(post_id):
    thumb_id = run_wp_cli(f'post meta get {post_id} _thumbnail_id')
    if not thumb_id or "Error" in thumb_id:
        return None
    thumb_url = run_wp_cli(f'post get {thumb_id} --field=guid')
    if "Error" in thumb_url:
        return None
    return thumb_url.strip()

def fix_duplicates():
    posts = get_all_posts()
    if not posts:
        return

    # 1. Delete duplicate titles
    seen_titles = set()
    posts_to_delete = []
    unique_posts = []

    for p in posts:
        title = p['post_title'].lower().strip()
        if title in seen_titles:
            posts_to_delete.append(p['ID'])
        else:
            seen_titles.add(title)
            unique_posts.append(p)

    if posts_to_delete:
        print(f"Deleting {len(posts_to_delete)} duplicate articles (same title)...")
        # delete in chunks
        for i in range(0, len(posts_to_delete), 10):
            chunk = " ".join(str(x) for x in posts_to_delete[i:i+10])
            run_wp_cli(f'post delete {chunk} --force')
        print("Deleted duplicate articles.")

    # 2. Find shared images
    seen_images = set()
    posts_to_fix_image = []

    print("Checking for duplicate images among unique posts...")
    for p in unique_posts:
        url = get_thumbnail_url(p['ID'])
        if not url:
            continue
        if url in seen_images:
            posts_to_fix_image.append(p)
        else:
            seen_images.add(url)

    if not posts_to_fix_image:
        print("No duplicate images found!")
        return

    print(f"Found {len(posts_to_fix_image)} posts with duplicate images. Fixing...")

    for p in posts_to_fix_image:
        print(f"Fixing image for post {p['ID']}: {p['post_title']}")
        title_encoded = urllib.parse.quote(p['post_title'] + " professional nature plant green minimal --no text watermark logo")
        image_url = f"https://image.pollinations.ai/prompt/{title_encoded}?width=1200&height=630&model=flux&nologo=true"
        
        local_img = f"img_{p['ID']}.jpg"
        print(f"Downloading new image: {image_url}")
        
        try:
            req = urllib.request.Request(image_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response, open(local_img, 'wb') as out_file:
                out_file.write(response.read())
                
            remote_tmp = f"/home/u284669846/domains/plantsmag.com/public_html/tmp_upload/{local_img}"
            print("Uploading to server...")
            subprocess.run(f'scp -P 65002 {local_img} u284669846@187.124.245.99:{remote_tmp}', shell=True)
            
            print("Importing to media library and setting as featured...")
            import_cmd = f'media import {remote_tmp} --post_id={p["ID"]} --featured_image --title="{p["post_title"]}" --porcelain'
            run_wp_cli(import_cmd)
            
            if os.path.exists(local_img):
                os.remove(local_img)
            
            # Clean up old remote file just in case, though WP might move it
            run_wp_cli(f'eval-file - <<< "unlink(\'{remote_tmp}\');"')

        except Exception as e:
            print(f"Error fixing post {p['ID']}: {e}")

    # Clear cache
    print("Flushing cache...")
    run_wp_cli('cache flush')
    run_wp_cli('litespeed-purge all')
    print("Done!")

if __name__ == "__main__":
    fix_duplicates()
