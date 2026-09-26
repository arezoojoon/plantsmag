import paramiko, sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

print("=" * 60)
print("DEPLOY: Automated Images and Monday-only Drafts")
print("=" * 60)

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('72.62.93.117', port=22, username='root', password=r"5KT4'ub5B5oD8V9TB#/u", timeout=20)

sftp = ssh.open_sftp()
engine_files = [
    'lib/pexels.js',
    'lib/wordpress.js',
    'seo-automation-cron.js'
]

for f in engine_files:
    local_path = os.path.join(r'd:\project\plantsmag\engine', f.replace('/', os.sep))
    remote_path = f'/root/plantsmag-engine/{f}'
    with open(local_path, 'r', encoding='utf-8') as fh:
        content = fh.read()
    with sftp.open(remote_path, 'w') as fh:
        fh.write(content)
    print(f"  VPS: Uploaded {f}")

sftp.close()

_, o, _ = ssh.exec_command('pm2 restart plantsmag-seo 2>&1')
print(f"  PM2: Restarted Engine")

import time; time.sleep(3)
_, o, _ = ssh.exec_command('pm2 logs plantsmag-seo --nostream --lines 5 2>&1')
print("\nRecent Logs:\n" + o.read().decode('utf-8', errors='replace').strip()[-500:])

ssh.close()
print("\nDone!")
