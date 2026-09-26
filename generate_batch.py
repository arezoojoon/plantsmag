from google import genai
import json
import os

API_KEY = "REDACTED_API_KEY" 
client = genai.Client(api_key=API_KEY)

topics = [
    {
        "title": "The Future of Houseplants: Why LECA and Pon are Replacing Soil in 2026",
        "image": "leca_pon_houseplants_1776663127679.png"
    },
    {
        "title": "Tissue Culture Monstera: How the Rare Plant Market Crashed and What it Means for You",
        "image": "tissue_culture_monstera_1776663145306.png"
    },
    {
        "title": "Banish Fungus Gnats Forever: The Biological Control Revolution",
        "image": "fungus_gnats_biological_control_1776663181428.png"
    },
    {
        "title": "High-Tech Grow Tents: Transforming Spare Closets into Rare Anthurium Greenhouses",
        "image": "indoor_grow_tent_anthuriums_1776663197113.png"
    },
    {
        "title": "The Variegated Plant Craze: Understanding Genetic Mutations and Reverting",
        "image": "variegated_monstera_albo_1776663220767.png"
    },
    {
        "title": "Bioactive Terrariums: Merging Houseplants with Micro-Ecosystems",
        "image": "bioactive_terrarium_ecosystem_1776663236589.png"
    },
    {
        "title": "The Ultimate Guide to Plant Node Propagation & Air Layering",
        "image": "plant_node_propagation_1776663251054.png"
    }
]

articles_data = []

for topic in topics:
    print(f"Generating content for: {topic['title']}")
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=f"You are a top-tier SEO houseplant expert. Write a comprehensive, 1000-word deep-dive article on the topic: '{topic['title']}' for a houseplant blog 'PlantsMag'. This is a trending 'news jacking' style article. Divide it into distinct sections with h2 tags. Insert a bulleted list for key takeaways. Format entirely in standard HTML (use <p>, <h2>, <ul>). Do not use markdown wrappers. Remove all ```html tags."
        )
        text = response.text
        if text.startswith("```html"): text = text[7:]
        if text.endswith("```"): text = text[:-3]
        
        articles_data.append({
            "title": topic['title'],
            "content": text.strip(),
            "image": topic['image']
        })
    except Exception as e:
        print(f"Error on {topic['title']}: {e}")

output_path = "d:\\project\\plantsmag\\articles.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(articles_data, f, ensure_ascii=False, indent=4)

print(f"Successfully generated {len(articles_data)} articles and saved to {output_path}")
