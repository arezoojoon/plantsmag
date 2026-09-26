import requests
from requests.auth import HTTPBasicAuth
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

URL = "https://plantsmag.com/wp-json/wp/v2/posts"
USER = "n8n-bloger"
PASS = "VQ05 3amn qMzu aPkX VLsu 6XiA"
AUTH = HTTPBasicAuth(USER, PASS)

def get_post_by_slug(slug):
    res = requests.get(f"{URL}?slug={slug}", auth=AUTH)
    if res.status_code == 200 and len(res.json()) > 0:
        return res.json()[0]['id']
    return None

print("Starting SEO Remediation...")

# 1. Delete json-slug
pid = get_post_by_slug("json-slug")
if pid:
    res = requests.delete(f"{URL}/{pid}?force=true", auth=AUTH)
    print(f"Deleted json-slug (ID: {pid}): {res.status_code}")
else:
    print("json-slug not found.")

# 2. Update The Hydrogen Peroxide Root Bath
slug1 = "the-hydrogen-peroxide-root-bath-rescuing-rotting-monsteras-instantly"
pid1 = get_post_by_slug(slug1)
if pid1:
    res = requests.post(f"{URL}/{pid1}", json={"title": "How to Use Hydrogen Peroxide for Houseplant Root Rot Treatment"}, auth=AUTH)
    print(f"Updated H2O2 Root Rot (ID: {pid1}): {res.status_code}")
else:
    print(f"{slug1} not found.")

# 3. Update Hydrogen Peroxide vs Neem Oil
slug2 = "hydrogen-peroxide-vs-neem-oil-the-ultimate-pest-control-showdown"
pid2 = get_post_by_slug(slug2)
if pid2:
    res = requests.post(f"{URL}/{pid2}", json={"title": "Hydrogen Peroxide vs Neem Oil for Indoor Plant Pest Control"}, auth=AUTH)
    print(f"Updated H2O2 vs Neem (ID: {pid2}): {res.status_code}")
else:
    print(f"{slug2} not found.")

print("SEO Remediation Complete.")
