import paramiko, sys, json, time
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# ── Credentials ─────────────────────────────────────────────────
HOSTINGER_HOST = 'srv1156.hstgr.io'
HOSTINGER_PORT = 65002
HOSTINGER_USER = 'artinwebs2025'
HOSTINGER_PASS = r'Nh*RA%i0)EHY#mrqQ$1Mo@ER'

VPS_HOST = '72.62.93.117'
VPS_USER = 'root'
VPS_PASS = "5KT4'ub5B5oD8V9TB#/u"

N8N_WP_USER  = 'n8n-bloger'
N8N_WP_PASS  = 'pcvN yStV uI9f GRUK SC59 vhH5'  # new app password
N8N_LOGIN_EMAIL = 'plantsmag@gmail.com'
N8N_LOGIN_PASS  = 'PlantsMag2026!'

LOCAL_THEME  = r'd:\project\plantsmag\plantsmag-premium'
LOCAL_BASE   = r'd:\project\plantsmag'

REMOTE_BASE  = '/home/artinwebs2025/domains/plantsmag.com/public_html'
THEME_REMOTE = f'{REMOTE_BASE}/wp-content/themes/plantsmag-premium'

# ────────────────────────────────────────────────────────────────
print("=" * 65)
print("PlantsMag Phase 2 — Full Deploy + Fix")
print("=" * 65)

# ── PART 1: Deploy files to Hostinger ───────────────────────────
print("\n📦 PART 1: Deploying files to Hostinger via SFTP...")

FILES = [
    (rf'{LOCAL_THEME}\assets\css\lead-magnet.css',         f'{THEME_REMOTE}/assets/css/lead-magnet.css'),
    (rf'{LOCAL_THEME}\assets\js\disease-finder.js',        f'{THEME_REMOTE}/assets/js/disease-finder.js'),
    (rf'{LOCAL_THEME}\assets\js\watering-calculator.js',   f'{THEME_REMOTE}/assets/js/watering-calculator.js'),
    (rf'{LOCAL_THEME}\inc\class-disease-finder.php',       f'{THEME_REMOTE}/inc/class-disease-finder.php'),
    (rf'{LOCAL_THEME}\inc\class-watering-calculator.php',  f'{THEME_REMOTE}/inc/class-watering-calculator.php'),
    (rf'{LOCAL_THEME}\inc\lead-capture.php',               f'{THEME_REMOTE}/inc/lead-capture.php'),
    (rf'{LOCAL_THEME}\functions.php',                      f'{THEME_REMOTE}/functions.php'),
]

try:
    ssh_h = paramiko.SSHClient()
    ssh_h.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_h.connect(HOSTINGER_HOST, port=HOSTINGER_PORT,
                  username=HOSTINGER_USER, password=HOSTINGER_PASS, timeout=20)
    sftp = ssh_h.open_sftp()
    
    ok = 0
    for local, remote in FILES:
        try:
            sftp.put(local, remote)
            import os
            size = os.path.getsize(local)
            print(f"  ✅ {os.path.basename(local)} ({size:,} bytes)")
            ok += 1
        except Exception as e:
            print(f"  ❌ {local.split(chr(92))[-1]}: {e}")
    
    # Flush OPcache via wp-cli
    _, out, _ = ssh_h.exec_command('find /home/artinwebs2025 -name wp -type f 2>/dev/null | head -1', timeout=10)
    wp_cli = out.read().decode().strip()
    if wp_cli:
        _, out2, _ = ssh_h.exec_command(f'{wp_cli} cache flush --path={REMOTE_BASE} 2>/dev/null', timeout=15)
        print(f"  Cache flush: {out2.read().decode().strip()[:60] or 'done'}")
    
    sftp.close()
    ssh_h.close()
    print(f"\n  → Uploaded {ok}/{len(FILES)} files ✅")

except Exception as e:
    print(f"  ❌ SFTP Error: {e}")

# ── PART 2: Fix n8n via VPS ─────────────────────────────────────
print("\n🔧 PART 2: Fixing n8n credentials + workflows...")

ssh_v = paramiko.SSHClient()
ssh_v.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_v.connect(VPS_HOST, port=22, username=VPS_USER, password=VPS_PASS, timeout=15)

def vps(cmd, timeout=30):
    _, o, _ = ssh_v.exec_command(cmd, timeout=timeout)
    return o.read().decode('utf-8', errors='replace').strip()

