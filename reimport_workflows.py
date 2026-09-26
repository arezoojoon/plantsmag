import paramiko, sys, json, time
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('72.62.93.117', port=22, username='root', password="5KT4'ub5B5oD8V9TB#/u", timeout=15)

def run(cmd, timeout=30):
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=timeout)
    out = stdout.read().decode('utf-8', errors='replace').strip()
    err = stderr.read().decode('utf-8', errors='replace').strip()
    return out, err

# First get auth cookie by logging in
print("1. Getting auth token from n8n...")
login_cmd = """curl -s -c /tmp/n8n_cookies.txt -X POST http://localhost:5678/rest/login \
  -H 'Content-Type: application/json' \
  -d '{"email":"plantsmag@gmail.com","password":"PlantsMag2026!"}' 2>/dev/null"""
out, _ = run(login_cmd)
print(f"Login response: {out[:200]}")

# Get workflows list to confirm auth works
out, _ = run("curl -s -b /tmp/n8n_cookies.txt http://localhost:5678/rest/workflows 2>/dev/null | python3 -c \"import sys,json; d=json.load(sys.stdin); print('Auth OK, workflows:', len(d.get('data',[])))\" 2>&1")
print(f"Auth check: {out}")

# Import workflows via REST API (POST /rest/workflows)
print("\n2. Importing workflows via REST API...")

workflows = [
    '/var/www/n8n/workflow_1_us_trendjacker.json',
    '/var/www/n8n/workflow_2_uae_amazon.json', 
    '/var/www/n8n/workflow_3_highticket_funnel.json',
]

for wf_path in workflows:
    wf_name = wf_path.split('/')[-1].replace('.json', '')
    
    # Read the workflow JSON
    out, _ = run(f"cat {wf_path}")
    try:
        wf_data = json.loads(out)
    except:
        print(f"  ⚠️ Could not parse {wf_name}")
        continue
    
    # Remove fields that conflict with new instance
    for field in ['id', 'versionId', 'createdAt', 'updatedAt', 'triggerCount']:
        wf_data.pop(field, None)
    
    # Remove credential references that don't exist in new instance
    for node in wf_data.get('nodes', []):
        node.pop('credentials', None)
    
    # POST to n8n REST API
    wf_json = json.dumps(wf_data).replace("'", "'\\''")
    
    import_cmd = f"""curl -s -b /tmp/n8n_cookies.txt -X POST http://localhost:5678/rest/workflows \
  -H 'Content-Type: application/json' \
  -d '{wf_json}' 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print('Created:', d.get('data',{{}}).get('name','?'), '| ID:', d.get('data',{{}}).get('id','?'))" 2>&1"""
    
    out, _ = run(import_cmd, timeout=30)
    print(f"  {wf_name}: {out[:100]}")

# Final count
print("\n3. Final workflow count...")
out, _ = run("curl -s -b /tmp/n8n_cookies.txt http://localhost:5678/rest/workflows 2>/dev/null | python3 -c \"import sys,json; d=json.load(sys.stdin); wfs=d.get('data',[]); print(f'Total: {len(wfs)} workflows'); [print(f'  [{i+1}] {w[chr(34)+chr(110)+chr(97)+chr(109)+chr(101)+chr(34)]}') for i,w in enumerate(wfs)]\" 2>&1")
print(out)

ssh.close()
