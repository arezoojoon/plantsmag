import paramiko, json

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('72.62.93.117', port=22, username='root', password="5KT4'ub5B5oD8V9TB#/u", timeout=15)

def run(cmd):
    _, o, _ = ssh.exec_command(cmd)
    return o.read().decode('utf-8')

run('''curl -s -c /tmp/n8n_session.txt -X POST http://localhost:5678/rest/login -H "Content-Type: application/json" -d '{"emailOrLdapLoginId":"plantsmag@gmail.com","password":"PlantsMag2026!"}' ''')
execs_raw = run('curl -s -b /tmp/n8n_session.txt http://localhost:5678/rest/executions?limit=5')
execs = json.loads(execs_raw).get('data', [])

for e in execs:
    print(f"ID: {e['id']} | WF: {e['workflowId']} | Status: {e['status']} | Node: {e.get('data', {}).get('resultData', {}).get('error', {}).get('node', '?')} | Error: {e.get('data', {}).get('resultData', {}).get('error', {}).get('message', '?')[:150]}")

ssh.close()
