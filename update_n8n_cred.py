import paramiko, json

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('72.62.93.117', port=22, username='root', password="5KT4'ub5B5oD8V9TB#/u", timeout=15)

def run(cmd):
    _, o, _ = ssh.exec_command(cmd)
    return o.read().decode('utf-8')

# Login
run('''curl -s -c /tmp/n8n_session.txt -X POST http://localhost:5678/rest/login -H "Content-Type: application/json" -d '{"emailOrLdapLoginId":"plantsmag@gmail.com","password":"PlantsMag2026!"}\' ''')
print("Logged in to N8N")

# Update credential with new password
new_cred = json.dumps({
    "name": "PlantsMag WP Auth",
    "type": "httpBasicAuth",
    "data": {
        "user": "n8n-bloger",
        "password": "VQ05 3amn qMzu aPkX VLsu 6XiA"
    }
})

sftp = ssh.open_sftp()
with sftp.open('/tmp/cred_update.json', 'w') as f:
    f.write(new_cred)
sftp.close()

# Update both credential IDs
for cred_id in ['gB8bPmc1dpPDMqKb', '2Mi5Z0ayPeyLt7Uz']:
    result = run(f'curl -s -b /tmp/n8n_session.txt -X PATCH http://localhost:5678/rest/credentials/{cred_id} -H "Content-Type: application/json" -d @/tmp/cred_update.json')
    print(f"Credential {cred_id}: {result[:100]}")

ssh.close()
print("\nN8N credentials updated with new WP password!")
