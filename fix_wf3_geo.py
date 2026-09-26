import paramiko, json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('72.62.93.117', port=22, username='root', password="5KT4'ub5B5oD8V9TB#/u", timeout=15)

def run(cmd):
    _, o, _ = ssh.exec_command(cmd)
    return o.read().decode('utf-8', errors='replace')

run('''curl -s -c /tmp/n8n_session.txt -X POST http://localhost:5678/rest/login -H "Content-Type: application/json" -d '{"emailOrLdapLoginId":"plantsmag@gmail.com","password":"PlantsMag2026!"}\' ''')

# Get WF3 nodes
wf3_out = run('curl -s -b /tmp/n8n_session.txt http://localhost:5678/rest/workflows/SLgAkWAL2NBVzZ7U')
wf3 = json.loads(wf3_out).get('data', {})
for n in wf3.get('nodes', []):
    print(f"Node: {n['name']} | Type: {n['type']}")
    if n['type'] == 'n8n-nodes-base.httpRequest':
        print(f"  URL: {n['parameters'].get('url', 'N/A')}")

# Update WF3 Gemini node (whatever its name is)
GEO_PROMPT_FUNNEL = """Write a comprehensive 2500+ word high-value SEO article about: {{ $json.selectedTopic }}.

Target audience: Serious US plant collectors willing to invest in premium equipment and rare plants.

CRITICAL STRUCTURE REQUIREMENTS:

1. Premium, authoritative tone - position as expert consultation
2. Include HTML <table> comparing premium products with pricing tiers
3. Include FAQ section with <details><summary> HTML tags
4. Reference high-ticket items: professional grow light systems ($200+), premium soil mixes, rare plant varieties
5. Include ROI calculations or cost-benefit analysis where relevant
6. Use data-driven arguments with specific numbers
7. Include <ol> step-by-step guides for complex procedures

Return JSON: {"title": "...", "slug": "...", "meta_description": "...", "content": "..."}
Return ONLY JSON. No markdown fences."""

modified = False
for node in wf3.get('nodes', []):
    if node['type'] == 'n8n-nodes-base.httpRequest' and 'generativelanguage' in node['parameters'].get('url', ''):
        new_body = '={"contents":[{"parts":[{"text":"' + GEO_PROMPT_FUNNEL.replace('"', '\\"').replace('\n', '\\n') + '"}]}],"generationConfig":{"temperature":0.7,"maxOutputTokens":8192}}'
        node['parameters']['body'] = new_body
        modified = True
        print(f"\nUpdated Gemini prompt for node: {node['name']}")

if modified:
    update_payload = json.dumps({"nodes": wf3['nodes']})
    sftp = ssh.open_sftp()
    with sftp.open('/tmp/wf3_update.json', 'w') as f:
        f.write(update_payload)
    sftp.close()
    result = run('curl -s -b /tmp/n8n_session.txt -X PATCH http://localhost:5678/rest/workflows/SLgAkWAL2NBVzZ7U -H "Content-Type: application/json" -d @/tmp/wf3_update.json')
    if '"updatedAt"' in result:
        print("SUCCESS: WF3 updated with GEO prompt!")
    else:
        print(f"Result: {result[:200]}")

ssh.close()
