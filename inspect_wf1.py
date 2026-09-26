import paramiko, json, time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('72.62.93.117', port=22, username='root', password="5KT4'ub5B5oD8V9TB#/u", timeout=15)

def run(cmd):
    _, o, e = ssh.exec_command(cmd)
    return o.read().decode('utf-8'), e.read().decode('utf-8')

# Login
run('''curl -s -c /tmp/n8n_session.txt -X POST http://localhost:5678/rest/login -H "Content-Type: application/json" -d '{"emailOrLdapLoginId":"plantsmag@gmail.com","password":"PlantsMag2026!"}\' ''')

# Get WF1 full detail with all node parameters
print("=== Getting WF1 full config ===")
wf1_out, _ = run('curl -s -b /tmp/n8n_session.txt http://localhost:5678/rest/workflows/CpyU2cf01DdtpfWo')
wf1 = json.loads(wf1_out).get('data', {})

# Print each node's full parameters
for n in wf1.get('nodes', []):
    print(f"\n--- Node: {n['name']} ({n['type']}) ---")
    print(json.dumps(n.get('parameters', {}), indent=2)[:800])
    if 'credentials' in n:
        print(f"  Credentials: {json.dumps(n['credentials'])}")

# Also check what credential IDs exist
print("\n=== Credential Details ===")
for cred_id in ['gB8bPmc1dpPDMqKb', '2Mi5Z0ayPeyLt7Uz']:
    cred_out, _ = run(f'curl -s -b /tmp/n8n_session.txt http://localhost:5678/rest/credentials/{cred_id}')
    cred = json.loads(cred_out).get('data', {})
    print(f"\nCred {cred_id}: {cred.get('name')} | Type: {cred.get('type')}")
    # Print the decrypted data if available
    if 'data' in cred:
        print(f"  Data: {json.dumps(cred['data'])[:200]}")

# Check Gemini credential
print("\n=== Gemini Credential ===")
gemini_out, _ = run('curl -s -b /tmp/n8n_session.txt http://localhost:5678/rest/credentials/snhmLm7CcjRQvFJn')
gemini = json.loads(gemini_out).get('data', {})
print(f"Name: {gemini.get('name')} | Type: {gemini.get('type')}")
if 'data' in gemini:
    print(f"Data keys: {list(gemini['data'].keys()) if isinstance(gemini['data'], dict) else 'raw'}")

ssh.close()
print("\nDone!")
