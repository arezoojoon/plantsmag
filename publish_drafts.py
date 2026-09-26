import urllib.request
import urllib.parse
import json
import base64

WP_USER = 'n8n-bloger'
WP_APP_PASS = 'VQ05 3amn qMzu aPkX VLsu 6XiA'
auth = base64.b64encode(f"{WP_USER}:{WP_APP_PASS}".encode()).decode('utf-8')

headers = {
    'Authorization': f'Basic {auth}',
    'Content-Type': 'application/json'
}

# Fetch all drafts
req = urllib.request.Request('https://plantsmag.com/wp-json/wp/v2/posts?status=draft&per_page=100', headers=headers)
try:
    with urllib.request.urlopen(req) as response:
        drafts = json.loads(response.read().decode())
        print(f"Found {len(drafts)} drafts.")
        for draft in drafts:
            post_id = draft['id']
            title = draft['title']['rendered']
            print(f"Publishing: {title} (ID: {post_id})")
            
            update_req = urllib.request.Request(
                f'https://plantsmag.com/wp-json/wp/v2/posts/{post_id}',
                data=json.dumps({"status": "publish"}).encode(),
                headers=headers,
                method='POST'
            )
            urllib.request.urlopen(update_req)
        print("Done!")
except Exception as e:
    print(f"Error: {e}")
