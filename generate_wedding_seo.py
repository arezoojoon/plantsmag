import os
import json
import urllib.request
import urllib.error
import base64
import time
import re

def to_title_case(text):
    exceptions = {'a', 'an', 'and', 'as', 'at', 'but', 'by', 'for', 'in', 'of', 'on', 'or', 'so', 'the', 'to', 'up', 'yet', 'with'}
    words = re.split(r'(\s+)', text)
    result = []
    for i, word in enumerate(words):
        if not word.strip():
            result.append(word)
            continue
        lower_word = word.lower()
        if i == 0 or i == len(words) - 1 or lower_word not in exceptions:
            result.append(word.capitalize())
        else:
            result.append(lower_word)
    return ''.join(result)

API_KEY = "REDACTED_API_KEY" # Primary key
TEXT_MODEL = "gemini-2.5-pro"
IMAGE_MODEL = "gemini-3.1-flash-image"

# The 10 pilot slugs
PAGES = [
    {"slug": "average-cost-of-flowers-for-a-wedding", "type": "cost", "theme": "General Wedding"},
    {"slug": "wedding-flowers-on-a-budget", "type": "cost", "theme": "Budget Wedding"},
    {"slug": "wedding-florist-prices", "type": "cost", "theme": "General Wedding"},
    {"slug": "how-much-do-wedding-flowers-cost", "type": "cost", "theme": "General Wedding"},
    {"slug": "sage-green-wedding-flowers", "type": "theme", "theme": "Sage Green"},
    {"slug": "terracotta-wedding-theme", "type": "theme", "theme": "Terracotta"},
    {"slug": "dusty-blue-wedding-flowers", "type": "theme", "theme": "Dusty Blue"},
    {"slug": "burgundy-and-blush-wedding-flowers", "type": "theme", "theme": "Burgundy and Blush"},
    {"slug": "boho-wedding-bouquet", "type": "theme", "theme": "Boho"},
    {"slug": "rustic-wedding-centerpieces", "type": "theme", "theme": "Rustic"}
]

DATA_DIR = r"d:\project\plantsmag\plantsmag-nextjs-apps\public\wedding-data"
IMG_DIR = r"d:\project\plantsmag\plantsmag-nextjs-apps\public\wedding-images"
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(IMG_DIR, exist_ok=True)

def generate_text(prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{TEXT_MODEL}:generateContent?key={API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.4, "maxOutputTokens": 8192, "responseMimeType": "application/json"}
    }
    
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})
    
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode('utf-8'))
                text = result['candidates'][0]['content']['parts'][0]['text']
                if text.startswith('```json'): text = text[7:]
                if text.endswith('```'): text = text[:-3]
                return text.strip()
        except urllib.error.HTTPError as e:
            print(f"HTTPError on text generation: {e.code} - {e.read().decode()}")
            time.sleep(2)
        except Exception as e:
            print(f"Error on text generation: {e}")
            time.sleep(2)
    return ""

def generate_image(prompt, reference_b64=None):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{IMAGE_MODEL}:generateContent?key={API_KEY}"
    
    parts = [{"text": prompt}]
    if reference_b64:
        parts.append({
            "inlineData": {
                "mimeType": "image/jpeg",
                "data": reference_b64
            }
        })
        
    payload = {
        "contents": [{"parts": parts}],
        "generationConfig": {
            "temperature": 0.5
        }
    }
    
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})
    
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode('utf-8'))
                if 'inlineData' in result['candidates'][0]['content']['parts'][0]:
                    return result['candidates'][0]['content']['parts'][0]['inlineData']['data']
                else:
                    return result['candidates'][0]['content']['parts'][0]['text']
        except urllib.error.HTTPError as e:
            print(f"HTTPError on image generation: {e.code} - {e.read().decode()}")
            time.sleep(2)
        except Exception as e:
            print(f"Error on image generation: {e}")
            time.sleep(2)
    return None

def generate_alt_text(image_b64):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent?key={API_KEY}"
    prompt = "Write a short, descriptive alt text for this wedding image. Max 100 characters. Only output the text."
    
    payload = {
        "contents": [{"parts": [
            {"text": prompt},
            {"inlineData": {"mimeType": "image/jpeg", "data": image_b64}}
        ]}],
        "generationConfig": {"temperature": 0.2}
    }
    
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result['candidates'][0]['content']['parts'][0]['text'].strip()
    except Exception as e:
        print(f"Alt text error: {e}")
        return "Wedding floral arrangement"

