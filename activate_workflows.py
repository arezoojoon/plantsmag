import paramiko, sys, json
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('72.62.93.117', port=22, username='root', password="5KT4'ub5B5oD8V9TB#/u", timeout=15)

def run(cmd, timeout=30):
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=timeout)
    return stdout.read().decode('utf-8', errors='replace').strip()

# Fresh login
run("""curl -s -c /tmp/fresh.txt -X POST http://localhost:5678/rest/login \
  -H 'Content-Type: application/json' \
  -d '{"emailOrLdapLoginId":"plantsmag@gmail.com","password":"PlantsMag2026!"}' -o /dev/null 2>/dev/null""")

# Activate each workflow directly
for wf_id in ['4PHayTAXFhGLZjtP', 'UKegbNpPIBkkNUrd', 'SLgAkWAL2NBVzZ7U']:
    resp = run(f"curl -s -b /tmp/fresh.txt -X PATCH http://localhost:5678/rest/workflows/{wf_id} -H 'Content-Type: application/json' -d '{{\"active\":true}}' 2>/dev/null")
    try:
        data = json.loads(resp).get('data', {})
        print(f"ID {wf_id}: {data.get('name','?')} -> active={data.get('active','?')}")
    except:
        print(f"ID {wf_id}: {resp[:100]}")

# Show final state
wf_json = run("curl -s -b /tmp/fresh.txt http://localhost:5678/rest/workflows 2>/dev/null")
wfs = json.loads(wf_json).get('data', [])
print(f"\nFinal: {len(wfs)} workflows")
for w in wfs:
    icon = "GREEN" if w.get('active') else "off"
    print(f"  [{icon}] {w['name']}")

ssh.close()
