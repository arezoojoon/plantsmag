import urllib.request
import urllib.parse
import json
import subprocess
import os
import random
import time

API_KEY = "REDACTED_API_KEY" 

articles = [
    {
        "title": "The Tissue Culture Crash: How Rare Monsteras Became Cheap and Why It Changes Everything in 2026",
        "prompt": "You are a top-tier SEO houseplant expert. Write a comprehensive, 2500-word deep-dive article on the trending US houseplant keyword: '{title}'. This is a trending 'Mega-Content' style article for the PlantsMag blog. It MUST be at least 2500 words and score 100/100 for on-page SEO. Divide it into distinct sections with h2 and h3 tags. Include an introduction, the science behind Tissue Culture (TC) propagation, why rare plant prices (like Thai Constellation) crashed, how to acclimate TC plants from agar to soil, understanding humidity and transpiration, and a conclusion. Include internal links using standard HTML `<a>` tags targeting these exact URLs naturally in the text: `/category/plant-care/watering/`, `/category/diseases/root-rot/`, `/disease-finder`. Include an 'affiliate-box' div with a class='pm-affiliate-box' for product recommendations (like sphagnum moss or humidity domes). Format entirely in standard HTML.",
        "img_prompt": "Close up professional macro photography of tiny Monstera Thai Constellation plantlets growing inside a sterile glass flask filled with clear agar gel, laboratory tissue culture, modern houseplant aesthetic, 8k resolution, photorealistic, no text, no watermark"
    },
    {
        "title": "Bioactive Terrariums: Merging Houseplants with Micro-Ecosystems in US Apartments",
        "prompt": "You are a top-tier SEO houseplant expert. Write a comprehensive, 2500-word deep-dive article on the trending US houseplant keyword: '{title}'. This is a trending 'Mega-Content' style article for the PlantsMag blog. It MUST be at least 2500 words and score 100/100 for on-page SEO. Divide it into distinct sections with h2 and h3 tags. Include an introduction, the rise of bioactive setups in 2026, the role of clean-up crews (springtails and isopods), choosing the right false bottom and substrate (mentioning CEC and aeration), lighting a closed terrarium (mentioning DLI and PPFD), maintaining the nitrogen cycle, and a conclusion. Include internal links using standard HTML `<a>` tags targeting these exact URLs naturally in the text: `/category/plant-care/grow-lights/`, `/category/diseases/root-rot/`, `/disease-finder`. Include an 'affiliate-box' div with a class='pm-affiliate-box' for product recommendations (like terrarium kits, springtail cultures, or LED grow lights). Format entirely in standard HTML.",
        "img_prompt": "Professional photography of a large beautiful geometric glass terrarium filled with lush miniature ferns, moss, and creeping figs, an enclosed bioactive ecosystem sitting on a modern wooden desk, warm natural lighting, 8k resolution, photorealistic, no text, no watermark"
    }
]

for article in articles:
    title = article['title']
    print(f"\n======================================")
    print(f"Generating 2500-word SEO article for: {title}", flush=True)

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent?key={API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": article['prompt'].format(title=title)}]}],
        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 8192}
    }

    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})

    html_content = ""
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            text = result['candidates'][0]['content']['parts'][0]['text']
            if text.startswith("```html"): text = text[7:]
            if text.endswith("```"): text = text[:-3]
            html_content = text.strip()
    except Exception as e:
        print(f"Error generating: {e}")
        continue

    print(f"Article generated! Length: {len(html_content.split())} words.", flush=True)

    # Generate Image
    encoded_prompt = urllib.parse.quote(article['img_prompt'])
    seed = random.randint(100000, 999999)
    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1200&height=630&model=flux&nologo=true&seed={seed}"

    local_img = f"img_{seed}.jpg"
    print(f"Downloading image from {image_url}...", flush=True)

    img_req = urllib.request.Request(image_url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(img_req, timeout=60) as response:
            with open(local_img, 'wb') as f:
                f.write(response.read())
    except Exception as e:
        print(f"Error downloading image: {e}")
        continue

    print(f"Publishing: {title}", flush=True)
    filename = os.path.basename(local_img)
    remote_tmp_img = f"/home/u284669846/domains/plantsmag.com/public_html/tmp_upload/{filename}"

    # SCP the image
    print("Uploading image via SCP...", flush=True)
    subprocess.run(f'scp -P 65002 "{local_img}" u284669846@187.124.245.99:{remote_tmp_img}', shell=True)

    # Write HTML to local tmp
    local_html = f"tmp_article_{seed}.html"
    with open(local_html, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print("Uploading HTML via SCP...", flush=True)
    subprocess.run(f'scp -P 65002 {local_html} u284669846@187.124.245.99:/home/u284669846/domains/plantsmag.com/public_html/tmp_upload/{local_html}', shell=True)

    # SSH command to import media and create post
    print("Executing SSH WP-CLI commands...", flush=True)
    safe_title = title.replace("'", "\\'")
    SSH_CMD = 'ssh -p 65002 u284669846@187.124.245.99'
    ssh_cmd = f"""{SSH_CMD} "
MEDIA_ID=\$(wp --path=/home/u284669846/domains/plantsmag.com/public_html media import {remote_tmp_img} --porcelain)
POST_ID=\$(wp --path=/home/u284669846/domains/plantsmag.com/public_html post create /home/u284669846/domains/plantsmag.com/public_html/tmp_upload/{local_html} --post_title='{safe_title}' --post_status=publish --post_category='Trending' --porcelain)
wp --path=/home/u284669846/domains/plantsmag.com/public_html post meta set \$POST_ID _thumbnail_id \$MEDIA_ID
echo "Published Post ID: \$POST_ID with Thumbnail ID: \$MEDIA_ID"
rm -f {remote_tmp_img}
rm -f /home/u284669846/domains/plantsmag.com/public_html/tmp_upload/{local_html}
" """
    res = subprocess.run(ssh_cmd, shell=True, capture_output=True, text=True)
    print(res.stdout)
    if res.stderr:
        print("Errors:", res.stderr)

    print(f"Successfully published {title}!", flush=True)

    if os.path.exists(local_html): os.remove(local_html)
    if os.path.exists(local_img): os.remove(local_img)
    
    print("Sleeping for 10 seconds before next article...", flush=True)
    time.sleep(10)

print("Flushing caches globally...", flush=True)
subprocess.run(f'{SSH_CMD} "wp --path=/home/u284669846/domains/plantsmag.com/public_html cache flush && wp --path=/home/u284669846/domains/plantsmag.com/public_html litespeed-purge all"', shell=True)
print("All Done!", flush=True)
