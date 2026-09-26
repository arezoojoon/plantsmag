"""Quick redeploy of updated engine files to VPS"""
import paramiko, sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('72.62.93.117', port=22, username='root', password=r"5KT4'ub5B5oD8V9TB#/u", timeout=20)

def run(cmd, timeout=60):
    _, o, _ = ssh.exec_command(cmd, timeout=timeout)
    return o.read().decode('utf-8', errors='replace')

remote = '/root/plantsmag-engine'
local = r'd:\project\plantsmag\engine'

# Upload changed files
sftp = ssh.open_sftp()
files = [
    'lib/linker.js',
    'strategies/plant-care.js',
    'strategies/comparison.js',
    'strategies/trending-rss.js',
    'seo-automation-cron.js',
]

for f in files:
    local_path = os.path.join(local, f.replace('/', os.sep))
    remote_path = f'{remote}/{f}'
    with open(local_path, 'r', encoding='utf-8') as fh:
        content = fh.read()
    with sftp.open(remote_path, 'w') as fh:
        fh.write(content)
    print(f"  Uploaded: {f}")

sftp.close()

# Restart PM2
print("\nRestarting PM2...")
out = run('pm2 restart plantsmag-seo 2>&1')
print(out.strip())

# Wait and check logs
import time; time.sleep(3)
out = run('pm2 logs plantsmag-seo --nostream --lines 10 2>&1')
print("\nRecent logs:")
print(out.strip())

ssh.close()
print("\nDone!")
