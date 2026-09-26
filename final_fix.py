import paramiko, sys, json, time
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

VPS_HOST = '72.62.93.117'
VPS_PASS = "5KT4'ub5B5oD8V9TB#/u"
N8N_EMAIL = 'plantsmag@gmail.com'
N8N_PASS  = 'PlantsMag2026!'

# CONFIRMED WORKING credentials (HTTP 201 tested)
WP_USER = 'n8n-bloger'
WP_PASS = 'XzLM9TAsLMmFeldUawUSkLCu'
WP_URL  = 'https://plantsmag.com'

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(VPS_HOST, port=22, username='root', password=VPS_PASS, timeout=15)

def vps(cmd, t=30):
    _, o, _ = ssh.exec_command(cmd, timeout=t)
    return o.read().decode('utf-8', errors='replace').strip()

print("=" * 65)
print("Final Fix: Update n8n credentials + Rebuild Publish nodes")
print("=" * 65)

# Verify password first from VPS
print("\n0. Verifying WP credentials from VPS...")
test = vps(f'''curl -s -o /dev/null -w "%{{http_code}}" \
  -u "{WP_USER}:{WP_PASS}" \
  "{WP_URL}/wp-json/wp/v2/users/me" 2>/dev/null''')
print(f"   GET /users/me: HTTP {test}")

test2 = vps(f'''curl -s -o /dev/null -w "%{{http_code}}" \
  -X POST -u "{WP_USER}:{WP_PASS}" \
  -H "Content-Type: application/json" \
  -d '{{"title":"n8n-test","content":"test content","status":"draft"}}' \
  "{WP_URL}/wp-json/wp/v2/posts" 2>/dev/null''')
print(f"   POST /posts: HTTP {test2}")

# Login n8n
vps(f'''curl -s -c /tmp/final2.txt -X POST http://localhost:5678/rest/login \
  -H "Content-Type: application/json" \
  -d '{{"emailOrLdapLoginId":"{N8N_EMAIL}","password":"{N8N_PASS}"}}' \
  -o /dev/null 2>/dev/null''')

# Update ALL credentials
print("\n1. Updating all PlantsMag WP credentials...")
creds = json.loads(vps("curl -s -b /tmp/final2.txt http://localhost:5678/rest/credentials 2>/dev/null")).get('data', [])

for c in creds:
    if 'httpBasicAuth' in c.get('type','') or 'WP Auth' in c.get('name','') or 'PlantsMag' in c.get('name',''):
        cid = c['id']
        payload = {"name": c['name'], "type": c['type'], "data": {"user": WP_USER, "password": WP_PASS}}
        vps(f"""python3 -c "import json; open('/tmp/cf{cid}.json','w').write(json.dumps({repr(payload)}))" """)
        r = vps(f"""curl -s -b /tmp/final2.txt -X PATCH http://localhost:5678/rest/credentials/{cid} \
          -H "Content-Type: application/json" -d @/tmp/cf{cid}.json 2>/dev/null | \
          python3 -c "import sys,json;d=json.load(sys.stdin);print('  ✅',d.get('data',{{}}).get('name','err'))" """)
        print(f"   {r}")

# Get WF1 and check publish node
print("\n2. Rebuilding WF1 Publish node with correct JSON body...")
wfs = json.loads(vps("curl -s -b /tmp/final2.txt http://localhost:5678/rest/workflows 2>/dev/null")).get('data', [])

