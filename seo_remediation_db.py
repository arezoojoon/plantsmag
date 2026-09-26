import requests
from requests.auth import HTTPBasicAuth
import sys
import io
import re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

WP_URL = "https://plantsmag.com/wp-json/wp/v2"
USER = "n8n-bloger"
PASS = "VQ05 3amn qMzu aPkX VLsu 6XiA"
AUTH = HTTPBasicAuth(USER, PASS)

print("Updating About Us page (ID: 31)...")
about_res = requests.get(f"{WP_URL}/pages/31?context=edit", auth=AUTH)
if about_res.status_code == 200:
    page = about_res.json()
    content = page['content']['raw']
    # Replace false claims
    new_content = content.replace("Every guide is researched, tested, and written to give you care advice you can actually trust.", "We evaluate products using manufacturer specifications, verified customer feedback, horticultural guidance and publicly available testing data.")
    
    if new_content != content:
        res = requests.post(f"{WP_URL}/pages/31", json={"content": new_content}, auth=AUTH)
        print(f"About Us updated: {res.status_code}")
    else:
        print("About Us already compliant.")
else:
    print(f"Failed to fetch About Us: {about_res.status_code}")

print("\nScanning all posts for AI footprints and false claims...")

page = 1
total_pages = 1
affected_posts = 0

while page <= total_pages:
    print(f"Fetching page {page} of posts...")
    res = requests.get(f"{WP_URL}/posts?context=edit&per_page=100&page={page}", auth=AUTH)
    if res.status_code != 200:
        break
    
    if page == 1:
        total_pages = int(res.headers.get('X-WP-TotalPages', 1))
        
    posts = res.json()
    for post in posts:
        content = post['content']['raw']
        original_content = content
        
        # Remove AI footprint
        content = content.replace("Pro Tips for Advanced Plant Care App Users (EEAT Compliant Insights)", "")
        # Remove specific sentences mentioning "months testing"
        content = re.sub(r'[^.]*months testing products[^.]*\.', '', content, flags=re.IGNORECASE)
        
        # Look for leaked schema strings like {"@context" or "FAQPage" in visible text (if they are not inside script tags)
        # We will just do a simple check: if we see "```json" or similar.
        content = content.replace("```json", "")
        content = content.replace("```", "")
        
        if content != original_content:
            update_res = requests.post(f"{WP_URL}/posts/{post['id']}", json={"content": content}, auth=AUTH)
            print(f"  -> Fixed Post ID {post['id']} ({post['slug']}): {update_res.status_code}")
            affected_posts += 1
            
    page += 1

print(f"\nRemediation complete. Fixed {affected_posts} posts.")