# Verify WP credentials first
print("\n  Testing new WP credentials...")
test = vps(f'''curl -s -o /dev/null -w "%{{http_code}}" \
  -u "{N8N_WP_USER}:{N8N_WP_PASS}" \
  "https://plantsmag.com/wp-json/wp/v2/users/me" 2>/dev/null''')
print(f"  WP /users/me → HTTP {test}")

test_post = vps(f'''curl -s -o /dev/null -w "%{{http_code}}" \
  -X POST \
  -u "{N8N_WP_USER}:{N8N_WP_PASS}" \
  -H "Content-Type: application/json" \
  -d '{{"title":"n8n-test","content":"test","status":"draft"}}' \
  "https://plantsmag.com/wp-json/wp/v2/posts" 2>/dev/null''')
print(f"  WP POST /posts → HTTP {test_post}")

# Login to n8n
vps(f'''curl -s -c /tmp/pm_deploy.txt -X POST http://localhost:5678/rest/login \
  -H "Content-Type: application/json" \
  -d '{{"emailOrLdapLoginId":"{N8N_LOGIN_EMAIL}","password":"{N8N_LOGIN_PASS}"}}' \
  -o /dev/null 2>/dev/null''')

# Get all credentials
creds_raw = vps("curl -s -b /tmp/pm_deploy.txt http://localhost:5678/rest/credentials 2>/dev/null")
try:
    creds = json.loads(creds_raw).get('data', [])
except:
    # Try project-based
    proj_raw = vps("curl -s -b /tmp/pm_deploy.txt 'http://localhost:5678/rest/credentials?includeData=false' 2>/dev/null")
    creds = json.loads(proj_raw).get('data', [])

print(f"\n  n8n credentials found: {len(creds)}")
wp_creds_fixed = 0

for c in creds:
    cname = c.get('name', '')
    ctype = c.get('type', '')
    cid   = c.get('id', '')
    
    # Fix all HTTP Basic Auth credentials used for WordPress
    if 'httpBasicAuth' in ctype or ('PlantsMag' in cname and 'WP' in cname) or 'WP Auth' in cname:
        print(f"  Updating: [{ctype}] {cname} (ID: {cid})")
        update = {
            "name": cname,
            "type": ctype,
            "data": {
                "user": N8N_WP_USER,
                "password": N8N_WP_PASS
            }
        }
        vps(f"""python3 -c "import json; open('/tmp/cred_{cid}.json','w').write(json.dumps({repr(update)}))" """)
        result = vps(f"""curl -s -b /tmp/pm_deploy.txt \
          -X PATCH http://localhost:5678/rest/credentials/{cid} \
          -H "Content-Type: application/json" \
          -d @/tmp/cred_{cid}.json 2>/dev/null | python3 -c "import sys,json;d=json.load(sys.stdin);n=d.get('data',{{}}).get('name','?');print('→',n)" 2>/dev/null""")
        print(f"    {result}")
        wp_creds_fixed += 1

if wp_creds_fixed == 0:
    print("  No WP creds found to update — creating new one...")
    new_cred = {
        "name": "PlantsMag WP Auth",
        "type": "httpBasicAuth",
        "data": {"user": N8N_WP_USER, "password": N8N_WP_PASS}
    }
    vps(f"""python3 -c "import json; open('/tmp/new_cred.json','w').write(json.dumps({repr(new_cred)}))" """)
    result = vps("""curl -s -b /tmp/pm_deploy.txt \
      -X POST http://localhost:5678/rest/credentials \
      -H "Content-Type: application/json" \
      -d @/tmp/new_cred.json 2>/dev/null | python3 -c "import sys,json;d=json.load(sys.stdin);print('Created ID:',d.get('data',{}).get('id','?'))" 2>/dev/null""")
    print(f"  {result}")

# ── PART 3: Fix WF1 Gemini model ────────────────────────────────
print("\n🤖 PART 3: Fixing WF1 Gemini model...")
wfs_raw = vps("curl -s -b /tmp/pm_deploy.txt http://localhost:5678/rest/workflows 2>/dev/null")
wfs = json.loads(wfs_raw).get('data', [])

