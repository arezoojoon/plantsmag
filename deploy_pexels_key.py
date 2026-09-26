import paramiko, sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

print("=" * 60)
print("DEPLOY: Adding Pexels API Key to VPS")
print("=" * 60)

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('72.62.93.117', port=22, username='root', password=r"5KT4'ub5B5oD8V9TB#/u", timeout=20)

sftp = ssh.open_sftp()
local_env = r'd:\project\plantsmag\engine\.env'
remote_env = '/root/plantsmag-engine/.env'

with open(local_env, 'r', encoding='utf-8') as fh:
    content = fh.read()
with sftp.open(remote_env, 'w') as fh:
    fh.write(content)

print(f"  VPS: Uploaded .env with Pexels API Key")
sftp.close()

_, o, _ = ssh.exec_command('pm2 restart plantsmag-seo 2>&1')
print(f"  PM2: Restarted Engine to apply API key")

ssh.close()
print("\nDone!")
