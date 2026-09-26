import paramiko, sys, json
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('72.62.93.117', port=22, username='root', password="5KT4'ub5B5oD8V9TB#/u", timeout=15)

def run(cmd, timeout=30):
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=timeout)
    return stdout.read().decode('utf-8', errors='replace').strip()

# Fresh login
run("""curl -s -c /tmp/n8n_cookie.txt -X POST http://localhost:5678/rest/login \
  -H 'Content-Type: application/json' \
  -d '{"emailOrLdapLoginId":"plantsmag@gmail.com","password":"PlantsMag2026!"}' -o /dev/null 2>/dev/null""")

for wf_id in ['CpyU2cf01DdtpfWo', 'UKegbNpPIBkkNUrd', 'SLgAkWAL2NBVzZ7U']:
    # Get versionId
    wf_data_str = run(f"curl -s -b /tmp/n8n_cookie.txt http://localhost:5678/rest/workflows/{wf_id} 2>/dev/null")
    try:
        wf_data = json.loads(wf_data_str)
        versionId = wf_data['data']['versionId']
        print(f"Found versionId for {wf_id}: {versionId}")
        
        # POST activate
        payload = json.dumps({"versionId": versionId})
        resp = run(f"curl -s -b /tmp/n8n_cookie.txt -X POST http://localhost:5678/rest/workflows/{wf_id}/activate -H 'Content-Type: application/json' -d '{payload}' 2>/dev/null")
        if 'active":true' in resp or 'active": true' in resp or '"id"' in resp or 'active":true' in resp.replace(" ", ""):
            print(f"Workflow {wf_id} activated successfully!")
        else:
            print(f"Workflow {wf_id} response: {resp[:100]}")
    except Exception as e:
        print(f"Error for {wf_id}: {e}\nResponse was: {wf_data_str[:100]}")

# Show final state
wf_json = run("curl -s -b /tmp/n8n_cookie.txt http://localhost:5678/rest/workflows 2>/dev/null")
try:
    wfs = json.loads(wf_json).get('data', [])
    print(f"\nFinal: {len(wfs)} workflows")
    for w in wfs:
        icon = "🟢 ACTIVE" if w.get('active') else "🔴 OFF"
        print(f"  [{icon}] {w['name']} (ID: {w['id']})")
except Exception as e:
    print("Could not parse JSON:", e)

ssh.close()
