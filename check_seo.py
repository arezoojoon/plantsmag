import requests
r = requests.get('https://plantsmag.com/')
if 'Rank Math' in r.text:
    print("Rank Math is active!")
elif 'Yoast SEO' in r.text:
    print("Yoast is active!")
else:
    print("No obvious SEO plugin signature.")
