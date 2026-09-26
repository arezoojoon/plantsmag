import urllib.request
import urllib.parse
import json
import os
import random
import subprocess

API_KEY = "REDACTED_API_KEY" 

title = "The 7 Best Self-Watering Pots for Aroids in 2026 (Tested & Reviewed)"
prompt = "You are a top-tier SEO houseplant expert. Write a massive, 4000-word commercial buying guide targeting the keyword: '{title}'. This is a 'Hub Page' designed to rank #1 on Google and sell Amazon affiliate products. It MUST score 100/100 for on-page SEO. Divide it into distinct sections with h2, h3, and h4 tags. Structure: Introduction, Why Self-Watering Pots are Essential for Aroids (Monsteras, Philodendrons), The Criteria for our Testing (Drainage, Wicking mechanism, Aeration), The Top 7 Pots (Review each in detail), How to Pot an Aroid in a Self-Watering Planter, FAQ, and Conclusion. \n\nCRITICAL: In your Top 7 reviews, specifically highlight 'LECHUZA Classico' linking to 'https://amzn.to/4tll8BC' as the premium option, and 'QRRICA Plant Pots (Set of 5)' linking to 'https://amzn.to/4exPwoG' as the budget option. Use standard HTML `<a>` tags for all links. Include internal links to: `/category/plant-care/watering/`, `/category/plants/monstera/`, `/disease-finder`. Include multiple div blocks with class='pm-affiliate-box' for the product recommendations with compelling CTAs. Format entirely in standard HTML."
img_prompt = "Professional studio photography of a beautiful collection of sleek, modern self-watering plant pots in matte white and charcoal, planted with healthy Monstera and Philodendron plants, set against a clean white background, high-end product photography, 8k resolution, highly detailed, no text, no watermark"

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent?key={API_KEY}"
payload = {
    "contents": [{"parts": [{"text": prompt.format(title=title)}]}],
    "generationConfig": {"temperature": 0.7, "maxOutputTokens": 8192}
}

print(f"Generating content for Hub Page: {title}...")
data = json.dumps(payload).encode('utf-8')
req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
try:
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode('utf-8'))
        text = result['candidates'][0]['content']['parts'][0]['text']
        if text.startswith("```html"): text = text[7:]
        if text.endswith("```"): text = text[:-3]
        html_content = text.strip()
except Exception as e:
    print(f"Error generating content: {e}")
    exit(1)

seed = random.randint(100000, 999999)
local_html = f"hub_page_{seed}.html"
with open(local_html, 'w', encoding='utf-8') as f:
    f.write(html_content)
print(f"Saved {local_html} ({len(html_content.split())} words)")

print("Downloading image...")
encoded_prompt = urllib.parse.quote(img_prompt)
image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1200&height=630&model=flux&nologo=true&seed={seed}"
local_img = f"hub_img_{seed}.jpg"
img_req = urllib.request.Request(image_url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(img_req, timeout=60) as response:
        with open(local_img, 'wb') as f:
            f.write(response.read())
    print(f"Saved {local_img}")
except Exception as e:
    print(f"Error downloading image: {e}")
    exit(1)

# SCP
remote_html = f"/home/u284669846/domains/plantsmag.com/public_html/tmp_upload/{local_html}"
remote_img = f"/home/u284669846/domains/plantsmag.com/public_html/tmp_upload/{local_img}"
print("Uploading files via SCP...")
subprocess.run(f'scp -P 65002 {local_img} u284669846@187.124.245.99:{remote_img}', shell=True)
subprocess.run(f'scp -P 65002 {local_html} u284669846@187.124.245.99:{remote_html}', shell=True)

# Publish
print("Publishing via WP-CLI...")
SSH_CMD = 'ssh -p 65002 u284669846@187.124.245.99'
import_cmd = f'{SSH_CMD} "wp --path=/home/u284669846/domains/plantsmag.com/public_html media import {remote_img} --porcelain"'
media_id = subprocess.check_output(import_cmd, shell=True, text=True).strip()

post_cmd = f'{SSH_CMD} "wp --path=/home/u284669846/domains/plantsmag.com/public_html post create {remote_html} --post_title=\'{title}\' --post_status=publish --post_category=Tools --porcelain"'
post_id = subprocess.check_output(post_cmd, shell=True, text=True).strip()

link_cmd = f'{SSH_CMD} "wp --path=/home/u284669846/domains/plantsmag.com/public_html post meta set {post_id} _thumbnail_id {media_id}"'
subprocess.run(link_cmd, shell=True)

print(f"Success! Hub Page published as Post ID: {post_id} with Media ID: {media_id}")

# Flush caches
subprocess.run(f'{SSH_CMD} "wp --path=/home/u284669846/domains/plantsmag.com/public_html cache flush && wp --path=/home/u284669846/domains/plantsmag.com/public_html litespeed-purge all"', shell=True)
