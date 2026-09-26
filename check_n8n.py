import paramiko, sys, time
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('72.62.93.117', port=22, username='root', password="5KT4'ub5B5oD8V9TB#/u", timeout=15)

def run(cmd):
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=20)
    return stdout.read().decode('utf-8', errors='replace').strip()

print("Waiting 10s for n8n to fully start...")
time.sleep(10)

# Health check
code = run("curl -s -o /dev/null -w '%{http_code}' http://localhost:5678/healthz 2>/dev/null")
print(f"Health: HTTP {code}")

# Try signin page
code2 = run("curl -s -o /dev/null -w '%{http_code}' http://localhost:5678/signin 2>/dev/null")
print(f"Signin: HTTP {code2}")

# Check env var is set correctly
env_check = run("pm2 env 2 2>/dev/null | grep SECURE || echo 'env var not in pm2 env'")
print(f"Env check: {env_check}")

# Check n8n logs for cookie message
logs = run("pm2 logs n8n --lines 15 --nostream 2>&1 | cat | grep -i 'cookie\\|error\\|started\\|listen\\|ready' | head -10")
print(f"Logs:\n{logs}")

ssh.close()
