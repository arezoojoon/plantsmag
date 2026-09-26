import paramiko, sys, json
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('72.62.93.117', port=22, username='root', password="5KT4'ub5B5oD8V9TB#/u", timeout=15)

def run(cmd, timeout=30):
    _, stdout, _ = ssh.exec_command(cmd, timeout=timeout)
    return stdout.read().decode('utf-8', errors='replace').strip()

print("=" * 60)
print("Importing WF4 — Lead Magnet Email Engine to n8n")
print("=" * 60)

# Fresh login
run("""curl -s -c /tmp/fresh4.txt -X POST http://localhost:5678/rest/login \
  -H 'Content-Type: application/json' \
  -d '{"emailOrLdapLoginId":"plantsmag@gmail.com","password":"PlantsMag2026!"}' -o /dev/null 2>/dev/null""")

chk = run("curl -s -b /tmp/fresh4.txt http://localhost:5678/rest/workflows 2>/dev/null | python3 -c \"import sys,json;d=json.load(sys.stdin);print('Auth OK, workflows:',len(d.get('data',[])))\"")
print(f"  {chk}")

# Read WF4 JSON from local and upload via SFTP
print("\nUploading WF4 JSON...")
sftp = ssh.open_sftp()
sftp.put('workflow_4_lead_magnet.json', '/tmp/wf4.json')
sftp.close()

# Create WF4 via REST API
resp = run("curl -s -b /tmp/fresh4.txt -X POST http://localhost:5678/rest/workflows -H 'Content-Type: application/json' -d @/tmp/wf4.json 2>/dev/null")
try:
    data = json.loads(resp)
    wf = data.get('data', {})
    wf_id = wf.get('id', '')
    wf_name = wf.get('name', '?')
    if wf_id:
        print(f"  Created: {wf_name} (ID: {wf_id})")
        
        # Activate WF4
        act = run(f"curl -s -b /tmp/fresh4.txt -X PATCH http://localhost:5678/rest/workflows/{wf_id} -H 'Content-Type: application/json' -d '{{\"active\":true}}' 2>/dev/null | python3 -c \"import sys,json;d=json.load(sys.stdin);print('Active:',d.get('data',{{}}).get('active','?'))\"")
        print(f"  {act}")
    else:
        print(f"  Error: {resp[:200]}")
except Exception as e:
    print(f"  Error: {e} | {resp[:150]}")

# Final status
print("\n" + "="*55)
print("ALL WORKFLOWS:")
all_wf = run("curl -s -b /tmp/fresh4.txt http://localhost:5678/rest/workflows 2>/dev/null")
wfs = json.loads(all_wf).get('data', [])
for w in wfs:
    icon = "GREEN" if w.get('active') else "off"
    print(f"  [{icon}] {w['name']}")

# Webhook URL
print(f"\nWF4 Webhook URL: http://72.62.93.117:5678/webhook/plantsmag-lead")
print(f"(Production: https://72.62.93.117:5678/webhook/plantsmag-lead)")
print("="*55)

ssh.close()
