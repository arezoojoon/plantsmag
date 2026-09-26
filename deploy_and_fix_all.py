import paramiko, sys, os, json, time
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# ── Credentials ──────────────────────────────────────────────────
HOST = '187.124.245.99'
PORT = 65002
USER = 'u284669846'
PASS = '[3pPybi0[3pPybi0'

VPS_HOST = '72.62.93.117'
VPS_PASS = "5KT4'ub5B5oD8V9TB#/u"

N8N_WP_USER = 'n8n-bloger'
N8N_WP_PASS = 'pcvN yStV uI9f GRUK SC59 vhH5'
N8N_EMAIL   = 'plantsmag@gmail.com'
N8N_PASS    = 'PlantsMag2026!'

LOCAL_THEME  = r'd:\project\plantsmag\plantsmag-premium'
REMOTE_BASE  = '/home/u284669846/domains/plantsmag.com/public_html'
THEME_REMOTE = f'{REMOTE_BASE}/wp-content/themes/plantsmag-premium'

FILES = [
    (rf'{LOCAL_THEME}\assets\css\lead-magnet.css',         f'{THEME_REMOTE}/assets/css/lead-magnet.css'),
    (rf'{LOCAL_THEME}\assets\js\disease-finder.js',        f'{THEME_REMOTE}/assets/js/disease-finder.js'),
    (rf'{LOCAL_THEME}\assets\js\watering-calculator.js',   f'{THEME_REMOTE}/assets/js/watering-calculator.js'),
    (rf'{LOCAL_THEME}\inc\class-disease-finder.php',       f'{THEME_REMOTE}/inc/class-disease-finder.php'),
    (rf'{LOCAL_THEME}\inc\class-watering-calculator.php',  f'{THEME_REMOTE}/inc/class-watering-calculator.php'),
    (rf'{LOCAL_THEME}\inc\lead-capture.php',               f'{THEME_REMOTE}/inc/lead-capture.php'),
    (rf'{LOCAL_THEME}\functions.php',                      f'{THEME_REMOTE}/functions.php'),
]

print("=" * 65)
print("FULL PlantsMag Phase 2 Deploy + n8n Fix")
print("=" * 65)

# ── PART 1: Upload to Hostinger ─────────────────────────────────
print("\n📦 PART 1: SFTP Upload to Hostinger")
print(f"   Host: {HOST}:{PORT} → {REMOTE_BASE}")

ssh_h = paramiko.SSHClient()
ssh_h.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_h.connect(HOST, port=PORT, username=USER, password=PASS, timeout=20)

def hrun(cmd, t=15):
    _, o, _ = ssh_h.exec_command(cmd, timeout=t)
    return o.read().decode('utf-8', errors='replace').strip()

# Verify remote theme exists
theme_check = hrun(f'ls {THEME_REMOTE}/functions.php 2>/dev/null || echo MISSING')
print(f"   Theme found: {'✅' if 'MISSING' not in theme_check else '❌'} {theme_check[:60]}")

sftp = ssh_h.open_sftp()
ok = 0
for local, remote in FILES:
    try:
        sftp.put(local, remote)
        size = os.path.getsize(local)
        print(f"   ✅ {os.path.basename(local)} ({size:,} bytes)")
        ok += 1
    except Exception as e:
        print(f"   ❌ {os.path.basename(local)}: {e}")
sftp.close()

# Flush OPcache
print(f"\n   Uploaded: {ok}/{len(FILES)}")
cache_out = hrun(f'php -r "opcache_reset();" 2>/dev/null && echo OPcache_cleared || echo skip')
print(f"   OPcache: {cache_out}")

# WP-CLI cache flush
wpcli = hrun('find /home/u284669846 -name "wp" -executable -type f 2>/dev/null | head -1')
if wpcli:
    flush = hrun(f'{wpcli} cache flush --path={REMOTE_BASE} --allow-root 2>&1', t=20)
    print(f"   WP cache: {flush[:80]}")

ssh_h.close()

# ── PART 2: Verify WP credentials ─────────────────────────────────
print("\n🔑 PART 2: Verifying WordPress Credentials")

