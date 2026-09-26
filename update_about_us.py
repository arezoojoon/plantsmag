import requests
from requests.auth import HTTPBasicAuth
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

WP_URL = "https://plantsmag.com/wp-json/wp/v2"
USER = "n8n-bloger"
PASS = "VQ05 3amn qMzu aPkX VLsu 6XiA"
AUTH = HTTPBasicAuth(USER, PASS)

content = """
<div class="about-us-container" style="max-width: 800px; margin: 0 auto; padding: 2rem 1rem;">
    <h2 style="font-size: 2.5rem; color: #1e3932; margin-bottom: 1.5rem; font-family: 'Outfit', sans-serif;">About PlantsMag</h2>
    <p style="font-size: 1.15rem; line-height: 1.8; color: #4a5568; margin-bottom: 1.5rem;">
        PlantsMag is a houseplant-care publication helping over 50,000 plant parents keep their indoor jungles alive and thriving. 
        Our team combines hands-on horticulture experience with AI-powered tools — including a Smart Watering Calculator and a Gemini-powered AI Plant Doctor — 
        to turn plant-care guesswork into precise, personalized guidance.
    </p>
    <p style="font-size: 1.15rem; line-height: 1.8; color: #4a5568;">
        Every guide is researched, tested, and written to give you care advice you can actually trust.
    </p>
</div>
"""

payload = {
    "content": content
}

print("Updating About Us page (ID: 31)...")
res = requests.post(f"{WP_URL}/pages/31", json=payload, auth=AUTH)
if res.status_code == 200:
    print("Successfully updated About Us page!")
else:
    print(f"Failed: {res.status_code} - {res.text}")
