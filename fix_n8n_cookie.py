import paramiko
import sys
import time

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

HOST = '72.62.93.117'
USER = 'root'
PASS = "5KT4'ub5B5oD8V9TB#/u"

def run(ssh, cmd, timeout=30):
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=timeout)
    out = stdout.read().decode('utf-8', errors='replace').strip()
    err = stderr.read().decode('utf-8', errors='replace').strip()
    return out, err

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST, port=22, username=USER, password=PASS, timeout=15)
print("Connected to VPS")

# Stop current n8n instance
print("\n1. Stopping n8n...")
run(ssh, "pm2 stop n8n 2>&1")
run(ssh, "pm2 delete n8n 2>&1")
time.sleep(2)

# Write new .env with N8N_SECURE_COOKIE=false
env_content = """N8N_HOST=0.0.0.0
N8N_PORT=5678
N8N_PROTOCOL=http
WEBHOOK_URL=http://72.62.93.117:5678/
N8N_BASIC_AUTH_ACTIVE=true
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=PlantsMag2026!
N8N_USER_FOLDER=/var/www/n8n
EXECUTIONS_DATA_SAVE_ON_ERROR=all
EXECUTIONS_DATA_SAVE_ON_SUCCESS=none
EXECUTIONS_DATA_SAVE_MANUAL_EXECUTIONS=true
N8N_LOG_LEVEL=info
GENERIC_TIMEZONE=Asia/Tehran
N8N_SECURE_COOKIE=false
"""

print("2. Writing new .env with N8N_SECURE_COOKIE=false...")
# Write file line by line to avoid shell quoting issues
run(ssh, "cat > /var/www/n8n/.env << 'ENVEOF'\n" + env_content + "\nENVEOF")
out, _ = run(ssh, "cat /var/www/n8n/.env | grep SECURE")
print(f"   Verified: {out}")

# Restart n8n with env vars directly (most reliable method)
print("\n3. Restarting n8n with N8N_SECURE_COOKIE=false...")
start_cmd = (
    "cd /var/www/n8n && "
    "N8N_HOST=0.0.0.0 "
    "N8N_PORT=5678 "
    "N8N_PROTOCOL=http "
    "N8N_BASIC_AUTH_ACTIVE=true "
    "N8N_BASIC_AUTH_USER=admin "
    "N8N_BASIC_AUTH_PASSWORD='PlantsMag2026!' "
    "N8N_USER_FOLDER=/var/www/n8n "
    "GENERIC_TIMEZONE=Asia/Tehran "
    "WEBHOOK_URL=http://72.62.93.117:5678/ "
    "N8N_SECURE_COOKIE=false "
    "pm2 start n8n --name n8n -- start 2>&1"
)
out, err = run(ssh, start_cmd, timeout=20)
print(f"   {out[:200]}")

print("   Waiting 8s for n8n to start...")
time.sleep(8)

# Verify
out, _ = run(ssh, "curl -s -o /dev/null -w '%{http_code}' http://localhost:5678/healthz 2>/dev/null")
print(f"\n4. Health check: HTTP {out}")

out, _ = run(ssh, "pm2 list --no-color 2>&1 | cat")
print(f"\n5. PM2 status:\n{out}")

# Save PM2 config
run(ssh, "pm2 save 2>&1")
print("\n6. PM2 config saved.")

ssh.close()
print("\n✅ Done! n8n is now accessible without HTTPS requirement.")
print("   Open: http://72.62.93.117:5678")
print("   Login: admin / PlantsMag2026!")
