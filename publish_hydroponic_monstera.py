import urllib.request
import urllib.parse
import json
import subprocess
import os
import random

API_KEY = "REDACTED_API_KEY" 

title = "The 2026 Hydroponic Houseplant Revolution: Transitioning Your Monstera to LECA Without Melting Roots"

print(f"Generating 2500-word SEO article for: {title}", flush=True)

prompt = f"""You are a top-tier SEO houseplant expert. Write a comprehensive, 2500-word deep-dive article on the trending US houseplant keyword: '{title}'. 
This is a trending 'Mega-Content' style article for the PlantsMag blog. 
It MUST be at least 2500 words and score 100/100 for on-page SEO. 
Divide it into distinct sections with h2 and h3 tags. 
Include an introduction, the science behind hydroponics vs soil, why Monstera roots rot in transition, how to properly clean and prep LECA, understanding Cation Exchange Capacity (CEC) and Capillary Action, the importance of Daily Light Integral (DLI) and PPFD during transition, and a conclusion.
Include internal links using standard HTML `<a>` tags targeting these exact URLs naturally in the text:
- `/category/plant-care/watering/`
- `/category/diseases/root-rot/`
- `/disease-finder` (our AI Disease Finder tool)
- `/category/plant-care/grow-lights/`

Include an 'affiliate-box' div with a class="pm-affiliate-box" for product recommendations (like LECA pebbles or specific hydroponic nutrients).
Format entirely in standard HTML (uses <p>, <h2>, <ul>, etc). Do not use markdown wrappers like ```html. Remove all ```html tags. Ensure 100% HTML compliance."""

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent?key={API_KEY}"

payload = {
    "contents": [{"parts": [{"text": prompt}]}],
    "generationConfig": {"temperature": 0.7, "maxOutputTokens": 8192}
}

data = json.dumps(payload).encode('utf-8')
req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})

html_content = ""
try:
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode('utf-8'))
        text = result['candidates'][0]['content']['parts'][0]['text']
        
        # Clean HTML format
        if text.startswith("```html"):
            text = text[7:]
        if text.endswith("```"):
            text = text[:-3]
            
        html_content = text.strip()
except Exception as e:
    print(f"Error generating: {e}")
    exit(1)

print(f"Article generated! Length: {len(html_content.split())} words.", flush=True)

# Generate Image
img_prompt = "Close up professional photography of Monstera roots growing in LECA clay pebbles inside a sleek glass vase, modern indoor home aesthetic, bright natural light, 8k resolution, no text, no watermark"
encoded_prompt = urllib.parse.quote(img_prompt)
seed = random.randint(100000, 999999)
image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1200&height=630&model=flux&nologo=true&seed={seed}"

local_img = f"img_monstera_leca_{seed}.jpg"
print(f"Downloading image from {image_url}...", flush=True)

img_req = urllib.request.Request(image_url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(img_req, timeout=60) as response:
        with open(local_img, 'wb') as f:
            f.write(response.read())
except Exception as e:
    print(f"Error downloading image: {e}")
    exit(1)

print(f"Publishing: {title}", flush=True)

filename = os.path.basename(local_img)
remote_tmp_img = f"/home/u284669846/domains/plantsmag.com/public_html/tmp_upload/{filename}"

# 1. SCP the image
print("Uploading image via SCP...", flush=True)
scp_cmd = f'scp -P 65002 "{local_img}" u284669846@187.124.245.99:{remote_tmp_img}'
subprocess.run(scp_cmd, shell=True)

# Write HTML to local tmp
local_html = f"tmp_article_monstera_leca.html"
with open(local_html, 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Uploading HTML via SCP...", flush=True)
scp_html = f'scp -P 65002 {local_html} u284669846@187.124.245.99:/home/u284669846/domains/plantsmag.com/public_html/tmp_upload/{local_html}'
subprocess.run(scp_html, shell=True)

# 2. SSH command to import media and create post
print("Executing SSH WP-CLI commands...", flush=True)
SSH_CMD = 'ssh -p 65002 u284669846@187.124.245.99'
ssh_cmd = f"""{SSH_CMD} "
MEDIA_ID=\$(wp --path=/home/u284669846/domains/plantsmag.com/public_html media import {remote_tmp_img} --porcelain)
POST_ID=\$(wp --path=/home/u284669846/domains/plantsmag.com/public_html post create /home/u284669846/domains/plantsmag.com/public_html/tmp_upload/{local_html} --post_title='{title}' --post_status=publish --post_category='Trending,Plant Guides' --post_thumbnail=\$MEDIA_ID --porcelain)
echo "Published Post ID: \$POST_ID"
rm -f {remote_tmp_img}
rm -f /home/u284669846/domains/plantsmag.com/public_html/tmp_upload/{local_html}
wp --path=/home/u284669846/domains/plantsmag.com/public_html cache flush
wp --path=/home/u284669846/domains/plantsmag.com/public_html litespeed-purge all
" """

res = subprocess.run(ssh_cmd, shell=True, capture_output=True, text=True)
print(res.stdout)
if res.stderr:
    print("Errors:", res.stderr)

print(f"Successfully published {title}!", flush=True)

# Clean up
if os.path.exists(local_html):
    os.remove(local_html)
if os.path.exists(local_img):
    os.remove(local_img)
