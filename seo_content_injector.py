import os
import urllib.request
import json
import base64
import time

WP_USER = 'n8n-bloger'
WP_APP_PASS = 'VQ05 3amn qMzu aPkX VLsu 6XiA'
auth = base64.b64encode(f"{WP_USER}:{WP_APP_PASS}".encode()).decode('utf-8')
headers = {
    'Authorization': f'Basic {auth}',
    'Content-Type': 'application/json'
}

GEMINI_API_KEY = 'REDACTED_API_KEY'

def generate_text(prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.7}
    }
    req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers={'Content-Type': 'application/json'})
    try:
        resp = urllib.request.urlopen(req, timeout=30)
        res_data = json.loads(resp.read().decode())
        text = res_data['candidates'][0]['content']['parts'][0]['text']
        if text.startswith('```html'): text = text[7:]
        if text.startswith('```'): text = text[3:]
        if text.endswith('```'): text = text[:-3]
        return text.strip()
    except Exception as e:
        print("Gemini API error:", e)
        return ""

def get_post_content(post_id):
    req = urllib.request.Request(f'https://plantsmag.com/wp-json/wp/v2/posts/{post_id}', headers=headers)
    try:
        resp = urllib.request.urlopen(req, timeout=30)
        data = json.loads(resp.read().decode())
        return data['content']['rendered'], data['title']['rendered']
    except:
        return "", ""

def update_post_content(post_id, new_content):
    post_data = {"content": new_content}
    req = urllib.request.Request(
        f'https://plantsmag.com/wp-json/wp/v2/posts/{post_id}',
        data=json.dumps(post_data).encode(),
        headers=headers,
        method='POST'
    )
    try:
        urllib.request.urlopen(req, timeout=30)
        return True
    except Exception as e:
        print("Failed to update post:", e)
        return False

# Read valid urls
with open('unindexed_valid_urls.txt', 'r') as f:
    lines = [line.strip() for line in f.readlines() if line.strip()]

posts = []
print("Fetching word counts...")
for line in lines:
    parts = line.split(',')
    if len(parts) != 2: continue
    url, pid = parts
    content, title = get_post_content(pid)
    word_count = len(content.split())
    posts.append({'id': pid, 'url': url, 'title': title, 'content': content, 'words': word_count})

# Sort by word count, ascending
posts.sort(key=lambda x: x['words'])

# Take the 50 thinnest articles
target_posts = posts[:50]
print(f"Targeting {len(target_posts)} thinnest articles for SEO expansion...")

for i, p in enumerate(target_posts):
    print(f"[{i+1}/50] Upgrading '{p['title']}' ({p['words']} words)...")
    
    # Check if already expanded
    if "seo-expert-faq" in p['content'] or "pro-tips-section" in p['content']:
        print("  Already expanded. Skipping.")
        continue
        
    prompt = f"""
    You are an expert botanist and SEO specialist.
    I have an article titled "{p['title']}".
    Write an advanced SEO expansion section in pure HTML format (no markdown fences, just HTML tags).
    
    Include:
    1. A `<div class="pro-tips-section">` containing 2-3 highly advanced "Pro Tips" or "Experience-based" insights about the topic (EEAT compliant).
    2. A `<div class="seo-expert-faq">` containing 3 Frequently Asked Questions with detailed answers. Wrap the FAQ section with FAQPage Schema JSON-LD so Google understands it.
    
    Only output the raw HTML and JSON-LD script tag. Do not include the original article.
    """
    
    expansion_html = generate_text(prompt)
    if expansion_html:
        new_content = p['content'] + "\n<hr>\n" + expansion_html
        success = update_post_content(p['id'], new_content)
        if success:
            print(f"  Successfully upgraded.")
        time.sleep(2)
    else:
        print("  Failed to generate expansion.")
        
print("SEO Expansion complete.")
