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

cta_box = """
<div class="affiliate-disclosure" style="background-color: #f9f9f9; padding: 10px; margin-bottom: 20px; font-size: 0.9em; border-left: 4px solid #1e3932;">
    <em><strong>Affiliate Disclosure:</strong> Some of the links below may be affiliate links. We evaluate products using manufacturer specifications, verified customer feedback, horticultural guidance and publicly available testing data. If you click a link and make a purchase, we may earn a small commission at no extra cost to you.</em>
</div>
<div class="quick-comparison-box" style="border: 1px solid #ddd; padding: 20px; margin-bottom: 30px; border-radius: 8px; background: #fff;">
    <h3 style="margin-top: 0;">Quick Comparison</h3>
    <ul style="list-style-type: none; padding: 0; margin: 0;">
        <li style="margin-bottom: 15px; border-bottom: 1px solid #eee; padding-bottom: 10px;"><strong>Best Overall:</strong> <a href="#amazon" rel="nofollow noopener sponsored" class="btn btn-primary" style="background-color: #f90; color: #111; padding: 8px 15px; text-decoration: none; border-radius: 4px; float: right; font-weight: bold;">Check Current Price</a><div style="clear: both;"></div></li>
        <li style="margin-bottom: 15px; border-bottom: 1px solid #eee; padding-bottom: 10px;"><strong>Best Value:</strong> <a href="#amazon" rel="nofollow noopener sponsored" class="btn btn-primary" style="background-color: #f90; color: #111; padding: 8px 15px; text-decoration: none; border-radius: 4px; float: right; font-weight: bold;">Check Current Price</a><div style="clear: both;"></div></li>
        <li style="margin-bottom: 0px;"><strong>Budget Pick:</strong> <a href="#amazon" rel="nofollow noopener sponsored" class="btn btn-primary" style="background-color: #f90; color: #111; padding: 8px 15px; text-decoration: none; border-radius: 4px; float: right; font-weight: bold;">Check Current Price</a><div style="clear: both;"></div></li>
    </ul>
</div>
"""

post_table_ctas = """
<div class="table-ctas" style="margin-top: 15px; margin-bottom: 30px; text-align: center;">
    <a href="#amazon" rel="nofollow noopener sponsored" class="btn btn-primary" style="background-color: #f90; color: #111; padding: 10px 20px; text-decoration: none; border-radius: 4px; font-weight: bold; margin-right: 10px;">Check Best Overall Price</a>
    <a href="#amazon" rel="nofollow noopener sponsored" class="btn btn-primary" style="background-color: #f90; color: #111; padding: 10px 20px; text-decoration: none; border-radius: 4px; font-weight: bold;">Check Budget Pick Price</a>
</div>
"""

slugs = [
    "systemic-insecticide-granules-bonide-bioadvanced-comparison-2024",
    "pruning-shears-comparison-felco-fiskars-ars-2024"
]

for slug in slugs:
    res = requests.get(f"{WP_URL}/posts?slug={slug}&context=edit", auth=AUTH)
    if res.status_code == 200 and len(res.json()) > 0:
        post = res.json()[0]
        content = post['content']['raw']
        
        # Don't inject twice
        if "affiliate-disclosure" in content:
            print(f"Skipping {slug}, already has CTAs")
            continue
            
        # Insert CTA Box after first paragraph
        parts = content.split("</p>", 1)
        if len(parts) > 1:
            content = parts[0] + "</p>\n" + cta_box + parts[1]
        
        # Insert table CTAs after table, or at end
        if "</table>" in content:
            content = content.replace("</table>", "</table>\n" + post_table_ctas)
        else:
            content = content + "\n" + post_table_ctas
            
        update_res = requests.post(f"{WP_URL}/posts/{post['id']}", json={"content": content}, auth=AUTH)
        print(f"Updated {slug}: {update_res.status_code}")
    else:
        print(f"Could not find {slug}")

