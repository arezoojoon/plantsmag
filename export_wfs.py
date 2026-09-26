import paramiko, json

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('72.62.93.117', port=22, username='root', password="5KT4'ub5B5oD8V9TB#/u", timeout=15)

def run(cmd):
    _, o, _ = ssh.exec_command(cmd)
    return o.read().decode('utf-8')

wfs_raw = run('curl -s -b /tmp/n8n_session.txt http://localhost:5678/rest/workflows')
wfs = json.loads(wfs_raw).get('data', [])

full_wfs = []
for w in wfs:
    if w.get('active'):
        wf_detail = run(f'curl -s -b /tmp/n8n_session.txt http://localhost:5678/rest/workflows/{w["id"]}')
        full_wfs.append(json.loads(wf_detail).get('data', {}))

with open('d:/project/plantsmag/full_wfs.json', 'w', encoding='utf-8') as f:
    json.dump(full_wfs, f, indent=2)

ssh.close()
