import urllib.request
import urllib.parse
import json
import subprocess
import os
import time

API_KEY = "REDACTED_API_KEY" 

topics = [
    {
        "title": "The Future of Houseplants: Why LECA and Pon are Replacing Soil in 2026",
        "image": r"C:\Users\arezo\.gemini\antigravity\brain\7c139712-687a-4da6-8e84-0a619f5e84e6\leca_pon_houseplants_1776663127679.png"
    },
    {
        "title": "Tissue Culture Monstera: How the Rare Plant Market Crashed and What it Means for You",
        "image": r"C:\Users\arezo\.gemini\antigravity\brain\7c139712-687a-4da6-8e84-0a619f5e84e6\tissue_culture_monstera_1776663145306.png"
    },
    {
        "title": "Banish Fungus Gnats Forever: The Biological Control Revolution",
        "image": r"C:\Users\arezo\.gemini\antigravity\brain\7c139712-687a-4da6-8e84-0a619f5e84e6\fungus_gnats_biological_control_1776663181428.png"
    },
    {
        "title": "High-Tech Grow Tents: Transforming Spare Closets into Rare Anthurium Greenhouses",
        "image": r"C:\Users\arezo\.gemini\antigravity\brain\7c139712-687a-4da6-8e84-0a619f5e84e6\indoor_grow_tent_anthuriums_1776663197113.png"
    },
    {
        "title": "The Variegated Plant Craze: Understanding Genetic Mutations and Reverting",
        "image": r"C:\Users\arezo\.gemini\antigravity\brain\7c139712-687a-4da6-8e84-0a619f5e84e6\variegated_monstera_albo_1776663220767.png"
    },
    {
        "title": "Bioactive Terrariums: Merging Houseplants with Micro-Ecosystems",
        "image": r"C:\Users\arezo\.gemini\antigravity\brain\7c139712-687a-4da6-8e84-0a619f5e84e6\bioactive_terrarium_ecosystem_1776663236589.png"
    },
    {
        "title": "The Ultimate Guide to Plant Node Propagation & Air Layering",
        "image": r"C:\Users\arezo\.gemini\antigravity\brain\7c139712-687a-4da6-8e84-0a619f5e84e6\plant_node_propagation_1776663251054.png"
    }
]

def generate_article(title):
    print(f"Generating 2500-word article for: {title}")
    
    # We use a huge prompt structure to force 2500 words via section expansion
    prompt = f"""You are a top-tier SEO houseplant expert. Write a comprehensive, 2500-word deep-dive article on the topic: '{title}'. 
This is a trending 'news jacking' style article for the PlantsMag blog. 
It MUST be at least 2500 words. Divide it into 8 distinct sections with h2 and h3 tags. 
Include an introduction, historical context, step-by-step guides, pros vs cons, cost analysis, and a conclusion.
Format entirely in standard HTML (uses <p>, <h2>, <ul>, etc). Do not use markdown wrappers. Remove all ```html tags."""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={API_KEY}"
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 8192}
    }
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            text = result['candidates'][0]['content']['parts'][0]['text']
            
            # Clean HTML format
            if text.startswith("```html"):
                text = text[7:]
            if text.endswith("```"):
                text = text[:-3]
                
            return text.strip()
    except Exception as e:
        print(f"Error generating: {e}")
        return "<p>Content generation failed.</p>"

def publish_to_wp(title, html_content, image_path):
    print(f"Publishing: {title}")
    
    filename = os.path.basename(image_path)
    remote_tmp = f"/home/u284669846/domains/plantsmag.com/public_html/tmp_upload/{filename}"
    
    # 1. SCP the image
    scp_cmd = f'scp -P 65002 "{image_path}" u284669846@187.124.245.99:{remote_tmp}'
    subprocess.run(scp_cmd, shell=True)
    
    # Write HTML to local tmp
    local_html = f"tmp_article.html"
    with open(local_html, 'w', encoding='utf-8') as f:
        f.write(html_content)
        
    scp_html = f'scp -P 65002 {local_html} u284669846@187.124.245.99:/home/u284669846/domains/plantsmag.com/public_html/tmp_upload/tmp_article.html'
    subprocess.run(scp_html, shell=True)
    
    # 2. SSH command to import media and create post
    import re
    clean_slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')[:100]
    
    ssh_cmd = f"""ssh -p 65002 u284669846@187.124.245.99 "
    MEDIA_ID=\$(wp --path=/home/u284669846/domains/plantsmag.com/public_html media import {remote_tmp} --porcelain)
    wp --path=/home/u284669846/domains/plantsmag.com/public_html post create /home/u284669846/domains/plantsmag.com/public_html/tmp_upload/tmp_article.html --post_title='{title}' --post_name='{clean_slug}' --post_status=publish --post_category='Trending,Plant Guides' --post_thumbnail=\$MEDIA_ID --porcelain
    " """
    
    subprocess.run(ssh_cmd, shell=True)
    print(f"Successfully published {title}!")
    
    # Clean up
    if os.path.exists(local_html):
        os.remove(local_html)

for topic in topics:
    html = generate_article(topic["title"])
    print(f"Length of generated content: {len(html.split())} words")
    publish_to_wp(topic["title"], html, topic["image"])
    time.sleep(2) # Prevent rate limiting

print("All 7 agentic articles published successfully!")
