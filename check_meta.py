import urllib.request
import re

urls = [
    'https://plantsmag.com/',
    'https://plantsmag.com/best-aroid-soil-mix-store-bought-vs-diy-2024/',
    'https://plantsmag.com/author/n8n-bloger/',
    'https://plantsmag.com/tag/houseplants/',
    'https://plantsmag.com/category/trending/'
]

for url in urls:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req).read().decode('utf-8', 'ignore')
        matches = re.findall(r'<meta[^>]*name=[\"\'\s]*robots[\"\'\s]*[^>]*>', html, re.IGNORECASE)
        print(f"\n{url}:")
        for m in matches:
            print("  " + m)
    except urllib.error.HTTPError as e:
        print(f"\n{url}: HTTP {e.code}")
    except Exception as e:
        print(f"\n{url}: {e}")