for w in wfs:
    if 'US Trend Jacker' not in w['name']:
        continue
    wf_id = w['id']
    wf_raw = vps(f"curl -s -b /tmp/pm_deploy.txt http://localhost:5678/rest/workflows/{wf_id} 2>/dev/null")
    wf = json.loads(wf_raw).get('data', {})
    
    nodes = wf.get('nodes', [])
    changed = False
    for node in nodes:
        p = node.get('parameters', {})
        url = p.get('url', '')
        # Fix old gemini model
        if 'gemini' in url and ('2.5-flash-preview' in url or 'gemini-2.5' in url):
            p['url'] = url.replace('gemini-2.5-flash-preview-04-17', 'gemini-2.0-flash').replace('gemini-2.5-flash', 'gemini-2.0-flash')
            node['parameters'] = p
            changed = True
            print(f"  Fixed Gemini URL: {p['url'][:80]}")
        # Also fix body if it references wrong model
        body = p.get('body', '')
        if isinstance(body, str) and 'gemini-2.5' in body:
            p['body'] = body.replace('gemini-2.5-flash-preview-04-17', 'gemini-2.0-flash')
            node['parameters'] = p
            changed = True
    
    if changed:
        upd = {"name": wf['name'], "nodes": nodes, "connections": wf.get('connections', {}), "settings": wf.get('settings', {}), "active": True}
        vps(f"""python3 -c "import json; open('/tmp/wf1_upd.json','w').write(json.dumps({repr(upd)}))" """)
        res = vps(f"""curl -s -b /tmp/pm_deploy.txt \
          -X PUT http://localhost:5678/rest/workflows/{wf_id} \
          -H "Content-Type: application/json" \
          -d @/tmp/wf1_upd.json 2>/dev/null | python3 -c "import sys,json;d=json.load(sys.stdin);print('Updated:',d.get('data',{{}}).get('name','?'))" """)
        print(f"  {res}")
    else:
        print(f"  WF1 Gemini URL already correct")

# ── PART 4: Activate WF4 ─────────────────────────────────────────
print("\n⚡ PART 4: Activating WF4...")
for w in wfs:
    if 'Lead Magnet' in w['name'] or 'WF4' in w['name']:
        wf_id = w['id']
        active = w.get('active', False)
        print(f"  WF4: {w['name']} — active={active}")
        if not active:
            res = vps(f"""curl -s -b /tmp/pm_deploy.txt \
              -X PATCH http://localhost:5678/rest/workflows/{wf_id} \
              -H "Content-Type: application/json" \
              -d '{{"active":true}}' 2>/dev/null | python3 -c "import sys,json;d=json.load(sys.stdin);print('→ active:',d.get('data',{{}}).get('active','?'))" """)
            print(f"  {res}")

# ── PART 5: Test WF1 ─────────────────────────────────────────────
print("\n🚀 PART 5: Testing WF1 execution...")
for w in wfs:
    if 'US Trend Jacker' not in w['name']:
        continue
    wf_id = w['id']
    exec_res = vps(f"""curl -s -b /tmp/pm_deploy.txt \
      -X POST "http://localhost:5678/rest/workflows/{wf_id}/run" \
      -H "Content-Type: application/json" \
      -d '{{}}' 2>/dev/null""")
    try:
        exec_data = json.loads(exec_res)
        exec_id = exec_data.get('data', {}).get('executionId', '')
        print(f"  WF1 execution started: {exec_id}")
        if exec_id:
            print("  Waiting 35s for result...")
            time.sleep(35)
            result = vps(f"curl -s -b /tmp/pm_deploy.txt http://localhost:5678/rest/executions/{exec_id} 2>/dev/null")
            rdata = json.loads(result).get('data', {})
            status = rdata.get('status', '?')
            print(f"  → Status: {status}")
            if status == 'error':
                run_data = rdata.get('data', {}).get('resultData', {}).get('runData', {})
                for nname, nruns in run_data.items():
                    for nr in (nruns or []):
                        err = (nr or {}).get('error', {})
                        if err and isinstance(err, dict):
                            print(f"  ❌ {nname}: {err.get('message','?')[:120]}")
    except Exception as e:
        print(f"  Parse error: {e} | {exec_res[:100]}")
    break

# ── Final summary ─────────────────────────────────────────────────
print("\n" + "=" * 65)
print("✅ All done! Summary:")
print(f"  WordPress: user='{N8N_WP_USER}' | app_pass='pcvN yStV uI9f GRUK SC59 vhH5'")
print(f"  n8n WP credentials: updated {wp_creds_fixed}")
print(f"  WF4 webhook: http://72.62.93.117:5678/webhook/plantsmag-lead")
print("=" * 65)

ssh_v.close()
