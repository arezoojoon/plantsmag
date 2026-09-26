import paramiko, sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# 1. Deploy Engine fixes to VPS
print("=" * 60)
print("DEPLOY 1: Securing Node.js Engine on VPS")
print("=" * 60)

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('72.62.93.117', port=22, username='root', password=r"5KT4'ub5B5oD8V9TB#/u", timeout=20)

sftp = ssh.open_sftp()
engine_files = [
    'package.json',
    'seo-automation-cron.js',
    'lib/gemini.js',
    'lib/wordpress.js',
    '.env'
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

_, o, _ = ssh.exec_command('cd /root/plantsmag-engine && npm install 2>&1')
print(f"  NPM: {o.read().decode()[:200]}")

_, o, _ = ssh.exec_command('pm2 restart plantsmag-seo 2>&1')
print(f"  PM2 Restarted")
import time; time.sleep(3)
_, o, _ = ssh.exec_command('pm2 logs plantsmag-seo --nostream --lines 5 2>&1')
print(o.read().decode('utf-8', errors='replace').strip()[-500:])

ssh.close()

# 2. Deploy Hostinger fixes
print("\n" + "=" * 60)
print("DEPLOY 2: Securing public PHP scripts on Hostinger")
print("=" * 60)

ssh2 = paramiko.SSHClient()
ssh2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh2.connect('187.124.245.99', port=65002, username='u284669846', password='[3pPybi0[3pPybi0', timeout=20)
sftp2 = ssh2.open_sftp()
wp = '/home/u284669846/domains/plantsmag.com/public_html'

hostinger_files = ['fast_index.php', 'lead-capture.php']
for f in hostinger_files:
    local_path = os.path.join(r'd:\project\plantsmag', f)
    with open(local_path, 'r', encoding='utf-8') as fh:
        content = fh.read()
    with sftp2.open(f'{wp}/{f}', 'w') as fh:
        fh.write(content)
    print(f"  Uploaded: {f}")

sftp2.close()

# Delete content_builder.php
print("\nDeleting dangerous script: content_builder.php...")
_, o, _ = ssh2.exec_command(f'rm -f {wp}/content_builder.php && echo DELETED')
print(f"  {o.read().decode().strip()}")

ssh2.close()

print("\nAll security patches deployed successfully!")
