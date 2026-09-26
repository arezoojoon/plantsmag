from google import genai
import subprocess
import os

API_KEY = "REDACTED_API_KEY" 
client = genai.Client(api_key=API_KEY)

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

for topic in topics:
    print(f"\n--- processing {topic['title']} ---", flush=True)
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=f"Write a 1500-word highly detailed article about '{topic['title']}' for a houseplant blog. Use standard HTML, h2 tags, ul. Don't use markdown ticks."
        )
        text = response.text
        if text.startswith("```html"): text = text[7:]
        if text.endswith("```"): text = text[:-3]
        text = text.replace("'", "\\'") # escape for Bash
        
        # SCP image
        filename = os.path.basename(topic['image'])
        r_img_path = f"/home/u284669846/domains/plantsmag.com/public_html/tmp_upload/{filename}"
        subprocess.run(f'scp -P 65002 "{topic["image"]}" u284669846@187.124.245.99:{r_img_path}', shell=True)
        print("Scp image done", flush=True)
        
        # Write HTML locally and SCP it
        local_html = "d:\\project\\plantsmag\\tmp.html"
        with open(local_html, "w", encoding="utf-8") as f:
            f.write(text.strip())
        subprocess.run(f'scp -P 65002 "{local_html}" u284669846@187.124.245.99:/home/u284669846/domains/plantsmag.com/public_html/tmp_upload/tmp.html', shell=True)
        print("Scp HTML done", flush=True)
        
        # SSH command
        ssh_cmd = f"""ssh -p 65002 u284669846@187.124.245.99 "
        MEDIA_ID=\$(wp --path=/home/u284669846/domains/plantsmag.com/public_html media import {r_img_path} --porcelain)
        wp --path=/home/u284669846/domains/plantsmag.com/public_html post create /home/u284669846/domains/plantsmag.com/public_html/tmp_upload/tmp.html --post_title='{topic["title"]}' --post_status=publish --post_category='Trending' --post_thumbnail=\$MEDIA_ID --porcelain
        " """
        res = subprocess.run(ssh_cmd, shell=True, capture_output=True, text=True)
        print("SSH done:", res.stdout, res.stderr, flush=True)
        
    except Exception as e:
        print(f"Failed: {e}", flush=True)
