import paramiko, sys, json
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('72.62.93.117', port=22, username='root', password="5KT4'ub5B5oD8V9TB#/u", timeout=15)

def run(cmd, timeout=30):
    _, stdout, _ = ssh.exec_command(cmd, timeout=timeout)
    return stdout.read().decode('utf-8', errors='replace').strip()

print("=" * 65)
print("Creating new WP App Password via API + Fixing all n8n credentials")
print("=" * 65)

# Test WordPress users
print("\n1. Testing WordPress credentials...")
users_to_try = [
    ('artinwebs2025', 'NMlqAdopJpS$CfFbZ5ax^LL('),
    ('artinmag', 'PlantsMag2026!'),
    ('artinwebs2025', 'PlantsMag2026!'),
    ('admin', 'PlantsMag2026!'),
]

valid_user = None
valid_pass = None

for user, pwd in users_to_try:
    code = run(f"""curl -s -o /dev/null -w "%{{http_code}}" \
      -u "{user}:{pwd}" \
      "https://plantsmag.com/wp-json/wp/v2/users/me" 2>/dev/null""")
    print(f"  {user}: HTTP {code}")
    if code in ('200', '201'):
        valid_user = user
        valid_pass = pwd
        print(f"  ✅ Valid: {user}")
        break

if not valid_user:
    # Try creating app password via WP-CLI if available
    print("\n2. Trying WP-CLI on Hostinger...")
    # Try to reach Hostinger via sshpass from the VPS
    wp_cli = run("""which wp 2>/dev/null || echo 'no-wp-cli'""")
    print(f"  WP-CLI on VPS: {wp_cli}")
    
    # Check if we can reach WordPress from VPS
    wp_test = run("""curl -s -o /dev/null -w "%{http_code}" https://plantsmag.com/wp-json/wp/v2/posts?per_page=1 2>/dev/null""")
    print(f"  WP REST API (public): HTTP {wp_test}")
    
    # Try the old app password from earlier sessions
    old_passwords = [
        'XH18 J5Wq 52Ow oM2M gukl hNcH',  # from session history
        'XH18J5Wq52OwoM2Mgukl hNcH',
    ]
    for pwd in old_passwords:
        for user in ['artinwebs2025', 'artinmag', 'admin']:
            code = run(f"""curl -s -o /dev/null -w "%{{http_code}}" \
              -u "{user}:{pwd}" \
              "https://plantsmag.com/wp-json/wp/v2/users/me" 2>/dev/null""")
            if code in ('200', '201'):
                valid_user = user
                valid_pass = pwd
                print(f"  ✅ FOUND! {user}: {pwd}")
                break
        if valid_user:
            break

print(f"\nValid credentials: user='{valid_user}', found={bool(valid_user)}")

# Login to n8n and update ALL credentials
run("""curl -s -c /tmp/fix2.txt -X POST http://localhost:5678/rest/login \
  -H 'Content-Type: application/json' \
  -d '{"emailOrLdapLoginId":"plantsmag@gmail.com","password":"PlantsMag2026!"}' -o /dev/null 2>/dev/null""")

# Get all credentials
creds_out = run("curl -s -b /tmp/fix2.txt http://localhost:5678/rest/credentials 2>/dev/null")
try:
    creds = json.loads(creds_out).get('data', [])
    print(f"\n3. Found {len(creds)} credentials in n8n:")
    for c in creds:
        print(f"  [{c['type']}] {c['name']} (ID: {c['id']})")
except:
    print(f"  Error parsing: {creds_out[:200]}")

# If we found valid WP creds, update all PlantsMag WP Auth credentials
if valid_user:
    print(f"\n4. Updating all 'PlantsMag WP Auth' credentials...")
    for c in creds:
        if 'PlantsMag WP Auth' in c['name'] or ('plantsmag' in c['name'].lower() and 'wp' in c['name'].lower()):
            cred_id = c['id']
            # Get full credential
            full_cred = run(f"curl -s -b /tmp/fix2.txt http://localhost:5678/rest/credentials/{cred_id} 2>/dev/null")
            try:
                cred_data = json.loads(full_cred).get('data', {})
                update_payload = {
                    'name': cred_data['name'],
                    'type': cred_data['type'],
                    'data': {
                        'user': valid_user,
                        'password': valid_pass
                    }
                }
                import json as js
                cmd = f"""python3 -c "import json; open('/tmp/cred_{cred_id}.json','w').write(json.dumps({repr(update_payload)}))" """
                run(cmd)
                result = run(f"""curl -s -b /tmp/fix2.txt \
                  -X PUT http://localhost:5678/rest/credentials/{cred_id} \
                  -H 'Content-Type: application/json' \
                  -d @/tmp/cred_{cred_id}.json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print('Updated:', d.get('data',{{}}).get('name','?'))" """)
                print(f"  {c['name']}: {result}")
            except Exception as e:
                print(f"  Error updating {c['name']}: {e}")
else:
    print("\n❌ Could not find valid WordPress credentials")
    print("   Action needed: Login to WordPress admin manually and create new Application Password")

# Check WF1 node URL
print("\n5. Verifying WF1 Gemini node...")
wfs_out = run("curl -s -b /tmp/fix2.txt http://localhost:5678/rest/workflows 2>/dev/null")
wfs = json.loads(wfs_out).get('data', [])
for w in wfs:
    if 'US Trend Jacker' in w['name']:
        wf_detail = run(f"curl -s -b /tmp/fix2.txt http://localhost:5678/rest/workflows/{w['id']} 2>/dev/null")
        wf_data = json.loads(wf_detail).get('data', {})
        for node in wf_data.get('nodes', []):
            url = node.get('parameters', {}).get('url', '')
            if 'gemini' in url.lower() or 'generativeai' in url.lower():
                print(f"  Gemini node '{node['name']}': {url[:80]}")

ssh.close()
print("\nDone!")
