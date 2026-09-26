import paramiko, sys, json, time
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('72.62.93.117', port=22, username='root', password="5KT4'ub5B5oD8V9TB#/u", timeout=15)

def run(cmd, timeout=45):
    _, stdout, stderr = ssh.exec_command(cmd, timeout=timeout)
    return stdout.read().decode('utf-8', errors='replace').strip()

print("=" * 65)
print("FULL DIAGNOSIS: PlantsMag n8n Workflows")
print("=" * 65)

# Login
run("""curl -s -c /tmp/diag.txt -X POST http://localhost:5678/rest/login \
  -H 'Content-Type: application/json' \
  -d '{"emailOrLdapLoginId":"plantsmag@gmail.com","password":"PlantsMag2026!"}' -o /dev/null 2>/dev/null""")

# Get all workflows
out = run("curl -s -b /tmp/diag.txt http://localhost:5678/rest/workflows 2>/dev/null")
wfs = json.loads(out).get('data', [])
print(f"\nTotal workflows: {len(wfs)}")

# Check executions of each
for w in wfs:
    wf_id = w['id']
    wf_name = w['name']
    active = w.get('active', False)
    print(f"\n{'='*55}")
    print(f"  {wf_name} — active={active}")
    
    # Get last 3 executions
    exec_out = run(f"curl -s -b /tmp/diag.txt 'http://localhost:5678/rest/executions?workflowId={wf_id}&limit=3' 2>/dev/null")
    try:
        execs = json.loads(exec_out).get('data', {}).get('results', [])
        if not execs:
            print("  No executions yet")
        for ex in execs[:2]:
            status = ex.get('status', '?')
            started = ex.get('startedAt', '?')[:19]
            print(f"  [{status}] {started}")
            if status in ('error', 'crashed'):
                # Get details
                exec_id = ex.get('id', '')
                det = run(f"curl -s -b /tmp/diag.txt http://localhost:5678/rest/executions/{exec_id} 2>/dev/null")
                det_data = json.loads(det).get('data', {})
                run_data = det_data.get('data', {}).get('resultData', {}).get('runData', {})
                for node_name, node_runs in run_data.items():
                    for nr in (node_runs or []):
                        err = nr.get('error', {})
                        if err:
                            print(f"    ❌ {node_name}: {err.get('message','?')[:100]}")
    except Exception as e:
        print(f"  Parse error: {e}")

# Test WP credentials directly
print("\n" + "="*65)
print("Testing WordPress REST API credentials...")
wp_url = "https://plantsmag.com"

# Test with artinmag user + app password
cred_test = run(f"""curl -s -o /dev/null -w "%{{http_code}}" \
  -u "artinmag:XH18 J5Wq 52Ow oM2M gukl hNcH" \
  "{wp_url}/wp-json/wp/v2/posts?per_page=1" 2>/dev/null""")
print(f"  artinmag + app password: HTTP {cred_test}")

# Check what username WP has
user_check = run(f"""curl -s \
  -u "artinmag:XH18 J5Wq 52Ow oM2M gukl hNcH" \
  "{wp_url}/wp-json/wp/v2/users/me" 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print('User:', d.get('name','?'), '| slug:', d.get('slug','?'), '| roles:', d.get('roles','?'))" 2>/dev/null""")
print(f"  User check: {user_check}")

# Try posting
post_test = run(f"""curl -s -o /dev/null -w "%{{http_code}}" \
  -X POST \
  -u "artinmag:XH18 J5Wq 52Ow oM2M gukl hNcH" \
  -H "Content-Type: application/json" \
  -d '{{"title":"Test","content":"Test","status":"draft"}}' \
  "{wp_url}/wp-json/wp/v2/posts" 2>/dev/null""")
print(f"  POST new post test: HTTP {post_test}")

print("\n" + "="*65)
print("Testing Hostinger SSH credentials...")
for host in ['srv1156.hstgr.io']:
    result = run(f"""timeout 8 ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 \
      -p 65002 artinwebs2025@{host} 'echo SSH_OK && whoami' 2>&1 || echo FAILED""")
    print(f"  {host}:65002 -> {result[:80]}")

ssh.close()
