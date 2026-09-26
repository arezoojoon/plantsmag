import paramiko, sys, json
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

HOST = '187.124.245.99'
PORT = 65002
USER = 'u284669846'
PASS = '[3pPybi0[3pPybi0'

VPS_HOST = '72.62.93.117'
VPS_PASS = "5KT4'ub5B5oD8V9TB#/u"

REMOTE_BASE = '/home/u284669846/domains/plantsmag.com/public_html'
N8N_EMAIL   = 'plantsmag@gmail.com'
N8N_PASS    = 'PlantsMag2026!'

ssh_h = paramiko.SSHClient()
ssh_h.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_h.connect(HOST, port=PORT, username=USER, password=PASS, timeout=20)

def hrun(cmd, t=20):
    _, o, e = ssh_h.exec_command(cmd, timeout=t)
    out = o.read().decode('utf-8', errors='replace').strip()
    err = e.read().decode('utf-8', errors='replace').strip()
    return out, err

print("=" * 65)
print("Creating WP Application Password via WP-CLI")
print("=" * 65)

# Find WP-CLI
out, _ = hrun('which wp 2>/dev/null || find /usr/local/bin /usr/bin -name "wp" 2>/dev/null | head -1')
wp = out.strip() or 'wp'
print(f"WP-CLI: {wp}")

# List WordPress users
print("\n1. WordPress users:")
users_out, _ = hrun(f'{wp} user list --path={REMOTE_BASE} --format=json 2>/dev/null')
try:
    users = json.loads(users_out)
    for u in users:
        print(f"   ID:{u['ID']} | {u['user_login']} | {u['roles']}")
except Exception as e:
    print(f"   Error: {e} | {users_out[:200]}")
    # Try another way
    users_out2, _ = hrun(f'{wp} user list --path={REMOTE_BASE} 2>/dev/null')
    print(f"   {users_out2[:300]}")

# Create app password for admin user (ID 1 typically)
print("\n2. Creating Application Password for n8n...")

# Delete old app passwords for n8n-bloger first
del_out, _ = hrun(f'{wp} user application-password delete n8n-bloger --all --path={REMOTE_BASE} 2>/dev/null')
print(f"   Delete old passwords: {del_out[:80] or 'done'}")

# Create new app password
new_pass_out, _ = hrun(f'{wp} user application-password create n8n-bloger "n8n-auto-$(date +%s)" --porcelain --path={REMOTE_BASE} 2>/dev/null')
print(f"   New app password: '{new_pass_out}'")

if not new_pass_out or 'Error' in new_pass_out:
    # Try with admin user
    print("   Trying with admin user...")
    # Get admin username
    admin_out, _ = hrun(f'{wp} user list --role=administrator --field=user_login --path={REMOTE_BASE} 2>/dev/null')
    admin_user = admin_out.strip().split('\n')[0] if admin_out else 'admin'
    print(f"   Admin user: {admin_user}")
    
    new_pass_out, _ = hrun(f'{wp} user application-password create "{admin_user}" "n8n-auto" --porcelain --path={REMOTE_BASE} 2>/dev/null')
    print(f"   New app password (admin): '{new_pass_out}'")
    
    if new_pass_out and 'Error' not in new_pass_out:
        NEW_WP_USER = admin_user
        NEW_WP_PASS = new_pass_out.strip()
    else:
        NEW_WP_USER = None
        NEW_WP_PASS = None
else:
    NEW_WP_USER = 'n8n-bloger'
    NEW_WP_PASS = new_pass_out.strip()

