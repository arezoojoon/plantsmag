import paramiko
import json
import time
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

HOST = '72.62.93.117'
PORT = 22
USER = 'root'
PASSWORD = "5KT4'ub5B5oD8V9TB#/u"

def run(ssh, cmd, timeout=60):
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=timeout)
    out = stdout.read().decode('utf-8', errors='replace').strip()
    err = stderr.read().decode('utf-8', errors='replace').strip()
    return out, err

def scp_upload(ssh, local_path, remote_path):
    sftp = ssh.open_sftp()
    sftp.put(local_path, remote_path)
    sftp.close()
    print(f"  Uploaded: {local_path.split(chr(92))[-1]}")

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST, port=PORT, username=USER, password=PASSWORD, timeout=20)
print("Connected to VPS 72.62.93.117")

# Upload workflow
print("\n1. Upload workflow JSON...")
scp_upload(ssh, r'D:\project\plantsmag\plantsmag_n8n_workflow.json', '/var/www/n8n/plantsmag_workflow.json')

# Import workflow via n8n CLI
print("\n2. Import workflow into n8n...")
env_prefix = "N8N_USER_FOLDER=/var/www/n8n N8N_BASIC_AUTH_ACTIVE=true N8N_BASIC_AUTH_USER=admin N8N_BASIC_AUTH_PASSWORD='PlantsMag2026!'"
out, err = run(ssh, f"{env_prefix} n8n import:workflow --input=/var/www/n8n/plantsmag_workflow.json 2>&1", timeout=30)
print(f"  Result: {out or err}")

# Verify n8n is running
print("\n3. Verify n8n status...")
out, _ = run(ssh, "curl -s -o /dev/null -w '%{http_code}' http://localhost:5678/healthz 2>/dev/null")
print(f"  n8n health: HTTP {out}")

out, _ = run(ssh, "curl -s -u admin:PlantsMag2026! http://localhost:5678/rest/workflows 2>/dev/null | python3 -c \"import sys,json; d=json.load(sys.stdin); print(f'Workflows count: {len(d.get(chr(34)+chr(100)+chr(97)+chr(116)+chr(97)+chr(34), d) if isinstance(d, dict) else d)}')\" 2>/dev/null || echo 'manual check needed'")
print(f"  {out}")

print("\n4. Final PM2 status...")
out, _ = run(ssh, "pm2 list --no-color 2>&1 | cat")
print(out)

print("\n" + "="*60)
print("DONE!")
print(f"n8n UI   : http://72.62.93.117:5678")
print(f"Username : admin")
print(f"Password : PlantsMag2026!")
print("Go to Workflows tab to see and activate the PlantsMag workflow")
print("="*60)
ssh.close()
