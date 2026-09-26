import paramiko, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

print("=" * 60)
print("DEPLOY: Gemini API Model Update")
print("=" * 60)

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('72.62.93.117', port=22, username='root', password=r"5KT4'ub5B5oD8V9TB#/u", timeout=20)

sftp = ssh.open_sftp()
local_path = r'd:\project\plantsmag\engine\lib\gemini.js'
remote_path = '/root/plantsmag-engine/lib/gemini.js'

with open(local_path, 'r', encoding='utf-8') as fh:
    content = fh.read()
with sftp.open(remote_path, 'w') as fh:
    fh.write(content)

print(f"  VPS: Uploaded {remote_path}")
sftp.close()

_, o, _ = ssh.exec_command('pm2 restart plantsmag-seo 2>&1')
print(f"  PM2: Restarted Engine to apply model change")

ssh.close()
print("\nDone!")