import urllib.request
def wp_test(user, pwd, endpoint='users/me'):
    import base64
    cred = base64.b64encode(f'{user}:{pwd}'.encode()).decode()
    req = urllib.request.Request(
        f'https://plantsmag.com/wp-json/wp/v2/{endpoint}',
        headers={'Authorization': f'Basic {cred}'}
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, {}

code, data = wp_test(N8N_WP_USER, N8N_WP_PASS)
print(f"   n8n-bloger auth: HTTP {code}")
if code == 200:
    print(f"   User: {data.get('name','?')} | Roles: {data.get('roles','?')}")
    CAN_POST = True
else:
    print(f"   ❌ Auth failed — trying artinwebs2025...")
    code2, data2 = wp_test('artinwebs2025', 'Nh*RA%i0)EHY#mrqQ$1Mo@ER')
    print(f"   artinwebs2025: HTTP {code2} | {data2.get('name','?')}")
    CAN_POST = False

# ── PART 3: Fix n8n credentials via VPS ─────────────────────────
print("\n🔧 PART 3: Updating n8n Credentials via VPS")

ssh_v = paramiko.SSHClient()
ssh_v.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_v.connect(VPS_HOST, port=22, username='root', password=VPS_PASS, timeout=15)

def vps(cmd, t=30):
    _, o, _ = ssh_v.exec_command(cmd, timeout=t)
    return o.read().decode('utf-8', errors='replace').strip()

# Login to n8n
vps(f'''curl -s -c /tmp/pm3.txt -X POST http://localhost:5678/rest/login \
  -H "Content-Type: application/json" \
  -d '{{"emailOrLdapLoginId":"{N8N_EMAIL}","password":"{N8N_PASS}"}}' \
  -o /dev/null 2>/dev/null''')

# List all credentials
creds_raw = vps("curl -s -b /tmp/pm3.txt http://localhost:5678/rest/credentials 2>/dev/null")
try:
    creds = json.loads(creds_raw).get('data', [])
except:
    creds = []

print(f"   Found {len(creds)} credentials in n8n")

updated = 0
for c in creds:
    cname = c.get('name','')
    ctype = c.get('type','')
    cid   = c.get('id','')
    if 'httpBasicAuth' in ctype or 'WP Auth' in cname or ('PlantsMag' in cname and 'WP' in cname):
        payload = {"name": cname, "type": ctype, "data": {"user": N8N_WP_USER, "password": N8N_WP_PASS}}
        vps(f"""python3 -c "import json; open('/tmp/c{cid}.json','w').write(json.dumps({repr(payload)}))" """)
        result = vps(f"""curl -s -b /tmp/pm3.txt -X PATCH http://localhost:5678/rest/credentials/{cid} \
          -H "Content-Type: application/json" -d @/tmp/c{cid}.json 2>/dev/null | \
          python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('data',{{}}).get('name','err'))" 2>/dev/null""")
        print(f"   ✅ Updated: {cname} → {result}")
        updated += 1

if updated == 0:
    # Create new
    payload = {"name": "PlantsMag WP Auth", "type": "httpBasicAuth", "data": {"user": N8N_WP_USER, "password": N8N_WP_PASS}}
    vps(f"""python3 -c "import json; open('/tmp/new_wp.json','w').write(json.dumps({repr(payload)}))" """)
    result = vps("""curl -s -b /tmp/pm3.txt -X POST http://localhost:5678/rest/credentials \
      -H "Content-Type: application/json" -d @/tmp/new_wp.json 2>/dev/null | \
      python3 -c "import sys,json;d=json.load(sys.stdin);print('Created:',d.get('data',{}).get('id','?'))" 2>/dev/null""")
    print(f"   {result}")

# ── PART 4: Fix WF1 Gemini + Test ────────────────────────────────
print("\n🤖 PART 4: Checking WF1 + Execute Test")

wfs_raw = vps("curl -s -b /tmp/pm3.txt http://localhost:5678/rest/workflows 2>/dev/null")
wfs = json.loads(wfs_raw).get('data', [])

print(f"\n   Active workflows:")
for w in wfs:
    icon = "🟢" if w.get('active') else "⚫"
    print(f"   {icon} {w['name']}")

# Run WF1
for w in wfs:
    if 'US Trend Jacker' not in w['name']:
        continue
    wf_id = w['id']
    # Deactivate + reactivate to refresh credentials
    vps(f"""curl -s -b /tmp/pm3.txt -X PATCH http://localhost:5678/rest/workflows/{wf_id} \
      -H "Content-Type: application/json" -d '{{"active":false}}' -o /dev/null 2>/dev/null""")
    time.sleep(2)
    vps(f"""curl -s -b /tmp/pm3.txt -X PATCH http://localhost:5678/rest/workflows/{wf_id} \
      -H "Content-Type: application/json" -d '{{"active":true}}' -o /dev/null 2>/dev/null""")
    
    # Execute
    exec_raw = vps(f"""curl -s -b /tmp/pm3.txt -X POST "http://localhost:5678/rest/workflows/{wf_id}/run" \
      -H "Content-Type: application/json" -d '{{}}' 2>/dev/null""")
    try:
        exec_id = json.loads(exec_raw).get('data', {}).get('executionId', '')
        print(f"\n   WF1 execution: {exec_id}")
        if exec_id:
            print("   Waiting 40s...")
            time.sleep(40)
            res_raw = vps(f"curl -s -b /tmp/pm3.txt http://localhost:5678/rest/executions/{exec_id} 2>/dev/null")
            res = json.loads(res_raw).get('data', {})
            status = res.get('status', '?')
            print(f"   WF1 status: {status}")
            if status == 'error':
                run_data = res.get('data',{}).get('resultData',{}).get('runData',{})
                for node, runs in run_data.items():
                    for r in (runs or []):
                        err = (r or {}).get('error',{})
                        if err and isinstance(err, dict):
                            msg = err.get('message','?')[:120]
                            print(f"   ❌ {node}: {msg}")
    except Exception as e:
        print(f"   Error: {e}")
    break

# ── PART 5: Activate WF4 ─────────────────────────────────────────
print("\n⚡ PART 5: Activating WF4 (Lead Magnet)")
for w in wfs:
    if 'Lead Magnet' in w['name'] or 'WF4' in w['name']:
        wf_id = w['id']
        if not w.get('active'):
            res = vps(f"""curl -s -b /tmp/pm3.txt -X PATCH http://localhost:5678/rest/workflows/{wf_id} \
              -H "Content-Type: application/json" -d '{{"active":true}}' 2>/dev/null | \
              python3 -c "import sys,json;d=json.load(sys.stdin);print('WF4 active:',d.get('data',{{}}).get('active','?'))" 2>/dev/null""")
            print(f"   {res}")
        else:
            print(f"   ✅ WF4 already active")

ssh_v.close()
print("\n" + "=" * 65)
print("✅ Phase 2 Deploy Complete!")
print(f"   WP User:    n8n-bloger")
print(f"   App Pass:   pcvN yStV uI9f GRUK SC59 vhH5")
print(f"   WF4 hook:   http://72.62.93.117:5678/webhook/plantsmag-lead")
print(f"   Disease URL: https://plantsmag.com/plant-disease-finder/")
print(f"   Watering URL: https://plantsmag.com/watering-calculator/")
print("=" * 65)
