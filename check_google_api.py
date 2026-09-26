import paramiko, sys, time, json
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Test Google Indexing API with the key - check actual response
import urllib.request
import urllib.parse

KEY_FILE = r'd:\project\artinwebs.org\scripts\google_indexing_key.json'

with open(KEY_FILE, 'r') as f:
    key_data = json.load(f)

print(f"Service Account: {key_data['client_email']}")
print(f"Project: {key_data['project_id']}")
print()
print("IMPORTANT: For Google Indexing API to work, you need to:")
print()
print("1. Go to Google Search Console: https://search.google.com/search-console")
print("2. Select your property: plantsmag.com")
print("3. Go to: Settings → Users and permissions")
print("4. Click 'Add user'")
print("5. Enter this email as OWNER:")
print(f"   {key_data['client_email']}")
print()
print("Without this step, the API returns 403/0 confirmations.")
print("After adding as Owner, Google Indexing API will confirm all submitted URLs.")