if NEW_WP_PASS:
    print(f"\n✅ NEW WordPress Credentials:")
    print(f"   User: {NEW_WP_USER}")
    print(f"   Pass: {NEW_WP_PASS}")
    
    # Test immediately
    test_out, _ = hrun(f'''curl -s -o /dev/null -w "%{{http_code}}" \
      -u "{NEW_WP_USER}:{NEW_WP_PASS}" \
      "https://plantsmag.com/wp-json/wp/v2/users/me" 2>/dev/null''')
    print(f"   Auth test: HTTP {test_out}")
    
    post_test, _ = hrun(f'''curl -s -o /dev/null -w "%{{http_code}}" \
      -X POST \
      -u "{NEW_WP_USER}:{NEW_WP_PASS}" \
      -H "Content-Type: application/json" \
      -d '{{"title":"n8n-test","content":"test","status":"draft"}}' \
      "https://plantsmag.com/wp-json/wp/v2/posts" 2>/dev/null''')
    print(f"   POST test: HTTP {post_test}")
    
    ssh_h.close()
    
    # Update n8n credentials
    print("\n🔧 Updating n8n credentials...")
    ssh_v = paramiko.SSHClient()
    ssh_v.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_v.connect(VPS_HOST, port=22, username='root', password=VPS_PASS, timeout=15)
    
    def vps(cmd, t=20):
        _, o, _ = ssh_v.exec_command(cmd, timeout=t)
        return o.read().decode('utf-8', errors='replace').strip()
    
    vps(f'''curl -s -c /tmp/final.txt -X POST http://localhost:5678/rest/login \
      -H "Content-Type: application/json" \
      -d '{{"emailOrLdapLoginId":"{N8N_EMAIL}","password":"{N8N_PASS}"}}' \
      -o /dev/null 2>/dev/null''')
    
    creds_raw = vps("curl -s -b /tmp/final.txt http://localhost:5678/rest/credentials 2>/dev/null")
    creds = json.loads(creds_raw).get('data', [])
    
    for c in creds:
        if 'httpBasicAuth' in c.get('type','') or 'WP Auth' in c.get('name',''):
            cid = c['id']
            payload = {"name": c['name'], "type": c['type'], "data": {"user": NEW_WP_USER, "password": NEW_WP_PASS}}
            vps(f"""python3 -c "import json; open('/tmp/cfinal{cid}.json','w').write(json.dumps({repr(payload)}))" """)
            r = vps(f"""curl -s -b /tmp/final.txt -X PATCH http://localhost:5678/rest/credentials/{cid} \
              -H "Content-Type: application/json" -d @/tmp/cfinal{cid}.json 2>/dev/null | \
              python3 -c "import sys,json;d=json.load(sys.stdin);print('✅ Updated:',d.get('data',{{}}).get('name','?'))" """)
            print(f"   {r}")
    
    # Test WF1
    print("\n🚀 Testing WF1...")
    wfs = json.loads(vps("curl -s -b /tmp/final.txt http://localhost:5678/rest/workflows 2>/dev/null")).get('data',[])
    for w in wfs:
        if 'US Trend Jacker' in w['name']:
            exec_r = vps(f"""curl -s -b /tmp/final.txt -X POST "http://localhost:5678/rest/workflows/{w['id']}/run" \
              -H "Content-Type: application/json" -d '{{}}' 2>/dev/null""")
            exec_id = json.loads(exec_r).get('data',{}).get('executionId','')
            print(f"   Execution ID: {exec_id}")
            if exec_id:
                import time; time.sleep(35)
                res = json.loads(vps(f"curl -s -b /tmp/final.txt http://localhost:5678/rest/executions/{exec_id} 2>/dev/null")).get('data',{})
                status = res.get('status','?')
                print(f"   Status: {status}")
                if status == 'error':
                    run_data = res.get('data',{}).get('resultData',{}).get('runData',{})
                    for node, runs in run_data.items():
                        for r in (runs or []):
                            err = (r or {}).get('error',{})
                            if err and isinstance(err, dict):
                                print(f"   ❌ {node}: {err.get('message','?')[:120]}")
            break
    
    ssh_v.close()
    print(f"\n{'='*65}")
    print(f"✅ DONE! Final credentials:")
    print(f"   WP User: {NEW_WP_USER}")
    print(f"   WP Pass: {NEW_WP_PASS}")
    print(f"{'='*65}")

else:
    ssh_h.close()
    print("\n❌ Could not create app password via WP-CLI")
    print("   Please create manually in WP Admin → Users → n8n-bloger → Application Passwords")
