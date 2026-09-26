import requests

url = "https://images.unsplash.com/photo-1545165375-1b744b9ed7c4?w=900&auto=format&fit=crop&q=80"
print(f"Downloading {url}...")
r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
if r.status_code == 200:
    with open(r'd:\project\plantsmag\plantsmag-premium\hero-plant.webp', 'wb') as f:
        f.write(r.content)
    print("Saved hero-plant.webp successfully.")
else:
    print(f"Failed to download: {r.status_code}")
