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
        "generationConfig": {"temperature": 0.8}
    }
    req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers={'Content-Type': 'application/json'})
    resp = urllib.request.urlopen(req)
    res_data = json.loads(resp.read().decode())
    text = res_data['candidates'][0]['content']['parts'][0]['text']
    if text.startswith('```json'): text = text[7:]
    if text.startswith('```html'): text = text[7:]
    if text.startswith('```'): text = text[3:]
    if text.endswith('```'): text = text[:-3]
    return text.strip()

def main():
    print("Generating 10-part series outline...")
    outline_prompt = """
    We need a 10-part educational, story-like article series for local SEO in the UAE (Dubai/Abu Dhabi). 
    Product: "Click and Grow Smart Garden 9"
    The series should follow a continuous human experience (e.g. from struggling with dead herbs in Dubai heat, to unboxing, planting, waiting, harvesting, and expanding).
    Return a JSON array of 10 objects, each with 'title' (SEO optimized for UAE, e.g. "Dubai Indoor Gardening", "Smart Garden 9 Review UAE"), 'slug', and 'focus' (what part of the story).
    Strictly output valid JSON only.
    """
    outline_json = generate_text(outline_prompt)
    try:
        articles = json.loads(outline_json)
    except:
        print("Failed to parse outline JSON. Raw:", outline_json)
        return

    published_links = []
    
    for i, art in enumerate(articles):
        print(f"Generating Part {i+1}: {art['title']}")
        
        content_prompt = f"""
        Write Part {i+1} of 10 in our UAE Smart Garden story series.
        Title: {art['title']}
        Focus: {art['focus']}
        
        Requirements:
        1. Write in HTML format (no html/head/body tags, just h2, p, ul).
        2. Tone: Human-like, experiential, like a Dubai resident sharing their journey.
        3. Include 2-3 educational tips for UAE indoor gardeners.
        4. MUST include exactly this affiliate link naturally in the text: <a href="https://link.amazon/B05d6ohqv" target="_blank" rel="nofollow">Click & Grow Smart Garden 9</a>
        5. Include a placeholder for the user's images: <p style="text-align: center;"><em>[لطفاً عکس محصول را اینجا قرار دهید]</em></p>
        6. End with a "teaser" for the next part (if not part 10) to encourage reading the series.
        7. Output strictly the HTML content, nothing else. Do not wrap in markdown fences.
        """
        
        content = generate_text(content_prompt)
        
        if published_links:
            prev_links_html = "<h3>Catch Up on the Series:</h3><ul>"
            for link in published_links[-3:]:
                prev_links_html += f"<li><a href='{link['url']}'>{link['title']}</a></li>"
            prev_links_html += "</ul>"
            content = content + "\n<hr>\n" + prev_links_html
            
        print(f"Publishing Part {i+1} to WordPress...")
        post_data = {
            "title": art['title'],
            "slug": art['slug'],
            "content": content,
            "status": "publish"
        }
        
        wp_req = urllib.request.Request(
            'https://plantsmag.com/wp-json/wp/v2/posts',
            data=json.dumps(post_data).encode(),
            headers=headers,
            method='POST'
        )
        try:
            resp = urllib.request.urlopen(wp_req)
            res_json = json.loads(resp.read().decode())
            pub_url = res_json['link']
            print(f"Published: {pub_url}")
            published_links.append({"title": art['title'], "url": pub_url})
        except Exception as e:
            print(f"Failed to publish part {i+1}:", e)
            
        time.sleep(3)

if __name__ == "__main__":
    main()