for w in wfs:
    if 'US Trend Jacker' not in w['name']:
        continue
    wf_id = w['id']
    wf_raw = vps(f"curl -s -b /tmp/final2.txt http://localhost:5678/rest/workflows/{wf_id} 2>/dev/null")
    wf = json.loads(wf_raw).get('data', {})
    
    nodes = wf.get('nodes', [])
    changed = False
    
    for node in nodes:
        name = node.get('name', '')
        ptype = node.get('type', '')
        
        # Fix Gemini model if needed
        if 'gemini' in name.lower() or 'write' in name.lower():
            params = node.get('parameters', {})
            url = params.get('url', '')
            if 'gemini-2.5' in url or 'preview' in url:
                params['url'] = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent'
                node['parameters'] = params
                changed = True
                print(f"   Fixed Gemini URL in: {name}")
        
        # Fix WordPress publish node
        if ('publish' in name.lower() or 'wordpress' in name.lower()) and 'httpRequest' in ptype:
            params = node.get('parameters', {})
            print(f"   Checking publish node: {name}")
            print(f"     URL: {params.get('url','?')[:80]}")
            print(f"     Method: {params.get('method','?')}")
            print(f"     Body mode: {params.get('specifyBody','?')}")
            
            # Rebuild with correct JSON body
            params['method'] = 'POST'
            params['url'] = f'{WP_URL}/wp-json/wp/v2/posts'
            params['authentication'] = 'predefinedCredentialType'
            params['nodeCredentialType'] = 'httpBasicAuth'
            params['specifyBody'] = 'json'
            
            # Set JSON body with expressions
            params['jsonBody'] = '={{ {"title": $json.title, "content": $json.content, "status": "publish", "slug": $json.slug || ""} }}'
            
            # Also set sendBody
            params['sendBody'] = True
            params['contentType'] = 'json'
            
            node['parameters'] = params
            changed = True
            print(f"   ✅ Rebuilt publish node: {name}")
    
    if changed:
        upd = {
            'name': wf['name'],
            'nodes': nodes,
            'connections': wf.get('connections', {}),
            'settings': wf.get('settings', {}),
            'active': True
        }
        vps(f"""python3 -c "import json; open('/tmp/wf1r.json','w').write(json.dumps({repr(upd)}))" """)
        res = vps(f"""curl -s -b /tmp/final2.txt -X PUT http://localhost:5678/rest/workflows/{wf_id} \
          -H "Content-Type: application/json" -d @/tmp/wf1r.json 2>/dev/null | \
          python3 -c "import sys,json;d=json.load(sys.stdin);print('Updated:',d.get('data',{{}}).get('name','?'))" """)
        print(f"   {res}")
    break

# Execute WF1 test
print("\n3. Executing WF1 test...")
for w in wfs:
    if 'US Trend Jacker' not in w['name']:
        continue
    wf_id = w['id']
    exec_r = vps(f"""curl -s -b /tmp/final2.txt -X POST "http://localhost:5678/rest/workflows/{wf_id}/run" \
      -H "Content-Type: application/json" -d '{{}}' 2>/dev/null""")
    try:
        exec_id = json.loads(exec_r).get('data', {}).get('executionId', '')
        print(f"   Execution ID: {exec_id}")
        if exec_id:
            print("   Waiting 45s for result...")
            time.sleep(45)
            res = json.loads(vps(f"curl -s -b /tmp/final2.txt http://localhost:5678/rest/executions/{exec_id} 2>/dev/null")).get('data', {})
            status = res.get('status', '?')
            print(f"   Status: {status}")
            if status == 'success':
                print("   🎉 SUCCESS! WF1 is publishing articles!")
            elif status == 'error':
                run_data = res.get('data', {}).get('resultData', {}).get('runData', {})
                for node, runs in run_data.items():
                    for r in (runs or []):
                        err = (r or {}).get('error', {})
                        if err and isinstance(err, dict):
                            print(f"   ❌ {node}: {err.get('message','?')[:150]}")
                        elif err:
                            print(f"   ❌ {node}: {str(err)[:150]}")
        else:
            print(f"   No exec ID. Response: {exec_r[:200]}")
    except Exception as e:
        print(f"   Error: {e}")
    break

print("\n" + "="*65)
print("Final WP Credentials:")
print(f"  User: {WP_USER}")
print(f"  Pass: {WP_PASS}")
print(f"  POST test: HTTP {test2}")
print("="*65)

ssh.close()
