#!/usr/bin/env python3
"""
PlantsMag Content Credibility Audit Script
==========================================
Finds and reports (does NOT modify) problematic content:
1. Fake expert quotes (Dr. Elara Vance, etc.)
2. Year mismatches in titles (2024 title on 2026 posts)
3. AI-reveal phrases ("as plant journalists", etc.)

Usage:
    python audit_content.py

Requirements:
    pip install requests
"""

import requests
import json
import re
from datetime import datetime

WP_BASE = "https://plantsmag.com/wp-json/wp/v2"

# WP Application Password — set these or use env vars
# WP_USER = "your_username"
# WP_PASS = "your_application_password"
# AUTH = (WP_USER, WP_PASS)
# For read-only public audit, no auth needed for published posts

FAKE_NAMES = ["Elara Vance", "Dr. Vance", "Horticultural Tech Analyst"]
AI_REVEAL_PHRASES = [
    "as plant journalists",
    "as seo strategists",
    "plant journalists and seo",
    "as journalists",
]
YEAR_MISMATCH_PATTERN = re.compile(r'\b(2024)\b', re.IGNORECASE)


def fetch_all_posts():
    posts = []
    page = 1
    while True:
        r = requests.get(
            f"{WP_BASE}/posts",
            params={"per_page": 100, "page": page, "_fields": "id,title,content,date,link"},
            timeout=30
        )
        if r.status_code != 200:
            break
        batch = r.json()
        if not batch:
            break
        posts.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    return posts


def audit_posts(posts):
    issues = {
        "fake_expert_quotes": [],
        "year_mismatches": [],
        "ai_reveal_phrases": [],
    }

    for post in posts:
        post_id = post.get("id")
        title = post.get("title", {}).get("rendered", "")
        content = post.get("content", {}).get("rendered", "")
        date_str = post.get("date", "")
        link = post.get("link", "")
        content_lower = content.lower()
        
        try:
            post_year = datetime.fromisoformat(date_str[:10]).year
        except Exception:
            post_year = None

        # Check for fake expert names
        for name in FAKE_NAMES:
            if name.lower() in content_lower:
                issues["fake_expert_quotes"].append({
                    "id": post_id,
                    "title": title,
                    "link": link,
                    "found": name,
                })
                break

        # Check for year mismatch (title says 2024, post year is 2025/2026)
        title_years = YEAR_MISMATCH_PATTERN.findall(title)
        if title_years and post_year and post_year > 2024:
            issues["year_mismatches"].append({
                "id": post_id,
                "title": title,
                "link": link,
                "title_says": title_years[0],
                "post_year": post_year,
            })

        # Check for AI-reveal phrases
        for phrase in AI_REVEAL_PHRASES:
            if phrase in content_lower:
                issues["ai_reveal_phrases"].append({
                    "id": post_id,
                    "title": title,
                    "link": link,
                    "found": phrase,
                })
                break

    return issues


def print_report(issues):
    print("\n" + "=" * 60)
    print("  PlantsMag Content Credibility Audit Report")
    print(f"  Run at: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)

    # Fake expert quotes
    print(f"\n🚨 FAKE EXPERT QUOTES ({len(issues['fake_expert_quotes'])} found)")
    print("   These must be removed IMMEDIATELY — highest risk for Amazon/AdSense review")
    for item in issues["fake_expert_quotes"]:
        print(f"   → Post #{item['id']}: {item['title'][:60]}")
        print(f"     Found: \"{item['found']}\"")
        print(f"     Edit: {item['link'].replace('plantsmag.com', 'plantsmag.com/wp-admin/post.php?action=edit&post=' + str(item['id']))}")

    # Year mismatches
    print(f"\n⚠️  TITLE YEAR MISMATCHES ({len(issues['year_mismatches'])} found)")
    print("   Title says 2024 but post was published in a later year")
    for item in issues["year_mismatches"]:
        print(f"   → Post #{item['id']}: {item['title'][:60]}")
        print(f"     Title year: {item['title_says']} | Post year: {item['post_year']}")
        print(f"     Link: {item['link']}")

    # AI-reveal phrases
    print(f"\n⚠️  AI-REVEAL PHRASES ({len(issues['ai_reveal_phrases'])} found)")
    print("   These expose AI authorship and hurt E-E-A-T signals")
    for item in issues["ai_reveal_phrases"]:
        print(f"   → Post #{item['id']}: {item['title'][:60]}")
        print(f"     Found: \"{item['found']}\"")
        print(f"     Link: {item['link']}")

    total = sum(len(v) for v in issues.values())
    print(f"\n{'=' * 60}")
    print(f"  Total issues found: {total}")
    print("=" * 60 + "\n")

    # Save to JSON for reference
    with open("audit_results.json", "w", encoding="utf-8") as f:
        json.dump(issues, f, ensure_ascii=False, indent=2)
    print("  Results saved to audit_results.json\n")


if __name__ == "__main__":
    print("Fetching posts from plantsmag.com...")
    posts = fetch_all_posts()
    print(f"  Found {len(posts)} published posts. Auditing...")
    issues = audit_posts(posts)
    print_report(issues)
