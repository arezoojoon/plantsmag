"""Deploy: wordpress.js (draft mode) + seo-automation-cron.js (log) + llms.txt"""
import paramiko, sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# ── Deploy engine files to VPS ────────────────────────────────────────────────
print("=" * 60)
print("DEPLOY 1: Engine files to VPS (draft mode + topic tracking)")
print("=" * 60)

ssh.connect('72.62.93.117', port=22, username='root', password=r"5KT4'ub5B5oD8V9TB#/u", timeout=20)
sftp = ssh.open_sftp()

engine_files = [
    'lib/wordpress.js',
    'seo-automation-cron.js',
]

for f in engine_files:
    local_path = os.path.join(r'd:\project\plantsmag\engine', f.replace('/', os.sep))
    remote_path = f'/root/plantsmag-engine/{f}'
    with open(local_path, 'r', encoding='utf-8') as fh:
        content = fh.read()
    with sftp.open(remote_path, 'w') as fh:
        fh.write(content)
    print(f"  VPS: {f}")

sftp.close()

# Restart PM2
_, o, _ = ssh.exec_command('pm2 restart plantsmag-seo 2>&1')
print(f"  PM2: {o.read().decode()[:200]}")

import time; time.sleep(3)
_, o, _ = ssh.exec_command('pm2 logs plantsmag-seo --nostream --lines 6 2>&1')
print(o.read().decode('utf-8', errors='replace').strip()[-500:])

ssh.close()

# ── Deploy llms.txt to Hostinger ──────────────────────────────────────────────
print("\n" + "=" * 60)
print("DEPLOY 2: llms.txt to Hostinger (honest version)")
print("=" * 60)

ssh2 = paramiko.SSHClient()
ssh2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh2.connect('187.124.245.99', port=65002, username='u284669846', password='[3pPybi0[3pPybi0', timeout=20)

sftp2 = ssh2.open_sftp()
wp = '/home/u284669846/domains/plantsmag.com/public_html'

with open(r'd:\project\plantsmag\llms.txt', 'r', encoding='utf-8') as f:
    content = f.read()
with sftp2.open(f'{wp}/llms.txt', 'w') as f:
    f.write(content)
sftp2.close()
print("  Uploaded llms.txt")

# Verify
import urllib.request, ssl
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

try:
    req = urllib.request.Request('https://plantsmag.com/llms.txt', headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=10, context=ctx) as r:
        body = r.read().decode('utf-8')
        has_false = 'experienced plant care specialists' in body
        has_honest = 'AI-assisted and editorially reviewed' in body
        print(f"  Status: {r.status}")
        print(f"  False claim removed: {'YES' if not has_false else 'NO ❌'}")
        print(f"  Honest description: {'YES' if has_honest else 'NO ❌'}")
except Exception as e:
    print(f"  Error: {e}")

# Check current draft count
_, o, _ = ssh2.exec_command(f'cd {wp} && wp post list --post_status=draft --format=count 2>&1')
drafts = o.read().decode().strip()
print(f"\n  Current drafts in WP: {drafts}")

ssh2.close()
print("\nDone!")
