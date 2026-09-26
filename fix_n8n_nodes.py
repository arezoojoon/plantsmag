import json, paramiko, tempfile, os

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('72.62.93.117', port=22, username='root', password="5KT4'ub5B5oD8V9TB#/u", timeout=15)

def run(cmd):
    _, o, _ = ssh.exec_command(cmd)
    return o.read().decode('utf-8')

run('curl -s -c /tmp/n8n_session.txt -X POST http://localhost:5678/rest/login -H "Content-Type: application/json" -d \'{"emailOrLdapLoginId":"plantsmag@gmail.com","password":"PlantsMag2026!"}\'')

wfs_raw = run('curl -s -b /tmp/n8n_session.txt http://localhost:5678/rest/workflows')
wfs = json.loads(wfs_raw).get('data', [])

for w in wfs:
    if any(name in w['name'] for name in ['US Trend Jacker', 'UAE Amazon Market', 'High-Ticket Funnel', 'Content Factory']):
        wf_id = w['id']
        wf_detail = run(f'curl -s -b /tmp/n8n_session.txt http://localhost:5678/rest/workflows/{wf_id}')
        wf_data = json.loads(wf_detail).get('data', {})
        
        modified = False
        for node in wf_data.get('nodes', []):
            if node['type'] == 'n8n-nodes-base.httpRequest' and 'Publish' in node['name']:
                # Update node to use specifyBody: json
                node['parameters']['specifyBody'] = 'json'
                node['parameters']['contentType'] = 'json'
                
                # Create a json body depending on what's available
                jsonBody = '{\n  "title": "={{ $json.title }}",\n  "content": "={{ $json.content }}",\n  "status": "publish"'
                if 'meta_description' in str(wf_data) or 'excerpt' in str(node):
                     jsonBody += ',\n  "excerpt": "={{ $json.meta_description }}"'
                if 'slug' in str(node):
                     jsonBody += ',\n  "slug": "={{ $json.slug }}"'
                jsonBody += '\n}'
                
                node['parameters']['jsonBody'] = jsonBody
                if 'bodyParameters' in node['parameters']:
                    del node['parameters']['bodyParameters']
                modified = True
                
        if modified:
            print(f"Updating {w['name']}...")
            payload = {"nodes": wf_data['nodes']}
            
            local_path = os.path.join(tempfile.gettempdir(), f"{wf_id}.json")
            with open(local_path, 'w') as f:
                json.dump(payload, f)
                
            sftp = ssh.open_sftp()
            sftp.put(local_path, f'/tmp/{wf_id}.json')
            sftp.close()
            
            res = run(f'curl -s -b /tmp/n8n_session.txt -X PATCH http://localhost:5678/rest/workflows/{wf_id} -H "Content-Type: application/json" -d @/tmp/{wf_id}.json')
            print(f"Result for {w['name']}: {res[:100]}")

ssh.close()
