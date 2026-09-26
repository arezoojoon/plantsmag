import paramiko, sys, json
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('72.62.93.117', port=22, username='root', password="5KT4'ub5B5oD8V9TB#/u", timeout=15)

def run(cmd):
    stdin, stdout, stderr = ssh.exec_command(cmd)
    return stdout.read().decode('utf-8', errors='replace').strip()

print("Authenticating...")
run("""curl -s -c /tmp/n8n_session.txt -X POST http://localhost:5678/rest/login \
  -H 'Content-Type: application/json' \
  -d '{"emailOrLdapLoginId":"plantsmag@gmail.com","password":"PlantsMag2026!"}' -o /dev/null 2>/dev/null""")

wf_json = run("curl -s -b /tmp/n8n_session.txt http://localhost:5678/rest/workflows 2>/dev/null")
wfs = json.loads(wf_json).get('data', [])

# List of the new IDs we just created: B00SZRef3O89gmlZ, n6THe5kGGOcPflGH, 3u9OYGvhgO5CWQAW
target_ids = ["B00SZRef3O89gmlZ", "n6THe5kGGOcPflGH", "3u9OYGvhgO5CWQAW"]

for w in wfs:
    if w.get('id') in target_ids:
        print(f"Activating {w['name']} ({w['id']})...")
        res = run(f"curl -s -b /tmp/n8n_session.txt -X PATCH http://localhost:5678/rest/workflows/{w['id']} -H 'Content-Type: application/json' -d '{{\"active\":true}}'")
        print(f"Result: {res}")
        
ssh.close()
print("Done.")
