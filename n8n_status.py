import paramiko, json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('72.62.93.117', port=22, username='root', password="5KT4'ub5B5oD8V9TB#/u", timeout=15)

def run(cmd):
    _, o, _ = ssh.exec_command(cmd)
    return o.read().decode('utf-8', errors='replace')

run('''curl -s -c /tmp/n8n_session.txt -X POST http://localhost:5678/rest/login -H "Content-Type: application/json" -d '{"emailOrLdapLoginId":"plantsmag@gmail.com","password":"PlantsMag2026!"}\' ''')

# Get all workflows
wfs_out = run('curl -s -b /tmp/n8n_session.txt http://localhost:5678/rest/workflows')
wfs = json.loads(wfs_out).get('data', [])

print("=" * 70)
print("N8N WORKFLOW STATUS & SCHEDULE REPORT")
print("=" * 70)

for w in wfs:
    wf_id = w['id']
    name = w['name']
    active = w.get('active', False)
    
    # Get full details
    detail = run(f'curl -s -b /tmp/n8n_session.txt http://localhost:5678/rest/workflows/{wf_id}')
    wf_data = json.loads(detail).get('data', {})
    
    print(f"\n{'='*50}")
    print(f"  Name: {name}")
    print(f"  ID: {wf_id}")
    print(f"  Active: {'YES' if active else 'NO'}")
    
    # Find schedule trigger
    for node in wf_data.get('nodes', []):
        if 'trigger' in node['type'].lower() or 'schedule' in node['type'].lower():
            params = node.get('parameters', {})
            rule = params.get('rule', {})
            intervals = rule.get('interval', [])
            for interval in intervals:
                field = interval.get('field', '')
                if field == 'cronExpression':
                    cron = interval.get('expression', '')
                    print(f"  Schedule: cron({cron})")
                    # Decode cron
                    parts = cron.split()
                    if len(parts) == 5:
                        minute, hour = parts[0], parts[1]
                        if hour != '*':
                            print(f"  Runs at: {hour}:{minute} UTC daily")
                elif field == 'hours':
                    hours = interval.get('hoursInterval', '')
                    print(f"  Schedule: Every {hours} hours")
                else:
                    print(f"  Schedule: {json.dumps(interval)}")
        
        # Check if it has Gemini node
        if node['type'] == 'n8n-nodes-base.httpRequest' and 'generativelanguage' in node['parameters'].get('url', ''):
            body = node['parameters'].get('body', '')
            has_table = '<table' in body
            has_details = '<details' in body
            print(f"  GEO prompt: table={'YES' if has_table else 'NO'}, details/summary={'YES' if has_details else 'NO'}")
        
        # Check publish node
        if node['type'] == 'n8n-nodes-base.httpRequest' and 'wp-json' in node['parameters'].get('url', ''):
            json_body = node['parameters'].get('jsonBody', '')
            uses_stringify = 'JSON.stringify' in json_body
            print(f"  Publish method: {'JSON.stringify (FIXED)' if uses_stringify else 'OTHER: ' + json_body[:80]}")
            cred = node.get('credentials', {})
            print(f"  WP Credential: {json.dumps(cred)}")

# Check recent executions
print(f"\n{'='*70}")
print("RECENT EXECUTIONS (last 10)")
print("=" * 70)
execs_out = run('curl -s -b /tmp/n8n_session.txt "http://localhost:5678/rest/executions?limit=10"')
execs = json.loads(execs_out).get('data', {}).get('results', [])
for e in execs:
    status = 'OK' if e.get('status') == 'success' else 'FAIL'
    print(f"  [{status}] {e.get('workflowName', 'unknown')[:40]:40s} | {e.get('startedAt', '')[:19]} | {e.get('status')}")

ssh.close()
print(f"\n{'='*70}")
print("SUMMARY")
print("=" * 70)
