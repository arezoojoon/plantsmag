import paramiko, sys, json, time
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# VPS SSH (this still works)
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('72.62.93.117', port=22, username='root', password="5KT4'ub5B5oD8V9TB#/u", timeout=15)

def run(cmd, timeout=45):
    _, stdout, stderr = ssh.exec_command(cmd, timeout=timeout)
    out = stdout.read().decode('utf-8', errors='replace').strip()
    err = stderr.read().decode('utf-8', errors='replace').strip()
    return out, err

print("=" * 60)
print("Fixing WF1 Gemini Model via n8n API")
print("=" * 60)

# Login to n8n
run("""curl -s -c /tmp/n8n_fix.txt -X POST http://localhost:5678/rest/login \
  -H 'Content-Type: application/json' \
  -d '{"emailOrLdapLoginId":"plantsmag@gmail.com","password":"PlantsMag2026!"}' -o /dev/null 2>/dev/null""")

# Get WF1 full data
print("\nFetching WF1...")
out, _ = run("curl -s -b /tmp/n8n_fix.txt http://localhost:5678/rest/workflows 2>/dev/null")
wfs = json.loads(out).get('data', [])

wf1 = None
for w in wfs:
    if 'US Trend Jacker' in w.get('name', '') and w.get('active'):
        wf1 = w
        break

if not wf1:
    for w in wfs:
        if 'US Trend Jacker' in w.get('name', ''):
            wf1 = w
            break

if not wf1:
    print("WF1 not found!")
    ssh.close()
    sys.exit(1)

wf1_id = wf1['id']
print(f"Found WF1: {wf1['name']} (ID: {wf1_id})")

# Get full workflow JSON
out, _ = run(f"curl -s -b /tmp/n8n_fix.txt http://localhost:5678/rest/workflows/{wf1_id} 2>/dev/null")
wf_data = json.loads(out).get('data', {})

# Fix Gemini node URL
nodes = wf_data.get('nodes', [])
fixed = 0
for node in nodes:
    params = node.get('parameters', {})
    url = params.get('url', '')
    if 'gemini-2.5-flash' in url or 'gemini-2.5' in url:
        old_url = url
        new_url = url.replace('gemini-2.5-flash-preview-04-17', 'gemini-2.0-flash')
        new_url = new_url.replace('gemini-2.5-flash', 'gemini-2.0-flash')
        new_url = new_url.replace('gemini-2.5', 'gemini-2.0-flash')
        params['url'] = new_url
        node['parameters'] = params
        print(f"\nFixed Gemini URL in node '{node['name']}':")
        print(f"  OLD: {old_url}")
        print(f"  NEW: {new_url}")
        fixed += 1

if fixed == 0:
    # Search in all string fields
    print("Searching all node fields for gemini URL...")
    for node in nodes:
        name = node.get('name', '')
        params = node.get('parameters', {})
        
        def fix_dict(d):
            count = 0
            if isinstance(d, dict):
                for k, v in d.items():
                    if isinstance(v, str) and 'gemini' in v.lower():
                        print(f"  Found in {name}.{k}: {v[:80]}")
                    elif isinstance(v, (dict, list)):
                        count += fix_dict(v)
            elif isinstance(d, list):
                for item in d:
                    fix_dict(item)
            return count
        fix_dict(params)

# Also check for v1beta vs v1
print(f"\nFixed {fixed} node(s)")

# Save fixed workflow
wf_update = {
    'name': wf_data.get('name'),
    'nodes': nodes,
    'connections': wf_data.get('connections', {}),
    'settings': wf_data.get('settings', {}),
    'staticData': wf_data.get('staticData'),
    'active': True
}

# Write to temp file on server
run(f"echo '{json.dumps(wf_update)}' > /tmp/wf1_fixed.json 2>/dev/null")
# Better: use python to write
import tempfile, json as js
fix_json = js.dumps(wf_update)
# Write via SSH heredoc
cmd = f"""python3 -c "import json; data={repr(wf_update)}; open('/tmp/wf1_fixed.json','w').write(json.dumps(data))" 2>/dev/null"""
run(cmd)

# Verify file written
out, _ = run("wc -c /tmp/wf1_fixed.json")
print(f"Fix file size: {out}")

# Update workflow
out, err = run(f"""curl -s -b /tmp/n8n_fix.txt \
  -X PUT http://localhost:5678/rest/workflows/{wf1_id} \
  -H 'Content-Type: application/json' \
  -d @/tmp/wf1_fixed.json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print('Updated:', d.get('data',{{}}).get('name','?'))" """)
print(f"\nAPI Update result: {out}")

# Test execute WF1
print("\nExecuting WF1 test run...")
out, _ = run(f"""curl -s -b /tmp/n8n_fix.txt \
  -X POST http://localhost:5678/rest/workflows/{wf1_id}/run \
  -H 'Content-Type: application/json' \
  -d '{{}}' 2>/dev/null""")
try:
    exec_data = json.loads(out)
    exec_id = exec_data.get('data', {}).get('executionId', '')
    print(f"Execution started: {exec_id}")
    
    # Wait and check result
    time.sleep(30)
    out2, _ = run(f"curl -s -b /tmp/n8n_fix.txt http://localhost:5678/rest/executions/{exec_id} 2>/dev/null")
    exec_result = json.loads(out2).get('data', {})
    status = exec_result.get('status', '?')
    print(f"Execution status: {status}")
    if status == 'error':
        # Find error node
        run_data = exec_result.get('data', {}).get('resultData', {}).get('runData', {})
        for node_name, node_runs in run_data.items():
            for run in node_runs:
                if run.get('error'):
                    print(f"Error in node '{node_name}': {run['error'].get('message', '?')[:150]}")
except Exception as e:
    print(f"Parse error: {e} | {out[:200]}")

ssh.close()
print("\nDone!")
