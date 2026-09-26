from PIL import Image
import os

img_path = r'C:\Users\arezo\.gemini\antigravity\brain\89aa66a9-49cb-4cff-90c3-1ff5d7afdaba\hero_plant_monstera_1781445236332.png'
out_dir = r'd:\project\plantsmag\plantsmag-premium\assets'
out_path = os.path.join(out_dir, 'hero-plant.webp')

if not os.path.exists(out_dir):
    os.makedirs(out_dir)

try:
    with Image.open(img_path) as img:
        # Resize if necessary (e.g., max width 1200px)
        img.thumbnail((1200, 1200))
        img.save(out_path, 'WEBP', quality=85)
    print("Successfully converted and saved hero-plant.webp")
except Exception as e:
    print(f"Error: {e}")