def build_page_data(page):
    slug = page["slug"]
    print(f"Processing: {slug}")
    
    # The Knot 2026 Real Weddings Study data
    text_prompt = f"""You are a professional wedding floral expert. 
Write a short, engaging 300-word SEO article for the keyword/slug: "{slug}".
Include real names of flowers that match the {page['theme']} theme. 
Include the season they bloom.
CRITICAL TONE RULES: Go straight to the point. DO NOT use generic AI intros like "{page['theme']} is more than a color; it's a feeling" or "Choosing the right flowers can tie your theme together." Start directly with actionable floral advice.
CRITICAL COST DATA: If this is a cost-related page, explicitly state that according to "The Knot 2026 Real Weddings Study" (based on 10,474 US couples married in 2025), the average cost of wedding flowers is $2,800. Mention that the average total wedding cost is $34,200, making florals roughly 10% of the total budget. Explain that this $2,800 average typically covers the bridal bouquet, boutonnieres, wedding party flowers, and reception centerpieces. For budget breakdown: couples with budgets under $15k spend on average $8,900 total; between $15k-$40k spend $26,400 total; and over $40k spend $70,300 total. Do NOT invent other numbers.

Return exactly and ONLY a valid JSON object with:
"h1_title": "Optimized H1 title",
"title": "SEO Meta Title (max 60 chars, use proper Title Case, lowercase for prepositions/conjunctions like 'and', 'to', 'for')",
"meta_description": "SEO Meta Description (max 160 chars)",
"content_html": "Your 300-400 words content. MUST use valid HTML tags (<h2>, <h3>, <p>, <ul>, <li>). DO NOT use markdown like ** or ##."
"""
    text_res = generate_text(text_prompt)
    try:
        page_content = json.loads(text_res)
    except Exception as e:
        print(f"Failed to parse JSON for {slug}. Error: {e}")
        print(f"Raw: {text_res}")
        return None

    # 2. Generate Images
    page_img_dir = os.path.join(IMG_DIR, slug)
    os.makedirs(page_img_dir, exist_ok=True)
    
    images_metadata = []
    
    # Check if images already exist
    existing_images = [f for f in os.listdir(page_img_dir) if f.endswith('.webp')]
    if len(existing_images) >= 8:
        print(f"  Images already exist for {slug}. Skipping image generation.")
        # Load existing images from data.json if possible to keep alt texts
        data_json_path = os.path.join(DATA_DIR, "data.json")
        if os.path.exists(data_json_path):
            try:
                with open(data_json_path, 'r', encoding='utf-8') as f:
                    old_data = json.load(f)
                    for old_page in old_data.get('pages', []):
                        if old_page['slug'] == slug and 'images' in old_page:
                            images_metadata = old_page['images']
                            break
            except Exception as e:
                print(f"Could not load old data.json: {e}")
        
        if not images_metadata:
            for i in range(1, 9):
                img_path = f"/wedding-images/{slug}/{slug}-0{i}.webp"
                images_metadata.append({
                    "url": img_path,
                    "alt": f"Beautiful {page['theme']} wedding floral arrangement"
                })
    else:
        # Highly descriptive prompt for the seed image
        seed_prompt = f"""Cinematic editorial wedding photography, close-up shot of a reception table centerpiece. 
A luxurious {page['theme']} floral arrangement featuring white garden roses, ranunculus, lisianthus, and silver dollar eucalyptus. 
The table features a solid {page['theme']} tablecloth and {page['theme']} cloth napkins, with elegant gold cutlery. 
Soft natural window light, shallow depth of field. 
Empty room, no people, no guests in the background."""

        print(f"  Generating Seed Image for {slug}...")
        seed_b64 = generate_image(seed_prompt)
        
        if seed_b64:
            seed_path = os.path.join(page_img_dir, f"{slug}-01.webp")
            with open(seed_path, "wb") as f:
                f.write(base64.b64decode(seed_b64))
            
            alt_text = generate_alt_text(seed_b64)
            images_metadata.append({
                "url": f"/wedding-images/{slug}/{slug}-01.webp",
                "alt": alt_text
            })
            
            # Framings for variation
            framings = [
                f"Wide angle shot of the empty wedding reception hall showing the {page['theme']} decorated tables.",
                f"Close-up of the bridal bouquet matching the {page['theme']} floral design.",
                f"Close-up of a groom's boutonniere featuring {page['theme']} floral accents.",
                f"A magnificent {page['theme']} floral wedding arch for the ceremony, empty background.",
                f"A tall {page['theme']} floral centerpiece on a glass vase, elegant table setting.",
                f"Detail shot of the {page['theme']} cloth napkins and menu card decorated with a single eucalyptus leaf.",
                f"An outdoor aisle decorated with {page['theme']} floral arrangements along the chairs."
            ]
            
            # Generate 7 variations using the seed
            for i, frame in enumerate(framings, 2):
                print(f"  Generating Variation {i} for {slug} ({frame[:30]}...)...")
                var_prompt = f"Cinematic editorial wedding photography. {frame} Maintain the exact same style, lighting, and color palette as the reference. No people, empty scene."
                var_b64 = generate_image(var_prompt, reference_b64=seed_b64)
                if var_b64:
                    var_path = os.path.join(page_img_dir, f"{slug}-0{i}.webp")
                    with open(var_path, "wb") as f:
                        f.write(base64.b64decode(var_b64))
                    var_alt = generate_alt_text(var_b64)
                    images_metadata.append({
                        "url": f"/wedding-images/{slug}/{slug}-0{i}.webp",
                        "alt": var_alt
                    })
                time.sleep(2) # Rate limit

    page_data = {
        "slug": slug,
        "h1_title": to_title_case(page_content.get("h1_title", slug.replace("-", " ").title())),
        "title": to_title_case(page_content.get("title", slug.replace("-", " ").title())),
        "meta_description": page_content.get("meta_description", ""),
        "content_html": page_content.get("content_html", ""),
        "images": images_metadata,
        "related_links": []
    }
    
    return page_data

def main():
    all_pages = []
    
    for page in PAGES:
        p_data = build_page_data(page)
        if p_data:
            all_pages.append(p_data)
        time.sleep(2)
        
    final_json = {"pages": all_pages}
    with open(os.path.join(DATA_DIR, "data.json"), "w", encoding="utf-8") as f:
        json.dump(final_json, f, indent=4, ensure_ascii=False)
        
    print("SEO Data and Images Generation Complete!")

if __name__ == "__main__":
    main()
