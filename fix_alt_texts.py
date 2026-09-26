import json
import urllib.request
import base64
import os
import time

API_KEY = "REDACTED_API_KEY"

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
    
    for _ in range(3):
        try:
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode('utf-8'))
                return result['candidates'][0]['content']['parts'][0]['text'].strip()
        except Exception as e:
            print(f"Alt text error: {e}")
            time.sleep(2)
    return "Wedding floral arrangement"

data_file = r"d:\project\plantsmag\plantsmag-nextjs-apps\public\wedding-data\data.json"
with open(data_file, "r") as f:
    data = json.load(f)

for page in data['pages']:
    if page['slug'] == 'sage-green-wedding-flowers':
        for img in page['images']:
            img_path = os.path.join(r"d:\project\plantsmag\plantsmag-nextjs-apps\public", img['url'].strip('/'))
            print(f"Processing {img_path}")
            with open(img_path, "rb") as img_file:
                b64 = base64.b64encode(img_file.read()).decode('utf-8')
            new_alt = generate_alt_text(b64)
            print(f"Old alt: {img['alt']} -> New alt: {new_alt}")
            img['alt'] = new_alt
            time.sleep(2)

with open(data_file, "w") as f:
    json.dump(data, f, indent=4)

print("Alt texts updated successfully!")
