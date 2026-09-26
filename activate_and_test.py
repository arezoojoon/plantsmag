import paramiko, sys, json
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('72.62.93.117', port=22, username='root', password="5KT4'ub5B5oD8V9TB#/u", timeout=15)

def run(cmd, timeout=30):
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=timeout)
    return stdout.read().decode('utf-8', errors='replace').strip()

# Get all workflows
wf_json = run("curl -s -b /tmp/n8n_session.txt http://localhost:5678/rest/workflows 2>/dev/null")
wfs = json.loads(wf_json).get('data', [])

print(f"Found {len(wfs)} workflows:")
for w in wfs:
    icon = "🟢" if w.get('active') else "⚫"
    print(f"  {icon} [{w['id']}] {w['name']}")

# Delete duplicate WF1 (the older one that's inactive)
# Keep active ones, activate inactive new ones
for w in wfs:
    wf_id = w['id']
    wf_name = w['name']
    
    if not w.get('active'):
        # Delete old duplicate if name is duplicate
        dup_names = [x['name'] for x in wfs if x['id'] != wf_id]
        if wf_name in dup_names:
            # This is a duplicate, delete it
            del_resp = run(f"curl -s -b /tmp/n8n_session.txt -X DELETE http://localhost:5678/rest/workflows/{wf_id} -o /dev/null -w '%{{http_code}}' 2>/dev/null")
            print(f"  🗑️  Deleted duplicate: {wf_name} (HTTP {del_resp})")
        else:
            # Not a duplicate, activate it
            act_resp = run(f"curl -s -b /tmp/n8n_session.txt -X PATCH http://localhost:5678/rest/workflows/{wf_id} -H 'Content-Type: application/json' -d '{{\"active\":true}}' -o /dev/null -w '%{{http_code}}' 2>/dev/null")
            print(f"  ✅ Activated: {wf_name} (HTTP {act_resp})")

# Test execute WF1
print("\nTesting WF1 execution (this will take ~30 seconds)...")
wf_json2 = run("curl -s -b /tmp/n8n_session.txt http://localhost:5678/rest/workflows 2>/dev/null")
wfs2 = json.loads(wf_json2).get('data', [])
wf1 = next((w for w in wfs2 if 'Trend Jacker' in w.get('name','') or ('WF1' in w.get('name','') and w.get('active'))), None)

if wf1:
    exec_payload = '{"startNodes":[],"destinationNode":null,"runData":null,"pinData":{}}'
    exec_resp = run(f"curl -s -b /tmp/n8n_session.txt -X POST http://localhost:5678/rest/workflows/{wf1['id']}/run -H 'Content-Type: application/json' -d '{exec_payload}' 2>/dev/null")
    try:
        exec_data = json.loads(exec_resp)
        exec_id = exec_data.get('data', {}).get('executionId', '?')
        print(f"  Execution started: ID={exec_id}")
        
        # Wait and check result
        import time
        time.sleep(25)
        exec_check = run(f"curl -s -b /tmp/n8n_session.txt http://localhost:5678/rest/executions/{exec_id} 2>/dev/null")
        exec_result = json.loads(exec_check)
        status = exec_result.get('data', {}).get('status', '?')
        finished = exec_result.get('data', {}).get('finished', False)
        print(f"  Execution status: {status} | Finished: {finished}")
        
        if status == 'error' or not finished:
            # Get error details
            run_data = exec_result.get('data', {}).get('data', {}).get('resultData', {}).get('runData', {})
            for node_name, node_runs in run_data.items():
                for run in node_runs:
                    if run.get('error'):
                        print(f"  Error in {node_name}: {json.dumps(run['error'])[:200]}")
    except Exception as e:
        print(f"  Exec error: {e} | Response: {exec_resp[:200]}")

# Final status
print("\n" + "="*55)
print("FINAL STATE:")
wf_json3 = run("curl -s -b /tmp/n8n_session.txt http://localhost:5678/rest/workflows 2>/dev/null")
wfs3 = json.loads(wf_json3).get('data', [])
for w in wfs3:
    icon = "🟢" if w.get('active') else "⚫"
    print(f"  {icon} {w['name']}")
print("="*55)

ssh.close()
