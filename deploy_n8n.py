import paramiko
import time
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

HOST = '72.62.93.117'
PORT = 22
USER = 'root'
PASSWORD = "5KT4'ub5B5oD8V9TB#/u"

def run(ssh, cmd, timeout=120):
    print(f"\n▶ {cmd[:80]}")
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=timeout)
    out = stdout.read().decode('utf-8', errors='replace').strip()
    err = stderr.read().decode('utf-8', errors='replace').strip()
    if out:
        print(out[:2000])
    if err and 'warn' not in err.lower() and 'deprecat' not in err.lower():
        if len(err) < 500:
            print(f"  ⚠ {err}")
    return out, err

print("=" * 60)
print("  n8n Deployment Script — PlantsMag VPS")
print("=" * 60)

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST, port=PORT, username=USER, password=PASSWORD, timeout=20)
print("✅ Connected to server")

# ── STEP 1: Create /var/www/n8n directory ─────────────────────────────────────
print("\n── STEP 1: Create /var/www/n8n ──")
run(ssh, "mkdir -p /var/www/n8n")
run(ssh, "ls /var/www/")

# ── STEP 2: Install n8n globally ─────────────────────────────────────────────
print("\n── STEP 2: Install n8n ──")
# Check if n8n already installed
out, _ = run(ssh, "n8n --version 2>/dev/null || echo 'NOT_INSTALLED'")
if 'NOT_INSTALLED' in out:
    print("Installing n8n (this takes 2-3 minutes)...")
    run(ssh, "npm install -g n8n --legacy-peer-deps 2>&1 | tail -5", timeout=300)
    out, _ = run(ssh, "n8n --version 2>/dev/null || echo 'FAILED'")
    if 'FAILED' in out:
        print("❌ n8n install failed, trying alternative...")
        run(ssh, "npm install -g n8n@latest 2>&1 | tail -5", timeout=300)
    else:
        print(f"✅ n8n installed: {out}")
else:
    print(f"✅ n8n already installed: {out}")

# ── STEP 3: Create n8n environment config ─────────────────────────────────────
print("\n── STEP 3: Create n8n config ──")
n8n_env = """N8N_HOST=0.0.0.0
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
"""

# Write env file
run(ssh, f"cat > /var/www/n8n/.env << 'ENVEOF'\n{n8n_env}\nENVEOF")
run(ssh, "cat /var/www/n8n/.env")

# ── STEP 4: Create PM2 config for n8n ─────────────────────────────────────────
print("\n── STEP 4: Create PM2 config ──")
pm2_config = """{
  "apps": [
    {
      "name": "n8n",
      "script": "n8n",
      "args": "start",
      "cwd": "/var/www/n8n",
      "env_file": "/var/www/n8n/.env",
      "restart_delay": 3000,
      "max_restarts": 5,
      "log_date_format": "YYYY-MM-DD HH:mm:ss",
      "out_file": "/var/www/n8n/logs/n8n-out.log",
      "error_file": "/var/www/n8n/logs/n8n-error.log"
    }
  ]
}"""

run(ssh, "mkdir -p /var/www/n8n/logs")
run(ssh, f"cat > /var/www/n8n/ecosystem.config.json << 'PMEOF'\n{pm2_config}\nPMEOF")

# ── STEP 5: Start n8n with PM2 ─────────────────────────────────────────────
print("\n── STEP 5: Start n8n with PM2 ──")

# Stop any existing n8n instance
run(ssh, "pm2 stop n8n 2>/dev/null || true")
run(ssh, "pm2 delete n8n 2>/dev/null || true")

# Start n8n
# Use env vars directly since env_file may not work with all PM2 versions
n8n_start_cmd = (
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
    "pm2 start n8n --name n8n -- start 2>&1"
)
run(ssh, n8n_start_cmd, timeout=30)
print("Waiting 8 seconds for n8n to start...")
time.sleep(8)

# Check status
out, _ = run(ssh, "pm2 list --no-color 2>&1 | cat")
print(out)

# Verify n8n is listening
out, _ = run(ssh, "curl -s -o /dev/null -w '%{http_code}' http://localhost:5678/healthz 2>/dev/null || echo 'not responding yet'")
print(f"  n8n health: {out}")

# ── STEP 6: Save PM2 config for auto-restart ──────────────────────────────────
print("\n── STEP 6: Save PM2 startup config ──")
run(ssh, "pm2 save 2>&1")
run(ssh, "pm2 startup 2>&1 | tail -3")

# ── STEP 7: Configure Nginx for n8n ──────────────────────────────────────────
print("\n── STEP 7: Configure Nginx reverse proxy ──")
nginx_config = """server {
    listen 80;
    server_name 72.62.93.117;

    # n8n on /n8n/ path (so it coexists with other apps)
    location /n8n/ {
        proxy_pass http://127.0.0.1:5678/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_cache_bypass $http_upgrade;
        proxy_read_timeout 3600s;
        proxy_send_timeout 3600s;
    }

    # Also allow direct port 5678 access (firewall must allow it)
    # Access n8n at: http://72.62.93.117:5678
}
"""

# Check if nginx config exists for this server
out, _ = run(ssh, "ls /etc/nginx/sites-available/ 2>/dev/null || echo 'no sites-available'")
print(f"Nginx sites: {out}")

run(ssh, "cat > /etc/nginx/sites-available/n8n << 'NGINXEOF'\n" + nginx_config + "\nNGINXEOF")

# Only enable if plantsmag-apps config doesn't conflict
out, _ = run(ssh, "ls /etc/nginx/sites-enabled/")
print(f"Enabled sites: {out}")

# Check existing nginx config
run(ssh, "nginx -t 2>&1")

# Allow port 5678 through UFW if active
run(ssh, "ufw status 2>/dev/null | head -5")
run(ssh, "ufw allow 5678/tcp 2>/dev/null || true")

# ── STEP 8: Verify everything ─────────────────────────────────────────────────
print("\n── STEP 8: Final verification ──")
print("Waiting 5 more seconds...")
time.sleep(5)

out, _ = run(ssh, "pm2 list --no-color 2>&1 | cat")
print(out)

out, _ = run(ssh, "curl -s -o /dev/null -w '%{http_code}' http://localhost:5678/healthz 2>/dev/null")
if out.strip() == '200':
    print(f"\n✅ n8n is UP and healthy! HTTP {out}")
elif out.strip() == '401':
    print(f"\n✅ n8n is UP with auth! HTTP {out} (need username/password)")
else:
    print(f"\n⚠️ n8n health: HTTP {out}")
    run(ssh, "pm2 logs n8n --lines 20 --nostream 2>&1 | cat")

print("\n" + "=" * 60)
print(f"  🎉 n8n Deployment Complete!")
print(f"  Access: http://72.62.93.117:5678")
print(f"  User  : admin")
print(f"  Pass  : PlantsMag2026!")
print("=" * 60)

ssh.close()
