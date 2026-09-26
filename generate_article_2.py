import urllib.request
import urllib.parse
import json
import os
import random

API_KEY = "REDACTED_API_KEY" 

title = "Biological Pest Warfare: Why US Plant Owners Are Replacing Neem Oil with Predatory Mites"
prompt = "You are a top-tier SEO houseplant expert. Write a comprehensive, 2500-word deep-dive article on the trending US houseplant keyword: '{title}'. This is a trending 'Mega-Content' style article for the PlantsMag blog. It MUST be at least 2500 words and score 100/100 for on-page SEO. Divide it into distinct sections with h2 and h3 tags. Include an introduction, why pests like Thrips and Spider Mites have become resistant to Neem Oil, the rise of beneficial insects (Amblyseius swirskii, Orius insidiosus), how to deploy predatory mites in a US apartment without them escaping, humidity requirements for beneficials, and a conclusion. Include internal links using standard HTML `<a>` tags targeting these exact URLs naturally in the text: `/category/diseases/pests/`, `/disease-finder`, `/watering-calculator/`. Include an 'affiliate-box' div with a class='pm-affiliate-box' promoting the 'QRRICA Plant Pots (Set of 5)' linking to 'https://amzn.to/4exPwoG' with a compelling CTA for repotting quarantined plants. Format entirely in standard HTML."
img_prompt = "Extreme macro photography of a tiny predatory mite hunting a spider mite on the underside of a Calathea leaf, incredibly detailed, National Geographic style micro photography, vivid green leaf texture, 8k resolution, photorealistic, no text, no watermark"

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent?key={API_KEY}"
payload = {
    "contents": [{"parts": [{"text": prompt.format(title=title)}]}],
    "generationConfig": {"temperature": 0.7, "maxOutputTokens": 8192}
}

print("Generating content...")
data = json.dumps(payload).encode('utf-8')
req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
with urllib.request.urlopen(req) as response:
    result = json.loads(response.read().decode('utf-8'))
    text = result['candidates'][0]['content']['parts'][0]['text']
    if text.startswith("```html"): text = text[7:]
    if text.endswith("```"): text = text[:-3]
    html_content = text.strip()

seed = random.randint(100000, 999999)
local_html = f"tmp_article_2_{seed}.html"
with open(local_html, 'w', encoding='utf-8') as f:
    f.write(html_content)
print(f"Saved {local_html}")

print("Downloading image...")
encoded_prompt = urllib.parse.quote(img_prompt)
image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1200&height=630&model=flux&nologo=true&seed={seed}"
local_img = f"img_2_{seed}.jpg"
img_req = urllib.request.Request(image_url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(img_req, timeout=60) as response:
    with open(local_img, 'wb') as f:
        f.write(response.read())
print(f"Saved {local_img}")
