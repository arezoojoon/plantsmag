import requests
import json
import re
from datetime import datetime

WP_API_URL = "https://plantsmag.com/wp-json/wp/v2/posts"
# If there are many posts, we should handle pagination
PER_PAGE = 100

def check_posts():
    print("Starting WordPress content audit...")
    page = 1
    found_elara = []
    found_persian = []
    found_date_mismatch = []

    while True:
        try:
            print(f"Fetching page {page}...")
            response = requests.get(f"{WP_API_URL}?per_page={PER_PAGE}&page={page}")
            
            if response.status_code == 400:
                # We've exceeded the maximum number of pages
                break
                
            response.raise_for_status()
            posts = response.json()
            
            if not posts:
                break
                
            for post in posts:
                post_id = post['id']
                title = post['title']['rendered']
                content = post['content']['rendered']
                link = post['link']
                date_str = post['date']
                
                # Check for "Dr. Elara Vance"
                if "Dr. Elara Vance" in content or "Dr. Elara Vance" in title:
                    found_elara.append({'id': post_id, 'title': title, 'link': link})
                    
                # Check for "ما به‌عنوان روزنامه‌نگاران گیاه و استراتژیست‌های سئو"
                # Doing a slightly more robust check ignoring zero-width spaces etc if needed, but exact string first
                persian_phrase = "ما به‌عنوان روزنامه‌نگاران گیاه و استراتژیست‌های سئو"
                persian_alt = "ما به عنوان روزنامه نگاران گیاه"
                if persian_phrase in content or persian_alt in content:
                    found_persian.append({'id': post_id, 'title': title, 'link': link})
                    
                # Check for 2024 in title but 2026 in date
                # Date format is like "2026-08-19T10:00:00"
                if "2024" in title and "2026" in date_str:
                    found_date_mismatch.append({'id': post_id, 'title': title, 'link': link, 'date': date_str})

            page += 1
            
        except Exception as e:
            print(f"Error fetching page {page}: {e}")
            break

    # Print Report
    print("\n" + "="*50)
    print("AUDIT REPORT")
    print("="*50)
    
    print(f"\n1. Posts containing 'Dr. Elara Vance': {len(found_elara)}")
    for p in found_elara:
        print(f"   - {p['title']} ({p['link']})")

    print(f"\n2. Posts with 2024 in title but published in 2026: {len(found_date_mismatch)}")
    for p in found_date_mismatch:
        print(f"   - {p['title']} ({p['link']})")

    print(f"\n3. Posts containing Persian phrase: {len(found_persian)}")
    for p in found_persian:
        print(f"   - {p['title']} ({p['link']})")
        
    print("\nDone.")

if __name__ == "__main__":
    check_posts()
